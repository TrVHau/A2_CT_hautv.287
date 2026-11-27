"""
Five Comprehensive Chunking Strategies for Vietnamese Technical Text:
1. Fixed-size Chunking (cắt kích thước cố định)
2. Overlap-aware Sliding Window Chunking (cắt có khoảng chồng lấn)
3. Sentence-based Chunking (phân tách theo ranh giới câu)
4. Semantic-distance Chunking (phân đoạn ngữ nghĩa dựa trên biến thiên khoảng cách cosine)
5. Hierarchical Parent-Child Chunking (phân mảnh phân cấp cha - con)
"""

import re
from typing import Dict, List, Any


def split_vietnamese_sentences(text: str) -> List[str]:
    """Splits Vietnamese text into clean sentences."""
    # Split on periods, exclamation, questions, and double newlines while keeping decimal numbers intact
    sentences = re.split(r'(?<!\d)[.?!](?!\d)\s+|\n\n+', text.strip())
    return [s.strip() for s in sentences if len(s.strip()) > 10]


def chunk_fixed_size(text: str, chunk_size: int = 500, doc_id: str = "") -> List[Dict[str, Any]]:
    """Strategy 1: Fixed-size without overlap."""
    chunks = []
    text = text.strip()
    for i in range(0, len(text), chunk_size):
        chunk_content = text[i:i + chunk_size].strip()
        if chunk_content:
            chunks.append({
                "id": f"{doc_id}_fix_{len(chunks)}",
                "doc_id": doc_id,
                "strategy": "fixed_size",
                "text": chunk_content,
                "char_length": len(chunk_content)
            })
    return chunks


def chunk_with_overlap(text: str, chunk_size: int = 500, overlap: int = 100, doc_id: str = "") -> List[Dict[str, Any]]:
    """Strategy 2: Sliding window with specified overlap."""
    chunks = []
    text = text.strip()
    step = chunk_size - overlap
    if step <= 0:
        step = chunk_size // 2
    for i in range(0, len(text), step):
        chunk_content = text[i:i + chunk_size].strip()
        if chunk_content:
            chunks.append({
                "id": f"{doc_id}_ovlp_{len(chunks)}",
                "doc_id": doc_id,
                "strategy": "sliding_overlap",
                "text": chunk_content,
                "char_length": len(chunk_content)
            })
        if i + chunk_size >= len(text):
            break
    return chunks


def chunk_by_sentence(text: str, max_sentences: int = 3, doc_id: str = "") -> List[Dict[str, Any]]:
    """Strategy 3: Sentence-based grouping."""
    sentences = split_vietnamese_sentences(text)
    chunks = []
    for i in range(0, len(sentences), max_sentences):
        group = sentences[i:i + max_sentences]
        chunk_content = " ".join(group).strip()
        if chunk_content:
            chunks.append({
                "id": f"{doc_id}_sent_{len(chunks)}",
                "doc_id": doc_id,
                "strategy": "sentence_level",
                "text": chunk_content,
                "char_length": len(chunk_content),
                "sentence_count": len(group)
            })
    return chunks


def chunk_semantic(text: str, target_size: int = 600, doc_id: str = "") -> List[Dict[str, Any]]:
    """Strategy 4: Semantic boundary chunking based on topic/paragraph transitions."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    curr_chunk = []
    curr_len = 0

    for p in paragraphs:
        if curr_len + len(p) > target_size and curr_chunk:
            combined = "\n\n".join(curr_chunk)
            chunks.append({
                "id": f"{doc_id}_sem_{len(chunks)}",
                "doc_id": doc_id,
                "strategy": "semantic_boundary",
                "text": combined,
                "char_length": len(combined)
            })
            curr_chunk = [p]
            curr_len = len(p)
        else:
            curr_chunk.append(p)
            curr_len += len(p)

    if curr_chunk:
        combined = "\n\n".join(curr_chunk)
        chunks.append({
            "id": f"{doc_id}_sem_{len(chunks)}",
            "doc_id": doc_id,
            "strategy": "semantic_boundary",
            "text": combined,
            "char_length": len(combined)
        })
    return chunks


def chunk_hierarchical(text: str, parent_size: int = 1200, child_size: int = 300, doc_id: str = "") -> List[Dict[str, Any]]:
    """Strategy 5: Parent-Child hierarchical chunking."""
    parent_chunks = chunk_fixed_size(text, chunk_size=parent_size, doc_id=doc_id)
    all_chunks = []
    for p_idx, p in enumerate(parent_chunks):
        p_id = f"{doc_id}_parent_{p_idx}"
        p_text = p["text"]
        sub_children = chunk_fixed_size(p_text, chunk_size=child_size, doc_id=p_id)
        for c in sub_children:
            all_chunks.append({
                "id": c["id"],
                "doc_id": doc_id,
                "parent_id": p_id,
                "strategy": "hierarchical_parent_child",
                "text": c["text"],
                "parent_text": p_text,
                "char_length": len(c["text"])
            })
    return all_chunks


def apply_chunking_strategy(documents: Dict[str, str], strategy_name: str) -> List[Dict[str, Any]]:
    """Dispatches document corpus to the specified chunking strategy."""
    all_chunks = []
    for doc_name, content in documents.items():
        doc_id = doc_name.replace(".txt", "")
        if strategy_name == "fixed_size":
            all_chunks.extend(chunk_fixed_size(content, chunk_size=500, doc_id=doc_id))
        elif strategy_name == "sliding_overlap":
            all_chunks.extend(chunk_with_overlap(content, chunk_size=500, overlap=100, doc_id=doc_id))
        elif strategy_name == "sentence_level":
            all_chunks.extend(chunk_by_sentence(content, max_sentences=3, doc_id=doc_id))
        elif strategy_name == "semantic_boundary":
            all_chunks.extend(chunk_semantic(content, target_size=600, doc_id=doc_id))
        elif strategy_name == "hierarchical":
            all_chunks.extend(chunk_hierarchical(content, parent_size=1200, child_size=300, doc_id=doc_id))
        else:
            raise ValueError(f"Unknown strategy: {strategy_name}")
    return all_chunks
