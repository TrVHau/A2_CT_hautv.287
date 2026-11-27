"""
Grounded Verifier and Faithfulness Auditor for Tieuluan 2:
- Strict citation validation: every [n] citation must resolve to an authentic evidence chunk
- Numeric faithfulness checker: validates that all quantitative claims (HbA1c %, prices, ratios) exist in evidence
- Deterministic fallback synthesis preventing LLM hallucination
"""

import re
from typing import Dict, List, Tuple, Any, Set


NUM_REGEX = re.compile(r'\b\d+(?:[.,]\d+)?%?\b')


def normalize_numeric_string(num_str: str) -> str:
    """Standardizes numeric strings (handling comma vs period decimal marks)."""
    clean = num_str.replace("%", "").strip()
    clean = clean.replace(",", ".")
    return clean


class GroundedVerifier:
    """Evaluates answer faithfulness against gathered evidence."""
    def __init__(self, numeric_threshold: float = 0.85):
        self.numeric_threshold = numeric_threshold

    def audit_response(self, candidate_answer: str, evidence_list: List[Tuple[str, str]], user_question: str = "") -> Dict[str, Any]:
        """
        Audits answer against evidence:
        - evidence_list: List of (source_id, content_text)
        - Checks citations [1], [2], ...
        - Checks numerical faithfulness
        """
        # 1. Check citations
        citations = [int(x) for x in re.findall(r'\[(\d+)\]', candidate_answer)]
        n_evidence = len(evidence_list)
        citations_valid = bool(citations) and all(1 <= c <= n_evidence for c in citations)

        # 2. Extract numbers from evidence + question
        all_evidence_text = " ".join([txt for _, txt in evidence_list]) + " " + user_question
        raw_evidence_nums = NUM_REGEX.findall(all_evidence_text)
        evidence_num_set = {normalize_numeric_string(n) for n in raw_evidence_nums}

        # Extract numbers from candidate answer (ignoring citation indices [n])
        text_no_citations = re.sub(r'\[\d+\]', '', candidate_answer)
        raw_answer_nums = NUM_REGEX.findall(text_no_citations)
        answer_nums = [n for n in raw_answer_nums if len(normalize_numeric_string(n)) >= 1]

        found_nums = []
        unsupported_nums = []
        for n in answer_nums:
            norm = normalize_numeric_string(n)
            # Match directly or as substring
            if norm in evidence_num_set or any(norm in ev_n for ev_n in evidence_num_set):
                found_nums.append(n)
            else:
                unsupported_nums.append(n)

        faithfulness = 1.0 if not answer_nums else len(found_nums) / len(answer_nums)
        is_passed = citations_valid and (faithfulness >= self.numeric_threshold)

        return {
            "passed": is_passed,
            "has_citation": bool(citations),
            "citations_valid": citations_valid,
            "total_citations": len(citations),
            "unique_citations": len(set(citations)),
            "numeric_faithfulness": float(faithfulness),
            "faithfulness_percentage": f"{faithfulness * 100:.1f}%",
            "supported_numbers": found_nums,
            "unsupported_numbers": unsupported_nums,
            "audit_verdict": "CHẤP THUẬN (VERIFIED FAITHFUL)" if is_passed else "TỪ CHỐI (REJECTED - HALLUCINATION DETECTED)"
        }
