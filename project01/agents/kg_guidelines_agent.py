#!/usr/bin/env python3
"""
Agent 3: Diabetes Knowledge Graph & Guidelines Consultant (DiaGraph-Agent)
Traverses the Medical Knowledge Graph to retrieve evidence-based guidance, pathophysiological links, and complications.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from knowledge_graph.diabetes_kg_queries import DiabetesKGQuerier

class KGGuidelinesAgent:
    def __init__(self, name: str = "DiaGraph-Agent (Tác Tử Đồ Thị Tri Thức & Phác Đồ ADA 2024)"):
        self.name = name
        self.querier = DiabetesKGQuerier()

    def consult(self, patient: dict, ai_consensus: dict) -> dict:
        kg_res = self.querier.analyze_patient_kg(patient)

        med_names = [m["name"] for m in kg_res["medications"]]
        comp_names = [c["name"] for c in kg_res["complications"]]
        life_names = [l["name"] for l in kg_res["lifestyles"]]

        msg = (
            f"Tôi là {self.name}.\n"
            f"Đối chiếu kết quả dự đoán của 7 mô hình AI ({ai_consensus['consensus_confidence']}% nguy cơ) với Đồ thị Tri thức Đái tháo đường & Khuyến cáo Hiệp hội Đái tháo đường Hoa Kỳ (ADA 2024):\n"
            f"• Phân loại thực thể bệnh học: {kg_res['disease_name']} (Mã ICD-10: {kg_res['icd10']})\n"
            f"• Nguy cơ biến chứng cơ quan đích: {', '.join(comp_names) if comp_names else 'Nguy cơ biến chứng thấp'}\n"
            f"• Chỉ định dược lý đầu tay theo đồ thị: {', '.join(med_names) if med_names else 'Chưa có chỉ định dùng thuốc'}\n"
            f"• Kế hoạch can thiệp lối sống chuẩn: {', '.join(life_names)}\n"
            f"• Cảnh báo lâm sàng từ Knowledge Graph: {'; '.join(kg_res['clinical_cautions']) if kg_res['clinical_cautions'] else 'Không có chống chỉ định đặc biệt'}"
        )

        return {
            "agent": self.name,
            "kg_analysis": kg_res,
            "disease_name": kg_res["disease_name"],
            "icd10": kg_res["icd10"],
            "medications": kg_res["medications"],
            "complications": kg_res["complications"],
            "lifestyles": kg_res["lifestyles"],
            "clinical_cautions": kg_res["clinical_cautions"],
            "message": msg
        }
