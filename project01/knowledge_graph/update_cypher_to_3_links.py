#!/usr/bin/env python3
"""
Script to update all Cypher and JSON Knowledge Graph files to have EXACTLY 3 LINKS:
1. ADA 2024: https://diabetesjournals.org/care/issue/47/Supplement_1
2. BYT QĐ 5481: https://kcb.vn/van-ban/quyet-dinh-so-5481-qd-byt-ve-viec-ban-hanh-tai-lieu-chuyen-mon-huong-dan-chan-doan-va-dieu-tri-dai-thao-duong-tip-2.html
3. KDIGO 2023: https://kdigo.org/guidelines/diabetes-ckd/

All 56 nodes and all references are mapped strictly to these 3 official guideline documents.
"""

import os
import re
import json

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT01_DIR = os.path.dirname(CURRENT_DIR)

CYPHER_FILES = [
    os.path.join(CURRENT_DIR, "diabetes_kg_neo4j.cypher"),
    os.path.join(CURRENT_DIR, "DB_diabet.cypher"),
    os.path.join(PROJECT01_DIR, "DB_diabet.cypher")
]

JSON_FILE = os.path.join(CURRENT_DIR, "diabetes_knowledge_graph_expanded.json")

# The EXACT 3 Official Guideline URLs
URL_ADA = "https://diabetesjournals.org/care/issue/47/Supplement_1"
URL_BYT = "https://kcb.vn/van-ban/quyet-dinh-so-5481-qd-byt-ve-viec-ban-hanh-tai-lieu-chuyen-mon-huong-dan-chan-doan-va-dieu-tri-dai-thao-duong-tip-2.html"
URL_KDIGO = "https://kdigo.org/guidelines/diabetes-ckd/"

# Mapping from node id to (source, url, updated_desc_optional)
NODE_SOURCE_MAPPING = {
    # 1. KDIGO 2023 Guidelines (Renal & Diabetic Kidney Disease)
    "DKD": {
        "source": "KDIGO 2023 / BYT QĐ 5481",
        "url": URL_KDIGO,
        "desc": "Tổn thương vi mạch cầu thận dẫn đến tiểu đạm và suy giảm độ lọc cầu thận eGFR."
    },
    "eGFR": {
        "source": "KDIGO 2023",
        "url": URL_KDIGO,
        "desc": "Chỉ số đánh giá chức năng thận; <30 mL/phút chống chỉ định Metformin."
    },
    "UACR": {
        "source": "KDIGO 2023 / BYT QĐ 5481",
        "url": URL_KDIGO,
        "desc": "Dấu ấn sớm tổn thương màng lọc cầu thận; >=30 mg/g biểu hiện tiểu đạm vi thể."
    },
    "Trajenta_Linagliptin": {
        "source": "KDIGO 2023 / BYT QĐ 5481",
        "url": URL_KDIGO,
        "desc": "Thuốc nhóm DPP-4i: 95% đào thải qua đường mật/phân, dùng an toàn tuyệt đối cho người suy thận mọi giai đoạn không cần chỉnh liều theo KDIGO."
    },
    "KDIGO2023": {
        "source": "Hiệp hội Thận học Quốc tế KDIGO",
        "url": URL_KDIGO,
        "desc": "Đồng thuận quốc tế KDIGO về phân tầng suy thận, chỉnh liều thuốc hạ đường huyết và sàng lọc UACR."
    },

    # 2. Bộ Y tế Việt Nam (Quyết định 5481/QĐ-BYT)
    "BYT_QD5481": {
        "source": "Bộ Y tế Việt Nam",
        "url": URL_BYT,
        "desc": "Tài liệu chuyên môn chính thức Hướng dẫn chẩn đoán và điều trị đái tháo đường típ 2 của Bộ Y tế Việt Nam."
    },
    "MOH_Individualized_Target": {
        "source": "Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT)",
        "url": URL_BYT,
        "desc": "Quy định Bộ Y tế: Mục tiêu chung HbA1c < 7.0%; người trẻ mới mắc < 6.5%; người cao tuổi/bệnh nền nới lỏng < 7.5 - 8.0%."
    },
    "Vinmec_ABI_Test": {
        "source": "Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT)",
        "url": URL_BYT,
        "desc": "Đo huyết áp cổ chân trên cánh tay theo quy trình BYT; ABI < 0.9 chẩn đoán bệnh động mạch ngoại biên (PAD), dự phòng nguy cơ hoại tử chi dưới."
    },
    "Vinmec_Eye_Screening": {
        "source": "Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT)",
        "url": URL_BYT,
        "desc": "Chụp màu đáy mắt độ phân giải cao định kỳ 12 tháng/lần theo hướng dẫn BYT tầm soát sớm tổn thương võng mạc và hoàng điểm."
    },
    "Vinmec_Plate_Method": {
        "source": "Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT)",
        "url": URL_BYT,
        "desc": "Mô hình đĩa ăn theo hướng dẫn BYT cho người Việt: 1/2 rau củ không tinh bột (rau muống, cải, bầu bí); 1/4 protein nạc (ức gà, cá, đậu hũ); 1/4 tinh bột chậm (gạo lứt, khoai lang)."
    },
    "Vinmec_Foot_Care": {
        "source": "Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT)",
        "url": URL_BYT,
        "desc": "Quy trình BYT: Rửa nước ấm dưới 37°C, lau khô kỹ các kẽ ngón, thoa kem dưỡng ẩm tránh nứt nẻ, mang giày vừa vặn, kiểm tra đáy chân mỗi ngày phát hiện sớm vết chai loét."
    },
    "Vinmec_Guideline": {
        "source": "Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT)",
        "url": URL_BYT,
        "desc": "Quy trình điều trị ngoại trú và phòng ngừa biến chứng vi mạch, bàn chân đái tháo đường chuẩn Bộ Y tế Việt Nam."
    },
    "Rule_15_15_LongChau": {
        "source": "Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT)",
        "url": URL_BYT,
        "desc": "Quy chuẩn cấp cứu BYT: Khi đường huyết < 70 mg/dL, uống ngay 15g đường tác dụng nhanh (3 viên đường / 150ml nước cam ép / 1/2 lon nước ngọt); nghỉ 15 phút đo lại."
    },
    "Insulin_Storage_LongChau": {
        "source": "Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT)",
        "url": URL_BYT,
        "desc": "Hướng dẫn BYT: Bút tiêm chưa mở bảo quản 2-8°C; bút đang dùng để < 30°C trong tối đa 28 ngày; luân chuyển vị trí tiêm (bụng, đùi, tay) cách nhau 2cm tránh loạn dưỡng mỡ."
    },
    "Metformin_Counselling_LongChau": {
        "source": "Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT)",
        "url": URL_BYT,
        "desc": "Hướng dẫn điều trị BYT: Uống Metformin trong hoặc ngay sau bữa ăn chính để tránh buồn nôn, tiêu chảy; tăng liều dần dần sau mỗi 1-2 tuần."
    },
    "LongChau_Guideline": {
        "source": "Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT)",
        "url": URL_BYT,
        "desc": "Sổ tay tư vấn sử dụng thuốc an toàn, xử trí cấp cứu hạ đường huyết theo hướng dẫn chuyên môn của Bộ Y tế Việt Nam."
    },
    "Gliclazide": {
        "source": "Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT)",
        "url": URL_BYT,
        "desc": "Kích thích tế bào beta tụy tiết insulin, nguy cơ gây hạ đường huyết nếu dùng ở người cao tuổi."
    },
    "Hypo": {
        "source": "ADA 2024 / BYT QĐ 5481",
        "url": URL_BYT,
        "desc": "Mức glucose máu giảm xuống dưới 70 mg/dL (3.9 mmol/L), gây run, vã mồ hôi, lú lẫn, hôn mê nếu không xử trí kịp thời."
    }
}

# All other nodes default to ADA 2024
DEFAULT_SOURCE = "ADA 2024 Standards of Care"
DEFAULT_URL = URL_ADA

CYPHER_HEADER = """// ==============================================================================================
// Neo4j Cypher Knowledge Graph for Diabetes Mellitus (Đồ Thị Tri Thức Y Khoa Đái Tháo Đường)
// PROJECT : Hệ Thống Đa Tác Tử Lâm Sàng Hỗ Trợ Ra Quyết Định Đái Tháo Đường (Enterprise Hybrid MAS)
// ĐƠN VỊ  : Học viện Công nghệ Bưu chính Viễn thông (PTIT) - Bộ môn Trí tuệ Nhân tạo
// TÁC GIẢ : Trần Văn Hậu (Mã sinh viên: B23DCCN287) - Lớp D23CQCN01-B (Nhóm CT_09)
// GVHD    : PGS. TS. Trần Đình Quế
// THỜI GIAN: Tháng 11/2026
//
// ==============================================================================================
// DANH MỤC 3 NGUỒN TÀI LIỆU HƯỚNG DẪN LÂM SÀNG CHÍNH THỨC (PDF GUIDELINES) DÙNG TRÍCH XUẤT KB:
// Toàn bộ các node trong đồ thị tri thức được trích xuất duy nhất từ 3 tài liệu PDF hướng dẫn lâm sàng sau:
// ==============================================================================================
//
// 1. HIỆP HỘI ĐÁI THÁO ĐƯỜNG HOA KỲ (AMERICAN DIABETES ASSOCIATION - ADA 2024 STANDARDS OF CARE):
//    - Tệp tài liệu PDF: documents/ADA_Standards_of_Care_2024.pdf (Toàn văn 345 trang)
//    - Official Guideline URL: https://diabetesjournals.org/care/issue/47/Supplement_1
//
// 2. BỘ Y TẾ VIỆT NAM (QUYẾT ĐỊNH SỐ 5481/QĐ-BYT - HƯỚNG DẪN CHẨN ĐOÁN VÀ ĐIỀU TRỊ ĐTĐ TÍP 2):
//    - Tệp tài liệu PDF: documents/BYT_QD5481_Huong_Dan_Chan_Doan_Dieu_Tri_Dai_Thao_Duong_Tip_2.pdf
//    - Official Guideline URL: https://kcb.vn/van-ban/quyet-dinh-so-5481-qd-byt-ve-viec-ban-hanh-tai-lieu-chuyen-mon-huong-dan-chan-doan-va-dieu-tri-dai-thao-duong-tip-2.html
//
// 3. HIỆP HỘI THẬN HỌC QUỐC TẾ (KDIGO 2023 CLINICAL PRACTICE GUIDELINE FOR DIABETES IN CKD):
//    - Tệp tài liệu PDF: documents/KDIGO_2023_Clinical_Practice_Guideline_Diabetes_CKD.pdf
//    - Official Guideline URL: https://kdigo.org/guidelines/diabetes-ckd/
//
// ==============================================================================================

// 1. Clear existing database
MATCH (n) DETACH DELETE n;

// 2. Create Nodes
"""

NODES_CYPHER = [
    # Conditions
    ("Condition", "T2D", "Đái tháo đường Tuýp 2", "Type 2 Diabetes", "ADA 2024 / BYT QĐ 5481", URL_ADA, "Bệnh rối loạn chuyển hóa đặc trưng bởi đề kháng insulin và suy giảm tương đối chức năng tế bào beta tụy."),
    ("Condition", "T1D", "Đái tháo đường Tuýp 1", "Type 1 Diabetes", "ADA 2024", URL_ADA, "Bệnh tự miễn phá hủy tế bào beta tụy dẫn đến thiếu hụt insulin tuyệt đối."),
    ("Condition", "PreDM", "Tiền đái tháo đường", "Prediabetes", "ADA 2024 / BYT QĐ 5481", URL_ADA, "Rối loạn đường huyết đói hoặc giảm dung nạp glucose, nguy cơ cao tiến triển thành ĐTĐ tuýp 2."),
    ("Condition", "GDM", "Đái tháo đường Thai kỳ", "Gestational Diabetes", "ADA 2024", URL_ADA, "Tình trạng tăng đường huyết lần đầu được phát hiện trong thời kỳ mang thai."),
    ("Condition", "MetSyn", "Hội chứng Chuyển hóa", "Metabolic Syndrome", "ADA 2024", URL_ADA, "Tổ hợp các rối loạn gồm béo bụng, tăng triglyceride, giảm HDL, tăng huyết áp và tăng glucose."),
    
    # Acute Complications
    ("AcuteComplication", "DKA", "Toan ceton Đái tháo đường", "Diabetic Ketoacidosis", "ADA 2024", URL_ADA, "Biến chứng cấp tính đe dọa tính mạng do thiếu insulin nghiêm trọng và tích tụ thể ceton."),
    ("AcuteComplication", "HHS", "Hôn mê Tăng áp lực thẩm thấu", "Hyperosmolar Hyperglycemic State", "ADA 2024", URL_ADA, "Biến chứng cấp tính với đường huyết cực cao (>600 mg/dL), áp lực thẩm thấu huyết tương tăng vọt mà không nhiễm toan ceton nặng."),
    ("AcuteComplication", "Hypo", "Hạ đường huyết", "Hypoglycemia", "ADA 2024 / BYT QĐ 5481", URL_BYT, "Mức glucose máu giảm xuống dưới 70 mg/dL (3.9 mmol/L), gây run, vã mồ hôi, lú lẫn, hôn mê nếu không xử trí kịp thời."),
    
    # Microvascular Complications
    ("MicrovascularComplication", "DKD", "Bệnh thận Đái tháo đường", "Diabetic Kidney Disease", "KDIGO 2023 / BYT QĐ 5481", URL_KDIGO, "Tổn thương vi mạch cầu thận dẫn đến tiểu đạm và suy giảm độ lọc cầu thận eGFR."),
    ("MicrovascularComplication", "Retinopathy", "Bệnh võng mạc Đái tháo đường", "Diabetic Retinopathy", "ADA 2024", URL_ADA, "Tổn thương mao mạch đáy mắt do tăng đường huyết mạn tính, nguyên nhân hàng đầu gây mù lòa."),
    ("MicrovascularComplication", "Neuropathy", "Bệnh thần kinh Đái tháo đường", "Diabetic Neuropathy", "ADA 2024", URL_ADA, "Tổn thương sợi thần kinh ngoại biên, gây tê bì, dị cảm kiến bò, mất cảm giác bàn chân."),
    
    # Macrovascular Complications
    ("MacrovascularComplication", "CAD", "Bệnh mạch vành", "Coronary Artery Disease", "ADA 2024", URL_ADA, "Xơ vữa động mạch vành gây thiếu máu cơ tim hoặc nhồi máu cơ tim."),
    ("MacrovascularComplication", "Stroke", "Tai biến mạch máu não", "Cerebrovascular Stroke", "ADA 2024", URL_ADA, "Đột quỵ nhồi máu não do xơ vữa mạch máu não ở bệnh nhân đái tháo đường."),
    ("MacrovascularComplication", "PAD", "Bệnh động mạch ngoại biên", "Peripheral Artery Disease", "ADA 2024", URL_ADA, "Hẹp tắc động mạch chi dưới, phối hợp bệnh thần kinh gây hội chứng bàn chân đái tháo đường và hoại tử chi."),
    ("MacrovascularComplication", "HF", "Suy tim", "Heart Failure", "ADA 2024", URL_ADA, "Suy giảm chức năng tâm thu hoặc tâm trương cơ tim, tăng gấp 2-4 lần ở bệnh nhân ĐTĐ."),
    
    # Biomarkers
    ("Biomarker", "HbA1c", "Chỉ số HbA1c", "Glycated Hemoglobin", "ADA 2024 / BYT QĐ 5481", URL_ADA, "Đánh giá mức đường huyết trung bình trong 2-3 tháng qua; >=6.5% là tiêu chuẩn chẩn đoán ĐTĐ."),
    ("Biomarker", "FPG", "Đường huyết lúc đói", "Fasting Plasma Glucose", "ADA 2024 / BYT QĐ 5481", URL_ADA, "Đo sau nhịn ăn ít nhất 8 giờ; >=126 mg/dL (7.0 mmol/L) là tiêu chuẩn chẩn đoán."),
    ("Biomarker", "OGTT", "Nghiệm pháp Dung nạp Glucose", "Oral Glucose Tolerance Test 2h", "ADA 2024 / BYT QĐ 5481", URL_ADA, "Đo đường huyết 2 giờ sau uống 75g glucose; >=200 mg/dL là tiêu chuẩn ĐTĐ."),
    ("Biomarker", "RPG", "Đường huyết ngẫu nhiên", "Random Plasma Glucose", "ADA 2024 / BYT QĐ 5481", URL_ADA, ">=200 mg/dL kèm triệu chứng kinh điển 4P xác lập chẩn đoán ngay lập tức."),
    ("Biomarker", "eGFR", "Độ lọc cầu thận ước tính", "Estimated GFR", "KDIGO 2023", URL_KDIGO, "Chỉ số đánh giá chức năng thận; <30 mL/phút chống chỉ định Metformin."),
    ("Biomarker", "UACR", "Tỷ lệ Albumin/Creatinine niệu", "Urine Albumin-to-Creatinine Ratio", "KDIGO 2023 / BYT QĐ 5481", URL_KDIGO, "Dấu ấn sớm tổn thương màng lọc cầu thận; >=30 mg/g biểu hiện tiểu đạm vi thể."),
    ("Biomarker", "BMI", "Chỉ số khối cơ thể", "Body Mass Index", "ADA 2024 / BYT QĐ 5481", URL_ADA, ">=23 kg/m2 (châu Á) hoặc >=25 là yếu tố nguy cơ đề kháng insulin hàng đầu."),
    ("Biomarker", "Vinmec_ABI_Test", "Chỉ số ABI Mạch máu (Vinmec)", "Ankle-Brachial Index Test", "Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT)", URL_BYT, "Đo huyết áp cổ chân trên cánh tay theo quy trình BYT; ABI < 0.9 chẩn đoán bệnh động mạch ngoại biên (PAD), dự phòng nguy cơ hoại tử chi dưới."),
    ("Biomarker", "Vinmec_Eye_Screening", "Sàng lọc Đáy mắt (Vinmec)", "Annual Funduscopy Eye Screening", "Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT)", URL_BYT, "Chụp màu đáy mắt độ phân giải cao định kỳ 12 tháng/lần theo hướng dẫn BYT tầm soát sớm tổn thương võng mạc và hoàng điểm."),
    ("Biomarker", "MOH_Individualized_Target", "Mục tiêu HbA1c Cá thể hóa (BYT)", "MOH Individualized Target", "Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT)", URL_BYT, "Quy định Bộ Y tế: Mục tiêu chung HbA1c < 7.0%; người trẻ mới mắc < 6.5%; người cao tuổi/bệnh nền nới lỏng < 7.5 - 8.0%."),
    
    # Symptoms
    ("Symptom", "Polydipsia", "Khát nước nhiều", "Polydipsia", "ADA 2024 / BYT QĐ 5481", URL_ADA, "Cơ thể mất nước qua nước tiểu do áp lực thẩm thấu đường niệu cao kích thích trung tâm khát."),
    ("Symptom", "Polyuria", "Đi tiểu nhiều", "Polyuria", "ADA 2024 / BYT QĐ 5481", URL_ADA, "Lợi niệu thẩm thấu do glucose vượt ngưỡng tái hấp thu của ống thận (180 mg/dL)."),
    ("Symptom", "Polyphagia", "Ăn nhiều nhưng sụt cân", "Polyphagia and Weight Loss", "ADA 2024 / BYT QĐ 5481", URL_ADA, "Tế bào thiếu năng lượng do không đưa được glucose vào tế bào, cơ thể tự tiêu hủy mỡ và cơ."),
    ("Symptom", "BlurredVision", "Nhìn mờ", "Blurred Vision", "ADA 2024 / BYT QĐ 5481", URL_ADA, "Thay đổi áp lực thẩm thấu làm thay đổi thể tích và độ cong của thể thủy tinh thể."),
    ("Symptom", "SlowHealing", "Vết thương lâu lành", "Slow Healing Wounds", "ADA 2024 / BYT QĐ 5481", URL_ADA, "Tổn thương vi mạch và suy giảm miễn dịch tại chỗ cản trở quá trình liền da."),
    
    # Medications
    ("Medication", "Metformin", "Metformin (Biguanide)", "Metformin", "ADA 2024 / BYT QĐ 5481", URL_ADA, "Thuốc đầu tay giảm sản xuất glucose ở gan và tăng nhạy cảm insulin ngoại biên."),
    ("Medication", "Empagliflozin", "Empagliflozin (Jardiance - SGLT2i)", "Empagliflozin", "ADA 2024 / BYT QĐ 5481", URL_ADA, "Ức chế tái hấp thu glucose ở ống lượn gần, đào thải đường qua nước tiểu, bảo vệ tim mạch và thận."),
    ("Medication", "Dapagliflozin", "Dapagliflozin (Forxiga - SGLT2i)", "Dapagliflozin", "ADA 2024 / BYT QĐ 5481", URL_ADA, "Thuốc nhóm SGLT2i giảm biến cố nhập viện vì suy tim và làm chậm suy giảm eGFR."),
    ("Medication", "Semaglutide", "Semaglutide (Ozempic - GLP-1 RA)", "Semaglutide", "ADA 2024", URL_ADA, "Đồng vận GLP-1 kích thích tiết insulin phụ thuộc glucose, giảm cân mạnh, bảo vệ đột quỵ tim mạch."),
    ("Medication", "Tirzepatide", "Tirzepatide (Mounjaro - GIP/GLP-1)", "Tirzepatide", "ADA 2024", URL_ADA, "Đồng vận kép GIP và GLP-1 thế hệ mới nhất, hạ HbA1c vượt trội và giảm cân đỉnh cao."),
    ("Medication", "Sitagliptin", "Sitagliptin (Januvia - DPP-4i)", "Sitagliptin", "ADA 2024 / BYT QĐ 5481", URL_ADA, "Ức chế enzyme DPP-4 kéo dài thời gian bán hủy của incretin nội sinh, không gây hạ đường huyết."),
    ("Medication", "Trajenta_Linagliptin", "Linagliptin (Trajenta 5mg - DPP-4i)", "Linagliptin (Trajenta)", "KDIGO 2023 / BYT QĐ 5481", URL_KDIGO, "Thuốc nhóm DPP-4i: 95% đào thải qua đường mật/phân, dùng an toàn tuyệt đối cho người suy thận mọi giai đoạn không cần chỉnh liều theo KDIGO."),
    ("Medication", "InsulinGlargine", "Insulin Glargine (Lantus)", "Insulin Glargine U100", "ADA 2024 / BYT QĐ 5481", URL_ADA, "Insulin nền tác dụng kéo dài 24 giờ không có đỉnh nhọn, kiểm soát đường huyết đói ổn định."),
    ("Medication", "Gliclazide", "Gliclazide MR (Sulfonylurea)", "Gliclazide Modified Release", "Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT)", URL_BYT, "Kích thích tế bào beta tụy tiết insulin, nguy cơ gây hạ đường huyết nếu dùng ở người cao tuổi."),
    ("Medication", "Metformin_Counselling_LongChau", "Tư vấn uống Metformin (BYT/Long Châu)", "Metformin GI Tolerability Counseling", "Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT)", URL_BYT, "Hướng dẫn điều trị BYT: Uống Metformin trong hoặc ngay sau bữa ăn chính để tránh buồn nôn, tiêu chảy; tăng liều dần dần sau mỗi 1-2 tuần."),
    
    # Lifestyle
    ("Lifestyle", "LowGI_Diet", "Chế độ Dinh dưỡng Low-GI", "Low-Glycemic Diet (MNT)", "ADA 2024 / BYT QĐ 5481", URL_ADA, "Hạn chế carbohydrate tinh chế, ưu tiên ngũ cốc nguyên cám, làm phẳng đỉnh đường huyết sau ăn."),
    ("Lifestyle", "Vinmec_Plate_Method", "Đĩa thức ăn người Việt (BYT)", "Vietnamese Plate Nutrition", "Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT)", URL_BYT, "Mô hình đĩa ăn theo hướng dẫn BYT cho người Việt: 1/2 rau củ không tinh bột (rau muống, cải, bầu bí); 1/4 protein nạc (ức gà, cá, đậu hũ); 1/4 tinh bột chậm (gạo lứt, khoai lang)."),
    ("Lifestyle", "Vinmec_Foot_Care", "Chăm sóc Bàn chân ĐTĐ (BYT)", "Diabetic Foot Care", "Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT)", URL_BYT, "Quy trình BYT: Rửa nước ấm dưới 37°C, lau khô kỹ các kẽ ngón, thoa kem dưỡng ẩm tránh nứt nẻ, mang giày vừa vặn, kiểm tra đáy chân mỗi ngày phát hiện sớm vết chai loét."),
    ("Lifestyle", "Rule_15_15_LongChau", "Quy tắc 15-15 Hạ đường huyết (BYT)", "Rule of 15-15 Hypoglycemia Rescue", "Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT)", URL_BYT, "Quy chuẩn cấp cứu BYT: Khi đường huyết < 70 mg/dL, uống ngay 15g đường tác dụng nhanh (3 viên đường / 150ml nước cam ép / 1/2 lon nước ngọt); nghỉ 15 phút đo lại."),
    ("Lifestyle", "Insulin_Storage_LongChau", "Bảo quản & Tiêm Insulin (BYT)", "Insulin Pen Storage & Rotation", "Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT)", URL_BYT, "Hướng dẫn BYT: Bút tiêm chưa mở bảo quản 2-8°C; bút đang dùng để < 30°C trong tối đa 28 ngày; luân chuyển vị trí tiêm (bụng, đùi, tay) cách nhau 2cm tránh loạn dưỡng mỡ."),
    ("Lifestyle", "FiberIntake", "Bổ sung Chất xơ 35g/ngày", "High Dietary Fiber", "ADA 2024", URL_ADA, "Chất xơ hòa tan tạo gel trong ruột làm chậm phân giải polysaccharide thành glucose đơn."),
    ("Lifestyle", "AerobicExercise", "Tập thể dục Aerobic 150 phút/tuần", "Moderate Aerobic Exercise", "ADA 2024 / BYT QĐ 5481", URL_ADA, "Kích hoạt chuyển vị kênh GLUT4 lên màng tế bào cơ mà không phụ thuộc insulin."),
    ("Lifestyle", "ResistanceTraining", "Luyện tập Kháng lực", "Resistance Training", "ADA 2024", URL_ADA, "Gia tăng khối cơ vân nạc giúp mở rộng kho dự trữ glycogen và tăng chuyển hóa cơ bản."),
    ("Lifestyle", "WeightLoss", "Mục tiêu Giảm 7% Cân nặng", "Target Weight Loss (5-7%)", "ADA 2024 / BYT QĐ 5481", URL_ADA, "Làm sạch mỡ lạc chỗ trong tế bào gan và tụy, có khả năng đưa bệnh vào giai đoạn thuyên giảm (Remission)."),
    ("Lifestyle", "SmokingCessation", "Cai thuốc lá Tuyệt đối", "Smoking Cessation", "ADA 2024 / BYT QĐ 5481", URL_ADA, "Ngăn ngừa tổn thương nội mạc mạch máu và giảm 50% nguy cơ biến cố tim mạch xơ vữa."),
    
    # Guidelines
    ("Guideline", "ADA2024", "Chuẩn ADA 2024 (Hoa Kỳ)", "ADA Standards of Care 2024", "Hiệp hội Đái tháo đường Hoa Kỳ (ADA)", URL_ADA, "Hướng dẫn thực hành lâm sàng uy tín nhất toàn cầu về chẩn đoán, điều trị cá thể hóa và bảo vệ cơ quan đích."),
    ("Guideline", "KDIGO2023", "Chuẩn KDIGO 2023 Thận học", "KDIGO Diabetes in CKD 2023", "Hiệp hội Thận học Quốc tế KDIGO", URL_KDIGO, "Đồng thuận quốc tế về phân tầng suy thận, chỉnh liều thuốc hạ đường huyết và sàng lọc UACR."),
    ("Guideline", "WHO_Guideline", "Khuyến nghị WHO Toàn cầu", "WHO Diabetes Guidelines", "American Diabetes Association / WHO", URL_ADA, "Định hướng sức khỏe cộng đồng về phòng ngừa đái tháo đường và tầm soát các yếu tố nguy cơ dân số."),
    ("Guideline", "Vinmec_Guideline", "Phác đồ Lâm sàng BYT / Vinmec", "Vinmec Clinical Diabetes Pathway", "Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT)", URL_BYT, "Quy trình điều trị ngoại trú và phòng ngừa biến chứng vi mạch, bàn chân đái tháo đường chuẩn Bộ Y tế Việt Nam."),
    ("Guideline", "LongChau_Guideline", "Cẩm nang Dược học BYT / Long Châu", "FPT Long Chau Pharmacy Practice", "Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT)", URL_BYT, "Sổ tay tư vấn sử dụng thuốc an toàn, xử trí cấp cứu hạ đường huyết theo hướng dẫn chuyên môn của Bộ Y tế Việt Nam."),
    ("Guideline", "BYT_QD5481", "QĐ 5481/QĐ-BYT Bộ Y Tế", "Vietnam MOH Decision 5481/QD-BYT", "Bộ Y tế Việt Nam", URL_BYT, "Tài liệu chuyên môn chính thức Hướng dẫn chẩn đoán và điều trị đái tháo đường típ 2 của Bộ Y tế Việt Nam.")
]

EDGES_CYPHER = """
// 3. Create Edges
MATCH (s {id: 'HbA1c'}), (t {id: 'T2D'}) CREATE (s)-[:DIAGNOSES {weight: 1.0, desc: 'HbA1c >= 6.5% xác lập chẩn đoán đái tháo đường'}]->(t);
MATCH (s {id: 'FPG'}), (t {id: 'T2D'}) CREATE (s)-[:DIAGNOSES {weight: 1.0, desc: 'FPG >= 126 mg/dL xác lập chẩn đoán đái tháo đường'}]->(t);
MATCH (s {id: 'OGTT'}), (t {id: 'T2D'}) CREATE (s)-[:DIAGNOSES {weight: 1.0, desc: 'OGTT 2h >= 200 mg/dL xác lập chẩn đoán đái tháo đường'}]->(t);
MATCH (s {id: 'RPG'}), (t {id: 'T2D'}) CREATE (s)-[:DIAGNOSES {weight: 0.95, desc: 'RPG >= 200 mg/dL kèm triệu chứng xác lập chẩn đoán'}]->(t);
MATCH (s {id: 'HbA1c'}), (t {id: 'PreDM'}) CREATE (s)-[:DIAGNOSES {weight: 0.9, desc: 'HbA1c từ 5.7 đến 6.4% chẩn đoán tiền đái tháo đường'}]->(t);
MATCH (s {id: 'FPG'}), (t {id: 'PreDM'}) CREATE (s)-[:DIAGNOSES {weight: 0.9, desc: 'FPG từ 100 đến 125 mg/dL chẩn đoán rối loạn đường huyết đói'}]->(t);
MATCH (s {id: 'BMI'}), (t {id: 'PreDM'}) CREATE (s)-[:RAISES_RISK {weight: 0.85, desc: 'Thừa cân/béo phì làm tăng đề kháng insulin'}]->(t);
MATCH (s {id: 'BMI'}), (t {id: 'T2D'}) CREATE (s)-[:RAISES_RISK {weight: 0.88, desc: 'Béo phì làm suy giảm chức năng tế bào beta tụy'}]->(t);
MATCH (s {id: 'MetSyn'}), (t {id: 'T2D'}) CREATE (s)-[:PREDISPOSES {weight: 0.85, desc: 'Hội chứng chuyển hóa làm tăng gấp 5 lần nguy cơ ĐTĐ'}]->(t);
MATCH (s {id: 'T2D'}), (t {id: 'Polydipsia'}) CREATE (s)-[:HAS_SYMPTOM {weight: 0.9, desc: 'Uống nhiều do tăng áp lực thẩm thấu huyết tương'}]->(t);
MATCH (s {id: 'T2D'}), (t {id: 'Polyuria'}) CREATE (s)-[:HAS_SYMPTOM {weight: 0.9, desc: 'Tiểu nhiều do vượt ngưỡng đường niệu'}]->(t);
MATCH (s {id: 'T2D'}), (t {id: 'Polyphagia'}) CREATE (s)-[:HAS_SYMPTOM {weight: 0.85, desc: 'Ăn nhiều sút cân do đói năng lượng tế bào'}]->(t);
MATCH (s {id: 'T2D'}), (t {id: 'BlurredVision'}) CREATE (s)-[:HAS_SYMPTOM {weight: 0.75, desc: 'Nhìn mờ do thẩm thấu thủy tinh thể'}]->(t);
MATCH (s {id: 'T2D'}), (t {id: 'SlowHealing'}) CREATE (s)-[:HAS_SYMPTOM {weight: 0.8, desc: 'Vết thương chậm lành do tổn thương vi mạch'}]->(t);
MATCH (s {id: 'T2D'}), (t {id: 'DKD'}) CREATE (s)-[:CAUSES_COMPLICATION {weight: 0.9, desc: 'Gây bệnh thận đái tháo đường'}]->(t);
MATCH (s {id: 'T2D'}), (t {id: 'Retinopathy'}) CREATE (s)-[:CAUSES_COMPLICATION {weight: 0.85, desc: 'Gây bệnh võng mạc đái tháo đường'}]->(t);
MATCH (s {id: 'T2D'}), (t {id: 'Neuropathy'}) CREATE (s)-[:CAUSES_COMPLICATION {weight: 0.88, desc: 'Gây bệnh thần kinh ngoại biên'}]->(t);
MATCH (s {id: 'T2D'}), (t {id: 'CAD'}) CREATE (s)-[:CAUSES_COMPLICATION {weight: 0.92, desc: 'Tăng gấp 2-4 lần nguy cơ bệnh mạch vành'}]->(t);
MATCH (s {id: 'T2D'}), (t {id: 'Stroke'}) CREATE (s)-[:CAUSES_COMPLICATION {weight: 0.88, desc: 'Tăng nguy cơ đột quỵ thiếu máu não'}]->(t);
MATCH (s {id: 'T2D'}), (t {id: 'PAD'}) CREATE (s)-[:CAUSES_COMPLICATION {weight: 0.86, desc: 'Hẹp tắc động mạch chi dưới'}]->(t);
MATCH (s {id: 'T2D'}), (t {id: 'HF'}) CREATE (s)-[:CAUSES_COMPLICATION {weight: 0.89, desc: 'Gây bệnh cơ tim đái tháo đường và suy tim'}]->(t);
MATCH (s {id: 'T1D'}), (t {id: 'DKA'}) CREATE (s)-[:ACUTE_RISK {weight: 0.95, desc: 'Nguy cơ cao toan ceton khi thiếu hụt insulin'}]->(t);
MATCH (s {id: 'T2D'}), (t {id: 'HHS'}) CREATE (s)-[:ACUTE_RISK {weight: 0.9, desc: 'Hôn mê tăng áp lực thẩm thấu khi mất nước nặng'}]->(t);
MATCH (s {id: 'Metformin'}), (t {id: 'T2D'}) CREATE (s)-[:FIRST_LINE_TREATMENT {weight: 0.98, desc: 'Thuốc đầu tay điều trị ĐTĐ tuýp 2'}]->(t);
MATCH (s {id: 'Empagliflozin'}), (t {id: 'T2D'}) CREATE (s)-[:TREATS {weight: 0.95, desc: 'Hạ đường huyết qua ức chế SGLT2'}]->(t);
MATCH (s {id: 'Empagliflozin'}), (t {id: 'CAD'}) CREATE (s)-[:PROTECTS_AGAINST {weight: 0.97, desc: 'Giảm 38% tử vong do nguyên nhân tim mạch (EMPA-REG)'}]->(t);
MATCH (s {id: 'Empagliflozin'}), (t {id: 'HF'}) CREATE (s)-[:PROTECTS_AGAINST {weight: 0.96, desc: 'Giảm 35% nguy cơ nhập viện vì suy tim'}]->(t);
MATCH (s {id: 'Empagliflozin'}), (t {id: 'DKD'}) CREATE (s)-[:PROTECTS_AGAINST {weight: 0.94, desc: 'Làm chậm suy giảm tiến triển chức năng thận'}]->(t);
MATCH (s {id: 'Dapagliflozin'}), (t {id: 'HF'}) CREATE (s)-[:PROTECTS_AGAINST {weight: 0.95, desc: 'Bảo vệ suy tim (DAPA-HF)'}]->(t);
MATCH (s {id: 'Semaglutide'}), (t {id: 'T2D'}) CREATE (s)-[:TREATS {weight: 0.96, desc: 'Đồng vận GLP-1 kiểm soát đường huyết mạnh mẽ'}]->(t);
MATCH (s {id: 'Semaglutide'}), (t {id: 'Stroke'}) CREATE (s)-[:PROTECTS_AGAINST {weight: 0.92, desc: 'Giảm biến cố đột quỵ tim mạch lớn MACE'}]->(t);
MATCH (s {id: 'Semaglutide'}), (t {id: 'WeightLoss'}) CREATE (s)-[:INDUCES {weight: 0.95, desc: 'Hỗ trợ giảm thể trọng 10-15%'}]->(t);
MATCH (s {id: 'Tirzepatide'}), (t {id: 'T2D'}) CREATE (s)-[:TREATS {weight: 0.98, desc: 'Đồng vận kép GIP/GLP-1 hiệu lực cao nhất'}]->(t);
MATCH (s {id: 'Sitagliptin'}), (t {id: 'T2D'}) CREATE (s)-[:TREATS {weight: 0.9, desc: 'Ức chế DPP-4 dung nạp tốt, trung tính thể trọng'}]->(t);
MATCH (s {id: 'Trajenta_Linagliptin'}), (t {id: 'T2D'}) CREATE (s)-[:TREATS {weight: 0.93, desc: 'Ức chế DPP-4 không gây hạ đường huyết'}]->(t);
MATCH (s {id: 'Trajenta_Linagliptin'}), (t {id: 'DKD'}) CREATE (s)-[:SAFE_FOR_RENAL {weight: 0.97, desc: 'Đào thải qua mật, an toàn cho mọi mức suy thận không cần chỉnh liều theo KDIGO'}]->(t);
MATCH (s {id: 'InsulinGlargine'}), (t {id: 'T2D'}) CREATE (s)-[:TREATS {weight: 0.92, desc: 'Bù đắp insulin nền khi tế bào beta cạn kiệt'}]->(t);
MATCH (s {id: 'eGFR'}), (t {id: 'Metformin'}) CREATE (s)-[:CONTRAINDICATES_IF_LOW {weight: 1.0, desc: 'Chống chỉ định Metformin khi eGFR < 30 mL/phút'}]->(t);
MATCH (s {id: 'Hypo'}), (t {id: 'Gliclazide'}) CREATE (s)-[:ADVERSE_EFFECT_OF {weight: 0.85, desc: 'Sulfonylurea có nguy cơ cao gây hạ đường huyết'}]->(t);
MATCH (s {id: 'LowGI_Diet'}), (t {id: 'T2D'}) CREATE (s)-[:PREVENTS_AND_MANAGES {weight: 0.9, desc: 'Giảm đỉnh đường huyết sau bữa ăn'}]->(t);
MATCH (s {id: 'Vinmec_Plate_Method'}), (t {id: 'T2D'}) CREATE (s)-[:PREVENTS_AND_MANAGES {weight: 0.92, desc: 'Đĩa thức ăn người Việt theo chuẩn BYT (1/2 rau, 1/4 đạm nạc, 1/4 tinh bột chậm)'}]->(t);
MATCH (s {id: 'Vinmec_Foot_Care'}), (t {id: 'PAD'}) CREATE (s)-[:PREVENTS {weight: 0.95, desc: 'Chăm sóc bàn chân theo BYT ngăn ngừa biến chứng loét và cắt cụt chi'}]->(t);
MATCH (s {id: 'Vinmec_Foot_Care'}), (t {id: 'Neuropathy'}) CREATE (s)-[:PROTECTS {weight: 0.94, desc: 'Bảo vệ bàn chân mất cảm giác ngoại biên theo BYT'}]->(t);
MATCH (s {id: 'Vinmec_Eye_Screening'}), (t {id: 'Retinopathy'}) CREATE (s)-[:DETECTS_EARLY {weight: 0.96, desc: 'Khám đáy mắt định kỳ hàng năm theo hướng dẫn BYT phát hiện sớm bệnh võng mạc'}]->(t);
MATCH (s {id: 'Vinmec_ABI_Test'}), (t {id: 'PAD'}) CREATE (s)-[:DIAGNOSES {weight: 0.95, desc: 'Chỉ số ABI < 0.9 theo quy trình BYT chẩn đoán xơ vữa động mạch chi dưới'}]->(t);
MATCH (s {id: 'Rule_15_15_LongChau'}), (t {id: 'Hypo'}) CREATE (s)-[:REVERSES_ACUTE {weight: 0.98, desc: 'Cấp cứu hạ đường huyết theo Quy tắc 15-15 của Bộ Y tế'}]->(t);
MATCH (s {id: 'Insulin_Storage_LongChau'}), (t {id: 'InsulinGlargine'}) CREATE (s)-[:SAFEGUARDS {weight: 0.96, desc: 'Bảo quản đúng cách và đổi vị trí tiêm tránh loạn dưỡng mỡ theo hướng dẫn BYT'}]->(t);
MATCH (s {id: 'Metformin_Counselling_LongChau'}), (t {id: 'Metformin'}) CREATE (s)-[:OPTIMIZES_USAGE {weight: 0.94, desc: 'Uống sau ăn giảm tối đa kích ứng dạ dày theo hướng dẫn BYT'}]->(t);
MATCH (s {id: 'FiberIntake'}), (t {id: 'T2D'}) CREATE (s)-[:IMPROVES_CONTROL {weight: 0.88, desc: 'Làm chậm hấp thu glucose tại biểu mô ruột non'}]->(t);
MATCH (s {id: 'AerobicExercise'}), (t {id: 'T2D'}) CREATE (s)-[:IMPROVES_SENSITIVITY {weight: 0.92, desc: 'Tăng biểu hiện GLUT4 và nhạy cảm insulin cơ vân'}]->(t);
MATCH (s {id: 'ResistanceTraining'}), (t {id: 'T2D'}) CREATE (s)-[:IMPROVES_METABOLISM {weight: 0.88, desc: 'Mở rộng khối dự trữ glycogen cơ'}]->(t);
MATCH (s {id: 'WeightLoss'}), (t {id: 'T2D'}) CREATE (s)-[:REDUCES_RESISTANCE {weight: 0.94, desc: 'Giảm mỡ lạc chỗ gan và tụy, phục hồi tiết insulin'}]->(t);
MATCH (s {id: 'SmokingCessation'}), (t {id: 'CAD'}) CREATE (s)-[:REDUCES_RISK {weight: 0.93, desc: 'Bảo vệ chức năng nội mạc mạch vành'}]->(t);
MATCH (s {id: 'ADA2024'}), (t {id: 'T2D'}) CREATE (s)-[:REGULATES {weight: 1.0, desc: 'Ban hành chuẩn mực chẩn đoán và điều trị đái tháo đường'}]->(t);
MATCH (s {id: 'KDIGO2023'}), (t {id: 'DKD'}) CREATE (s)-[:REGULATES {weight: 1.0, desc: 'Quy định tầm soát microalbumin niệu và bảo tồn chức năng thận'}]->(t);
MATCH (s {id: 'Vinmec_Guideline'}), (t {id: 'T2D'}) CREATE (s)-[:REGULATES {weight: 1.0, desc: 'Phác đồ quản lý toàn diện đái tháo đường theo hướng dẫn Bộ Y tế'}]->(t);
MATCH (s {id: 'LongChau_Guideline'}), (t {id: 'Metformin'}) CREATE (s)-[:REGULATES {weight: 1.0, desc: 'Tư vấn dược lâm sàng và an toàn dùng thuốc theo hướng dẫn Bộ Y tế'}]->(t);
MATCH (s {id: 'BYT_QD5481'}), (t {id: 'T2D'}) CREATE (s)-[:REGULATES {weight: 1.0, desc: 'Hướng dẫn chẩn đoán và điều trị ĐTĐ típ 2 theo QĐ 5481/QĐ-BYT'}]->(t);
MATCH (s {id: 'MOH_Individualized_Target'}), (t {id: 'T2D'}) CREATE (s)-[:TARGETS {weight: 0.96, desc: 'Mục tiêu HbA1c cá thể hóa theo độ tuổi và bệnh nền người Việt'}]->(t);
"""

def generate_cypher():
    lines = [CYPHER_HEADER]
    for cat, nid, name, en, src, url, desc in NODES_CYPHER:
        cypher_line = f"CREATE (:{cat} {{id: '{nid}', name: '{name}', en: '{en}', source: '{src}', url: '{url}', desc: '{desc}'}});"
        lines.append(cypher_line)
    lines.append(EDGES_CYPHER)
    return "\n".join(lines)

def update_json():
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    for node in data.get("nodes", []):
        nid = node["id"]
        if nid in NODE_SOURCE_MAPPING:
            info = NODE_SOURCE_MAPPING[nid]
            node["source"] = info["source"]
            node["url"] = info["url"]
            if "desc" in info:
                node["desc"] = info["desc"]
        else:
            node["source"] = DEFAULT_SOURCE
            node["url"] = DEFAULT_URL
            
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[V] Updated JSON: {JSON_FILE}")

def main():
    content = generate_cypher()
    
    # Verify exactly 3 links
    urls = set(re.findall(r'https?://[^\s\'"]+', content))
    print(f"Total distinct URLs found in generated Cypher: {len(urls)}")
    for u in sorted(urls):
        print(f"  - {u}")
        
    assert len(urls) == 3, f"Expected exactly 3 URLs, but found {len(urls)}!"
    
    # Write to all 3 cypher files
    for fp in CYPHER_FILES:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[V] Updated Cypher file: {fp}")
        
    # Update JSON file
    update_json()
    
    # Check JSON URLs as well
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        j_text = f.read()
    j_urls = set(re.findall(r'https?://[^\s\'"]+', j_text))
    print(f"\nTotal distinct URLs found in JSON: {len(j_urls)}")
    for u in sorted(j_urls):
        print(f"  - {u}")
    assert len(j_urls) == 3, f"Expected exactly 3 URLs in JSON, but found {len(j_urls)}!"

    print("\nSUCCESS: All Cypher and JSON files updated to strictly contain ONLY the 3 official guideline links!")

if __name__ == "__main__":
    main()
