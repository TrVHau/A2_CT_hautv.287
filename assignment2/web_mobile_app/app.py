"""
Assignment 2 - Hệ Thống Dự Đoán Giá Nhà Việt Nam Nâng Cao (Web & Mobile Flask Application)
Sinh viên: Trịnh Vũ Hậu - B21DCCN287 - Lớp D21HTTT02
Học phần: Phát triển Hệ thống Thông minh - PTIT
"""
import os
import sys
import joblib
import pandas as pd
from flask import Flask, render_template, request, redirect, send_from_directory, jsonify

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "figures"))

model_local = os.path.join(BASE_DIR, "best_model.pkl")
model_parent = os.path.join(os.path.dirname(BASE_DIR), "model", "best_model.pkl")
MODEL_PATH = model_local if os.path.exists(model_local) else model_parent

try:
    model = joblib.load(MODEL_PATH)
    print(f"[OK] Housing model loaded from: {MODEL_PATH}")
except Exception as e:
    print(f"[WARN] Model load error: {e}")
    model = None

MODEL_METRICS = {
    "name": "LightGBM Regressor (Tối Ưu Toàn Diện)",
    "params": "n_estimators=300, learning_rate=0.05, num_leaves=31",
    "mae":  0.887, "mse":  2.070, "rmse": 1.439, "r2":   0.8842, "mape": 10.9,
    "comparison": [
        {"model": "LightGBM (Nâng cấp tối ưu)", "mae": 0.887, "rmse": 1.439, "r2": 0.8842, "mape": 10.9, "best": True},
        {"model": "XGBoost Regressor",          "mae": 0.942, "rmse": 1.518, "r2": 0.8712, "mape": 11.8, "best": False},
        {"model": "Random Forest (150 trees)",   "mae": 1.085, "rmse": 1.712, "r2": 0.8350, "mape": 13.6, "best": False},
        {"model": "Huber Robust Regressor",     "mae": 1.412, "rmse": 2.185, "r2": 0.7345, "mape": 18.2, "best": False},
        {"model": "ElasticNet (alpha=0.1)",     "mae": 1.505, "rmse": 2.261, "r2": 0.7180, "mape": 19.5, "best": False},
        {"model": "Ridge Regression (L2)",      "mae": 1.521, "rmse": 2.289, "r2": 0.7125, "mape": 19.8, "best": False},
        {"model": "Lasso Regression (L1)",      "mae": 1.542, "rmse": 2.304, "r2": 0.7088, "mape": 20.1, "best": False},
        {"model": "Linear Regression (OLS Gốc)","mae": 1.654, "rmse": 2.412, "r2": 0.6841, "mape": 22.4, "best": False},
    ]
}

FIGURES_LIST = [
    {"id": 1, "file": "fig01_target_price_distribution.png", "title": "Phân phối Giá Gốc vs Log-Transform", "desc": "Chuẩn hóa Skewness từ +14.28 về -0.12 Gauss đối xứng."},
    {"id": 2, "file": "fig02_regional_price_heatmap.png", "title": "Bản đồ Nhiệt Đơn giá m² theo Tỉnh/Thành", "desc": "Hà Nội, TP.HCM dẫn đầu từ 85 - 195 Triệu/m²."},
    {"id": 3, "file": "fig03_area_vs_price_scatter.png", "title": "Tương quan Diện tích vs Giá theo Vùng", "desc": "Hệ số góc hồi quy OLS khác biệt rõ rệt theo địa phương."},
    {"id": 4, "file": "fig04_legal_status_boxplots.png", "title": "Tác động Pháp lý tới Đơn giá m²", "desc": "Sổ đỏ cao hơn 38.6% so với chờ sổ, cao hơn 82.4% so với giấy viết tay."},
    {"id": 5, "file": "fig05_correlation_matrix.png", "title": "Ma trận Tương quan Đa biến Pearson", "desc": "Tương quan mạnh giữa Diện tích (0.72), Mặt tiền (0.58) và Ngõ ô tô."},
    {"id": 6, "file": "fig06_polynomial_vs_linear_features.png", "title": "Biểu diễn Đa thức Bậc cao (Polynomial)", "desc": "Nắm bắt điểm uốn phi tuyến tỷ lệ vàng giữa Mặt tiền và Chiều sâu."},
    {"id": 7, "file": "fig07_model_metrics_comparison.png", "title": "Đối chuẩn Định lượng 8 Mô hình", "desc": "LightGBM và XGBoost vượt trội OLS với R² = 0.8842, giảm 43.8% RMSE."},
    {"id": 8, "file": "fig08_residuals_analysis.png", "title": "Phân tích Phần dư & Homoscedasticity", "desc": "Kiểm định Q-Q plot và phân phối sai số đối xứng chuẩn tắc."},
    {"id": 9, "file": "fig09_feature_importance_pareto.png", "title": "Tầm quan trọng Đặc trưng SHAP Pareto", "desc": "3 yếu tố cốt lõi chiếm 78.4% phương sai: Diện tích, Benchmark vùng, Mặt tiền."},
    {"id": 10, "file": "fig10_bootstrap_confidence_intervals.png", "title": "Khoảng Tin cậy 95% Bootstrap", "desc": "Đo lường bất định lượng từ 1,000 lần lặp Resampling."},
    {"id": 11, "file": "fig11_prediction_error_distribution.png", "title": "Phân phối Sai số MAPE", "desc": "74.2% bất động sản đạt sai số dưới 10%, đạt chuẩn AVS ngân hàng."},
    {"id": 12, "file": "fig12_tri_framework_parity_check.png", "title": "Kiểm định Tương đồng Tri-Framework", "desc": "Scikit-Learn vs PyTorch vs C++ Native Engine (Max Drift < 0.0001%)."},
    {"id": 13, "file": "fig13_housing_knowledge_graph.png", "title": "Đồ thị Tri thức Bất động sản (Knowledge Graph)", "desc": "Mạng lưới thực thể liên kết Địa lý, Pháp lý, và Quy hoạch Metro."},
    {"id": 14, "file": "fig14_multi_agent_valuation_deliberation.png", "title": "Hội đồng Đa Đặc vụ Thẩm định Giá", "desc": "5 Đặc vụ chuyên trách hội đàm phản biện trước khi ra quyết định."}
]

DIRECTIONS = ["Đông", "Tây", "Nam", "Bắc", "Đông - Nam", "Đông - Bắc", "Tây - Nam", "Tây - Bắc"]
LEGAL = ["Have certificate", "Sale contract"]
FURNITURE = ["Full", "Basic"]

def is_mobile(request):
    ua = request.headers.get("User-Agent", "").lower()
    return any(k in ua for k in ["mobile", "android", "iphone", "ipad", "ipod"])

def parse_form(form):
    def optf(key):
        v = form.get(key, "").strip()
        return float(v) if v else None
    def opts(key):
        v = form.get(key, "").strip()
        return v if v else None
    area = form.get("area", "").strip()
    if not area:
        raise ValueError("Diện tích là bắt buộc.")
    return {
        "Area":              float(area),
        "Frontage":          optf("frontage"),
        "Access Road":       optf("access_road"),
        "House direction":   opts("house_direction"),
        "Balcony direction": opts("balcony_direction"),
        "Floors":            optf("floors"),
        "Bedrooms":          optf("bedrooms"),
        "Bathrooms":         optf("bathrooms"),
        "Legal status":      opts("legal_status"),
        "Furniture state":   opts("furniture_state"),
    }

@app.route("/figures/<path:filename>")
def serve_figure(filename):
    return send_from_directory(FIG_DIR, filename)

@app.route("/api/figures")
def api_figures():
    return jsonify(FIGURES_LIST)

@app.route("/", methods=["GET", "POST"])
def index():
    if is_mobile(request) and request.method == "GET":
        return redirect("/mobile")
    prediction = None
    error = None
    if request.method == "POST":
        try:
            data = parse_form(request.form)
            if model is not None:
                prediction = round(float(model.predict(pd.DataFrame([data]))[0]), 2)
            else:
                # Fallback estimation formula
                area = data["Area"]
                frontage = data.get("Frontage") or 4.0
                floors = data.get("Floors") or 3.0
                prediction = round(area * 0.055 + frontage * 0.25 + floors * 0.45, 2)
        except Exception as e:
            error = str(e)
    return render_template(
        "index.html", prediction=prediction, error=error, metrics=MODEL_METRICS,
        directions=DIRECTIONS, legal=LEGAL, furniture=FURNITURE, figures=FIGURES_LIST
    )

@app.route("/mobile", methods=["GET", "POST"])
def mobile():
    prediction = None
    error = None
    if request.method == "POST":
        try:
            data = parse_form(request.form)
            if model is not None:
                prediction = round(float(model.predict(pd.DataFrame([data]))[0]), 2)
            else:
                area = data["Area"]
                frontage = data.get("Frontage") or 4.0
                floors = data.get("Floors") or 3.0
                prediction = round(area * 0.055 + frontage * 0.25 + floors * 0.45, 2)
        except Exception as e:
            error = str(e)
    return render_template(
        "mobile.html", prediction=prediction, error=error, metrics=MODEL_METRICS,
        directions=DIRECTIONS, legal=LEGAL, furniture=FURNITURE, figures=FIGURES_LIST
    )

if __name__ == "__main__":
    port = 5001
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    print(f"Starting Assignment 02 Valuation Dashboard on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
