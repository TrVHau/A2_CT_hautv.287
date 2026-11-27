# -*- coding: utf-8 -*-
"""Front matter: Cover, Acknowledgements, Abbreviations, TOC, List of Tables and Figures."""

from pathlib import Path
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def add_cover(doc, logo_path):
    # Cover Section
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(12)
    p_inst.paragraph_format.space_after = Pt(2)
    r1 = p_inst.add_run("HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG\n")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(14)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(15, 23, 42)
    r2 = p_inst.add_run("KHOA CÔNG NGHỆ THÔNG TIN 1")
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(13)
    r2.font.bold = True
    r2.font.color.rgb = RGBColor(30, 58, 138)

    p_div = doc.add_paragraph()
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_div.paragraph_format.space_after = Pt(18)
    r_div = p_div.add_run("———————o0o———————")
    r_div.font.name = "Times New Roman"
    r_div.font.color.rgb = RGBColor(100, 116, 139)

    # Logo
    if Path(logo_path).exists():
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_after = Pt(20)
        p_logo.add_run().add_picture(str(logo_path), width=Inches(1.5))

    # Title
    p_type = doc.add_paragraph()
    p_type.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_type.paragraph_format.space_after = Pt(8)
    rt = p_type.add_run("BÁO CÁO TIỂU LUẬN FINAL MÔN HỌC\nPHÁT TRIỂN HỆ THỐNG THÔNG MINH")
    rt.font.name = "Times New Roman"
    rt.font.size = Pt(15)
    rt.font.bold = True
    rt.font.color.rgb = RGBColor(30, 58, 138)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(8)
    p_title.paragraph_format.space_after = Pt(6)
    r_main = p_title.add_run("NGHIÊN CỨU VÀ PHÁT TRIỂN HỆ THỐNG THÔNG MINH TOÀN DIỆN:")
    r_main.font.name = "Times New Roman"
    r_main.font.size = Pt(17)
    r_main.font.bold = True
    r_main.font.color.rgb = RGBColor(15, 23, 42)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(24)
    r_sub = p_sub.add_run("TỪ HỌC MÁY CƠ BẢN, CNN, RNN–LSTM ĐẾN KNOWLEDGE GRAPH,\nDEEP GRAPH VÀ HỆ ĐA TÁC TỬ TỰ CHỦ\n(Dual Domains: Hệ Y tế Chuyển hóa & Hệ Tài chính Định lượng)")
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(13.5)
    r_sub.font.bold = True
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(29, 78, 216)

    # Info box
    p_info = doc.add_paragraph()
    p_info.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_info.paragraph_format.left_indent = Inches(1.8)
    p_info.paragraph_format.space_before = Pt(24)
    p_info.paragraph_format.line_spacing = 1.3
    
    infos = [
        ("Giảng viên hướng dẫn:", "PGS. TS. Trần Đình Quế"),
        ("Sinh viên thực hiện:", "Trần Văn Hậu"),
        ("Mã sinh viên:", "B23DCCN287"),
        ("Lớp chuyên ngành:", "D23CTPM01"),
        ("Nhóm môn học:", "CT"),
        ("Nhóm tiểu luận:", "09"),
    ]
    for lbl, val in infos:
        r_l = p_info.add_run(f"{lbl:<24} ")
        r_l.font.name = "Times New Roman"
        r_l.font.size = Pt(12)
        r_l.font.bold = True
        r_v = p_info.add_run(f"{val}\n")
        r_v.font.name = "Times New Roman"
        r_v.font.size = Pt(12)
        r_v.font.bold = False

    # Location & Date
    p_loc = doc.add_paragraph()
    p_loc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_loc.paragraph_format.space_before = Pt(36)
    r_loc = p_loc.add_run("HÀ NỘI — THÁNG 11 NĂM 2026")
    r_loc.font.name = "Times New Roman"
    r_loc.font.size = Pt(11.5)
    r_loc.font.bold = True
    r_loc.font.color.rgb = RGBColor(100, 116, 139)


def add_academic_preamble(doc, p_body, h_sec):
    doc.add_page_break()
    h_sec(doc, "LỜI CAM ĐOAN VÀ LỜI CẢM ƠN")
    
    p_body(doc, "Tôi xin cam đoan đây là công trình nghiên cứu và thực nghiệm độc lập của bản thân tôi — sinh viên Trần Văn Hậu, dưới sự giảng dạy, định hướng và hướng dẫn khoa học tận tình của PGS. TS. Trần Đình Quế. Toàn bộ các kết quả thực nghiệm, số liệu phân tích trong các bảng biểu, các đồ thị trực quan hóa không gian ẩn, các ma trận nhầm lẫn và kết quả đo đạc kiểm chứng chéo (cross-validation) trong báo cáo này đều được tính toán và trích xuất trực tiếp từ các mã nguồn, tập dữ liệu thực tế và các kịch bản chạy thật của bản thân tôi trong suốt quá trình học tập môn học Phát triển Hệ thống Thông minh.")
    p_body(doc, "Mọi thông tin, tri thức tham khảo, các định lý toán học, các kiến trúc kinh điển của các nhà khoa học tiền bối (như Alan Turing, Yann LeCun, Thomas Kipf, Ashish Vaswani...) đều được dẫn chiếu nguồn gốc minh bạch, đầy đủ theo đúng chuẩn học thuật quốc tế IEEE.")
    p_body(doc, "Tôi xin gửi lời tri ân sâu sắc nhất tới PGS. TS. Trần Đình Quế — người thầy đã truyền thụ cho chúng tôi tư duy hệ thống mạch lạc, phương pháp luận nghiên cứu sâu sắc: 'Hiểu bản chất toán học, biểu diễn tường minh thông tin, học từ dữ liệu thực tế và hiện thực hóa thành ứng dụng hoàn chỉnh'. Nhờ những lời chỉ dẫn quý báu, những yêu cầu khắt khe về tính đúng đắn khoa học và kiểm chứng tương đương, tôi đã hoàn thiện được công trình tiểu luận tổng hợp này với tất cả niềm đam mê nghiên cứu khoa học công nghệ.")
    
    p_sign = doc.add_paragraph()
    p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sign.paragraph_format.space_before = Pt(14)
    r_s1 = p_sign.add_run("Sinh viên thực hiện\n\n\n")
    r_s1.font.name = "Times New Roman"
    r_s1.font.italic = True
    r_s2 = p_sign.add_run("Trần Văn Hậu\nB23DCCN287")
    r_s2.font.name = "Times New Roman"
    r_s2.font.bold = True


def add_abbreviations(doc, h_sec, add_table_data):
    doc.add_page_break()
    h_sec(doc, "DANH MỤC TỪ VIẾT TẮT")
    headers = ["Ký hiệu", "Tên tiếng Anh đầy đủ", "Ý nghĩa / Diễn giải tiếng Việt"]
    rows = [
        ["AI", "Artificial Intelligence", "Trí tuệ Nhân tạo"],
        ["ML", "Machine Learning", "Học máy"],
        ["DL", "Deep Learning", "Học sâu"],
        ["ANN / MLP", "Artificial Neural Network / Multilayer Perceptron", "Mạng nơ-ron nhân tạo / Mạng nơ-ron truyền thẳng nhiều lớp"],
        ["CNN", "Convolutional Neural Network", "Mạng nơ-ron tích chập (chuyên xử lý dữ liệu lưới không gian / ảnh)"],
        ["RNN", "Recurrent Neural Network", "Mạng nơ-ron hồi quy (chuyên xử lý dữ liệu chuỗi tuần tự / thời gian)"],
        ["LSTM", "Long Short-Term Memory", "Mạng nơ-ron bộ nhớ dài - ngắn hạn có cơ chế cổng điều khiển"],
        ["GRU", "Gated Recurrent Unit", "Đơn vị hồi quy có cổng (phiên bản tinh gọn của LSTM)"],
        ["BPTT", "Backpropagation Through Time", "Thuật toán lan truyền ngược qua thời gian trong mạng hồi quy"],
        ["Grad-CAM", "Gradient-weighted Class Activation Mapping", "Bản đồ kích hoạt lớp có trọng số gradient để giải thích trực quan CNN"],
        ["KG", "Knowledge Graph", "Đồ thị tri thức (biểu diễn tri thức dưới dạng các bộ ba thực thể - quan hệ)"],
        ["RAG", "Retrieval-Augmented Generation", "Sinh văn bản tăng cường bằng truy xuất tri thức có căn cứ"],
        ["RRF", "Reciprocal Rank Fusion", "Thuật toán hợp nhất thứ hạng nghịch đảo cho truy hồi lai Hybrid"],
        ["GNN", "Graph Neural Network", "Mạng nơ-ron đồ thị (học sâu trên dữ liệu cấu trúc phi Euclid)"],
        ["GCN", "Graph Convolutional Network", "Mạng tích chập đồ thị (biến đổi Fourier trên phổ Laplacian chuẩn hóa)"],
        ["GraphSAGE", "Sample and Aggregate", "Khung lấy mẫu và gộp quy nạp cho mạng nơ-ron đồ thị"],
        ["GAT", "Graph Attention Network", "Mạng chú ý đồ thị (cơ chế tự chú ý gán trọng số cho từng cạnh liên kết)"],
        ["MPNN", "Message Passing Neural Network", "Khung truyền thông điệp tổng quát hóa cho các mạng nơ-ron đồ thị"],
        ["1-WL", "1-Weisfeiler-Lehman Test", "Phép thử đẳng cấu đồ thị xác định giới hạn biểu diễn của GNN"],
        ["MAD", "Mean Average Distance", "Khoảng cách trung bình giữa các nút (thước đo hiện tượng làm trơn quá mức)"],
        ["MAS", "Multi-Agent Systems", "Hệ đa tác tử (hệ thống gồm nhiều tác tử phần mềm phối hợp/đối kháng)"],
        ["MARL", "Multi-Agent Reinforcement Learning", "Học tăng cường đa tác tử"],
        ["LLM", "Large Language Model", "Mô hình ngôn ngữ lớn (như GPT-4, Qwen, Llama, Gemini)"],
        ["PEAS", "Performance, Environment, Actuators, Sensors", "Mô hình đặc tả chuẩn cho hệ thống tác tử thông minh"],
        ["EDA", "Exploratory Data Analysis", "Phân tích và khám phá dữ liệu"],
        ["ROC-AUC", "Receiver Operating Characteristic - Area Under Curve", "Diện tích dưới đường cong đặc trưng hoạt động bộ thu"],
        ["PR-AUC", "Precision-Recall Area Under Curve", "Diện tích dưới đường cong độ chính xác - độ bao phủ"],
        ["CGM", "Continuous Glucose Monitoring", "Hệ thống theo dõi nồng độ đường huyết liên tục (15 phút/lần)"],
        ["TF-IDF", "Term Frequency - Inverse Document Frequency", "Tần suất từ - nghịch đảo tần suất tài liệu (trích xuất đặc trưng văn bản)"],
        ["SGD", "Stochastic Gradient Descent", "Thuật toán hạ gradient ngẫu nhiên"],
    ]
    add_table_data(doc, headers, rows, widths=[1.2, 2.5, 2.8])
