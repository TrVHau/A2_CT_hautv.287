# -*- coding: utf-8 -*-
"""
CHƯƠNG 5: BẢN THỂ HỌC ĐỒ THỊ TRI THỨC Y TẾ (CLINICAL KNOWLEDGE GRAPH ONTOLOGY) & NEO4J
Sinh viên thực hiện: Trần Văn Hậu | MSV: B23DCCN287 | Lớp: D23CTPM01 | Nhóm CT_09
Giảng viên hướng dẫn: PGS. TS. Trần Đình Quế

Hiện thực hóa:
  1. Định nghĩa mô hình bản thể học (TBox & ABox, chuẩn OWL/RDF SPO Triples)
  2. Các thực thể: Disease, Symptom, Biomarker, Drug, Food, Complication
  3. Quan hệ: HAS_SYMPTOM, INDICATES, TREATED_BY, CONTRAINDICATED_WITH, MONITORS
  4. Trình sinh truy vấn Cypher và Engine truy vấn đồ thị nội nhớ (In-Memory Graph Engine)
"""

import sys
from typing import List, Dict, Any, Tuple

sys.stdout.reconfigure(encoding='utf-8')


class ClinicalOntology:
    """Định nghĩa cấu trúc Ontology và Cypher queries cho miền bệnh đái tháo đường."""
    
    SCHEMA_CYPHER = """
    // Ràng buộc tính duy nhất (Uniqueness Constraints)
    CREATE CONSTRAINT IF NOT EXISTS FOR (d:Disease) REQUIRE d.id IS UNIQUE;
    CREATE CONSTRAINT IF NOT EXISTS FOR (s:Symptom) REQUIRE s.id IS UNIQUE;
    CREATE CONSTRAINT IF NOT EXISTS FOR (b:Biomarker) REQUIRE b.id IS UNIQUE;
    CREATE CONSTRAINT IF NOT EXISTS FOR (m:Drug) REQUIRE m.id IS UNIQUE;
    CREATE CONSTRAINT IF NOT EXISTS FOR (c:Complication) REQUIRE c.id IS UNIQUE;
    """

    @staticmethod
    def get_seed_triples() -> List[Tuple[str, str, str, str, str]]:
        """Trả về danh sách các bộ 3 tri thức chuẩn lâm sàng (Subject, S_Type, Predicate, Object, O_Type)."""
        return [
            ("Type_2_Diabetes", "Disease", "HAS_SYMPTOM", "Polydipsia", "Symptom"),
            ("Type_2_Diabetes", "Disease", "HAS_SYMPTOM", "Polyuria", "Symptom"),
            ("Type_2_Diabetes", "Disease", "HAS_SYMPTOM", "Fatigue", "Symptom"),
            ("Type_2_Diabetes", "Disease", "INDICATES", "High_Fasting_Glucose", "Biomarker"),
            ("Type_2_Diabetes", "Disease", "INDICATES", "High_HbA1c", "Biomarker"),
            ("Type_2_Diabetes", "Disease", "TREATED_BY", "Metformin", "Drug"),
            ("Type_2_Diabetes", "Disease", "TREATED_BY", "Empagliflozin", "Drug"),
            ("Type_2_Diabetes", "Disease", "CAUSES_COMPLICATION", "Diabetic_Retinopathy", "Complication"),
            ("Type_2_Diabetes", "Disease", "CAUSES_COMPLICATION", "Diabetic_Nephropathy", "Complication"),
            ("Metformin", "Drug", "CONTRAINDICATED_WITH", "Severe_Renal_Impairment", "Disease"),
            ("Empagliflozin", "Drug", "REDUCES_RISK", "Heart_Failure", "Disease"),
            ("Diabetic_Retinopathy", "Complication", "HAS_SYMPTOM", "Blurred_Vision", "Symptom"),
            ("High_Fasting_Glucose", "Biomarker", "MEASURED_BY", "Blood_Glucose_Test", "DiagnosticTest"),
            ("High_HbA1c", "Biomarker", "THRESHOLD", "HbA1c_GE_6_5", "ClinicalCriteria")
        ]

    @staticmethod
    def build_multi_hop_cypher(patient_symptoms: List[str]) -> str:
        """Sinh truy vấn Cypher đa bước tìm các bệnh tiềm năng và phác đồ thuốc tương ứng."""
        symptom_list_str = str(patient_symptoms)
        cypher = f"""
        MATCH (s:Symptom)<-[:HAS_SYMPTOM]-(d:Disease)-[:TREATED_BY]->(m:Drug)
        WHERE s.name IN {symptom_list_str}
        OPTIONAL MATCH (d)-[:CAUSES_COMPLICATION]->(c:Complication)
        OPTIONAL MATCH (m)-[:CONTRAINDICATED_WITH]->(contra:Disease)
        RETURN d.name AS Disease, 
               collect(DISTINCT s.name) AS MatchedSymptoms,
               collect(DISTINCT m.name) AS RecommendedDrugs,
               collect(DISTINCT c.name) AS PotentialComplications,
               collect(DISTINCT contra.name) AS Contraindications
        ORDER BY size(MatchedSymptoms) DESC
        """
        return cypher


class InMemoryClinicalKnowledgeGraph:
    """Bộ mô phỏng đồ thị tri thức lâm sàng nội nhớ hỗ trợ truy vấn đa bước không cần cài Neo4j."""
    def __init__(self):
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: List[Dict[str, str]] = []
        self._load_seed_data()

    def _load_seed_data(self):
        triples = ClinicalOntology.get_seed_triples()
        for s, s_type, p, o, o_type in triples:
            self.nodes[s] = {"name": s, "type": s_type}
            self.nodes[o] = {"name": o, "type": o_type}
            self.edges.append({"source": s, "relation": p, "target": o})

    def query_multihop_reasoning(self, observed_symptoms: List[str]) -> List[Dict[str, Any]]:
        """Truy vấn đồ thị đa bước suy luận nguyên nhân bệnh học và cảnh báo chống chỉ định."""
        results = []
        # Tìm tất cả bệnh có chứa triệu chứng quan sát
        diseases = {}
        for edge in self.edges:
            if edge["relation"] == "HAS_SYMPTOM" and edge["target"] in observed_symptoms:
                d = edge["source"]
                if d not in diseases:
                    diseases[d] = {"symptoms": set(), "drugs": set(), "complications": set(), "contraindications": set()}
                diseases[d]["symptoms"].add(edge["target"])

        # Mở rộng multi-hop: tìm thuốc và biến chứng
        for d in diseases:
            for edge in self.edges:
                if edge["source"] == d and edge["relation"] == "TREATED_BY":
                    drug = edge["target"]
                    diseases[d]["drugs"].add(drug)
                    # Tìm chống chỉ định của thuốc này
                    for c_edge in self.edges:
                        if c_edge["source"] == drug and c_edge["relation"] == "CONTRAINDICATED_WITH":
                            diseases[d]["contraindications"].add(f"{drug} cấm dùng khi có {c_edge['target']}")
                if edge["source"] == d and edge["relation"] == "CAUSES_COMPLICATION":
                    diseases[d]["complications"].add(edge["target"])

            results.append({
                "disease": d,
                "matched_symptoms": list(diseases[d]["symptoms"]),
                "recommended_drugs": list(diseases[d]["drugs"]),
                "potential_complications": list(diseases[d]["complications"]),
                "contraindications": list(diseases[d]["contraindications"]),
                "match_score": len(diseases[d]["symptoms"]) / max(1, len(observed_symptoms))
            })

        results.sort(key=lambda x: x["match_score"], reverse=True)
        return results


def test_ontology():
    print("=" * 70)
    print("KIỂM TRA BẢN THỂ HỌC ĐỒ THỊ TRI THỨC Y TẾ (NEO4J & ONTOLOGY)")
    print("Tác giả: Trần Văn Hậu - B23DCCN287 | Nhóm CT_09")
    print("=" * 70)

    kg = InMemoryClinicalKnowledgeGraph()
    print(f"Tổng số đỉnh (Nodes): {len(kg.nodes)} | Tổng số quan hệ (Edges): {len(kg.edges)}")
    
    symptoms = ["Polydipsia", "Polyuria"]
    print(f"\nTruy vấn suy luận đa bước với triệu chứng quan sát: {symptoms}")
    res = kg.query_multihop_reasoning(symptoms)

    for item in res:
        print(f"\n[Bệnh phát hiện]: {item['disease']} (Match Score: {item['match_score']*100:.1f}%)")
        print(f"  - Triệu chứng trùng khớp: {item['matched_symptoms']}")
        print(f"  - Thuốc điều trị chuẩn:   {item['recommended_drugs']}")
        print(f"  - Cảnh báo chống chỉ định:{item['contraindications']}")
        print(f"  - Nguy cơ biến chứng:     {item['potential_complications']}")

    print("\nTruy vấn Cypher mẫu sinh tự động:")
    print(ClinicalOntology.build_multi_hop_cypher(symptoms).strip())
    print("=" * 70)


if __name__ == "__main__":
    test_ontology()
