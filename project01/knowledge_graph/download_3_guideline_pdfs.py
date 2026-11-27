#!/usr/bin/env python3
"""
Download 3 Official Clinical Guideline PDFs for Knowledge Graph Construction:
1. ADA Standards of Care in Diabetes 2024 (Full 345-page official supplement)
2. Bộ Y tế Việt Nam - Quyết định số 5481/QĐ-BYT (Hướng dẫn chẩn đoán & điều trị ĐTĐ típ 2)
3. KDIGO 2023 Clinical Practice Guideline for Diabetes Management in Chronic Kidney Disease
"""

import os
import sys
import ssl
import time
import urllib.request

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(CURRENT_DIR, "documents")
os.makedirs(DOCS_DIR, exist_ok=True)

PDF_SOURCES = [
    {
        "id": "ADA_2024",
        "name": "American Diabetes Association (ADA 2024 Standards of Care in Diabetes)",
        "filename": "ADA_Standards_of_Care_2024.pdf",
        "official_url": "https://diabetesjournals.org/care/issue/47/Supplement_1",
        "download_url": "https://www.sochob.cl/web1/wp-content/uploads/2023/12/Standards-of-Care-in-Diabetes%E2%80%942024.pdf"
    },
    {
        "id": "BYT_QD5481",
        "name": "Bộ Y tế Việt Nam (Quyết định 5481/QĐ-BYT - Hướng dẫn chẩn đoán và điều trị ĐTĐ típ 2)",
        "filename": "BYT_QD5481_Huong_Dan_Chan_Doan_Dieu_Tri_Dai_Thao_Duong_Tip_2.pdf",
        "official_url": "https://kcb.vn/van-ban/quyet-dinh-so-5481-qd-byt-ve-viec-ban-hanh-tai-lieu-chuyen-mon-huong-dan-chan-doan-va-dieu-tri-dai-thao-duong-tip-2.html",
        "download_url": "https://file.medinet.gov.vn/%2fdata%2fsoytehcm%5ctytphuongphuthuan%5cattachments%2f2026_8%2fbyt_qd_so_5481_qd-byt_ngay_30122020_ve_viec_ban_hanh_tai_lieu_chuyen_mon_huong__38202614.pdf"
    },
    {
        "id": "KDIGO_2023",
        "name": "Hiệp hội Thận học Quốc tế (KDIGO 2023 Guideline for Diabetes Management in CKD)",
        "filename": "KDIGO_2023_Clinical_Practice_Guideline_Diabetes_CKD.pdf",
        "official_url": "https://kdigo.org/guidelines/diabetes-ckd/",
        "download_url": "https://kdigo.org/wp-content/uploads/2022/10/KDIGO-2022-Clinical-Practice-Guideline-for-Diabetes-Management-in-CKD.pdf"
    }
]

def download_file(url, target_path):
    print(f"[*] Downloading: {url}")
    print(f"    -> Destination: {target_path}")
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/pdf,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }
    
    req = urllib.request.Request(url, headers=headers)
    
    t0 = time.time()
    with urllib.request.urlopen(req, context=ctx, timeout=60) as response, open(target_path, 'wb') as out_file:
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        chunk_size = 65536
        
        while True:
            chunk = response.read(chunk_size)
            if not chunk:
                break
            out_file.write(chunk)
            downloaded += len(chunk)
            if total_size > 0:
                percent = downloaded * 100 / total_size
                print(f"\r    Progress: {downloaded/(1024*1024):.1f}/{total_size/(1024*1024):.1f} MB ({percent:.1f}%)", end="", flush=True)
            else:
                print(f"\r    Downloaded: {downloaded/(1024*1024):.1f} MB", end="", flush=True)
                
    elapsed = time.time() - t0
    final_size = os.path.getsize(target_path) / (1024 * 1024)
    print(f"\n[V] Completed in {elapsed:.1f}s ({final_size:.2f} MB)")

def main():
    print("=" * 80)
    print("DOWNLOAD OFFICIAL CLINICAL GUIDELINE PDFS FOR KNOWLEDGE BASE (3 SOURCES)")
    print("=" * 80)
    
    for item in PDF_SOURCES:
        target = os.path.join(DOCS_DIR, item["filename"])
        print(f"\n[+] {item['name']}:")
        print(f"    • Official Reference URL: {item['official_url']}")
        if os.path.exists(target) and os.path.getsize(target) > 500000:
            print(f"    [!] File already exists: {target} ({os.path.getsize(target)/(1024*1024):.2f} MB). Skipping.")
            continue
        try:
            download_file(item["download_url"], target)
        except Exception as e:
            print(f"    [X] Error downloading {item['filename']}: {e}")

    print("\n" + "=" * 80)
    print(f"Directory contents of {DOCS_DIR}:")
    for f in os.listdir(DOCS_DIR):
        fp = os.path.join(DOCS_DIR, f)
        print(f"  • {f} ({os.path.getsize(fp)/(1024*1024):.2f} MB)")
    print("=" * 80)

if __name__ == "__main__":
    main()
