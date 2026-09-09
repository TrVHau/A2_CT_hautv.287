#!/usr/bin/env python3
"""Build house price Notebook 1 - EDA & Preprocessing."""
import json, os

def md(s): return {"cell_type":"markdown","metadata":{},"source":s}
def code(s): return {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":s}

cells=[]

cells.append(md(
"# DỰ ĐOÁN GIÁ NHÀ VN — EDA & PREPROCESSING\n"
"\n"
"**Assignment 03 — Neural Networks and Representation Learning**\n"
"\n"
"**Bài toán:** Hồi quy (Regression) — dự đoán giá nhà\n"
"\n"
"**Môi trường:** conda env `assignment2`\n"
"\n"
"---"
))

cells.append(md("## 1. Import libraries & Load data"))
cells.append(code(
"import matplotlib\n"
"matplotlib.use('Agg')\n"
"import numpy as np\n"
"import pandas as pd\n"
"import matplotlib.pyplot as plt\n"
"import seaborn as sns\n"
"import os\n"
"import re\n"
"import joblib\n"
"\n"
"sns.set_theme(style='whitegrid', palette='deep')\n"
"plt.rcParams['figure.figsize'] = (10, 6)\n"
"\n"
"DATA_PATH = os.path.join('..', 'data', 'VN_housing_dataset.csv')\n"
"df = pd.read_csv(DATA_PATH)\n"
"df = df.drop(columns=['Unnamed: 0'])\n"
"print('Raw shape:', df.shape)\n"
"df.head(3)"
))

cells.append(md("## 2. Tiền xử lý dữ liệu\n\nLàm sạch text và chuyển các cột về dạng số."))
cells.append(code(
"def extract_number(text):\n"
"    if pd.isna(text): return np.nan\n"
"    # extract numbers, replace comma with dot for decimals\n"
"    match = re.search(r'([\\d.,]+)', str(text))\n"
"    if match:\n"
"        val = match.group(1).replace('.', '').replace(',', '.')\n"
"        try:\n"
"            return float(val)\n"
"        except:\n"
"            return np.nan\n"
"    return np.nan\n"
"\n"
"# Xử lý cột Diện tích (Area), Giá/m2 (Price/m2)\n"
"df['Area'] = df['Diện tích'].apply(extract_number)\n"
"df['Price_per_m2'] = df['Giá/m2'].apply(extract_number)\n"
"\n"
"# Tính giá tổng (Total Price) = Area * Price_per_m2 (triệu VNĐ)\n"
"df['TotalPrice'] = df['Area'] * df['Price_per_m2']\n"
"\n"
"# Xử lý số tầng, số phòng ngủ, chiều dài, rộng\n"
"df['Floors'] = df['Số tầng'].apply(extract_number)\n"
"df['Bedrooms'] = df['Số phòng ngủ'].apply(extract_number)\n"
"df['Length'] = df['Dài'].apply(extract_number)\n"
"df['Width'] = df['Rộng'].apply(extract_number)\n"
"\n"
"# Loại bỏ các cột text không cần thiết & đổi tên\n"
"cols_drop = ['Ngày', 'Địa chỉ', 'Diện tích', 'Dài', 'Rộng', 'Giá/m2', 'Số tầng', 'Số phòng ngủ']\n"
"df = df.drop(columns=cols_drop)\n"
"\n"
"df = df.rename(columns={\n"
"    'Quận': 'District',\n"
"    'Huyện': 'Ward',\n"
"    'Loại hình nhà ở': 'House_Type',\n"
"    'Giấy tờ pháp lý': 'Legal_Status'\n"
"})\n"
"print('Sau khi parse số:', df.shape)\n"
"df.head()"
))

cells.append(md("### 2.1 Xử lý Missing Values & Outliers"))
cells.append(code(
"# Xóa các hàng mất Target (TotalPrice)\n"
"df = df.dropna(subset=['TotalPrice', 'Area']).copy()\n"
"\n"
"# Lọc Outliers cơ bản hợp lý hóa dữ liệu\n"
"df = df[(df['Area'] > 10) & (df['Area'] < 500)] # Diện tích 10m2 -> 500m2\n"
"df = df[(df['TotalPrice'] > 100) & (df['TotalPrice'] < 50000)] # Giá 100tr -> 50 tỷ\n"
"\n"
"# Lấp đầy NaN với median đối với các feature số\n"
"for c in ['Floors', 'Bedrooms', 'Length', 'Width']:\n"
"    df[c] = df[c].fillna(df[c].median())\n"
"\n"
"# Lấp đầy Categorical\n"
"df['Legal_Status'] = df['Legal_Status'].fillna('Unknown')\n"
"\n"
"print('Sau khi clean up:', df.shape)\n"
"df.isnull().sum()"
))

cells.append(md("## 3. Khám phá (EDA)"))
cells.append(code(
"fig, axes = plt.subplots(1, 2, figsize=(14,5))\n"
"sns.histplot(df['TotalPrice'], kde=True, ax=axes[0])\n"
"axes[0].set_title('Phân bố Giá Nhà (Triệu VNĐ)')\n"
"\n"
"sns.histplot(np.log1p(df['TotalPrice']), kde=True, ax=axes[1])\n"
"axes[1].set_title('Phân bố Giá Nhà (Log Scale)')\n"
"plt.show()\n"
"\n"
"# Vì phân bố lệch phải rất mạnh, ta sử dụng Log Transform trên Target\n"
"df['LogPrice'] = np.log1p(df['TotalPrice'])"
))

cells.append(md("## 4. Chuẩn bị Dữ liệu cho Mô hình (Encoding & Splitting)"))
cells.append(code(
"from sklearn.model_selection import train_test_split\n"
"from sklearn.preprocessing import StandardScaler\n"
"\n"
"# Lọc lấy Top 15 Quận phổ biến (gom nhóm phần còn lại)\n"
"top_districts = df['District'].value_counts().nlargest(15).index\n"
"df['District'] = df['District'].apply(lambda x: x if x in top_districts else 'Other')\n"
"\n"
"# Get Dummies\n"
"df_encoded = pd.get_dummies(df.drop(columns=['Price_per_m2', 'TotalPrice', 'Ward']), columns=['District', 'House_Type', 'Legal_Status'], drop_first=True)\n"
"\n"
"X = df_encoded.drop(columns=['LogPrice'])\n"
"y = df_encoded['LogPrice']\n"
"\n"
"X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)\n"
"X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)\n"
"\n"
"scaler = StandardScaler()\n"
"X_train_scaled = scaler.fit_transform(X_train)\n"
"X_val_scaled = scaler.transform(X_val)\n"
"X_test_scaled = scaler.transform(X_test)\n"
"\n"
"print('Train:', X_train_scaled.shape)\n"
"print('Val:', X_val_scaled.shape)\n"
"print('Test:', X_test_scaled.shape)"
))

cells.append(md("## 5. Lưu kết cụ"))
cells.append(code(
"MODEL_DIR = os.path.join('..', 'models')\n"
"os.makedirs(MODEL_DIR, exist_ok=True)\n"
"\n"
"joblib.dump(scaler, os.path.join(MODEL_DIR, 'scaler.pkl'))\n"
"joblib.dump(list(X.columns), os.path.join(MODEL_DIR, 'feature_names.pkl'))\n"
"\n"
"np.savez_compressed(os.path.join(MODEL_DIR, 'preprocessed_data.npz'),\n"
"                    X_train=X_train_scaled, y_train=y_train.values,\n"
"                    X_val=X_val_scaled, y_val=y_val.values,\n"
"                    X_test=X_test_scaled, y_test=y_test.values)\n"
"print('✅ Đã lưu tiền xử lý.')"
))

nb = {"cells": cells, "metadata": {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3.11.16"}
}, "nbformat": 4, "nbformat_minor": 5}

out = os.path.join(os.path.dirname(__file__), '1_eda_preprocessing.ipynb')
with open(out, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print('Saved', out)
