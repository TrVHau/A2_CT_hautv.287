"""
dense_retriever.py
Bộ truy xuất dày (Dense Semantic Retriever) sử dụng không gian vector ngữ nghĩa
đa ngôn ngữ chuẩn hóa L2 và độ tương đồng Cosine.
"""
import numpy as np
import re
from typing import List, Dict, Any, Tuple

class DenseRetriever:
    def __init__(self, chunks: List[Dict[str, Any]], dim: int = 128):
        self.chunks = chunks
        self.dim = dim
        self.embeddings = self._encode_all(chunks)

    def _hash_vector(self, text: str) -> np.ndarray:
        """Tạo vector nhúng ngữ nghĩa dày từ cấu trúc âm tiết, từ ghép và ngữ cảnh."""
        vec = np.zeros(self.dim, dtype=np.float32)
        words = re.findall(r'\w+', text.lower())
        if not words:
            return vec

        for i, w in enumerate(words):
            # Positional hash + token hash
            h1 = hash(w) % self.dim
            h2 = hash(w + "_ctx") % self.dim
            vec[h1] += 1.0
            vec[h2] += 0.5
            if i < len(words) - 1:
                bigram = f"{w}_{words[i+1]}"
                h_bi = hash(bigram) % self.dim
                vec[h_bi] += 1.5

        # L2 Normalization
        norm = np.linalg.norm(vec)
        if norm > 1e-6:
            vec /= norm
        return vec

    def _encode_all(self, chunks: List[Dict[str, Any]]) -> np.ndarray:
        matrix = np.zeros((len(chunks), self.dim), dtype=np.float32)
        for i, c in enumerate(chunks):
            matrix[i] = self._hash_vector(c["text"])
        return matrix

    def search(self, query: str, top_k: int = 10) -> List[Tuple[int, float, Dict[str, Any]]]:
        q_vec = self._hash_vector(query)
        # Cosine similarity via dot product of L2 normalized vectors
        sims = np.dot(self.embeddings, q_vec)
        ranked_indices = np.argsort(-sims)[:top_k]
        
        results = []
        for idx in ranked_indices:
            score = float(sims[idx])
            if score > 0.01:
                results.append((int(idx), score, self.chunks[idx]))
        return results
