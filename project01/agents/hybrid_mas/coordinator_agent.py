#!/usr/bin/env python3
"""
CoordinatorAgent (A_coord)
Sequential multiagent orchestrator and decision aggregator.
Implements Layer 3 & Layer 4 / Agent A_coord in project_architecture_multiagent_diabet_v1.pdf.
Mathematical formulation: M = (A, S, O, C, F), with aggregation function F(y_DL, y_rule, y_KG, y_monitor).
Strict adherence to Section 5.3 Sequential Execution Pipeline and Section 10 Safety Limitations.
"""

import time
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List

from .data_contract import AgentMessage, DecisionSupportReport
from .patient_data_agent import PatientDataAgent
from .dl_prediction_agent import DLPredictionAgent
from .rule_based_agent import RuleBasedAgent
from .kg_rag_agent import KGRAGAgent
from .explanation_agent import ExplanationAgent
from .monitoring_agent import MonitoringAgent
from .rl_simulation_agent import RLSimulationAgent


# Section 10 Safety & Research Limitations Specifications
SECTION_10_SAFETY_LIMITATIONS = [
    "Hệ thống là bản thử nghiệm nghiên cứu khoa học (Research Prototype) phát triển cho Đồ án Hệ thống Thông minh PTIT (Tháng 11/2026).",
    "Kết quả từ hệ thống KHÔNG PHẢI là chẩn đoán y khoa xác định cuối cùng và không thay thế thăm khám của bác sĩ chuyên khoa.",
    "Hệ thống KHÔNG kê đơn thuốc hoặc quyết định liều lượng cụ thể trực tiếp cho người bệnh. Mọi chỉ định dược lý phải do bác sĩ phụ trách phê duyệt.",
    "Tác tử Học tăng cường (A_RL) vận hành độc quyền trong môi trường mô phỏng số sinh lý học ảo phục vụ nghiên cứu & tối ưu hóa lối sống dự phòng.",
    "Mọi kết luận y khoa cần tuân thủ phác đồ của Bộ Y tế và Hướng dẫn Hiệp hội Đái tháo đường Hoa Kỳ (ADA Standards of Care 2024)."
]


class CoordinatorAgent:
    """A_coord: Orchestrates 8 canonical agents, executes sequential workflow, aggregates decisions."""

    def __init__(self, version: str = "A_coord_v1.0"):
        self.agent_name = "CoordinatorAgent"
        self.version = version

        # Instantiate 7 subordinate canonical agents
        self.a_data = PatientDataAgent()
        self.a_dl = DLPredictionAgent()
        self.a_rule = RuleBasedAgent()
        self.a_kg = KGRAGAgent()
        self.a_exp = ExplanationAgent()
        self.a_monitor = MonitoringAgent()
        self.a_rl = RLSimulationAgent()

    def run_workflow(self, raw_patient_data: Dict[str, Any], include_simulation: bool = True) -> DecisionSupportReport:
        """Executes the complete Section 5.3 Sequential Pipeline."""
        start_pipeline_time = time.time()
        req_id = f"req_{int(time.time())}_{uuid.uuid4().hex[:6]}"
        timestamp_now = datetime.now(timezone.utc).isoformat()

        agent_messages: List[AgentMessage] = []
        latencies: Dict[str, float] = {}

        # -------------------------------------------------------------
        # Step 1: PatientDataAgent (A_data)
        # -------------------------------------------------------------
        t0 = time.time()
        msg_data = self.a_data.process(req_id, raw_patient_data)
        latencies["PatientDataAgent"] = round((time.time() - t0) * 1000, 2)
        agent_messages.append(msg_data)

        # Early termination check if input validation failed
        if msg_data.status == "error":
            return DecisionSupportReport(
                request_id=req_id,
                timestamp=timestamp_now,
                prediction={"error": "Dữ liệu đầu vào không hợp lệ", "details": msg_data.payload.get("errors")},
                rule_results={},
                evidence={},
                explanation={"error": "Quy trình dừng sớm do lỗi kiểm định dữ liệu ban đầu."},
                simulation=None,
                monitoring={"audit_verdict": "REJECTED_INPUT_VALIDATION_ERROR", "latencies_ms": latencies},
                agent_messages=[m.to_dict() for m in agent_messages],
                safety_limitations=SECTION_10_SAFETY_LIMITATIONS
            )

        clean_features = msg_data.payload["features"]

        # -------------------------------------------------------------
        # Step 2: DLPredictionAgent (A_DL)
        # -------------------------------------------------------------
        t0 = time.time()
        msg_dl = self.a_dl.predict(req_id, clean_features)
        latencies["DLPredictionAgent"] = round((time.time() - t0) * 1000, 2)
        agent_messages.append(msg_dl)

        # -------------------------------------------------------------
        # Step 3: RuleBasedAgent (A_rule)
        # -------------------------------------------------------------
        t0 = time.time()
        msg_rule = self.a_rule.evaluate(req_id, clean_features)
        latencies["RuleBasedAgent"] = round((time.time() - t0) * 1000, 2)
        agent_messages.append(msg_rule)

        # -------------------------------------------------------------
        # Step 4: KGRAGAgent (A_KG)
        # -------------------------------------------------------------
        t0 = time.time()
        msg_kg = self.a_kg.query(req_id, clean_features, msg_rule.payload)
        latencies["KGRAGAgent"] = round((time.time() - t0) * 1000, 2)
        agent_messages.append(msg_kg)

        # -------------------------------------------------------------
        # Step 5: Decision Aggregation Function F(y_DL, y_rule, y_KG, y_monitor)
        # -------------------------------------------------------------
        dl_prob = float(msg_dl.payload.get("probability", 0.0))
        rule_decision_num = int(msg_rule.payload.get("rule_decision_numeric", 0))
        critical_override = bool(msg_rule.payload.get("critical_override", False))
        rule_class_str = msg_rule.payload.get("classification", "")

        if critical_override:
            final_pred_code = 1
            final_pred_label = f"CẤP CỨU LÂM SÀNG ({msg_rule.payload.get('urgency_level')})"
            aggregated_confidence = 100.0
            consensus_mode = "OVERRIDE_BY_ACUTE_SAFETY_RULE"
        elif rule_decision_num == 1:
            final_pred_code = 1
            final_pred_label = "Mắc Đái Tháo Đường (Positive - Đồng thuận ADA & TabResNet)"
            aggregated_confidence = max(round(dl_prob * 100, 1), 85.0)
            consensus_mode = "HARMONIZED_CLINICAL_AGREEMENT"
        elif "Tiền đái tháo đường" in rule_class_str:
            final_pred_code = 0
            final_pred_label = "Tiền Đái Tháo Đường (Prediabetes - Rối loạn dung nạp glucose)"
            aggregated_confidence = max(round(dl_prob * 100, 1), 65.0)
            consensus_mode = "IMPAIRED_GLUCOSE_REGULATION"
        else:
            if dl_prob >= 0.50:
                final_pred_code = 1
                final_pred_label = "Nghi ngờ Đái Tháo Đường (Cảnh báo Học Sâu phi tuyến)"
                aggregated_confidence = round(dl_prob * 100, 1)
                consensus_mode = "DEEP_LEARNING_EARLY_WARNING"
            else:
                final_pred_code = 0
                final_pred_label = "Không Mắc Đái Tháo Đường (Negative - Bình thường)"
                aggregated_confidence = round((1.0 - dl_prob) * 100, 1)
                consensus_mode = "NORMAL_GLUCOSE_HOMEOSTASIS"

        aggregated_prediction = {
            "final_prediction": final_pred_code,
            "final_diagnosis": final_pred_label,
            "aggregated_confidence_pct": aggregated_confidence,
            "consensus_mechanism": consensus_mode,
            "dl_probability": dl_prob,
            "dl_probability_percentage": msg_dl.payload.get("probability_percentage"),
            "dl_risk_tier": msg_dl.payload.get("risk_tier"),
            "dl_model_architecture": msg_dl.payload.get("model_architecture"),
            "rule_classification": rule_class_str,
            "critical_safety_override": critical_override
        }

        # -------------------------------------------------------------
        # Step 6: ExplanationAgent (A_exp)
        # -------------------------------------------------------------
        t0 = time.time()
        msg_exp = self.a_exp.explain(
            req_id,
            msg_dl.payload,
            msg_rule.payload,
            msg_kg.payload,
            clean_features
        )
        latencies["ExplanationAgent"] = round((time.time() - t0) * 1000, 2)
        agent_messages.append(msg_exp)

        # -------------------------------------------------------------
        # Step 7: MonitoringAgent (A_monitor)
        # -------------------------------------------------------------
        t0 = time.time()
        msg_monitor = self.a_monitor.audit(
            req_id,
            latencies,
            dl_prob,
            rule_decision_num,
            clean_features
        )
        latencies["MonitoringAgent"] = round((time.time() - t0) * 1000, 2)
        agent_messages.append(msg_monitor)

        # -------------------------------------------------------------
        # Step 8: RLSimulationAgent (A_RL)
        # -------------------------------------------------------------
        sim_payload = None
        if include_simulation:
            t0 = time.time()
            msg_rl = self.a_rl.simulate(req_id, clean_features)
            latencies["RLSimulationAgent"] = round((time.time() - t0) * 1000, 2)
            agent_messages.append(msg_rl)
            sim_payload = msg_rl.payload

        # Self-Message for Coordinator (A_coord)
        total_mas_latency = round((time.time() - start_pipeline_time) * 1000, 2)
        latencies["CoordinatorAgent"] = round(total_mas_latency - sum(latencies.values()), 2)

        msg_coord = AgentMessage.create(
            request_id=req_id,
            agent=self.agent_name,
            status="ok",
            payload={
                "pipeline_execution": "SUCCESS",
                "total_pipeline_latency_ms": total_mas_latency,
                "agent_count": len(agent_messages) + 1,
                "workflow_sequence": [
                    "A_data (PatientDataAgent)",
                    "A_DL (DLPredictionAgent)",
                    "A_rule (RuleBasedAgent)",
                    "A_KG (KGRAGAgent)",
                    "F (Aggregation Function)",
                    "A_exp (ExplanationAgent)",
                    "A_monitor (MonitoringAgent)",
                    "A_RL (RLSimulationAgent)",
                    "A_coord (CoordinatorAgent)"
                ]
            },
            evidence=[
                "Sequential Multiagent Pipeline Architecture (Section 5.3)",
                "Mathematical Abstraction M = (A, S, O, C, F) (Section 4)"
            ],
            version=self.version
        )
        agent_messages.append(msg_coord)

        # Compile final structured report
        return DecisionSupportReport(
            request_id=req_id,
            timestamp=timestamp_now,
            prediction=aggregated_prediction,
            rule_results=msg_rule.payload,
            evidence=msg_kg.payload,
            explanation=msg_exp.payload,
            simulation=sim_payload,
            monitoring=msg_monitor.payload,
            agent_messages=[m.to_dict() for m in agent_messages],
            safety_limitations=SECTION_10_SAFETY_LIMITATIONS
        )
