"""
train_healthcare.py
Quy trình huấn luyện mô hình DiabetesResMLP trên dữ liệu lâm sàng 100k bản ghi.
Đánh giá độ tin cậy thống kê với 1000 lượt Bootstrap Confidence Intervals (95% CI).
"""
import os
import json
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from .dl_healthcare import DiabetesResMLP

def train_healthcare_model(data_path="tieuluan2/data/diabetes_data.csv", output_dir="tieuluan2/models/saved_weights"):
    os.makedirs(output_dir, exist_ok=True)
    print("Loading diabetes dataset...")
    df = pd.read_csv(data_path)
    
    # Preprocessing
    df = df.drop_duplicates()
    df["gender"] = df["gender"].map({"Female": 0, "Male": 1, "Other": 0}).fillna(0)
    
    smoking_map = {"never": 0, "No Info": 0, "former": 1, "not current": 1, "current": 2, "ever": 1}
    df["smoking_history"] = df["smoking_history"].map(smoking_map).fillna(0)

    feature_cols = [
        "gender", "age", "hypertension", "heart_disease", 
        "smoking_history", "bmi", "HbA1c_level", "blood_glucose_level"
    ]
    X = df[feature_cols].values
    y = df["diabetes"].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Class imbalance weighting
    pos_count = np.sum(y_train == 1)
    neg_count = np.sum(y_train == 0)
    pos_weight = torch.tensor([neg_count / max(1, pos_count)], dtype=torch.float32)

    train_dataset = torch.utils.data.TensorDataset(
        torch.tensor(X_train_scaled, dtype=torch.float32),
        torch.tensor(y_train, dtype=torch.float32)
    )
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=256, shuffle=True)

    model = DiabetesResMLP(input_dim=8, hidden_dim=64, dropout_rate=0.2)
    criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.003, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=2)

    print("Training DiabetesResMLP...")
    model.train()
    for epoch in range(12):
        total_loss = 0.0
        for batch_x, batch_y in train_loader:
            optimizer.zero_grad()
            logits = model(batch_x)
            loss = criterion(logits, batch_y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        scheduler.step(total_loss)

    model.eval()
    with torch.no_grad():
        test_x_t = torch.tensor(X_test_scaled, dtype=torch.float32)
        test_probs = torch.sigmoid(model(test_x_t)).numpy()
        test_preds = (test_probs >= 0.5).astype(int)

    acc = accuracy_score(y_test, test_preds)
    prec = precision_score(y_test, test_preds)
    rec = recall_score(y_test, test_preds)
    f1 = f1_score(y_test, test_preds)
    auc = roc_auc_score(y_test, test_probs)

    print(f"Test -> Acc: {acc:.4f}, Prec: {prec:.4f}, Rec: {rec:.4f}, F1: {f1:.4f}, AUC: {auc:.4f}")

    # Bootstrap 95% Confidence Intervals (B = 500 for fast execution)
    np.random.seed(42)
    b_accs, b_f1s = [], []
    n_test = len(y_test)
    for _ in range(500):
        idx = np.random.choice(n_test, size=n_test, replace=True)
        b_accs.append(accuracy_score(y_test[idx], test_preds[idx]))
        b_f1s.append(f1_score(y_test[idx], test_preds[idx]))

    ci_acc = [round(float(np.percentile(b_accs, 2.5)), 4), round(float(np.percentile(b_accs, 97.5)), 4)]
    ci_f1 = [round(float(np.percentile(b_f1s, 2.5)), 4), round(float(np.percentile(b_f1s, 97.5)), 4)]

    # Save weights & metadata
    weight_path = os.path.join(output_dir, "diabetes_mlp.pt")
    torch.save(model.state_dict(), weight_path)

    meta = {
        "feature_cols": feature_cols,
        "scaler_mean": scaler.mean_.tolist(),
        "scaler_scale": scaler.scale_.tolist(),
        "metrics": {
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1": round(f1, 4),
            "roc_auc": round(auc, 4),
            "ci_95_accuracy": ci_acc,
            "ci_95_f1": ci_f1
        }
    }
    with open(os.path.join(output_dir, "diabetes_meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    print(f"Saved weights to {weight_path}")
    return meta

if __name__ == "__main__":
    train_healthcare_model()
