"""
Sparse Retrieval Engine for Vietnamese Technical Texts:
- Vietnamese Syllable Tokenization
- BM25 Okapi Algorithm with k1=1.5, b=0.75
- Inverted Index and Document Length Normalization
"""

import math
import re
from typing import Dict, List, Tuple, Any
import collections


def tokenize_vietnamese(text: str) -> List[str]:
    """Tokenizes Vietnamese text into normalized lower-case syllables/tokens."""
    tokens = re.findall(r'[\w]+', text.lower())
    # Filter short stop characters
    return [t for t in tokens if len(t) > 1 or t in ["f", "e", "s", "p"]]


class BM25Retriever:
    """Production BM25 Okapi retrieval implementation."""
    def __init__(self, chunks: List[Dict[str, Any]], k1: float = 1.5, b: float = 0.75):
        self.chunks = chunks
        self.k1 = k1
        self.b = b
        self.N = len(chunks)
        self.doc_lens = [len(tokenize_vietnamese(c["text"])) for c in chunks]
        self.avgdl = sum(self.doc_lens) / max(self.N, 1)

        # Build Inverted Index and Term Frequencies
        self.inverted_index = collections.defaultdict(dict)
        self.df = collections.defaultdict(int)

        for doc_idx, c in enumerate(chunks):
            tokens = tokenize_vietnamese(c["text"])
            counts = collections.Counter(tokens)
            for t, cnt in counts.items():
                self.inverted_index[t][doc_idx] = cnt
                self.df[t] += 1

        # Calculate IDF for each term
        self.idf = {}
        for t, freq in self.df.items():
            # Standard Robertson-Spärck Jones IDF
            self.idf[t] = math.log((self.N - freq + 0.5) / (freq + 0.5) + 1.0)

    def retrieve(self, query: str, top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        q_tokens = tokenize_vietnamese(query)
        scores = collections.defaultdict(float)

        for t in q_tokens:
            if t not in self.inverted_index:
                continue
            idf_val = self.idf[t]
            for doc_idx, tf in self.inverted_index[t].items():
                dl = self.doc_lens[doc_idx]
                numerator = tf * (self.k1 + 1.0)
                denominator = tf + self.k1 * (1.0 - self.b + self.b * (dl / self.avgdl))
                scores[doc_idx] += idf_val * (numerator / denominator)

        sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        return [(self.chunks[doc_idx], score) for doc_idx, score in sorted_docs]
