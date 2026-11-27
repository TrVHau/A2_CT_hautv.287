"""
Assignment 1 - Hệ Thống Chẩn Đoán Bệnh Tiểu Đường (Flask Web Application)
Sinh viên: Trần Văn Hậu - B23DCCN287 - Lớp D23CTPM01
"""
import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from flask import Flask, render_template, request, jsonify

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "diabetes_model.pkl"
NEO4J_DIR  = BASE_DIR / "neo4j"

if NEO4J_DIR.exists():
    sys.path.insert(0, str(NEO4J_DIR))

app = Flask(__name__)

model = None
def load_model():
    global model
    if MODEL_PATH.exists():
        model = joblib.load(MODEL_PATH)
        print(f"[OK] Diabetes model loaded from: {MODEL_PATH}")
    else:
        print(f"[WARN] Model not found at: {MODEL_PATH}")

load_model()

FEATURES = [
    "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
    "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"
]

FEATURE_LABELS = {
    "Pregnancies": "Số lần mang thai",
    "Glucose": "Nồng độ Glucose (mg/dL)",
    "BloodPressure": "Huyết áp tâm trương (mm Hg)",
    "SkinThickness": "Độ dày nếp gấp da (mm)",
    "Insulin": "Insulin huyết thanh (μU/mL)",
    "BMI": "Chỉ số khối cơ thể (BMI)",
    "DiabetesPedigreeFunction": "Hệ số phả hệ tiểu đường",
    "Age": "Tuổi"
}

FEATURE_RANGES = {
    "Pregnancies": (0, 20),
    "Glucose": (0, 300),
    "BloodPressure": (0, 200),
    "SkinThickness": (0, 100),
    "Insulin": (0, 900),
    "BMI": (0.0, 70.0),
    "DiabetesPedigreeFunction": (0.0, 3.0),
    "Age": (1, 120),
}

def get_static_advice(prediction, probability, input_data):
    if prediction == 1:
        risk_level = "very_high" if probability >= 0.75 else "high"
        risk_label = "Nguy cơ rất cao" if probability >= 0.75 else "Nguy cơ cao"
        risk_color = "#dc2626" if probability >= 0.75 else "#ea580c"
        lifestyle = [
            "Đến cơ sở y tế chuyên khoa nội tiết để xét nghiệm HbA1c và đường huyết lúc đói.",
            "Tự theo dõi đường huyết tại nhà 2-3 lần/tuần trước và sau bữa ăn.",
            "Duy trì giấc ngủ 7-8 tiếng/đêm; tránh căng thẳng kéo dài."
        ]
        diet = [
            "Hạn chế tối đa tinh bột chuyển hóa nhanh: đường kính, nước ngọt, bánh kẹo.",
            "Tăng cường chất xơ hòa tan: rau xanh đậm, yến mạch, các loại đậu.",
            "Chia nhỏ khẩu phần thành 5-6 bữa/ngày."
        ]
        exercise = [
            "Đi bộ nhanh hoặc đạp xe tối thiểu 30 phút/ngày, 5 ngày/tuần.",
            "Kết hợp các bài tập kháng lực nhẹ 2 lần/tuần."
        ]
        medical_tests = [
            {"test": "Xét nghiệm HbA1c", "reason": "Đánh giá mức kiểm soát đường huyết 3 tháng qua", "urgency": "Cần làm ngay"},
            {"test": "Đường huyết lúc đói (FPG)", "reason": "Xác nhận chẩn đoán theo tiêu chuẩn ADA", "urgency": "Cần làm ngay"}
        ]
    else:
        risk_level = "moderate" if probability >= 0.35 else "low"
        risk_label = "Nguy cơ trung bình (Tiền tiểu đường)" if probability >= 0.35 else "Nguy cơ thấp"
        risk_color = "#ca8a04" if probability >= 0.35 else "#16a34a"
        lifestyle = ["Khám sức khỏe tổng quát định kỳ mỗi năm một lần.", "Duy trì lối sống lành mạnh."]
        diet = ["Chế độ dinh dưỡng cân đối: đủ protein, chất béo tốt và vitamin."]
        exercise = ["Duy trì hoạt động thể lực đều đặn ít nhất 30 phút mỗi ngày."]
        medical_tests = [{"test": "Khám sức khỏe tổng quát", "reason": "Theo dõi sức khỏe chung", "urgency": "1 năm/lần"}]

    return {
        "risk_level": risk_level, "risk_label": risk_label, "risk_color": risk_color,
        "lifestyle": lifestyle, "diet": diet, "exercise": exercise, "medical_tests": medical_tests
    }

@app.route("/")
def index():
    return render_template("index.html", features=FEATURES, labels=FEATURE_LABELS, ranges=FEATURE_RANGES)

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Mô hình chưa sẵn sàng."}), 500
    try:
        data = request.get_json(force=True)
        input_data = {feat: float(data[feat]) for feat in FEATURES}
        df_input = pd.DataFrame([input_data])[FEATURES]

        prediction = int(model.predict(df_input)[0])
        probability = float(model.predict_proba(df_input)[0][1])
        advice = get_static_advice(prediction, probability, input_data)

        return jsonify({
            "success": True,
            "prediction": prediction,
            "probability": round(probability * 100, 1),
            "result_text": "Dương tính (Có nguy cơ cao)" if prediction == 1 else "Âm tính (Nguy cơ thấp)",
            "risk_label": advice["risk_label"],
            "risk_color": advice["risk_color"],
            "advice": advice
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    port = 5000
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    print("\n" + "="*56)
    print(f"  [HEALTH] Assignment 1 - Hệ Chẩn Đoán Bệnh Tiểu Đường")
    print(f"  URL: http://localhost:{port}")
    print("="*56 + "\n")
    app.run(host="0.0.0.0", port=port, debug=True)
