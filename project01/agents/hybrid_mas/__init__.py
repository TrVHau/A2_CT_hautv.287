#!/usr/bin/env python3
"""
Hybrid Multiagent System (MAS) Package
Compliant with project_architecture_multiagent_diabet_v1.pdf:
- 6-Layer Architecture
- 8 Canonical Agents: A_data, A_DL, A_rule, A_KG, A_coord, A_exp, A_monitor, A_RL
- Standardized Message Schema: m_i = (id, agent, status, payload, evidence, version)
- Structured DecisionSupportReport: Prediction + Evidence + Limitations
"""

from .data_contract import AgentMessage, DecisionSupportReport
from .patient_data_agent import PatientDataAgent
from .dl_prediction_agent import DLPredictionAgent
from .rule_based_agent import RuleBasedAgent
from .kg_rag_agent import KGRAGAgent
from .explanation_agent import ExplanationAgent
from .monitoring_agent import MonitoringAgent
from .rl_simulation_agent import RLSimulationAgent
from .coordinator_agent import CoordinatorAgent, SECTION_10_SAFETY_LIMITATIONS

__all__ = [
    "AgentMessage",
    "DecisionSupportReport",
    "PatientDataAgent",
    "DLPredictionAgent",
    "RuleBasedAgent",
    "KGRAGAgent",
    "ExplanationAgent",
    "MonitoringAgent",
    "RLSimulationAgent",
    "CoordinatorAgent",
    "SECTION_10_SAFETY_LIMITATIONS",
]
