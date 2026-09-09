# Assignment 3 - Basic ML & Deep Learning

## Yêu cầu

1. **Chuẩn bị dữ liệu** cho 3 bài toán: `diabetes`, `house-price`, `comments`
2. **Chọn 3 mô hình ML cơ bản**
3. **Xây dựng mô hình Deep Learning**
4. **So sánh 4 mô hình** (3 ML cơ bản + 1 DL)

## Cấu trúc thư mục

```
assignment3/
├── require_assign3.txt                        # Yêu cầu bài tập
├── int_sys_dev_slide_03_basicML_deepLearning_04.09.pdf   # Slide lý thuyết
├── intel_sys_dev_slide_03.pdf                 # Slide lý thuyết (bản khác)
│
├── diabetes/                                  # Bài toán 1: Dự đoán tiểu đường (phân loại)
│   ├── data/
│   │   └── diabetes_prediction_dataset.csv
│   ├── notebook/
│   │   ├── 1_eda_and_preprocessing.ipynb
│   │   ├── 2_ml_models.ipynb                  # 3 mô hình ML cơ bản
│   │   ├── 3_deep_learning.ipynb             # Mô hình Deep Learning
│   │   └── 4_model_comparison.ipynb          # So sánh 4 mô hình
│   ├── models/                                # Lưu model đã huấn luyện
│   └── web/                                   # Demo web (Flask/Streamlit)
│
├── house_price/                               # Bài toán 2: Dự đoán giá nhà (hồi quy)
│   ├── data/
│   │   └── VN_housing_dataset.csv
│   ├── notebook/
│   │   ├── 1_eda_and_preprocessing.ipynb
│   │   ├── 2_ml_models.ipynb
│   │   ├── 3_deep_learning.ipynb
│   │   └── 4_model_comparison.ipynb
│   ├── models/
│   └── web/
│
├── customer_behavior/                         # Bài toán 3: Phân tích đánh giá khách hàng (NLP text)
│   ├── data/
│   │   └── Womens Clothing E-Commerce Reviews.csv
│   ├── notebook/
│   │   ├── 1_eda_and_preprocessing.ipynb
│   │   ├── 2_ml_models.ipynb
│   │   ├── 3_deep_learning.ipynb
│   │   └── 4_model_comparison.ipynb
│   ├── models/
│   └── web/
│
├── report/                                    # Báo cáo tổng hợp & so sánh
└── screenshots/                               # Ảnh chụp màn hình
```

## Ghi chú

- Data được sao chép từ **Assignment 2** (`/home/dau/assignment2`).
- So sánh 4 mô hình dựa trên: Accuracy, Precision, Recall, F1-score (phân loại) / MAE, MSE, RMSE, R² (hồi quy).
