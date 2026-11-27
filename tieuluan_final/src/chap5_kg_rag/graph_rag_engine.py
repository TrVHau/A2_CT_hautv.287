# -*- coding: utf-8 -*-
"""
CHƯƠNG 5: ĐỘNG CƠ TRUY VẤN GRAPH-RAG SUY LUẬN ĐA BƯỚC (MULTI-HOP GRAPH-RAG ENGINE)
Sinh viên thực hiện: Trần Văn Hậu | MSV: B23DCCN287 | Lớp: D23CTPM01 | Nhóm CT_09
Giảng viên hướng dẫn: PGS. TS. Trần Đình Quế

GraphRAG tích hợp 2 luồng:
  1. Luồng phi cấu trúc: Hybrid Retrieval (BM25 + Dense RRF) trích xuất đoạn văn bản liên quan
  2. Luồng có cấu trúc: Knowledge Graph Cypher Expansion trích xuất thực thể, mối quan hệ, chống chỉ định
  3. Context Synthesizer: Hợp nhất ngữ cảnh và sinh câu trả lời lâm sàng có trích dẫn minh bạch
"""

import sys
import json
from typing import Dict, Any, List
from neo4j_ontology import InMemoryClinicalKnowledgeGraph
from hybrid_retriever import HybridRRFRetriever

sys.stdout.reconfigure(encoding='utf-8')


class GraphRAGEngine:
    """Động cơ GraphRAG hợp nhất tri thức đồ thị và tài liệu phi cấu trúc."""
    def __init__(self, corpus: List[str]):
        self.kg = InMemoryClinicalKnowledgeGraph()
        self.retriever = HybridRRFRetriever(corpus)

    def extract_clinical_entities(self, query: str) -> List[str]:
        """Trích xuất thực thể y tế từ câu hỏi của người dùng."""
        known_symptoms = ["Polydipsia", "Polyuria", "Fatigue", "Blurred_Vision"]
        # So khớp đơn giản
        q_lower = query.lower()
        extracted = []
        if "khát nước" in q_lower or "uống nhiều" in q_lower or "polydipsia" in q_lower:
            extracted.append("Polydipsia")
        if "tiểu nhiều" in q_lower or "polyuria" in q_lower:
            extracted.append("Polyuria")
        if "mệt mỏi" in q_lower or "fatigue" in q_lower:
            extracted.append("Fatigue")
        if "mờ mắt" in q_lower or "blurred_vision" in q_lower:
            extracted.append("Blurred_Vision")
        return extracted if extracted else ["Polydipsia", "Polyuria"]

    def answer_query(self, query: str) -> Dict[str, Any]:
        """Thực thi quy trình GraphRAG hoàn chỉnh."""
        # 1. Trích xuất thực thể & truy vấn tri thức cấu trúc từ KG
        entities = self.extract_clinical_entities(query)
        kg_reasoning = self.kg.query_multihop_reasoning(entities)

        # 2. Truy vấn tài liệu liên quan từ Hybrid Retriever
        unstructured_docs = self.retriever.retrieve(query, top_k=2)

        # 3. Tổng hợp ngữ cảnh kiểm chứng (Grounded Context)
        context_parts = []
        context_parts.append("=== DỮ LIỆU ĐỒ THỊ TRI THỨC CẤU TRÚC (KNOWLEDGE GRAPH) ===")
        for res in kg_reasoning:
            context_parts.append(f"- Chẩn đoán tiềm năng: {res['disease']} (Khớp {res['match_score']*100:.0f}% triệu chứng)")
            context_parts.append(f"  + Thuốc chỉ định: {', '.join(res['recommended_drugs'])}")
            if res['contraindications']:
                context_parts.append(f"  + CẢNH BÁO CHỐNG CHỈ ĐỊNH: {'; '.join(res['contraindications'])}")
            if res['potential_complications']:
                context_parts.append(f"  + Nguy cơ biến chứng dài hạn: {', '.join(res['potential_complications'])}")

        context_parts.append("\n=== TÀI LIỆU HƯỚNG DẪN LÂM SÀNG (HYBRID RETRIEVAL) ===")
        for doc in unstructured_docs:
            context_parts.append(f"- [Tài liệu #{doc['doc_id']}] (RRF Score: {doc['rrf_score']:.4f}): {doc['text']}")

        final_context = "\n".join(context_parts)

        # 4. Sinh phản hồi lâm sàng đã kiểm chứng
        synthesis = f"""Dựa trên tổng hợp thông tin đối chiếu giữa Đồ thị Tri thức Y tế và Hướng dẫn Lâm sàng:
1. Triệu chứng lâm sàng ({', '.join(entities)}) có mức tương thích cao với bệnh lý {kg_reasoning[0]['disease']}.
2. Phác đồ điều trị khuyến nghị bậc 1: {', '.join(kg_reasoning[0]['recommended_drugs'])}.
3. Cảnh báo an toàn người bệnh: {kg_reasoning[0]['contraindications'][0] if kg_reasoning[0]['contraindications'] else 'Không phát hiện chống chỉ định tuyệt đối'}.
4. Khuyến nghị dự phòng biến chứng: Cần tầm soát định kỳ {', '.join(kg_reasoning[0]['potential_complications'])}."""

        return {
            "query": query,
            "extracted_entities": entities,
            "kg_results": kg_reasoning,
            "retrieved_docs": unstructured_docs,
            "grounded_context": final_context,
            "clinical_response": synthesis
        }


def test_graph_rag():
    print("=" * 75)
    print("THỰC THI TRUY VẤN GRAPH-RAG HỢP NHẤT TRI THỨC ĐA BƯỚC")
    print("Tác giả: Trần Văn Hậu - B23DCCN287 | Nhóm CT_09")
    print("=" * 75)

    guidelines = [
        "Metformin là thuốc khởi đầu tiêu chuẩn cho Đái tháo đường típ 2, chống chỉ định khi eGFR < 30 mL/phút.",
        "Bệnh nhân có triệu chứng ăn nhiều, uống nhiều, tiểu nhiều và sụt cân cần làm xét nghiệm đường huyết ngay.",
        "Empagliflozin là thuốc ức chế SGLT2 giúp giảm biến cố tim mạch và bảo vệ suy thận tiến triển.",
        "Biến chứng võng mạc tiểu đường cần được soi đáy mắt ít nhất mỗi năm 1 lần."
    ]

    engine = GraphRAGEngine(guidelines)
    query = "Bệnh nhân có biểu hiện khát nước nhiều, tiểu nhiều, hỏi phác đồ điều trị và lưu ý dùng thuốc?"

    result = engine.answer_query(query)
    print(f"Câu hỏi: {result['query']}\n")
    print(f"Thực thể nhận diện: {result['extracted_entities']}\n")
    print(result['grounded_context'])
    print("\n" + "=" * 50)
    print("PHẢN HỒI LÂM SÀNG CỦA GRAPH-RAG:")
    print("=" * 50)
    print(result['clinical_response'])
    print("=" * 75)


if __name__ == "__main__":
    from typing import Tuple
    test_graph_rag()
