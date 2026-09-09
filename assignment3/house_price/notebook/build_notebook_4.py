#!/usr/bin/env python3
"""Build house price Notebook 4 - Model Comparison."""
import json, os

def md(s): return {"cell_type":"markdown","metadata":{},"source":s}
def code(s): return {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":s}

cells=[]

cells.append(md(
"# DỰ ĐOÁN GIÁ NHÀ VN — SO SÁNH 4 MÔ HÌNH\n"
"**Ba ML (Ridge, Tree, Forest) vs PyTorch MLP**"
))

cells.append(code(
"import numpy as np\n"
"import pandas as pd\n"
"import matplotlib.pyplot as plt\n"
"import joblib, os\n"
"import torch, torch.nn as nn\n"
"from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score\n"
"import matplotlib\n"
"matplotlib.use('Agg')\n"
"\n"
"MODEL_DIR = os.path.join('..', 'models')\n"
"data = np.load(os.path.join(MODEL_DIR, 'preprocessed_data.npz'))\n"
"X_test, y_test = data['X_test'], data['y_test']\n"
"y_test_real = np.expm1(y_test)\n"
"\n"
"models = ['Ridge Regression', 'Decision Tree', 'Random Forest']\n"
"results = []\n"
"\n"
"for m in models:\n"
"    model = joblib.load(os.path.join(MODEL_DIR, f\"hp_{m.lower().replace(' ', '_')}.pkl\"))\n"
"    preds = np.expm1(model.predict(X_test))\n"
"    results.append({\n"
"        'Model': m,\n"
"        'MAE (Tr VNĐ)': mean_absolute_error(y_test_real, preds),\n"
"        'RMSE (Tr VNĐ)': np.sqrt(mean_squared_error(y_test_real, preds)),\n"
"        'R2': r2_score(y_test_real, preds)\n"
"    })\n"
"\n"
"# Dữ liệu DL\n"
"dl_preds = np.load(os.path.join(MODEL_DIR, 'hp_dl_preds.npz'))['preds_real']\n"
"results.append({\n"
"    'Model': 'Deep Learning (PyTorch)',\n"
"    'MAE (Tr VNĐ)': mean_absolute_error(y_test_real, dl_preds),\n"
"    'RMSE (Tr VNĐ)': np.sqrt(mean_squared_error(y_test_real, dl_preds)),\n"
"    'R2': r2_score(y_test_real, dl_preds)\n"
"})\n"
"\n"
"df_comp = pd.DataFrame(results)\n"
"print(df_comp)\n"
"\n"
"fig, ax = plt.subplots(figsize=(10,6))\n"
"df_comp.set_index('Model')[['R2']].plot(kind='bar', ax=ax, rot=15)\n"
"ax.set_ylim(0, 1)\n"
"ax.set_title('So Sánh R2 Score (Càng gần 1 càng tốt)')\n"
"plt.tight_layout(); plt.show()\n"
))

cells.append(md(
"## Kết luận\n"
"Random Forest thường đạt kết quả cao nhất (R2 lớn nhất, MAE/RMSE nhỏ nhất) do tính chất của Regression trên Dữ liệu Bảng (Tabular Data). Deep Learning cần cấu hình/tuning phức tạp hơn để bắt kịp cây quyết định trên kiểu dữ liệu này."
))

nb = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}}, "nbformat": 4, "nbformat_minor": 5}
out = os.path.join(os.path.dirname(__file__), '4_model_comparison.ipynb')
with open(out, 'w', encoding='utf-8') as f: json.dump(nb, f, ensure_ascii=False, indent=1)
print('Saved', out)
