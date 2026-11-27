# BÁO CÁO KỸ THUẬT NGHIÊN CỨU & TRIỂN KHAI NÂNG CAO (ASSIGNMENT 02)
## HỆ THỐNG ĐỊNH GIÁ NHÀ ĐẤT VIỆT NAM THÔNG MINH
**Học phần:** Phát triển Hệ thống Thông minh (Intelligent Systems Development)  
**Giảng viên hướng dẫn:** TS. Nguyễn Huy Điệp  
**Sinh viên thực hiện:** Trịnh Vũ Hậu | **Mã SV:** B21DCCN287 | **Lớp:** D21HTTT02  
**Học viện Công nghệ Bưu chính Viễn thông (PTIT)** — Tháng 11/2026  

---

> [!IMPORTANT]
> **Bản Báo cáo Toàn diện Microsoft Word (.docx) kèm 14 Biểu đồ độ phân giải cao 300 DPI và Toàn bộ Mã Nguồn Thực Thi:**  
> Đã được biên soạn và lưu trữ tại: [`Bao_Cao_Assignment_02_Nang_Cap_Toan_Dien.docx`](file:///c:/code/A2_CT_hautv.287/assignment2/Bao_Cao_Assignment_02_Nang_Cap_Toan_Dien.docx) (Dung lượng: 3.64 MB).

---

## 1. TỔNG QUAN & ĐẶT VẤN ĐỀ
Thị trường bất động sản Việt Nam là thị trường phi tập trung với độ phức tạp rất cao:
- **Pháp lý đa dạng:** Sổ đỏ/Sổ hồng lâu dài, Sổ nông nghiệp/chờ chuyển mục đích, Giấy tờ viết tay/vi bằng.
- **Hình thái giao thông đặc thù:** Hệ thống ngõ hẻm chằng chịt, giá trị nhà biến thiên mạnh tùy theo độ rộng ngõ (ngõ ô tô tránh nhau vs ngõ xe máy).
- **Phân phối giá cực đoan:** Dữ liệu rao bán thực tế có phân phối lệch phải (Right-skewed Power Law) với Skewness lên tới +14.28.

---

## 2. KHÁM PHÁ DỮ LIỆU LỚN (EDA) VÀ PIPELINE TIỀN XỬ LÝ DỮ LIỆU

Tập dữ liệu gồm **30,168 bất động sản thực tế** trên khắp Việt Nam sau khi làm sạch ngoại lai bằng bộ lọc IQR và giới hạn biên vật lý.

### 2.1. Phân phối Biến Mục tiêu & Phép Biến đổi Logarit (Figure 01)
Biến mục tiêu Giá bán (Tỷ VNĐ) ban đầu có độ lệch phải rất lớn. Áp dụng phép biến đổi $y' = \ln(1 + y)$ đã đưa phân phối về dạng Gauss đối xứng tuyệt đối (Skewness = -0.12).

![Figure 01: Target Price Distribution](figures/fig01_target_price_distribution.png)
*Hình 1: Phân phối Giá nhà gốc so với Phân phối chuẩn Log-Transformed (N = 30,168).*

```python
# Pipeline Tiền Xử Lý Dữ Liệu Bất Động Sản & Log-Transform Target (vietnam_housing_preprocessing.py)
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class HousingDataPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self, area_bounds=(10, 1500), frontage_bounds=(1.5, 50.0)):
        self.area_bounds = area_bounds
        self.frontage_bounds = frontage_bounds
        self.regional_imputers = {}
        
    def fit(self, X, y=None):
        df = X.copy()
        for region in df['District'].unique():
            self.regional_imputers[region] = {
                'median_frontage': df[df['District'] == region]['Frontage'].median(),
                'median_road': df[df['District'] == region]['Access Road'].median()
            }
        return self

    def transform(self, X):
        df = X.copy()
        df = df[(df['Area'] >= self.area_bounds[0]) & (df['Area'] <= self.area_bounds[1])]
        for region, medians in self.regional_imputers.items():
            mask = df['District'] == region
            df.loc[mask & df['Frontage'].isna(), 'Frontage'] = medians['median_frontage']
            df.loc[mask & df['Access Road'].isna(), 'Access Road'] = medians['median_road']
            
        df['Has_Certificate'] = (df['Legal status'] == 'Have certificate').astype(int)
        df['Has_Car_Road'] = (df['Access Road'] >= 4.0).astype(int)
        return df

# Log1p transformation đưa Skewness từ +14.28 về -0.12
y_raw = df['Price_Billion'].values
y_log = np.log1p(y_raw)
print(f"Skewness ban đầu: {pd.Series(y_raw).skew():.2f} -> Sau Log1p: {pd.Series(y_log).skew():.2f}")
```

---

### 2.2. Bản đồ Nhiệt Đơn giá m² theo Địa phương & Loại hình (Figure 02)
![Figure 02: Regional Price Heatmap](figures/fig02_regional_price_heatmap.png)
*Hình 2: Bản đồ nhiệt Đơn giá m² theo Tỉnh/Thành phố và Loại hình Bất động sản.*

### 2.3. Tương quan Diện tích vs Giá & Hồi quy OLS (Figure 03)
![Figure 03: Area vs Price Scatter](figures/fig03_area_vs_price_scatter.png)
*Hình 3: Tương quan Diện tích vs Giá theo từng Tỉnh thành kèm Đường hồi quy OLS.*

### 2.4. Phân tích Tác động Pháp lý (Figure 04)
![Figure 04: Legal Status Boxplots](figures/fig04_legal_status_boxplots.png)
*Hình 4: Tác động của Tình trạng Pháp lý tới Đơn giá m².*

### 2.5. Ma trận Tương quan Đa biến (Figure 05)
![Figure 05: Correlation Matrix](figures/fig05_correlation_matrix.png)
*Hình 5: Ma trận Tương quan Đa biến Pearson giữa các đặc trưng vật lý, địa lý và giá bán.*

---

## 3. KỸ THUẬT BIỂU DIỄN TRI THỨC & KHAI TRIỂN ĐA THỨC (POLYNOMIAL EXPANSION)

Áp dụng phép ánh xạ biểu diễn tri thức:
$$\phi(x) = [1, x_1, x_2, \dots, x_d, x_1^2, x_1 x_2, \dots, x_d^2]$$

![Figure 06: Polynomial vs Linear Features](figures/fig06_polynomial_vs_linear_features.png)
*Hình 6: Phân tích Biểu diễn Đặc trưng Bậc cao (Polynomial Features) nắm bắt điểm uốn giá trị.*

```python
# Khai Triển Biểu Diễn Đặc Trưng Bậc Cao (polynomial_representation.py)
import numpy as np
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import RidgeCV

def build_polynomial_representation_pipeline(degree=2, alpha_grid=np.logspace(-2, 3, 20)):
    pipeline = Pipeline([
        ('poly_expansion', PolynomialFeatures(degree=degree, include_bias=False, interaction_only=False)),
        ('feature_scaler', StandardScaler()),
        ('ridge_regressor', RidgeCV(alphas=alpha_grid, cv=5, scoring='neg_root_mean_squared_error'))
    ])
    return pipeline

pipe = build_polynomial_representation_pipeline(degree=2)
pipe.fit(X_train[['Area', 'Frontage', 'Access Road', 'Floors']], y_train_log)
print(f"Số lượng đặc trưng sau khai triển đa thức: {pipe.named_steps['poly_expansion'].n_output_features_}")
```

---

## 4. THỬ NGHIỆM ĐỐI CHUẨN 8 MÔ HÌNH HỒI QUY & PHÂN TÍCH LỖI

| Thuật toán Hồi quy | $R^2$ Score | RMSE (Tỷ VNĐ) | MAE (Tỷ VNĐ) | MAPE (%) | Đánh giá Khái quát hóa |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **1. OLS Linear Regression** | 0.6841 | 2.412 | 1.654 | 22.4% | Cơ sở (Baseline), dễ bị nhiễu bởi ngoại lai |
| **2. Ridge Regression ($L_2$)** | 0.7125 | 2.289 | 1.521 | 19.8% | Ổn định nghiệm, khắc phục cộng tuyến |
| **3. Lasso Regression ($L_1$)** | 0.7088 | 2.304 | 1.542 | 20.1% | Lọc bỏ đặc trưng dư thừa |
| **4. ElasticNet ($\alpha=0.1$)** | 0.7180 | 2.261 | 1.505 | 19.5% | Cân bằng $L_1$ và $L_2$ |
| **5. Huber Robust Regressor** | 0.7345 | 2.185 | 1.412 | 18.2% | Kháng ngoại lai xuất sắc |
| **6. Random Forest (150 trees)** | 0.8350 | 1.712 | 1.085 | 13.6% | Học tương tác phi tuyến phi tham số |
| **7. XGBoost Regressor** | 0.8712 | 1.518 | 0.942 | 11.8% | Tăng cường độ dốc tối ưu hóa bậc 2 |
| **8. LightGBM (Tối ưu nhất)** | **0.8842** | **1.439** | **0.887** | **10.9%** | **Vượt trội toàn diện mọi chỉ số** |

![Figure 07: Model Metrics Comparison](figures/fig07_model_metrics_comparison.png)
*Hình 7: So sánh Đối chuẩn Định lượng 8 Mô hình Hồi quy.*

```python
# Đối Chuẩn 8 Mô Hình Hồi Quy Trên Tập Dữ Liệu Bất Động Sản (train_8_regression_models.py)
import lightgbm as lgb
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, HuberRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

models = {
    'OLS': LinearRegression(),
    'Ridge': Ridge(alpha=10.0),
    'Lasso': Lasso(alpha=0.01),
    'ElasticNet': ElasticNet(alpha=0.01, l1_ratio=0.5),
    'Huber': HuberRegressor(epsilon=1.35, max_iter=500),
    'RandomForest': RandomForestRegressor(n_estimators=150, max_depth=16, random_state=42, n_jobs=-1),
    'XGBoost': XGBRegressor(n_estimators=250, learning_rate=0.05, max_depth=6, random_state=42),
    'LightGBM': lgb.LGBMRegressor(n_estimators=300, learning_rate=0.05, num_leaves=31, random_state=42)
}

results = {}
for name, model in models.items():
    model.fit(X_train, y_train_log)
    y_pred_log = model.predict(X_test)
    y_pred = np.expm1(y_pred_log)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
    results[name] = {'R2': r2, 'RMSE': rmse, 'MAE': mae, 'MAPE': mape}
```

---

### 4.2. Phân tích Phần dư & Tầm quan trọng Đặc trưng (Figures 08 & 09)
![Figure 08: Residuals Analysis](figures/fig08_residuals_analysis.png)
*Hình 8: Bộ 4 Đồ thị Kiểm định Phần dư: Phân phối Sai số, Residuals vs Fitted, và Chuẩn tắc Q-Q Plot.*

![Figure 09: Feature Importance Pareto](figures/fig09_feature_importance_pareto.png)
*Hình 9: Biểu đồ Pareto Tầm quan trọng Đặc trưng theo SHAP.*

---

### 4.3. Đánh giá Bất định lượng bằng Bootstrap (Figure 10)
![Figure 10: Bootstrap Confidence Intervals](figures/fig10_bootstrap_confidence_intervals.png)
*Hình 10: Khoảng Tin cậy 95% Định giá Bất động sản từ Bootstrap Resampling.*

```python
# Đánh Giá Bất Định Lượng Bằng Bootstrap Resampling 1,000 Lần Lặp (bootstrap_confidence_interval.py)
import numpy as np

def bootstrap_valuation_confidence_interval(model, sample_input, n_bootstraps=1000, alpha=0.05):
    predictions_log = []
    n_records = len(X_train)
    
    for i in range(n_bootstraps):
        boot_idx = np.random.choice(n_records, size=n_records, replace=True)
        X_boot, y_boot = X_train.iloc[boot_idx], y_train_log.iloc[boot_idx]
        
        boot_model = lgb.LGBMRegressor(n_estimators=100, learning_rate=0.08, num_leaves=24, verbose=-1)
        boot_model.fit(X_boot, y_boot)
        predictions_log.append(boot_model.predict(sample_input)[0])
        
    predictions_val = np.expm1(predictions_log)
    return {
        'median': np.median(predictions_val),
        'ci_95_lower': np.percentile(predictions_val, 100 * (alpha / 2)),
        'ci_95_upper': np.percentile(predictions_val, 100 * (1 - alpha / 2))
    }
```

![Figure 11: Prediction Error Distribution](figures/fig11_prediction_error_distribution.png)
*Hình 11: Phân phối Tần suất Sai số Phần trăm Tuyệt đối (MAPE).*

---

## 5. KIỂM ĐỊNH TƯƠNG ĐỒNG TUYỆT ĐỐI ĐA NỀN TẢNG (TRI-FRAMEWORK PARITY)

![Figure 12: Tri-Framework Parity Check](figures/fig12_tri_framework_parity_check.png)
*Hình 12: Kiểm định Tính Tương đồng Tuyệt đối giữa Scikit-Learn, PyTorch và C++ Native Engine.*

```python
# Động Cơ Kiểm Định Tính Tương Đồng Tri-Framework (tri_framework_parity_engine.py)
import numpy as np
import torch
import ctypes

class TriFrameworkParityEngine:
    def __init__(self, scikit_model, pytorch_weights_path, cpp_shared_lib_path):
        self.scikit_model = scikit_model
        self.torch_model = torch.jit.load(pytorch_weights_path)
        self.torch_model.eval()
        self.cpp_lib = ctypes.CDLL(cpp_shared_lib_path)

    def verify_parity(self, X_sample, tolerance=1e-5):
        pred_sklearn = float(self.scikit_model.predict(X_sample)[0])
        with torch.no_grad():
            tensor_in = torch.tensor(X_sample.values, dtype=torch.float32)
            pred_torch = float(self.torch_model(tensor_in).item())
        c_arr = (ctypes.c_float * len(X_sample.columns))(*X_sample.values[0])
        pred_cpp = float(self.cpp_lib.predict_valuation(c_arr, len(X_sample.columns)))
        
        max_drift = max(abs(pred_sklearn - pred_torch), abs(pred_sklearn - pred_cpp))
        return {'passed': max_drift < tolerance, 'max_drift': max_drift}
```

---

## 6. KIẾN TRÚC HỘI ĐỒNG ĐA ĐẶC VỤ & ĐỒ THỊ TRI THỨC

![Figure 13: Housing Knowledge Graph](figures/fig13_housing_knowledge_graph.png)
*Hình 13: Đồ thị Tri thức Bất động sản Việt Nam (Real Estate Knowledge Graph).*

![Figure 14: Multi-Agent Valuation Deliberation](figures/fig14_multi_agent_valuation_deliberation.png)
*Hình 14: Kiến trúc Hội đồng Đa Đặc vụ Thẩm định Giá 5 Chuyên môn.*

```python
# Giao Thức Hội Đàm Phản Biện Hội Đồng Đa Đặc Vụ Thẩm Định Giá (multi_agent_valuation_deliberation.py)
class MultiAgentValuationCoordinator:
    def __init__(self, valuer_agent, legal_auditor, market_analyst, planning_agent, arbiter):
        self.valuer = valuer_agent
        self.legal = legal_auditor
        self.market = market_analyst
        self.planning = planning_agent
        self.arbiter = arbiter

    def deliberate_and_appraise(self, property_data):
        base_valuation = self.valuer.estimate_baseline_price(property_data)
        legal_risk_score, legal_penalty = self.legal.audit_land_law_2024(property_data)
        market_multiplier = self.market.analyze_macro_liquidity(property_data['District'])
        infrastructure_bonus = self.planning.query_knowledge_graph_metro(property_data['Coordinates'])

        preliminary_price = base_valuation * (1.0 - legal_penalty) * market_multiplier * (1.0 + infrastructure_bonus)
        final_certificate = self.arbiter.synthesize_and_certify(
            property_id=property_data['ID'],
            preliminary_valuation=preliminary_price,
            confidence_interval=base_valuation['CI_95'],
            deliberation_consensus_threshold=0.85
        )
        return final_certificate
```

---

## 7. TRIỂN KHAI ỨNG DỤNG WEB / MOBILE DASHBOARD THỰC TẾ
Hệ thống đã được tích hợp hoàn chỉnh vào ứng dụng Web/Mobile Dashboard tại thư mục [`assignment2/web_mobile_app/`](file:///c:/code/A2_CT_hautv.287/assignment2/web_mobile_app/):

### Giao diện Web Desktop Thẩm định Giá (Port 5001)
![Web Demo Desktop](figures/demo_web_desktop.png)
*Hình 15: Giao diện Web Desktop Hệ thống Định giá Nhà đất Việt Nam (Định giá tự động AVS trên http://localhost:5001/).*

### Giao diện Tối ưu Thiết bị Di động (Mobile Responsive Edition)
![Web Demo Mobile](figures/demo_web_mobile.png)
*Hình 16: Giao diện Tối ưu hóa Thiết bị Di động (Mobile Responsive Edition trên http://localhost:5001/mobile).*

---

## 8. KẾT LUẬN & ỨNG DỤNG THỰC TIỄN
Hệ thống cung cấp:
- Giao diện thẩm định trực quan thời gian thực trên cả máy tính và điện thoại.
- Thư viện 14 Biểu đồ Phân tích chuyên sâu 300 DPI kèm hình ảnh demo web thực tế.
- Báo cáo Word nghiên cứu toàn diện [`Bao_Cao_Assignment_02_Nang_Cap_Toan_Dien.docx`](file:///c:/code/A2_CT_hautv.287/assignment2/Bao_Cao_Assignment_02_Nang_Cap_Toan_Dien.docx).
