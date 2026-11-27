#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MASTER MARKDOWN REPORT V2 BUILDER
Assembles the complete master final term paper in Markdown format directly
from the enhanced V2 chapter modules to guarantee 100% parity with the Word DOCX report.
Author: Tran Van Hau (B23DCCN287) - Class D23CTPM01 - Group CT_09
Supervisor: PGS. TS. Tran Dinh Que
Institution: Posts and Telecommunications Institute of Technology (PTIT)
"""

import sys
from pathlib import Path

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

ROOT = Path("c:/code/A2_CT_hautv.287").resolve()
FINAL_DIR = ROOT / "tieuluan_final"
V2_DIR = FINAL_DIR / "v2_sections"
if str(V2_DIR) not in sys.path:
    sys.path.insert(0, str(V2_DIR))

# Import section modules
from v2_sec_front_matter import (
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

MD_OUT = FINAL_DIR / "tieuluan_final_CT_09_Hautv.287_v2.md"


class MarkdownCollector:
    def __init__(self):
        self.lines = []

    def add(self, text=""):
        self.lines.append(text)

    def get_content(self):
        return "\n".join(self.lines)


class DummyFont:
    def __init__(self):
        self.name = ""
        self.size = 0
        self.bold = False
        self.italic = False
        self.color = type('c', (), {'rgb': None})()


class DummyRun:
    def __init__(self):
        self.font = DummyFont()


class DummyParagraph:
    def __init__(self, collector):
        self.collector = collector
        self.paragraph_format = type('obj', (), {
            'space_after': 0, 'line_spacing': 0, 'left_indent': 0, 
            'first_line_indent': 0, 'space_before': 0
        })()

    def add_run(self, text=""):
        if text and text.strip():
            self.collector.add(f"{text.strip()}")
        return DummyRun()


class DummyDoc:
    def __init__(self, collector):
        self.collector = collector

    def add_paragraph(self, text="", style=None):
        if text:
            self.collector.add(f"{text}\n")
        return DummyParagraph(self.collector)

    def add_page_break(self):
        self.collector.add("\n---\n")


def p_body_md(collector, text="", bold=False, italic=False, **kwargs):
    if not text:
        return DummyParagraph(collector)
    prefix = "**" if bold else ("*" if italic else "")
    suffix = "**" if bold else ("*" if italic else "")
    collector.add(f"{prefix}{text}{suffix}\n")
    return DummyParagraph(collector)


def p_bullet_md(collector, text, bold_prefix="", **kwargs):
    if bold_prefix:
        collector.add(f"- **{bold_prefix}** {text}")
    else:
        collector.add(f"- {text}")
    return DummyParagraph(collector)


def h_chap_md(collector, text):
    collector.add(f"\n# {text}\n")
    return DummyParagraph(collector)


def h_sec_md(collector, text):
    collector.add(f"\n## {text}\n")
    return DummyParagraph(collector)


def h_sub_md(collector, text):
    collector.add(f"\n### {text}\n")
    return DummyParagraph(collector)


def add_math_md(collector, formula_text, display=True):
    if display:
        collector.add(f"\n$$\n{formula_text}\n$$\n")
    else:
        collector.add(f"${formula_text}$")
    return DummyParagraph(collector)


def add_figure_md(collector, img_path, caption="", width=None):
    collector.add(f"\n![{caption}]({img_path})\n***{caption}***\n")


def add_code_block_md(collector, code_str, title=""):
    collector.add(f"\n```{title if title else ''}\n{code_str.strip()}\n```\n")


def add_table_data_md(collector, headers, rows, widths=None, caption=None):
    if caption:
        collector.add(f"\n**{caption}**\n")
    
    header_line = "| " + " | ".join(str(h) for h in headers) + " |"
    separator_line = "| " + " | ".join(["---"] * len(headers)) + " |"
    collector.add(header_line)
    collector.add(separator_line)

    for row in rows:
        row_line = "| " + " | ".join(str(c).replace("\n", "<br>") for c in row) + " |"
        collector.add(row_line)
    collector.add("")


def build_markdown_report_v2():
    print("==================================================")
    print("STARTING BUILD MASTER MARKDOWN REPORT V2")
    print("Sinh viên: Trần Văn Hậu (B23DCCN287) - Lớp D23CTPM01 - CT_09")
    print("==================================================")

    collector = MarkdownCollector()
    dummy_doc = DummyDoc(collector)

    # Adapters
    def p_body(doc, text="", bold=False, italic=False, **kwargs):
        return p_body_md(collector, text, bold, italic, **kwargs)

    def p_bullet(doc, text, bold_prefix="", **kwargs):
        return p_bullet_md(collector, text, bold_prefix, **kwargs)

    def h_chap(doc, text):
        return h_chap_md(collector, text)

    def h_sec(doc, text):
        return h_sec_md(collector, text)

    def h_sub(doc, text):
        return h_sub_md(collector, text)

    def add_math(doc, formula_text, display=True):
        return add_math_md(collector, formula_text, display)

    def add_figure(doc, img_path, caption="", width=None):
        add_figure_md(collector, img_path, caption, width)

    def add_code_block(doc, code_str, title=""):
        add_code_block_md(collector, code_str, title)

    def add_table_data(doc, headers, rows, widths=None, caption=None):
        add_table_data_md(collector, headers, rows, widths, caption)

    # Header front matter in MD
    collector.add("""# BÁO CÁO TIỂU LUẬN TỔNG KẾT MÔN HỌC (PHIÊN BẢN V2 TOÀN DIỆN)
## HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG — KHOA CÔNG NGHỆ THÔNG TIN 1
**Môn học:** Phát triển Hệ thống Thông minh  
**Giảng viên hướng dẫn:** PGS. TS. Trần Đình Quế  
**Sinh viên thực hiện:** Trần Văn Hậu  
**Mã sinh viên:** B23DCCN287 | **Lớp:** D23CTPM01 | **Nhóm tiểu luận:** CT_09  
**Đề tài:** Nghiên cứu và Xây dựng Hệ thống Thông minh Toàn diện: Từ Học máy Cơ bản, CNN, RNN–LSTM đến Knowledge Graph, Deep Graph và Hệ Đa Tác tử Tự chủ  

---
""")

    print("1/10 Assembling Front Matter V2...")
    add_academic_preamble_v2(dummy_doc, p_body, h_sec)
    add_executive_summary_v2(dummy_doc, h_sec, p_body)
    add_abbreviations_v2(dummy_doc, h_sec, add_table_data)
    add_table_of_contents_v2(dummy_doc, h_sec, p_body)
    add_figures_and_tables_list_v2(dummy_doc, h_sec, p_body)

    print("2/10 Assembling MỞ ĐẦU V2...")
    add_mo_dau_v2(dummy_doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure)

    print("3/10 Assembling CHƯƠNG 1 V2...")
    add_chap1_history_v2(dummy_doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math)

    print("4/10 Assembling CHƯƠNG 2 V2...")
    add_chap2_ml_basic_v2(dummy_doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math)

    print("5/10 Assembling CHƯƠNG 3 V2...")
    add_chap3_cnn_v2(dummy_doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math)

    print("6/10 Assembling CHƯƠNG 4 V2...")
    add_chap4_rnn_v2(dummy_doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math)

    print("7/10 Assembling CHƯƠNG 5 V2...")
    add_chap5_kg_rag_v2(dummy_doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math)

    print("8/10 Assembling CHƯƠNG 6 V2...")
    add_chap6_deep_graph_v2(dummy_doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math)

    print("9/10 Assembling CHƯƠNG 7 V2...")
    add_chap7_multi_agent_v2(dummy_doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math)

    print("10/10 Assembling KẾT LUẬN & PHỤ LỤC V2...")
    add_conclusion_and_appendix_v2(dummy_doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math)

    print(f"Writing Markdown to: {MD_OUT} ...")
    content = collector.get_content()
    with open(MD_OUT, "w", encoding="utf-8") as f:
        f.write(content)

    file_size_kb = MD_OUT.stat().st_size / 1024
    print(f"Markdown build V2 completed successfully! File size: {file_size_kb:.2f} KB ({len(content.splitlines())} lines)")


if __name__ == "__main__":
    build_markdown_report_v2()
