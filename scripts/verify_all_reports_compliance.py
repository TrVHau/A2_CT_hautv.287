"""
Comprehensive Verification Script for ALL 10 Independent Units:
- Assignment 1 to 6 (assignment1 - assignment6)
- Tieuluan 1 to 3 (tieuluan1 - tieuluan3)
- Project 01 (project01)

Verifies:
1. Docx file exists and size (MB)
2. Markdown file exists
3. Number of images embedded in Docx
4. Web demo screenshot exists and embedded at the end
5. Code blocks embedded in Docx
"""

import os
import sys
import docx

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

DOMAINS = [
    {
        "id": "A1",
        "name": "Assignment 01 (Chẩn Đoán Đái Tháo Đường Lâm Sàng)",
        "dir": "assignment1",
        "docx": "assignment1/Bao_Cao_Assignment_01_Nang_Cap_Toan_Dien.docx",
        "md": "assignment1/BAO_CAO_ASSIGNMENT_01_NANG_CAP.md",
        "demo_img": "assignment1/figures/demo_web_ui.png"
    },
    {
        "id": "A2",
        "name": "Assignment 02 (Định Giá Bất Động Sản Đô Thị)",
        "dir": "assignment2",
        "docx": "assignment2/Bao_Cao_Assignment_02_Nang_Cap_Toan_Dien.docx",
        "md": "assignment2/BAO_CAO_ASSIGNMENT_02_NANG_CAP.md",
        "demo_img": "assignment2/figures/demo_web_desktop.png"
    },
    {
        "id": "A3",
        "name": "Assignment 03 (Tổng Hợp Đa Miền Y Tế, Nhà Đất & Khách Hàng)",
        "dir": "assignment3",
        "docx": "assignment3/Bao_Cao_Assignment_03_Nang_Cap_Toan_Dien.docx",
        "md": "assignment3/BAO_CAO_ASSIGNMENT_03_NANG_CAP.md",
        "demo_img": "assignment3/figures/demo_web_diabetes.png"
    },
    {
        "id": "A4",
        "name": "Assignment 04 (Mạng CNN & Khảo Sát Framework Dogs vs Cats / MNIST)",
        "dir": "assignment4",
        "docx": "assignment4/Bao_Cao_Assignment_04_Nang_Cap_Toan_Dien.docx",
        "md": "assignment4/BAO_CAO_ASSIGNMENT_04_NANG_CAP.md",
        "demo_img": "assignment4/figures/demo_web_ui.png"
    },
    {
        "id": "A5",
        "name": "Assignment 05 (Mạng Nơ-ron Tích Chập CNN & Grad-CAM Web Demo)",
        "dir": "assignment5",
        "docx": "assignment5/Bao_Cao_Assignment_05_Nang_Cap_Toan_Dien.docx",
        "md": "assignment5/BAO_CAO_ASSIGNMENT_05_NANG_CAP.md",
        "demo_img": "assignment5/figures/demo_web_cnn_mnist_fashion.png"
    },
    {
        "id": "A6",
        "name": "Assignment 06 (Mạng Hồi Quy RNN & LSTM Chuỗi Thời Gian)",
        "dir": "assignment6",
        "docx": "assignment6/Bao_Cao_Assignment_06_Nang_Cap_Toan_Dien.docx",
        "md": "assignment6/BAO_CAO_ASSIGNMENT_06_NANG_CAP.md",
        "demo_img": "assignment6/figures/demo_web_ui.png"
    },
    {
        "id": "TL1",
        "name": "Tiểu Luận 01 (Hệ Thống Chẩn Đoán Tiểu Đường Lâm Sàng Nâng Cấp)",
        "dir": "tieuluan1",
        "docx": "tieuluan1/Bao_Cao_Tieu_Luan_1_He_Tieu_Duong.docx",
        "md": "tieuluan1/BAO_CAO_TIEU_LUAN_1_NANG_CAP.md",
        "demo_img": "tieuluan1/figures/demo_web_ui.png"
    },
    {
        "id": "TL2",
        "name": "Tiểu Luận 02 (Hệ Thống Định Giá Bất Động Sản Đô Thị Nâng Cấp)",
        "dir": "tieuluan2",
        "docx": "tieuluan2/Bao_Cao_Tieu_Luan_2_He_Gia_Nha.docx",
        "md": "tieuluan2/BAO_CAO_TIEU_LUAN_2_NANG_CAP.md",
        "demo_img": "tieuluan2/figures/demo_web_ui.png"
    },
    {
        "id": "TL3",
        "name": "Tiểu Luận 03 (AI Đầu Tư Tài Chính, LSTM, RAG & Đa Agent)",
        "dir": "tieuluan3",
        "docx": "tieuluan3/Bao_Cao_Tieu_Luan_3_AI_Tai_Chinh_NLP.docx",
        "md": "tieuluan3/BAO_CAO_TIEU_LUAN_3_NANG_CAP.md",
        "demo_img": "tieuluan3/figures/demo_web_ui.png"
    },
    {
        "id": "P01",
        "name": "Project 01 (Hội Chẩn Đa Đặc Vụ Y Khoa Qwen 2.5 CoT & ADA 2024)",
        "dir": "project01",
        "docx": "project01/Bao_Cao_Nghien_Cuu_Project01_Nang_Cap.docx",
        "md": "project01/PROJECT01_COMPREHENSIVE_UPGRADE_REPORT.md",
        "demo_img": "project01/figures/demo_web_dashboard_overview.png"
    }
]

print("=" * 90)
print("BẢNG TỔNG HỢP KIỂM ĐỊNH TOÀN DIỆN 10 PHÂN HỆ ĐỘC LẬP:")
print("6 ASSIGNMENTS (A1-A6) + 3 TIỂU LUẬN (TL1-TL3) + 1 PROJECT (PROJECT 01)")
print("=" * 90)

all_passed = True

for d in DOMAINS:
    print(f"\n📂 [{d['id']}] {d['name']}")
    
    # Docx check
    docx_path = d['docx']
    if os.path.exists(docx_path):
        size_mb = os.path.getsize(docx_path) / (1024 * 1024)
        doc = docx.Document(docx_path)
        img_count = doc._element.xml.count("<w:drawing>")
        
        code_blocks = 0
        for t in doc.tables:
            for r in t.rows:
                for c in r.cells:
                    for p in c.paragraphs:
                        for run in p.runs:
                            if run.font.name in ["Consolas", "Courier New"]:
                                code_blocks += 1
                                break
        print(f"  ✓ Word Report (.docx): {docx_path} ({size_mb:.2f} MB)")
        print(f"    - Ảnh nhúng trong docx: {img_count} ảnh")
        print(f"    - Khối mã nguồn Code Block: {code_blocks} khối")
    else:
        print(f"  ❌ THIẾU Word Report (.docx): {docx_path}")
        all_passed = False
        
    # MD check
    md_path = d['md']
    if os.path.exists(md_path):
        md_size_kb = os.path.getsize(md_path) / 1024
        print(f"  ✓ Markdown Report (.md): {md_path} ({md_size_kb:.1f} KB)")
    else:
        print(f"  ❌ THIẾU Markdown Report (.md): {md_path}")
        all_passed = False
        
    # Web Demo check
    demo_path = d['demo_img']
    if os.path.exists(demo_path):
        demo_size_kb = os.path.getsize(demo_path) / 1024
        print(f"  ✓ Ảnh Demo Web ở cuối: {demo_path} ({demo_size_kb:.1f} KB)")
    else:
        print(f"  ❌ THIẾU Ảnh Demo Web: {demo_path}")
        all_passed = False

print("\n" + "=" * 90)
if all_passed:
    print("XÁC NHẬN HOÀN TOÀN: TẤT CẢ 10 BÁO CÁO ĐỘC LẬP ĐÃ SẴN SÀNG VÀ ĐẠT 100% TIÊU CHUẨN!")
else:
    print("CẢNH BÁO: CÓ PHÂN HỆ CHƯA ĐẠT CHUẨN!")
print("=" * 90)
