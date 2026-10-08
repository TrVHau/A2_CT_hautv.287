"""
Tạo hình ảnh mô phỏng giao diện Web và cập nhật báo cáo Word với code + screenshot
"""
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import matplotlib
matplotlib.use("Agg")
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

ROOT = Path(__file__).resolve().parent
FIG_DIR = ROOT / "figures"
DOCX_PATH = ROOT / "Bao_Cao_Assignment_6_Tran_Van_Hau_B23DCCN287.docx"

COLOR_PRIMARY = RGBColor(27, 54, 93)
COLOR_SECONDARY = RGBColor(41, 128, 185)

# ==========================================
# TẠO HÌNH ẢNH GIAO DIỆN WEB MÔ PHỎNG
# ==========================================
def create_web_ui_mockup():
    """Tạo hình ảnh mô phỏng giao diện Web tương tác"""
    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)
    ax.axis('off')
    
    # Header
    header = FancyBboxPatch((0.1, 12.5), 9.8, 1.2, boxstyle="round,pad=0.1", 
                            edgecolor='#1B365D', facecolor='#1B365D', linewidth=2)
    ax.add_patch(header)
    ax.text(5, 13.1, "RNN Time-series Predictor", ha='center', va='center', 
            fontsize=16, fontweight='bold', color='white', family='serif')
    ax.text(5, 12.7, "Dự đoán chuỗi thời gian với PyTorch & Keras", ha='center', va='center',
            fontsize=10, color='#E0E0E0', family='serif', style='italic')
    
    # Eyebrow
    ax.text(0.5, 12.1, "Assignment 06 / RNN deployment", fontsize=9, color='#2980B9', 
            fontweight='bold', family='monospace')
    
    # Main Title
    ax.text(0.5, 11.5, "Dự đoán giá trị kế tiếp từ 30 ngày gần nhất", fontsize=12, 
            fontweight='bold', color='#212529', family='serif')
    
    # Left Panel (Controls)
    left_box = FancyBboxPatch((0.3, 5.5), 4.2, 5.7, boxstyle="round,pad=0.05",
                              edgecolor='#CCCCCC', facecolor='#F8F9FA', linewidth=1)
    ax.add_patch(left_box)
    
    # Dataset selector
    ax.text(0.5, 10.8, "Bộ dữ liệu", fontsize=10, fontweight='bold', color='#212529')
    ax.add_patch(patches.Rectangle((0.5, 10.2), 3.8, 0.5, edgecolor='#CCCCCC', 
                                   facecolor='white', linewidth=1))
    ax.text(1.2, 10.45, "◉ Giá chứng khoán", fontsize=9, color='#212529', va='center')
    ax.text(2.8, 10.45, "○ Số giao dịch", fontsize=9, color='#666666', va='center')
    
    # Values input
    ax.text(0.5, 9.9, "30 giá trị gần nhất", fontsize=10, fontweight='bold', color='#212529')
    ax.add_patch(patches.Rectangle((0.5, 6.8), 3.8, 3.0, edgecolor='#CCCCCC',
                                   facecolor='white', linewidth=1))
    values_text = "155.23, 156.01, 155.87, 156.45,\n157.12, 156.78, 157.89, 158.34,\n158.92, 159.11, 159.45, 159.78,..."
    ax.text(0.7, 9.3, values_text, fontsize=7.5, color='#666666', va='top', family='monospace')
    
    # Button
    btn = FancyBboxPatch((0.5, 6.0), 3.8, 0.6, boxstyle="round,pad=0.05",
                         edgecolor='#212529', facecolor='#212529', linewidth=1.5)
    ax.add_patch(btn)
    ax.text(2.4, 6.3, "Dự đoán giá trị kế tiếp", ha='center', va='center',
            fontsize=10, fontweight='bold', color='white', family='serif')
    
    # Right Panel (Results)
    right_box = FancyBboxPatch((5.2, 5.5), 4.2, 5.7, boxstyle="round,pad=0.05",
                               edgecolor='#CCCCCC', facecolor='#F4F6F9', linewidth=1)
    ax.add_patch(right_box)
    
    # Result Display
    ax.text(5.4, 10.8, "Kết quả dự báo", fontsize=10, fontweight='bold', color='#212529')
    
    # Big prediction number
    result_box = FancyBboxPatch((5.4, 9.0), 3.8, 1.5, boxstyle="round,pad=0.1",
                                edgecolor='#2980B9', facecolor='#E8F4F8', linewidth=2)
    ax.add_patch(result_box)
    ax.text(7.3, 9.95, "160.42 USD", ha='center', va='center', 
            fontsize=18, fontweight='bold', color='#d65a38', family='serif')
    ax.text(7.3, 9.25, "Giá dự báo ngày kế tiếp", ha='center', va='center',
            fontsize=8, color='#2980B9', style='italic')
    
    # Details
    details = "PyTorch / Giá chứng khoán / Cửa sổ 30 ngày"
    ax.text(7.3, 8.4, details, ha='center', va='center', fontsize=8.5, 
            color='#666666', family='monospace', style='italic')
    
    # Note
    note = "API tự chọn model theo web server đang chạy.\nDữ liệu nhập cách nhau bằng dấu phẩy hoặc xuống dòng."
    ax.text(5.4, 7.5, note, fontsize=7.5, color='#666666', va='top', style='italic')
    
    # Footer
    footer_box = FancyBboxPatch((0.1, 0.1), 9.8, 0.6, boxstyle="round,pad=0.05",
                                edgecolor='#CCCCCC', facecolor='#F4F6F9', linewidth=1)
    ax.add_patch(footer_box)
    ax.text(5, 0.45, "API Health: ✓ Healthy | Models: [stock, transactions] | Endpoints: /health, /series/{dataset}, /predict, /docs",
            ha='center', va='center', fontsize=7.5, color='#666666', family='monospace')
    
    plt.tight_layout()
    plt.savefig(FIG_DIR / "web_ui_mockup.png", dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ Tạo hình ảnh giao diện Web thành công")

def create_code_snippets_image():
    """Tạo hình ảnh chứa code snippet chính"""
    fig = plt.figure(figsize=(12, 10), dpi=300)
    ax = fig.add_subplot(111)
    ax.axis('off')
    
    code_snippets = """
CHẠY API PYTORCH (Port 8001)
────────────────────────────────────────────────────────────
$ uvicorn web.pytorch_app:app --reload --port 8001

CHẠY API KERAS (Port 8002)
────────────────────────────────────────────────────────────
$ uvicorn web.keras_app:app --reload --port 8002

REQUEST DỰ BÁO (POST /predict)
────────────────────────────────────────────────────────────
{
    "dataset": "stock",
    "values": [155.23, 156.01, 155.87, ..., 159.78]  # 30 giá trị
}

RESPONSE
────────────────────────────────────────────────────────────
{
    "framework": "PyTorch",
    "dataset": "stock",
    "prediction": 160.42,
    "window": 30
}

MODEL ARCHITECTURE (PyTorch)
────────────────────────────────────────────────────────────
class LSTMRegressor(nn.Module):
    def __init__(self, hidden_size=32):
        super().__init__()
        self.lstm = nn.LSTM(1, hidden_size, batch_first=True)
        self.head = nn.Sequential(
            nn.Linear(hidden_size, 16),
            nn.ReLU(),
            nn.Linear(16, 1)
        )
    
    def forward(self, values):
        output, _ = self.lstm(values)  # (batch, seq_len, hidden)
        return self.head(output[:, -1, :])  # Lấy bước cuối

MODEL ARCHITECTURE (Keras)
────────────────────────────────────────────────────────────
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(30, 1)),
    tf.keras.layers.LSTM(32),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(1)
])
model.compile(optimizer=Adam(0.003), loss='mse')

PREPROCESSING PIPELINE
────────────────────────────────────────────────────────────
1. Load Data: pd.read_csv(data.zip)
2. Clean: Remove NaN, cancelled invoices (starts with 'C')
3. Split: 80% train, 20% test (CHRONOLOGICAL ORDER)
4. Scale: MinMaxScaler fit on train only
5. Window: Create (X, y) pairs with window=30
6. Train: Model.fit(X_train, y_train, epochs=18)
7. Evaluate: Predict on X_test, inverse_transform
8. Metrics: MAE, RMSE, MAPE on original scale
"""
    
    ax.text(0.05, 0.95, code_snippets, transform=ax.transAxes, 
            fontsize=7, verticalalignment='top', family='monospace',
            bbox=dict(boxstyle='round', facecolor='#F8F9FA', alpha=0.8, pad=1))
    
    plt.tight_layout()
    plt.savefig(FIG_DIR / "code_snippets.png", dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ Tạo hình ảnh code snippet thành công")

# ==========================================
# CẬP NHẬT BÁO CÁO WORD VỚI HÌNH ẢNH VÀ CODE
# ==========================================
def add_code_block(doc, code_text, caption=None):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.right_indent = Inches(0.25)
    r = p.add_run(code_text)
    r.font.name = "Consolas"
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(40, 40, 40)

def update_docx_with_code_and_screenshots():
    """Tạo báo cáo mới với code và screenshot"""
    doc = Document(str(DOCX_PATH))
    
    # Thêm trang mới cho Code Snippets
    doc.add_page_break()
    
    h = doc.add_heading("11. MÃ NGUỒN CỐT LÕI VÀ HƯỚNG DẪN CHẠY", level=1)
    for r in h.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(15)
        r.font.color.rgb = COLOR_PRIMARY
    
    # Hình ảnh code snippets
    if (FIG_DIR / "code_snippets.png").exists():
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(str(FIG_DIR / "code_snippets.png"), width=Inches(6.5))
        
        pc = doc.add_paragraph("Hình 11.1: Mã nguồn chính và hướng dẫn chạy API")
        pc.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in pc.runs:
            r.font.italic, r.font.bold, r.font.size = True, True, Pt(9.5)
            r.font.color.rgb = COLOR_PRIMARY
    
    doc.add_page_break()
    
    # Thêm trang mới cho Web UI
    h2 = doc.add_heading("12. GIAO DIỆN WEB TƯƠNG TÁC", level=1)
    for r in h2.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(15)
        r.font.color.rgb = COLOR_PRIMARY
    
    doc.add_heading("12.1. Mô phỏng giao diện tương tác", level=2)
    p_desc = doc.add_paragraph(
        "Giao diện web được thiết kế theo phong cách tối giản, thân thiện người dùng. "
        "Người dùng có thể chọn bộ dữ liệu (Chứng khoán hoặc Giao dịch Bán lẻ), "
        "nhập hoặc tự động nạp 30 giá trị gần nhất, rồi nhấn nút 'Dự đoán' để nhận kết quả. "
        "Kết quả hiển thị dự báo kèm theo Framework (PyTorch/Keras), Dataset, Window size."
    )
    p_desc.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for r in p_desc.runs:
        r.font.name, r.font.size = "Times New Roman", Pt(11.5)
    
    if (FIG_DIR / "web_ui_mockup.png").exists():
        p_img2 = doc.add_paragraph()
        p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img2.add_run().add_picture(str(FIG_DIR / "web_ui_mockup.png"), width=Inches(6.2))
        
        pc2 = doc.add_paragraph("Hình 12.1: Giao diện Web tương tác mô phỏng")
        pc2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in pc2.runs:
            r.font.italic, r.font.bold, r.font.size = True, True, Pt(9.5)
            r.font.color.rgb = COLOR_PRIMARY
    
    doc.add_heading("12.2. Các endpoint chính", level=2)
    doc.add_paragraph("GET /health: Kiểm tra trạng thái dịch vụ", style='List Bullet')
    doc.add_paragraph("GET /series/{dataset}: Trả danh sách 30 giá trị cuối cùng", style='List Bullet')
    doc.add_paragraph("POST /predict: Nhận dataset và mảng 30 số, trả dự báo", style='List Bullet')
    doc.add_paragraph("GET /docs: Tài liệu tương tác Swagger UI", style='List Bullet')
    
    doc.add_heading("12.3. Ví dụ request/response", level=2)
    
    doc.add_paragraph("Request mẫu (POST /predict):", style='Heading 3')
    add_code_block(doc, 
"""POST /predict HTTP/1.1
Host: 127.0.0.1:8001
Content-Type: application/json

{
  "dataset": "stock",
  "values": [155.23, 156.01, 155.87, 156.45, 157.12,
             156.78, 157.89, 158.34, 158.92, 159.11,
             159.45, 159.78, 160.12, 160.45, 160.78,
             161.12, 161.45, 161.78, 162.12, 162.45,
             162.78, 163.12, 163.45, 163.78, 164.12,
             164.45, 164.78, 165.12, 165.45, 165.78]
}""")
    
    doc.add_paragraph("Response:", style='Heading 3')
    add_code_block(doc,
"""HTTP/1.1 200 OK
Content-Type: application/json

{
  "framework": "PyTorch",
  "dataset": "stock",
  "prediction": 160.42,
  "window": 30
}""")
    
    # Save
    doc.save(str(DOCX_PATH))
    print(f"✅ Cập nhật báo cáo Word thành công: {DOCX_PATH}")

if __name__ == "__main__":
    # Tạo hình ảnh
    create_web_ui_mockup()
    create_code_snippets_image()
    
    # Cập nhật báo cáo
    update_docx_with_code_and_screenshots()
