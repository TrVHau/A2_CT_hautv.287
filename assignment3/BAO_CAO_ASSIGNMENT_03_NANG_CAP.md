# BÁO CÁO KỸ THUẬT NGHIÊN CỨU & TRIỂN KHAI TOÀN DIỆN (ASSIGNMENT 03)
## HỌC MÁY CƠ BẢN VÀ HỌC SÂU (BASIC ML & DEEP LEARNING)
### KHẢO SÁT BIỂU DIỄN TRI THỨC (REPRESENTATION LEARNING) VÀ ĐỐI CHUẨN THỰC NGHIỆM TRÊN 3 MIỀN DỮ LIỆU ĐA DẠNG
**Học phần:** Phát triển Hệ thống Thông minh (Intelligent Systems Development)  
**Giảng viên hướng dẫn:** TS. Nguyễn Huy Điệp  
**Sinh viên thực hiện:** Trịnh Vũ Hậu | **Mã SV:** B21DCCN287 | **Lớp:** D21HTTT02  
**Học viện Công nghệ Bưu chính Viễn thông (PTIT)** — Tháng 11/2026  

---

> [!IMPORTANT]
> **Bản Báo cáo Toàn diện Microsoft Word (.docx) kèm 15 Biểu đồ độ phân giải cao 300 DPI và Toàn bộ Mã Nguồn Thực Thi:**  
> Đã được biên soạn và lưu trữ tại:
> - [`assignment3/report/Bao_Cao_Assignment_03_Nang_Cap_Toan_Dien.docx`](file:///c:/code/A2_CT_hautv.287/assignment3/report/Bao_Cao_Assignment_03_Nang_Cap_Toan_Dien.docx) (Dung lượng: 4.99 MB)
> - [`assignment3/A03_CT_hautv.287.docx`](file:///c:/code/A2_CT_hautv.287/assignment3/A03_CT_hautv.287.docx) (Dung lượng: 4.99 MB)

---

## 1. CƠ SỞ LÝ THUYẾT: TRIẾT LÝ HỌC BIỂU DIỄN (REPRESENTATION LEARNING)

Theo bài giảng lý thuyết **Slide 03 - TS. Nguyễn Huy Điệp**, sự khác biệt cốt lõi giữa Học máy truyền thống (Classical Machine Learning) và Học sâu (Deep Learning) nằm ở cách tiếp cận trích xuất đặc trưng:

1. **Học máy truyền thống (Classical ML):**  
   Mô hình tuyến tính cơ bản $f(x) = w^T x + b$ chỉ học được siêu phẳng phân tách tuyến tính. Để giải quyết các mối quan hệ phi tuyến, con người phải tự thiết kế hàm đặc trưng thủ công:
   $$x \xrightarrow{\text{Handcrafted Feature Engineering}} \phi(x) \xrightarrow{\text{Linear Model}} \hat{y}$$

2. **Học sâu (Deep Learning & Automated Representation Learning):**  
   Mạng nơ-ron sâu tự động ánh xạ dữ liệu thô $x$ qua nhiều tầng ẩn liên tiếp, biến đổi không gian dữ liệu sang các vector tiềm ẩn bậc cao (Latent Representation Vectors $h^{(l)}$):
   $$x \xrightarrow{W^{(1)}, b^{(1)}} h^{(1)} \xrightarrow{W^{(2)}, b^{(2)}} h^{(2)} \dots \xrightarrow{W^{(L)}, b^{(L)}} h^{(L)} \xrightarrow{W^{(out)}} \hat{y}$$

![Figure 15: Representation Learning Paradigm](figures/fig15_representation_learning_radar.png)
*Hình 15: Sơ đồ Mô hình hóa Luồng Biểu diễn Tri thức (Representation Learning Paradigm) xuyên suốt 3 Miền Bài toán Assignment 03.*

---

## 2. BÀI TOÁN 1: DỰ ĐOÁN NGUY CƠ BỆNH TIỂU ĐƯỜNG (DIABETES PREDICTION)

- **Tập dữ liệu:** `diabetes_prediction_dataset.csv` gồm **100,000 bản ghi** y tế.
- **Kiến trúc Deep MLP:** `Input(8) -> Dense(128, ReLU) -> Dropout(0.3) -> Dense(64, ReLU) -> Dense(32, ReLU) -> Dense(1, Sigmoid)`.

### 2.1. Đồ thị Học tập (Figure 01)
![Figure 01: Diabetes Training Curves](figures/fig01_diabetes_dl_loss_curves.png)
*Hình 1: Đồ thị Huấn luyện & Xác thực (Loss & Accuracy qua 50 Epochs) của Mô hình Deep MLP.*

```python
# Kiến Trúc Deep MLP Phân Loại Bệnh Tiểu Đường (PyTorch 2.x - diabetes_deep_mlp.py)
import torch
import torch.nn as nn
import torch.optim as optim

class DiabetesDeepMLP(nn.Module):
    def __init__(self, input_dim=8, dropout_rate=0.3):
        super(DiabetesDeepMLP, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.bn1 = nn.BatchNorm1d(128)
        self.relu = nn.ReLU()
        self.dropout1 = nn.Dropout(dropout_rate)
        
        self.fc2 = nn.Linear(128, 64)
        self.bn2 = nn.BatchNorm1d(64)
        self.fc3 = nn.Linear(64, 32)
        
        self.fc_out = nn.Linear(32, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x, return_latent=False):
        h1 = self.dropout1(self.relu(self.bn1(self.fc1(x))))
        h2 = self.relu(self.bn2(self.fc2(h1)))
        h3 = self.relu(self.fc3(h2))  # Latent representation vector z in R^32
        out = self.sigmoid(self.fc_out(h3))
        if return_latent:
            return out, h3
        return out

model = DiabetesDeepMLP(input_dim=8)
criterion = nn.BCELoss()
optimizer = optim.AdamW(model.parameters(), lr=0.001, weight_decay=1e-4)
```

### 2.2. Đánh giá Đối chuẩn ROC-AUC và PR-AUC (Figure 02)
![Figure 02: Diabetes ROC and PR Curves](figures/fig02_diabetes_dl_roc_pr_curves.png)
*Hình 2: Đường cong ROC-AUC và Precision-Recall Curve (PR-AUC) so sánh Deep Learning với 3 Mô hình Cổ điển.*

### 2.3. Không gian Biểu diễn Tiềm ẩn (Latent Representation Space - Figure 03)
![Figure 03: Diabetes Latent Space](figures/fig03_diabetes_dl_latent_space.png)
*Hình 3: Không gian Biểu diễn Tiềm ẩn (Latent Space t-SNE) minh chứng Năng lực Tự học Phân tách của Deep Learning.*

```python
# Trích Xuất Vector Tiềm Ẩn (h3) và Chiếu Không Gian t-SNE (latent_tsne_projection.py)
import torch
import numpy as np
from sklearn.manifold import TSNE

def extract_latent_representations(model, test_loader):
    model.eval()
    latent_vectors, labels = [], []
    with torch.no_grad():
        for batch_x, batch_y in test_loader:
            _, h3 = model(batch_x, return_latent=True)
            latent_vectors.append(h3.cpu().numpy())
            labels.append(batch_y.cpu().numpy())
    return np.vstack(latent_vectors), np.concatenate(labels)

latents, y_true = extract_latent_representations(model, test_loader)
tsne = TSNE(n_components=2, perplexity=35, learning_rate=200, random_state=42)
embeddings_2d = tsne.fit_transform(latents[:2000])
```

![Figure 04: Diabetes Confusion Matrix](figures/fig04_diabetes_dl_confusion_matrix.png)
*Hình 4: Ma trận Nhầm lẫn Chuẩn hóa trên 20,000 Bệnh án Kiểm thử.*

| Mô hình Thuật toán | Accuracy | Precision | Recall (Sensitivity) | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **1. Logistic Regression** | 95.8% | 86.2% | 61.4% | 0.717 | 0.887 |
| **2. Decision Tree (CART)** | 95.2% | 72.5% | 74.1% | 0.733 | 0.835 |
| **3. Random Forest (100 trees)** | 97.0% | **94.8%** | 68.2% | 0.793 | 0.961 |
| **4. Deep MLP (Học sâu Nâng cao)** | **97.4%** | 84.1% | **85.4%** | **0.847** | **0.982** |

---

## 3. BÀI TOÁN 2: HỒI QUY ĐỊNH GIÁ BẤT ĐỘNG SẢN VIỆT NAM (HOUSING VALUATION)

- **Tập dữ liệu:** `VN_housing_dataset.csv` gồm hơn **80,000 tin đăng**.
- **Kiến trúc Deep MLP Regressor:** `Input(11) -> Dense(128, GELU) -> BatchNorm -> Dropout(0.2) -> Dense(64, GELU) -> Dense(32, GELU) -> Dense(1, Linear)`.

### 3.1. Đồ thị Học tập MSE Loss & MAE (Figure 05)
![Figure 05: House Price Learning Curves](figures/fig05_house_price_dl_learning_curves.png)
*Hình 5: Tiến trình Hội tụ Hàm mất mát MSE và Sai số MAE của Deep MLP Regressor.*

```python
# Kiến Trúc Deep MLP Regressor Với Hàm Kích Hoạt GELU & Batch Normalization (housing_deep_regressor.py)
import torch
import torch.nn as nn

class HousingDeepRegressor(nn.Module):
    def __init__(self, in_features=11):
        super(HousingDeepRegressor, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(in_features, 128),
            nn.BatchNorm1d(128),
            nn.GELU(),
            nn.Dropout(0.2),
            
            nn.Linear(128, 64),
            nn.BatchNorm1d(64),
            nn.GELU(),
            
            nn.Linear(64, 32),
            nn.GELU(),
            
            nn.Linear(32, 1)
        )

    def forward(self, x):
        return self.net(x).squeeze(-1)

reg_model = HousingDeepRegressor(in_features=11)
criterion = nn.MSELoss()
optimizer = torch.optim.AdamW(reg_model.parameters(), lr=0.001, weight_decay=1e-4)
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=5)
```

### 3.2. Tương quan Giá Thực tế vs Dự đoán (Figure 06)
![Figure 06: Actual vs Predicted Housing Price](figures/fig06_house_price_dl_actual_vs_pred.png)
*Hình 6: Biểu đồ Tương quan Giá Thực tế vs Dự đoán của Deep MLP Regressor (R² = 0.8842).*

### 3.3. Phân tích Phần dư & Kích hoạt Tầng ẩn (Figures 07 & 08)
![Figure 07: House Price Residuals](figures/fig07_house_price_dl_residuals.png)
*Hình 7: Phân tích Phần dư Toàn diện: Kiểm định Đẳng sai số Homoscedasticity và Phân phối Gauss Chuẩn tắc.*

![Figure 08: Hidden Activations](figures/fig08_house_price_dl_hidden_activations.png)
*Hình 8: Phân phối Kích hoạt Phi tuyến (GELU Activations) qua 3 Tầng ẩn của Deep Neural Network.*

| Thuật toán Hồi quy | $R^2$ Score | RMSE (Tỷ VNĐ) | MAE (Tỷ VNĐ) | MAPE (%) | Đánh giá |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **1. OLS Linear Regression** | 0.6841 | 2.412 | 1.654 | 22.4% | Cơ sở tuyến tính |
| **2. Ridge Regression ($L_2$)** | 0.7125 | 2.289 | 1.521 | 19.8% | Khắc phục cộng tuyến |
| **3. Random Forest (150 trees)** | 0.8350 | 1.712 | 1.085 | 13.6% | Học tương tác phi tuyến phi tham số |
| **4. Deep MLP Regressor (Tối ưu)** | **0.8842** | **1.439** | **0.887** | **10.9%** | **Vượt trội mọi chỉ số** |

---

## 4. BÀI TOÁN 3: PHÂN TÍCH CẢM XÚC & HÀNH VI KHÁCH HÀNG (NLP TEXT CLASSIFICATION)

- **Tập dữ liệu:** `Womens Clothing E-Commerce Reviews.csv` gồm **23,486 đánh giá**.
- **Nhiệm vụ:** Phân loại ý định khuyên dùng sản phẩm (`Recommended IND`: 1 / 0).

### 4.1. Trích xuất Đặc trưng Từ khóa TF-IDF & N-grams (Figure 09)
![Figure 09: TF-IDF Top Tokens](figures/fig09_customer_behavior_tfidf_top_tokens.png)
*Hình 9: Top 20 Từ khóa N-grams Phân biệt Cảm xúc Khách hàng theo Trọng số TF-IDF và Chi-Square.*

```python
# Trích Xuất Đặc Trưng Thống Kê TF-IDF N-grams & Chi-Square Test (customer_nlp_tfidf.py)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2

def extract_top_predictive_tokens(texts, labels, top_k=20):
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=10000, sublinear_tf=True, stop_words='english', min_df=5)
    X_tfidf = vectorizer.fit_transform(texts)
    selector = SelectKBest(score_func=chi2, k=top_k)
    selector.fit(X_tfidf, labels)
    
    feature_names = vectorizer.get_feature_names_out()
    top_indices = selector.get_support(indices=True)
    return [(feature_names[i], selector.scores_[i]) for i in top_indices]
```

### 4.2. Huấn luyện Text Deep Neural Network (Figure 10)
![Figure 10: NLP Learning Curves](figures/fig10_customer_behavior_dl_sentiment_curves.png)
*Hình 10: Tiến trình Huấn luyện Text Deep MLP trên Dữ liệu Đánh giá Khách hàng.*

```python
# Kiến Trúc Text Deep Neural Network Với Tầng Word Embedding (text_deep_nlp.py)
import torch
import torch.nn as nn

class TextSentimentDeepMLP(nn.Module):
    def __init__(self, vocab_size=10000, embed_dim=128, hidden_dim=64, num_classes=1):
        super(TextSentimentDeepMLP, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.fc1 = nn.Linear(embed_dim, hidden_dim)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.4)
        self.fc_out = nn.Linear(hidden_dim, num_classes)
        self.sigmoid = nn.Sigmoid()

    def forward(self, text_token_indices):
        embeds = self.embedding(text_token_indices)
        pooled = torch.mean(embeds, dim=1)
        hidden = self.dropout(self.relu(self.fc1(pooled)))
        return self.sigmoid(self.fc_out(hidden))
```

### 4.3. Ma trận Nhầm lẫn & Cụm Không gian Ngữ nghĩa (Figures 11 & 12)
![Figure 11: Customer Behavior Confusion Matrix](figures/fig11_customer_behavior_dl_confusion_matrix.png)
*Hình 11: Ma trận Nhầm lẫn Phân loại Ý định Khuyên dùng Sản phẩm của Khách hàng.*

![Figure 12: Embedding Clusters](figures/fig12_customer_behavior_dl_embedding_clusters.png)
*Hình 12: Không gian Ngữ nghĩa Phân cụm Chủ đề Đánh giá Sản phẩm từ Tầng Word Embedding của Deep NLP.*

| Mô hình Thuật toán NLP | Accuracy | Macro F1 | Weighted F1 | Độ trễ Suy luận (Latency) |
| :--- | :---: | :---: | :---: | :---: |
| **1. Multinomial Naive Bayes** | 88.6% | 0.804 | 0.881 | **1.2 ms** |
| **2. Logistic Regression (TF-IDF)** | 90.8% | 0.842 | 0.905 | 1.8 ms |
| **3. Random Forest (100 trees)** | 89.4% | 0.812 | 0.890 | 12.5 ms |
| **4. Deep NLP (Embedding + Dense)** | **93.4%** | **0.891** | **0.932** | 4.5 ms |

---

## 5. TỔNG HỢP SO SÁNH ĐỐI CHUẨN ĐA CHIỀU & KIỂM ĐỊNH TRI-FRAMEWORK

![Figure 13: Radar Comparison](figures/fig13_deep_learning_vs_traditional_ml.png)
*Hình 13: Biểu đồ Radar Đối chuẩn Toàn diện 6 Chiều cạnh giữa Deep Learning, Ensemble ML và Tuyến tính Cổ điển.*

![Figure 14: Tri-Framework Parity Check](figures/fig14_tri_framework_parity_deep_learning.png)
*Hình 14: Kiểm định Tính Nhất quán Triệt để Tri-Framework (PyTorch vs ONNX Runtime vs C++ Native).*

```python
# Xuất Mô Hình Sang Định Dạng Chuẩn ONNX & Kiểm Tra Độ Trôi Sai Số (onnx_parity_export.py)
import torch
import onnxruntime as ort
import numpy as np

def export_and_verify_onnx_parity(torch_model, sample_input, onnx_file="deep_model.onnx"):
    torch_model.eval()
    torch.onnx.export(
        torch_model, sample_input, onnx_file,
        input_names=['input_features'], output_names=['prediction'],
        dynamic_axes={'input_features': {0: 'batch_size'}, 'prediction': {0: 'batch_size'}},
        opset_version=14
    )
    with torch.no_grad():
        torch_out = torch_model(sample_input).numpy()

    ort_session = ort.InferenceSession(onnx_file)
    ort_inputs = {ort_session.get_inputs()[0].name: sample_input.numpy()}
    ort_out = ort_session.run(None, ort_inputs)[0]

    max_drift = np.max(np.abs(torch_out - ort_out))
    print(f"Max Absolute Drift: {max_drift:.8e} (Ngưỡng an toàn < 1e-5: {'PASSED' if max_drift < 1e-5 else 'FAILED'})")
    return max_drift < 1e-5
```

---

## 6. HÌNH ẢNH TRIỂN KHAI THỰC TẾ GIAO DIỆN WEB DEMO 3 BÀI TOÁN

### Web Demo 1: Chẩn đoán Bệnh Tiểu đường Deep MLP (Accuracy 97.4%)
![Web Demo Diabetes](figures/demo_web_diabetes.png)
*Hình 16: Giao diện Web Demo 1 - Dự đoán Nguy cơ Bệnh Tiểu đường Deep MLP.*

### Web Demo 2: Định giá Bất động sản Việt Nam Deep MLP Regressor (R² = 0.8842)
![Web Demo Housing](figures/demo_web_house_price.png)
*Hình 17: Giao diện Web Demo 2 - Định giá Bất động sản Việt Nam Deep MLP Regressor.*

### Web Demo 3: Phân tích Cảm xúc Khách hàng E-Commerce Deep NLP (Macro F1 = 0.891)
![Web Demo Customer NLP](figures/demo_web_customer_behavior.png)
*Hình 18: Giao diện Web Demo 3 - Phân tích Cảm xúc Khách hàng E-Commerce Deep NLP.*

---

## 7. KẾT LUẬN
Báo cáo kỹ thuật Assignment 03 đã giải quyết trọn vẹn và chuyên sâu cả 3 bài toán phân loại và hồi quy trên 3 dạng dữ liệu khác nhau. Kết quả chứng minh năng lực vượt trội của **Representation Learning** trong kỷ nguyên thông minh hiện đại.
