#!/usr/bin/env python3
"""
Part 04: Chapter 4 - Multi-Source Data Engineering, Dual Cohort Strategy, Data Dictionary, and In-Depth EDA.
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from helpers import add_custom_heading, add_body_p, add_callout, add_figure, populate_table

def build_chapter4(doc):
    print("  [+] Building Chapter 4: Data Engineering, Dual Cohorts & EDA...")
    
    add_custom_heading(doc, "4. KỸ THUẬT DỮ LIỆU ĐA NGUỒN & PHÂN TÍCH KHÁM PHÁ (DATA ENGINEERING & EDA)", level=1)
    
    add_custom_heading(doc, "4.1. Chiến Lược Đa Cohort Kép (Dual Cohort Strategy) & Nguồn Dữ Liệu Minh Bạch", level=2)
    add_body_p(
        doc,
        "Một trong những nguyên nhân hàng đầu khiến các mô hình học máy chẩn đoán y tế thất bại khi đưa vào ứng dụng thực tiễn là sự sai lệch phân phối "
        "dữ liệu (Distribution Shift) và sự thiếu hụt các dấu ấn sinh học đo trực tiếp. Các nghiên cứu trước đây (điển hình như bài báo cơ sở dựa trên "
        "khảo sát BRFSS 2015 của CDC với 253.680 hồ sơ) hoàn toàn dựa trên bảng hỏi tự khai của người dân qua điện thoại. Người được phỏng vấn tự ước lượng "
        "tình trạng sức khỏe mà không có bất kỳ xét nghiệm máu khách quan nào. Điều này tạo ra một lỗ hổng lâm sàng chết người: giai đoạn tiền đái tháo đường "
        "(Prediabetes) hoàn toàn không có triệu chứng rõ rệt, do đó người bệnh không thể tự biết để khai báo, dẫn đến việc mô hình bỏ sót hơn 80% ca bệnh."
    )
    add_body_p(
        doc,
        "Để giải quyết triệt để rào cản này, công trình này kiến tạo Chiến Lược Đa Cohort Kép (Dual Cohort Strategy) kết hợp ba nguồn dữ liệu bổ trợ lẫn nhau:\n"
        "• Cohort 1 (Quần thể Lâm sàng Lớn - Kaggle Healthcare EHR 100.000 ca): Dữ liệu bệnh án điện tử thực tế gồm 100.000 bệnh nhân có đầy đủ hai xét nghiệm "
        "sinh hóa tiêu chuẩn vàng là chỉ số HbA1c (Glycated Hemoglobin) và Glucose huyết tương lúc đói (FPG), kết hợp với chỉ số khối cơ thể BMI, tiền sử tăng huyết áp, "
        "bệnh tim mạch và thói quen hút thuốc.\n"
        "• Cohort 2A (Quần thể Khảo sát Dân số CDC BRFSS 2015 - 253.680 ca): Bộ dữ liệu dịch tễ học quy mô lớn nhất Hoa Kỳ về lối sống, tần suất vận động thể lực, "
        "chế độ ăn rau củ và tự đánh giá sức khỏe, dùng để huấn luyện tác tử phân tích hành vi và lối sống.\n"
        "• Cohort 2B (Quần thể Đối chuẩn Sinh học Chuẩn UCI Pima Indians Diabetes - 768 ca): Bộ dữ liệu lâm sàng kinh điển của Viện Quốc gia về Bệnh Đái tháo đường, "
        "Tiêu hóa và Bệnh thận Hoa Kỳ (NIDDK), gồm 768 phụ nữ người da đỏ Pima với các xét nghiệm nồng độ Insulin huyết thanh 2 giờ và nghiệm pháp dung nạp glucose OGTT."
    )

    add_custom_heading(doc, "4.2. Từ Điển Dữ Liệu Lâm Sàng Toàn Diện (Comprehensive Clinical Data Dictionary)", level=2)
    add_body_p(
        doc,
        "Bảng từ điển dữ liệu chuẩn hóa toàn bộ các biến số đầu vào của hệ thống, chỉ rõ kiểu dữ liệu, khoảng giá trị sinh lý bình thường và ý nghĩa bệnh lý học:"
    )

    dict_headers = ["Tên Biến (Feature)", "Kiểu Dữ Liệu", "Khoảng Sinh Lý Bình Thường", "Ngưỡng Cảnh Báo Lâm Sàng (ADA 2024)", "Ý Nghĩa Bệnh Học Sinh Lý"]
    dict_data = [
        ["HbA1c_level", "Float (Liên tục)", "4.0% - 5.6%", ">= 5.7% (Tiền ĐTĐ)\n>= 6.5% (ĐTĐ xác định)", "Tỷ lệ hemoglobin gắn glucose trong hồng cầu; phản ánh mức đường huyết trung bình trong 120 ngày qua. Tiêu chuẩn vàng chẩn đoán."],
        ["blood_glucose_level", "Float (Liên tục)", "70 - 99 mg/dL", "100 - 125 mg/dL (Rối loạn FPG)\n>= 126 mg/dL (Đái tháo đường)", "Nồng độ glucose tự do trong huyết tương sau nhịn ăn 8h. Đo lường trực tiếp tình trạng đề kháng insulin cấp tính."],
        ["bmi (Body Mass Index)", "Float (Liên tục)", "18.5 - 22.9 kg/m² (Châu Á)\n18.5 - 24.9 kg/m² (WHO)", ">= 23.0 (Thừa cân Châu Á)\n>= 25.0 (Béo phì)", "Chỉ số khối cơ thể. Mô mỡ nội tạng giải phóng các cytokine gây viêm (TNF-alpha, IL-6) làm suy giảm nhạy cảm thụ thể insulin."],
        ["age (Tuổi)", "Integer (Rời rạc)", "18 - 64 tuổi", ">= 45 tuổi (Sàng lọc định kỳ)\n>= 65 tuổi (Nguy cơ cao)", "Lão hóa làm suy giảm khối lượng tế bào beta tụy và tăng hiện tượng xơ hóa cơ quan chuyển hóa."],
        ["gender (Giới tính)", "Categorical (2 mức)", "Male / Female", "Nam giới có nguy cơ kháng insulin sớm hơn", "Khác biệt về phân bố mô mỡ (mỡ nội tạng ở nam so với mỡ dưới da ở nữ) và tác động của hormone estrogen."],
        ["hypertension", "Binary (0 hoặc 1)", "0 (Huyết áp < 120/80 mmHg)", "1 (HA >= 130/80 mmHg)", "Tăng huyết áp gây xơ cứng vi mạch cầu thận và mạch vành, gia tăng gấp đôi nguy cơ biến cố tim mạch ở người ĐTĐ."],
        ["heart_disease", "Binary (0 hoặc 1)", "0 (Không tiền sử tim mạch)", "1 (Tiền sử nhồi máu cơ tim, suy tim)", "Biến chứng tim mạch xơ vữa (ASCVD) là nguyên nhân gây tử vong hàng đầu (>60%) ở bệnh nhân đái tháo đường tuýp 2."],
        ["smoking_history", "Categorical (5 mức)", "never (Chưa từng hút)", "current (Đang hút)\nformer (Đã cai)", "Nicotine và các gốc tự do làm tổn thương lớp nội mạc mạch máu, gia tăng kháng insulin và thúc đẩy biến chứng bàn chân."],
        ["eGFR (Độ lọc cầu thận)", "Float (Ước tính)", ">= 90 mL/phút/1.73m²", "< 60 (Suy thận mạn CKD)\n< 30 (Chống chỉ định Metformin)", "Đo lường chức năng lọc của cầu thận. Chỉ số sống còn quyết định liều lượng và chống chỉ định các thuốc hạ đường huyết."],
        ["insulin (Pima cohort)", "Float (Liên tục)", "16 - 166 mcU/mL", ">= 200 mcU/mL (Cường insulin)\n< 15 (Suy kiệt tế bào beta)", "Nồng độ insulin huyết thanh sau ăn. Phản ánh giai đoạn bù trừ (cường insulin) hay giai đoạn suy kiệt tế bào beta tụy."]
    ]
    populate_table(doc, dict_headers, dict_data, col_widths=[1.5, 1.2, 1.3, 1.5, 2.0], header_bg="1E3A8A")

    add_custom_heading(doc, "4.3. Quy Trình Tiền Xử Lý Dữ Liệu Lâm Sàng Chuẩn Mực", level=2)
    add_body_p(
        doc,
        "Dữ liệu y tế luôn chứa các giá trị khuyết thiếu (Missing values) mang tính chất bệnh lý và các giá trị ngoại lai (Outliers). "
        "Hệ thống thiết lập một đường ống tiền xử lý nghiêm ngặt bảo đảm không rò rỉ thông tin (Data Leakage Protection):\n"
        "1. Làm sạch giá trị ngoại lai sinh học: Trong tập dữ liệu Pima Indians, nhiều thuộc tính sinh học (như Glucose = 0, Huyết áp = 0, Độ dày nếp gấp da = 0, "
        "Insulin = 0) về mặt y học là không thể xảy ra đối với bệnh nhân còn sống. Chúng được nhận diện là mã quy ước cho dữ liệu bị thiếu và được điền "
        "khuyết bằng thuật toán K-Nearest Neighbors Imputer (KNNImputer với k = 5 dựa trên ma trận khoảng cách Gower).\n"
        "2. Chuẩn hóa thang đo thích nghi: Áp dụng RobustScaler (chuẩn hóa theo trung vị và khoảng tứ phân vị IQR) cho các biến có phân phối lệch đuôi dài "
        "(như Glucose, Insulin) để giảm thiểu ảnh hưởng của các ca bệnh cực đoan, và áp dụng StandardScaler cho các biến xấp xỉ phân phối chuẩn (Age, BMI).\n"
        "3. Xử lý mất cân bằng dữ liệu (Imbalanced Class Handling): Nhóm bệnh nhân đái tháo đường chiếm tỷ lệ thiểu số (khoảng 8.5% trong tập 100k EHR). "
        "Hệ thống áp dụng kết hợp kỹ thuật tái lấy mẫu tổng hợp SMOTE (Synthetic Minority Over-sampling Technique) trên tập huấn luyện kết hợp kỹ thuật "
        "đánh trọng số lớp mất mát (Class-Weighted Binary Cross-Entropy Loss) trong quá trình tối ưu hóa mạng nơ-ron."
    )

    add_custom_heading(doc, "4.4. Phân Tích Thăm Dò Dữ Liệu Chuyên Sâu (In-Depth Exploratory Data Analysis - EDA)", level=2)
    add_body_p(
        doc,
        "Dưới đây là chuỗi 6 biểu đồ phân tích thăm dò dữ liệu chuyên sâu thực hiện trên quần thể nghiên cứu:"
    )

    # Fig 1 & Fig 2
    add_figure(
        doc,
        "fig1_target_distribution.png",
        "Hình 4.1. Phân phối biến mục tiêu Đái tháo đường trên Quần thể Lâm sàng 100.000 ca bệnh (8.5% Dương tính, 91.5% Âm tính).",
        width_inches=5.8
    )
    add_figure(
        doc,
        "fig2_numerical_distributions.png",
        "Hình 4.2. Phân phối xác suất của 4 biến số sinh hóa liên tục: Tuổi, BMI, Nồng độ Glucose huyết tương và Chỉ số HbA1c.",
        width_inches=6.0
    )

    add_body_p(
        doc,
        "Quan sát Hình 4.1 và 4.2 cho thấy phân phối của Glucose và HbA1c biểu hiện rõ hai đỉnh (Bimodal Distribution): đỉnh chính đại diện cho quần thể "
        "người khỏe mạnh với Glucose dao động quanh 85–100 mg/dL và HbA1c quanh 5.0–5.5%; đỉnh thứ hai kéo dài về phía bên phải với các giá trị Glucose > 160 mg/dL "
        "và HbA1c > 7.5%, đại diện cho nhóm bệnh nhân đái tháo đường chưa được kiểm soát tốt."
    )

    # Fig 3 & Fig 4
    add_figure(
        doc,
        "fig3_boxplots_by_diabetes.png",
        "Hình 4.3. Biểu đồ hộp (Boxplots) so sánh phân phối các biến liên tục giữa nhóm Không mắc bệnh (0) và Mắc bệnh đái tháo đường (1).",
        width_inches=6.0
    )
    add_figure(
        doc,
        "fig4_categorical_risk_factors.png",
        "Hình 4.4. Tỷ lệ mắc đái tháo đường phân tầng theo các yếu tố nguy cơ phân loại: Tăng huyết áp, Tiền sử tim mạch và Thói quen hút thuốc.",
        width_inches=6.0
    )

    add_body_p(
        doc,
        "Biểu đồ hộp Hình 4.3 chứng minh rõ rệt: ở nhóm bệnh nhân đái tháo đường (màu cam), trung vị của Glucose (160 mg/dL) và HbA1c (7.8%) "
        "nằm hoàn toàn tách biệt phía trên đường phân vị thứ 75 của nhóm bình thường. Hình 4.4 khẳng định người có tiền sử bệnh tim mạch hoặc tăng huyết áp "
        "có tỷ lệ mắc đái tháo đường cao gấp gần 4 lần so với nhóm không có bệnh nền tim mạch."
    )

    # Fig 5 & Fig 6
    add_figure(
        doc,
        "fig5_correlation_heatmap.png",
        "Hình 4.5. Ma trận tương quan nhiệt Pearson giữa các thuộc tính lâm sàng và biến mục tiêu Đái tháo đường.",
        width_inches=5.8
    )
    add_figure(
        doc,
        "fig6_glucose_vs_hba1c_ada_cutoffs.png",
        "Hình 4.6. Biểu đồ phân tán hai chiều giữa Nồng độ Glucose đói và HbA1c kèm các đường phân ranh giới chuẩn chẩn đoán ADA 2024.",
        width_inches=6.0
    )

    add_body_p(
        doc,
        "Hình 4.5 xác lập hệ số tương quan tuyến tính Pearson cực mạnh giữa HbA1c với chẩn đoán đái tháo đường (r = 0.46, p < 0.001) và giữa Glucose với bệnh (r = 0.44). "
        "Đặc biệt, Hình 4.6 trực quan hóa không gian phân chia hai chiều theo đúng tiêu chuẩn vàng ADA 2024: ranh giới HbA1c = 6.5% và Glucose = 126 mg/dL phân tách "
        "hoàn hảo góc phần tư trên bên phải chứa đại đa số các ca bệnh dương tính thực sự."
    )
