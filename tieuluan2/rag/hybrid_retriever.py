"""
hybrid_retriever.py
Bộ truy xuất lai (Hybrid Retriever) hợp nhất thứ hạng BM25 và Dense
theo thuật toán Reciprocal Rank Fusion (RRF k=60).
"""
from typing import List, Dict, Any, Tuple
from .sparse_retriever import BM25Retriever
from .dense_retriever import DenseRetriever

class HybridRRFRetriever:
    def __init__(self, bm25: BM25Retriever, dense: DenseRetriever, k: int = 60):
        self.bm25 = bm25
        self.dense = dense
        self.k = k

    def search(self, query: str, top_k: int = 10, candidate_k: int = 30) -> List[Tuple[int, float, Dict[str, Any]]]:
        bm25_res = self.bm25.search(query, top_k=candidate_k)
        dense_res = self.dense.search(query, top_k=candidate_k)

        rrf_scores: Dict[int, float] = {}

        # Accumulate RRF scores from BM25 ranks
        for rank, (doc_idx, _, _) in enumerate(bm25_res, 1):
            rrf_scores[doc_idx] = rrf_scores.get(doc_idx, 0.0) + (1.0 / (self.k + rank))

        # Accumulate RRF scores from Dense ranks
        for rank, (doc_idx, _, _) in enumerate(dense_res, 1):
            rrf_scores[doc_idx] = rrf_scores.get(doc_idx, 0.0) + (1.0 / (self.k + rank))

        ranked = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        
        results = []
        for doc_idx, score in ranked:
            results.append((doc_idx, score, self.bm25.chunks[doc_idx]))
        return results
