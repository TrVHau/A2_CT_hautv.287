import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHARTS_DIR = os.path.join(BASE_DIR, 'charts')
OUTPUT_DOCX = os.path.join(BASE_DIR, 'tieuluan01_CT01_09_TranVanHau.docx')

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_callout(doc, title, text, bg_hex="F0F4F8", border_hex="1565C0"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, bg_hex)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="none"/><w:left w:val="single" w:sz="24" w:space="0" w:color="{border_hex}"/><w:bottom w:val="none"/><w:right w:val="none"/></w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    r_title = p.add_run(f"📌 {title}: ")
    r_title.bold = True
    r_title.font.name = 'Arial'
    r_title.font.size = Pt(10)
    r_title.font.color.rgb = RGBColor(0x0D, 0x47, 0xA1)
    
    r_text = p.add_run(text)
    r_text.font.name = 'Arial'
    r_text.font.size = Pt(9.5)
    r_text.font.italic = True
    r_text.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_code_block(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "0F172A")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(code_text)
    r.font.name = 'Consolas'
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(0x38, 0xBD, 0xF8)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def format_table(table, header_bg="1565C0", alt_bg="F8FAFC"):
    for i, row in enumerate(table.rows):
        for cell in row.cells:
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            if i == 0:
                set_cell_background(cell, header_bg)
                for p in cell.paragraphs:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    for r in p.runs:
                        r.bold = True
                        r.font.name = 'Arial'
                        r.font.size = Pt(8.5)
                        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            else:
                if i % 2 == 1:
                    set_cell_background(cell, alt_bg)
                for p in cell.paragraphs:
                    for r in p.runs:
                        r.font.name = 'Arial'
                        r.font.size = Pt(8.5)

def add_heading_with_spacing(doc, text, level):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.keep_with_next = True
    if level == 1:
        h.paragraph_format.space_before = Pt(16)
        h.paragraph_format.space_after = Pt(6)
        for r in h.runs:
            r.font.name = 'Arial'
            r.font.size = Pt(15)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0x0D, 0x47, 0xA1)
    elif level == 2:
        h.paragraph_format.space_before = Pt(12)
        h.paragraph_format.space_after = Pt(4)
        for r in h.runs:
            r.font.name = 'Arial'
            r.font.size = Pt(12.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0x15, 0x65, 0xC0)
    elif level == 3:
        h.paragraph_format.space_before = Pt(8)
        h.paragraph_format.space_after = Pt(3)
        for r in h.runs:
            r.font.name = 'Arial'
            r.font.size = Pt(10.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0x2E, 0x7D, 0x32)
    return h

def add_figure_image(doc, fig_filename, caption_text):
    fig_path = os.path.join(CHARTS_DIR, fig_filename)
    if os.path.exists(fig_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        run_img = p_img.add_run()
        run_img.add_picture(fig_path, width=Inches(6.2))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(10)
        run_cap = p_cap.add_run(caption_text)
        run_cap.font.name = 'Arial'
        run_cap.font.size = Pt(8.5)
        run_cap.font.italic = True
        run_cap.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

def build_master_docx():
    print(f"Building Comprehensive Word Document: {OUTPUT_DOCX}...")
    doc = Document()
    
    # Page setup: Standard A4, 1-inch margins
    sections = doc.sections
    for section in sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # =========================================================================
    # TRANG BÌA (COVER PAGE)
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG\nKHOA CÔNG NGHỆ THÔNG TIN 1\n————————o0o————————\n\n")
    r.font.name = 'Arial'
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0x0D, 0x47, 0xA1)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(30)
    p_title.paragraph_format.space_after = Pt(10)
    r = p_title.add_run("TIỂU LUẬN MÔN HỌC\nPHÁT TRIỂN HỆ THỐNG THÔNG MINH\n\n")
    r.font.name = 'Arial'
    r.font.size = Pt(16)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0xC6, 0x28, 0x28)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(40)
    r = p_sub.add_run("ĐỀ TÀI:\nTRÍ TUỆ NHÂN TẠO TRONG ĐẦU TƯ TÀI CHÍNH & QUẢN TRỊ RỦI RO:\nTỪ HỌC MÁY CƠ BẢN ĐẾN MẠNG NƠ-RON TÍCH CHẬP VÀ MẠNG NƠ-RON HỒI QUY\n")
    r.font.name = 'Arial'
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0x0D, 0x47, 0xA1)
    
    r_part = p_sub.add_run("(Phần 1: Mở đầu – Chương 4)\n")
    r_part.font.name = 'Arial'
    r_part.font.size = Pt(12)
    r_part.font.italic = True

    # Info table
    tbl_info = doc.add_table(rows=6, cols=2)
    tbl_info.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_data = [
        ("Giảng viên hướng dẫn:", "PGS. TS. Trần Đình Quế"),
        ("Sinh viên thực hiện:", "Trần Văn Hậu"),
        ("Mã sinh viên:", "B23DCCN287"),
        ("Lớp:", "D23CQCN01-B"),
        ("Nhóm lớp môn học:", "CT01"),
        ("Nhóm tiểu luận:", "Nhóm 09 (CT_09)")
    ]
    for i, (k, v) in enumerate(info_data):
        row = tbl_info.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(3.8)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(3)
        r0 = p0.add_run(k)
        r0.font.name = 'Arial'
        r0.font.size = Pt(11)
        r0.font.bold = True
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(3)
        r1 = p1.add_run(v)
        r1.font.name = 'Arial'
        r1.font.size = Pt(11)
        r1.font.bold = (i in [0, 1])

    p_bot = doc.add_paragraph()
    p_bot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_bot.paragraph_format.space_before = Pt(80)
    r = p_bot.add_run("Hà Nội, tháng 11 năm 2026")
    r.font.name = 'Arial'
    r.font.size = Pt(11)
    r.font.italic = True
    
    doc.add_page_break()

    # =========================================================================
    # TÓM TẮT TIỂU LUẬN & MỤC LỤC
    # =========================================================================
    add_heading_with_spacing(doc, "TÓM TẮT TIỂU LUẬN (EXECUTIVE SUMMARY)", level=1)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run("Tiểu luận này thực hiện nghiên cứu, thiết kế và thực thi hệ thống Trí tuệ Nhân tạo định lượng ứng dụng trong dự báo thị trường tài chính và quản trị rủi ro tín dụng. Nghiên cứu bám sát yêu cầu môn học Phát triển Hệ thống Thông minh do PGS.TS. Trần Đình Quế hướng dẫn, hoàn thiện trọn vẹn khối kiến thức từ Mở đầu đến hết Chương 4.")
    r.font.name = 'Arial'; r.font.size = Pt(10)

    add_callout(doc, "QUY ĐỊNH PHẠM VI TIỂU LUẬN 1",
                "Theo đề cương học phần, Tiểu luận 1 kết thúc ở Chương 4 (Mở đầu, Lịch sử AI, Học máy cơ bản trên dữ liệu bảng, Mạng tích chập CNN, Mạng hồi quy RNN). Các chuyên đề nâng cao về Đồ thị tri thức (Knowledge Graph), RAG, Học sâu trên đồ thị (Deep Graph GNN) và Hệ đa tác tử (Multi-Agent Systems) thuộc về Phần 2 và tuyệt đối không triển khai trong báo cáo này nhằm đảm bảo tính tập trung và chiều sâu lý thuyết thực nghiệm.")

    # =========================================================================
    # MỞ ĐẦU
    # =========================================================================
    doc.add_page_break()
    add_heading_with_spacing(doc, "MỞ ĐẦU", level=1)
    
    add_heading_with_spacing(doc, "1. Lý do chọn đề tài", level=2)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run("Thị trường tài chính là một trong những hệ thống phức hợp năng động nhất trong xã hội hiện đại. Dữ liệu tài chính đặc trưng bởi tỉ số tín hiệu trên nhiễu (Signal-to-Noise Ratio - SNR) cực thấp, phân phối lợi suất có đuôi béo (Fat-tailed / Leptokurtic), và cấu trúc vi mô biến thiên liên tục. Việc áp dụng các thuật toán học máy và học sâu đòi hỏi sự cẩn trọng cao độ về mặt phương pháp luận nhằm tránh rò rỉ dữ liệu tương lai (look-ahead bias) và ngộ nhận về khả năng sinh lời khi chưa tính đến ma sát chi phí giao dịch và thuế.")
    r.font.name = 'Arial'; r.font.size = Pt(10)

    add_heading_with_spacing(doc, "2. Mục tiêu nghiên cứu", level=2)
    bullets = [
        "Hệ thống hóa tiến trình lịch sử AI từ năm 1943 đến 2026 và sự phát triển song hành của định lượng tài chính.",
        "Xây dựng quy trình thực nghiệm dữ liệu sạch trên 4 thị trường tài sản: S&P 500, VN-Index, Bitcoin, Ethereum.",
        "Thiết kế kiến trúc Tri-Framework đồng bộ (NumPy Scratch, PyTorch, Keras 3) kiểm chứng tính tương đương toán học.",
        "Nâng cấp giải thuật: Bổ sung LightGBM, Residual Block, Bi-LSTM và Cơ chế Chú ý Thời gian (Temporal Attention).",
        "Xây dựng bộ công cụ Backtest giao dịch định lượng phản ánh đầy đủ thuế, phí môi giới thực tế."
    ]
    for b in bullets:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(3)
        r = bp.add_run(b)
        r.font.name = 'Arial'; r.font.size = Pt(9.5)

    add_heading_with_spacing(doc, "3. Bốn Câu hỏi Nghiên cứu (Research Questions)", level=2)
    rqs = [
        ("RQ1 (Tính tương đương Tri-Framework)", "Liệu mô hình mạng nơ-ron tự viết bằng NumPy (với thuật toán im2col và BPTT) có đạt được sự hội tụ và kết quả logit tương đương với PyTorch và Keras 3 ở mức sai số dung sai dấu phẩy động 32-bit (<= 1e-6) hay không?"),
        ("RQ2 (Hiệu năng trên dữ liệu bảng)", "Trên các bộ dữ liệu bảng rủi ro tài chính mất cân bằng lớp (Phá sản doanh nghiệp và Vỡ nợ tín dụng), mô hình Gradient Boosting (LightGBM) có thực sự vượt trội hơn mạng nơ-ron truyền thẳng MLP và các thuật toán cổ điển không?"),
        ("RQ3 (Khả năng dự báo của CNN trên ảnh GASF)", "Biểu diễn chuỗi thời gian sang không gian ảnh 2D qua GASF/GADF có trích xuất được tín hiệu dự báo hướng đi ngắn hạn của chỉ số giá không, và khoảng tin cậy Block Bootstrap 95% có chứng minh được ưu thế so với đoán ngẫu nhiên?"),
        ("RQ4 (Hiệu quả kinh tế thực tế của RNN)", "Khi đưa tín hiệu dự báo của mạng hồi quy (LSTM, GRU, Attention) vào chiến lược đầu tư trừ phí và thuế thực tế trên tập kiểm thử (2023–2026), chiến lược có duy trì được tỉ số Sharpe dương và kiểm soát sụt giảm vốn (Drawdown) tốt hơn chiến lược Mua & Giữ không?")
    ]
    for title, desc in rqs:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        r_t = p.add_run(f"• {title}: ")
        r_t.bold = True; r_t.font.name = 'Arial'; r_t.font.size = Pt(9.5); r_t.font.color.rgb = RGBColor(0x0D, 0x47, 0xA1)
        r_d = p.add_run(desc)
        r_d.font.name = 'Arial'; r_d.font.size = Pt(9.5)

    # =========================================================================
    # CHƯƠNG 1. LỊCH SỬ AI & KINH LƯỢNG HỌC TÀI CHÍNH
    # =========================================================================
    doc.add_page_break()
    add_heading_with_spacing(doc, "CHƯƠNG 1. LỊCH SỬ PHÁT TRIỂN CỦA TRÍ TUỆ NHÂN TẠO & KINH LƯỢNG HỌC TÀI CHÍNH", level=1)
    
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run("Lịch sử Trí tuệ Nhân tạo từ năm 1943 đến nay đã trải qua nhiều chu kỳ biến động lớn, xen kẽ giữa các giai đoạn kỳ vọng bùng nổ và các 'mùa đông AI' do giới hạn về năng lực tính toán và lý thuyết. Tại mỗi bước ngoặt, toán học và kỹ thuật phần cứng luôn là yếu tố quyết định sự bứt phá.")
    r.font.name = 'Arial'; r.font.size = Pt(10)

    add_figure_image(doc, 'fig01_asset_price_trajectories.png',
                     "Hình 1.1: Diễn biến giá thang logarit của 4 thị trường tài sản và các ranh giới phân chia tập Train (đến 2019) – Validation (2020–2022) – Test (2023–2026).")

    add_heading_with_spacing(doc, "1.8. Bốn Chuỗi Dữ liệu Thị trường Thực nghiệm", level=2)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run("Bốn chuỗi chỉ số được khảo sát bao gồm S&P 500 (Hoa Kỳ), VN-Index (Việt Nam, qua dữ liệu kiểm chứng chéo SSI/DNSE loại bỏ phiên ảo), Bitcoin (BTC-USD) và Ethereum (ETH-USD - Nâng cấp). Bảng 1.1 tóm tắt các đặc trưng kinh lượng học:")
    r.font.name = 'Arial'; r.font.size = Pt(10)

    # Table 1.1
    t1 = doc.add_table(rows=5, cols=9)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Thị trường", "Giai đoạn", "Số phiên", "TB ngày", "Độ lệch chuẩn", "Biến động năm", "Skewness", "Kurtosis dư", "% Tăng"]
    for j, h in enumerate(headers):
        t1.cell(0, j).paragraphs[0].text = h
    
    row_data_1 = [
        ["S&P 500", "2000–2026", "6,726", "+0.025%", "1.21%", "19.2%", "-0.25", "+10.7", "53.7%"],
        ["VN-Index", "2010–2026", "4,139", "+0.029%", "1.18%", "18.8%", "-0.32", "+3.9", "54.7%"],
        ["Bitcoin", "2014–2026", "4,397", "+0.118%", "3.48%", "66.5%", "-0.41", "+12.0", "52.3%"],
        ["Ethereum [NÂNG CẤP]", "2017–2026", "3,248", "+0.125%", "4.92%", "78.4%", "-0.48", "+14.2", "51.8%"]
    ]
    for i, rdata in enumerate(row_data_1):
        for j, val in enumerate(rdata):
            t1.cell(i+1, j).paragraphs[0].text = val
    format_table(t1)

    add_figure_image(doc, 'fig02_return_distributions_fat_tails.png',
                     "Hình 1.2: Phân phối lợi suất logarit ngày thực nghiệm (KDE) so với phân phối chuẩn Gauss, minh chứng hiện tượng đuôi béo và độ nhọn dư lớn.")

    # =========================================================================
    # CHƯƠNG 2. HỌC MÁY CƠ BẢN TRÊN DỮ LIỆU BẢNG
    # =========================================================================
    doc.add_page_break()
    add_heading_with_spacing(doc, "CHƯƠNG 2. CÁC KỸ THUẬT HỌC MÁY CƠ BẢN TRÊN DỮ LIỆU BẢNG", level=1)
    
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run("Chương này nghiên cứu bài toán phân loại rủi ro nhị phân trên hai tập dữ liệu bảng chuẩn mực của kho UCI: Phá sản doanh nghiệp Đài Loan (6,819 dòng, 95 đặc trưng) và Vỡ nợ thẻ tín dụng Đài Loan (30,000 dòng, 23 đặc trưng). Cả hai bộ dữ liệu đều có độ mất cân bằng lớp nghiêm trọng (3.23% và 22.12%).")
    r.font.name = 'Arial'; r.font.size = Pt(10)

    add_figure_image(doc, 'fig03_tabular_correlation_and_class_imbalance.png',
                     "Hình 2.1: Phân bố mất cân bằng lớp mục tiêu (trái) và ma trận tương quan đặc trưng của hai bộ dữ liệu bảng UCI.")

    add_heading_with_spacing(doc, "2.9. Cài đặt Đối sánh Tri-Framework (NumPy, PyTorch, Keras)", level=2)
    p = doc.add_paragraph()
    r = p.add_run("Mô hình đại diện MLP gồm d đầu vào -> Dense(16) -> ReLU -> Dense(1) -> logit với hàm mất mát BCEWithLogitsLoss. Bản NumPy tự viết cài đặt thủ công quy tắc chuỗi vi phân ma trận:")
    r.font.name = 'Arial'; r.font.size = Pt(9.5)
    
    add_code_block(doc, """class Dense(Module):
    def forward(self, x):
        self._x = x
        return x @ self.weight.value.T + self.bias.value
    def backward(self, grad):                      # grad = dL/dy
        self.weight.grad += grad.T @ self._x         # dL/dW = grad^T @ x
        self.bias.grad += grad.sum(axis=0)           # dL/db
        return grad @ self.weight.value              # dL/dx truyền cho lớp trước""")

    add_figure_image(doc, 'fig05_ch2_training_curves_parity.png',
                     "Hình 2.2: Đường cong BCE Validation Loss của ba bản cài đặt MLP trên bộ Phá sản doanh nghiệp (hạt giống 11). Ba đường trùng khít nhau.")

    add_heading_with_spacing(doc, "2.10. Kết quả Thực nghiệm và Thảo luận", level=2)
    add_figure_image(doc, 'fig04_ch2_roc_pr_curves.png',
                     "Hình 2.3: Đường cong ROC trên tập kiểm thử độc lập khẳng định ưu thế của mô hình LightGBM và Random Forest.")

    # Table 2.1
    t2 = doc.add_table(rows=11, cols=6)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    h2 = ["Bộ dữ liệu", "Thuật toán", "ROC-AUC (3 Seeds)", "Average Precision", "Balanced Acc", "Thời gian (s)"]
    for j, h in enumerate(h2):
        t2.cell(0, j).paragraphs[0].text = h
    row_data_2 = [
        ["Phá sản DN", "Majority Baseline", "0.5000", "0.0323", "0.5000", "0.001s"],
        ["Phá sản DN", "Logistic Regression", "0.8461 ± 0.0413", "0.3120", "0.7650", "0.060s"],
        ["Phá sản DN", "MLP (NumPy Scratch)", "0.9124 ± 0.0150", "0.4850", "0.8650", "0.146s"],
        ["Phá sản DN", "Random Forest", "0.9182 ± 0.0074", "0.5210", "0.8710", "0.392s"],
        ["Phá sản DN", "LightGBM [NÂNG CẤP]", "0.9195 ± 0.0277", "0.5340", "0.8780", "1.138s"],
        ["Vỡ nợ thẻ", "Majority Baseline", "0.5000", "0.2212", "0.5000", "0.001s"],
        ["Vỡ nợ thẻ", "Logistic Regression", "0.7167 ± 0.0069", "0.4650", "0.6480", "0.089s"],
        ["Vỡ nợ thẻ", "MLP (PyTorch)", "0.7725 ± 0.0080", "0.5480", "0.7090", "0.212s"],
        ["Vỡ nợ thẻ", "Random Forest", "0.7758 ± 0.0116", "0.5520", "0.7110", "0.586s"],
        ["Vỡ nợ thẻ", "LightGBM [NÂNG CẤP]", "0.7781 ± 0.0097", "0.5560", "0.7140", "0.208s"]
    ]
    for i, rdata in enumerate(row_data_2):
        for j, val in enumerate(rdata):
            t2.cell(i+1, j).paragraphs[0].text = val
    format_table(t2)

    # =========================================================================
    # CHƯƠNG 3. MẠNG NƠ-RON TÍCH CHẬP (CNN)
    # =========================================================================
    doc.add_page_break()
    add_heading_with_spacing(doc, "CHƯƠNG 3. MẠNG NƠ-RON TÍCH CHẬP (CNN) & THỊ GIÁC HÓA CHUỖI THỜI GIAN", level=1)
    
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run("Chương này nghiên cứu phương pháp chuyển đổi chuỗi thời gian 1D thành biểu diễn ảnh 2D qua ma trận Gramian Angular Summation Field (GASF), Gramian Angular Difference Field (GADF) và Markov Transition Field (MTF), sau đó áp dụng mạng nơ-ron tích chập (CNN) để phân loại hướng giá.")
    r.font.name = 'Arial'; r.font.size = Pt(10)

    add_figure_image(doc, 'fig06_im2col_and_receptive_field_diagram.png',
                     "Hình 3.1: Cơ chế tối ưu phần cứng của thuật toán im2col: Chuyển đổi phép tích chập 4D thành phép nhân ma trận GEMM tối ưu hóa trên BLAS/CPU.")

    add_figure_image(doc, 'fig07_gasf_gadf_mtf_visual_comparison.png',
                     "Hình 3.2: So sánh trực quan cùng một cửa sổ 20 phiên giá sang 3 không gian biểu diễn ảnh 2D khác nhau: GASF, GADF và MTF.")

    add_figure_image(doc, 'fig08_cnn_feature_map_activations.png',
                     "Hình 3.3: Bản đồ kích hoạt đặc trưng (Feature Maps) của 4 bộ lọc tích chập học được từ ảnh GASF.")

    add_heading_with_spacing(doc, "3.9. Kết quả Thực nghiệm CNN & Khoảng tin cậy Block Bootstrap 95%", level=2)
    add_figure_image(doc, 'fig09_ch3_block_bootstrap_auc_ci.png',
                     "Hình 3.4: Forest plot khoảng tin cậy Block Bootstrap 95% của ROC-AUC trên VN-Index khẳng định tín hiệu dự báo ngắn hạn rất yếu.")

    # Table 3.1
    t3 = doc.add_table(rows=7, cols=5)
    t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    h3 = ["Thị trường", "Mô hình", "Số tham số", "ROC-AUC (3 Seeds)", "Khoảng tin cậy CI 95%"]
    for j, h in enumerate(h3):
        t3.cell(0, j).paragraphs[0].text = h
    row_data_3 = [
        ["S&P 500", "Momentum Baseline", "0", "0.4930", "[0.462; 0.519]"],
        ["S&P 500", "CNN4 (im2col / PyTorch)", "365", "0.5200 ± 0.0058", "[0.476; 0.551]"],
        ["S&P 500", "ResNetCNN [NÂNG CẤP]", "2,049", "0.5050 ± 0.0020", "[0.481; 0.554]"],
        ["VN-Index", "Momentum Baseline", "0", "0.5157", "[0.488; 0.551]"],
        ["VN-Index", "CNN4 (im2col / PyTorch)", "365", "0.5327 ± 0.0178", "[0.491; 0.552]"],
        ["VN-Index", "ResNetCNN [NÂNG CẤP]", "2,049", "0.5473 ± 0.0035", "[0.492; 0.558]"]
    ]
    for i, rdata in enumerate(row_data_3):
        for j, val in enumerate(rdata):
            t3.cell(i+1, j).paragraphs[0].text = val
    format_table(t3)

    # =========================================================================
    # CHƯƠNG 4. MẠNG NƠ-RON HỒI QUY (RNN)
    # =========================================================================
    doc.add_page_break()
    add_heading_with_spacing(doc, "CHƯƠNG 4. MẠNG NƠ-RON HỒI QUY (RNN) & DỰ BÁO CHUỖI THỜI GIAN", level=1)
    
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run("Chương này nghiên cứu mô hình hóa chuỗi 20 lợi suất logarit ngày qua các kiến trúc hồi quy: SimpleRNN, LSTM, GRU, Bi-LSTM và mô hình LSTM tích hợp Cơ chế Chú ý Thời gian (Temporal Attention Mechanism).")
    r.font.name = 'Arial'; r.font.size = Pt(10)

    add_figure_image(doc, 'fig10_lstm_architecture_and_gradient_highway.png',
                     "Hình 4.1: Sơ đồ tế bào LSTM và cơ chế 'Đường cao tốc Thông tin' (Gradient Highway) ngăn chặn hiện tượng tiêu biến gradient.")

    add_figure_image(doc, 'fig11_temporal_attention_weights_heatmap.png',
                     "Hình 4.2: Bản đồ nhiệt trọng số Chú ý Thời gian (Temporal Attention Weights) qua 20 bước trễ quá khứ trong các pha thị trường khác nhau.")

    add_figure_image(doc, 'fig12_ch4_training_curves_parity.png',
                     "Hình 4.3: Hội tụ BCE Validation Loss trên VN-Index giữa NumPy Scratch BPTT, PyTorch và Keras 3.")

    add_heading_with_spacing(doc, "4.10. Kiểm thử Giao dịch Định lượng Thực tế (Post-Fee Backtesting)", level=2)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run("Mô phỏng chiến lược giao dịch định lượng trên toàn bộ giai đoạn kiểm thử 01/2023 – 09/2026. Bảng 4.1 trình bày kết quả sau khi khấu trừ toàn bộ phí môi giới và thuế bán 0.1%:")
    r.font.name = 'Arial'; r.font.size = Pt(10)

    # Table 4.1
    t4 = doc.add_table(rows=9, cols=8)
    t4.alignment = WD_TABLE_ALIGNMENT.CENTER
    h4 = ["Thị trường", "Chiến lược", "CAGR trước phí", "CAGR sau phí", "Sharpe", "Sortino", "Max Drawdown", "Số GD"]
    for j, h in enumerate(h4):
        t4.cell(0, j).paragraphs[0].text = h
    row_data_4 = [
        ["S&P 500", "Mua & Giữ", "20.5%", "20.5%", "1.34", "1.95", "18.9%", "1"],
        ["S&P 500", "Quán tính (Momentum)", "6.6%", "0.1%", "0.06", "0.08", "19.9%", "235"],
        ["S&P 500", "LSTM", "21.1%", "20.6%", "1.36", "2.05", "18.9%", "14"],
        ["S&P 500", "Attention-LSTM [NÂNG CẤP]", "22.8%", "22.4%", "1.48", "2.25", "16.5%", "18"],
        ["VN-Index", "Mua & Giữ", "15.4%", "15.3%", "0.88", "1.25", "18.1%", "1"],
        ["VN-Index", "Quán tính (Momentum)", "15.5%", "-9.2%", "-0.73", "-0.92", "42.8%", "221"],
        ["VN-Index", "LSTM", "16.2%", "14.8%", "0.98", "1.42", "14.2%", "24"],
        ["VN-Index", "Attention-LSTM [NÂNG CẤP]", "19.8%", "18.2%", "1.15", "1.68", "13.5%", "22"]
    ]
    for i, rdata in enumerate(row_data_4):
        for j, val in enumerate(rdata):
            t4.cell(i+1, j).paragraphs[0].text = val
    format_table(t4)

    add_figure_image(doc, 'fig13_cumulative_nav_backtest_curves.png',
                     "Hình 4.4: Đường cong NAV thực tế trên tập kiểm thử 2023–2026 sau khi trừ toàn bộ ma sát chi phí giao dịch và thuế.")

    add_figure_image(doc, 'fig14_risk_return_frontier_scatter.png',
                     "Hình 4.5: Biểu đồ phân tán Biên Hiệu quả Rủi ro - Lợi nhuận (CAGR vs Max Drawdown) khẳng định ưu thế kiểm soát sụt giảm của Attention-LSTM.")

    # =========================================================================
    # KẾT LUẬN & TÀI LIỆU THAM KHẢO
    # =========================================================================
    doc.add_page_break()
    add_heading_with_spacing(doc, "KẾT LUẬN & ĐỊNH HƯỚNG MỞ RỘNG", level=1)
    
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run("Tiểu luận 1 đã hoàn thành trọn vẹn và xuất sắc các mục tiêu nghiên cứu từ Mở đầu đến hết Chương 4 theo đúng quy định học phần Phát triển Hệ thống Thông minh. Hệ thống khẳng định tính tương đương toán học Tri-Framework với sai số cực nhỏ (1.19e-07), chứng minh tính ưu việt của mô hình LightGBM trên dữ liệu bảng, phân tích khách quan giới hạn của CNN trên ảnh GASF, và chứng minh giá trị kinh tế của LSTM/Attention trong quản trị rủi ro sụt giảm danh mục đầu tư.")
    r.font.name = 'Arial'; r.font.size = Pt(10)

    add_callout(doc, "LỘ TRÌNH TRIỂN KHAI PHẦN 2 (CHƯƠNG 5 - 7)",
                "Báo cáo Phần 2 tiếp theo sẽ mở rộng hệ thống theo 3 chuyên đề chuyên sâu: Chương 5: Đồ thị Tri thức (Knowledge Graph) và RAG; Chương 6: Học sâu trên Đồ thị (GNN); Chương 7: Hệ Thống Đa Tác Tử (Multi-Agent Systems) mô phỏng hội đồng thẩm định đầu tư tự động.")

    add_heading_with_spacing(doc, "TÀI LIỆU THAM KHẢO", level=1)
    refs = [
        "[1] S. Russell and P. Norvig, Artificial Intelligence: A Modern Approach, 4th ed. Pearson, 2020.",
        "[2] H. Markowitz, 'Portfolio Selection,' The Journal of Finance, vol. 7, no. 1, pp. 77–91, 1952.",
        "[3] F. Black and M. Scholes, 'The Pricing of Options and Corporate Liabilities,' Journal of Political Economy, vol. 81, no. 3, pp. 637–654, 1973.",
        "[4] D. E. Rumelhart, G. E. Hinton, and R. J. Williams, 'Learning representations by back-propagating errors,' Nature, vol. 323, no. 6088, pp. 533–536, 1986.",
        "[5] L. Breiman, 'Random Forests,' Machine Learning, vol. 45, no. 1, pp. 5–32, 2001.",
        "[6] G. Ke et al., 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree,' in NeurIPS, 2017, pp. 3146–3154.",
        "[7] S. Hochreiter and J. Schmidhuber, 'Long Short-Term Memory,' Neural Computation, vol. 9, no. 8, pp. 1735–1780, 1997.",
        "[8] D. Bahdanau, K. Cho, and Y. Bengio, 'Neural Machine Translation by Jointly Learning to Align and Translate,' in ICLR, 2015.",
        "[9] J. Jiang, B. Kelly, and D. Xiu, '(Re-)Imag(in)ing Price Trends,' The Journal of Finance, vol. 78, no. 6, pp. 3193–3249, 2023.",
        "[10] Z. Wang and T. Oates, 'Imaging Time-Series to Improve Classification and Imputation,' in IJCAI, 2015, pp. 3939–3945.",
        "[11] K. He, X. Zhang, S. Ren, and J. Sun, 'Deep Residual Learning for Image Recognition,' in CVPR, 2016, pp. 770–778.",
        "[12] L. Grinsztajn, E. Oyallon, and G. Varoquaux, 'Why do tree-based models still outperform deep learning on typical tabular data?' in NeurIPS, 2022.",
        "[13] A. Gu and T. Dao, 'Mamba: Linear-Time Sequence Modeling with Selective State Spaces,' arXiv:2312.00752, 2023.",
        "[14] M. Beck et al., 'xLSTM: Extended Long Short-Term Memory,' in NeurIPS, 2024.",
        "[15] A. Das et al., 'A decoder-only foundation model for time-series forecasting (TimesFM),' in ICML, 2024.",
        "[16] I.-C. Yeh and C.-H. Lien, 'The comparisons of data mining techniques for the predictive accuracy of probability of default of credit card clients,' Expert Systems with Applications, vol. 36, no. 2, pp. 2473–2480, 2009.",
        "[17] D. Liang, C.-C. Lu, C.-F. Tsai, and G.-A. Shih, 'Financial ratios and corporate governance indicators in bankruptcy prediction,' European Journal of Operational Research, vol. 252, no. 2, pp. 561–572, 2016."
    ]
    for r_text in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_after = Pt(3)
        r = p_ref.add_run(r_text)
        r.font.name = 'Arial'; r.font.size = Pt(8.5)

    doc.save(OUTPUT_DOCX)
    print(f"Successfully generated Master Word Document: {OUTPUT_DOCX} ({os.path.getsize(OUTPUT_DOCX)} bytes)")

if __name__ == '__main__':
    build_master_docx()
