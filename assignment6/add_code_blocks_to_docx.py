"""
Add real styled code blocks to assignment6/Bao_Cao_Assignment_06_Nang_Cap_Toan_Dien.docx
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

DOC_PATH = "assignment6/Bao_Cao_Assignment_06_Nang_Cap_Toan_Dien.docx"
doc = docx.Document(DOC_PATH)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def add_code_block(doc, code_str, title="MÃ NGUỒN THỰC THI (PYTHON 3.12 / PYTORCH / KERAS)"):
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

# 1. Code 1: PyTorch LSTM Architecture
c1 = """class LSTMRegressor(nn.Module):
    def __init__(self, hidden_size=32):
        super().__init__()
        self.lstm = nn.LSTM(1, hidden_size, batch_first=True)
        self.head = nn.Sequential(
            nn.Linear(hidden_size, 16),
            nn.ReLU(),
            nn.Linear(16, 1)
        )
    def forward(self, values):
        output, _ = self.lstm(values)
        return self.head(output[:, -1, :])"""

# 2. Code 2: Keras LSTM Sequential
c2 = """model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(30, 1)),
    tf.keras.layers.LSTM(32),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(1)
])
model.compile(optimizer=tf.keras.optimizers.Adam(0.003), loss='mse')"""

# 3. Code 3: Preprocessing
c3 = """def preprocess_timeseries(series, window_size=30, train_ratio=0.8):
    split_idx = int(len(series) * train_ratio)
    train_data = series[:split_idx].reshape(-1, 1)
    test_data = series[split_idx:].reshape(-1, 1)
    scaler = MinMaxScaler()
    train_scaled = scaler.fit_transform(train_data)
    test_scaled = scaler.transform(test_data)
    return train_scaled, test_scaled, scaler"""

# 4. Code 4: Web FastAPI Backend
c4 = """@app.post("/predict")
def predict_next(req: PredictRequest):
    data = np.array(req.values[-30:]).reshape(1, 30, 1)
    scaled = scaler.transform(data.reshape(-1, 1)).reshape(1, 30, 1)
    with torch.no_grad():
        pred_scaled = model(torch.tensor(scaled, dtype=torch.float32)).item()
    pred_val = scaler.inverse_transform([[pred_scaled]])[0, 0]
    return {"prediction": float(pred_val), "framework": "PyTorch"}"""

doc.add_page_break()
h_cb = doc.add_heading("PHỤ LỤC MÃ NGUỒN CỐT LÕI (PYTORCH & TENSORFLOW/KERAS)", level=1)
h_cb.runs[0].font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

add_code_block(doc, c1, title="MÃ NGUỒN 1: KIẾN TRÚC MẠNG PYTORCH LSTM REGRESSOR")
add_code_block(doc, c2, title="MÃ NGUỒN 2: KIẾN TRÚC MẠNG TENSORFLOW/KERAS LSTM SEQUENTIAL")
add_code_block(doc, c3, title="MÃ NGUỒN 3: PIPELINE CHUẨN HÓA DỮ LIỆU CHUỖI THỜI GIAN MINMAXSCALER")
add_code_block(doc, c4, title="MÃ NGUỒN 4: FASTAPI BACKEND SUY LUẬN WEB THỜI GIAN THỰC")

doc.save(DOC_PATH)
print(f"Added 4 code blocks to {DOC_PATH}")
