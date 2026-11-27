# DATA VERIFICATION REPORT
## Assignment 2 - Pre-Coding Analysis
**Date:** 2026-09-03
**Status:** ✅ All datasets verified and ready for implementation

---

## DATASET 1: DIABETES PREDICTION

### 📊 Basic Information
- **File:** `diabetes/diabetes_prediction_dataset.csv`
- **Rows:** 100,000
- **Columns:** 9
- **Problem Type:** Binary Classification
- **Target Variable:** `diabetes` (0 = No diabetes, 1 = Has diabetes)

### 📋 Column Details

| Column | Type | Description | Missing | Unique Values |
|--------|------|-------------|---------|---------------|
| gender | Categorical | Patient gender | 0 | 3 (Female: 58,552, Male: 41,430, Other: 18) |
| age | Numerical | Patient age (years) | 0 | 102 (range: 0.08-80.0) |
| hypertension | Binary | Has hypertension (0/1) | 0 | 2 |
| heart_disease | Binary | Has heart disease (0/1) | 0 | 2 |
| smoking_history | Categorical | Smoking status | 0 | 6 (never, No Info, former, current, not current, ever) |
| bmi | Numerical | Body Mass Index | 0 | 4,247 (range: 10.01-95.69, mean: 27.32) |
| HbA1c_level | Numerical | Hemoglobin A1c level | 0 | 18 (range: 3.5-9.0, mean: 5.53) |
| blood_glucose_level | Numerical | Blood glucose level | 0 | 18 (range: 80-300, mean: 138.06) |
| **diabetes** | **Binary (TARGET)** | **Diabetes diagnosis** | **0** | **2** |

### 🎯 Target Distribution
- **Class 0 (No diabetes):** 91,500 samples (91.5%) ⚠️ **IMBALANCED**
- **Class 1 (Has diabetes):** 8,500 samples (8.5%)
- **Implication:** Need stratified split and consider class weights

### ⚠️ Data Quality Issues
1. **Duplicates:** 3,854 duplicate rows (3.85%) - need removal
2. **Class imbalance:** Severe (91.5% vs 8.5%) - stratification required
3. **Age outliers:** Min age 0.08 years (infant) - validate if appropriate

### ✅ Assignment Requirements Match
- ✅ Suitable for classification
- ✅ Clear binary target variable
- ✅ Mix of numerical and categorical features
- ✅ Sufficient samples (100K rows)
- ✅ Can demonstrate categorical encoding (gender, smoking_history)
- ✅ Can demonstrate numerical scaling (age, bmi, glucose, HbA1c)

### 📐 Data Representation Pipeline
```
CSV → DataFrame → Clean Data → Encoded/Scaled Features → X ∈ ℝ^(N×d)

Where:
- N = ~96,146 (after removing duplicates)
- d = 8 features (after encoding gender, smoking_history)
- X ∈ ℝ^(96146×8) for one-hot encoding gender+smoking
- y ∈ {0,1}^N
```

---

## DATASET 2: HOUSE PRICE (VN Housing)

### 📊 Basic Information
- **File:** `house_price/VN_housing_dataset.csv`
- **Rows:** 82,497
- **Columns:** 13 (with 1 index column '﻿')
- **Problem Type:** Regression
- **Target Variable:** `Giá/m2` (Price per m²)
- **Language:** Vietnamese column names

### 📋 Column Details

| Column (Vietnamese) | English Translation | Type | Missing | Description |
|---------------------|---------------------|------|---------|-------------|
| ﻿ | Index | Numerical | 1 (0.00%) | Row ID |
| Ngày | Date | Date | 1 (0.00%) | Listing date |
| Địa chỉ | Address | Text | 48 (0.06%) | Full address |
| Quận | District | Categorical | 2 (0.00%) | District (30 unique) |
| Huyện | Ward | Categorical | 48 (0.06%) | Ward/commune |
| Loại hình nhà ở | House type | Categorical | 32 (0.04%) | 5 types |
| Giấy tờ pháp lý | Legal docs | Categorical | 28,887 (35.02%) | Legal status |
| Số tầng | Number of floors | Numerical | 46,098 (55.88%) | Floors |
| Số phòng ngủ | Bedrooms | Categorical | 39 (0.05%) | Bedroom count |
| Diện tích | Area | Numerical | 2 (0.00%) | Area in m² |
| Dài | Length | Numerical | 62,670 (75.97%) | Length in m |
| Rộng | Width | Numerical | 47,052 (57.03%) | Width in m |
| **Giá/m2** | **Price/m² (TARGET)** | **Numerical** | **13 (0.02%)** | **Price per m²** |

### 🎯 Target Variable: Giá/m2 (Price per m²)
- **Format:** Vietnamese text with commas: "86,96 triệu/m²", "100 triệu/m²"
- **Unit:** Million VND per m²
- **Parsing Required:** 
  - Remove " triệu/m²" suffix
  - Replace comma with dot for decimals
  - Convert to float
- **Sample values:**
  - "86,96 triệu/m²" → 86.96
  - "116,22 triệu/m²" → 116.22
  - "65 triệu/m²" → 65.0

### 🏷️ Categorical Features

**Quận (District) - 30 unique:**
- Top 5: Đống Đa (13,991), Thanh Xuân (12,959), Hoàng Mai (11,165), Hai Bà Trưng (10,578), Hà Đông (7,833)

**Loại hình nhà ở (House type) - 5 types:**
- Nhà ngõ, hẻm (62,537) - Alley house
- Nhà mặt phố, mặt tiền (17,095) - Street-front house
- Nhà phố liền kề (1,881) - Townhouse
- Nhà biệt thự (952) - Villa
- NaN (31)

**Số phòng ngủ (Bedrooms) - 12 categories:**
- Top 3: "4 phòng" (29,069), "3 phòng" (27,162), "5 phòng" (7,924)
- **Format:** Text with "phòng" suffix - need parsing

**Giấy tờ pháp lý (Legal docs) - 4 types:**
- Đã có sổ (52,914) - Has certificate
- Đang chờ sổ (356) - Waiting for certificate
- Giấy tờ khác (340) - Other documents
- Missing: 35.02%

### ⚠️ Data Quality Issues
1. **High missing rates:**
   - Dài (Length): 75.97% missing
   - Rộng (Width): 57.03% missing
   - Số tầng (Floors): 55.88% missing
   - Giấy tờ pháp lý: 35.02% missing
2. **Vietnamese text format:** All columns use Vietnamese
3. **Mixed format features:**
   - "Số phòng ngủ" contains "phòng" suffix
   - "Diện tích" contains "m²" suffix
   - "Giá/m2" needs parsing
4. **Duplicate information:** Dài × Rộng ≈ Diện tích (length × width ≈ area)

### ✅ Assignment Requirements Match
- ✅ Suitable for regression
- ✅ Clear continuous target (price)
- ✅ Mix of numerical and categorical features
- ✅ Sufficient samples (82K rows)
- ✅ Location features (District, Ward) for categorical encoding
- ✅ Numerical features (area, dimensions) for scaling

### 📐 Data Representation Pipeline
```
CSV (Vietnamese) → Parse Text → Clean → Encode → Scale → X ∈ ℝ^(N×d)

Steps:
1. Parse "Giá/m2": "86,96 triệu/m²" → 86.96 (float)
2. Parse "Diện tích": "46 m²" → 46 (float)
3. Parse "Số phòng ngủ": "5 phòng" → 5 (int or encode)
4. Encode categorical: Quận (30), Loại hình (5), Giấy tờ (4)
5. Handle missing values (especially Dài, Rộng, Số tầng)

Result:
- N = 82,484 (after removing 13 rows with missing target)
- d = varies based on encoding strategy (one-hot vs ordinal)
- Example: X ∈ ℝ^(82484×d) where d ≈ 8-40 depending on encoding
- y ∈ ℝ^N (continuous price values)
```

---

## DATASET 3: E-COMMERCE CUSTOMER BEHAVIOR

### 📊 Basic Information
- **File:** `customer_behavior/Womens Clothing E-Commerce Reviews.csv`
- **Rows:** 23,486
- **Columns:** 11
- **Problem Type:** Classification (multiple target options available)
- **Special Feature:** ✅ **Contains TEXT data (Review Text column)**

### 📋 Column Details

| Column | Type | Description | Missing | Unique/Stats |
|--------|------|-------------|---------|--------------|
| (unnamed) | Index | Row ID | 0 | 23,486 |
| Clothing ID | Numerical | Product ID | 0 | Unique products |
| Age | Numerical | Customer age | 0 | Range: 18-99, Mean: 43.2 |
| Title | Text | Review title | 3,810 (16.22%) | 19,676 non-empty |
| **Review Text** | **Text** | **Review content** | **845 (3.60%)** | **22,641 non-empty** ⭐ |
| Rating | Categorical | Rating 1-5 | 0 | 5 classes |
| Recommended IND | Binary | Recommendation | 0 | 2 classes (0/1) |
| Positive Feedback Count | Numerical | Helpful votes | 0 | Range: 0-122, Mean: 2.5 |
| Division Name | Categorical | Product division | 14 (0.06%) | 3 (General, General Petite, Initmates) |
| Department Name | Categorical | Product department | 14 (0.06%) | 6 (Tops, Dresses, Bottoms, Intimate, Jackets, Trend) |
| Class Name | Categorical | Product class | 14 (0.06%) | 20 unique |

### 🎯 Possible Target Variables (Choose ONE)

#### **Option 1: Recommended IND (Binary Classification) - RECOMMENDED**
- **Type:** Binary (0 = Not recommend, 1 = Recommend)
- **Distribution:** 
  - Class 0: 4,172 (17.8%)
  - Class 1: 19,314 (82.2%)
- **Imbalance:** Moderate (82:18 ratio)
- **Business value:** Predict if customer will recommend product

#### **Option 2: Rating (Multi-class Classification)**
- **Type:** Ordinal (1-5 stars)
- **Distribution:**
  - 1 star: 842 (3.6%)
  - 2 stars: 1,565 (6.7%)
  - 3 stars: 2,871 (12.2%)
  - 4 stars: 5,077 (21.6%)
  - 5 stars: 13,131 (55.9%)
- **Imbalance:** Severe skew toward 5 stars

#### Option 3: Department Name (Multi-class)
- **Classes:** 6 departments
- **Distribution:** Tops (10,468), Dresses (6,319), Bottoms (3,799), etc.

#### Option 4: Class Name (Multi-class)
- **Classes:** 20 product classes
- **More granular but more challenging**

### ⭐ TEXT DATA ANALYSIS (CRITICAL)

**Review Text column:**
- **Non-empty:** 22,641 reviews (96.4%)
- **Empty:** 845 (3.6%)
- **Sample reviews:**
  - "Absolutely wonderful - silky and sexy and comfortable"
  - "Love this dress! it's sooo pretty..."
  - "I had such high hopes for this dress..."

**TEXT REPRESENTATION REQUIRED (per Assignment):**
```
Raw Text → Tokenization → Token IDs → Embeddings

Example:
"I like wireless headphones"
  ↓ Tokenize
["I", "like", "wireless", "headphones"]
  ↓ Token IDs
[42, 17, 381, ...]
  ↓ Embedding
E ∈ ℝ^(T×d) where T=tokens, d=embedding_dim
```

### ⚠️ Data Quality Issues
1. **No duplicates:** 0 duplicate rows ✅
2. **Missing Review Text:** 845 rows (3.6%) - drop or impute
3. **Missing Title:** 3,810 rows (16.2%) - less critical
4. **Class imbalance:** Both Recommended IND and Rating are imbalanced

### ✅ Assignment Requirements Match
- ✅ Suitable for classification (multiple target options)
- ✅ **HAS TEXT DATA** - Review Text column (critical requirement)
- ✅ Mix of tabular and text features
- ✅ Can demonstrate text transformation: Comment → Tokens → IDs → Embeddings
- ✅ **Can compare tabular-only vs tabular+text models** (required by assignment)
- ✅ Categorical features for encoding (Department, Division, Class)
- ✅ Numerical features (Age, Positive Feedback Count)

### 📐 Data Representation Pipeline

**Tabular-only representation:**
```
X_tabular = [Age, Clothing_ID, Positive_Feedback_Count, 
             encoded_Division, encoded_Department, encoded_Class]
X_tabular ∈ ℝ^(N×d_tabular)
```

**Text representation:**
```
Review Text → Tokenize → Token IDs → Embeddings

Options:
1. TF-IDF: X_text ∈ ℝ^(N×vocab_size)
2. Count Vectorizer: X_text ∈ ℝ^(N×vocab_size)
3. Word2Vec/GloVe: E ∈ ℝ^(N×d_embed)
4. Sentence embeddings: E ∈ ℝ^(N×d_embed)
```

**Combined representation:**
```
X_combined = [X_tabular | X_text]
X_combined ∈ ℝ^(N×(d_tabular+d_text))
```

**Final shapes (example with TF-IDF, max_features=1000):**
```
N = 22,641 (non-empty reviews)
d_tabular ≈ 10-30 (depending on encoding)
d_text = 1000 (TF-IDF features)
X_combined ∈ ℝ^(22641×1030)
y ∈ {0,1}^N (for Recommended IND target)
```

---

## DATASET vs ASSIGNMENT REQUIREMENTS COMPARISON

### ✅ Requirement Checklist

| Requirement | Diabetes | House Price | Customer Behavior | Status |
|-------------|----------|-------------|-------------------|--------|
| Kaggle dataset | ✅ | ✅ | ✅ | All from Kaggle |
| Clear target | ✅ diabetes (0/1) | ✅ Giá/m2 (price) | ✅ Multiple options | Complete |
| Classification task | ✅ Binary | ❌ Regression | ✅ Binary/Multi | 2/3 ✅ |
| Regression task | ❌ | ✅ Continuous | ❌ | 1/3 ✅ |
| Numerical features | ✅ 6 features | ✅ 4+ features | ✅ 3 features | All ✅ |
| Categorical features | ✅ 2 features | ✅ 5 features | ✅ 4 features | All ✅ |
| Text data (e-commerce only) | N/A | N/A | ✅ Review Text | ✅ |
| Sufficient samples | ✅ 100K | ✅ 82K | ✅ 23K | All ✅ |
| Data quality issues | ⚠️ Duplicates | ⚠️ Missing values | ⚠️ Imbalance | Expected |
| Representation demonstrable | ✅ | ✅ | ✅ | All ✅ |

### 📊 Three Applications Summary

| Aspect | Diabetes | House Price | Customer Behavior |
|--------|----------|-------------|-------------------|
| **Problem type** | Classification | Regression | Classification |
| **Observation** | Patient | House listing | Customer review |
| **Target** | diabetes (binary) | Giá/m2 (continuous) | Recommended IND (binary) |
| **Raw data form** | CSV tabular | CSV tabular (Vietnamese) | CSV + text |
| **Input shape** | ℝ^(N×8) | ℝ^(N×d) | ℝ^(N×d) or ℝ^(N×(d+1000)) |
| **Representation** | Feature vector + matrix | Feature vector + matrix | Feature vector + text embeddings |
| **Best model** | TBD (5 to compare) | TBD (4-5 to compare) | TBD (6 to compare) |
| **Main metric** | Accuracy, F1, ROC-AUC | MAE, RMSE, R² | Accuracy, F1, ROC-AUC |
| **Web deployment** | ✅ Required | ✅ Required | ✅ Required |
| **Mobile deployment** | ✅ Required | ✅ Required | ✅ Required |
| **Special requirement** | Stratification | Parse Vietnamese | Text representation |

---

## RECOMMENDED TARGETS AND FEATURES

### 🎯 Dataset 1: Diabetes Prediction

**Recommended Target:**
```python
target = 'diabetes'  # Binary: 0 or 1
```

**Recommended Features (8 total after encoding):**
```python
numerical_features = [
    'age',                    # Patient age
    'bmi',                    # Body Mass Index
    'HbA1c_level',           # Hemoglobin A1c
    'blood_glucose_level',   # Blood glucose
    'hypertension',          # 0/1
    'heart_disease'          # 0/1
]

categorical_features = [
    'gender',                # Male/Female/Other → one-hot (3 columns)
    'smoking_history'        # 6 categories → one-hot (6 columns)
]

# After encoding:
# X ∈ ℝ^(N×8) if using label encoding
# X ∈ ℝ^(N×15) if using one-hot encoding (6 numerical + 3 gender + 6 smoking)
```

**Data Representation to Show:**
```
1. Raw CSV row (single patient record)
2. Parsed DataFrame row
3. Encoded categorical → numerical
4. Scaled numerical features
5. Final feature vector: x_i ∈ ℝ^d
6. Feature matrix: X ∈ ℝ^(N×d)
7. Target vector: y ∈ {0,1}^N
```

**Models to Compare (5):**
1. Logistic Regression (baseline)
2. Decision Tree Classifier
3. Random Forest Classifier
4. Support Vector Machine (SVM)
5. K-Nearest Neighbors (KNN)

---

### 🎯 Dataset 2: House Price Prediction

**Recommended Target:**
```python
target = 'Giá/m2'  # Continuous (after parsing)
# Parse: "86,96 triệu/m²" → 86.96
```

**Recommended Features:**

**Must parse from Vietnamese:**
```python
# Numerical features (parse and convert)
'Diện tích'   # "46 m²" → 46.0 (Area in m²)
'Số tầng'     # "4" → 4 (Floors) - high missing rate
'Dài'         # "10 m" → 10.0 (Length) - high missing rate
'Rộng'        # "4 m" → 4.0 (Width) - high missing rate

# Categorical features
'Quận'        # District (30 unique) - IMPORTANT
'Loại hình nhà ở'  # House type (5 types)
'Giấy tờ pháp lý'  # Legal status (3 types + missing)
'Số phòng ngủ'     # "4 phòng" → 4 or encode (12 categories)
```

**Feature Engineering Suggestions:**
```python
# Create from existing
'total_area' = parse('Diện tích')
'bedrooms' = parse_bedrooms('Số phòng ngủ')  # "4 phòng" → 4
'has_legal_docs' = ('Giấy tờ pháp lý' == 'Đã có sổ')
'is_street_front' = ('Loại hình nhà ở' == 'Nhà mặt phố, mặt tiền')

# Derived features
'aspect_ratio' = Dài / Rộng (if both available)
'floor_area_ratio' = total_area / bedrooms (if available)
```

**Data Representation to Show:**
```
1. Raw CSV row (Vietnamese text with units)
2. Parsed values (text → numeric)
3. Encoded categorical (Quận, Loại hình, etc.)
4. Scaled numerical features
5. Handle missing values (impute or drop)
6. Final feature vector: x_i = [x_area, x_bedrooms, x_location, ...]^T
7. Feature matrix: X ∈ ℝ^(N×d)
8. Target vector: y ∈ ℝ^N (continuous prices)
```

**Models to Compare (5):**
1. Linear Regression (baseline)
2. Ridge Regression
3. Decision Tree Regressor
4. Random Forest Regressor
5. Gradient Boosting Regressor

---

### 🎯 Dataset 3: E-Commerce Customer Behavior

**Recommended Target (Option 1 - Best balance):**
```python
target = 'Recommended IND'  # Binary: 0 or 1
# 0 = Customer does not recommend product
# 1 = Customer recommends product
# Distribution: 82% positive class
```

**Alternative Target (if want more challenge):**
```python
target = 'Rating'  # Multi-class: 1, 2, 3, 4, 5
# Ordinal classification problem
```

**Tabular Features:**
```python
numerical_features = [
    'Age',                      # Customer age (18-99)
    'Positive Feedback Count',  # Number of helpful votes
    'Clothing ID'               # Product identifier (optional)
]

categorical_features = [
    'Division Name',   # 3 categories
    'Department Name', # 6 categories
    'Class Name'       # 20 categories
]
```

**Text Features (CRITICAL - REQUIRED):**
```python
text_feature = 'Review Text'  # 22,641 non-empty reviews

# Must demonstrate transformation:
# Review Text → Tokens → Token IDs → Embeddings
```

**Data Representation to Show (MANDATORY):**
```
TABULAR TRANSFORMATION:
1. Raw CSV row
2. Numerical features as-is
3. Categorical encoding (one-hot or label)
4. X_tabular ∈ ℝ^(N×d_tabular)

TEXT TRANSFORMATION (MUST SHOW):
1. Raw review: "I like wireless headphones"
2. Tokenization: ["I", "like", "wireless", "headphones"]
3. Token IDs: [42, 17, 381, ...]
4. Option A - TF-IDF: X_text ∈ ℝ^(N×vocab_size)
5. Option B - Embeddings: E ∈ ℝ^(N×d_embed)

Example with TF-IDF:
   "Absolutely wonderful - silky and sexy"
   → Tokenize → ['absolutely', 'wonderful', 'silky', 'sexy']
   → TF-IDF vector → [0, 0.23, 0, ..., 0.45, 0, 0.67, ...]
   → Shape: ℝ^(1×1000) if max_features=1000

COMBINED REPRESENTATION:
X_combined = [X_tabular | X_text]
X_combined ∈ ℝ^(N×(d_tabular+d_text))

Example shape with one-hot encoding:
- Age: 1 feature
- Positive Feedback: 1 feature
- Division (one-hot): 3 features
- Department (one-hot): 6 features
- Class (one-hot): 20 features
- TF-IDF text: 1000 features
TOTAL: X ∈ ℝ^(22641×1031)
```

**Models to Compare (6 - INCLUDING TEXT MODEL):**

**Tabular-only models (3-4):**
1. Logistic Regression (baseline)
2. Decision Tree
3. Random Forest
4. SVM

**Text-based models (1-2):**
5. Logistic Regression with TF-IDF features
6. Another text classifier (Naive Bayes, SVM with text kernel, or simple neural network)

**MUST COMPARE:**
- Tabular-only performance
- Text-only performance
- Combined (tabular + text) performance

---

## CRITICAL PRE-CODING REQUIREMENTS CONFIRMED

### ✅ All Dataset Requirements Met

1. **Three distinct applications:** ✅
   - Diabetes: Classification (health)
   - House Price: Regression (real estate)
   - Customer Behavior: Classification (e-commerce)

2. **Different data types:** ✅
   - Tabular numerical/categorical (all 3)
   - Text data (customer behavior)
   - Vietnamese text requiring parsing (house price)

3. **Text representation capability:** ✅
   - Customer behavior has 22,641 reviews
   - Can demonstrate: Comment → Tokens → IDs → Embeddings
   - Can compare tabular vs tabular+text

4. **Clear targets:** ✅
   - Diabetes: `diabetes` (binary)
   - House Price: `Giá/m2` (continuous, needs parsing)
   - Customer Behavior: `Recommended IND` (binary)

5. **Sufficient samples:** ✅
   - Diabetes: 100K rows
   - House Price: 82K rows
   - Customer Behavior: 23K rows

6. **Data representation demonstrable:** ✅
   - All datasets can show: Raw → Clean → Encode → Scale → Tensor
   - Shapes can be reported: X ∈ ℝ^(N×d), y ∈ ℝ^N

---

## NEXT STEPS (AFTER CONFIRMATION)

### Phase 1: Notebook Development (23 sections each)
1. Create 3 Jupyter notebooks with identical structure
2. Implement all 23 sections per Appendix B
3. Focus on Data Representation section (Section 12)

### Phase 2: Model Training
1. Diabetes: Train 5 classification models
2. House Price: Train 5 regression models
3. Customer Behavior: Train 6 models (including text)

### Phase 3: Pipeline & Persistence
1. Create preprocessing pipelines
2. Save with joblib: preprocessor.joblib, model.joblib
3. Test inference with saved pipeline

### Phase 4: Deployment
1. Web: FastAPI with 3 endpoints
2. Mobile: Flutter/React Native calling APIs
3. Screenshots and documentation

### Phase 5: Report
1. 10-page technical report
2. Comparison of 3 applications
3. Data representation emphasis

---

## RECOMMENDED PREPROCESSING STRATEGIES

### Diabetes:
```python
# 1. Remove duplicates (3,854 rows)
# 2. Encode: gender (one-hot), smoking_history (one-hot or ordinal)
# 3. Scale: age, bmi, HbA1c_level, blood_glucose_level (StandardScaler)
# 4. Stratified train/test split (class imbalance)
# 5. Consider SMOTE or class weights for imbalance
```

### House Price:
```python
# 1. Parse Vietnamese text:
#    - "86,96 triệu/m²" → 86.96
#    - "46 m²" → 46.0
#    - "4 phòng" → 4
# 2. Handle missing values:
#    - Số tầng, Dài, Rộng: 55-76% missing → impute or drop
#    - Giấy tờ pháp lý: 35% missing → "Unknown" category
# 3. Encode categorical: Quận (30), Loại hình (5), etc.
# 4. Scale numerical features
# 5. Feature engineering: ratios, area calculations
```

### Customer Behavior:
```python
# 1. Drop 845 rows with missing Review Text (3.6%)
# 2. Tabular preprocessing:
#    - Encode: Division, Department, Class (one-hot or target encoding)
#    - Scale: Age, Positive Feedback Count
# 3. Text preprocessing:
#    - Lowercase, remove punctuation, tokenize
#    - TF-IDF vectorizer (max_features=1000)
#    - OR Word embeddings (Word2Vec, GloVe)
# 4. Create two feature sets:
#    - X_tabular only
#    - X_combined (tabular + text)
# 5. Compare model performance with and without text
```

---

## DATA LEAKAGE PREVENTION PLAN

### Critical: Same Preprocessing for Train and Inference

**DO:**
- ✅ Fit scalers/encoders ONLY on training data
- ✅ Transform validation/test using fitted objects
- ✅ Save fitted preprocessing objects with joblib
- ✅ Load same preprocessing for inference

**DON'T:**
- ❌ Fit any preprocessing on test data
- ❌ Fit any preprocessing on validation data
- ❌ Fit any preprocessing on user input during inference
- ❌ Use different encoding during training vs inference

**Example (correct approach):**
```python
# Training
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', RandomForestClassifier())
])

# Fit ONLY on training data
pipeline.fit(X_train, y_train)

# Save entire pipeline
joblib.dump(pipeline, 'model_pipeline.joblib')

# Inference
loaded_pipeline = joblib.load('model_pipeline.joblib')
prediction = loaded_pipeline.predict(new_data)  # Uses same scaler fitted on train
```

---

## STATUS: ✅ READY FOR IMPLEMENTATION

All datasets verified. All requirements confirmed. No blocking issues.

**Waiting for user confirmation to proceed with coding.**
