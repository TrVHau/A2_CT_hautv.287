# BỘ MÃ NGUỒN THỰC NGHIỆM TIỂU LUẬN TOÀN DIỆN 7 CHƯƠNG

**Học viện Công nghệ Bưu chính Viễn thông (PTIT)**  
**Khoa Công nghệ Thông tin 1 — Bộ môn Hệ thống Thông minh**  

- **Sinh viên thực hiện:** Trần Văn Hậu
- **Mã sinh viên:** B23DCCN287
- **Lớp:** D23CTPM01
- **Nhóm môn học:** CT | **Nhóm tiểu luận:** 09
- **Giảng viên hướng dẫn:** PGS. TS. Trần Đình Quế
- **Môn học:** Phát triển các hệ thống thông minh

---

## 1. Cấu trúc Thư mục Mã nguồn

Bộ mã nguồn được tổ chức module hóa chặt chẽ theo đúng 7 chương nội dung của luận văn:

```
tieuluan_final/src/
├── chap1_history/                      # CHƯƠNG 1: LỊCH SỬ AI & ĐỐI ĐẦU 4 THẾ HỆ
│   ├── __init__.py
│   └── benchmark_4_generations.py      # Thực nghiệm đối đầu 4 thế hệ mô hình trên Pima Diabetes
│
├── chap2_ml_basic/                     # CHƯƠNG 2: HỌC MÁY CƠ BẢN & GRADIENT PARITY CHECK
│   ├── __init__.py
│   ├── scratch_mlp.py                  # MLP viết thuần từ đầu bằng NumPy (Forward & Backward)
│   ├── keras_mlp.py                    # MLP cài đặt trên Keras / TensorFlow Sequential API
│   ├── pytorch_mlp.py                  # MLP kế thừa torch.nn.Module với BatchNorm & Dropout
│   ├── gradient_parity_check.py        # Kiểm chứng tương đương đạo hàm Scratch vs PyTorch (< 1e-7)
│   └── train_9_algorithms.py           # 10-Fold Stratified Cross-Validation trên 9 thuật toán ML
│
├── chap3_cnn/                          # CHƯƠNG 3: CNN, GRAD-CAM & MÃ HÓA TÍN HIỆU 2D
│   ├── __init__.py
│   ├── scratch_conv2d.py               # Toán tử Conv2D & MaxPool viết thuần NumPy (Parity < 1e-7)
│   ├── pytorch_cnn.py                  # Kiến trúc MedicalCNN & Residual Block trên PyTorch
│   ├── gradcam.py                      # Trích xuất trọng số kênh alpha_k^c & lập Heatmap giải thích
│   └── timeseries_to_image.py          # Biến đổi chuỗi 1D thành ảnh 2D (GASF, GADF, MTF)
│
├── chap4_rnn/                          # CHƯƠNG 4: RNN, LSTM, GRU & DỰ BÁO CHUỖI THỜI GIAN
│   ├── __init__.py
│   ├── scratch_lstm.py                 # Tế bào LSTM viết thuần NumPy với băng chuyền lỗi CEC
│   ├── pytorch_rnn_lstm_gru.py         # So sánh Vanilla RNN, LSTM, GRU & Temporal Attention
│   ├── train_forecasting.py            # Dự báo đường huyết CGM (Walk-Forward Validation)
│   └── backtest_quantitative.py        # Hệ thống kiểm thử định lượng tài chính (CAGR, Sharpe, MDD)
│
├── chap5_kg_rag/                       # CHƯƠNG 5: KNOWLEDGE GRAPH, RAG LAI & REACT TOOL-AGENT
│   ├── __init__.py
│   ├── neo4j_ontology.py               # Bản thể học lâm sàng (OWL/RDF) & Cypher Query Builder
│   ├── hybrid_retriever.py             # Truy vấn lai: Okapi BM25 + Dense Vector + RRF (k=60)
│   ├── graph_rag_engine.py             # Động cơ GraphRAG suy luận đa bước kết hợp đồ thị tri thức
│   ├── ragas_evaluator.py              # Đánh giá chất lượng RAG theo bộ 3 chỉ số chuẩn Ragas
│   └── tool_agent_router.py            # Tác tử ReAct điều phối công cụ linh hoạt
│
├── chap6_deep_graph/                   # CHƯƠNG 6: DEEP GRAPH LEARNING & OVER-SMOOTHING
│   ├── __init__.py
│   ├── spectral_gcn.py                 # Tầng tích chập phổ GCN Kipf & Welling (ICLR 2017)
│   ├── graphsage.py                    # Học quy nạp GraphSAGE với lấy mẫu & gom cụm láng giềng
│   ├── gat_attention.py                # Graph Attention Network (GAT) với cơ chế tự chú ý đa đầu
│   ├── oversmoothing_mad.py            # Đo lường năng lượng Dirichlet E(H) & chỉ số sụp đổ MAD
│   └── train_graph_benchmark.py        # Đo chuẩn phân loại đỉnh bán giám sát trên đồ thị trích dẫn
│
├── chap7_multi_agent/                  # CHƯƠNG 7: AUTONOMOUS MULTI-AGENT & CLINICAL COUNCIL
│   ├── __init__.py
│   ├── gridworld_marl.py               # MARL Q-Learning Pursuit-Evasion Gridworld (CTDE)
│   ├── council_agents.py               # Hội đồng 5 tác tử tham vấn (Diagnostic, Pharma, Lifestyle, Critic, CMO)
│   ├── consensus_gate.py               # Cổng đồng thuận Bayesian Consensus Gate (tau = 0.85)
│   ├── guardrails_pipeline.py          # Đường ống phòng thủ 4 tầng (Schema, Hallucination, Safety, Privacy)
│   └── deliberation_runner.py          # Thực thi hội chẩn tự động trên 150 ca bệnh lâm sàng phức tạp
│
├── web_demo/                           # GIAO DIỆN WEB DASHBOARD TƯƠNG TÁC
│   ├── __init__.py
│   ├── app.py                          # Ứng dụng Web Flask tích hợp điều khiển cả 7 chương
│   └── templates/
│       └── index.html                  # Giao diện responsive Bootstrap 5 trực quan hóa
│
├── run_all_experiments.py              # KỊCH BẢN MASTER RUNNER CHẠY TỰ ĐỘNG TOÀN BỘ 7 CHƯƠNG
└── README.md                           # Hướng dẫn chi tiết
```

---

## 2. Hướng dẫn Cài đặt & Môi trường

Yêu cầu môi trường:
- Python 3.10 trở lên (khuyến nghị Python 3.11 - 3.13)
- Hệ điều hành: Windows, macOS, hoặc Linux

Cài đặt các thư viện cần thiết:
```bash
pip install numpy pandas scikit-learn torch torchvision flask
```

---

## 3. Chạy Toàn Bộ Thí Nghiệm Chỉ Với Một Lệnh

Để kiểm thử và chạy toàn bộ mã nguồn của cả 7 chương từ đầu đến cuối:
```bash
python tieuluan_final/src/run_all_experiments.py
```

---

## 4. Chạy Từng Chương Riêng Biệt

### Chương 1: Đối chuẩn 4 Thế hệ AI
```bash
python tieuluan_final/src/chap1_history/benchmark_4_generations.py
```

### Chương 2: Kiểm chứng Tương đương Đạo hàm Parity Check
```bash
python tieuluan_final/src/chap2_ml_basic/gradient_parity_check.py
python tieuluan_final/src/chap2_ml_basic/train_9_algorithms.py
```

### Chương 3: CNN Scratch, Grad-CAM & Mã hóa Tín hiệu
```bash
python tieuluan_final/src/chap3_cnn/scratch_conv2d.py
python tieuluan_final/src/chap3_cnn/gradcam.py
python tieuluan_final/src/chap3_cnn/timeseries_to_image.py
```

### Chương 4: LSTM Scratch, Dự báo CGM & Backtest Tài chính
```bash
python tieuluan_final/src/chap4_rnn/scratch_lstm.py
python tieuluan_final/src/chap4_rnn/train_forecasting.py
python tieuluan_final/src/chap4_rnn/backtest_quantitative.py
```

### Chương 5: Đồ thị Tri thức & GraphRAG
```bash
python tieuluan_final/src/chap5_kg_rag/neo4j_ontology.py
python tieuluan_final/src/chap5_kg_rag/hybrid_retriever.py
python tieuluan_final/src/chap5_kg_rag/graph_rag_engine.py
python tieuluan_final/src/chap5_kg_rag/ragas_evaluator.py
python tieuluan_final/src/chap5_kg_rag/tool_agent_router.py
```

### Chương 6: Deep Graph Learning & Quá làm mịn
```bash
python tieuluan_final/src/chap6_deep_graph/spectral_gcn.py
python tieuluan_final/src/chap6_deep_graph/oversmoothing_mad.py
python tieuluan_final/src/chap6_deep_graph/train_graph_benchmark.py
```

### Chương 7: Hệ Thống Đa Tác Tử & Hội Đồng Y Tế
```bash
python tieuluan_final/src/chap7_multi_agent/gridworld_marl.py
python tieuluan_final/src/chap7_multi_agent/council_agents.py
python tieuluan_final/src/chap7_multi_agent/consensus_gate.py
python tieuluan_final/src/chap7_multi_agent/guardrails_pipeline.py
python tieuluan_final/src/chap7_multi_agent/deliberation_runner.py
```

---

## 5. Khởi chạy Giao diện Web Demo Trực quan

Khởi động Web Dashboard:
```bash
python tieuluan_final/src/web_demo/app.py
```
Sau đó mở trình duyệt truy cập địa chỉ: `http://localhost:5000`
Giao diện bao gồm 7 tabs trực quan hóa kết quả đồ thị, ma trận so sánh, bản đồ nhiệt Grad-CAM, và bảng điều khiển mô phỏng Hội chẩn Đa tác tử tương tác trực tiếp.
