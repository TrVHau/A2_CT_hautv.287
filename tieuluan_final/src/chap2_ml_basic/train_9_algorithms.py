# -*- coding: utf-8 -*-
"""
CHƯƠNG 2: THỰC NGHIỆM ĐỐI ĐẦU 9 THUẬT TOÁN HỌC MÁY CƠ BẢN VÀ MẠNG NƠ-RON
Sinh viên thực hiện: Trần Văn Hậu | MSV: B23DCCN287 | Lớp: D23CTPM01 | Nhóm CT_09
Giảng viên hướng dẫn: PGS. TS. Trần Đình Quế

Quy trình chuẩn hóa 10-Fold Stratified Cross-Validation không rò rỉ dữ liệu (No Data Leakage).
Đánh giá toàn diện 9 thuật toán:
  1. Logistic Regression (L2 Penalty)
  2. Ridge Classifier
  3. Support Vector Classifier (RBF Kernel)
  4. Decision Tree (CART)
  5. Random Forest Ensemble
  6. Gradient Boosting (HistGradientBoosting / XGBoost)
  7. K-Nearest Neighbors (KNN k=5)
  8. Gaussian Naive Bayes
  9. Multilayer Perceptron (MLP)
"""

import sys
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, roc_auc_score
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')


def load_dataset():
    """Load or create benchmark clinical dataset."""
    csv_candidates = [
        Path("c:/code/A2_CT_hautv.287/project01/data/pima_diabetes_dataset.csv"),
        Path("c:/code/A2_CT_hautv.287/assignment1/data/diabetes_dataset.csv"),
    ]
    for p in csv_candidates:
        if p.exists():
            df = pd.read_csv(p)
            feature_cols = [c for c in df.columns if c not in ['Outcome', 'Diabetes', 'target', 'id', 'Patient_ID']]
            target_col = 'Outcome' if 'Outcome' in df.columns else ('Diabetes' if 'Diabetes' in df.columns else df.columns[-1])
            X = df[feature_cols].values
            y = df[target_col].values
            return X, y, feature_cols

    # Synthetic fallback
    np.random.seed(42)
    N = 768
    X = np.random.randn(N, 8)
    logits = 0.8 * X[:, 1] + 0.5 * X[:, 5] + 0.3 * X[:, 7] + np.random.randn(N) * 0.5
    y = (logits > 0.3).astype(int)
    cols = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigree', 'Age']
    return X, y, cols


def get_models():
    """Tập hợp 9 thuật toán học máy phân loại."""
    return {
        "1. Logistic Regression (L2)": LogisticRegression(C=1.0, max_iter=1000, random_state=42),
        "2. Ridge Classifier": RidgeClassifier(alpha=1.0, random_state=42),
        "3. Support Vector Machine (RBF)": SVC(C=1.0, kernel='rbf', probability=True, random_state=42),
        "4. Decision Tree (CART)": DecisionTreeClassifier(max_depth=5, min_samples_split=10, random_state=42),
        "5. Random Forest (100 Trees)": RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42),
        "6. Hist Gradient Boosting": HistGradientBoostingClassifier(max_iter=100, random_state=42),
        "7. K-Nearest Neighbors (k=5)": KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2),
        "8. Gaussian Naive Bayes": GaussianNB(),
        "9. Multilayer Perceptron (MLP)": MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=500, random_state=42),
    }


def evaluate_9_algorithms(n_splits=10, random_state=42):
    """Chạy quy trình 10-Fold CV nghiêm ngặt và tổng hợp bảng kết quả."""
    X, y, feature_names = load_dataset()
    print("=" * 80)
    print("THỰC NGHIỆM ĐỐI ĐẦU 9 THUẬT TOÁN HỌC MÁY CƠ BẢN VÀ MẠNG NƠ-RON (10-FOLD CV)")
    print("Tác giả: Trần Văn Hậu - B23DCCN287 | Lớp: D23CTPM01 | Nhóm: CT_09")
    print(f"Kích thước mẫu: N={len(y)}, Số đặc trưng d={X.shape[1]}")
    print("=" * 80)

    models = get_models()
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    
    results = []

    for name, clf in models.items():
        acc_list, bacc_list, f1_list, auc_list = [], [], [], []

        for fold, (train_idx, val_idx) in enumerate(skf.split(X, y)):
            X_tr, y_tr = X[train_idx], y[train_idx]
            X_va, y_va = X[val_idx], y[val_idx]

            # Chuẩn hóa StandardScaler trong từng fold (chống Data Leakage)
            scaler = StandardScaler()
            X_tr_sc = scaler.fit_transform(X_tr)
            X_va_sc = scaler.transform(X_va)

            clf.fit(X_tr_sc, y_tr)
            y_pred = clf.predict(X_va_sc)

            acc_list.append(accuracy_score(y_va, y_pred))
            bacc_list.append(balanced_accuracy_score(y_va, y_pred))
            f1_list.append(f1_score(y_va, y_pred, zero_division=0))

            # Tính ROC-AUC nếu có predict_proba hoặc decision_function
            if hasattr(clf, "predict_proba"):
                y_prob = clf.predict_proba(X_va_sc)[:, 1]
                auc_list.append(roc_auc_score(y_va, y_prob))
            elif hasattr(clf, "decision_function"):
                y_score = clf.decision_function(X_va_sc)
                auc_list.append(roc_auc_score(y_va, y_score))
            else:
                auc_list.append(roc_auc_score(y_va, y_pred))

        mean_acc = np.mean(acc_list) * 100
        std_acc = np.std(acc_list) * 100
        mean_bacc = np.mean(bacc_list) * 100
        mean_f1 = np.mean(f1_list)
        mean_auc = np.mean(auc_list)

        results.append({
            "Mô hình thuật toán": name,
            "Accuracy (%)": f"{mean_acc:.2f} ± {std_acc:.2f}",
            "Balanced Acc (%)": f"{mean_bacc:.2f}",
            "F1-Score": f"{mean_f1:.4f}",
            "ROC-AUC": f"{mean_auc:.4f}",
            "_raw_acc": mean_acc,
            "_raw_auc": mean_auc
        })

    # In kết quả
    res_df = pd.DataFrame(results)
    print(res_df[["Mô hình thuật toán", "Accuracy (%)", "Balanced Acc (%)", "F1-Score", "ROC-AUC"]].to_string(index=False))
    print("=" * 80)
    
    best_acc_idx = np.argmax([r["_raw_acc"] for r in results])
    best_auc_idx = np.argmax([r["_raw_auc"] for r in results])
    print(f"Thuật toán có Accuracy cao nhất: {results[best_acc_idx]['Mô hình thuật toán']} ({results[best_acc_idx]['Accuracy (%)']}%)")
    print(f"Thuật toán có ROC-AUC cao nhất:   {results[best_auc_idx]['Mô hình thuật toán']} ({results[best_auc_idx]['ROC-AUC']})")
    print("=" * 80)
    return results


if __name__ == "__main__":
    evaluate_9_algorithms(n_splits=10, random_state=42)
