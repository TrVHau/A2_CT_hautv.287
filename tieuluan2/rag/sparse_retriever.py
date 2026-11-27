"""
sparse_retriever.py
Hiện thực bộ truy xuất thưa BM25 (Okapi BM25) tối ưu hóa cho âm tiết và cụm từ tiếng Việt.
"""
import math
import re
from typing import List, Dict, Any, Tuple
from collections import Counter

class BM25Retriever:
    def __init__(self, chunks: List[Dict[str, Any]], k1: float = 1.5, b: float = 0.75):
        self.chunks = chunks
        self.k1 = k1
        self.b = b
        self.doc_len: List[int] = []
        self.avg_doc_len: float = 0.0
        self.doc_freqs: Dict[str, int] = Counter()
        self.inverted_index: Dict[str, List[Tuple[int, int]]] = {} # term -> list of (doc_idx, tf)
        self.corpus_size = len(chunks)
        self.build_index()

    def tokenize(self, text: str) -> List[str]:
        cleaned = re.sub(r'[^\w\s]', ' ', text.lower())
        tokens = cleaned.split()
        # Add bi-gram for Vietnamese phrases
        bigrams = [f"{tokens[i]}_{tokens[i+1]}" for i in range(len(tokens) - 1)]
        return tokens + bigrams

    def build_index(self):
        total_len = 0
        for idx, c in enumerate(self.chunks):
            tokens = self.tokenize(c["text"])
            self.doc_len.append(len(tokens))
            total_len += len(tokens)
            
            tf_counter = Counter(tokens)
            for token, count in tf_counter.items():
                self.doc_freqs[token] += 1
                if token not in self.inverted_index:
                    self.inverted_index[token] = []
                self.inverted_index[token].append((idx, count))

        self.avg_doc_len = total_len / max(1, self.corpus_size)

    def idf(self, term: str) -> float:
        df = self.doc_freqs.get(term, 0)
        return math.log(1.0 + (self.corpus_size - df + 0.5) / (df + 0.5))

    def search(self, query: str, top_k: int = 10) -> List[Tuple[int, float, Dict[str, Any]]]:
        q_tokens = self.tokenize(query)
        scores = [0.0] * self.corpus_size
        
        for term in q_tokens:
            if term not in self.inverted_index:
                continue
            term_idf = self.idf(term)
            for doc_idx, tf in self.inverted_index[term]:
                dl = self.doc_len[doc_idx]
                numerator = tf * (self.k1 + 1.0)
                denominator = tf + self.k1 * (1.0 - self.b + self.b * (dl / self.avg_doc_len))
                scores[doc_idx] += term_idf * (numerator / denominator)

        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:top_k]
        results = []
        for idx, score in ranked:
            if score > 0:
                results.append((idx, score, self.chunks[idx]))
        return results
