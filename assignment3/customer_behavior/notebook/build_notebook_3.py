#!/usr/bin/env python3
"""Build Customer Behavior Notebook 3 - Deep Learning."""
import json, os

def md(s): return {"cell_type":"markdown","metadata":{},"source":s}
def code(s): return {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":s}

cells=[]

cells.append(md(
"# PHÂN TÍCH ĐÁNH GIÁ KHÁCH HÀNG — DEEP LEARNING (PYTORCH MLP)\n"
"**Bài toán:** Phân loại cảm xúc/khuyến nghị (Binary Classification)\n"
"---\n"
"**Mô hình:** Mạng Nơ-ron Phân loại Văn bản (Text Classification MLP with PyTorch)."
))

cells.append(code(
"import numpy as np\n"
"import pandas as pd\n"
"import joblib, os, time\n"
"import torch\n"
"import torch.nn as nn\n"
"import torch.optim as optim\n"
"from torch.utils.data import TensorDataset, DataLoader\n"
"from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score\n"
"\n"
"MODEL_DIR = os.path.join('..', 'models')\n"
"data = np.load(os.path.join(MODEL_DIR, 'tfidf_data.npz'))\n"
"X_train, y_train = data['X_train'], data['y_train']\n"
"X_val, y_val = data['X_val'], data['y_val']\n"
"X_test, y_test = data['X_test'], data['y_test']\n"
"\n"
"X_tr_t = torch.tensor(X_train, dtype=torch.float32)\n"
"y_tr_t = torch.tensor(y_train, dtype=torch.long)\n"
"X_va_t = torch.tensor(X_val, dtype=torch.float32)\n"
"y_va_t = torch.tensor(y_val, dtype=torch.long)\n"
"X_te_t = torch.tensor(X_test, dtype=torch.float32)\n"
"\n"
"train_loader = DataLoader(TensorDataset(X_tr_t, y_tr_t), batch_size=128, shuffle=True)\n"
"val_loader = DataLoader(TensorDataset(X_va_t, y_va_t), batch_size=128, shuffle=False)\n"
))

cells.append(code(
"class TextClassifierMLP(nn.Module):\n"
"    def __init__(self, in_features, num_classes=2):\n"
"        super().__init__()\n"
"        self.net = nn.Sequential(\n"
"            nn.Linear(in_features, 128),\n"
"            nn.BatchNorm1d(128),\n"
"            nn.ReLU(),\n"
"            nn.Dropout(0.3),\n"
"            nn.Linear(128, 32),\n"
"            nn.BatchNorm1d(32),\n"
"            nn.ReLU(),\n"
"            nn.Dropout(0.2),\n"
"            nn.Linear(32, num_classes)\n"
"        )\n"
"    def forward(self, x):\n"
"        return self.net(x)\n"
"\n"
"torch.manual_seed(42)\n"
"model = TextClassifierMLP(X_train.shape[1], num_classes=2)\n"
"criterion = nn.CrossEntropyLoss()\n"
"optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4)\n"
"\n"
"for epoch in range(1, 16):\n"
"    model.train()\n"
"    total_loss = 0.0\n"
"    for xb, yb in train_loader:\n"
"        optimizer.zero_grad()\n"
"        loss = criterion(model(xb), yb)\n"
"        loss.backward()\n"
"        optimizer.step()\n"
"        total_loss += loss.item() * len(xb)\n"
"    \n"
"    model.eval()\n"
"    with torch.no_grad():\n"
"        val_preds = model(X_va_t).argmax(dim=1).numpy()\n"
"        val_acc = accuracy_score(y_val, val_preds)\n"
"    if epoch % 5 == 0 or epoch == 1:\n"
"        print(f'Epoch {epoch:2d}: Train Loss = {total_loss/len(X_train):.4f} | Val Acc = {val_acc:.4f}')\n"
))

cells.append(code(
"model.eval()\n"
"with torch.no_grad():\n"
"    logits = model(X_te_t)\n"
"    probs = torch.softmax(logits, dim=1)[:, 1].numpy()\n"
"    preds = logits.argmax(dim=1).numpy()\n"
"\n"
"acc = accuracy_score(y_test, preds)\n"
"prec = precision_score(y_test, preds, zero_division=0)\n"
"rec = recall_score(y_test, preds, zero_division=0)\n"
"f1 = f1_score(y_test, preds, zero_division=0)\n"
"auc = roc_auc_score(y_test, probs)\n"
"\n"
"print(f\"Deep Learning (PyTorch MLP) -> Acc: {acc:.4f}, Prec: {prec:.4f}, Rec: {rec:.4f}, F1: {f1:.4f}, AUC: {auc:.4f}\")\n"
"\n"
"torch.save(model.state_dict(), os.path.join(MODEL_DIR, 'cb_mlp_best.pth'))\n"
"np.savez_compressed(os.path.join(MODEL_DIR, 'cb_dl_preds.npz'), preds=preds, probs=probs)\n"
"print('Saved PyTorch Model.')\n"
))

nb = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}}, "nbformat": 4, "nbformat_minor": 5}
out = os.path.join(os.path.dirname(__file__), '3_deep_learning.ipynb')
with open(out, 'w', encoding='utf-8') as f: json.dump(nb, f, ensure_ascii=False, indent=1)
print('Saved', out)
