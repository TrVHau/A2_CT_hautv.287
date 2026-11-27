import json
import os

CYPHER_HEADER = """// ==============================================================================================
// Neo4j Cypher Knowledge Graph for Diabetes Mellitus (Đồ Thị Tri Thức Y Khoa Đái Tháo Đường)
// PROJECT : Hệ Thống Đa Tác Tử Lâm Sàng Hỗ Trợ Ra Quyết Định Đái Tháo Đường (Enterprise Hybrid MAS)
// ĐƠN VỊ  : Học viện Công nghệ Bưu chính Viễn thông (PTIT) - Bộ môn Trí tuệ Nhân tạo
// TÁC GIẢ : Trần Văn Hậu (Mã sinh viên: B23DCCN287) - Lớp D23CQCN01-B (Nhóm CT_09)
// GVHD    : PGS. TS. Trần Đình Quế
// THỜI GIAN: Tháng 11/2026
//
// ==============================================================================================
// DANH MỤC ĐẦY ĐỦ CÁC ĐƯỜNG DẪN / LIÊN KẾT NGUỒN DỮ LIỆU ĐÃ TRÍCH XUẤT (OFFICIAL SOURCE LINKS):
// ==============================================================================================
//
// 1. HIỆP HỘI ĐÁI THÁO ĐƯỜNG HOA KỲ (AMERICAN DIABETES ASSOCIATION - ADA 2024 STANDARDS OF CARE):
//    - Cổng toàn văn ADA Standards of Care in Diabetes 2024 (Supplement 1):
//      https://diabetesjournals.org/care/issue/47/Supplement_1
//    - Chương 2: Phân loại & Tiêu chuẩn chẩn đoán ĐTĐ (Classification and Diagnosis of Diabetes):
//      https://doi.org/10.2337/dc24-S002
//    - Chương 3: Dự phòng và trì hoãn ĐTĐ tuýp 2 (Prevention or Delay of Type 2 Diabetes):
//      https://doi.org/10.2337/dc24-S003
//    - Chương 5: Hành vi lối sống & Dinh dưỡng tiết chế y khoa MNT (Facilitating Positive Health Behaviors):
//      https://doi.org/10.2337/dc24-S005
//    - Chương 8: Béo phì & Quản lý cân nặng trong ĐTĐ (Obesity and Weight Management):
//      https://doi.org/10.2337/dc24-S008
//    - Chương 9: Tiếp cận Dược lý & Hạ đường huyết (Pharmacologic Approaches to Glycemic Treatment):
//      https://doi.org/10.2337/dc24-S009
//    - Chương 10: Bệnh tim mạch & Quản lý nguy cơ ASCVD, Suy tim (Cardiovascular Disease and Risk Management):
//      https://doi.org/10.2337/dc24-S010
//    - Chương 11: Bệnh thận mạn tính ĐTĐ (Chronic Kidney Disease and Risk Management):
//      https://doi.org/10.2337/dc24-S011
//    - Chương 12: Bệnh lý võng mạc, thần kinh & chăm sóc bàn chân (Retinopathy, Neuropathy, and Foot Care):
//      https://doi.org/10.2337/dc24-S012
//    - Chương 15: Quản lý đái tháo đường thai kỳ (Management of Diabetes in Pregnancy):
//      https://doi.org/10.2337/dc24-S015
//    - Chương 16: Chăm sóc ĐTĐ tại bệnh viện & cấp cứu DKA/HHS (Diabetes Care in the Hospital):
//      https://doi.org/10.2337/dc24-S016
//
// 2. BỘ Y TẾ VIỆT NAM (VIETNAMESE MINISTRY OF HEALTH - QUYẾT ĐỊNH 5481/QĐ-BYT):
//    - Quyết định số 5481/QĐ-BYT ban hành tài liệu chuyên môn "Hướng dẫn chẩn đoán và điều trị đái tháo đường típ 2":
//      https://kcb.vn/van-ban/quyet-dinh-so-5481-qd-byt-ve-viec-ban-hanh-tai-lieu-chuyen-mon-huong-dan-chan-doan-va-dieu-tri-dai-thao-duong-tip-2.html
//    - Văn bản lưu trữ Thư Viện Pháp Luật (Toàn văn tài liệu hướng dẫn lâm sàng):
//      https://thuvienphapluat.vn/van-ban/The-thao-Y-te/Quyet-dinh-5481-QD-BYT-2020-tai-lieu-chuyen-mon-Huong-dan-chan-doan-dieu-tri-dai-thao-duong-tip-2-461324.aspx
//
// 3. HIỆP HỘI THẬN HỌC QUỐC TẾ (KDIGO 2023 CLINICAL PRACTICE GUIDELINE FOR DIABETES IN CKD):
//    - Hướng dẫn lâm sàng chính thức KDIGO về đái tháo đường trên bệnh thận mạn:
//      https://kdigo.org/guidelines/diabetes-ckd/
//    - Xuất bản trên Tạp chí Thận học Quốc tế Kidney International (DOI):
//      https://doi.org/10.1016/j.kint.2023.08.014
//
// 4. HỆ THỐNG Y TẾ VINMEC (BỆNH VIỆN ĐA KHOA QUỐC TẾ VINMEC - TIÊU CHUẨN JCI):
//    - Chẩn đoán, nguyên nhân, triệu chứng và phác đồ điều trị bệnh tiểu đường:
//      https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/noi-tiet-tieu-hoa-va-gan-mat/benh-tieu-duong-nguyen-nhan-trieu-chung-chan-doan-va-dieu-tri/
//    - Mô hình dinh dưỡng đĩa thức ăn Vinmec cho người Việt (Vinmec Vietnamese Plate Nutrition):
//      https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/dinh-duong/che-do-an-uong-cho-nguoi-tieu-duong-loai-2/
//    - Quy trình khám và chăm sóc bàn chân đái tháo đường tránh hoại tử cắt cụt chi (Vinmec Foot Care):
//      https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/noi-tiet-tieu-hoa-va-gan-mat/huong-dan-cham-soc-ban-chan-cho-nguoi-benh-tieu-duong/
//    - Quy trình tầm soát sớm bệnh võng mạc và chụp màu đáy mắt định kỳ (Vinmec Eye Screening):
//      https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/mat/sang-loc-benh-vong-mac-dai-thao-duong/
//    - Ý nghĩa chỉ số đo huyết áp cổ chân - cánh tay (ABI Test) trong xơ vữa động mạch ngoại biên:
//      https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/tim-mach/y-nghia-cua-chi-so-abi-trong-chan-doan-benh-dong-mach-ngoai-bien/
//    - Biến chứng thần kinh ngoại biên đái tháo đường:
//      https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/noi-tiet-tieu-hoa-va-gan-mat/bien-chung-than-kinh-ngoai-bien-o-benh-nhan-tieu-duong/
//    - Chế độ tập luyện thể dục tối ưu cho người bệnh tiểu đường:
//      https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/song-khoe/bai-tap-the-duc-cho-nguoi-tieu-duong-tot-nhat/
//    - Lý do bắt buộc người bệnh đái tháo đường phải cai thuốc lá tuyệt đối:
//      https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/song-khoe/vi-sao-nguoi-benh-tieu-duong-can-cai-thuoc-la-ngay-lap-tuc/
//
// 5. HỆ THỐNG NHÀ THUỐC FPT LONG CHÂU (CẨM NANG DƯỢC HỌC LÂM SÀNG & TƯ VẤN THỰC ĐỊA):
//    - Hướng dẫn Dược sĩ Long Châu: Quy tắc 15-15 xử trí cấp cứu hạ đường huyết:
//      https://nhathuoclongchau.com.vn/bai-viet/quy-tac-15-15-trong-xu-tri-ha-duong-huyet-o-nguoi-benh-tieu-duong-61389.html
//    - Tư vấn Dược học: Uống thuốc Metformin lúc nào tốt nhất để giảm kích ứng dạ dày:
//      https://nhathuoclongchau.com.vn/bai-viet/uong-metformin-luc-nao-tot-nhat-huong-dan-dung-thuoc-dung-cach-62145.html
//    - Hoạt chất Metformin & các biệt dược điều trị ĐTĐ tuýp 2:
//      https://nhathuoclongchau.com.vn/thanh-phan/metformin
//    - Thuốc Trajenta Linagliptin 5mg (Đào thải qua mật, an toàn tuyệt đối cho người suy thận không cần chỉnh liều):
//      https://nhathuoclongchau.com.vn/thuoc/trajenta-5mg-boehringer-3x10-18454.html
//    - Thuốc Jardiance Empagliflozin 10mg / 25mg (Ức chế SGLT2 bảo vệ tim mạch, suy tim và thận):
//      https://nhathuoclongchau.com.vn/thuoc/jardiance-10mg-boehringer-3x10-18451.html
//    - Thuốc Forxiga Dapagliflozin 10mg (Giảm nhập viện do suy tim và bảo tồn chức năng thận):
//      https://nhathuoclongchau.com.vn/thuoc/forxiga-10mg-astrazeneca-2x14-17799.html
//    - Hướng dẫn bảo quản, thao tác lắp kim và luân chuyển vị trí tiêm bút tiêm Insulin:
//      https://nhathuoclongchau.com.vn/bai-viet/huong-dan-cach-tiem-insulin-bang-but-tiem-dung-chuan-57989.html
//    - Thuốc Lantus SoloStar Insulin Glargine 100 IU/ml (Insulin nền kéo dài 24 giờ):
//      https://nhathuoclongchau.com.vn/thuoc/lantus-solostar-100iu-ml-sanofi-hop-5-but-tiem-2015.html
//    - Thuốc Diamicron MR 30mg / 60mg Gliclazide (Nhóm Sulfonylurea kích thích tiết insulin):
//      https://nhathuoclongchau.com.vn/thuoc/diamicron-mr-30mg-les-laboratoires-servier-industrie-2-vi-x-30-vien-2811.html
//    - Thuốc Januvia Sitagliptin 100mg (Nhóm ức chế enzyme DPP-4):
//      https://nhathuoclongchau.com.vn/thuoc/januvia-100mg-msd-2x14-610.html
//    - Hoạt chất Semaglutide (Đồng vận thụ thể GLP-1 giảm cân và giảm biến cố tim mạch xơ vữa):
//      https://nhathuoclongchau.com.vn/thanh-phan/semaglutide
//
// 6. TỔ CHỨC Y TẾ THẾ GIỚI (WORLD HEALTH ORGANIZATION - WHO):
//    - Báo cáo dữ liệu & Tổng quan bệnh đái tháo đường (WHO Fact Sheet):
//      https://www.who.int/news-room/fact-sheets/detail/diabetes
//    - Định nghĩa và tiêu chuẩn chẩn đoán đái tháo đường & giảm dung nạp glucose (WHO Diagnostic Criteria):
//      https://www.who.int/publications/i/item/9789241516594
//    - Tiêu chuẩn phân loại BMI khu vực Châu Á - Tây Thái Bình Dương (WPRO Obesity Standards):
//      https://www.who.int/westernpacific/health-topics/obesity
// ==============================================================================================
"""

# Dictionary of node URLs
NODE_URLS = {
    'T2D': 'https://diabetesjournals.org/care/issue/47/Supplement_1',
    'T1D': 'https://doi.org/10.2337/dc24-S002',
    'PreDM': 'https://doi.org/10.2337/dc24-S003',
    'GDM': 'https://doi.org/10.2337/dc24-S015',
    'MetSyn': 'https://www.who.int/news-room/fact-sheets/detail/diabetes',
    'DKA': 'https://doi.org/10.2337/dc24-S016',
    'HHS': 'https://doi.org/10.2337/dc24-S016',
    'Hypo': 'https://nhathuoclongchau.com.vn/bai-viet/quy-tac-15-15-trong-xu-tri-ha-duong-huyet-o-nguoi-benh-tieu-duong-61389.html',
    'DKD': 'https://kdigo.org/guidelines/diabetes-ckd/',
    'Retinopathy': 'https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/mat/sang-loc-benh-vong-mac-dai-thao-duong/',
    'Neuropathy': 'https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/noi-tiet-tieu-hoa-va-gan-mat/bien-chung-than-kinh-ngoai-bien-o-benh-nhan-tieu-duong/',
    'CAD': 'https://doi.org/10.2337/dc24-S010',
    'Stroke': 'https://doi.org/10.2337/dc24-S010',
    'PAD': 'https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/tim-mach/y-nghia-cua-chi-so-abi-trong-chan-doan-benh-dong-mach-ngoai-bien/',
    'HF': 'https://doi.org/10.2337/dc24-S010',
    'HbA1c': 'https://doi.org/10.2337/dc24-S002',
    'FPG': 'https://doi.org/10.2337/dc24-S002',
    'OGTT': 'https://www.who.int/publications/i/item/9789241516594',
    'RPG': 'https://doi.org/10.2337/dc24-S002',
    'eGFR': 'https://kdigo.org/guidelines/diabetes-ckd/',
    'UACR': 'https://kdigo.org/guidelines/diabetes-ckd/',
    'BMI': 'https://www.who.int/westernpacific/health-topics/obesity',
    'Vinmec_ABI_Test': 'https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/tim-mach/y-nghia-cua-chi-so-abi-trong-chan-doan-benh-dong-mach-ngoai-bien/',
    'Vinmec_Eye_Screening': 'https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/mat/sang-loc-benh-vong-mac-dai-thao-duong/',
    'MOH_Individualized_Target': 'https://kcb.vn/van-ban/quyet-dinh-so-5481-qd-byt-ve-viec-ban-hanh-tai-lieu-chuyen-mon-huong-dan-chan-doan-va-dieu-tri-dai-thao-duong-tip-2.html',
    'Polydipsia': 'https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/noi-tiet-tieu-hoa-va-gan-mat/benh-tieu-duong-nguyen-nhan-trieu-chung-chan-doan-va-dieu-tri/',
    'Polyuria': 'https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/noi-tiet-tieu-hoa-va-gan-mat/benh-tieu-duong-nguyen-nhan-trieu-chung-chan-doan-va-dieu-tri/',
    'Polyphagia': 'https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/noi-tiet-tieu-hoa-va-gan-mat/benh-tieu-duong-nguyen-nhan-trieu-chung-chan-doan-va-dieu-tri/',
    'BlurredVision': 'https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/mat/vi-sao-benh-tieu-duong-gay-nhin-mo/',
    'SlowHealing': 'https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/noi-tiet-tieu-hoa-va-gan-mat/huong-dan-cham-soc-ban-chan-cho-nguoi-benh-tieu-duong/',
    'Metformin': 'https://nhathuoclongchau.com.vn/thanh-phan/metformin',
    'Empagliflozin': 'https://nhathuoclongchau.com.vn/thuoc/jardiance-10mg-boehringer-3x10-18451.html',
    'Dapagliflozin': 'https://nhathuoclongchau.com.vn/thuoc/forxiga-10mg-astrazeneca-2x14-17799.html',
    'Semaglutide': 'https://nhathuoclongchau.com.vn/thanh-phan/semaglutide',
    'Tirzepatide': 'https://doi.org/10.2337/dc24-S009',
    'Sitagliptin': 'https://nhathuoclongchau.com.vn/thuoc/januvia-100mg-msd-2x14-610.html',
    'Trajenta_Linagliptin': 'https://nhathuoclongchau.com.vn/thuoc/trajenta-5mg-boehringer-3x10-18454.html',
    'InsulinGlargine': 'https://nhathuoclongchau.com.vn/thuoc/lantus-solostar-100iu-ml-sanofi-hop-5-but-tiem-2015.html',
    'Gliclazide': 'https://nhathuoclongchau.com.vn/thuoc/diamicron-mr-30mg-les-laboratoires-servier-industrie-2-vi-x-30-vien-2811.html',
    'Metformin_Counselling_LongChau': 'https://nhathuoclongchau.com.vn/bai-viet/uong-metformin-luc-nao-tot-nhat-huong-dan-dung-thuoc-dung-cach-62145.html',
    'LowGI_Diet': 'https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/dinh-duong/che-do-an-uong-cho-nguoi-tieu-duong-loai-2/',
    'Vinmec_Plate_Method': 'https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/dinh-duong/che-do-an-uong-cho-nguoi-tieu-duong-loai-2/',
    'Vinmec_Foot_Care': 'https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/noi-tiet-tieu-hoa-va-gan-mat/huong-dan-cham-soc-ban-chan-cho-nguoi-benh-tieu-duong/',
    'Rule_15_15_LongChau': 'https://nhathuoclongchau.com.vn/bai-viet/quy-tac-15-15-trong-xu-tri-ha-duong-huyet-o-nguoi-benh-tieu-duong-61389.html',
    'Insulin_Storage_LongChau': 'https://nhathuoclongchau.com.vn/bai-viet/huong-dan-cach-tiem-insulin-bang-but-tiem-dung-chuan-57989.html',
    'FiberIntake': 'https://doi.org/10.2337/dc24-S005',
    'AerobicExercise': 'https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/song-khoe/bai-tap-the-duc-cho-nguoi-tieu-duong-tot-nhat/',
    'ResistanceTraining': 'https://doi.org/10.2337/dc24-S005',
    'WeightLoss': 'https://doi.org/10.2337/dc24-S008',
    'SmokingCessation': 'https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/song-khoe/vi-sao-nguoi-benh-tieu-duong-can-cai-thuoc-la-ngay-lap-tuc/',
    'ADA2024': 'https://diabetesjournals.org/care/issue/47/Supplement_1',
    'KDIGO2023': 'https://kdigo.org/guidelines/diabetes-ckd/',
    'WHO_Guideline': 'https://www.who.int/news-room/fact-sheets/detail/diabetes',
    'Vinmec_Guideline': 'https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/noi-tiet-tieu-hoa-va-gan-mat/benh-tieu-duong-nguyen-nhan-trieu-chung-chan-doan-va-dieu-tri/',
    'LongChau_Guideline': 'https://nhathuoclongchau.com.vn/bai-viet/quy-tac-15-15-trong-xu-tri-ha-duong-huyet-o-nguoi-benh-tieu-duong-61389.html',
    'BYT_QD5481': 'https://kcb.vn/van-ban/quyet-dinh-so-5481-qd-byt-ve-viec-ban-hanh-tai-lieu-chuyen-mon-huong-dan-chan-doan-va-dieu-tri-dai-thao-duong-tip-2.html'
}

print("Node URLs defined:", len(NODE_URLS))
