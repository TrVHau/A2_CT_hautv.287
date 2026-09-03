# BÁO CÁO MÔN HỌC: PHÁT TRIỂN CÁC HỆ THỐNG THÔNG MINH
## Assignment 02 – End-to-End Machine Learning Systems

> **Học viện Công nghệ Bưu chính Viễn thông – Khoa Công nghệ Thông tin 1**  
> **Họ và tên sinh viên**: Trần Văn Hậu  
> **Mã sinh viên**: B23DCCN287  
> **Lớp học phần**: D23CQCN01-B  
> **Giảng viên hướng dẫn**: PGS. TS. Trần Đình Quế  
> **GitHub Repository**: [https://github.com/TrVHau/A2_CT_hautv.287](https://github.com/TrVHau/A2_CT_hautv.287)  

---

ASSIGNMENT 02

From Data Representation to Deployable Intelligent Systems



| Họ tên: | Trần Văn Hậu |  |
| --- | --- | --- |
| Mã sinh viên: | B23DCCN287 |
| Lớp: | D23CQCN01-B |
| Giảng viên | PGS. TS. Trần Đình Quế |


Hà Nội – 2026


# 1. Tổng quan & Cơ sở Lý thuyết Phát triển Hệ thống Thông minh


## 1.1. Bản chất Toán học của Biểu diễn Dữ liệu (Data Representation Theory)

Trong lý thuyết Học máy hiện đại (Machine Learning Theory, Lecture 02), một hệ thống thông minh không bao giờ tương tác trực tiếp với các thực thể thô trong thế giới thực (như hồ sơ bệnh án, tin rao bán bất động sản hay các câu văn nhận xét của người dùng). Thay vào đó, toàn bộ thực thể được ánh xạ vào một không gian vector Euclid đa chiều thông qua toán tử biểu diễn dữ liệu phi tuyến:

$$\phi: \mathcal{X} \longrightarrow \mathbb{R}^d, \quad \mathbf{x} = \phi(\text{raw\_instance}) = [x_1, x_2, \dots, x_d]^T \in \mathbb{R}^d$$

Tập dữ liệu huấn luyện kích thước N quan sát trở thành một ma trận đặc trưng $\mathbf{X} \in \mathbb{R}^{N \times d}$ cùng vector nhãn giám sát $\mathbf{y} \in \mathcal{Y}^N$. Nhiệm vụ của giải thuật học máy là tối ưu hóa hàm giả thuyết $f_\theta: \mathbb{R}^d \rightarrow \mathcal{Y}$ nhằm cực tiểu hóa hàm mất mát kỳ vọng (Expected Risk Minimization):

$$\min_{\theta} \mathcal{R}_{\text{emp}}(\theta) = \frac{1}{N} \sum_{i=1}^N \mathcal{L}(f_\theta(\mathbf{x}_i), y_i) + \Omega(\theta)$$

Trong đó $\mathcal{L}(\cdot, \cdot)$ là hàm tổn thất phản ánh sai số dự đoán và $\Omega(\theta)$ là số hạng điều chuẩn (Regularization) nhằm kiểm soát độ phức tạp mô hình, ngăn chặn hiện tượng quá khớp (Overfitting).


## 1.2. Lý thuyết Tiền xử lý, Chuẩn hóa & Không gian Đặc trưng

Tùy thuộc vào bản chất vật lý của từng miền dữ liệu, các kỹ thuật biến đổi toán học tương ứng được áp dụng:

• 1. Chuẩn hóa Z-Score: Z-Score Standard Scaling: Chuyển đổi đặc trưng số có phân phối chuẩn về kỳ vọng 0 và phương sai 1: $z = \frac{x - \mu}{\sigma}$. Áp dụng cho dữ liệu y tế không chứa ngoại lệ cực đoan.

• 2. Robust Scaling: Robust Scaling qua Khoảng Tứ phân vị (IQR): Biến đổi dựa trên trung vị (Median) và khoảng biến thiên $IQR = Q_3 - Q_1$: $x_{\text{robust}} = \frac{x - Q_2}{IQR}$. Giúp bảo vệ mô hình hồi quy giá nhà trước các tin đăng ngoại lệ do sốt đất hoặc bất động sản siêu sang.

• 3. Mã hóa One-Hot: One-Hot Encoding (OHE): Ánh xạ biến định danh $C$ trạng thái thành vector nhị phân $\mathbf{e} \in \{0, 1\}^C$. Giúp loại bỏ giả định thứ tự nhân tạo của Label Encoding.

• 4. Vector hóa Văn bản: TF-IDF Vectorization: Biểu diễn văn bản tự nhiên qua tần suất từ (Term Frequency) và nghịch đảo tần suất văn bản (Inverse Document Frequency):

$$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \left( \log\frac{1 + |D|}{1 + |\{d' \in D : t \in d'\}|} + 1 \right)$$


## 1.3. Lý thuyết Đánh giá & Định lý Phòng chống Rò rỉ Dữ liệu (Anti-Leakage Theorem)

Đối với bài toán phân loại mất cân bằng nhãn (Imbalanced Classification), chỉ số Accuracy thông thường dẫn đến 'Nghịch lý độ chính xác' (Accuracy Paradox). Báo cáo ưu tiên các chỉ số chuyên sâu:

• • Precision: Precision: $P = \frac{TP}{TP + FP}$ — Tỷ lệ dự đoán dương tính thực sự chính xác.

• • Recall: Recall (Sensitivity): $R = \frac{TP}{TP + FN}$ — Năng lực phát hiện toàn bộ các ca bệnh/ca tích cực thực tế trong quần thể.

• • F1-Score: F1-Score: $F_1 = 2 \frac{P \times R}{P + R}$ — Trung bình điều hòa cân bằng giữa Precision và Recall.

• • ROC-AUC: ROC-AUC: Diện tích dưới đường cong ROC biểu thị xác suất mô hình xếp hạng một mẫu dương ngẫu nhiên cao hơn một mẫu âm ngẫu nhiên.

Định lý Chống rò rỉ dữ liệu: Nguyên tắc Chống rò rỉ dữ liệu (Data Leakage Prevention): Toàn bộ các phép biến đổi (tính toán $\mu, \sigma, Q_1, Q_3$, xây dựng từ điển TF-IDF, bộ mã hóa OHE) bắt buộc phải được `fit` duy nhất trên tập huấn luyện $X_{\text{train}}$. Tập kiểm thử $X_{\text{test}}$ và dữ liệu thực tế tại API chỉ được phép thực hiện `transform` dựa trên các tham số đã đóng băng.



| Hệ thống thông minh | Bản chất bài toán | Biểu diễn số học x_i | Mô hình tối ưu lựa chọn | Hiệu năng kiểm thử chính | FastAPI Endpoint |
| --- | --- | --- | --- | --- | --- |
| 1. Diabetes Screening | Phân loại nhị phân (Binary) | x ∈ R^15 (Z-Score + OHE) | Random Forest Classifier | Accuracy: 91.74%ROC-AUC: 0.9738 | POST /predictGET /health |
| 2. House Price Valuation | Hồi quy liên tục (Regression) | x ∈ R^55 (RobustScaler + OHE) | Random Forest Regressor | MAE: 23.34 tr/m²R²: 0.3729 | POST /predictGET /health |
| 3. Customer Recommendation | Phân loại đa phương thức (Multimodal) | x ∈ R^1,038 (TF-IDF + Tabular) | Logistic Regression (Balanced) | Accuracy: 93.33%ROC-AUC: 0.9772 | POST /predictGET /health |



# 2. Ứng dụng 1: Hệ thống Sàng lọc & Dự đoán Nguy cơ Tiểu đường (Diabetes Prediction)

Link GitHub Notebook: https://github.com/TrVHau/A2_CT_hautv.287/blob/main/diabetes/notebook/diabetes_prediction.ipynb

Link Kaggle Dataset: https://www.kaggle.com/datasets/iammustafatz/diabetes-prediction-dataset


## 2.1. Phân tích Dữ liệu Nguồn & Kiểm định Chất lượng Lâm sàng (EDA)

Bộ dữ liệu Diabetes Prediction Dataset thu thập 100,000 bản ghi bệnh nhân thực tế. Qua quy trình kiểm định chất lượng nghiêm ngặt:

• 1. Deduplication: Kiểm tra trùng lặp: Phát hiện và loại bỏ 3,552 bản ghi trùng lặp hoàn toàn, giữ lại 96,448 quan sát độc lập.

• 2. Physiological Range: Kiểm định khuyết thiếu & dải sinh lý: Xác nhận 0 giá trị thiếu. Dải giá trị hoàn toàn hợp lệ về mặt y sinh học: Glucose từ 80 - 300 mg/dL, HbA1c từ 3.5 - 9.0%, BMI từ 10.0 - 80.0 kg/m².

• 3. Class Imbalance: Phân phối nhãn mục tiêu: Nhãn 0 (Không tiểu đường) chiếm 91.5% (88,290 ca), nhãn 1 (Tiểu đường) chiếm 8.5% (8,158 ca), tạo ra sự mất cân bằng lớp lớn đòi hỏi kỹ thuật điều chỉnh trọng số huấn luyện.



| Thuộc tính | Kiểu dữ liệu | Miền giá trị | Vai trò lâm sàng & Phương pháp xử lý |
| --- | --- | --- | --- |
| age | Số thực (float) | 0.08 – 80.0 tuổi | Tuổi bệnh nhân; Chuẩn hóa StandardScaler |
| bmi | Số thực (float) | 10.01 – 80.0 kg/m² | Chỉ số khối cơ thể Body Mass Index; StandardScaler |
| HbA1c_level | Số thực (float) | 3.5 – 9.0 % | Tỷ lệ đường huyết gắn Hemoglobin (chỉ số vàng); StandardScaler |
| blood_glucose_level | Số nguyên (int) | 80 – 300 mg/dL | Đường huyết ngẫu nhiên trong huyết tương; StandardScaler |
| hypertension | Nhị phân (int) | 0 hoặc 1 | Tiền sử tăng huyết áp (0: Bình thường, 1: Bệnh lý); StandardScaler |
| heart_disease | Nhị phân (int) | 0 hoặc 1 | Tiền sử bệnh tim mạch; StandardScaler |
| gender | Định danh (str) | Female, Male, Other | Giới tính; Mã hóa OneHotEncoder |
| smoking_history | Định danh (str) | never, current, former, ... | Thói quen hút thuốc; Mã hóa OneHotEncoder |
| diabetes | Nhị phân (int) | 0 hoặc 1 | Biến mục tiêu giám sát (0: Âm tính, 1: Dương tính) |



*Hình: Phân phối biến mục tiêu diabetes và tỷ lệ mất cân bằng dữ liệu*


> **📊 Phân tích ý nghĩa biểu đồ: Biểu đồ phân phối nhãn thể hiện rõ độ lệch mất cân bằng (8.5% ca bệnh). Điều này chứng minh rằng việc đánh giá mô hình chỉ dựa trên Accuracy sẽ dẫn đến sai lầm nguy hiểm, cần kết hợp trọng số class_weight='balanced' và đánh giá ưu tiên chỉ số Recall.**


*Hình: Biểu đồ Violin Plot phân tích hình dáng phân phối và mật độ của Age, BMI, Blood Glucose theo nhãn bệnh*


> **📊 Phân tích ý nghĩa biểu đồ: Phân tích Violin Plot cho thấy nhóm bệnh nhân tiểu đường (diabetes=1) có trung vị và mật độ tập trung của HbA1c và Blood Glucose cao vượt trội so với nhóm bình thường, khẳng định đây là 2 biến phân tách mạnh mẽ nhất.**


*Hình: Ma trận tương quan Pearson giữa các chỉ số lâm sàng với biến mục tiêu diabetes*


> **📊 Phân tích ý nghĩa biểu đồ: Ma trận tương quan định lượng hóa mức độ liên kết tuyến tính: HbA1c_level (r=0.40) và blood_glucose_level (r=0.42) có tương quan dương mạnh nhất với khả năng mắc bệnh tiểu đường.**


## 2.2. Biểu diễn Không gian Đặc trưng & Pipeline Tiền xử lý Scikit-Learn

Mỗi bệnh nhân i được biểu diễn bởi một vector đặc trưng có số chiều $d = 15$ trong không gian Euclid:

$$\mathbf{x}_i = [z(\text{age}), z(\text{bmi}), z(\text{HbA1c}), z(\text{glucose}), z(\text{hyper}), z(\text{heart}), \mathbf{e}_{\text{gender}}, \mathbf{e}_{\text{smoke}}]^T \in \mathbb{R}^{15}$$

Dữ liệu được phân chia ngẫu nhiên có bảo toàn tỷ lệ lớp (Stratified 80/20 Train-Test Split), tạo ra tập huấn luyện $X_{\text{train}} \in \mathbb{R}^{77,158 \times 15}$ và tập kiểm định độc lập $X_{\text{test}} \in \mathbb{R}^{19,290 \times 15}$. Toàn bộ tham số thống kê chỉ được học trên $X_{\text{train}}$.


#### 💻 Xây dựng ColumnTransformer Preprocessing Pipeline cho Diabetes

```python
# Pipeline tiền xử lý và Vector hóa đặc trưng Diabetes
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
 
num_features = ['age', 'bmi', 'HbA1c_level', 'blood_glucose_level', 'hypertension', 'heart_disease']
cat_features = ['gender', 'smoking_history']
 
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), num_features),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_features)
    ]
)
 
# Đóng gói Pipeline hoàn chỉnh chống Data Leakage
diabetes_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, max_depth=12, 
                                          class_weight='balanced', random_state=42, n_jobs=-1))
])
```


> **🔍 Phân tích mã nguồn: Khối mã nguồn sử dụng ColumnTransformer để áp dụng đồng thời StandardScaler lên 6 biến định lượng và OneHotEncoder lên 2 biến phân loại. Pipeline đóng gói toàn bộ quy trình từ dữ liệu thô DataFrame đến mô hình Random Forest với class_weight='balanced' nhằm phạt nặng lỗi bỏ sót ca bệnh.**


## 2.3. Thực nghiệm, Đánh giá So sánh & Lựa chọn Mô hình

Nhóm đã tiến hành thử nghiệm đối chiếu 6 thuật toán học máy phổ biến trên cùng tập kiểm thử độc lập $X_{\text{test}}$ (19,290 mẫu):



| Thuật toán (Mô hình) | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| --- | --- | --- | --- | --- | --- |
| Random Forest (Selected) | 0.9174 | 0.5189 | 0.8679 | 0.6495 | 0.9738 |
| Decision Tree (Tối ưu độ sâu) | 0.8806 | 0.4189 | 0.9151 | 0.5747 | 0.9704 |
| SVM (LinearSVC Calibrated) | 0.9588 | 0.8604 | 0.6362 | 0.7315 | 0.9600 |
| K-Nearest Neighbors (K=11) | 0.9602 | 0.9167 | 0.6032 | 0.7276 | 0.9294 |
| Logistic Regression | 0.8846 | 0.4253 | 0.8797 | 0.5734 | 0.9601 |
| Dummy Classifier (Baseline) | 0.9150 | 0.0000 | 0.0000 | 0.0000 | 0.5000 |



*Hình: So sánh hiệu năng 6 mô hình phân loại Tiểu đường trên tập Test*


> **📊 Phân tích ý nghĩa biểu đồ: Biểu đồ so sánh trực quan cho thấy Random Forest đạt sự cân bằng tối ưu giữa Recall (0.8679), F1-score (0.6495) và ROC-AUC (0.9738), vượt trội hoàn toàn so với mô hình cơ sở Dummy Baseline.**


*Hình: Đường cong Precision-Recall Tradeoff và các đường đồng mức iso-F1 curves*


> **📊 Phân tích ý nghĩa biểu đồ: Biểu đồ PR Curve minh họa rõ sự đánh đổi giữa Precision và Recall. Random Forest duy trì diện tích dưới đường cong PR cao nhất, cho phép linh hoạt điều chỉnh ngưỡng quyết định phù hợp với yêu cầu thực tế y khoa.**


*Hình: Ma trận nhầm lẫn (Confusion Matrix) của mô hình Random Forest trên 19,290 mẫu kiểm thử*


> **📊 Phân tích ý nghĩa biểu đồ: Ma trận nhầm lẫn cho thấy mô hình phát hiện chính xác 1,417 / 1,632 ca mắc bệnh thực tế (đạt tỷ lệ Recall 86.8%), hạn chế tối đa nguy cơ bỏ sót bệnh nhân trong quá trình sàng lọc lâm sàng.**


*Hình: Đường cong ROC và chỉ số AUC của mô hình Random Forest Classifier*


> **📊 Phân tích ý nghĩa biểu đồ: Đường cong ROC tiến sát góc trên bên trái với ROC-AUC = 0.9738, chứng minh khả năng phân biệt xuất sắc giữa bệnh nhân nguy cơ cao và người bình thường.**

Kết luận lựa chọn mô hình: Quyết định lựa chọn: Random Forest Classifier được chọn làm mô hình chính thức nhờ đạt chỉ số tổng hợp Composite Score cao nhất (0.8193), khả năng bao quát ca bệnh Recall = 86.79%, ROC-AUC xuất sắc đạt 0.9738. Toàn bộ pipeline được lưu trữ thành file nhị phân `diabetes_pipeline.joblib` (dung lượng 18.3 MB).


## 2.4. Triển khai REST API Backend & Giao diện Ứng dụng Web/Mobile


#### 💻 Triển khai REST API dự đoán nguy cơ Tiểu đường với FastAPI

```python
# Trích đoạn Backend FastAPI triển khai Diabetes Prediction
from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib, pandas as pd
 
app = FastAPI(title="Diabetes Risk Prediction API")
pipeline = joblib.load("models/diabetes_pipeline.joblib")
 
class PatientInput(BaseModel):
    gender: str = Field(..., example="Male")
    age: float = Field(..., ge=0, le=120)
    hypertension: int = Field(..., ge=0, le=1)
    heart_disease: int = Field(..., ge=0, le=1)
    smoking_history: str = Field(..., example="former")
    bmi: float = Field(..., ge=10.0, le=80.0)
    HbA1c_level: float = Field(..., ge=3.0, le=15.0)
    blood_glucose_level: int = Field(..., ge=50, le=500)
 
@app.post("/predict")
def predict_diabetes_risk(data: PatientInput):
    df_in = pd.DataFrame([data.dict()])
    prob = pipeline.predict_proba(df_in)[0]
    pred_label = int(prob[1] >= 0.40) # Ngưỡng tối ưu Recall
    return {
        "prediction": pred_label,
        "risk_level": "Nguy cơ cao" if pred_label == 1 else "Nguy cơ thấp",
        "probability_diabetic": float(prob[1]),
        "probability_healthy": float(prob[0])
    }
```


> **🔍 Phân tích mã nguồn: API sử dụng Pydantic để tự động xác thực miền giá trị đầu vào (validation). Khi nhận HTTP POST request, dữ liệu được chuyển đổi thành DataFrame 1 dòng và đưa trực tiếp vào pipeline.predict_proba() để tính toán xác suất thời gian thực với độ trễ dưới 2ms.**


*Hình: Giao diện Web Client: Form nhập liệu 8 chỉ số lâm sàng (Chụp thực tế từ App đang chạy)*


*Hình: Giao diện Web Client: Hiển thị kết quả đánh giá nguy cơ và phân phối xác suất thời gian thực*


*Hình: Giao diện Mobile Client: Nhập liệu trên điện thoại di động (Chụp thực tế)*


*Hình: Giao diện Mobile Client: Thẻ kết quả rủi ro trên điện thoại di động*


# 3. Ứng dụng 2: Hệ thống Định giá Bất động sản Nhà ở Hà Nội (House Price Prediction)

Link GitHub Notebook: https://github.com/TrVHau/A2_CT_hautv.287/blob/main/house_price/notebook/house_price_prediction.ipynb

Link Kaggle Dataset: https://www.kaggle.com/datasets/ladcva/vietnam-housing-dataset-hanoi/data


## 3.1. Phân tích Dữ liệu Bất động sản & Làm sạch Ngoại lệ (EDA)

Bộ dữ liệu Vietnam Housing Dataset Hanoi gồm 82,497 tin đăng giao dịch thực tế. Quá trình làm sạch dữ liệu bao gồm: chuyển đổi dữ liệu chuỗi sang định dạng số liên tục, loại bỏ các bản ghi không có thông tin diện tích hoặc đơn giá, áp dụng phân vị IQR để lọc các giá trị ngoại lệ phi lý (giữ diện tích từ 10 - 1,000 m², đơn giá từ 5 - 500 triệu/m²). Kỹ thuật trích xuất đặc trưng hình học (Feature Engineering) đã tạo thêm các biến: Tỷ lệ dài/rộng (Aspect_Ratio), Diện tích tính toán (Calculated_Area), cờ có kích thước (Has_Dimensions) và cờ pháp lý (Has_Legal_Docs).



| Nhóm đặc trưng | Các biến thành phần | Xử lý trong Pipeline toán học |
| --- | --- | --- |
| Đặc trưng hình học & kích thước | Area, Length, Width, Aspect_Ratio, Calculated_Area | Xử lý khuyết thiếu Median Imputer + Chuẩn hóa RobustScaler |
| Chỉ báo nhị phân (Binary Flags) | Has_Dimensions, Has_Legal_Docs | Chuẩn hóa RobustScaler |
| Đặc trưng phân loại (Categorical) | Quận, Loại hình nhà ở, Giấy tờ pháp lý, Bedrooms_Category | Mode Imputer + Mã hóa đa chiều OneHotEncoder |
| Biến mục tiêu (Target) | Price_per_m2 (triệu VNĐ/m²), Total_Price (tỷ VNĐ) | Hồi quy giá trị thực liên tục y ∈ R+ |



*Hình: Phân phối đơn giá (triệu/m²) và tương quan giữa Diện tích với Tổng giá trị BĐS tại Hà Nội*


> **📊 Phân tích ý nghĩa biểu đồ: Biểu đồ phân phối đơn giá thể hiện phân phối lệch phải đặc trưng của thị trường bất động sản. Biểu đồ tán xạ chỉ ra mối tương quan phi tuyến giữa diện tích và tổng giá nhà, khẳng định sự cần thiết của các mô hình phi tuyến tính như Random Forest.**


## 3.2. Biểu diễn Không gian Đặc trưng & Đóng gói Pipeline Hồi quy

Sau khi áp dụng One-Hot Encoding cho 30 đơn vị hành chính cấp Quận/Huyện, 4 loại hình nhà ở, các trạng thái pháp lý và nhóm phòng ngủ, mỗi căn nhà được ánh xạ thành một vector đặc trưng có số chiều $d = 55$:

$$\mathbf{x}_i \in \mathbb{R}^{55}, \quad \hat{y}_i = f(\mathbf{x}_i; \mathbf{w}) \in \mathbb{R}$$

Dữ liệu được phân chia thành tập huấn luyện (64,024 mẫu) và tập kiểm thử (16,007 mẫu). Pipeline hồi quy sử dụng `RobustScaler` thay vì `StandardScaler` nhằm loại bỏ ảnh hưởng của các mức giá bất thường.


#### 💻 Kiến trúc Pipeline Hồi quy Định giá BĐS Hà Nội

```python
# Pipeline tiền xử lý và Huấn luyện mô hình Hồi quy Giá nhà
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import RobustScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
 
num_cols = ['Area', 'Length', 'Width', 'Aspect_Ratio', 'Calculated_Area', 'Has_Dimensions', 'Has_Legal_Docs']
cat_cols = ['Quận', 'Loại hình nhà ở', 'Giấy tờ pháp lý', 'Bedrooms_Category']
 
num_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', RobustScaler())
])
 
cat_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])
 
preprocessor = ColumnTransformer(transformers=[
    ('num', num_pipeline, num_cols),
    ('cat', cat_pipeline, cat_cols)
])
 
# Pipeline hoàn chỉnh Random Forest Regressor
hp_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, max_depth=20, 
                                        min_samples_split=10, random_state=42, n_jobs=-1))
])
```


> **🔍 Phân tích mã nguồn: Đoạn mã xây dựng hai nhánh pipeline tiền xử lý riêng biệt: nhánh số sử dụng Median Imputer kết hợp RobustScaler để chống ngoại lệ; nhánh phân loại sử dụng Mode Imputer kết hợp OneHotEncoder. Toàn bộ chuỗi được nối với Random Forest Regressor có max_depth=20 nhằm khống chế Overfitting.**


## 3.3. Kết quả Thực nghiệm & Đánh giá Hiệu năng Hồi quy



| Thuật toán Hồi quy | MAE (triệu/m²) | MSE | RMSE (triệu/m²) | R² Score | Thời gian (s) |
| --- | --- | --- | --- | --- | --- |
| Random Forest Regressor (Selected) | 23.34 | 1221.15 | 34.95 | 0.3729 | 3.42s |
| Gradient Boosting Regressor | 25.12 | 1354.24 | 36.80 | 0.3410 | 5.18s |
| Decision Tree Regressor | 26.85 | 1560.25 | 39.50 | 0.2850 | 0.45s |
| Ridge Regression (alpha=10.0) | 29.40 | 1772.41 | 42.10 | 0.2150 | 0.08s |
| Linear Regression (OLS) | 29.42 | 1774.09 | 42.12 | 0.2148 | 0.09s |
| Baseline Predictor (Mean) | 36.80 | 2450.25 | 49.50 | 0.0000 | 0.01s |



*Hình: So sánh sai số MAE, RMSE và hệ số R² giữa các mô hình hồi quy Giá nhà Hà Nội*


> **📊 Phân tích ý nghĩa biểu đồ: Biểu đồ so sánh 3 tiêu chí hồi quy khẳng định Random Forest Regressor vượt trội toàn diện với MAE thấp nhất (23.34 triệu/m²) và R² cao nhất (0.3729), giảm thiểu sai số dự đoán 36.6% so với mô hình Mean Baseline.**


## 3.4. Triển khai REST API & Giao diện Định giá Web/Mobile


*Hình: Giao diện Web: Form nhập đặc trưng căn nhà (Diện tích 85.5 m², Cầu Giấy, Sổ đỏ)*


*Hình: Giao diện Web: Card hiển thị đơn giá định giá (91.25 tr/m²) và tổng giá trị (5.47 tỷ VNĐ)*


*Hình: Giao diện Mobile: Form định giá trên ứng dụng di động*


*Hình: Giao diện Mobile: Kết quả định giá bất động sản trên di động*


# 4. Ứng dụng 3: Hệ thống Phân loại Khuyến nghị Đa phương thức (Customer Behavior)

Link GitHub Notebook: https://github.com/TrVHau/A2_CT_hautv.287/blob/main/customer_behavior/notebook/customer_behavior.ipynb

Link Kaggle Dataset: https://www.kaggle.com/datasets/nicapotato/womens-ecommerce-clothing-reviews


## 4.1. Định nghĩa bài toán & Hướng tiếp cận Multimodal Fusion

Mục tiêu bài toán là dự đoán hành vi khách hàng có sẵn sàng khuyến nghị sản phẩm thời trang cho người khác hay không (biến mục tiêu `Recommended IND` ∈ {0, 1}).

Kiến trúc Kết hợp đa phương thức (Multimodal Feature Fusion) được thiết kế đồng bộ:

• 1. Tabular Modality: Nhánh Tabular: Khai thác 8 đặc trưng cấu trúc gồm Age, Rating, Positive Feedback Count, Review Length, Word Count, Has Title và phân cấp ngành hàng qua StandardScaler và OneHotEncoder (d_tab = 38 chiều).

• 2. Text Modality: Nhánh Text: Ghép nối Title + Review Text, tiền xử lý và trích xuất TF-IDF unigram + bigram (d_text = 1,000 chiều).



| Nhánh phương thức | Đặc trưng đầu vào | Phương pháp Vector hóa | Số chiều d |
| --- | --- | --- | --- |
| Tabular - Số liên tục | Age, Rating, Positive Feedback, review_length, word_count | StandardScaler | 5 chiều |
| Tabular - Cờ nhị phân | has_title (Có tiêu đề hay không) | Passthrough (Binary) | 1 chiều |
| Tabular - Phân loại | Division Name, Department Name, Class Name | OneHotEncoder(handle_unknown='ignore') | 32 chiều |
| Text - Ngôn ngữ tự nhiên | full_text = Title + ' ' + Review Text | TfidfVectorizer(1000, ngram=(1,2), stop_words) | 1,000 chiều |
| Multimodal Concatenation | Toàn bộ thông tin thực thể khách hàng & bài đánh giá | Hợp nhất không gian vector (ColumnTransformer) | 1,038 chiều |



*Hình: Phân phối nhãn Recommended IND trên 23,486 đánh giá thương mại điện tử*


> **📊 Phân tích ý nghĩa biểu đồ: Biểu đồ phân phối cho thấy 82.2% khách hàng khuyến nghị sản phẩm và 17.8% không khuyến nghị, tạo ra sự thiên lệch đòi hỏi điều chỉnh class_weight='balanced' trong mô hình phân loại.**


*Hình: Phân phối độ dài ký tự và số lượng từ trong bài đánh giá theo nhãn khuyến nghị*


> **📊 Phân tích ý nghĩa biểu đồ: Phân tích mật độ KDE cho thấy các bài nhận xét không khuyến nghị thường có xu hướng dài hơn và sử dụng nhiều từ ngữ miêu tả chi tiết các điểm lỗi của sản phẩm.**


## 4.2. Pipeline Hợp nhất Đa phương thức & Mô hình Huấn luyện

Tổng không gian vector đặc trưng sau khi hợp nhất đạt $d = 1,038$ chiều: $\mathbf{x}_i = [\mathbf{x}_{\text{tab}}, \mathbf{x}_{\text{text}}]^T \in \mathbb{R}^{1038}$. Toàn bộ tiền xử lý được tích hợp trong một ColumnTransformer duy nhất:


#### 💻 Xây dựng Multimodal Feature Fusion Pipeline trong Scikit-Learn

```python
# Kiến trúc Multimodal Fusion Pipeline cho Customer Behavior
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
 
# 1. Định nghĩa các nhánh xử lý
tabular_num_cols = ['Age', 'Rating', 'Positive Feedback Count', 'review_length', 'word_count', 'has_title']
tabular_cat_cols = ['Division Name', 'Department Name', 'Class Name']
text_col = 'full_text'
 
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), tabular_num_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=True), tabular_cat_cols),
        ('text', TfidfVectorizer(max_features=1000, ngram_range=(1,2), stop_words='english'), text_col)
    ]
)
 
# 2. Pipeline Multimodal Logistic Regression Balanced
multimodal_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42))
])
```


> **🔍 Phân tích mã nguồn: Mã nguồn triển khai kiến trúc Early Fusion bằng cách gom 3 bộ biến đổi (StandardScaler, OneHotEncoder, TfidfVectorizer) vào một ColumnTransformer duy nhất, xuất ra ma trận thưa csr_matrix kích thước N x 1038 đưa vào Logistic Regression với class_weight='balanced'.**


## 4.3. Đánh giá Đối chiếu 3 Hướng tiếp cận (Tabular vs Text vs Multimodal)



| Hướng tiếp cận | Mô hình phân loại | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| --- | --- | --- | --- | --- | --- | --- |
| Multimodal Fusion | Logistic Regression (Balanced) | 93.33% | 98.71% | 93.11% | 95.83% | 0.9772 |
| Multimodal Fusion | LinearSVC (Calibrated) | 93.25% | 95.06% | 96.81% | 95.93% | 0.9735 |
| Multimodal Fusion | Random Forest Classifier | 93.07% | 98.76% | 92.74% | 95.66% | 0.9692 |
| Tabular-Only | Logistic Regression | 93.16% | 98.79% | 92.82% | 95.71% | 0.9720 |
| Tabular-Only | Random Forest Classifier | 93.12% | 98.71% | 92.85% | 95.69% | 0.9655 |
| Text-Only (NLP) | LinearSVC (Calibrated) | 89.84% | 91.49% | 96.63% | 93.99% | 0.9218 |
| Text-Only (NLP) | Logistic Regression | 86.62% | 95.75% | 87.61% | 91.50% | 0.9268 |



*Hình: So sánh chỉ số F1, Recall, Precision và ROC-AUC giữa 3 hướng tiếp cận*


> **📊 Phân tích ý nghĩa biểu đồ: Biểu đồ so sánh 3 trường phái chứng minh mô hình Multimodal Fusion vượt trội toàn diện so với mô hình chỉ dùng Text hoặc chỉ dùng Tabular trên toàn bộ các thang đo Accuracy, F1-Score và ROC-AUC.**


*Hình: Radar Chart đánh giá hiệu năng toàn diện đa chiều của các mô hình*


> **📊 Phân tích ý nghĩa biểu đồ: Radar Chart 5 chiều trực quan hóa không gian bao phủ hiệu năng, làm nổi bật diện tích đa giác của Multimodal Logistic Regression và LinearSVC áp đảo hoàn toàn các hướng tiếp cận đơn lẻ.**


*Hình: Đường cong Precision-Recall Tradeoff và các đường iso-F1 trong phân tích hành vi khách hàng*


> **📊 Phân tích ý nghĩa biểu đồ: Biểu đồ PR Tradeoff cho thấy mô hình Multimodal đạt diện tích dưới đường cong PR AP=0.985, duy trì độ chính xác cực cao (Precision > 98%) ngay cả khi độ bao phủ đạt trên 93%.**

Kết luận đánh giá: Hướng tiếp cận Multimodal Fusion đạt hiệu năng cao nhất, trong đó Logistic Regression Balanced đạt ROC-AUC = 0.9772 và F1 = 95.83%. Mô hình có ưu thế vượt trội về khả năng giải thích (Interpretable AI) qua trọng số từ khóa TF-IDF và thời gian suy luận cực nhanh (dưới 5ms/request).


## 4.4. Triển khai REST API & Giao diện Web/Mobile


*Hình: Giao diện Web: Form nhập thông tin đánh giá sản phẩm (Chụp từ App đang chạy)*


*Hình: Giao diện Web: Thẻ kết quả 'SẴN SÀNG KHUYẾN NGHỊ' với độ tin cậy 99.7%*


*Hình: Giao diện Mobile: Nhập nhận xét thời trang trên điện thoại*


*Hình: Giao diện Mobile: Kết quả phân tích cảm xúc và khuyến nghị trên di động*


# 5. Phân tích So sánh & Đối chiếu Ba Hệ thống Thông minh

Bảng dưới đây tổng hợp đối chiếu toàn diện 3 hệ thống học máy về các khía cạnh kỹ thuật then chốt:



| Khía cạnh kỹ thuật | 1. Diabetes Screening | 2. House Price Valuation | 3. Customer Recommendation |
| --- | --- | --- | --- |
| Bài toán & Miền dữ liệu | Phân loại nhị phân Y tế | Hồi quy Bất động sản | Phân loại nhị phân Đa phương thức TMĐT |
| Đối tượng một quan sát | Một bệnh nhân | Một tin đăng căn nhà | Một bài nhận xét sản phẩm thời trang |
| Không gian đặc trưng x_i | x ∈ R^15 (6 số + 9 OHE) | x ∈ R^55 (7 số + 48 OHE) | x ∈ R^1,038 (38 Tabular + 1,000 TF-IDF) |
| Chiến lược Tiền xử lý | StandardScaler + OneHotEncoder | RobustScaler + Median Imputer + OHE | StandardScaler + OHE + TF-IDF Vectorizer |
| Mô hình được chọn | Random Forest Classifier | Random Forest Regressor | Logistic Regression (Balanced) |
| Tiêu chí đánh giá chính | Recall, F1-Score, ROC-AUC | MAE, RMSE, R² Score | F1-Score, Precision, ROC-AUC |
| Rủi ro dữ liệu thực tế | Mất cân bằng nhãn; Bỏ sót ca bệnh (FN) | Ngoại lệ giá cao; Thiếu tọa độ GPS | Mất cân bằng nhãn; Đánh giá ngắn/nhiễu |
| Artifact đóng gói | diabetes_pipeline.joblib (18.3 MB) | house_price_model.pkl (44.8 MB) | customer_behavior_pipeline.joblib (50 KB) |
| Công nghệ Web / API | FastAPI + Uvicorn + HTML5 Client | FastAPI + Uvicorn + HTML5 Client | FastAPI + Uvicorn + HTML5 Client |



# 6. Khả năng Tái lập, Thảo luận & Hạn chế của Hệ thống


## 6.1. Đảm bảo Tính Tái lập Thực nghiệm (Reproducibility)

• 1. Random Seed: Cố định hạt giống ngẫu nhiên: Mọi bước phân chia dữ liệu (train_test_split) và khởi tạo mô hình đều cố định RANDOM_STATE = 42.

• 2. Anti-Leakage Architecture: Đóng gói Pipeline nguyên khối: Toàn bộ quá trình tiền xử lý được fit duy nhất trên tập Train và đóng gói cùng bộ phân loại thành file artifact (.joblib/.pkl). Khi API nhận dữ liệu mới, pipeline chỉ gọi hàm .transform() mà không fit lại, ngăn chặn tuyệt đối rủi ro Data Leakage.

• 3. Codebase & Environment: Mã nguồn mở và chuẩn hóa môi trường: Toàn bộ code notebook, backend và frontend được quản lý phiên bản trên Git repository [https://github.com/TrVHau/A2_CT_hautv.287](https://github.com/TrVHau/A2_CT_hautv.287) với môi trường Python 3.11 Conda độc lập.


## 6.2. Thảo luận về Giới hạn Thực tế của Hệ thống

• 1. Y tế: Diabetes Prediction: Dù đạt ROC-AUC 0.9738, mô hình vẫn tồn tại 13.2% False Negatives. Dự đoán chỉ mang giá trị cảnh báo sớm hỗ trợ bác sĩ sàng lọc, tuyệt đối không thay thế xét nghiệm chẩn đoán y khoa chuyên sâu.

• 2. Bất động sản: House Price Prediction: R² đạt 0.3729 do dữ liệu tin đăng thiếu các biến không gian then chốt (tọa độ GPS chính xác, khoảng cách tới trường học/bệnh viện, tình trạng pháp lý quy hoạch).

• 3. Thương mại điện tử: Customer Behavior Prediction: Dữ liệu bị mất cân bằng (82.2% nhãn tích cực) và thiếu định danh khách hàng (Customer ID) theo chuỗi thời gian, do đó mô hình chỉ phân loại cảm xúc ở cấp độ từng bài đánh giá đơn lẻ.


# 7. Kết luận & Bài học Kinh nghiệm

• 1. Tầm quan trọng của Biểu diễn dữ liệu (Data Representation): Biểu diễn dữ liệu quyết định thành công của hệ thống: Mô hình học máy không làm việc trực tiếp với file văn bản hay bảng tính CSV thô. Việc lựa chọn phương pháp biểu diễn số học phù hợp (Z-Score cho y tế, RobustScaler cho BĐS có ngoại lệ, TF-IDF n-gram cho văn bản) đóng vai trò nền tảng quyết định chất lượng dự đoán.

• 2. Lựa chọn Mô hình & Chỉ số Đánh giá phù hợp: Đánh giá mô hình phải gắn liền với bản chất bài toán: Không thể chỉ dựa vào Accuracy khi dữ liệu mất cân bằng. Trong y tế, Recall là ưu tiên số 1 để tránh bỏ sót bệnh nhân; trong thương mại điện tử, F1 và ROC-AUC giúp cân bằng giữa độ chính xác và độ bao quát.

• 3. Chuẩn hóa Pipeline Triển khai: Tách bạch kiến trúc Client - Server trong triển khai công nghiệp: Việc đóng gói toàn bộ chuỗi tiền xử lý và mô hình vào Pipeline artifact giúp tách biệt hoàn toàn tầng thuật toán với tầng giao diện (Web/Mobile), đảm bảo tính nhất quán giữa lúc huấn luyện và khi triển khai thực tế.
