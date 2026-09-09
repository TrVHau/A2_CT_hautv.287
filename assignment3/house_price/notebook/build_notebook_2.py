#!/usr/bin/env python3
"""Build house price Notebook 2 - ML Models."""
import json, os

def md(s): return {"cell_type":"markdown","metadata":{},"source":s}
def code(s): return {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":s}

cells=[]

cells.append(md(
"# DỰ ĐOÁN GIÁ NHÀ VN — 3 MÔ HÌNH ML CƠ BẢN\n"
"**Bài toán:** Hồi quy (Regression)\n"
"---\n"
"**3 Mô hình ML:** Linear Regression (Baseline), Decision Tree Regressor, Random Forest Regressor."
))

cells.append(code(
"import numpy as np\n"
"import pandas as pd\n"
"import matplotlib.pyplot as plt\n"
"import joblib, os\n"
"from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score\n"
"\n"
"MODEL_DIR = os.path.join('..', 'models')\n"
"data = np.load(os.path.join(MODEL_DIR, 'preprocessed_data.npz'))\n"
"X_train, y_train = data['X_train'], data['y_train']\n"
"X_val, y_val = data['X_val'], data['y_val']\n"
"X_test, y_test = data['X_test'], data['y_test']\n"
"print('Loaded Data:', X_train.shape, X_val.shape, X_test.shape)"
))

cells.append(code(
"def evaluate(model, X_train, y_train, X_val, y_val, X_test, y_test, name):\n"
"    model.fit(X_train, y_train)\n"
"    preds = model.predict(X_test)\n"
"    # Giải Log\n"
"    y_test_real = np.expm1(y_test)\n"
"    preds_real = np.expm1(preds)\n"
"    mae = mean_absolute_error(y_test_real, preds_real)\n"
"    rmse = np.sqrt(mean_squared_error(y_test_real, preds_real))\n"
"    r2 = r2_score(y_test_real, preds_real)\n"
"    return {'name': name, 'model': model, 'mae': mae, 'rmse': rmse, 'r2': r2, 'preds_real': preds_real}\n"
))

cells.append(code(
"from sklearn.linear_model import Ridge\n"
"from sklearn.tree import DecisionTreeRegressor\n"
"from sklearn.ensemble import RandomForestRegressor\n"
"\n"
"res_lr = evaluate(Ridge(alpha=1.0), X_train, y_train, X_val, y_val, X_test, y_test, 'Ridge Regression')\n"
"res_dt = evaluate(DecisionTreeRegressor(max_depth=12, random_state=42), X_train, y_train, X_val, y_val, X_test, y_test, 'Decision Tree')\n"
"res_rf = evaluate(RandomForestRegressor(n_estimators=100, max_depth=15, n_jobs=-1, random_state=42), X_train, y_train, X_val, y_val, X_test, y_test, 'Random Forest')\n"
"\n"
"res_list = [res_lr, res_dt, res_rf]\n"
"df_comp = pd.DataFrame([{k:v for k,v in r.items() if k not in ['model', 'preds_real']} for r in res_list])\n"
"print(df_comp)\n"
"\n"
"for r in res_list:\n"
"    joblib.dump(r['model'], os.path.join(MODEL_DIR, f\"hp_{r['name'].lower().replace(' ','_')}.pkl\"))\n"
"print('Saved models.')"
))

nb = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}}, "nbformat": 4, "nbformat_minor": 5}

out = os.path.join(os.path.dirname(__file__), '2_ml_models.ipynb')
with open(out, 'w', encoding='utf-8') as f: json.dump(nb, f, ensure_ascii=False, indent=1)
print('Saved', out)
