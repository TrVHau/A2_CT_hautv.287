#!/usr/bin/env python3
"""
Train Tabular Q-Learning and Deep Q-Network (DQN) for 24-hour Glucose-Insulin Control.
Saves model checkpoints and generates evaluation comparison against Heuristic Rule Coach and Sedentary Baseline.
"""

import os
import sys
import json
import random
import numpy as np

sys.path.insert(0, os.path.abspath("."))
from project01.agents.rl_lifestyle_coach import (
    VirtualPatient,
    VirtualPatientEnv,
    TabularQCoach,
    DQNCoach,
    evaluate_policy_on_cohort
)

def train_tabular_q(episodes: int = 15000, seed: int = 42):
    print(f"[*] Training Tabular Q-Learning ({episodes} episodes)...")
    rng = random.Random(seed)
    coach = TabularQCoach(alpha=0.15, gamma=0.97)
    learning_curve = []

    for ep in range(episodes):
        eps = max(0.05, 1.0 - 0.95 * ep / (0.75 * episodes))
        cohort = rng.choice(["good", "moderate", "severe"])
        patient = VirtualPatient.random_cohort_patient(cohort, rng)
        env = VirtualPatientEnv(patient=patient, seed=rng.randint(1, 100000))
        env.reset()

        done = False
        ep_ret = 0.0
        while not done:
            s_idx = env.encode_discrete_state()
            action = coach.act(env, epsilon=eps, rng=rng)
            curr_hour = env.hour
            _, r, done, _ = env.step(action)
            s_next = env.encode_discrete_state()
            coach.update(s_idx, action, r, s_next, env.hour, done)
            ep_ret += r

        if (ep + 1) % 1500 == 0:
            learning_curve.append({"episode": ep + 1, "epsilon": round(eps, 3), "return": round(ep_ret, 2)})
            print(f"    Tabular Episode {ep+1}/{episodes} | Return: {ep_ret:.2f} | Epsilon: {eps:.3f} | Visited states: {len(coach.q_table)}")

    return coach, learning_curve


def train_dqn(episodes: int = 600, seed: int = 42):
    print(f"[*] Training Deep Q-Network DQN ({episodes} episodes)...")
    rng = random.Random(seed)
    coach = DQNCoach(gamma=0.97, lr=0.001)
    learning_curve = []

    for ep in range(episodes):
        eps = max(0.05, 1.0 - 0.95 * ep / (0.8 * episodes))
        cohort = rng.choice(["good", "moderate", "severe"])
        patient = VirtualPatient.random_cohort_patient(cohort, rng)
        env = VirtualPatientEnv(patient=patient, seed=rng.randint(1, 100000))
        env.reset()

        done = False
        ep_ret = 0.0
        losses = []
        while not done:
            s_feat = env.get_feature_vector()
            action = coach.act(env, epsilon=eps, rng=rng)
            curr_hour = env.hour
            _, r, done, _ = env.step(action)
            s_next_feat = env.get_feature_vector()
            coach.remember(s_feat, action, r, s_next_feat, env.hour, done)
            loss = coach.train_step()
            if loss > 0:
                losses.append(loss)
            ep_ret += r

        if (ep + 1) % 10 == 0:
            coach.update_target()

        if (ep + 1) % 100 == 0:
            avg_loss = float(np.mean(losses)) if losses else 0.0
            learning_curve.append({"episode": ep + 1, "epsilon": round(eps, 3), "return": round(ep_ret, 2), "loss": round(avg_loss, 4)})
            print(f"    DQN Episode {ep+1}/{episodes} | Return: {ep_ret:.2f} | Avg Loss: {avg_loss:.4f} | Epsilon: {eps:.3f}")

    return coach, learning_curve


def main():
    os.makedirs("project01/models", exist_ok=True)
    
    # 1. Train Tabular Q-Learning
    tabular_coach, tab_curve = train_tabular_q(episodes=15000)
    tabular_coach.save("project01/models/rl_qtable.json")

    # 2. Train DQN
    dqn_coach, dqn_curve = train_dqn(episodes=600)
    dqn_coach.save("project01/models/rl_dqn.pt")

    # 3. Comprehensive Multi-Cohort Evaluation
    print("\n[*] Evaluating All Policies across 3 Insulin Sensitivity Cohorts...")
    cohorts = ["good", "moderate", "severe"]
    evaluation_matrix = {}

    for c in cohorts:
        evaluation_matrix[c] = {
            "DQN_Coach": evaluate_policy_on_cohort(dqn_coach, c, num_patients=50, days_per_patient=5),
            "Tabular_Q_Coach": evaluate_policy_on_cohort(tabular_coach, c, num_patients=50, days_per_patient=5),
            "Rule_Based_Coach": evaluate_policy_on_cohort("rule", c, num_patients=50, days_per_patient=5),
            "Sedentary_No_Coach": evaluate_policy_on_cohort("none", c, num_patients=50, days_per_patient=5),
        }
        print(f"  Cohort [{c.upper()}]:")
        for p_name, res in evaluation_matrix[c].items():
            print(f"    - {p_name:18s}: TIR={res['tir_percent']:5.1f}% | Mean Glucose={res['mean_glucose']:5.1f} mg/dL | Return={res['mean_daily_return']:6.2f}")

    out_data = {
        "tabular_learning_curve": tab_curve,
        "dqn_learning_curve": dqn_curve,
        "evaluation_matrix": evaluation_matrix
    }

    with open("project01/models/rl_evaluation_results.json", "w", encoding="utf-8") as f:
        json.dump(out_data, f, indent=2)

    print("\n[V] RL Training & Multi-Cohort Benchmark Complete! Saved to project01/models/rl_evaluation_results.json")

if __name__ == "__main__":
    main()
