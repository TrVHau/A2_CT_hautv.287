#!/usr/bin/env python3
"""
Diabetes Knowledge Graph Traversal & Query Engine
Executes multi-hop clinical reasoning based on the 8 diabetes features:
  - Traverses from Patient Biomarkers -> Disease State -> Medication Protocol -> Complications -> Safety Guards.
"""

import os
import json
import networkx as nx

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KG_JSON = os.path.join(BASE_DIR, "knowledge_graph", "diabetes_knowledge_graph.json")

class DiabetesKGQuerier:
    def __init__(self, json_path=None):
        if json_path is None:
            json_path = KG_JSON
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.G = nx.node_link_graph(data)

    def analyze_patient_kg(self, patient: dict) -> dict:
        hba1c = float(patient.get("HbA1c_level", 5.5))
        glucose = float(patient.get("blood_glucose_level", 95))
        bmi = float(patient.get("bmi", 24.0))
        hypertension = int(patient.get("hypertension", 0))
        heart_disease = int(patient.get("heart_disease", 0))
        smoking = str(patient.get("smoking_history", "never")).lower()
        age = float(patient.get("age", 45))

        # 1. Determine Disease state from Knowledge Graph cutoffs
        if hba1c >= 6.5 or glucose >= 126.0:
            if heart_disease == 1 or hypertension == 1 or smoking in ["current", "ever"]:
                primary_disease = "DIS_DIABETES_CVD"
            else:
                primary_disease = "DIS_DIABETES_T2"
        elif (5.7 <= hba1c <= 6.4) or (100.0 <= glucose <= 125.0):
            primary_disease = "DIS_PREDIABETES"
        else:
            primary_disease = "DIS_NORMAL"

        disease_node = self.G.nodes[primary_disease]

        # 2. Extract Connected Medications
        medications = []
        for _, target, edge in self.G.out_edges(primary_disease, data=True):
            if self.G.nodes[target].get("type") == "Medication":
                med_node = self.G.nodes[target]
                medications.append({
                    "id": target,
                    "name": med_node.get("name"),
                    "class": med_node.get("class"),
                    "desc": med_node.get("desc"),
                    "relation": edge.get("relation"),
                    "evidence": edge.get("evidence", "ADA 2024")
                })

        # If very high HbA1c, add Insulin
        if hba1c >= 9.0 or glucose >= 200:
            ins_node = self.G.nodes["MED_INSULIN"]
            if not any(m["id"] == "MED_INSULIN" for m in medications):
                medications.append({
                    "id": "MED_INSULIN",
                    "name": ins_node.get("name"),
                    "class": ins_node.get("class"),
                    "desc": ins_node.get("desc"),
                    "relation": "REQUIRES_EARLY_INITIATION",
                    "evidence": "ADA 2024 (HbA1c >= 9%)"
                })

        # 3. Extract Lifestyle Interventions
        lifestyles = []
        for _, target, edge in self.G.out_edges(primary_disease, data=True):
            if self.G.nodes[target].get("type") == "Lifestyle":
                node = self.G.nodes[target]
                lifestyles.append({
                    "id": target,
                    "name": node.get("name"),
                    "desc": node.get("desc"),
                    "relation": edge.get("relation")
                })
        # If smoking, always add smoking cessation
        if smoking in ["current", "ever"]:
            stop_smoke = self.G.nodes["LIFE_STOP_SMOKING"]
            if not any(l["id"] == "LIFE_STOP_SMOKING" for l in lifestyles):
                lifestyles.append({
                    "id": "LIFE_STOP_SMOKING",
                    "name": stop_smoke.get("name"),
                    "desc": stop_smoke.get("desc"),
                    "relation": "MANDATORY_CESSATION"
                })

        # 4. Extract Complications
        complications = []
        for _, target, edge in self.G.out_edges(primary_disease, data=True):
            if self.G.nodes[target].get("type") == "Complication":
                node = self.G.nodes[target]
                complications.append({
                    "id": target,
                    "name": node.get("name"),
                    "desc": node.get("desc"),
                    "pathway": edge.get("pathway", "Micro/Macrovascular")
                })

        # 5. Contraindications & Caution Rules
        cautions = []
        if age >= 70:
            cautions.append("Bệnh nhân cao tuổi (>= 70 tuổi): Mục tiêu HbA1c nới lỏng < 7.5% - 8.0% để phòng ngừa hạ đường huyết đột ngột gây té ngã và đột quỵ.")
        if heart_disease == 1:
            cautions.append("Có tiền sử bệnh tim mạch: Ưu tiên bắt buộc nhóm SGLT2i (Empagliflozin/Dapagliflozin) hoặc GLP-1 RA (Semaglutide) có bằng chứng bảo vệ tim mạch vượt trội; thận trọng dùng Sulfonylurea.")
        if bmi >= 30.0:
            cautions.append("Béo phì độ II/III (BMI >= 30): Ưu tiên GLP-1 RA giúp giảm 10-15% thể trọng đồng thời cải thiện độ nhạy insulin gan/cơ.")

        return {
            "disease_id": primary_disease,
            "disease_name": disease_node.get("name"),
            "disease_desc": disease_node.get("desc"),
            "icd10": disease_node.get("icd10", "E11"),
            "medications": medications,
            "lifestyles": lifestyles,
            "complications": complications,
            "clinical_cautions": cautions
        }

if __name__ == "__main__":
    querier = DiabetesKGQuerier()
    test_p = {"age": 60, "HbA1c_level": 8.5, "blood_glucose_level": 170, "heart_disease": 1, "smoking_history": "current", "bmi": 31.5}
    res = querier.analyze_patient_kg(test_p)
    print("Diagnosis:", res["disease_name"])
    print("Medications:", [m["name"] for m in res["medications"]])
    print("Cautions:", res["clinical_cautions"])
