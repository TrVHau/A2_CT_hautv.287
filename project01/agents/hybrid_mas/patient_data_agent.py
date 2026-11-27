#!/usr/bin/env python3
"""
PatientDataAgent (A_data)
Deterministic preprocessing and validation agent for clinical patient intakes.
Implements Layer 4 / Agent A_data in project_architecture_multiagent_diabet_v1.pdf.
"""

import time
from typing import Dict, Any, List
from .data_contract import AgentMessage


class PatientDataAgent:
    """A_data: Validates types, ranges, missing values, and normalizes clinical features."""

    def __init__(self, version: str = "A_data_v1.0"):
        self.agent_name = "PatientDataAgent"
        self.version = version

    def process(self, request_id: str, raw_input: Dict[str, Any]) -> AgentMessage:
        start_time = time.time()
        errors: List[str] = []
        warnings: List[str] = []
        features: Dict[str, Any] = {}

        # 1. Age validation (1 - 120)
        try:
            age = float(raw_input.get("age", 45))
            if not (1 <= age <= 120):
                errors.append(f"Tuổi ngoài phạm vi hợp lệ [1, 120]: {age}")
            features["age"] = age
        except (ValueError, TypeError):
            errors.append("Trường 'age' không đúng định dạng số.")
            features["age"] = 45.0

        # 2. Gender validation
        gender_raw = str(raw_input.get("gender", "Female")).strip().capitalize()
        if gender_raw in ["Male", "Nam"]:
            features["gender"] = "Male"
        elif gender_raw in ["Female", "Nữ"]:
            features["gender"] = "Female"
        else:
            features["gender"] = "Other"
            warnings.append(f"Giới tính ghi nhận dạng khác: {gender_raw}")

        # 3. BMI / Height / Weight validation
        bmi = None
        if "bmi" in raw_input and raw_input["bmi"] is not None:
            try:
                bmi = float(raw_input["bmi"])
            except (ValueError, TypeError):
                pass

        if bmi is None or bmi <= 0:
            height = raw_input.get("height_cm") or raw_input.get("height")
            weight = raw_input.get("weight_kg") or raw_input.get("weight")
            if height and weight:
                try:
                    h_m = float(height) / 100.0
                    w_kg = float(weight)
                    if 0.5 <= h_m <= 2.5 and 10 <= w_kg <= 300:
                        bmi = round(w_kg / (h_m * h_m), 1)
                        features["height_cm"] = float(height)
                        features["weight_kg"] = float(weight)
                except Exception:
                    pass

        if bmi is None:
            bmi = 24.5
            warnings.append("Thiếu chỉ số BMI/chiều cao/cân nặng, sử dụng giá trị trung vị 24.5 kg/m²")

        if not (10.0 <= bmi <= 80.0):
            warnings.append(f"Chỉ số BMI có dấu hiệu ngoại lai cực trị: {bmi} kg/m²")

        features["bmi"] = bmi

        # BMI Classification (WHO / Asian-Pacific criteria)
        if bmi < 18.5:
            bmi_cat = "Thiếu cân (Underweight)"
        elif bmi < 23.0:
            bmi_cat = "Bình thường (Normal - Tiêu chuẩn Châu Á)"
        elif bmi < 25.0:
            bmi_cat = "Thừa cân (Overweight)"
        else:
            bmi_cat = "Béo phì (Obese)"
        features["bmi_category"] = bmi_cat

        # 4. HbA1c validation (3.0 - 20.0 %)
        try:
            hba1c = float(raw_input.get("HbA1c_level", 5.5))
            if not (3.0 <= hba1c <= 20.0):
                warnings.append(f"Chỉ số HbA1c {hba1c}% ngoài dải sinh lý thông thường [3.0, 20.0]%")
            features["HbA1c_level"] = hba1c
        except (ValueError, TypeError):
            errors.append("Chỉ số HbA1c không đúng định dạng số.")
            features["HbA1c_level"] = 5.5

        # 5. Blood Glucose validation (30 - 700 mg/dL)
        try:
            glucose = float(raw_input.get("blood_glucose_level", 100.0))
            if not (30.0 <= glucose <= 700.0):
                warnings.append(f"Đường huyết {glucose} mg/dL ngoài dải đo thông thường [30.0, 700.0] mg/dL")
            features["blood_glucose_level"] = glucose
        except (ValueError, TypeError):
            errors.append("Đường huyết không đúng định dạng số.")
            features["blood_glucose_level"] = 100.0

        # 6. Hypertension (0 or 1)
        ht = raw_input.get("hypertension", 0)
        features["hypertension"] = 1 if str(ht).lower() in ["1", "true", "yes", "có"] else 0

        # 7. Heart Disease (0 or 1)
        hd = raw_input.get("heart_disease", 0)
        features["heart_disease"] = 1 if str(hd).lower() in ["1", "true", "yes", "có"] else 0

        # 8. Smoking history
        smk = str(raw_input.get("smoking_history", "never")).strip().lower()
        if smk in ["never", "không", "không hút", "chưa từng"]:
            features["smoking_history"] = "never"
        elif smk in ["former", "từng", "từng hút", "đã cai"]:
            features["smoking_history"] = "former"
        elif smk in ["current", "có", "đang hút", "hút thuốc"]:
            features["smoking_history"] = "current"
        elif smk in ["not current", "hiện không hút"]:
            features["smoking_history"] = "not current"
        elif smk in ["ever"]:
            features["smoking_history"] = "ever"
        else:
            features["smoking_history"] = "No Info"

        # Optional symptoms & eGFR
        features["symptoms"] = str(raw_input.get("symptoms", "")).strip()
        try:
            features["egfr"] = float(raw_input.get("egfr", 85.0))
        except (ValueError, TypeError):
            features["egfr"] = 85.0

        latency_ms = round((time.time() - start_time) * 1000, 2)
        status = "error" if errors else "ok"

        payload = {
            "valid": len(errors) == 0,
            "features": features,
            "errors": errors,
            "warnings": warnings,
            "latency_ms": latency_ms,
            "raw_field_count": len(raw_input)
        }

        evidence = [
            "ADA Standards of Medical Care 2024: Clinical Intake Specifications",
            "WHO Anthropometric & Biochemical Physiological Parameter Bounds"
        ]

        return AgentMessage.create(
            request_id=request_id,
            agent=self.agent_name,
            status=status,
            payload=payload,
            evidence=evidence,
            version=self.version
        )
