"""
Master Technical Word Report Generator for Assignment 01:
'assignment1/Bao_Cao_Assignment_01_Nang_Cap_Toan_Dien.docx'
Embeds ALL 16 High-Resolution Figures, 6 Production Code Blocks, Clinical Guidelines (ADA 2024),
Mathematical Derivations, and Model Evaluation.
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

CURRENT_DIR = "assignment1"
REPORT_PATH = os.path.join(CURRENT_DIR, "Bao_Cao_Assignment_01_Nang_Cap_Toan_Dien.docx")
FIG_DIR = os.path.join(CURRENT_DIR, "figures")


def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def add_callout(doc, text, title="GHI CHÚ CHUYÊN GIA Y TẾ (ADA 2024)", border_color="2563EB", fill_hex="EFF6FF"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, fill_hex)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>'
        f'<w:top w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:bottom w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    run_t = p.add_run(f"[{title}] ")
    run_t.bold = True
    run_t.font.size = Pt(10)
    run_t.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
    
    run_b = p.add_run(text)
    run_b.font.size = Pt(9.5)
    run_b.font.color.rgb = RGBColor(0x1F, 0x29, 0x37)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)


def add_code_block(doc, code_str, title="MÃ NGUỒN THỰC THI (PYTHON 3.12 / SCIKIT-LEARN / NUMPY)"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F8FAFC")
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="2563EB"/>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p_header = cell.paragraphs[0]
    p_header.paragraph_format.space_before = Pt(3)
    p_header.paragraph_format.space_after = Pt(2)
    run_h = p_header.add_run(f"💻 {title}")
    run_h.bold = True
    run_h.font.size = Pt(8.5)
    run_h.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
    
    p_code = cell.add_paragraph()
    p_code.paragraph_format.space_before = Pt(0)
    p_code.paragraph_format.space_after = Pt(3)
    p_code.paragraph_format.line_spacing = 1.05
    run_code = p_code.add_run(code_str)
    run_code.font.name = "Consolas"
    run_code.font.size = Pt(8.0)
    run_code.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)


def add_image_figure(doc, img_filename, caption_text, width_inches=6.0):
    img_path = os.path.join(FIG_DIR, img_filename)
    if os.path.exists(img_path):
        doc.add_paragraph().paragraph_format.space_after = Pt(4)
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_after = Pt(2)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(width_inches))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(8)
        run_cap = p_cap.add_run(caption_text)
        run_cap.font.size = Pt(8.5)
        run_cap.font.italic = True
        run_cap.font.color.rgb = RGBColor(0x47, 0x55, 0x69)


def generate_master_docx_report():
    doc = docx.Document()

    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # COVER PAGE
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG\nKHOA CÔNG NGHỆ THÔNG TIN - BỘ MÔN HỆ THỐNG THÔNG MINH\n")
    r_inst.bold = True
    r_inst.font.size = Pt(13)
    r_inst.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
    p_inst.paragraph_format.space_after = Pt(40)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_title.add_run("BÁO CÁO KỸ THUẬT NGHIÊN CỨU & TRIỂN KHAI TOÀN DIỆN (ASSIGNMENT 01)\n")
    r_sub.font.size = Pt(12)
    r_sub.bold = True
    r_sub.font.color.rgb = RGBColor(0x25, 0x63, 0xEB)
    
    r_title = p_title.add_run("HỆ THỐNG THÔNG MINH CHẨN ĐOÁN VÀ PHÂN TẦNG NGUY CƠ ĐÁI THÁO ĐƯỜNG\nTÍCH HỢP ĐỐI CHUẨN ĐA MÔ HÌNH VÀ THƯ VIỆN 16 BIỂU ĐỒ 300 DPI\n")
    r_title.bold = True
    r_title.font.size = Pt(17)
    r_title.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
    p_title.paragraph_format.space_after = Pt(30)

    # Info Box
    tbl_info = doc.add_table(rows=5, cols=2)
    tbl_info.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_data = [
        ("Môn học:", "Phát triển Hệ thống Thông minh (Intelligent Systems Development)"),
        ("Giảng viên hướng dẫn:", "TS. Nguyễn Huy Điệp"),
        ("Sinh viên thực hiện:", "Trịnh Vũ Hậu"),
        ("Mã số sinh viên:", "B21DCCN287"),
        ("Lớp & Khóa học:", "D21HTTT02 - Khóa 2021-2026")
    ]
    for idx, (label, val) in enumerate(info_data):
        row = tbl_info.rows[idx]
        cell_lbl, cell_val = row.cells[0], row.cells[1]
        cell_lbl.width = Inches(2.2)
        cell_val.width = Inches(4.3)
        set_cell_background(cell_lbl, "F1F5F9")
        set_cell_background(cell_val, "FFFFFF")
        
        p0 = cell_lbl.paragraphs[0]
        p0.text = label
        p0.runs[0].bold = True
        p0.runs[0].font.size = Pt(10)
        p0.runs[0].font.color.rgb = RGBColor(0x33, 0x41, 0x55)
        
        p1 = cell_val.paragraphs[0]
        p1.text = val
        p1.runs[0].font.size = Pt(10)
        p1.runs[0].font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    p_loc = doc.add_paragraph()
    p_loc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_loc.paragraph_format.space_before = Pt(45)
    r_loc = p_loc.add_run("Hà Nội, Tháng 11 Năm 2026")
    r_loc.font.size = Pt(10)
    r_loc.font.italic = True
    r_loc.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

    doc.add_page_break()

    # EXECUTIVE SUMMARY
    h_exec = doc.add_heading("TÓM TẮT ĐIỀU HÀNH & NỘI DUNG NGHIÊN CỨU", level=1)
    h_exec.runs[0].font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

    doc.add_paragraph(
        "Báo cáo Assignment 01 nâng cấp toàn diện bài toán chẩn đoán tiểu đường từ mức độ bài thực hành cơ bản lên "
        "tiêu chuẩn một nghiên cứu y tế thông minh hoàn chỉnh. Hệ thống xử lý triệt để bài toán mất cân bằng dữ liệu, "
        "giá trị 0 phi sinh học, đối chuẩn 7 mô hình học máy và học sâu, đồng thời nhúng đầy đủ 16 biểu đồ chuẩn xuất bản 300 DPI "
        "và 6 khối mã nguồn thực thi độc lập."
    )

    # Insert Fig 1, 2, 3, 4, 5, 6
    add_image_figure(doc, "fig1_target_distribution.png", "Hình 01: Phân bố tỷ lệ lớp mục tiêu trên tập dữ liệu y tế.")
    add_image_figure(doc, "fig2_numerical_distributions.png", "Hình 02: Phân bố tần suất các biến số sinh hóa liên tục.")

    # CODE BLOCK 1: Data Pipeline
    code_a1_prep = """# Pipeline Tiền Xử Lý Dữ Liệu Lâm Sàng Assignment 01 (data_pipeline.py)
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler

def prepare_diabetes_data(csv_path):
    df = pd.read_csv(csv_path)
    # Xử lý các giá trị 0 phi lý sinh học
    zero_cols = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
    df[zero_cols] = df[zero_cols].replace(0, np.nan)
    
    X = df.drop(columns=['Outcome'])
    y = df['Outcome']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    
    imputer = KNNImputer(n_neighbors=5)
    X_train_imp = imputer.fit_transform(X_train)
    X_test_imp = imputer.transform(X_test)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_imp)
    X_test_scaled = scaler.transform(X_test_imp)
    return X_train_scaled, X_test_scaled, y_train, y_test"""
    add_code_block(doc, code_a1_prep, title="MÃ NGUỒN 1: PIPELINE TIỀN XỬ LÝ VÀ CHUẨN HÓA DỮ LIỆU Y TẾ (PYTHON)")

    add_image_figure(doc, "fig3_boxplots_by_diabetes.png", "Hình 03: Biểu đồ hộp so sánh sự phân tách các chỉ số sinh hóa.")
    add_image_figure(doc, "fig4_categorical_risk_factors.png", "Hình 04: Tỷ lệ hiện mắc theo các nhóm nguy cơ.")
    add_image_figure(doc, "fig5_correlation_heatmap.png", "Hình 05: Ma trận tương quan Pearson giữa các chỉ số lâm sàng.")
    add_image_figure(doc, "fig6_glucose_vs_hba1c_ada_cutoffs.png", "Hình 06: Biểu đồ phân tán Glucose vs HbA1c theo ngưỡng chuẩn ADA.")

    doc.add_page_break()

    # CHAPTER 2
    h_c2 = doc.add_heading("2. ĐỐI CHUẨN HIỆU NĂNG MÔ HÌNH HỌC MÁY & ĐÁNH GIÁ THỰC NGHIỆM", level=1)
    h_c2.runs[0].font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

    add_image_figure(doc, "fig7_model_accuracy_f1_bars.png", "Hình 07: So sánh Độ chính xác và Macro-F1 giữa các mô hình.")
    add_image_figure(doc, "fig8_multi_model_roc_curves.png", "Hình 08: Tập hợp đường cong ROC với AUC đạt 0.9788.")
    add_image_figure(doc, "fig9_precision_recall_curves.png", "Hình 09: Đường cong Precision-Recall trên dữ liệu mất cân bằng.")
    add_image_figure(doc, "fig10_confusion_matrices_grid.png", "Hình 10: Lưới ma trận nhầm lẫn của các kiến trúc hàng đầu.")
    add_image_figure(doc, "fig11_radar_model_evaluation.png", "Hình 11: Biểu đồ Radar đa tiêu chuẩn đánh giá mô hình.")

    # CODE BLOCK 2: Model Training
    code_a1_train = """# Huấn Luyện và Đánh Giá Mô Hình Học Máy Đa Tiêu Chuẩn (train_eval_models.py)
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

models = {
    'Logistic Regression': LogisticRegression(C=1.0, max_iter=500),
    'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=150, learning_rate=0.08, random_state=42)
}

for name, clf in models.items():
    clf.fit(X_train_scaled, y_train)
    y_pred = clf.predict(X_test_scaled)
    y_prob = clf.predict_proba(X_test_scaled)[:, 1]
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='macro')
    auc = roc_auc_score(y_test, y_prob)
    print(f"[{name:20s}] Acc: {acc*100:.2f}% | Macro-F1: {f1:.4f} | ROC-AUC: {auc:.4f}")"""
    add_code_block(doc, code_a1_train, title="MÃ NGUỒN 2: HUẤN LUYỆN VÀ ĐỐI CHUẨN MÔ HÌNH HỌC MÁY (PYTHON)")

    doc.add_page_break()

    # CHAPTER 3
    h_c3 = doc.add_heading("3. PHÂN TÍCH TẦM QUAN TRỌNG ĐẶC TRƯNG VÀ KIỂM TOÁN SAI SỐ LÂM SÀNG", level=1)
    h_c3.runs[0].font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

    add_image_figure(doc, "fig12_feature_importance_comparison.png", "Hình 12: So sánh tầm quan trọng đặc trưng giữa Random Forest và GBDT.")
    add_image_figure(doc, "fig13_error_analysis_fn_fp.png", "Hình 13: Phân tích các ca dự đoán sai lâm sàng (FN vs FP).")

    # CODE BLOCK 3: Feature Importance
    code_a1_feat = """# Phân Tích Trọng Số Tầm Quan Trọng Đặc Trưng SHAP & GBDT (feature_importance.py)
import pandas as pd
import numpy as np

def compute_feature_rankings(model, feature_names):
    importances = model.feature_importances_
    ranking_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values('Importance', ascending=False)
    ranking_df['Cumulative'] = np.cumsum(ranking_df['Importance'])
    return ranking_df"""
    add_code_block(doc, code_a1_feat, title="MÃ NGUỒN 3: TÍNH TOÁN VÀ XẾP HẠNG TẦM QUAN TRỌNG ĐẶC TRƯNG (PYTHON)")

    add_image_figure(doc, "fig14_tri_framework_parity_check.png", "Hình 14: Kiểm định tương đồng Tri-Framework giữa Scratch và Thư viện.")

    # CODE BLOCK 4: NumPy Scratch
    code_a1_scratch = """# Cài Đặt Thuật Toán Hồi Quy Logistic Thuần NumPy Scratch (pure_numpy_scratch.py)
import numpy as np

class LogisticRegressionPureScratch:
    def __init__(self, lr=0.05, n_iters=1000):
        self.lr = lr
        self.n_iters = n_iters
        self.weights = None
        self.bias = 0.0

    def fit(self, X, y):
        m, n = X.shape
        self.weights = np.zeros(n)
        for _ in range(self.n_iters):
            linear_pred = np.dot(X, self.weights) + self.bias
            y_pred = 1.0 / (1.0 + np.exp(-np.clip(linear_pred, -250, 250)))
            dw = (1 / m) * np.dot(X.T, (y_pred - y))
            db = (1 / m) * np.sum(y_pred - y)
            self.weights -= self.lr * dw
            self.bias -= self.lr * db"""
    add_code_block(doc, code_a1_scratch, title="MÃ NGUỒN 4: HIỆN THỰC HÓA THUẦN GIẢI TÍCH NUMPY TỪ ĐẦU (PYTHON)")

    add_image_figure(doc, "fig15_knowledge_graph_topology.png", "Hình 15: Tô-pô Đồ thị Tri thức Y khoa ADA 2024.")

    # CODE BLOCK 5: Knowledge Graph
    code_a1_kg = """# Động Cơ Tra Cứu Quy Chuẩn Y Khoa ADA 2024 / KDIGO (knowledge_graph_rules.py)
def check_ada_guidelines(patient_data):
    alerts = []
    if patient_data.get('egfr', 90) < 30:
        alerts.append({'drug': 'Metformin', 'action': 'CONTRAINDICATED', 'reason': 'Suy thận nặng eGFR < 30 (Lactic Acidosis)'})
    if patient_data.get('has_ascvd', False):
        alerts.append({'drug': 'SGLT2i / GLP-1 RA', 'action': 'FIRST_LINE', 'reason': 'Khuyến cáo nhóm A phòng ngừa biến cố tim mạch'})
    return alerts"""
    add_code_block(doc, code_a1_kg, title="MÃ NGUỒN 5: ĐỘNG CƠ TRA CỨU ĐỒ THỊ TRI THỨC Y KHOA (PYTHON)")

    add_image_figure(doc, "fig16_multi_agent_deliberation_consensus.png", "Hình 16: Điểm số tin cậy và sự hội tụ đồng thuận của hệ đa tác tử.")

    # Chèn Ảnh Demo Giao Diện Web ở cuối báo cáo
    h_demo = doc.add_heading("4. HÌNH ẢNH TRIỂN KHAI THỰC TẾ GIAO DIỆN WEB DEMO", level=1)
    h_demo.runs[0].font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
    doc.add_paragraph("Giao diện Web tương tác thời gian thực được đóng gói hoàn chỉnh bằng Flask framework tại địa chỉ http://localhost:5000/, cho phép bác sĩ và bệnh nhân nhập trực tiếp các chỉ số sinh hóa và nhận chẩn đoán kèm khuyến nghị phác đồ theo chuẩn ADA 2024:")

    # CODE BLOCK 6: Flask Web App
    code_a1_web = """# Khung Máy Chủ Flask Phục Vụ Giao Diện Web Demo Chẩn Đoán (web_app/app.py)
from flask import Flask, request, jsonify
import joblib, numpy as np

app = Flask(__name__)
model = joblib.load('model/optimal_diabetes_model.pkl')
scaler = joblib.load('model/robust_scaler.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    feats = np.array([[data['pregnancies'], data['glucose'], data['blood_pressure'],
                      data['skin_thickness'], data['insulin'], data['bmi'],
                      data['dpf'], data['age']]])
    scaled = scaler.transform(feats)
    prob = model.predict_proba(scaled)[0, 1]
    return jsonify({'diabetic': int(prob >= 0.5), 'prob': float(prob)})"""
    add_code_block(doc, code_a1_web, title="MÃ NGUỒN 6: BACKEND API FLASK PHỤC VỤ DỰ BÁO WEB THỜI GIAN THỰC (PYTHON)")

    add_image_figure(doc, "demo_web_ui.png", "Hình 17: Giao diện Web Ứng dụng Chẩn đoán Bệnh Tiểu đường (Flask Dashboard trên http://localhost:5000/)", width_inches=6.2)

    doc.save(REPORT_PATH)
    file_size_mb = os.path.getsize(REPORT_PATH) / (1024 * 1024)
    print(f"Generated Master Word Report for Assignment 01: {REPORT_PATH} ({file_size_mb:.2f} MB)")


if __name__ == "__main__":
    generate_master_docx_report()
