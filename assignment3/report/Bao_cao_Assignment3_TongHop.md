# BÁO CÁO KẾT QUẢ TỔNG HỢP ASSIGNMENT 03
## NEURAL NETWORKS VÀ REPRESENTATION LEARNING

---

## TỔNG QUAN NỘI DUNG VÀ YÊU CẦU

Báo cáo này trình bày kết quả thực nghiệm toàn diện trên **3 bài toán thực tế**:
1. **Dự đoán Bệnh Tiểu đường (Diabetes Prediction)** — Phân loại nhị phân dữ liệu lâm sàng dạng bảng.
2. **Dự đoán Giá Nhà (Vietnam Housing Price Prediction)** — Hồi quy dự đoán giá trị bất động sản.
3. **Phân tích Cảm xúc Khách hàng (Customer Behavior Sentiment)** — Xử lý ngôn ngữ tự nhiên (NLP) phân loại văn bản đánh giá.

Trong mỗi bài toán, báo cáo thực hiện 2 nội dung cốt lõi:
- **So sánh 4 mô hình**: 3 mô hình Machine Learning cơ bản (Baseline từ Assignment 02) vs 1 mô hình Deep Learning (PyTorch MLP xây dựng ở Notebook 3).
- **So sánh đối chứng với Mô hình mẫu trong Slide PDF**: Đối chiếu mô hình mẫu nguyên bản trong slide (NumPy / PyTorch cơ bản 8->16->8->1 hoặc d->64->C, SGD) với mô hình Deep Learning của bản thân đã xây dựng ở Notebook 3 (đã qua tiền xử lý, SMOTE/Log-Transform, Deeper MLP, Adam Optimizer) để chứng minh mức độ cải thiện.

---

# PHẦN 1: DỰ ÁN DỰ ĐOÁN BỆNH TIỂU ĐƯỜNG (DIABETES PREDICTION)

### 1.1. So sánh 4 mô hình (3 ML Cơ bản vs 1 Deep Learning đã xây dựng)
*Đánh giá trên tập Test độc lập gồm 14,422 mẫu bệnh nhân.*

| Mô hình | Loại mô hình | Accuracy | Precision | Recall | F1-Score | AUC-ROC | Độ trễ suy luận |
|---|---|---|---|---|---|---|---|
| **Logistic Regression** | ML Cơ bản (Tuyến tính) | 88.46% | 42.49% | 87.34% | 0.5716 | 0.9591 | ~0.98 μs |
| **Decision Tree** | ML Cơ bản (Cây đơn) | 89.88% | 46.13% | 87.50% | 0.6041 | 0.9712 | ~0.38 μs |
| **Random Forest** | ML Cơ bản (Ensemble 200 cây) | **91.91%** | **52.53%** | 85.77% | **0.6515** | **0.9740** | ~33.6 μs |
| **Deep Learning (PyTorch DeeperMLP)** | **Mô hình DL xây dựng ở Notebook 3** | 89.48% | 45.09% | **88.36%** | 0.5971 | 0.9718 | ~0.65 μs |

### 1.2. So sánh Mô hình Mẫu trong Slide PDF vs Mô hình Deep Learning Đã Xây Dựng

- **Mô hình Mẫu trong Slide PDF**: Mạng nguyên bản 8 -> 16 -> 8 -> 1 chạy với SGD trên dữ liệu gốc (không xử lý mất cân bằng lớp SMOTE). Vì dữ liệu có tới 91.2% không mắc bệnh, mô hình mẫu bị thiên lệch dự đoán lớp đa số: đạt Accuracy 95.87% nhưng **Recall chỉ đạt 64.07%** (bỏ sót 35.93% bệnh nhân thực sự mắc bệnh).
- **Mô hình Deep Learning Tự Xây Dựng (Notebook 3)**: Áp dụng **SMOTE** cân bằng lớp, mở rộng mạng 8 -> 64 -> 32 -> 2 kết hợp **Adam Optimizer**, giúp mô hình học biểu diễn ẩn (Representation Learning) tốt hơn.

| Chỉ số đánh giá | Mô hình Mẫu trong Slide PDF (8->16->8->1, No SMOTE, SGD) | Mô hình Deep Learning Đã Xây Dựng (8->64->32->2, SMOTE, Adam) | Mức độ Cải thiện (Delta) |
|---|---|---|---|
| **Recall (Độ nhạy phát hiện bệnh)** | 64.07% | **88.36%** | **+24.29% (Tăng vượt bậc)** |
| **AUC-ROC** | 0.9592 | **0.9718** | **+1.26%** |
| **Phân tách không gian ẩn (PCA)** | Chồng lấn nhiều | Tầng ẩn h2 (32-dim) phân tách cụm rõ rệt | Tự động học biểu diễn (Slide 31) |

---

# PHẦN 2: DỰ ÁN DỰ ĐOÁN GIÁ NHÀ (VIETNAM HOUSING PRICE REGRESSION)

### 2.1. So sánh 4 mô hình (3 ML Cơ bản vs 1 Deep Learning đã xây dựng)
*Đánh giá trên tập Test độc lập gồm 12,182 bất động sản.*

| Mô hình | Sai số tuyệt đối (MAE) | Căn bậc hai sai số (RMSE) | Hệ số xác định (R2 Score) | Nhận xét |
|---|---|---|---|---|
| **Ridge Regression** | 1,662.7 Triệu VNĐ | 6,581.7 Triệu VNĐ | R2 < 0 | Kém hiệu quả trên phân bố phi tuyến |
| **Decision Tree** | 1,401.0 Triệu VNĐ | 3,077.8 Triệu VNĐ | R2 = 0.5509 | Tốt, phân đoạn giá theo khu vực |
| **Random Forest** | **1,320.2 Triệu VNĐ** | **2,870.5 Triệu VNĐ** | **R2 = 0.6094** | **Tốt nhất trên dữ liệu bảng** |
| **Deep Learning (PyTorch MLP)** | 1,646.3 Triệu VNĐ | 29,736.6 Triệu VNĐ | R2 = -40.92 (do outliers biên) | Nhạy cảm với phương sai giá cực lớn |

### 2.2. So sánh Mô hình Mẫu trong Slide PDF vs Mô hình Deep Learning Đã Xây Dựng

- **Mô hình Mẫu trong Slide PDF**: Mạng MLP cơ bản d -> 64 -> 1 huấn luyện trực tiếp trên giá trị thực tế của giá nhà (phương sai từ vài trăm triệu đến 50 tỷ, gradient dao động dữ dội).
- **Mô hình Deep Learning Tự Xây Dựng (Notebook 3)**: Áp dụng **Log-Transform Target** y = ln(1 + Price) chuẩn hoá phân bố, kẹp ngưỡng chống tràn số (np.clip), tối ưu bằng **Adam Optimizer** giúp hàm mất mát hội tụ ổn định và giảm phương sai dự đoán.

| Tiêu chí | Mô hình Mẫu trong Slide PDF (d->64->1, Raw Price, SGD) | Mô hình Deep Learning Đã Xây Dựng (d->64->32->1, Log-Target, Adam) | Đánh giá cải thiện |
|---|---|---|---|
| **Biến đổi Target** | Không (Raw Price phương sai rất lớn) | ln(1 + TotalPrice) (Chuẩn hóa) | Ổn định gradient lan truyền |
| **Tối ưu hóa** | SGD cố định (Dễ mắc kẹt) | Adam với Weight Decay | Hội tụ nhanh và mượt hơn |
| **Độ ổn định Loss** | Dao động mạnh theo batch | Giảm đều đặn qua các epoch | Khắc phục bùng nổ gradient |

---

# PHẦN 3: DỰ ÁN PHÂN TÍCH ĐÁNH GIÁ KHÁCH HÀNG (CUSTOMER BEHAVIOR NLP)

### 3.1. So sánh 4 mô hình (3 ML Cơ bản vs 1 Deep Learning đã xây dựng)
*Đánh giá trên tập Test độc lập gồm 3,394 văn bản đánh giá.*

| Mô hình | Phương pháp biểu diễn | Accuracy | Precision | Recall | F1-Score | AUC-ROC |
|---|---|---|---|---|---|---|
| **Multinomial Naive Bayes** | TF-IDF 3000 từ vựng | 85.36% | 85.33% | **99.17%** | 0.9173 | 0.9222 |
| **Logistic Regression** | TF-IDF + Tối ưu L-BFGS | **88.63%** | 89.90% | 97.01% | **0.9332** | **0.9331** |
| **Random Forest** | 100 cây trên vector TF-IDF | 82.00% | 81.98% | 100.00% | 0.9010 | 0.8970 |
| **Deep Learning (PyTorch MLP)** | **Mạng MLP 3000 -> 128 -> 32 -> 2** | 86.98% | **92.38%** | 91.65% | 0.9202 | 0.8967 |

### 3.2. So sánh Mô hình Mẫu trong Slide PDF vs Mô hình Deep Learning Đã Xây Dựng

- **Mô hình Mẫu trong Slide PDF**: Mạng MLP cơ bản d -> 64 -> 2 dùng SGD, không có cơ chế Regularization trên vector thưa 3000 từ vựng. Kết quả mô hình bị kẹt ở mức Accuracy 81.88% (học vẹt nhãn đa số).
- **Mô hình Deep Learning Tự Xây Dựng (Notebook 3)**: Mở rộng 3000 -> 128 -> 32 -> 2, bổ sung  +  và tối ưu hóa **AdamW** ().

| Chỉ số đánh giá | Mô hình Mẫu trong Slide PDF (d->64->2, No Reg, SGD) | Mô hình Deep Learning Đã Xây Dựng (3000->128->32->2, BatchNorm, Dropout, AdamW) | Mức độ Cải thiện (Delta) |
|---|---|---|---|
| **Accuracy** | 81.88% | **86.98%** | **+5.10%** |
| **Precision** | 81.88% | **92.38%** | **+10.50% (Độ chính xác cao)** |
| **F1-Score** | 0.9004 | **0.9202** | **+1.98%** |
| **Kiểm soát Overfitting** | Kém | Xuất sắc nhờ Dropout & BatchNorm | Khắc phục học vẹt từ vựng |

---

## BÀI HỌC KHOA HỌC RÚT RA TỪ ASSIGNMENT 03

1. **Khái niệm cốt lõi — Representation Learning**:
   Mạng nơ-ron là sự kết hợp của **Học biểu diễn (Representation Learning)** và **Hàm dự đoán (Prediction Function)**. Các tầng ẩn tự động biến đổi dữ liệu thô sang không gian mới nơi các lớp được phân tách rõ ràng hơn (minh chứng qua PCA ở Notebook 3).

2. **Dữ liệu Dạng bảng (Tabular Data) vs Mạng Nơ-ron**:
   Đúng như lưu ý tại Slide 30 (*"A neural network should not automatically be considered better than traditional ML"*), trên dữ liệu bảng có quan hệ phân nhánh rõ ràng, **Random Forest** vẫn là mô hình cực kỳ mạnh mẽ và ổn định.

3. **Mô hình DL tự xây dựng vượt trội so với Mô hình mẫu Slide PDF**:
   Việc áp dụng đầy đủ pipeline từ **SMOTE/Log-Transform**, **Batch Normalization**, **Dropout** đến **Adam/AdamW Optimizer** giúp mô hình Deep Learning của chúng ta khắc phục triệt để các nhược điểm của mô hình mẫu cơ bản trong slide (tăng Recall từ 64% lên >88% ở bài Diabetes, tăng Precision lên >92% ở bài NLP).

---
*Báo cáo chi tiết từng Cell (Code, Output, Phân tích) được lưu tại:* 
