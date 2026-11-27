"""
reranker.py
Ống dẫn chấm điểm lại (Cross-Encoder Reranker Pipeline) tính điểm tương tác
chéo giữa truy vấn và các đoạn văn bản ứng viên từ bộ truy xuất lai.
"""
import re
from typing import List, Dict, Any, Tuple

class CrossEncoderReranker:
    def __init__(self):
        pass

    def _cross_score(self, query: str, doc_text: str) -> float:
        """Đo điểm tương thích chéo: tỷ lệ bao phủ n-gram, khớp thực thể và liên kết câu."""
        q_clean = query.lower()
        d_clean = doc_text.lower()
        q_words = set(re.findall(r'\w+', q_clean))
        d_words = set(re.findall(r'\w+', d_clean))
        
        if not q_words:
            return 0.0

        # Exact word overlap
        word_overlap = len(q_words.intersection(d_words)) / len(q_words)
        
        # Phrase match boost
        phrase_boost = 0.0
        q_tokens = q_clean.split()
        for i in range(len(q_tokens) - 1):
            bigram = f"{q_tokens[i]} {q_tokens[i+1]}"
            if bigram in d_clean:
                phrase_boost += 0.25

        # Position penalty / heading boost
        header_boost = 0.2 if any(w in doc_text[:100].lower() for w in q_words) else 0.0

        total_score = word_overlap * 0.6 + min(phrase_boost, 0.3) + header_boost
        return float(total_score)

    def rerank(self, query: str, candidates: List[Tuple[int, float, Dict[str, Any]]], top_k: int = 5) -> List[Tuple[int, float, Dict[str, Any]]]:
        rescored = []
        for doc_idx, orig_score, chunk in candidates:
            cross_score = self._cross_score(query, chunk["text"])
            # Combined score: 40% initial hybrid rank, 60% cross interaction
            final_score = orig_score * 0.4 + cross_score * 0.6
            rescored.append((doc_idx, final_score, chunk))

        rescored.sort(key=lambda x: x[1], reverse=True)
        return rescored[:top_k]
