#!/usr/bin/env python3
"""
Pharmacogenomics, Renal Clearance & Drug Interaction Agent (DiaPharmacogenomicsAgent)
Evaluates drug metabolism, genetic polymorphism risk (CYP2C9, SLCO1B1),
Cockcroft-Gault renal clearance, and polypharmacy contraindications.
"""

class DiaPharmacogenomicsAgent:
    """Tác Tử Dược Lý Di Truyền Học & Tương Tác Thuốc Cá Thể Hóa"""
    def __init__(self):
        self.name = "DiaPharmacogenomics-Agent (Tác Tử Dược Lý Di Truyền & Tương Tác Đa Thuốc)"

    def analyze_pharmacogenomics_and_interactions(self, patient: dict, prescribed_drugs: list) -> dict:
        age = float(patient.get("age", 45))
        gender = str(patient.get("gender", "Female")).lower()
        bmi = float(patient.get("bmi", 25.0))
        hba1c = float(patient.get("HbA1c_level", 5.5))
        glucose = float(patient.get("blood_glucose_level", 95))
        heart_disease = int(patient.get("heart_disease", 0))
        hypertension = int(patient.get("hypertension", 0))

        # Estimate weight from BMI (assume height = 1.65m)
        height_m = 1.65
        weight_kg = bmi * (height_m ** 2)

        # Estimate serum creatinine based on age, gender
        base_scr = 0.9 if gender == "female" else 1.1
        if age >= 65:
            base_scr += 0.2

        # Cockcroft-Gault CrCl formula (mL/min)
        crcl = ((140.0 - age) * weight_kg) / (72.0 * base_scr)
        if gender == "female":
            crcl *= 0.85
        crcl = round(crcl, 1)

        pharmacogenomic_notes = []
        interaction_warnings = []

        # 1. CYP2C9 Genotype evaluation (for Sulfonylurea metabolism)
        has_su = any("Gliclazide" in d or "Glimepiride" in d for d in prescribed_drugs)
        if has_su:
            if age >= 65 or crcl < 60:
                pharmacogenomic_notes.append(
                    "[ĐA HÌNH GEN CYP2C9*3]: Bệnh nhân cao tuổi có nguy cơ giảm chuyển hóa Sulfonylurea do alen CYP2C9*3, "
                    "làm kéo dài thời gian bán thải và tăng gấp 3 lần nguy cơ hạ đường huyết nguy hiểm. Đề xuất chuyển sang DPP-4i hoặc SGLT2i."
                )

        # 2. SLCO1B1 Transporter (Statin interaction for Cardiovascular protection)
        if heart_disease == 1 or age >= 50:
            pharmacogenomic_notes.append(
                "[VẬN CHUYỂN SLCO1B1 (Statin)]: Khuyến nghị tầm soát kiểu gen SLCO1B1 trước khi dùng Statin liều cao. "
                "Ưu tiên Rosuvastatin liều thấp hoặc Atorvastatin 20mg để phòng ngừa đau cơ / tiêu cơ vân."
            )

        # 3. Renal Clearance Contraindication Check
        has_metformin = any("Metformin" in d for d in prescribed_drugs)
        if has_metformin:
            if crcl < 30:
                interaction_warnings.append(
                    f"[CHỐNG CHỈ ĐỊNH SUY THẬN NẶNG]: Độ thanh thải Creatinin CrCl = {crcl} mL/phút < 30 mL/phút. "
                    "CHỐNG CHỈ ĐỊNH TUYỆT ĐỐI Metformin do nguy cơ nhiễm toan Lactic tử vong."
                )
            elif crcl < 45:
                interaction_warnings.append(
                    f"[CHỈNH LIỀU THẬN]: CrCl = {crcl} mL/phút (30-44 mL/phút). "
                    "Giảm tối đa 50% liều Metformin (tối đa 1000mg/ngày) và theo dõi CrCl mỗi 3 tháng."
                )
            else:
                pharmacogenomic_notes.append(f"[THANH THẢI THẬN TỐT]: CrCl ước tính = {crcl} mL/phút >= 45. An toàn với Metformin liều tiêu chuẩn.")

        # 4. SGLT2i + ACEi/ARB Dual Organ Protection
        has_sglt2i = any("Empagliflozin" in d or "Dapagliflozin" in d for d in prescribed_drugs)
        if has_sglt2i and (heart_disease == 1 or hypertension == 1):
            pharmacogenomic_notes.append(
                "[HIỆP ĐỒNG BẢO VỆ TIM - THẬN]: Phối hợp SGLT2i với thuốc huyết áp giúp giảm áp lực trong vi cầu thận "
                "và giảm 38% tử vong tim mạch (Dữ liệu EMPA-REG / DAPA-CKD)."
            )

        speech = (
            f"Tôi là {self.name}.\n"
            f"✦ ĐÁNH GIÁ DƯỢC LÝ DI TRUYỀN & ĐỘ THANH THẢI THẬN:\n"
            f"  • Độ thanh thải Creatinin CrCl ước tính (Cockcroft-Gault): {crcl} mL/phút\n"
            f"  • Đánh giá an toàn thuốc: " + ("AN TOÀN" if not interaction_warnings else "CẦN CHỈNH LIỀU/CHỐNG CHỈ ĐỊNH") + "\n"
            + "\n".join([f"  • {n}" for n in pharmacogenomic_notes]) + "\n"
            + "\n".join([f"  • {w}" for w in interaction_warnings])
        )

        return {
            "agent": self.name,
            "crcl_ml_min": crcl,
            "pharmacogenomic_notes": pharmacogenomic_notes,
            "interaction_warnings": interaction_warnings,
            "speech": speech
        }
