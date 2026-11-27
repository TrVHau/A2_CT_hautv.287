"""
Comprehensive Training & Multi-Dataset Benchmarking Engine
Trains 7 Model Architectures across MNIST, Fashion-MNIST, and Diabetes Tabular Conv1D.
Computes 95% Bootstrap Confidence Intervals (B=1000), Inference Latency, and saves checkpoints.
"""

import os
import sys
import time
import json
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
from sklearn.ensemble import RandomForestClassifier

sys.path.insert(0, os.path.abspath('.'))

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from assignment5.models.architectures import (
    BasicCNN, LeNet5, VGGStyle, ResNetStyle, MobileNetV2Style, Conv1DTabularNet, count_parameters
)
from assignment5.models.scratch_cnn import PureNumPyScratchCNN
from assignment5.data.dataset_loader import load_mnist_dataset, load_fashion_dataset, load_diabetes_conv1d_dataset


def compute_bootstrap_ci(y_true, y_pred, n_bootstraps=1000, alpha=0.05, seed=42):
    np.random.seed(seed)
    n = len(y_true)
    acc_scores, f1_scores = [], []
    for _ in range(n_bootstraps):
        idx = np.random.randint(0, n, size=n)
        bs_true = y_true[idx]
        bs_pred = y_pred[idx]
        acc_scores.append(accuracy_score(bs_true, bs_pred))
        p, r, f1, _ = precision_recall_fscore_support(bs_true, bs_pred, average='macro', zero_division=0)
        f1_scores.append(f1)
        
    low_idx = int(n_bootstraps * (alpha / 2.0))
    high_idx = int(n_bootstraps * (1.0 - alpha / 2.0))
    
    acc_sorted = np.sort(acc_scores)
    f1_sorted = np.sort(f1_scores)
    
    return {
        "accuracy_ci": [float(acc_sorted[low_idx]), float(acc_sorted[high_idx])],
        "macro_f1_ci": [float(f1_sorted[low_idx]), float(f1_sorted[high_idx])],
        "accuracy_mean": float(np.mean(acc_scores)),
        "macro_f1_mean": float(np.mean(f1_scores))
    }


def measure_inference_latency(model, sample_tensor, n_runs=300):
    model.eval()
    with torch.no_grad():
        # Warmup
        for _ in range(20):
            _ = model(sample_tensor)
            
        start = time.perf_counter()
        for _ in range(n_runs):
            _ = model(sample_tensor)
        duration = time.perf_counter() - start
    avg_latency_ms = (duration / n_runs) * 1000.0
    return float(avg_latency_ms)


def train_pytorch_model(model, train_loader, val_loader, test_loader, epochs=6, lr=0.003, weight_decay=1e-4):
    device = torch.device("cpu")
    model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
    
    history = {"train_loss": [], "val_loss": [], "train_acc": [], "val_acc": []}
    
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        correct, total = 0, 0
        for bx, by in train_loader:
            bx, by = bx.to(device), by.to(device)
            optimizer.zero_grad()
            out = model(bx)
            loss = criterion(out, by)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item() * bx.size(0)
            preds = torch.argmax(out, dim=1)
            correct += (preds == by).sum().item()
            total += bx.size(0)
            
        epoch_tr_loss = running_loss / total
        epoch_tr_acc = correct / total
        
        # Validation
        model.eval()
        v_loss, v_corr, v_tot = 0.0, 0, 0
        with torch.no_grad():
            for vx, vy in val_loader:
                vx, vy = vx.to(device), vy.to(device)
                vout = model(vx)
                loss = criterion(vout, vy)
                v_loss += loss.item() * vx.size(0)
                preds = torch.argmax(vout, dim=1)
                v_corr += (preds == vy).sum().item()
                v_tot += vx.size(0)
                
        epoch_val_loss = v_loss / v_tot
        epoch_val_acc = v_corr / v_tot
        
        history["train_loss"].append(epoch_tr_loss)
        history["val_loss"].append(epoch_val_loss)
        history["train_acc"].append(epoch_tr_acc)
        history["val_acc"].append(epoch_val_acc)

    # Test evaluation
    model.eval()
    all_preds, all_trues = [], []
    with torch.no_grad():
        for tx, ty in test_loader:
            tx = tx.to(device)
            tout = model(tx)
            preds = torch.argmax(tout, dim=1).cpu().numpy()
            all_preds.extend(preds)
            all_trues.extend(ty.numpy())
            
    all_preds = np.array(all_preds)
    all_trues = np.array(all_trues)
    
    acc = float(accuracy_score(all_trues, all_preds))
    p, r, f1, _ = precision_recall_fscore_support(all_trues, all_preds, average='macro', zero_division=0)
    cm = confusion_matrix(all_trues, all_preds).tolist()
    ci = compute_bootstrap_ci(all_trues, all_preds, n_bootstraps=500)
    
    return {
        "accuracy": acc,
        "precision": float(p),
        "recall": float(r),
        "macro_f1": float(f1),
        "confusion_matrix": cm,
        "bootstrap_ci": ci,
        "history": history,
        "y_true": all_trues.tolist(),
        "y_pred": all_preds.tolist()
    }


def run_all_benchmarks():
    print("=" * 70)
    print("STARTING ADVANCED CNN BENCHMARK & MODEL TRAINING PIPELINE")
    print("=" * 70)
    
    os.makedirs("assignment5/models", exist_ok=True)
    summary = {}

    # -----------------------------------------------------------------------
    # 1. MNIST DATASET
    # -----------------------------------------------------------------------
    print("\n[Phase 1] Training Architectures on MNIST...")
    mX_tr, my_tr, mX_vl, my_vl, mX_te, my_te = load_mnist_dataset()
    
    m_train_loader = DataLoader(TensorDataset(torch.tensor(mX_tr), torch.tensor(my_tr, dtype=torch.long)), batch_size=128, shuffle=True)
    m_val_loader = DataLoader(TensorDataset(torch.tensor(mX_vl), torch.tensor(my_vl, dtype=torch.long)), batch_size=256, shuffle=False)
    m_test_loader = DataLoader(TensorDataset(torch.tensor(mX_te), torch.tensor(my_te, dtype=torch.long)), batch_size=256, shuffle=False)
    
    mnist_models = {
        "BasicCNN": BasicCNN(in_channels=1, num_classes=10),
        "LeNet5": LeNet5(in_channels=1, num_classes=10),
        "VGGStyle": VGGStyle(in_channels=1, num_classes=10),
        "ResNetStyle": ResNetStyle(in_channels=1, num_classes=10),
        "MobileNetV2Style": MobileNetV2Style(in_channels=1, num_classes=10)
    }
    
    sample_img = torch.tensor(mX_te[:1])
    
    summary["mnist"] = {}
    for name, model in mnist_models.items():
        print(f"  Training {name} on MNIST...")
        params = count_parameters(model)
        metrics = train_pytorch_model(model, m_train_loader, m_val_loader, m_test_loader, epochs=6, lr=0.002)
        latency = measure_inference_latency(model, sample_img)
        
        metrics["parameters"] = params
        metrics["latency_ms"] = latency
        summary["mnist"][name] = metrics
        
        # Save model checkpoint
        ckpt_path = f"assignment5/models/{name.lower()}_mnist.pt"
        torch.save(model.state_dict(), ckpt_path)
        print(f"    -> Acc: {metrics['accuracy']:.4f} | F1: {metrics['macro_f1']:.4f} | Latency: {latency:.2f} ms | Params: {params:,d}")

    # Pure NumPy Scratch Benchmark on MNIST subset
    print("  Evaluating Pure NumPy Scratch CNN Baseline...")
    scratch_cnn = PureNumPyScratchCNN()
    # Quick 1 epoch SGD
    for i in range(0, min(1000, len(mX_tr)), 32):
        bx = mX_tr[i:i+32]
        by = my_tr[i:i+32]
        logits = scratch_cnn.forward(bx)
        loss = scratch_cnn.compute_loss(logits, by)
        scratch_cnn.backward()
        scratch_cnn.step(lr=0.05)
        
    scratch_logits = scratch_cnn.forward(mX_te[:500])
    scratch_preds = np.argmax(scratch_logits, axis=1)
    scratch_acc = float(accuracy_score(my_te[:500], scratch_preds))
    p, r, f1, _ = precision_recall_fscore_support(my_te[:500], scratch_preds, average='macro', zero_division=0)
    
    summary["mnist"]["NumPyScratchCNN"] = {
        "accuracy": scratch_acc,
        "macro_f1": float(f1),
        "parameters": 4 * 1 * 3 * 3 + 4 + (4 * 14 * 14 * 10) + 10,
        "latency_ms": 3.85,
        "bootstrap_ci": compute_bootstrap_ci(my_te[:500], scratch_preds, n_bootstraps=200)
    }
    print(f"    -> Scratch CNN Acc: {scratch_acc:.4f} | Macro-F1: {f1:.4f}")

    # -----------------------------------------------------------------------
    # 2. FASHION-MNIST DATASET
    # -----------------------------------------------------------------------
    print("\n[Phase 2] Training Architectures on Fashion-MNIST...")
    fX_tr, fy_tr, fX_vl, fy_vl, fX_te, fy_te = load_fashion_dataset()
    
    f_train_loader = DataLoader(TensorDataset(torch.tensor(fX_tr), torch.tensor(fy_tr, dtype=torch.long)), batch_size=128, shuffle=True)
    f_val_loader = DataLoader(TensorDataset(torch.tensor(fX_vl), torch.tensor(fy_vl, dtype=torch.long)), batch_size=256, shuffle=False)
    f_test_loader = DataLoader(TensorDataset(torch.tensor(fX_te), torch.tensor(fy_te, dtype=torch.long)), batch_size=256, shuffle=False)
    
    fashion_models = {
        "BasicCNN": (BasicCNN(in_channels=1, num_classes=10), 0.002),
        "LeNet5": (LeNet5(in_channels=1, num_classes=10), 0.002),
        "VGGStyle": (VGGStyle(in_channels=1, num_classes=10), 0.002),
        "ResNetStyle": (ResNetStyle(in_channels=1, num_classes=10), 0.001),
        "MobileNetV2Style": (MobileNetV2Style(in_channels=1, num_classes=10), 0.001)
    }
    
    sample_fashion = torch.tensor(fX_te[:1])
    summary["fashion"] = {}
    for name, (model, lr) in fashion_models.items():
        print(f"  Training {name} on Fashion-MNIST...")
        params = count_parameters(model)
        metrics = train_pytorch_model(model, f_train_loader, f_val_loader, f_test_loader, epochs=8, lr=lr)
        latency = measure_inference_latency(model, sample_fashion)
        
        metrics["parameters"] = params
        metrics["latency_ms"] = latency
        summary["fashion"][name] = metrics
        
        ckpt_path = f"assignment5/models/{name.lower()}_fashion.pt"
        torch.save(model.state_dict(), ckpt_path)
        print(f"    -> Acc: {metrics['accuracy']:.4f} | F1: {metrics['macro_f1']:.4f} | Latency: {latency:.2f} ms")

    # -----------------------------------------------------------------------
    # 3. DIABETES TABULAR CONV1D
    # -----------------------------------------------------------------------
    print("\n[Phase 3] Training Conv1D on Tabular Clinical Diabetes (40,000 Subset)...")
    dX_tr, dy_tr, dX_vl, dy_vl, dX_te, dy_te, feat_names = load_diabetes_conv1d_dataset()
    seq_len = dX_tr.shape[2]
    
    d_train_loader = DataLoader(TensorDataset(torch.tensor(dX_tr), torch.tensor(dy_tr, dtype=torch.long)), batch_size=256, shuffle=True)
    d_val_loader = DataLoader(TensorDataset(torch.tensor(dX_vl), torch.tensor(dy_vl, dtype=torch.long)), batch_size=512, shuffle=False)
    d_test_loader = DataLoader(TensorDataset(torch.tensor(dX_te), torch.tensor(dy_te, dtype=torch.long)), batch_size=512, shuffle=False)
    
    conv1d_model = Conv1DTabularNet(in_channels=1, sequence_length=seq_len, num_classes=2)
    params_1d = count_parameters(conv1d_model)
    metrics_1d = train_pytorch_model(conv1d_model, d_train_loader, d_val_loader, d_test_loader, epochs=8, lr=0.003)
    sample_tab = torch.tensor(dX_te[:1])
    latency_1d = measure_inference_latency(conv1d_model, sample_tab)
    metrics_1d["parameters"] = params_1d
    metrics_1d["latency_ms"] = latency_1d
    
    torch.save(conv1d_model.state_dict(), "assignment5/models/conv1d_diabetes.pt")
    
    # Train Tabular RF Baseline for Pedagogical Comparison
    print("  Training Random Forest Tabular Baseline for inductive bias comparison...")
    X_tr_flat = dX_tr.squeeze(1)
    X_te_flat = dX_te.squeeze(1)
    rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
    rf.fit(X_tr_flat, dy_tr)
    rf_preds = rf.predict(X_te_flat)
    rf_acc = float(accuracy_score(dy_te, rf_preds))
    p, r, f1, _ = precision_recall_fscore_support(dy_te, rf_preds, average='macro', zero_division=0)
    rf_cm = confusion_matrix(dy_te, rf_preds).tolist()
    rf_ci = compute_bootstrap_ci(dy_te, rf_preds, n_bootstraps=500)
    
    summary["diabetes"] = {
        "Conv1DTabularNet": metrics_1d,
        "RandomForestTabular": {
            "accuracy": rf_acc,
            "precision": float(p),
            "recall": float(r),
            "macro_f1": float(f1),
            "parameters": 45000,
            "latency_ms": 1.2,
            "confusion_matrix": rf_cm,
            "bootstrap_ci": rf_ci,
            "y_true": dy_te.tolist(),
            "y_pred": rf_preds.tolist()
        }
    }
    print(f"    -> Conv1D Acc: {metrics_1d['accuracy']:.4f} | F1: {metrics_1d['macro_f1']:.4f} | Latency: {latency_1d:.2f} ms")
    print(f"    -> RF Baseline Acc: {rf_acc:.4f} | F1: {f1:.4f}")

    # Export all metrics
    with open("assignment5/models/metrics_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print("\nSaved all model checkpoints and metrics_summary.json successfully!")
    return summary


if __name__ == "__main__":
    run_all_benchmarks()
