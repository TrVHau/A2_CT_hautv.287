// ==============================================================================================
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

CREATE (:Condition {id: 'T2D', name: 'Đái tháo đường Tuýp 2', en: 'Type 2 Diabetes', source: 'ADA 2024 / BYT QĐ 5481', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Bệnh rối loạn chuyển hóa đặc trưng bởi đề kháng insulin và suy giảm tương đối chức năng tế bào beta tụy.'});
CREATE (:Condition {id: 'T1D', name: 'Đái tháo đường Tuýp 1', en: 'Type 1 Diabetes', source: 'ADA 2024', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Bệnh tự miễn phá hủy tế bào beta tụy dẫn đến thiếu hụt insulin tuyệt đối.'});
CREATE (:Condition {id: 'PreDM', name: 'Tiền đái tháo đường', en: 'Prediabetes', source: 'ADA 2024 / BYT QĐ 5481', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Rối loạn đường huyết đói hoặc giảm dung nạp glucose, nguy cơ cao tiến triển thành ĐTĐ tuýp 2.'});
CREATE (:Condition {id: 'GDM', name: 'Đái tháo đường Thai kỳ', en: 'Gestational Diabetes', source: 'ADA 2024', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Tình trạng tăng đường huyết lần đầu được phát hiện trong thời kỳ mang thai.'});
CREATE (:Condition {id: 'MetSyn', name: 'Hội chứng Chuyển hóa', en: 'Metabolic Syndrome', source: 'ADA 2024', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Tổ hợp các rối loạn gồm béo bụng, tăng triglyceride, giảm HDL, tăng huyết áp và tăng glucose.'});
CREATE (:AcuteComplication {id: 'DKA', name: 'Toan ceton Đái tháo đường', en: 'Diabetic Ketoacidosis', source: 'ADA 2024', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Biến chứng cấp tính đe dọa tính mạng do thiếu insulin nghiêm trọng và tích tụ thể ceton.'});
CREATE (:AcuteComplication {id: 'HHS', name: 'Hôn mê Tăng áp lực thẩm thấu', en: 'Hyperosmolar Hyperglycemic State', source: 'ADA 2024', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Biến chứng cấp tính với đường huyết cực cao (>600 mg/dL), áp lực thẩm thấu huyết tương tăng vọt mà không nhiễm toan ceton nặng.'});
CREATE (:AcuteComplication {id: 'Hypo', name: 'Hạ đường huyết', en: 'Hypoglycemia', source: 'ADA 2024 / BYT QĐ 5481', url: 'https://kcb.vn/van-ban/quyet-dinh-so-5481-qd-byt-ve-viec-ban-hanh-tai-lieu-chuyen-mon-huong-dan-chan-doan-va-dieu-tri-dai-thao-duong-tip-2.html', desc: 'Mức glucose máu giảm xuống dưới 70 mg/dL (3.9 mmol/L), gây run, vã mồ hôi, lú lẫn, hôn mê nếu không xử trí kịp thời.'});
CREATE (:MicrovascularComplication {id: 'DKD', name: 'Bệnh thận Đái tháo đường', en: 'Diabetic Kidney Disease', source: 'KDIGO 2023 / BYT QĐ 5481', url: 'https://kdigo.org/guidelines/diabetes-ckd/', desc: 'Tổn thương vi mạch cầu thận dẫn đến tiểu đạm và suy giảm độ lọc cầu thận eGFR.'});
CREATE (:MicrovascularComplication {id: 'Retinopathy', name: 'Bệnh võng mạc Đái tháo đường', en: 'Diabetic Retinopathy', source: 'ADA 2024', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Tổn thương mao mạch đáy mắt do tăng đường huyết mạn tính, nguyên nhân hàng đầu gây mù lòa.'});
CREATE (:MicrovascularComplication {id: 'Neuropathy', name: 'Bệnh thần kinh Đái tháo đường', en: 'Diabetic Neuropathy', source: 'ADA 2024', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Tổn thương sợi thần kinh ngoại biên, gây tê bì, dị cảm kiến bò, mất cảm giác bàn chân.'});
CREATE (:MacrovascularComplication {id: 'CAD', name: 'Bệnh mạch vành', en: 'Coronary Artery Disease', source: 'ADA 2024', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Xơ vữa động mạch vành gây thiếu máu cơ tim hoặc nhồi máu cơ tim.'});
CREATE (:MacrovascularComplication {id: 'Stroke', name: 'Tai biến mạch máu não', en: 'Cerebrovascular Stroke', source: 'ADA 2024', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Đột quỵ nhồi máu não do xơ vữa mạch máu não ở bệnh nhân đái tháo đường.'});
CREATE (:MacrovascularComplication {id: 'PAD', name: 'Bệnh động mạch ngoại biên', en: 'Peripheral Artery Disease', source: 'ADA 2024', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Hẹp tắc động mạch chi dưới, phối hợp bệnh thần kinh gây hội chứng bàn chân đái tháo đường và hoại tử chi.'});
CREATE (:MacrovascularComplication {id: 'HF', name: 'Suy tim', en: 'Heart Failure', source: 'ADA 2024', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Suy giảm chức năng tâm thu hoặc tâm trương cơ tim, tăng gấp 2-4 lần ở bệnh nhân ĐTĐ.'});
CREATE (:Biomarker {id: 'HbA1c', name: 'Chỉ số HbA1c', en: 'Glycated Hemoglobin', source: 'ADA 2024 / BYT QĐ 5481', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Đánh giá mức đường huyết trung bình trong 2-3 tháng qua; >=6.5% là tiêu chuẩn chẩn đoán ĐTĐ.'});
CREATE (:Biomarker {id: 'FPG', name: 'Đường huyết lúc đói', en: 'Fasting Plasma Glucose', source: 'ADA 2024 / BYT QĐ 5481', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Đo sau nhịn ăn ít nhất 8 giờ; >=126 mg/dL (7.0 mmol/L) là tiêu chuẩn chẩn đoán.'});
CREATE (:Biomarker {id: 'OGTT', name: 'Nghiệm pháp Dung nạp Glucose', en: 'Oral Glucose Tolerance Test 2h', source: 'ADA 2024 / BYT QĐ 5481', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Đo đường huyết 2 giờ sau uống 75g glucose; >=200 mg/dL là tiêu chuẩn ĐTĐ.'});
CREATE (:Biomarker {id: 'RPG', name: 'Đường huyết ngẫu nhiên', en: 'Random Plasma Glucose', source: 'ADA 2024 / BYT QĐ 5481', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: '>=200 mg/dL kèm triệu chứng kinh điển 4P xác lập chẩn đoán ngay lập tức.'});
CREATE (:Biomarker {id: 'eGFR', name: 'Độ lọc cầu thận ước tính', en: 'Estimated GFR', source: 'KDIGO 2023', url: 'https://kdigo.org/guidelines/diabetes-ckd/', desc: 'Chỉ số đánh giá chức năng thận; <30 mL/phút chống chỉ định Metformin.'});
CREATE (:Biomarker {id: 'UACR', name: 'Tỷ lệ Albumin/Creatinine niệu', en: 'Urine Albumin-to-Creatinine Ratio', source: 'KDIGO 2023 / BYT QĐ 5481', url: 'https://kdigo.org/guidelines/diabetes-ckd/', desc: 'Dấu ấn sớm tổn thương màng lọc cầu thận; >=30 mg/g biểu hiện tiểu đạm vi thể.'});
CREATE (:Biomarker {id: 'BMI', name: 'Chỉ số khối cơ thể', en: 'Body Mass Index', source: 'ADA 2024 / BYT QĐ 5481', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: '>=23 kg/m2 (châu Á) hoặc >=25 là yếu tố nguy cơ đề kháng insulin hàng đầu.'});
CREATE (:Biomarker {id: 'Vinmec_ABI_Test', name: 'Chỉ số ABI Mạch máu (Vinmec)', en: 'Ankle-Brachial Index Test', source: 'Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT)', url: 'https://kcb.vn/van-ban/quyet-dinh-so-5481-qd-byt-ve-viec-ban-hanh-tai-lieu-chuyen-mon-huong-dan-chan-doan-va-dieu-tri-dai-thao-duong-tip-2.html', desc: 'Đo huyết áp cổ chân trên cánh tay theo quy trình BYT; ABI < 0.9 chẩn đoán bệnh động mạch ngoại biên (PAD), dự phòng nguy cơ hoại tử chi dưới.'});
CREATE (:Biomarker {id: 'Vinmec_Eye_Screening', name: 'Sàng lọc Đáy mắt (Vinmec)', en: 'Annual Funduscopy Eye Screening', source: 'Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT)', url: 'https://kcb.vn/van-ban/quyet-dinh-so-5481-qd-byt-ve-viec-ban-hanh-tai-lieu-chuyen-mon-huong-dan-chan-doan-va-dieu-tri-dai-thao-duong-tip-2.html', desc: 'Chụp màu đáy mắt độ phân giải cao định kỳ 12 tháng/lần theo hướng dẫn BYT tầm soát sớm tổn thương võng mạc và hoàng điểm.'});
CREATE (:Biomarker {id: 'MOH_Individualized_Target', name: 'Mục tiêu HbA1c Cá thể hóa (BYT)', en: 'MOH Individualized Target', source: 'Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT)', url: 'https://kcb.vn/van-ban/quyet-dinh-so-5481-qd-byt-ve-viec-ban-hanh-tai-lieu-chuyen-mon-huong-dan-chan-doan-va-dieu-tri-dai-thao-duong-tip-2.html', desc: 'Quy định Bộ Y tế: Mục tiêu chung HbA1c < 7.0%; người trẻ mới mắc < 6.5%; người cao tuổi/bệnh nền nới lỏng < 7.5 - 8.0%.'});
CREATE (:Symptom {id: 'Polydipsia', name: 'Khát nước nhiều', en: 'Polydipsia', source: 'ADA 2024 / BYT QĐ 5481', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Cơ thể mất nước qua nước tiểu do áp lực thẩm thấu đường niệu cao kích thích trung tâm khát.'});
CREATE (:Symptom {id: 'Polyuria', name: 'Đi tiểu nhiều', en: 'Polyuria', source: 'ADA 2024 / BYT QĐ 5481', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Lợi niệu thẩm thấu do glucose vượt ngưỡng tái hấp thu của ống thận (180 mg/dL).'});
CREATE (:Symptom {id: 'Polyphagia', name: 'Ăn nhiều nhưng sụt cân', en: 'Polyphagia and Weight Loss', source: 'ADA 2024 / BYT QĐ 5481', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Tế bào thiếu năng lượng do không đưa được glucose vào tế bào, cơ thể tự tiêu hủy mỡ và cơ.'});
CREATE (:Symptom {id: 'BlurredVision', name: 'Nhìn mờ', en: 'Blurred Vision', source: 'ADA 2024 / BYT QĐ 5481', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Thay đổi áp lực thẩm thấu làm thay đổi thể tích và độ cong của thể thủy tinh thể.'});
CREATE (:Symptom {id: 'SlowHealing', name: 'Vết thương lâu lành', en: 'Slow Healing Wounds', source: 'ADA 2024 / BYT QĐ 5481', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Tổn thương vi mạch và suy giảm miễn dịch tại chỗ cản trở quá trình liền da.'});
CREATE (:Medication {id: 'Metformin', name: 'Metformin (Biguanide)', en: 'Metformin', source: 'ADA 2024 / BYT QĐ 5481', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Thuốc đầu tay giảm sản xuất glucose ở gan và tăng nhạy cảm insulin ngoại biên.'});
CREATE (:Medication {id: 'Empagliflozin', name: 'Empagliflozin (Jardiance - SGLT2i)', en: 'Empagliflozin', source: 'ADA 2024 / BYT QĐ 5481', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Ức chế tái hấp thu glucose ở ống lượn gần, đào thải đường qua nước tiểu, bảo vệ tim mạch và thận.'});
CREATE (:Medication {id: 'Dapagliflozin', name: 'Dapagliflozin (Forxiga - SGLT2i)', en: 'Dapagliflozin', source: 'ADA 2024 / BYT QĐ 5481', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Thuốc nhóm SGLT2i giảm biến cố nhập viện vì suy tim và làm chậm suy giảm eGFR.'});
CREATE (:Medication {id: 'Semaglutide', name: 'Semaglutide (Ozempic - GLP-1 RA)', en: 'Semaglutide', source: 'ADA 2024', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Đồng vận GLP-1 kích thích tiết insulin phụ thuộc glucose, giảm cân mạnh, bảo vệ đột quỵ tim mạch.'});
CREATE (:Medication {id: 'Tirzepatide', name: 'Tirzepatide (Mounjaro - GIP/GLP-1)', en: 'Tirzepatide', source: 'ADA 2024', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Đồng vận kép GIP và GLP-1 thế hệ mới nhất, hạ HbA1c vượt trội và giảm cân đỉnh cao.'});
CREATE (:Medication {id: 'Sitagliptin', name: 'Sitagliptin (Januvia - DPP-4i)', en: 'Sitagliptin', source: 'ADA 2024 / BYT QĐ 5481', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Ức chế enzyme DPP-4 kéo dài thời gian bán hủy của incretin nội sinh, không gây hạ đường huyết.'});
CREATE (:Medication {id: 'Trajenta_Linagliptin', name: 'Linagliptin (Trajenta 5mg - DPP-4i)', en: 'Linagliptin (Trajenta)', source: 'KDIGO 2023 / BYT QĐ 5481', url: 'https://kdigo.org/guidelines/diabetes-ckd/', desc: 'Thuốc nhóm DPP-4i: 95% đào thải qua đường mật/phân, dùng an toàn tuyệt đối cho người suy thận mọi giai đoạn không cần chỉnh liều theo KDIGO.'});
CREATE (:Medication {id: 'InsulinGlargine', name: 'Insulin Glargine (Lantus)', en: 'Insulin Glargine U100', source: 'ADA 2024 / BYT QĐ 5481', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Insulin nền tác dụng kéo dài 24 giờ không có đỉnh nhọn, kiểm soát đường huyết đói ổn định.'});
CREATE (:Medication {id: 'Gliclazide', name: 'Gliclazide MR (Sulfonylurea)', en: 'Gliclazide Modified Release', source: 'Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT)', url: 'https://kcb.vn/van-ban/quyet-dinh-so-5481-qd-byt-ve-viec-ban-hanh-tai-lieu-chuyen-mon-huong-dan-chan-doan-va-dieu-tri-dai-thao-duong-tip-2.html', desc: 'Kích thích tế bào beta tụy tiết insulin, nguy cơ gây hạ đường huyết nếu dùng ở người cao tuổi.'});
CREATE (:Medication {id: 'Metformin_Counselling_LongChau', name: 'Tư vấn uống Metformin (BYT/Long Châu)', en: 'Metformin GI Tolerability Counseling', source: 'Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT)', url: 'https://kcb.vn/van-ban/quyet-dinh-so-5481-qd-byt-ve-viec-ban-hanh-tai-lieu-chuyen-mon-huong-dan-chan-doan-va-dieu-tri-dai-thao-duong-tip-2.html', desc: 'Hướng dẫn điều trị BYT: Uống Metformin trong hoặc ngay sau bữa ăn chính để tránh buồn nôn, tiêu chảy; tăng liều dần dần sau mỗi 1-2 tuần.'});
CREATE (:Lifestyle {id: 'LowGI_Diet', name: 'Chế độ Dinh dưỡng Low-GI', en: 'Low-Glycemic Diet (MNT)', source: 'ADA 2024 / BYT QĐ 5481', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Hạn chế carbohydrate tinh chế, ưu tiên ngũ cốc nguyên cám, làm phẳng đỉnh đường huyết sau ăn.'});
CREATE (:Lifestyle {id: 'Vinmec_Plate_Method', name: 'Đĩa thức ăn người Việt (BYT)', en: 'Vietnamese Plate Nutrition', source: 'Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT)', url: 'https://kcb.vn/van-ban/quyet-dinh-so-5481-qd-byt-ve-viec-ban-hanh-tai-lieu-chuyen-mon-huong-dan-chan-doan-va-dieu-tri-dai-thao-duong-tip-2.html', desc: 'Mô hình đĩa ăn theo hướng dẫn BYT cho người Việt: 1/2 rau củ không tinh bột (rau muống, cải, bầu bí); 1/4 protein nạc (ức gà, cá, đậu hũ); 1/4 tinh bột chậm (gạo lứt, khoai lang).'});
CREATE (:Lifestyle {id: 'Vinmec_Foot_Care', name: 'Chăm sóc Bàn chân ĐTĐ (BYT)', en: 'Diabetic Foot Care', source: 'Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT)', url: 'https://kcb.vn/van-ban/quyet-dinh-so-5481-qd-byt-ve-viec-ban-hanh-tai-lieu-chuyen-mon-huong-dan-chan-doan-va-dieu-tri-dai-thao-duong-tip-2.html', desc: 'Quy trình BYT: Rửa nước ấm dưới 37°C, lau khô kỹ các kẽ ngón, thoa kem dưỡng ẩm tránh nứt nẻ, mang giày vừa vặn, kiểm tra đáy chân mỗi ngày phát hiện sớm vết chai loét.'});
CREATE (:Lifestyle {id: 'Rule_15_15_LongChau', name: 'Quy tắc 15-15 Hạ đường huyết (BYT)', en: 'Rule of 15-15 Hypoglycemia Rescue', source: 'Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT)', url: 'https://kcb.vn/van-ban/quyet-dinh-so-5481-qd-byt-ve-viec-ban-hanh-tai-lieu-chuyen-mon-huong-dan-chan-doan-va-dieu-tri-dai-thao-duong-tip-2.html', desc: 'Quy chuẩn cấp cứu BYT: Khi đường huyết < 70 mg/dL, uống ngay 15g đường tác dụng nhanh (3 viên đường / 150ml nước cam ép / 1/2 lon nước ngọt); nghỉ 15 phút đo lại.'});
CREATE (:Lifestyle {id: 'Insulin_Storage_LongChau', name: 'Bảo quản & Tiêm Insulin (BYT)', en: 'Insulin Pen Storage & Rotation', source: 'Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT)', url: 'https://kcb.vn/van-ban/quyet-dinh-so-5481-qd-byt-ve-viec-ban-hanh-tai-lieu-chuyen-mon-huong-dan-chan-doan-va-dieu-tri-dai-thao-duong-tip-2.html', desc: 'Hướng dẫn BYT: Bút tiêm chưa mở bảo quản 2-8°C; bút đang dùng để < 30°C trong tối đa 28 ngày; luân chuyển vị trí tiêm (bụng, đùi, tay) cách nhau 2cm tránh loạn dưỡng mỡ.'});
CREATE (:Lifestyle {id: 'FiberIntake', name: 'Bổ sung Chất xơ 35g/ngày', en: 'High Dietary Fiber', source: 'ADA 2024', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Chất xơ hòa tan tạo gel trong ruột làm chậm phân giải polysaccharide thành glucose đơn.'});
CREATE (:Lifestyle {id: 'AerobicExercise', name: 'Tập thể dục Aerobic 150 phút/tuần', en: 'Moderate Aerobic Exercise', source: 'ADA 2024 / BYT QĐ 5481', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Kích hoạt chuyển vị kênh GLUT4 lên màng tế bào cơ mà không phụ thuộc insulin.'});
CREATE (:Lifestyle {id: 'ResistanceTraining', name: 'Luyện tập Kháng lực', en: 'Resistance Training', source: 'ADA 2024', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Gia tăng khối cơ vân nạc giúp mở rộng kho dự trữ glycogen và tăng chuyển hóa cơ bản.'});
CREATE (:Lifestyle {id: 'WeightLoss', name: 'Mục tiêu Giảm 7% Cân nặng', en: 'Target Weight Loss (5-7%)', source: 'ADA 2024 / BYT QĐ 5481', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Làm sạch mỡ lạc chỗ trong tế bào gan và tụy, có khả năng đưa bệnh vào giai đoạn thuyên giảm (Remission).'});
CREATE (:Lifestyle {id: 'SmokingCessation', name: 'Cai thuốc lá Tuyệt đối', en: 'Smoking Cessation', source: 'ADA 2024 / BYT QĐ 5481', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Ngăn ngừa tổn thương nội mạc mạch máu và giảm 50% nguy cơ biến cố tim mạch xơ vữa.'});
CREATE (:Guideline {id: 'ADA2024', name: 'Chuẩn ADA 2024 (Hoa Kỳ)', en: 'ADA Standards of Care 2024', source: 'Hiệp hội Đái tháo đường Hoa Kỳ (ADA)', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Hướng dẫn thực hành lâm sàng uy tín nhất toàn cầu về chẩn đoán, điều trị cá thể hóa và bảo vệ cơ quan đích.'});
CREATE (:Guideline {id: 'KDIGO2023', name: 'Chuẩn KDIGO 2023 Thận học', en: 'KDIGO Diabetes in CKD 2023', source: 'Hiệp hội Thận học Quốc tế KDIGO', url: 'https://kdigo.org/guidelines/diabetes-ckd/', desc: 'Đồng thuận quốc tế về phân tầng suy thận, chỉnh liều thuốc hạ đường huyết và sàng lọc UACR.'});
CREATE (:Guideline {id: 'WHO_Guideline', name: 'Khuyến nghị WHO Toàn cầu', en: 'WHO Diabetes Guidelines', source: 'American Diabetes Association / WHO', url: 'https://diabetesjournals.org/care/issue/47/Supplement_1', desc: 'Định hướng sức khỏe cộng đồng về phòng ngừa đái tháo đường và tầm soát các yếu tố nguy cơ dân số.'});
CREATE (:Guideline {id: 'Vinmec_Guideline', name: 'Phác đồ Lâm sàng BYT / Vinmec', en: 'Vinmec Clinical Diabetes Pathway', source: 'Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT)', url: 'https://kcb.vn/van-ban/quyet-dinh-so-5481-qd-byt-ve-viec-ban-hanh-tai-lieu-chuyen-mon-huong-dan-chan-doan-va-dieu-tri-dai-thao-duong-tip-2.html', desc: 'Quy trình điều trị ngoại trú và phòng ngừa biến chứng vi mạch, bàn chân đái tháo đường chuẩn Bộ Y tế Việt Nam.'});
CREATE (:Guideline {id: 'LongChau_Guideline', name: 'Cẩm nang Dược học BYT / Long Châu', en: 'FPT Long Chau Pharmacy Practice', source: 'Bộ Y tế Việt Nam (QĐ 5481/QĐ-BYT)', url: 'https://kcb.vn/van-ban/quyet-dinh-so-5481-qd-byt-ve-viec-ban-hanh-tai-lieu-chuyen-mon-huong-dan-chan-doan-va-dieu-tri-dai-thao-duong-tip-2.html', desc: 'Sổ tay tư vấn sử dụng thuốc an toàn, xử trí cấp cứu hạ đường huyết theo hướng dẫn chuyên môn của Bộ Y tế Việt Nam.'});
CREATE (:Guideline {id: 'BYT_QD5481', name: 'QĐ 5481/QĐ-BYT Bộ Y Tế', en: 'Vietnam MOH Decision 5481/QD-BYT', source: 'Bộ Y tế Việt Nam', url: 'https://kcb.vn/van-ban/quyet-dinh-so-5481-qd-byt-ve-viec-ban-hanh-tai-lieu-chuyen-mon-huong-dan-chan-doan-va-dieu-tri-dai-thao-duong-tip-2.html', desc: 'Tài liệu chuyên môn chính thức Hướng dẫn chẩn đoán và điều trị đái tháo đường típ 2 của Bộ Y tế Việt Nam.'});

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
