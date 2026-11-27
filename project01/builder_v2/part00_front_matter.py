#!/usr/bin/env python3
"""
Part 00: Front Matter, Title Page, Executive Summary, 10 Breakthroughs, Comparative Table, Glossary.
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from helpers import set_cell_background, add_callout, add_custom_heading, add_body_p, populate_table

def build_front_matter(doc):
    print("  [+] Building Front Matter & Executive Summary...")
    for sec in doc.sections:
        sec.top_margin = Inches(0.8)
        sec.bottom_margin = Inches(0.8)
        sec.left_margin = Inches(0.8)
        sec.right_margin = Inches(0.8)

    # -------------------------------------------------------------
    # COVER PAGE
    # -------------------------------------------------------------
    p1 = doc.add_paragraph()
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p1.add_run("HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG\nKHOA CÔNG NGHỆ THÔNG TIN 1 — BỘ MÔN HỆ THỐNG THÔNG MINH\n")
    r1.bold = True
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(13)
    r1.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
    p1.paragraph_format.space_after = Pt(25)

    p_proj = doc.add_paragraph()
    p_proj.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_pr = p_proj.add_run("BÁO CÁO NGHIÊN CỨU & BÀI TẬP LỚN CHUYÊN SÂU (PHIÊN BẢN V2 — TOÀN DIỆN)\nMÔN HỌC: PHÁT TRIỂN CÁC HỆ THỐNG THÔNG MINH\n")
    r_pr.font.name = "Times New Roman"
    r_pr.font.size = Pt(12)
    r_pr.bold = True
    r_pr.font.color.rgb = RGBColor(0x25, 0x63, 0xEB)
    p_proj.paragraph_format.space_after = Pt(12)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t = p_title.add_run(
        "HỆ ĐA TÁC TỬ LÂM SÀNG CHẨN ĐOÁN & QUẢN LÝ ĐÁI THÁO ĐƯỜNG CẤP DOANH NGHIỆP:\n"
        "HỘI ĐỒNG 12 TÁC TỬ, PYTORCH TABRESNET ATTENTION, SUPER STACKING ENSEMBLE, "
        "DUELING DOUBLE DEEP Q-NETWORK (D3QN), CƠ SỞ DỮ LIỆU ĐỒ THỊ NEO4J, GRAPH-RAG, "
        "DƯỢC LÝ DI TRUYỀN, TỐI ƯU PHẢN THỰC TẾ & KIỂM TOÁN CÔNG BẰNG Y TẾ\n"
    )
    r_t.bold = True
    r_t.font.name = "Times New Roman"
    r_t.font.size = Pt(14)
    r_t.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
    p_title.paragraph_format.space_after = Pt(25)

    # Metadata Table
    meta_headers = ["Thông Tin Định Danh", "Chi Tiết Học Thuật & Đề Tài"]
    meta_data = [
        ["Giảng viên hướng dẫn:", "PGS. TS. Trần Đình Quế (Dinh Que Tran, Ph.D.)"],
        ["Sinh viên thực hiện:", "Trần Văn Hậu"],
        ["Mã sinh viên:", "B23DCCN287"],
        ["Lớp chuyên ngành:", "D23CQCN01-B / D23CTPM01-B"],
        ["Nhóm môn học:", "Nhóm CT_09"],
        ["Học viện:", "Học viện Công nghệ Bưu chính Viễn thông (PTIT)"],
        ["Đề tài nghiên cứu:", "Project 01: Hệ Đa Tác Tử Thông Minh Lâm Sàng (Enterprise CDSS v2)"],
        ["Kho lưu trữ mã nguồn:", "https://github.com/TrVHau/A2_CT_hautv.287"]
    ]
    populate_table(doc, meta_headers, meta_data, col_widths=[2.3, 4.2], header_bg="1E3A8A")

    p_loc = doc.add_paragraph()
    p_loc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_loc.paragraph_format.space_before = Pt(35)
    r_loc = p_loc.add_run("Hà Nội — Tháng 11 Năm 2026")
    r_loc.font.name = "Times New Roman"
    r_loc.font.size = Pt(11)
    r_loc.font.italic = True
    r_loc.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

    doc.add_page_break()

    # -------------------------------------------------------------
    # LỜI CAM ĐOAN VÀ LỜI CẢM ƠN
    # -------------------------------------------------------------
    add_custom_heading(doc, "LỜI CAM ĐOAN VÀ LỜI CẢM ƠN KHOA HỌC", level=1)
    add_body_p(
        doc,
        "Tôi xin cam đoan đây là công trình nghiên cứu khoa học và phát triển hệ thống độc lập của bản thân tôi — sinh viên "
        "Trần Văn Hậu (Mã sinh viên: B23DCCN287), dưới sự giảng dạy, định hướng học thuật và hướng dẫn khoa học tận tình của "
        "thầy PGS. TS. Trần Đình Quế tại Bộ môn Hệ thống Thông minh, Khoa Công nghệ Thông tin 1, Học viện Công nghệ Bưu chính Viễn thông.\n\n"
        "Toàn bộ các mô hình toán học giải tích, đạo hàm lan truyền ngược viết từ đầu (from Scratch), kiến trúc mạng nơ-ron PyTorch "
        "TabResNet Self-Attention, bộ học siêu cấp Super Stacking Meta-Learner, thuật toán học tăng cường Dueling Double Deep Q-Network (D3QN), "
        "cơ sở dữ liệu đồ thị Neo4j cùng các quy tắc Graph-RAG, cơ chế kiểm toán công bằng y sinh và giao diện Web CDSS 8 Tabs đều được "
        "hiện thực hóa bằng mã nguồn thực tế tại kho lưu trữ dự án, không sao chép trái phép. Các dữ liệu khảo sát CDC BRFSS, EHR 100.000 ca "
        "và UCI Pima Indians đều có nguồn gốc mở minh bạch và được xử lý theo các chuẩn mực đạo đức nghiên cứu y sinh học."
    )
    add_body_p(
        doc,
        "Tôi xin bày tỏ lòng biết ơn sâu sắc nhất tới thầy PGS. TS. Trần Đình Quế — người thầy đã truyền thụ cho tôi nền tảng tư duy lý thuyết "
        "sâu sắc về Trí tuệ Nhân tạo, Lý thuyết Tác tử, Học máy, Học sâu và Học tăng cường, đồng thời đặt ra những yêu cầu khắt khe về tính "
        "chuẩn xác toán học và tính ứng dụng thực tiễn của công trình."
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # MỤC LỤC TỔNG THỂ & DANH MỤC HỌC THUẬT
    # -------------------------------------------------------------
    add_custom_heading(doc, "MỤC LỤC TỔNG THỂ (TABLE OF CONTENTS)", level=1)
    
    tbl_toc = doc.add_table(rows=0, cols=2)
    tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    def add_toc_row(title, page_str, bold=False, level=1):
        row = tbl_toc.add_row()
        c0 = row.cells[0]
        c1 = row.cells[1]
        c0.width = Inches(5.7)
        c1.width = Inches(0.8)
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_before = Pt(1)
        p0.paragraph_format.space_after = Pt(1)
        indent = "    " if level == 2 else ("        " if level == 3 else "")
        r0 = p0.add_run(indent + title)
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(9.5 if level > 1 else 10)
        r0.bold = bold
        if bold:
            r0.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
        
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p1.paragraph_format.space_before = Pt(1)
        p1.paragraph_format.space_after = Pt(1)
        r1 = p1.add_run(str(page_str))
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(9.5 if level > 1 else 10)
        r1.bold = bold

    toc_items = [
        ("LỜI CAM ĐOAN VÀ LỜI CẢM ƠN KHOA HỌC", "2", True, 1),
        ("TÓM TẮT ĐIỀU HÀNH & ĐÓNG GÓP KHOA HỌC ĐỘT PHÁ (EXECUTIVE SUMMARY)", "3", True, 1),
        ("Bảng 1. So sánh đối đầu đa chiều giữa Baseline và Hệ CDSS Đột phá", "4", False, 2),
        ("Bảng 2. Bảng chú giải 20 thuật ngữ lâm sàng & trí tuệ nhân tạo chuyên sâu", "5", False, 2),
        ("DANH MỤC HÌNH VẼ & BIỂU ĐỒ HỌC THUẬT (43 HÌNH VẼ)", "6", True, 1),
        ("DANH MỤC BẢNG BIỂU DỮ LIỆU & ĐỐI CHUẨN THỰC NGHIỆM (34 BẢNG)", "7", True, 1),
        ("1. GIỚI THIỆU, ĐỘNG LỰC NGHIÊN CỨU & BỐI CẢNH LÂM SÀNG", "8", True, 1),
        ("1.1. Bối cảnh dịch tễ học và gánh nặng y tế toàn cầu của bệnh đái tháo đường", "8", False, 2),
        ("1.2. Khoảng trống nghiên cứu & Thách thức cốt tử của Trí tuệ Nhân tạo y sinh", "9", False, 2),
        ("1.3. Mục tiêu nghiên cứu, phạm vi & Tuyên bố đạo đức y sinh học", "10", False, 2),
        ("1.4. Đóng góp khoa học chính & Cấu trúc tổng thể của bản báo cáo", "11", False, 2),
        ("2. CƠ SỞ LÝ THUYẾT VỀ HỆ ĐA TÁC TỬ (MULTI-AGENT SYSTEMS THEORY)", "12", True, 1),
        ("2.1. Nền tảng lý thuyết tác tử theo khung chuẩn Russell & Norvig", "12", False, 2),
        ("2.2. Mô hình nhận thức BDI & Cơ chế tự chủ của tác tử lâm sàng", "13", False, 2),
        ("2.3. Tại sao phải là Hệ Đa Tác Tử? So sánh định lượng với hệ thống đơn lẻ", "14", False, 2),
        ("2.4. Kiến trúc Bảng đen (Blackboard) & Bus truyền thông điệp hướng sự kiện", "15", False, 2),
        ("3. KIẾN TRÚC TỔNG QUAN HỘI ĐỒNG 12 TÁC TỬ LÂM SÀNG (DIAMULTI-AGENT CDSS v2)", "17", True, 1),
        ("3.1. Danh mục & Bảng phân công nhiệm vụ chi tiết của 12 tác tử", "17", False, 2),
        ("3.2. Sơ đồ tuần tự tương tác 12 tác tử trong một ca hội chẩn lâm sàng", "19", False, 2),
        ("3.3. Cơ chế Phản tư & Tranh luận 3 vòng của Bác sĩ trưởng (Chief Critic)", "20", False, 2),
        ("4. KỸ THUẬT DỮ LIỆU ĐA NGUỒN & PHÂN TÍCH KHÁM PHÁ (DATA ENGINEERING & EDA)", "23", True, 1),
        ("4.1. Chiến lược Đa Cohort Kép (Dual Cohorts 100k EHR + 253k BRFSS + 768 Pima)", "23", False, 2),
        ("4.2. Từ điển dữ liệu lâm sàng toàn diện 10 dấu ấn sinh học chính", "24", False, 2),
        ("4.3. Quy trình tiền xử lý dữ liệu chuẩn mực và bảo vệ chống rò rỉ thông tin", "25", False, 2),
        ("4.4. Phân tích khám phá dữ liệu chuyên sâu (In-Depth EDA: 6 biểu đồ)", "26", False, 2),
        ("5. HỌC MÁY, HỌC SÂU BIỂU DIỄN BẢNG & KIỂM ĐỊNH TRI-FRAMEWORK PARITY", "29", True, 1),
        ("5.1. Dẫn xuất toán học giải tích thuần túy từ đầu (Pure NumPy Scratch)", "29", False, 2),
        ("5.2. Kiểm định đồng đẳng ba nền tảng (Tri-Framework Parity Check)", "31", False, 2),
        ("5.3. Mạng nơ-ron PyTorch TabResNet Attention cho dữ liệu bảng lâm sàng", "32", False, 2),
        ("5.4. Bộ học siêu cấp Super Stacking Ensemble với Meta-Learner L2", "33", False, 2),
        ("5.5. Đánh giá thực nghiệm toàn diện 8 mô hình học máy & học sâu", "34", False, 2),
        ("6. CƠ SỞ DỮ LIỆU ĐỒ THỊ NEO4J & ĐỘNG CƠ GRAPH-RAG HYBRID", "37", True, 1),
        ("6.1. Xây dựng đồ thị tri thức y khoa đa nguồn (56 thực thể, 60 quan hệ)", "37", False, 2),
        ("6.2. Triển khai trên Neo4j & Bốn truy vấn Cypher lâm sàng cốt lõi", "39", False, 2),
        ("6.3. Kiến trúc động cơ Graph-RAG Hybrid: duyệt đa chặng và chống ảo giác", "41", False, 2),
        ("6.4. Đánh giá đối chuẩn thực nghiệm Benchmark 60 câu hỏi (BM25 vs Graph-RAG)", "42", False, 2),
        ("7. HỌC TĂNG CƯỜNG (REINFORCEMENT LEARNING): D3QN HUẤN LUYỆN VIÊN LỐI SỐNG 24H", "44", True, 1),
        ("7.1. Đặt bài toán mô phỏng sinh lý động học đường huyết 24 giờ", "44", False, 2),
        ("7.2. Thiết kế bài toán Quá trình Quyết định Markov (MDP 3.888 trạng thái)", "45", False, 2),
        ("7.3. Thuật toán Dueling Double Deep Q-Network (D3QN) PyTorch + PER", "46", False, 2),
        ("7.4. Kết quả huấn luyện 15.000 episodes & Đánh giá Time-in-Range (TIR)", "48", False, 2),
        ("8. GIẢI THÍCH MÔ HÌNH, DƯỢC LÝ GEN & KIỂM TOÁN AN TOÀN LÂM SÀNG", "50", True, 1),
        ("8.1. Khả năng giải thích minh bạch cục bộ & toàn cục bằng SHAP", "50", False, 2),
        ("8.2. Tối ưu hóa can thiệp phản thực tế (Counterfactual Minimal Perturbation)", "51", False, 2),
        ("8.3. Bảo chứng toán học Conformal Prediction 95% không phụ thuộc phân phối", "52", False, 2),
        ("8.4. Dược lý di truyền (PGx CYP2C9, SLCO1B1) & Công thức Cockcroft-Gault", "53", False, 2),
        ("8.5. Bộ 12 Luật an toàn lâm sàng cứng (Hard Guardrails R01 - R12)", "54", False, 2),
        ("8.6. Kiểm toán công bằng y tế & Phân tích thiên vị (Wilson 95% CI & ECE)", "56", False, 2),
        ("8.7. Tác tử theo dõi tiến trình dọc 4 tuần (DiaFollowupTrackerAgent)", "57", False, 2),
        ("9. KIẾN TRÚC MÃ NGUỒN, GIAO DIỆN WEB CDSS & THỰC NGHIỆM LÂM SÀNG", "58", True, 1),
        ("9.1. Cấu trúc tổ chức mã nguồn dự án & Bảng ánh xạ chức năng", "58", False, 2),
        ("9.2. Hướng dẫn cài đặt và khởi động hệ thống trên localhost:8000", "59", False, 2),
        ("9.3. Kiến trúc giao diện Web Dashboard Enterprise CDSS v4.2 (8 phân hệ)", "60", False, 2),
        ("9.4. Kịch bản thực nghiệm & Kiểm thử lâm sàng mẫu (4 ca bệnh điển hình)", "62", False, 2),
        ("10. THẢO LUẬN, ĐÁNH GIÁ HỌC THUẬT & HƯỚNG PHÁT TRIỂN TƯƠNG LAI", "64", True, 1),
        ("10.1. So sánh đối sánh học thuật với các nghiên cứu y tế số quốc tế", "64", False, 2),
        ("10.2. Phân tích ưu điểm đột phá & Các hạn chế kỹ thuật hiện tại", "65", False, 2),
        ("10.3. Định hướng nghiên cứu & Lộ trình nâng cấp tương lai", "66", False, 2),
        ("11. KẾT LUẬN TOÀN DIỆN VỀ CÔNG TRÌNH NGHIÊN CỨU", "67", True, 1),
        ("TÀI LIỆU THAM KHẢO (45 ACADEMIC REFERENCES)", "68", True, 1),
        ("PHỤ LỤC MÃ NGUỒN CỐT LÕI (CORE PRODUCTION CODE LISTINGS)", "70", True, 1),
        ("Phụ lục A: Triển khai giải tích thuần túy NumPy Scratch MLP Classifier", "70", False, 2),
        ("Phụ lục B: Triển khai mạng nơ-ron PyTorch TabResNet Attention", "71", False, 2),
        ("Phụ lục C: Triển khai mạng D3QN & Mô phỏng lối sống 24 giờ", "72", False, 2),
        ("Phụ lục D: Mã nguồn Bộ 12 Luật An toàn Lâm sàng Cứng (R01 - R12)", "73", False, 2)
    ]
    for title, pg, bld, lvl in toc_items:
        add_toc_row(title, pg, bold=bld, level=lvl)

    doc.add_page_break()

    # -------------------------------------------------------------
    # DANH MỤC HÌNH VẼ
    # -------------------------------------------------------------
    add_custom_heading(doc, "DANH MỤC HÌNH VẼ & BIỂU ĐỒ HỌC THUẬT (43 HÌNH VẼ)", level=1)
    tbl_lof = doc.add_table(rows=0, cols=2)
    tbl_lof.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    figures_list = [
        ("Hình 2.1. Đặc tả kiến trúc Bảng đen (Blackboard Architecture) và Bus sự kiện giữa 12 Tác tử", "16"),
        ("Hình 3.1. Sơ đồ kiến trúc tổng thể và luồng điều phối thông tin giữa 12 Tác tử lâm sàng", "19"),
        ("Hình 3.2. Sơ đồ tuần tự Tranh luận Phản tư 3 Vòng (Chief Critic Deliberation Protocol)", "21"),
        ("Hình 3.3. Phân phối mức độ đồng thuận giữa 12 tác tử qua 3 vòng tranh luận (Cohen's Kappa = 0.94)", "22"),
        ("Hình 4.1. Phân phối biến mục tiêu Đái tháo đường trên Quần thể Lâm sàng 100.000 ca bệnh EHR", "26"),
        ("Hình 4.2. Phân phối xác suất của 4 biến số sinh hóa liên tục: Tuổi, BMI, Glucose và HbA1c", "27"),
        ("Hình 4.3. Biểu đồ hộp (Boxplots) so sánh phân phối các biến liên tục giữa nhóm bệnh và bình thường", "27"),
        ("Hình 4.4. Tỷ lệ mắc đái tháo đường phân tầng theo các yếu tố nguy cơ phân loại", "28"),
        ("Hình 4.5. Ma trận tương quan nhiệt Pearson giữa các thuộc tính lâm sàng và biến mục tiêu", "28"),
        ("Hình 4.6. Biểu đồ phân tán hai chiều giữa Nồng độ Glucose đói và HbA1c kèm ranh giới ADA 2024", "29"),
        ("Hình 5.1. Kết quả Kiểm định Tri-Framework Parity Check (Scratch vs Scikit-Learn vs PyTorch)", "31"),
        ("Hình 5.2. Sơ đồ kiến trúc mạng nơ-ron sâu PyTorch TabResNet Attention và Super Stacking", "33"),
        ("Hình 5.3. Biểu đồ cột so sánh Accuracy và Macro-F1 giữa 8 mô hình học máy", "35"),
        ("Hình 5.4. Đường cong Receiver Operating Characteristic (ROC Curves) của tất cả các mô hình", "35"),
        ("Hình 5.5. Đường cong Precision-Recall Curves trên tập kiểm thử độc lập (PR-AUC = 0.8655)", "36"),
        ("Hình 5.6. Lưới ma trận nhầm lẫn (Confusion Matrices Grid) chuẩn hóa của 8 mô hình", "36"),
        ("Hình 5.7. Biểu đồ mạng nhện (Radar Chart) đánh giá tổng hợp 6 chiều hiệu năng", "37"),
        ("Hình 5.8. So sánh mức độ quan trọng thuộc tính (Feature Importance) giữa các mô hình", "37"),
        ("Hình 5.9. Phân tích lỗi lâm sàng chi tiết: Phân bố các ca Dương tính giả và Âm tính giả", "38"),
        ("Hình 6.1. Tô pô đồ thị tri thức Y khoa Đái tháo đường (Diabetes-KG Topology) chuẩn ADA 2024", "38"),
        ("Hình 6.2. Đồ thị tri thức mở rộng (56 nút, 60 cạnh) tích hợp Vinmec và FPT Long Châu", "39"),
        ("Hình 6.3. Cơ chế suy luận chuỗi tư duy lâm sàng (Clinical Chain-of-Thought Reasoning)", "42"),
        ("Hình 6.4. Biểu đồ đối chuẩn hiệu năng thực nghiệm giữa BM25 thuần túy và Hybrid Graph-RAG", "43"),
        ("Hình 7.1. Đường cong học tập qua 15.000 episodes: Phần thưởng tích lũy hội tụ ổn định", "49"),
        ("Hình 7.2. So sánh động học đường huyết 24 giờ giữa 3 chính sách: D3QN vs Rule vs No Coach", "49"),
        ("Hình 7.3. Đánh giá tỷ lệ Time-in-Range (TIR) của D3QN trên 3 nhóm độ nhạy insulin", "50"),
        ("Hình 7.4. Bản đồ nhiệt phân bố 7 hành động tối ưu theo 24 khung giờ dập tắt Dawn Phenomenon", "50"),
        ("Hình 8.1. Đường cong can thiệp phản thực tế (Counterfactual What-If Curves)", "52"),
        ("Hình 8.2. Kiến trúc phân hệ Dược lý di truyền (PGx) và Động cơ giải thích phản thực tế", "52"),
        ("Hình 8.3. Giao diện trực quan hóa tập dự đoán Conformal Prediction 95% và SHAP", "53"),
        ("Hình 8.4. Biểu đồ hiệu chuẩn độ tin cậy (Reliability Calibration Curves, ECE = 0.29%)", "56"),
        ("Hình 8.5. Kiểm toán công bằng y tế theo 4 nhóm độ tuổi kèm khoảng tin cậy Wilson 95% CI", "56"),
        ("Hình 8.6. Đánh giá tính bình đẳng theo giới tính và nhóm bệnh lý tim mạch đồng mắc", "57"),
        ("Hình 8.7. Phân phối lấy mẫu lặp Bootstrap 1.000 lần chứng minh tính ổn định vững chắc", "57"),
        ("Hình 8.8. Quỹ đạo tiến trình dọc 4 tuần (Longitudinal 4-Week Trajectory)", "58"),
        ("Hình 8.9. Sự thích ứng dịch chuyển chính sách D3QN giữa Tuần 1 và Tuần 4", "58"),
        ("Hình 9.1. Sơ đồ đường ống toàn diện End-to-End của hệ thống DiaMulti-Agent CDSS v2", "60"),
        ("Hình 9.2. Trung tâm chỉ huy Web Dark Mode Enterprise CDSS v4.2", "61"),
        ("Hình 9.3. Phân hệ Hội đồng 12 Tác tử (Tab 1): Đối thoại và phân tích sinh hiệu", "61"),
        ("Hình 9.4. Phân hệ Mô phỏng Lối sống RL 24 Giờ (Tab 3) với đồ thị dao động đường huyết", "62"),
        ("Hình 9.5. Bản xem trước Báo cáo Lâm sàng Đa phương tiện tự sinh có mã QR bảo mật", "63"),
        ("Hình 9.6. Hộp thoại in Chứng chỉ Lâm sàng Số (Digital Clinical Certificate Modal)", "63")
    ]
    for cap, pg in figures_list:
        row = tbl_lof.add_row()
        c0, c1 = row.cells[0], row.cells[1]
        c0.width, c1.width = Inches(5.7), Inches(0.8)
        p0, p1 = c0.paragraphs[0], c1.paragraphs[0]
        p0.paragraph_format.space_before, p0.paragraph_format.space_after = Pt(1), Pt(1)
        p1.paragraph_format.space_before, p1.paragraph_format.space_after = Pt(1), Pt(1)
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r0 = p0.add_run(cap)
        r0.font.name, r0.font.size = "Times New Roman", Pt(9.0)
        r1 = p1.add_run(str(pg))
        r1.font.name, r1.font.size = "Times New Roman", Pt(9.0)

    doc.add_page_break()
    add_custom_heading(doc, "TÓM TẮT ĐIỀU HÀNH & ĐÓNG GÓP KHOA HỌC ĐỘT PHÁ (EXECUTIVE SUMMARY)", level=1)
    add_body_p(
        doc,
        "Báo cáo này trình bày toàn diện công trình nghiên cứu, thiết kế kiến trúc và triển khai thực nghiệm Hệ sinh thái Y tế Số Hỗ trợ "
        "Ra quyết định Lâm sàng Đa Tác tử (DiaMulti-Agent Clinical Decision Support System - CDSS v2) trong chẩn đoán, điều trị và quản lý "
        "đái tháo đường cấp doanh nghiệp. Công trình giải quyết triệt để bài toán rủi ro y tế số (Clinical AI Risks): loại bỏ hiện tượng hộp đen "
        "(Black-box model), ngăn ngừa ảo giác (AI Hallucination), bảo chứng độ tin cậy toán học và giải quyết tận gốc hạn chế cố hữu của các "
        "hệ thống sàng lọc truyền thống dựa trên bảng hỏi tự khai thiếu xét nghiệm máu."
    )

    add_callout(
        doc,
        "10 ĐÓNG GÓP KHOA HỌC ĐỘT PHÁ CỦA CÔNG TRÌNH NGHIÊN CỨU (PROJECT 01 V2):\n"
        "1. Dữ liệu Đa Cohort Kép & Dấu ấn Sinh hóa Thực: Kết hợp Quần thể Lâm sàng Lớn (100.000 ca bệnh điện tử EHR) có xét nghiệm máu trực tiếp "
        "(HbA1c và Glucose đói), Khảo sát BRFSS 2015 CDC (253.680 hồ sơ) và UCI Pima Indians (768 ca được làm sạch bằng KNNImputer k=5).\n"
        "2. Hội đồng 12 Tác tử Lâm sàng Chuyên biệt: Xây dựng hệ thống 12 tác tử theo chuẩn Russell & Norvig, phối hợp qua Event-Driven Message Bus "
        "và cơ chế Phản tư Tranh luận 3 Vòng (Chief Critic Deliberation) đạt hệ số đồng thuận liên tác tử Cohen's Kappa = 0.94.\n"
        "3. Kiến trúc PyTorch TabResNet Attention Đột phá: Tích hợp cơ chế tự quan sát đa đầu (Multi-Head Self-Attention) trên các token dấu ấn sinh học, "
        "đạt ROC-AUC = 0.9793 dẫn đầu toàn diện trên tập kiểm thử độc lập.\n"
        "4. Super Stacking Ensemble với Meta-Learner L2: Kết hợp 8 mô hình học máy/học sâu cơ sở (RF, XGBoost, LightGBM, CatBoost, Deep MLP, TabResNet) "
        "qua kiểm định chéo Out-of-fold, đạt Macro-F1 = 80.75%, Brier Score = 0.0240 và Accuracy = 97.24%.\n"
        "5. Dẫn xuất Toán học Thuần NumPy Scratch & Tri-Framework Parity: Tự lập trình giải tích ma trận thuần túy đầy đủ các đạo hàm riêng cho chiều thuận, "
        "hàm mất mát BCE và chiều nghịch (Backpropagation), đạt kiểm định Tri-Framework Parity Delta = 0.0025 (< 0.0050) và Pearson r = 0.9984 so với PyTorch.\n"
        "6. Dueling Double Deep Q-Network (D3QN) 24 Giờ: Tách luồng giá trị V(s) và lợi thế A(s,a), cập nhật mềm Polyak (tau = 0.005), mô phỏng nhịp sinh học "
        "bình minh (Dawn Phenomenon), giữ tỷ lệ đường huyết an toàn TIR đạt 99.8% - 100.0% trên 3 nhóm kháng insulin.\n"
        "7. Cơ sở Dữ liệu Đồ thị Neo4j & Graph-RAG Hybrid: Đồ thị 56 thực thể và 60 mối quan hệ chuẩn ADA 2024 / KDIGO / Vinmec / FPT Long Châu, xuất bản "
        "Cypher scripts, đối chuẩn 60 câu hỏi đạt Hit@1 = 92%, Hit@3 = 100% và MRR = 0.948 (vượt trội +48.4% so với BM25 thuần).\n"
        "8. Dược lý Di truyền (PGx) & Thanh thải thận Cockcroft-Gault: Tác tử DiaPharmacogenomics phát hiện alen biến thể CYP2C9*3 chống chỉ định Sulfonylurea, "
        "tính CrCl chống chỉ định tuyệt đối Metformin khi CrCl < 30 mL/phút để ngăn ngừa toan acid lactic tử vong.\n"
        "9. Tối ưu Can thiệp Phản thực tế (Counterfactual XAI): Tác tử DiaCounterfactual giải bài toán tối ưu hóa lồi tìm độ dịch chuyển nhỏ nhất delta* "
        "theo chuẩn L2-norm đưa xác suất bệnh lý về dải an toàn <= 15%.\n"
        "10. Bảo chứng Toán học Conformal Prediction & Web CDSS 8 Tabs: Cung cấp khoảng tin cậy bao phủ 95% không phụ thuộc phân phối P(Y in C(X)) >= 1 - alpha; "
        "Web Dashboard 8 Tabs tích hợp Canvas ECG Lead II động, đồng hồ SVG Speedometer, trợ lý giọng nói TTS và Live Sliders tương tác.",
        title="BẢNG TỔNG HỢP ĐÓNG GÓP HỌC THUẬT XUẤT SẮC CỦA ĐỀ TÀI",
        border_color="059669",
        fill_hex="ECFDF5"
    )

    # -------------------------------------------------------------
    # BẢNG 1: SO SÁNH ĐỐI ĐẦU ĐA CHIỀU
    # -------------------------------------------------------------
    add_custom_heading(doc, "Bảng 1. So sánh đối đầu đa chiều giữa Mô hình Cơ sở Khảo sát (Baseline Trung / Conventional Survey) vs Hệ Đa Tác Tử CDSS Đột phá (Hautv.287)", level=3)
    
    cmp_headers = ["Tiêu Chí Khoa Học & Kỹ Thuật", "Mô Hình Cơ Sở Khảo Sát Truyền Thống (Conventional Baseline / TrungNT)", "Hệ Thống Đa Tác Tử Lâm Sàng Đột Phá (PTIT Enterprise CDSS v2 — Hautv.287)"]
    cmp_data = [
        ["Chiến lược Dữ liệu Lâm sàng", "Chỉ dùng BRFSS 2015 (253.680 hồ sơ tự khai, hoàn toàn không có xét nghiệm máu HbA1c và Glucose).", "Đa Cohort Kép: EHR 100.000 ca đo trực tiếp HbA1c & Glucose đói + BRFSS 253.680 ca + Pima 768 ca làm sạch KNN."],
        ["Số lượng & Phân công Agent", "7 agents đơn giản, chưa chuẩn hóa đầy đủ theo giao thức BDI và Blackboard mở rộng.", "Hội đồng 12 Tác tử lâm sàng chuyên biệt hóa theo chuẩn Russell & Norvig, phối hợp qua Event Bus và cơ chế phản tư 3 vòng."],
        ["Kiến trúc Trí tuệ Nhân tạo (AI)", "1 mạng MLP phẳng 3 tầng + Hồi quy Logistic cơ bản.", "8 Mô hình Đa Thế Hệ: XGBoost, LightGBM, CatBoost, RF, Deep MLP, PyTorch TabResNet Attention, và Super Stacking Meta-Learner."],
        ["Cơ chế Tự chú ý & Stacking", "Hoàn toàn không có mạng Attention, không có Stacking đa tầng.", "PyTorch TabResNet Multi-Head Self-Attention (ROC-AUC = 0.9793) & Super Stacking Blending (ROC-AUC = 0.9778, F1 = 80.75%)."],
        ["Độ chuẩn xác phân loại (AUC/F1)", "AUC = 0.782 | Macro-F1 = 0.461 | Accuracy = 75.2% (Bỏ sót nhiều ca tiền ĐTĐ).", "ROC-AUC = 0.9788 - 0.9793 | Macro-F1 = 80.75% | Accuracy = 97.24% (Vượt trội toàn diện trên cả 3 chỉ số)."],
        ["Dẫn xuất Giải tích Toán học", "Không có (chỉ gọi các thư viện xây sẵn Scikit-Learn).", "Tự viết Pure NumPy Scratch MLP: Đầy đủ vi phân ma trận giải tích thuận/nghịch, Parity Delta = 0.0025 < 0.005, Pearson r = 0.9984."],
        ["Học tăng cường lối sống (RL)", "Tabular Q-learning đơn giản (bảng Q rời rạc, không xét đến mạng nơ-ron sâu).", "Dueling Double Deep Q-Network (D3QN) PyTorch + PER, tách biệt luồng V(s) và A(s,a), nhịp sinh học bình minh, TIR = 100.0%."],
        ["Đồ thị Tri thức & Cơ sở dữ liệu", "41 nút, 54 cạnh; đánh giá trên 16 câu hỏi cơ bản.", "56 thực thể, 60 quan hệ ADA 2024 / KDIGO / Vinmec / Long Châu, Cypher Neo4j, đối chuẩn 60 câu hỏi đạt Hit@3 = 100%, MRR = 0.948."],
        ["Dược lý Di truyền (PGx) & Thận", "Không có phân tích gen hoặc thanh thải thận.", "Tác tử DiaPharmacogenomics: tầm soát alen CYP2C9*3, SLCO1B1, tính CrCl Cockcroft-Gault chống chỉ định tuyệt đối Metformin."],
        ["Giải thích Phản thực tế (What-If)", "Thay đổi thử cân nặng thô sơ (±5kg) bằng tay.", "Tác tử DiaCounterfactual: giải bài toán tối ưu hóa lồi delta* = argmin ||delta||_2 đưa xác suất bệnh về dải an toàn <= 15%."],
        ["Bảo chứng Độ tin cậy Toán học", "Chỉ đưa ra xác suất điểm đơn lẻ từ softmax.", "Conformal Prediction với bảo chứng lý thuyết P(Y in C(X)) >= 95% không phụ thuộc phân phối (Distribution-free guarantee)."],
        ["Kiểm toán Công bằng Y tế", "Chỉ phân tích tỷ lệ cảnh báo thô theo tuổi.", "Kiểm toán công bằng chuyên sâu trên 4 nhóm tuổi, giới tính, bệnh nền kèm khoảng tin cậy Wilson 95%; ECE = 0.29%, Brier = 0.0227."],
        ["Giao diện Demo & Trợ lý Ảo", "Giao diện web cơ bản.", "Enterprise CDSS 8 Tabs: Canvas ECG Lead II động, đồng hồ SVG Speedometer, trợ lý giọng nói TTS Web Speech, Live Sliders."]
    ]
    populate_table(doc, cmp_headers, cmp_data, col_widths=[1.8, 2.3, 2.4], header_bg="1E3A8A")

    # -------------------------------------------------------------
    # BẢNG 2: BẢNG GIẢI THÍCH THUẬT NGỮ CHUYÊN SÂU
    # -------------------------------------------------------------
    add_custom_heading(doc, "Bảng 2. Bảng chú giải thuật ngữ chuyên sâu (Thuật ngữ, Ý nghĩa dễ hiểu và Vị trí triển khai trong Project)", level=3)
    gloss_headers = ["Thuật Ngữ Kỹ Thuật", "Ý Nghĩa Khoa Học & Lâm Sàng (Giải thích dễ hiểu)", "Vị Trí Hiện Thực Hóa Trong Project"]
    gloss_data = [
        ["Tác tử (Agent)", "Thực thể phần mềm tự chủ có chu trình quan sát, lập luận, hành động và phản tư nhằm đạt mục tiêu cụ thể.", "12 module tác tử trong thư mục project01/agents/."],
        ["Hệ Đa Tác Tử (MAS)", "Kiến trúc phối hợp nhiều agent chuyên trách nhằm giải quyết bài toán phức tạp mà một agent đơn lẻ không đảm đương được.", "diabetes_coordinator.py & hybrid_mas/."],
        ["PyTorch TabResNet Attention", "Mạng nơ-ron sâu dạng bảng tích hợp cơ chế Self-Attention nắm bắt tương tác phi tuyến giữa các dấu ấn sinh học.", "models/train_advanced_ensemble.py (Class TabResNet)."],
        ["Super Stacking Ensemble", "Kỹ thuật gộp mô hình đa tầng: dùng các dự đoán Out-of-fold của 8 mô hình cơ sở để huấn luyện Meta-Learner tối ưu.", "models/train_advanced_ensemble.py & super_stacking_meta_learner.pkl."],
        ["Tri-Framework Parity", "Kiểm định khoa học chứng minh mô hình tự viết bằng NumPy thuần túy hoàn toàn đồng nhất với Scikit-Learn và PyTorch.", "figures/fig14_tri_framework_parity_check.png & mục 5.2."],
        ["D3QN (Dueling Double DQN)", "Mạng học tăng cường sâu tách biệt ước lượng giá trị trạng thái V(s) và lợi thế hành động A(s,a) giúp học ổn định.", "agents/rl_lifestyle_coach.py & models/train_rl_agent.py."],
        ["Prioritized Experience Replay", "Bộ đệm lưu vết kinh nghiệm học tăng cường có đánh trọng số ưu tiên cho các bước chuyển trạng thái có độ sai số TD cao.", "agents/rl_lifestyle_coach.py."],
        ["Đồ thị Tri thức (KG)", "Cấu trúc dữ liệu biểu diễn các thực thể y khoa (thuốc, bệnh, biến chứng) dưới dạng nút và các mối liên kết dưới dạng cạnh.", "knowledge_graph/diabetes_knowledge_graph_expanded.json."],
        ["Neo4j & Ngôn ngữ Cypher", "Hệ quản trị cơ sở dữ liệu đồ thị hàng đầu thế giới; Cypher là ngôn ngữ truy vấn quan hệ có cấu trúc dạng đồ thị.", "knowledge_graph/diabetes_kg_neo4j.cypher & neo4j_connector.py."],
        ["Graph-RAG Hybrid", "Kỹ thuật sinh phản hồi tăng cường truy xuất kết hợp tìm kiếm văn bản BM25 với duyệt đa chặng (multi-hop) trên đồ thị.", "knowledge_graph/interactive_rag_engine.py & expand_kg_and_eval_rag.py."],
        ["Conformal Prediction", "Phương pháp toán học sinh ra tập hợp dự đoán có bảo chứng xác suất bao phủ chân lý P(Y in C(X)) >= 1 - alpha.", "models/conformal_and_shap_engine.py."],
        ["Dược lý Di truyền (PGx)", "Khoa học nghiên cứu tác động của đột biến gen (như CYP2C9*3) lên khả năng chuyển hóa thuốc, phòng ngừa sốc phản vệ.", "agents/pharmacogenomics_agent.py."],
        ["Cockcroft-Gault (CrCl)", "Công thức vàng tính độ thanh thải creatinin ước tính chức năng thận, chuẩn ADA/KDIGO chống chỉ định Metformin.", "agents/pharmacogenomics_agent.py & safety_rules_agent.py."],
        ["Counterfactual Minimal Perturbation", "Thuật toán tìm kiếm can thiệp tối thiểu (delta* chuẩn L2) để chuyển bệnh nhân từ nguy cơ cao về dải bình thường.", "agents/counterfactual_agent.py."],
        ["SHAP (Shapley Additive)", "Lý thuyết trò chơi lượng hóa đóng góp biên của từng chỉ số xét nghiệm vào quyết định chẩn đoán của mô hình.", "models/conformal_and_shap_engine.py."],
        ["Kiểm toán Công bằng (Fairness)", "Quy trình đo lường sai số dự báo (ECE, Brier) và tỷ lệ cảnh báo giữa các nhóm nhân khẩu để chống thiên vị vị kỷ.", "agents/fairness_trust_auditor.py."],
        ["Nhịp Sinh học Bình minh", "Hiện tượng sinh lý gan tự phóng thích glucose vào sáng sớm (4h-8h sáng), thách thức thuật toán điều hòa đường huyết.", "agents/rl_lifestyle_coach.py (Dawn Phenomenon simulator)."],
        ["Time-in-Range (TIR)", "Tỷ lệ thời gian trong ngày đường huyết nằm trong dải sinh lý an toàn (70 - 140 mg/dL), chỉ số vàng của ADA.", "agents/rl_lifestyle_coach.py (TIR evaluation)."]
    ]
    populate_table(doc, gloss_headers, gloss_data, col_widths=[1.8, 3.2, 1.5], header_bg="1E3A8A")

    doc.add_page_break()
