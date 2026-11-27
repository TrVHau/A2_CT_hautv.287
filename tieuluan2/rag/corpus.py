"""
corpus.py
Quản lý nạp kho văn bản đa miền (Y tế & Tài chính), áp dụng các chiến lược
phân mảnh và đánh chỉ mục ngữ nghĩa.
"""
import os
import glob
from typing import List, Dict, Any
from .chunking import chunk_parent_child, chunk_recursive

class DocumentCorpus:
    def __init__(self, doc_dir: str = "tieuluan2/data/documents"):
        self.doc_dir = doc_dir
        self.raw_docs: Dict[str, str] = {}
        self.chunks: List[Dict[str, Any]] = []
        self.load_all()

    def load_all(self):
        file_paths = glob.glob(os.path.join(self.doc_dir, "*.txt"))
        for p in file_paths:
            fname = os.path.basename(p)
            with open(p, "r", encoding="utf-8") as f:
                content = f.read()
            self.raw_docs[fname] = content
            domain = "health" if fname.startswith("h") else "finance"
            
            # Use Parent-Child / Recursive as standard high-performance chunking
            doc_chunks = chunk_parent_child(content)
            for c in doc_chunks:
                c["doc_id"] = fname
                c["domain"] = domain
                self.chunks.append(c)

        print(f"Loaded {len(self.raw_docs)} documents, created {len(self.chunks)} structured chunks.")

    def get_chunk(self, chunk_id: str) -> Dict[str, Any]:
        for c in self.chunks:
            if c["chunk_id"] == chunk_id:
                return c
        return {}
