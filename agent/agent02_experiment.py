"""
AGENT02: Reinforcement-Learning-Based Agent vs Rule-Based Agent
Course: Phát triển các hệ thống thông minh (Intelligent System Development)
Academic Year: 2026-2027
Student: Trần Văn Hậu - B23DCCN287 - Lớp: D23CTPM01 - Nhóm: CT_09
Giảng viên hướng dẫn: PGS.TS. Trần Đình Quế

Baseline Implementation compliant with instructor requirements:
- Q-learning tabular agent
- Rule-based agent
- Experiments A, B, C, D, E
"""

from dataclasses import dataclass
from pathlib import Path
import csv
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 1. CONFIGURATION
# ============================================================

@dataclass
class Config:
    episodes: int = 5000
    steps_per_episode: int = 20

    alpha: float = 0.10
    gamma: float = 0.90

    epsilon_start: float = 0.20
    epsilon_min: float = 0.02
    epsilon_decay: float = 0.995

    price: float = 10.0
    unit_cost: float = 5.0
    discount_rate: float = 0.20

    low_demand_customers: int = 10
    high_demand_customers: int = 20

    seed: int = 42
    evaluation_episodes: int = 500

    output_dir: str = "agent02_results"


State = tuple[int, int]


# ============================================================
# 2. E-COMMERCE ENVIRONMENT
# ============================================================

class ECommerceEnvironment:
    """
    Two agents compete in a simplified e-commerce market.

    State:
        (demand, competitor_previous_action)
        demand: 0 = low demand (10 customers), 1 = high demand (20 customers)
        competitor_previous_action: 0 = no discount, 1 = discount

    Action:
        0 = no discount
        1 = discount (20% off)

    Reward:
        Profit = sales * profit_per_sale
    """

    def __init__(self, config: Config, seed: int = None):
        self.config = config
        actual_seed = config.seed if seed is None else seed
        self.rng = np.random.default_rng(actual_seed)

        self.demand = 0
        self.previous_actions = [0, 0]

    def reset(self):
        self.demand = int(self.rng.integers(0, 2))
        self.previous_actions = [0, 0]
        return self.get_states()

    def get_states(self):
        return [
            (self.demand, self.previous_actions[1]),
            (self.demand, self.previous_actions[0])
        ]

    def step(self, actions: list[int]):
        if len(actions) != 2:
            raise ValueError("Exactly two actions are required.")

        if any(action not in (0, 1) for action in actions):
            raise ValueError("Actions must be 0 or 1.")

        rewards = []
        sales_list = []
        conversion_list = []

        if self.demand == 0:
            customers = self.config.low_demand_customers
        else:
            customers = self.config.high_demand_customers

        # Both actions are selected simultaneously before this function is called.
        for i in range(2):
            own_action = actions[i]
            competitor_action = actions[1 - i]

            # Conversion probability formula
            conversion = (
                0.30
                + 0.25 * self.demand
                + 0.15 * own_action
                - 0.10 * competitor_action
            )

            conversion = float(np.clip(conversion, 0.05, 0.95))

            # Stochastic binomial sales
            sales = int(self.rng.binomial(customers, conversion))

            # Effective price after discount
            effective_price = self.config.price * (
                1.0 - self.config.discount_rate * own_action
            )

            profit_per_sale = effective_price - self.config.unit_cost
            profit = sales * profit_per_sale

            rewards.append(float(profit))
            sales_list.append(sales)
            conversion_list.append(conversion)

        # Update previous actions for next step observation
        self.previous_actions = list(actions)

        # Demand evolves independently (i.i.d Bernoulli(0.5))
        self.demand = int(self.rng.integers(0, 2))

        next_states = self.get_states()

        info = {
            "sales": sales_list,
            "conversion": conversion_list,
            "customers": customers
        }

        return next_states, rewards, info


# ============================================================
# 3. REINFORCEMENT-LEARNING-BASED AGENT (TABULAR Q-LEARNING)
# ============================================================

class QLearningAgent:
    """
    Tabular Q-learning agent.
    Q[demand, competitor_previous_action, action]
    Total states = 2 * 2 = 4; Total state-action pairs = 4 * 2 = 8
    """

    def __init__(
        self,
        alpha: float = 0.10,
        gamma: float = 0.90,
        epsilon: float = 0.20,
        seed: int = 123
    ):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

        self.rng = np.random.default_rng(seed)
        self.q = np.zeros((2, 2, 2), dtype=float)

    def act(self, state: State, explore: bool = True) -> int:
        demand, competitor_previous_action = state

        # Exploration branch
        if explore and self.rng.random() < self.epsilon:
            return int(self.rng.integers(0, 2))

        # Exploitation branch (greedy with tie-breaking)
        values = self.q[demand, competitor_previous_action]
        best_actions = np.flatnonzero(np.isclose(values, np.max(values)))
        return int(self.rng.choice(best_actions))

    def learn(
        self,
        state: State,
        action: int,
        reward: float,
        next_state: State,
        terminal: bool = False
    ):
        demand, competitor_previous_action = state
        next_demand, next_competitor_action = next_state

        old_value = self.q[demand, competitor_previous_action, action]

        if terminal:
            target = reward
        else:
            best_future_value = np.max(
                self.q[next_demand, next_competitor_action]
            )
            target = reward + self.gamma * best_future_value

        # Q-learning TD update
        self.q[demand, competitor_previous_action, action] = old_value + self.alpha * (
            target - old_value
        )

    def greedy_policy(self) -> dict:
        policy = {}
        for demand in range(2):
            for competitor_action in range(2):
                state = (demand, competitor_action)
                policy[state] = int(np.argmax(self.q[demand, competitor_action]))
        return policy


# ============================================================
# 4. RULE-BASED AGENT
# ============================================================

class RuleBasedAgent:
    """
    Hand-crafted expert rule:
    Rule 1: Low demand -> No discount (0)
    Rule 2: High demand & competitor discounted previously -> Discount (1)
    Rule 3: High demand & competitor did not discount -> No discount (0)
    """

    def act(self, state: State) -> int:
        demand, competitor_previous_action = state
        if demand == 0:
            return 0
        elif demand == 1 and competitor_previous_action == 1:
            return 1
        else:
            return 0


# ============================================================
# 5. TRAINING ROUTINES
# ============================================================

def train_rl_against_rule(
    config: Config,
    seed: int,
    alpha: float = None,
    epsilon_start: float = None,
    epsilon_min: float = None,
    epsilon_decay: float = None
):
    alpha = config.alpha if alpha is None else alpha
    epsilon_start = config.epsilon_start if epsilon_start is None else epsilon_start
    epsilon_min = config.epsilon_min if epsilon_min is None else epsilon_min
    epsilon_decay = config.epsilon_decay if epsilon_decay is None else epsilon_decay

    env = ECommerceEnvironment(config, seed=seed)
    rl_agent = QLearningAgent(
        alpha=alpha,
        gamma=config.gamma,
        epsilon=epsilon_start,
        seed=seed + 10_000
    )
    rule_agent = RuleBasedAgent()

    episode_results = []

    for episode in range(config.episodes):
        # Epsilon decay
        rl_agent.epsilon = max(
            epsilon_min,
            epsilon_start * (epsilon_decay ** episode)
        )

        states = env.reset()
        episode_rewards = [0.0, 0.0]

        for step in range(config.steps_per_episode):
            rl_action = rl_agent.act(states[0], explore=True)
            rule_action = rule_agent.act(states[1])
            actions = [rl_action, rule_action]

            next_states, rewards, info = env.step(actions)
            terminal = (step == config.steps_per_episode - 1)

            rl_agent.learn(
                state=states[0],
                action=rl_action,
                reward=rewards[0],
                next_state=next_states[0],
                terminal=terminal
            )

            episode_rewards[0] += rewards[0]
            episode_rewards[1] += rewards[1]
            states = next_states

        episode_results.append({
            "episode": episode + 1,
            "rl_episode_reward": episode_rewards[0],
            "rule_episode_reward": episode_rewards[1],
            "rl_mean_reward_per_step": episode_rewards[0] / config.steps_per_episode,
            "rule_mean_reward_per_step": episode_rewards[1] / config.steps_per_episode,
            "epsilon": rl_agent.epsilon,
            "alpha": alpha
        })

    return rl_agent, episode_results


# ============================================================
# 6. SEPARATE FAIR POLICY EVALUATION
# ============================================================

def evaluate_pair(
    config: Config,
    rl_agent: QLearningAgent,
    episodes: int = None,
    seed: int = 900_000
):
    if episodes is None:
        episodes = config.evaluation_episodes

    env = ECommerceEnvironment(config, seed=seed)
    rule_agent = RuleBasedAgent()

    total_rewards = np.zeros(2, dtype=float)
    action_counts = np.zeros((2, 2), dtype=int)
    episode_results = []

    for episode in range(episodes):
        states = env.reset()
        rewards_this_episode = [0.0, 0.0]

        for _ in range(config.steps_per_episode):
            # Greedy evaluation: exploration strictly disabled
            rl_action = rl_agent.act(states[0], explore=False)
            rule_action = rule_agent.act(states[1])
            actions = [rl_action, rule_action]

            next_states, rewards, info = env.step(actions)

            for i in range(2):
                total_rewards[i] += rewards[i]
                rewards_this_episode[i] += rewards[i]
                action_counts[i, actions[i]] += 1

            states = next_states

        episode_results.append({
            "episode": episode + 1,
            "rl_reward": rewards_this_episode[0],
            "rule_reward": rewards_this_episode[1],
            "rl_mean_reward_per_step": rewards_this_episode[0] / config.steps_per_episode,
            "rule_mean_reward_per_step": rewards_this_episode[1] / config.steps_per_episode
        })

    total_steps = episodes * config.steps_per_episode
    summary = []

    for i, name in enumerate(["RL", "Rule-based"]):
        summary.append({
            "agent": name,
            "total_reward": total_rewards[i],
            "mean_reward_per_step": total_rewards[i] / total_steps,
            "no_discount_actions": int(action_counts[i, 0]),
            "discount_actions": int(action_counts[i, 1]),
            "discount_action_rate": action_counts[i, 1] / total_steps
        })

    return summary, episode_results


# ============================================================
# 7. HELPERS: CSV & PLOTS
# ============================================================

def write_csv(filepath: Path, rows: list[dict]):
    if not rows:
        return
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def save_q_table(filepath: Path, agent: QLearningAgent):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("Q-table: Q[demand, competitor_previous_action, action]\n")
        f.write("Action 0 = no discount; Action 1 = discount\n\n")
        for demand in range(2):
            for comp_act in range(2):
                q0 = agent.q[demand, comp_act, 0]
                q1 = agent.q[demand, comp_act, 1]
                best = int(np.argmax(agent.q[demand, comp_act]))
                f.write(
                    f"State=({demand}, {comp_act}) | "
                    f"Q0={q0:.6f} | Q1={q1:.6f} | "
                    f"Greedy action={best} ({'DISCOUNT' if best==1 else 'NO DISCOUNT'})\n"
                )


def moving_average(values: list[float], window: int = 100) -> np.ndarray:
    arr = np.asarray(values, dtype=float)
    if len(arr) < window:
        return arr
    kernel = np.ones(window) / window
    return np.convolve(arr, kernel, mode="valid")


def plot_training_rewards(rows: list[dict], filepath: Path):
    episodes = [row["episode"] for row in rows]
    rl_rewards = [row["rl_mean_reward_per_step"] for row in rows]
    rule_rewards = [row["rule_mean_reward_per_step"] for row in rows]

    plt.figure(figsize=(10, 6))
    plt.plot(episodes, rl_rewards, alpha=0.15, color="#2563EB", label="RL step reward")
    plt.plot(episodes, rule_rewards, alpha=0.15, color="#DC2626", label="Rule step reward")

    window = 100
    if len(rows) >= window:
        ma_rl = moving_average(rl_rewards, window)
        ma_rule = moving_average(rule_rewards, window)
        plt.plot(episodes[window - 1:], ma_rl, linewidth=2.2, color="#1D4ED8", label=f"RL Moving Avg ({window})")
        plt.plot(episodes[window - 1:], ma_rule, linewidth=2.2, color="#B91C1C", linestyle="--", label=f"Rule Moving Avg ({window})")

    plt.xlabel("Training Episode", fontsize=11, fontweight="bold")
    plt.ylabel("Mean Reward per Step", fontsize=11, fontweight="bold")
    plt.title("Experiment B: RL Training Dynamics vs Rule-Based Opponent", fontsize=13, fontweight="bold")
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(frameon=True, facecolor="white", framealpha=0.9)
    plt.tight_layout()
    plt.savefig(filepath, dpi=300)
    plt.close()


def plot_bar_comparison(rows: list[dict], label_key: str, value_key: str, filepath: Path, title: str):
    labels = [str(r[label_key]) for r in rows]
    values = [r[value_key] for r in rows]

    plt.figure(figsize=(8, 5))
    bars = plt.bar(labels, values, color="#3B82F6", edgecolor="#1D4ED8", width=0.5)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.3, f"{yval:.3f}", ha='center', va='bottom', fontweight='bold', fontsize=10)

    plt.xlabel(label_key.replace("_", " ").title(), fontsize=11, fontweight="bold")
    plt.ylabel(value_key.replace("_", " ").title(), fontsize=11, fontweight="bold")
    plt.title(title, fontsize=12, fontweight="bold")
    plt.grid(axis="y", linestyle=":", alpha=0.6)
    plt.ylim(0, max(values) * 1.15)
    plt.tight_layout()
    plt.savefig(filepath, dpi=300)
    plt.close()


# ============================================================
# 8. EXPERIMENT SUITE
# ============================================================

def run_baseline(config: Config, output_dir: Path):
    print("\n" + "=" * 60)
    print("EXPERIMENT 1: BASELINE (Experiment A & B)")
    print("=" * 60)

    agent, training_rows = train_rl_against_rule(config, seed=config.seed)

    write_csv(output_dir / "baseline_episode_rewards.csv", training_rows)
    save_q_table(output_dir / "q_tables.txt", agent)
    plot_training_rewards(training_rows, output_dir / "episode_rewards.png")

    summary, eval_rows = evaluate_pair(
        config,
        agent,
        episodes=config.evaluation_episodes,
        seed=config.seed + 500_000
    )

    write_csv(output_dir / "baseline_evaluation.csv", summary)
    write_csv(output_dir / "baseline_evaluation_episodes.csv", eval_rows)

    print("\nSeparate Evaluation Results:")
    for row in summary:
        print(f"  {row['agent']:12s} | Mean Reward/Step = {row['mean_reward_per_step']:.4f} | Discount Rate = {row['discount_action_rate']:.3f}")

    print("\nLearned Greedy Policy:")
    for state, act in agent.greedy_policy().items():
        print(f"  State {state}: {'DISCOUNT (1)' if act==1 else 'NO DISCOUNT (0)'}")

    return agent


def run_learning_rate_experiment(config: Config, output_dir: Path):
    print("\n" + "=" * 60)
    print("EXPERIMENT 2: LEARNING RATE (Experiment C)")
    print("=" * 60)

    results = []
    for alpha in [0.01, 0.10, 0.50]:
        agent, _ = train_rl_against_rule(
            config,
            seed=config.seed + 1000,
            alpha=alpha
        )
        summary, _ = evaluate_pair(
            config,
            agent,
            episodes=config.evaluation_episodes,
            seed=config.seed + 600_000
        )
        rl_res = next(r for r in summary if r["agent"] == "RL")
        results.append({
            "alpha": alpha,
            "rl_mean_reward_per_step": rl_res["mean_reward_per_step"],
            "rl_discount_action_rate": rl_res["discount_action_rate"]
        })
        print(f"  alpha = {alpha:4.2f} | Eval Reward/Step = {rl_res['mean_reward_per_step']:.4f}")

    write_csv(output_dir / "learning_rate_comparison.csv", results)
    plot_bar_comparison(
        results,
        "alpha",
        "rl_mean_reward_per_step",
        output_dir / "learning_rate_comparison.png",
        "Experiment C: Impact of Learning Rate (alpha) on Final Evaluation Reward"
    )
    return results


def run_exploration_experiment(config: Config, output_dir: Path):
    print("\n" + "=" * 60)
    print("EXPERIMENT 3: EXPLORATION (Experiment D)")
    print("=" * 60)

    settings = [
        ("low", 0.05, 0.02, 0.999),
        ("baseline", 0.20, 0.02, 0.995),
        ("high", 0.50, 0.05, 0.995),
        ("fixed_0.05", 0.05, 0.05, 1.000),
        ("fixed_0.30", 0.30, 0.30, 1.000),
    ]

    results = []
    for name, eps_start, eps_min, eps_decay in settings:
        agent, _ = train_rl_against_rule(
            config,
            seed=config.seed + 2000,
            epsilon_start=eps_start,
            epsilon_min=eps_min,
            epsilon_decay=eps_decay
        )
        summary, _ = evaluate_pair(
            config,
            agent,
            episodes=config.evaluation_episodes,
            seed=config.seed + 700_000
        )
        rl_res = next(r for r in summary if r["agent"] == "RL")
        results.append({
            "exploration_setting": name,
            "epsilon_start": eps_start,
            "epsilon_min": eps_min,
            "epsilon_decay": eps_decay,
            "rl_mean_reward_per_step": rl_res["mean_reward_per_step"],
            "rl_discount_action_rate": rl_res["discount_action_rate"]
        })
        print(f"  {name:12s} | Eval Reward/Step = {rl_res['mean_reward_per_step']:.4f}")

    write_csv(output_dir / "exploration_comparison.csv", results)
    plot_bar_comparison(
        results,
        "exploration_setting",
        "rl_mean_reward_per_step",
        output_dir / "exploration_comparison.png",
        "Experiment D: Effect of Exploration Strategy on Policy Quality"
    )
    return results


def run_multi_seed_experiment(config: Config, output_dir: Path):
    print("\n" + "=" * 60)
    print("EXPERIMENT 4: MULTIPLE RANDOM SEEDS (Experiment E)")
    print("=" * 60)

    seeds = [11, 22, 33, 44, 55, 66, 77, 88, 99, 111]
    results = []

    for seed in seeds:
        agent, _ = train_rl_against_rule(config, seed=seed)
        summary, _ = evaluate_pair(
            config,
            agent,
            episodes=config.evaluation_episodes,
            seed=seed + 800_000
        )
        for row in summary:
            results.append({
                "seed": seed,
                "agent": row["agent"],
                "mean_reward_per_step": row["mean_reward_per_step"],
                "discount_action_rate": row["discount_action_rate"]
            })

    write_csv(output_dir / "multi_seed_summary.csv", results)

    print("\nStatistical Aggregate across 10 independent seeds:")
    for name in ["RL", "Rule-based"]:
        vals = [r["mean_reward_per_step"] for r in results if r["agent"] == name]
        mean_val = np.mean(vals)
        std_val = np.std(vals, ddof=1)
        sem_val = std_val / np.sqrt(len(vals))
        print(f"  {name:12s} | Mean = {mean_val:.4f} | Std = {std_val:.4f} | SEM = {sem_val:.4f} | 95% CI = [{mean_val - 1.96*sem_val:.4f}, {mean_val + 1.96*sem_val:.4f}]")

    return results


def main():
    config = Config()
    out_dir = Path(config.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("AGENT02: REINFORCEMENT LEARNING VS RULE-BASED EXPERIMENTS")
    print("=" * 60)
    print(f"Episodes: {config.episodes}")
    print(f"Steps/Episode: {config.steps_per_episode}")
    print(f"Evaluation Episodes: {config.evaluation_episodes}")
    print(f"Output Directory: {out_dir.resolve()}")

    run_baseline(config, out_dir)
    run_learning_rate_experiment(config, out_dir)
    run_exploration_experiment(config, out_dir)
    run_multi_seed_experiment(config, out_dir)

    print("\n" + "=" * 60)
    print("ALL BASELINE EXPERIMENTS COMPLETED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == "__main__":
    main()
