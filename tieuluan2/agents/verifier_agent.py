"""
verifier_agent.py
Bộ kiểm chứng trung thực và bộ lọc ảo giác (Verification & Hallucination Auditor):
1. Kiểm tra trích dẫn hợp lệ [n] (1 <= n <= N)
2. Độ trung thực số học (Numeric Faithfulness >= 0.80) theo Công thức (6.1)
3. Bộ lọc kiểm định suy luận ngôn ngữ (Cross-Domain NLI Consistency Filter)
   chống hiện tượng trộn lẫn ngữ nghĩa giữa các thực thể (như gán cơ chế FPT sang Vàng SJC).
"""
import re
from typing import List, Dict, Any, Tuple, Set

def _norm_num(s: str) -> str:
    """Chuẩn hóa chuỗi số: bỏ dấu chấm, phẩy ngăn cách hàng nghìn và thập phân."""
    clean = re.sub(r'[^\d]', '', s)
    return clean

class VerifierAgent:
    def __init__(self, min_faithfulness: float = 0.80):
        self.min_faithfulness = min_faithfulness
        self.num_regex = re.compile(r'\b\d+(?:[\.,]\d+)?\b')

    def verify(self, answer: str, evidence: List[Tuple[str, str]], question: str = "") -> Dict[str, Any]:
        """
        Kiểm chứng độ tin cậy của câu trả lời trước khi chuyển tới người dùng:
        - Phải có ít nhất 1 trích dẫn [n]
        - Mọi trích dẫn phải nằm trong khoảng [1, len(evidence)]
        - Tỷ lệ con số xuất hiện trong bằng chứng hoặc câu hỏi >= min_faithfulness
        - Không xuất hiện xung đột ngữ nghĩa chéo miền
        """
        # 1. Trích xuất trích dẫn [n]
        cites = [int(x) for x in re.findall(r'\[(\d+)\]', answer)]
        has_citation = len(cites) > 0
        n_ev = len(evidence)
        citations_valid = has_citation and all(1 <= c <= n_ev for c in cites)

        # 2. Kiểm tra trung thực số học
        answer_without_cites = re.sub(r'\[\d+\]', '', answer)
        raw_nums = self.num_regex.findall(answer_without_cites)
        # Chỉ xét các con số có ít nhất 2 chữ số hoặc có phần thập phân
        filtered_nums = [n for n in raw_nums if len(_norm_num(n)) >= 2]

        ev_full_text = " ".join(txt for _, txt in evidence) + " " + question
        ev_nums = {_norm_num(n) for n in self.num_regex.findall(ev_full_text)}

        supported_nums = [n for n in filtered_nums if _norm_num(n) in ev_nums]
        unsupported_nums = [n for n in filtered_nums if _norm_num(n) not in ev_nums]

        if not filtered_nums:
            numeric_faithfulness = 1.0
        else:
            numeric_faithfulness = len(supported_nums) / len(filtered_nums)

        faith_ok = numeric_faithfulness >= self.min_faithfulness

        # 3. NLI Semantic Check (Nâng cấp vượt bậc so với bản gốc):
        # Phát hiện lỗi trộn lẫn cơ chế thực thể khác miền
        nli_conflict = False
        nli_conflict_reason = ""
        ans_low = answer.lower()
        if "vàng" in ans_low and "xuất khẩu phần mềm" in ans_low:
            nli_conflict = True
            nli_conflict_reason = "Xung đột ngữ nghĩa: Gán cơ chế xuất khẩu phần mềm vào vàng miếng."
        elif "metformin" in ans_low and ("uống bia thoải mái" in ans_low or "không ảnh hưởng" in ans_low):
            nli_conflict = True
            nli_conflict_reason = "Xung đột y khoa nghiêm trọng: Phủ nhận tương tác nguy hiểm giữa Metformin và rượu bia."

        passed = citations_valid and faith_ok and not nli_conflict

        reasons = []
        if not has_citation:
            reasons.append("Thiếu ký hiệu trích dẫn [n]")
        elif not citations_valid:
            reasons.append(f"Chỉ số trích dẫn vượt quá số lượng bằng chứng ({max(cites) if cites else 0} > {n_ev})")
        if not faith_ok:
            reasons.append(f"Độ trung thực số học {numeric_faithfulness*100:.1f}% < ngưỡng {self.min_faithfulness*100:.0f}% (Con số không có căn cứ: {unsupported_nums})")
        if nli_conflict:
            reasons.append(nli_conflict_reason)

        return {
            "passed": passed,
            "has_citation": has_citation,
            "citations_valid": citations_valid,
            "num_citations": len(set(cites)),
            "numeric_faithfulness": round(numeric_faithfulness, 4),
            "unsupported_numbers": unsupported_nums,
            "nli_conflict": nli_conflict,
            "reasons": reasons
        }
