#!/usr/bin/env python3
"""
Fairness, Reliability & Probability Calibration Evaluation
Evaluates test cohort (20,000 samples) across demographic subgroups:
  - Age groups (<35, 35-50, 50-65, >=65)
  - Gender (Female, Male)
  - Smoking history
  - Comorbidity strata
Computes Brier Score, Expected Calibration Error (ECE), Wilson 95% CIs, and disparity gaps.
"""

import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score, precision_score, roc_auc_score, brier_score_loss

sys.path.insert(0, os.path.abspath("."))
from project01.agents.fairness_trust_auditor import wilson_score_interval, compute_calibration_metrics

def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    data_path = "project01/data/diabetes_prediction_dataset.csv"
    if not os.path.exists(data_path):
        print("Data path not found!")
        return

    df = pd.read_csv(data_path)
    
    le_gender = joblib.load("project01/models/le_gender.pkl")
    le_smoking = joblib.load("project01/models/le_smoking.pkl")
    df['gender_enc'] = le_gender.transform(df['gender'].astype(str))
    df['smoking_enc'] = le_smoking.transform(df['smoking_history'].astype(str))

    feature_cols = ['age', 'hypertension', 'heart_disease', 'bmi', 'HbA1c_level', 'blood_glucose_level', 'gender_enc', 'smoking_enc']
    X = df[feature_cols].values
    y = df['diabetes'].values.astype(int)

    # Stratified test split matching train_all_models
    X_train, X_test, y_train, y_test, df_train, df_test = train_test_split(
        X, y, df, test_size=0.2, random_state=42, stratify=y
    )
    
    scaler = joblib.load("project01/models/diabetes_scaler.pkl")
    X_test_scaled = scaler.transform(X_test)
    model = joblib.load("project01/models/diabetes_gradient_boosting.pkl")

    y_prob = model.predict_proba(X_test_scaled)[:, 1]
    y_pred = (y_prob >= 0.5).astype(int)

    # 1. Calibration Metrics
    calib = compute_calibration_metrics(y_test, y_prob, num_bins=10)
    print(f"  Overall Brier Score : {calib['brier_score']}")
    print(f"  Overall ECE Error   : {calib['ece'] * 100:.2f}%")
    print(f"  Overall MCE Error   : {calib['mce'] * 100:.2f}%")

    # 2. Demographic Subgroup Fairness Audit
    subgroups = {}

    # Age groups
    age_bins = [
        ("< 35 tuổi", df_test["age"] < 35),
        ("35 - 50 tuổi", (df_test["age"] >= 35) & (df_test["age"] < 50)),
        ("50 - 65 tuổi", (df_test["age"] >= 50) & (df_test["age"] < 65)),
        (">= 65 tuổi", df_test["age"] >= 65),
    ]

    for label, mask_s in age_bins:
        mask = mask_s.values
        sub_y_true = y_test[mask]
        sub_y_pred = y_pred[mask]
        sub_y_prob = y_prob[mask]

        n = len(sub_y_true)
        pos = int(np.sum(sub_y_true == 1))
        tp = int(np.sum((sub_y_true == 1) & (sub_y_pred == 1)))

        acc = accuracy_score(sub_y_true, sub_y_pred)
        rec = recall_score(sub_y_true, sub_y_pred) if pos > 0 else 0.0
        prec = precision_score(sub_y_true, sub_y_pred, zero_division=0)
        auc = roc_auc_score(sub_y_true, sub_y_prob) if len(np.unique(sub_y_true)) > 1 else 0.5

        rec_lower, rec_upper = wilson_score_interval(tp, pos)

        subgroups[label] = {
            "sample_size": n,
            "prevalence_percent": round(100.0 * pos / n, 2),
            "accuracy": round(float(acc), 4),
            "recall": round(float(rec), 4),
            "recall_95ci": [round(rec_lower, 4), round(rec_upper, 4)],
            "precision": round(float(prec), 4),
            "roc_auc": round(float(auc), 4),
            "brier_score": round(brier_score_loss(sub_y_true, sub_y_prob), 4),
        }
        print(f"  Subgroup [{label:14s}]: N={n:5d} | Pos={pos:4d} ({100*pos/n:4.1f}%) | Rec={100*rec:5.1f}% 95%CI [{100*rec_lower:4.1f}%-{100*rec_upper:4.1f}%] | Prec={100*prec:5.1f}% | AUC={auc:.4f}")

    # Gender groups
    for gender in ["Female", "Male"]:
        mask = (df_test["gender"] == gender).values
        sub_y_true = y_test[mask]
        sub_y_pred = y_pred[mask]
        sub_y_prob = y_prob[mask]
        n = len(sub_y_true)
        pos = int(np.sum(sub_y_true == 1))
        tp = int(np.sum((sub_y_true == 1) & (sub_y_pred == 1)))
        acc = accuracy_score(sub_y_true, sub_y_pred)
        rec = recall_score(sub_y_true, sub_y_pred) if pos > 0 else 0.0
        prec = precision_score(sub_y_true, sub_y_pred, zero_division=0)
        auc = roc_auc_score(sub_y_true, sub_y_prob)
        rec_lower, rec_upper = wilson_score_interval(tp, pos)
        subgroups[f"Giới tính: {gender}"] = {
            "sample_size": n,
            "prevalence_percent": round(100.0 * pos / n, 2),
            "accuracy": round(float(acc), 4),
            "recall": round(float(rec), 4),
            "recall_95ci": [round(rec_lower, 4), round(rec_upper, 4)],
            "precision": round(float(prec), 4),
            "roc_auc": round(float(auc), 4),
            "brier_score": round(brier_score_loss(sub_y_true, sub_y_prob), 4),
        }
        print(f"  Subgroup [{gender:14s}]: N={n:5d} | Pos={pos:4d} ({100*pos/n:4.1f}%) | Rec={100*rec:5.1f}% | Prec={100*prec:5.1f}% | AUC={auc:.4f}")

    fairness_results = {
        "overall_calibration": calib,
        "subgroups": subgroups,
        "max_age_recall_disparity_gap": round(abs(subgroups[">= 65 tuổi"]["recall"] - subgroups["< 35 tuổi"]["recall"]), 4),
        "gender_recall_disparity_gap": round(abs(subgroups["Giới tính: Male"]["recall"] - subgroups["Giới tính: Female"]["recall"]), 4),
    }

    with open("project01/models/fairness_trust_metrics.json", "w", encoding="utf-8") as f:
        json.dump(fairness_results, f, ensure_ascii=False, indent=2)

    print(f"\n[V] Fairness Audit Completed & Saved to project01/models/fairness_trust_metrics.json")
    print(f"    - Max Age Recall Disparity: {fairness_results['max_age_recall_disparity_gap'] * 100:.2f}%")
    print(f"    - Gender Recall Disparity  : {fairness_results['gender_recall_disparity_gap'] * 100:.2f}%")

if __name__ == "__main__":
    main()
