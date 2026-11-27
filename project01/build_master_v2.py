#!/usr/bin/env python3
"""
Master Build Runner for Project 01 V2 Report:
Compiles all 11 chapter modules into:
  - project01/Bao_Cao_Project01_CT_09_Hautv_v2.docx
  - project01/project01_CT_09_hautv_v2.pdf
  - ./project01_CT_09_hautv_v2.pdf
And syncs to default report files.
"""

import os
import sys
import time
import shutil
import docx
import win32com.client

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_ROOT = os.path.dirname(CURRENT_DIR)
BUILDER_DIR = os.path.join(CURRENT_DIR, "builder_v2")

sys.path.insert(0, BUILDER_DIR)

from part00_front_matter import build_front_matter
from part01_introduction import build_chapter1
from part02_mas_theory import build_chapter2
from part03_council_architecture import build_chapter3
from part04_data_engineering import build_chapter4
from part05_ml_dl_parity import build_chapter5
from part06_neo4j_graph_rag import build_chapter6
from part07_reinforcement_learning import build_chapter7
from part08_explainability_safety import build_chapter8
from part09_code_and_demo import build_chapter9
from part10_discussion_conclusion import build_chapter10
from part11_appendix_code import build_appendix

OUT_DOCX_V2 = os.path.join(CURRENT_DIR, "Bao_Cao_Project01_CT_09_Hautv_v2.docx")
OUT_PDF_V2 = os.path.join(CURRENT_DIR, "project01_CT_09_hautv_v2.pdf")
ROOT_PDF_V2 = os.path.join(WORKSPACE_ROOT, "project01_CT_09_hautv_v2.pdf")

# Standard paths to keep in sync
OUT_DOCX_DEFAULT = os.path.join(CURRENT_DIR, "Bao_Cao_Project01_CT_09_Hautv.287.docx")
OUT_PDF_DEFAULT = os.path.join(CURRENT_DIR, "project01_CT_09_hautv.pdf")
ROOT_PDF_DEFAULT = os.path.join(WORKSPACE_ROOT, "project01_CT_09_hautv.pdf")

def main():
    print("=" * 80)
    print("PROJECT 01 V2 MASTER ACADEMIC REPORT COMPILER")
    print("Author: Tran Van Hau (MSSV: B23DCCN287 - Nhom CT_09)")
    print("Supervisor: PGS. TS. Tran Dinh Que")
    print("=" * 80)

    t0 = time.time()
    doc = docx.Document()

    print("[*] Stage 1: Assembling all 11 comprehensive chapters...")
    build_front_matter(doc)
    build_chapter1(doc)
    build_chapter2(doc)
    build_chapter3(doc)
    build_chapter4(doc)
    build_chapter5(doc)
    build_chapter6(doc)
    build_chapter7(doc)
    build_chapter8(doc)
    build_chapter9(doc)
    build_chapter10(doc)
    build_appendix(doc)

    print(f"[*] Saving Word Document to: {OUT_DOCX_V2}")
    doc.save(OUT_DOCX_V2)
    # Also sync to default docx
    shutil.copy2(OUT_DOCX_V2, OUT_DOCX_DEFAULT)
    print(f"[V] Word document saved successfully! Size: {os.path.getsize(OUT_DOCX_V2)/(1024*1024):.2f} MB")

    # Word stats
    paragraphs = len(doc.paragraphs)
    tables = len(doc.tables)
    words = sum(len(p.text.split()) for p in doc.paragraphs)
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                words += sum(len(p.text.split()) for p in cell.paragraphs)
    print(f"    • Paragraphs: {paragraphs}")
    print(f"    • Tables: {tables}")
    print(f"    • Total Words: {words:,} words")

    print("[*] Stage 2: Exporting Word Document to High-Definition PDF via Word COM...")
    word = None
    try:
        word = win32com.client.DispatchEx("Word.Application")
        word.Visible = False
        word.DisplayAlerts = 0  # wdAlertsNone

        doc_word = word.Documents.Open(
            os.path.abspath(OUT_DOCX_V2),
            ReadOnly=True,
            ConfirmConversions=False,
            AddToRecentFiles=False
        )
        
        # Update Table of Contents / Fields if any
        try:
            doc_word.Fields.Update()
        except Exception:
            pass

        print(f"    • Word reports total pages: {doc_word.ComputeStatistics(2)}")  # 2: wdStatisticPages

        # Export PDF
        doc_word.ExportAsFixedFormat(
            os.path.abspath(OUT_PDF_V2),
            17,  # wdExportFormatPDF
            OpenAfterExport=False,
            OptimizeFor=0  # wdExportOptimizeForPrint
        )
        doc_word.Close(SaveChanges=False)
        print(f"[V] PDF V2 successfully created at: {OUT_PDF_V2}")

        # Copy to root and default locations
        shutil.copy2(OUT_PDF_V2, ROOT_PDF_V2)
        shutil.copy2(OUT_PDF_V2, OUT_PDF_DEFAULT)
        shutil.copy2(OUT_PDF_V2, ROOT_PDF_DEFAULT)
        print(f"[V] Synchronized PDF to root: {ROOT_PDF_V2}")
        print(f"[V] Synchronized PDF to default: {OUT_PDF_DEFAULT}")

    except Exception as e:
        print(f"[X] Error exporting to PDF via Word: {e}")
    finally:
        if word is not None:
            try:
                word.Quit()
            except Exception:
                pass

    elapsed = time.time() - t0
    print("=" * 80)
    print(f"[V] PROJECT 01 V2 BUILD COMPLETED IN {elapsed:.1f} SECONDS!")
    print(f"    - Word V2: {OUT_DOCX_V2}")
    print(f"    - PDF V2:  {OUT_PDF_V2}")
    print("=" * 80)

if __name__ == "__main__":
    main()
