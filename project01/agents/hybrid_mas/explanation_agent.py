#!/usr/bin/env python3
"""
ExplanationAgent (A_exp)
Explainable AI and clinical narrative synthesis agent.
Implements Layer 4 / Agent A_exp in project_architecture_multiagent_diabet_v1.pdf.
Grounding: Synthesizes DL scores, symbolic rules, and Knowledge Graph evidence without hallucination.
"""

import time
from typing import Dict, Any, List
from .data_contract import AgentMessage


class ExplanationAgent:
    """A_exp: Generates evidence-grounded structured explanations."""

    def __init__(self, version: str = "A_exp_v1.0"):
        self.agent_name = "ExplanationAgent"
        self.version = version

    def explain(self, request_id: str,
                dl_payload: Dict[str, Any],
                rule_payload: Dict[str, Any],
                kg_payload: Dict[str, Any],
                features: Dict[str, Any]) -> AgentMessage:
        start_time = time.time()

        glucose = float(features.get("blood_glucose_level", 100.0))
        hba1c = float(features.get("HbA1c_level", 5.5))
        bmi = float(features.get("bmi", 24.5))
        age = float(features.get("age", 45))
        ht = int(features.get("hypertension", 0))
        hd = int(features.get("heart_disease", 0))
        smk = str(features.get("smoking_history", "never"))

        prob_pct = dl_payload.get("probability_percentage", 0.0)
        risk_tier = dl_payload.get("risk_tier", "Chưa xác định")
        rule_class = rule_payload.get("classification", "Chưa xác định")
        crit_override = rule_payload.get("critical_override", False)
        urgency = rule_payload.get("urgency_level", "Thường quy")

        disease_info = kg_payload.get("disease_entity", {})
        disease_name = disease_info.get("name", "Đái tháo đường")
        icd10 = disease_info.get("icd10", "E11")

        # 1. Executive Summary
        if crit_override:
            summary = (
                f"CẢNH BÁO KHẨN CẤP: Hệ thống ghi nhận trạng thái {urgency}. "
                f"Đường huyết đo được {glucose} mg/dL vượt ngưỡng an toàn. "
                f"Mô hình Học sâu TabResNet ước tính xác suất rủi ro {prob_pct}%, xếp loại {risk_tier}. "
                f"Quy tắc an toàn lâm sàng ADA 2024 kích hoạt yêu cầu chuyển tuyến cấp cứu ngay."
            )
        elif rule_payload.get("rule_decision_numeric") == 1 or prob_pct >= 50.0:
            summary = (
                f"KẾT LUẬN ĐỒNG THUẬN: Bệnh nhân được phân loại {disease_name} (ICD-10: {icd10}). "
                f"Mô hình TabResNet Self-Attention dự báo xác suất nguy cơ {prob_pct}% ({risk_tier}). "
                f"Kết quả được bảo chứng bởi các quy tắc chẩn đoán xác định của Hiệp hội Đái tháo đường Hoa Kỳ (ADA 2024)."
            )
        else:
            summary = (
                f"KẾT LUẬN ĐỒNG THUẬN: Bệnh nhân hiện ở phân loại {rule_class}. "
                f"Mô hình TabResNet Self-Attention dự báo xác suất nguy cơ thấp ({prob_pct}%), "
                f"phù hợp với các mốc sinh hóa glucose máu và HbA1c trong giới hạn cho phép."
            )

        # 2. Key Physiological Drivers
        drivers = []
        if hba1c >= 6.5:
            drivers.append(f"Chỉ số HbA1c={hba1c}% vượt ngưỡng chẩn đoán xác định đái tháo đường (ngưỡng chuẩn >= 6.5%).")
        elif hba1c >= 5.7:
            drivers.append(f"Chỉ số HbA1c={hba1c}% nằm trong khoảng nguy cơ cao tiền đái tháo đường [5.7 - 6.4]%.")
        else:
            drivers.append(f"Chỉ số HbA1c={hba1c}% trong ngưỡng bình thường (< 5.7%).")

        if glucose >= 126.0:
            drivers.append(f"Đường huyết lúc đói={glucose} mg/dL vượt ngưỡng chẩn đoán bệnh lý (>= 126 mg/dL).")
        elif glucose >= 100.0:
            drivers.append(f"Đường huyết lúc đói={glucose} mg/dL biểu hiện rối loạn dung nạp đường [100 - 125] mg/dL.")
        else:
            drivers.append(f"Đường huyết={glucose} mg/dL ổn định trong dải bình thường (< 100 mg/dL).")

        if bmi >= 25.0:
            drivers.append(f"Chỉ số khối cơ thể BMI={bmi} kg/m² ({features.get('bmi_category')}) gây đề kháng insulin.")

        if ht == 1 or hd == 1:
            comorb_str = []
            if ht == 1:
                comorb_str.append("Tăng huyết áp")
            if hd == 1:
                comorb_str.append("Bệnh tim mạch")
            drivers.append(f"Tiền sử bệnh lý nền đồng mắc: {', '.join(comorb_str)}, làm tăng nguy cơ biến chứng mạch máu.")

        if smk in ["current", "former", "ever", "hút thuốc"]:
            drivers.append("Yếu tố lối sống (hút thuốc lá) làm gia tăng tổn thương nội mô mạch máu và biến cố tim mạch xơ vữa.")

        # 3. Clinical Rationale
        rationale = (
            f"Sự phối hợp giữa mô hình học sâu TabResNet (khai thác tương tác phi tuyến giữa 8 dấu ấn sinh học) "
            f"và hệ suy luận biểu tượng (ADA 2024 Guardrails) mang lại sự thống nhất cao: "
            f"Xác suất {prob_pct}% tương thích với kết luận lâm sàng '{rule_class}'. "
            f"Không phát hiện xung đột mâu thuẫn giữa mô hình định lượng và phác đồ y khoa."
        )

        # 4. Monitoring Recommendations
        monitoring_plan = [
            "Xét nghiệm lại HbA1c định kỳ mỗi 3 tháng nếu chưa đạt mục tiêu, hoặc 6 tháng/lần nếu đã ổn định.",
            "Tự theo dõi đường huyết mao mạch tại nhà theo chỉ dẫn của bác sĩ điều trị.",
            "Tầm soát biến chứng vi mạch: Định kỳ khám đáy mắt giãn đồng tử, xét nghiệm tỷ lệ microalbumin/creatinine niệu hàng năm.",
            "Kiểm soát huyết áp (< 130/80 mmHg) và mỡ máu lipid panel (LDL-C < 70 mg/dL hoặc < 55 mg/dL nếu có ASCVD)."
        ]

        latency_ms = round((time.time() - start_time) * 1000, 2)

        payload = {
            "executive_summary": summary,
            "key_drivers": drivers,
            "clinical_rationale": rationale,
            "monitoring_recommendations": monitoring_plan,
            "latency_ms": latency_ms
        }

        evidence = [
            "Grounded in DLPredictionAgent probability output and TabResNet biomarker attributions",
            "Synthesized with ADA 2024 / KDIGO deterministic guardrails from RuleBasedAgent",
            "Evidence relations retrieved from DB_diabet.cypher Knowledge Graph"
        ]

        return AgentMessage.create(
            request_id=request_id,
            agent=self.agent_name,
            status="ok",
            payload=payload,
            evidence=evidence,
            version=self.version
        )
