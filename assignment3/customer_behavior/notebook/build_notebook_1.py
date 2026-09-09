#!/usr/bin/env python3
"""Build Customer Behavior Notebook 1 - EDA & Preprocessing."""
import json, os

def md(s): return {"cell_type":"markdown","metadata":{},"source":s}
def code(s): return {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":s}

cells=[]

cells.append(md(
"# PHÂN TÍCH ĐÁNH GIÁ KHÁCH HÀNG E-COMMERCE — EDA & TEXT PREPROCESSING\n"
"\n"
"**Assignment 03 — Neural Networks and Representation Learning**\n"
"\n"
"**Bài toán:** Phân loại nhị phân — Dự đoán sản phẩm có được khuyên dùng hay không (`Recommended IND`) dựa trên văn bản đánh giá (`Review Text`).\n"
"**Dữ liệu:** Womens Clothing E-Commerce Reviews\n"
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
"DATA_PATH = os.path.join('..', 'data', 'Womens Clothing E-Commerce Reviews.csv')\n"
"df = pd.read_csv(DATA_PATH)\n"
"df = df.drop(columns=['Unnamed: 0', 'Clothing ID', 'Title'])\n"
"print('Raw shape:', df.shape)\n"
"df.head(3)"
))

cells.append(md("## 2. Tiền xử lý dữ liệu (Text Cleaning)"))
cells.append(code(
"# Xóa các hàng mất Review Text (feature chính)\n"
"df = df.dropna(subset=['Review Text', 'Recommended IND']).copy()\n"
"\n"
"def clean_text(text):\n"
"    text = str(text).lower()\n"
"    text = re.sub(r'[^a-z0-9 ]+', '', text) # Chỉ giữ lại chữ và số\n"
"    text = re.sub(r'\\s+', ' ', text).strip() # Xóa khoảng trắng thừa\n"
"    return text\n"
"\n"
"df['Clean_Review'] = df['Review Text'].apply(clean_text)\n"
"\n"
"# Lọc những đánh giá quá ngắn\n"
"df['Review_Length'] = df['Clean_Review'].apply(lambda x: len(x.split()))\n"
"df = df[df['Review_Length'] > 3] # Chứa ít nhất 3 từ\n"
"\n"
"print('Sau khi clean text:', df.shape)\n"
"df[['Review Text', 'Clean_Review', 'Recommended IND']].head()"
))

cells.append(md("## 3. Khám phá (EDA)"))
cells.append(code(
"fig, axes = plt.subplots(1, 2, figsize=(14,5))\n"
"sns.countplot(data=df, x='Recommended IND', ax=axes[0])\n"
"axes[0].set_title('Phân bố Recommended IND')\n"
"\n"
"sns.histplot(df['Review_Length'], bins=50, kde=True, ax=axes[1])\n"
"axes[1].set_title('Phân Phối Chiều Dài Đánh Giá (Số Từ)')\n"
"plt.show()"
))

cells.append(md("## 4. Feature Engineering: Vector hóa văn bản bằng TF-IDF\n\nMô hình Học máy cổ điển cần dữ liệu số, ta dùng TF-IDF để vectơ hóa văn bản."))
cells.append(code(
"from sklearn.model_selection import train_test_split\n"
"from sklearn.feature_extraction.text import TfidfVectorizer\n"
"\n"
"X_text = df['Clean_Review']\n"
"y = df['Recommended IND'].values\n"
"\n"
"# Chia Train / Val / Test (70/15/15)\n"
"X_train_text, X_temp_text, y_train, y_temp = train_test_split(X_text, y, test_size=0.3, random_state=42, stratify=y)\n"
"X_val_text, X_test_text, y_val, y_test = train_test_split(X_temp_text, y_temp, test_size=0.5, random_state=42, stratify=y_temp)\n"
"\n"
"# TF-IDF Vectorization (sử dụng tối đa 3000 features phổ biến nhất)\n"
"tfidf = TfidfVectorizer(max_features=3000, stop_words='english')\n"
"X_train_tfidf = tfidf.fit_transform(X_train_text).toarray()\n"
"X_val_tfidf = tfidf.transform(X_val_text).toarray()\n"
"X_test_tfidf = tfidf.transform(X_test_text).toarray()\n"
"\n"
"print('Train TF-IDF:', X_train_tfidf.shape)\n"
"print('Val TF-IDF:', X_val_tfidf.shape)\n"
"print('Test TF-IDF:', X_test_tfidf.shape)"
))

cells.append(md("## 5. Lưu dữ liệu đã xử lý"))
cells.append(code(
"MODEL_DIR = os.path.join('..', 'models')\n"
"os.makedirs(MODEL_DIR, exist_ok=True)\n"
"\n"
"# Lưu TF-IDF model\n"
"joblib.dump(tfidf, os.path.join(MODEL_DIR, 'tfidf_vectorizer.pkl'))\n"
"\n"
"# Lưu Dữ liệu gốc (để Deep Learning PyTorch dùng tokenization / embedding riêng) \n"
"np.savez_compressed(os.path.join(MODEL_DIR, 'raw_text_data.npz'),\n"
"                    X_train=X_train_text.values, y_train=y_train,\n"
"                    X_val=X_val_text.values, y_val=y_val,\n"
"                    X_test=X_test_text.values, y_test=y_test)\n"
"\n"
"# Lưu Dữ liệu TF-IDF (dành cho ML truyền thống)\n"
"np.savez_compressed(os.path.join(MODEL_DIR, 'tfidf_data.npz'),\n"
"                    X_train=X_train_tfidf, y_train=y_train,\n"
"                    X_val=X_val_tfidf, y_val=y_val,\n"
"                    X_test=X_test_tfidf, y_test=y_test)\n"
"print('✅ Đã lưu vectorizer và biến.')"
))

nb = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}}, "nbformat": 4, "nbformat_minor": 5}
out = os.path.join(os.path.dirname(__file__), '1_eda_preprocessing.ipynb')
with open(out, 'w', encoding='utf-8') as f: json.dump(nb, f, ensure_ascii=False, indent=1)
print('Saved', out)
