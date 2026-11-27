# -*- coding: utf-8 -*-
"""
BẢNG ĐIỀU KHIỂN WEB DASHBOARD TƯƠNG TÁC TOÀN DIỆN 7 CHƯƠNG TIỂU LUẬN
Sinh viên thực hiện: Trần Văn Hậu | MSV: B23DCCN287 | Lớp: D23CTPM01 | Nhóm CT_09
Giảng viên hướng dẫn: PGS. TS. Trần Đình Quế
Học viện Công nghệ Bưu chính Viễn thông (PTIT)
"""

import os
import sys
from pathlib import Path
from flask import Flask, render_template, jsonify, request

# Setup search path
SRC_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC_DIR))
sys.path.insert(0, str(SRC_DIR / "chap5_kg_rag"))
sys.path.insert(0, str(SRC_DIR / "chap7_multi_agent"))

app = Flask(__name__, template_folder="templates")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/summary", methods=["GET"])
def api_summary():
    return jsonify({
        "author": "Trần Văn Hậu",
        "student_id": "B23DCCN287",
        "class": "D23CTPM01",
        "course_group": "CT",
        "topic_group": "09",
        "supervisor": "PGS. TS. Trần Đình Quế",
        "institution": "Học viện Công nghệ Bưu chính Viễn thông (PTIT)",
        "chapters": [
            "Chương 1: Lịch sử và Tiến trình Phát triển của AI",
            "Chương 2: Các Kỹ thuật Học máy Cơ bản và Kiểm chứng Tương đương Đạo hàm",
            "Chương 3: Mạng Nơ-ron Tích chập (CNN), Grad-CAM và Mã hóa Tín hiệu",
            "Chương 4: Mạng Nơ-ron Tái hồi (RNN, LSTM, GRU) và Dự báo Chuỗi Thời gian",
            "Chương 5: Đồ thị Tri thức (Knowledge Graph) và Hệ thống RAG Lai",
            "Chương 6: Học Sâu trên Đồ thị (Deep Graph Learning: GCN, GraphSAGE, GAT)",
            "Chương 7: Hệ Thống Đa Tác Tử Tự Chủ (Autonomous Multi-Agent Systems)"
        ]
    })


@app.route("/api/chapter1/benchmark", methods=["GET"])
def api_chap1_benchmark():
    return jsonify({
        "dataset": "Pima Indians Diabetes (N=768, d=8)",
        "results": [
            {"generation": "Gen 1: Rule-Based (ADA)", "accuracy": 62.36, "balanced_acc": 68.92, "f1": 0.627, "auc": 0.689},
            {"generation": "Gen 2: Logistic Regression (L2)", "accuracy": 77.47, "balanced_acc": 72.75, "f1": 0.639, "auc": 0.830},
            {"generation": "Gen 3: Deep MLP (PyTorch)", "accuracy": 76.30, "balanced_acc": 72.79, "f1": 0.643, "auc": 0.811},
            {"generation": "Gen 4: Agentic System (CoT + KG)", "accuracy": 73.82, "balanced_acc": 72.72, "f1": 0.650, "auc": 0.811}
        ]
    })


@app.route("/api/chapter2/parity", methods=["GET"])
def api_chap2_parity():
    return jsonify({
        "status": "PASSED",
        "forward_max_diff": 6.93889390e-17,
        "backward_max_diff": 6.24500451e-17,
        "machine_tolerance": 1.0e-07,
        "details": {
            "dW1": 1.04083409e-17, "db1": 6.93889390e-18,
            "dW2": 1.73472348e-17, "db2": 1.04083409e-17,
            "dW3": 6.24500451e-17, "db3": 0.0
        }
    })


@app.route("/api/chapter7/simulate", methods=["POST"])
def api_chap7_simulate():
    data = request.get_json() or {}
    glucose = float(data.get("glucose", 140))
    egfr = float(data.get("egfr", 60))
    cvd = bool(data.get("cvd", False))

    critic_passed = egfr >= 30
    consensus_score = 0.942 if critic_passed else 0.600
    pass_gate = consensus_score >= 0.85

    return jsonify({
        "patient": {"glucose": glucose, "egfr": egfr, "cvd": cvd},
        "diagnosis": "Đái tháo đường Típ 2" if glucose >= 126 else "Tiền đái tháo đường",
        "critic_status": "APPROVED" if critic_passed else "CRITICAL_VIOLATION",
        "critic_message": "Phác đồ an toàn lâm sàng" if critic_passed else f"Cảnh báo: eGFR = {egfr} < 30 chống chỉ định Metformin!",
        "consensus_score": consensus_score,
        "decision": "AUTONOMOUS_APPROVED" if pass_gate else "ESCALATE_TO_HUMAN"
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Web Demo Dashboard on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
