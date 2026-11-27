# -*- coding: utf-8 -*-
"""
Convert V2 DOCX to PDF using Word COM and verify page count.
Author: Tran Van Hau (B23DCCN287)
"""

import os
import sys
import time
from pathlib import Path

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

import win32com.client
import pymupdf

ROOT = Path("c:/code/A2_CT_hautv.287").resolve()
FINAL_DIR = ROOT / "tieuluan_final"
DOCX_PATH = FINAL_DIR / "tieuluan_final_CT_09_Hautv.287_v2.docx"
PDF_PATH = FINAL_DIR / "tieuluan_final_CT_09_Hautv.287_v2.pdf"

print("==================================================")
print(f"CONVERTING DOCX TO PDF VIA WORD COM")
print(f"Input DOCX: {DOCX_PATH}")
print(f"Output PDF: {PDF_PATH}")
print("==================================================")

if not DOCX_PATH.exists():
    print(f"ERROR: File not found: {DOCX_PATH}")
    sys.exit(1)

# Initialize Word Application
word = None
doc = None
try:
    print("Launching Microsoft Word COM application...")
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0

    print("Opening DOCX document...")
    doc = word.Documents.Open(str(DOCX_PATH), ReadOnly=True)

    # Update all fields in document (TOC, page numbers, etc.)
    try:
        print("Updating fields in document body and footers...")
        doc.Fields.Update()
        for sec in doc.Sections:
            sec.Footers(1).Range.Fields.Update()
            sec.Headers(1).Range.Fields.Update()
    except Exception as e:
        print(f"Warning: Could not update all fields: {e}")

    # wdFormatPDF = 17
    wdFormatPDF = 17
    print(f"Exporting to PDF: {PDF_PATH} ...")
    doc.SaveAs(str(PDF_PATH), FileFormat=wdFormatPDF)
    print("SaveAs PDF complete!")

except Exception as e:
    print(f"ERROR during Word COM conversion: {e}")
    sys.exit(1)
finally:
    if doc:
        try:
            doc.Close(SaveChanges=0)
        except Exception:
            pass
    if word:
        try:
            word.Quit()
        except Exception:
            pass

time.sleep(1)

if not PDF_PATH.exists():
    print("ERROR: PDF output was not created!")
    sys.exit(1)

file_size_mb = PDF_PATH.stat().st_size / (1024 * 1024)
print(f"PDF created successfully! File size: {file_size_mb:.2f} MB")

# Verify Page Count with PyMuPDF
doc_pdf = pymupdf.open(str(PDF_PATH))
page_count = len(doc_pdf)
print(f"Total pages in PDF: {page_count} pages")

# Inspect Table of Contents / Outline
toc = doc_pdf.get_toc()
print(f"TOC entries found in PDF metadata: {len(toc)}")

doc_pdf.close()
print("==================================================")
