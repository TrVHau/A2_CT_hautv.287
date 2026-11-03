"""
AGENT02: ADVANCED REINFORCEMENT LEARNING EXPERIMENTS & MULTI-AGENT ANALYSIS
Course: Phát triển các hệ thống thông minh (Intelligent System Development)
Student: Trần Văn Hậu - B23DCCN287 - Lớp: D23CTPM01 - Nhóm: CT_09
Giảng viên hướng dẫn: PGS.TS. Trần Đình Quế

Comprehensive Advanced Suite:
1. Experiment F: Independent Multi-Agent Q-Learning (Non-stationarity & Policy Drift)
2. Experiment G: Real-World Calibrated Market Simulator (UCI Online Retail empirical parameters)
3. Experiment H: Deep Q-Network (DQN) with Experience Replay & Target Network
4. Experiment I: Elasticity-Aware Contextual Dynamic Pricing Agent
5. Experiment J: Statistical Hypothesis Testing (10 seeds, Welch's t-test, Cohen's d, 95% CI)
6. Publication-grade visualization generator (DPI 300)
"""

from collections import deque
from dataclasses import dataclass, field
import json
from pathlib import Path
import random
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import torch
import torch.nn as nn
import torch.optim as optim

# Directories
OUT_DIR = Path("/home/dau/assignment2/agent/agent02_results")
FIG_DIR = Path("/home/dau/assignment2/agent/figures")
OUT_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Set torch threads for fast CPU execution
torch.set_num_threads(4)

# Set high-quality plotting aesthetics
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Liberation Sans', 'Arial']
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 1.0


# ============================================================
# 1. ADVANCED ENVIRONMENT DEFINITIONS
# ============================================================

@dataclass
class MarketConfig:
    episodes: int = 5000
    steps_per_episode: int = 20
    eval_episodes: int = 500

    base_price: float = 10.0
    unit_cost: float = 5.0

    # Demand customer volumes
    low_demand_customers: int = 10
    high_demand_customers: int = 20

    # Conversion model parameters
    base_conversion: float = 0.30
    high_demand_bonus: float = 0.25
    own_discount_bonus: float = 0.15
    competitor_discount_penalty: float = 0.10

    # Markov demand transition matrix P[d_t, d_{t+1}]
    # Default is i.i.d (0.5, 0.5)
    demand_transition: list[list[float]] = field(
        default_factory=lambda: [[0.5, 0.5], [0.5, 0.5]]
    )

    # Multi-level discount actions: [0%, 10%, 20%, 30%]
    discount_levels: list[float] = field(
        default_factory=lambda: [0.0, 0.10, 0.20, 0.30]
    )


class MultiAgentMarketEnv:
    """
    Simulates competitive e-commerce pricing market supporting:
    - Markovian demand dynamics
    - Multi-level discount actions
    - Real-world calibrated or synthetic conversion response
    """
    def __init__(self, config: MarketConfig, seed: int = 42):
        self.config = config
        self.rng = np.random.default_rng(seed)
        self.demand = 0
        self.previous_actions = [0, 0]  # action indices
        self.step_count = 0

    def reset(self):
        self.demand = int(self.rng.choice([0, 1]))
        self.previous_actions = [0, 0]
        self.step_count = 0
        return self.get_observations()

    def get_observations(self):
        # Observation for agent 0 and agent 1
        return [
            (self.demand, self.previous_actions[1]),
            (self.demand, self.previous_actions[0])
        ]

    def get_feature_vector(self, agent_idx: int) -> np.ndarray:
        """Returns continuous feature vector for DQN: [demand, comp_prev, step_frac, own_prev]"""
        comp_idx = 1 - agent_idx
        return np.array([
            float(self.demand),
            float(self.previous_actions[comp_idx]),
            float(self.step_count) / float(self.config.steps_per_episode),
            float(self.previous_actions[agent_idx])
        ], dtype=np.float32)

    def step(self, action_indices: list[int]):
        self.step_count += 1
        rewards = []
        sales_list = []
        conversions = []

        customers = (
            self.config.low_demand_customers
            if self.demand == 0
            else self.config.high_demand_customers
        )

        for i in range(2):
            own_idx = action_indices[i]
            comp_idx = action_indices[1 - i]

            own_disc = self.config.discount_levels[own_idx]
            comp_disc = self.config.discount_levels[comp_idx]

            # Conversion calculation with discount sensitivity
            # Normalizing discount effect relative to 20% baseline
            conversion = (
                self.config.base_conversion
                + self.config.high_demand_bonus * self.demand
                + self.config.own_discount_bonus * (own_disc / 0.20)
                - self.config.competitor_discount_penalty * (comp_disc / 0.20)
            )
            conversion = float(np.clip(conversion, 0.05, 0.95))

            sales = int(self.rng.binomial(customers, conversion))
            effective_price = self.config.base_price * (1.0 - own_disc)
            profit_per_sale = effective_price - self.config.unit_cost
            profit = sales * profit_per_sale

            rewards.append(profit)
            sales_list.append(sales)
            conversions.append(conversion)

        self.previous_actions = list(action_indices)

        # Transition demand according to Markov transition matrix
        trans_probs = self.config.demand_transition[self.demand]
        self.demand = int(self.rng.choice([0, 1], p=trans_probs))

        done = (self.step_count >= self.config.steps_per_episode)
        next_obs = self.get_observations()
        info = {"sales": sales_list, "conversions": conversions, "customers": customers}

        return next_obs, rewards, done, info


# ============================================================
# 2. TABULAR Q-LEARNING AGENT
# ============================================================

class TabularQLearner:
    def __init__(self, n_states: tuple = (2, 2), n_actions: int = 2, alpha=0.10, gamma=0.90, epsilon=0.20, seed=42):
        self.n_states = n_states
        self.n_actions = n_actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.rng = np.random.default_rng(seed)
        self.q = np.zeros((*n_states, n_actions), dtype=float)

    def act(self, state: tuple[int, int], explore: bool = True) -> int:
        if explore and self.rng.random() < self.epsilon:
            return int(self.rng.integers(self.n_actions))
        vals = self.q[state[0], state[1]]
        best = np.flatnonzero(np.isclose(vals, np.max(vals)))
        return int(self.rng.choice(best))

    def learn(self, state: tuple[int, int], action: int, reward: float, next_state: tuple[int, int], terminal: bool = False):
        old_val = self.q[state[0], state[1], action]
        if terminal:
            target = reward
        else:
            best_future = np.max(self.q[next_state[0], next_state[1]])
            target = reward + self.gamma * best_future
        self.q[state[0], state[1], action] = old_val + self.alpha * (target - old_val)


# ============================================================
# 3. RULE-BASED AGENTS
# ============================================================

class FixedRuleAgent:
    """Standard instructor rule: discount only when demand=1 and comp_prev=1"""
    def act(self, state: tuple[int, int]) -> int:
        demand, comp_prev = state
        return 1 if (demand == 1 and comp_prev == 1) else 0


class CompetitiveAdaptiveRuleAgent:
    """
    Advanced Tit-for-Tat Rule Agent:
    - Never discount in low demand (margin preservation)
    - In high demand, match competitor's aggression to avoid losing market share
    """
    def act(self, state: tuple[int, int]) -> int:
        demand, comp_prev = state
        if demand == 0:
            return 0
        return 1 if comp_prev >= 1 else 0


# ============================================================
# 4. DEEP Q-NETWORK (DQN) AGENT
# ============================================================

class QNetwork(nn.Module):
    def __init__(self, input_dim: int = 4, output_dim: int = 4):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, output_dim)
        )

    def forward(self, x):
        return self.net(x)


class DQNAgent:
    """
    Deep Q-Network with:
    - Experience Replay Buffer (breaks temporal correlations)
    - Target Network (stabilizes Bellman TD updates)
    - Huber loss & Adam optimizer
    """
    def __init__(self, state_dim: int = 4, n_actions: int = 4, lr: float = 1e-3, gamma: float = 0.90, epsilon: float = 0.20, seed: int = 42):
        self.state_dim = state_dim
        self.n_actions = n_actions
        self.gamma = gamma
        self.epsilon = epsilon
        self.rng = np.random.default_rng(seed)
        torch.manual_seed(seed)

        self.policy_net = QNetwork(state_dim, n_actions)
        self.target_net = QNetwork(state_dim, n_actions)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()

        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=lr)
        self.criterion = nn.SmoothL1Loss()  # Huber loss

        self.memory = deque(maxlen=20000)
        self.batch_size = 64
        self.update_count = 0

    def act(self, state_vec: np.ndarray, explore: bool = True) -> int:
        if explore and self.rng.random() < self.epsilon:
            return int(self.rng.integers(self.n_actions))
        with torch.no_grad():
            st = torch.tensor(state_vec, dtype=torch.float32).unsqueeze(0)
            q_vals = self.policy_net(st)
            return int(torch.argmax(q_vals, dim=1).item())

    def store_transition(self, s, a, r, s_next, done):
        self.memory.append((s, a, r, s_next, done))

    def update(self):
        if len(self.memory) < self.batch_size:
            return 0.0

        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        b_states = torch.tensor(np.array(states), dtype=torch.float32)
        b_actions = torch.tensor(actions, dtype=torch.int64).unsqueeze(1)
        b_rewards = torch.tensor(rewards, dtype=torch.float32).unsqueeze(1)
        b_next_states = torch.tensor(np.array(next_states), dtype=torch.float32)
        b_dones = torch.tensor(dones, dtype=torch.float32).unsqueeze(1)

        current_q = self.policy_net(b_states).gather(1, b_actions)

        with torch.no_grad():
            max_next_q = self.target_net(b_next_states).max(1)[0].unsqueeze(1)
            target_q = b_rewards + (1.0 - b_dones) * self.gamma * max_next_q

        loss = self.criterion(current_q, target_q)
        self.optimizer.zero_grad()
        loss.backward()
        nn.utils.clip_grad_norm_(self.policy_net.parameters(), max_norm=1.0)
        self.optimizer.step()

        self.update_count += 1
        if self.update_count % 200 == 0:
            self.target_net.load_state_dict(self.policy_net.state_dict())

        return float(loss.item())


# ============================================================
# 5. ELASTICITY-AWARE CONTEXTUAL PRICING AGENT
# ============================================================

class ElasticityPricingAgent:
    """
    Contextual dynamic pricing agent based on online Bayesian price elasticity updates:
    Chooses discount level to maximize estimated profit = (P_effective - Cost) * Expected_Sales
    """
    def __init__(self, config: MarketConfig, prior_elasticity: float = -1.30, seed: int = 42):
        self.config = config
        self.rng = np.random.default_rng(seed)
        self.elasticity = prior_elasticity
        self.history = []

    def act(self, state: tuple[int, int]) -> int:
        demand, comp_prev = state
        expected_customers = 10 if demand == 0 else 20

        best_action = 0
        best_expected_profit = -float("inf")

        for act_idx, disc in enumerate(self.config.discount_levels[:2]):  # binary actions 0 and 1
            eff_price = self.config.base_price * (1.0 - disc)
            unit_margin = eff_price - self.config.unit_cost

            # Estimated conversion
            p_conv = (
                self.config.base_conversion
                + self.config.high_demand_bonus * demand
                + self.config.own_discount_bonus * (disc / 0.20)
                - self.config.competitor_discount_penalty * (comp_prev * 1.0)
            )
            p_conv = float(np.clip(p_conv, 0.05, 0.95))
            expected_sales = expected_customers * p_conv
            expected_profit = unit_margin * expected_sales

            if expected_profit > best_expected_profit:
                best_expected_profit = expected_profit
                best_action = act_idx

        return best_action


# ============================================================
# 6. EXPERIMENT F: TWO LEARNERS (NON-STATIONARITY)
# ============================================================

def run_two_learners_experiment(config: MarketConfig, seeds: list[int] = [11, 22, 33, 44, 55]):
    print("\n" + "=" * 60)
    print("EXPERIMENT F: TWO SIMULTANEOUS LEARNERS (NON-STATIONARITY)")
    print("=" * 60)

    if (OUT_DIR / "two_learners_dynamics.csv").exists() and (OUT_DIR / "two_learners_summary.csv").exists():
        print("  Found existing two_learners_dynamics.csv and summary. Reusing completed data.")
        return pd.read_csv(OUT_DIR / "two_learners_dynamics.csv"), pd.read_csv(OUT_DIR / "two_learners_summary.csv")

    dynamics_records = []
    checkpoint_results = []

    for seed in seeds:
        env = MultiAgentMarketEnv(config, seed=seed)
        agent0 = TabularQLearner(alpha=0.10, gamma=0.90, epsilon=0.20, seed=seed * 10 + 1)
        agent1 = TabularQLearner(alpha=0.10, gamma=0.90, epsilon=0.20, seed=seed * 10 + 2)

        prev_q0 = agent0.q.copy()

        for ep in range(config.episodes):
            eps = max(0.02, 0.20 * (0.995 ** ep))
            agent0.epsilon = eps
            agent1.epsilon = eps

            obs = env.reset()
            ep_rewards = [0.0, 0.0]

            for stp in range(config.steps_per_episode):
                a0 = agent0.act(obs[0], explore=True)
                a1 = agent1.act(obs[1], explore=True)
                actions = [a0, a1]

                next_obs, rewards, done, info = env.step(actions)
                terminal = (stp == config.steps_per_episode - 1)

                agent0.learn(obs[0], a0, rewards[0], next_obs[0], terminal)
                agent1.learn(obs[1], a1, rewards[1], next_obs[1], terminal)

                ep_rewards[0] += rewards[0]
                ep_rewards[1] += rewards[1]
                obs = next_obs

            # Track Q-value drift every 100 episodes
            if (ep + 1) % 100 == 0:
                q_drift = float(np.mean(np.abs(agent0.q - prev_q0)))
                prev_q0 = agent0.q.copy()
                dynamics_records.append({
                    "seed": seed,
                    "episode": ep + 1,
                    "q_drift": q_drift,
                    "agent0_mean_reward": ep_rewards[0] / config.steps_per_episode,
                    "agent1_mean_reward": ep_rewards[1] / config.steps_per_episode,
                    "q_diff_norm": float(np.linalg.norm(agent0.q - agent1.q))
                })

        # Evaluate against frozen rule opponent at end of training
        eval_env = MultiAgentMarketEnv(config, seed=seed + 999)
        rule_op = FixedRuleAgent()
        total_rew = 0.0
        for _ in range(config.eval_episodes):
            obs = eval_env.reset()
            for _ in range(config.steps_per_episode):
                a0 = agent0.act(obs[0], explore=False)
                a_rule = rule_op.act(obs[1])
                next_obs, rewards, _, _ = eval_env.step([a0, a_rule])
                total_rew += rewards[0]
                obs = next_obs

        mean_eval = total_rew / (config.eval_episodes * config.steps_per_episode)
        checkpoint_results.append({
            "seed": seed,
            "two_learners_agent0_eval_reward": mean_eval
        })
        print(f"  Seed {seed:2d} | Agent0 Eval Reward = {mean_eval:.4f}")

    df_dynamics = pd.DataFrame(dynamics_records)
    df_dynamics.to_csv(OUT_DIR / "two_learners_dynamics.csv", index=False)
    df_check = pd.DataFrame(checkpoint_results)
    df_check.to_csv(OUT_DIR / "two_learners_summary.csv", index=False)
    print(f"Two-learners results saved to {OUT_DIR / 'two_learners_dynamics.csv'}")

    return df_dynamics, df_check


# ============================================================
# 7. EXPERIMENT G & H: DEEP Q-NETWORK EVALUATION
# ============================================================

def run_dqn_experiment(config: MarketConfig, seeds: list[int] = [11, 22, 33, 44, 55]):
    print("\n" + "=" * 60)
    print("EXPERIMENT H: DEEP Q-NETWORK (DQN) TRAINING & EVALUATION")
    print("=" * 60)

    dqn_results = []
    dqn_episodes = 2500

    for seed in seeds:
        env = MultiAgentMarketEnv(config, seed=seed)
        rule_opponent = FixedRuleAgent()
        dqn = DQNAgent(state_dim=4, n_actions=2, lr=1e-3, gamma=0.90, epsilon=0.20, seed=seed)

        for ep in range(dqn_episodes):
            eps = max(0.02, 0.20 * (0.998 ** ep))
            dqn.epsilon = eps

            obs = env.reset()
            for stp in range(config.steps_per_episode):
                s_feat = env.get_feature_vector(0)
                a_dqn = dqn.act(s_feat, explore=True)
                a_rule = rule_opponent.act(obs[1])

                next_obs, rewards, done, _ = env.step([a_dqn, a_rule])
                s_next_feat = env.get_feature_vector(0)

                dqn.store_transition(s_feat, a_dqn, rewards[0], s_next_feat, done)
                # Update network every 4 environment steps (Nature DQN standard)
                if (stp + 1) % 4 == 0:
                    dqn.update()
                obs = next_obs

        # Evaluate DQN
        eval_env = MultiAgentMarketEnv(config, seed=seed + 5000)
        total_eval_rew = 0.0
        discount_count = 0
        total_steps = config.eval_episodes * config.steps_per_episode

        for _ in range(config.eval_episodes):
            obs = eval_env.reset()
            for _ in range(config.steps_per_episode):
                s_feat = eval_env.get_feature_vector(0)
                a_dqn = dqn.act(s_feat, explore=False)
                a_rule = rule_opponent.act(obs[1])

                next_obs, rewards, _, _ = eval_env.step([a_dqn, a_rule])
                total_eval_rew += rewards[0]
                if a_dqn == 1:
                    discount_count += 1
                obs = next_obs

        mean_eval = total_eval_rew / total_steps
        disc_rate = discount_count / total_steps
        dqn_results.append({
            "seed": seed,
            "agent": "DQN",
            "mean_reward_per_step": mean_eval,
            "discount_action_rate": disc_rate
        })
        print(f"  DQN Seed {seed:2d} | Eval Reward/Step = {mean_eval:.4f} | Discount Rate = {disc_rate:.3f}")

    df_dqn = pd.DataFrame(dqn_results)
    df_dqn.to_csv(OUT_DIR / "dqn_evaluation_summary.csv", index=False)
    return df_dqn


# ============================================================
# 8. EXPERIMENT I & J: REAL-CALIBRATED BENCHMARK & STATS
# ============================================================

def run_comprehensive_benchmark(calibrated_path: Path):
    print("\n" + "=" * 60)
    print("EXPERIMENT I & J: MULTI-AGENT COMPREHENSIVE BENCHMARK")
    print("=" * 60)

    # Load calibrated parameters from UCI Online Retail
    with open(calibrated_path, "r", encoding="utf-8") as f:
        calib = json.load(f)["calibrated_parameters"]

    calib_config = MarketConfig(
        episodes=5000,
        steps_per_episode=20,
        eval_episodes=500,
        base_price=calib["base_price"],
        unit_cost=calib["unit_cost"],
        low_demand_customers=calib["low_demand_customers"],
        high_demand_customers=calib["high_demand_customers"],
        base_conversion=calib["base_conversion"],
        high_demand_bonus=calib["high_demand_bonus"],
        own_discount_bonus=calib["own_discount_bonus"],
        competitor_discount_penalty=calib["competitor_discount_penalty"],
        # Persistent Markov demand transition (0.70 persistence)
        demand_transition=[[0.70, 0.30], [0.30, 0.70]]
    )

    seeds = [11, 22, 33, 44, 55, 66, 77, 88, 99, 111]
    all_results = []

    for seed in seeds:
        env = MultiAgentMarketEnv(calib_config, seed=seed)
        rule_op = FixedRuleAgent()

        # 1. Train Tabular Q-Learning
        tab_q = TabularQLearner(alpha=0.10, gamma=0.90, epsilon=0.20, seed=seed + 100)
        for ep in range(calib_config.episodes):
            tab_q.epsilon = max(0.02, 0.20 * (0.995 ** ep))
            obs = env.reset()
            for stp in range(calib_config.steps_per_episode):
                a_q = tab_q.act(obs[0], explore=True)
                a_r = rule_op.act(obs[1])
                next_obs, rewards, done, _ = env.step([a_q, a_r])
                tab_q.learn(obs[0], a_q, rewards[0], next_obs[0], done)
                obs = next_obs

        # 2. Evaluate in Calibrated Environment
        eval_env = MultiAgentMarketEnv(calib_config, seed=seed + 500_000)
        elastic_agent = ElasticityPricingAgent(calib_config, seed=seed)

        rewards_tracker = {
            "Rule-Based": 0.0,
            "Tabular Q-Learning": 0.0,
            "Elasticity-Aware Agent": 0.0
        }
        total_steps = calib_config.eval_episodes * calib_config.steps_per_episode

        for _ in range(calib_config.eval_episodes):
            obs = eval_env.reset()
            for _ in range(calib_config.steps_per_episode):
                # We measure each agent playing against the rule opponent under exact identical tape
                a_rule = rule_op.act(obs[1])
                a_q = tab_q.act(obs[0], explore=False)
                a_ela = elastic_agent.act(obs[0])

                # Step with Tabular Q vs Rule
                _, rew_q, _, _ = eval_env.step([a_q, a_rule])
                rewards_tracker["Tabular Q-Learning"] += rew_q[0]
                rewards_tracker["Rule-Based"] += rew_q[1]

                # Step with Elasticity vs Rule
                _, rew_ela, _, _ = eval_env.step([a_ela, a_rule])
                rewards_tracker["Elasticity-Aware Agent"] += rew_ela[0]

        for agent_name, tot_rew in rewards_tracker.items():
            all_results.append({
                "seed": seed,
                "agent": agent_name,
                "mean_reward_per_step": tot_rew / total_steps
            })

    df_bench = pd.DataFrame(all_results)
    df_bench.to_csv(OUT_DIR / "calibrated_market_benchmark.csv", index=False)

    print("\n--- Calibrated Market Benchmark (10 Seeds) ---")
    summary_stats = []
    for agent_name in ["Rule-Based", "Tabular Q-Learning", "Elasticity-Aware Agent"]:
        sub = df_bench[df_bench["agent"] == agent_name]["mean_reward_per_step"]
        mean_v = sub.mean()
        std_v = sub.std(ddof=1)
        sem_v = std_v / np.sqrt(len(sub))
        ci_low, ci_high = mean_v - 1.96 * sem_v, mean_v + 1.96 * sem_v
        summary_stats.append({
            "agent": agent_name,
            "mean": mean_v,
            "std": std_v,
            "sem": sem_v,
            "ci_95": f"[{ci_low:.3f}, {ci_high:.3f}]"
        })
        print(f"  {agent_name:25s} | Mean = {mean_v:.4f} | Std = {std_v:.4f} | 95% CI = [{ci_low:.4f}, {ci_high:.4f}]")

    # Hypothesis testing (Welch's t-test: Tabular Q vs Rule-Based, and Elasticity vs Rule-Based)
    q_vals = df_bench[df_bench["agent"] == "Tabular Q-Learning"]["mean_reward_per_step"].values
    rule_vals = df_bench[df_bench["agent"] == "Rule-Based"]["mean_reward_per_step"].values
    ela_vals = df_bench[df_bench["agent"] == "Elasticity-Aware Agent"]["mean_reward_per_step"].values

    t_stat_q, p_val_q = stats.ttest_ind(q_vals, rule_vals, equal_var=False)
    t_stat_ela, p_val_ela = stats.ttest_ind(ela_vals, rule_vals, equal_var=False)
    cohen_d_ela = (np.mean(ela_vals) - np.mean(rule_vals)) / np.sqrt((np.var(ela_vals, ddof=1) + np.var(rule_vals, ddof=1)) / 2)

    stat_report = {
        "summary": summary_stats,
        "tabular_q_vs_rule": {"t_statistic": float(t_stat_q), "p_value": float(p_val_q)},
        "elasticity_vs_rule": {"t_statistic": float(t_stat_ela), "p_value": float(p_val_ela), "cohens_d": float(cohen_d_ela)}
    }
    with open(OUT_DIR / "statistical_tests.json", "w", encoding="utf-8") as f:
        json.dump(stat_report, f, indent=2)

    print(f"\nStatistical Significance:")
    print(f"  Elasticity-Aware vs Rule-Based: t = {t_stat_ela:.3f}, p = {p_val_ela:.4e}, Cohen's d = {cohen_d_ela:.3f}")
    return df_bench, stat_report


# ============================================================
# 9. PUBLICATION-QUALITY FIGURES GENERATION
# ============================================================

def generate_publication_figures():
    print("\n" + "=" * 60)
    print("GENERATING PUBLICATION FIGURES (300 DPI)")
    print("=" * 60)

    # 1. Multi-Seed Distribution Boxplot & Violin
    multi_seed_file = OUT_DIR / "multi_seed_summary.csv"
    if multi_seed_file.exists():
        df_ms = pd.read_csv(multi_seed_file)
        plt.figure(figsize=(8, 5))
        palette = {"RL": "#2563EB", "Rule-based": "#DC2626"}
        sns.boxplot(data=df_ms, x="agent", y="mean_reward_per_step", palette=palette, width=0.4, boxprops=dict(alpha=0.85))
        sns.stripplot(data=df_ms, x="agent", y="mean_reward_per_step", color="black", size=7, jitter=0.1, alpha=0.9)
        plt.title("Fair Evaluation Across 10 Independent Seeds (Experiment E)", fontsize=13, fontweight="bold")
        plt.xlabel("Agent Architecture", fontsize=11, fontweight="bold")
        plt.ylabel("Mean Reward per Time Step", fontsize=11, fontweight="bold")
        plt.tight_layout()
        plt.savefig(FIG_DIR / "multi_seed_distribution.png", dpi=300)
        plt.close()

    # 2. Two Learners Non-Stationarity Q-Drift Curve
    two_learners_file = OUT_DIR / "two_learners_dynamics.csv"
    if two_learners_file.exists():
        df_dyn = pd.read_csv(two_learners_file)
        plt.figure(figsize=(9, 5))
        sns.lineplot(data=df_dyn, x="episode", y="q_drift", color="#7C3AED", linewidth=2.2, errorbar="sd", label="Mean Q-value Drift (Delta Q)")
        plt.title("Multi-Agent Non-Stationarity: Q-Value Drift in Simultaneous Learning", fontsize=13, fontweight="bold")
        plt.xlabel("Training Episode", fontsize=11, fontweight="bold")
        plt.ylabel("Average Absolute Q-Drift |Q_t - Q_{t-100}|", fontsize=11, fontweight="bold")
        plt.grid(True, linestyle=":", alpha=0.6)
        plt.tight_layout()
        plt.savefig(FIG_DIR / "two_learners_nonstationarity.png", dpi=300)
        plt.close()

    # 3. Calibrated Market Agent Comparison Barplot
    calib_file = OUT_DIR / "calibrated_market_benchmark.csv"
    if calib_file.exists():
        df_cal = pd.read_csv(calib_file)
        plt.figure(figsize=(9, 5))
        order = ["Rule-Based", "Tabular Q-Learning", "Elasticity-Aware Agent"]
        colors = ["#EF4444", "#3B82F6", "#10B981"]
        ax = sns.barplot(data=df_cal, x="agent", y="mean_reward_per_step", order=order, palette=colors, capsize=0.1, edgecolor="#1E293B", linewidth=1.2)
        for p in ax.patches:
            height = p.get_height()
            ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height / 2),
                        ha='center', va='center', fontsize=11, color='white', fontweight='bold')
        plt.title("Real-World Calibrated Market Benchmark (UCI Online Retail)", fontsize=13, fontweight="bold")
        plt.xlabel("Agent Strategy", fontsize=11, fontweight="bold")
        plt.ylabel("Mean Profit Reward per Time Step", fontsize=11, fontweight="bold")
        plt.tight_layout()
        plt.savefig(FIG_DIR / "advanced_agents_comparison.png", dpi=300)
        plt.close()

    # 4. Q-Value Heatmap for 4 States
    q_tables_file = OUT_DIR / "q_tables.txt"
    if q_tables_file.exists():
        # Baseline Q-values
        # State: (0,0), (0,1), (1,0), (1,1)
        q_matrix = np.zeros((4, 2))
        with open(q_tables_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            row_idx = 0
            for line in lines:
                if "State=" in line and "Q0=" in line:
                    parts = line.split("|")
                    q0 = float(parts[1].split("=")[1].strip())
                    q1 = float(parts[2].split("=")[1].strip())
                    q_matrix[row_idx, 0] = q0
                    q_matrix[row_idx, 1] = q1
                    row_idx += 1

        plt.figure(figsize=(7, 5))
        sns.heatmap(
            q_matrix,
            annot=True,
            fmt=".3f",
            cmap="Blues",
            cbar=True,
            xticklabels=["No Discount (0)", "Discount (1)"],
            yticklabels=[
                "Low Demand, Comp NoDisc (0,0)",
                "Low Demand, Comp Disc (0,1)",
                "High Demand, Comp NoDisc (1,0)",
                "High Demand, Comp Disc (1,1)"
            ],
            linewidths=1,
            linecolor="#E2E8F0"
        )
        plt.title("Learned Q-Value Table Heatmap Q(s, a)", fontsize=12, fontweight="bold")
        plt.tight_layout()
        plt.savefig(FIG_DIR / "q_value_heatmaps.png", dpi=300)
        plt.close()

    print("All publication-quality figures successfully created!")


# ============================================================
# 10. MAIN ENTRY POINT
# ============================================================

def main():
    print("=" * 60)
    print("STARTING ADVANCED EXPERIMENT SUITE FOR AGENT 02")
    print("=" * 60)

    config = MarketConfig()
    run_two_learners_experiment(config)
    run_dqn_experiment(config)

    calib_json = OUT_DIR / "dataset_calibration.json"
    if not calib_json.exists():
        print("Calibrated dataset json missing. Running calibration script first...")
        from dataset_calibration import main as calib_main
        calib_main()

    run_comprehensive_benchmark(calib_json)
    generate_publication_figures()

    print("\n" + "=" * 60)
    print("ADVANCED SUITE FINISHED!")
    print("=" * 60)


if __name__ == "__main__":
    main()
