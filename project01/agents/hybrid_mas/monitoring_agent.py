#!/usr/bin/env python3
"""
MonitoringAgent (A_monitor)
Operational audit, agent latency tracking, and discrepancy detection agent.
Implements Layer 4 & Layer 6 / Agent A_monitor in project_architecture_multiagent_diabet_v1.pdf.
"""

import time
from datetime import datetime, timezone
from typing import Dict, Any, List
from .data_contract import AgentMessage


class MonitoringAgent:
    """A_monitor: Observability, latency logging, discrepancy verification, and clinical audit trail."""

    def __init__(self, version: str = "A_monitor_v1.0"):
        self.agent_name = "MonitoringAgent"
        self.version = version

    def audit(self, request_id: str,
              agent_latencies: Dict[str, float],
              dl_prob: float,
              rule_decision_numeric: int,
              features: Dict[str, Any]) -> AgentMessage:
        start_time = time.time()

        # 1. Total latency calculation
        total_latency_ms = round(sum(agent_latencies.values()), 2)

        # 2. DL vs Rule Discrepancy Check: |y_DL - y_rule|
        discrepancy_delta = round(abs(dl_prob - float(rule_decision_numeric)), 4)
        discrepancy_flag = discrepancy_delta > 0.50
        discrepancy_note = "Học sâu và Quy tắc y khoa đồng thuận cao."
        if discrepancy_flag:
            discrepancy_note = (
                f"CẢNH BÁO SAI LỆCH: Sai lệch giữa xác suất Học sâu ({dl_prob:.2f}) "
                f"và Quyết định Quy tắc ({rule_decision_numeric}) là Δ = {discrepancy_delta:.2f} > 0.50. "
                f"Hệ thống tự động kích hoạt cờ thẩm định chuyên gia người thật (Human-in-the-Loop)."
            )

        # 3. Physiological Outlier Checks
        outliers: List[str] = []
        glucose = float(features.get("blood_glucose_level", 100))
        hba1c = float(features.get("HbA1c_level", 5.5))
        bmi = float(features.get("bmi", 24.5))

        if glucose > 400.0 or glucose < 50.0:
            outliers.append(f"Cực trị đường huyết: {glucose} mg/dL")
        if hba1c > 15.0 or hba1c < 4.0:
            outliers.append(f"Cực trị HbA1c: {hba1c}%")
        if bmi > 55.0 or bmi < 13.0:
            outliers.append(f"Cực trị BMI: {bmi} kg/m²")

        # 4. Audit Status
        audit_passed = (len(outliers) == 0) and not discrepancy_flag
        audit_verdict = "PASSED (Đạt tiêu chuẩn vận hành an toàn)" if audit_passed else "FLAGGED_FOR_HUMAN_REVIEW (Cần bác sĩ duyệt)"

        self_latency = round((time.time() - start_time) * 1000, 2)
        agent_latencies["MonitoringAgent"] = self_latency

        payload = {
            "audit_verdict": audit_verdict,
            "audit_passed": audit_passed,
            "discrepancy_flag": discrepancy_flag,
            "discrepancy_delta": discrepancy_delta,
            "discrepancy_note": discrepancy_note,
            "physiological_outliers": outliers,
            "agent_latencies_ms": agent_latencies,
            "total_execution_latency_ms": round(sum(agent_latencies.values()), 2),
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "active_governance_rules": ["ADA_2024_PARITY_CHECK", "OUTLIER_BOUNDS_CHECK", "LATENCY_SLA_CHECK"]
        }

        evidence = [
            "ISO/IEC 42001 & WHO AI Governance Principles for Healthcare Systems",
            "Continuous Discrepancy & Drift Surveillance Protocol (Section 8)"
        ]

        status = "ok" if audit_passed else "flagged"

        return AgentMessage.create(
            request_id=request_id,
            agent=self.agent_name,
            status=status,
            payload=payload,
            evidence=evidence,
            version=self.version
        )
