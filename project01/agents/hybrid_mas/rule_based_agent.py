#!/usr/bin/env python3
"""
RuleBasedAgent (A_rule)
Symbolic reasoning agent executing deterministic clinical rules and safety overrides.
Implements Layer 4 / Agent A_rule in project_architecture_multiagent_diabet_v1.pdf.
Grounding: ADA 2024 Standards of Care, KDIGO 2023, WHO Guidelines.
"""

import time
from typing import Dict, Any, List
from .data_contract import AgentMessage


class RuleBasedAgent:
    """A_rule: Evaluates explicit ADA 2024 diagnostic thresholds and clinical safety constraints."""

    def __init__(self, version: str = "A_rule_v1.0"):
        self.agent_name = "RuleBasedAgent"
        self.version = version

    def evaluate(self, request_id: str, features: Dict[str, Any]) -> AgentMessage:
        start_time = time.time()

        glucose = float(features.get("blood_glucose_level", 100.0))
        hba1c = float(features.get("HbA1c_level", 5.5))
        bmi = float(features.get("bmi", 24.5))
        age = float(features.get("age", 45.0))
        hypertension = int(features.get("hypertension", 0))
        heart_disease = int(features.get("heart_disease", 0))
        smoking = str(features.get("smoking_history", "never")).lower()
        egfr = float(features.get("egfr", 85.0))

        triggered_rules: List[Dict[str, Any]] = []
        contraindications: List[str] = []
        critical_override = False
        urgency_level = "Thường quy (Routine)"

        # ---------------------------------------------------------
        # 1. ACUTE SAFETY OVERRIDES (EMERGENCY)
        # ---------------------------------------------------------
        # Critical Hyperglycemia (HHS / DKA risk)
        if glucose >= 250.0:
            critical_override = True
            urgency_level = "CẤP CỨU KHẨN CẤP (EMERGENCY)"
            triggered_rules.append({
                "rule_id": "R_CRIT_HYPER",
                "severity": "CRITICAL",
                "condition": f"Đường huyết đo được {glucose} mg/dL >= 250 mg/dL",
                "guideline": "ADA Standards of Care 2024 - Khủng hoảng tăng đường huyết cấp",
                "action": "Chỉ định cấp cứu bệnh viện ngay lập tức. Cần tầm soát toan ceton (DKA) và hội chứng tăng áp lực thẩm thấu (HHS). Không trì hoãn xử trí."
            })

        # Severe Hypoglycemia
        if glucose < 70.0:
            critical_override = True
            urgency_level = "CẤP CỨU HẠ ĐƯỜNG HUYẾT (EMERGENCY)"
            triggered_rules.append({
                "rule_id": "R_CRIT_HYPO",
                "severity": "CRITICAL",
                "condition": f"Đường huyết đo được {glucose} mg/dL < 70 mg/dL",
                "guideline": "Quy tắc 15-15 của ADA / WHO",
                "action": "Nguy cơ hôn mê hạ đường huyết! Bổ sung ngay 15g carbohydrate hấp thu nhanh (nước đường/nước trái cây), đo lại sau 15 phút."
            })

        # ---------------------------------------------------------
        # 2. ADA 2024 DIAGNOSTIC THRESHOLDS
        # ---------------------------------------------------------
        dm_criteria_met = (hba1c >= 6.5) or (glucose >= 126.0)
        predm_criteria_met = (5.7 <= hba1c < 6.5) or (100.0 <= glucose < 126.0)

        if dm_criteria_met:
            classification = "Đái tháo đường (Diabetic - Tiêu chuẩn ADA 2024)"
            dm_flag = 1
            rule_reasons = []
            if hba1c >= 6.5:
                rule_reasons.append(f"HbA1c {hba1c}% >= 6.5%")
            if glucose >= 126.0:
                rule_reasons.append(f"Đường huyết đói {glucose} mg/dL >= 126 mg/dL")

            triggered_rules.append({
                "rule_id": "R_ADA_DM",
                "severity": "HIGH",
                "condition": " VÀ/HOẶC ".join(rule_reasons),
                "guideline": "ADA Standards of Care 2024 - Tiêu chuẩn chẩn đoán ĐTĐ",
                "action": "Xác nhận chẩn đoán Đái tháo đường. Khởi động phác đồ điều trị đa mô thức và can thiệp lối sống tích cực."
            })
        elif predm_criteria_met:
            classification = "Tiền đái tháo đường (Prediabetes - Nguy cơ cao)"
            dm_flag = 0
            rule_reasons = []
            if 5.7 <= hba1c < 6.5:
                rule_reasons.append(f"HbA1c {hba1c}% nằm trong khoảng [5.7, 6.4]%")
            if 100.0 <= glucose < 126.0:
                rule_reasons.append(f"Đường huyết đói {glucose} mg/dL trong khoảng [100, 125] mg/dL")

            triggered_rules.append({
                "rule_id": "R_ADA_PREDM",
                "severity": "MODERATE",
                "condition": " VÀ/HOẶC ".join(rule_reasons),
                "guideline": "ADA 2024 Prevention or Delay of Type 2 Diabetes",
                "action": "Chẩn đoán Tiền đái tháo đường. Can thiệp thay đổi lối sống giảm 5-7% trọng lượng cơ thể, luyện tập thể lực 150 phút/tuần."
            })
        else:
            classification = "Bình thường (Normal Glucose Metabolism)"
            dm_flag = 0
            triggered_rules.append({
                "rule_id": "R_ADA_NORMAL",
                "severity": "LOW",
                "condition": f"HbA1c {hba1c}% < 5.7% và Đường huyết {glucose} mg/dL < 100 mg/dL",
                "guideline": "ADA 2024",
                "action": "Các chỉ số chuyển hóa glucose trong giới hạn bình thường. Duy trì chế độ sinh hoạt lành mạnh."
            })

        # ---------------------------------------------------------
        # 3. CLINICAL SAFETY CONSTRAINTS & COMORBIDITIES
        # ---------------------------------------------------------
        # Metformin contraindication check (eGFR < 30)
        if egfr < 30.0:
            contraindications.append("Chống chỉ định tuyệt đối Metformin (eGFR < 30 mL/min/1.73m²) do nguy cơ toan acid lactic")
            triggered_rules.append({
                "rule_id": "R_CONTRA_MET_SEVERE",
                "severity": "CRITICAL_PHARMA",
                "condition": f"eGFR ước tính {egfr} < 30 mL/min/1.73m²",
                "guideline": "FDA & KDIGO 2023 Guidelines on Metformin in CKD",
                "action": "Chống chỉ định tuyệt đối Metformin. Chuyển sang ức chế DPP-4 chỉnh liều hoặc Insulin nền."
            })
        elif egfr < 45.0:
            contraindications.append("Cảnh báo liều Metformin: eGFR 30-44 mL/min/1.73m², giảm liều tối đa 1000mg/ngày")
            triggered_rules.append({
                "rule_id": "R_WARN_MET_MODERATE",
                "severity": "WARNING_PHARMA",
                "condition": f"eGFR ước tính {egfr} trong khoảng [30, 44] mL/min/1.73m²",
                "guideline": "ADA / KDIGO 2023",
                "action": "Khuyến cáo giảm 50% liều Metformin, theo dõi chức năng thận định kỳ 3 tháng."
            })

        # Cardioprotective therapy recommendation (DM + CVD or Hypertension)
        if dm_flag == 1 and (heart_disease == 1 or hypertension == 1):
            triggered_rules.append({
                "rule_id": "R_CARDIO_RENAL_PROTECTION",
                "severity": "HIGH_CLINICAL",
                "condition": "Đái tháo đường kết hợp Bệnh tim mạch hoặc Tăng huyết áp",
                "guideline": "ADA 2024 Section 10: Cardiovascular Disease and Risk Management",
                "action": "Ưu tiên chỉ định nhóm ức chế SGLT2 (SGLT2i) hoặc đồng vận thụ thể GLP-1 (GLP-1 RA) có bằng chứng bảo vệ tim mạch - thận rõ rệt."
            })

        # Smoking cessation alert
        if smoking in ["current", "ever", "hút thuốc"]:
            triggered_rules.append({
                "rule_id": "R_SMOKING_CESSATION",
                "severity": "WARNING_LIFESTYLE",
                "condition": "Tiền sử hoặc hiện tại đang hút thuốc lá",
                "guideline": "ADA / WHO Smoking Cessation in Diabetes",
                "action": "Khuyến cáo tư vấn cai thuốc lá khẩn cấp: Hút thuốc làm tăng 2-3 lần biến cố tim mạch xơ vữa và biến chứng thận đái tháo đường."
            })

        # Obesity metabolic syndrome alert
        if bmi >= 30.0:
            triggered_rules.append({
                "rule_id": "R_OBESITY_MANAGEMENT",
                "severity": "WARNING_LIFESTYLE",
                "condition": f"Chỉ số BMI {bmi} kg/m² >= 30.0 (Béo phì)",
                "guideline": "ADA 2024 Obesity and Weight Management",
                "action": "Mục tiêu giảm tối thiểu 7-10% thể trọng để cải thiện độ nhạy insulin và kiểm soát đường huyết."
            })

        latency_ms = round((time.time() - start_time) * 1000, 2)
        status = "flagged" if critical_override else "ok"

        payload = {
            "classification": classification,
            "rule_decision_numeric": dm_flag,
            "critical_override": critical_override,
            "urgency_level": urgency_level,
            "triggered_rules_count": len(triggered_rules),
            "triggered_rules": triggered_rules,
            "contraindications": contraindications,
            "latency_ms": latency_ms
        }

        evidence = [
            "ADA Standards of Care in Diabetes 2024: Chapter 2 (Classification & Diagnosis)",
            "KDIGO 2023 Clinical Practice Guideline for Diabetes Management in Chronic Kidney Disease",
            "WHO Guidelines on Diagnosis and Management of Type 2 Diabetes Mellitus"
        ]

        return AgentMessage.create(
            request_id=request_id,
            agent=self.agent_name,
            status=status,
            payload=payload,
            evidence=evidence,
            version=self.version
        )
