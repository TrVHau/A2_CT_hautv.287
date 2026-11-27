# -*- coding: utf-8 -*-
"""
CHƯƠNG 7: HỘI ĐỒNG THAM VẤN Y TẾ ĐA TÁC TỬ (LLM MULTI-AGENT CLINICAL COUNCIL)
Sinh viên thực hiện: Trần Văn Hậu | MSV: B23DCCN287 | Lớp: D23CTPM01 | Nhóm CT_09
Giảng viên hướng dẫn: PGS. TS. Trần Đình Quế

Hội đồng gồm 5 vai trò tác tử chuyên biệt hóa sâu:
  1. DiagnosticAgent: Đánh giá triệu chứng, tiêu chuẩn chẩn đoán ADA 2024, phân tầng nguy cơ
  2. PharmacotherapyAgent: Lập phác đồ dược lý, chỉnh liều theo chức năng thận (eGFR), tương tác thuốc
  3. LifestyleNutritionAgent: Thiết kế chế độ dinh dưỡng (low-GI, chất xơ) và vận động cá thể hóa
  4. CriticSafetyAgent: Tác tử phản biện độc lập (Red-Teaming), dò tìm chống chỉ định và rủi ro hạ đường huyết
  5. ChiefMedicalOfficerAgent: Chủ tọa hội đồng, tổng hợp ý kiến, kích hoạt cổng đồng thuận và ban hành quyết định
"""

import sys
import json
from typing import Dict, Any, List

sys.stdout.reconfigure(encoding='utf-8')


class DiagnosticAgent:
    """Tác tử Chẩn đoán chuyên sâu bệnh học nội tiết."""
    def __init__(self):
        self.role = "Diagnostic Specialist"

    def analyze(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        glucose = patient_data.get("Glucose", 120)
        hba1c = patient_data.get("HbA1c", 6.5)
        bmi = patient_data.get("BMI", 25.0)

        diagnosis = "Đái tháo đường Típ 2" if (glucose >= 126 or hba1c >= 6.5) else "Tiền đái tháo đường"
        severity = "Nặng / Cần can thiệp tích cực" if (glucose > 180 or hba1c > 8.5) else "Trung bình"

        return {
            "agent": self.role,
            "diagnosis": diagnosis,
            "severity": severity,
            "confidence": 0.95 if glucose >= 126 else 0.82,
            "reasoning": f"Đường huyết lúc đói {glucose} mg/dL, HbA1c {hba1c}% thỏa mãn tiêu chuẩn chẩn đoán ADA 2024."
        }


class PharmacotherapyAgent:
    """Tác tử Dược lý lâm sàng và phác đồ thuốc."""
    def __init__(self):
        self.role = "Pharmacotherapy Specialist"

    def prescribe(self, patient_data: Dict[str, Any], diag_result: Dict[str, Any]) -> Dict[str, Any]:
        egfr = patient_data.get("eGFR", 60)
        has_cvd = patient_data.get("History_CVD", False)

        prescriptions = []
        # Kiểm tra chống chỉ định Metformin
        if egfr >= 45:
            prescriptions.append({"drug": "Metformin", "dose": "1000mg/ngày", "note": "Khởi đầu chuẩn"})
        elif egfr >= 30:
            prescriptions.append({"drug": "Metformin", "dose": "500mg/ngày", "note": "Giảm nửa liều vì eGFR suy giảm nhẹ"})
        else:
            prescriptions.append({"drug": "Insulin / DPP-4i", "dose": "Chỉnh theo đường huyết", "note": "Metformin chống chỉ định tuyệt đối do eGFR < 30"})

        # Ưu tiên bảo vệ tim mạch
        if has_cvd:
            prescriptions.append({"drug": "Empagliflozin (SGLT-2i)", "dose": "10mg/ngày", "note": "Bảo vệ tim và thận vượt trội"})

        return {
            "agent": self.role,
            "prescriptions": prescriptions,
            "confidence": 0.92,
            "reasoning": f"Chức năng thận eGFR = {egfr} mL/min, tiền sử tim mạch = {has_cvd} -> Lựa chọn thuốc bảo đảm an toàn thận."
        }


class LifestyleNutritionAgent:
    """Tác tử Dinh dưỡng và lối sống cá thể hóa."""
    def __init__(self):
        self.role = "Lifestyle & Nutrition Specialist"

    def advise(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        bmi = patient_data.get("BMI", 25.0)
        target_calories = 1500 if bmi >= 25.0 else 1800

        return {
            "agent": self.role,
            "diet_plan": {
                "target_calories": f"{target_calories} kcal/ngày",
                "macro_ratio": "Carb 45% (ưu tiên low-GI), Protein 25%, Lipid 30%",
                "fiber_target": ">= 30g/ngày"
            },
            "exercise_plan": "Đi bộ nhanh hoặc aerobic tối thiểu 150 phút/tuần, không nghỉ quá 2 ngày liên tiếp",
            "confidence": 0.88
        }


class CriticSafetyAgent:
    """Tác tử Phản biện an toàn y khoa (Red-Teaming Critic Agent)."""
    def __init__(self):
        self.role = "Critic & Safety Officer"

    def inspect(self, patient_data: Dict[str, Any], pharma_plan: Dict[str, Any]) -> Dict[str, Any]:
        egfr = patient_data.get("eGFR", 60)
        prescriptions = pharma_plan.get("prescriptions", [])
        
        flags = []
        severity = "SAFE"

        # Tấn công kiểm thử chống chỉ định Metformin
        for p in prescriptions:
            if "Metformin" in p["drug"] and egfr < 30:
                flags.append(f"VI PHẠM NGUY HIỂM: Kê đơn Metformin khi eGFR={egfr} < 30 mL/phút -> Nguy cơ nhiễm toan Lactic tử vong!")
                severity = "CRITICAL_VIOLATION"

        # Kiểm tra nguy cơ hạ đường huyết quá mức
        if any("Insulin" in p["drug"] for p in prescriptions) and any("Sulfonylurea" in p["drug"] for p in prescriptions):
            flags.append("CẢNH BÁO: Phối hợp Insulin và Sulfonylurea làm tăng vọt nguy cơ tụt đường huyết cấp cứu.")
            if severity != "CRITICAL_VIOLATION":
                severity = "HIGH_RISK"

        passed = len(flags) == 0
        return {
            "agent": self.role,
            "passed": passed,
            "severity": severity,
            "critique_flags": flags,
            "confidence": 0.98,
            "recommendation": "Phê duyệt kế hoạch" if passed else "Yêu cầu Hội đồng điều chỉnh khẩn cấp"
        }


class ChiefMedicalOfficerAgent:
    """Tác tử Chủ tọa Hội đồng (CMO) tổng hợp và ra quyết định tối hậu."""
    def __init__(self):
        self.role = "Chief Medical Officer (CMO)"

    def deliberate(self, diag, pharma, lifestyle, critic) -> Dict[str, Any]:
        if not critic["passed"]:
            status = "KẾ HOẠCH BỊ BÁC BỎ DO VI PHẠM AN TOÀN"
            final_actions = "Hội đồng yêu cầu thu hồi đơn thuốc và điều chỉnh theo cảnh báo của Critic."
        else:
            status = "KẾ HOẠCH ĐƯỢC PHÊ DUYỆT ĐỒNG THUẬN CAO"
            final_actions = f"Chẩn đoán: {diag['diagnosis']}. Điều trị: {', '.join([p['drug'] for p in pharma['prescriptions']])}. Chế độ ăn: {lifestyle['diet_plan']['target_calories']}."

        return {
            "agent": self.role,
            "status": status,
            "deliberation_summary": final_actions,
            "critic_verdict": critic["severity"]
        }


def test_council():
    print("=" * 70)
    print("KIỂM TRA HỘI ĐỒNG THAM VẤN Y TẾ 5 TÁC TỬ (CLINICAL COUNCIL)")
    print("Tác giả: Trần Văn Hậu - B23DCCN287 | Nhóm CT_09")
    print("=" * 70)

    # Ca 1: Bệnh nhân bình thường eGFR = 65
    patient1 = {"Glucose": 145, "HbA1c": 7.4, "BMI": 26.2, "eGFR": 65, "History_CVD": True}
    
    diag_ag = DiagnosticAgent()
    pharma_ag = PharmacotherapyAgent()
    life_ag = LifestyleNutritionAgent()
    critic_ag = CriticSafetyAgent()
    cmo_ag = ChiefMedicalOfficerAgent()

    d1 = diag_ag.analyze(patient1)
    p1 = pharma_ag.prescribe(patient1, d1)
    l1 = life_ag.advise(patient1)
    c1 = critic_ag.inspect(patient1, p1)
    cmo1 = cmo_ag.deliberate(d1, p1, l1, c1)

    print(f"Ca 1 Kết quả Chủ tọa: {cmo1['status']}")
    print(f"Chi tiết: {cmo1['deliberation_summary']}\n")

    # Ca 2: Bệnh nhân suy thận nặng eGFR = 22 (thử nghiệm bắt lỗi an toàn)
    patient2 = {"Glucose": 160, "HbA1c": 8.0, "BMI": 27.0, "eGFR": 22, "History_CVD": False}
    # Giả lập kê nhầm Metformin để kiểm tra Critic
    p2_faulty = {"prescriptions": [{"drug": "Metformin", "dose": "1000mg"}]}
    c2 = critic_ag.inspect(patient2, p2_faulty)
    cmo2 = cmo_ag.deliberate(d1, p2_faulty, l1, c2)

    print(f"Ca 2 Kiểm thử Red-Teaming với ca bệnh suy thận nặng:")
    print(f"Trạng thái Critic: {c2['severity']}")
    print(f"Cảnh báo bắt được: {c2['critique_flags']}")
    print(f"Phán quyết Chủ tọa: {cmo2['status']}")

    assert not c2["passed"]
    print("\nClinical Council verification PASSED!")
    print("=" * 70)


if __name__ == "__main__":
    test_council()
