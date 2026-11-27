# ASSIGNMENT 2: HỆ THỐNG DỰ ĐOÁN GIÁ NHÀ VIỆT NAM
**Sinh viên:** Trần Văn Hậu - B23DCCN287 - Lớp D23CTPM01

## Mô tả hệ thống
- **Bài toán:** Hồi quy (Regression) ước tính giá trị bất động sản nhà ở Việt Nam (tỷ VNĐ).
- **Dữ liệu:** Vietnam Housing Dataset 2024 (30.229 tin đăng, 10 đặc trưng).
- **Mô hình tối ưu:** Random Forest Regressor (100 cây, `max_depth=15`) đạt RMSE: 1.8170 tỷ VNĐ, R²: 0.3229, MAE: 1.4406 tỷ VNĐ.
- **Triển khai đa nền tảng:** Hỗ trợ song song cả giao diện Desktop (/) và Mobile tối ưu (/mobile) với bộ tự động nhận diện User-Agent.

## Hướng dẫn chạy
1. Cài đặt thư viện: `pip install -r requirements.txt`
2. Huấn luyện mô hình: Chạy notebook `notebooks/dudoangiannha.ipynb`
3. Khởi chạy Web & Mobile App: Nhấp đúp vào `run_app.bat` hoặc chạy lệnh:
   ```bash
   cd web_mobile_app
   python app.py 5001
   ```
4. Truy cập giao diện:
   - Desktop: `http://localhost:5001`
   - Mobile: `http://localhost:5001/mobile`
