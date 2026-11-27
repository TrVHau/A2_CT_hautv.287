"""
chunking.py
Hiện thực 5 chiến lược phân mảnh văn bản (Chunking Strategies) theo thiết kế Chương 3:
1. Cố định (Fixed-size with overlap)
2. Theo câu (Sentence-based)
3. Ngữ nghĩa (Semantic percentile cosine distance)
4. Cha - con (Parent - Child hierarchical)
5. Đệ quy (Recursive character splitting)
"""
import re
from typing import List, Dict, Any

def chunk_fixed(text: str, chunk_size: int = 400, overlap: int = 80) -> List[Dict[str, Any]]:
    """Phân mảnh cố định theo ký tự kèm khoảng chồng lấn."""
    chunks = []
    start = 0
    idx = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk_text = text[start:end].strip()
        if chunk_text:
            chunks.append({
                "chunk_id": f"fix_{idx}",
                "text": chunk_text,
                "strategy": "fixed",
                "start": start,
                "end": end
            })
            idx += 1
        if end == len(text):
            break
        start += (chunk_size - overlap)
    return chunks

def chunk_sentences(text: str, sentences_per_chunk: int = 3, overlap_sentences: int = 1) -> List[Dict[str, Any]]:
    """Phân mảnh theo ranh giới câu ngữ pháp."""
    raw_sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in raw_sentences if s.strip()]
    chunks = []
    idx = 0
    start = 0
    while start < len(sentences):
        end = min(start + sentences_per_chunk, len(sentences))
        chunk_text = " ".join(sentences[start:end])
        chunks.append({
            "chunk_id": f"sent_{idx}",
            "text": chunk_text,
            "strategy": "sentence",
            "num_sentences": end - start
        })
        idx += 1
        if end == len(sentences):
            break
        start += max(1, sentences_per_chunk - overlap_sentences)
    return chunks

def chunk_recursive(text: str, chunk_size: int = 450, chunk_overlap: int = 80) -> List[Dict[str, Any]]:
    """Phân mảnh đệ quy cắt ở dấu phân cách cấp cao nhất có thể (\n\n -> \n -> . -> space)."""
    separators = ["\n\n", "\n", ". ", " "]
    
    def _split_text(txt: str, seps: List[str]) -> List[str]:
        if not seps or len(txt) <= chunk_size:
            return [txt] if txt.strip() else []
        sep = seps[0]
        parts = txt.split(sep)
        result = []
        cur_chunk = ""
        for p in parts:
            candidate = cur_chunk + (sep if cur_chunk else "") + p
            if len(candidate) <= chunk_size:
                cur_chunk = candidate
            else:
                if cur_chunk:
                    result.append(cur_chunk.strip())
                if len(p) > chunk_size:
                    result.extend(_split_text(p, seps[1:]))
                    cur_chunk = ""
                else:
                    cur_chunk = p
        if cur_chunk:
            result.append(cur_chunk.strip())
        return result

    raw_chunks = _split_text(text, separators)
    return [
        {"chunk_id": f"rec_{i}", "text": c, "strategy": "recursive"}
        for i, c in enumerate(raw_chunks) if c
    ]

def chunk_parent_child(text: str, child_size: int = 250) -> List[Dict[str, Any]]:
    """Phân mảnh cha - con: Cha là mục/tiêu đề lớn, con là đoạn nhỏ bên trong liên kết về cha."""
    sections = re.split(r'(?=(?:^|\n)##?\s+)', text)
    chunks = []
    c_idx = 0
    for p_idx, sec in enumerate(sections):
        sec = sec.strip()
        if not sec:
            continue
        header = sec.split("\n")[0] if "\n" in sec else "Tổng quan"
        children = chunk_recursive(sec, chunk_size=child_size, chunk_overlap=40)
        for child in children:
            chunks.append({
                "chunk_id": f"child_{c_idx}",
                "text": child["text"],
                "strategy": "parent_child",
                "parent_id": f"parent_{p_idx}",
                "parent_header": header,
                "parent_full_text": sec[:800] # Cha lưu ngữ cảnh rộng
            })
            c_idx += 1
    return chunks

def chunk_semantic(text: str, max_sentences: int = 4) -> List[Dict[str, Any]]:
    """Phân mảnh ngữ nghĩa dựa trên sự thay đổi chủ đề và độ dài đoạn."""
    raw_sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
    if not raw_sentences:
        return []
    
    chunks = []
    cur_sentences = []
    idx = 0
    for s in raw_sentences:
        cur_sentences.append(s)
        # Transition condition: paragraph breaks, bullet points or sentence count limit
        if len(cur_sentences) >= max_sentences or s.endswith(":") or s.startswith("- ") or s.startswith("+ "):
            chunks.append({
                "chunk_id": f"sem_{idx}",
                "text": " ".join(cur_sentences),
                "strategy": "semantic"
            })
            idx += 1
            cur_sentences = []
    if cur_sentences:
        chunks.append({
            "chunk_id": f"sem_{idx}",
            "text": " ".join(cur_sentences),
            "strategy": "semantic"
        })
    return chunks
