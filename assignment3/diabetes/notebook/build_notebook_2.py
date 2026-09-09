#!/usr/bin/env python3
"""Build the diabetes ML models notebook for Assignment 03."""
import json, os

def md(s): return {"cell_type":"markdown","metadata":{},"source":s}
def code(s): return {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":s}

cells=[]

cells.append(md(
"# DỰ ĐOÁN BỆNH TIỂU ĐƯỜNG — 3 MÔ HÌNH ML CƠ BẢN\n"
"\n"
"**Assignment 03 — Neural Networks and Representation Learning**\n"
"\n"
"**Bài toán:** Phân loại nhị phân — so sánh 3 mô hình ML truyền thống\n"
"\n"
"**Mô hình:** Logistic Regression, Decision Tree, Random Forest\n"
"\n"
"---"
))

cells.append(md(
"## 1. Mục tiêu\n"
"\n"
"- Huấn luyện **3 mô hình ML cơ bản** trên dữ liệu đã tiền xử lý từ Notebook 1\n"
"- Đánh giá trên tập **validation** và **test**\n"
"- Lưu mô hình tốt nhất để so sánh với Deep Learning ở Notebook 4\n"
"- Sử dụng metrics: **Accuracy, Precision, Recall, F1-score, AUC-ROC**\n"
"\n"
"Lưu ý: Mất cân bằng lớp đã được xử lý bằng SMOTE trên tập train, validation/test giữ phân bố gốc."
))

cells.append(md(
"## 2. Import & Load dữ liệu tiền xử lý"
))
cells.append(code(
"import matplotlib\n"
"matplotlib.use('Agg')\n"
"import numpy as np\n"
"import pandas as pd\n"
"import matplotlib.pyplot as plt\n"
"import seaborn as sns\n"
"import joblib\n"
"import os\n"
"\n"
"MODEL_DIR = os.path.join('..', 'models')\n"
"\n"
"# Load preprocessed data\n"
"data = np.load(os.path.join(MODEL_DIR, 'preprocessed_data.npz'))\n"
"X_train_res = data['X_train_res']\n"
"y_train_res = data['y_train_res']\n"
"X_val = data['X_val']\n"
"y_val = data['y_val']\n"
"X_test = data['X_test']\n"
"y_test = data['y_test']\n"
"\n"
"print('Train (SMOTE):', X_train_res.shape, '| Val:', X_val.shape, '| Test:', X_test.shape)\n"
"print('Train 0/1:', sum(y_train_res==0), '/', sum(y_train_res==1))\n"
"print('Val 0/1:', sum(y_val==0), '/', sum(y_val==1))\n"
"print('Test 0/1:', sum(y_test==0), '/', sum(y_test==1))"
))

cells.append(code(
"# Load feature names\n"
"feature_names = joblib.load(os.path.join(MODEL_DIR, 'feature_names.pkl'))\n"
"feature_names"
))

cells.append(md(
"## 3. Đánh giá mô hình — Hàm helper"
))
cells.append(code(
"from sklearn.metrics import (accuracy_score, precision_score, recall_score,\n"
"                             f1_score, roc_auc_score, confusion_matrix,\n"
"                             classification_report, RocCurveDisplay)\n"
"from sklearn.model_selection import cross_val_score\n"
"\n"
"def evaluate_model(model, X_train, y_train, X_val, y_val, X_test, y_test, name):\n"
"    \"\"\"Huấn luyện và đánh giá mô hình trên train/val/test.\"\"\"\n"
"    model.fit(X_train, y_train)\n"
"    \n"
"    # Predict\n"
"    y_pred_val = model.predict(X_val)\n"
"    y_pred_test = model.predict(X_test)\n"
"    \n"
"    # Probabilities (cho AUC)\n"
"    y_prob_val = model.predict_proba(X_val)[:, 1] if hasattr(model, 'predict_proba') else None\n"
"    y_prob_test = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None\n"
"    \n"
"    results = {\n"
"        'name': name,\n"
"        'val_acc': accuracy_score(y_val, y_pred_val),\n"
"        'val_prec': precision_score(y_val, y_pred_val, zero_division=0),\n"
"        'val_rec': recall_score(y_val, y_pred_val, zero_division=0),\n"
"        'val_f1': f1_score(y_val, y_pred_val, zero_division=0),\n"
"        'test_acc': accuracy_score(y_test, y_pred_test),\n"
"        'test_prec': precision_score(y_test, y_pred_test, zero_division=0),\n"
"        'test_rec': recall_score(y_test, y_pred_test, zero_division=0),\n"
"        'test_f1': f1_score(y_test, y_pred_test, zero_division=0),\n"
"        'y_pred_test': y_pred_test,\n"
"        'y_prob_test': y_prob_test,\n"
"        'model': model\n"
"    }\n"
"    if y_prob_val is not None:\n"
"        results['val_auc'] = roc_auc_score(y_val, y_prob_val)\n"
"        results['test_auc'] = roc_auc_score(y_test, y_prob_test)\n"
"    \n"
"    return results\n"
"\n"
"def print_metrics(results, prefix=''):\n"
"    print(f\"{prefix}{results['name']}\")\n"
"    print(f\"  Validation:  Acc={results['val_acc']:.4f}  Prec={results['val_prec']:.4f}  Rec={results['val_rec']:.4f}  F1={results['val_f1']:.4f}  AUC={results.get('val_auc',0):.4f}\")\n"
"    print(f\"  Test:        Acc={results['test_acc']:.4f}  Prec={results['test_prec']:.4f}  Rec={results['test_rec']:.4f}  F1={results['test_f1']:.4f}  AUC={results.get('test_auc',0):.4f}\")\n"
"    print()"
))

cells.append(md(
"## 4. Mô hình 1: Logistic Regression (Baseline tuyến tính)\n"
"\n"
"Logistic Regression là baseline tốt cho bài toán phân loại nhị phân. "
"Được sử dụng trong Assignment 02, ta sẽ so sánh lại ở đây."
))
cells.append(code(
"from sklearn.linear_model import LogisticRegression\n"
"\n"
"lr = LogisticRegression(\n"
"    random_state=42,\n"
"    max_iter=1000,\n"
"    class_weight=None,  # SMOTE đã cân bằng\n"
"    solver='lbfgs',\n"
"    C=1.0\n"
")\n"
"\n"
"lr_results = evaluate_model(lr, X_train_res, y_train_res, X_val, y_val, X_test, y_test, 'Logistic Regression')\n"
"print_metrics(lr_results)"
))

cells.append(md(
"### 4.1. Classification report & Confusion matrix (Test)"
))
cells.append(code(
"print('=== TEST Classification Report ===')\n"
"print(classification_report(y_test, lr_results['y_pred_test'], target_names=['No Diabetes', 'Diabetes']))\n"
"\n"
"cm = confusion_matrix(y_test, lr_results['y_pred_test'])\n"
"fig, ax = plt.subplots(figsize=(5,4))\n"
"sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,\n"
"            xticklabels=['No Diabetes', 'Diabetes'],\n"
"            yticklabels=['No Diabetes', 'Diabetes'])\n"
"ax.set_xlabel('Predicted'); ax.set_ylabel('Actual')\n"
"ax.set_title('Confusion Matrix - Logistic Regression (Test)')\n"
"plt.tight_layout(); plt.show()"
))

cells.append(md(
"## 5. Mô hình 2: Decision Tree\n"
"\n"
"Decision Tree có khả năng mô hình hóa phi tuyến tính, dễ giải thích. "
"Sử dụng entropy hoặc gini làm criterion."
))
cells.append(code(
"from sklearn.tree import DecisionTreeClassifier\n"
"\n"
"dt = DecisionTreeClassifier(\n"
"    random_state=42,\n"
"    criterion='entropy',\n"
"    max_depth=10,\n"
"    min_samples_split=10,\n"
"    min_samples_leaf=5,\n"
"    class_weight=None\n"
")\n"
"\n"
"dt_results = evaluate_model(dt, X_train_res, y_train_res, X_val, y_val, X_test, y_test, 'Decision Tree')\n"
"print_metrics(dt_results)"
))

cells.append(md(
"### 5.1. Classification report & Confusion matrix (Test)"
))
cells.append(code(
"print('=== TEST Classification Report ===')\n"
"print(classification_report(y_test, dt_results['y_pred_test'], target_names=['No Diabetes', 'Diabetes']))\n"
"\n"
"cm = confusion_matrix(y_test, dt_results['y_pred_test'])\n"
"fig, ax = plt.subplots(figsize=(5,4))\n"
"sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,\n"
"            xticklabels=['No Diabetes', 'Diabetes'],\n"
"            yticklabels=['No Diabetes', 'Diabetes'])\n"
"ax.set_xlabel('Predicted'); ax.set_ylabel('Actual')\n"
"ax.set_title('Confusion Matrix - Decision Tree (Test)')\n"
"plt.tight_layout(); plt.show()"
))

cells.append(md(
"### 5.2. Feature Importance"
))
cells.append(code(
"dt_importance = pd.DataFrame({\n"
"    'feature': feature_names,\n"
"    'importance': dt.feature_importances_\n"
"}).sort_values('importance', ascending=False)\n"
"\n"
"plt.figure(figsize=(8, 5))\n"
"sns.barplot(data=dt_importance, x='importance', y='feature')\n"
"plt.title('Feature Importance - Decision Tree')\n"
"plt.tight_layout(); plt.show()\n"
"\n"
"print(dt_importance.to_string(index=False))"
))

cells.append(md(
"## 6. Mô hình 3: Random Forest\n"
"\n"
"Random Forest là ensemble của nhiều Decision Tree, thường cho hiệu năng tốt và ổn định hơn single tree."
))
cells.append(code(
"from sklearn.ensemble import RandomForestClassifier\n"
"\n"
"rf = RandomForestClassifier(\n"
"    n_estimators=200,\n"
"    random_state=42,\n"
"    max_depth=12,\n"
"    min_samples_split=10,\n"
"    min_samples_leaf=5,\n"
"    n_jobs=-1,\n"
"    class_weight=None\n"
")\n"
"\n"
"rf_results = evaluate_model(rf, X_train_res, y_train_res, X_val, y_val, X_test, y_test, 'Random Forest')\n"
"print_metrics(rf_results)"
))

cells.append(md(
"### 6.1. Classification report & Confusion matrix (Test)"
))
cells.append(code(
"print('=== TEST Classification Report ===')\n"
"print(classification_report(y_test, rf_results['y_pred_test'], target_names=['No Diabetes', 'Diabetes']))\n"
"\n"
"cm = confusion_matrix(y_test, rf_results['y_pred_test'])\n"
"fig, ax = plt.subplots(figsize=(5,4))\n"
"sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,\n"
"            xticklabels=['No Diabetes', 'Diabetes'],\n"
"            yticklabels=['No Diabetes', 'Diabetes'])\n"
"ax.set_xlabel('Predicted'); ax.set_ylabel('Actual')\n"
"ax.set_title('Confusion Matrix - Random Forest (Test)')\n"
"plt.tight_layout(); plt.show()"
))

cells.append(md(
"### 6.2. Feature Importance"
))
cells.append(code(
"rf_importance = pd.DataFrame({\n"
"    'feature': feature_names,\n"
"    'importance': rf.feature_importances_\n"
"}).sort_values('importance', ascending=False)\n"
"\n"
"plt.figure(figsize=(8, 5))\n"
"sns.barplot(data=rf_importance, x='importance', y='feature')\n"
"plt.title('Feature Importance - Random Forest')\n"
"plt.tight_layout(); plt.show()\n"
"\n"
"print(rf_importance.to_string(index=False))"
))

cells.append(md(
"## 7. So sánh 3 mô hình ML cơ bản"
))
cells.append(code(
"# Thu thập kết quả\n"
"all_results = [lr_results, dt_results, rf_results]\n"
"\n"
"# Bảng so sánh\n"
"comp = pd.DataFrame([{\n"
"    'Model': r['name'],\n"
"    'Val_Acc': r['val_acc'],\n"
"    'Val_Prec': r['val_prec'],\n"
"    'Val_Rec': r['val_rec'],\n"
"    'Val_F1': r['val_f1'],\n"
"    'Val_AUC': r.get('val_auc', 0),\n"
"    'Test_Acc': r['test_acc'],\n"
"    'Test_Prec': r['test_prec'],\n"
"    'Test_Rec': r['test_rec'],\n"
"    'Test_F1': r['test_f1'],\n"
"    'Test_AUC': r.get('test_auc', 0),\n"
"} for r in all_results])\n"
"\n"
"pd.set_option('display.float_format', '{:.4f}'.format)\n"
"print(comp.to_string(index=False))"
))

cells.append(md(
"### 7.1. Biểu đồ so sánh F1 & AUC (Validation)"
))
cells.append(code(
"fig, axes = plt.subplots(1, 2, figsize=(12, 5))\n"
"\n"
"x = range(len(comp))\n"
"width = 0.35\n"
"\n"
"axes[0].bar([i - width/2 for i in x], comp['Val_F1'], width, label='Val F1', color='#2ca02c')\n"
"axes[0].bar([i + width/2 for i in x], comp['Test_F1'], width, label='Test F1', color='#98df8a')\n"
"axes[0].set_xticks(x)\n"
"axes[0].set_xticklabels(comp['Model'], rotation=15)\n"
"axes[0].set_ylabel('F1-score')\n"
"axes[0].set_title('F1-score: Validation vs Test')\n"
"axes[0].legend()\n"
"axes[0].set_ylim(0, 1)\n"
"\n"
"axes[1].bar([i - width/2 for i in x], comp['Val_AUC'], width, label='Val AUC', color='#1f77b4')\n"
"axes[1].bar([i + width/2 for i in x], comp['Test_AUC'], width, label='Test AUC', color='#aec7e8')\n"
"axes[1].set_xticks(x)\n"
"axes[1].set_xticklabels(comp['Model'], rotation=15)\n"
"axes[1].set_ylabel('AUC-ROC')\n"
"axes[1].set_title('AUC-ROC: Validation vs Test')\n"
"axes[1].legend()\n"
"axes[1].set_ylim(0, 1)\n"
"\n"
"plt.tight_layout(); plt.show()"
))

cells.append(md(
"### 7.2. ROC Curves trên Test set"
))
cells.append(code(
"fig, ax = plt.subplots(figsize=(8, 6))\n"
"for r in all_results:\n"
"    if r['y_prob_test'] is not None:\n"
"        RocCurveDisplay.from_predictions(y_test, r['y_prob_test'], name=r['name'], ax=ax)\n"
"ax.plot([0, 1], [0, 1], 'k--', label='Random (AUC=0.5)')\n"
"ax.set_title('ROC Curves - 3 ML Models (Test)')\n"
"plt.tight_layout(); plt.show()"
))

cells.append(md(
"## 8. Lưu mô hình tốt nhất cho so sánh sau\n"
"\n"
"Lưu cả 3 mô hình để tái sử dụng trong Notebook 4 (So sánh ML vs DL)."
))
cells.append(code(
"# Chọn mô hình tốt nhất theo Test F1\n"
"best = max(all_results, key=lambda x: x['test_f1'])\n"
"print(f\"Best model by Test F1: {best['name']} (F1={best['test_f1']:.4f})\")\n"
"\n"
"# Lưu tất cả\n"
"for r in all_results:\n"
"    joblib.dump(r['model'], os.path.join(MODEL_DIR, f\"diabetes_{r['name'].lower().replace(' ', '_')}.pkl\"))\n"
"\n"
"# Lưu kết quả so sánh\n"
"comp.to_csv(os.path.join(MODEL_DIR, 'diabetes_ml_comparison.csv'), index=False)\n"
"print('✅ Đã lưu 3 models + bảng so sánh vào', MODEL_DIR)"
))

cells.append(md(
"## 9. Kết luận (3 ML Models)\n"
"\n"
"- **Logistic Regression**: Baseline tuyến tính, nhanh, interpretable.\n"
"- **Decision Tree**: Phi tuyến, dễ hiểu nhưng dễ overfit nếu không điều chỉnh depth.\n"
"- **Random Forest**: Ensemble mạnh, ít overfit hơn, thường cho F1/AUC cao nhất.\n"
"\n"
"Mô hình ML tốt nhất (theo Test F1) sẽ được so sánh với Deep Learning ở Notebook 4.\n"
"\n"
"**Tiếp theo: Notebook 3 — Deep Learning (NumPy từ đầu + MLP PyTorch + 3 thí nghiệm bắt buộc)**"
))

nb = {"cells": cells, "metadata": {
    "kernelspec": {"display_name": "Python 3 (ipykernel)", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3.11.16"}
}, "nbformat": 4, "nbformat_minor": 5}

out = os.path.join(os.path.dirname(__file__), '2_ml_models.ipynb')
with open(out, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print('Saved', out)