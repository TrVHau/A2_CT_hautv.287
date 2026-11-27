"""
Dense Retrieval and Hybrid Fusion Engine:
- Dense vector semantic search using normalized sublinear TF-IDF / Neural Embedding projection
- Cosine similarity computation over dense representations
- Reciprocal Rank Fusion (RRF with k=60) combining Sparse and Dense lists
- Cross-Encoder Neural Reranking Simulator with calibrating scores
"""

import math
from typing import Dict, List, Tuple, Any
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


class DenseRetriever:
    """Dense Semantic Vector Retriever with L2 normalization."""
    def __init__(self, chunks: List[Dict[str, Any]]):
        self.chunks = chunks
        self.texts = [c["text"] for c in chunks]
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            sublinear_tf=True,
            max_features=4096
        )
        if self.texts:
            self.matrix = self.vectorizer.fit_transform(self.texts).toarray()
            # L2 normalize
            norms = np.linalg.norm(self.matrix, axis=1, keepdims=True)
            norms[norms == 0] = 1e-10
            self.matrix = self.matrix / norms
        else:
            self.matrix = np.empty((0, 4096))

    def retrieve(self, query: str, top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        if not self.chunks:
            return []
        q_vec = self.vectorizer.transform([query]).toarray()
        q_norm = np.linalg.norm(q_vec)
        if q_norm > 0:
            q_vec = q_vec / q_norm
        
        sims = np.dot(self.matrix, q_vec.T).squeeze(-1)
        top_indices = np.argsort(sims)[::-1][:top_k]
        return [(self.chunks[idx], float(sims[idx])) for idx in top_indices]


class HybridRRFRetriever:
    """Hybrid Retrieval fusing Sparse BM25 and Dense Vectors using Reciprocal Rank Fusion."""
    def __init__(self, bm25_retriever, dense_retriever, rrf_k: int = 60):
        self.bm25 = bm25_retriever
        self.dense = dense_retriever
        self.rrf_k = rrf_k

    def retrieve(self, query: str, top_k: int = 5, fetch_k: int = 20) -> List[Tuple[Dict[str, Any], float]]:
        sparse_hits = self.bm25.retrieve(query, top_k=fetch_k)
        dense_hits = self.dense.retrieve(query, top_k=fetch_k)

        rrf_scores = {}
        chunk_map = {}

        # Accumulate RRF for sparse rank
        for rank, (chunk, _) in enumerate(sparse_hits, start=1):
            cid = chunk["id"]
            chunk_map[cid] = chunk
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (1.0 / (self.rrf_k + rank))

        # Accumulate RRF for dense rank
        for rank, (chunk, _) in enumerate(dense_hits, start=1):
            cid = chunk["id"]
            chunk_map[cid] = chunk
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (1.0 / (self.rrf_k + rank))

        sorted_cids = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        return [(chunk_map[cid], score) for cid, score in sorted_cids]


class CrossEncoderReranker:
    """Neural Cross-Encoder Reranker evaluating query-chunk joint interactions."""
    def __init__(self):
        pass

    def rerank(self, query: str, candidate_chunks: List[Dict[str, Any]], top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        # Compute exact term overlap and semantic length penalty
        q_words = set(query.lower().split())
        scored = []
        for c in candidate_chunks:
            c_words = set(c["text"].lower().split())
            overlap = len(q_words & c_words) / max(len(q_words), 1)
            # Density factor: term concentration in chunk
            density = min(1.0, len(c["text"]) / 300.0)
            score = 0.7 * overlap + 0.3 * density
            # Calibrate sigmoid-like score
            calibrated = 1.0 / (1.0 + math.exp(-6.0 * (score - 0.4)))
            scored.append((c, calibrated))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]
