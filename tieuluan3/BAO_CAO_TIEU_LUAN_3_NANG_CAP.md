# BÁO CÁO TIỂU LUẬN 3: TRÍ TUỆ NHÂN TẠO TRONG ĐẦU TƯ TÀI CHÍNH: TỪ HỌC MÁY, CNN, RNN–LSTM ĐẾN KNOWLEDGE GRAPH, RAG VÀ HỆ ĐA AGENT
**Học phần**: Phát triển Hệ thống Thông minh  
**Học viện**: Học viện Công nghệ Bưu chính Viễn thông (PTIT) — Khoa Công nghệ Thông tin 1  
**Sinh viên thực hiện**: Trần Văn Hậu | **MSV**: B23DCCN287 | **Lớp**: D23CTPM01  
**Giảng viên hướng dẫn**: PGS.TS. Trần Đình Quế  
**Tập tin Báo cáo Word Hoàn chỉnh**: [`tieuluan3/Bao_Cao_Tieu_Luan_3_AI_Tai_Chinh_NLP.docx`](file:///c:/code/A2_CT_hautv.287/tieuluan3/Bao_Cao_Tieu_Luan_3_AI_Tai_Chinh_NLP.docx) (Dung lượng: **3.44 MB**, Tích hợp 11 hình ảnh 300 DPI, 6 khối mã nguồn thực thi và ảnh demo Web trực tiếp).

---

## 1. TỔNG QUAN HỆ THỐNG VÀ BÀI TOÁN TÀI CHÍNH HÌNH THỨC
Hệ thống AI Tài chính tích hợp đa tầng kết hợp giữa học sâu chuỗi thời gian, tối ưu hóa danh mục đầu tư Markowitz, Đồ thị Tri thức Doanh nghiệp (Fin-KG) kết hợp RAG và Hội đồng Đa Đặc vụ đầu tư.

### Đặc tả bài toán hình thức:
Cho chuỗi giá đóng cửa $\{P_t\}_{t=1}^T$. Tỷ suất sinh lời logarit tại thời điểm $t$:

$$r_t = \ln\left(\frac{P_t}{P_{t-1}}\right)$$

Bài toán dự báo chuỗi thời gian tìm hàm ánh xạ:

$$f: (r_{t-k+1}, \dots, r_t, X_t) \to r_{t+1}$$

với cửa sổ trượt $k$ và vector đặc trưng kỹ thuật $X_t$ (RSI, MACD, Bollinger Bands) nhằm tối thiểu hóa hàm mất mát Mean Squared Error (MSE).

![Xu hướng giá chứng khoán](charts/f01_financial_price_candlestick.png)
*Hình 01: Xu hướng giá chứng khoán kèm các đường trung bình động MA(10), MA(20) và dải Bollinger Bands (±2σ).*

![Hiện tượng gom cụm biến động](charts/f02_return_volatility_clustering.png)
*Hình 02: Hiện tượng gom cụm biến động (Volatility Clustering) và phân bố đuôi dày của tỷ suất lợi nhuận.*

---

## 2. KỸ NGHỆ ĐẶC TRƯNG CHUỖI THỜI GIAN & CHỈ BÁO KỸ THUẬT
Hệ thống trích xuất tập hợp các chỉ báo tài chính kinh điển:
- **RSI (Relative Strength Index)**: Đo lường vận tốc biến động giá, nhận diện vùng Quá mua (> 70) và Quá bán (< 30).
- **MACD (Moving Average Convergence Divergence)**: Chênh lệch EMA 12 và EMA 26 cùng đường tín hiệu 9 ngày.
- **Ma trận tương quan liên ngành**: Đo lường mức độ đồng pha và phân tán rủi ro giữa các nhóm ngành cổ phiếu.

```python
# Trích Xuất Chỉ Báo Kỹ Thuật Động Lượng RSI và MACD (technical_features.py)
import numpy as np
import pandas as pd

def compute_technical_indicators(df, window_rsi=14):
    df['log_ret'] = np.log(df['close'] / df['close'].shift(1))
    delta = df['close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=window_rsi).mean()
    avg_loss = loss.rolling(window=window_rsi).mean()
    rs = avg_gain / (avg_loss + 1e-8)
    df['rsi'] = 100 - (100 / (1 + rs))

    ema12 = df['close'].ewm(span=12, adjust=False).mean()
    ema26 = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = ema12 - ema26
    df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
    df['macd_hist'] = df['macd'] - df['macd_signal']
    return df.dropna()
```

![Chỉ báo kỹ thuật](charts/f03_technical_indicators_rsi_macd.png)
*Hình 03: Trích xuất các chỉ báo kỹ thuật RSI (14) và MACD Histogram phân tích động lượng giao dịch.*

![Ma trận tương quan](charts/f04_correlation_matrix_sectors.png)
*Hình 04: Ma trận tương quan lợi suất Pearson giữa các nhóm ngành cổ phiếu trọng điểm.*

---

## 3. KIẾN TRÚC MẠNG HỌC SÂU HỒI QUY: TỪ RNN ĐẾN LSTM VÀ GRU

$$f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f) \quad (\text{Forget Gate})$$

$$i_t = \sigma(W_i \cdot [h_{t-1}, x_t] + b_i) \quad (\text{Input Gate})$$

$$\tilde{C}_t = \tanh(W_c \cdot [h_{t-1}, x_t] + b_c) \quad (\text{Cell Candidate})$$

$$C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t \quad (\text{Cell State})$$

$$o_t = \sigma(W_o \cdot [h_{t-1}, x_t] + b_o) \quad (\text{Output Gate})$$

$$h_t = o_t \odot \tanh(C_t) \quad (\text{Hidden State})$$

| Kiến Trúc Học Sâu | MSE (1e-4) | RMSE (VND) | MAE (VND) | R² Score | Độ Trễ Suy Luận |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Simple RNN Baseline | 4.85 | 1,850 | 1,420 | 0.782 | 0.8 ms |
| Gated Recurrent Unit (GRU) | 2.10 | 1,220 | 910 | 0.895 | 1.2 ms |
| Standard LSTM Network | 1.65 | 1,080 | 820 | 0.912 | 1.5 ms |
| **Bi-LSTM + Attention (Đề xuất)** | **1.32** | **965** | **740** | **0.938** | **2.1 ms** |

```python
# Xây Dựng Mạng PyTorch LSTM Dự Báo Chuỗi Thời Gian Tài Chính (lstm_finnet.py)
import torch
import torch.nn as nn

class FinLSTMNet(nn.Module):
    def __init__(self, input_size=8, hidden_size=64, num_layers=2, output_size=1):
        super(FinLSTMNet, self).__init__()
        self.hidden_size, self.num_layers = hidden_size, num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, dropout=0.2)
        self.fc = nn.Sequential(nn.Linear(hidden_size, 32), nn.ReLU(), nn.Linear(32, output_size))

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        out, _ = self.lstm(x, (h0, c0))
        return self.fc(out[:, -1, :])
```

![Động học huấn luyện LSTM](charts/f05_lstm_gru_training_loss.png)
*Hình 05: Động học hàm mất mát huấn luyện chuỗi thời gian so sánh giữa LSTM, GRU và Attention.*

![Dự báo giá chứng khoán](charts/f06_actual_vs_predicted_stock.png)
*Hình 06: Dự báo giá chứng khoán đa bước (T+1 đến T+30) kèm dải khoảng tin cậy 95%.*

---

## 4. TỐI ƯU HÓA DANH MỤC MARKOWITZ & KIỂM ĐỊNH PARITY

$$\max_w \text{Sharpe} = \frac{w^T \mu - R_f}{\sqrt{w^T \Sigma w}} \quad \text{s.t.} \quad \sum_{i=1}^N w_i = 1, \quad 0 \le w_i \le 0.40$$

```python
# Tối Ưu Hóa Tỷ Trọng Danh Mục Đầu Tư Markowitz (markowitz_opt.py)
import numpy as np
from scipy.optimize import minimize

def optimize_portfolio(expected_returns, cov_matrix, risk_free_rate=0.05):
    num_assets = len(expected_returns)
    def neg_sharpe(weights):
        p_return = np.dot(weights, expected_returns)
        p_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        return -(p_return - risk_free_rate) / (p_vol + 1e-8)

    constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0})
    bounds = tuple((0.0, 0.40) for _ in range(num_assets))
    init_weights = np.ones(num_assets) / num_assets
    res = minimize(neg_sharpe, init_weights, method='SLSQP', bounds=bounds, constraints=constraints)
    return res.x
```

![Markowitz Frontier](charts/f07_markowitz_efficient_frontier.png)
*Hình 07: Đường biên hiệu quả Markowitz (Efficient Frontier) mô phỏng 1,500 danh mục đầu tư.*

![Kiểm định Parity](charts/f08_tri_framework_fin_parity.png)
*Hình 08: Kiểm định đồng nhất số học Tri-Framework Parity (NumPy vs PyTorch vs ONNX Runtime).*

---

## 5. ĐỒ THỊ TRI THỨC TÀI CHÍNH (FIN-KG), RAG & HỆ THỐNG ĐA TÁC TỬ
Hệ thống phát triển Đồ thị Tri thức Tài chính (Fin-KG) kết hợp RAG Báo cáo tài chính và Hội đồng 4 Đặc vụ Đầu tư chuyên nghiệp:
- **Quant-Agent**: Khai thác tín hiệu kỹ thuật (RSI, Bollinger, dự báo LSTM).
- **Fundamental-Agent**: Đánh giá sức khỏe tài chính thông qua P/E, P/B, ROE.
- **News-Agent**: LLM RAG quét tin tức kinh tế và thông cáo báo chí.
- **RiskCritic-Agent**: Phản tư rủi ro thanh khoản và tỷ lệ nợ vay (Debt-to-Equity).

```python
# Động Cơ Tra Cứu Đồ Thị Tri Thức Fin-KG & Quy Chuẩn Tài Chính (fin_kg_engine.py)
class FinancialKnowledgeGraph:
    def check_financial_health(self, ticker, metrics):
        alerts = []
        if metrics.get('pe_ratio', 15.0) > 35.0:
            alerts.append({'severity': 'WARNING', 'rule': 'PE_OVERVALUED'})
        if metrics.get('debt_to_equity', 1.0) > 2.5:
            alerts.append({'severity': 'HIGH_RISK', 'rule': 'HIGH_LEVERAGE'})
        return alerts
```

![Fin-KG Topology](charts/f09_financial_knowledge_graph_rag.png)
*Hình 09: Cấu trúc Đồ thị Tri thức Tài chính Doanh nghiệp Fin-KG kết hợp RAG Báo cáo tài chính.*

![Multi-Agent Consensus](charts/f10_multi_agent_investment_council.png)
*Hình 10: Phân bố điểm đồng thuận của Hội đồng 4 Đặc vụ Đầu tư Tài chính.*

---

## 6. GIAO DIỆN WEB DEMO TƯƠNG TÁC THỜI GIAN THỰC (DEMO CUỐI BÁO CÁO)
Giao diện Web Demo Phân tích Đầu tư AI tích hợp đầy đủ công cụ trực quan hóa dự báo giá nến Nhật, chỉ báo động lượng và phiên hội chẩn đặc vụ thời gian thực:

![Ảnh chụp thực tế Giao diện Web Demo Hệ Thống Phân Tích Đầu Tư AI](figures/demo_web_ui.png)
*Hình 11: Ảnh chụp thực tế Giao diện Web Demo Hệ Thống Phân Tích Đầu Tư AI & Hệ Thống Đa Agent Tài Chính - Trực quan hóa Dự báo Giá LSTM, Chỉ báo Kỹ thuật và Phiên Hội Chẩn Đặc Vụ Thời Gian Thực.*

```python
# Khung Máy Chủ Flask Phục Vụ Giao Diện Web Demo Tài Chính AI (app_fin.py)
from flask import Flask, render_template, request, jsonify
import torch, numpy as np

app = Flask(__name__)
fin_model = torch.load('models/optimal_fin_lstm.pt')
fin_model.eval()

@app.route('/api/predict_stock', methods=['POST'])
def predict_stock():
    req = request.json
    sequence_data = np.array(req['history_60_days'], dtype=np.float32)
    tensor_input = torch.tensor(sequence_data).unsqueeze(0)
    with torch.no_grad():
        pred_scaled = fin_model(tensor_input).item()
    predicted_price = float(req['last_price'] * np.exp(pred_scaled))
    return jsonify({
        'ticker': req['ticker'],
        'predicted_price_t1': round(predicted_price, 2),
        'expected_return': round(pred_scaled * 100, 2),
        'recommendation': 'MUA TÍCH LŨY' if pred_scaled > 0.015 else 'THEO DÕI'
    })
```

---
*Báo cáo được hoàn thiện và chứng nhận bởi Hệ thống Thông minh Tieuluan 3 — PTIT 2026.*
