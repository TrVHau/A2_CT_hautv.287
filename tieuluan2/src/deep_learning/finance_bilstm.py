"""
PyTorch Deep Learning Module for Financial Time-Series Forecasting:
- Bidirectional LSTM (BiLSTM): 2 layers, 64 hidden units per direction (total 128)
- Fully connected head: 128 -> 32 -> 1 log return
- Total parameters: exactly 140,865 parameters matching thesis specification
- Huber Loss (delta=1.0) robust to financial market fat tails
- Monte Carlo Dropout (200 passes) estimating epistemic and aleatoric uncertainty
- Generates 90% confidence interval bounds for next-day log return and price
"""

import os
import json
import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any, Optional


class SeqForecaster(nn.Module):
    """Bidirectional LSTM with FC head predicting next-session log return."""
    def __init__(self, d_in: int = 7, hidden: int = 64, layers: int = 2, dropout: float = 0.2, bidirectional: bool = True):
        super().__init__()
        self.bidirectional = bidirectional
        self.rnn = nn.LSTM(
            input_size=d_in,
            hidden_size=hidden,
            num_layers=layers,
            batch_first=True,
            dropout=dropout if layers > 1 else 0.0,
            bidirectional=bidirectional
        )
        k = 2 if bidirectional else 1
        self.head = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(k * hidden, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out, _ = self.rnn(x)
        # Take the output at the last time step
        last_step = out[:, -1, :]
        return self.head(last_step).squeeze(-1)


EXOG_VARS = ["USD_VND", "XAU", "DXY", "VN30"]


def build_financial_features(df: pd.DataFrame, target: str = "FPT", window: int = 30) -> Tuple[np.ndarray, np.ndarray, np.ndarray, List[str]]:
    """
    Constructs rolling window features:
    - Target log return: r_target = ln(P_t / P_{t-1})
    - Exogenous returns: USD/VND, XAU, DXY, VN30
    - Price deviation from 20-day moving average: P / MA20 - 1
    - 20-day historical rolling return volatility
    - Next-session return label: y = r_{t+1}
    """
    df_calc = df.copy()
    prices = df_calc[target].values
    r_target = np.diff(np.log(prices), prepend=np.nan)

    feat_df = pd.DataFrame({"r_target": r_target}, index=df_calc.index)
    for s in EXOG_VARS:
        if s != target and not (target == "GOLD_VND" and s == "XAU"):
            r_s = np.diff(np.log(df_calc[s].values), prepend=np.nan)
            feat_df[f"r_{s}"] = r_s

    # MA20 deviation and 20-day rolling volatility
    ma20 = df_calc[target].rolling(20).mean().values
    feat_df["dev_ma20"] = (prices / ma20) - 1.0
    feat_df["vol20"] = pd.Series(r_target).rolling(20).std().values
    feat_df["y"] = pd.Series(r_target).shift(-1).values
    feat_df["price"] = prices

    valid_idx = feat_df.dropna().index
    feat_clean = feat_df.loc[valid_idx]

    feature_cols = [c for c in feat_clean.columns if c not in ["y", "price"]]
    X_raw = feat_clean[feature_cols].to_numpy(dtype=np.float32)
    y_raw = feat_clean["y"].to_numpy(dtype=np.float32)
    prices_raw = feat_clean["price"].to_numpy(dtype=np.float32)

    # Build 30-day sliding windows
    n_samples = len(X_raw) - window + 1
    X_windows = np.stack([X_raw[i:i + window] for i in range(n_samples)])
    y_windows = y_raw[window - 1: window - 1 + n_samples]
    p_windows = prices_raw[window - 1: window - 1 + n_samples]

    return X_windows, y_windows, p_windows, feature_cols


class FinancialForecaster:
    """Inference and Training Manager for BiLSTM."""
    def __init__(self, target_asset: str = "FPT", model_path: Optional[str] = None):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.target_asset = target_asset
        self.d_in = 7 if target_asset != "GOLD_VND" else 6
        self.model = SeqForecaster(d_in=self.d_in, hidden=64, layers=2, dropout=0.2, bidirectional=True).to(self.device)
        self.residual_std = 0.015
        
        if model_path and os.path.exists(model_path):
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            self.model.eval()

    def fit_and_train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray,
        epochs: int = 50,
        batch_size: int = 128,
        lr: float = 1e-3
    ) -> Dict[str, Any]:
        """Trains BiLSTM using Huber Loss (delta=1.0) and AdamW."""
        criterion = nn.HuberLoss(delta=1.0)
        optimizer = torch.optim.AdamW(self.model.parameters(), lr=lr, weight_decay=1e-4)

        x_tr_t = torch.tensor(X_train, dtype=torch.float32, device=self.device)
        y_tr_t = torch.tensor(y_train, dtype=torch.float32, device=self.device)
        x_va_t = torch.tensor(X_val, dtype=torch.float32, device=self.device)
        y_va_t = torch.tensor(y_val, dtype=torch.float32, device=self.device)

        best_loss = float("inf")
        best_state = None
        history = []
        n_samples = len(X_train)

        for ep in range(1, epochs + 1):
            self.model.train()
            perm = torch.randperm(n_samples, device=self.device)
            total_loss = 0.0

            for i in range(0, n_samples, batch_size):
                b_idx = perm[i:i + batch_size]
                optimizer.zero_grad()
                pred = self.model(x_tr_t[b_idx])
                loss = criterion(pred, y_tr_t[b_idx])
                loss.backward()
                nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
                optimizer.step()
                total_loss += loss.item() * len(b_idx)

            avg_train_loss = total_loss / n_samples

            self.model.eval()
            with torch.no_grad():
                val_pred = self.model(x_va_t)
                val_loss = criterion(val_pred, y_va_t).item()

            history.append({"epoch": ep, "train_loss": avg_train_loss, "val_loss": val_loss})

            if val_loss < best_loss:
                best_loss = val_loss
                best_state = {k: v.cpu().clone() for k, v in self.model.state_dict().items()}

        if best_state is not None:
            self.model.load_state_dict(best_state)
            self.model.eval()

        # Compute empirical residual std on validation set
        with torch.no_grad():
            res = (val_pred.cpu().numpy() - y_val)
            self.residual_std = float(np.std(res))

        return {"history": history, "best_val_loss": float(best_loss), "residual_std": self.residual_std}

    def predict_with_mc_dropout(self, last_30d_tensor: np.ndarray, last_price: float, n_mc: int = 200) -> Dict[str, Any]:
        """
        Monte Carlo Dropout inference (200 stochastic forward passes):
        - Estimates epistemic variance sigma^2_MC
        - Combines with aleatoric residual variance sigma^2_eps
        - Produces 90% confidence bounds (z = 1.645)
        """
        # Keep dropout active during evaluation
        self.model.train()
        x_t = torch.tensor(last_30d_tensor.reshape(1, 30, self.d_in), dtype=torch.float32, device=self.device)

        mc_preds = []
        with torch.no_grad():
            for _ in range(n_mc):
                r_pred = self.model(x_t).item()
                mc_preds.append(r_pred)

        mc_preds = np.array(mc_preds)
        mean_return = float(np.mean(mc_preds))
        epistemic_var = float(np.var(mc_preds))
        aleatoric_var = self.residual_std ** 2
        total_std = np.sqrt(epistemic_var + aleatoric_var)

        # 90% confidence bound (1.645 std)
        z = 1.645
        r_lower = mean_return - z * total_std
        r_upper = mean_return + z * total_std

        # Converted price forecasts: P_{t+1} = P_t * exp(r)
        price_pred = last_price * np.exp(mean_return)
        price_lower = last_price * np.exp(r_lower)
        price_upper = last_price * np.exp(r_upper)

        prob_up = float(np.mean(mc_preds > 0))

        return {
            "target_asset": self.target_asset,
            "current_price": float(last_price),
            "predicted_next_price": float(price_pred),
            "predicted_log_return": float(mean_return),
            "return_pct_str": f"{mean_return * 100:+.2f}%",
            "ci_90_price": [float(price_lower), float(price_upper)],
            "ci_90_price_str": f"[{price_lower:,.2f} - {price_upper:,.2f}]",
            "ci_90_return": [float(r_lower), float(r_upper)],
            "prob_increase": float(prob_up),
            "prob_increase_str": f"{prob_up * 100:.1f}%",
            "mc_uncertainty_std": float(total_std),
            "recommendation": "TÍN HIỆU TĂNG GIÁ (MUA/NẮM GIỮ)" if mean_return > 0.002 and prob_up > 0.60 else ("TÍN HIỆU GIẢM GIÁ (PHÒNG VỆ/CHỐT LỜI)" if mean_return < -0.002 and prob_up < 0.40 else "TÍN HIỆU TRUNG TÍNH (QUAN SÁT)")
        }
