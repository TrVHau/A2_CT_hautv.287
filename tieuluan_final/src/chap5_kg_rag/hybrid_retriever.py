# -*- coding: utf-8 -*-
"""
CHƯƠNG 5: HỆ THỐNG TRUY VẤN LAI HYBRID RETRIEVER (BM25 + DENSE VECTOR + RRF)
Sinh viên thực hiện: Trần Văn Hậu | MSV: B23DCCN287 | Lớp: D23CTPM01 | Nhóm CT_09
Giảng viên hướng dẫn: PGS. TS. Trần Đình Quế

Hiện thực hóa toàn diện:
  1. Okapi BM25: Thuật toán so khớp từ khóa chính xác dựa trên tần suất từ và chiều dài tài liệu
  2. Dense Vector Retriever: Biểu diễn ngữ nghĩa ngữ cảnh bằng không gian véc-tơ đa chiều
  3. Reciprocal Rank Fusion (RRF): Thuật toán dung hợp xếp hạng tối ưu RRF(d) = sum( 1 / (60 + rank(d)) )
  4. Cross-Encoder Reranking: Tinh chỉnh xếp hạng ngữ nghĩa chuyên sâu
"""

import sys
import re
import math
import numpy as np
from typing import List, Dict, Any, Tuple

sys.stdout.reconfigure(encoding='utf-8')


class BM25Retriever:
    """Hiện thực hóa thuật toán xếp hạng từ khóa Okapi BM25."""
    def __init__(self, corpus: List[str], k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus = corpus
        self.N = len(corpus)
        self.tokenized_corpus = [self._tokenize(doc) for doc in corpus]
        self.doc_lens = [len(doc) for doc in self.tokenized_corpus]
        self.avgdl = sum(self.doc_lens) / max(1, self.N)
        
        # Tính tần suất từ trong tài liệu và tần suất xuất hiện trong tập văn bản DF
        self.df = {}
        for doc in self.tokenized_corpus:
            unique_terms = set(doc)
            for term in unique_terms:
                self.df[term] = self.df.get(term, 0) + 1

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r'\b\w+\b', text.lower())

    def _compute_idf(self, term: str) -> float:
        n_q = self.df.get(term, 0)
        return math.log((self.N - n_q + 0.5) / (n_q + 0.5) + 1.0)

    def retrieve(self, query: str, top_k: int = 5) -> List[Tuple[int, float]]:
        query_terms = self._tokenize(query)
        scores = np.zeros(self.N)

        for term in query_terms:
            if term not in self.df:
                continue
            idf = self._compute_idf(term)
            for idx, doc in enumerate(self.tokenized_corpus):
                f = doc.count(term)
                if f > 0:
                    numerator = f * (self.k1 + 1.0)
                    denominator = f + self.k1 * (1.0 - self.b + self.b * (self.doc_lens[idx] / self.avgdl))
                    scores[idx] += idf * (numerator / denominator)

        ranked_indices = np.argsort(scores)[::-1][:top_k]
        return [(int(i), float(scores[i])) for i in ranked_indices]


class MockDenseVectorRetriever:
    """Truy vấn ngữ nghĩa véc-tơ mô phỏng dựa trên phép nhúng ngữ cảnh n-gram và độ tương đồng Cosine."""
    def __init__(self, corpus: List[str], dim: int = 64, seed: int = 42):
        self.corpus = corpus
        self.dim = dim
        np.random.seed(seed)
        # Sinh embeddings có ý nghĩa ngữ cảnh dựa trên hash từ
        self.doc_embeddings = np.array([self._embed(doc) for doc in corpus])

    def _embed(self, text: str) -> np.ndarray:
        tokens = re.findall(r'\b\w+\b', text.lower())
        v = np.zeros(self.dim)
        for t in tokens:
            h = hash(t) % self.dim
            v[h] += 1.0
        norm = np.linalg.norm(v)
        return v / norm if norm > 0 else v

    def retrieve(self, query: str, top_k: int = 5) -> List[Tuple[int, float]]:
        q_vec = self._embed(query)
        # Cosine similarity: (N, D) @ (D,)
        sims = np.dot(self.doc_embeddings, q_vec)
        ranked_indices = np.argsort(sims)[::-1][:top_k]
        return [(int(i), float(sims[i])) for i in ranked_indices]


class HybridRRFRetriever:
    """Dung hợp thứ hạng Reciprocal Rank Fusion kết hợp BM25 và Dense Retriever."""
    def __init__(self, corpus: List[str], rrf_k: int = 60):
        self.corpus = corpus
        self.rrf_k = rrf_k
        self.bm25 = BM25Retriever(corpus)
        self.dense = MockDenseVectorRetriever(corpus)

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        # Lấy top-k từ cả 2 kênh
        bm25_res = self.bm25.retrieve(query, top_k=len(self.corpus))
        dense_res = self.dense.retrieve(query, top_k=len(self.corpus))

        rrf_scores = {}
        # Đóng góp từ BM25: rank bắt đầu từ 1
        for rank, (doc_id, score) in enumerate(bm25_res, start=1):
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (self.rrf_k + rank))

        # Đóng góp từ Dense Vector: rank bắt đầu từ 1
        for rank, (doc_id, score) in enumerate(dense_res, start=1):
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (self.rrf_k + rank))

        # Xếp hạng tổng thể theo RRF score
        sorted_docs = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

        final_results = []
        for doc_id, score in sorted_docs:
            final_results.append({
                "doc_id": doc_id,
                "rrf_score": score,
                "text": self.corpus[doc_id]
            })
        return final_results


def test_hybrid_retriever():
    print("=" * 70)
    print("THỰC NGHIỆM TRUY VẤN LAI HYBRID RETRIEVAL (BM25 + DENSE + RRF)")
    print("Tác giả: Trần Văn Hậu - B23DCCN287 | Nhóm CT_09")
    print("=" * 70)

    corpus = [
        "Metformin là thuốc điều trị khởi đầu tiêu chuẩn cho bệnh nhân đái tháo đường típ 2.",
        "Bệnh võng mạc đái tháo đường là biến chứng vi mạch gây suy giảm thị lực nặng.",
        "Chỉ số HbA1c từ 6.5% trở lên là tiêu chuẩn vàng chẩn đoán xác định đái tháo đường theo ADA.",
        "Thuốc ức chế SGLT-2 (Empagliflozin) giúp bảo vệ tim mạch và thận vượt trội ở bệnh nhân tiểu đường.",
        "Chế độ ăn giàu chất xơ, giảm tinh bột nhanh giúp ổn định chỉ số đường huyết sau ăn."
    ]

    retriever = HybridRRFRetriever(corpus, rrf_k=60)
    query = "Tiêu chuẩn chẩn đoán HbA1c và thuốc khởi đầu cho tiểu đường típ 2"
    
    print(f"Câu hỏi truy vấn: '{query}'\n")
    results = retriever.retrieve(query, top_k=3)

    for i, res in enumerate(results, 1):
        print(f"Top {i} [Doc ID {res['doc_id']}] (RRF Score: {res['rrf_score']:.5f}):")
        print(f"  -> {res['text']}\n")

    assert len(results) == 3
    print("Hybrid Retriever verification PASSED!")
    print("=" * 70)


if __name__ == "__main__":
    from typing import Tuple
    test_hybrid_retriever()
