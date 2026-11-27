"""
VietnamDiabetesKG: Clinical Knowledge Graph for Type 2 Diabetes Mellitus in Vietnam
- 23 formal classes and 17 predicates
- Clinical rules: ADA 2024 / KDIGO 2024 / Vietnam Ministry of Health (BYT Decision 5481)
- Explicit drug interactions (Metformin + Ethanol -> Lactic Acidosis)
- Traditional Vietnamese dietary nutritional indexing (GI, Carbohydrates, Plate Method)
"""

from typing import Dict, List, Any, Optional
from rdflib import Graph, Literal, Namespace, RDF, RDFS, OWL, URIRef
from .ontology import Ontology, Predicate


EX = Namespace("http://ptit.edu.vn/tieuluan2/diabetes/")


def build_diabetes_ontology() -> Ontology:
    """Builds the 23-class clinical ontology with 17 predicates."""
    ont = Ontology("VietnamDiabetesOntology")

    # Class taxonomy (23 classes)
    classes = [
        ("MedicalEntity", "Entity"),
        ("Disease", "MedicalEntity"),
        ("EndocrineDisease", "Disease"),
        ("DiabetesT2", "EndocrineDisease"),
        ("PreDiabetes", "EndocrineDisease"),
        ("Symptom", "MedicalEntity"),
        ("LabTest", "MedicalEntity"),
        ("BloodGlucoseTest", "LabTest"),
        ("HbA1cTest", "LabTest"),
        ("OGTTTest", "LabTest"),
        ("KidneyFunctionTest", "LabTest"),
        ("UACRTest", "KidneyFunctionTest"),
        ("Drug", "MedicalEntity"),
        ("HypoglycemicDrug", "Drug"),
        ("Biguanide", "HypoglycemicDrug"),
        ("Sulfonylurea", "HypoglycemicDrug"),
        ("SGLT2Inhibitor", "HypoglycemicDrug"),
        ("Complication", "MedicalEntity"),
        ("MicrovascularComplication", "Complication"),
        ("MacrovascularComplication", "Complication"),
        ("Food", "MedicalEntity"),
        ("DietaryPattern", "MedicalEntity"),
        ("LifestyleRisk", "MedicalEntity")
    ]
    for c, p in classes:
        ont.add_class(c, p)

    # 17 Predicates
    predicates = [
        Predicate("has_symptom", "Disease", "Symptom", description="Triệu chứng của bệnh"),
        Predicate("diagnosed_by", "Disease", "LabTest", description="Tiêu chuẩn chẩn đoán cận lâm sàng"),
        Predicate("treated_by", "Disease", "Drug", description="Chỉ định điều trị bằng thuốc"),
        Predicate("contraindicated_with", "Drug", "MedicalEntity", description="Chống chỉ định"),
        Predicate("causes_interaction_with", "Drug", "LifestyleRisk", symmetric=True, description="Tương tác nguy hiểm"),
        Predicate("increases_risk_of", "MedicalEntity", "Complication", transitive=True, description="Tăng nguy cơ biến chứng"),
        Predicate("has_complication", "Disease", "Complication", description="Biến chứng tiến triển"),
        Predicate("recommends_diet", "Disease", "DietaryPattern", description="Chế độ dinh dưỡng khuyến nghị"),
        Predicate("contains_food", "DietaryPattern", "Food", description="Thực phẩm trong thực đơn"),
        Predicate("has_gi_index", "Food", None, description="Chỉ số đường huyết Glycemic Index"),
        Predicate("has_threshold", "LabTest", None, description="Ngưỡng chẩn đoán giá trị xét nghiệm"),
        Predicate("eGFR_safety_limit", "Drug", None, description="Giới hạn an toàn lọc cầu thận eGFR"),
        Predicate("target_hba1c_range", "Disease", None, description="Khoảng mục tiêu kiểm soát HbA1c"),
        Predicate("has_adverse_effect", "Drug", "Complication", description="Tác dụng phụ nghiêm trọng"),
        Predicate("prevents_progression_of", "Drug", "Complication", description="Bảo vệ cơ quan đích"),
        Predicate("affects_glycemia", "Food", "BloodGlucoseTest", description="Tác động lên đường huyết"),
        Predicate("synergistic_toxic_with", "Drug", "MedicalEntity", symmetric=True, description="Độc tính hiệp đồng")
    ]
    for p in predicates:
        ont.add_predicate(p)

    return ont


class VietnamDiabetesKG:
    """Vietnam Diabetes Clinical Knowledge Graph implementation."""
    def __init__(self):
        self.ontology = build_diabetes_ontology()
        self.graph = Graph()
        self.graph.bind("ex", EX)
        self.graph.bind("rdf", RDF)
        self.graph.bind("rdfs", RDFS)
        self.graph.bind("owl", OWL)
        
        self.entities: Dict[str, Dict[str, Any]] = {}
        self.triples_raw: List[Dict[str, Any]] = []
        self._populate_knowledge()

    def _add_entity(self, eid: str, name_vi: str, cls: str, properties: Optional[Dict] = None):
        self.entities[eid] = {
            "id": eid,
            "name": name_vi,
            "class": cls,
            "properties": properties or {}
        }
        uri = EX[eid]
        cls_uri = EX[cls]
        self.graph.add((uri, RDF.type, cls_uri))
        self.graph.add((uri, RDFS.label, Literal(name_vi, lang="vi")))
        for k, v in (properties or {}).items():
            self.graph.add((uri, EX[k], Literal(str(v))))

    def _add_relation(self, s_id: str, pred_name: str, o_id: str, evidence_doc: str = "", metadata: Optional[Dict] = None):
        # Validate constraint
        s_cls = self.entities[s_id]["class"]
        o_cls = self.entities[o_id]["class"]
        valid, msg = self.ontology.validate_triple(s_cls, pred_name, o_cls)
        if not valid:
            print(f"[KG Validation Warning] {msg}")

        s_uri = EX[s_id]
        p_uri = EX[pred_name]
        o_uri = EX[o_id]
        self.graph.add((s_uri, p_uri, o_uri))

        triple_data = {
            "subject": s_id,
            "subject_name": self.entities[s_id]["name"],
            "predicate": pred_name,
            "object": o_id,
            "object_name": self.entities[o_id]["name"],
            "evidence": evidence_doc,
            "metadata": metadata or {}
        }
        self.triples_raw.append(triple_data)

    def _populate_knowledge(self):
        # 1. Diseases
        self._add_entity("DT2", "Đái tháo đường típ 2", "DiabetesT2", {"code_icd10": "E11", "prevalence_vn": "7.3%"})
        self._add_entity("PreDM", "Tiền đái tháo đường", "PreDiabetes", {"code_icd10": "R73.0", "hba1c_range": "5.7-6.4%"})

        # 2. Symptoms
        self._add_entity("Polyuria", "Tiểu nhiều lần trong ngày", "Symptom")
        self._add_entity("Polydipsia", "Khát nhiều, uống nước liên tục", "Symptom")
        self._add_entity("WeightLoss", "Sụt cân không rõ nguyên nhân", "Symptom")
        self._add_entity("Fatigue", "Mệt mỏi suy nhược kéo dài", "Symptom")

        # 3. Lab Tests
        self._add_entity("FPG", "Đường huyết tương lúc đói (FPG)", "BloodGlucoseTest", {"unit": "mg/dL", "threshold_dm": 126.0, "threshold_predm": 100.0})
        self._add_entity("HbA1c", "Chỉ số hemoglobin gắn đường (HbA1c)", "HbA1cTest", {"unit": "%", "threshold_dm": 6.5, "threshold_predm": 5.7, "target_standard": 7.0})
        self._add_entity("OGTT", "Nghiệm pháp dung nạp glucose đường uống 2h", "OGTTTest", {"unit": "mg/dL", "threshold_dm": 200.0, "threshold_predm": 140.0})
        self._add_entity("UACR", "Tỷ số Albumin/Creatinine niệu", "UACRTest", {"unit": "mg/g", "microalbuminuria_cutoff": 30.0})

        # 4. Drugs
        self._add_entity("Metformin", "Metformin (Glucophage 500mg/850mg/1000mg)", "Biguanide", {
            "first_line": True, "max_dose_daily": "2000mg", "egfr_cutoff": 30.0, "egfr_reduce_dose": 45.0
        })
        self._add_entity("Gliclazide", "Gliclazide (Diamicron MR 30mg/60mg)", "Sulfonylurea", {
            "mechanism": "Kích thích tế bào beta tụy tiết insulin", "hypoglycemia_risk": "Trung bình - Cao"
        })
        self._add_entity("Dapagliflozin", "Dapagliflozin (Forxiga 10mg)", "SGLT2Inhibitor", {
            "organ_protection": "Tim mạch và Thận", "weight_loss_benefit": True
        })
        self._add_entity("Empagliflozin", "Empagliflozin (Jardiance 10mg/25mg)", "SGLT2Inhibitor", {
            "organ_protection": "Giảm tử vong tim mạch và suy tim", "indication": "T2D kèm suy tim hoặc bệnh thận mạn"
        })

        # 5. Complications
        self._add_entity("LacticAcidosis", "Nhiễm toan Lactic (Lactic Acidosis)", "MicrovascularComplication", {
            "mortality_rate": "30-50%", "diagnostic_anion_gap": ">16 mEq/L", "lactate_level": ">5.0 mmol/L"
        })
        self._add_entity("Nephropathy", "Bệnh thận đái tháo đường (Diabetic Kidney Disease)", "MicrovascularComplication")
        self._add_entity("Retinopathy", "Bệnh võng mạc đái tháo đường", "MicrovascularComplication")
        self._add_entity("CAD", "Bệnh động mạch vành và nhồi máu cơ tim", "MacrovascularComplication")
        self._add_entity("Stroke", "Đột quỵ não nhồi máu", "MacrovascularComplication")

        # 6. Lifestyle & Foods
        self._add_entity("Alcohol", "Rượu bia và đồ uống có cồn (Ethanol)", "LifestyleRisk", {
            "pathway": "Tăng tỷ lệ cytosolic NADH/NAD+ tại gan, ức chế thanh thải lactate"
        })
        self._add_entity("Sedentary", "Lối sống tĩnh tại, ít vận động thể lực", "LifestyleRisk")
        self._add_entity("PlateMethod", "Mô hình Đĩa ăn cân bằng (50% rau, 25% đạm, 25% bột)", "DietaryPattern")
        self._add_entity("WhiteRice", "Cơm trắng gạo tẻ tinh chế", "Food", {"gi": 83.0, "category": "GI Cao", "carbs_per_100g": 28.0})
        self._add_entity("BrownRice", "Cơm gạo lứt nguyên cám", "Food", {"gi": 55.0, "category": "GI Thấp", "fiber_rich": True})
        self._add_entity("ChickenBreast", "Thịt ức gà ta bỏ da luộc", "Food", {"gi": 0.0, "category": "Đạm nạc an toàn", "protein_per_100g": 31.0, "fat_per_100g": 3.6})
        self._add_entity("GreenVeggies", "Rau muống, cải xanh, súp lơ luộc", "Food", {"gi": 15.0, "category": "Chất xơ hòa tan cao"})

        # Relations
        self._add_relation("DT2", "has_symptom", "Polyuria", "D01_Phac_Do_Bo_Y_Te_Dai_Thao_Duong.txt")
        self._add_relation("DT2", "has_symptom", "Polydipsia", "D01_Phac_Do_Bo_Y_Te_Dai_Thao_Duong.txt")
        self._add_relation("DT2", "has_symptom", "WeightLoss", "D01_Phac_Do_Bo_Y_Te_Dai_Thao_Duong.txt")
        self._add_relation("DT2", "diagnosed_by", "FPG", "D01_Phac_Do_Bo_Y_Te_Dai_Thao_Duong.txt", {"rule": "FPG >= 126 mg/dL"})
        self._add_relation("DT2", "diagnosed_by", "HbA1c", "D01_Phac_Do_Bo_Y_Te_Dai_Thao_Duong.txt", {"rule": "HbA1c >= 6.5%"})
        self._add_relation("DT2", "diagnosed_by", "OGTT", "D01_Phac_Do_Bo_Y_Te_Dai_Thao_Duong.txt", {"rule": "OGTT 2h >= 200 mg/dL"})
        
        self._add_relation("DT2", "treated_by", "Metformin", "D02_Duoc_Lam_Sang_Metformin.txt", {"priority": "First-line (Đầu tay)"})
        self._add_relation("DT2", "treated_by", "Gliclazide", "D01_Phac_Do_Bo_Y_Te_Dai_Thao_Duong.txt", {"priority": "Second-line (Phối hợp)"})
        self._add_relation("DT2", "treated_by", "Dapagliflozin", "D06_Tieu_Chuan_Hoi_Noi_Tiet_ADA_KDIGO.txt", {"benefit": "Tim mạch và Thận"})
        self._add_relation("DT2", "treated_by", "Empagliflozin", "D06_Tieu_Chuan_Hoi_Noi_Tiet_ADA_KDIGO.txt", {"benefit": "Giảm tử vong tim mạch"})

        # CRITICAL CLINICAL SAFETY INTERACTION: METFORMIN + ALCOHOL -> LACTIC ACIDOSIS
        self._add_relation("Metformin", "causes_interaction_with", "Alcohol", "D03_Tuong_Tac_Thuoc_Va_Nhiem_Toan_Lactic.txt", {
            "danger_level": "CỰC KỲ NGUY HIỂM",
            "consequence": "Nhiễm toan Lactic (Lactic Acidosis)",
            "mechanism": "Ethanol tăng NADH/NAD+ ức chế chuyển hóa lactate tại gan; Metformin ức chế chuỗi hô hấp ty thể phức hợp I."
        })
        self._add_relation("Alcohol", "increases_risk_of", "LacticAcidosis", "D03_Tuong_Tac_Thuoc_Va_Nhiem_Toan_Lactic.txt")
        self._add_relation("Metformin", "has_adverse_effect", "LacticAcidosis", "D02_Duoc_Lam_Sang_Metformin.txt")

        # Complications and Organ Protection
        self._add_relation("DT2", "has_complication", "Nephropathy", "D05_Bien_Chung_Dai_Thao_Duong_Va_Kiem_Soat.txt")
        self._add_relation("DT2", "has_complication", "Retinopathy", "D05_Bien_Chung_Dai_Thao_Duong_Va_Kiem_Soat.txt")
        self._add_relation("DT2", "has_complication", "CAD", "D05_Bien_Chung_Dai_Thao_Duong_Va_Kiem_Soat.txt")
        self._add_relation("DT2", "has_complication", "Stroke", "D05_Bien_Chung_Dai_Thao_Duong_Va_Kiem_Soat.txt")

        self._add_relation("Dapagliflozin", "prevents_progression_of", "Nephropathy", "D06_Tieu_Chuan_Hoi_Noi_Tiet_ADA_KDIGO.txt")
        self._add_relation("Empagliflozin", "prevents_progression_of", "CAD", "D06_Tieu_Chuan_Hoi_Noi_Tiet_ADA_KDIGO.txt")

        # Nutrition
        self._add_relation("DT2", "recommends_diet", "PlateMethod", "D04_Dinh_Duong_Lam_Sang_Va_Chi_So_GI.txt")
        self._add_relation("PlateMethod", "contains_food", "ChickenBreast", "D04_Dinh_Duong_Lam_Sang_Va_Chi_So_GI.txt")
        self._add_relation("PlateMethod", "contains_food", "GreenVeggies", "D04_Dinh_Duong_Lam_Sang_Va_Chi_So_GI.txt")
        self._add_relation("PlateMethod", "contains_food", "BrownRice", "D04_Dinh_Duong_Lam_Sang_Va_Chi_So_GI.txt")

    def query_drug_interactions(self, drug_id: str) -> List[Dict[str, Any]]:
        """Finds direct and indirect interactions for a given drug."""
        results = []
        for t in self.triples_raw:
            if (t["subject"] == drug_id or t["object"] == drug_id) and t["predicate"] in ["causes_interaction_with", "contraindicated_with", "synergistic_toxic_with"]:
                other = t["object"] if t["subject"] == drug_id else t["subject"]
                other_name = t["object_name"] if t["subject"] == drug_id else t["subject_name"]
                results.append({
                    "drug": self.entities[drug_id]["name"],
                    "interacts_with": other_name,
                    "predicate": t["predicate"],
                    "metadata": t["metadata"],
                    "evidence": t["evidence"]
                })
        return results

    def query_food_nutrition(self, food_id: str) -> Dict[str, Any]:
        """Returns food GI and dietary advice."""
        if food_id in self.entities:
            ent = self.entities[food_id]
            return {
                "food": ent["name"],
                "class": ent["class"],
                "properties": ent["properties"],
                "diet_advice": "Khuyến nghị trong đĩa ăn 1/4 đạm nạc" if ent["properties"].get("gi", 100) < 55 else "Nên giảm lượng tiêu thụ hoặc thay thế bằng gạo lứt"
            }
        return {}

    def get_summary_statistics(self) -> Dict[str, Any]:
        return {
            "name": "VietnamDiabetesKG",
            "classes_count": len(self.ontology.classes),
            "predicates_count": len(self.ontology.predicates),
            "entities_count": len(self.entities),
            "triples_count": len(self.triples_raw)
        }
