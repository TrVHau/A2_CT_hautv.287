#!/usr/bin/env python3
"""Build house price Notebook 3 - Deep Learning."""
import json, os

def md(s): return {"cell_type":"markdown","metadata":{},"source":s}
def code(s): return {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":s}

cells=[]

cells.append(md(
"# DỰ ĐOÁN GIÁ NHÀ VN — DEEP LEARNING (PYTORCH)\n"
"**Bài toán:** Hồi quy (Regression)\n"
"---\n"
"**Mô hình:** Tương tự Deep Learning MLP."
))

cells.append(code(
"import numpy as np\n"
"import pandas as pd\n"
"import joblib, os, time\n"
"import torch\n"
"import torch.nn as nn\n"
"import torch.optim as optim\n"
"from torch.utils.data import TensorDataset, DataLoader\n"
"from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score\n"
"\n"
"MODEL_DIR = os.path.join('..', 'models')\n"
"data = np.load(os.path.join(MODEL_DIR, 'preprocessed_data.npz'))\n"
"X_train, y_train = data['X_train'], data['y_train']\n"
"X_test, y_test = data['X_test'], data['y_test']\n"
"\n"
"X_tr_t = torch.tensor(X_train, dtype=torch.float32)\n"
"y_tr_t = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)\n"
"X_te_t = torch.tensor(X_test, dtype=torch.float32)\n"
"\n"
"train_loader = DataLoader(TensorDataset(X_tr_t, y_tr_t), batch_size=256, shuffle=True)\n"
))

cells.append(code(
"class RegressorMLP(nn.Module):\n"
"    def __init__(self, in_features):\n"
"        super().__init__()\n"
"        self.net = nn.Sequential(\n"
"            nn.Linear(in_features, 64),\n"
"            nn.ReLU(),\n"
"            nn.Linear(64, 32),\n"
"            nn.ReLU(),\n"
"            nn.Linear(32, 1)\n"
"        )\n"
"    def forward(self, x):\n"
"        return self.net(x)\n"
"\n"
"torch.manual_seed(42)\n"
"model = RegressorMLP(X_train.shape[1])\n"
"criterion = nn.MSELoss()\n"
"optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4)\n"
"\n"
"for epoch in range(1, 21):\n"
"    model.train()\n"
"    for xb, yb in train_loader:\n"
"        optimizer.zero_grad()\n"
"        loss = criterion(model(xb), yb)\n"
"        loss.backward()\n"
"        optimizer.step()\n"
"    if epoch % 5 == 0: print(f'Epoch {epoch}: Loss = {loss.item():.4f}')\n"
))

cells.append(code(
"model.eval()\n"
"with torch.no_grad():\n"
"    preds = model(X_te_t).numpy().ravel()\n""preds = np.clip(preds, 0, 15)\n""\n"
"y_test_real = np.expm1(y_test)\n"
"preds_real = np.expm1(preds)\n"
"mae = mean_absolute_error(y_test_real, preds_real)\n"
"rmse = np.sqrt(mean_squared_error(y_test_real, preds_real))\n"
"r2 = r2_score(y_test_real, preds_real)\n"
"print(f\"Deep Learning -> MAE: {mae:.2f}, RMSE: {rmse:.2f}, R2: {r2:.4f}\")\n"
"\n"
"torch.save(model.state_dict(), os.path.join(MODEL_DIR, 'hp_mlp_best.pth'))\n"
"np.savez_compressed(os.path.join(MODEL_DIR, 'hp_dl_preds.npz'), preds_real=preds_real)\n"
"print('Saved PyTorch Model.')\n"
))

nb = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}}, "nbformat": 4, "nbformat_minor": 5}
out = os.path.join(os.path.dirname(__file__), '3_deep_learning.ipynb')
with open(out, 'w', encoding='utf-8') as f: json.dump(nb, f, ensure_ascii=False, indent=1)
print('Saved', out)
