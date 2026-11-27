"""
Model Training Script for Tieuluan 2:
- Trains PyTorch DiabetesMLP (13 features, pos_weight BCE, AdamW)
- Trains PyTorch SeqForecaster BiLSTM (30x7 window, Huber loss, AdamW)
- Saves model checkpoints and evaluation metrics to tieuluan2/data/
"""

import os
import sys
import json
sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("tieuluan2"))

import torch
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any, Optional
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, average_precision_score

from tieuluan2.src.deep_learning.diabetes_mlp import DiabetesPredictor, preprocess_diabetes_features
from tieuluan2.src.deep_learning.finance_bilstm import FinancialForecaster, build_financial_features

DATA_DIR = os.path.join("tieuluan2", "data")


def train_diabetes():
    print("=== Training DiabetesMLP (PyTorch) ===")
    csv_path = os.path.join(DATA_DIR, "diabetes_prediction_dataset.csv")
    df = pd.read_csv(csv_path)
    X, y = preprocess_diabetes_features(df)

    # Train (70%), Val (15%), Test (15%)
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.30, random_state=42, stratify=y)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp)

    predictor = DiabetesPredictor()
    res = predictor.fit_and_train(X_train, y_train, X_val, y_val, epochs=25, batch_size=1024, lr=1e-3)

    # Evaluate on Test set
    norm_test = (X_test - predictor.means) / predictor.stds
    x_test_t = torch.tensor(norm_test, dtype=torch.float32, device=predictor.device)
    predictor.model.eval()
    with torch.no_grad():
        logits = predictor.model(x_test_t).cpu().numpy()
        probs = 1.0 / (1.0 + np.exp(-logits))

    threshold = 0.9016
    preds = (probs >= threshold).astype(int)

    test_metrics = {
        "accuracy": float(accuracy_score(y_test, preds)),
        "precision": float(precision_score(y_test, preds)),
        "recall": float(recall_score(y_test, preds)),
        "f1": float(f1_score(y_test, preds)),
        "roc_auc": float(roc_auc_score(y_test, probs)),
        "pr_auc": float(average_precision_score(y_test, probs)),
        "threshold": threshold,
        "parameters_count": sum(p.numel() for p in predictor.model.parameters())
    }

    # Save model and stats
    torch.save(predictor.model.state_dict(), os.path.join(DATA_DIR, "diabetes_mlp.pt"))
    with open(os.path.join(DATA_DIR, "diabetes_scaler.json"), "w") as f:
        json.dump({"means": predictor.means.tolist(), "stds": predictor.stds.tolist()}, f)
    with open(os.path.join(DATA_DIR, "diabetes_metrics.json"), "w") as f:
        json.dump(test_metrics, f, indent=2)

    print(f"DiabetesMLP trained successfully! Parameters: {test_metrics['parameters_count']:,}")
    print(f"Test F1: {test_metrics['f1']:.4f} | ROC-AUC: {test_metrics['roc_auc']:.4f} | PR-AUC: {test_metrics['pr_auc']:.4f}")
    return test_metrics


def train_finance():
    print("\n=== Training BiLSTM SeqForecaster (PyTorch) ===")
    csv_path = os.path.join(DATA_DIR, "finance_market_data.csv")
    df = pd.read_csv(csv_path)

    # Focus on FPT
    target = "FPT"
    X_win, y_win, p_win, feat_cols = build_financial_features(df, target=target, window=30)

    # Temporal split: Train (75%), Val (12.5%), Test (12.5%)
    n = len(X_win)
    n_train = int(n * 0.75)
    n_val = int(n * 0.125)

    X_train, y_train = X_win[:n_train], y_win[:n_train]
    X_val, y_val = X_win[n_train:n_train + n_val], y_win[n_train:n_train + n_val]
    X_test, y_test = X_win[n_train + n_val:], y_win[n_train + n_val:]

    forecaster = FinancialForecaster(target_asset=target)
    res = forecaster.fit_and_train(X_train, y_train, X_val, y_val, epochs=30, batch_size=128, lr=1e-3)

    # Evaluate on Test set
    forecaster.model.eval()
    x_test_t = torch.tensor(X_test, dtype=torch.float32, device=forecaster.device)
    with torch.no_grad():
        test_preds = forecaster.model(x_test_t).cpu().numpy()

    # RMSE of model vs RMSE of naive "no return change" (y_pred = 0)
    rmse_model = np.sqrt(np.mean((test_preds - y_test) ** 2))
    rmse_naive = np.sqrt(np.mean((y_test) ** 2))
    ratio = rmse_model / max(rmse_naive, 1e-6)

    # Directional accuracy: sign(pred) == sign(true)
    dir_acc = np.mean((test_preds > 0) == (y_test > 0))

    test_metrics = {
        "target_asset": target,
        "rmse_model": float(rmse_model),
        "rmse_naive": float(rmse_naive),
        "rmse_ratio": float(ratio),
        "directional_accuracy": float(dir_acc),
        "residual_std": float(forecaster.residual_std),
        "parameters_count": sum(p.numel() for p in forecaster.model.parameters())
    }

    # Save checkpoint and metrics
    torch.save(forecaster.model.state_dict(), os.path.join(DATA_DIR, "finance_bilstm.pt"))
    with open(os.path.join(DATA_DIR, "finance_metrics.json"), "w") as f:
        json.dump(test_metrics, f, indent=2)

    print(f"BiLSTM trained successfully! Parameters: {test_metrics['parameters_count']:,}")
    print(f"Test RMSE Ratio (Model/Naive): {test_metrics['rmse_ratio']:.4f} | Directional Acc: {test_metrics['directional_accuracy']:.2%}")
    return test_metrics


if __name__ == "__main__":
    train_diabetes()
    train_finance()
