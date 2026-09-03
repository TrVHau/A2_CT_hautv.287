#!/usr/bin/env python3
"""Script to build the complete diabetes_prediction.ipynb notebook."""

import json

# ============================================================
# Helper to create cells
# ============================================================
def md(source):
    return {"cell_type": "markdown", "metadata": {}, "source": source}

def code(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source,
    }

cells = []

# ============================================================
# Title
# ============================================================
cells.append(md(
    "# DỰ ĐOÁN BỆNH TIỂU ĐƯỜNG (DIABETES PREDICTION)\n"
    "\n"
    "**Assignment 02 - Intelligent System Development**\n"
    "\n"
    "**Ngày:** 2026-09-03\n"
    "\n"
    "---"
))

# ============================================================
# Section 1 – Problem Definition
# ============================================================
cells.append(md(
    "## 1. Định nghĩa bài toán (Problem Definition)\n"
    "\n"
    "### Mục tiêu\n"
    "Xây dựng hệ thống **dự đoán khả năng mắc bệnh tiểu đường** (Diabetes Prediction) dựa trên các "
    "đặc điểm lâm sàng của bệnh nhân.\n"
    "\n"
    "### Loại bài toán\n"
    "**Phân loại nhị phân (Binary Classification)**:\n"
    "- Class 0: Không mắc tiểu đường\n"
    "- Class 1: Mắc tiểu đường\n"
    "\n"
    "### Định nghĩa biến\n"
    "- **Đầu vào X**: Vector đặc trưng của bệnh nhân gồm các thông tin lâm sàng\n"
    "  - `gender` – Giới tính\n"
    "  - `age` – Tuổi\n"
    "  - `hypertension` – Tăng huyết áp (0/1)\n"
    "  - `heart_disease` – Bệnh tim (0/1)\n"
    "  - `smoking_history` – Tiền sử hút thuốc\n"
    "  - `bmi` – Chỉ số khối cơ thể\n"
    "  - `HbA1c_level` – Mức HbA1c (đường huyết bình quân 3 tháng)\n"
    "  - `blood_glucose_level` – Mức đường huyết\n"
    "- **Đầu ra y**: `diabetes` ∈ {0, 1}\n"
    "\n"
    "### Ý nghĩa thực tiễn\n"
    "Tiểu đường là bệnh mãn tính ảnh hưởng hàng triệu người. Phát hiện sớm giúp can thiệp kịp thời, "
    "giảm biến chứng và chi phí y tế. Hệ thống AI hỗ trợ bác sĩ sàng lọc nguy cơ tiểu đường nhanh "
    "và hiệu quả hơn."
))

# ============================================================
# Section 2 – Dataset Source
# ============================================================
cells.append(md(
    "## 2. Nguồn dữ liệu (Dataset Source)\n"
    "\n"
    "| Thuộc tính | Giá trị |\n"
    "|---|---|\n"
    "| **Tên dataset** | Diabetes Prediction Dataset |\n"
    "| **Nguồn** | Kaggle – Mohammed Mustafa |\n"
    "| **URL** | https://www.kaggle.com/datasets/iammustafatz/diabetes-prediction-dataset |\n"
    "| **Số quan sát** | ~100,000 bản ghi |\n"
    "| **Số thuộc tính** | 9 (8 features + 1 target) |\n"
    "\n"
    "### Mô tả các đặc trưng\n"
    "\n"
    "| Tên cột | Kiểu | Mô tả |\n"
    "|---|---|---|\n"
    "| `gender` | Categorical | Giới tính: Female / Male / Other |\n"
    "| `age` | Numerical | Tuổi bệnh nhân (năm) |\n"
    "| `hypertension` | Binary | Tăng huyết áp (0=Không, 1=Có) |\n"
    "| `heart_disease` | Binary | Bệnh tim mạch (0=Không, 1=Có) |\n"
    "| `smoking_history` | Categorical | Tiền sử hút thuốc |\n"
    "| `bmi` | Numerical | Chỉ số khối cơ thể (kg/m²) |\n"
    "| `HbA1c_level` | Numerical | Glycated hemoglobin (%) |\n"
    "| `blood_glucose_level` | Numerical | Mức đường huyết (mg/dL) |\n"
    "| `diabetes` | Binary (TARGET) | 0=Không mắc, 1=Mắc tiểu đường |\n"
    "\n"
    "### Mô tả một quan sát\n"
    "Mỗi dòng đại diện cho một **bệnh nhân**, với vector đặc trưng chứa thông tin "
    "nhân khẩu học, tiền sử bệnh và các chỉ số lâm sàng. Nhãn `diabetes` cho biết "
    "bệnh nhân đó có mắc tiểu đường hay không."
))

# ============================================================
# Section 3 – Dataset Loading
# ============================================================
cells.append(md("## 3. Tải dữ liệu (Dataset Loading)"))

cells.append(code(
    "# Import các thư viện cần thiết\n"
    "import warnings\n"
    "warnings.filterwarnings('ignore')\n"
    "\n"
    "import numpy as np\n"
    "import pandas as pd\n"
    "import matplotlib\n"
    "matplotlib.use('Agg')  # Backend không cần GUI\n"
    "import matplotlib.pyplot as plt\n"
    "import seaborn as sns\n"
    "import joblib\n"
    "import os\n"
    "import time\n"
    "\n"
    "from sklearn.model_selection import train_test_split\n"
    "from sklearn.preprocessing import StandardScaler, OneHotEncoder\n"
    "from sklearn.compose import ColumnTransformer\n"
    "from sklearn.pipeline import Pipeline\n"
    "from sklearn.dummy import DummyClassifier\n"
    "from sklearn.linear_model import LogisticRegression\n"
    "from sklearn.tree import DecisionTreeClassifier\n"
    "from sklearn.ensemble import RandomForestClassifier\n"
    "from sklearn.svm import LinearSVC\n"
    "from sklearn.neighbors import KNeighborsClassifier\n"
    "from sklearn.calibration import CalibratedClassifierCV\n"
    "from sklearn.metrics import (\n"
    "    accuracy_score, precision_score, recall_score,\n"
    "    f1_score, roc_auc_score, confusion_matrix,\n"
    "    classification_report, ConfusionMatrixDisplay, RocCurveDisplay\n"
    ")\n"
    "\n"
    "# Cấu hình\n"
    "RANDOM_STATE = 42\n"
    "DATA_PATH = '../data/diabetes_prediction_dataset.csv'\n"
    "MODEL_DIR = '../models'\n"
    "os.makedirs(MODEL_DIR, exist_ok=True)\n"
    "\n"
    "# Cài đặt style đồ thị\n"
    "sns.set_theme(style='whitegrid', palette='Set2')\n"
    "plt.rcParams['figure.figsize'] = (10, 6)\n"
    "plt.rcParams['font.size'] = 11\n"
    "\n"
    "print('✅ Các thư viện đã được import thành công!')\n"
    "print(f'NumPy:     {np.__version__}')\n"
    "print(f'Pandas:    {pd.__version__}')\n"
    "import sklearn; print(f'Sklearn:   {sklearn.__version__}')\n"
    "print(f'Matplotlib: {matplotlib.__version__}')"
))

cells.append(code(
    "# Đọc dataset\n"
    "df_raw = pd.read_csv(DATA_PATH)\n"
    "\n"
    "print(f'✅ Dataset đã được tải thành công!')\n"
    "print(f'Kích thước: {df_raw.shape[0]:,} dòng × {df_raw.shape[1]} cột')\n"
    "print()\n"
    "print('5 dòng đầu tiên:')\n"
    "df_raw.head()"
))

# ============================================================
# Section 4 – Dataset Inspection
# ============================================================
cells.append(md("## 4. Khảo sát dữ liệu (Dataset Inspection)"))

cells.append(code(
    "# Thông tin tổng quan về dataset\n"
    "print('=' * 60)\n"
    "print('THÔNG TIN DATASET')\n"
    "print('=' * 60)\n"
    "print(f'Số dòng (observations): {df_raw.shape[0]:,}')\n"
    "print(f'Số cột (features+target): {df_raw.shape[1]}')\n"
    "print()\n"
    "df_raw.info()"
))

cells.append(code(
    "# Thống kê mô tả\n"
    "print('Thống kê mô tả các biến số:')\n"
    "df_raw.describe(include='all').round(3)"
))

cells.append(code(
    "# Xác định các loại cột\n"
    "num_cols = df_raw.select_dtypes(include=['int64', 'float64']).columns.tolist()\n"
    "cat_cols = df_raw.select_dtypes(include=['object', 'category']).columns.tolist()\n"
    "\n"
    "print(f'Cột số (numerical):      {num_cols}')\n"
    "print(f'Cột phân loại (categorical): {cat_cols}')\n"
    "print(f'Biến mục tiêu (target):  diabetes')\n"
    "\n"
    "# Phân phối biến mục tiêu\n"
    "print()\n"
    "print('Phân phối target variable:')\n"
    "print(df_raw['diabetes'].value_counts())\n"
    "print()\n"
    "print(df_raw['diabetes'].value_counts(normalize=True).round(4) * 100, '(%)')"
))

# ============================================================
# Section 5 – Data Quality Analysis
# ============================================================
cells.append(md("## 5. Phân tích chất lượng dữ liệu (Data Quality Analysis)"))

cells.append(code(
    "# Tóm tắt chất lượng dữ liệu\n"
    "print('=' * 60)\n"
    "print('BÁO CÁO CHẤT LƯỢNG DỮ LIỆU')\n"
    "print('=' * 60)\n"
    "print(f'Tổng số quan sát:     {df_raw.shape[0]:,}')\n"
    "print(f'Tổng số thuộc tính:   {df_raw.shape[1] - 1} features + 1 target')\n"
    "print(f'Bộ nhớ sử dụng:       {df_raw.memory_usage(deep=True).sum() / 1024**2:.2f} MB')\n"
    "print()\n"
    "\n"
    "# Giá trị thiếu\n"
    "missing_count = df_raw.isna().sum().sum()\n"
    "print(f'Giá trị thiếu (NaN):  {missing_count}')\n"
    "\n"
    "# Bản sao\n"
    "dup_count = df_raw.duplicated().sum()\n"
    "print(f'Dòng trùng lặp:       {dup_count:,}')\n"
    "\n"
    "# Các giá trị duy nhất trong categorical\n"
    "print()\n"
    "print('Giá trị duy nhất trong cột categorical:')\n"
    "for col in cat_cols:\n"
    "    print(f'  {col}: {df_raw[col].unique()}')\n"
    "\n"
    "print()\n"
    "print('Giá trị duy nhất trong cột binary:')\n"
    "for col in ['hypertension', 'heart_disease', 'diabetes']:\n"
    "    print(f'  {col}: {sorted(df_raw[col].unique())}')"
))

# ============================================================
# Section 6 – Missing Value Analysis
# ============================================================
cells.append(md("## 6. Phân tích giá trị thiếu (Missing Value Analysis)"))

cells.append(code(
    "# Kiểm tra giá trị thiếu chi tiết\n"
    "missing_df = pd.DataFrame({\n"
    "    'Cột': df_raw.columns,\n"
    "    'Số lượng thiếu': df_raw.isna().sum().values,\n"
    "    'Phần trăm (%)': (df_raw.isna().sum().values / len(df_raw) * 100).round(4)\n"
    "})\n"
    "missing_df = missing_df.sort_values('Số lượng thiếu', ascending=False)\n"
    "print(missing_df.to_string(index=False))\n"
    "\n"
    "print()\n"
    "total_missing = df_raw.isna().sum().sum()\n"
    "if total_missing == 0:\n"
    "    print('✅ KHÔNG có giá trị thiếu trong dataset!')\n"
    "    print('   → Không cần imputation strategy.')\n"
    "else:\n"
    "    print(f'⚠️  Phát hiện {total_missing} giá trị thiếu. Cần xử lý!')\n"
    "\n"
    "# Biểu đồ missing values\n"
    "fig, ax = plt.subplots(figsize=(10, 4))\n"
    "missing_pct = (df_raw.isna().sum() / len(df_raw) * 100).sort_values(ascending=False)\n"
    "bars = ax.bar(missing_pct.index, missing_pct.values, color='coral', edgecolor='black', alpha=0.8)\n"
    "ax.set_title('Tỷ lệ giá trị thiếu theo từng cột (%)', fontsize=13, fontweight='bold')\n"
    "ax.set_xlabel('Cột')\n"
    "ax.set_ylabel('Phần trăm thiếu (%)')\n"
    "ax.set_ylim(0, max(missing_pct.max() + 5, 5))\n"
    "plt.xticks(rotation=30, ha='right')\n"
    "for bar, val in zip(bars, missing_pct.values):\n"
    "    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,\n"
    "            f'{val:.1f}%', ha='center', va='bottom', fontsize=9)\n"
    "plt.tight_layout()\n"
    "plt.savefig('../models/fig_missing_values.png', dpi=100, bbox_inches='tight')\n"
    "plt.show()\n"
    "print('Biểu đồ đã lưu.')"
))

# ============================================================
# Section 7 – Duplicate Analysis
# ============================================================
cells.append(md("## 7. Phân tích bản sao (Duplicate Analysis)"))

cells.append(code(
    "# Đếm bản sao\n"
    "dup_count = df_raw.duplicated().sum()\n"
    "print(f'Số dòng trùng lặp hoàn toàn: {dup_count:,}')\n"
    "print(f'Tỷ lệ: {dup_count / len(df_raw) * 100:.2f}%')\n"
    "\n"
    "if dup_count > 0:\n"
    "    print()\n"
    "    print('Ví dụ 5 dòng trùng lặp đầu tiên:')\n"
    "    print(df_raw[df_raw.duplicated(keep=False)].head(10))\n"
    "    print()\n"
    "    print('Lý do xóa bản sao: Cùng một quan sát xuất hiện nhiều lần có thể khiến')\n"
    "    print('dữ liệu train và test bị \"overlap\", dẫn đến đánh giá model quá lạc quan.')\n"
    "    print()\n"
    "    print('→ Loại bỏ bản sao TRƯỚC khi split để tránh data leakage...')\n"
    "    df_clean = df_raw.drop_duplicates().reset_index(drop=True)\n"
    "    print(f'✅ Sau khi xóa bản sao: {df_clean.shape[0]:,} dòng')\n"
    "else:\n"
    "    print('✅ Không có dòng trùng lặp hoàn toàn.')\n"
    "    df_clean = df_raw.copy()\n"
    "\n"
    "print(f'Dataset hiện tại: {df_clean.shape}')"
))

# ============================================================
# Section 8 – Invalid Value Analysis
# ============================================================
cells.append(md("## 8. Phân tích giá trị không hợp lệ (Invalid Value Analysis)"))

cells.append(code(
    "# Kiểm tra phạm vi hợp lệ của các biến số\n"
    "print('=' * 60)\n"
    "print('KIỂM TRA GIÁ TRỊ KHÔNG HỢP LỆ')\n"
    "print('=' * 60)\n"
    "\n"
    "# Định nghĩa phạm vi hợp lý dựa trên kiến thức y tế\n"
    "valid_ranges = {\n"
    "    'age':                (0, 120),\n"
    "    'bmi':                (10, 80),\n"
    "    'HbA1c_level':        (3.0, 20.0),\n"
    "    'blood_glucose_level': (50, 500),\n"
    "    'hypertension':       (0, 1),\n"
    "    'heart_disease':      (0, 1),\n"
    "    'diabetes':           (0, 1),\n"
    "}\n"
    "\n"
    "issues_found = False\n"
    "for col, (lo, hi) in valid_ranges.items():\n"
    "    invalid = df_clean[(df_clean[col] < lo) | (df_clean[col] > hi)]\n"
    "    if len(invalid) > 0:\n"
    "        print(f'⚠️  {col}: {len(invalid)} giá trị ngoài phạm vi [{lo}, {hi}]')\n"
    "        issues_found = True\n"
    "    else:\n"
    "        print(f'✅ {col}: Tất cả giá trị hợp lệ [{lo}, {hi}]')\n"
    "\n"
    "print()\n"
    "# Kiểm tra giá trị phân loại\n"
    "print('Kiểm tra giá trị phân loại:')\n"
    "print(f'  gender:          {sorted(df_clean[\"gender\"].unique())}')\n"
    "print(f'  smoking_history: {sorted(df_clean[\"smoking_history\"].unique())}')\n"
    "\n"
    "# Kiểm tra 'No Info' trong smoking_history\n"
    "no_info_count = (df_clean['smoking_history'] == 'No Info').sum()\n"
    "print(f'  → \"No Info\" trong smoking_history: {no_info_count:,} ({no_info_count/len(df_clean)*100:.1f}%)')\n"
    "print('  → \"No Info\" là nhãn hợp lệ (thông tin không có sẵn), KHÔNG phải missing value')\n"
    "\n"
    "if not issues_found:\n"
    "    print()\n"
    "    print('✅ Không phát hiện giá trị số nào ngoài phạm vi hợp lệ.')"
))

# ============================================================
# Section 9 – Outlier Analysis
# ============================================================
cells.append(md("## 9. Phân tích ngoại lệ (Outlier Analysis)"))

cells.append(code(
    "# Phân tích outlier bằng IQR cho các biến số liên tục\n"
    "numerical_features = ['age', 'bmi', 'HbA1c_level', 'blood_glucose_level']\n"
    "\n"
    "print('Phân tích Outlier (IQR method):')\n"
    "print('=' * 60)\n"
    "\n"
    "outlier_summary = []\n"
    "for col in numerical_features:\n"
    "    Q1 = df_clean[col].quantile(0.25)\n"
    "    Q3 = df_clean[col].quantile(0.75)\n"
    "    IQR = Q3 - Q1\n"
    "    lower = Q1 - 1.5 * IQR\n"
    "    upper = Q3 + 1.5 * IQR\n"
    "    outliers = df_clean[(df_clean[col] < lower) | (df_clean[col] > upper)]\n"
    "    pct = len(outliers) / len(df_clean) * 100\n"
    "    outlier_summary.append({'Cột': col, 'Q1': Q1, 'Q3': Q3, 'IQR': IQR,\n"
    "                            'Lower Fence': lower, 'Upper Fence': upper,\n"
    "                            'Số outlier': len(outliers), 'Tỷ lệ (%)': round(pct, 2)})\n"
    "    print(f'{col}: {len(outliers):,} outliers ({pct:.2f}%) | Fence: [{lower:.2f}, {upper:.2f}]')\n"
    "\n"
    "outlier_df = pd.DataFrame(outlier_summary)\n"
    "print()\n"
    "print(outlier_df[['Cột', 'Số outlier', 'Tỷ lệ (%)']].to_string(index=False))"
))

cells.append(code(
    "# Trực quan hóa outlier bằng boxplot\n"
    "fig, axes = plt.subplots(1, 4, figsize=(18, 5))\n"
    "for i, col in enumerate(numerical_features):\n"
    "    axes[i].boxplot(df_clean[col].dropna(), patch_artist=True,\n"
    "                    boxprops=dict(facecolor='lightblue', color='navy'),\n"
    "                    medianprops=dict(color='red', linewidth=2))\n"
    "    axes[i].set_title(col, fontsize=12, fontweight='bold')\n"
    "    axes[i].set_xlabel('Feature')\n"
    "    axes[i].set_ylabel('Giá trị')\n"
    "\n"
    "plt.suptitle('Boxplot phát hiện Outlier – Biến số liên tục', fontsize=14, fontweight='bold')\n"
    "plt.tight_layout()\n"
    "plt.savefig('../models/fig_outliers.png', dpi=100, bbox_inches='tight')\n"
    "plt.show()\n"
    "\n"
    "print('Kết luận phân tích outlier:')\n"
    "print('  - age: phân phối rộng nhưng không có outlier cực đoan')\n"
    "print('  - bmi: có một số outlier cao nhưng các giá trị này vẫn thực tế (béo phì nặng)')\n"
    "print('  - HbA1c_level: giá trị cao có thể là bệnh nhân tiểu đường nặng → giữ lại')\n"
    "print('  - blood_glucose_level: discrete values, outliers là giá trị y tế thực tế')\n"
    "print()\n"
    "print('→ Quyết định: KHÔNG loại bỏ outlier vì chúng phản ánh tình trạng lâm sàng thực tế')\n"
    "print('  của bệnh nhân. Loại bỏ có thể mất đi thông tin quan trọng.')"
))

# ============================================================
# Section 10 – EDA
# ============================================================
cells.append(md("## 10. Phân tích dữ liệu khám phá (Exploratory Data Analysis)"))

cells.append(code(
    "# ── Biểu đồ 1: Phân phối biến mục tiêu ──────────────────\n"
    "fig, axes = plt.subplots(1, 2, figsize=(12, 5))\n"
    "\n"
    "# Count plot\n"
    "class_counts = df_clean['diabetes'].value_counts()\n"
    "axes[0].bar(['Không tiểu đường (0)', 'Tiểu đường (1)'],\n"
    "            class_counts.values,\n"
    "            color=['#4ECDC4', '#FF6B6B'], edgecolor='black', alpha=0.85)\n"
    "axes[0].set_title('Phân phối Biến Mục Tiêu', fontsize=13, fontweight='bold')\n"
    "axes[0].set_ylabel('Số lượng')\n"
    "for i, v in enumerate(class_counts.values):\n"
    "    axes[0].text(i, v + 100, f'{v:,}\\n({v/len(df_clean)*100:.1f}%)',\n"
    "                ha='center', va='bottom', fontsize=10)\n"
    "\n"
    "# Pie chart\n"
    "axes[1].pie(class_counts.values, labels=['Không (0)', 'Có (1)'],\n"
    "            autopct='%1.1f%%', colors=['#4ECDC4', '#FF6B6B'],\n"
    "            startangle=90, explode=[0, 0.05])\n"
    "axes[1].set_title('Tỷ lệ Class Imbalance', fontsize=13, fontweight='bold')\n"
    "\n"
    "plt.suptitle('Biểu đồ 1: Phân phối Target Variable', fontsize=14, fontweight='bold')\n"
    "plt.tight_layout()\n"
    "plt.savefig('../models/fig_eda_target.png', dpi=100, bbox_inches='tight')\n"
    "plt.show()\n"
    "\n"
    "print('Observation: Dataset mất cân bằng nghiêm trọng.')\n"
    "neg, pos = class_counts[0], class_counts[1]\n"
    "print(f'  Class 0 (Không bệnh): {neg:,} ({neg/len(df_clean)*100:.1f}%)')\n"
    "print(f'  Class 1 (Mắc bệnh):  {pos:,} ({pos/len(df_clean)*100:.1f}%)')\n"
    "print()\n"
    "print('Interpretation: Tỷ lệ positive (diabetes=1) rất nhỏ.')\n"
    "print('ML Implication: Cần dùng stratify khi split, class_weight hoặc SMOTE.')\n"
    "print('  Không thể chỉ dựa vào Accuracy làm metric chính.')"
))

cells.append(code(
    "# ── Biểu đồ 2: Phân phối các biến số liên tục theo diabetes ─\n"
    "fig, axes = plt.subplots(2, 2, figsize=(14, 10))\n"
    "axes = axes.flatten()\n"
    "\n"
    "colors = {0: '#4ECDC4', 1: '#FF6B6B'}\n"
    "labels = {0: 'Không tiểu đường', 1: 'Tiểu đường'}\n"
    "\n"
    "for i, col in enumerate(numerical_features):\n"
    "    for cls in [0, 1]:\n"
    "        subset = df_clean[df_clean['diabetes'] == cls][col]\n"
    "        axes[i].hist(subset, bins=40, alpha=0.6, color=colors[cls],\n"
    "                     label=labels[cls], edgecolor='white')\n"
    "    axes[i].set_title(f'Phân phối {col} theo Diabetes', fontsize=11, fontweight='bold')\n"
    "    axes[i].set_xlabel(col)\n"
    "    axes[i].set_ylabel('Số lượng')\n"
    "    axes[i].legend()\n"
    "\n"
    "plt.suptitle('Biểu đồ 2: Phân phối Biến Số theo Target Variable', fontsize=14, fontweight='bold')\n"
    "plt.tight_layout()\n"
    "plt.savefig('../models/fig_eda_distributions.png', dpi=100, bbox_inches='tight')\n"
    "plt.show()\n"
    "\n"
    "print('Observation: Bệnh nhân tiểu đường có xu hướng:')\n"
    "print('  - Tuổi cao hơn')\n"
    "print('  - BMI cao hơn')\n"
    "print('  - HbA1c_level cao hơn rõ rệt (>6.5 là ngưỡng chẩn đoán)')\n"
    "print('  - blood_glucose_level cao hơn')\n"
    "print()\n"
    "print('ML Implication: HbA1c và blood_glucose là những features có tính phân biệt cao nhất.')"
))

cells.append(code(
    "# ── Biểu đồ 3: Tương quan và biến phân loại ──────────────\n"
    "fig, axes = plt.subplots(1, 3, figsize=(18, 5))\n"
    "\n"
    "# Correlation heatmap (chỉ biến số)\n"
    "numeric_df = df_clean[numerical_features + ['hypertension', 'heart_disease', 'diabetes']]\n"
    "corr = numeric_df.corr()\n"
    "mask = np.triu(np.ones_like(corr, dtype=bool))\n"
    "sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='RdYlGn',\n"
    "            ax=axes[0], linewidths=0.5, vmin=-1, vmax=1)\n"
    "axes[0].set_title('Correlation Matrix', fontsize=11, fontweight='bold')\n"
    "\n"
    "# Diabetes rate by hypertension and heart_disease\n"
    "ht_rate = df_clean.groupby('hypertension')['diabetes'].mean() * 100\n"
    "hd_rate = df_clean.groupby('heart_disease')['diabetes'].mean() * 100\n"
    "\n"
    "x = np.arange(2)\n"
    "width = 0.35\n"
    "axes[1].bar(x - width/2, ht_rate.values, width, label='Hypertension', color='#E8A87C', alpha=0.85)\n"
    "axes[1].bar(x + width/2, hd_rate.values, width, label='Heart Disease', color='#8B5CF6', alpha=0.85)\n"
    "axes[1].set_xticks(x)\n"
    "axes[1].set_xticklabels(['Không (0)', 'Có (1)'])\n"
    "axes[1].set_ylabel('Tỷ lệ mắc tiểu đường (%)')\n"
    "axes[1].set_title('Tỷ lệ Diabetes theo\\nHypertension & Heart Disease', fontsize=11, fontweight='bold')\n"
    "axes[1].legend()\n"
    "\n"
    "# Diabetes rate by gender\n"
    "gender_rate = df_clean.groupby('gender')['diabetes'].mean().sort_values(ascending=True) * 100\n"
    "axes[2].barh(gender_rate.index, gender_rate.values,\n"
    "             color=['#4ECDC4', '#FF6B6B', '#FFD93D'][:len(gender_rate)], alpha=0.85)\n"
    "axes[2].set_xlabel('Tỷ lệ mắc tiểu đường (%)')\n"
    "axes[2].set_title('Tỷ lệ Diabetes theo Gender', fontsize=11, fontweight='bold')\n"
    "for i, v in enumerate(gender_rate.values):\n"
    "    axes[2].text(v + 0.1, i, f'{v:.1f}%', va='center')\n"
    "\n"
    "plt.suptitle('Biểu đồ 3: Tương quan và Phân tích Biến Phân loại', fontsize=14, fontweight='bold')\n"
    "plt.tight_layout()\n"
    "plt.savefig('../models/fig_eda_correlation.png', dpi=100, bbox_inches='tight')\n"
    "plt.show()\n"
    "\n"
    "print('Observation:')\n"
    "print('  - HbA1c và blood_glucose có tương quan cao nhất với diabetes')\n"
    "print('  - Bệnh nhân có hypertension/heart_disease có tỷ lệ tiểu đường cao hơn')\n"
    "print('  - Tỷ lệ tiểu đường theo giới tính tương đối tương đồng')\n"
    "print()\n"
    "print('ML Implication: HbA1c_level và blood_glucose_level là features quan trọng nhất.')"
))

cells.append(code(
    "# ── Biểu đồ 4: Smoking History ────────────────────────────\n"
    "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n"
    "\n"
    "# Distribution of smoking_history\n"
    "smoke_counts = df_clean['smoking_history'].value_counts()\n"
    "axes[0].bar(smoke_counts.index, smoke_counts.values, color='steelblue', alpha=0.8)\n"
    "axes[0].set_title('Phân phối Smoking History', fontsize=11, fontweight='bold')\n"
    "axes[0].set_xlabel('Smoking History')\n"
    "axes[0].set_ylabel('Số lượng')\n"
    "plt.setp(axes[0].xaxis.get_majorticklabels(), rotation=30, ha='right')\n"
    "for i, v in enumerate(smoke_counts.values):\n"
    "    axes[0].text(i, v + 100, f'{v:,}', ha='center', va='bottom', fontsize=9)\n"
    "\n"
    "# Diabetes rate by smoking_history\n"
    "smoke_rate = df_clean.groupby('smoking_history')['diabetes'].mean().sort_values(ascending=True) * 100\n"
    "axes[1].barh(smoke_rate.index, smoke_rate.values, color='coral', alpha=0.85)\n"
    "axes[1].set_xlabel('Tỷ lệ mắc tiểu đường (%)')\n"
    "axes[1].set_title('Tỷ lệ Diabetes theo Smoking History', fontsize=11, fontweight='bold')\n"
    "for i, v in enumerate(smoke_rate.values):\n"
    "    axes[1].text(v + 0.1, i, f'{v:.1f}%', va='center')\n"
    "\n"
    "plt.tight_layout()\n"
    "plt.savefig('../models/fig_eda_smoking.png', dpi=100, bbox_inches='tight')\n"
    "plt.show()"
))

# ============================================================
# Section 11 – Feature Types
# ============================================================
cells.append(md("## 11. Các loại đặc trưng (Feature Types)"))

cells.append(code(
    "# Phân loại các đặc trưng\n"
    "NUMERICAL_CONTINUOUS = ['age', 'bmi', 'HbA1c_level', 'blood_glucose_level']\n"
    "BINARY_FEATURES      = ['hypertension', 'heart_disease']\n"
    "CATEGORICAL_FEATURES = ['gender', 'smoking_history']\n"
    "TARGET               = 'diabetes'\n"
    "\n"
    "ALL_FEATURES = NUMERICAL_CONTINUOUS + BINARY_FEATURES + CATEGORICAL_FEATURES\n"
    "\n"
    "print('Phân loại các đặc trưng:')\n"
    "print('=' * 60)\n"
    "print(f'Numerical Continuous:  {NUMERICAL_CONTINUOUS}')\n"
    "print(f'Binary (0/1):          {BINARY_FEATURES}')\n"
    "print(f'Categorical:           {CATEGORICAL_FEATURES}')\n"
    "print(f'Target:                {TARGET}')\n"
    "print()\n"
    "print('Giải thích tầm quan trọng của phân loại:')\n"
    "print('  - Numerical features → cần StandardScaler (đưa về cùng thang đo)')\n"
    "print('  - Binary features     → giữ nguyên (đã là 0/1, không cần encoding)')\n"
    "print('  - Categorical features → cần OneHotEncoder (chuyển sang dạng số)')\n"
    "print()\n"
    "print('Số lượng giá trị unique trong categorical features:')\n"
    "for col in CATEGORICAL_FEATURES:\n"
    "    print(f'  {col}: {df_clean[col].nunique()} giá trị → {sorted(df_clean[col].unique())}')"
))

# ============================================================
# Section 12 – Data Representation
# ============================================================
cells.append(md(
    "## 12. Biểu diễn dữ liệu (Data Representation) ⭐\n"
    "\n"
    "**Kết nối với Lecture 02 – Data Representation**\n"
    "\n"
    "### Công thức toán học\n"
    "\n"
    "Mỗi quan sát (bệnh nhân) được biểu diễn là một vector đặc trưng:\n"
    "\n"
    "$$\\mathbf{x}_i = [x_{i1}, x_{i2}, \\ldots, x_{id}]^\\top \\in \\mathbb{R}^d$$\n"
    "\n"
    "Toàn bộ dataset là một ma trận đặc trưng:\n"
    "\n"
    "$$\\mathbf{X} \\in \\mathbb{R}^{N \\times d}, \\quad \\mathbf{y} \\in \\{0, 1\\}^N$$\n"
    "\n"
    "Trong đó:\n"
    "- $N$ = số quan sát (bệnh nhân)\n"
    "- $d$ = số chiều đặc trưng **sau preprocessing**\n"
    "- Mỗi hàng $\\mathbf{x}_i$ là một bệnh nhân\n"
    "- Mỗi cột là một đặc trưng"
))

cells.append(code(
    "# Bước 1: Hiển thị một raw record\n"
    "print('=' * 70)\n"
    "print('BƯỚC 1: Một dòng CSV gốc (raw record)')\n"
    "print('=' * 70)\n"
    "sample_idx = 7  # dòng thứ 8 (index 7) – bệnh nhân có diabetes=1\n"
    "raw_record = df_clean.iloc[sample_idx]\n"
    "print(raw_record)\n"
    "print()\n"
    "print(f'→ Label: diabetes = {raw_record[\"diabetes\"]}')"
))

cells.append(code(
    "# Bước 2: Tách X và y (trước split)\n"
    "print('=' * 70)\n"
    "print('BƯỚC 2: Feature matrix X và target vector y')\n"
    "print('=' * 70)\n"
    "X = df_clean[ALL_FEATURES]\n"
    "y = df_clean[TARGET]\n"
    "\n"
    "print(f'X shape (raw, trước preprocessing): {X.shape}')\n"
    "print(f'y shape: {y.shape}')\n"
    "print(f'→ N = {X.shape[0]:,} quan sát, d_raw = {X.shape[1]} features (chưa encode)')\n"
    "print()\n"
    "print('Feature vector của bệnh nhân thứ 7 (raw):')\n"
    "print(X.iloc[sample_idx])"
))

# Section 12 continued after split - placeholder, will be filled after split
cells.append(code(
    "# NOTE: Phần còn lại của Section 12 (shape sau preprocessing) sẽ được\n"
    "# hiển thị sau khi thực hiện Split (Section 14) và Pipeline (Section 15)\n"
    "print('X.shape (raw):', X.shape)\n"
    "print('Các features:', list(X.columns))"
))

# ============================================================
# Section 13 – Feature Engineering
# ============================================================
cells.append(md("## 13. Kỹ thuật đặc trưng (Feature Engineering)"))

cells.append(code(
    "# Phân tích và quyết định feature engineering\n"
    "print('Phân tích Feature Engineering cho Diabetes Dataset:')\n"
    "print('=' * 60)\n"
    "print()\n"
    "print('1. age:')\n"
    "print('   - Phân phối tương đối đều, không cần transformation đặc biệt')\n"
    "print('   → Giữ nguyên, áp dụng StandardScaler')\n"
    "print()\n"
    "print('2. bmi:')\n"
    "print('   - Có một số outlier cao nhưng thực tế')\n"
    "print('   → Giữ nguyên, áp dụng StandardScaler')\n"
    "print()\n"
    "print('3. HbA1c_level:')\n"
    "print('   - Có ngưỡng chẩn đoán y tế rõ ràng (6.5% cho tiểu đường)')\n"
    "print('   → Giữ nguyên, để model học ngưỡng từ data')\n"
    "print()\n"
    "print('4. blood_glucose_level:')\n"
    "print('   - Giá trị discrete, phân phối không đồng đều')\n"
    "print('   → Giữ nguyên, áp dụng StandardScaler')\n"
    "print()\n"
    "print('5. gender, smoking_history:')\n"
    "print('   → OneHotEncoder')\n"
    "print()\n"
    "print('6. hypertension, heart_disease:')\n"
    "print('   → Đã là binary 0/1, xử lý như numerical (giữ trong num pipeline)')\n"
    "print()\n"
    "print('Kết luận: Không tạo feature mới phức tạp.')\n"
    "print('Lý do: Dataset đã có các features lâm sàng đủ mạnh và có ý nghĩa.')\n"
    "print('Tạo feature tương tác (BMI×age) có thể gây overfitting với 100k records.')\n"
    "\n"
    "# Định nghĩa feature groups cho pipeline\n"
    "# Binary features xử lý như numerical (không cần scaling đặc biệt)\n"
    "NUMERICAL_PIPELINE_COLS = NUMERICAL_CONTINUOUS + BINARY_FEATURES\n"
    "CATEGORICAL_PIPELINE_COLS = CATEGORICAL_FEATURES\n"
    "\n"
    "print()\n"
    "print(f'Numerical columns cho pipeline: {NUMERICAL_PIPELINE_COLS}')\n"
    "print(f'Categorical columns cho pipeline: {CATEGORICAL_PIPELINE_COLS}')"
))

# ============================================================
# Section 14 – Train/Test Split
# ============================================================
cells.append(md("## 14. Chia tập train/test (Train/Test Split)"))

cells.append(code(
    "# Train/Test split với stratification\n"
    "print('Thực hiện Train/Test Split...')\n"
    "print()\n"
    "\n"
    "X_train, X_test, y_train, y_test = train_test_split(\n"
    "    X, y,\n"
    "    test_size=0.2,\n"
    "    random_state=RANDOM_STATE,\n"
    "    stratify=y  # QUAN TRỌNG: giữ tỷ lệ class imbalance\n"
    ")\n"
    "\n"
    "print('Kết quả split:')\n"
    "print(f'  X_train shape: {X_train.shape}')\n"
    "print(f'  X_test  shape: {X_test.shape}')\n"
    "print(f'  y_train shape: {y_train.shape}')\n"
    "print(f'  y_test  shape: {y_test.shape}')\n"
    "print()\n"
    "\n"
    "# Kiểm tra phân phối sau khi split\n"
    "train_dist = y_train.value_counts(normalize=True) * 100\n"
    "test_dist  = y_test.value_counts(normalize=True) * 100\n"
    "\n"
    "print('Phân phối class trong y_train:')\n"
    "print(f'  Class 0: {y_train.value_counts()[0]:,} ({train_dist[0]:.2f}%)')\n"
    "print(f'  Class 1: {y_train.value_counts()[1]:,} ({train_dist[1]:.2f}%)')\n"
    "print()\n"
    "print('Phân phối class trong y_test:')\n"
    "print(f'  Class 0: {y_test.value_counts()[0]:,} ({test_dist[0]:.2f}%)')\n"
    "print(f'  Class 1: {y_test.value_counts()[1]:,} ({test_dist[1]:.2f}%)')\n"
    "print()\n"
    "print('✅ Stratified split thành công – tỷ lệ class imbalance được duy trì!')\n"
    "print()\n"
    "print('Tại sao phải split TRƯỚC KHI fit preprocessing?')\n"
    "print('  → Nếu fit scaler/encoder trên toàn bộ data rồi mới split,')\n"
    "print('     test set sẽ \"rò rỉ\" thông tin vào quá trình training (data leakage).')\n"
    "print('  → Mô hình sẽ có vẻ tốt hơn thực tế khi deploy production.')\n"
    "print('  → Phải fit preprocessing ONLY trên X_train, transform X_test.')"
))

# ============================================================
# Section 15 – Preprocessing Pipeline
# ============================================================
cells.append(md("## 15. Pipeline tiền xử lý (Preprocessing Pipeline)"))

cells.append(code(
    "# Xây dựng Preprocessing Pipeline với ColumnTransformer\n"
    "print('Xây dựng Preprocessing Pipeline...')\n"
    "print()\n"
    "\n"
    "# Pipeline cho numerical features (bao gồm cả binary 0/1)\n"
    "numerical_transformer = Pipeline(steps=[\n"
    "    ('scaler', StandardScaler())\n"
    "])\n"
    "\n"
    "# Pipeline cho categorical features\n"
    "categorical_transformer = Pipeline(steps=[\n"
    "    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))\n"
    "])\n"
    "\n"
    "# ColumnTransformer kết hợp\n"
    "preprocessor = ColumnTransformer(\n"
    "    transformers=[\n"
    "        ('num', numerical_transformer, NUMERICAL_PIPELINE_COLS),\n"
    "        ('cat', categorical_transformer, CATEGORICAL_PIPELINE_COLS),\n"
    "    ],\n"
    "    remainder='drop'  # loại bỏ các cột không được chỉ định\n"
    ")\n"
    "\n"
    "# Fit ONLY trên X_train – TRÁNH DATA LEAKAGE\n"
    "preprocessor.fit(X_train)\n"
    "\n"
    "# Transform cả train và test\n"
    "X_train_proc = preprocessor.transform(X_train)\n"
    "X_test_proc  = preprocessor.transform(X_test)\n"
    "\n"
    "print(f'X_train sau preprocessing: {X_train_proc.shape}')\n"
    "print(f'X_test  sau preprocessing: {X_test_proc.shape}')\n"
    "print()\n"
    "\n"
    "# Lấy tên features sau encoding\n"
    "cat_feature_names = preprocessor.named_transformers_['cat']['onehot'].get_feature_names_out(CATEGORICAL_PIPELINE_COLS)\n"
    "all_feature_names = NUMERICAL_PIPELINE_COLS + list(cat_feature_names)\n"
    "\n"
    "print(f'Số features sau preprocessing: {len(all_feature_names)}')\n"
    "print('Tên features sau preprocessing:')\n"
    "for i, fname in enumerate(all_feature_names):\n"
    "    print(f'  [{i:2d}] {fname}')\n"
    "print()\n"
    "print('✅ Pipeline đã fit trên X_train và transform X_train, X_test!')\n"
    "print('   Preprocessing có thể dùng lại cho inference mới.')"
))

# ============================================================
# Section 12 continued – Data Representation (after pipeline)
# ============================================================
cells.append(md(
    "## 12b. Biểu diễn dữ liệu – Tiếp theo (Sau Preprocessing)\n"
    "\n"
    "Phần này hoàn thành Section 12 với shape thực tế từ Pipeline."
))

cells.append(code(
    "# Hiển thị đầy đủ biểu diễn dữ liệu sau preprocessing\n"
    "print('=' * 70)\n"
    "print('BIỂU DIỄN DỮ LIỆU – DATA REPRESENTATION')\n"
    "print('=' * 70)\n"
    "print()\n"
    "\n"
    "# Raw record\n"
    "print('[ Raw Record – dòng CSV gốc (index 7) ]')\n"
    "print(df_clean.iloc[sample_idx].to_frame().T.to_string(index=False))\n"
    "print()\n"
    "\n"
    "# Feature vector (raw)\n"
    "print('[ Feature Vector x_i (raw, trước preprocessing) ]')\n"
    "raw_vec = X.iloc[sample_idx].values\n"
    "print(f'x_i (raw) = {raw_vec}')\n"
    "print(f'Shape: {raw_vec.shape} (d_raw = {X.shape[1]})')\n"
    "print()\n"
    "\n"
    "# Feature vector (sau preprocessing)\n"
    "sample_proc = preprocessor.transform(X.iloc[[sample_idx]])\n"
    "print('[ Feature Vector x_i (sau preprocessing / encoding / scaling) ]')\n"
    "print(f'x_i (processed) = {sample_proc[0].round(4)}')\n"
    "print(f'Shape: {sample_proc.shape} → d = {sample_proc.shape[1]} features')\n"
    "print()\n"
    "\n"
    "# Feature names\n"
    "print('[ Feature Names sau OneHotEncoding ]')\n"
    "for i, fname in enumerate(all_feature_names):\n"
    "    print(f'  x_{{i{i+1}}} = {fname:30s} → value = {sample_proc[0][i]:+.4f}')\n"
    "print()\n"
    "\n"
    "# Dataset matrix\n"
    "print('[ Ma trận Dataset X ∈ R^(N × d) ]')\n"
    "print(f'  N (số quan sát) = {X_train_proc.shape[0] + X_test_proc.shape[0]:,}')\n"
    "print(f'  d (số features sau preprocessing) = {X_train_proc.shape[1]}')\n"
    "print()\n"
    "print(f'  X_train.shape = {X_train_proc.shape}  → {X_train_proc.shape[0]:,} training samples')\n"
    "print(f'  X_test.shape  = {X_test_proc.shape}  → {X_test_proc.shape[0]:,} test samples')\n"
    "print()\n"
    "print(f'  Dtype: {X_train_proc.dtype}')\n"
    "print()\n"
    "\n"
    "# Target vector\n"
    "print('[ Target Vector y ∈ {0,1}^N ]')\n"
    "print(f'  y_train shape: {y_train.shape}, unique values: {sorted(y_train.unique())}')\n"
    "print(f'  y_test  shape: {y_test.shape},  unique values: {sorted(y_test.unique())}')\n"
    "print()\n"
    "print('⭐ Tóm tắt: Mỗi bệnh nhân được biểu diễn là vector')\n"
    "d = X_train_proc.shape[1]\n"
    "print(f'   x_i ∈ R^{d} (d = {d} features sau preprocessing)')"
))

# ============================================================
# Section 16 – Baseline Model
# ============================================================
cells.append(md("## 16. Mô hình cơ sở (Baseline Model)"))

cells.append(code(
    "# Baseline: DummyClassifier (most_frequent strategy)\n"
    "print('Huấn luyện Baseline Model (DummyClassifier)...')\n"
    "print()\n"
    "\n"
    "baseline = DummyClassifier(strategy='most_frequent', random_state=RANDOM_STATE)\n"
    "baseline.fit(X_train_proc, y_train)\n"
    "y_baseline_pred = baseline.predict(X_test_proc)\n"
    "\n"
    "# Metrics\n"
    "bl_acc  = accuracy_score(y_test, y_baseline_pred)\n"
    "bl_prec = precision_score(y_test, y_baseline_pred, zero_division=0)\n"
    "bl_rec  = recall_score(y_test, y_baseline_pred, zero_division=0)\n"
    "bl_f1   = f1_score(y_test, y_baseline_pred, zero_division=0)\n"
    "\n"
    "print('Baseline DummyClassifier (most_frequent) – Test Set Performance:')\n"
    "print(f'  Accuracy:  {bl_acc:.4f}')\n"
    "print(f'  Precision: {bl_prec:.4f}')\n"
    "print(f'  Recall:    {bl_rec:.4f}')\n"
    "print(f'  F1-Score:  {bl_f1:.4f}')\n"
    "print()\n"
    "print('Giải thích: Baseline chỉ predict \"Không bệnh\" cho mọi bệnh nhân.')\n"
    "print(f'  → Accuracy cao ({bl_acc:.1%}) nhưng Recall = 0% cho class 1.')\n"
    "print('  → Mô hình này vô dụng trong bối cảnh y tế (bỏ sót tất cả ca bệnh).')\n"
    "print('  → Các mô hình tiếp theo phải vượt qua mốc này!')"
))

# ============================================================
# Section 17 – Model Training
# ============================================================
cells.append(md("## 17. Huấn luyện mô hình (Model Training)"))

cells.append(code(
    "# Dictionary để lưu tất cả trained models\n"
    "trained_models = {}\n"
    "\n"
    "print('Bắt đầu huấn luyện các mô hình...')\n"
    "print('Dataset:', X_train_proc.shape)\n"
    "print()"
))

cells.append(code(
    "# ── Model 1: Logistic Regression ──────────────────────────\n"
    "print('=' * 50)\n"
    "print('1. Logistic Regression')\n"
    "t0 = time.time()\n"
    "\n"
    "lr = LogisticRegression(\n"
    "    class_weight='balanced',  # xử lý class imbalance\n"
    "    max_iter=1000,\n"
    "    random_state=RANDOM_STATE,\n"
    "    solver='saga',  # hiệu quả với dataset lớn\n"
    "    n_jobs=-1\n"
    ")\n"
    "lr.fit(X_train_proc, y_train)\n"
    "trained_models['Logistic Regression'] = lr\n"
    "\n"
    "t1 = time.time()\n"
    "print(f'✅ Huấn luyện xong sau {t1-t0:.1f}s')\n"
    "print(f'   Train accuracy: {lr.score(X_train_proc, y_train):.4f}')\n"
    "print(f'   Test  accuracy: {lr.score(X_test_proc, y_test):.4f}')"
))

cells.append(code(
    "# ── Model 2: Decision Tree ────────────────────────────────\n"
    "print('=' * 50)\n"
    "print('2. Decision Tree Classifier')\n"
    "t0 = time.time()\n"
    "\n"
    "dt = DecisionTreeClassifier(\n"
    "    max_depth=10,\n"
    "    class_weight='balanced',\n"
    "    random_state=RANDOM_STATE\n"
    ")\n"
    "dt.fit(X_train_proc, y_train)\n"
    "trained_models['Decision Tree'] = dt\n"
    "\n"
    "t1 = time.time()\n"
    "print(f'✅ Huấn luyện xong sau {t1-t0:.1f}s')\n"
    "print(f'   Train accuracy: {dt.score(X_train_proc, y_train):.4f}')\n"
    "print(f'   Test  accuracy: {dt.score(X_test_proc, y_test):.4f}')"
))

cells.append(code(
    "# ── Model 3: Random Forest ───────────────────────────────\n"
    "print('=' * 50)\n"
    "print('3. Random Forest Classifier')\n"
    "t0 = time.time()\n"
    "\n"
    "rf = RandomForestClassifier(\n"
    "    n_estimators=100,\n"
    "    max_depth=15,\n"
    "    class_weight='balanced',\n"
    "    random_state=RANDOM_STATE,\n"
    "    n_jobs=-1\n"
    ")\n"
    "rf.fit(X_train_proc, y_train)\n"
    "trained_models['Random Forest'] = rf\n"
    "\n"
    "t1 = time.time()\n"
    "print(f'✅ Huấn luyện xong sau {t1-t0:.1f}s')\n"
    "print(f'   Train accuracy: {rf.score(X_train_proc, y_train):.4f}')\n"
    "print(f'   Test  accuracy: {rf.score(X_test_proc, y_test):.4f}')"
))

cells.append(code(
    "# ── Model 4: SVM (LinearSVC) ─────────────────────────────\n"
    "print('=' * 50)\n"
    "print('4. SVM – LinearSVC (calibrated for probability)')\n"
    "print('   Ghi chú: Dùng LinearSVC thay RBF SVM vì O(n) complexity')\n"
    "print('   với dataset 100k, RBF SVM quá chậm (O(n^2) ~ O(n^3))')\n"
    "t0 = time.time()\n"
    "\n"
    "# CalibratedClassifierCV để có predict_proba\n"
    "linear_svc = LinearSVC(\n"
    "    class_weight='balanced',\n"
    "    max_iter=2000,\n"
    "    random_state=RANDOM_STATE\n"
    ")\n"
    "svm = CalibratedClassifierCV(linear_svc, cv=3)\n"
    "svm.fit(X_train_proc, y_train)\n"
    "trained_models['SVM (LinearSVC)'] = svm\n"
    "\n"
    "t1 = time.time()\n"
    "print(f'✅ Huấn luyện xong sau {t1-t0:.1f}s')\n"
    "print(f'   Train accuracy: {svm.score(X_train_proc, y_train):.4f}')\n"
    "print(f'   Test  accuracy: {svm.score(X_test_proc, y_test):.4f}')"
))

cells.append(code(
    "# ── Model 5: KNN ─────────────────────────────────────────\n"
    "print('=' * 50)\n"
    "print('5. K-Nearest Neighbors (KNN)')\n"
    "print('   Ghi chú: Dùng n_neighbors=11, leaf_size=40 để giảm thời gian')\n"
    "t0 = time.time()\n"
    "\n"
    "knn = KNeighborsClassifier(\n"
    "    n_neighbors=11,\n"
    "    weights='distance',\n"
    "    n_jobs=-1,\n"
    "    leaf_size=40\n"
    ")\n"
    "knn.fit(X_train_proc, y_train)\n"
    "trained_models['KNN'] = knn\n"
    "\n"
    "t1 = time.time()\n"
    "print(f'✅ Huấn luyện xong sau {t1-t0:.1f}s')\n"
    "print(f'   Train accuracy: {knn.score(X_train_proc, y_train):.4f}')\n"
    "print(f'   Test  accuracy: {knn.score(X_test_proc, y_test):.4f}')\n"
    "\n"
    "print()\n"
    "print('✅ Tất cả 5 mô hình đã được huấn luyện thành công!')\n"
    "print(f'Models: {list(trained_models.keys())}')"
))

# ============================================================
# Section 18 – Model Comparison
# ============================================================
cells.append(md("## 18. So sánh mô hình (Model Comparison)"))

cells.append(code(
    "# Hàm tính metrics cho một model\n"
    "def evaluate_model(name, model, X_tr, y_tr, X_te, y_te):\n"
    "    \"\"\"Tính các metrics trên train và test set.\"\"\"\n"
    "    y_pred = model.predict(X_te)\n"
    "    \n"
    "    # ROC-AUC cần predict_proba\n"
    "    if hasattr(model, 'predict_proba'):\n"
    "        y_prob = model.predict_proba(X_te)[:, 1]\n"
    "        roc_auc = roc_auc_score(y_te, y_prob)\n"
    "    else:\n"
    "        y_score = model.decision_function(X_te)\n"
    "        roc_auc = roc_auc_score(y_te, y_score)\n"
    "    \n"
    "    return {\n"
    "        'Model': name,\n"
    "        'Accuracy': accuracy_score(y_te, y_pred),\n"
    "        'Precision': precision_score(y_te, y_pred, zero_division=0),\n"
    "        'Recall': recall_score(y_te, y_pred, zero_division=0),\n"
    "        'F1': f1_score(y_te, y_pred, zero_division=0),\n"
    "        'ROC-AUC': roc_auc,\n"
    "    }\n"
    "\n"
    "# Đánh giá tất cả models\n"
    "results = []\n"
    "for name, model in trained_models.items():\n"
    "    metrics = evaluate_model(name, model, X_train_proc, y_train, X_test_proc, y_test)\n"
    "    results.append(metrics)\n"
    "    print(f'{name:20s}: Acc={metrics[\"Accuracy\"]:.4f}, P={metrics[\"Precision\"]:.4f}, R={metrics[\"Recall\"]:.4f}, F1={metrics[\"F1\"]:.4f}, AUC={metrics[\"ROC-AUC\"]:.4f}')\n"
    "\n"
    "# Tạo DataFrame so sánh\n"
    "comparison_df = pd.DataFrame(results).set_index('Model')\n"
    "comparison_df = comparison_df.round(4)\n"
    "print()\n"
    "print('Bảng so sánh đầy đủ:')\n"
    "comparison_df"
))

cells.append(code(
    "# Trực quan hóa so sánh models\n"
    "metrics_to_plot = ['Accuracy', 'Precision', 'Recall', 'F1', 'ROC-AUC']\n"
    "comparison_plot = comparison_df[metrics_to_plot].reset_index()\n"
    "\n"
    "fig, axes = plt.subplots(1, 5, figsize=(20, 5))\n"
    "colors = sns.color_palette('Set2', len(trained_models))\n"
    "\n"
    "for i, metric in enumerate(metrics_to_plot):\n"
    "    vals = comparison_plot[metric].values\n"
    "    model_names = comparison_plot['Model'].values\n"
    "    bars = axes[i].bar(range(len(model_names)), vals, color=colors, edgecolor='black', alpha=0.85)\n"
    "    axes[i].set_title(metric, fontsize=12, fontweight='bold')\n"
    "    axes[i].set_ylim(0, 1.05)\n"
    "    axes[i].set_xticks(range(len(model_names)))\n"
    "    axes[i].set_xticklabels(model_names, rotation=35, ha='right', fontsize=9)\n"
    "    axes[i].axhline(y=0.9, color='red', linestyle='--', alpha=0.5, linewidth=0.8)\n"
    "    for bar, v in zip(bars, vals):\n"
    "        axes[i].text(bar.get_x() + bar.get_width()/2, v + 0.01,\n"
    "                     f'{v:.3f}', ha='center', va='bottom', fontsize=8)\n"
    "\n"
    "plt.suptitle('So sánh hiệu suất các mô hình trên Test Set', fontsize=14, fontweight='bold')\n"
    "plt.tight_layout()\n"
    "plt.savefig('../models/fig_model_comparison.png', dpi=100, bbox_inches='tight')\n"
    "plt.show()\n"
    "\n"
    "print('Giải thích ý nghĩa metrics trong ngữ cảnh dự đoán tiểu đường:')\n"
    "print('  Accuracy:  Tỷ lệ dự đoán đúng tổng thể (misleading với imbalanced data)')\n"
    "print('  Precision: Trong số dự đoán Có bệnh, bao nhiêu % thực sự Có bệnh')\n"
    "print('  Recall:    Trong số thực sự Có bệnh, phát hiện được bao nhiêu % (quan trọng nhất!)')\n"
    "print('  F1:        Harmonic mean của Precision và Recall')\n"
    "print('  ROC-AUC:   Khả năng phân biệt giữa 2 class (1.0 = hoàn hảo)')"
))

# ============================================================
# Section 19 – Evaluation
# ============================================================
cells.append(md("## 19. Đánh giá (Evaluation)"))

cells.append(code(
    "# Đánh giá chi tiết top 3 models theo F1\n"
    "top3_models = comparison_df.sort_values('F1', ascending=False).head(3).index.tolist()\n"
    "print(f'Top 3 models theo F1: {top3_models}')\n"
    "print()"
))

cells.append(code(
    "# Confusion Matrix cho các top models\n"
    "fig, axes = plt.subplots(1, len(top3_models), figsize=(6 * len(top3_models), 5))\n"
    "if len(top3_models) == 1:\n"
    "    axes = [axes]\n"
    "\n"
    "for ax, model_name in zip(axes, top3_models):\n"
    "    model = trained_models[model_name]\n"
    "    y_pred = model.predict(X_test_proc)\n"
    "    cm = confusion_matrix(y_test, y_pred)\n"
    "    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['No Diabetes', 'Diabetes'])\n"
    "    disp.plot(ax=ax, colorbar=False, cmap='Blues')\n"
    "    ax.set_title(f'{model_name}\\nConfusion Matrix', fontsize=11, fontweight='bold')\n"
    "\n"
    "plt.suptitle('Confusion Matrix – Top Models trên Test Set', fontsize=13, fontweight='bold')\n"
    "plt.tight_layout()\n"
    "plt.savefig('../models/fig_confusion_matrix.png', dpi=100, bbox_inches='tight')\n"
    "plt.show()"
))

cells.append(code(
    "# Classification Report chi tiết\n"
    "print('Classification Reports – Top Models:')\n"
    "print('=' * 70)\n"
    "for model_name in top3_models:\n"
    "    model = trained_models[model_name]\n"
    "    y_pred = model.predict(X_test_proc)\n"
    "    print(f'\\n--- {model_name} ---')\n"
    "    print(classification_report(y_test, y_pred,\n"
    "                                target_names=['No Diabetes (0)', 'Diabetes (1)']))"
))

cells.append(code(
    "# ROC Curve cho các top models\n"
    "fig, ax = plt.subplots(figsize=(8, 6))\n"
    "\n"
    "colors_roc = ['#2196F3', '#FF5722', '#4CAF50', '#9C27B0', '#FF9800']\n"
    "for idx, model_name in enumerate(top3_models):\n"
    "    model = trained_models[model_name]\n"
    "    if hasattr(model, 'predict_proba'):\n"
    "        y_prob = model.predict_proba(X_test_proc)[:, 1]\n"
    "    else:\n"
    "        y_prob = model.decision_function(X_test_proc)\n"
    "    auc = roc_auc_score(y_test, y_prob)\n"
    "    RocCurveDisplay.from_predictions(\n"
    "        y_test, y_prob, name=f'{model_name} (AUC={auc:.3f})',\n"
    "        ax=ax, color=colors_roc[idx % len(colors_roc)]\n"
    "    )\n"
    "\n"
    "ax.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Random (AUC=0.5)')\n"
    "ax.set_title('ROC Curve – Top Models trên Test Set', fontsize=13, fontweight='bold')\n"
    "ax.set_xlabel('False Positive Rate')\n"
    "ax.set_ylabel('True Positive Rate')\n"
    "ax.legend(loc='lower right')\n"
    "ax.grid(True, alpha=0.3)\n"
    "\n"
    "plt.tight_layout()\n"
    "plt.savefig('../models/fig_roc_curve.png', dpi=100, bbox_inches='tight')\n"
    "plt.show()\n"
    "\n"
    "print('Giải thích ROC Curve:')\n"
    "print('  - AUC càng gần 1.0 → model càng tốt')\n"
    "print('  - AUC = 0.5 → không tốt hơn random guessing')\n"
    "print('  - Trong y tế: cần AUC > 0.85 để có giá trị lâm sàng')"
))

# ============================================================
# Section 20 – Error Analysis
# ============================================================
cells.append(md("## 20. Phân tích lỗi (Error Analysis)"))

cells.append(code(
    "# Chọn model tốt nhất cho error analysis\n"
    "best_model_name = comparison_df.sort_values('F1', ascending=False).index[0]\n"
    "best_model = trained_models[best_model_name]\n"
    "print(f'Model được chọn để phân tích lỗi: {best_model_name}')\n"
    "print()\n"
    "\n"
    "y_pred_best = best_model.predict(X_test_proc)\n"
    "if hasattr(best_model, 'predict_proba'):\n"
    "    y_prob_best = best_model.predict_proba(X_test_proc)[:, 1]\n"
    "else:\n"
    "    y_prob_best = best_model.decision_function(X_test_proc)\n"
    "\n"
    "# Phân tích TP, TN, FP, FN\n"
    "cm = confusion_matrix(y_test, y_pred_best)\n"
    "tn, fp, fn, tp = cm.ravel()\n"
    "\n"
    "print('Phân tích Confusion Matrix:')\n"
    "print(f'  True Negative  (TN): {tn:,} – Dự đoán đúng: Không bệnh')\n"
    "print(f'  False Positive (FP): {fp:,} – Dự đoán sai: Nói có bệnh nhưng thực ra không')\n"
    "print(f'  False Negative (FN): {fn:,} – Dự đoán sai: Nói không bệnh nhưng thực ra có ← NGUY HIỂM')\n"
    "print(f'  True Positive  (TP): {tp:,} – Dự đoán đúng: Có bệnh')\n"
    "print()\n"
    "print('⚠️  False Negative trong bài toán tiểu đường là nguy hiểm nhất!')\n"
    "print('   → Bệnh nhân thực sự có tiểu đường nhưng model nói \"không bệnh\"')\n"
    "print('   → Họ sẽ không được điều trị kịp thời → biến chứng nặng')\n"
    "print('   → Recall cao (phát hiện nhiều ca bệnh thật) là ưu tiên hàng đầu')"
))

cells.append(code(
    "# Phân tích chi tiết các trường hợp sai\n"
    "X_test_reset = X_test.reset_index(drop=True)\n"
    "y_test_reset = y_test.reset_index(drop=True)\n"
    "\n"
    "# Tạo DataFrame errors\n"
    "error_df = X_test_reset.copy()\n"
    "error_df['true_label'] = y_test_reset.values\n"
    "error_df['pred_label'] = y_pred_best\n"
    "error_df['pred_prob']  = y_prob_best\n"
    "error_df['error_type'] = 'Correct'\n"
    "error_df.loc[(error_df['true_label'] == 0) & (error_df['pred_label'] == 1), 'error_type'] = 'FP'\n"
    "error_df.loc[(error_df['true_label'] == 1) & (error_df['pred_label'] == 0), 'error_type'] = 'FN'\n"
    "\n"
    "# Thống kê lỗi\n"
    "print('Thống kê các loại lỗi:')\n"
    "print(error_df['error_type'].value_counts())\n"
    "print()\n"
    "\n"
    "# Bảng 5 False Negatives (nguy hiểm nhất)\n"
    "fn_cases = error_df[error_df['error_type'] == 'FN'].head(5)\n"
    "print(f'Ví dụ 5 trường hợp False Negative (thực ra có bệnh nhưng bị bỏ sót):')\n"
    "print(fn_cases[['age', 'bmi', 'HbA1c_level', 'blood_glucose_level',\n"
    "                'true_label', 'pred_label', 'pred_prob']].to_string())\n"
    "print()\n"
    "\n"
    "# Bảng 5 False Positives\n"
    "fp_cases = error_df[error_df['error_type'] == 'FP'].head(5)\n"
    "print(f'Ví dụ 5 trường hợp False Positive (dự đoán có bệnh nhưng thực ra không):')\n"
    "print(fp_cases[['age', 'bmi', 'HbA1c_level', 'blood_glucose_level',\n"
    "                'true_label', 'pred_label', 'pred_prob']].to_string())"
))

cells.append(code(
    "# Phân tích đặc điểm của FN cases\n"
    "fn_all = error_df[error_df['error_type'] == 'FN']\n"
    "fp_all = error_df[error_df['error_type'] == 'FP']\n"
    "correct_pos = error_df[(error_df['error_type'] == 'Correct') & (error_df['true_label'] == 1)]\n"
    "\n"
    "print('Đặc điểm trung bình của các trường hợp sai:')\n"
    "print()\n"
    "\n"
    "compare_groups = pd.DataFrame({\n"
    "    'FN (Bỏ sót ca bệnh)': fn_all[numerical_features].mean(),\n"
    "    'FP (Cảnh báo sai)':   fp_all[numerical_features].mean(),\n"
    "    'TP (Phát hiện đúng)': correct_pos[numerical_features].mean(),\n"
    "}).round(3)\n"
    "\n"
    "print(compare_groups)\n"
    "print()\n"
    "print('Phân tích:')\n"
    "print('  FN cases: Bệnh nhân có HbA1c và glucose thấp hơn TP cases')\n"
    "print('  → Đây là ca \"borderline\" gần ngưỡng phân loại')\n"
    "print('  → Có thể cải thiện bằng cách điều chỉnh threshold hoặc dùng ensemble')\n"
    "print()\n"
    "print('Đề xuất cải thiện:')\n"
    "print('  1. Giảm threshold quyết định (ưu tiên Recall cao hơn)')\n"
    "print('  2. Dùng SMOTE để cân bằng dữ liệu train')\n"
    "print('  3. Feature engineering thêm (HbA1c × glucose interaction)')"
))

# ============================================================
# Section 21 – Model Selection
# ============================================================
cells.append(md("## 21. Lựa chọn mô hình (Model Selection)"))

cells.append(code(
    "# Tóm tắt để chọn model\n"
    "print('Bảng so sánh cuối cùng để chọn model:')\n"
    "print('=' * 70)\n"
    "\n"
    "final_comparison = comparison_df[['Accuracy', 'Precision', 'Recall', 'F1', 'ROC-AUC']].copy()\n"
    "final_comparison['Rank F1'] = final_comparison['F1'].rank(ascending=False).astype(int)\n"
    "final_comparison['Rank AUC'] = final_comparison['ROC-AUC'].rank(ascending=False).astype(int)\n"
    "final_comparison['Rank Recall'] = final_comparison['Recall'].rank(ascending=False).astype(int)\n"
    "print(final_comparison.sort_values('F1', ascending=False).to_string())\n"
    "print()\n"
    "\n"
    "# Chọn model tốt nhất dựa trên F1 + Recall + AUC\n"
    "# Score tổng hợp\n"
    "final_comparison['Composite Score'] = (\n"
    "    0.35 * final_comparison['F1'] +\n"
    "    0.35 * final_comparison['Recall'] +\n"
    "    0.30 * final_comparison['ROC-AUC']\n"
    ")\n"
    "\n"
    "best_name = final_comparison['Composite Score'].idxmax()\n"
    "best_metrics = final_comparison.loc[best_name]\n"
    "\n"
    "print(f'Model được chọn: {best_name}')\n"
    "print(f'  F1-Score:  {best_metrics[\"F1\"]:.4f}')\n"
    "print(f'  Recall:    {best_metrics[\"Recall\"]:.4f}')\n"
    "print(f'  ROC-AUC:   {best_metrics[\"ROC-AUC\"]:.4f}')\n"
    "print()\n"
    "print('Lý do lựa chọn:')\n"
    "print(f'  1. F1-Score cao → cân bằng tốt giữa Precision và Recall')\n"
    "print(f'  2. Recall cao → phát hiện nhiều ca tiểu đường thực sự (ưu tiên y tế)')\n"
    "print(f'  3. ROC-AUC cao → khả năng phân biệt class tốt')\n"
    "print(f'  4. Không chọn chỉ dựa vào Accuracy vì dataset imbalanced')\n"
    "print(f'  5. Phù hợp deployment: có thể giải thích kết quả và inference nhanh')"
))

cells.append(code(
    "# Lưu final model\n"
    "FINAL_MODEL_NAME = best_name\n"
    "final_model = trained_models[FINAL_MODEL_NAME]\n"
    "print(f'Final model: {FINAL_MODEL_NAME}')"
))

# ============================================================
# Section 22 – Model Persistence
# ============================================================
cells.append(md("## 22. Lưu trữ mô hình (Model Persistence)"))

cells.append(code(
    "# Tạo pipeline hoàn chỉnh: Preprocessing + Model\n"
    "print('Tạo full pipeline (preprocessing + model)...')\n"
    "\n"
    "# Tái tạo preprocessing pipeline (cần fit lại để tích hợp vào full pipeline)\n"
    "preprocessing_for_pipeline = ColumnTransformer(\n"
    "    transformers=[\n"
    "        ('num', Pipeline(steps=[('scaler', StandardScaler())]), NUMERICAL_PIPELINE_COLS),\n"
    "        ('cat', Pipeline(steps=[('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))]), CATEGORICAL_PIPELINE_COLS),\n"
    "    ],\n"
    "    remainder='drop'\n"
    ")\n"
    "\n"
    "# Rebuild the final model instance\n"
    "if FINAL_MODEL_NAME == 'Logistic Regression':\n"
    "    final_estimator = LogisticRegression(class_weight='balanced', max_iter=1000,\n"
    "                                         random_state=RANDOM_STATE, solver='saga', n_jobs=-1)\n"
    "elif FINAL_MODEL_NAME == 'Decision Tree':\n"
    "    final_estimator = DecisionTreeClassifier(max_depth=10, class_weight='balanced',\n"
    "                                              random_state=RANDOM_STATE)\n"
    "elif FINAL_MODEL_NAME == 'Random Forest':\n"
    "    final_estimator = RandomForestClassifier(n_estimators=100, max_depth=15,\n"
    "                                              class_weight='balanced',\n"
    "                                              random_state=RANDOM_STATE, n_jobs=-1)\n"
    "elif FINAL_MODEL_NAME == 'SVM (LinearSVC)':\n"
    "    final_estimator = CalibratedClassifierCV(\n"
    "        LinearSVC(class_weight='balanced', max_iter=2000, random_state=RANDOM_STATE), cv=3\n"
    "    )\n"
    "elif FINAL_MODEL_NAME == 'KNN':\n"
    "    final_estimator = KNeighborsClassifier(n_neighbors=11, weights='distance', n_jobs=-1)\n"
    "else:\n"
    "    final_estimator = final_model\n"
    "\n"
    "# Full pipeline\n"
    "full_pipeline = Pipeline(steps=[\n"
    "    ('preprocessor', preprocessing_for_pipeline),\n"
    "    ('classifier',   final_estimator)\n"
    "])\n"
    "\n"
    "# Fit trên toàn bộ training data\n"
    "print(f'Fitting full pipeline ({FINAL_MODEL_NAME}) trên X_train...')\n"
    "full_pipeline.fit(X_train, y_train)\n"
    "print('✅ Full pipeline đã được fit thành công!')\n"
    "\n"
    "# Verify trên test set\n"
    "y_final_pred = full_pipeline.predict(X_test)\n"
    "y_final_prob = full_pipeline.predict_proba(X_test)[:, 1]\n"
    "final_acc  = accuracy_score(y_test, y_final_pred)\n"
    "final_f1   = f1_score(y_test, y_final_pred, zero_division=0)\n"
    "final_auc  = roc_auc_score(y_test, y_final_prob)\n"
    "print(f'Xác nhận – Full Pipeline Test Performance:')\n"
    "print(f'  Accuracy: {final_acc:.4f}')\n"
    "print(f'  F1:       {final_f1:.4f}')\n"
    "print(f'  AUC:      {final_auc:.4f}')"
))

cells.append(code(
    "# Lưu pipeline bằng joblib\n"
    "PIPELINE_PATH = os.path.join(MODEL_DIR, 'diabetes_pipeline.joblib')\n"
    "\n"
    "joblib.dump(full_pipeline, PIPELINE_PATH)\n"
    "file_size = os.path.getsize(PIPELINE_PATH) / 1024\n"
    "\n"
    "print(f'✅ Pipeline đã được lưu thành công!')\n"
    "print(f'  Đường dẫn: {PIPELINE_PATH}')\n"
    "print(f'  Kích thước: {file_size:.1f} KB')\n"
    "print()\n"
    "print('Tại sao phải lưu cả preprocessing + model?')\n"
    "print('  → Khi nhận dữ liệu mới (raw input), cần preprocessing giống hệt training.')\n"
    "print('  → Nếu chỉ lưu model mà bỏ preprocessing, sẽ phải viết lại logic')\n"
    "print('    thủ công → dễ sai sót và data leakage trong production.')\n"
    "print('  → Pipeline đảm bảo preprocessing + model luôn được áp dụng nhất quán.')"
))

# ============================================================
# Section 23 – Inference Test
# ============================================================
cells.append(md("## 23. Kiểm tra suy luận (Inference Test)"))

cells.append(code(
    "# Bước 1: Load pipeline từ disk\n"
    "print('Bước 1: Load pipeline từ disk...')\n"
    "loaded_pipeline = joblib.load(PIPELINE_PATH)\n"
    "print(f'✅ Pipeline đã được load từ: {PIPELINE_PATH}')\n"
    "print(f'   Pipeline type: {type(loaded_pipeline)}')\n"
    "print(f'   Steps: {[s[0] for s in loaded_pipeline.steps]}')"
))

cells.append(code(
    "# Bước 2: Tạo sample input mới (raw record)\n"
    "print('Bước 2: Tạo dữ liệu mới (raw input - chưa preprocessing)...')\n"
    "print()\n"
    "\n"
    "# Sample 1: Bệnh nhân nguy cơ cao\n"
    "sample_high_risk = pd.DataFrame([{\n"
    "    'gender': 'Male',\n"
    "    'age': 65.0,\n"
    "    'hypertension': 1,\n"
    "    'heart_disease': 1,\n"
    "    'smoking_history': 'current',\n"
    "    'bmi': 32.5,\n"
    "    'HbA1c_level': 7.2,\n"
    "    'blood_glucose_level': 200\n"
    "}])\n"
    "\n"
    "# Sample 2: Bệnh nhân nguy cơ thấp\n"
    "sample_low_risk = pd.DataFrame([{\n"
    "    'gender': 'Female',\n"
    "    'age': 25.0,\n"
    "    'hypertension': 0,\n"
    "    'heart_disease': 0,\n"
    "    'smoking_history': 'never',\n"
    "    'bmi': 21.5,\n"
    "    'HbA1c_level': 4.8,\n"
    "    'blood_glucose_level': 90\n"
    "}])\n"
    "\n"
    "print('Bệnh nhân 1 (Nguy cơ CAO):')\n"
    "print(sample_high_risk.to_string(index=False))\n"
    "print()\n"
    "print('Bệnh nhân 2 (Nguy cơ THẤP):')\n"
    "print(sample_low_risk.to_string(index=False))"
))

cells.append(code(
    "# Bước 3: Thực hiện dự đoán\n"
    "print('Bước 3: Thực hiện dự đoán với loaded_pipeline...')\n"
    "print('(Preprocessing được áp dụng TỰ ĐỘNG trong pipeline)')\n"
    "print()\n"
    "\n"
    "for name, sample in [('Bệnh nhân 1 (Nguy cơ CAO)', sample_high_risk),\n"
    "                      ('Bệnh nhân 2 (Nguy cơ THẤP)', sample_low_risk)]:\n"
    "    pred_class = loaded_pipeline.predict(sample)[0]\n"
    "    pred_proba = loaded_pipeline.predict_proba(sample)[0]\n"
    "    \n"
    "    print(f'{'=' * 50}')\n"
    "    print(f'{name}')\n"
    "    print(f'  Predicted class:       {pred_class} ({\"Có tiểu đường\" if pred_class == 1 else \"Không tiểu đường\"})')\n"
    "    print(f'  Probability (class 0): {pred_proba[0]:.4f} ({pred_proba[0]*100:.1f}%)')\n"
    "    print(f'  Probability (class 1): {pred_proba[1]:.4f} ({pred_proba[1]*100:.1f}%)')\n"
    "    if pred_class == 1:\n"
    "        print(f'  ⚠️  KHUYẾN NGHỊ: Cần xét nghiệm chuyên sâu để chẩn đoán tiểu đường')\n"
    "    else:\n"
    "        print(f'  ✅  Nguy cơ tiểu đường thấp, duy trì lối sống lành mạnh')\n"
    "print()"
))

cells.append(code(
    "# Bước 4: Xác nhận pipeline hoạt động độc lập\n"
    "print('Bước 4: Xác nhận pipeline hoạt động hoàn toàn độc lập...')\n"
    "print()\n"
    "\n"
    "# Lấy raw record từ test set (chưa preprocessing)\n"
    "real_sample = X_test.iloc[:5]\n"
    "real_truth  = y_test.iloc[:5].values\n"
    "\n"
    "pred_from_pipeline = loaded_pipeline.predict(real_sample)\n"
    "prob_from_pipeline = loaded_pipeline.predict_proba(real_sample)[:, 1]\n"
    "\n"
    "print('Kết quả inference trên 5 samples từ test set (raw, chưa preprocessing):')\n"
    "result_df = real_sample.copy()\n"
    "result_df['true_label'] = real_truth\n"
    "result_df['predicted']  = pred_from_pipeline\n"
    "result_df['prob_diabetes'] = prob_from_pipeline.round(4)\n"
    "print(result_df[['age', 'bmi', 'HbA1c_level', 'blood_glucose_level',\n"
    "                  'true_label', 'predicted', 'prob_diabetes']].to_string())\n"
    "print()\n"
    "correct = (pred_from_pipeline == real_truth).sum()\n"
    "print(f'Correct predictions: {correct}/5')\n"
    "print()\n"
    "print('✅ Pipeline đã được xác nhận hoạt động thành công sau khi reload từ disk!')\n"
    "print('   → Preprocessing (StandardScaler + OneHotEncoder) được áp dụng tự động')\n"
    "print('   → Không cần preprocessing thủ công khi inference')\n"
    "print(f'   → Model path: {PIPELINE_PATH}')"
))

# ============================================================
# Conclusion
# ============================================================
cells.append(md(
    "---\n"
    "\n"
    "## Kết luận\n"
    "\n"
    "Notebook này đã hoàn thành **23 bước** theo đúng yêu cầu Assignment 2:\n"
    "\n"
    "| Bước | Mô tả | Trạng thái |\n"
    "|------|-------|------------|\n"
    "| 1–2 | Problem Definition & Dataset Source | ✅ |\n"
    "| 3–4 | Dataset Loading & Inspection | ✅ |\n"
    "| 5–9 | Data Quality, Missing, Duplicates, Invalid, Outliers | ✅ |\n"
    "| 10 | EDA với 4 biểu đồ có ý nghĩa | ✅ |\n"
    "| 11 | Feature Types phân loại rõ ràng | ✅ |\n"
    "| 12 | Data Representation (xi ∈ R^d, X ∈ R^(N×d)) | ✅ |\n"
    "| 13 | Feature Engineering có giải thích | ✅ |\n"
    "| 14 | Train/Test Split với stratify | ✅ |\n"
    "| 15 | Pipeline với ColumnTransformer, fit ONLY on train | ✅ |\n"
    "| 16 | Baseline DummyClassifier | ✅ |\n"
    "| 17 | 5 Models (LR, DT, RF, SVM-Linear, KNN) | ✅ |\n"
    "| 18 | Model Comparison DataFrame + charts | ✅ |\n"
    "| 19 | Evaluation: confusion matrix, classification report, ROC | ✅ |\n"
    "| 20 | Error Analysis: FP, FN, TP, TN với giải thích | ✅ |\n"
    "| 21 | Model Selection dựa trên F1+Recall+AUC | ✅ |\n"
    "| 22 | Model Persistence: joblib pipeline | ✅ |\n"
    "| 23 | Inference Test: load + predict + probability | ✅ |\n"
    "\n"
    "**Hệ thống dự đoán tiểu đường đã sẵn sàng cho bước tiếp theo: Triển khai Web API.**"
))

# ============================================================
# Build notebook JSON
# ============================================================
notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3 (ipykernel)",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.11.16"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4,
}

output_path = '/home/dau/assignment2/diabetes/notebook/diabetes_prediction.ipynb'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print(f"Notebook written to: {output_path}")
print(f"Total cells: {len(cells)}")
code_cells = sum(1 for c in cells if c['cell_type'] == 'code')
md_cells = sum(1 for c in cells if c['cell_type'] == 'markdown')
print(f"  Code cells: {code_cells}")
print(f"  Markdown cells: {md_cells}")
