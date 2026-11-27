"""
Reasoning Tools and Deterministic Planner for Tieuluan 2:
- 5 Core Production Tools:
    1. tool_kg_diabetes: Knowledge Graph clinical queries and drug interaction checks
    2. tool_kg_finance: Macroeconomic transmission channels and shock propagation
    3. tool_rag_retrieve: Hybrid RRF + GraphRAG evidence retrieval
    4. tool_mlp_diabetes_risk: PyTorch 13-feature DiabetesMLP inference
    5. tool_bilstm_forecast: PyTorch BiLSTM time series forecasting with MC Dropout
- Deterministic Planner:
    - Intent and Domain Classification
    - Entity Extraction and Tool Sequence Selection
"""

import re
from typing import Dict, List, Tuple, Any, Callable, Optional


class Tool:
    """Standardized tool interface with execution telemetry."""
    def __init__(self, name: str, domain: str, description: str, func: Callable):
        self.name = name
        self.domain = domain
        self.description = description
        self.func = func

    def execute(self, **kwargs) -> Any:
        return self.func(**kwargs)


class DeterministicPlanner:
    """Deterministic tool selector preventing unconstrained agent hallucinations."""
    def __init__(self):
        pass

    def plan_execution_path(self, question: str, patient_record: Optional[Dict] = None) -> Dict[str, Any]:
        q_lower = question.lower()

        # Domain 1: Healthcare (Y tế / Đái tháo đường)
        health_keywords = ["đường", "tiểu đường", "metformin", "hba1c", "glucose", "fpg", "bệnh nhân", "uống", "thuốc", "ăn", "thịt gà", "cơm", "bụng", "lactic"]
        is_health = any(w in q_lower for w in health_keywords) or patient_record is not None

        # Domain 2: Finance (Tài chính / Vĩ mô / Cổ phiếu / Vàng)
        finance_keywords = ["fed", "lãi suất", "tỷ giá", "usd", "vnd", "vàng", "sjc", "xau", "cổ phiếu", "fpt", "vnm", "hpg", "vcb", "vn30", "dự báo", "dxy"]
        is_finance = any(w in q_lower for w in finance_keywords)

        steps = []
        if is_health:
            domain = "Healthcare"
            if patient_record:
                steps.append({"tool": "tool_mlp_diabetes_risk", "args": {"record": patient_record}})
            if any(w in q_lower for w in ["tương tác", "rượu", "bia", "thuốc", "phác đồ", "chỉ số", "gi", "ăn"]):
                steps.append({"tool": "tool_kg_diabetes", "args": {"query": question}})
            steps.append({"tool": "tool_rag_retrieve", "args": {"query": question, "domain": "Healthcare"}})

        elif is_finance:
            domain = "Finance"
            if any(w in q_lower for w in ["dự báo", "ngày mai", "phiên tới", "giá"]):
                # Identify asset
                asset = "FPT"
                for a in ["FPT", "VNM", "HPG", "VCB", "GOLD_SJC"]:
                    if a.lower() in q_lower:
                        asset = a
                        break
                steps.append({"tool": "tool_bilstm_forecast", "args": {"asset": asset}})
            if any(w in q_lower for w in ["kênh", "tác động", "lan truyền", "truyền dẫn", "tỷ giá", "fed", "lãi suất"]):
                steps.append({"tool": "tool_kg_finance", "args": {"query": question}})
            steps.append({"tool": "tool_rag_retrieve", "args": {"query": question, "domain": "Finance"}})

        else:
            domain = "General"
            steps.append({"tool": "tool_rag_retrieve", "args": {"query": question, "domain": "All"}})

        return {
            "question": question,
            "detected_domain": domain,
            "planned_tool_sequence": steps
        }
