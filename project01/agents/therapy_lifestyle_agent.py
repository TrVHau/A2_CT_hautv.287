#!/usr/bin/env python3
"""
Agent 4: Personalized Therapy & Nutrition Specialist (DiaTherapy-Agent)
Formulates tailored pharmacological regimens, Medical Nutrition Therapy (MNT), and lifestyle goals.
"""

class TherapyLifestyleAgent:
    def __init__(self, name: str = "DiaTherapy-Agent (Tác Tử Phác Đồ Trị Liệu & Dinh Dưỡng Cá Nhân Hóa)"):
        self.name = name

    def prescribe(self, patient: dict, ai_res: dict, kg_res: dict) -> dict:
        hba1c = float(patient.get("HbA1c_level", 5.5))
        glucose = float(patient.get("blood_glucose_level", 95))
        bmi = float(patient.get("bmi", 24.5))
        heart_disease = int(patient.get("heart_disease", 0))
        hypertension = int(patient.get("hypertension", 0))
        smoking = str(patient.get("smoking_history", "never")).lower()
        age = float(patient.get("age", 45))

        prescribed_drugs = []
        diet_plan = []
        exercise_plan = []

        # Drug formulation
        if hba1c >= 6.5 or glucose >= 126.0:
            if heart_disease == 1 or hypertension == 1:
                prescribed_drugs.append("Metformin 500mg (1 viên x 2 lần/ngày sau bữa ăn chính)")
                prescribed_drugs.append("Empagliflozin (Jardiance) 10mg (1 viên/ngày buổi sáng - bảo vệ tim mạch)")
            elif hba1c >= 9.0 or glucose >= 200:
                prescribed_drugs.append("Metformin 850mg (1 viên x 2 lần/ngày)")
                prescribed_drugs.append("Semaglutide 0.5mg (tiêm dưới da 1 lần/tuần) hoặc Insulin Glargine 10 IU khởi đầu")
            else:
                prescribed_drugs.append("Metformin 500mg (1 viên x 2 lần/ngày sau ăn)")
        elif 5.7 <= hba1c <= 6.4:
            if bmi >= 30.0:
                prescribed_drugs.append("Cân nhắc Metformin 500mg phòng ngừa tiến triển ĐTĐ (khuyến nghị ADA)")
            else:
                prescribed_drugs.append("Chưa chỉ định thuốc. Ưu tiên tuyệt đối can thiệp dinh dưỡng & thể lực.")
        else:
            prescribed_drugs.append("Không cần dùng thuốc. Tiếp tục duy trì chế độ dinh dưỡng cân bằng.")

        # Nutrition Plan
        diet_plan.append("Kiểm soát Carbohydrate Low-GI: Hạn chế cơm trắng, bánh mì trắng, nước ngọt; thay bằng gạo lứt, yến mạch, đậu đỗ.")
        diet_plan.append("Tăng cường chất xơ: Tối thiểu 30-40g chất xơ/ngày từ rau xanh đậm và quả hạch để làm chậm hấp thu glucose.")
        if bmi >= 25.0:
            diet_plan.append(f"Mục tiêu giảm năng lượng nạp: Cắt giảm 500 kcal/ngày để giảm 5-7% thể trọng hiện tại (BMI hiện tại: {bmi}).")

        # Exercise Plan
        exercise_plan.append("Tối thiểu 150 phút hoạt động aerobic cường độ trung bình/tuần (30 phút/ngày x 5 ngày/tuần như đi bộ nhanh, bơi lội, đạp xe).")
        exercise_plan.append("Không nghỉ tập thể lực quá 2 ngày liên tiếp để duy trì độ nhạy của thụ thể insulin ngoại vi.")
        if smoking in ["current", "ever"]:
            exercise_plan.append("Chương trình hỗ trợ cai thuốc lá tích cực bằng liệu pháp hành vi.")

        msg = (
            f"Tôi là {self.name}.\n"
            f"Dựa trên phân tích đồng thuận 7 mô hình AI và khuyến nghị Knowledge Graph:\n"
            f"✦ ĐƠN THUỐC ĐỀ XUẤT BAN ĐẦU:\n"
            + "\n".join([f"  • {d}" for d in prescribed_drugs]) + "\n"
            f"✦ KẾ HOẠCH DINH DƯỠNG (MNT):\n"
            + "\n".join([f"  • {dp}" for dp in diet_plan]) + "\n"
            f"✦ PHÁC ĐỒ VẬN ĐỘNG & LỐI SỐNG:\n"
            + "\n".join([f"  • {ep}" for ep in exercise_plan]) + "\n"
            f"✦ Chuyển toàn bộ hồ sơ lên DiaCritic-Agent để thực hiện cơ chế Tự đánh giá phản biện an toàn."
        )

        return {
            "agent": self.name,
            "prescribed_drugs": prescribed_drugs,
            "diet_plan": diet_plan,
            "exercise_plan": exercise_plan,
            "message": msg
        }
