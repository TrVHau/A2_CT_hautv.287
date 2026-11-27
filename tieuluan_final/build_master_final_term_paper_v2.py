#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MASTER FINAL TERM PAPER V2 GENERATOR
Học viện Công nghệ Bưu chính Viễn thông (PTIT) - Khoa Công nghệ Thông tin 1
Môn học: Phát triển Hệ thống Thông minh
Giảng viên hướng dẫn: PGS. TS. Trần Đình Quế
Sinh viên thực hiện: Trần Văn Hậu | MSV: B23DCCN287 | Lớp: D23CTPM01 | Nhóm: CT_09
Đề tài: Nghiên cứu và Xây dựng Hệ thống Thông minh Toàn diện:
        Từ Học máy Cơ bản, CNN, RNN–LSTM đến Knowledge Graph, Deep Graph và Hệ Đa Tác tử Tự chủ
Phiên bản: V2 Master Expanded Academic Edition
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
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

# Paths
ROOT = Path("c:/code/A2_CT_hautv.287").resolve()
FINAL_DIR = ROOT / "tieuluan_final"
V2_DIR = FINAL_DIR / "v2_sections"
if str(V2_DIR) not in sys.path:
    sys.path.insert(0, str(V2_DIR))

# Import V2 Section modules
from v2_sec_front_matter import (
    add_cover_v2,
    add_academic_preamble_v2,
    add_executive_summary_v2,
    add_abbreviations_v2,
    add_table_of_contents_v2,
    add_figures_and_tables_list_v2,
)
from v2_sec_mo_dau import add_mo_dau_v2
from v2_sec_chap1_history import add_chap1_history_v2
from v2_sec_chap2_ml_basic import add_chap2_ml_basic_v2
from v2_sec_chap3_cnn import add_chap3_cnn_v2
from v2_sec_chap4_rnn import add_chap4_rnn_v2
from v2_sec_chap5_kg_rag import add_chap5_kg_rag_v2
from v2_sec_chap6_deep_graph import add_chap6_deep_graph_v2
from v2_sec_chap7_multi_agent import add_chap7_multi_agent_v2
from v2_sec_conclusion_and_appendix import add_conclusion_and_appendix_v2

DOCX_OUT = FINAL_DIR / "tieuluan_final_CT_09_Hautv.287_v2.docx"
LOGO_PATH = ROOT / "agent" / "ptit_logo.png"

# Color Palette
C_NAVY = RGBColor(15, 23, 42)       # Slate 900
C_PRIMARY = RGBColor(30, 58, 138)   # Blue 900
C_SECONDARY = RGBColor(29, 78, 216) # Blue 700
C_TEXT = RGBColor(30, 41, 59)       # Slate 800
C_MUTED = RGBColor(100, 116, 139)   # Slate 500
C_CODE = RGBColor(51, 65, 85)       # Slate 700

# Hex colors for table and box XML shading
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
    hrun = hp.add_run("HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG — TIỂU LUẬN FINAL HỆ THỐNG THÔNG MINH (V2)")
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
    text = str(text).replace("\x08", "\\b").replace("\x0c", "\\f").replace("\x07", "\\a").replace("\x0b", "\\v")
    return "".join(ch for ch in text if ord(ch) >= 32 or ch in ("\t", "\n"))


# Element Builders
def p_body(doc, text="", bold=False, italic=False, color=C_TEXT, space_after=6.0, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.45
    if text:
        r = p.add_run(clean_xml_text(text))
        r.font.name = "Times New Roman"
        r.font.size = Pt(13)
        r.font.bold = bold
        r.font.italic = italic
        r.font.color.rgb = color
    return p


def p_bullet(doc, text, bold_prefix="", level=0):
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(4.5)
    p.paragraph_format.line_spacing = 1.38
    if bold_prefix:
        r_pre = p.add_run(clean_xml_text(bold_prefix) + " ")
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(13)
        r_pre.font.bold = True
        r_pre.font.color.rgb = C_PRIMARY
    r = p.add_run(clean_xml_text(text))
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.color.rgb = C_TEXT
    return p


def h_chap(doc, text):
    doc.add_page_break()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(20)
    p.paragraph_format.space_after = Pt(14)
    r = p.add_run(clean_xml_text(text))
    r.font.name = "Times New Roman"
    r.font.size = Pt(16.0)
    r.font.bold = True
    r.font.color.rgb = C_PRIMARY
    return p


def h_sec(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(15)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(clean_xml_text(text))
    r.font.name = "Times New Roman"
    r.font.size = Pt(14.0)
    r.font.bold = True
    r.font.color.rgb = C_PRIMARY
    return p


def h_sub(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(11)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(clean_xml_text(text))
    r.font.name = "Times New Roman"
    r.font.size = Pt(13.0)
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
        p_cap.paragraph_format.space_before = Pt(10)
        p_cap.paragraph_format.space_after = Pt(5)
        r_cap = p_cap.add_run(clean_xml_text(caption))
        r_cap.font.name = "Times New Roman"
        r_cap.font.size = Pt(11.0)
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
        hp.paragraph_format.space_after = Pt(3.5)
        hp.paragraph_format.space_before = Pt(3.5)
        hrun = hp.add_run(clean_xml_text(str(h)))
        hrun.font.name = "Times New Roman"
        hrun.font.size = Pt(10.5)
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
            rp.paragraph_format.space_after = Pt(3)
            rp.paragraph_format.space_before = Pt(3)
            rrun = rp.add_run(val_str)
            rrun.font.name = "Times New Roman"
            rrun.font.size = Pt(10.0)
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
    p_img.paragraph_format.space_before = Pt(8)
    p_img.paragraph_format.space_after = Pt(3)
    p_img.add_run().add_picture(str(full_path), width=Inches(width))

    if caption:
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(3)
        p_cap.paragraph_format.space_after = Pt(10)
        rc = p_cap.add_run(clean_xml_text(caption))
        rc.font.name = "Times New Roman"
        rc.font.size = Pt(10.5)
        rc.font.italic = True
        rc.font.color.rgb = C_MUTED


def add_code_block(doc, code_str, title=""):
    if title:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(8)
        p_t.paragraph_format.space_after = Pt(3)
        rt = p_t.add_run(clean_xml_text(f"Mã nguồn: {title}"))
        rt.font.name = "Consolas"
        rt.font.size = Pt(10.0)
        rt.font.bold = True
        rt.font.color.rgb = C_PRIMARY

    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = t.rows[0].cells[0]
    cell.width = Inches(6.5)
    shade_cell(cell, HEX_CODE_BG)
    cell.text = ""
    cp = cell.paragraphs[0]
    cp.paragraph_format.space_before = Pt(5)
    cp.paragraph_format.space_after = Pt(5)
    cp.paragraph_format.line_spacing = 1.20
    crun = cp.add_run(clean_xml_text(code_str.strip()))
    crun.font.name = "Consolas"
    crun.font.size = Pt(9.5)
    crun.font.color.rgb = C_CODE
    p_body(doc, "", space_after=4)


def build_full_report_v2():
    print("==================================================")
    print("STARTING BUILD MASTER FINAL TERM PAPER DOCX V2")
    print("Sinh viên: Trần Văn Hậu (B23DCCN287) - Lớp D23CTPM01 - CT_09")
    print("==================================================")

    doc = Document()
    configure_document(doc)

    print("1/10 Building Front Matter V2 (Cover, Preamble, Executive Summary, Abbreviations, Detailed TOC, Figures/Tables List)...")
    add_cover_v2(doc, LOGO_PATH)
    add_academic_preamble_v2(doc, p_body, h_sec)
    add_executive_summary_v2(doc, h_sec, p_body)
    add_abbreviations_v2(doc, h_sec, add_table_data)
    add_table_of_contents_v2(doc, h_sec, p_body)
    add_figures_and_tables_list_v2(doc, h_sec, p_body)

    print("2/10 Building MỞ ĐẦU V2 (Introduction, Dual Domains, 7 Research Questions, 10 Contributions)...")
    add_mo_dau_v2(doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure)

    print("3/10 Building CHƯƠNG 1 V2 (Lịch sử AI, Novikoff Proof, Minsky-Papert XOR Proof, Dual Domains History, 4 Gen Benchmark)...")
    add_chap1_history_v2(doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math)

    print("4/10 Building CHƯƠNG 2 V2 (Học máy cơ bản, Bias-Variance Proof, OLS/Ridge, BCE, SVM KKT, XGBoost, LendingClub 36k, Parity < 10^-7)...")
    add_chap2_ml_basic_v2(doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math)

    print("5/10 Building CHƯƠNG 3 V2 (CNN, Conv2D Math, im2col GEMM, Receptive Field, ResNet, Grad-CAM, GASF/GADF, RetinaMNIST, Parity)...")
    add_chap3_cnn_v2(doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math)

    print("6/10 Building CHƯƠNG 4 V2 (RNN, BPTT Vanishing Proof, LSTM CEC Derivation, GRU, Temporal Attention, Shanghai CGM, Backtest sau phí)...")
    add_chap4_rnn_v2(doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math)

    print("7/10 Building CHƯƠNG 5 V2 (Knowledge Graph, Neo4j 90k nodes, Hybrid Retrieval BM25+Dense+RRF, GraphRAG Multi-Hop, Ragas 1.0, ToolAgent)...")
    add_chap5_kg_rag_v2(doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math)

    print("8/10 Building CHƯƠNG 6 V2 (Deep Graph Learning, MPNN, Spectral Kipf-Welling GCN, GraphSAGE, GAT, Dirichlet Over-Smoothing Proof, 1-WL)...")
    add_chap6_deep_graph_v2(doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math)

    print("9/10 Building CHƯƠNG 7 V2 (Multi-Agent Systems, PEAS, Dec-POMDP, CTDE, 5-Agent Council, Bayesian Consensus Gate tau=0.85, Guardrails)...")
    add_chap7_multi_agent_v2(doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math)

    print("10/10 Building KẾT LUẬN & PHỤ LỤC V2 (Trả lời CH1-CH7, Hợp hàm vạn năng, 4 Hạn chế, 6 Hướng phát triển, 48 IEEE Refs, 4 Phụ lục)...")
    add_conclusion_and_appendix_v2(doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math)

    print(f"Saving DOCX to: {DOCX_OUT} ...")
    doc.save(str(DOCX_OUT))
    file_size_mb = DOCX_OUT.stat().st_size / (1024 * 1024)
    print(f"DOCX build V2 completed successfully! File size: {file_size_mb:.2f} MB")


if __name__ == "__main__":
    build_full_report_v2()
