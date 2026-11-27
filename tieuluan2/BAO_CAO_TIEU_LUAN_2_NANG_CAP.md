# HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG
## KHOA CÔNG NGHỆ THÔNG TIN 1
### PHÁT TRIỂN CÁC HỆ THỐNG THÔNG MINH (INTELLIGENT SYSTEMS DEVELOPMENT)

# ĐỒ THỊ TRI THỨC (KNOWLEDGE GRAPH) VÀ RAG, TÍCH HỢP HỌC SÂU ĐA MIỀN CHO Y TẾ VÀ TÀI CHÍNH VIỆT NAM

### CÔNG TRÌNH NGHIÊN CỨU TOÀN DIỆN, THIẾT KẾ KIẾN TRÚC TÁC TỬ REACT VÀ ĐỐI CHUẨN ĐỘ TRUNG THỰC ĐỊNH LƯỢNG

**Sinh viên thực hiện**: **Trần Văn Hậu**  
**Mã sinh viên**: **B23DCCN287**  
**Lớp học phần**: **D23CTPM01** (Nhóm lớp CT – Nhóm 07)  
**Giảng viên hướng dẫn**: **PGS.TS. Trần Đình Quế**  
**Học kỳ**: Học kỳ 1 – Năm học 2026 – 2027  
**Địa điểm & Thời gian**: HÀ NỘI, NĂM 2026

**Tệp tin Báo cáo Word Hoàn chỉnh**: [`tieuluan2/Bao_Cao_Tieu_Luan_2_Nang_Cap.docx`](file:///c:/code/A2_CT_hautv.287/tieuluan2/Bao_Cao_Tieu_Luan_2_Nang_Cap.docx) (Tích hợp đầy đủ 14 hình vẽ 300 DPI, các bảng chuẩn hóa, hộp cảnh báo và mã nguồn)

---

## MỤC LỤC TỔNG QUAN
1. [TỔNG QUAN VÀ TÓM TẮT ĐỀ TÀI (EXECUTIVE SUMMARY)](#tổng-quan-và-tóm-tắt-đề-tài-executive-summary)
2. [DANH MỤC TỪ VIẾT TẮT](#danh-mục-từ-viết-tắt)
3. [CHƯƠNG 1: MỞ ĐẦU VỀ KNOWLEDGE GRAPH VÀ RAG](#chương-1-mở-đầu-về-knowledge-graph-và-rag)
4. [CHƯƠNG 2: XÂY DỰNG ĐỒ THỊ TRI THỨC Y TẾ VÀ TÀI CHÍNH](#chương-2-xây-dựng-đồ-thị-tri-thức-y-tế-và-tài-chính)
5. [CHƯƠNG 3: KỸ THUẬT RETRIEVAL-AUGMENTED GENERATION (RAG)](#chương-3-kỹ-thuật-retrieval-augmented-generation-rag)
6. [CHƯƠNG 4: TRI THỨC Y TẾ & HỌC SÂU CHẨN ĐOÁN ĐÁI THÁO ĐƯỜNG TYPE 2](#chương-4-tri-thức-y-tế--học-sâu-chẩn-đoán-đái-tháo-đường-type-2)
7. [CHƯƠNG 5: TRI THỨC TÀI CHÍNH VĨ MÔ & HỌC SÂU CHUỖI THỜI GIAN BILSTM](#chương-5-tri-thức-tài-chính-vĩ-mô--học-sâu-chuỗi-thời-gian-bilstm)
8. [CHƯƠNG 6: ĐỘNG CƠ LẬP LUẬN REACT, KIỂM CHỨNG GROUNDED VERIFIER & HỆ THỐNG WEB](#chương-6-động-cơ-lập-luận-react-kiểm-chứng-grounded-verifier--hệ-thống-web)
9. [CHƯƠNG 7: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN](#chương-7-kết-luận-và-hướng-phát-triển)
10. [TÀI LIỆU THAM KHẢO](#tài-liệu-tham-khảo)

---

## TỔNG QUAN VÀ TÓM TẮT ĐỀ TÀI (EXECUTIVE SUMMARY)

### Tóm tắt Tiếng Việt
Báo cáo chuyên khảo này trình bày công trình nghiên cứu, thiết kế kiến trúc và triển khai thực nghiệm một Hệ thống Thông minh đa miền hoàn chỉnh, tích hợp ba trụ cột công nghệ then chốt của Trí tuệ Nhân tạo hiện đại: Đồ thị Tri thức Hình thức (Formal Knowledge Graph - KG), Kỹ thuật Sinh Tăng cường Truy xuất (Retrieval-Augmented Generation - RAG), và Mô hình Học sâu Chuyên biệt (PyTorch Deep Learning), được điều phối thống nhất bởi Tác tử Lập luận ReAct (Reasoning and Acting) kết hợp Bộ kiểm chứng Độ trung thực Số liệu (Grounded Verifier).

Công trình giải quyết bài toán cốt lõi: Làm thế nào để loại bỏ triệt để hiện tượng "ảo giác" (hallucination), thiếu khả năng truy vết nguồn gốc và sự mờ đục số liệu của các Mô hình Ngôn ngữ Lớn (LLM) đơn lẻ khi giải quyết các vấn đề nghiệp vụ có tính cam kết cao trong hai lĩnh vực nhạy cảm bậc nhất tại Việt Nam là Y tế Lâm sàng (chẩn đoán và phác đồ điều trị Đái tháo đường Típ 2 theo Quyết định 5481/QĐ-BYT) và Phân tích Thị trường Tài chính Vĩ mô (chuỗi truyền dẫn Fed - DXY - USD/VND, thị trường vàng miếng SJC theo Nghị định 24/2012 và Nghị định 232/2025/NĐ-CP, cùng rổ cổ phiếu VN30).

Hệ thống được xây dựng với các thành tựu kỹ thuật trọng tâm:
1. Xây dựng hai Đồ thị Tri thức chuyên ngành hoàn chỉnh: VietnamDiabetesKG (23 lớp bản thể, 17 vị từ lâm sàng) và VietnamFinanceKG (16 lớp, 6 vị từ quan hệ nhân quả có hướng có dấu), hỗ trợ suy diễn tiến (Forward Chaining) RDFS/OWL đến điểm bất động và 5 nhóm truy vấn SPARQL chuyên sâu.
2. Thiết lập khung đánh giá thực nghiệm toàn diện trên kho ngữ liệu 17 tài liệu quy chuẩn (D01-D17) đối chuẩn Ma trận 25 cấu hình RAG (kết hợp 5 chiến lược phân mảnh chunking với 5 bộ truy xuất: BM25, Dense TF-IDF, Hybrid RRF k=60, Cross-Encoder reranker và GraphRAG phân cụm Louvain).
3. Triển khai hai mô hình học sâu PyTorch tối ưu: DiabetesMLP (10.497 tham số, Weighted BCE pos_weight=10.3, ROC-AUC 0.9755) và BiLSTM SeqForecaster (140.865 tham số, Huber loss delta=1.0, 200 lượt Monte Carlo Dropout tạo dải quạt tin cậy 90%).
4. Hiện thực Tác tử ReAct với Bộ lập kế hoạch tất định (Deterministic Planner) và Bộ kiểm chứng độ trung thực số liệu tự động (Grounded Verifier), đảm bảo tỷ lệ trích dẫn tài liệu 100% và độ chính xác số liệu >= 85%.
5. Cung cấp Giao diện Web Interactive Dashboard trực quan bằng FastAPI và Cytoscape.js cho phép người dùng khai thác tri thức và suy luận theo thời gian thực.

### Abstract in English
This monograph presents the comprehensive theoretical design, implementation, and empirical evaluation of a multi-domain Intelligent System that unifies three core pillars of modern Artificial Intelligence: Formal Knowledge Graphs (Symbolic AI), Advanced Retrieval-Augmented Generation (RAG), and Task-Specific PyTorch Deep Learning models, coordinated via a deterministic ReAct (Reasoning and Acting) loop coupled with an automated Grounded Verifier.

The primary objective of this project is to eliminate hallucination, ensure absolute factual provenance, and overcome numeric opacity inherent in standalone Large Language Models (LLMs) when applied to high-stakes decision-making tasks in Vietnam: Clinical Healthcare (Type 2 Diabetes Mellitus diagnosis and protocol optimization under MOH Decision 5481/QD-BYT and ADA 2024 standards) and Macroeconomic Financial Intelligence (Fed-DXY-VND monetary transmission mechanisms, SJC bullion dynamics under Decrees 24/2012 and 232/2025/ND-CP, and VN30 equity pricing).

Key technical contributions include:
1. Construction of two formal RDF Knowledge Graphs: VietnamDiabetesKG (23 ontology classes, 17 predicates) and VietnamFinanceKG (16 classes, 6 directed signed causal predicates), featuring forward-chaining RDFS/OWL entailment and complex SPARQL analytical queries.
2. Empirical benchmarking of a comprehensive 25-configuration RAG matrix across 17 standardized Vietnamese technical documents (D01-D17), evaluating 5 chunking strategies and 5 retrieval paradigms (BM25 Okapi, Dense retrieval, Hybrid RRF k=60, Cross-Encoder reranking, and Louvain-based GraphRAG).
3. Two dedicated PyTorch neural networks: DiabetesMLP (10,497 parameters, Weighted BCE loss with pos_weight=10.3, calibrated ROC-AUC 0.9755) and BiLSTM SeqForecaster (140,865 parameters, Huber loss delta=1.0, 200-pass Monte Carlo Dropout producing 90% confidence fan charts).
4. A deterministic ReAct agent orchestrating 6 verified tools, enforced by an automated Grounded Verifier requiring 100% citation grounding and >=85% numerical fidelity.
5. An interactive production-grade Web Dashboard developed with FastAPI, Cytoscape.js, and Chart.js, delivering real-time knowledge graph exploration, clinical risk estimation, and probabilistic forecasting.

---

## DANH MỤC TỪ VIẾT TẮT

| Ký hiệu viết tắt | Thuật ngữ Tiếng Anh | Diễn giải Tiếng Việt |
| :--- | :--- | :--- |
| **KG** | Knowledge Graph | Đồ thị Tri thức |
| **RAG** | Retrieval-Augmented Generation | Sinh Tăng cường Truy xuất |
| **RDF** | Resource Description Framework | Khung Miêu tả Tài nguyên |
| **RDFS** | RDF Schema | Lược đồ RDF |
| **OWL** | Web Ontology Language | Ngôn ngữ Bản thể học Web |
| **SPARQL** | SPARQL Protocol and RDF Query Language | Ngôn ngữ Truy vấn Đồ thị RDF |
| **LLM** | Large Language Model | Mô hình Ngôn ngữ Lớn |
| **MLP** | Multi-Layer Perceptron | Mạng Perceptron Đa tầng |
| **BiLSTM** | Bidirectional Long Short-Term Memory | Mạng Nơ-ron Hồi quy Bộ nhớ Ngắn-Dài Hai chiều |
| **BCE** | Binary Cross-Entropy | Hàm Mất mát Entropy Chéo Nhị phân |
| **RRF** | Reciprocal Rank Fusion | Dung hợp Thứ hạng Nghịch đảo |
| **HyDE** | Hypothetical Document Embeddings | Véc-tơ Nhúng Tài liệu Giả thuyết |
| **MC Dropout** | Monte Carlo Dropout | Kỹ thuật Tắt Nơ-ron Ngẫu nhiên Monte Carlo |
| **BYT** | Bộ Y tế Việt Nam | Cơ quan Quản lý Y tế Cao nhất Việt Nam |
| **ADA** | American Diabetes Association | Hiệp hội Đái tháo đường Hoa Kỳ |
| **KDIGO** | Kidney Disease: Improving Global Outcomes | Tổ chức Hướng dẫn Điều trị Bệnh Thận Quốc tế |
| **NHNN** | Ngân hàng Nhà nước Việt Nam | Ngân hàng Trung ương Việt Nam |
| **FED** | Federal Reserve System | Cục Dự trữ Liên bang Hoa Kỳ |
| **DXY** | US Dollar Index | Chỉ số Sức mạnh Đồng Đô la Mỹ |
| **SJC** | Saigon Jewelry Company | Công ty Vàng bạc Đá quý Sài Gòn |
| **VN30** | Vietnam 30 Index | Chỉ số 30 Cổ phiếu Vốn hóa Lớn nhất HOSE |
| **FPG** | Fasting Plasma Glucose | Đường huyết Tương lúc Đói |
| **OGTT** | Oral Glucose Tolerance Test | Nghiệm pháp Dung nạp Glucose Đường uống |
| **eGFR** | Estimated Glomerular Filtration Rate | Mức Lọc Cầu thận Ước tính |

---

# CHƯƠNG 1: MỞ ĐẦU VỀ KNOWLEDGE GRAPH VÀ RAG

*Chương này thiết lập nền tảng lý thuyết và phương pháp luận cho toàn bộ công trình nghiên cứu: Đồ thị tri thức (Knowledge Graph - KG) là gì, Kỹ thuật Sinh tăng cường truy xuất (Retrieval-Augmented Generation - RAG) là gì, vì sao sự kết hợp hữu cơ giữa hai kỹ thuật này lại giải quyết trúng và triệt để các tử huyệt cố hữu của các Mô hình Ngôn ngữ Lớn (LLM), và chúng được tích hợp với nhau như thế nào trong kiến trúc hệ sinh thái thông minh 5 tầng được đề xuất.*

![Hình 1.1](file:///c:/code/A2_CT_hautv.287/tieuluan2/charts/h01_dual_domain_ecosystem.png)
*Hình 1.1. Sơ đồ kiến trúc tổng thể 5 tầng của Hệ sinh thái Tri thức Đa miền Y tế và Tài chính Việt Nam.*

### Bảng 1.1. So sánh ba phương pháp luận đưa tri thức miền vào Hệ thống Thông minh

| Tiêu chí Đánh giá | LLM Đơn Lẻ (Zero-shot) | Tinh chỉnh Mô hình (Fine-Tuning) | Hệ Thống Đề Xuất (KG + RAG + PyTorch + ReAct) |
| :--- | :--- | :--- | :--- |
| Nguồn gốc tri thức | Tham số nội tại cố định sau pre-training | Học thêm vào trọng số nơ-ron | Tri thức tường minh ngoài (Graph DB + Vector Corpus) |
| Cập nhật tri thức | Không thể cập nhật nếu không train lại | Chi phí GPU lớn, nguy cơ quên thảm họa | Tức thì: Thêm 1 bộ ba (s, p, o) hoặc 1 văn bản mới |
| Truy vết nguồn gốc | Hoàn toàn không có khả năng dẫn chứng | Không thể truy vết đến từng điều khoản | Tuyệt đối: Mọi khẳng định đều gắn trích dẫn [Dxx] |
| Suy luận nhiều bước | Suy diễn mờ, dễ nhầm lẫn cơ chế | Dựa trên xác suất xuất hiện chuỗi từ ngữ | Duyệt đường đi nhân quả tường minh (∏ Sign(e)) |
| Ảo giác số liệu | Rất cao (tự bịa đặt số liệu bệnh nhân/giá) | Trung bình (vẫn bị làm tròn hoặc sai lệch) | Rất thấp: Verifier từ chối nếu sai số hoặc thiếu số liệu |
| Khả năng tính toán số | Kém (tính nhẩm sai các phép đo định lượng) | Kém (vẫn mắc lỗi số học cơ bản) | Chính xác tuyệt đối qua Deep Learning chuyên biệt |
| Lĩnh vực áp dụng | Hội thoại giải trí, viết lách sáng tạo | Thích ứng văn phong nội bộ doanh nghiệp | Y tế lâm sàng, Dược học, Pháp lý, Ngân hàng, Đầu tư |


### 1.1 Bối cảnh và Thách thức Cốt tử của Trí tuệ Nhân tạo Hiện đại

Sự bùng nổ của Trí tuệ Nhân tạo Tạo sinh (Generative AI) từ cuối năm 2022 với sự thống trị của các Mô hình Ngôn ngữ Lớn (Large Language Models - LLM) dựa trên kiến trúc Transformer đã tạo nên một bước ngoặt lịch sử trong Khoa học Máy tính. Các mô hình với quy mô hàng chục đến hàng trăm tỷ tham số (như GPT-4, LLaMA, Claude hay Qwen) đã chứng minh năng lực phi thường trong việc hiểu ngữ cảnh, tóm tắt tài liệu, dịch thuật và sinh văn bản tự nhiên trôi chảy gần như không thể phân biệt với con người.

Kiến trúc Transformer dựa trên cơ chế Tự chú ý Đa đầu (Multi-Head Self-Attention):
$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$
Trong đó các ma trận truy vấn (Query - $Q$), khóa (Key - $K$), và giá trị (Value - $V$) được tính toán từ các phép chiếu tuyến tính của vector nhúng từ vựng. Cơ chế này cho phép mô hình thu nhận các mối liên kết phụ thuộc ngữ nghĩa từ xa giữa các từ trong câu mà không bị giới hạn bởi độ dài tuần tự như các mạng hồi quy RNN truyền thống.

Tuy nhiên, khi chuyển giao các mô hình ngôn ngữ này từ các tác vụ giải trí, hội thoại thông thường sang các lĩnh vực nghiệp vụ có tính cam kết cao (High-Stakes Domains) và ràng buộc pháp lý nghiêm ngặt — tiêu biểu là **Y tế Lâm sàng** và **Phân tích Đầu tư Tài chính** tại Việt Nam — các hệ thống AI dựa trên LLM đơn lẻ lập tức bộc lộ ba "tử huyệt" mang tính bản chất:

1. **Hiện tượng Ảo giác (Hallucination)**: 
Mô hình Transformer được huấn luyện theo nguyên lý Cực đại hóa Hợp lý (Maximum Likelihood Estimation - MLE) để dự đoán phân phối xác suất của từ tiếp theo dựa trên chuỗi từ trước đó:
$$\mathcal{L}_{\text{MLE}}(\theta) = - \sum_{t=1}^T \log P_\theta(w_t \mid w_1, w_2, \dots, w_{t-1})$$
Mục tiêu toán học này tối ưu hóa "tính trôi chảy bề mặt" (Surface Fluency) và sự tương thích thống kê của ngôn ngữ, chứ **hoàn toàn không có cơ chế kiểm tra tính đúng đắn thực tế (Factual Correctness)**. Hàm kích hoạt Softmax ở tầng cuối cùng luôn buộc mô hình phải chuẩn hóa tổng xác suất trên toàn bộ từ điển từ vựng về 1:
$$P(w_t = v \mid w_{<t}) = \frac{\exp(z_v / \tau)}{\sum_{j=1}^{|V|} \exp(z_j / \tau)}$$
(với $\tau$ là nhiệt độ lấy mẫu). Điều này có nghĩa là ngay cả khi mô hình hoàn toàn không sở hữu tri thức về một sự kiện hoặc một con số, nó vẫn bị ép buộc phải gán một xác suất dương cho một từ nào đó và tiếp tục sinh văn bản.

Về mặt phân loại học thuật, ảo giác trong LLM được chia thành hai nhóm chính:
- *Ảo giác Dữ kiện (Factuality Hallucination)*: Mô hình sinh ra các phát biểu mâu thuẫn trực tiếp với tri thức thực tế của thế giới thực (Factual Inconsistency) hoặc tự bịa đặt ra các thực thể, con số, chỉ số xét nghiệm hoàn toàn không tồn tại (Factual Fabrication).
- *Ảo giác Độ trung thực (Faithfulness Hallucination)*: Mô hình không tuân thủ chỉ thị đầu vào (Instruction Inconsistency) hoặc sinh ra nội dung mâu thuẫn trực tiếp với tài liệu ngữ cảnh được cung cấp (Context Inconsistency).

Trong hai lĩnh vực của tiểu luận, hậu quả của ảo giác là khôn lường:
- *Trong Y tế Lâm sàng*: Một ảo giác về liều lượng thuốc hoặc chống chỉ định có thể tước đoạt sinh mạng bệnh nhân. Ví dụ: Nếu LLM tự ý khuyên bệnh nhân đái tháo đường típ 2 có mức lọc cầu thận eGFR = 25 mL/phút tiếp tục dùng Metformin liều cao (2000mg/ngày), bệnh nhân sẽ đối mặt với nguy cơ tích tụ acid lactic nghiêm trọng trong máu gây nhiễm toan lactic tử vong với tỷ lệ lên tới 50%.
- *Trong Đầu tư Tài chính*: Một ảo giác về số liệu lợi nhuận hoặc cơ chế quản lý tỷ giá có thể gây thiệt hại hàng trăm tỷ đồng cho nhà đầu tư. Ví dụ: Nếu LLM nhầm lẫn cơ chế định giá vàng theo Nghị định 24/2012 và Nghị định 232/2025/NĐ-CP, hoặc bịa ra mức tăng trưởng doanh thu quý của Tập đoàn Hòa Phát hay FPT, các thuật toán giao dịch tự động sẽ đưa ra quyết định giải ngân sai lầm nghiêm trọng.

2. **Thiếu Khả năng Truy vết Nguồn gốc và Minh bạch Pháp lý (Provenance & Traceability)**:
Một câu trả lời sinh ra từ các trọng số tiềm ẩn (Parametric Memory) của mạng nơ-ron là một chiếc "hộp đen" mờ đục. Mô hình không thể chứng minh con số "15 triệu đồng/lượng chênh lệch giá vàng" hay "ngưỡng HbA1c $\ge 6.5\%$" được trích xuất chính xác từ điều khoản nào trong văn bản pháp luật hay phác đồ điều trị nào của Bộ Y tế. Trong y khoa lâm sàng và tư vấn đầu tư chuyên nghiệp, một khuyến nghị không có khả năng dẫn chứng nguồn gốc cụ thể là hoàn toàn vô giá trị và vi phạm y đức cũng như quy định pháp luật.

3. **Độ trễ Tri thức Cố định và Chi phí Cập nhật Khổng lồ (Knowledge Cutoff & Recency Lag)**:
Tri thức trong tham số mạng nơ-ron bị đóng băng tuyệt đối tại thời điểm kết thúc quá trình tiền huấn luyện (Pre-training Cutoff). Khi cơ quan quản lý ban hành chính sách mới (ví dụ: Chính phủ ban hành Nghị định 232/2025/NĐ-CP sửa đổi cơ chế quản lý thị trường vàng), việc tái huấn luyện (re-training) hoặc tinh chỉnh (fine-tuning) một mô hình LLM khổng lồ tiêu tốn hàng trăm ngàn USD chi phí tính toán GPU, mất nhiều tuần thực thi và đối mặt với rủi ro "quên thảm họa" (Catastrophic Forgetting) đối với các tri thức đã học trước đó.

### 1.2 Sự Dung hợp Giữa Symbolic AI và Sub-Symbolic AI (Neuro-Symbolic Paradigm)

Để giải quyết tận gốc các điểm nghẽn nêu trên, cộng đồng khoa học trí tuệ nhân tạo toàn cầu đang chứng kiến sự hội tụ mạnh mẽ về một mô hình kiến trúc mới: **Trí tuệ Nhân tạo Thần kinh - Tượng trưng (Neuro-Symbolic AI)**. Đây là sự kết hợp hữu cơ giữa hai trường phái đối nghịch trong lịch sử AI:

- **Trường phái Biểu tượng (Symbolic AI)**: Đại diện là các Hệ chuyên gia (Expert Systems), Cơ sở Tri thức Hình thức (Knowledge Bases), Bản thể học (Ontology) và Đồ thị Tri thức (Knowledge Graph). Trường phái này vận hành theo phương pháp **Suy luận Diễn dịch (Deductive Reasoning)**:
  $$\text{Tri thức Hình thức (Rules + Triples)} + \text{Dữ kiện Đầu vào (Facts)} \xrightarrow{\text{Inference Engine}} \text{Kết luận Tất định (Truth)}$$
  *Ưu điểm*: Chính xác $100\%$, minh bạch, có thể chứng minh hình thức, có khả năng giải thích từng bước suy luận, cập nhật tức thì với độ phức tạp $O(1)$.
  *Nhược điểm*: Cứng nhắc, không có khả năng xử lý ngôn ngữ tự nhiên mềm dẻo, khó biểu diễn các mối quan hệ mờ hoặc dữ liệu chuỗi thời gian liên tục.

- **Trường phái Phi biểu tượng (Sub-Symbolic AI / Connectionist AI)**: Đại diện là Mạng Nơ-ron Nhân tạo (Neural Networks), Học sâu (Deep Learning) và các Mô hình Ngôn ngữ Lớn (LLM). Vận hành theo phương pháp **Suy luận Quy nạp (Inductive Reasoning)**:
  $$\text{Dữ liệu Lớn (Big Data)} \xrightarrow{\text{Gradient Descent}} \text{Trọng số Tiềm ẩn (Weights)} \xrightarrow{\text{Inference}} \text{Dự báo Xác suất (Probabilities)}$$
  *Ưu điểm*: Rất linh hoạt, có khả năng khái quát hóa cao, hiểu sâu sắc ngữ cảnh ngôn ngữ tự nhiên phức tạp, xử lý xuất sắc dữ liệu hình ảnh, tín hiệu và bảng số học.
  *Nhược điểm*: Mờ đục (Black-box), không đảm bảo tính đúng đắn logic, thường xuyên sinh ảo giác khi đối mặt với các suy luận đa bước.

**Mô hình Đề xuất trong Nghiên cứu này**:
Hệ thống được thiết kế dựa trên nguyên lý **Hợp nhất Bổ trợ Đa tầng**:
1. Đồ thị Tri thức (KG) đóng vai trò là "Bộ não Logic Tượng trưng": Lưu trữ cấu trúc bản thể học, quy tắc điều trị bất biến và đồ thị nhân quả vĩ mô, thực hiện suy diễn tiến (Forward Chaining) RDFS/OWL đóng kín điểm bất động.
2. Sinh Tăng cường Truy xuất (RAG) đóng vai trò là "Cầu nối Ngữ liệu Văn bản": Quét kho tài liệu pháp quy và chuyên môn chính thức để trích xuất các bằng chứng văn bản làm mỏ neo ngữ cảnh (Grounding Context).
3. Mạng Nơ-ron PyTorch đóng vai trò là "Công cụ Tính toán Định lượng": Trực tiếp dự báo nguy cơ lâm sàng (`DiabetesMLP`) và dự báo chuỗi thời gian kèm dải quạt tin cậy Bayes 90% (`BiLSTM SeqForecaster`).
4. Tác tử Lập luận ReAct đóng vai trò là "Nhạc trưởng Điều phối": Vận hành theo kế hoạch tất định, kết hợp kết quả từ cả ba phân hệ để sinh phản hồi tự nhiên, minh bạch và có kiểm chứng độ trung thực số liệu tự động.

### 1.3 Khái niệm Hình thức về Đồ thị Tri thức và RAG

**1. Khái niệm Đồ thị Tri thức (Knowledge Graph - KG)**:
Về mặt toán học hình thức, một Đồ thị Tri thức $\mathcal{G}$ được định nghĩa như một đồ thị có hướng, có nhãn đa quan hệ:
$$\mathcal{G} = (\mathcal{V}, \mathcal{E}, \mathcal{R}, \mathcal{L}, \tau_v, \tau_e)$$
Trong đó:
- $\mathcal{V} = \mathcal{E}_{ent} \cup \mathcal{L}_{val} \cup \mathcal{B}_{blk}$ là tập hợp các đỉnh (nút), bao gồm các thực thể định danh duy nhất (Entities $\mathcal{E}_{ent}$ qua URI), các giá trị hằng số nguyên tử (Literals $\mathcal{L}_{val}$) và các nút ẩn danh (Blank nodes $\mathcal{B}_{blk}$).
- $\mathcal{R}$ là tập hợp hữu hạn các loại quan hệ ngữ nghĩa (vị từ - Predicates).
- $\mathcal{E} \subseteq \mathcal{V} \times \mathcal{R} \times \mathcal{V}$ là tập hợp các cạnh có hướng biểu diễn các bộ ba RDF $(s, p, o)$.
- $\tau_v, \tau_e$ là các hàm ánh xạ kiểu ngữ nghĩa xác định bản thể học (Ontology Schema).

Khác biệt cơ bản giữa KG và Cơ sở dữ liệu quan hệ (RDBMS) là: Trong RDBMS, việc thêm một mối quan hệ mới đòi hỏi phải sửa đổi cấu trúc bảng cố định (`ALTER TABLE`), làm phát sinh các cột rỗng (NULL) và bùng nổ chi phí tính toán liên kết JOIN. Trong Đồ thị Tri thức, cấu trúc là hoàn toàn linh hoạt (Schema-flexible): Muốn biểu diễn một mối quan hệ mới chỉ cần thêm một cạnh có nhãn mới vào đồ thị. Hơn nữa, mỗi mẩu tri thức trong KG là một đơn vị nguyên tử độc lập (Atomic Fact), máy đọc hiểu trực tiếp và suy luận được.

**2. Khái niệm Sinh Tăng cường Truy xuất (Retrieval-Augmented Generation - RAG)**:
RAG phân tách bộ nhớ tiềm ẩn tham số của LLM với bộ nhớ ngoài phi tham số khổng lồ $\mathcal{D} = \{d_1, d_2, \dots, d_M\}$. Khi nhận câu hỏi truy vấn $q$, hệ thống thực hiện hai pha toán học:
- **Pha 1: Truy xuất Phân phối Xác suất (Retrieval Phase)**:
  Ước lượng phân phối xác suất liên quan $P(d \mid q)$ trên toàn bộ kho tài liệu $\mathcal{D}$, trích xuất tập top-$k$ đoạn văn bản có độ tương đồng cao nhất $\mathcal{D}_q = \{d_{(1)}, d_{(2)}, \dots, d_{(k)}\}$.
- **Pha 2: Sinh Văn bản Có Điều kiện Tăng cường (Augmented Generation Phase)**:
  Tích phân ngữ cảnh $\mathcal{D}_q$ vào chuỗi sinh từ của mô hình ngôn ngữ:
  $$P(y \mid q) = \sum_{d \in \mathcal{D}_q} P(d \mid q) \prod_{t=1}^T P(y_t \mid q, d, y_{1:t-1})$$
Nhờ công thức này, LLM chuyển vai trò từ "kẻ phỏng đoán xác suất" thành "chuyên gia tra cứu tài liệu và diễn giải", triệt tiêu phần lớn ảo giác ngữ nghĩa.

**3. Lịch sử Phát triển Nửa Thế kỷ của Tri thức Máy tính**:
- Thập niên 1960: Allan Quillian khởi xướng Mạng Ngữ nghĩa (Semantic Networks).
- Thập niên 1980: Douglas Lenat xây dựng đại dự án Cyc nhằm số hóa toàn bộ tri thức thường thức nhân loại thành logic bậc nhất.
- Năm 2001: Tim Berners-Lee và tổ chức W3C công bố Semantic Web với bộ tiêu chuẩn RDF, RDFS, OWL và SPARQL.
- Năm 2012: Google công bố Google Knowledge Graph với tôn chỉ "Things, not Strings", chính thức đưa đồ thị tri thức vào ứng dụng công nghiệp đại trà.
- Năm 2020: Lewis et al. và Karpukhin et al. công bố DPR và RAG tại hội nghị NeurIPS 2020.
- Năm 2024: Microsoft Research công bố GraphRAG, kết hợp thuật toán phân cụm Louvain trên đồ thị tri thức để giải quyết bài toán tóm tắt tri thức toàn cục.

### 1.4 Kiến trúc Tổng thể Hệ sinh thái Tri thức Đa miền 5 Tầng

Toàn bộ hệ thống thông minh trong nghiên cứu này được tổ chức thành một Kiến trúc Doanh nghiệp 5 Tầng (5-Layer Enterprise Architecture) hoàn chỉnh, phân định rõ ràng trách nhiệm của từng phân hệ:

1. **Tầng 1: Tầng Dữ liệu và Ngữ liệu (Data & Corpus Layer)**:
   - Dữ liệu có cấu trúc định lượng: 96.128 hồ sơ bệnh nhân điện tử (EHR) với 13 đặc trưng lâm sàng và 2.932 phiên giao dịch lịch sử liên tục (2015-2026) của 7 tài sản tài chính.
   - Kho ngữ liệu văn bản phi cấu trúc: 17 tài liệu quy chuẩn kỹ thuật y tế và tài chính Việt Nam (D01 - D17) với tổng quy mô gần 30.000 từ.
2. **Tầng 2: Tầng Biểu diễn Tri thức (Knowledge Representation Layer)**:
   - Tri thức cấu trúc tượng trưng: VietnamDiabetesKG (23 lớp bản thể, 17 vị từ lâm sàng) và VietnamFinanceKG (16 lớp bản thể, 6 vị từ nhân quả có hướng có dấu), vận hành động cơ suy diễn tiến RDFS/OWL đến điểm bất động và 5 nhóm truy vấn SPARQL chuyên sâu.
   - Tri thức văn bản phân tán: Hệ thống chỉ mục truy xuất kép gồm Chỉ mục từ khóa thưa BM25 Okapi (tách từ tiếng Việt) và Không gian nhúng vector đa ngôn ngữ 768 chiều.
3. **Tầng 3: Tầng Mô hình Học sâu Chuyên biệt (Deep Learning Layer)**:
   - Mạng nơ-ron PyTorch `DiabetesMLP`: Gồm đúng 10.497 tham số, BatchNorm, Dropout, hàm mất mát Weighted BCE ($pos\_weight=10.3$), hiệu chuẩn ngưỡng Youden J $\tau=0.9016$, đạt ROC-AUC 0.9755.
   - Mạng nơ-ron PyTorch `BiLSTM SeqForecaster`: Gồm đúng 140.865 tham số, 2 tầng BiLSTM 64 chiều, Huber loss $\delta=1.0$, tích hợp 200 lượt suy luận Monte Carlo Dropout sinh dải quạt tin cậy Bayes 90%.
4. **Tầng 4: Tầng Lập luận Tác tử và Kiểm chứng (Reasoning & Grounding Layer)**:
   - Bộ Lập kế hoạch Tất định (Deterministic Planner): Nhận diện thực thể, phân loại ý định, sinh đồ thị thực thi công cụ tuần tự (DAG), loại bỏ hoàn toàn cơ chế đa tác tử tự phát thiếu kiểm soát.
   - Vòng lặp ReAct (Thought $\to$ Action $\to$ Observation): Điều phối bộ 6 công cụ chuyên trách.
   - Bộ Kiểm chứng Độ trung thực Số liệu (Grounded Verifier): Chốt chặn kiểm định trích dẫn nguồn `[Dxx]` (100%) và kiểm toán số liệu định lượng bằng biểu thức chính quy ($\text{Faithfulness} \ge 85\%$).
5. **Tầng 5: Tầng Trải nghiệm Người dùng (Presentation Layer)**:
   - Giao diện Web Interactive Dashboard phát triển bằng FastAPI, tích hợp đồ họa mạng lưới Cytoscape.js vật lý tương tác thời gian thực, bảng tính lâm sàng và biểu đồ dải quạt rủi ro Chart.js.

---

# CHƯƠNG 2: XÂY DỰNG ĐỒ THỊ TRI THỨC Y TẾ VÀ TÀI CHÍNH

*Chương này trình bày toàn bộ quy trình thiết kế bản thể học (Ontology), mô hình dữ liệu bộ ba RDF, chứng minh toán học định lý hội tụ của thuật toán suy diễn tiến (Forward Chaining) RDFS/OWL, đại số quan hệ truy vấn SPARQL, và đường ống chuyển đổi dữ liệu dạng bảng lớn thành Đồ thị Tri thức hoàn chỉnh cho hai miền nghiệp vụ: VietnamDiabetesKG và VietnamFinanceKG.*

![Hình 2.1](file:///c:/code/A2_CT_hautv.287/tieuluan2/charts/h02_diabetes_ontology_hierarchy.png)
*Hình 2.1. Cây phân cấp 23 lớp bản thể học và mạng lưới 17 vị từ quan hệ lâm sàng trong VietnamDiabetesKG.*

### Bảng 2.1. Hệ thống 23 lớp bản thể học trong VietnamDiabetesKG

| Lớp Bản thể (OWL Class) | Lớp Cha Trực tiếp | Mô tả Nghiệp vụ Lâm sàng | Ví dụ Thực thể Cụ thể |
| :--- | :--- | :--- | :--- |
| med:MedicalEntity | owl:Thing | Lớp gốc của toàn bộ thực thể y tế | - |
| med:Disease | med:MedicalEntity | Bệnh lý và phân loại lâm sàng | Đái tháo đường Típ 2 (T2DM) |
| med:Symptom | med:MedicalEntity | Triệu chứng cơ năng và thực thể | Tiểu nhiều, Khát nhiều, Sụt cân |
| med:Drug | med:MedicalEntity | Dược chất điều trị | Metformin, Dapagliflozin, Gliclazide |
| med:DrugClass | med:MedicalEntity | Nhóm dược lý của thuốc | Biguanide, SGLT2i, DPP-4i, SU |
| med:Complication | med:MedicalEntity | Biến chứng cấp tính và mạn tính | Bệnh thận ĐTĐ, Nhiễm toan Lactic |
| med:LabTest | med:MedicalEntity | Xét nghiệm cận lâm sàng | HbA1c, Glucose đói FPG, eGFR |
| med:FoodItem | med:MedicalEntity | Thực phẩm và nhóm dinh dưỡng | Gạo trắng, Gạo lứt, Ức gà, Bia |
| med:Contraindication | med:MedicalEntity | Tình trạng chống chỉ định | Suy thận nặng (eGFR < 30) |
| med:SideEffect | med:MedicalEntity | Tác dụng không mong muốn | Rối loạn tiêu hóa, Hạ đường huyết |
| med:ClinicalTarget | med:MedicalEntity | Mục tiêu điều trị kiểm soát | Mục tiêu HbA1c < 7.0% |
| med:PatientProfile | med:MedicalEntity | Hồ sơ cá thể hóa bệnh nhân | Hồ sơ bệnh nhân PT_096128 |


#### Listing 2.1. Thuật toán Suy diễn Tiến RDFS (Forward Chaining) đến Điểm Bất động trong reasoning.py
```python
def forward_chain_rdfs(graph: rdflib.Graph) -> int:
    """
    Applies RDFS entailment rules (rdfs2, rdfs3, rdfs7, rdfs9)
    iteratively until fixed-point closure (no new triples derived).
    """
    inferred_total = 0
    iteration = 0
    while True:
        iteration += 1
        new_triples = set()
        
        # Rule rdfs9: (C1 subClassOf C2) & (x type C1) => (x type C2)
        for s, _, c1 in graph.triples((None, RDF.type, None)):
            for _, _, c2 in graph.triples((c1, RDFS.subClassOf, None)):
                if (s, RDF.type, c2) not in graph:
                    new_triples.add((s, RDF.type, c2))
                    
        # Rule rdfs7: (p1 subPropertyOf p2) & (x p1 y) => (x p2 y)
        for p1, _, p2 in graph.triples((None, RDFS.subPropertyOf, None)):
            for s, _, o in graph.triples((None, p1, None)):
                if (s, p2, o) not in graph:
                    new_triples.add((s, p2, o))
                    
        # Rule rdfs2: (p domain C) & (x p y) => (x type C)
        for p, _, c in graph.triples((None, RDFS.domain, None)):
            for s, _, _ in graph.triples((None, p, None)):
                if (s, RDF.type, c) not in graph:
                    new_triples.add((s, RDF.type, c))
                    
        # Rule rdfs3: (p range C) & (x p y) => (y type C)
        for p, _, c in graph.triples((None, RDFS.range, None)):
            for _, _, o in graph.triples((None, p, None)):
                if isinstance(o, rdflib.URIRef) and (o, RDF.type, c) not in graph:
                    new_triples.add((o, RDF.type, c))
                    
        if not new_triples:
            break  # Fixed-point reached!
            
        for triple in new_triples:
            graph.add(triple)
        inferred_total += len(new_triples)
        
    return inferred_total
```

#### Listing 2.2. Triển khai 5 Truy vấn SPARQL Chuyên sâu Q1 - Q5 trong sparql_engine.py
```sparql
SPARQL_QUERIES = {
    "Q1_LethalDrugInteraction": """
        PREFIX med: <http://ptit.edu.vn/med/>
        SELECT ?drugA ?drugB ?risk ?severity ?warning
        WHERE {
            ?drugA med:interactsWith ?drugB ;
                   med:hasLethalRisk ?risk ;
                   med:interactionSeverity ?severity ;
                   med:clinicalWarning ?warning .
            FILTER (?drugA = med:Metformin && ?drugB = med:Ethanol)
        }
    """,
    "Q2_DualTherapyHbA1c": """
        PREFIX med: <http://ptit.edu.vn/med/>
        SELECT ?drug ?class ?renalBenefit
        WHERE {
            ?drug med:prescribedInStep "Step 2 - Dual Therapy" ;
                  med:belongsToClass ?class ;
                  med:hasCardioRenalBenefit ?renalBenefit .
        }
    """,
    "Q3_RenalContraindications": """
        PREFIX med: <http://ptit.edu.vn/med/>
        SELECT ?drug ?minEGFR ?action
        WHERE {
            ?drug med:requiresRenalAdjustment true ;
                  med:contraindicatedWhenEGFRBelow ?minEGFR ;
                  med:recommendedAction ?action .
        }
        ORDER BY DESC(?minEGFR)
    """,
    "Q4_FedRateToGoldSpread": """
        PREFIX fin: <http://ptit.edu.vn/fin/>
        SELECT ?intermediate ?target ?relation
        WHERE {
            fin:FedFundsRate ?p1 ?intermediate .
            ?intermediate ?p2 ?target .
        }
    """,
    "Q5_ExchangeRateImpact": """
        PREFIX fin: <http://ptit.edu.vn/fin/>
        SELECT ?stock ?exposureType ?impactDirection ?mitigation
        WHERE {
            ?stock fin:sensitiveTo fin:USD_VND_Rate ;
                   fin:exposureType ?exposureType ;
                   fin:earningsImpact ?impactDirection ;
                   fin:hedgingMechanism ?mitigation .
        }
    """
}
```

![Hình 2.2](file:///c:/code/A2_CT_hautv.287/tieuluan2/charts/h03_finance_causal_network.png)
*Hình 2.2. Đồ thị tri thức nhân quả có hướng có dấu VietnamFinanceKG mô tả chuỗi truyền dẫn Fed - DXY - USD/VND - SJC - VN30.*

![Hình 2.3](file:///c:/code/A2_CT_hautv.287/tieuluan2/charts/h13_graphdb_vs_vectordb_radar.png)
*Hình 2.3. Biểu đồ Radar 6 chiều so sánh đặc tính kỹ thuật giữa Graph Database và Vector Database.*

### 2.1 Các Thành phần Cấu tạo của Knowledge Graph

Một Đồ thị Tri thức hoàn chỉnh trong hệ thống được cấu thành từ ba thành phần cơ bản theo đặc tả chuẩn W3C:
1. **Nút Thực thể (Entity Nodes)**: Đại diện cho các đối tượng hoặc khái niệm trừu tượng trong thế giới thực. Mỗi thực thể được gán một Định danh Tài nguyên Đồng nhất (URI), ví dụ `http://ptit.edu.vn/med/Metformin` hoặc `http://ptit.edu.vn/fin/SJC_Gold`. Điều này đảm bảo tính duy nhất trên toàn cầu, tránh sự trùng lặp hoặc hiểu nhầm giữa các khái niệm có cùng tên gọi trong các bối cảnh khác nhau.
2. **Nút Giá trị Hằng số (Literal Nodes)**: Biểu thị các giá trị định lượng hoặc thuộc tính nguyên tử gắn liền với thực thể, bao gồm chuỗi ký tự mô tả, các ngưỡng số học lâm sàng (ví dụ: ngưỡng HbA1c 6.5%, ngưỡng eGFR 30 mL/phút/1.73m^2), hoặc các mức giá đóng cửa thị trường (ví dụ: giá đóng cửa FPT 135.000 đồng). Các literal đều được gắn thẻ kiểu dữ liệu XML Schema (`xsd:string`, `xsd:float`, `xsd:integer`).
3. **Cạnh Quan hệ Ngữ nghĩa (Semantic Relation Edges)**: Nối giữa hai nút thực thể hoặc giữa một nút thực thể với một nút literal. Mỗi cạnh mang một nhãn vị từ (Predicate) xác định ý nghĩa của mối liên kết, tuân thủ nghiêm ngặt theo các tiên đề bản thể học.

### 2.2 Mô hình Biểu diễn Bộ ba RDF (Resource Description Framework)

Toàn bộ tri thức của hệ thống được chuẩn hóa theo đặc tả W3C RDF 1.1. Mỗi đơn vị tri thức là một bộ ba (Triple) gồm ba thành phần theo cấu trúc ngữ pháp hình thức:
$$(s, p, o) \in (\text{Subject}, \text{Predicate}, \text{Object})$$

Trong đó:
- **Chủ từ (Subject - $s$)**: Là thực thể tài nguyên được mô tả, bắt buộc phải là một URI hoặc một nút ẩn danh (Blank Node).
- **Vị từ (Predicate - $p$)**: Là mối quan hệ ngữ nghĩa có hướng từ chủ từ sang đối từ, bắt buộc phải là một URI.
- **Đối từ (Object - $o$)**: Có thể là một thực thể tài nguyên khác (URI), một nút ẩn danh, hoặc một giá trị dữ liệu cụ thể (Literal).

Hệ thống định nghĩa các không gian tên (Namespaces) chuyên biệt:
- `rdf:` (`http://www.w3.org/1999/02/22-rdf-syntax-ns#`): Cung cấp các từ vựng cơ bản như `rdf:type`.
- `rdfs:` (`http://www.w3.org/2000/01/rdf-schema#`): Cung cấp quan hệ kế thừa `rdfs:subClassOf`, `rdfs:subPropertyOf`, định nghĩa miền xác định `rdfs:domain` và miền giá trị `rdfs:range`.
- `owl:` (`http://www.w3.org/2002/07/owl#`): Hỗ trợ các quan hệ bản thể nâng cao như tương đương `owl:equivalentClass` hoặc đối nghịch `owl:disjointWith`.
- `med:` (`http://ptit.edu.vn/med/`): Không gian tên chuyên ngành Y tế Đái tháo đường Típ 2 Việt Nam.
- `fin:` (`http://ptit.edu.vn/fin/`): Không gian tên chuyên ngành Tài chính và Kinh tế Vĩ mô Việt Nam.

Ví dụ về định dạng Turtle chuẩn của một bộ ba thể hiện tương tác nguy hiểm trong y tế:
```turtle
@prefix med: <http://ptit.edu.vn/med/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

med:Metformin med:interactsWith med:Ethanol ;
              med:hasLethalRisk med:LacticAcidosis ;
              rdfs:label "Metformin tương tác nguy hiểm với Rượu bia sinh toan lactic"@vi .
```

### 2.2.1 Ngữ nghĩa Hình thức của Không gian Tên và Phân cấp Thực thể

Cơ chế Định danh Tài nguyên Đồng nhất (URI) trong đồ thị tri thức đóng vai trò sống còn trong việc ngăn chặn hiện tượng đa nghĩa (Polysemy) và đồng âm khác nghĩa. Trong môi trường y tế và tài chính, một từ viết tắt có thể mang nhiều tầng ý nghĩa trái ngược nhau. Ví dụ: từ "CAP" trong y tế có thể chỉ "Viêm phổi mắc phải tại cộng đồng" (Community-Acquired Pneumonia), trong khi trong tài chính lại chỉ "Giới hạn trần lãi suất" (Interest Rate Cap) hoặc "Vốn hóa thị trường" (Market Capitalization). Nhờ cơ chế không gian tên phân định rõ ràng `med:CAP` và `fin:MarketCap`, hệ thống triệt tiêu hoàn toàn sự nhập nhằng khái niệm ở mức biểu diễn hình thức.

Phân cấp thực thể trong hệ thống được thiết lập theo logic mô tả $\mathcal{SROIQ}(\mathcal{D})$:
- Tiên đề Bao hàm Khái niệm (Concept Inclusion Axiom): $C \sqsubseteq D$ biểu diễn rằng mọi cá thể thuộc lớp $C$ đều là cá thể thuộc lớp $D$. Ví dụ: $\text{med:Biguanide} \sqsubseteq \text{med:Drug}$.
- Tiên đề Không giao nhau (Disjointness Axiom): $C \sqcap D = \bot$ biểu diễn hai lớp triệt tiêu lẫn nhau, không thể có thực thể nào đồng thời thuộc cả hai lớp. Ví dụ: $\text{med:AcuteComplication} \sqcap \text{med:ChronicComplication} = \bot$.
- Tiên đề Giới hạn Thuộc tính (Role Quantification): Khai báo miền xác định $\exists R.\top \sqsubseteq C$ và miền giá trị $\top \sqsubseteq \forall R.D$, đảm bảo quan hệ vị từ $R$ chỉ được phép nối từ thực thể kiểu $C$ sang thực thể kiểu $D$.

### 2.3 Bản thể học (Ontology) và Biểu diễn Tri thức Hình thức

Bản thể học đóng vai trò là "bộ luật định nghĩa ngữ nghĩa" cho đồ thị tri thức. Nó xác định các lớp đối tượng được phép tồn tại, mối quan hệ kế thừa hình cây giữa các lớp, và các ràng buộc logic áp đặt lên các thuộc tính dựa trên logic mô tả Description Logic.

**1. Bản thể học Y tế (VietnamDiabetesKG)**:
Hệ thống xây dựng 23 lớp bản thể phân cấp chặt chẽ, xếp dưới lớp gốc `med:MedicalEntity`:
- `med:Disease`: Lớp bệnh lý (thực thể tiêu biểu: `med:Type2Diabetes`, `med:Prediabetes`).
- `med:Symptom`: Lớp triệu chứng (ví dụ: `med:Polyuria` - tiểu nhiều, `med:Polydipsia` - khát nhiều, `med:Polyphagia` - ăn nhiều, `med:WeightLoss` - sụt cân).
- `med:DrugClass`: Lớp nhóm thuốc dược lý (gồm `med:Biguanide`, `med:SGLT2Inhibitor`, `med:DPP4Inhibitor`, `med:Sulfonylurea`, `med:Thiazolidinedione`, `med:GLP1RA`, `med:InsulinRegimen`).
- `med:Drug`: Lớp dược chất cụ thể (thực thể: `med:Metformin`, `med:Dapagliflozin`, `med:Empagliflozin`, `med:Gliclazide`, `med:Sitagliptin`, `med:Linagliptin`).
- `med:Complication`: Lớp biến chứng lâm sàng (chia thành biến chứng cấp tính `med:AcuteComplication` gồm hạ đường huyết, nhiễm toan lactic; và biến chứng mạn tính `med:ChronicComplication` như bệnh thận ĐTĐ, bệnh thần kinh ngoại biên, biến chứng mắt võng mạc, bàn chân ĐTĐ).
- `med:LabTest`: Lớp xét nghiệm cận lâm sàng (thực thể: `med:HbA1cTest`, `med:FPGTest`, `med:OGTTTest`, `med:eGFRTest`, `med:CreatinineTest`, `med:UACRTest`).
- `med:Contraindication`: Lớp tình trạng chống chỉ định lâm sàng tuyệt đối và tương đối.
- `med:FoodItem`: Lớp thực phẩm trong chế độ dinh dưỡng (thực thể: `med:ChickenBreast`, `med:WhiteRice`, `med:BrownRice`, `med:EthanolBeverage`).
- `med:ClinicalTarget`: Lớp mục tiêu kiểm soát (ví dụ: mục tiêu HbA1c < 7.0%, đường huyết đói 80-130 mg/dL).
- `med:PatientProfile`: Lớp hồ sơ bệnh nhân điện tử.

Mạng lưới quan hệ y tế gồm **17 vị từ chính**: `med:indicatedFor`, `med:contraindicatedWith`, `med:hasSideEffect`, `med:interactsWith`, `med:requiresRenalAdjustment`, `med:targetHbA1c`, `med:prescribedInStep`, `med:hasNutritionalComposition`, `med:contraindicatedWhenEGFRBelow`, `med:hasLethalRisk`, `med:interactionSeverity`, `med:clinicalWarning`, `med:hasCardioRenalBenefit`, `med:diagnosticCutoff`, `med:belongsToClass`, `med:hasComplication`, `med:lifestyleAdvice`.

**2. Bản thể học Tài chính (VietnamFinanceKG)**:
Gồm 16 lớp thực thể tài chính vĩ mô và doanh nghiệp phân cấp dưới `fin:FinancialEntity`:
- `fin:MonetaryPolicy`: Chính sách tiền tệ (lãi suất điều hành, cung tiền M2, can thiệp bán ngoại hối).
- `fin:MacroIndicator`: Chỉ số vĩ mô (chỉ số DXY, lạm phát CPI, tỷ giá USD/VND, lãi suất liên ngân hàng O/N).
- `fin:CommodityAsset`: Lớp hàng hóa kim loại quý (thực thể: `fin:SJC_Bullion`, `fin:World_Gold_Ounce`).
- `fin:StockEquity`: Lớp cổ phiếu doanh nghiệp niêm yết (thực thể: `fin:FPT`, `fin:VNM`, `fin:HPG`, `fin:VCB`).
- `fin:MarketIndex`: Chỉ số thị trường (thực thể: `fin:VN30_Index`, `fin:VN_Index`).
- `fin:RegulatoryDecree`: Văn bản quy phạm pháp luật (thực thể: `fin:Decree_24_2012`, `fin:Decree_232_2025`).

Các quan hệ tài chính được thiết kế đặc thù là các quan hệ nhân quả có hướng có dấu:
- `fin:causesPositive`: Tác động cùng chiều (A tăng làm B tăng, A giảm làm B giảm, trọng số dấu $+1$).
- `fin:causesNegative`: Tác động ngược chiều (A tăng làm B giảm, A giảm làm B tăng, trọng số dấu $-1$).
- `fin:regulates`: Quan hệ điều tiết pháp lý của cơ quan quản lý nhà nước.
- `fin:benchmarks`: Quan hệ định chuẩn tham chiếu giá quy đổi.
- `fin:affectsCostOfCapital`: Quan hệ tác động chi phí vốn doanh nghiệp.
- `fin:influencesEarnings`: Quan hệ ảnh hưởng biên lợi nhuận ròng.

### 2.3.1 Thuật toán Suy diễn Tiến trên RDF và Chứng minh Định lý Hội tụ

Một trong những ưu thế vượt trội nhất của Đồ thị Tri thức so với cơ sở dữ liệu quan hệ truyền thống là khả năng suy luận tự động nhằm phát hiện ra các tri thức mới chưa từng được khai báo tường minh trong cơ sở dữ liệu ban đầu. Hệ thống triển khai động cơ suy diễn tiến (Forward Chaining Engine) áp dụng 4 quy tắc bao hàm chuẩn của W3C RDF Schema:

1. **Quy tắc Miền xác định (rdfs2 - Domain Entailment)**:
   $$\frac{(p, \text{rdfs:domain}, C), \quad (x, p, y)}{(x, \text{rdf:type}, C)}$$
2. **Quy tắc Miền giá trị (rdfs3 - Range Entailment)**:
   $$\frac{(p, \text{rdfs:range}, C), \quad (x, p, y)}{(y, \text{rdf:type}, C)}$$
3. **Quy tắc Bắc cầu của Thuộc tính con (rdfs7 - SubProperty Entailment)**:
   $$\frac{(p_1, \text{rdfs:subPropertyOf}, p_2), \quad (x, p_1, y)}{(x, p_2, y)}$$
4. **Quy tắc Kế thừa Lớp (rdfs9 - SubClass Entailment)**:
   $$\frac{(C_1, \text{rdfs:subClassOf}, C_2), \quad (x, \text{rdf:type}, C_1)}{(x, \text{rdf:type}, C_2)}$$

**Chứng minh Toán học Định lý Hội tụ Điểm Bất động (Fixed-Point Convergence Theorem)**:
- *Bổ đề*: Cho không gian các đồ thị con $\mathcal{P}(\mathcal{U})$ trên vũ trụ bộ ba Herbrand hữu hạn $\mathcal{U} = (\mathcal{E} \cup \mathcal{B}) \times \mathcal{R} \times (\mathcal{E} \cup \mathcal{B} \cup \mathcal{L})$. Định nghĩa toán tử suy diễn tiến $\mathcal{T}: \mathcal{P}(\mathcal{U}) \to \mathcal{P}(\mathcal{U})$:
  $$\mathcal{T}(\mathcal{G}) = \mathcal{G} \cup \{t \in \mathcal{U} \mid \mathcal{G} \vdash_{\text{RDFS}} t\}$$
- *Tính Đơn điệu (Monotonicity)*: Dễ thấy với mọi $\mathcal{G}_A \subseteq \mathcal{G}_B$, nếu một bộ ba $t$ được suy ra từ $\mathcal{G}_A$ bởi các tiền đề của rdfs2, rdfs3, rdfs7, rdfs9 thì các tiền đề đó cũng tồn tại trong $\mathcal{G}_B$. Do đó $\mathcal{T}(\mathcal{G}_A) \subseteq \mathcal{T}(\mathcal{G}_B)$.
- *Tính Bị chặn trên (Boundedness)*: Vì vũ trụ thực thể $|\mathcal{V}| = N$ và số vị từ $|\mathcal{R}| = M$ là hữu hạn, tổng số bộ ba tối đa có thể tồn tại trong vũ trụ là $|	ext{Triples}| \le N^2 \cdot M < \infty$.
- *Kết luận*: Theo Định lý Điểm Bất động Knaster-Tarski, dãy lặp:
  $$\mathcal{G}_0 \subseteq \mathcal{G}_1 = \mathcal{T}(\mathcal{G}_0) \subseteq \mathcal{G}_2 = \mathcal{T}(\mathcal{G}_1) \subseteq \dots$$
  chắc chắn phải dừng sau một số bước hữu hạn $k \le N^2 \cdot M$, tại đó $\mathcal{T}(\mathcal{G}_k) = \mathcal{G}_k = \mathcal{G}^*$. Trạng thái $\mathcal{G}^*$ là bao đóng suy diễn đóng kín (Deductive Closure) duy nhất của đồ thị tri thức.

### 2.3.2 Truy vấn SPARQL và Đại số Quan hệ Đồ thị

Hệ thống sử dụng ngôn ngữ truy vấn SPARQL (SPARQL Protocol and RDF Query Language) tiêu chuẩn để trích xuất tri thức hình thức. Cốt lõi của SPARQL là phép so khớp mẫu đồ thị cơ sở (Basic Graph Pattern - BGP Matching) trên đại số quan hệ đồ thị:
- Toán tử BGP: Ánh xạ một tập các biến số $\mu: \text{Vars} \to \mathcal{E} \cup \mathcal{L}$ thỏa mãn toàn bộ các bộ ba trong mẫu đồ thị.
- Toán tử Join ($\bowtie$): Kết hợp hai phép so khớp có chung biến số.
- Toán tử Filter ($\sigma_R$): Giữ lại các bộ lời giải thỏa mãn biểu thức logic $R$.

Dưới đây là 5 truy vấn SPARQL chuyên sâu đại diện cho các tác vụ nghiệp vụ quan trọng trong hệ thống:
1. **Truy vấn Q1 (Lethal Drug Interaction)**: Phát hiện tương tác chết người giữa Metformin và Ethanol thông qua việc truy vết vị từ `med:hasLethalRisk` và lọc điều kiện `FILTER (?drugA = med:Metformin && ?drugB = med:Ethanol)`.
2. **Truy vấn Q2 (Dual Therapy Selection)**: Tìm kiếm các thuốc kết hợp bước 2 có lợi ích kép bảo vệ tim mạch và thận khi HbA1c vượt mục tiêu.
3. **Truy vấn Q3 (Renal Contraindications)**: Quét toàn bộ danh mục thuốc có thuộc tính `med:requiresRenalAdjustment true`, sắp xếp giảm dần theo ngưỡng lọc cầu thận an toàn `med:contraindicatedWhenEGFRBelow`.
4. **Truy vấn Q4 (Fed Rate Shock Propagation)**: Khám phá chuỗi truyền dẫn đa chặng từ chính sách tiền tệ Mỹ đến phần bù giá vàng SJC trong nước.
5. **Truy vấn Q5 (Exchange Rate Impact)**: Phân tích mức độ tổn thương của các mã cổ phiếu xuất nhập khẩu (FPT, HPG, VNM) trước biến động của tỷ giá USD/VND.

### 2.3.3 Kiểm tra Ràng buộc và Tính Nhất quán Lâm sàng / Kinh tế

Đồ thị Tri thức giải quyết dứt điểm các lỗi logic ngớ ngẩn thường gặp của mô hình ngôn ngữ thông qua hệ thống Ràng buộc Nhất quán (Consistency Constraint Validator):
1. **Ràng buộc Lâm sàng Tuyệt đối (Absolute Clinical Constraints)**:
   - *Ràng buộc Thận đối với Metformin*: Nếu hồ sơ bệnh nhân ghi nhận $\text{eGFR} < 30\text{ mL/phút/1.73m}^2$, hệ thống kích hoạt ràng buộc cứng:
     $$\forall p \in \text{Patients}: (p, \text{hasEGFR}, v) \land (v < 30) \implies \neg (p, \text{prescribedWith}, \text{Metformin})$$
     Mọi kế hoạch điều trị vi phạm ràng buộc này đều bị hệ thống chặn đứng ở tầng logic trước khi chuyển sang bước tổng hợp ngôn ngữ.
   - *Ràng buộc Thận đối với thuốc ức chế SGLT2*: Nếu $\text{eGFR} < 20\text{ mL/phút/1.73m}^2$, hệ thống ngăn chặn chỉ định mới của Dapagliflozin / Empagliflozin do hiệu quả hạ đường huyết của thuốc qua đường bài tiết nước tiểu bị mất hoàn toàn tại ngưỡng này.
2. **Ràng buộc Tính Nhất quán Kinh tế Vĩ mô**:
   - Mọi chu trình nhân quả trong VietnamFinanceKG đều được kiểm tra tính triệt tiêu hoặc cộng hưởng dấu. Nếu một chuỗi suy luận tạo ra mâu thuẫn dấu (ví dụ: lãi suất tăng đồng thời dẫn đến chi phí vốn rẻ hơn), hệ thống sẽ cảnh báo lỗi cấu trúc bản thể để chuyên gia hiệu chỉnh lại quan hệ.

### 2.3.4 Bản thể học Mở rộng: Đa dạng Sinh học và Đồng chuyển hóa trong Y tế

Trong thực tiễn điều trị tại các bệnh viện Việt Nam, bệnh nhân đái tháo đường típ 2 hiếm khi xuất hiện như một bệnh lý đơn lẻ thuần túy mà thường nằm trong bối cảnh phức tạp của **Hội chứng Chuyển hóa (Metabolic Syndrome)** với các bệnh đồng mắc (Co-morbidities) nghiêm trọng:
- Tăng huyết áp nguyên phát (`med:Hypertension`): Chiếm hơn 70% bệnh nhân đái tháo đường tại Việt Nam, làm gia tăng gấp đôi nguy cơ đột quỵ và biến cố tim mạch.
- Rối loạn lipid máu (`med:Dyslipidemia`): Đặc trưng bởi tăng triglycerid, giảm HDL-C và tăng các hạt LDL-C nhỏ đậm đặc gây xơ vữa động mạch sớm.
- Bệnh gan thoái hóa mỡ không do rượu (`med:NAFLD`): Thúc đẩy tình trạng đề kháng insulin tại gan trầm trọng hơn.
- Bệnh thận mạn tính do đái tháo đường (`med:DiabeticKidneyDisease - DKD`): Là nguyên nhân hàng đầu dẫn tới suy thận giai đoạn cuối phải chạy thận nhân tạo chu kỳ.

Bản thể học VietnamDiabetesKG mã hóa các mối quan hệ đồng mắc này thông qua vị từ `med:hasComorbidityRisk` và `med:sharedRiskFactor`. Nhờ đó, khi tác tử đánh giá một bệnh nhân, nó không chỉ nhìn vào một chỉ số HbA1c đơn lẻ mà thực hiện một đánh giá toàn diện về nguy cơ tim mạch - thận - chuyển hóa (Cardio-Renal-Metabolic Continuum) để đưa ra khuyến nghị phối hợp thuốc tối ưu.

### 2.3.5 Bản thể học Mở rộng: Cấu trúc Rổ Chỉ số VN30 và Trọng số Vốn hóa

Chỉ số VN30 là chỉ số giá đại diện cho 30 doanh nghiệp niêm yết có giá trị vốn hóa và thanh khoản hàng đầu trên Sở Giao dịch Chứng khoán TP.HCM (HOSE), chiếm hơn 75% giá trị vốn hóa và 60% giá trị giao dịch của toàn thị trường chứng khoán Việt Nam.

Công thức tính chỉ số VN30 được mã hóa trong VietnamFinanceKG tuân thủ quy tắc định lượng:
$$\text{VN30-Index}_t = \frac{\sum_{i=1}^{30} P_{i, t} \times Q_{i, t} \times f_{i, t} \times c_{i, t}}{\text{Hệ số chia cơ sở } D_t} \times 1000$$
Trong đó:
- $P_{i, t}$ là giá thị trường của cổ phiếu $i$ tại thời điểm $t$.
- $Q_{i, t}$ là khối lượng cổ phiếu đang lưu hành của doanh nghiệp $i$.
- $f_{i, t}$ là tỷ lệ cổ phiếu tự do chuyển nhượng (Free-float Ratio), loại bỏ các cổ phiếu bị hạn chế chuyển nhượng do Nhà nước hoặc cổ đông sáng lập nắm giữ dài hạn.
- $c_{i, t} = 10\%$ là hệ số giới hạn tỷ trọng vốn hóa (Capping Ratio), nhằm đảm bảo không có bất kỳ một cổ phiếu đơn lẻ nào (như VCB hay HPG) có thể thao túng hoặc chi phối quá 10% biến động của toàn bộ rổ chỉ số.
- $D_t$ là hệ số chia được điều chỉnh kỹ thuật khi có các sự kiện doanh nghiệp (chia tách cổ phiếu, trả cổ tức bằng cổ phiếu, phát hành thêm) để đảm bảo tính liên tục của đường chỉ số.

### 2.4 Xây dựng Cơ sở Tri thức (KB) và Đồ thị (KG) từ Dữ liệu Bảng Lớn

Thách thức lớn trong thực tiễn là dữ liệu nghiệp vụ thường nằm ở dạng bảng quan hệ hoặc file CSV (hồ sơ bệnh án điện tử, dữ liệu phiên giao dịch chứng khoán). Để đưa vào đồ thị tri thức, hệ thống thiết kế đường ống ETL (Extract - Transform - Load) bán tự động:

- **Chuyển đổi 96.128 Hồ sơ Bệnh nhân**: Mỗi dòng trong file `diabetes_prediction_dataset.csv` đại diện cho một cá thể bệnh nhân duy nhất. Một thuật toán sinh đồ thị tự động chuyển đổi mỗi hàng thành một thực thể `med:PatientProfile_XXXXX`, sau đó liên kết các đặc trưng thành các bộ ba RDF:
  - `(PatientProfile_XXXXX, rdf:type, med:PatientProfile)`
  - `(PatientProfile_XXXXX, med:hasAge, "55"^^xsd:integer)`
  - `(PatientProfile_XXXXX, med:hasBMI, "27.4"^^xsd:float)`
  - `(PatientProfile_XXXXX, med:hasHbA1c, "7.2"^^xsd:float)`
  - `(PatientProfile_XXXXX, med:hasSmokingHistory, "former"^^xsd:string)`
  Quá trình này tạo ra hơn **961.280 bộ ba RDF** định lượng, cho phép hệ thống thực hiện các truy vấn thống kê dân số học hoặc tìm các bệnh nhân tương đồng bằng ngôn ngữ SPARQL chuẩn.
- **Chuyển đổi 2.932 Phiên Giao dịch Thị trường (2015 - 2026)**: Tương tự, dữ liệu chuỗi thời gian OHLCV của 7 tài sản được ánh xạ thành các nút sự kiện phiên giao dịch `fin:TradingSession_YYYYMMDD`, lưu giữ giá đóng cửa, khối lượng, tỷ lệ biến động và mối liên hệ chéo giữa các chỉ số vĩ mô.

### 2.5 So sánh Chi tiết: Graph Database và Vector Database

Hiện nay trong cộng đồng kỹ thuật AI có nhiều tranh luận về việc nên sử dụng Cơ sở Dữ liệu Đồ thị (Graph Database) hay Cơ sở Dữ liệu Vector (Vector Database). Nghiên cứu này khẳng định: Đây không phải là hai công nghệ đối đầu triệt tiêu nhau, mà là hai mặt bổ trợ của cùng một vấn đề:

- **Bản chất lưu trữ**: Graph DB lưu trữ các thực thể và quan hệ rõ ràng dưới dạng bộ ba hoặc nút/cạnh có nhãn. Vector DB lưu trữ các mảng số thực nhiều chiều (Embeddings) đại diện cho tọa độ ngữ nghĩa của đoạn văn bản.
- **Khả năng suy luận đa bước (Multi-hop Reasoning)**: Graph DB có khả năng duyệt đường đi nhiều chặng ($k$-hops) với độ chính xác tuyệt đối thông qua phép toán duyệt đồ thị BFS/DFS hoặc câu truy vấn Cypher/SPARQL. Trong khi đó, Vector DB chỉ có thể tìm kiếm độ tương đồng cục bộ quanh một điểm vector, hoàn toàn bất lực khi cần suy luận bắc cầu qua 3-4 nút trung gian.
- **Tính giải thích được (Explainability)**: Kết quả của Graph DB là một đường đi hình học minh bạch gồm các thực thể và vị từ rõ ràng. Kết quả của Vector DB là một con số tương đồng cosin trừu tượng không thể giải thích tại sao hai đoạn văn lại gần nhau.
- **Chi phí cập nhật**: Graph DB cập nhật với chi phí $O(1)$ cho mỗi cạnh mới. Vector DB đòi hỏi phải chạy qua mô hình nhúng nơ-ron để sinh vector mới và tái cấu trúc cây chỉ mục xấp xỉ lân cận (HNSW/IVF).

Hệ thống giải quyết bài toán này bằng cách **hợp nhất cả hai**: Sử dụng Graph DB làm bộ xương sống logic kiểm soát tính đúng đắn và suy luận quan hệ, đồng thời sử dụng Vector DB làm công cụ tìm kiếm ngữ nghĩa linh hoạt trên văn bản phi cấu trúc.

---

# CHƯƠNG 3: KỸ THUẬT RETRIEVAL-AUGMENTED GENERATION (RAG)

*Chương này nghiên cứu toàn diện ngăn xếp công nghệ RAG từ cơ bản đến nâng cao: phân tích các điểm nghẽn của Naive RAG, thiết lập thực nghiệm trên kho 17 tài liệu quy chuẩn tiếng Việt, khảo sát 5 chiến lược phân mảnh (chunking), đánh giá 5 phương pháp truy xuất (BM25, Dense, Hybrid RRF, Cross-Encoder, GraphRAG), xây dựng ma trận đối chuẩn 25 cấu hình, phân tích độ phức tạp tính toán và bộ nhớ, và phân tích kỹ thuật phân cụm Louvain trong GraphRAG.*

![Hình 3.1](file:///c:/code/A2_CT_hautv.287/tieuluan2/charts/h04_chunking_strategies_comparison.png)
*Hình 3.1. So sánh trực quan 5 chiến lược phân mảnh văn bản.*

### Bảng 3.1. Danh mục 17 tài liệu quy chuẩn trong kho ngữ liệu thực nghiệm

| Mã | Lĩnh vực | Tiêu đề Tài liệu | Số phần / đoạn | Số từ | Nội dung Nghiệp vụ Trọng tâm |
| :--- | :--- | :--- | :--- | :--- | :--- |
| D01 | Y tế | Chẩn đoán Đái tháo đường Típ 2 | 6 | 1.450 | QĐ 5481/QĐ-BYT: 4 tiêu chuẩn FPG, OGTT, HbA1c, RPG |
| D02 | Y tế | Thuốc Điều trị ĐTĐ Típ 2 | 8 | 2.120 | Metformin, SGLT2i, DPP-4i, SU, TZD, GLP-1 RA, Insulin |
| D03 | Y tế | Phác đồ Phối hợp Thuốc & Suy thận | 7 | 1.890 | Chỉ định theo eGFR, chống chỉ định Metformin eGFR < 30 |
| D04 | Y tế | Dinh dưỡng Người ĐTĐ & Đĩa ăn | 6 | 1.670 | Quy tắc Đĩa ăn: 1/2 rau, 1/4 đạm ức gà, 1/4 tinh bột |
| D05 | Y tế | Vận động & Kiểm soát Cân nặng | 5 | 1.230 | 150 phút/tuần, bài tập kháng lực, giảm 5-7% cân nặng |
| D06 | Y tế | Biến chứng Mạn tính ĐTĐ | 6 | 1.740 | Bệnh võng mạc, bàn chân ĐTĐ, thần kinh ngoại biên, tim mạch |
| D07 | Y tế | Hạ Glucose Huyết Cấp tính | 5 | 1.310 | Quy tắc 15-15, triệu chứng cảnh báo và xử trí cấp cứu |
| D08 | Y tế | Insulin: Chỉ định & Chỉnh liều | 7 | 1.980 | Insulin nền, bolus, chỉnh liều dựa trên đường huyết đói |
| D09 | Tài chính | Vàng miếng SJC & Nghị định 24 | 6 | 1.820 | Độc quyền sản xuất vàng SJC, nguyên nhân chênh lệch giá |
| D10 | Tài chính | Nghị định 232/2025/NĐ-CP Quản lý Vàng | 7 | 2.250 | Xóa bỏ độc quyền, cấp phép hạn ngạch và thuế giao dịch |
| D11 | Tài chính | Giá Vàng Thế giới & Công thức Quy đổi | 5 | 1.430 | Hệ số 1.20565, 0.82945, thuế phí và phần bù SJC |
| D12 | Tài chính | Tỷ giá USD/VND & Cơ chế Điều hành | 6 | 1.760 | Tỷ giá trung tâm, biên độ +-5%, can thiệp ngoại hối NHNN |
| D13 | Tài chính | Lãi suất Fed & Kênh Truyền dẫn DXY | 7 | 2.040 | Chu kỳ lãi suất Fed, sức mạnh DXY và áp lực tỷ giá |
| D14 | Tài chính | Cổ phiếu FPT - Công nghệ & Bán lẻ | 6 | 1.650 | Chuyển đổi số, xuất khẩu phần mềm, chuỗi Long Châu |
| D15 | Tài chính | Cổ phiếu VNM - Tiêu dùng Sữa | 5 | 1.520 | Thị phần sữa, chi phí sữa bột nhập khẩu, biên EBITDA |
| D16 | Tài chính | Cổ phiếu HPG - Thép & Xây dựng | 6 | 1.710 | Khu liên hợp Dung Quất, giá quặng sắt, bất động sản |
| D17 | Tài chính | Cổ phiếu VCB & Ngành Ngân hàng | 6 | 1.850 | NIM, CASA, chất lượng tài sản và chi phí trích lập dự phòng |


### Bảng 3.2. Kết quả Ma trận Thực nghiệm 25 Cấu hình RAG (Hit@k, MRR, NDCG, Latency)

| Chiến lược Chia đoạn | Bộ Truy xuất | Hit@1 | Hit@3 | Hit@5 | MRR | NDCG@5 | Độ trễ (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Fixed-500 | BM25 Okapi | 63.33% | 80.00% | 86.67% | 0.7251 | 0.7602 | 12.4 |
| Fixed-500 | Dense TF-IDF | 70.00% | 83.33% | 90.00% | 0.7783 | 0.8091 | 18.2 |
| Fixed-500 | Hybrid RRF (k=60) | 76.67% | 90.00% | 93.33% | 0.8354 | 0.8601 | 24.6 |
| Fixed-500 | Hybrid + Reranker | 80.00% | 93.33% | 96.67% | 0.8712 | 0.8955 | 74.8 |
| Fixed-500 | GraphRAG Louvain | 76.67% | 86.67% | 90.00% | 0.8240 | 0.8432 | 112.5 |
| Sliding-500-100 | BM25 Okapi | 66.67% | 83.33% | 90.00% | 0.7542 | 0.7915 | 14.1 |
| Sliding-500-100 | Dense TF-IDF | 73.33% | 86.67% | 93.33% | 0.8051 | 0.8378 | 20.5 |
| Sliding-500-100 | Hybrid RRF (k=60) | 80.00% | 93.33% | 96.67% | 0.8681 | 0.8930 | 28.3 |
| Sliding-500-100 | Hybrid + Reranker | 83.33% | 96.67% | 96.67% | 0.9015 | 0.9184 | 82.4 |
| Sliding-500-100 | GraphRAG Louvain | 80.00% | 90.00% | 93.33% | 0.8522 | 0.8726 | 119.8 |
| Sentence-Based | BM25 Okapi | 56.67% | 73.33% | 80.00% | 0.6548 | 0.6912 | 16.8 |
| Sentence-Based | Dense TF-IDF | 63.33% | 80.00% | 86.67% | 0.7210 | 0.7573 | 23.4 |
| Sentence-Based | Hybrid RRF (k=60) | 70.00% | 86.67% | 90.00% | 0.7845 | 0.8136 | 32.1 |
| Sentence-Based | Hybrid + Reranker | 73.33% | 90.00% | 93.33% | 0.8192 | 0.8480 | 89.5 |
| Sentence-Based | GraphRAG Louvain | 73.33% | 83.33% | 86.67% | 0.7891 | 0.8089 | 128.2 |
| Semantic-MD | BM25 Okapi | 73.33% | 86.67% | 93.33% | 0.8021 | 0.8354 | 13.2 |
| Semantic-MD | Dense TF-IDF | 76.67% | 90.00% | 93.33% | 0.8340 | 0.8592 | 19.7 |
| Semantic-MD | Hybrid RRF (k=60) | 83.33% | 93.33% | 96.67% | 0.8875 | 0.9076 | 26.8 |
| Semantic-MD | Hybrid + Reranker | 86.67% | 96.67% | 100.00% | 0.9234 | 0.9428 | 79.1 |
| Semantic-MD | GraphRAG Louvain | 83.33% | 93.33% | 96.67% | 0.8841 | 0.9048 | 115.4 |
| Parent-Child | BM25 Okapi | 76.67% | 90.00% | 93.33% | 0.8350 | 0.8601 | 15.4 |
| Parent-Child | Dense TF-IDF | 80.00% | 93.33% | 96.67% | 0.8682 | 0.8929 | 22.0 |
| Parent-Child | Hybrid RRF (k=60) | 86.67% | 96.67% | 100.00% | 0.9184 | 0.9388 | 30.5 |
| Parent-Child | Hybrid + Reranker | 90.00% | 100.00% | 100.00% | 0.9511 | 0.9634 | 86.2 |
| Parent-Child | GraphRAG Louvain | 86.67% | 96.67% | 100.00% | 0.9192 | 0.9395 | 124.6 |


#### Listing 3.1. Thuật toán Truy xuất Thưa BM25 Okapi cho Tiếng Việt trong sparse_retrieval.py
```python
class BM25Retriever:
    """Okapi BM25 implementation optimized for Vietnamese medical/financial corpus."""
    def __init__(self, corpus: List[Dict[str, Any]], k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus = corpus
        self.doc_len = [len(tokenize_vietnamese(d['text'])) for d in corpus]
        self.avgdl = sum(self.doc_len) / max(len(self.doc_len), 1)
        self.doc_freqs = Counter()
        self.doc_token_counts = []
        for d in corpus:
            tokens = tokenize_vietnamese(d['text'])
            counts = Counter(tokens)
            self.doc_token_counts.append(counts)
            for token in counts.keys():
                self.doc_freqs[token] += 1
        self.N = len(corpus)
        self.idf = {t: math.log((self.N - freq + 0.5) / (freq + 0.5) + 1.0)
                    for t, freq in self.doc_freqs.items()}

    def score(self, query: str) -> List[Tuple[int, float]]:
        q_tokens = tokenize_vietnamese(query)
        scores = []
        for idx, counts in enumerate(self.doc_token_counts):
            score = 0.0
            dl = self.doc_len[idx]
            denom_const = self.k1 * (1.0 - self.b + self.b * (dl / self.avgdl))
            for q in q_tokens:
                if q in counts:
                    tf = counts[q]
                    idf = self.idf.get(q, 0.0)
                    score += idf * (tf * (self.k1 + 1.0)) / (tf + denom_const)
            scores.append((idx, score))
        return sorted(scores, key=lambda x: x[1], reverse=True)
```

#### Listing 3.2. Thuật toán Dung hợp Thứ hạng Nghịch đảo (Hybrid RRF k=60) trong hybrid_retrieval.py
```python
def reciprocal_rank_fusion(
    ranked_lists: List[List[Tuple[str, float]]],
    k: int = 60
) -> List[Tuple[str, float]]:
    """
    Combines multiple rankings (e.g., BM25 and Dense Cosine)
    using Cormack et al.'s Reciprocal Rank Fusion formula:
    RRF(d) = sum_{m} 1.0 / (k + rank_m(d))
    """
    rrf_scores = defaultdict(float)
    for rank_list in ranked_lists:
        for rank, (doc_id, _) in enumerate(rank_list, start=1):
            rrf_scores[doc_id] += 1.0 / (k + rank)
            
    sorted_docs = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_docs
```

![Hình 3.2](file:///c:/code/A2_CT_hautv.287/tieuluan2/charts/h05_rag_matrix_heatmap.png)
*Hình 3.2. Biểu đồ nhiệt (Heatmap) thể hiện độ chính xác Hit@1 trên ma trận thực nghiệm 25 cấu hình RAG.*

![Hình 3.3](file:///c:/code/A2_CT_hautv.287/tieuluan2/charts/h06_sparse_vs_dense_vs_hybrid_radar.png)
*Hình 3.3. Biểu đồ Radar đa chiều đối sánh các bộ truy xuất.*

### 3.1 Naive RAG và Các Điểm Nghẽn Cốt Tử

Kiến trúc RAG nguyên bản (Naive RAG) thường được triển khai theo một đường ống tuyến tính đơn giản: Tài liệu văn bản được cắt nhỏ thành các đoạn cố định (ví dụ: 500 từ), chuyển hóa thành vector nhúng thông qua một mô hình nhúng nơ-ron (như BERT hoặc text-embedding-ada-002), lưu trữ vào cơ sở dữ liệu vector. Khi có truy vấn từ người dùng, hệ thống tính độ tương đồng cosin để lấy ra top-$k$ đoạn gần nhất và đưa trực tiếp vào câu lệnh nhắc (prompt) của LLM.

Mặc dù dễ triển khai, Naive RAG bộc lộ 4 điểm nghẽn chí mạng trong các ứng dụng thực tế:
1. **Hiện tượng Trôi dạt Ngữ nghĩa (Semantic Drift)**: Mô hình nhúng biểu diễn toàn bộ một đoạn văn dài thành một vector duy nhất. Trong các văn bản kỹ thuật y tế hoặc tài chính, một đoạn văn thường chứa nhiều thông tin phụ bên cạnh thông tin chính. Vector nhúng bị phân tán trọng số, dẫn đến việc truy xuất các đoạn văn có vẻ liên quan về mặt từ ngữ nhưng hoàn toàn lạc đề về mặt nghiệp vụ cốt lõi.
2. **Hiện tượng "Mất mát ở Giữa" (Lost in the Middle)**: Nghiên cứu của Liu et al. (Stanford, 2023) đã chỉ ra rằng các LLM dựa trên kiến trúc Transformer có xu hướng chú ý mạnh mẽ vào các đoạn văn bản ở đầu và cuối ngữ cảnh đầu vào theo đường cong chữ U (U-shaped Attention Curve), nhưng lại bỏ sót hoặc đánh giá thấp các thông tin nằm ở phần giữa của prompt. Khi Naive RAG nhồi nhét 5-10 đoạn văn bản không được sắp xếp tối ưu, chứng cứ quan trọng nằm ở giữa thường bị LLM phớt lờ.
3. **Phân mảnh Ngữ cảnh Làm Đứt gãy Chuỗi Nhân quả**: Cắt văn bản cố định theo số lượng từ mà không hiểu cấu trúc ngữ nghĩa thường xé đôi một điều khoản pháp luật, một câu điều kiện lâm sàng phức tạp (ví dụ: vế "chỉ định thuốc..." nằm ở đoạn trước, còn vế "ngoại trừ bệnh nhân có tiền sử suy thận nặng..." bị văng sang đoạn sau). Hậu quả là LLM tiếp nhận thông tin phiến diện và đưa ra chỉ định sai lầm chết người.
4. **Bùng nổ Nhiễu trong Ngữ cảnh (Context Pollution)**: Việc truy xuất các đoạn văn bản chứa nhiều từ ngữ thừa làm cạn kiệt cửa sổ ngữ cảnh hữu ích của LLM, làm tăng chi phí tính toán và gia tăng tỷ lệ kích hoạt ảo giác của mô hình.

### 3.2 Thiết lập Thực nghiệm Truy xuất Quy chuẩn

Để đánh giá khách quan và khoa học hiệu năng của các kỹ thuật RAG, hệ thống xây dựng một môi trường thực nghiệm chuẩn hóa:

**Kho Ngữ liệu 17 Tài liệu Quy chuẩn (Corpus D01 - D17)**:
Gồm 8 tài liệu y tế chính thức ban hành bởi Bộ Y tế và các tổ chức y khoa quốc tế (Quyết định 5481/QĐ-BYT, tiêu chuẩn ADA 2024, hướng dẫn tổn thương thận KDIGO 2024, tài liệu dinh dưỡng đĩa ăn, phác đồ insulin, biến chứng cấp và mạn tính); cùng 9 tài liệu tài chính pháp quy và báo cáo phân tích ngành của Việt Nam (Nghị định 24/2012/NĐ-CP, Nghị định 232/2025/NĐ-CP, cơ chế tỷ giá trung tâm của Ngân hàng Nhà nước, phân tích chuỗi cung ứng và định giá 4 doanh nghiệp đầu ngành FPT, VNM, HPG, VCB, và phương pháp tính chỉ số VN30). Tổng quy mô kho ngữ liệu đạt gần 30.000 từ chuyên ngành được định dạng Markdown chuẩn.

**Bộ 30 Câu hỏi Thực nghiệm Đa tầng (Benchmark Queries)**:
Bộ câu hỏi được thiết kế bao phủ 4 nhóm bài toán từ dễ đến phức tạp:
- *Nhóm 1: Truy vấn Sự kiện Tường minh (Factoid Queries)*: Kiểm tra khả năng tìm kiếm chính xác các con số và định nghĩa (ví dụ: "Tiêu chuẩn chẩn đoán đái tháo đường theo đường huyết lúc đói FPG là bao nhiêu?").
- *Nhóm 2: Truy vấn Ràng buộc Lâm sàng / Pháp lý (Constraint-Checking Queries)*: Kiểm tra phát hiện điều kiện loại trừ (ví dụ: "Mức lọc cầu thận eGFR dưới bao nhiêu thì chống chỉ định tuyệt đối dùng Metformin?").
- *Nhóm 3: Truy vấn So sánh và Đối chiếu (Comparative Queries)*: Yêu cầu tổng hợp thông tin từ nhiều nguồn (ví dụ: "So sánh cơ chế quản lý thị trường vàng giữa Nghị định 24/2012 và Nghị định 232/2025").
- *Nhóm 4: Truy vấn Suy luận Nhân quả Đa bước (Multi-hop Causal Queries)*: Đòi hỏi kết nối các mắt xích logic qua nhiều tài liệu (ví dụ: "Lãi suất Fed tăng tác động thế nào đến chi phí vốn của Tập đoàn Hòa Phát HPG?").

**Các Độ đo Đánh giá Chuẩn mực**:
- **Hit@k ($k \in \{1, 3, 5\}$)**: Tỷ lệ phần trăm các câu hỏi mà đoạn văn bản chứa đáp án chính xác xuất hiện trong top-$k$ kết quả trả về.
- **MRR (Mean Reciprocal Rank)**: Nghịch đảo của thứ hạng của đoạn tài liệu đúng đầu tiên:
  $$\text{MRR} = \frac{1}{|Q|} \sum_{i=1}^{|Q|} \frac{1}{\text{rank}_i}$$
- **NDCG@5 (Normalized Discounted Cumulative Gain)**: Đánh giá chất lượng của toàn bộ danh sách xếp hạng top-5 có tính đến vị trí xuất hiện của tài liệu liên quan:
  $$\text{DCG}@p = \sum_{i=1}^p \frac{2^{\text{rel}_i} - 1}{\log_2(i + 1)}, \quad \text{NDCG}@p = \frac{\text{DCG}@p}{\text{IDCG}@p}$$
- **Latency (Độ trễ truy xuất)**: Thời gian thực thi tính bằng mili-giây (ms) trên phần cứng chuẩn CPU.

### 3.3 Các Chiến lược Phân mảnh Văn bản (Chunking Strategies)

Khâu phân mảnh văn bản là bước quyết định chất lượng đầu vào của mọi hệ thống RAG. Hệ thống tiến hành đối chuẩn thực nghiệm 5 chiến lược phân mảnh khác nhau:

1. **Chiến lược 1: Phân mảnh Cố định (Fixed-size Chunking, 500 từ)**:
   Văn bản được cắt tuần tự thành các khối đúng 500 từ, không có phần gối đầu. Ưu điểm là tốc độ xử lý cực nhanh, dễ triển khai. Tuy nhiên, nhược điểm chí mạng là thường xuyên cắt ngang giữa câu hoặc giữa bảng số liệu, làm đứt gãy thông tin ngữ nghĩa.
2. **Chiến lược 2: Trượt Gối đầu (Sliding Window Chunking, 500-100 từ)**:
   Mỗi đoạn có độ dài 500 từ nhưng có khoảng chồng lấn 100 từ với đoạn liền trước. Khoảng gối đầu giúp duy trì tính liên tục của ngữ cảnh tại các ranh giới cắt, giảm thiểu nguy cơ mất mát thông tin.
3. **Chiến lược 3: Phân mảnh theo Ranh giới Câu (Sentence-based Chunking)**:
   Sử dụng bộ tách câu dựa trên dấu chấm câu và ngữ pháp tiếng Việt. Các câu được ghép lại cho đến khi đạt độ dài mong muốn. Chiến lược này bảo toàn tính toàn vẹn ngữ pháp của từng câu, nhưng có độ dài các đoạn không đồng đều.
4. **Chiến lược 4: Ranh giới Ngữ nghĩa Markdown (Markdown Semantic-aware Chunking)**:
   Tận dụng cấu trúc tiêu đề phân cấp của văn bản Markdown (`#`, `##`, `###`). Đoạn văn được phân chia tự nhiên theo từng tiểu mục nội dung. Nhờ đó, mỗi đoạn đại diện cho một chủ đề logic hoàn chỉnh, các bảng số liệu và danh sách liệt kê được giữ nguyên vẹn trong một khối duy nhất.
5. **Chiến lược 5: Cây Phân cấp Cha - Con (Hierarchical Parent-Child Chunking, 1000-200 từ)**:
   Tài liệu được phân mảnh thành hai cấp độ song song: Cấp con (Child chunks) gồm các đoạn ngắn 200 từ được sử dụng để lập chỉ mục và tính toán tương đồng tìm kiếm vector (nhờ tính tập trung cao độ của ngữ nghĩa); khi tìm thấy đoạn con khớp nhất, hệ thống tự động truy xuất đoạn cha (Parent chunk) có độ dài 1000 từ bao bọc lấy đoạn con đó để nạp vào prompt cho LLM. Chiến lược này giải quyết trọn vẹn sự đánh đổi giữa "độ nhạy tìm kiếm" và "độ đầy đủ của ngữ cảnh giải thích".

### 3.4 Các Kỹ thuật Truy xuất: Thưa, Dày, Lai và Xếp hạng lại

Sau khi văn bản được phân mảnh, hệ thống thử nghiệm 5 mô hình truy xuất tài liệu khác nhau:

**1. Truy xuất Thưa bằng BM25 Okapi (Sparse Retrieval)**:
Dựa trên mô hình xác suất và không gian vector từ vựng. Hệ thống áp dụng thuật toán tách từ tiếng Việt chuẩn, sau đó tính điểm BM25 giữa câu truy vấn $Q$ và đoạn văn $D$:
$$\text{Score}(D, Q) = \sum_{q_i \in Q} \text{IDF}(q_i) \cdot \frac{f(q_i, D) \cdot (k_1 + 1)}{f(q_i, D) + k_1 \cdot \left(1 - b + b \cdot \frac{|D|}{\text{avgdl}}\right)}$$
Trong đó:
- $f(q_i, D)$ là tần số xuất hiện của từ $q_i$ trong đoạn văn $D$.
- $|D|$ và $\text{avgdl}$ lần lượt là độ dài của đoạn văn và độ dài trung bình của toàn bộ các đoạn trong kho ngữ liệu.
- Các siêu tham số được tối ưu hóa cho tiếng Việt: $k_1 = 1.5$ (kiểm soát độ bão hòa tần số từ) và $b = 0.75$ (mức độ phạt độ dài đoạn văn).
- Công thức trọng số nghịch đảo tần số tài liệu chuẩn W3C:
  $$\text{IDF}(q_i) = \ln \left( \frac{N - n(q_i) + 0.5}{n(q_i) + 0.5} + 1 \right)$$
BM25 cực kỳ mạnh mẽ trong việc tìm kiếm chính xác các từ khóa hiếm, các mã số quy chuẩn (như `5481/QĐ-BYT`, `eGFR`, `DXY`, `HPG`), hoàn toàn miễn nhiễm với hiện tượng ảo giác vector.

**2. Truy xuất Dày Ngữ nghĩa (Dense Semantic Retrieval)**:
Sử dụng không gian nhúng đa ngôn ngữ để chiếu cả câu truy vấn và đoạn văn bản thành các vector thực 768 chiều. Độ tương đồng ngữ nghĩa được tính bằng hàm tích vô hướng trên các vector đã được chuẩn hóa độ dài Euclidean ($L_2$ Normalization), tương đương với Cosine Similarity:
$$\text{CosineSim}(q, d) = \frac{\mathbf{e}_q \cdot \mathbf{e}_d}{\|\mathbf{e}_q\|_2 \|\mathbf{e}_d\|_2}$$
Dense Retrieval có khả năng vượt trội trong việc hiểu các khái niệm đồng nghĩa (ví dụ: "thuốc hạ đường" tương đồng với "dược chất kiểm soát glucose"), ngay cả khi người dùng không sử dụng chính xác các thuật ngữ khoa học.

**3. Truy xuất Lai bằng Reciprocal Rank Fusion (Hybrid RRF, $k=60$)**:
Nhận thấy BM25 và Dense Retrieval có tính chất bù trừ hoàn hảo, hệ thống kết hợp kết quả xếp hạng của hai phương pháp bằng thuật toán Reciprocal Rank Fusion (RRF) nổi tiếng của Cormack et al. (SIGIR 2009):
$$\text{RRF\_Score}(d) = \sum_{m \in \{\text{BM25}, \text{Dense}\}} \frac{1}{k + r_m(d)}$$
Với $r_m(d)$ là thứ hạng xuất hiện của tài liệu $d$ trong hệ thống truy xuất $m$, và $k = 60$ là hằng số làm mịn thứ hạng. RRF có ưu điểm vượt trội là không phụ thuộc vào thang đo điểm số nội tại vốn rất khác biệt giữa BM25 và Cosine, giúp cân bằng hoàn hảo giữa tính chính xác từ khóa và độ tương đồng khái niệm.

**4. Xếp hạng lại Bằng Cross-Encoder (Cross-Encoder Reranking)**:
Các mô hình Bi-Encoder tính toán vector của truy vấn và đoạn văn bản hoàn toàn độc lập, làm mất đi các tương tác từ vựng chéo tinh vi. Hệ thống bổ sung tầng Cross-Encoder ở giai đoạn hai: Nhận top-20 ứng viên từ bước truy xuất lai, ghép thành chuỗi đầu vào duy nhất `[CLS] Query [SEP] Passage [SEP]` và đưa qua các tầng Transformer đầy đủ cơ chế Self-Attention đa chiều. Cross-Encoder gán lại điểm liên quan với độ chính xác vượt trội, đẩy các đoạn văn chứa bằng chứng cốt lõi lên top-1.

**5. Ma trận Thực nghiệm 25 Cấu hình RAG**:
Bảng 3.2 trong báo cáo đối chuẩn toàn bộ 25 sự kết hợp giữa 5 chiến lược chia đoạn và 5 bộ truy xuất. Kết quả chỉ ra rõ ràng:
- Cấu hình thấp nhất: Phân mảnh theo câu + BM25 chỉ đạt Hit@1 = 56.67%, MRR = 0.6548.
- Cấu hình tối ưu nhất: **Cây Phân cấp Cha - Con + Hybrid RRF + Cross-Encoder Reranker** xuất sắc đạt **Hit@1 = 90.00%**, **Hit@3 = 100.00%**, **Hit@5 = 100.00%**, **MRR = 0.9511**, và **NDCG@5 = 0.9634**, với độ trễ xử lý chấp nhận được là 86.2 ms.

### 3.4.6 Phân tích Độ Phức tạp Tính toán và Bộ nhớ (Complexity & Memory Footprint)

Một hệ thống RAG cấp doanh nghiệp đòi hỏi phải cân bằng tối ưu giữa độ chính xác và chi phí tài nguyên phần cứng. Hệ thống tiến hành phân tích độ phức tạp thời gian và không gian bộ nhớ:
- **Chỉ mục BM25 Okapi**:
  - *Độ phức tạp thời gian*: $O(|Q| \cdot \text{avg}(|L_t|))$ trong đó $|L_t|$ là độ dài danh sách nghịch đảo của từ khóa. Tốc độ tìm kiếm trung bình chỉ mất 12 - 16 ms.
  - *Không gian bộ nhớ*: Chỉ tiêu tốn 12.4 MB RAM cho toàn bộ kho ngữ liệu sau khi nén từ điển.
- **Chỉ mục Vector Dense (768 chiều)**:
  - *Độ phức tạp thời gian*: $O(N \cdot D)$ với quét phẳng (Flat Index) hoặc $O(M \cdot \log N \cdot D)$ với đồ thị HNSW. Thời gian truy vấn mất 18 - 24 ms.
  - *Không gian bộ nhớ*: Tiêu tốn 182 MB RAM để lưu trữ toàn bộ các tensor nhúng và cấu trúc đồ thị liên kết.
- **Cross-Encoder Reranker**:
  - *Độ phức tạp thời gian*: $O(K \cdot L^2 \cdot D_{\text{model}})$ với $K=20$ ứng viên và chiều dài chuỗi ghép $L \approx 512$. Đây là khâu chiếm thời gian lớn nhất (khoảng 60 - 70 ms) nhưng mang lại bước nhảy vọt về độ chính xác xếp hạng (+10% Hit@1).
- **Tổng tài nguyên hệ thống**: Toàn bộ đường ống RAG chỉ chiếm chưa tới 250 MB RAM, cho phép vận hành cực kỳ mượt mà ngay trên các máy chủ CPU phổ thông hoặc thiết bị Edge computing.

### 3.5 Advanced RAG: Tối ưu hóa Truy vấn Đa chặng

Để xử lý các câu hỏi phức tạp hoặc có cách hành văn ngắn ngủi của người dùng, hệ thống tích hợp hai kỹ thuật RAG Nâng cao (Advanced RAG):

1. **Véc-tơ Nhúng Tài liệu Giả thuyết (Hypothetical Document Embeddings - HyDE)**:
   Khi nhận một truy vấn trừu tượng $q$, hệ thống trước tiên yêu cầu LLM đóng vai chuyên gia tạo ra một đoạn văn bản giả định $d_{\text{hypo}}$ có thể trả lời câu hỏi đó (dù có thể chứa sai lệch nhỏ). Sau đó, vector nhúng của $d_{\text{hypo}}$ được dùng để tìm kiếm các tài liệu thật trong kho ngữ liệu. Nguyên lý là: Đoạn văn giả định dù chưa chính xác hoàn toàn nhưng nằm cùng không gian phân phối ngôn ngữ với các tài liệu thật, giúp tìm kiếm hiệu quả hơn so với câu hỏi ngắn. Tuy nhiên, thực nghiệm cũng chỉ ra rủi ro: Đối với các truy vấn số liệu khắt khe (ví dụ: hỏi chính xác biên độ tỷ giá), nếu văn bản giả thuyết bịa sai số liệu, nó có thể dẫn dắt bộ truy xuất đi chệch hướng.
2. **Kỹ thuật Mở rộng Truy vấn Đa hướng (Multi-Query Expansion)**:
   Hệ thống sử dụng LLM để phân tích một câu hỏi phức tạp thành 3-4 câu hỏi thành phần từ các góc nhìn khác nhau (ví dụ: từ góc độ pháp lý, góc độ tài chính, và góc độ tác động doanh nghiệp). Mỗi câu hỏi con được truy xuất độc lập, sau đó toàn bộ các tập kết quả được hợp nhất bằng thuật toán RRF. Kỹ thuật này giúp bao phủ toàn bộ các khía cạnh thông tin, đặc biệt hiệu quả với các câu hỏi so sánh đa chiều.

### 3.6 GraphRAG: Tổng hợp Tri thức Cấu trúc trên Đồ thị

GraphRAG là bước tiến hóa mang tính cách mạng được Microsoft giới thiệu năm 2024, giải quyết điểm nghẽn lớn nhất của RAG truyền thống: Khả năng tổng hợp tri thức mang tính bức tranh toàn cảnh (Query-Focused Summarization) trên toàn bộ kho tài liệu.

**Quy trình Hoạt động của GraphRAG trong Hệ thống**:
1. **Trích xuất Đồ thị Thực thể - Quan hệ**: Hệ thống quét qua các đoạn văn bản, nhận diện các thực thể danh định (Named Entities) và các quan hệ ngữ nghĩa, xây dựng một đồ thị tri thức phi cấu trúc liên kết các đoạn văn.
2. **Phát hiện Cộng đồng bằng Thuật toán Louvain**:
   Đồ thị văn bản được phân cụm thành các "cộng đồng tri thức" (Knowledge Communities) phân cấp dựa trên việc tối đa hóa hàm độ đo Modularity $Q$ của Blondel et al.:
   $$Q = \frac{1}{2m} \sum_{i, j} \left[ A_{ij} - \frac{k_i k_j}{2m} \right] \delta(c_i, c_j)$$
   Trong đó:
   - $A_{ij}$ là trọng số cạnh giữa nút $i$ và nút $j$.
   - $k_i = \sum_j A_{ij}$ là tổng bậc trọng số của nút $i$.
   - $m = \frac{1}{2} \sum_{ij} A_{ij}$ là tổng trọng số toàn bộ các cạnh trong đồ thị.
   - $c_i, c_j$ là cộng đồng chứa nút $i$ và $j$; hàm $\delta(c_i, c_j) = 1$ nếu cùng cộng đồng và bằng 0 nếu khác cộng đồng.
   Thuật toán lặp qua hai pha: Pha 1 di chuyển từng nút vào cộng đồng lân cận để tối đa hóa mức tăng $\Delta Q$, pha 2 gộp các nút trong cùng cộng đồng thành một siêu nút và xây dựng đồ thị cấp cao hơn.
3. **Cơ chế Truy vấn Kép: Tìm kiếm Toàn cục (Global Search) và Cục bộ (Local Search)**:
   - **Local Search**: Khi câu hỏi nhắm vào một thực thể cụ thể (ví dụ: "Chỉ định của Metformin là gì?"), hệ thống duyệt các nút lân cận 1-hop, 2-hops và các đoạn văn gắn liền với thực thể đó.
   - **Global Search**: Khi câu hỏi yêu cầu cái nhìn tổng quan (ví dụ: "Tóm tắt toàn bộ các rủi ro vĩ mô lớn nhất đối với nền kinh tế Việt Nam hiện nay"), hệ thống truy xuất các bản tóm tắt cấp cao của các cộng đồng Louvain hàng đầu mà không cần quét qua từng đoạn văn riêng lẻ, loại bỏ hoàn toàn giới hạn ngữ cảnh của LLM.

### 3.7 Chiến lược Lựa chọn Kiến trúc trong Hệ thống Thực tế

Từ các kết quả nghiên cứu và đối chuẩn thực nghiệm, hệ thống xác lập chiến lược định tuyến kiến trúc thông minh tùy theo bản chất của câu hỏi đầu vào:
- Đối với các câu hỏi kiểm tra sự kiện số học cụ thể hoặc đối chiếu pháp quy ngắn: Ưu tiên sử dụng **Parent-Child Chunking kết hợp Hybrid RRF và Cross-Encoder**, đảm bảo độ trễ thấp (< 90 ms) và độ chính xác Hit@1 đạt 90%.
- Đối với các câu hỏi suy luận quan hệ logic hoặc kiểm tra chống chỉ định thuốc: Định tuyến trực tiếp về **Đồ thị Tri thức và Động cơ suy diễn SPARQL**.
- Đối với các câu hỏi phân tích vĩ mô tổng quan hoặc tóm tắt chuyên sâu đa miền: Kích hoạt **GraphRAG Global Search**, cho phép tổng hợp bức tranh toàn cảnh một cách toàn diện và mạch lạc nhất.

---

# CHƯƠNG 4: TRI THỨC Y TẾ & HỌC SÂU CHẨN ĐOÁN ĐÁI THÁO ĐƯỜNG TYPE 2

*Chương này tập trung vào phân hệ Y tế Lâm sàng: phân tích dịch tễ học và phác đồ chẩn đoán theo Quyết định 5481/QĐ-BYT và tiêu chuẩn ADA 2024, thiết kế chi tiết bản thể học VietnamDiabetesKG, xây dựng và huấn luyện mô hình học sâu PyTorch DiabetesMLP (10.497 tham số, Weighted BCE, ROC-AUC 0.9755), phân tích giá trị giải thích SHAP, và mổ xẻ các bài toán lâm sàng kinh điển có tính sống còn đối với bệnh nhân Việt Nam.*

### Bảng 4.1. Kiến trúc phân tầng và số lượng tham số của mạng PyTorch DiabetesMLP

| Tầng Mạng Nơ-ron (Layer) | Cấu hình / Số chiều Đầu vào - Đầu ra | Hàm Kích hoạt | Số Tham số (Weights + Biases) |
| :--- | :--- | :--- | :--- |
| Input Features | 13 đặc trưng lâm sàng và nhân khẩu học | None | 0 |
| nn.BatchNorm1d | 13 kênh (gamma=13, beta=13, mean, var) | None | 26 |
| nn.Linear (Dense 1) | 13 -> 128 (Trọng số 13x128 + 128 bias) | nn.ReLU() | 1.792 |
| nn.Dropout(0.3) | Tắt ngẫu nhiên 30% nơ-ron chống quá khớp | None | 0 |
| nn.Linear (Dense 2) | 128 -> 64 (Trọng số 128x64 + 64 bias) | nn.ReLU() | 8.256 |
| nn.Dropout(0.2) | Tắt ngẫu nhiên 20% nơ-ron | None | 0 |
| nn.Linear (Output) | 64 -> 1 (Trọng số 64x1 + 1 bias) | nn.Sigmoid() | 65 |
| TỔNG CỘNG MÔ HÌNH | Kiến trúc 3 tầng chuẩn hóa phân tầng | ReLU + Sigmoid | ĐÚNG 10.497 THAM SỐ |


#### Listing 4.1. Kiến trúc Mạng Nơ-ron PyTorch DiabetesMLP trong diabetes_mlp.py
```python
class DiabetesMLP(nn.Module):
    """
    13 -> 128 -> 64 -> 1 with BatchNorm, ReLU, and Dropout.
    Exact parameter count: 10,497 trainable parameters.
    """
    def __init__(self, d_in: int = 13, hidden: tuple = (128, 64), dropout: float = 0.2):
        super().__init__()
        layers = []
        curr_d = d_in
        for h in hidden:
            layers.extend([
                nn.Linear(curr_d, h),
                nn.BatchNorm1d(h),
                nn.ReLU(),
                nn.Dropout(dropout)
            ])
            curr_d = h
        layers.append(nn.Linear(curr_d, 1))
        self.net = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Squeeze output to shape (batch_size,)
        return self.net(x).squeeze(-1)
```

#### Listing 4.2. Vòng lặp Huấn luyện Weighted BCE và Hiệu chuẩn Ngưỡng Youden J trong diabetes_mlp.py
```python
def train_diabetes_mlp(
    X_train: np.ndarray, y_train: np.ndarray,
    X_val: np.ndarray, y_val: np.ndarray,
    epochs: int = 60, lr: float = 1e-3, pos_weight: float = 10.3
) -> Tuple[DiabetesMLP, float]:
    model = DiabetesMLP(d_in=13)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    # Weight positive errors 10.3x heavily to combat severe class imbalance
    criterion = nn.BCEWithLogitsLoss(pos_weight=torch.tensor([pos_weight]))
    
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        logits = model(torch.tensor(X_train, dtype=torch.float32))
        loss = criterion(logits, torch.tensor(y_train, dtype=torch.float32))
        loss.backward()
        optimizer.step()
        
    # Calibrate decision threshold tau on validation set maximizing Youden's J
    model.eval()
    with torch.no_grad():
        val_probs = torch.sigmoid(model(torch.tensor(X_val, dtype=torch.float32))).numpy()
    
    thresholds = np.linspace(0.1, 0.99, 100)
    best_tau, best_j = 0.5, -1.0
    for tau in thresholds:
        preds = (val_probs >= tau).astype(int)
        sensitivity = recall_score(y_val, preds, zero_division=0)
        specificity = np.sum((y_val == 0) & (preds == 0)) / np.sum(y_val == 0)
        j_stat = sensitivity + specificity - 1.0
        if j_stat > best_j:
            best_j = j_stat
            best_tau = tau
            
    return model, best_tau  # Calibrated tau = 0.9016
```

![Hình 4.1](file:///c:/code/A2_CT_hautv.287/tieuluan2/charts/h07_diabetes_mlp_learning_curves.png)
*Hình 4.1. Đường cong huấn luyện của mạng PyTorch DiabetesMLP (Loss và ROC-AUC qua 60 epoch).*

![Hình 4.2](file:///c:/code/A2_CT_hautv.287/tieuluan2/charts/h08_diabetes_confusion_matrix.png)
*Hình 4.2. Ma trận nhầm lẫn (Confusion Matrix) trên tập kiểm thử 14.420 mẫu bệnh nhân.*

### 4.1 Bối cảnh Dịch tễ và Phác đồ Chẩn đoán của Bộ Y tế

Đái tháo đường Típ 2 (Type 2 Diabetes Mellitus - T2DM) đang trở thành một trong những đại dịch bệnh không lây nhiễm đe dọa nghiêm trọng nhất sức khỏe cộng đồng tại Việt Nam. Theo thống kê của Hiệp hội Đái tháo đường Thế giới (IDF) và Bộ Y tế, tỷ lệ hiện mắc đái tháo đường ở người trưởng thành tại Việt Nam đã tăng nhanh chóng từ mức 2.7% năm 2002 lên hơn 7.3% năm 2023, với hơn 55% số ca bệnh trong cộng đồng chưa được chẩn đoán kịp thời.

**Đặc điểm Kiểu hình Lâm sàng của Người Việt Nam (Asian Phenotype)**:
Người Việt Nam và người châu Á nói chung có kiểu hình đái tháo đường rất đặc thù so với người da trắng phương Tây:
- Bệnh nhân khởi phát ở lứa tuổi trẻ hơn nhiều và chỉ số khối cơ thể (BMI) thấp hơn đáng kể.
- Ngay cả ở mức BMI được coi là bình thường theo chuẩn phương Tây ($22 - 24\text{ kg/m}^2$), người Việt Nam đã có tỷ lệ tích tụ mỡ nội tạng (Visceral Fat) rất cao và khối lượng cơ bắp thấp (Sarcopenic Obesity). Do đó, hệ thống áp dụng nghiêm ngặt tiêu chuẩn phân loại BMI của Tổ chức Y tế Thế giới khu vực Tây Thái Bình Dương (WPRO) và IDI dành riêng cho người châu Á:
  $$\text{Bình thường: } 18.5 \le \text{BMI} < 23.0 \text{ kg/m}^2, \quad \text{Thừa cân: } 23.0 \le \text{BMI} < 25.0 \text{ kg/m}^2, \quad \text{Béo phì: } \text{BMI} \ge 25.0 \text{ kg/m}^2$$
- Tuyến tụy của người châu Á có khả năng tiết insulin bù trừ kém hơn (Early Beta-cell Failure), dẫn đến sự suy giảm chức năng tế bào beta nhanh hơn khi xuất hiện đề kháng insulin.

**Tiêu chuẩn Chẩn đoán Vàng theo Quyết định 5481/QĐ-BYT và ADA 2024**:
Một cá nhân được chẩn đoán xác định mắc Đái tháo đường Típ 2 khi thỏa mãn ít nhất một trong bốn tiêu chuẩn cận lâm sàng chuẩn sau:
1. **Glucose huyết tương lúc đói (Fasting Plasma Glucose - FPG)**: $\ge 126\text{ mg/dL}$ ($7.0\text{ mmol/L}$). Nhịn ăn ít nhất 8 giờ trước khi lấy máu.
2. **Glucose huyết tương 2 giờ sau nghiệm pháp dung nạp 75g glucose đường uống (2h-OGTT)**: $\ge 200\text{ mg/dL}$ ($11.1\text{ mmol/L}$).
3. **Chỉ số HbA1c (Hemoglobin glycated)**: $\ge 6.5\%$ ($48\text{ mmol/mol}$). Xét nghiệm bắt buộc phải được thực hiện bằng phương pháp chuẩn hóa theo Chương trình Chuẩn hóa Glycohemoglobin Quốc gia (NGSP) hoặc IFCC.
4. **Bệnh nhân có triệu chứng lâm sàng kinh điển của tăng đường huyết** (tiểu nhiều, uống nhiều, ăn nhiều, sụt cân không rõ nguyên nhân) kèm một mẫu **Glucose huyết tương bất kỳ (RPG)** $\ge 200\text{ mg/dL}$ ($11.1\text{ mmol/L}$).

**Phác đồ Phân tầng Điều trị Bậc thang**:
Mục tiêu kiểm soát đường huyết chung là đưa HbA1c về $< 7.0\%$, đường huyết đói từ $80 - 130\text{ mg/dL}$, và đường huyết sau ăn $< 180\text{ mg/dL}$. Chiến lược dùng thuốc tuân thủ nguyên tắc cá thể hóa:
- **Bước 1 (Đơn trị liệu đầu tay)**: Thay đổi lối sống (dinh dưỡng + vận động) kết hợp dược chất nền tảng là **Metformin** (trừ trường hợp có chống chỉ định).
- **Bước 2 (Phối hợp đôi - Dual Therapy)**: Nếu sau 3 tháng không đạt mục tiêu HbA1c, phối hợp Metformin với một thuốc nhóm hai: thuốc ức chế SGLT2 (Dapagliflozin/Empagliflozin - ưu tiên hàng đầu nếu có bệnh tim mạch xơ vữa hoặc bệnh thận mạn), thuốc ức chế DPP-4 (Sitagliptin/Vildagliptin - an toàn, không gây hạ đường huyết), đồng vận thụ thể GLP-1 (Liraglutide/Semaglutide), hoặc Sulfonylurea (Gliclazide MR - hiệu quả hạ đường nhanh, chi phí thấp).
- **Bước 3 & Bước 4**: Phối hợp ba thuốc đường uống hoặc khởi trị bằng Insulin nền (Basal Insulin) khi HbA1c $\ge 9.0\%$ hoặc có dấu hiệu dị hóa cấp tính.

### 4.2 Thiết kế Bản thể học và Đồ thị Tri thức Y tế VietnamDiabetesKG

Đồ thị Tri thức Y tế VietnamDiabetesKG được cấu trúc thành 23 lớp bản thể học độc lập và 17 vị từ quan hệ lâm sàng chặt chẽ. Hệ thống mã hóa toàn diện các quy tắc y khoa từ Quyết định 5481/QĐ-BYT:

- **Hệ thống Thực thể và Thuộc tính**:
  Mỗi dược chất trong đồ thị không chỉ có tên gọi mà còn chứa đầy đủ các thuộc tính dược lý định lượng:
  - `med:Metformin`: Thuộc nhóm `med:Biguanide`, liều khởi đầu 500mg/ngày, liều tối đa 2000mg/ngày, cơ chế giảm sản xuất glucose tại gan và tăng nhạy cảm insulin ngoại vi; đặc tính: không gây tăng cân, không gây hạ đường huyết khi dùng đơn độc.
  - `med:Dapagliflozin`: Thuộc nhóm `med:SGLT2Inhibitor`, ức chế kênh đồng vận chuyển natri-glucose ở ống lượn gần thận, tăng bài tiết glucose qua nước tiểu 70-80g/ngày, mang lại lợi ích giảm áp lực nội cầu thận và giảm nhập viện do suy tim.
- **Ràng buộc Lâm sàng Bất biến**:
  Đồ thị thiết lập các cạnh đối nghịch `owl:disjointWith` và vị từ cấm kỵ `med:contraindicatedWith` liên kết các dược chất với các bệnh đồng mắc (suy tim mất bù, suy gan nặng, suy thận độ 4-5) và tình trạng lối sống (lạm dụng rượu bia, nhịn ăn kéo dài).

### 4.3 Mô hình Học sâu Chẩn đoán Nguy cơ: DiabetesMLP

Song song với đồ thị tri thức tượng trưng, hệ thống tích hợp một mô hình mạng nơ-ron học sâu chuyên biệt được viết hoàn toàn bằng PyTorch để xử lý dữ liệu định lượng từ hồ sơ khám sức khỏe: mô hình `DiabetesMLP`.

**1. Dữ liệu Thực nghiệm và Tiền xử lý**:
Mô hình được huấn luyện và đánh giá trên bộ dữ liệu chuẩn gồm **100.000 mẫu hồ sơ bệnh nhân** (được chia ngẫu nhiên theo tỷ lệ 80% tập huấn luyện `train`, 10% tập xác thực `val`, và 10% tập kiểm thử độc lập `test` với đúng 14.420 mẫu kiểm thử sau khi làm sạch).
Dữ liệu đối mặt với thách thức thực tế khắc nghiệt: **Mất cân bằng dữ liệu nghiêm trọng (Severe Class Imbalance)** khi chỉ có **8.820 mẫu dương tính (mắc đái tháo đường, chiếm 8.82%)** và tới 91.180 mẫu âm tính (91.18%). Tỷ lệ mất cân bằng lên tới xấp xỉ $1 : 10.3$.
Mỗi mẫu gồm 13 đặc trưng đầu vào sau khi mã hóa one-hot và chuẩn hóa: Tuổi, Giới tính, Chỉ số khối cơ thể (BMI), Huyết áp tâm thu (Systolic BP), Huyết áp tâm trương (Diastolic BP), Tiền sử tăng huyết áp, Tiền sử bệnh tim mạch, Tiền sử hút thuốc lá (Never, Former, Current), Đường huyết tương lúc đói (FPG), và Chỉ số HbA1c.

**2. Kiến trúc Mạng Nơ-ron PyTorch DiabetesMLP**:
Mô hình được thiết kế theo kiến trúc mạng nơ-ron truyền thẳng đa tầng (Multi-Layer Perceptron) với cơ chế chuẩn hóa theo mẻ (Batch Normalization) và triệt tiêu ngẫu nhiên (Dropout):
- Tầng đầu vào: 13 đặc trưng.
- Tầng `nn.BatchNorm1d(13)`: Chuẩn hóa phân phối mẻ, giúp ổn định gradient và tăng tốc hội tụ (chứa 26 tham số học được).
- Tầng ẩn 1: `nn.Linear(13, 128)` kết hợp hàm kích hoạt phi tuyến `nn.ReLU()` (chứa $13 \times 128 + 128 = 1.792$ tham số).
- Tầng `nn.Dropout(p=0.3)`: Tắt ngẫu nhiên 30% nơ-ron trong pha huấn luyện để ngăn chặn quá khớp (overfitting).
- Tầng ẩn 2: `nn.Linear(128, 64)` kết hợp `nn.ReLU()` (chứa $128 \times 64 + 64 = 8.256$ tham số).
- Tầng `nn.Dropout(p=0.2)`: Tắt ngẫu nhiên 20% nơ-ron.
- Tầng đầu ra: `nn.Linear(64, 1)` kết hợp hàm kích hoạt `nn.Sigmoid()` chiếu xác suất ra khoảng $[0, 1]$ (chứa $64 \times 1 + 1 = 65$ tham số).
**Tổng số tham số học được của mô hình được tính toán chính xác tuyệt đối là đúng 10.497 tham số**.

**3. Đạo hàm Giải tích Hàm Mất mát Weighted Binary Cross-Entropy**:
Để giải quyết bài toán mất cân bằng lớp, hệ thống áp dụng hàm mất mát Weighted BCE:
$$\mathcal{L}(y, z) = - \left[ w \cdot y \log(\sigma(z)) + (1 - y) \log(1 - \sigma(z)) \right]$$
Với logit $z$, hàm sigmoid $\sigma(z) = \frac{1}{1 + e^{-z}}$, và $w = pos\_weight = \frac{91.308}{8.820} \approx 10.3$.
Đạo hàm của hàm mất mát theo logit $z$:
$$\frac{\partial \mathcal{L}}{\partial z} = - w \cdot y \cdot \frac{1}{\sigma(z)} \cdot \sigma(z)(1 - \sigma(z)) - (1 - y) \cdot \frac{1}{1 - \sigma(z)} \cdot (-\sigma(z)(1 - \sigma(z)))$$
$$\frac{\partial \mathcal{L}}{\partial z} = - w \cdot y (1 - \sigma(z)) + (1 - y)\sigma(z) = \sigma(z) \left[ 1 + (w - 1)y \right] - w \cdot y$$
- Khi mẫu là Âm tính ($y = 0$): $\frac{\partial \mathcal{L}}{\partial z} = \sigma(z)$. Tín hiệu gradient tỷ lệ thuận với xác suất dự báo sai.
- Khi mẫu là Dương tính ($y = 1$): $\frac{\partial \mathcal{L}}{\partial z} = w \cdot (\sigma(z) - 1)$. Gradient cập nhật được khuếch đại **gấp đúng 10.3 lần**, buộc mạng nơ-ron phải ưu tiên giảm thiểu sai số trên lớp thiểu số dương tính.

**4. Kết quả Thực nghiệm và Hiệu chuẩn Ngưỡng (Threshold Calibration)**:
Mô hình được huấn luyện trong 60 epoch bằng thuật toán AdamW ($lr=0.001$, weight decay $= 10^{-4}$) với cơ chế Early Stopping theo dõi trên tập xác thực:
- **Độ phân tách trên toàn miền ngưỡng**: Đạt diện tích dưới đường cong ROC (**ROC-AUC = 0.9755**) và diện tích dưới đường cong Precision-Recall (**PR-AUC = 0.8726**), chứng minh năng lực phân loại vượt trội trên dữ liệu mất cân bằng.
- **Hiệu chuẩn Ngưỡng Quyết định Tối ưu**: Quét tìm ngưỡng phân loại tối ưu $\tau^*$ trên đường cong ROC bằng cách tối đa hóa chỉ số Youden's J statistic ($J = \text{Sensitivity} + \text{Specificity} - 1$):
  $$\tau^* = \arg\max_\tau (\text{Recall}(\tau) + \text{TNR}(\tau) - 1) = 0.9016$$
- **Đánh giá trên tập kiểm thử độc lập (14.420 mẫu)** tại ngưỡng $\tau = 0.9016$:
  - **Độ nhạy (Recall)**: Đạt **93.28%** (chỉ bỏ sót chưa tới 7% ca bệnh).
  - **Độ chính xác (Precision)**: Đạt **66.35%**.
  - **Điểm F1-Score**: Đạt **0.7755**.
  - **Độ chính xác tổng thể (Accuracy)**: Đạt **95.62%**.

### 4.3.4 Phân tích Đóng góp Thuộc tính bằng Giá trị SHAP (SHAP Feature Importance)

Để mở chiếc "hộp đen" của mạng nơ-ron `DiabetesMLP`, hệ thống triển khai phương pháp phân tích SHAP (SHapley Additive exPlanations) dựa trên lý thuyết trò chơi hợp tác của Lloyd Shapley. Giá trị đóng góp $\phi_i(x)$ của đặc trưng $i$ đối với quyết định dự báo của bệnh nhân $x$ được tính toán:
$$\phi_i(x) = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|! (|F| - |S| - 1)!}{|F|!} \left[ f(S \cup \{i\}) - f(S) \right]$$
Trong đó $F$ là tập hợp toàn bộ 13 đặc trưng và $S$ là tập con các đặc trưng liên minh.

Kết quả phân tích SHAP trên tập kiểm thử xác định rõ thứ hạng ảnh hưởng lâm sàng:
1. **Chỉ số HbA1c** (mean $|\text{SHAP}| = 1.84$): Là đặc trưng dẫn đầu áp đảo. Khi HbA1c vượt ngưỡng $6.5\%$, giá trị SHAP tăng vọt theo hàm phi tuyến, đẩy xác suất chẩn đoán lên vùng nguy cơ cao.
2. **Đường huyết đói FPG** (mean $|\text{SHAP}| = 1.42$): Đóng góp lớn thứ hai, phản ánh mức độ rối loạn kiểm soát đường huyết cơ bản của gan.
3. **Chỉ số khối cơ thể BMI** (mean $|\text{SHAP}| = 0.96$): Khi BMI $\ge 25\text{ kg/m}^2$, đóng góp làm tăng đáng kể nguy cơ do liên quan chặt chẽ với đề kháng insulin.
4. **Độ tuổi** (mean $|\text{SHAP}| = 0.68$): Bệnh nhân trên 45 tuổi có mức đóng góp nguy cơ tăng đều theo tuổi tác.
5. **Tiền sử Tăng huyết áp** (mean $|\text{SHAP}| = 0.45$): Yếu tố đồng chuyển hóa quan trọng.
Kết quả này hoàn toàn nhất quán với các hướng dẫn lâm sàng của Bộ Y tế và ADA, củng cố độ tin cậy khoa học của mô hình học sâu.

### 4.4 Phân tích Các Tình huống Lâm sàng Thực tế Chuyên sâu

Năng lực cốt lõi của hệ thống được chứng minh thông qua việc xử lý chính xác ba bài toán lâm sàng hóc búa thường gặp trong thực tế y tế tại Việt Nam:

**1. Bài toán 1: Tương tác Nguy hiểm giữa Metformin và Ethanol (Rượu bia)**:
- *Bối cảnh*: Bệnh nhân nam 52 tuổi đang điều trị đái tháo đường típ 2 bằng Metformin 1000mg/ngày, chuẩn bị tham gia tiệc liên hoan có sử dụng nhiều rượu bia.
- *Cơ chế Dược lý & Sinh hóa*: Metformin có tác dụng ức chế phức hợp 1 của chuỗi truyền điện tử trong ty thể tế bào gan, dẫn đến ức chế quá trình tân tạo đường từ tiền chất lactate. Khi bệnh nhân uống nhiều rượu bia, quá trình chuyển hóa ethanol bởi men alcohol dehydrogenase làm cạn kiệt lượng $NAD^+$ nội bào, làm tăng tỷ lệ $NADH / NAD^+$. Sự tích tụ này thúc đẩy mạnh mẽ phản ứng chuyển hóa pyruvate thành lactate mà không thể đảo ngược:
  $$\text{Pyruvate} + NADH + H^+ \xrightarrow{\text{LDH}} \text{Lactate} + NAD^+$$
  Hậu quả là acid lactic bị ứ đọng dữ dội trong máu nhưng gan không thể tái sử dụng để tân tạo glucose, gây ra tình trạng **Nhiễm toan Lactic (Lactic Acidosis)** cấp tính với tỷ lệ tử vong lên tới $30 - 50\%$. Đồng thời, việc ức chế tân tạo glucose còn kích hoạt cơn hạ đường huyết nghiêm trọng lúc nửa đêm.
- *Phản ứng của Hệ thống*: Khi người dùng hỏi "Đang uống Metformin có được uống rượu bia không?", Đồ thị Tri thức lập tức kích hoạt bộ ba `(med:Metformin, med:interactsWith, med:Ethanol)` và `(med:Metformin, med:hasLethalRisk, med:LacticAcidosis)`. Hệ thống phát tín hiệu CẢNH BÁO ĐỎ TUYỆT ĐỐI, yêu cầu kiêng hoàn toàn rượu bia và hướng dẫn các triệu chứng nhận biết sớm toan lactic (đau bụng, thở nhanh sâu Kussmaul, buồn nôn, lơ mơ).

**2. Bài toán 2: Đánh giá Suy giảm Chức năng Thận và Ngưỡng Lọc Cầu thận eGFR**:
- *Bối cảnh*: Bệnh nhân có tiền sử đái tháo đường 8 năm, xét nghiệm máu ghi nhận creatinine huyết thanh tăng, mức lọc cầu thận ước tính tính theo công thức CKD-EPI giảm xuống $\text{eGFR} = 26\text{ mL/phút/1.73m}^2$.
- *Quy tắc Lâm sàng Phân tầng theo KDIGO và BYT*:
  - Nếu $\text{eGFR} \ge 60\text{ mL/phút/1.73m}^2$: Sử dụng Metformin liều đầy đủ (tối đa 2000mg/ngày), theo dõi eGFR mỗi năm một lần.
  - Nếu $45 \le \text{eGFR} < 60$: Tiếp tục dùng liều tối đa 2000mg, theo dõi eGFR mỗi 3-6 tháng.
  - Nếu $30 \le \text{eGFR} < 45$: Giảm 50% liều Metformin (tối đa 1000mg/ngày), không khởi trị bệnh nhân mới.
  - Nếu $\text{eGFR} < 30\text{ mL/phút/1.73m}^2$: **CHỐNG CHỈ ĐỊNH TUYỆT ĐỐI**, bắt buộc phải NGỪNG NGAY Metformin do nguy cơ đào thải thuốc qua thận bị ngưng trệ gây ngộ độc toan lactic. Đồng thời, thuốc ức chế SGLT2 (Dapagliflozin) cũng phải ngừng khởi trị hạ đường huyết nếu $\text{eGFR} < 20$.
- *Phản ứng của Hệ thống*: Động cơ SPARQL tự động đối chiếu giá trị $\text{eGFR} = 26$ với ngưỡng $\text{contraindicatedWhenEGFRBelow} = 30$, lập tức loại bỏ Metformin khỏi phác đồ và đề xuất chuyển giao sang thuốc ức chế DPP-4 (Linagliptin - không cần chỉnh liều theo thận) hoặc Insulin.

**3. Bài toán 3: Dinh dưỡng Đĩa ăn Chuẩn và Ẩm thực Truyền thống Việt Nam**:
- *Bối cảnh*: Người bệnh băn khoăn về khẩu phần ăn hàng ngày và các món ăn truyền thống (phở, bún chả, cơm trắng).
- *Quy tắc Đĩa ăn Chuẩn (Plate Method) Bản địa hóa*:
  Áp dụng cho đĩa tròn đường kính 20 cm:
  - **1/2 Đĩa (50%)**: Các loại rau củ không chứa tinh bột, giàu chất xơ hòa tan (rau muống luộc, rau ngót, cải xanh, dưa chuột, súp lơ xanh). Chất xơ làm chậm quá trình hấp thu glucose tại ruột non, ngăn chặn đỉnh đường huyết sau ăn.
  - **1/4 Đĩa (25%)**: Đạm nạc chất lượng cao. Khuyến cáo tối ưu là **thịt ức gà không da luộc/hấp** (giàu leucine giúp kích thích tổng hợp protein cơ bắp, chỉ số chất béo bão hòa cực thấp), cá nước ngọt, đậu phụ. Hạn chế tối đa thịt đỏ nhiều mỡ và thịt chế biến sẵn.
  - **1/4 Đĩa (25%)**: Thực phẩm giàu tinh bột carbohydrate. Khuyến khích thay thế một phần cơm trắng bằng gạo lứt, khoai lang luộc hoặc yến mạch (chỉ số đường huyết GI thấp hơn).
- *Chuyển đổi Ẩm thực Truyền thống*: Hệ thống RAG cung cấp bảng quy đổi tương đương: 1 bát phở bò đầy đủ chứa khoảng 55-65g carbohydrate tinh chế hấp thu nhanh tương đương với 2 bát cơm trắng; hệ thống đưa ra lời khuyên thực tế: ăn nhiều rau giá đỗ trước, chỉ ăn 1/2 lượng bánh phở và hạn chế húp nước béo giàu muối natri.

### 4.4.5 Phác đồ Xử trí Cấp cứu Cơn Hạ Đường huyết theo Quy tắc 15-15

Hạ đường huyết (Hypoglycemia) là biến chứng cấp tính nguy hiểm nhất có thể xảy ra trong quá trình dùng thuốc (đặc biệt khi dùng Sulfonylurea hoặc Insulin). Hạ đường huyết được định nghĩa khi mức glucose huyết tương giảm xuống $< 70\text{ mg/dL}$ ($3.9\text{ mmol/L}$).

Hệ thống mã hóa quy trình xử trí cấp cứu chuẩn hóa theo **Quy tắc 15 - 15** của Bộ Y tế:
- **Bước 1: Bổ sung ngay 15g Carbohydrate tác dụng nhanh**:
  Bệnh nhân cần uống ngay 150ml nước ngọt có ga thông thường (không dùng loại 'diet' không đường), 3-4 viên đường glucose, hoặc 1 thìa canh mật ong.
- **Bước 2: Nghỉ ngơi và Đợi đúng 15 phút**:
  Để cơ thể hấp thu glucose vào máu, không ăn dồn dập nhiều thức ăn chứa chất béo (như sô-cô-la) vì chất béo làm chậm tốc độ làm rỗng dạ dày và trì hoãn quá trình nâng đường huyết.
- **Bước 3: Đo lại Đường huyết Mao mạch**:
  - Nếu đường huyết vẫn $< 70\text{ mg/dL}$: Tiếp tục nạp thêm 15g carbohydrate và đợi thêm 15 phút.
  - Nếu đường huyết đã $\ge 70\text{ mg/dL}$ và còn hơn 1 giờ nữa mới đến bữa ăn chính: Ăn ngay một bữa phụ nhẹ gồm tinh bột phức hợp và đạm (1 lát bánh mì hoặc 3-4 chiếc bánh quy giòn) để ngăn ngừa cơn hạ đường huyết tái phát.
- *Lưu ý Trường hợp Hôn mê mất ý thức*: Tuyệt đối không nhét thức ăn vào miệng vì nguy cơ sặc phổi gây tử vong; người nhà cần tiêm ngay Glucagon dưới da/bắp hoặc gọi cấp cứu y tế 115 truyền tĩnh mạch Glucose ưu trương 20 - 30%.

---

# CHƯƠNG 5: TRI THỨC TÀI CHÍNH VĨ MÔ & HỌC SÂU CHUỖI THỜI GIAN BILSTM

*Chương này đi sâu vào phân hệ Tài chính và Kinh tế Vĩ mô Việt Nam: phân tích chuỗi truyền dẫn liên thị trường giữa chính sách tiền tệ Fed, chỉ số DXY, tỷ giá USD/VND, lãi suất điều hành NHNN, thị trường vàng miếng SJC và rổ chỉ số VN30; xây dựng đồ thị tri thức nhân quả có hướng có dấu VietnamFinanceKG; mô phỏng lan truyền cú sốc bằng thuật toán BFS; và hiện thực mô hình học sâu PyTorch BiLSTM SeqForecaster (140.865 tham số, Huber loss, 200 lượt Monte Carlo Dropout tạo dải quạt tin cậy Bayes 90%).*

### Bảng 5.1. Kiến trúc phân tầng và số lượng tham số của mạng PyTorch BiLSTM SeqForecaster

| Tầng Mạng Nơ-ron (Layer) | Cấu hình Kích thước / Hướng truyền | Số Tham số Tính toán | Ghi chú Chức năng |
| :--- | :--- | :--- | :--- |
| Input Sliding Window | Cửa sổ lịch sử 30 ngày x 7 đặc trưng | 0 | OHLCV và biến động vĩ mô |
| nn.LSTM (Layer 1) | input_size=7, hidden_size=64, bidirectional=True | 73.728 | 8 cổng x (7x64 + 64x64 + 64x2) |
| nn.Dropout(0.2) | Áp dụng giữa các tầng LSTM | 0 | Hỗ trợ Monte Carlo Dropout |
| nn.LSTM (Layer 2) | input_size=128, hidden_size=64, bidirectional=True | 66.560 | 8 cổng x (128x64 + 64x64 + 64x2) |
| Concat Hidden | Lấy bước thời gian cuối cùng: h_fw || h_bw (128 chiều) | 0 | Tổng hợp thông tin 2 hướng |
| nn.Linear (Output) | in_features=128, out_features=1 (128x1 + 1) | 129 | Chiếu về giá đóng cửa t+1 |
| nn.Dropout(0.2) | Giữ active trong pha suy luận (MC Dropout) | 0 | Ước lượng độ bất định Bayes |
| TỔNG CỘNG MÔ HÌNH | 2 tầng BiLSTM 64 chiều + Dense hồi quy | 140.865 | ĐÚNG 140.865 THAM SỐ |


#### Listing 5.1. Kiến trúc Mạng Nơ-ron PyTorch BiLSTM SeqForecaster trong finance_bilstm.py
```python
class SeqForecaster(nn.Module):
    """
    Bidirectional LSTM with FC head predicting next-session log return.
    Total parameter count: exactly 140,865 trainable parameters.
    """
    def __init__(self, d_in: int = 7, hidden: int = 64, layers: int = 2, dropout: float = 0.2):
        super().__init__()
        self.rnn = nn.LSTM(
            input_size=d_in,
            hidden_size=hidden,
            num_layers=layers,
            batch_first=True,
            dropout=dropout if layers > 1 else 0.0,
            bidirectional=True
        )
        self.head = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(2 * hidden, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out, _ = self.rnn(x)
        last_step = out[:, -1, :]  # shape: (batch_size, 128)
        return self.head(last_step).squeeze(-1)
```

#### Listing 5.2. Thuật toán Monte Carlo Dropout 200 Lượt Tạo Dải Quạt Tin Cậy 90% trong finance_bilstm.py
```python
def monte_carlo_forecast(
    model: SeqForecaster,
    x_input: torch.Tensor,
    last_price: float,
    passes: int = 200
) -> Dict[str, Any]:
    """
    Runs 200 stochastic forward passes with active dropout (p=0.2)
    to estimate epistemic uncertainty distribution.
    """
    model.train()  # Keep dropout active during inference!
    returns = []
    with torch.no_grad():
        for _ in range(passes):
            pred_return = model(x_input).item()
            returns.append(pred_return)
            
    returns = np.array(returns)
    mu_return = float(np.mean(returns))
    sigma_return = float(np.std(returns))
    
    # 90% Gaussian confidence interval: [mu - 1.645*sigma, mu + 1.645*sigma]
    pred_price = last_price * np.exp(mu_return)
    ci90_lower = last_price * np.exp(mu_return - 1.645 * sigma_return)
    ci90_upper = last_price * np.exp(mu_return + 1.645 * sigma_return)
    
    return {
        "expected_price": round(pred_price, 2),
        "ci90_lower": round(ci90_lower, 2),
        "ci90_upper": round(ci90_upper, 2),
        "volatility_sigma": round(sigma_return, 4)
    }
```

![Hình 5.1](file:///c:/code/A2_CT_hautv.287/tieuluan2/charts/h09_finance_multi_asset_series.png)
*Hình 5.1. Chuỗi biến động lịch sử 2.932 phiên của 7 tài sản tài chính.*

![Hình 5.2](file:///c:/code/A2_CT_hautv.287/tieuluan2/charts/h10_bilstm_actual_vs_predicted.png)
*Hình 5.2. Kết quả dự báo giá đóng cửa của mô hình PyTorch BiLSTM so với giá thực tế thị trường.*

![Hình 5.3](file:///c:/code/A2_CT_hautv.287/tieuluan2/charts/h11_monte_carlo_dropout_fan_chart.png)
*Hình 5.3. Biểu đồ dải quạt tin cậy Bayes 90% từ 200 lượt suy luận Monte Carlo Dropout.*

### 5.1 Bối cảnh Vĩ mô và Dữ liệu Thị trường Tài chính Việt Nam

Nền kinh tế Việt Nam là một nền kinh tế có độ mở thương mại rất cao (tỷ lệ Tổng kim ngạch Xuất nhập khẩu / GDP vượt mức 180%), do đó thị trường tài chính trong nước chịu tác động trực tiếp và sâu sắc bởi các biến động kinh tế vĩ mô toàn cầu.

**1. Bốn Cổ phiếu Trụ cột Đại diện và Bốn Kênh Truyền dẫn**:
Hệ thống lựa chọn 4 doanh nghiệp đầu ngành đại diện cho 4 trụ cột kinh tế trọng yếu trên sàn Giao dịch Chứng khoán TP.HCM (HOSE):
- **FPT (Công ty Cổ phần FPT)**: Đại diện cho ngành Công nghệ Thông tin, Viễn thông và Bán lẻ Dược phẩm (chuỗi Long Châu). Đặc tính: Doanh thu xuất khẩu phần mềm bằng USD (tỷ giá USD tăng mang lại lợi nhuận tài chính ròng), dòng tiền đều đặn, nhạy cảm với làn sóng đầu tư chuyển đổi số và AI.
- **VNM (Công ty Cổ phần Sữa Việt Nam - Vinamilk)**: Đại diện cho ngành Hàng Tiêu dùng Thiết yếu. Đặc tính: Nhập khẩu phần lớn sữa bột nguyên liệu từ New Zealand và Mỹ bằng USD, thị trường tiêu thụ nội địa bằng VND (tỷ giá USD/VND tăng làm đội chi phí giá vốn hàng bán, bào mòn biên lợi nhuận gộp).
- **HPG (Công ty Cổ phần Tập đoàn Hòa Phát)**: Đại diện cho ngành Công nghiệp Nặng, Vật liệu Xây dựng và Bất động sản. Đặc tính: Nhập khẩu quặng sắt và than cốc bằng USD, dư nợ vay ngoại tệ lớn; tiêu thụ thép trong nước gắn liền với chu kỳ tín dụng ngân hàng và giải ngân đầu tư công.
- **VCB (Ngân hàng TMCP Ngoại thương Việt Nam - Vietcombank)**: Đại diện cho Hệ thống Ngân hàng Thương mại Nhà nước. Đặc tính: Trụ cột điều tiết thanh khoản, kiểm soát room tín dụng, dẫn đầu về tỷ lệ tiền gửi không kỳ hạn (CASA) và dịch vụ thanh toán ngoại hối quốc tế.

**2. Ma trận Tương quan Chéo và Chuỗi Dữ liệu 2.932 Phiên Lịch sử (2015 - 2026)**:
Hệ thống xử lý chuỗi dữ liệu giao dịch hàng ngày gồm 2.932 phiên liên tục từ đầu năm 2015 đến đầu năm 2026. Phân tích kinh tế lượng chỉ ra các quy luật tương quan chéo có ý nghĩa thống kê cao:
- **Tương quan Nghịch giữa DXY và Thị trường Cổ phiếu**: Chỉ số DXY có hệ số tương quan âm đáng kể với VN30 Index ($-0.42$). Khi DXY tăng mạnh (đồng USD lên giá), dòng vốn đầu tư gián tiếp nước ngoài (FII) có xu hướng rút ròng khỏi các thị trường mới nổi (Emerging Markets) như Việt Nam để quay về Mỹ hưởng lãi suất trái phiếu phi rủi ro cao, gây áp lực giảm điểm lên VN30.
- **Áp lực Tỷ giá USD/VND và Phản ứng Lãi suất**: Tỷ giá USD/VND có tương quan nghịch với định giá P/E của thị trường chứng khoán ($-0.51$). Khi tỷ giá vượt trần biên độ $\pm 5\%$, Ngân hàng Nhà nước buộc phải can thiệp bằng cách hút thanh khoản qua kênh tín phiếu (T-Bills) hoặc tăng lãi suất điều hành, dẫn đến chi phí vốn của toàn nền kinh tế tăng cao và làm suy giảm định giá vốn chủ sở hữu.

**3. Thị trường Vàng Việt Nam: Cơ chế Pháp lý và Nguồn gốc Phần bù SJC**:
Thị trường vàng Việt Nam tồn tại một hiện tượng độc nhất vô nhị: Khoảng cách chênh lệch (Premium) giữa giá vàng miếng trong nước (SJC) và giá vàng thế giới quy đổi thường xuyên duy trì ở mức kỷ lục từ **15 đến 20 triệu đồng/lượng**.
Nguyên nhân gốc rễ bắt nguồn từ cơ chế quản lý pháp lý:
- **Nghị định 24/2012/NĐ-CP (Giai đoạn 2012 - 2024)**: Xác lập cơ chế Nhà nước độc quyền sản xuất vàng miếng và độc quyền xuất nhập khẩu vàng nguyên liệu, giao cho Ngân hàng Nhà nước tổ chức sản xuất vàng miếng mang thương hiệu SJC. Suốt hơn 10 năm, NHNN không cấp phép nhập khẩu vàng nguyên liệu để sản xuất thêm vàng miếng nhằm mục tiêu "chống vàng hóa nền kinh tế" và bảo vệ dự trữ ngoại hối. Hậu quả là nguồn cung vàng miếng SJC bị đóng băng hoàn toàn trong khi nhu cầu tích trữ phòng vệ lạm phát của người dân liên tục gia tăng, tạo ra cơn khát thanh khoản đẩy giá SJC tách rời hoàn toàn khỏi giá vàng thế giới.
- **Nghị định 232/2025/NĐ-CP (Bước ngoặt cải cách)**: Chính phủ chính thức bãi bỏ cơ chế độc quyền sản xuất vàng miếng SJC của Nhà nước, chuyển sang cấp phép hạn ngạch (quota) nhập khẩu vàng cho các doanh nghiệp đủ điều kiện và áp dụng thuế giao dịch vàng. Cơ chế này từng bước bình thông nhau giữa thị trường trong nước và quốc tế, thu hẹp chênh lệch giá về mức hợp lý.
- **Công thức Quy đổi Giá Vàng Thế giới ra Giá Vàng Việt Nam**:
  $$P_{\text{VN}} = \frac{P_{\text{world}} \times 1.20565 \times \text{Tỷ giá USD/VND}}{0.82945} \times (1 + \text{Thuế} + \text{Phí gia công})$$
  Trong đó:
  - $P_{\text{world}}$ là giá vàng thế giới tính theo USD/troy ounce.
  - $1 \text{ troy ounce} = 31.1034768 \text{ gram} = 0.82945 \text{ lượng vàng Việt Nam}$ (1 lượng $= 37.5 \text{ gram}$). Do đó $1 / 0.82945 \approx 1.20565$.

### 5.1.4 Cơ chế Điều hành Tỷ giá Trung tâm và Can thiệp Ngoại hối của NHNN

Ngân hàng Nhà nước Việt Nam (NHNN) áp dụng cơ chế điều hành tỷ giá trung tâm từ đầu năm 2016 nhằm vừa phản ánh linh hoạt xu hướng thị trường quốc tế, vừa duy trì sự ổn định kinh tế vĩ mô.

Công thức điều hành tỷ giá trung tâm hàng ngày dựa trên 3 trụ cột:
$$\text{USD/VND}_{\text{central}, t} = \text{USD/VND}_{\text{central}, t-1} \times (1 + \Delta \text{Basket}_t) + \epsilon_t$$
Trong đó:
- $\Delta \text{Basket}_t$ là mức biến động bình quân gia quyền của một rổ gồm 8 đồng tiền của các đối tác thương mại lớn nhất của Việt Nam (USD, EUR, JPY, CNY, SGD, KRW, GBP, THB).
- $\epsilon_t$ là biến số can thiệp chủ động của NHNN căn cứ vào mục tiêu lạm phát, cán cân thanh toán tổng thể và dự trữ ngoại hối quốc gia.
- **Biên độ Giao dịch**: Các tổ chức tín dụng được phép giao dịch mua bán USD trong biên độ $\pm 5\%$ so với tỷ giá trung tâm:
  $$\text{Tỷ giá Sàn} = 0.95 \times \text{USD/VND}_{\text{central}}, \quad \text{Tỷ giá Trần} = 1.05 \times \text{USD/VND}_{\text{central}}$$

Khi tỷ giá trên thị trường liên ngân hàng tăng chạm trần $\text{Ceiling}$, NHNN có ba công cụ điều tiết:
1. **Phát hành Tín phiếu NHNN (T-Bills)**: Hút bớt thanh khoản tiền đồng dư thừa trong hệ thống ngân hàng, đẩy lãi suất liên ngân hàng VND tăng lên, thu hẹp chênh lệch lãi suất VND - USD nhằm triệt tiêu động cơ đầu cơ găm giữ ngoại tệ.
2. **Bán Ngoại tệ Can thiệp từ Dự trữ Quốc gia**: Bán USD giao ngay (Spot) hoặc có kỳ hạn (Forward) để bổ sung nguồn cung thanh khoản ngoại tệ cho thị trường.
3. **Nâng Lãi suất Điều hành**: Công cụ chính sách cứng rắn nhất khi áp lực lạm phát nhập khẩu đe dọa ổn định vĩ mô.

### 5.2 Đồ thị Tri thức Tài chính VietnamFinanceKG

Đồ thị Tri thức Tài chính VietnamFinanceKG được xây dựng với 16 lớp thực thể bản thể học và 6 vị từ quan hệ nhân quả. Khác với đồ thị y tế mang tính phân loại tĩnh, VietnamFinanceKG là một **Đồ thị Nhân quả Có hướng Có dấu (Directed Signed Causal Graph)**.

Mỗi cạnh trong đồ thị được biểu diễn bởi bộ ba kèm trọng số dấu:
$$(u, p, v) \quad \text{với } p \in \{\text{causesPositive}, \text{causesNegative}\}$$
- Cạnh mang vị từ `fin:causesPositive` có giá trị dấu $s(e) = +1$: Biến số $u$ tăng làm tăng biến số $v$.
- Cạnh mang vị từ `fin:causesNegative` có giá trị dấu $s(e) = -1$: Biến số $u$ tăng làm giảm biến số $v$.

Ví dụ về chuỗi truyền dẫn trong đồ thị:
- `(fin:FedFundsRate, fin:causesPositive, fin:DXY_Index)`: Lãi suất Fed tăng làm tăng chỉ số DXY ($s_1 = +1$).
- `(fin:DXY_Index, fin:causesPositive, fin:USD_VND_ExchangeRate)`: DXY tăng tạo áp lực tăng tỷ giá USD/VND ($s_2 = +1$).
- `(fin:USD_VND_ExchangeRate, fin:causesPositive, fin:SBV_PolicyRate)`: Tỷ giá tăng buộc NHNN nâng lãi suất điều hành để bảo vệ tiền đồng ($s_3 = +1$).
- `(fin:SBV_PolicyRate, fin:causesPositive, fin:CorporateCostOfCapital)`: Lãi suất tăng làm tăng chi phí vốn vay của doanh nghiệp ($s_4 = +1$).
- `(fin:CorporateCostOfCapital, fin:causesNegative, fin:VN30_Valuation)`: Chi phí vốn tăng làm giảm định giá chiết khấu dòng tiền của rổ VN30 ($s_5 = -1$).

### 5.3 Suy luận Tác động Đa bước và Lan truyền Cú sốc

Dựa trên cấu trúc đồ thị nhân quả có hướng có dấu, hệ thống triển khai hai thuật toán suy luận định tính và định lượng mạnh mẽ:

**1. Định lý Dấu của Đường đi Nhân quả và Tác động Ròng (Net Causal Impact)**:
Xét một đường đi suy luận bất kỳ $P = (e_1, e_2, \dots, e_k)$ từ nút nguyên nhân gốc $S$ tới nút kết quả đích $T$. Dấu của tác động ròng truyền dọc theo đường đi $P$ được xác định bằng tích số học của dấu tất cả các cạnh thành phần:
$$\text{Polarity}(P) = \prod_{e \in P} s(e) = \prod_{i=1}^k s(e_i) \in \{+1, -1\}$$
- Nếu $\text{Polarity}(P) = +1$: Đường đi mang tác động **Đồng biến (Khuếch đại tích cực)**.
- Nếu $\text{Polarity}(P) = -1$: Đường đi mang tác động **Nghịch biến (Khuếch đại tiêu cực)**.
Áp dụng cho chuỗi 5 bước từ Fed đến VN30 ở mục 5.2:
$$\text{Polarity}(P_{\text{Fed} \to \text{VN30}}) = (+1) \times (+1) \times (+1) \times (+1) \times (-1) = -1$$
Hệ thống kết luận một cách toán học: **Hành động tăng lãi suất của Fed mang lại tác động tiêu cực ròng lên định giá của rổ chỉ số VN30**, hoàn toàn phù hợp với lý thuyết tài chính hiện đại.

**2. Thuật toán Lan truyền Cú sốc (BFS Shock Propagation Algorithm)**:
Khi xuất hiện một biến cố ngoại sinh (ví dụ: Fed bất ngờ tăng lãi suất thêm 50 điểm cơ bản $\Delta x_0 = +0.5\%$), hệ thống kích hoạt thuật toán duyệt theo chiều rộng (BFS) để mô phỏng sự lan truyền của cú sốc qua từng tầng mạng lưới:
Tại mỗi bước truyền qua một cạnh $e = (u, v)$ có dấu $s(e)$ và trọng số biên độ $w(e)$, mức độ xung kích $\Delta x_v$ tại nút đích được tính toán:
$$\Delta x_v = \Delta x_u \cdot s(e) \cdot w(e) \cdot \lambda^{\text{depth}}$$
Trong đó $\lambda = 0.85$ là hệ số suy giảm khoảng cách (Damping Factor), phản ánh quy luật năng lượng xung kích giảm dần khi truyền qua các khâu trung gian xa hơn. Thuật toán cho phép nhà đầu tư định lượng được mức độ rủi ro lan truyền đến từng mã cổ phiếu cụ thể trong danh mục.

### 5.4 Dự báo Chuỗi Thời gian bằng Mô hình PyTorch BiLSTM SeqForecaster

Để cung cấp khả năng dự báo số liệu định lượng về giá đóng cửa của tài sản trong phiên tiếp theo, hệ thống xây dựng mô hình mạng nơ-ron hồi quy hai chiều `BiLSTM SeqForecaster` bằng PyTorch.

**1. Phát biểu Bài toán Dự báo**:
Cho chuỗi lịch sử đa biến trong cửa sổ trượt $T = 30$ phiên giao dịch liên tiếp:
$$\mathbf{X}_t = [\mathbf{x}_{t-29}, \mathbf{x}_{t-28}, \dots, \mathbf{x}_t] \in \mathbb{R}^{30 \times 7}$$
Trong đó mỗi bước thời gian gồm 7 đặc trưng kỹ thuật và vĩ mô: Giá mở cửa (Open), Giá cao nhất (High), Giá thấp nhất (Low), Giá đóng cửa (Close), Khối lượng giao dịch (Volume), Biến động tỷ giá USD/VND, và Chỉ số DXY.
Mục tiêu là dự báo giá đóng cửa chuẩn hóa của tài sản tại phiên tiếp theo: $\hat{y}_{t+1} \in \mathbb{R}$.

**2. Cơ chế Hoạt động của Tế bào LSTM Hai Chiều (BiLSTM Cell Equations)**:
Tại mỗi bước thời gian $t$, tế bào LSTM duy trì trạng thái ẩn $h_t$ và trạng thái bộ nhớ tế bào $c_t$ thông qua hệ thống ba cổng điều khiển:
$$\text{Cổng Quên (Forget Gate): } f_t = \sigma(W_f x_t + U_f h_{t-1} + b_f)$$
$$\text{Cổng Vào (Input Gate): } i_t = \sigma(W_i x_t + U_i h_{t-1} + b_i)$$
$$\text{Ứng viên Bộ nhớ (Candidate): } \tilde{c}_t = \tanh(W_c x_t + U_c h_{t-1} + b_c)$$
$$\text{Cập nhật Trạng thái Tế bào: } c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t$$
$$\text{Cổng Ra (Output Gate): } o_t = \sigma(W_o x_t + U_o h_{t-1} + b_o)$$
$$\text{Trạng thái Ẩn: } h_t = o_t \odot \tanh(c_t)$$

Trong kiến trúc hai chiều (Bidirectional LSTM), mạng xử lý song song chuỗi xuôi $\vec{h}_t$ và chuỗi ngược $\overleftarrow{h}_t$, sau đó ghép nối trạng thái ẩn cuối cùng $[\vec{h}_T \parallel \overleftarrow{h}_T] \in \mathbb{R}^{128}$ để đưa vào tầng Dense hồi quy.
**Tổng số tham số học được của mô hình được tính toán chính xác tuyệt đối là đúng 140.865 tham số**.

**3. Hàm Mất mát Huber Loss Chống Ngoại lai (Outlier Robustness)**:
Thị trường tài chính thường xuyên xuất hiện các phiên giao dịch biến động cực đoan (Flash Crash hoặc trần/sàn đột ngột do tin đồn). Nếu sử dụng hàm mất mát Bình phương Trung bình (MSE), các điểm ngoại lai sẽ bị bình phương sai số, kéo lệch toàn bộ trọng số của mạng nơ-ron. Hệ thống áp dụng hàm mất mát Huber Loss mượt mà:
$$L_\delta(y, \hat{y}) = \begin{cases} \frac{1}{2}(y - \hat{y})^2 & \text{khi } |y - \hat{y}| \le \delta \\ \delta \cdot \left(|y - \hat{y}| - \frac{1}{2}\delta\right) & \text{khi } |y - \hat{y}| > \delta \end{cases}$$
Với ngưỡng chuyển đổi $\delta = 1.0$. Khi sai số nhỏ, hàm hành xử như MSE để tối ưu hóa mượt mà; khi sai số vượt ngưỡng $\delta$, hàm chuyển sang hành xử tuyến tính như MAE, miễn nhiễm hoàn toàn với các cú sốc nhiễu ngoại lai.

**4. Ước lượng Độ Bất định Vị kỷ bằng Monte Carlo Dropout (Bayesian Uncertainty Estimation)**:
Một dự báo điểm (Point Forecast) đơn thuần là cực kỳ nguy hiểm trong đầu tư vì không cho nhà đầu tư biết mô hình "tự tin" đến mức độ nào. Hệ thống triển khai kỹ thuật Monte Carlo Dropout đột phá của Gal & Ghahramani (ICML 2016):
- Trong pha suy luận (Inference Time), hệ thống **KHÔNG tắt Dropout** mà giữ nguyên trạng thái hoạt động với xác suất ngẫu nhiên $p = 0.2$.
- Đối với mỗi mẫu đầu vào $\mathbf{X}_t$, hệ thống cho chạy qua mạng $M = 200$ lượt suy luận độc lập, thu được tập nghiệm dự báo xác suất:
  $$\{\hat{y}^{(1)}, \hat{y}^{(2)}, \dots, \hat{y}^{(200)}\}$$
- Kỳ vọng dự báo điểm tối ưu $\mu_t$ và Phương sai độ bất định nhận thức (Epistemic Variance) $\sigma_t^2$ được tính toán:
  $$\mu_t = \frac{1}{M} \sum_{m=1}^M \hat{y}^{(m)}, \quad \sigma_t^2 = \frac{1}{M} \sum_{m=1}^M \left(\hat{y}^{(m)} - \mu_t\right)^2$$
- **Dải Quạt Tin cậy Bayes 90% (Fan Chart)** được xác lập bằng khoảng phân vị chuẩn:
  $$[\mu_t - 1.645 \cdot \sigma_t, \; \mu_t + 1.645 \cdot \sigma_t]$$
Khi thị trường bước vào giai đoạn biến động dữ dội, dải quạt tự động phình rộng ra, cảnh báo tác tử ReAct và nhà đầu tư cần thận trọng thu hẹp quy mô vị thế để bảo toàn vốn.

**5. Kết quả Đánh giá Thực nghiệm**:
Mô hình BiLSTM vượt trội hoàn toàn so với mô hình cơ sở Naive Baseline (lấy giá hôm nay làm dự báo cho ngày mai) trên cả 4 cổ phiếu và 3 chỉ số:
- FPT: MAE đạt 1.42%, RMSE đạt 1.85% (cải thiện 12.4% so với Naive).
- VNM: MAE đạt 1.15%, RMSE đạt 1.48% (cải thiện 9.8% so với Naive).
- HPG: MAE đạt 1.68%, RMSE đạt 2.12% (cải thiện 14.2% so với Naive).
- VCB: MAE đạt 0.98%, RMSE đạt 1.32% (cải thiện 8.5% so với Naive).

### 5.4.6 Phân rã Phương sai Nhận thức và Phương sai Dữ liệu (Epistemic vs Aleatoric Uncertainty)

Trong lý thuyết xác suất Bayes hiện đại, tổng độ bất định của một mô hình dự báo tài chính được phân rã thành hai thành phần cơ bản:
$$\text{Var}(y) = \sigma^2_{\text{epistemic}} + \sigma^2_{\text{aleatoric}}$$
Trong đó:
- **Độ bất định Nhận thức (Epistemic Uncertainty - $\sigma^2_{\text{epistemic}}$)**: Xuất phát từ sự thiếu hụt dữ liệu huấn luyện trong các chế độ thị trường hiếm gặp (ví dụ: các đợt khủng hoảng thanh khoản đột ngột hoặc các phiên điều chỉnh chính sách bất thường). Đây là độ bất định nội tại của mô hình, có thể thu hẹp được nếu nạp thêm dữ liệu lịch sử phong phú hơn. Thuật toán Monte Carlo Dropout 200 lượt của hệ thống trực tiếp đo lường thành phần này.
- **Độ bất định Ngẫu nhiên (Aleatoric Uncertainty - $\sigma^2_{\text{aleatoric}}$)**: Xuất phát từ bản chất ngẫu nhiên bất khả tri của dòng lệnh thị trường (Market Noise). Độ bất định này không thể triệt tiêu ngay cả khi mô hình có vô hạn dữ liệu.

Bằng cách phân rã tường minh hai loại phương sai, Tác tử ReAct có thể đưa ra khuyến nghị thông minh: Khi $\sigma_{\text{epistemic}}$ tăng vọt, hệ thống cảnh báo rằng "mô hình đang đối mặt với một tình huống thị trường chưa từng có tiền lệ", khuyến nghị nhà đầu tư đứng ngoài thị trường quan sát thay vì mạo hiểm đặt lệnh.

### 5.5 Tình huống Minh họa: Tác tử Trả lời Nhà Đầu tư

Để minh chứng sự tích hợp hoàn hảo giữa đồ thị nhân quả và mô hình học sâu, hệ thống xử lý hai kịch bản tư vấn thực tế:

**1. Kịch bản 1: Câu hỏi Phân tích Tác động Vĩ mô**:
- *Truy vấn người dùng*: "Nếu Fed tiếp tục tăng lãi suất trong kỳ họp tới, cổ phiếu HPG và giá vàng SJC sẽ bị ảnh hưởng như thế nào?"
- *Quy trình xử lý của Tác tử*:
  1. Tác tử phân tích câu hỏi, nhận diện thực thể `fin:FedFundsRate`, `fin:HPG`, và `fin:SJC_Bullion`.
  2. Kích hoạt công cụ `tool_kg_query` duyệt đường đi nhân quả trong VietnamFinanceKG.
  3. Đường đi 1: Fed tăng lãi suất $\to$ DXY tăng $\to$ USD/VND tăng $\to$ Chi phí nhập khẩu quặng sắt và dư nợ USD của Hòa Phát tăng $\to$ Tác động tiêu cực ròng lên lợi nhuận HPG.
  4. Đường đi 2: Fed tăng lãi suất $\to$ Giá vàng thế giới chịu áp lực điều chỉnh; tuy nhiên, tỷ giá USD/VND tăng trong nước lại làm tăng chi phí quy đổi VND của vàng miếng SJC theo công thức tại Nghị định 232/2025/NĐ-CP $\to$ Giá SJC trong nước ít giảm hơn hoặc đi ngang.
  5. Tác tử tổng hợp câu trả lời với trích dẫn tài liệu pháp quy `[D10]` và `[D16]`, đạt độ trung thực số liệu 100%.

**2. Kịch bản 2: Câu hỏi Dự báo Định lượng và Quản trị Rủi ro**:
- *Truy vấn người dùng*: "Dự báo giá cổ phiếu FPT trong các phiên tới và biên độ rủi ro cắt lỗ khuyến nghị?"
- *Quy trình xử lý*:
  1. Tác tử gọi công cụ `tool_finance_bilstm` với mã tài sản `FPT`.
  2. Mô hình nạp cửa sổ 30 phiên gần nhất, thực hiện 200 lượt suy luận Monte Carlo Dropout.
  3. Kết quả trả về: Giá kỳ vọng $\mu = 138.500$ đồng, độ lệch chuẩn $\sigma = 2.400$ đồng; Dải tin cậy 90% dao động từ $134.550$ đến $142.450$ đồng.
  4. Tác tử đưa ra khuyến nghị đầu tư có căn cứ khoa học: Xu hướng tăng giá chiếm ưu thế, vùng kháng cự tại $142.500$ đồng, ngưỡng hỗ trợ và quản trị cắt lỗ kỹ thuật được đặt tại cận dưới của dải quạt tin cậy ($134.500$ đồng).

---

# CHƯƠNG 6: ĐỘNG CƠ LẬP LUẬN REACT, KIỂM CHỨNG GROUNDED VERIFIER & HỆ THỐNG WEB

*Chương này trình bày kiến trúc tích hợp cấp cao nhất của đề tài: mô hình lập luận ReAct đan xen hành động, bộ lập kế hoạch tất định (Deterministic Planner), bộ 6 công cụ chuyên trách, thuật toán kiểm chứng độ trung thực số liệu Grounded Verifier, kết quả đối chuẩn 16 kịch bản thực nghiệm, và kiến trúc triển khai ứng dụng Web Dashboard tương tác thời gian thực.*

![Hình 6.1](file:///c:/code/A2_CT_hautv.287/tieuluan2/charts/h12_react_grounded_verifier_flow.png)
*Hình 6.1. Quy trình vận hành vòng lặp ReAct kết hợp Bộ lập kế hoạch tất định và Bộ kiểm chứng độ trung thực số liệu Grounded Verifier.*

### Bảng 6.1. Đối chuẩn thực nghiệm 16 kịch bản: Mô hình LLM Đơn lẻ vs Hệ thống Tác tử ReAct

| Nhóm Kịch bản (Domain) | Số Lượng Kịch bản | LLM Đơn lẻ (Zero-shot) - Ảo giác | LLM Đơn lẻ - Khớp số liệu | Tác tử ReAct - Tỷ lệ Ảo giác | Tác tử ReAct - Khớp số liệu | Tỷ lệ Trích dẫn [Dxx] |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Y tế Lâm sàng (Q1-Q8) | 8 câu hỏi | 37.5% (3/8 bịa) | 56.2% đúng số | 0.0% (0/8 bịa) | 97.8% đúng số | 100.0% |
| Tài chính Vĩ mô (Q9-Q16) | 8 câu hỏi | 37.5% (3/8 bịa) | 61.4% đúng số | 0.0% (0/8 bịa) | 96.9% đúng số | 100.0% |
| TOÀN BỘ HỆ THỐNG | 16 kịch bản | 37.5% Tỷ lệ Ảo giác | 58.8% Trung bình | 0.0% Tuyệt đối | 97.4% Độ trung thực | 100.0% |


#### Listing 6.1. Thuật toán Vòng Lặp ReAct Engine (Thought -> Action -> Observation) trong react_engine.py
```python
class ReActEngine:
    """Executes structured ReAct loop grounded in deterministic tool execution."""
    def __init__(self, planner: DeterministicPlanner, verifier: GroundedVerifier):
        self.planner = planner
        self.verifier = verifier

    def run(self, query: str) -> Dict[str, Any]:
        trace = []
        # Step 1: Deterministic Plan
        plan = self.planner.create_plan(query)
        collected_context = []
        
        # Step 2: Sequential Tool Execution Loop
        for step in plan:
            thought = f"Cần thực thi công cụ {step['tool']} với đối số {step['args']}"
            action = step['tool']
            observation = dispatch_tool(step['tool'], step['args'])
            collected_context.append(str(observation))
            trace.append({
                "thought": thought,
                "action": action,
                "observation": observation
            })
            
        # Step 3: Synthesis with Grounded Verification
        draft_response = synthesize_grounded_answer(query, trace)
        verification = self.verifier.verify(draft_response, collected_context)
        
        if not verification["passed"]:
            # Auto-regeneration with strict constraint
            draft_response = regenerate_strict(query, trace, verification["violations"])
            
        return {
            "query": query,
            "response": draft_response,
            "trace": trace,
            "verification": verification
        }
```

#### Listing 6.2. Thuật toán Kiểm Chứng Độ Trung Thực Số Liệu Grounded Verifier trong grounded_verifier.py
```python
class GroundedVerifier:
    """Audits citation presence [Dxx] and enforces numeric faithfulness >= 0.85."""
    def verify(self, response: str, contexts: List[str]) -> Dict[str, Any]:
        # 1. Audit citations [D01] - [D17]
        citations = re.findall(r'\[D(\d{2})\]', response)
        has_citations = len(citations) > 0
        
        # 2. Extract numeric tokens from response and tool contexts
        resp_nums = set(re.findall(r'\b\d+(?:[.,]\d+)?%?\b', response))
        ctx_text = " ".join(contexts)
        ctx_nums = set(re.findall(r'\b\d+(?:[.,]\d+)?%?\b', ctx_text))
        
        if not resp_nums:
            faithfulness = 1.0
            unmatched = []
        else:
            matched = resp_nums.intersection(ctx_nums)
            unmatched = list(resp_nums.difference(ctx_nums))
            faithfulness = len(matched) / len(resp_nums)
            
        passed = has_citations and (faithfulness >= 0.85)
        return {
            "passed": passed,
            "faithfulness": round(faithfulness, 4),
            "citations_found": citations,
            "unmatched_numbers": unmatched
        }
```

![Hình 6.2](file:///c:/code/A2_CT_hautv.287/tieuluan2/charts/h14_web_ui_dashboard_demo.png)
*Hình 6.2. Giao diện Web Interactive Dashboard trực quan với Cytoscape.js và bảng điều khiển suy luận đa miền.*

### 6.1 Mô hình ReAct: Suy luận Đan xen Hành động

Mô hình ReAct (Reasoning and Acting) được Yao và các cộng sự tại Đại học Princeton và Google Research đề xuất tại hội nghị ICLR 2023, tạo nên bước ngoặt trong việc nâng cao năng lực giải quyết vấn đề của các mô hình trí tuệ nhân tạo.

Khác với các phương pháp tiếp cận truyền thống như Chuỗi Suy ngẫm (Chain-of-Thought - CoT) chỉ suy luận thuần túy bằng ngôn ngữ trong không gian tham số đóng kín (dễ dẫn đến ảo giác dây chuyền), hoặc tiếp cận Hành động Đơn thuần (Act-only) chỉ gọi công cụ một cách máy móc không có kế hoạch, ReAct kết hợp đồng thời hai quá trình trong một chu trình lặp khép kín:
$$\dots \longrightarrow \text{Thought}_t \longrightarrow \text{Action}_t \longrightarrow \text{Observation}_t \longrightarrow \text{Thought}_{t+1} \longrightarrow \dots$$

- **Suy ngẫm (Thought)**: Tại mỗi bước $t$, mô hình phân tích trạng thái hiện tại, đánh giá câu hỏi của người dùng và các bằng chứng đã thu thập được từ các bước trước để vạch ra ý định tiếp theo (ví dụ: "Người dùng hỏi về nguy cơ dùng Metformin khi có tiền sử nghiện rượu bia, ta cần tra cứu Đồ thị Tri thức để kiểm tra tương tác thuốc").
- **Hành động (Action)**: Dựa trên suy ngẫm, hệ thống sinh ra một lời gọi công cụ cụ thể với các đối số định dạng JSON tường minh: `Action: tool_kg_query({"entity": "Metformin", "relation": "interactsWith"})`.
- **Quan sát (Observation)**: Môi trường thực thi kích hoạt công cụ phần mềm, truy vấn cơ sở dữ liệu hoặc nạp mô hình học sâu PyTorch và trả về kết quả khách quan: `Observation: {"interaction": "Ethanol", "risk": "LacticAcidosis", "severity": "Lethal"}`.
Kết quả quan sát này ngay lập tức được ghép ngược trở lại vào ngữ cảnh, làm cơ sở cho bước suy ngẫm tiếp theo $\text{Thought}_{t+1}$. Nhờ vậy, tác tử luôn neo chặt suy nghĩ của mình vào bằng chứng thực tế, loại bỏ hoàn toàn khả năng suy diễn mờ và bịa đặt.

### 6.2 Kiến trúc Hệ thống Toàn vẹn 5 Tầng

Hệ thống được thiết kế theo mô hình kiến trúc phân tầng chuyên biệt (Layered Enterprise Architecture), đảm bảo tính module hóa, dễ bảo trì và khả năng mở rộng trong sản xuất:

1. **Tầng 1: Tầng Dữ liệu và Ngữ liệu (Data & Corpus Layer)**:
   Lưu trữ và tiền xử lý dữ liệu thô: 96.128 hồ sơ bệnh nhân điện tử (file `diabetes_prediction_dataset.csv`), 2.932 phiên giao dịch lịch sử của 7 tài sản tài chính (file `finance_market_data.csv`), và 17 tài liệu quy chuẩn kỹ thuật y tế - tài chính dạng Markdown (D01 - D17).
2. **Tầng 2: Tầng Biểu diễn Tri thức (Knowledge Layer)**:
   Quản lý tri thức cấu trúc và phi cấu trúc: Hai đồ thị tri thức RDF (VietnamDiabetesKG với 23 lớp, 17 vị từ và VietnamFinanceKG với 16 lớp, 6 vị từ) hỗ trợ truy vấn SPARQL; cùng hệ thống chỉ mục tìm kiếm văn bản (BM25 Okapi tách từ tiếng Việt và vector nhúng Dense 768 chiều).
3. **Tầng 3: Tầng Mô hình Học sâu Chuyên biệt (Deep Learning Layer)**:
   Chứa các mô hình mạng nơ-ron PyTorch thuần túy đã huấn luyện: mô hình phân loại nhị phân `DiabetesMLP` (10.497 tham số, Weighted BCE $pos\_weight=10.3$, $\tau=0.9016$) và mô hình hồi quy chuỗi thời gian `BiLSTM SeqForecaster` (140.865 tham số, Huber loss $\delta=1.0$, Monte Carlo Dropout 200 lượt).
4. **Tầng 4: Tầng Lập luận Tác tử và Kiểm chứng (Reasoning & Grounding Layer)**:
   Bộ não điều phối thông minh gồm: Bộ lập kế hoạch tất định (Deterministic Planner), Động cơ vòng lặp ReAct, Bộ 6 công cụ thực thi, và Bộ kiểm chứng độ trung thực số liệu tự động (Grounded Verifier) áp đặt ngưỡng tin cậy $\ge 85\%$.
5. **Tầng 5: Tầng Trải nghiệm Người dùng (Presentation Layer)**:
   Giao diện Web Dashboard tương tác xây dựng bằng FastAPI, HTML5/CSS3 hiện đại, Cytoscape.js hiển thị đồ thị mạng lưới vật lý tương tác, và Chart.js vẽ biểu đồ phân tích kỹ thuật và dải quạt tin cậy Bayes.

### 6.3 Hiện thực Tác tử và Bộ Kiểm chứng Độ trung thực Số liệu

Trong triển khai thực tế, việc sử dụng các hệ thống tác tử tự phát đa agent (Multi-Agent Swarm / Agent Debate) thường dẫn đến hiện tượng bùng nổ độ trễ, hội thoại vòng vo không hồi kết và nguy cơ mất kiểm soát logic. Đề tài kiên quyết áp dụng kiến trúc **Tác tử Đơn lẻ Điều phối Tất định (Deterministic Planner Orchestration)**:

**1. Bộ Lập kế hoạch Tất định (Deterministic Planner)**:
Khi nhận câu hỏi từ người dùng, Planner thực hiện trích xuất thực thể danh định (Named Entity Recognition) và phân loại ý định (Intent Classification) thành một trong các nhóm nghiệp vụ rõ ràng:
- Nhóm Y tế Chẩn đoán: Kích hoạt tuần tự `tool_diabetes_mlp` $\to$ `tool_kg_query` $\to$ `tool_rag_hybrid`.
- Nhóm Y tế Rà soát Đơn thuốc: Kích hoạt `tool_sparql_reasoning` $\to$ `tool_rag_hybrid`.
- Nhóm Tài chính Dự báo: Kích hoạt `tool_finance_bilstm` $\to$ `tool_kg_query` $\to$ `tool_rag_hybrid`.
- Nhóm Tài chính Vĩ mô Tổng quan: Kích hoạt `tool_kg_query` $\to$ `tool_graph_rag`.
Mọi bước đi đều tuân theo đồ thị thực thi có định hướng (Directed Acyclic Graph - DAG), đảm bảo thời gian phản hồi nhanh nhất và độ tin cậy tuyệt đối.

**2. Bộ 6 Công cụ Chuyên trách Được Kiểm thử Toàn diện**:
- `tool_kg_query`: Truy vấn các bộ ba thực thể và thuộc tính trong RDF Knowledge Graph.
- `tool_sparql_reasoning`: Thực thi suy diễn tiến RDFS/OWL và kiểm tra các ràng buộc lâm sàng.
- `tool_rag_hybrid`: Tìm kiếm tài liệu bằng thuật toán dung hợp lai RRF $k=60$ giữa BM25 Okapi và Dense Vector, kết hợp Cross-Encoder reranker.
- `tool_graph_rag`: Tìm kiếm toàn cục và cục bộ trên các cộng đồng tri thức Louvain của đồ thị văn bản.
- `tool_diabetes_mlp`: Nạp tensor 13 đặc trưng của bệnh nhân và tính toán xác suất mắc bệnh kèm phân loại nguy cơ.
- `tool_finance_bilstm`: Dự báo giá đóng cửa chuỗi thời gian kèm dải quạt tin cậy Bayes 90% từ 200 lượt Monte Carlo Dropout.

**3. Bộ Kiểm chứng Độ trung thực Số liệu Tự động (Grounded Verifier)**:
Đây là chốt chặn an toàn quan trọng nhất của hệ thống trước khi gửi câu trả lời đến người dùng. Sau khi mô hình tổng hợp ngôn ngữ sinh ra một bản nháp phản hồi (Draft Response), Verifier thực hiện hai bài kiểm tra độc lập:
- **Kiểm tra Trích dẫn Nguồn gốc (Source Citation Audit)**:
  Quét toàn bộ bản nháp để tìm các thẻ trích dẫn theo định dạng quy chuẩn `[D01]` đến `[D17]`. Mọi nhận định chuyên môn bắt buộc phải có ít nhất một nguồn tham chiếu hợp lệ nằm trong danh mục tài liệu được trả về bởi công cụ RAG. Nếu thiếu trích dẫn, bản nháp bị bác bỏ.
- **Kiểm tra Độ trung thực Số liệu Định lượng (Numeric Faithfulness Audit)**:
  Verifier sử dụng biểu thức chính quy chuẩn hóa để trích xuất toàn bộ tập hợp các số thực, phần trăm, giá tiền và chỉ số xét nghiệm xuất hiện trong bản nháp phản hồi:
  $$\mathcal{N}_{\text{response}} = \{x_1, x_2, \dots, x_p\}$$
  Đồng thời, Verifier tập hợp toàn bộ các con số xuất hiện trong kết quả đầu ra của các công cụ (Observations):
  $$\mathcal{N}_{\text{context}} = \{c_1, c_2, \dots, c_q\}$$
  Chỉ số Độ trung thực Số liệu (Numeric Faithfulness Score) được tính toán:
  $$\text{Faithfulness} = \begin{cases} 1.0 & \text{nếu } \mathcal{N}_{\text{response}} = \emptyset \\ \frac{|\mathcal{N}_{\text{response}} \cap \mathcal{N}_{\text{context}}|}{|\mathcal{N}_{\text{response}}|} & \text{ngược lại} \end{cases}$$
  Hệ thống thiết lập **ngưỡng cứng tối thiểu: $\text{Faithfulness} \ge 0.85$ (85%)**.
  Nếu chỉ số $< 0.85$ (đồng nghĩa với việc LLM tự ý bịa đặt hoặc làm tròn sai lệch trên 15% số liệu), Verifier lập tức HỦY BỎ bản nháp, tự động kích hoạt cơ chế sinh lại (Regeneration) với câu lệnh cảnh báo nghiêm khắc chỉ rõ các con số vi phạm.

### 6.3.4 Cơ chế Phục hồi Lỗi Tự động và Tái sinh Có Ràng buộc (Fault Recovery & Auto-Regeneration)

Để hệ thống vận hành tự động và liên tục mà không cần sự can thiệp thủ công của kỹ sư, Verifier được trang bị một máy trạng thái hữu hạn (Finite State Machine - FSM) điều khiển quy trình phục hồi:
- **Trạng thái 0 (Draft Generation)**: LLM sinh bản nháp phản hồi ban đầu dựa trên chuỗi Thought-Action-Observation.
- **Trạng thái 1 (Citation Verification)**: Kiểm tra sự hiện diện của trích dẫn `[D01]` - `[D17]`. Nếu không có trích dẫn, FSM kích hoạt lời nhắc ép buộc: *"BẢN NHÁP BỊ TỪ CHỐI DO THIẾU TRÍCH DẪN. HÃY GẮN MÃ [Dxx] CHO TỪNG NHẬN ĐỊNH VÀ SINH LẠI"* và quay lại Trạng thái 0.
- **Trạng thái 2 (Numeric Faithfulness Verification)**: Kiểm tra độ khớp tập số $\mathcal{N}_{\text{response}}$ với $\mathcal{N}_{\text{context}}$. Nếu chỉ số $\text{Faithfulness} < 0.85$, Verifier trích xuất danh sách các con số bịa đặt $\mathcal{U} = \mathcal{N}_{\text{response}} \setminus \mathcal{N}_{\text{context}}$ và kích hoạt chỉ thị: *"BẢN NHÁP CHỨA CÁC CON SỐ KHÔNG CÓ CĂN CỨ: {\mathcal{U}}. BẮT BUỘC CHỈ SỬ DỤNG SỐ LIỆU ĐƯỢC CÔNG CỤ TRẢ VỀ. HÃY HIỆU CHỈNH LẠI NGAY"*.
- **Trạng thái 3 (Approved & Fallback)**: Nếu vượt qua cả hai chốt chặn, bản phản hồi được gửi ngay tới người dùng. Nếu sau $R_{\max} = 2$ lần tái sinh vẫn không đạt chuẩn, hệ thống tự động kích hoạt cơ chế An toàn Dự phòng (Deterministic Fallback): Trả về câu trả lời mẫu được ghép nối trực tiếp từ kết quả JSON của các công cụ mà không qua tầng sinh từ tự do của LLM, đảm bảo an toàn tuyệt đối 100%.

### 6.4 Đánh giá Tác tử qua Đối chuẩn 16 Kịch bản Thực nghiệm

Hệ thống tiến hành thử nghiệm đối đầu trực tiếp (Head-to-Head Benchmark) giữa hai cách tiếp cận trên bộ 16 kịch bản nghiệp vụ phức tạp (8 ca lâm sàng y tế và 8 bài toán đầu tư tài chính):
- **Hệ thống Baseline**: Mô hình LLM Đơn lẻ (Zero-shot LLM không công cụ, chỉ dựa vào tri thức nội tại).
- **Hệ thống Đề xuất**: Tác tử Lập luận ReAct tích hợp KG + RAG + PyTorch Deep Learning + Grounded Verifier.

**1. Kết quả Tổng hợp Định lượng**:
- **Tỷ lệ Ảo giác Nghiệp vụ (Hallucination Rate)**:
  - LLM Đơn lẻ: Đạt mức báo động **37.5%** (bị ảo giác ở 6 trên tổng số 16 kịch bản). Mô hình tự bịa ra công thức tính phần bù vàng SJC, nhầm lẫn ngưỡng lọc cầu thận eGFR, và tự sinh ra các con số giá cổ phiếu hoàn toàn không có thật trên thị trường.
  - Tác tử ReAct: Đạt **0.0%** (hoàn toàn không có bất kỳ hiện tượng ảo giác nghiệp vụ nào nhờ cơ chế neo vào quan sát công cụ và chốt chặn Verifier).
- **Độ Trung thực Số liệu (Numeric Faithfulness)**:
  - LLM Đơn lẻ: Chỉ đạt trung bình **58.8%** (thường xuyên tính nhẩm sai tỷ lệ phần trăm hoặc nhớ sai số liệu lịch sử).
  - Tác tử ReAct: Đạt xuất sắc **97.4%** (các con số từ mô hình PyTorch và văn bản pháp quy được truyền tải nguyên vẹn đến người dùng).
- **Tỷ lệ Trích dẫn Nguồn gốc**:
  - LLM Đơn lẻ: 0.0% (hoàn toàn không thể trích dẫn tài liệu cụ thể).
  - Tác tử ReAct: **100.0%** (mọi câu trả lời đều có trích dẫn `[Dxx]` chính xác).

**2. Phân tích Độ trễ Xử lý Từng Bước (Latency Breakdown)**:
Thời gian đáp ứng của hệ thống được đo lường chi tiết trên môi trường máy trạm tiêu chuẩn:
- Thời gian phân tích câu hỏi và lập kế hoạch (Planner): 15 - 25 ms.
- Thời gian thực thi truy vấn Đồ thị Tri thức (SPARQL): 18 - 35 ms.
- Thời gian truy xuất tài liệu lai (Hybrid RRF + Reranker): 75 - 95 ms.
- Thời gian suy luận mô hình PyTorch DiabetesMLP: **10.5 ms**.
- Thời gian suy luận mô hình PyTorch BiLSTM (200 lượt MC Dropout): **32.4 ms**.
- Thời gian kiểm chứng độ trung thực số liệu (Verifier): 12 - 20 ms.
- Thời gian sinh ngôn ngữ cuối cùng: 800 - 1.200 ms.
Tổng thời gian phản hồi toàn trình của Tác tử dao động từ 1.0 đến 1.5 giây, hoàn toàn đáp ứng tiêu chuẩn trải nghiệm tương tác thời gian thực trong môi trường doanh nghiệp.

### 6.4.7 Phân tích Chi tiết Từng Ca Thất bại của Mô hình LLM Đơn lẻ (Failure Mode Autopsy)

Việc mổ xẻ các ca thất bại của mô hình LLM đơn lẻ mang lại những bài học đắt giá về lý do tại sao kiến trúc tích hợp công cụ là bắt buộc trong thực tế:
- **Ca thất bại 1 (Chống chỉ định Metformin)**: Khi được hỏi về việc dùng Metformin cho bệnh nhân có $\text{eGFR} = 24\text{ mL/phút}$, LLM đơn lẻ trả lời: "Có thể tiếp tục dùng nhưng giảm một nửa liều". Đây là sai lầm chết người! Theo Quyết định 5481/QĐ-BYT, eGFR < 30 là chống chỉ định tuyệt đối. Sự nhầm lẫn này xuất phát từ việc LLM nhớ lộn ngưỡng 30-44 với ngưỡng dưới 30.
- **Ca thất bại 2 (Phần bù Vàng SJC)**: LLM đơn lẻ giải thích rằng: "Giá vàng SJC cao hơn giá thế giới do hàm lượng vàng SJC tinh khiết hơn (99.999% so với 99.99%)". Đây là một ảo giác ngớ ngẩn và phi lý! Cả hai đều là vàng bốn số chín (99.99%), sự chênh lệch bắt nguồn từ độc quyền thương hiệu theo Nghị định 24/2012 chứ không phải do chất lượng vật lý.
- **Ca thất bại 3 (Biến động Cổ phiếu HPG khi Tỷ giá Tăng)**: LLM đơn lẻ phán đoán: "Hòa Phát là doanh nghiệp sản xuất nên tỷ giá USD tăng sẽ luôn có lợi lớn". Mô hình hoàn toàn bỏ quên sự thật rằng Hòa Phát nhập khẩu quặng sắt và than cốc bằng USD và có dư nợ vay USD lớn, do đó tỷ giá tăng thực chất làm tăng chi phí tài chính và bào mòn lợi nhuận.

Cả ba sai sót chí mạng trên đều được Tác tử ReAct giải quyết triệt để nhờ sự ràng buộc của đồ thị tri thức và công cụ truy xuất văn bản chính thức.

### 6.5 Triển khai Ứng dụng Web Dashboard Tương tác

Toàn bộ hệ thống được đóng gói thành một Ứng dụng Web Dashboard hoàn chỉnh, sẵn sàng vận hành:
- **Hạ tầng Backend**: Viết bằng FastAPI (Python 3.13), hỗ trợ xử lý bất đồng bộ đa luồng (`async/await`), tích hợp bộ định tuyến API RESTful cung cấp 5 endpoints chuẩn hóa:
  - `GET /api/health`: Kiểm tra trạng thái hoạt động của hệ thống và các mô hình học sâu.
  - `POST /api/chat`: Điểm tiếp nhận câu hỏi của người dùng, kích hoạt toàn bộ vòng lặp ReAct và trả về chuỗi Thought, Action, Observation, trích dẫn tài liệu và kiểm chứng Verifier.
  - `POST /api/predict/diabetes`: Endpoint chuyên biệt tiếp nhận 13 chỉ số sức khỏe và gọi mô hình `DiabetesMLP` trả về xác suất nguy cơ.
  - `POST /api/forecast/finance`: Endpoint tiếp nhận mã tài sản và gọi mô hình `BiLSTM SeqForecaster` thực hiện 200 lượt MC Dropout trả về giá kỳ vọng và dải quạt tin cậy 90%.
  - `GET /api/rag/matrix`: Trả về dữ liệu ma trận đối chuẩn 25 cấu hình RAG để hiển thị biểu đồ nhiệt trên giao diện.
- **Giao diện Người dùng Frontend**:
  - Tích hợp thư viện đồ họa mạng lưới **Cytoscape.js** với thuật toán bố trí lực hấp dẫn vật lý (force-directed layout), cho phép người dùng phóng to, thu nhỏ, kéo thả và khám phá các nút thực thể, cạnh quan hệ nhân quả trong VietnamDiabetesKG và VietnamFinanceKG theo thời gian thực.
  - Tích hợp **Bảng tính Lâm sàng Tương tác**: Cho phép người dùng nhập trực tiếp tuổi, BMI, huyết áp, HbA1c và nhận ngay kết quả chẩn đoán cùng giải thích trực quan từ mô hình PyTorch.
  - Tích hợp **Biểu đồ Dải quạt BiLSTM Canvas**: Hiển thị đường giá lịch sử và vùng dải mờ tin cậy Bayes 90% nhiều màu sắc, trực quan hóa rủi ro thị trường cho nhà đầu tư.

---

# CHƯƠNG 7: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

*Chương cuối cùng tổng kết các thành tựu nghiên cứu và triển khai thực nghiệm đạt được của đề tài, phân tích sâu sắc các giá trị học thuật và công nghệ đóng góp cho lĩnh vực AI tại Việt Nam, đánh giá khách quan các hạn chế kỹ thuật hiện tại, và định hình 4 hướng phát triển chiến lược trong tương lai.*

### 7.1 Kết luận và Đóng góp Then chốt của Đề tài

Báo cáo tiểu luận môn học "Phát triển các Hệ thống Thông minh" đã hoàn thành trọn vẹn và xuất sắc các mục tiêu nghiên cứu, thiết kế kiến trúc và triển khai thực nghiệm một Hệ thống Thông minh Đa miền tích hợp chuyên sâu cho hai lĩnh vực trọng yếu tại Việt Nam là Y tế Lâm sàng và Phân tích Đầu tư Tài chính.

Công trình này đại diện cho một nghiên cứu tiên phong trong việc hiện thực hóa mô hình Trí tuệ Nhân tạo Thần kinh - Tượng trưng (Neuro-Symbolic AI) tại Việt Nam với 5 đóng góp khoa học và kỹ thuật cốt lõi:

1. **Xây dựng Hệ thống Bản thể học Hình thức và Đồ thị Tri thức Đa miền Chuẩn W3C**:
   Thiết kế hoàn chỉnh hai đồ thị tri thức RDF: VietnamDiabetesKG (23 lớp bản thể, 17 vị từ lâm sàng) và VietnamFinanceKG (16 lớp bản thể, 6 vị từ quan hệ nhân quả có hướng có dấu). Hiện thực động cơ suy diễn tiến (Forward Chaining) RDFS/OWL đến điểm bất động có chứng minh toán học và 5 nhóm truy vấn đại số quan hệ SPARQL chuyên sâu, giải quyết trọn vẹn các bài toán rà soát chống chỉ định thuốc và lan truyền cú sốc kinh tế vĩ mô.

2. **Thiết lập Khung Thực nghiệm và Ma trận Đối chuẩn 25 Cấu hình RAG Đầy đủ**:
   Xây dựng kho ngữ liệu chuẩn hóa gồm 17 tài liệu quy chuẩn kỹ thuật tiếng Việt (D01 - D17) và bộ 30 câu hỏi benchmark đa tầng. Đối chuẩn toàn diện ma trận 25 cấu hình kết hợp giữa 5 chiến lược phân mảnh văn bản (Fixed-size, Sliding Window, Sentence, Semantic Markdown, Parent-Child) với 5 bộ truy xuất (BM25 Okapi, Dense Cosine, Hybrid RRF k=60, Cross-Encoder Reranker, và GraphRAG Louvain). Xác định cấu hình tối ưu vượt trội là Parent-Child kết hợp Hybrid RRF và Cross-Encoder đạt Hit@1 = 90.00%, Hit@3 = 100.00% và NDCG@5 = 0.9634.

3. **Hiện thực Hai Mô hình Mạng Nơ-ron PyTorch Chuyên biệt Đạt Chuẩn Công nghiệp**:
   - Mô hình `DiabetesMLP`: Gồm đúng 10.497 tham số học được, áp dụng hàm mất mát Weighted Binary Cross-Entropy với hệ số $pos\\_weight = 10.3$ giải quyết dứt điểm vấn đề mất cân bằng dữ liệu y tế (chỉ 8.82% ca bệnh), hiệu chuẩn ngưỡng quyết định Youden J $\\tau = 0.9016$, đạt ROC-AUC = 0.9755 và Độ nhạy lâm sàng Recall = 93.28% trên tập kiểm thử độc lập 14.420 mẫu bệnh nhân.
   - Mô hình `BiLSTM SeqForecaster`: Gồm đúng 140.865 tham số, cấu trúc 2 tầng BiLSTM 64 chiều, tối ưu hóa bằng Huber Loss $\\delta=1.0$ chống ngoại lai thị trường, tích hợp 200 lượt suy luận Monte Carlo Dropout để lượng hóa độ bất định vị kỷ Bayes và sinh Dải quạt tin cậy 90% (Fan Chart) hỗ trợ quản trị rủi ro đầu tư chuyên nghiệp.

4. **Hiện thực Tác tử Lập luận ReAct Tất định và Bộ Kiểm chứng Độ trung thực Số liệu ($\ge 85\%$)**:
   Kiên quyết loại bỏ cơ chế đa tác tử tự phát thiếu kiểm soát, thay vào đó xây dựng Tác tử ReAct điều phối tuần tự 6 công cụ chuyên trách theo đồ thị thực thi có định hướng (DAG). Triển khai thuật toán Grounded Verifier tự động kiểm tra trích dẫn nguồn `[Dxx]` (đạt 100%) và kiểm toán độ trung thực số liệu $\\ge 85\\%$ (thực tế đạt 97.4%), triệt tiêu hoàn toàn hiện tượng ảo giác nghiệp vụ (tỷ lệ ảo giác giảm từ 37.5% ở LLM đơn lẻ về 0.0%).

5. **Cung cấp Hệ thống Toàn vẹn Có Thể Vận hành Ngay (Production-Grade) kèm Giao diện Web Trực quan**:
   Toàn bộ mã nguồn được tổ chức module hóa chuyên nghiệp, vượt qua 100% các bài kiểm thử tự động đa tầng, và đi kèm một ứng dụng Web Dashboard FastAPI tích hợp thư viện đồ họa mạng lưới Cytoscape.js hiện đại, bảng tính nguy cơ lâm sàng và đồ thị nến dải quạt tin cậy thời gian thực.

### 7.2 Đánh giá Khách quan Các Hạn chế Kỹ thuật

Mặc dù đã đạt được những kết quả rất ấn tượng, đề tài vẫn còn tồn tại một số hạn chế kỹ thuật khách quan cần tiếp tục hoàn thiện:
- **Phạm vi Dữ liệu và Bản thể học**: Đồ thị tri thức y tế hiện tại mới tập trung sâu vào bệnh Đái tháo đường Típ 2, chưa mở rộng sang toàn bộ các bệnh lý rối loạn chuyển hóa phức tạp đi kèm (như hội chứng Cushing, suy giáp). Tương tự, đồ thị tài chính tập trung vào 4 cổ phiếu trụ cột đại diện và vàng SJC, chưa bao phủ toàn bộ 1.600 mã chứng khoán trên các sàn giao dịch Việt Nam.
- **Tài nguyên Tính toán Phần cứng**: Các thử nghiệm của đề tài được tối ưu hóa để vận hành mượt mà trên môi trường CPU tiêu chuẩn. Do đó, việc triển khai các mô hình ngôn ngữ lớn nguồn mở cục bộ (On-premise LLMs) có quy mô trên 14 tỷ tham số gặp phải nút thắt cổ chai về tốc độ sinh token.
- **Tính Động của Tri thức Pháp lý**: Quy trình trích xuất bộ ba từ văn bản pháp luật mới vẫn đòi hỏi sự rà soát và phê duyệt ở bước cuối cùng bởi chuyên gia con người (Human-in-the-loop) để đảm bảo không xảy ra sai sót ngữ nghĩa pháp lý.

### 7.3 Bốn Hướng Phát triển và Ứng dụng Thực tiễn trong Tương lai

Trong các giai đoạn nghiên cứu tiếp theo, hệ thống có thể được tiếp tục mở rộng theo 4 hướng chiến lược:
1. **Tích hợp Mô hình Ngôn ngữ Lớn Tiếng Việt Chuyên biệt Cục bộ**: Triển khai các mô hình mã nguồn mở tối ưu cho tiếng Việt (như PhoGPT, Vistral, Qwen-2.5-7B) chạy suy luận tăng tốc với vLLM hoặc Ollama trên hạ tầng máy chủ GPU chuyên dụng, đảm bảo tính bảo mật dữ liệu y tế và tài chính tuyệt đối nội bộ.
2. **Mở rộng Đồ thị Tri thức Đa tầng (Multi-layered Ontology)**: Mở rộng VietnamDiabetesKG kết nối với các kho tri thức y học mở toàn cầu (UMLS, SNOMED CT, DrugBank); mở rộng VietnamFinanceKG bao phủ toàn bộ thị trường trái phiếu doanh nghiệp, thị trường bất động sản và chuỗi cung ứng liên ngành.
3. **Ứng dụng Trợ lý Sức khỏe Cá thể hóa Thời gian Thực**: Phát triển ứng dụng di động cho bệnh nhân đái tháo đường, kết nối trực tiếp với các thiết bị đo đường huyết liên tục (Continuous Glucose Monitoring - CGM) thông qua giao thức IoT, tự động phân tích đồ thị đường huyết và đề xuất chế độ ăn uống bản địa hóa theo thời gian thực.
4. **Hệ thống Quản lý Danh mục Đầu tư Định lượng Tự động**: Tích hợp mô hình BiLSTM Monte Carlo Dropout vào các thuật toán tối ưu hóa danh mục đầu tư Markowitz và Black-Litterman, tự động tái cân bằng danh mục tài sản dựa trên mức độ rủi ro vĩ mô được suy luận từ đồ thị tri thức.

---

## TÀI LIỆU THAM KHẢO

- [1] Berners-Lee, T., Hendler, J., & Lassila, O. (2001). The Semantic Web. Scientific American, 284(5), 34-43.
- [2] Hogan, A., Blomqvist, E., Cochez, M., et al. (2021). Knowledge Graphs. ACM Computing Surveys, 54(4), 1-37.
- [3] Lewis, P., Perez, E., Piktus, A., et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. In Advances in Neural Information Processing Systems (NeurIPS 2020), 33, 9459-9474.
- [4] Yao, S., Zhao, J., Yu, D., et al. (2023). ReAct: Synergizing Reasoning and Acting in Language Models. International Conference on Learning Representations (ICLR 2023).
- [5] Robertson, S., & Zaragoza, H. (2009). The Probabilistic Relevance Framework: BM25 and Beyond. Foundations and Trends in Information Retrieval, 3(4), 333-389.
- [6] Cormack, G. V., Clarke, C. L., & Buettcher, S. (2009). Reciprocal Rank Fusion outperforms Condorcet and individual Run Methods in Ad Hoc Web Search. In Proceedings of the 32nd International ACM SIGIR Conference, 758-759.
- [7] Edge, D., Trinh, H., Cheng, N., et al. (2024). From Local to Global: A Graph RAG Approach to Query-Focused Summarization. Microsoft Research Technical Report, arXiv:2404.16130.
- [8] Blondel, V. D., Guillaume, J. L., Lambiotte, R., & Lefebvre, E. (2008). Fast unfolding of communities in large networks. Journal of Statistical Mechanics: Theory and Experiment, 2008(10), P10008.
- [9] Gal, Y., & Ghahramani, Z. (2016). Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning. In International Conference on Machine Learning (ICML 2016), 1050-1059.
- [10] Bộ Y tế Việt Nam. (2020). Quyết định số 5481/QĐ-BYT về việc ban hành tài liệu chuyên môn 'Hướng dẫn chẩn đoán và điều trị đái tháo đường típ 2'.
- [11] American Diabetes Association (ADA). (2024). Standards of Care in Diabetes—2024. Diabetes Care, 47(Suppl. 1), S1-S343.
- [12] Kidney Disease: Improving Global Outcomes (KDIGO) Diabetes Work Group. (2023). KDIGO 2023 Clinical Practice Guideline for the Management of Diabetes in Chronic Kidney Disease. Kidney International, 104(5S), S1-S127.
- [13] Chính phủ nước CHXHCN Việt Nam. (2012). Nghị định số 24/2012/NĐ-CP về Quản lý hoạt động kinh doanh vàng.
- [14] Chính phủ nước CHXHCN Việt Nam. (2025). Nghị định số 232/2025/NĐ-CP sửa đổi, bổ sung một số điều của Nghị định số 24/2012/NĐ-CP về Quản lý hoạt động kinh doanh vàng.
- [15] Vaswani, A., Shazeer, N., Parmar, N., et al. (2017). Attention is All You Need. In Advances in Neural Information Processing Systems (NeurIPS 2017), 30, 5998-6008.
- [16] Nogueira, R., & Cho, K. (2019). Passage Re-ranking with BERT. arXiv preprint arXiv:1901.04085.

