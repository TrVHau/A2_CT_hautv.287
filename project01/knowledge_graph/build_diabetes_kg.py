#!/usr/bin/env python3
"""
Medical Knowledge Graph for Diabetes Mellitus (ADA 2024 / WHO Standards)
Maps the 8 clinical features of diabetes_prediction_dataset.csv:
  - Age, Gender, BMI, Hypertension, Heart Disease, Smoking History, HbA1c, Blood Glucose
to Clinical Diagnosis, Pharmacotherapy, Lifestyle, Complications & Contraindications.
Exports to JSON for interactive Vis.js graph rendering & NetworkX traversal.
"""

import os
import sys
import json
import networkx as nx

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KG_DIR = os.path.join(BASE_DIR, "knowledge_graph")
os.makedirs(KG_DIR, exist_ok=True)
OUT_JSON = os.path.join(KG_DIR, "diabetes_knowledge_graph.json")

def build_diabetes_knowledge_graph():
    G = nx.DiGraph(name="Diabetes_Clinical_Knowledge_Graph")

    # 1. Disease States
    diseases = [
        {"id": "DIS_NORMAL", "name": "Bình Thường (Không Đái Tháo Đường)", "type": "Disease", "icd10": "Z00", "desc": "Chỉ số chuyển hóa glucose và HbA1c hoàn toàn trong giới hạn sinh lý."},
        {"id": "DIS_PREDIABETES", "name": "Tiền Đái Tháo Đường (Prediabetes)", "type": "Disease", "icd10": "R73.03", "desc": "Rối loạn đường huyết đói (IFG) hoặc rối loạn dung nạp glucose (IGT), nguy cơ tiến triển thành ĐTĐ tuýp 2."},
        {"id": "DIS_DIABETES_T2", "name": "Đái Tháo Đường Tuýp 2 (Type 2 Diabetes)", "type": "Disease", "icd10": "E11", "desc": "Bệnh lý chuyển hóa mạn tính do giảm tiết insulin tương đối kết hợp đề kháng insulin."},
        {"id": "DIS_DIABETES_CVD", "name": "ĐTĐ Kèm Nguy Cơ Tim Mạch Cao (Diabetes + CVD)", "type": "Disease", "icd10": "E11.5", "desc": "Bệnh nhân ĐTĐ có kèm tiền sử bệnh mạch vành, tăng huyết áp hoặc hút thuốc lá nặng."}
    ]

    # 2. Risk Factors & Biomarker Cutoffs (Matching dataset columns)
    features = [
        {"id": "FEAT_HBA1C_NORMAL", "name": "HbA1c < 5.7%", "type": "Biomarker", "cutoff": "<5.7", "desc": "Mức HbA1c bình thường (ADA 2024)."},
        {"id": "FEAT_HBA1C_PRE", "name": "HbA1c 5.7% - 6.4%", "type": "Biomarker", "cutoff": "5.7-6.4", "desc": "Ngưỡng chẩn đoán Tiền đái tháo đường."},
        {"id": "FEAT_HBA1C_DIAB", "name": "HbA1c >= 6.5%", "type": "Biomarker", "cutoff": ">=6.5", "desc": "Tiêu chuẩn vàng xác định mắc Đái tháo đường."},
        {"id": "FEAT_HBA1C_VERY_HIGH", "name": "HbA1c >= 9.0%", "type": "Biomarker", "cutoff": ">=9.0", "desc": "Đường huyết kiểm soát rất kém, cần phối hợp thuốc sớm hoặc Insulin."},
        {"id": "FEAT_GLUCOSE_NORMAL", "name": "Đường huyết < 100 mg/dL", "type": "Biomarker", "cutoff": "<100", "desc": "Đường huyết đói bình thường."},
        {"id": "FEAT_GLUCOSE_PRE", "name": "Đường huyết 100 - 125 mg/dL", "type": "Biomarker", "cutoff": "100-125", "desc": "Rối loạn đường huyết đói (Impaired Fasting Glucose)."},
        {"id": "FEAT_GLUCOSE_DIAB", "name": "Đường huyết >= 126 mg/dL", "type": "Biomarker", "cutoff": ">=126", "desc": "Ngưỡng chẩn đoán Đái tháo đường khi nhịn đói >= 8h."},
        {"id": "FEAT_GLUCOSE_SEVERE", "name": "Đường huyết >= 200 mg/dL", "type": "Biomarker", "cutoff": ">=200", "desc": "Tăng áp lực thẩm thấu, nguy cơ biến chứng cấp tính."},
        {"id": "FEAT_BMI_OBESE", "name": "BMI >= 25.0 kg/m² (Thừa cân / Béo phì)", "type": "Biomarker", "cutoff": ">=25", "desc": "Mô mỡ nội tạng gia tăng phóng thích acid béo tự do gây đề kháng insulin."},
        {"id": "FEAT_HYPERTENSION", "name": "Tăng Huyết Áp (Hypertension = 1)", "type": "Comorbidity", "desc": "Tăng áp lực thành mạch, thúc đẩy tổn thương nội mạc và suy thận."},
        {"id": "FEAT_HEART_DISEASE", "name": "Bệnh Tim Mạch (Heart Disease = 1)", "type": "Comorbidity", "desc": "Bệnh động mạch vành / xơ vữa, ưu tiên thuốc có lợi ích bảo vệ tim."},
        {"id": "FEAT_SMOKING", "name": "Hút Thuốc Lá (Smoking History = Current)", "type": "RiskFactor", "desc": "Nicotine và chất oxy hóa làm co thắt vi mạch và tăng độc tính tế bào beta tụy."}
    ]

    # 3. Medications (Pharmacological Interventions)
    medications = [
        {"id": "MED_METFORMIN", "name": "Metformin (Glucophage 500-1000mg)", "type": "Medication", "class": "Biguanide", "desc": "Thuốc đầu tay: Giảm tân tạo glucose tại gan, tăng nhạy cảm insulin mô cơ."},
        {"id": "MED_SGLT2I", "name": "Empagliflozin / Dapagliflozin (10mg)", "type": "Medication", "class": "SGLT2 Inhibitor", "desc": "Thải đường qua nước tiểu, hạ huyết áp, bảo vệ tim mạch và giảm nhập viện do suy tim."},
        {"id": "MED_GLP1RA", "name": "Semaglutide / Liraglutide", "type": "Medication", "class": "GLP-1 RA", "desc": "Đồng vận GLP-1: Kích thích tiết insulin phụ thuộc glucose, giảm cân mạnh mẽ và bảo vệ biến cố tim mạch."},
        {"id": "MED_SU", "name": "Gliclazide MR (30-60mg)", "type": "Medication", "class": "Sulfonylurea", "desc": "Kích thích tế bào beta tụy tiết insulin, nguy cơ hạ đường huyết nhẹ."},
        {"id": "MED_INSULIN", "name": "Insulin Nền (Glargine / Degludec)", "type": "Medication", "class": "Basal Insulin", "desc": "Bù đắp insulin sinh lý khi tế bào beta tụy suy kiệt hoặc HbA1c > 9-10%."}
    ]

    # 4. Lifestyle & Nutrition
    lifestyles = [
        {"id": "LIFE_LOW_GI", "name": "Chế độ ăn Low-GI (Kiểm soát Carbohydrate)", "type": "Lifestyle", "desc": "Tăng chất xơ hòa tan, rau xanh, ngũ cốc nguyên cám, giảm đường tinh luyện."},
        {"id": "LIFE_EXERCISE", "name": "Vận động thể lực 150 phút/tuần", "type": "Lifestyle", "desc": "Đi bộ nhanh, đạp xe 30p x 5 ngày/tuần tăng nhạy cảm thụ thể GLUT4 ở cơ bắp."},
        {"id": "LIFE_WEIGHT_LOSS", "name": "Giảm 5% - 7% Trọng Lượng Cơ Thể", "type": "Lifestyle", "desc": "Đảo ngược đề kháng insulin tại gan và cơ quan nội tạng."},
        {"id": "LIFE_STOP_SMOKING", "name": "Cai Thuốc Lá Tuyệt Đối", "type": "Lifestyle", "desc": "Ngăn ngừa xơ vữa động mạch và bảo tồn chức năng vi mạch."}
    ]

    # 5. Complications
    complications = [
        {"id": "COMP_NEPHROPATHY", "name": "Bệnh Thận ĐTĐ (Diabetic Nephropathy)", "type": "Complication", "desc": "Tổn thương vi mạch cầu thận dẫn đến tiểu đạm và suy giảm chức năng lọc."},
        {"id": "COMP_RETINOPATHY", "name": "Bệnh Võng Mạc ĐTĐ (Retinopathy)", "type": "Complication", "desc": "Xuất huyết mao mạch võng mạc, phù hoàng điểm làm suy giảm thị lực."},
        {"id": "COMP_NEUROPATHY", "name": "Bệnh Thần Kinh Ngoại Biên (Neuropathy)", "type": "Complication", "desc": "Tê bì, mất cảm giác hoặc cảm giác châm chích kiểu đi găng đi tất."},
        {"id": "COMP_CAD", "name": "Bệnh Động Mạch Vành & Nhồi Máu Cơ Tim", "type": "Complication", "desc": "Biến chứng mạch máu lớn gây thiếu máu cơ tim và suy tim."}
    ]

    # Add all nodes
    for group in [diseases, features, medications, lifestyles, complications]:
        for n in group:
            node_id = n.pop("id")
            G.add_node(node_id, **n)

    # 6. Directed Relationships (Edges)
    edges = [
        # Normal
        ("FEAT_HBA1C_NORMAL", "DIS_NORMAL", {"relation": "INDICATES", "strength": "Definitive"}),
        ("FEAT_GLUCOSE_NORMAL", "DIS_NORMAL", {"relation": "INDICATES", "strength": "Definitive"}),
        ("DIS_NORMAL", "LIFE_EXERCISE", {"relation": "MAINTAINS", "desc": "Duy trì lối sống lành mạnh"}),

        # Prediabetes
        ("FEAT_HBA1C_PRE", "DIS_PREDIABETES", {"relation": "DIAGNOSED_BY", "evidence": "ADA 2024"}),
        ("FEAT_GLUCOSE_PRE", "DIS_PREDIABETES", {"relation": "DIAGNOSED_BY", "evidence": "ADA 2024"}),
        ("DIS_PREDIABETES", "LIFE_LOW_GI", {"relation": "FIRST_LINE_MANAGEMENT", "desc": "Can thiệp lối sống tích cực"}),
        ("DIS_PREDIABETES", "LIFE_WEIGHT_LOSS", {"relation": "CRUCIAL_INTERVENTION", "desc": "Giảm 7% cân nặng giúp ngừa 58% tiến triển ĐTĐ"}),
        ("DIS_PREDIABETES", "DIS_DIABETES_T2", {"relation": "CAN_PROGRESS_TO", "risk": "10% mỗi năm nếu không can thiệp"}),

        # Type 2 Diabetes
        ("FEAT_HBA1C_DIAB", "DIS_DIABETES_T2", {"relation": "CONFIRMED_BY", "evidence": "ADA 2024"}),
        ("FEAT_GLUCOSE_DIAB", "DIS_DIABETES_T2", {"relation": "CONFIRMED_BY", "evidence": "ADA 2024"}),
        ("FEAT_BMI_OBESE", "DIS_DIABETES_T2", {"relation": "MAJOR_RISK_FACTOR", "mechanism": "Insulin Resistance"}),
        ("DIS_DIABETES_T2", "MED_METFORMIN", {"relation": "FIRST_LINE_DRUG", "evidence": "ADA Class A"}),
        ("DIS_DIABETES_T2", "LIFE_LOW_GI", {"relation": "MANDATORY_NUTRITION", "desc": "Giảm tải đường huyết sau ăn"}),
        ("DIS_DIABETES_T2", "COMP_NEPHROPATHY", {"relation": "CAN_CAUSE", "pathway": "Microvascular"}),
        ("DIS_DIABETES_T2", "COMP_RETINOPATHY", {"relation": "CAN_CAUSE", "pathway": "Microvascular"}),
        ("DIS_DIABETES_T2", "COMP_NEUROPATHY", {"relation": "CAN_CAUSE", "pathway": "Microvascular"}),

        # High-Risk Diabetes + CVD
        ("FEAT_HEART_DISEASE", "DIS_DIABETES_CVD", {"relation": "TRIGGERS_RISK_TIER", "risk": "Very High"}),
        ("FEAT_HYPERTENSION", "DIS_DIABETES_CVD", {"relation": "SYNERGISTIC_RISK", "desc": "Gấp đôi nguy cơ tim mạch"}),
        ("FEAT_SMOKING", "DIS_DIABETES_CVD", {"relation": "ACCELERATES", "desc": "Thúc đẩy xơ vữa"}),
        ("DIS_DIABETES_CVD", "MED_SGLT2I", {"relation": "MANDATORY_CARDIOPROTECTIVE", "evidence": "EMPA-REG / DAPA-HF"}),
        ("DIS_DIABETES_CVD", "MED_GLP1RA", {"relation": "MANDATORY_CARDIOPROTECTIVE", "evidence": "LEADER / SUSTAIN-6"}),
        ("DIS_DIABETES_CVD", "LIFE_STOP_SMOKING", {"relation": "URGENT_INTERVENTION", "desc": "Giảm ngay 50% nguy cơ nhồi máu tái phát"}),
        ("DIS_DIABETES_CVD", "COMP_CAD", {"relation": "HIGH_COMPLICATION_RISK", "severity": "Life-Threatening"}),

        # Very high HbA1c
        ("FEAT_HBA1C_VERY_HIGH", "MED_INSULIN", {"relation": "REQUIRES_EARLY_INITIATION", "evidence": "ADA 2024"}),
        ("FEAT_GLUCOSE_SEVERE", "MED_INSULIN", {"relation": "REQUIRES_INSULIN_THERAPY", "desc": "Khắc phục ngộ độc đường cấp"}),

        # Safety & Contraindication rules
        ("FEAT_HEART_DISEASE", "MED_SU", {"relation": "PRECAUTION", "desc": "Tránh hạ đường huyết gây khởi phát cơn thiếu máu cơ tim ở bệnh nhân tim mạch."})
    ]

    for u, v, data in edges:
        G.add_edge(u, v, **data)

    # Export to JSON
    json_data = nx.node_link_data(G)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    print(f"[✓] Đã tạo Diabetes Knowledge Graph với {G.number_of_nodes()} thực thể, {G.number_of_edges()} quan hệ tại: {OUT_JSON}")
    return G

if __name__ == "__main__":
    build_diabetes_knowledge_graph()
