#!/usr/bin/env python3
"""
Helper utilities for Project 01 V2 Report Generator
Provides robust styling, callouts, tables, figures, and code block formatting.
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(CURRENT_DIR)
FIG_DIR = os.path.join(PROJECT_DIR, "figures")

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def add_callout(doc, text, title="QUY CHUẨN LÂM SÀNG & KHUYẾN NGHỊ CHUYÊN GIA", border_color="2563EB", fill_hex="EFF6FF"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, fill_hex)
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="28" w:space="0" w:color="{border_color}"/>'
        f'<w:top w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:bottom w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    run_t = p.add_run(f"[{title}]\n")
    run_t.bold = True
    run_t.font.name = "Times New Roman"
    run_t.font.size = Pt(10)
    run_t.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
    
    run_b = p.add_run(text)
    run_b.font.name = "Times New Roman"
    run_b.font.size = Pt(9.5)
    run_b.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
    doc.add_paragraph().paragraph_format.space_after = Pt(3)

def add_code_block(doc, code_str, caption="Mã nguồn triển khai thuật toán"):
    p_cap = doc.add_paragraph()
    p_cap.paragraph_format.space_before = Pt(6)
    p_cap.paragraph_format.space_after = Pt(2)
    run_c = p_cap.add_run(f"✦ {caption}:")
    run_c.font.name = "Times New Roman"
    run_c.font.size = Pt(9.5)
    run_c.font.bold = True
    run_c.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="18" w:space="0" w:color="475569"/>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    run_code = p.add_run(code_str.strip())
    run_code.font.name = "Consolas"
    run_code.font.size = Pt(8.0)
    run_code.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_figure(doc, img_filename, caption_text, width_inches=6.0):
    img_path = os.path.join(FIG_DIR, img_filename)
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(width_inches))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(10)
        run_cap = p_cap.add_run(caption_text)
        run_cap.font.name = "Times New Roman"
        run_cap.font.size = Pt(9.0)
        run_cap.font.italic = True
        run_cap.font.color.rgb = RGBColor(0x47, 0x55, 0x69)
    else:
        print(f"[!] Warning: Figure {img_filename} not found in {FIG_DIR}.")

def add_custom_heading(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.space_before = Pt(14 if level == 1 else 10)
    h.paragraph_format.space_after = Pt(6)
    h.paragraph_format.keep_with_next = True
    
    for r in h.runs:
        r.font.name = "Times New Roman"
        if level == 1:
            r.font.size = Pt(15)
            r.bold = True
            r.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)  # Navy
        elif level == 2:
            r.font.size = Pt(13)
            r.bold = True
            r.font.color.rgb = RGBColor(0x1D, 0x4E, 0xD8)  # Blue
        elif level == 3:
            r.font.size = Pt(11)
            r.bold = True
            r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)  # Slate
    return h

def add_body_p(doc, text, bold_prefix=None, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.2
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(10.5)
        r_pre.bold = True
        r_pre.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        
    r_body = p.add_run(text)
    r_body.font.name = "Times New Roman"
    r_body.font.size = Pt(10.5)
    r_body.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
    return p

def populate_table(doc, headers, data_rows, col_widths=None, header_bg="1E3A8A"):
    tbl = doc.add_table(rows=len(data_rows) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Header
    for j, h in enumerate(headers):
        c = tbl.cell(0, j)
        set_cell_background(c, header_bg)
        set_cell_margins(c, top=80, bottom=80, left=120, right=120)
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(h)
        r.font.name = "Times New Roman"
        r.font.size = Pt(8.5)
        r.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    # Rows
    for i, row in enumerate(data_rows):
        bg = "FFFFFF" if i % 2 == 0 else "F8FAFC"
        for j, val in enumerate(row):
            c = tbl.cell(i + 1, j)
            set_cell_background(c, bg)
            set_cell_margins(c, top=60, bottom=60, left=100, right=100)
            p = c.paragraphs[0]
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            r = p.add_run(str(val))
            r.font.name = "Times New Roman"
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
            if j == 0:
                r.bold = True
                
    # Widths
    if col_widths and len(col_widths) == len(headers):
        for row in tbl.rows:
            for j, w in enumerate(col_widths):
                row.cells[j].width = Inches(w)
                
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    return tbl
