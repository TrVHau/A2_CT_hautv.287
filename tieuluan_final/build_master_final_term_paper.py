#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MASTER FINAL TERM PAPER GENERATOR
Học viện Công nghệ Bưu chính Viễn thông (PTIT) - Khoa Công nghệ Thông tin 1
Môn học: Phát triển Hệ thống Thông minh
Giảng viên hướng dẫn: PGS. TS. Trần Đình Quế
Sinh viên: Trần Văn Hậu | MSV: B23DCCN287 | Lớp: D23CTPM01 | Nhóm CT_09
Đề tài: Nghiên cứu và Xây dựng Hệ thống Thông minh Toàn diện:
        Từ Học máy Cơ bản, CNN, RNN–LSTM đến Knowledge Graph, Deep Graph và Hệ Đa Tác tử Tự chủ
"""

import os
import sys

# Ensure UTF-8 output on Windows console
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

# Ensure current directory is on python path
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

# Import section modules
from sec_front_matter import add_cover, add_academic_preamble, add_abbreviations
from sec_mo_dau import add_mo_dau
from sec_chap1_history import add_chap1_history
from sec_chap2_ml_basic import add_chap2_ml_basic
from sec_chap3_cnn import add_chap3_cnn
from sec_chap4_rnn import add_chap4_rnn
from sec_chap5_kg_rag import add_chap5_kg_rag
from sec_chap6_deep_graph import add_chap6_deep_graph
from sec_chap7_multi_agent import add_chap7_multi_agent
from sec_conclusion_and_appendix import add_conclusion_and_appendix

# Paths
ROOT = Path("c:/code/A2_CT_hautv.287").resolve()
FINAL_DIR = ROOT / "tieuluan_final"
DOCX_OUT = FINAL_DIR / "tieuluan_final_CT_09_Hautv.287.docx"
MD_OUT = FINAL_DIR / "tieuluan_final_CT_09_Hautv.287.md"
LOGO_PATH = ROOT / "agent" / "ptit_logo.png"

# Colors
C_NAVY = RGBColor(15, 23, 42)       # Slate 900
C_PRIMARY = RGBColor(30, 58, 138)   # Blue 900
C_SECONDARY = RGBColor(29, 78, 216) # Blue 700
C_TEXT = RGBColor(30, 41, 59)       # Slate 800
C_MUTED = RGBColor(100, 116, 139)   # Slate 500
C_CODE = RGBColor(51, 65, 85)       # Slate 700

# Hex colors for XML shading
HEX_PRIMARY = "1E3A8A"
HEX_LIGHT_BG = "F8FAFC"
HEX_ALT_ROW = "F1F5F9"
HEX_CODE_BG = "F1F5F9"
HEX_BORDER = "CBD5E1"


def shade_cell(cell, hex_color):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), hex_color)
    tc_pr.append(shd)


def add_xml_field(p, field_code):
    run = p.add_run()
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = field_code
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    fldChar3 = OxmlElement('w:fldChar')
    fldChar3.set(qn('w:fldCharType'), 'end')
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)


def configure_document(doc):
    style_normal = doc.styles["Normal"]
    style_normal.font.name = "Times New Roman"
    style_normal.font.size = Pt(12)
    style_normal.font.color.rgb = C_TEXT

    sec = doc.sections[0]
    sec.page_width = Inches(8.27)   # A4 Width
    sec.page_height = Inches(11.69) # A4 Height
    sec.top_margin = Inches(0.79)   # 20mm
    sec.bottom_margin = Inches(0.79)# 20mm
    sec.left_margin = Inches(0.98)  # 25mm
    sec.right_margin = Inches(0.79) # 20mm

    # Configure Header & Footer
    header = sec.header
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hrun = hp.add_run("HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG — TIỂU LUẬN FINAL HỆ THỐNG THÔNG MINH")
    hrun.font.name = "Times New Roman"
    hrun.font.size = Pt(8.5)
    hrun.font.color.rgb = C_MUTED
    hrun.font.italic = True

    footer = sec.footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    frun = fp.add_run("Trần Văn Hậu — B23DCCN287 | Lớp D23CTPM01 | Nhóm CT_09 | Trang ")
    frun.font.name = "Times New Roman"
    frun.font.size = Pt(9.5)
    frun.font.color.rgb = C_MUTED
    add_xml_field(fp, "PAGE")
    frun2 = fp.add_run(" / ")
    frun2.font.name = "Times New Roman"
    frun2.font.size = Pt(9.5)
    frun2.font.color.rgb = C_MUTED
    add_xml_field(fp, "NUMPAGES")


def clean_xml_text(text):
    if not text:
        return ""
    # Replace accidental escapes from LaTeX formulas
    text = str(text).replace("\x08", "\\b").replace("\x0c", "\\f").replace("\x07", "\\a").replace("\x0b", "\\v")
    # Remove any other non-XML control characters
    return "".join(ch for ch in text if ord(ch) >= 32 or ch in ("\t", "\n"))


# Element Builders
def p_body(doc, text="", bold=False, italic=False, color=C_TEXT, space_after=5, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.25
    if text:
        r = p.add_run(clean_xml_text(text))
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)
        r.font.bold = bold
        r.font.italic = italic
        r.font.color.rgb = color
    return p


def p_bullet(doc, text, bold_prefix="", level=0):
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.2
    if bold_prefix:
        r_pre = p.add_run(clean_xml_text(bold_prefix) + " ")
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(12)
        r_pre.font.bold = True
        r_pre.font.color.rgb = C_PRIMARY
    r = p.add_run(clean_xml_text(text))
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.color.rgb = C_TEXT
    return p


def h_chap(doc, text):
    doc.add_page_break()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(14)
    r = p.add_run(clean_xml_text(text))
    r.font.name = "Times New Roman"
    r.font.size = Pt(15.5)
    r.font.bold = True
    r.font.color.rgb = C_PRIMARY
    return p


def h_sec(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(clean_xml_text(text))
    r.font.name = "Times New Roman"
    r.font.size = Pt(13.0)
    r.font.bold = True
    r.font.color.rgb = C_PRIMARY
    return p


def h_sub(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(clean_xml_text(text))
    r.font.name = "Times New Roman"
    r.font.size = Pt(12.0)
    r.font.bold = True
    r.font.color.rgb = C_SECONDARY
    return p


def add_math(doc, formula_text, display=True):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if display else WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(clean_xml_text(formula_text))
    r.font.name = "Cambria Math"
    r.font.size = Pt(11.5)
    r.font.italic = True
    r.font.color.rgb = C_NAVY
    return p


def add_table_data(doc, headers, rows, widths=None, caption=None):
    if caption:
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(8)
        p_cap.paragraph_format.space_after = Pt(4)
        r_cap = p_cap.add_run(clean_xml_text(caption))
        r_cap.font.name = "Times New Roman"
        r_cap.font.size = Pt(10.5)
        r_cap.font.bold = True
        r_cap.font.color.rgb = C_PRIMARY

    t = doc.add_table(rows=1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.style = "Table Grid"

    # Header Row
    hdr_cells = t.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = ""
        hp = hdr_cells[i].paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        hp.paragraph_format.space_after = Pt(2)
        hp.paragraph_format.space_before = Pt(2)
        hrun = hp.add_run(clean_xml_text(str(h)))
        hrun.font.name = "Times New Roman"
        hrun.font.size = Pt(9.5)
        hrun.font.bold = True
        hrun.font.color.rgb = RGBColor(255, 255, 255)
        shade_cell(hdr_cells[i], HEX_PRIMARY)
        hdr_cells[i].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER

    # Data Rows
    for r_idx, row in enumerate(rows):
        row_cells = t.add_row().cells
        bg_hex = HEX_ALT_ROW if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row):
            row_cells[c_idx].text = ""
            rp = row_cells[c_idx].paragraphs[0]
            val_str = clean_xml_text(str(val))
            if len(val_str) <= 12:
                rp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                rp.alignment = WD_ALIGN_PARAGRAPH.LEFT
            rp.paragraph_format.space_after = Pt(2)
            rp.paragraph_format.space_before = Pt(2)
            rrun = rp.add_run(val_str)
            rrun.font.name = "Times New Roman"
            rrun.font.size = Pt(9.0)
            rrun.font.color.rgb = C_TEXT
            shade_cell(row_cells[c_idx], bg_hex)
            row_cells[c_idx].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER

    if widths:
        for r in t.rows:
            for idx, w in enumerate(widths):
                r.cells[idx].width = Inches(w)

    p_body(doc, "", space_after=4)
    return t


def add_figure(doc, img_path, caption="", width=5.6):
    full_path = Path(img_path)
    if not full_path.is_absolute():
        full_path = ROOT / img_path

    if not full_path.exists():
        p_body(doc, f"[HÌNH ẢNH: {caption} - Đường dẫn file không tìm thấy: {full_path.name}]", italic=True, color=C_MUTED)
        return

    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(6)
    p_img.paragraph_format.space_after = Pt(2)
    p_img.add_run().add_picture(str(full_path), width=Inches(width))

    if caption:
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(8)
        rc = p_cap.add_run(clean_xml_text(caption))
        rc.font.name = "Times New Roman"
        rc.font.size = Pt(10)
        rc.font.italic = True
        rc.font.color.rgb = C_MUTED


def add_code_block(doc, code_str, title=""):
    if title:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(6)
        p_t.paragraph_format.space_after = Pt(2)
        rt = p_t.add_run(clean_xml_text(f"Mã nguồn: {title}"))
        rt.font.name = "Consolas"
        rt.font.size = Pt(9.5)
        rt.font.bold = True
        rt.font.color.rgb = C_PRIMARY

    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = t.rows[0].cells[0]
    cell.width = Inches(6.5)
    shade_cell(cell, HEX_CODE_BG)
    cell.text = ""
    cp = cell.paragraphs[0]
    cp.paragraph_format.space_before = Pt(3)
    cp.paragraph_format.space_after = Pt(3)
    crun = cp.add_run(clean_xml_text(code_str.strip()))
    crun.font.name = "Consolas"
    crun.font.size = Pt(8.5)
    crun.font.color.rgb = C_CODE
    p_body(doc, "", space_after=4)


def build_full_report():
    print("==================================================")
    print("STARTING BUILD MASTER FINAL TERM PAPER DOCX & MD")
    print("==================================================")
    
    doc = Document()
    configure_document(doc)

    print("1/10 Building Front Matter (Cover, Preambles, Abbreviations)...")
    add_cover(doc, LOGO_PATH)
    add_academic_preamble(doc, p_body, h_sec)
    add_abbreviations(doc, h_sec, add_table_data)

    print("2/10 Building MỞ ĐẦU (Introduction)...")
    add_mo_dau(doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data)

    print("3/10 Building CHƯƠNG 1 (Lịch sử phát triển AI)...")
    add_chap1_history(doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math)

    print("4/10 Building CHƯƠNG 2 (Học máy cơ bản & 3 cách cài đặt)...")
    add_chap2_ml_basic(doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math)

    print("5/10 Building CHƯƠNG 3 (CNN, Grad-CAM & 3 cách cài đặt)...")
    add_chap3_cnn(doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math)

    print("6/10 Building CHƯƠNG 4 (RNN, LSTM, GRU & Backtest)...")
    add_chap4_rnn(doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math)

    print("7/10 Building CHƯƠNG 5 (Knowledge Graph & GraphRAG)...")
    add_chap5_kg_rag(doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math)

    print("8/10 Building CHƯƠNG 6 (Deep Graph Learning, GCN & GAT)...")
    add_chap6_deep_graph(doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math)

    print("9/10 Building CHƯƠNG 7 (Multi-Agent Systems & Deliberation Council)...")
    add_chap7_multi_agent(doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math)

    print("10/10 Building Kết luận, Tài liệu tham khảo và Phụ lục...")
    add_conclusion_and_appendix(doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math)

    print(f"Saving DOCX to: {DOCX_OUT} ...")
    doc.save(str(DOCX_OUT))
    print("DOCX build completed successfully!")


if __name__ == "__main__":
    build_full_report()
