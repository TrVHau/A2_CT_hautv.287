"""
Append Web Demo Screenshot to Assignment 04 Reports:
- assignment4/Bao_Cao_Assignment_04_Nang_Cap_Toan_Dien.docx
- assignment4/A04_CT_hautv.287.docx
- assignment4/A4_CT_hautv.287.docx
- assignment4/Assignment4_Report.docx
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

DOCX_TARGETS = [
    "assignment4/Bao_Cao_Assignment_04_Nang_Cap_Toan_Dien.docx",
    "assignment4/A04_CT_hautv.287.docx",
    "assignment4/A4_CT_hautv.287.docx",
    "assignment4/Assignment4_Report.docx"
]

IMG_DOGCAT = "assignment4/figures/demo_web_dogcat.png"
IMG_MNIST = "assignment4/figures/demo_web_mnist_canvas.png"

for target_path in DOCX_TARGETS:
    if not os.path.exists(target_path):
        continue
    doc = docx.Document(target_path)
    
    # Check if demo already added
    has_demo = False
    for p in doc.paragraphs[-15:]:
        if "demo_web" in p.text or "HÌNH ẢNH TRIỂN KHAI THỰC TẾ GIAO DIỆN WEB DEMO" in p.text:
            has_demo = True
            break
            
    if not has_demo:
        doc.add_page_break()
        h_demo = doc.add_heading("IV. HÌNH ẢNH TRIỂN KHAI THỰC TẾ GIAO DIỆN WEB DEMO (PORT 5004)", level=1)
        if len(h_demo.runs) > 0:
            h_demo.runs[0].font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
        
        p_desc = doc.add_paragraph(
            "Nhằm trực quan hóa sản phẩm nghiên cứu và tạo điều kiện kiểm thử thực tế đa nền tảng, "
            "hệ thống đã triển khai ứng dụng Web tương tác thời gian thực tại địa chỉ http://localhost:5004. "
            "Giao diện cho phép người dùng lựa chọn ảnh ngẫu nhiên từ tập dữ liệu Dogs vs Cats và vẽ tương tác số viết tay MNIST, "
            "lựa chọn engine thực thi (PyTorch, TensorFlow/Keras hoặc NumPy Scratch) và quan sát xác suất dự báo tức thì."
        )
        
        if os.path.exists(IMG_DOGCAT):
            p_img1 = doc.add_paragraph()
            p_img1.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_img1 = p_img1.add_run()
            r_img1.add_picture(IMG_DOGCAT, width=Inches(6.2))
            
            p_cap1 = doc.add_paragraph(
                "Hình: Ảnh chụp thực tế Giao diện Web Ứng dụng Phân loại Thị giác Máy tính CNN Dogs vs Cats (Port 5004) "
                "- Tương tác Lựa chọn Mẫu Ảnh, Chuyển đổi Đa Framework (PyTorch/Keras/NumPy) và Thanh Xác suất Dự báo"
            )
            p_cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if len(p_cap1.runs) > 0:
                p_cap1.runs[0].font.size = Pt(8.5)
                p_cap1.runs[0].font.italic = True
                p_cap1.runs[0].font.color.rgb = RGBColor(0x47, 0x55, 0x69)

        if os.path.exists(IMG_MNIST):
            p_img2 = doc.add_paragraph()
            p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_img2 = p_img2.add_run()
            r_img2.add_picture(IMG_MNIST, width=Inches(6.2))
            
            p_cap2 = doc.add_paragraph(
                "Hình: Giao diện Nhận diện Chữ số Viết tay MNIST Canvas Tương tác Thời gian thực (Port 5004) "
                "- Bảng vẽ Trực quan HTML5 Canvas và Phân phối Xác suất Softmax 10 Chữ số"
            )
            p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if len(p_cap2.runs) > 0:
                p_cap2.runs[0].font.size = Pt(8.5)
                p_cap2.runs[0].font.italic = True
                p_cap2.runs[0].font.color.rgb = RGBColor(0x47, 0x55, 0x69)

        doc.save(target_path)
        size_mb = os.path.getsize(target_path) / (1024 * 1024)
        print(f"Appended web demo to {target_path} ({size_mb:.2f} MB)")
    else:
        print(f"Already had web demo: {target_path}")

