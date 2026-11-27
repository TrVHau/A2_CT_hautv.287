"""
PyTorch Deep Learning Module for Diabetes Risk Prediction:
- 13-feature input vector (age, BMI, HbA1c, glucose, gender, hypertension, heart_disease, 6 smoking one-hot)
- DiabetesMLP: 13 -> 128 -> 64 -> 1 logit with BatchNorm, ReLU, Dropout(0.2)
- Exactly 10,497 parameters matching thesis specification
- Class-imbalanced Weighted BCE loss (pos_weight = 10.3)
- Calibrated decision threshold tau = 0.9016 maximizing F1 on validation cohort
"""

import os
import json
from typing import Tuple, Dict, Any, Optional
import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, average_precision_score


class DiabetesMLP(nn.Module):
    """13 -> 128 -> 64 -> 1 with BatchNorm, ReLU, and Dropout."""
    def __init__(self, d_in: int = 13, hidden: tuple = (128, 64), dropout: float = 0.2):
        super().__init__()
        layers = []
        curr_d = d_in
        for h in hidden:
            layers.extend([
                nn.Linear(curr_d, h),
                nn.BatchNorm1d(h),
                nn.ReLU(),
                nn.Dropout(dropout)
            ])
            curr_d = h
        layers.append(nn.Linear(curr_d, 1))
        self.net = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x).squeeze(-1)


NUMERIC_COLS = ["age", "bmi", "HbA1c_level", "blood_glucose_level"]
SMOKING_CATS = ["never", "current", "former", "ever", "not current", "No Info"]


def preprocess_diabetes_features(df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
    """Encodes raw dataframe into 13-feature matrix and binary labels."""
    X = pd.DataFrame()
    for col in NUMERIC_COLS:
        X[col] = df[col].astype(float)

    # Demographic & Co-morbidities
    X["male"] = (df["gender"] == "Male").astype(float)
    X["hypertension"] = df["hypertension"].astype(float)
    X["heart_disease"] = df["heart_disease"].astype(float)

    # 6 one-hot smoking columns
    for s in SMOKING_CATS:
        X[f"smoke_{s}"] = (df["smoking_history"] == s).astype(float)

    y = df["diabetes"].to_numpy(dtype=np.float32) if "diabetes" in df.columns else np.zeros(len(df))
    return X.to_numpy(dtype=np.float32), y


class DiabetesPredictor:
    """Inference and Evaluation Wrapper for DiabetesMLP."""
    def __init__(self, model_path: Optional[str] = None, scaler_path: Optional[str] = None):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = DiabetesMLP(d_in=13, hidden=(128, 64), dropout=0.2).to(self.device)
        self.threshold = 0.9016
        self.means = None
        self.stds = None
        
        if model_path and os.path.exists(model_path):
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            self.model.eval()

        if scaler_path and os.path.exists(scaler_path):
            with open(scaler_path, "r") as f:
                stats = json.load(f)
                self.means = np.array(stats["means"], dtype=np.float32)
                self.stds = np.array(stats["stds"], dtype=np.float32)

    def fit_and_train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray,
        epochs: int = 60,
        batch_size: int = 1024,
        lr: float = 1e-3,
        weight_decay: float = 1e-4
    ) -> Dict[str, Any]:
        """Trains DiabetesMLP on training set and validates on validation set."""
        # Normalize features based on train statistics
        self.means = np.mean(X_train, axis=0)
        self.stds = np.std(X_train, axis=0)
        self.stds[self.stds == 0] = 1.0

        X_tr = (X_train - self.means) / self.stds
        X_va = (X_val - self.means) / self.stds

        # Calculate pos_weight = N_neg / N_pos
        n_pos = np.sum(y_train == 1)
        n_neg = np.sum(y_train == 0)
        pos_weight_val = n_neg / max(n_pos, 1)

        pos_weight = torch.tensor([pos_weight_val], dtype=torch.float32, device=self.device)
        criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
        optimizer = torch.optim.AdamW(self.model.parameters(), lr=lr, weight_decay=weight_decay)
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode="max", factor=0.5, patience=3)

        x_tr_t = torch.tensor(X_tr, dtype=torch.float32, device=self.device)
        y_tr_t = torch.tensor(y_train, dtype=torch.float32, device=self.device)
        x_va_t = torch.tensor(X_va, dtype=torch.float32, device=self.device)
        y_va_t = torch.tensor(y_val, dtype=torch.float32, device=self.device)

        best_ap = -1.0
        best_state = None
        history = []

        self.model.train()
        n_samples = len(X_tr)

        for ep in range(1, epochs + 1):
            perm = torch.randperm(n_samples, device=self.device)
            total_loss = 0.0

            self.model.train()
            for i in range(0, n_samples, batch_size):
                batch_idx = perm[i:i + batch_size]
                optimizer.zero_grad()
                logits = self.model(x_tr_t[batch_idx])
                loss = criterion(logits, y_tr_t[batch_idx])
                loss.backward()
                optimizer.step()
                total_loss += loss.item() * len(batch_idx)

            avg_train_loss = total_loss / n_samples

            # Validation
            self.model.eval()
            with torch.no_grad():
                val_logits = self.model(x_va_t)
                val_loss = criterion(val_logits, y_va_t).item()
                val_probs = torch.sigmoid(val_logits).cpu().numpy()

            val_ap = average_precision_score(y_val, val_probs)
            val_roc = roc_auc_score(y_val, val_probs)
            scheduler.step(val_ap)

            history.append({
                "epoch": ep,
                "train_loss": avg_train_loss,
                "val_loss": val_loss,
                "val_pr_auc": float(val_ap),
                "val_roc_auc": float(val_roc)
            })

            if val_ap > best_ap:
                best_ap = val_ap
                best_state = {k: v.cpu().clone() for k, v in self.model.state_dict().items()}

        if best_state is not None:
            self.model.load_state_dict(best_state)
            self.model.eval()

        return {"history": history, "best_val_pr_auc": float(best_ap)}

    def predict_risk(self, feature_vector: np.ndarray) -> Dict[str, Any]:
        """Inference for a single patient (13 features)."""
        self.model.eval()
        if self.means is not None and self.stds is not None:
            norm_feat = (feature_vector - self.means) / self.stds
        else:
            norm_feat = feature_vector

        x_t = torch.tensor(norm_feat.reshape(1, -1), dtype=torch.float32, device=self.device)
        with torch.no_grad():
            logit = self.model(x_t).item()
            prob = 1.0 / (1.0 + np.exp(-logit))

        is_high_risk = bool(prob >= self.threshold)
        return {
            "risk_probability": float(prob),
            "risk_percentage": f"{prob * 100:.2f}%",
            "threshold": self.threshold,
            "risk_status": "NGUY CƠ CAO (VƯỢT NGƯỠNG)" if is_high_risk else "NGUY CƠ THẤP / BÌNH THƯỜNG",
            "clinical_advice": "Cần can thiệp lối sống tích cực và hội chẩn bác sĩ nội tiết để làm nghiệm pháp OGTT/HbA1c định kỳ." if is_high_risk else "Duy trì chế độ dinh dưỡng lành mạnh và tập luyện thể lực thường xuyên."
        }
