#!/usr/bin/env python3
"""Build Customer Behavior Notebook 2 - 3 Basic ML Models."""
import json, os

def md(s): return {"cell_type":"markdown","metadata":{},"source":s}
def code(s): return {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":s}

cells=[]

cells.append(md(
"# PHÂN TÍCH ĐÁNH GIÁ KHÁCH HÀNG — 3 MÔ HÌNH ML CƠ BẢN\n"
"**Bài toán:** Phân loại cảm xúc/khuyến nghị (Binary Classification)\n"
"---\n"
"**3 Mô hình ML:** Multinomial Naive Bayes, Logistic Regression, Random Forest."
))

cells.append(code(
"import numpy as np\n"
"import pandas as pd\n"
"import joblib, os\n"
"from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score\n"
"from sklearn.naive_bayes import MultinomialNB\n"
"from sklearn.linear_model import LogisticRegression\n"
"from sklearn.ensemble import RandomForestClassifier\n"
"\n"
"MODEL_DIR = os.path.join('..', 'models')\n"
"data = np.load(os.path.join(MODEL_DIR, 'tfidf_data.npz'))\n"
"X_train, y_train = data['X_train'], data['y_train']\n"
"X_val, y_val = data['X_val'], data['y_val']\n"
"X_test, y_test = data['X_test'], data['y_test']\n"
"print('Loaded Data:', X_train.shape, X_val.shape, X_test.shape)"
))

cells.append(code(
"def evaluate(model, X_train, y_train, X_test, y_test, name):\n"
"    model.fit(X_train, y_train)\n"
"    y_pred = model.predict(X_test)\n"
"    y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None\n"
"    \n"
"    acc = accuracy_score(y_test, y_pred)\n"
"    prec = precision_score(y_test, y_pred, zero_division=0)\n"
"    rec = recall_score(y_test, y_pred, zero_division=0)\n"
"    f1 = f1_score(y_test, y_pred, zero_division=0)\n"
"    auc = roc_auc_score(y_test, y_prob) if y_prob is not None else 0.5\n"
"    \n"
"    return {\n"
"        'name': name,\n"
"        'model': model,\n"
"        'Accuracy': acc,\n"
"        'Precision': prec,\n"
"        'Recall': rec,\n"
"        'F1-Score': f1,\n"
"        'AUC-ROC': auc,\n"
"        'y_prob': y_prob\n"
"    }\n"
))

cells.append(code(
"res_nb = evaluate(MultinomialNB(), X_train, y_train, X_test, y_test, 'Multinomial Naive Bayes')\n"
"res_lr = evaluate(LogisticRegression(max_iter=500, random_state=42), X_train, y_train, X_test, y_test, 'Logistic Regression')\n"
"res_rf = evaluate(RandomForestClassifier(n_estimators=100, max_depth=15, n_jobs=-1, random_state=42), X_train, y_train, X_test, y_test, 'Random Forest')\n"
"\n"
"res_list = [res_nb, res_lr, res_rf]\n"
"df_comp = pd.DataFrame([{k:v for k,v in r.items() if k not in ['model', 'y_prob']} for r in res_list])\n"
"print(df_comp)\n"
"\n"
"for r in res_list:\n"
"    joblib.dump(r['model'], os.path.join(MODEL_DIR, f\"cb_{r['name'].lower().replace(' ', '_')}.pkl\"))\n"
"print('Saved models.')"
))

nb = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}}, "nbformat": 4, "nbformat_minor": 5}
out = os.path.join(os.path.dirname(__file__), '2_ml_models.ipynb')
with open(out, 'w', encoding='utf-8') as f: json.dump(nb, f, ensure_ascii=False, indent=1)
print('Saved', out)
