#!/usr/bin/env python3
"""
Convert Project 01 Master Word Report to PDF:
Input:  project01/Bao_Cao_Project01_CT_09_Hautv.287.docx (9.18 MB)
Output: project01/project01_CT_09_hautv.pdf and ./project01_CT_09_hautv.pdf
"""

import os
import sys
import time
import shutil
import win32com.client

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)

docx_path = os.path.join(CURRENT_DIR, "Bao_Cao_Project01_CT_09_Hautv.287.docx")
pdf_path_project = os.path.join(CURRENT_DIR, "project01_CT_09_hautv.pdf")
pdf_path_root = os.path.join(ROOT_DIR, "project01_CT_09_hautv.pdf")

if not os.path.exists(docx_path):
    print(f"[X] DOCX file not found: {docx_path}")
    sys.exit(1)

print(f"[*] Bat dau chuyen doi Báo cáo sang PDF...")
print(f"    - DOCX Nguon: {docx_path} ({os.path.getsize(docx_path)/(1024*1024):.2f} MB)")
print(f"    - PDF Dich 1: {pdf_path_project}")
print(f"    - PDF Dich 2: {pdf_path_root}")

t0 = time.time()
word = None
try:
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0  # wdAlertsNone
    
    print("[*] Dang mo tai lieu trong Microsoft Word...")
    doc = word.Documents.Open(
        os.path.abspath(docx_path),
        ReadOnly=True,
        ConfirmConversions=False,
        AddToRecentFiles=False
    )
    
    print(f"[*] Tai lieu da mo thanh cong ({doc.Paragraphs.Count} doan van). Dang xuat PDF...")
    # 17: wdExportFormatPDF
    # OptimizeFor: 0 (wdExportOptimizeForPrint)
    doc.ExportAsFixedFormat(
        os.path.abspath(pdf_path_project),
        17,
        OpenAfterExport=False,
        OptimizeFor=0
    )
    
    doc.Close(SaveChanges=False)
    print(f"[V] Da tao PDF tai project01: {pdf_path_project}")
    
    # Also copy to root for convenient access
    shutil.copy2(pdf_path_project, pdf_path_root)
    print(f"[V] Da sao chep PDF ra thu muc goc: {pdf_path_root}")
    
    elapsed = time.time() - t0
    pdf_size_mb = os.path.getsize(pdf_path_project) / (1024 * 1024)
    print(f"[V] CHUYEN DOI PDF HOAN TAT TRONG {elapsed:.1f}s!")
    print(f"    - Dung luong PDF: {pdf_size_mb:.2f} MB")

except Exception as e:
    print(f"[X] Loi khi chuyen doi sang PDF: {e}")
    sys.exit(1)
finally:
    if word is not None:
        try:
            word.Quit()
        except Exception:
            pass
