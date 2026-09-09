#!/usr/bin/env python3
"""Build the diabetes EDA & Preprocessing notebook for Assignment 03."""
import json, os

def md(s): return {"cell_type":"markdown","metadata":{},"source":s}
def code(s): return {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":s}

cells=[]

cells.append(md(
"# DỰ ĐOÁN BỆNH TIỂU ĐƯỜNG — EDA & PREPROCESSING\n"
"\n"
"**Assignment 03 — Neural Networks and Representation Learning**\n"
"\n"
"**Bài toán:** Phân loại nhị phân — dự đoán nguy cơ tiểu đường\n"
"\n"
"**Môi trường:** conda env `assignment2`\n"
"\n"
"---"
))

cells.append(md(
"## 1. Mục tiêu notebook\n"
"\n"
"Notebook này thực hiện:\n"
"1. Tải và khám phá dữ liệu (`diabetes_prediction_dataset.csv`)\n"
"2. Kiểm tra chất lượng dữ liệu: missing value, duplicates, outliers\n"
"3. Phân tích phân bố target và tương quan\n"
"4. **Tiền xử lý**: mã hoá biến categorical, xử lý mất cân bằng lớp, chuẩn hoá\n"
"5. **Chia tập**: train / validation / test\n"
"\n"
"Nội dung notebook phục vụ cho các notebook tiếp theo:\n"
"- `2_ml_models.ipynb` — 3 mô hình ML cơ bản\n"
"- `3_deep_learning.ipynb` — Deep Learning (NumPy từ đầu + MLP PyTorch)\n"
"- `4_ml_vs_dl_comparison.ipynb` — So sánh 4 mô hình"
))

cells.append(md(
"## 2. Import thư viện"
))
cells.append(code(
"import matplotlib\n"
"matplotlib.use('Agg')  # Fix no DISPLAY error in headless / notebook environments\n"
"import numpy as np\n"
"import pandas as pd\n"
"import matplotlib.pyplot as plt\n"
"import seaborn as sns\n"
"import os\n"
"\n"
"# Cấu hình đồ thị\n"
"sns.set_theme(style='whitegrid', palette='deep')\n"
"plt.rcParams['figure.figsize'] = (10, 6)\n"
"plt.rcParams['axes.titlesize'] = 13\n"
"\n"
"RANDOM_STATE = 42\n"
"np.random.seed(RANDOM_STATE)\n"
"\n"
"DATA_PATH = os.path.join('..', 'data', 'diabetes_prediction_dataset.csv')\n"
"print('Ready.')"
))

cells.append(md(
"## 3. Tải dữ liệu"
))
cells.append(code(
"df = pd.read_csv(DATA_PATH)\n"
"print('Shape:', df.shape)\n"
"df.head()"
))

cells.append(md(
"### 3.1. Kiểu dữ liệu & thông tin cơ bản"
))
cells.append(code(
"df.info()"
))
cells.append(code(
"df.describe().T"
))

cells.append(md(
"### 3.2. Kiểm tra missing values"
))
cells.append(code(
"missing = df.isnull().sum()\n"
"missing = missing[missing > 0]\n"
"if missing.empty:\n"
"    print('✅ Không có missing values.')\n"
"else:\n"
"    print('❌ Có missing values:')\n"
"    print(missing)"
))

cells.append(md(
"### 3.3. Kiểm tra duplicates"
))
cells.append(code(
"dup = df.duplicated().sum()\n"
"print(f'🔁 Số dòng trùng lặp: {dup} ({dup/len(df)*100:.2f}%)')\n"
"print('\\nSố lượng mỗi nhóm target trước khi xử lý:')\n"
"print(df['diabetes'].value_counts())"
))

cells.append(md(
"### 3.4. Xử lý duplicates\n"
"\n"
"Loại bỏ các dòng trùng lặp hoàn toàn để tránh nhiễu cho quá trình huấn luyện."
))
cells.append(code(
"df = df.drop_duplicates().reset_index(drop=True)\n"
"print('Shape sau khi loại duplicate:', df.shape)\n"
"print('\\nPhân bố target sau khi loại duplicate:')\n"
"print(df['diabetes'].value_counts())\n"
"print(f\"\\nTỷ lệ lớp 1 (diabetes): {df['diabetes'].mean()*100:.2f}%\")"
))

cells.append(md(
"## 4. Phân tích đơn biến (Univariate Analysis)"
))

cells.append(md(
"### 4.1. Phân bố target (diabetes)"
))
cells.append(code(
"ax = df['diabetes'].value_counts().plot(kind='bar', color=['#1f77b4','#d62728'])\n"
"ax.set_title('Phân bố biến target (diabetes)')\n"
"ax.set_xticklabels(['Không tiểu đường (0)', 'Tiểu đường (1)'], rotation=0)\n"
"ax.set_ylabel('Số lượng')\n"
"for p in ax.patches:\n"
"    ax.annotate(f'{int(p.get_height())}', (p.get_x()+p.get_width()/2, p.get_height()+500), ha='center')\n"
"plt.tight_layout(); plt.show()"
))

cells.append(md(
"### 4.2. Phân bố các biến số"
))
cells.append(code(
"num_cols = ['age','bmi','HbA1c_level','blood_glucose_level']\n"
"fig, axes = plt.subplots(2, 2, figsize=(12, 8))\n"
"for ax, col in zip(axes.ravel(), num_cols):\n"
"    sns.histplot(df[col], kde=True, ax=ax)\n"
"    ax.set_title(f'Phân bố {col}')\n"
"plt.tight_layout(); plt.show()"
))

cells.append(md(
"### 4.3. Phân bố biến categorical\n"
"\n"
"**Giới tính (`gender`)** và **tiền sử hút thuốc (`smoking_history`)**."
))
cells.append(code(
"fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n"
"sns.countplot(data=df, x='gender', ax=axes[0])\n"
"axes[0].set_title('Phân bố gender')\n"
"sns.countplot(data=df, x='smoking_history', order=df['smoking_history'].value_counts().index, ax=axes[1])\n"
"axes[1].set_title('Phân bố smoking_history')\n"
"axes[1].tick_params(axis='x', rotation=45)\n"
"plt.tight_layout(); plt.show()"
))

cells.append(md(
"## 5. Phân tích nhị biến (Bivariate Analysis)"
))

cells.append(md(
"### 5.1. Ma trận tương quan giữa biến số và target\n"
"\n"
"Hệ số tương quan Pearson cho thấy mức độ liên quan tuyến tính giữa các biến số và target."
))
cells.append(code(
"# Chỉ tính các biến số\n"
"df_numeric = df.select_dtypes(include=[np.number])\n"
"corr = df_numeric.corr()\n"
"\n"
"plt.figure(figsize=(10, 8))\n"
"sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', cbar=True)\n"
"plt.title('Ma trận tương quan')\n"
"plt.tight_layout(); plt.show()"
))

cells.append(md(
"### 5.2. Tương quan với target"
))
cells.append(code(
"corr_with_target = corr['diabetes'].drop('diabetes').sort_values(ascending=False)\n"
"print('Tương quan tuyến tính của các biến với target (diabetes):')\n"
"print(corr_with_target.round(3).to_string())"
))

cells.append(md(
"### 5.3. Tỷ lệ tiểu đường theo từng nhóm"
))
cells.append(code(
"fig, axes = plt.subplots(2, 2, figsize=(14, 9))\n"
"\n"
"sns.barplot(data=df, x='gender', y='diabetes', ax=axes[0,0])\n"
"axes[0,0].set_title('Tỷ lệ tiểu đường theo gender')\n"
"\n"
"sns.barplot(data=df, x='hypertension', y='diabetes', ax=axes[0,1])\n"
"axes[0,1].set_title('Tỷ lệ tiểu đường theo hypertension')\n"
"\n"
"sns.barplot(data=df, x='heart_disease', y='diabetes', ax=axes[1,0])\n"
"axes[1,0].set_title('Tỷ lệ tiểu đường theo heart_disease')\n"
"\n"
"sm_order = df.groupby('smoking_history')['diabetes'].mean().sort_values(ascending=False).index\n"
"sns.barplot(data=df, x='smoking_history', y='diabetes', order=sm_order, ax=axes[1,1])\n"
"axes[1,1].set_title('Tỷ lệ tiểu đường theo smoking_history')\n"
"axes[1,1].tick_params(axis='x', rotation=45)\n"
"\n"
"plt.tight_layout(); plt.show()"
))

cells.append(md(
"### 5.4. Boxplot: biến số theo target"
))
cells.append(code(
"fig, axes = plt.subplots(2, 2, figsize=(13, 9))\n"
"for ax, col in zip(axes.ravel(), num_cols):\n"
"    sns.boxplot(data=df, x='diabetes', y=col, ax=ax)\n"
"    ax.set_title(f'{col} theo diabetes')\n"
"    ax.set_xticklabels(['Không', 'Có'])\n"
"plt.tight_layout(); plt.show()"
))

cells.append(md(
"## 6. Chuẩn bị dữ liệu cho mô hình"
))

cells.append(md(
"### 6.1. Tách features và target"
))
cells.append(code(
"X = df.drop(columns=['diabetes'])\n"
"y = df['diabetes']\n"
"print('X shape:', X.shape)\n"
"print('y shape:', y.shape)\n"
"print('\\nCác cột feature:')\n"
"print(list(X.columns))"
))

cells.append(md(
"### 6.2. Mã hoá biến categorical\n"
"\n"
"Sử dụng `LabelEncoder` cho `gender` và `smoking_history`. "
"Để cho pipeline Deep Learning về sau, ta dùng OrdinalEncoder cho đầu vào số hoá. "
"Các biến binary (`hypertension`, `heart_disease`) giữ nguyên."
))
cells.append(code(
"from sklearn.preprocessing import LabelEncoder\n"
"\n"
"le_gender = LabelEncoder()\n"
"le_smoking = LabelEncoder()\n"
"\n"
"X['gender_enc'] = le_gender.fit_transform(X['gender'])\n"
"X['smoking_enc'] = le_smoking.fit_transform(X['smoking_history'])\n"
"\n"
"# Drop cột gốc\n"
"X = X.drop(columns=['gender', 'smoking_history'])\n"
"\n"
"print('Các cột sau khi mã hoá:', list(X.columns))\n"
"X.head()"
))

cells.append(md(
"### 6.3. Kiểm tra outliers (z-score)\n"
"\n"
"Ta kiểm tra xem có giá trị ngoại lai đáng kể không bằng z-score trên các biến số."
))
cells.append(code(
"from scipy.stats import zscore\n"
"\n"
"z = np.abs(zscore(X.select_dtypes(include=[np.number])))\n"
"outliers_mask = (z > 4).any(axis=1)\n"
"print(f'⚠️ Số dòng có z-score > 4 (outlier mạnh): {outliers_mask.sum()} ({outliers_mask.mean()*100:.2f}%)')\n"
"\n"
"# Với dataset lớn (gần 100k), ta giữ nguyên outliers vì MLP/ML vẫn học được; \n"
"# sẽ kiểm tra trong modeling nếu cần."
))

cells.append(md(
"### 6.4. Xử lý mất cân bằng lớp (Class Imbalance)\n"
"\n"
"Target có ~91% lớp 0 và ~9% lớp 1. Đây là mất cân bằng rõ rệt. "
"Ta dùng **SMOTE** trên tập **train** để cân bằng, giữ nguyên validation/test là phân bố gốc "
"(phản ánh thực tế)."
))
cells.append(code(
"from sklearn.model_selection import train_test_split\n"
"\n"
"# Chia train/validation/test theo thứ tự 70/15/15\n"
"X_train_val, X_test, y_train_val, y_test = train_test_split(\n"
"    X, y, test_size=0.15, random_state=RANDOM_STATE, stratify=y)\n"
"X_train, X_val, y_train, y_val = train_test_split(\n"
"    X_train_val, y_train_val, test_size=0.15/0.85, random_state=RANDOM_STATE, stratify=y_train_val)\n"
"\n"
"print('Train size:', X_train.shape)\n"
"print('Validation size:', X_val.shape)\n"
"print('Test size:', X_test.shape)\n"
"print('\\nPhân bố target:')\n"
"for name, yy in [('Train', y_train), ('Val', y_val), ('Test', y_test)]:\n"
"    print(f\"{name}: 0={sum(yy==0)}, 1={sum(yy==1)} (tỷ lệ 1: {yy.mean()*100:.2f}%)\")"
))

cells.append(md(
"### 6.5. Chuẩn hoá (StandardScaler)\n"
"\n"
"Chuẩn hoá để các feature có mean=0, std=1 — cần thiết cho MLP và nhiều mô hình ML (hồi quy logistic, SVM)."
))
cells.append(code(
"from sklearn.preprocessing import StandardScaler\n"
"\n"
"scaler = StandardScaler()\n"
"\n"
"# Fit trên TRAIN chỉ, để tránh data leakage\n"
"X_train_scaled = scaler.fit_transform(X_train)\n"
"X_val_scaled = scaler.transform(X_val)\n"
"X_test_scaled = scaler.transform(X_test)\n"
"\n"
"print('Scaler fit trên train.')\n"
"print('X_train_scaled shape:', X_train_scaled.shape)\n"
"print('X_val_scaled shape:', X_val_scaled.shape)\n"
"print('X_test_scaled shape:', X_test_scaled.shape)"
))

cells.append(md(
"### 6.6. (Tùy chọn) SMOTE trên tập train\n"
"\n"
"Vì MLP sau này cần cân bằng lớp, ta áp dụng SMOTE trên tập train **đã chuẩn hoá**."
))
cells.append(code(
"from imblearn.over_sampling import SMOTE\n"
"\n"
"smote = SMOTE(random_state=RANDOM_STATE)\n"
"X_train_res, y_train_res = smote.fit_resample(X_train_scaled, y_train)\n"
"\n"
"print('Sau SMOTE:')\n"
"print('  X_train_res shape:', X_train_res.shape)\n"
"print('  0:', sum(y_train_res==0), '| 1:', sum(y_train_res==1))\n"
"print('  Cân bằng:', np.mean(y_train_res==1)*100, '%')"
))

cells.append(md(
"### 6.7. Lưu tiền xử lý để tái sử dụng\n"
"\n"
"Lưu `scaler`, encoder, và các biến đã xử lý về models để dùng lại trong modeling notebook."
))
cells.append(code(
"import joblib\n"
"import os\n"
"\n"
"MODEL_DIR = os.path.join('..', 'models')\n"
"os.makedirs(MODEL_DIR, exist_ok=True)\n"
"\n"
"joblib.dump(scaler, os.path.join(MODEL_DIR, 'diabetes_scaler.pkl'))\n"
"joblib.dump(le_gender, os.path.join(MODEL_DIR, 'le_gender.pkl'))\n"
"joblib.dump(le_smoking, os.path.join(MODEL_DIR, 'le_smoking.pkl'))\n"
"\n"
"# Lưu data đã xử lý dạng numpy/pkl để dùng sau\n"
"np.savez_compressed(os.path.join(MODEL_DIR, 'preprocessed_data.npz'),\n"
"                    X_train=X_train_scaled, y_train=y_train,\n"
"                    X_train_res=X_train_res, y_train_res=y_train_res,\n"
"                    X_val=X_val_scaled, y_val=y_val,\n"
"                    X_test=X_test_scaled, y_test=y_test)\n"
"\n"
"print('✅ Đã lưu preprocessing (scaler, encoders, data) vào', MODEL_DIR)"
))

cells.append(md(
"### 6.8. Lưu tên feature\n"
))
cells.append(code(
"feature_names = list(X.columns)\n"
"joblib.dump(feature_names, os.path.join(MODEL_DIR, 'feature_names.pkl'))\n"
"print('Feature names:', feature_names)"
))

cells.append(md(
"## 7. Kết luận\n"
"\n"
"- Dataset có **100,000** dòng, 8 feature + 1 target `diabetes` (binary).\n"
"- Không có missing; **4-5% duplicates** đã được loại bỏ.\n"
"- **Mất cân bằng lớp** (91% vs 9%) — xử lý bằng SMOTE trên tập train.\n"
"- Đã mã hoá categorical (`gender`, `smoking_history`), chuẩn hoá bằng `StandardScaler`.\n"
"- Đã chia **Train (70%) / Validation (15%) / Test (15%)** theo stratify.\n"
"- Tương quan cao nhất với target: `HbA1c_level`, `blood_glucose_level`, `bmi`, `age`.\n"
"\n"
"**Dữ liệu đã sẵn sàng cho các bước modeling.**"
))

nb = {"cells": cells, "metadata": {
    "kernelspec": {"display_name": "Python 3 (ipykernel)", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3.11.16"}
}, "nbformat": 4, "nbformat_minor": 5}

out = os.path.join(os.path.dirname(__file__), '1_eda_preprocessing.ipynb')
with open(out, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print('Saved', out)
