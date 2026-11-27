#!/usr/bin/env python3
"""
Clinical Safety & Absolute Guardrails Agent (DiaSafetyRuleAgent)
Implements 12 Deterministic Medical Safety Rules (R1 - R12) based on ADA 2024 / KDIGO / WHO standards.
Acts as an unbypassable, prioritized safety layer independent of machine learning predictions.
"""

class DiaSafetyRuleAgent:
    """Tác Tử Hộ Lý An Toàn Tuyệt Đối (Deterministic Clinical Guardrails)"""
    def __init__(self):
        self.name = "DiaSafetyRule-Agent (Tác Tử Giám Sát An Toàn Tuyệt Đối & Cảnh Báo Khẩn)"

    def evaluate_safety_rules(self, patient: dict, ai_res: dict = None) -> dict:
        glucose = float(patient.get("blood_glucose_level", 95.0))
        hba1c = float(patient.get("HbA1c_level", 5.5))
        bmi = float(patient.get("bmi", 24.5))
        age = float(patient.get("age", 45.0))
        heart_disease = int(patient.get("heart_disease", 0))
        hypertension = int(patient.get("hypertension", 0))
        egfr = float(patient.get("egfr", 85.0))
        symptoms = [s.strip().lower() for s in str(patient.get("symptoms", "")).split(",") if s.strip()]

        triggered_rules = []

        # R1: Nguy cấp tăng áp lực thẩm thấu / hôn mê tăng đường huyết
        if glucose >= 250.0:
            triggered_rules.append({
                "rule_id": "R01",
                "level": "DANGER (CẤP CỨU)",
                "condition": f"Đường huyết đo được {glucose} mg/dL >= 250 mg/dL",
                "guideline": "ADA 2024 / NIDDK",
                "action": "Chỉ định cấp cứu ngay lập tức. Nguy cơ toan ceton (DKA) hoặc tăng áp lực thẩm thấu (HHS). Không trì hoãn tại phòng khám ngoại trú."
            })

        # R2: Tăng đường huyết nặng kèm triệu chứng mất nước
        if glucose >= 200.0 and len(symptoms) >= 2:
            triggered_rules.append({
                "rule_id": "R02",
                "level": "DANGER (CẤP CỨU)",
                "condition": f"Đường huyết {glucose} mg/dL >= 200 mg/dL kèm {len(symptoms)} triệu chứng rầm rộ",
                "guideline": "ADA Standards of Care",
                "action": "Cảnh báo khẩn cấp: Đủ tiêu chuẩn chẩn đoán đái tháo đường lâm sàng có triệu chứng, cần kiểm tra ngay ceton máu/niệu."
            })

        # R3: Hạ đường huyết nguy hiểm
        if glucose < 70.0:
            triggered_rules.append({
                "rule_id": "R03",
                "level": "DANGER (CẤP CỨU HẠ ĐƯỜNG HUYẾT)",
                "condition": f"Đường huyết {glucose} mg/dL < 70 mg/dL",
                "guideline": "Quy tắc 15-15 của ADA",
                "action": "Khẩn cấp: Uống ngay 15g carbohydrate hấp thu nhanh (1/2 ly nước trái cây hoặc 3 viên đường), đo lại sau 15 phút. Nguy cơ hôn mê hạ đường huyết!"
            })

        # R4: Đường huyết đói vượt ngưỡng chẩn đoán ĐTĐ
        if glucose >= 126.0:
            triggered_rules.append({
                "rule_id": "R04",
                "level": "WARNING (LƯU Ý LÂM SÀNG)",
                "condition": f"Đường huyết lúc đói {glucose} mg/dL >= 126 mg/dL",
                "guideline": "Tiêu chuẩn vàng ADA/WHO",
                "action": "Chỉ định làm lại xét nghiệm FPG lần 2 hoặc định lượng HbA1c để chính thức xác lập chẩn đoán ĐTĐ Tuýp 2."
            })

        # R5: Vùng Tiền đái tháo đường
        if 100.0 <= glucose < 126.0 or (5.7 <= hba1c <= 6.4):
            triggered_rules.append({
                "rule_id": "R05",
                "level": "WARNING (VÙNG TIỀN ĐÁI THÁO ĐƯỜNG)",
                "condition": f"Glucose {glucose} mg/dL (100-125) hoặc HbA1c {hba1c}% (5.7-6.4%)",
                "guideline": "ADA Prevention Guidelines",
                "action": "Can thiệp lối sống tích cực (giảm 7% cân nặng, 150 phút vận động/tuần). Cân nhắc Metformin phòng ngừa nếu BMI >= 35."
            })

        # R6: Chống chỉ định suy thận nặng đối với Metformin
        if egfr < 30.0:
            triggered_rules.append({
                "rule_id": "R06",
                "level": "CRITICAL CONTRAINDICATION (CHỐNG CHỈ ĐỊNH)",
                "condition": f"Độ lọc cầu thận eGFR = {egfr} mL/phút/1.73m2 < 30",
                "guideline": "KDIGO 2023 / FDA Black Box Warning",
                "action": "CHỐNG CHỈ ĐỊNH TUYỆT ĐỐI Metformin do nguy cơ nhiễm toan lactic tử vong. Chuyển sang Insulin hoặc ức chế DPP-4 chỉnh liều thận."
            })

        # R7: Bệnh tim mạch xơ vữa kèm đái tháo đường
        if (heart_disease == 1 or hypertension == 1) and (hba1c >= 6.5 or glucose >= 126.0):
            triggered_rules.append({
                "rule_id": "R07",
                "level": "WARNING (BẢO VỆ CƠ QUAN ĐÍCH)",
                "condition": "Đái tháo đường kèm tiền sử Tim mạch / Tăng huyết áp",
                "guideline": "ADA / ACC / ESC 2024",
                "action": "Bắt buộc phối hợp SGLT2i (Empagliflozin/Dapagliflozin) hoặc GLP-1 RA có chứng cứ bảo vệ tim mạch bất kể mức HbA1c."
            })

        # R8: Cảnh báo bệnh nhân cao tuổi phòng hạ đường huyết
        if age >= 70.0:
            triggered_rules.append({
                "rule_id": "R08",
                "level": "CAUTION (CẢNH BÁO CAO TUỔI)",
                "condition": f"Tuổi {age} >= 70 tuổi",
                "guideline": "Hiệp hội Lão khoa Hoa Kỳ (AGS Beers Criteria)",
                "action": "Tránh các thuốc kích thích tiết insulin kéo dài (Sulfonylurea). Nới lỏng mục tiêu HbA1c lên 7.0 - 7.5%."
            })

        # R9: Béo phì độ II trở lên
        if bmi >= 35.0:
            triggered_rules.append({
                "rule_id": "R09",
                "level": "WARNING (BÉO PHÌ NGUY CƠ CAO)",
                "condition": f"BMI {bmi} kg/m2 >= 35.0",
                "guideline": "ADA Obesity Management",
                "action": "Khuyến nghị ưu tiên các nhóm thuốc đồng vận thụ thể GLP-1 (Semaglutide/Tirzepatide) giúp giảm cân mạnh mẽ và cải thiện đề kháng insulin."
            })

        # R10: Đa triệu chứng điển hình (4P)
        if len(symptoms) >= 3:
            triggered_rules.append({
                "rule_id": "R10",
                "level": "WARNING (HỘI CHỨNG 4P)",
                "condition": f"Xuất hiện {len(symptoms)} triệu chứng (Ăn nhiều, uống nhiều, tiểu nhiều, sụt cân)",
                "guideline": "Triệu chứng học lâm sàng NIDDK",
                "action": "Chỉ định tầm soát biến chứng vi mạch: Soi đáy mắt, điện tim ECG, microalbumin niệu."
            })

        # R11: Tầm soát định kỳ người trưởng thành
        if age >= 35.0 and (glucose < 100 and hba1c < 5.7):
            triggered_rules.append({
                "rule_id": "R11",
                "level": "INFO (TẦM SOÁT ĐỊNH KỲ)",
                "condition": f"Tuổi {age} >= 35 với chỉ số bình thường",
                "guideline": "USPSTF / ADA Recommendation",
                "action": "Thực hiện tầm soát định kỳ xét nghiệm đường huyết mỗi 3 năm một lần."
            })

        # R12: Bất đồng giữa AI và lâm sàng thực tế (Safety Override)
        if ai_res and ai_res.get("consensus_probability", 0.0) < 0.30 and (glucose >= 126.0 or hba1c >= 6.5):
            triggered_rules.append({
                "rule_id": "R12",
                "level": "CRITICAL OVERRIDE (PHỦ QUYẾT BẢO VỆ)",
                "condition": f"Xác suất AI báo thấp ({ai_res.get('consensus_probability', 0):.1%}) nhưng chỉ số sinh học vượt ngưỡng (Glucose={glucose}, HbA1c={hba1c})",
                "guideline": "Nguyên tắc Pháp lý Y tế An toàn",
                "action": "PHỦ QUYẾT TOÀN DIỆN KẾT QUẢ AI: Ưu tiên tuyệt đối số liệu sinh hóa trực tiếp. Nâng mức nguy cơ lên CAO."
            })

        max_severity = "NORMAL"
        for r in triggered_rules:
            if "DANGER" in r["level"] or "CRITICAL" in r["level"]:
                max_severity = "DANGER"
                break
            elif "WARNING" in r["level"]:
                max_severity = "WARNING"
            elif max_severity == "NORMAL":
                max_severity = "INFO"

        speech = (
            f"Tôi là {self.name}.\n"
            f"✦ KIỂM TOÁN 12 QUY TẮC AN TOÀN Y KHOA TUYỆT ĐỐI:\n"
            f"  • Mức độ an toàn phân tầng: {max_severity}\n"
            f"  • Số quy tắc được kích hoạt: {len(triggered_rules)}/12 quy tắc\n"
            + "\n".join([f"  • [{r['rule_id']} - {r['level']}]: {r['condition']} -> {r['action']}" for r in triggered_rules])
        )

        return {
            "agent": self.name,
            "max_severity": max_severity,
            "triggered_rules": triggered_rules,
            "rule_count": len(triggered_rules),
            "speech": speech
        }
