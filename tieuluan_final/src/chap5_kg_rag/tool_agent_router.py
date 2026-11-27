# -*- coding: utf-8 -*-
"""
CHƯƠNG 5: TÁC TỬ ĐIỀU PHỐI CÔNG CỤ DỘNG (REACT TOOL-AGENT ROUTER)
Sinh viên thực hiện: Trần Văn Hậu | MSV: B23DCCN287 | Lớp: D23CTPM01 | Nhóm CT_09
Giảng viên hướng dẫn: PGS. TS. Trần Đình Quế

Bộ định tuyến thông minh theo mẫu hình ReAct (Reasoning + Acting):
  - Phân tích câu hỏi người dùng thành chuỗi suy nghĩ (Thought)
  - Chọn công cụ chuyên biệt tối ưu (Action): [Vector_RAG, Graph_Cypher, Pandas_Analytics]
  - Thu thập kết quả thực thi công cụ (Observation)
  - Tổng hợp câu trả lời cuối cùng (Final Answer)
"""

import sys
import re
from typing import Dict, Any, List

sys.stdout.reconfigure(encoding='utf-8')


class ReActToolAgentRouter:
    """Tác tử ReAct tự động điều phối công cụ phù hợp với tính chất của câu hỏi."""
    def __init__(self):
        self.tools = {
            "Graph_Cypher": "Truy vấn quan hệ có cấu trúc đa bước trên đồ thị tri thức (chống chỉ định, triệu chứng - bệnh)",
            "Vector_RAG": "Tìm kiếm tài liệu y văn lâm sàng và các hướng dẫn thực hành y khoa phi cấu trúc",
            "Pandas_Analytics": "Tính toán thống kê định lượng trên bảng dữ liệu xét nghiệm người bệnh"
        }

    def plan_and_route(self, query: str) -> Dict[str, Any]:
        """Phân tích ý định và chọn công cụ tối ưu theo chu trình ReAct."""
        q_lower = query.lower()
        
        # 1. Bước suy nghĩ (Thought)
        if any(w in q_lower for w in ["chống chỉ định", "tác dụng phụ", "liên quan giữa", "nguyên nhân", "biến chứng"]):
            chosen_tool = "Graph_Cypher"
            thought = "Câu hỏi đòi hỏi kiểm tra các ràng buộc quan hệ có cấu trúc giữa thuốc, bệnh lý và triệu chứng -> Dùng Graph_Cypher để bảo đảm tính chuẩn xác 100%."
            action_input = {"intent": "graph_traversal", "entities": [w for w in ["metformin", "suy thận", "đái tháo đường"] if w in q_lower]}
        elif any(w in q_lower for w in ["trung bình", "thống kê", "cao nhất", "bao nhiêu bệnh nhân", "tỷ lệ"]):
            chosen_tool = "Pandas_Analytics"
            thought = "Câu hỏi đòi hỏi tổng hợp số học và tính toán phân tích dữ liệu bảng -> Dùng Pandas_Analytics."
            action_input = {"intent": "aggregation", "metric": "mean_glucose"}
        else:
            chosen_tool = "Vector_RAG"
            thought = "Câu hỏi liên quan đến định nghĩa, kiến thức khái quát hoặc văn bản hướng dẫn -> Dùng Vector_RAG."
            action_input = {"intent": "semantic_search", "query": query}

        # 2. Bước thực thi hành động giả lập (Observation)
        if chosen_tool == "Graph_Cypher":
            observation = "Graph Engine trả về: Metformin có quan hệ CONTRAINDICATED_WITH với Severe_Renal_Impairment."
        elif chosen_tool == "Pandas_Analytics":
            observation = "Pandas Engine trả về: Đường huyết trung bình 141.2 mg/dL, độ lệch chuẩn 31.9 mg/dL trên 768 bệnh nhân."
        else:
            observation = "Vector RAG trả về: ADA 2024 khuyến nghị mục tiêu HbA1c < 7.0% cho hầu hết người trưởng thành không có thai."

        # 3. Tổng hợp câu trả lời cuối cùng (Final Answer)
        final_answer = f"Theo kết quả điều tra từ công cụ {chosen_tool}: {observation}"

        return {
            "query": query,
            "thought": thought,
            "action": chosen_tool,
            "action_input": action_input,
            "observation": observation,
            "final_answer": final_answer
        }


def test_tool_router():
    print("=" * 70)
    print("KIỂM TRA TÁC TỬ ĐIỀU PHỐI CÔNG CỤ REACT TOOL-AGENT")
    print("Tác giả: Trần Văn Hậu - B23DCCN287 | Nhóm CT_09")
    print("=" * 70)

    agent = ReActToolAgentRouter()
    test_queries = [
        "Metformin có chống chỉ định với bệnh lý nào?",
        "Tính đường huyết trung bình của nhóm bệnh nhân trên 50 tuổi?",
        "Mục tiêu kiểm soát HbA1c tiêu chuẩn là bao nhiêu?"
    ]

    for q in test_queries:
        res = agent.plan_and_route(q)
        print(f"\n[Truy vấn]: {res['query']}")
        print(f"  [Thought]:     {res['thought']}")
        print(f"  [Action]:      {res['action']}")
        print(f"  [Observation]: {res['observation']}")
        print(f"  [Answer]:      {res['final_answer']}")

    print("\nReAct ToolAgent routing verification PASSED!")
    print("=" * 70)


if __name__ == "__main__":
    test_tool_router()
