"""
diabetes_kg.py
Đồ thị Tri thức Y tế Việt Nam (VietnamDiabetesKG): Bệnh Đái tháo đường típ 2,
phác đồ điều trị Bộ Y Tế (Quyết định 5481/QĐ-BYT), tương tác thuốc, dinh dưỡng và biến chứng.
"""
from .ontology import Ontology, Predicate
from .kg_base import KnowledgeGraph

def build_vietnam_diabetes_ontology() -> Ontology:
    onto = Ontology("VietnamDiabetesOntology")
    
    # Class hierarchy
    classes = [
        ("MedicalEntity", "Thing"),
        ("Disease", "MedicalEntity"),
        ("ClinicalIndicator", "MedicalEntity"),
        ("Medication", "MedicalEntity"),
        ("OralAntidiabetic", "Medication"),
        ("InjectableAgent", "Medication"),
        ("Biguanide", "OralAntidiabetic"),
        ("SGLT2i", "OralAntidiabetic"),
        ("Sulfonylurea", "OralAntidiabetic"),
        ("Thiazolidinedione", "OralAntidiabetic"),
        ("Insulin", "InjectableAgent"),
        ("Substance", "MedicalEntity"),
        ("Complication", "MedicalEntity"),
        ("Food", "MedicalEntity"),
        ("LowGIFood", "Food"),
        ("HighGIFood", "Food"),
        ("LeanProtein", "Food"),
        ("ManagementProtocol", "MedicalEntity")
    ]
    for child, parent in classes:
        onto.add_class(child, parent)

    # Predicates with domain, range and semantic labels
    preds = [
        Predicate("CHI_DINH_DAU_TAY", "Medication", "Disease", "là chỉ định đầu tay cho"),
        Predicate("CHONG_CHI_DINH_KHI", "Medication", "MedicalEntity", "chống chỉ định nghiêm ngặt khi có"),
        Predicate("TUONG_TAC_NGUY_HIEM", "Medication", "Substance", "tương tác nguy hiểm đe dọa tính mạng với", is_symmetric=True),
        Predicate("CO_NGUY_CO_BIEN_CHUNG", "MedicalEntity", "Complication", "làm tăng nguy cơ biến chứng"),
        Predicate("UU_TIEN_KHI_KEM", "Medication", "Disease", "được ưu tiên chỉ định vượt trội khi kèm"),
        Predicate("TIEU_CHUAN_CHAN_DOAN", "ClinicalIndicator", "Disease", "là tiêu chuẩn khẳng định chẩn đoán của"),
        Predicate("KHUYEN_NGHI_AN", "Disease", "Food", "khuyến nghị tăng cường trong chế độ ăn của"),
        Predicate("HAN_CHE_AN", "Disease", "HighGIFood", "yêu cầu hạn chế hoặc định lượng nghiêm ngặt cho"),
        Predicate("XU_TRI_BANG", "Complication", "MedicalEntity", "được xử trí cấp cứu tức thì bằng"),
        Predicate("BIEN_CHUNG_CUA", "Disease", "Complication", "có thể dẫn tới biến chứng mạn tính nguy hiểm")
    ]
    for p in preds:
        onto.add_predicate(p)

    return onto

def build_vietnam_diabetes_kg() -> KnowledgeGraph:
    onto = build_vietnam_diabetes_ontology()
    kg = KnowledgeGraph("VietnamDiabetesKG", onto)

    # 1. Diseases
    kg.add_node("Dai_Thao_Duong_Tip_2", "Disease", "Đái tháo đường típ 2", ["tiểu đường", "tiểu đường tuýp 2", "t2d", "dtd tip 2"])
    kg.add_node("Tien_Dai_Thao_Duong", "Disease", "Tiền đái tháo đường", ["tiền tiểu đường", "pre-diabetes", "roi loan dung nap"])
    kg.add_node("Suy_Than_Nang", "Disease", "Suy thận nặng (eGFR < 30 mL/phút)", ["suy thận mạn nặng", "egfr < 30", "ckd stage 4"])
    kg.add_node("Suy_Tim", "Disease", "Suy tim xung huyết (Heart Failure)", ["suy tim", "suy tim nyha", "hfref", "hfpef"])
    kg.add_node("Suy_Gan", "Disease", "Suy tế bào gan nặng", ["suy gan"])

    # 2. Clinical Indicators
    kg.add_node("HbA1c_DTD", "ClinicalIndicator", "HbA1c >= 6.5%", ["hba1c 6.5", "hba1c >= 6.5"])
    kg.add_node("Glucose_Doi_DTD", "ClinicalIndicator", "Glucose máu lúc đói >= 126 mg/dL (7.0 mmol/L)", ["glucose lúc đói >= 126", "fpg >= 126"])
    kg.add_node("OGTT_2h_DTD", "ClinicalIndicator", "OGTT 2 giờ >= 200 mg/dL", ["ogtt >= 200"])
    kg.add_node("HbA1c_Tien", "ClinicalIndicator", "HbA1c 5.7% - 6.4%", ["hba1c 5.7-6.4", "hba1c tiền đái tháo đường"])
    kg.add_node("Glucose_Doi_Tien", "ClinicalIndicator", "Glucose lúc đói 100 - 125 mg/dL", ["glucose 100-125"])

    # 3. Medications
    kg.add_node("Metformin", "Biguanide", "Metformin (Glucophage 500/850/1000mg)", ["metformin", "glucophage"])
    kg.add_node("SGLT2_Empagliflozin", "SGLT2i", "Thuốc ức chế SGLT2 (Empagliflozin / Jardiance)", ["sglt2", "empagliflozin", "jardiance", "dapagliflozin"])
    kg.add_node("Sulfonylurea_Gliclazide", "Sulfonylurea", "Sulfonylurea (Gliclazide / Diamicron MR)", ["gliclazide", "diamicron", "sulfonylurea"])
    kg.add_node("Pioglitazone", "Thiazolidinedione", "Pioglitazone (Actos)", ["pioglitazone", "tzd"])
    kg.add_node("Insulin_Lieu", "Insulin", "Insulin ngoại sinh", ["tiêm insulin", "insulin"])

    # 4. Substances & Complications
    kg.add_node("Ruou_Bia", "Substance", "Rượu bia (Ethanol / Đồ uống có cồn)", ["rượu", "bia", "uống bia", "uống rượu", "ethanol"])
    kg.add_node("Toan_Acid_Lactic", "Complication", "Toan chuyển hóa Acid Lactic (Lactic Acidosis)", ["nhiễm toan lactic", "toan lactic", "lactic acidosis"])
    kg.add_node("Ha_Duong_Huyet", "Complication", "Hạ đường huyết cấp (< 70 mg/dL)", ["hạ đường huyết", "tụt đường huyết", "hypoglycemia"])
    kg.add_node("Bien_Chung_Than", "Complication", "Bệnh thận đái tháo đường (Diabetic Nephropathy)", ["biến chứng thận", "vi đạm niệu"])
    kg.add_node("Duong_Nhanh_15g", "MedicalEntity", "Carbohydrate hấp thu nhanh 15g (Quy tắc 15-15)", ["quy tắc 15-15", "nước đường", "kẹo ngọt"])

    # 5. Food & Nutrition
    kg.add_node("Thit_Ga_Luoc", "LeanProtein", "Thịt gà luộc / Ức gà bỏ da (GI = 0)", ["thịt gà", "thịt gà luộc", "ức gà", "ga luoc"])
    kg.add_node("Com_Trang", "HighGIFood", "Cơm trắng (GI = 73 - 83)", ["cơm trắng", "cơm", "com trang"])
    kg.add_node("Xoi_Nep", "HighGIFood", "Xôi nếp (GI = 85 - 93)", ["xôi nếp", "xôi", "bánh chưng"])
    kg.add_node("Rau_Xanh", "LowGIFood", "Rau xanh các loại (GI < 15, giàu chất xơ)", ["rau xanh", "rau cải", "rau muống", "chất xơ"])
    kg.add_node("Gao_Lut", "LowGIFood", "Gạo lứt nguyên cám (GI = 50)", ["gạo lứt", "gao lut"])

    # Triples / Facts
    # Diagnostic rules
    kg.add_fact("HbA1c_DTD", "TIEU_CHUAN_CHAN_DOAN", "Dai_Thao_Duong_Tip_2", source="QD-5481-BYT", rule="HbA1c >= 6.5%")
    kg.add_fact("Glucose_Doi_DTD", "TIEU_CHUAN_CHAN_DOAN", "Dai_Thao_Duong_Tip_2", source="QD-5481-BYT", rule="FPG >= 126 mg/dL")
    kg.add_fact("OGTT_2h_DTD", "TIEU_CHUAN_CHAN_DOAN", "Dai_Thao_Duong_Tip_2", source="QD-5481-BYT", rule="OGTT >= 200 mg/dL")
    kg.add_fact("HbA1c_Tien", "TIEU_CHUAN_CHAN_DOAN", "Tien_Dai_Thao_Duong", source="QD-5481-BYT", rule="HbA1c 5.7 - 6.4%")
    kg.add_fact("Glucose_Doi_Tien", "TIEU_CHUAN_CHAN_DOAN", "Tien_Dai_Thao_Duong", source="QD-5481-BYT", rule="FPG 100 - 125 mg/dL")

    # Indications & Contraindications
    kg.add_fact("Metformin", "CHI_DINH_DAU_TAY", "Dai_Thao_Duong_Tip_2", source="QD-5481-BYT", note="Hàng đầu cho đa số bệnh nhân")
    kg.add_fact("Metformin", "CHONG_CHI_DINH_KHI", "Suy_Than_Nang", source="QD-5481-BYT", warning="Tuyệt đối ngừng khi eGFR < 30 mL/phút")
    kg.add_fact("Metformin", "TUONG_TAC_NGUY_HIEM", "Ruou_Bia", source="QD-5481-BYT", effect="Cạnh tranh NAD+ ở gan làm tích tụ acid lactic gây sốc tử vong")
    kg.add_fact("Metformin", "CO_NGUY_CO_BIEN_CHUNG", "Toan_Acid_Lactic", source="QD-5481-BYT", trigger="Khi uống rượu bia hoặc kèm suy thận")

    kg.add_fact("SGLT2_Empagliflozin", "UU_TIEN_KHI_KEM", "Suy_Tim", source="ADA-ESC-2024", note="Giảm 38% nguy cơ tử vong tim mạch và nhập viện")
    kg.add_fact("Pioglitazone", "CHONG_CHI_DINH_KHI", "Suy_Tim", source="FDA-Alert", warning="Gây giữ muối nước nặng thêm suy tim NYHA I-IV")

    kg.add_fact("Sulfonylurea_Gliclazide", "CO_NGUY_CO_BIEN_CHUNG", "Ha_Duong_Huyet", source="QD-5481-BYT", note="Kích thích tiết insulin liên tục kể cả khi bỏ bữa")
    kg.add_fact("Insulin_Lieu", "CO_NGUY_CO_BIEN_CHUNG", "Ha_Duong_Huyet", source="QD-5481-BYT", note="Nguy cơ cao nhất khi dùng quá liều hoặc ăn muộn")
    kg.add_fact("Ha_Duong_Huyet", "XU_TRI_BANG", "Duong_Nhanh_15g", source="QD-5481-BYT", protocol="Quy tắc 15-15: uống 15g đường nhanh và đo lại sau 15 phút")

    kg.add_fact("Dai_Thao_Duong_Tip_2", "BIEN_CHUNG_CUA", "Bien_Chung_Than", source="QD-5481-BYT", note="Gây tổn thương vi mạch cầu thận")

    # Nutrition
    kg.add_fact("Dai_Thao_Duong_Tip_2", "KHUYEN_NGHI_AN", "Thit_Ga_Luoc", source="Nong-Nghiep-DD", advice="GI = 0, protein nạc tuyệt đối an toàn, ăn được")
    kg.add_fact("Dai_Thao_Duong_Tip_2", "KHUYEN_NGHI_AN", "Rau_Xanh", source="Vien-Dinh-Duong", advice="Ăn đầu tiên trước bữa ăn để làm phẳng đỉnh đường huyết")
    kg.add_fact("Dai_Thao_Duong_Tip_2", "KHUYEN_NGHI_AN", "Gao_Lut", source="Vien-Dinh-Duong", advice="Thay thế cơm trắng nhờ chỉ số GI thấp và giàu xơ")
    kg.add_fact("Dai_Thao_Duong_Tip_2", "HAN_CHE_AN", "Com_Trang", source="Vien-Dinh-Duong", rule="Định lượng 1/2 đến 2/3 bát mỗi bữa, ăn sau rau và thịt")
    kg.add_fact("Dai_Thao_Duong_Tip_2", "HAN_CHE_AN", "Xoi_Nep", source="Vien-Dinh-Duong", warning="GI cực cao 85-93, nguy cơ tăng vọt glucose máu sau ăn")

    return kg

if __name__ == "__main__":
    kg = build_vietnam_diabetes_kg()
    print(f"Built VietnamDiabetesKG: {len(kg.G.nodes)} nodes, {len(kg.G.edges)} edges.")
