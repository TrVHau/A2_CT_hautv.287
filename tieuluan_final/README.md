# BÁO CÁO TIỂU LUẬN FINAL MÔN HỌC: PHÁT TRIỂN HỆ THỐNG THÔNG MINH
**Học viện Công nghệ Bưu chính Viễn thông (PTIT) — Khoa Công nghệ Thông tin 1**  
**Giảng viên hướng dẫn:** PGS. TS. Trần Đình Quế  
**Sinh viên thực hiện:** Trần Văn Hậu | **MSV:** B23DCCN287 | **Lớp:** D23CTPM01  
**Nhóm môn học:** CT | **Nhóm tiểu luận:** 09  

---

## 1. Tổng quan đề tài tiểu luận
- **Tên đề tài chính thức:**  
  **NGHIÊN CỨU VÀ PHÁT TRIỂN HỆ THỐNG THÔNG MINH TOÀN DIỆN: TỪ HỌC MÁY CƠ BẢN, CNN, RNN–LSTM ĐẾN KNOWLEDGE GRAPH, DEEP GRAPH VÀ HỆ ĐA TÁC TỬ TỰ CHỦ**  
  *(A Comprehensive Intelligent System Framework: From Classical Machine Learning, CNN, RNN–LSTM to Knowledge Graphs, Deep Graph Neural Networks, and Autonomous Multi-Agent Systems)*
- **Chiến lược tiếp cận Đa miền (Dual Domains Strategy):**  
  Kết nối song hành hai trụ cột ứng dụng sống còn đòi hỏi độ chính xác và độ tin cậy khắt khe nhất:
  1. **Miền 1 — Y tế Chuyển hóa & Bệnh lý Đái tháo đường (Healthcare & Metabolic Analytics)**
  2. **Miền 2 — Kinh tế Định lượng & Phân tích Tài chính (Quantitative Finance & Risk Management)**

---

## 2. Các sản phẩm chính trong thư mục này

### 🌟 PHIÊN BẢN V2 NÂNG CẤP TOÀN DIỆN (CHÍNH THỨC & TỐI TÂN NHẤT)

| Tên tệp tin V2 | Định dạng / Kích thước | Quy mô & Đặc tả nội dung chi tiết |
| :--- | :---: | :--- |
| **`tieuluan_final_CT_09_Hautv.287_v2.pdf`** | Adobe PDF (.pdf)<br/>**8.05 MB — 152 Trang** | **Bản in tài liệu PDF V2 chuẩn xuất bản cao cấp nhất (152 trang)**, xuất trực tiếp từ Microsoft Word COM. Đầy đủ trang bìa Logo PTIT, Lời cam đoan, Lời cảm ơn, Tóm tắt quản hành, Danh mục 38 từ viết tắt, Mục lục chi tiết 7 chương & 4 phụ lục, Danh mục 69 Hình ảnh, Danh mục 51 Bảng biểu, 48 tài liệu tham khảo IEEE, toàn bộ 14 mã nguồn phụ lục C & 5 mã nguồn phụ lục D. Header & Footer động đánh số tự động `Trang X / 152`. |
| **`tieuluan_final_CT_09_Hautv.287_v2.docx`** | Microsoft Word (.docx)<br/>**16.19 MB — 152 Trang** | **Báo cáo kỹ thuật V2 Master Word hoàn chỉnh nhất**, định dạng chuẩn luận văn thạc sĩ/tiến sĩ PTIT (Times New Roman 13pt, dãn dòng 1.45 line spacing, khoảng cách đoạn 6.0pt, bảng biểu tương phản chuyên nghiệp, 69 hình ảnh độ nét cao). |
| **`tieuluan_final_CT_09_Hautv.287_v2.md`** | Markdown (.md)<br/>**326.64 KB — 4.529 Dòng** | **Bản Markdown toàn văn V2 cực kỳ chi tiết (4.529 dòng)**, hỗ trợ đọc trực tiếp trên VS Code/GitHub/Obsidian với đầy đủ công thức toán KaTeX ($$...$$), bảng biểu và toàn bộ mã nguồn. |
| **`build_master_final_term_paper_v2.py`** | Python Script | Bộ điều phối chính (Master Builder V2) xây dựng tài liệu Word tự động từ 10 mô-đun trong thư mục `v2_sections/`. |
| **`build_markdown_report_v2.py`** | Python Script | Script biên soạn toàn văn Markdown V2 đồng bộ tuyệt đối với bản Word. |
| **`convert_v2_to_pdf.py`** | Python Script | Script tự động chuyển đổi DOCX V2 sang PDF thông qua Word COM API. |
| **`v2_sections/` (10 mô-đun)** | Python Modules | 10 mô-đun chuyên sâu: Bìa, Mở đầu, Chương 1 $\to$ Chương 7, Kết luận & 4 Phụ lục mở rộng. |

---

### 📦 PHIÊN BẢN V1 (BẢN CƠ BẢN TIỀN NHIỆM)

| Tên tệp tin V1 | Định dạng / Kích thước | Mô tả nội dung chi tiết |
| :--- | :---: | :--- |
| **`tieuluan_final_CT_09_Hautv.287.pdf`** | Adobe PDF (.pdf)<br/>**8.71 MB — 97 Trang** | Bản in PDF phiên bản V1 cơ bản (97 trang). |
| **`tieuluan_final_CT_09_Hautv.287.docx`** | Microsoft Word (.docx)<br/>**20.45 MB** | Báo cáo kỹ thuật Word phiên bản V1. |
| **`tieuluan_final_CT_09_Hautv.287.md`** | Markdown (.md)<br/>**184 KB — 2.828 Dòng** | Tài liệu Markdown phiên bản V1. |

---

## 3. Đặc tả chất lượng khoa học và kỹ thuật của công trình

- **Độ phủ cấu trúc chương mục:** Trọn vẹn 7 Chương chuyên môn theo đề cương của Giảng viên hướng dẫn + Phần Mở đầu + Kết luận & Hướng phát triển + Danh mục tài liệu tham khảo chuẩn IEEE + 4 Phụ lục kỹ thuật.
- **Tiếp cận đa miền (Dual Domains):** Triển khai đồng thời trên dữ liệu Y tế lâm sàng (Pima Indians, NHANES, CGM Shanghai, RetinaMNIST, MedQuAD, Pubmed-Diabetes) và dữ liệu Tài chính định lượng (LendingClub, Housing Price, Candlestick OHLC, Cổ phiếu AAPL/VN-Index, FinQA).
- **Nền tảng toán học và chứng minh định lý sâu sắc:**
  - Chương 1: Chứng minh toán học mô hình nơ-ron McCulloch–Pitts, Định lý hội tụ Perceptron của Novikoff ($k \le \frac{R^2}{\gamma^2}$), Định lý bất khả phân tách tuyến tính XOR của Minsky–Papert, và Định luật tỷ lệ tham số (Scaling Laws).
  - Chương 2: Phân rã kỳ vọng sai số Bias-Variance, đạo hàm Normal Equation $w^* = (X^T X)^{-1} X^T y$ cho OLS và Ridge, gradient của Binary Cross-Entropy, bài toán đối ngẫu Lagrange & điều kiện KKT của SVM, và khai triển Taylor bậc 2 trong XGBoost.
  - Chương 3: Toán tích chập 2D xuôi và ngược ($\frac{\partial L}{\partial K} = X * \frac{\partial L}{\partial Y}$ và $\text{FullConv}$), thuật toán ma trận hóa `im2col` GEMM, công thức trường tiếp nhận $RF_l$, khối phần dư ResNet triệt tiêu suy giảm gradient, và đạo hàm Grad-CAM.
  - Chương 4: Chuỗi tích ma trận Jacobian trong BPTT chứng minh hiện tượng suy giảm/bùng nổ gradient, cơ chế đường cao tốc Constant Error Carousel (CEC) của LSTM ($\frac{\partial C_t}{\partial C_{t-1}} \approx I$), cơ chế Chú ý Thời gian (Temporal Attention), và backtest tài chính định lượng đạt Sharpe Ratio = 1.65.
  - Chương 5: Bản thể học RDF/OWL, TBox vs ABox, công thức Okapi BM25 với phân tích siêu tham số $(k_1, b)$, nhúng vector HNSW, thuật toán hợp nhất thứ hạng RRF, và GraphRAG suy luận đa bước trên Neo4j đạt Faithfulness = 0.942.
  - Chương 6: Rời rạc hóa toán tử Laplace–Beltrami thành Laplacian chuẩn hóa đối xứng $L_{sym}$, phép biến đổi Fourier đồ thị và tích chập phổ, xấp xỉ Chebyshev và Kipf–Welling renormalization trick, chứng minh toán học hiện tượng làm trơn quá mức qua Năng lượng Dirichlet $\mathcal{E}(H) \to 0$, và giới hạn biểu diễn của phép thử 1-WL.
  - Chương 7: Lý thuyết trò chơi (Trò chơi dạng chuẩn, Cân bằng Nash, Dec-POMDP, CTDE), học tăng cường MARL đối kháng Gridworld, Hội đồng 5 tác tử LLM có vòng lặp ReAct, Cổng đồng thuận Bayes ($\mathcal{S}_{\text{consensus}} \ge 0.85$), và 4 chốt an toàn Guardrails chống ảo giác đạt độ chính xác 91.3%.
- **Bộ ba cài đặt độc lập (Scratch - Keras - PyTorch):** Hiện thực hóa từ đầu bằng NumPy thuần (không dùng thư viện ngoài) cho MLP, CNN và RNN/LSTM, đối chứng nghiêm ngặt với Keras và PyTorch qua ma trận kiểm chứng đạo hàm (Parity Check) đạt sai số $< 10^{-7}$.
- **Lý thuyết Hợp các hàm toán học thống nhất:** Biểu diễn mọi kiến trúc từ MLP, CNN, RNN, GCN tới Hệ Đa Tác tử dưới dạng ánh xạ hàm hợp liên tục $f(x) = (f_L \circ \dots \circ f_1)(x)$.
- **Sẵn sàng triển khai thực tế (Web Demo Localhost):** Toàn bộ 7 chương đều có giao diện Web Dashboard tương tác trực quan thời gian thực trên các cổng localhost tương ứng.

---

## 4. Hướng dẫn thực thi và tái lập (Reproducibility)
Để tái tạo lại toàn bộ file Word, Markdown và PDF từ đầu:
```bash
# 1. Sinh tài liệu Word DOCX chính thức
python tieuluan_final/build_master_final_term_paper.py

# 2. Sinh tài liệu Markdown toàn văn
python tieuluan_final/build_markdown_report.py

# 3. Xuất tài liệu PDF chính thức
python -c "from docx2pdf import convert; convert('tieuluan_final/tieuluan_final_CT_09_Hautv.287.docx', 'tieuluan_final/tieuluan_final_CT_09_Hautv.287.pdf')"
```
Toàn bộ mã nguồn, dữ liệu thực nghiệm và tài liệu đã được kiểm thử, biên dịch thành công và sẵn sàng phục vụ báo cáo học thuật!


---

## 5. Cấu trúc Thư mục Mã nguồn Thực nghiệm (`tieuluan_final/src/`)

Toàn bộ mã nguồn thực thi độc lập cho cả 7 chương đã được đóng gói trực tiếp vào thư mục `tieuluan_final/src/`:

```
tieuluan_final/src/
├── chap1_history/               # Thực nghiệm đối đầu 4 thế hệ mô hình trên Pima Diabetes
├── chap2_ml_basic/              # Scratch MLP, Keras, PyTorch, Parity Check < 1e-7 & 9 mô hình ML
├── chap3_cnn/                   # Conv2D Scratch Parity, MedicalCNN, Grad-CAM Heatmap & GASF/GADF/MTF
├── chap4_rnn/                   # LSTM Scratch CEC, Attention-LSTM, Walk-Forward CGM & Backtest tài chính
├── chap5_kg_rag/                # Bản thể học Neo4j, Hybrid Retrieval (BM25+Dense RRF) & Ragas Tri-Framework
├── chap6_deep_graph/            # Spectral GCN, GraphSAGE, GAT, Hiện tượng Over-smoothing (Dirichlet & MAD)
├── chap7_multi_agent/           # Gridworld MARL CTDE, Hội đồng 5 tác tử, Cổng đồng thuận Bayes & Guardrails
├── web_demo/                    # Giao diện Web Dashboard Flask tương tác trực tiếp cả 7 chương
├── run_all_experiments.py       # Master runner chạy tự động kiểm thử toàn bộ 7 chương
└── README.md                    # Hướng dẫn chi tiết từng mô-đun mã nguồn
```

### Cách chạy kiểm thử nhanh:
```bash
# Chạy toàn bộ 7 chương tự động chỉ với 1 lệnh:
python tieuluan_final/src/run_all_experiments.py

# Khởi chạy giao diện Web Dashboard tương tác:
python tieuluan_final/src/web_demo/app.py
```
*(Truy cập `http://localhost:5000` trên trình duyệt)*
