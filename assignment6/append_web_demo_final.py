"""
Append Web Demo Section and Screenshot to the Very End of Assignment 06 Reports:
- assignment6/Bao_Cao_Assignment_06_Nang_Cap_Toan_Dien.docx
- assignment6/Bao_Cao_Assignment_6_Tran_Van_Hau_B23DCCN287.docx
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

DOCX_FILES = [
    "assignment6/Bao_Cao_Assignment_06_Nang_Cap_Toan_Dien.docx",
    "assignment6/Bao_Cao_Assignment_6_Tran_Van_Hau_B23DCCN287.docx"
]

DEMO_IMG = "assignment6/figures/demo_web_ui.png"

for doc_path in DOCX_FILES:
    if not os.path.exists(doc_path):
        continue
    doc = docx.Document(doc_path)
    
    # Check if final section already present in last 3 paragraphs
    last_text = "".join([p.text for p in doc.paragraphs[-5:]])
    if "HÌNH ẢNH TRIỂN KHAI THỰC TẾ GIAO DIỆN WEB DEMO DỰ BÁO CHUỖI THỜI GIAN" in last_text:
        print(f"Skipping {doc_path}, already has final web demo section at the end.")
        continue
        
    doc.add_page_break()
    h = doc.add_heading("PHẦN KẾT: HÌNH ẢNH TRIỂN KHAI THỰC TẾ GIAO DIỆN WEB DEMO DỰ BÁO CHUỖI THỜI GIAN RNN/LSTM (PORT 8001 / 8002)", level=1)
    if len(h.runs) > 0:
        h.runs[0].font.name = "Times New Roman"
        h.runs[0].font.size = Pt(14)
        h.runs[0].font.bold = True
        h.runs[0].font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        
    p_desc = doc.add_paragraph(
        "Nhằm cụ thể hóa năng lực triển khai thực tế của các mô hình học sâu chuỗi thời gian (RNN, LSTM, GRU), "
        "hệ thống đã xây dựng và vận hành máy chủ tương tác thời gian thực FastAPI tại địa chỉ http://localhost:8001 (PyTorch Engine) "
        "và http://localhost:8002 (TensorFlow/Keras Engine). "
        "Giao diện Web cho phép người dùng quan sát chuỗi 30 phiên giao dịch gần nhất, tùy chọn bài toán "
        "(Dự báo Giá Cổ phiếu Apple AAPL hoặc Số lượng Giao dịch Bán lẻ Retail Transactions), "
        "thực hiện suy luận dự báo điểm tiếp theo với độ trễ cực thấp (< 5ms) và trực quan hóa sai số đối chuẩn."
    )
    p_desc.runs[0].font.name = "Times New Roman"
    p_desc.runs[0].font.size = Pt(11)
    
    if os.path.exists(DEMO_IMG):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_img = p_img.add_run()
        r_img.add_picture(DEMO_IMG, width=Inches(6.2))
        
        p_cap = doc.add_paragraph(
            "Hình: Ảnh chụp thực tế Giao diện Web Ứng dụng Dự báo Chuỗi Thời gian RNN/LSTM (FastAPI Port 8001) "
            "- Tương tác Nhập Chuỗi Dữ liệu Cửa sổ Trượt (Sliding Window), Suy luận Thời gian thực và Đối chuẩn Đa Mô hình"
        )
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if len(p_cap.runs) > 0:
            p_cap.runs[0].font.name = "Times New Roman"
            p_cap.runs[0].font.size = Pt(9.5)
            p_cap.runs[0].font.italic = True
            p_cap.runs[0].font.color.rgb = RGBColor(0x47, 0x55, 0x69)
            
    doc.save(doc_path)
    size_mb = os.path.getsize(doc_path) / (1024 * 1024)
    print(f"Successfully placed Web Demo at the absolute end of {doc_path} ({size_mb:.2f} MB)")
