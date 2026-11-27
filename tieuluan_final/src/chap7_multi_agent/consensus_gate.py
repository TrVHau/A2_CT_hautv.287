# -*- coding: utf-8 -*-
"""
CHƯƠNG 7: CỔNG ĐỒNG THUẬN BAYES CÓ TRỌNG SỐ TIN CẬY (CONFIDENCE-WEIGHTED CONSENSUS GATE)
Sinh viên thực hiện: Trần Văn Hậu | MSV: B23DCCN287 | Lớp: D23CTPM01 | Nhóm CT_09
Giảng viên hướng dẫn: PGS. TS. Trần Đình Quế

Công thức toán học của Cổng Đồng Thuận:
  S_{consensus} = sum_{i=1}^M w_i * c_i * I( Vote_i == Vote* ) >= tau = 0.85
  - Nếu S_{consensus} >= 0.85: Kế hoạch được phê duyệt tự động với độ an toàn cao
  - Nếu S_{consensus} < 0.85: Tự động chuyển tuyến (Escalate) lên Bác sĩ lâm sàng cao cấp
"""

import sys
from typing import List, Dict, Any

sys.stdout.reconfigure(encoding='utf-8')


class BayesianConsensusGate:
    """Cổng đồng thuận Bayesian có trọng số tin cậy giữa các tác tử."""
    def __init__(self, threshold: float = 0.85):
        self.threshold = threshold
        # Trọng số vai trò (Role weights tổng = 1.0)
        self.weights = {
            "Diagnostic Specialist": 0.25,
            "Pharmacotherapy Specialist": 0.30,
            "Lifestyle & Nutrition Specialist": 0.15,
            "Critic & Safety Officer": 0.30  # Vai trò an toàn có trọng số cao nhất
        }

    def evaluate_consensus(self, agent_opinions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        agent_opinions: danh sách dict gồm:
          {"agent": role, "vote": "APPROVE" | "REJECT", "confidence": float in [0, 1]}
        """
        # Xác định phương án chiếm đa số phiếu
        votes = [op["vote"] for op in agent_opinions]
        majority_vote = max(set(votes), key=votes.count)

        weighted_score = 0.0
        total_weight = 0.0
        details = []

        for op in agent_opinions:
            role = op["agent"]
            w = self.weights.get(role, 0.20)
            c = op.get("confidence", 0.8)
            is_match = (op["vote"] == majority_vote)
            
            score_contribution = w * c if is_match else 0.0
            weighted_score += score_contribution
            total_weight += w

            details.append({
                "agent": role,
                "vote": op["vote"],
                "confidence": c,
                "weight": w,
                "contribution": round(score_contribution, 3)
            })

        consensus_score = round(weighted_score / total_weight, 3) if total_weight > 0 else 0.0
        is_passed = (consensus_score >= self.threshold) and (majority_vote == "APPROVE")

        status = "TỰ ĐỘNG PHÊ DUYỆT (AUTONOMOUS_APPROVED)" if is_passed else "CHUYỂN TUYẾN HỘI CHẨN BÁC SĨ (ESCALATE_TO_HUMAN)"

        return {
            "majority_vote": majority_vote,
            "consensus_score": consensus_score,
            "threshold": self.threshold,
            "is_passed": is_passed,
            "decision": status,
            "agent_breakdown": details
        }


def test_consensus_gate():
    print("=" * 70)
    print("KIỂM TRA CỔNG ĐỒNG THUẬN BAYES (BAYESIAN CONSENSUS GATE tau = 0.85)")
    print("Tác giả: Trần Văn Hậu - B23DCCN287 | Nhóm CT_09")
    print("=" * 70)

    gate = BayesianConsensusGate(threshold=0.85)

    # Kịch bản 1: Đồng thuận cao
    opinions_pass = [
        {"agent": "Diagnostic Specialist", "vote": "APPROVE", "confidence": 0.95},
        {"agent": "Pharmacotherapy Specialist", "vote": "APPROVE", "confidence": 0.92},
        {"agent": "Lifestyle & Nutrition Specialist", "vote": "APPROVE", "confidence": 0.90},
        {"agent": "Critic & Safety Officer", "vote": "APPROVE", "confidence": 0.98}
    ]
    res1 = gate.evaluate_consensus(opinions_pass)
    print(f"Kịch bản 1 (Đồng thuận cao): Score = {res1['consensus_score']:.3f} | Quyết định: {res1['decision']}")
    assert res1["is_passed"]

    # Kịch bản 2: Critic phủ quyết (Bất đồng thuận)
    opinions_veto = [
        {"agent": "Diagnostic Specialist", "vote": "APPROVE", "confidence": 0.90},
        {"agent": "Pharmacotherapy Specialist", "vote": "APPROVE", "confidence": 0.85},
        {"agent": "Lifestyle & Nutrition Specialist", "vote": "APPROVE", "confidence": 0.80},
        {"agent": "Critic & Safety Officer", "vote": "REJECT", "confidence": 0.99}  # Phủ quyết
    ]
    res2 = gate.evaluate_consensus(opinions_veto)
    print(f"Kịch bản 2 (Critic phủ quyết): Score = {res2['consensus_score']:.3f} | Quyết định: {res2['decision']}")
    assert not res2["is_passed"]

    print("\nBayesian Consensus Gate verification PASSED!")
    print("=" * 70)


if __name__ == "__main__":
    test_consensus_gate()
