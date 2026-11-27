# ASSIGNMENT 1: HỆ THỐNG CHẨN ĐOÁN BỆNH TIỂU ĐƯỜNG
**Sinh viên:** Trần Văn Hậu - B23DCCN287 - Lớp D23CTPM01

## Mô tả hệ thống
- **Bài toán:** Phân loại nhị phân (Binary Classification) dự đoán nguy cơ đái tháo đường.
- **Dữ liệu:** Pima Indians Diabetes Dataset (768 mẫu, 8 đặc trưng y tế).
- **Mô hình tối ưu:** Decision Tree Classifier (`max_depth=5`) đạt F1-score: 0.6271, Recall: 0.6852.
- **Tiền xử lý:** Pipeline khép kín gồm `KNNImputer(k=5)` + `StandardScaler` tránh rò rỉ dữ liệu (Data Leakage).

## Hướng dẫn chạy
1. Cài đặt thư viện: `pip install -r requirements.txt`
2. Huấn luyện mô hình: Chạy notebook `notebooks/diabetes.ipynb`
3. Khởi chạy Web App: Nhấp đúp vào `run_app.bat` hoặc chạy lệnh:
   ```bash
   cd web_app
   python app.py 5000
   ```
4. Truy cập trình duyệt: `http://localhost:5000`
