#!/usr/bin/env python3
"""
Agent 1: Triage & Metabolic Screening Specialist (DiaTriage-Agent)
Assesses patient's initial risk based on 8 features against ADA 2024 diagnostic thresholds.
"""

class TriageRiskAgent:
    def __init__(self, name: str = "DiaTriage-Agent (Tác Tử Tiếp Đón & Phân Tầng Lâm Sàng)"):
        self.name = name

    def evaluate(self, patient: dict) -> dict:
        hba1c = float(patient.get("HbA1c_level", 5.5))
        glucose = float(patient.get("blood_glucose_level", 95))
        bmi = float(patient.get("bmi", 24.0))
        hypertension = int(patient.get("hypertension", 0))
        heart_disease = int(patient.get("heart_disease", 0))
        smoking = str(patient.get("smoking_history", "never")).lower()
        age = float(patient.get("age", 45))

        red_flags = []
        warnings = []

        # Red flags
        if glucose >= 250.0:
            red_flags.append(f"Đường huyết nguy cấp ({glucose} mg/dL): Nguy cơ ngộ độc đường cấp hoặc mất nước ưu trương!")
        if hba1c >= 10.0:
            red_flags.append(f"HbA1c mức báo động ({hba1c}%): Tế bào beta tụy suy kiệt nghiêm trọng.")
        if heart_disease == 1 and hypertension == 1:
            red_flags.append("Tổ hợp bệnh tim mạch xơ vữa + Tăng huyết áp: Nguy cơ biến cố mạch vành cấp rất cao.")

        # Warnings
        if 180.0 <= glucose < 250.0:
            warnings.append(f"Tăng đường huyết rõ rệt ({glucose} mg/dL).")
        if 6.5 <= hba1c < 10.0:
            warnings.append(f"HbA1c ({hba1c}%) vượt ngưỡng chẩn đoán Đái tháo đường ADA (>=6.5%).")
        elif 5.7 <= hba1c <= 6.4:
            warnings.append(f"HbA1c ({hba1c}%) thuộc phân nhóm Tiền đái tháo đường.")
        if bmi >= 28.0:
            warnings.append(f"Chỉ số khối cơ thể BMI = {bmi} kg/m² (Thừa cân / Béo phì), thúc đẩy đề kháng insulin.")
        if smoking in ["current", "ever"]:
            warnings.append(f"Tiền sử hút thuốc lá ({smoking}) gây tổn thương tế bào nội mô mạch máu.")

        # Triage priority classification
        if red_flags:
            priority = "CẤP ĐỘ 1: BÁO ĐỘNG ĐỎ / NGUY CƠ BIẾN CHỨNG CẤP TÍNH"
            badge = "danger"
        elif len(warnings) >= 2 or hba1c >= 6.5 or glucose >= 140.0:
            priority = "CẤP ĐỘ 2: ƯU TIÊN HỘI CHẨN CHUYÊN KHOA ĐTĐ"
            badge = "warning"
        elif 5.7 <= hba1c <= 6.4 or 100 <= glucose <= 125:
            priority = "CẤP ĐỘ 3: THEO DÕI TIỀN ĐTĐ & CAN THIỆP LỐI SỐNG"
            badge = "info"
        else:
            priority = "CẤP ĐỘ 4: CHUYỂN HÓA KHỎE MẠNH / TẦM SOÁT ĐỊNH KỲ"
            badge = "success"

        msg = (
            f"Tôi là {self.name}.\n"
            f"Đã tiếp nhận hồ sơ bệnh nhân ({age} tuổi, giới tính {patient.get('gender', 'Khác')}):\n"
            f"• Phân loại ưu tiên: {priority}\n"
            f"• Các dấu hiệu cảnh báo ghi nhận: {', '.join(red_flags + warnings) if (red_flags + warnings) else 'Không phát hiện bất thường'}.\n"
            f"• Chuyển hồ sơ sang DiaDiagnostic-Agent để chạy toàn bộ 7 mô hình định lượng."
        )

        return {
            "agent": self.name,
            "priority": priority,
            "badge": badge,
            "red_flags": red_flags,
            "warnings": warnings,
            "message": msg
        }
