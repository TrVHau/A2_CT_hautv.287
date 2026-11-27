#!/usr/bin/env python3
"""
Communication and Data Contracts for Hybrid Multiagent System (MAS)
Implements Section 6 of project_architecture_multiagent_diabet_v1.pdf:
  m_i = (id, agent, status, payload, evidence, version)
"""

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
import time
import uuid

@dataclass
class AgentMessage:
    """Standardized Agent Message structure matching Section 6.1 of the architecture specification:
    m_i = (id, agent, status, payload, evidence, version)
    """
    id: str                                  # Request identifier (e.g., req_001)
    agent: str                               # Agent name (e.g., PatientDataAgent, DLPredictionAgent)
    status: str                              # Execution status: "ok", "error", "flagged"
    payload: Dict[str, Any]                  # Structured output payload
    evidence: List[str] = field(default_factory=list)  # Retrieved sources or clinical rationale
    model_version: str = "v1.0"              # Model or agent version

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def create(cls, request_id: str, agent: str, status: str, payload: Dict[str, Any],
               evidence: Optional[List[str]] = None, version: str = "v1.0") -> 'AgentMessage':
        return cls(
            id=request_id,
            agent=agent,
            status=status,
            payload=payload,
            evidence=evidence or [],
            model_version=version
        )


@dataclass
class DecisionSupportReport:
    """Structured Decision-Support Report matching Figure 1 and Section 2.2:
    Prediction + Evidence + Limitations
    """
    request_id: str
    timestamp: str
    prediction: Dict[str, Any]
    rule_results: Dict[str, Any]
    evidence: Dict[str, Any]
    explanation: Dict[str, Any]
    simulation: Optional[Dict[str, Any]]
    monitoring: Dict[str, Any]
    agent_messages: List[Dict[str, Any]]
    safety_limitations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
