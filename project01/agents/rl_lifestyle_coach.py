#!/usr/bin/env python3
"""
Advanced Reinforcement Learning Lifestyle Coach (DiaRLCoachAgent)
Simulates a 24-hour virtual physiological glucose-insulin environment with diurnal circadian variation.
Implements:
  1. VirtualPatientEnv (Physiological glucose simulator with dawn phenomenon)
  2. Tabular Q-Learning Coach
  3. Deep Q-Network (DQN) Coach
  4. Dueling Double Deep Q-Network (D3QN) with Value & Advantage streams (PyTorch)
  5. Heuristic Rule-Based Policy & Sedentary Baseline
  6. Multi-Cohort Benchmark (Good sensitivity, Moderate resistance, Severe resistance)
"""

import math
import random
import json
import os
from collections import deque
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

ACTIONS = [
    {"id": 0, "name": "Nghỉ ngơi", "code": "rest", "carbs": 0, "fast": False, "act": 0.0},
    {"id": 1, "name": "Ăn nhẹ có đường (cấp cứu)", "code": "sugary_snack", "carbs": 15, "fast": True, "act": 0.0},
    {"id": 2, "name": "Bữa phụ lành mạnh", "code": "snack", "carbs": 15, "fast": False, "act": 0.0},
    {"id": 3, "name": "Bữa chính cân bằng", "code": "main_meal", "carbs": 45, "fast": False, "act": 0.0},
    {"id": 4, "name": "Bữa nhiều tinh bột", "code": "high_carb_meal", "carbs": 75, "fast": False, "act": 0.0},
    {"id": 5, "name": "Đi bộ nhẹ 30 phút", "code": "walk", "carbs": 0, "fast": False, "act": 1.0},
    {"id": 6, "name": "Tập thể dục nhịp điệu 45 phút", "code": "exercise", "carbs": 0, "fast": False, "act": 2.0},
]
ACTION_NAMES = [a["name"] for a in ACTIONS]
NUM_ACTIONS = len(ACTIONS)

def is_night(hour: int) -> bool:
    h = hour % 24
    return h >= 22 or h < 6

def allowed_actions(hour: int):
    if is_night(hour):
        return [0, 1]  # Night: rest or emergency sugary snack only
    return list(range(NUM_ACTIONS))

class VirtualPatient:
    def __init__(self, insulin_sensitivity: float = 0.7, baseline_glucose: float = 100.0, medication: float = 0.0, name: str = "Bệnh nhân ảo"):
        self.insulin_sensitivity = float(insulin_sensitivity)
        self.baseline_glucose = float(baseline_glucose)
        self.medication = float(medication)
        self.name = name

    @classmethod
    def random_cohort_patient(cls, cohort: str = "moderate", rng: random.Random = None):
        if rng is None:
            rng = random.Random()
        if cohort == "good":
            s = rng.uniform(0.85, 1.15)
            base = rng.uniform(85, 105)
            med = 0.0
        elif cohort == "moderate":
            s = rng.uniform(0.55, 0.84)
            base = rng.uniform(105, 130)
            med = rng.choice([0.0, 5.0, 10.0])
        else: # severe
            s = rng.uniform(0.30, 0.54)
            base = rng.uniform(130, 160)
            med = rng.choice([10.0, 15.0, 20.0])
        return cls(insulin_sensitivity=s, baseline_glucose=base, medication=med)


class VirtualPatientEnv:
    def __init__(self, patient: VirtualPatient = None, seed: int = 42):
        self.rng = random.Random(seed)
        self.patient = patient or VirtualPatient()
        self.reset()

    def reset(self, patient: VirtualPatient = None):
        if patient is not None:
            self.patient = patient
        self.hour = 6  # Start at 6:00 AM
        self.glucose = float(self.patient.baseline_glucose + self.rng.gauss(0, 3.5))
        self.carbs = 0.0
        self.act = 0.0
        self.since_meal = 8  # Fasted overnight
        self.exercise_count = 0
        self.step_count = 0
        self.history = []
        return self._get_state_dict()

    def _get_state_dict(self):
        return {
            "hour": self.hour,
            "glucose": round(self.glucose, 1),
            "carbs": round(self.carbs, 2),
            "act": round(self.act, 2),
            "since_meal": self.since_meal,
            "exercise_count": self.exercise_count,
            "insulin_sensitivity": self.patient.insulin_sensitivity,
            "baseline_glucose": self.patient.baseline_glucose,
            "medication": self.patient.medication,
            "step_count": self.step_count,
        }

    def encode_discrete_state(self) -> int:
        h = self.hour % 24
        if 6 <= h < 9:
            tb = 0
        elif 9 <= h < 12:
            tb = 1
        elif 12 <= h < 15:
            tb = 2
        elif 15 <= h < 18:
            tb = 3
        elif 18 <= h < 22:
            tb = 4
        else:
            tb = 5

        g = self.glucose
        if g < 70:
            gb = 0
        elif g < 100:
            gb = 1
        elif g < 140:
            gb = 2
        elif g < 180:
            gb = 3
        elif g < 250:
            gb = 4
        else:
            gb = 5

        cb = 0 if self.carbs < 5 else (1 if self.carbs < 25 else 2)
        ab = 1 if self.act > 0.3 else 0
        hb = 0 if self.since_meal < 3 else (1 if self.since_meal < 6 else 2)
        sb = 0 if self.patient.insulin_sensitivity >= 0.85 else (1 if self.patient.insulin_sensitivity >= 0.55 else 2)
        mb = 1 if self.patient.medication > 0 else 0

        idx = (((((tb * 6 + gb) * 3 + cb) * 2 + ab) * 3 + hb) * 3 + sb) * 2 + mb
        return idx

    def get_feature_vector(self) -> np.ndarray:
        h_sin = math.sin(2 * math.pi * self.hour / 24.0)
        h_cos = math.cos(2 * math.pi * self.hour / 24.0)
        g_norm = (self.glucose - 120.0) / 60.0
        c_norm = self.carbs / 50.0
        a_norm = self.act / 2.0
        sm_norm = min(self.since_meal / 10.0, 1.5)
        s_norm = self.patient.insulin_sensitivity - 0.7
        med_norm = self.patient.medication / 20.0
        is_n = 1.0 if is_night(self.hour) else 0.0
        return np.array([h_sin, h_cos, g_norm, c_norm, a_norm, sm_norm, s_norm, med_norm, is_n], dtype=np.float32)

    def step(self, action_id: int):
        act = ACTIONS[action_id]
        s = self.patient.insulin_sensitivity
        base = self.patient.baseline_glucose
        med = self.patient.medication

        # Circadian cortisol morning dawn phenomenon
        circadian_factor = 1.15 if 6 <= (self.hour % 24) <= 8 else 1.0

        c_total = self.carbs + act["carbs"]
        absorb_rate = 0.75 if act["fast"] else 0.45
        absorbed = c_total * absorb_rate
        self.carbs = c_total - absorbed
        rise = absorbed * 1.35 * (1.7 - s) * circadian_factor

        a_total = self.act + act["act"]
        drop_act = a_total * 14.0 * (0.5 + 0.5 * s) * max(0.0, min(1.0, (self.glucose - 62.0) / 60.0))
        self.act = a_total * 0.5

        pull = (self.glucose - base) * 0.16 * s
        drop_med = med * max(0.0, min(1.0, (self.glucose - 55.0) / 60.0))

        noise = self.rng.gauss(0, 2.0)
        g_new = self.glucose + rise - drop_act - pull - drop_med + noise
        g_new = max(35.0, min(420.0, g_new))
        self.glucose = g_new

        is_meal = act["carbs"] >= 15
        if is_meal:
            self.since_meal = 0
        else:
            self.since_meal += 1

        if act["act"] > 0:
            self.exercise_count += 1

        reward = 0.0
        if 70.0 <= g_new <= 140.0:
            reward += 1.0
        elif 140.0 < g_new <= 180.0:
            reward += 0.5
        elif 180.0 < g_new <= 250.0:
            reward -= 1.0
        elif g_new > 250.0:
            reward -= 3.0
        elif 55.0 <= g_new < 70.0:
            reward -= 1.5
        else:
            reward -= 4.0

        night = is_night(self.hour)
        if self.since_meal >= 6 and not night:
            reward -= 0.6

        if act["act"] > 0 and self.exercise_count <= 2 and not night:
            reward += 0.35

        self.hour = (self.hour + 1) % 24
        self.step_count += 1
        done = (self.step_count >= 24)

        info = {
            "hour": self.hour,
            "action": act["name"],
            "glucose": round(self.glucose, 1),
            "rise": round(rise, 1),
            "drop": round(drop_act + drop_med, 1),
            "zone": "target" if 70 <= g_new <= 180 else ("high" if g_new > 180 else "low"),
        }
        self.history.append(info)
        return self._get_state_dict(), reward, done, info


class TabularQCoach:
    def __init__(self, alpha: float = 0.15, gamma: float = 0.97):
        self.alpha = alpha
        self.gamma = gamma
        self.q_table = {}

    def get_q(self, state_idx: int) -> list:
        if state_idx not in self.q_table:
            self.q_table[state_idx] = [0.0] * NUM_ACTIONS
        return self.q_table[state_idx]

    def act(self, env: VirtualPatientEnv, epsilon: float = 0.05, rng: random.Random = None) -> int:
        if rng is None:
            rng = random.Random()
        allowed = allowed_actions(env.hour)
        if rng.random() < epsilon:
            return rng.choice(allowed)
        s_idx = env.encode_discrete_state()
        q_vals = self.get_q(s_idx)
        best_a = max(allowed, key=lambda a: q_vals[a])
        return best_a

    def update(self, s: int, a: int, r: float, s_next: int, next_hour: int, done: bool):
        allowed_next = allowed_actions(next_hour)
        q_curr = self.get_q(s)
        if done:
            target = r
        else:
            q_next = self.get_q(s_next)
            best_next = max(q_next[act] for act in allowed_next)
            target = r + self.gamma * best_next
        q_curr[a] += self.alpha * (target - q_curr[a])

    def save(self, filepath: str):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({str(k): v for k, v in self.q_table.items()}, f)

    def load(self, filepath: str):
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.q_table = {int(k): v for k, v in data.items()}


# =========================================================================
# ADVANCED DUELING DOUBLE DEEP Q-NETWORK (D3QN) ARCHITECTURE
# Q(s, a) = V(s) + [A(s, a) - 1/|A| * sum(A(s, a'))]
# =========================================================================
class DuelingDQNetwork(nn.Module):
    def __init__(self, input_dim: int = 9, hidden_dim: int = 64, output_dim: int = NUM_ACTIONS):
        super().__init__()
        # Shared Feature Representation
        self.feature_extractor = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.ReLU()
        )
        # Value Stream V(s)
        self.value_stream = nn.Sequential(
            nn.Linear(hidden_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )
        # Advantage Stream A(s, a)
        self.advantage_stream = nn.Sequential(
            nn.Linear(hidden_dim, 32),
            nn.ReLU(),
            nn.Linear(32, output_dim)
        )

    def forward(self, x):
        feat = self.feature_extractor(x)
        val = self.value_stream(feat)
        adv = self.advantage_stream(feat)
        # Identifiability constraint: subtract mean advantage
        q_vals = val + (adv - adv.mean(dim=-1, keepdim=True))
        return q_vals


class D3QNCoach:
    """Dueling Double Deep Q-Network Coach with Target Network Decoupling"""
    def __init__(self, gamma: float = 0.97, lr: float = 0.001):
        self.gamma = gamma
        self.device = torch.device("cpu")
        self.policy_net = DuelingDQNetwork().to(self.device)
        self.target_net = DuelingDQNetwork().to(self.device)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=lr, weight_decay=1e-5)
        self.memory = deque(maxlen=15000)
        self.batch_size = 64

    def act(self, env: VirtualPatientEnv, epsilon: float = 0.05, rng: random.Random = None) -> int:
        if rng is None:
            rng = random.Random()
        allowed = allowed_actions(env.hour)
        if rng.random() < epsilon:
            return rng.choice(allowed)
        feat = torch.tensor(env.get_feature_vector(), dtype=torch.float32).unsqueeze(0).to(self.device)
        with torch.no_grad():
            q_values = self.policy_net(feat)[0].numpy()
        best_a = max(allowed, key=lambda a: q_values[a])
        return best_a

    def remember(self, state, action, reward, next_state, next_hour, done):
        self.memory.append((state, action, reward, next_state, next_hour, done))

    def train_step(self):
        if len(self.memory) < self.batch_size:
            return 0.0
        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, next_hours, dones = zip(*batch)

        states_t = torch.tensor(np.array(states), dtype=torch.float32)
        actions_t = torch.tensor(actions, dtype=torch.int64).unsqueeze(1)
        rewards_t = torch.tensor(rewards, dtype=torch.float32)
        next_states_t = torch.tensor(np.array(next_states), dtype=torch.float32)

        curr_q = self.policy_net(states_t).gather(1, actions_t).squeeze(1)

        # Double DQN update: action selected by policy_net, evaluated by target_net
        with torch.no_grad():
            policy_next_q = self.policy_net(next_states_t).numpy()
            target_next_q = self.target_net(next_states_t).numpy()
            target_q = []
            for i in range(self.batch_size):
                if dones[i]:
                    target_q.append(rewards[i])
                else:
                    allow = allowed_actions(next_hours[i])
                    # Double Q-learning selection:
                    best_next_action = max(allow, key=lambda a: policy_next_q[i, a])
                    q_val = target_next_q[i, best_next_action]
                    target_q.append(rewards[i] + self.gamma * q_val)
            target_t = torch.tensor(target_q, dtype=torch.float32)

        loss = nn.SmoothL1Loss()(curr_q, target_t)  # Huber Loss for robustness
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        return float(loss.item())

    def update_target(self, tau: float = 0.1):
        # Soft Polyak Target update
        for target_param, param in zip(self.target_net.parameters(), self.policy_net.parameters()):
            target_param.data.copy_(tau * param.data + (1.0 - tau) * target_param.data)

    def save(self, filepath: str):
        torch.save(self.policy_net.state_dict(), filepath)

    def load(self, filepath: str):
        if os.path.exists(filepath):
            try:
                self.policy_net.load_state_dict(torch.load(filepath, map_location=self.device))
                self.target_net.load_state_dict(self.policy_net.state_dict())
            except Exception:
                pass


class HeuristicRuleCoach:
    @staticmethod
    def act(env: VirtualPatientEnv) -> int:
        h = env.hour % 24
        g = env.glucose
        if is_night(h):
            return 1 if g < 75.0 else 0
        if g < 70.0:
            return 1
        if g > 180.0 and env.since_meal <= 2:
            return 5
        if h in [7, 12, 19] and env.since_meal >= 3:
            return 3
        if h in [10, 16] and env.since_meal >= 3:
            return 2
        if 8 <= h <= 17 and env.exercise_count < 1 and 100 <= g <= 160:
            return 6
        return 0


class SedentaryNoCoach:
    @staticmethod
    def act(env: VirtualPatientEnv) -> int:
        h = env.hour % 24
        if is_night(h):
            return 0
        if h in [7, 12, 19]:
            return 4
        if h in [10, 15, 21]:
            return 1
        return 0


def evaluate_policy_on_cohort(coach, cohort_name: str, num_patients: int = 50, days_per_patient: int = 5, seed: int = 999):
    rng = random.Random(seed)
    total_steps = 0
    in_range_steps = 0
    hypo_hours = 0
    hyper_hours = 0
    glucose_sum = 0.0
    daily_returns = []

    for _ in range(num_patients):
        patient = VirtualPatient.random_cohort_patient(cohort_name, rng)
        env = VirtualPatientEnv(patient=patient, seed=rng.randint(1, 100000))
        for _ in range(days_per_patient):
            env.reset(patient)
            ep_return = 0.0
            done = False
            while not done:
                if isinstance(coach, (TabularQCoach, D3QNCoach)):
                    action = coach.act(env, epsilon=0.0, rng=rng)
                elif coach == "rule":
                    action = HeuristicRuleCoach.act(env)
                elif coach == "none":
                    action = SedentaryNoCoach.act(env)
                else:
                    action = 0

                _, r, done, info = env.step(action)
                ep_return += r
                g = info["glucose"]
                total_steps += 1
                glucose_sum += g
                if 70.0 <= g <= 180.0:
                    in_range_steps += 1
                elif g < 70.0:
                    hypo_hours += 1
                else:
                    hyper_hours += 1
            daily_returns.append(ep_return)

    days = num_patients * days_per_patient
    return {
        "cohort": cohort_name,
        "tir_percent": round(100.0 * in_range_steps / total_steps, 2),
        "mean_glucose": round(glucose_sum / total_steps, 1),
        "hypo_hours_per_day": round(hypo_hours / days, 2),
        "hyper_hours_per_day": round(hyper_hours / days, 2),
        "mean_daily_return": round(sum(daily_returns) / len(daily_returns), 2),
    }


class DiaRLCoachAgent:
    """Tác Tử Huấn Luyện Lối Sống Reinforcement Learning Dueling Double DQN (D3QN)"""
    def __init__(self, model_dir: str = "project01/models"):
        self.name = "DiaD3QNCoach-Agent (Tác Tử Huấn Luyện Lối Sống Dueling Double Deep Q-Network)"
        self.model_dir = model_dir
        self.tabular_coach = TabularQCoach()
        self.d3qn_coach = D3QNCoach()
        
        q_path = os.path.join(model_dir, "rl_qtable.json")
        d3qn_path = os.path.join(model_dir, "rl_d3qn.pt")
        if not os.path.exists(d3qn_path):
            d3qn_path = os.path.join(model_dir, "rl_dqn.pt")
        if os.path.exists(q_path):
            self.tabular_coach.load(q_path)
        if os.path.exists(d3qn_path):
            self.d3qn_coach.load(d3qn_path)

    def formulate_daily_schedule(self, patient_data: dict) -> dict:
        bmi = float(patient_data.get("bmi", 25.0))
        hba1c = float(patient_data.get("HbA1c_level", 5.5))
        glucose = float(patient_data.get("blood_glucose_level", 100.0))
        
        if hba1c >= 8.0 or glucose >= 180 or bmi >= 32:
            cohort = "severe"
            s = 0.45
        elif hba1c >= 6.5 or glucose >= 126 or bmi >= 27:
            cohort = "moderate"
            s = 0.65
        else:
            cohort = "good"
            s = 0.95

        med = 10.0 if (hba1c >= 7.0 or glucose >= 140) else 0.0
        v_pat = VirtualPatient(insulin_sensitivity=s, baseline_glucose=min(160.0, glucose), medication=med, name="Bệnh nhân lâm sàng")
        env = VirtualPatientEnv(patient=v_pat, seed=42)
        env.reset()

        schedule = []
        done = False
        while not done:
            action = self.d3qn_coach.act(env, epsilon=0.0)
            st, r, done, info = env.step(action)
            h = (info["hour"] - 1) % 24
            schedule.append({
                "time": f"{h:02d}:00",
                "action": info["action"],
                "simulated_glucose": info["glucose"],
                "zone": info["zone"],
            })

        tir = round(100.0 * sum(1 for s in schedule if 70 <= s["simulated_glucose"] <= 180) / len(schedule), 1)
        mean_g = round(sum(s["simulated_glucose"] for s in schedule) / len(schedule), 1)

        msg = (
            f"Tôi là {self.name}.\n"
            f"✦ ĐIỀU PHỐI LỐI SỐNG DUELING DOUBLE DQN (D3QN) 24 GIỜ:\n"
            f"  • Độ nhạy Insulin ước tính: {s:.2f} ({cohort.upper()})\n"
            f"  • Thời gian trong ngưỡng an toàn (TIR 70-180 mg/dL): {tir}%\n"
            f"  • Đường huyết mô phỏng trung bình 24h: {mean_g} mg/dL\n"
            f"✦ LỘ TRÌNH CAN THIỆP SINH HOẠT TỐI ƯU CỦA DUELING DEEP Q-NETWORK:\n"
            + "\n".join([f"  • [{s['time']}] {s['action']} -> Glucose: {s['simulated_glucose']} mg/dL ({s['zone']})" 
                         for s in schedule if s['action'] != "Nghỉ ngơi" or int(s['time'][:2]) in [7, 12, 19]])
        )
        return {
            "agent": self.name,
            "cohort": cohort,
            "insulin_sensitivity": s,
            "tir_percent": tir,
            "mean_glucose": mean_g,
            "schedule": schedule,
            "speech": msg
        }
