"""
Master Monograph Generator (Markdown and Word Docx)
Generates:
1. tieuluan2/BAO_CAO_TIEU_LUAN_2_NANG_CAP.md
2. tieuluan2/Bao_Cao_Tieu_Luan_2_Nang_Cap.docx

Student: Tran Van Hau (B23DCCN287) - D23CTPM01 - PTIT
Supervisor: PGS.TS. Tran Dinh Que
"""

import os
import sys

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("tieuluan2"))
sys.stdout.reconfigure(encoding='utf-8')

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

from report_sections.metadata_tables import (
    FRONT_MATTER, EXECUTIVE_SUMMARY_VI, EXECUTIVE_SUMMARY_EN,
    ABBREVIATIONS, TABLES_DATA, FIGURES_CATALOG, BIBLIOGRAPHY
)
from report_sections.code_snippets import CODE_LISTINGS
from report_sections.chap1 import CHAP1_DATA
from report_sections.chap2 import CHAP2_DATA
from report_sections.chap3 import CHAP3_DATA
from report_sections.chap4 import CHAP4_DATA
from report_sections.chap5 import CHAP5_DATA
from report_sections.chap6 import CHAP6_DATA
from report_sections.chap7 import CHAP7_DATA

ALL_CHAPTERS = [
    CHAP1_DATA, CHAP2_DATA, CHAP3_DATA, CHAP4_DATA, CHAP5_DATA, CHAP6_DATA, CHAP7_DATA
]

# Word styling helpers
def set_cell_background(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=140, bottom=140, left=180, right=180):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_code_block_docx(doc, code_text, caption):
    p_cap = doc.add_paragraph()
    p_cap.paragraph_format.space_before = Pt(8)
    p_cap.paragraph_format.space_after = Pt(3)
    run_cap = p_cap.add_run(caption)
    run_cap.bold = True
    run_cap.font.name = "Times New Roman"
    run_cap.font.size = Pt(10)
    run_cap.font.color.rgb = RGBColor(30, 58, 138)

    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=120, bottom=120, left=160, right=160)

    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="none"/><w:left w:val="single" w:sz="24" w:space="0" w:color="1D4ED8"/><w:bottom w:val="none"/><w:right w:val="none"/></w:tcBorders>')
    tcPr.append(borders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(code_text.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_callout_box_docx(doc, text, title="LƯU Ý QUAN TRỌNG / KHUYẾN CÁO LÂM SÀNG", alert_type="danger"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)

    bg_color = "FEF2F2" if alert_type == "danger" else ("EFF6FF" if alert_type == "info" else "FEFCE8")
    border_color = "DC2626" if alert_type == "danger" else ("2563EB" if alert_type == "info" else "D97706")
    title_color = RGBColor(185, 28, 28) if alert_type == "danger" else (RGBColor(29, 78, 216) if alert_type == "info" else RGBColor(180, 83, 9))
    text_color = RGBColor(127, 29, 29) if alert_type == "danger" else (RGBColor(30, 58, 138) if alert_type == "info" else RGBColor(120, 53, 15))

    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)

    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="none"/><w:left w:val="single" w:sz="28" w:space="0" w:color="{border_color}"/><w:bottom w:val="none"/><w:right w:val="none"/></w:tcBorders>')
    tcPr.append(borders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    run_t = p.add_run(f"★ {title}\n")
    run_t.bold = True
    run_t.font.name = "Times New Roman"
    run_t.font.size = Pt(10.5)
    run_t.font.color.rgb = title_color

    run_b = p.add_run(text)
    run_b.font.name = "Times New Roman"
    run_b.font.size = Pt(10)
    run_b.font.color.rgb = text_color
    run_b.font.italic = True

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def add_image_figure_docx(doc, img_path, caption):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(10)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(6.0))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(10)
        run_cap = p_cap.add_run(caption)
        run_cap.italic = True
        run_cap.font.name = "Times New Roman"
        run_cap.font.size = Pt(9.5)
        run_cap.font.color.rgb = RGBColor(71, 85, 105)
    else:
        print(f"[Warning] Image not found: {img_path}")

def format_table_docx(doc, table_info):
    title = table_info["title"]
    headers = table_info["headers"]
    widths = table_info["widths"]
    rows = table_info["rows"]

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(10)
    p_title.paragraph_format.space_after = Pt(4)
    run_t = p_title.add_run(title)
    run_t.bold = True
    run_t.font.name = "Times New Roman"
    run_t.font.size = Pt(10)
    run_t.font.color.rgb = RGBColor(30, 58, 138)

    tbl = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = tbl.rows[0].cells
    for i, h_text in enumerate(headers):
        hdr_cells[i].text = h_text
        set_cell_background(hdr_cells[i], "1E3A8A")
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=140, right=140)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.bold = True
            run.font.name = "Times New Roman"
            run.font.size = Pt(9.5)
            run.font.color.rgb = RGBColor(255, 255, 255)

    for r_idx, r_data in enumerate(rows):
        row_cells = tbl.rows[r_idx + 1].cells
        bg_col = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, cell_val in enumerate(r_data):
            row_cells[c_idx].text = str(cell_val)
            set_cell_background(row_cells[c_idx], bg_col)
            set_cell_margins(row_cells[c_idx], top=90, bottom=90, left=120, right=120)
            p = row_cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 or c_idx == len(r_data) - 1 else WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(9)
                run.font.color.rgb = RGBColor(30, 41, 59)

    for row in tbl.rows:
        for i, w in enumerate(widths):
            row.cells[i].width = Inches(w)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)


def generate_markdown():
    print("Generating comprehensive Markdown report...")
    lines = []
    lines.append(f"# {FRONT_MATTER['institution']}")
    lines.append(f"## {FRONT_MATTER['faculty']}")
    lines.append(f"### {FRONT_MATTER['course']}\n")
    lines.append(f"# {FRONT_MATTER['title']}\n")
    lines.append(f"### {FRONT_MATTER['subtitle']}\n")
    lines.append(f"**Sinh viên thực hiện**: **{FRONT_MATTER['student_name']}**  ")
    lines.append(f"**Mã sinh viên**: **{FRONT_MATTER['student_id']}**  ")
    lines.append(f"**Lớp học phần**: **{FRONT_MATTER['class_name']}** ({FRONT_MATTER['group_name']})  ")
    lines.append(f"**Giảng viên hướng dẫn**: **{FRONT_MATTER['supervisor']}**  ")
    lines.append(f"**Học kỳ**: {FRONT_MATTER['academic_year']}  ")
    lines.append(f"**Địa điểm & Thời gian**: {FRONT_MATTER['location_year']}\n")
    lines.append(f"**Tệp tin Báo cáo Word Hoàn chỉnh**: [`tieuluan2/Bao_Cao_Tieu_Luan_2_Nang_Cap.docx`](file:///c:/code/A2_CT_hautv.287/tieuluan2/Bao_Cao_Tieu_Luan_2_Nang_Cap.docx) (Tích hợp đầy đủ 14 hình vẽ 300 DPI, các bảng chuẩn hóa, hộp cảnh báo và mã nguồn)\n")
    lines.append("---\n")

    lines.append("## MỤC LỤC TỔNG QUAN")
    lines.append("1. [TỔNG QUAN VÀ TÓM TẮT ĐỀ TÀI (EXECUTIVE SUMMARY)](#tổng-quan-và-tóm-tắt-đề-tài-executive-summary)")
    lines.append("2. [DANH MỤC TỪ VIẾT TẮT](#danh-mục-từ-viết-tắt)")
    lines.append("3. [CHƯƠNG 1: MỞ ĐẦU VỀ KNOWLEDGE GRAPH VÀ RAG](#chương-1-mở-đầu-về-knowledge-graph-và-rag)")
    lines.append("4. [CHƯƠNG 2: XÂY DỰNG ĐỒ THỊ TRI THỨC Y TẾ VÀ TÀI CHÍNH](#chương-2-xây-dựng-đồ-thị-tri-thức-y-tế-và-tài-chính)")
    lines.append("5. [CHƯƠNG 3: KỸ THUẬT RETRIEVAL-AUGMENTED GENERATION (RAG)](#chương-3-kỹ-thuật-retrieval-augmented-generation-rag)")
    lines.append("6. [CHƯƠNG 4: TRI THỨC Y TẾ & HỌC SÂU CHẨN ĐOÁN ĐÁI THÁO ĐƯỜNG TYPE 2](#chương-4-tri-thức-y-tế--học-sâu-chẩn-đoán-đái-tháo-đường-type-2)")
    lines.append("7. [CHƯƠNG 5: TRI THỨC TÀI CHÍNH VĨ MÔ & HỌC SÂU CHUỖI THỜI GIAN BILSTM](#chương-5-tri-thức-tài-chính-vĩ-mô--học-sâu-chuỗi-thời-gian-bilstm)")
    lines.append("8. [CHƯƠNG 6: ĐỘNG CƠ LẬP LUẬN REACT, KIỂM CHỨNG GROUNDED VERIFIER & HỆ THỐNG WEB](#chương-6-động-cơ-lập-luận-react-kiểm-chứng-grounded-verifier--hệ-thống-web)")
    lines.append("9. [CHƯƠNG 7: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN](#chương-7-kết-luận-và-hướng-phát-triển)")
    lines.append("10. [TÀI LIỆU THAM KHẢO](#tài-liệu-tham-khảo)\n")
    lines.append("---\n")

    lines.append("## TỔNG QUAN VÀ TÓM TẮT ĐỀ TÀI (EXECUTIVE SUMMARY)\n")
    lines.append("### Tóm tắt Tiếng Việt\n" + EXECUTIVE_SUMMARY_VI.strip() + "\n")
    lines.append("### Abstract in English\n" + EXECUTIVE_SUMMARY_EN.strip() + "\n")
    lines.append("---\n")

    lines.append("## DANH MỤC TỪ VIẾT TẮT\n")
    lines.append("| Ký hiệu viết tắt | Thuật ngữ Tiếng Anh | Diễn giải Tiếng Việt |")
    lines.append("| :--- | :--- | :--- |")
    for abbr, full_en, full_vi in ABBREVIATIONS:
        lines.append(f"| **{abbr}** | {full_en} | {full_vi} |")
    lines.append("\n---\n")

    # Add Chapters
    for chap in ALL_CHAPTERS:
        c_num = chap["chapter_num"]
        lines.append(f"# {chap['chapter_title']}\n")
        lines.append(f"*{chap['intro_text'].strip()}*\n")

        # Specific inserts per chapter
        if c_num == 1:
            lines.append("![Hình 1.1](file:///c:/code/A2_CT_hautv.287/tieuluan2/charts/h01_dual_domain_ecosystem.png)")
            lines.append("*Hình 1.1. Sơ đồ kiến trúc tổng thể 5 tầng của Hệ sinh thái Tri thức Đa miền Y tế và Tài chính Việt Nam.*\n")
            # Table 1.1
            t1 = TABLES_DATA["table_01_methods_comparison"]
            lines.append(f"### {t1['title']}\n")
            lines.append("| " + " | ".join(t1["headers"]) + " |")
            lines.append("| " + " | ".join([":---" for _ in t1["headers"]]) + " |")
            for row in t1["rows"]:
                lines.append("| " + " | ".join(row) + " |")
            lines.append("\n")

        elif c_num == 2:
            lines.append("![Hình 2.1](file:///c:/code/A2_CT_hautv.287/tieuluan2/charts/h02_diabetes_ontology_hierarchy.png)")
            lines.append("*Hình 2.1. Cây phân cấp 23 lớp bản thể học và mạng lưới 17 vị từ quan hệ lâm sàng trong VietnamDiabetesKG.*\n")
            # Table 2.1
            t2 = TABLES_DATA["table_03_diabetes_ontology"]
            lines.append(f"### {t2['title']}\n")
            lines.append("| " + " | ".join(t2["headers"]) + " |")
            lines.append("| " + " | ".join([":---" for _ in t2["headers"]]) + " |")
            for row in t2["rows"]:
                lines.append("| " + " | ".join(row) + " |")
            lines.append("\n")

            # Code Listings 2.1 & 2.2
            l21 = CODE_LISTINGS["listing_2_1"]
            lines.append(f"#### {l21['caption']}\n```python\n{l21['code']}\n```\n")
            l22 = CODE_LISTINGS["listing_2_2"]
            lines.append(f"#### {l22['caption']}\n```sparql\n{l22['code']}\n```\n")

            lines.append("![Hình 2.2](file:///c:/code/A2_CT_hautv.287/tieuluan2/charts/h03_finance_causal_network.png)")
            lines.append("*Hình 2.2. Đồ thị tri thức nhân quả có hướng có dấu VietnamFinanceKG mô tả chuỗi truyền dẫn Fed - DXY - USD/VND - SJC - VN30.*\n")
            lines.append("![Hình 2.3](file:///c:/code/A2_CT_hautv.287/tieuluan2/charts/h13_graphdb_vs_vectordb_radar.png)")
            lines.append("*Hình 2.3. Biểu đồ Radar 6 chiều so sánh đặc tính kỹ thuật giữa Graph Database và Vector Database.*\n")

        elif c_num == 3:
            lines.append("![Hình 3.1](file:///c:/code/A2_CT_hautv.287/tieuluan2/charts/h04_chunking_strategies_comparison.png)")
            lines.append("*Hình 3.1. So sánh trực quan 5 chiến lược phân mảnh văn bản.*\n")
            # Table 3.1
            t3 = TABLES_DATA["table_02_corpus_documents"]
            lines.append(f"### {t3['title']}\n")
            lines.append("| " + " | ".join(t3["headers"]) + " |")
            lines.append("| " + " | ".join([":---" for _ in t3["headers"]]) + " |")
            for row in t3["rows"]:
                lines.append("| " + " | ".join(row) + " |")
            lines.append("\n")

            # Table 3.2
            t4 = TABLES_DATA["table_04_rag_matrix_25"]
            lines.append(f"### {t4['title']}\n")
            lines.append("| " + " | ".join(t4["headers"]) + " |")
            lines.append("| " + " | ".join([":---" for _ in t4["headers"]]) + " |")
            for row in t4["rows"]:
                lines.append("| " + " | ".join(row) + " |")
            lines.append("\n")

            # Code Listings 3.1 & 3.2
            l31 = CODE_LISTINGS["listing_3_1"]
            lines.append(f"#### {l31['caption']}\n```python\n{l31['code']}\n```\n")
            l32 = CODE_LISTINGS["listing_3_2"]
            lines.append(f"#### {l32['caption']}\n```python\n{l32['code']}\n```\n")

            lines.append("![Hình 3.2](file:///c:/code/A2_CT_hautv.287/tieuluan2/charts/h05_rag_matrix_heatmap.png)")
            lines.append("*Hình 3.2. Biểu đồ nhiệt (Heatmap) thể hiện độ chính xác Hit@1 trên ma trận thực nghiệm 25 cấu hình RAG.*\n")
            lines.append("![Hình 3.3](file:///c:/code/A2_CT_hautv.287/tieuluan2/charts/h06_sparse_vs_dense_vs_hybrid_radar.png)")
            lines.append("*Hình 3.3. Biểu đồ Radar đa chiều đối sánh các bộ truy xuất.*\n")

        elif c_num == 4:
            # Table 4.1
            t5 = TABLES_DATA["table_05_diabetes_mlp_arch"]
            lines.append(f"### {t5['title']}\n")
            lines.append("| " + " | ".join(t5["headers"]) + " |")
            lines.append("| " + " | ".join([":---" for _ in t5["headers"]]) + " |")
            for row in t5["rows"]:
                lines.append("| " + " | ".join(row) + " |")
            lines.append("\n")

            # Code Listings 4.1 & 4.2
            l41 = CODE_LISTINGS["listing_4_1"]
            lines.append(f"#### {l41['caption']}\n```python\n{l41['code']}\n```\n")
            l42 = CODE_LISTINGS["listing_4_2"]
            lines.append(f"#### {l42['caption']}\n```python\n{l42['code']}\n```\n")

            lines.append("![Hình 4.1](file:///c:/code/A2_CT_hautv.287/tieuluan2/charts/h07_diabetes_mlp_learning_curves.png)")
            lines.append("*Hình 4.1. Đường cong huấn luyện của mạng PyTorch DiabetesMLP (Loss và ROC-AUC qua 60 epoch).*\n")
            lines.append("![Hình 4.2](file:///c:/code/A2_CT_hautv.287/tieuluan2/charts/h08_diabetes_confusion_matrix.png)")
            lines.append("*Hình 4.2. Ma trận nhầm lẫn (Confusion Matrix) trên tập kiểm thử 14.420 mẫu bệnh nhân.*\n")

        elif c_num == 5:
            # Table 5.1
            t6 = TABLES_DATA["table_06_finance_bilstm_arch"]
            lines.append(f"### {t6['title']}\n")
            lines.append("| " + " | ".join(t6["headers"]) + " |")
            lines.append("| " + " | ".join([":---" for _ in t6["headers"]]) + " |")
            for row in t6["rows"]:
                lines.append("| " + " | ".join(row) + " |")
            lines.append("\n")

            # Code Listings 5.1 & 5.2
            l51 = CODE_LISTINGS["listing_5_1"]
            lines.append(f"#### {l51['caption']}\n```python\n{l51['code']}\n```\n")
            l52 = CODE_LISTINGS["listing_5_2"]
            lines.append(f"#### {l52['caption']}\n```python\n{l52['code']}\n```\n")

            lines.append("![Hình 5.1](file:///c:/code/A2_CT_hautv.287/tieuluan2/charts/h09_finance_multi_asset_series.png)")
            lines.append("*Hình 5.1. Chuỗi biến động lịch sử 2.932 phiên của 7 tài sản tài chính.*\n")
            lines.append("![Hình 5.2](file:///c:/code/A2_CT_hautv.287/tieuluan2/charts/h10_bilstm_actual_vs_predicted.png)")
            lines.append("*Hình 5.2. Kết quả dự báo giá đóng cửa của mô hình PyTorch BiLSTM so với giá thực tế thị trường.*\n")
            lines.append("![Hình 5.3](file:///c:/code/A2_CT_hautv.287/tieuluan2/charts/h11_monte_carlo_dropout_fan_chart.png)")
            lines.append("*Hình 5.3. Biểu đồ dải quạt tin cậy Bayes 90% từ 200 lượt suy luận Monte Carlo Dropout.*\n")

        elif c_num == 6:
            lines.append("![Hình 6.1](file:///c:/code/A2_CT_hautv.287/tieuluan2/charts/h12_react_grounded_verifier_flow.png)")
            lines.append("*Hình 6.1. Quy trình vận hành vòng lặp ReAct kết hợp Bộ lập kế hoạch tất định và Bộ kiểm chứng độ trung thực số liệu Grounded Verifier.*\n")
            # Table 6.1
            t7 = TABLES_DATA["table_07_react_vs_llm_benchmark"]
            lines.append(f"### {t7['title']}\n")
            lines.append("| " + " | ".join(t7["headers"]) + " |")
            lines.append("| " + " | ".join([":---" for _ in t7["headers"]]) + " |")
            for row in t7["rows"]:
                lines.append("| " + " | ".join(row) + " |")
            lines.append("\n")

            # Code Listings 6.1 & 6.2
            l61 = CODE_LISTINGS["listing_6_1"]
            lines.append(f"#### {l61['caption']}\n```python\n{l61['code']}\n```\n")
            l62 = CODE_LISTINGS["listing_6_2"]
            lines.append(f"#### {l62['caption']}\n```python\n{l62['code']}\n```\n")

            lines.append("![Hình 6.2](file:///c:/code/A2_CT_hautv.287/tieuluan2/charts/h14_web_ui_dashboard_demo.png)")
            lines.append("*Hình 6.2. Giao diện Web Interactive Dashboard trực quan với Cytoscape.js và bảng điều khiển suy luận đa miền.*\n")

        for sec in chap["sections"]:
            lines.append(f"### {sec['title']}\n")
            lines.append(sec["text"].strip() + "\n")

        lines.append("---\n")

    lines.append("## TÀI LIỆU THAM KHẢO\n")
    for ref in BIBLIOGRAPHY:
        lines.append(f"- {ref}")
    lines.append("\n")

    md_content = "\n".join(lines)
    with open(os.path.join("tieuluan2", "BAO_CAO_TIEU_LUAN_2_NANG_CAP.md"), "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Written Markdown: {len(md_content)} characters, {len(md_content.split())} words.")


def generate_docx():
    print("Generating comprehensive Master Word document...")
    doc = docx.Document()

    # Page Margins
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    # 1. Formal Cover Page
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run(f"{FRONT_MATTER['institution']}\n{FRONT_MATTER['faculty']}\n")
    r_inst.bold = True
    r_inst.font.name = "Times New Roman"
    r_inst.font.size = Pt(13)
    r_inst.font.color.rgb = RGBColor(30, 58, 138)

    p_line = doc.add_paragraph()
    p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_line = p_line.add_run("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    r_line.font.color.rgb = RGBColor(148, 163, 184)
    p_line.paragraph_format.space_after = Pt(28)

    # PTIT Logo if available
    logo_path = os.path.join("tieuluan2", "figures", "ptit_logo.png")
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_after = Pt(20)
        p_logo.add_run().add_picture(logo_path, width=Inches(1.5))

    p_crs = doc.add_paragraph()
    p_crs.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_crs = p_crs.add_run("BÁO CÁO TIỂU LUẬN MÔN HỌC:\nPHÁT TRIỂN CÁC HỆ THỐNG THÔNG MINH\n")
    r_crs.bold = True
    r_crs.font.name = "Times New Roman"
    r_crs.font.size = Pt(14)
    r_crs.font.color.rgb = RGBColor(71, 85, 105)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(14)
    p_title.paragraph_format.space_after = Pt(12)
    r_title = p_title.add_run(f"ĐỀ TÀI:\n{FRONT_MATTER['title']}\n")
    r_title.bold = True
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(18)
    r_title.font.color.rgb = RGBColor(185, 28, 28)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(36)
    r_sub = p_sub.add_run(FRONT_MATTER['subtitle'])
    r_sub.italic = True
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = RGBColor(71, 85, 105)

    # Meta Table on Cover
    meta_tbl = doc.add_table(rows=5, cols=2)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Sinh viên thực hiện:", f"{FRONT_MATTER['student_name']}"),
        ("Mã sinh viên:", f"{FRONT_MATTER['student_id']}"),
        ("Lớp học phần:", f"{FRONT_MATTER['class_name']} ({FRONT_MATTER['group_name']})"),
        ("Giảng viên hướng dẫn:", f"{FRONT_MATTER['supervisor']}"),
        ("Học kỳ thực hiện:", f"{FRONT_MATTER['academic_year']}")
    ]
    for idx, (label, val) in enumerate(meta_data):
        c0, c1 = meta_tbl.rows[idx].cells[0], meta_tbl.rows[idx].cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(3.8)
        c0.paragraphs[0].paragraph_format.space_after = Pt(3)
        c1.paragraphs[0].paragraph_format.space_after = Pt(3)
        r0 = c0.paragraphs[0].add_run(label)
        r0.bold = True
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(11)
        r0.font.color.rgb = RGBColor(30, 41, 59)
        r1 = c1.paragraphs[0].add_run(val)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11)
        r1.font.color.rgb = RGBColor(15, 23, 42)

    p_loc = doc.add_paragraph()
    p_loc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_loc.paragraph_format.space_before = Pt(45)
    r_loc = p_loc.add_run(FRONT_MATTER['location_year'])
    r_loc.bold = True
    r_loc.font.name = "Times New Roman"
    r_loc.font.size = Pt(12)
    r_loc.font.color.rgb = RGBColor(71, 85, 105)

    doc.add_page_break()

    # Executive Summary
    h_sum = doc.add_heading(level=1)
    r_hs = h_sum.add_run("TỔNG QUAN VÀ TÓM TẮT ĐỀ TÀI (EXECUTIVE SUMMARY)")
    r_hs.font.name = "Times New Roman"
    r_hs.font.size = Pt(15)
    r_hs.font.color.rgb = RGBColor(30, 58, 138)
    h_sum.paragraph_format.space_after = Pt(8)

    h_vi = doc.add_heading(level=2)
    r_hvi = h_vi.add_run("Tóm tắt Đề tài Tiếng Việt")
    r_hvi.font.name = "Times New Roman"
    r_hvi.font.size = Pt(12)
    r_hvi.font.color.rgb = RGBColor(15, 23, 42)
    for p_text in EXECUTIVE_SUMMARY_VI.strip().split("\n\n"):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.25
        run = p.add_run(p_text.strip())
        run.font.name = "Times New Roman"
        run.font.size = Pt(11)

    h_en = doc.add_heading(level=2)
    r_hen = h_en.add_run("Abstract in English")
    r_hen.font.name = "Times New Roman"
    r_hen.font.size = Pt(12)
    r_hen.font.color.rgb = RGBColor(15, 23, 42)
    for p_text in EXECUTIVE_SUMMARY_EN.strip().split("\n\n"):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.25
        run = p.add_run(p_text.strip())
        run.font.name = "Times New Roman"
        run.font.size = Pt(11)
        run.italic = True

    # Abbreviations
    doc.add_page_break()
    h_abbr = doc.add_heading(level=1)
    r_ha = h_abbr.add_run("DANH MỤC CÁC KÝ HIỆU VÀ TỪ VIẾT TẮT")
    r_ha.font.name = "Times New Roman"
    r_ha.font.size = Pt(15)
    r_ha.font.color.rgb = RGBColor(30, 58, 138)
    h_abbr.paragraph_format.space_after = Pt(10)

    tbl_abbr = doc.add_table(rows=len(ABBREVIATIONS) + 1, cols=3)
    tbl_abbr.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_abbr = tbl_abbr.rows[0].cells
    hdr_abbr[0].text, hdr_abbr[1].text, hdr_abbr[2].text = "Ký hiệu", "Thuật ngữ Tiếng Anh", "Diễn giải Tiếng Việt"
    for cell in hdr_abbr:
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.bold = True
            run.font.name = "Times New Roman"
            run.font.size = Pt(9.5)
            run.font.color.rgb = RGBColor(255, 255, 255)

    for idx, (abbr, full_en, full_vi) in enumerate(ABBREVIATIONS):
        row_cells = tbl_abbr.rows[idx + 1].cells
        bg = "F8FAFC" if idx % 2 == 1 else "FFFFFF"
        row_cells[0].text, row_cells[1].text, row_cells[2].text = abbr, full_en, full_vi
        for c_idx, cell in enumerate(row_cells):
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(9)
                if c_idx == 0:
                    run.font.bold = True

    for row in tbl_abbr.rows:
        row.cells[0].width = Inches(1.2)
        row.cells[1].width = Inches(2.6)
        row.cells[2].width = Inches(2.6)

    # Chapters insertion
    for chap in ALL_CHAPTERS:
        doc.add_page_break()
        c_num = chap["chapter_num"]

        h_chap = doc.add_heading(level=1)
        r_hc = h_chap.add_run(chap["chapter_title"])
        r_hc.font.name = "Times New Roman"
        r_hc.font.size = Pt(15)
        r_hc.font.color.rgb = RGBColor(30, 58, 138)
        h_chap.paragraph_format.space_before = Pt(14)
        h_chap.paragraph_format.space_after = Pt(8)

        p_intro = doc.add_paragraph()
        p_intro.paragraph_format.space_after = Pt(10)
        p_intro.paragraph_format.line_spacing = 1.25
        r_intro = p_intro.add_run(chap["intro_text"].strip())
        r_intro.font.name = "Times New Roman"
        r_intro.font.size = Pt(11)
        r_intro.italic = True

        # Specific inserts
        if c_num == 1:
            add_image_figure_docx(doc, "tieuluan2/charts/h01_dual_domain_ecosystem.png",
                                 "Hình 1.1. Sơ đồ kiến trúc tổng thể 5 tầng của Hệ sinh thái Tri thức Đa miền Y tế và Tài chính Việt Nam.")
            format_table_docx(doc, TABLES_DATA["table_01_methods_comparison"])

        elif c_num == 2:
            add_image_figure_docx(doc, "tieuluan2/charts/h02_diabetes_ontology_hierarchy.png",
                                 "Hình 2.1. Cây phân cấp 23 lớp bản thể học và mạng lưới 17 vị từ quan hệ lâm sàng trong VietnamDiabetesKG.")
            format_table_docx(doc, TABLES_DATA["table_03_diabetes_ontology"])
            # Add Code Listings 2.1 & 2.2
            l21 = CODE_LISTINGS["listing_2_1"]
            add_code_block_docx(doc, l21["code"], l21["caption"])
            l22 = CODE_LISTINGS["listing_2_2"]
            add_code_block_docx(doc, l22["code"], l22["caption"])

            add_image_figure_docx(doc, "tieuluan2/charts/h03_finance_causal_network.png",
                                 "Hình 2.2. Đồ thị tri thức nhân quả có hướng có dấu VietnamFinanceKG mô tả chuỗi truyền dẫn Fed - DXY - USD/VND - SJC - VN30.")
            add_image_figure_docx(doc, "tieuluan2/charts/h13_graphdb_vs_vectordb_radar.png",
                                 "Hình 2.3. Biểu đồ Radar 6 chiều so sánh đặc tính kỹ thuật giữa Graph Database và Vector Database.")

        elif c_num == 3:
            add_image_figure_docx(doc, "tieuluan2/charts/h04_chunking_strategies_comparison.png",
                                 "Hình 3.1. So sánh trực quan 5 chiến lược phân mảnh văn bản.")
            format_table_docx(doc, TABLES_DATA["table_02_corpus_documents"])
            format_table_docx(doc, TABLES_DATA["table_04_rag_matrix_25"])
            # Add Code Listings 3.1 & 3.2
            l31 = CODE_LISTINGS["listing_3_1"]
            add_code_block_docx(doc, l31["code"], l31["caption"])
            l32 = CODE_LISTINGS["listing_3_2"]
            add_code_block_docx(doc, l32["code"], l32["caption"])

            add_image_figure_docx(doc, "tieuluan2/charts/h05_rag_matrix_heatmap.png",
                                 "Hình 3.2. Biểu đồ nhiệt (Heatmap) thể hiện độ chính xác Hit@1 trên ma trận thực nghiệm 25 cấu hình RAG.")
            add_image_figure_docx(doc, "tieuluan2/charts/h06_sparse_vs_dense_vs_hybrid_radar.png",
                                 "Hình 3.3. Biểu đồ Radar đa chiều đối sánh các bộ truy xuất.")

        elif c_num == 4:
            format_table_docx(doc, TABLES_DATA["table_05_diabetes_mlp_arch"])
            # Add Code Listings 4.1 & 4.2
            l41 = CODE_LISTINGS["listing_4_1"]
            add_code_block_docx(doc, l41["code"], l41["caption"])
            l42 = CODE_LISTINGS["listing_4_2"]
            add_code_block_docx(doc, l42["code"], l42["caption"])

            add_image_figure_docx(doc, "tieuluan2/charts/h07_diabetes_mlp_learning_curves.png",
                                 "Hình 4.1. Đường cong huấn luyện của mạng PyTorch DiabetesMLP (Loss và ROC-AUC qua 60 epoch).")
            add_image_figure_docx(doc, "tieuluan2/charts/h08_diabetes_confusion_matrix.png",
                                 "Hình 4.2. Ma trận nhầm lẫn (Confusion Matrix) trên tập kiểm thử 14.420 mẫu bệnh nhân.")
            add_callout_box_docx(doc,
                                 "CẢNH BÁO ĐỎ LÂM SÀNG: Tuyệt đối không sử dụng rượu bia khi đang điều trị bằng Metformin. Rượu ức chế phản ứng tân tạo glucose từ lactate tại gan, dẫn đến ứ đọng acid lactic nghiêm trọng kích hoạt Toan Lactic tử vong cao (30-50%).",
                                 "CẢNH BÁO TƯƠNG TÁC THUỐC TỬ VONG", "danger")

        elif c_num == 5:
            format_table_docx(doc, TABLES_DATA["table_06_finance_bilstm_arch"])
            # Add Code Listings 5.1 & 5.2
            l51 = CODE_LISTINGS["listing_5_1"]
            add_code_block_docx(doc, l51["code"], l51["caption"])
            l52 = CODE_LISTINGS["listing_5_2"]
            add_code_block_docx(doc, l52["code"], l52["caption"])

            add_image_figure_docx(doc, "tieuluan2/charts/h09_finance_multi_asset_series.png",
                                 "Hình 5.1. Chuỗi biến động lịch sử 2.932 phiên của 7 tài sản tài chính.")
            add_image_figure_docx(doc, "tieuluan2/charts/h10_bilstm_actual_vs_predicted.png",
                                 "Hình 5.2. Kết quả dự báo giá đóng cửa của mô hình PyTorch BiLSTM so với giá thực tế thị trường.")
            add_image_figure_docx(doc, "tieuluan2/charts/h11_monte_carlo_dropout_fan_chart.png",
                                 "Hình 5.3. Biểu đồ dải quạt tin cậy Bayes 90% từ 200 lượt suy luận Monte Carlo Dropout.")
            add_callout_box_docx(doc,
                                 "QUY TẮC QUẢN TRỊ RỦI RO ĐẦU TƯ: Khi thị trường xuất hiện cú sốc chính sách hoặc biến động tỷ giá cực đoan, Dải quạt tin cậy Bayes 90% sẽ tự động phình rộng. Nhà đầu tư bắt buộc phải thu hẹp quy mô vị thế và đặt ngưỡng cắt lỗ chặt tại cận dưới của dải tin cậy.",
                                 "QUY TẮC QUẢN TRỊ RỦI RO BAYES", "warning")

        elif c_num == 6:
            add_image_figure_docx(doc, "tieuluan2/charts/h12_react_grounded_verifier_flow.png",
                                 "Hình 6.1. Quy trình vận hành vòng lặp ReAct kết hợp Bộ lập kế hoạch tất định và Bộ kiểm chứng độ trung thực số liệu Grounded Verifier.")
            format_table_docx(doc, TABLES_DATA["table_07_react_vs_llm_benchmark"])
            # Add Code Listings 6.1 & 6.2
            l61 = CODE_LISTINGS["listing_6_1"]
            add_code_block_docx(doc, l61["code"], l61["caption"])
            l62 = CODE_LISTINGS["listing_6_2"]
            add_code_block_docx(doc, l62["code"], l62["caption"])

            add_image_figure_docx(doc, "tieuluan2/charts/h14_web_ui_dashboard_demo.png",
                                 "Hình 6.2. Giao diện Web Interactive Dashboard trực quan với Cytoscape.js và bảng điều khiển suy luận đa miền.")

        # Sections
        for sec in chap["sections"]:
            h_sec = doc.add_heading(level=2)
            r_hs = h_sec.add_run(sec["title"])
            r_hs.font.name = "Times New Roman"
            r_hs.font.size = Pt(12.5)
            r_hs.font.color.rgb = RGBColor(15, 23, 42)
            h_sec.paragraph_format.space_before = Pt(10)
            h_sec.paragraph_format.space_after = Pt(4)

            paragraphs = sec["text"].strip().split("\n\n")
            for p_raw in paragraphs:
                p = doc.add_paragraph()
                p.paragraph_format.space_after = Pt(6)
                p.paragraph_format.line_spacing = 1.25
                run = p.add_run(p_raw.strip())
                run.font.name = "Times New Roman"
                run.font.size = Pt(11)

    # Bibliography
    doc.add_page_break()
    h_bib = doc.add_heading(level=1)
    r_hb = h_bib.add_run("TÀI LIỆU THAM KHẢO")
    r_hb.font.name = "Times New Roman"
    r_hb.font.size = Pt(15)
    r_hb.font.color.rgb = RGBColor(30, 58, 138)
    h_bib.paragraph_format.space_after = Pt(10)

    for ref in BIBLIOGRAPHY:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.paragraph_format.line_spacing = 1.15
        run = p_ref.add_run(ref)
        run.font.name = "Times New Roman"
        run.font.size = Pt(10)

    out_path = os.path.join("tieuluan2", "Bao_Cao_Tieu_Luan_2_Nang_Cap.docx")
    doc.save(out_path)
    print(f"Written Word Document successfully: {out_path}")


if __name__ == "__main__":
    generate_markdown()
    generate_docx()
    print("Done generating Master Treatise!")
