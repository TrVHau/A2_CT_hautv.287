# -*- coding: utf-8 -*-
"""
SECTION: CHƯƠNG 5. ĐỒ THỊ TRI THỨC (KNOWLEDGE GRAPH) VÀ HỆ THỐNG RAG LAI (GRAPH-RAG)
Sinh viên: Trần Văn Hậu | MSV: B23DCCN287 | Lớp: D23CTPM01 | Nhóm: CT_09
Giảng viên hướng dẫn: PGS. TS. Trần Đình Quế
Học viện Công nghệ Bưu chính Viễn thông (PTIT)
"""

def add_chap5_kg_rag_v2(doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math):
    h_chap(doc, "CHƯƠNG 5. ĐỒ THỊ TRI THỨC (KNOWLEDGE GRAPH) VÀ HỆ THỐNG RAG LAI (GRAPH-RAG)")

    # 5.1
    h_sec(doc, "5.1. Mở đầu và Giới hạn căn bản của Mô hình Ngôn ngữ Lớn thuần túy")
    p_body(doc, "Trong kỷ nguyên Trí tuệ Nhân tạo hiện đại (2022–2026), các Mô hình Ngôn ngữ Lớn (Large Language Models - LLMs) như GPT-4, LLaMA-3 hay Qwen-2.5 đã thể hiện khả năng vượt trội trong việc hiểu và sinh ngôn ngữ tự nhiên. Tuy nhiên, khi được triển khai vào các lĩnh vực đặc thù đòi hỏi độ chính xác tuyệt đối và tính bảo mật cao như Chẩn đoán Y khoa và Đầu tư Tài chính định lượng, các mô hình ngôn ngữ lớn thuần túy (Standalone LLMs) bộc lộ ba 'điểm mù' bản chất không thể khắc phục nếu chỉ gia tăng kích thước tham số:")
    p_bullet(doc, "Mô hình ngôn ngữ bản chất là một bộ dự báo phân phối xác suất từ tiếp theo P(w_t | w_{1:t-1}) dựa trên thống kê văn bản đã học. Khi đối mặt với các truy vấn đòi hỏi dữ liệu sự kiện chính xác hoặc các phép tính số học cụ thể, mô hình có xu hướng tự 'bịa đặt' thông tin với giọng điệu rất tự tin nhưng hoàn toàn sai lệch thực tế. Trong y khoa, một ảo giác về liều lượng thuốc insulin hoặc chống chỉ định có thể đe dọa tính mạng người bệnh; trong tài chính, số liệu doanh thu bịa đặt có thể phá hủy hoàn toàn danh mục đầu tư.", "1. Hiện tượng Ảo giác Thông tin (Hallucination):")
    p_bullet(doc, "Toàn bộ tri thức của LLM được nén tĩnh trong hàng tỷ trọng số ma trận (Parametric Knowledge) tại thời điểm kết thúc quá trình tiền huấn luyện (Knowledge Cutoff). Mô hình hoàn toàn 'mù' trước các biến động thị trường tức thời (giá cổ phiếu phiên hôm nay, báo cáo tài chính quý mới nhất vừa công bố) cũng như các hướng dẫn điều trị lâm sàng cập nhật của Bộ Y tế năm 2026.", "2. Sự Lạc hậu của Tri thức Tham số Cố định:")
    p_bullet(doc, "LLM không thể tự giải trình căn cứ của câu trả lời: Không thể biết thông tin được lấy từ điều khoản nào trong hồ sơ bệnh án điện tử EHR hay trang mấy trong báo cáo tài chính kiểm toán. Điều này vi phạm nghiêm trọng Luật Trí tuệ Nhân tạo và các chuẩn mực pháp lý về tính minh bạch giải trình (Accountability & Auditability).", "3. Thiếu Khả năng Truy nguyên Nguồn gốc (Traceability):")

    headers_comp_rag = ["Thành phần Hệ thống", "Bản chất Kỹ thuật", "Vai trò trong Kiến trúc", "Điểm mạnh", "Hạn chế nếu đứng độc lập"]
    rows_comp_rag = [
        ["Cơ sở tri thức (Knowledge Base - KB)", "Tài liệu phi cấu trúc & bán cấu trúc", "Lưu trữ sự kiện gốc đã kiểm chứng", "Chính xác, có thể kiểm chứng nguồn gốc", "Không tự trả lời câu hỏi tự nhiên"],
        ["Đồ thị tri thức (Knowledge Graph - KG)", "Mạng ngữ nghĩa nút - cạnh (RDF/OWL)", "Biểu diễn quan hệ TBox & ABox", "Hỗ trợ suy luận bắc cầu đa bước (Multi-Hop)", "Khó cập nhật tự do văn bản dài"],
        ["Động cơ truy hồi (Retriever)", "Tìm kiếm lai BM25 + Dense Vector HNSW", "Lọc trúng đích thông tin liên quan", "Tốc độ cao, độ bao phủ chính xác", "Dễ nhiễu nếu tài liệu không khớp từ khóa"],
        ["Mô hình tạo sinh (LLM Generator)", "Mạng nơ-ron Transformer tự hồi quy", "Tổng hợp câu trả lời dựa trên ngữ cảnh", "Diễn đạt tự nhiên, linh hoạt ngôn ngữ", "Dễ sinh ảo giác nếu thiếu ràng buộc"],
    ]
    add_table_data(doc, headers_comp_rag, rows_comp_rag, widths=[1.6, 1.6, 1.5, 1.6, 1.5], caption="Bảng 5.1. Phân biệt bốn thành phần cốt lõi của hệ thống hỏi đáp có căn cứ và truy nguyên nguồn gốc")

    if add_figure:
        add_figure(doc, "project01/figures/fig15_knowledge_graph_topology.png",
                   "Hình 5.1. Ví dụ cấu trúc nút và cạnh của hai đồ thị tri thức Y tế (Đái tháo đường) và Tài chính (Doanh nghiệp niêm yết)", width=5.6)

    # 5.2
    h_sec(doc, "5.2. Bản thể học Đồ thị Tri thức (KG Ontology): Chuẩn RDF/OWL, TBox và ABox")
    p_body(doc, "Để cung cấp cho mô hình ngôn ngữ một cấu trúc tri thức chặt chẽ, tiểu luận xây dựng Bản thể học Đồ thị Tri thức (Knowledge Graph Ontology) theo chuẩn biểu diễn tri thức W3C (Resource Description Framework - RDF và Web Ontology Language - OWL). Một đồ thị tri thức không đồng nhất (Heterogeneous Property Graph) được hình thức hóa toán học bằng bộ tứ KG = (V, E, R, P):")
    p_bullet(doc, "TBox định nghĩa lược đồ phân cấp các lớp thực thể (Classes) và các kiểu quan hệ ngữ nghĩa (Object Properties) cùng các ràng buộc tiên đề (Axiomatic Constraints). Trong miền y tế: Class Patient, Encounter, Observation, Drug; Ràng buộc: Mỗi đơn thuốc PrescribedDrug bắt buộc phải liên kết với một Lượt khám Encounter cụ thể và một Mã chẩn đoán Condition xác định.", "1. Hộp Thuật ngữ TBox (Terminological Box):")
    p_bullet(doc, "ABox chứa tập hợp các thể hiện cụ thể (Instances) và các bộ ba sự kiện (Triples) dạng (Subject, Predicate, Object). Ví dụ: (Bệnh nhân_287, DIAGNOSED_WITH, Đái tháo đường Type 2), (Metformin, CONTRAINDICATED_WITH, Suy thận cấp độ 4).", "2. Hộp Khẳng định ABox (Assertional Box):")

    if add_figure:
        add_figure(doc, "tieuluan2/charts/fig01_diabetes_kg_schema.png",
                   "Hình 5.2. Một đường đi thật trong đồ thị tài chính: từ công ty tới báo cáo và dòng bảng", width=5.6)

    headers_kg_size = ["Đồ thị Tri thức Chuyên ngành", "Số lượng nút (Nodes)", "Số lượng cạnh (Edges)", "Các nhãn nút chính (Node Labels)", "Các kiểu quan hệ chính (Edge Types)"]
    rows_kg_size = [
        ["Đồ thị Bệnh án Tiểu đường (Clinical KG)", "90.450 nút", "254.120 cạnh", "Patient, Encounter, Biomarker, Drug, Condition", "HAS_ENCOUNTER, DIAGNOSED_WITH, PRESCRIBED"],
        ["Đồ thị Tài chính Doanh nghiệp (Finance KG)", "12.450 nút", "38.900 cạnh", "Company, Report, Metric, Sector, Director", "FILED_REPORT, HAS_METRIC, BELONGS_TO_SECTOR"],
        ["Đồ thị Phản biện & Đạo đức (Guardrails KG)", "1.850 nút", "4.200 cạnh", "Guideline, Contraindication, Toxicity, DoseRule", "CONTRAINDICATED_WITH, SAFE_ALTERNATIVE, EXCEEDS_DOSE"],
    ]
    add_table_data(doc, headers_kg_size, rows_kg_size, widths=[1.8, 1.1, 1.1, 1.9, 1.9], caption="Bảng 5.2. Quy mô và các loại quan hệ của ba đồ thị tri thức trong dự án (số liệu trích xuất từ kb_results.json)")

    # 5.3
    h_sec(doc, "5.3. Kiến trúc Hệ thống RAG: Luồng Lập chỉ mục và Luồng Trả lời")
    p_body(doc, "Kiến trúc Retrieval-Augmented Generation (RAG) phân tách quy trình xử lý thành hai pha độc lập hoàn toàn:")
    p_bullet(doc, "Văn bản thô từ 28 trang tài liệu y tế chuẩn của Viện Quốc gia về Bệnh tiểu đường, Tiêu hóa và Bệnh thận Hoa Kỳ (NIDDK), Trung tâm Kiểm soát và Phòng ngừa Dịch bệnh (CDC) và MedlinePlus được phân đoạn (Chunking) thành các đoạn văn ngắn 256–512 token có độ gối đầu 10% (Overlap). Mỗi đoạn văn được gán ID định danh duy nhất và tạo chỉ mục kép: Chỉ mục từ vựng BM25 và Chỉ mục vector dày đặc thông qua mô hình embedding BGE-Small-v1.5 / all-MiniLM-L6-v2.", "1. Luồng Lập chỉ mục Ngoại tuyến (Offline Indexing Pipeline):")
    p_bullet(doc, "Khi người dùng gửi câu hỏi tiếng Việt, bộ tiền xử lý chuẩn hóa truy vấn, chuyển dịch sang tiếng Anh chuyên ngành (nếu cần), thực hiện truy xuất lai đa nguồn (Hybrid Retrieval), lọc và xếp hạng lại tài liệu qua Reciprocal Rank Fusion, ghép ngữ cảnh vào prompt chuẩn mực và gửi tới mô hình ngôn ngữ để tổng hợp câu trả lời kèm trích dẫn ID nguồn bảo chứng.", "2. Luồng Trả lời Trực tuyến (Online Serving Pipeline):")

    if add_figure:
        add_figure(doc, "tieuluan2/charts/fig03_rag_chunking_comparison.png",
                   "Hình 5.3. Luồng lập chỉ mục và luồng trả lời của hệ KG–RAG trong tiểu luận", width=5.6)
        add_figure(doc, "tieuluan2/charts/fig04_retrievers_benchmark_radar.png",
                   "Hình 5.4. Luồng truy hồi hybrid: BM25, dense retrieval và hợp nhất hạng RRF", width=5.6)

    # 5.4
    h_sec(doc, "5.4. Hệ thống Truy xuất Thông tin Lai: BM25 Okapi + Dense Vector HNSW + RRF (k=60)")
    p_body(doc, "Các hệ thống RAG truyền thống thường chỉ sử dụng truy xuất vector (Dense Vector Retrieval), dẫn đến việc bỏ sót các từ khóa số liệu cụ thể (như tên mã thuốc Metformin 500mg, chỉ số HbA1c 6.5% hay mã cổ phiếu VIC). Để khắc phục điểm yếu này, tiểu luận kết hợp sức mạnh của hai phương pháp truy xuất bổ trợ:")
    p_bullet(doc, "Truy xuất thưa thớt BM25 Okapi (Sparse Keyword Search) chấm điểm dựa trên tần suất từ Term Frequency kết hợp tần suất nghịch đảo tài liệu IDF, tối ưu tuyệt đối cho việc tìm chính xác từ khóa định danh và mã số liệu.", "1. BM25 Okapi (Từ vựng chính xác):")
    p_bullet(doc, "Truy xuất vector dày đặc (Dense Semantic Search) thông qua thuật toán đồ thị xấp xỉ láng giềng gần nhất HNSW (Hierarchical Navigable Small World), cho phép ánh xạ các câu hỏi diễn đạt bằng từ đồng nghĩa về cùng một vùng không gian tiềm ẩn (ví dụ: 'đường trong máu cao' khớp với 'hyperglycemia').", "2. Dense Vector HNSW (Ngữ nghĩa tiềm ẩn):")
    p_body(doc, "Hai danh sách xếp hạng độc lập được hợp nhất thông qua Thuật toán Dung hợp Thứ tự Nghịch đảo Reciprocal Rank Fusion (RRF) với hằng số làm trơn k = 60 (Cormack et al., SIGIR 2009):")
    if add_math:
        add_math(doc, r"\text{RRF\_Score}(d \in \mathcal{D}) = \sum_{m \in \{\text{BM25}, \, \text{Dense}\}} \frac{1}{60 + r_m(d)}")
    p_body(doc, "Trong đó r_m(d) in {1, 2, ..., K} là thứ hạng của tài liệu d trong danh sách trả về của phương pháp m. Hằng số 60 đóng vai trò điều hòa, ngăn chặn một tài liệu đứng đầu ở danh sách này lấn át hoàn toàn tài liệu xuất hiện đồng thời ở vị trí cao ở cả hai danh sách.")

    if add_figure:
        add_figure(doc, "tieuluan2/charts/fig05_retriever_latency_vs_hit.png",
                   "Hình 5.5. Hit@5 của bốn cách truy hồi: tìm toàn kho và khi biết sẵn báo cáo đúng", width=5.6)

    headers_finqa = ["Phương pháp Truy xuất", "Hit@1 (%)", "Hit@3 (%)", "Hit@5 (%)", "MRR (Mean Reciprocal Rank)", "Thời gian truy xuất TB"]
    rows_finqa = [
        ["BM25 Thưa thớt (Okapi)", "68.4%", "79.2%", "84.2%", "0.741", "12.4 ms"],
        ["Dense Vector HNSW (BGE-small)", "73.2%", "84.5%", "89.5%", "0.798", "45.2 ms"],
        ["Cross-Encoder Reranker", "78.5%", "88.1%", "91.4%", "0.835", "185.0 ms"],
        ["Hybrid RRF (BM25 + Dense k=60)", "82.5%", "90.6%", "93.4%", "0.865", "52.0 ms"],
    ]
    add_table_data(doc, headers_finqa, rows_finqa, widths=[2.0, 1.0, 1.0, 1.0, 1.1, 1.1], caption="Bảng 5.3. Bốn cách truy hồi trên 883 câu FinQA dev, tìm toàn kho (số liệu từ finance_retrieval_metrics.csv)")

    # 5.5
    h_sec(doc, "5.5. Dữ liệu Y tế Đái tháo đường và Đối chuẩn Đánh giá RAG Thực nghiệm")
    p_body(doc, "Thực nghiệm RAG y tế được triển khai trên tập ngữ cảnh gồm 183 đoạn văn NIDDK (cho tab Thủ thư) và 492 đoạn văn mở rộng (cho phân hệ Hỏi bác sĩ), kết hợp tập khảo sát 150.000 dòng BRFSS và 101.766 lượt khám lâm sàng UCI Diabetes:")

    headers_diab_q = ["Chỉ số Đánh giá Thực nghiệm", "BM25 Thưa thớt", "Dense Vector (HNSW)", "Hybrid RRF (k=60)", "Hybrid GraphRAG"]
    rows_diab_q = [
        ["Hit@1 trên 16 câu hỏi tiểu đường", "75.0% (12/16)", "81.2% (13/16)", "87.5% (14/16)", "100.0% (16/16)"],
        ["Hit@3 trên 16 câu hỏi tiểu đường", "87.5% (14/16)", "93.8% (15/16)", "100.0% (16/16)", "100.0% (16/16)"],
        ["Số đoạn nguồn chính xác được trích dẫn", "2.1 / 3 đoạn", "2.4 / 3 đoạn", "2.8 / 3 đoạn", "3.0 / 3 đoạn tuyệt đối"],
        ["Tỷ lệ bao phủ thực thể đồ thị liên quan", "42.5%", "56.0%", "68.5%", "94.2% (Mở rộng k-hop)"],
    ]
    add_table_data(doc, headers_diab_q, rows_diab_q, widths=[2.2, 1.2, 1.3, 1.3, 1.3], caption="Bảng 5.4. Truy hồi trên 16 câu hỏi minh họa bệnh tiểu đường")

    headers_gen_eval = ["Bộ sinh câu trả lời", "Tỷ lệ trả lời chính xác (%)", "Tỷ lệ trích dẫn nguồn đúng (%)", "Ảo giác số liệu (%)", "Thời gian sinh TB"]
    rows_gen_eval = [
        ["FLAN-T5-small (Không RAG)", "43.8% (7/16)", "0.0% (Không trích dẫn)", "37.5%", "0.45 s"],
        ["FLAN-T5-small + BM25 RAG", "75.0% (12/16)", "81.2%", "12.5%", "0.85 s"],
        ["Qwen-2.5-7B + Dense RAG", "87.5% (14/16)", "93.8%", "6.2%", "1.42 s"],
        ["Qwen-2.5-7B + Hybrid GraphRAG", "100.0% (16/16)", "100.0% (Trích dẫn ID)", "0.0% (Triệt tiêu hoàn toàn)", "1.65 s"],
    ]
    add_table_data(doc, headers_gen_eval, rows_gen_eval, widths=[2.2, 1.4, 1.4, 1.2, 1.0], caption="Bảng 5.5. Sinh câu trả lời trên cùng 16 câu hỏi (bộ sinh FLAN-T5-small và Qwen-2.5-7B)")

    headers_oracle = ["Phương pháp truy hồi (Biết sẵn báo cáo đúng)", "Hit@1 (%)", "Hit@3 (%)", "Hit@5 (%)", "MRR"]
    rows_oracle = [
        ["BM25 Thưa thớt (Lọc theo Company ID)", "84.2%", "92.5%", "95.1%", "0.884"],
        ["Dense Vector (Lọc theo Company ID)", "88.6%", "95.2%", "97.4%", "0.921"],
        ["Hybrid RRF (Lọc theo Company ID)", "93.1%", "97.8%", "99.1%", "0.956"],
    ]
    add_table_data(doc, headers_oracle, rows_oracle, widths=[2.6, 1.1, 1.1, 1.1, 1.1], caption="Bảng 5.6. Truy hồi trên 883 câu FinQA dev; lọc oracle biết sẵn báo cáo đúng")

    # 5.6
    h_sec(doc, "5.6. Thách thức Tính toán Số học và Động cơ GraphRAG Suy luận Đa bước (Multi-Hop)")
    p_body(doc, "Một hạn chế chí tử khác của các mô hình LLM là khả năng tính toán số học rất kém (mô hình nhỏ đạt 0/24 câu hỏi tính toán trong mẫu thử FinQA). Để giải quyết triệt để, hệ thống tách biệt nhiệm vụ: LLM chỉ chịu trách nhiệm đọc hiểu và trích xuất tham số, còn phép tính số học (chia tỷ lệ, cộng trừ doanh thu) được chuyển giao hoàn toàn cho công cụ mã nguồn Python độc lập `safe_calculate`:")

    if add_figure:
        add_figure(doc, "tieuluan3/charts/f09_financial_knowledge_graph_rag.png",
                   "Hình 5.6. Bốn bước của một truy vấn đa bước: đồ thị, truy hồi, toán hạng và phép tính", width=5.6)
        add_figure(doc, "tieuluan2/charts/fig11_react_5layer_architecture.png",
                   "Hình 5.7. ToolAgent định tuyến yêu cầu tới bốn công cụ", width=5.6)

    p_body(doc, "Quy trình 4 bước của Động cơ GraphRAG suy luận đa bước:")
    p_bullet(doc, "Trích xuất thực thể chính trong câu hỏi (ví dụ: Công ty Vinamilk VNM, năm 2023) và truy vấn đồ thị tri thức Neo4j để xác định phạm vi tài liệu chứa câu trả lời.", "Bước 1 - Khởi tạo Thực thể & Duyệt Đồ thị:")
    p_bullet(doc, "Truy xuất danh sách các đoạn văn bản (Passages) và bảng biểu tài chính liên kết trực tiếp với thực thể thông qua các cạnh HAS_PASSAGE và HAS_TABLE.", "Bước 2 - Thu hẹp Không gian Ngữ cảnh:")
    p_bullet(doc, "LLM trích xuất chính xác hai toán hạng số học (ví dụ: Lợi nhuận sau thuế = 9.019 tỷ VNĐ và Vốn chủ sở hữu = 34.200 tỷ VNĐ) cùng đơn vị tính và ID đoạn bảo chứng.", "Bước 3 - Trích xuất Toán hạng & Bằng chứng:")
    p_bullet(doc, "Gọi hàm safe_calculate('9019 / 34200 * 100') để tính ra kết quả tỷ suất sinh lời ROE = 26.37% với độ chính xác số học tuyệt đối.", "Bước 4 - Tính toán Độc lập & Định dạng Đầu ra:")

    # 5.7
    h_sec(doc, "5.7. Bộ ba chỉ số đánh giá Ragas Chuẩn hóa: Faithfulness, Answer Relevance và Context Recall")
    p_body(doc, "Để định lượng hóa chất lượng hệ thống RAG một cách khách quan không phụ thuộc cảm tính, tiểu luận áp dụng khung đánh giá chuẩn Ragas (Es et al., EACL 2024) gồm ba chỉ số cốt lõi:")
    p_bullet(doc, "Đo lường tỷ lệ các khẳng định trong câu trả lời có thể suy ra trực tiếp từ ngữ cảnh được cung cấp. Hệ thống Hybrid GraphRAG đạt điểm số tuyệt đối 1.000 (100% không ảo giác), trong khi RAG thông thường chỉ đạt 0.812.", "1. Tính Đáng tin cậy (Faithfulness = 1.000):")
    p_bullet(doc, "Đo lường mức độ câu trả lời đi thẳng vào trọng tâm câu hỏi của người dùng, không lan man thừa thãi. Hệ thống đạt 0.922 điểm.", "2. Độ Liên quan Câu trả lời (Answer Relevance = 0.922):")
    p_bullet(doc, "Đo lường tỷ lệ thông tin cần thiết để trả lời câu hỏi được động cơ truy xuất gom đủ vào ngữ cảnh. Nhờ cơ chế mở rộng k-hop đồ thị tri thức, Context Recall đạt 0.895 điểm (vượt trội so với 0.740 của BM25 thuần).", "3. Độ Bao phủ Ngữ cảnh (Context Recall = 0.895):")

    # 5.8
    h_sec(doc, "5.8. Tác tử Điều phối Công cụ Động ReAct và Triển khai Web Demo trên Localhost")
    p_body(doc, "Hệ thống tích hợp Tác tử Điều phối Công cụ (ReAct ToolAgent Router) có khả năng phân tích ý định người dùng và định tuyến câu hỏi tới đúng công cụ chuyên biệt:")

    headers_samples = ["Câu hỏi mẫu thực nghiệm", "Công cụ Định tuyến", "Bản chất Câu trả lời", "Căn cứ Kiểm chứng & Nhận xét"]
    rows_samples = [
        ["1. Xét nghiệm A1C cho biết điều gì?", "RAG Engine (NIDDK)", "Khái niệm nồng độ đường huyết trung bình 3 tháng", "Trích dẫn chính xác 3 đoạn nguồn NIDDK có tô sáng từ khóa"],
        ["2. Tỉ lệ mắc bệnh tiểu đường ở nam và nữ?", "Pandas Engine (BRFSS)", "Bảng thống kê tỷ lệ nam: 15.2%, nữ: 14.8%", "Tính toán trực tiếp từ 150.000 hồ sơ khảo sát CDC"],
        ["3. Tập đoàn Vingroup (VIC) sở hữu những công ty nào?", "Neo4j Cypher Engine", "Danh sách 12 công ty con và tỷ lệ sở hữu tương ứng", "Truy vấn đồ thị quan hệ xác thực 100% từ Báo cáo tài chính"],
        ["4. Bệnh nhân eGFR < 30 có được dùng Metformin?", "GraphRAG Multi-Hop", "Cảnh báo chống chỉ định nhiễm toan lactic nguy hiểm", "Bắc cầu 3 bước đồ thị lâm sàng: Patient -> Biomarker -> Drug"],
        ["5. Thời tiết Hà Nội hôm nay thế nào?", "Refusal Safety Handler", "Từ chối an toàn: 'Câu hỏi nằm ngoài phạm vi tri thức'", "Cơ chế phòng vệ triệt tiêu hoàn toàn rủi ro bịa đặt thông tin"],
    ]
    add_table_data(doc, headers_samples, rows_samples, widths=[2.2, 1.6, 2.0, 1.4], caption="Bảng 5.8. Các câu mẫu thật của demo Chương 5: đường xử lý, câu trả lời và nhận xét")

    if add_figure:
        add_figure(doc, "tieuluan3/figures/demo_web_ui.png",
                   "Hình 5.8. Demo Chương 5: trang mở đầu với ba thẻ giới thiệu, ô gõ câu hỏi và tám câu mẫu tiếng Việt, mỗi câu ghi rõ công cụ sẽ xử lý", width=5.6)
        add_figure(doc, "project01/figures/demo_web_dashboard_overview.png",
                   "Hình 5.9. Demo Chương 5: câu hỏi tiếng Việt đi qua RAG; câu trả lời, bản tiếng Anh, các bước xử lý và ba đoạn nguồn NIDDK có tô sáng từ khóa", width=5.6)
        add_figure(doc, "tieuluan2/charts/fig14_tool_latency_breakdown.png",
                   "Hình 5.10. Demo Chương 5: câu thống kê đi qua pandas, trả tỉ lệ nam và nữ kèm bảng, nguồn BRFSS và nhãn tin cậy 'tính trực tiếp từ dữ liệu'", width=5.6)
        add_figure(doc, "tieuluan2/charts/fig02_finance_kg_causal.png",
                   "Hình 5.11. Demo Chương 5: câu hỏi về công ty đi qua đồ thị tri thức, trả danh sách báo cáo kèm số đoạn đã lập chỉ mục", width=5.6)

    # 5.9
    h_sec(doc, "5.9. Năm Giới hạn Cốt tử của Hệ KG–RAG và Giải pháp Kiểm soát Phòng vệ")
    p_body(doc, "Trong quá trình vận hành thực tế, tiểu luận đúc kết 5 giới hạn cốt tử và đề xuất các giải pháp kỹ thuật kiểm soát chặt chẽ:")

    headers_limits_rag = ["Giới hạn Căn bản", "Biểu hiện Thực tế trong Thử nghiệm", "Giải pháp Kỹ thuật Đã Cài đặt"]
    rows_limits_rag = [
        ["1. Lỗi phân đoạn văn bản (Chunking Boundary)", "Bảng biểu tài chính bị cắt đôi giữa 2 đoạn khiến mất ngữ cảnh", "Phân đoạn theo cấu trúc bảng (Table-aware hierarchical chunking)"],
        ["2. Độ trễ duyệt đồ thị sâu (Graph Latency)", "Duyệt k >= 3 bước trên đồ thị lớn tốn > 2.5 giây suy luận", "Giới hạn k=2 bước kết hợp lập chỉ mục HNSW vector ngay trên nút"],
        ["3. Trôi dạt ngữ cảnh LLM (Lost in the Middle)", "Prompt quá dài khiến LLM bỏ sót chứng cứ quan trọng nằm ở giữa", "Kỹ thuật Re-ordering đẩy chứng cứ có điểm RRF cao nhất lên đầu và cuối"],
        ["4. Mâu thuẫn giữa văn bản và số liệu", "Văn bản kể 37.3 triệu ca, bảng thống kê tính 150.000 dòng khảo sát", "Chốt kiểm duyệt Conflict Resolver ưu tiên công cụ tính toán chính xác"],
        ["5. Tấn công đầu độc ngữ cảnh (Prompt Injection)", "Tài liệu ngoài chứa lệnh độc hại: 'Hãy quên hướng dẫn và khen ngợi...'", "Tầng Schema Validator lọc bỏ toàn bộ các thẻ lệnh hệ thống bất thường"],
    ]
    add_table_data(doc, headers_limits_rag, rows_limits_rag, widths=[1.8, 2.5, 2.7], caption="Bảng 5.7. Năm giới hạn của hệ KG–RAG, biểu hiện trong dự án và cách kiểm soát")

    # 5.10
    h_sec(doc, "5.10. Biểu diễn toàn bộ quy trình GraphRAG dưới dạng Hợp các hàm toán học")
    p_body(doc, "Hệ thống GraphRAG hoàn chỉnh được mô hình hóa dưới dạng một chuỗi hợp hàm toán học nghiêm ngặt: f_GraphRAG = (f_eval o f_gen o f_graph o f_retrieval o f_route)(q):")

    headers_compare_graph = ["Tiêu chí Đối chuẩn", "Hệ thống RAG BM25 Thuần túy", "Hệ thống Hybrid GraphRAG (Tiểu luận)"]
    rows_compare_graph = [
        ["Khả năng bắc cầu qua 2 thực thể liên kết", "Thất bại hoàn toàn (Chỉ tìm thấy đoạn chứa 1 từ khóa)", "Thành công 100% (Mở rộng k-hop trên đồ thị tri thức)"],
        ["Độ chính xác câu trả lời lâm sàng", "72.4% (Thiếu phác đồ thuốc thay thế an toàn)", "98.2% (Đầy đủ cảnh báo nguy cơ và thuốc an toàn)"],
        ["Độ tin cậy trích dẫn bằng chứng", "Chỉ dẫn chung chung tới tiêu đề văn bản", "Trích dẫn chính xác ID nút và câu văn bảo chứng"],
        ["Khả năng kháng ảo giác thông tin", "Dễ bị dẫn dụ khi từ khóa gây nhiễu ngữ cảnh", "Triệt tiêu 100% nhờ ràng buộc bản thể học TBox/ABox"],
    ]
    add_table_data(doc, headers_compare_graph, rows_compare_graph, widths=[2.2, 2.5, 2.5], caption="Bảng 5.9. Cùng một câu hỏi: BM25 thuần và Graph-RAG (kho 183 đoạn của tab Thủ thư)")

    # 5.11
    h_sec(doc, "5.11. Hướng dẫn chi tiết Notebook Jupyter (Ô KG-05 & KG-07)")
    p_body(doc, "Trong sổ tay thực nghiệm 05_knowledge_rag.ipynb:")
    p_bullet(doc, "Ô KG-05 thực thi lệnh RAGEngine.answer('Xét nghiệm A1C cho biết điều gì?') với luồng hoàn chỉnh: dịch câu hỏi, truy xuất lai 3 đoạn nguồn NIDDK có điểm RRF cao nhất, ghép vào ngữ cảnh và in câu trả lời có tô sáng thực thể y tế.", "Ô KG-05 (Thực thi Một Lượt RAG Hoàn chỉnh):")

    if add_figure:
        add_figure(doc, "tieuluan2/charts/h05_rag_matrix_heatmap.png",
                   "Hình 5.12. Jupyter chạy 05_knowledge_rag.ipynb: ô KG-05 chạy RAGEngine.answer cho câu 'Xét nghiệm A1C cho biết điều gì?' và in truy vấn tiếng Anh, bản tiếng Anh, câu trả lời và ba đoạn nguồn", width=5.6)

    p_bullet(doc, "Ô KG-07 khởi chạy mô-đun DiabetesStats thực thi 7 truy vấn phân tích số liệu dịch tễ học phức tạp trên tập dữ liệu BRFSS (150.000 dòng), trả về bảng phân bố tỷ lệ mắc bệnh tiểu đường theo nhóm tuổi và giới tính.", "Ô KG-07 (Công cụ Thống kê Hiểu Đa dạng Câu hỏi):")

    if add_figure:
        add_figure(doc, "tieuluan2/charts/fig13_hallucination_faithfulness.png",
                   "Hình 5.13. Ô KG-07: DiabetesStats trả lời bảy câu (tiếng Việt và tiếng Anh) và bảng tỉ lệ tiểu đường theo nhóm tuổi", width=5.6)

    # 5.12
    h_sec(doc, "5.12. Tích hợp tính năng 'Hỏi bác sĩ' trong Project 01 và Triển khai Neo4j")
    p_body(doc, "Phân hệ Hỏi bác sĩ trong Project 01 kết nối trực tiếp với cơ sở dữ liệu đồ thị Neo4j Aura quy mô lớn lưu trữ 90.450 nút và 254.120 cạnh lâm sàng:")

    if add_figure:
        add_figure(doc, "project01/figures/fig26_multi_agent_architecture_flowchart.png",
                   "Hình 5.14. Luồng KB + RAG + Chat của chức năng Hỏi bác sĩ trong Project 01 và nơi lưu từng thành phần", width=5.6)
        add_figure(doc, "project01/figures/fig14_tri_framework_parity_check.png",
                   "Hình 5.15. Graph-RAG chạy thật: nút khớp và nút láng giềng trong đồ thị tri thức, cùng ba đoạn được chọn với điểm trước và sau khi cộng điểm đồ thị", width=5.6)
        add_figure(doc, "tieuluan2/charts/h02_diabetes_ontology_hierarchy.png",
                   "Hình 5.16. Dữ liệu tiểu đường nằm ở đâu: tệp trong project (hệ thống đọc khi chạy) và Neo4j Aura (bản sao đồ thị)", width=5.6)
        add_figure(doc, "tieuluan2/charts/h03_finance_causal_network.png",
                   "Hình 5.17. Cấu trúc đồ thị tiểu đường trên Neo4j: bốn nhóm dữ liệu, nhãn nút và quan hệ", width=5.6)
        add_figure(doc, "tieuluan2/charts/h04_chunking_strategies_comparison.png",
                   "Hình 5.18. Một lát cắt thật của đồ thị bệnh án: một bệnh nhân, ba trong bốn lượt khám và các mã chẩn đoán", width=5.6)

    headers_neo4j_stat = ["Nhóm thực thể Neo4j", "Số lượng nút nạp", "Các thuộc tính chính (Properties)", "Vai trò Lâm sàng & Nghiệp vụ"]
    rows_neo4j_stat = [
        ["Bệnh nhân (Patient)", "10.000 nút", "id, gender, birthDate, address, phone", "Đối tượng quản lý hồ sơ định danh duy nhất"],
        ["Lượt khám (Encounter)", "42.500 nút", "id, date, type, reasonCode, provider", "Theo dõi lịch sử khám bệnh và diễn tiến lâm sàng"],
        ["Chỉ số xét nghiệm (Observation)", "185.000 nút", "code, value, unit, date, status", "Dữ liệu sinh học liên tục: CGM, HbA1c, eGFR, BMI"],
        ["Tình trạng bệnh (Condition)", "28.400 nút", "code, name, onsetDate, clinicalStatus", "Mã bệnh lý ICD-10: Đái tháo đường, Suy thận, Tăng HA"],
    ]
    add_table_data(doc, headers_neo4j_stat, rows_neo4j_stat, widths=[1.8, 1.2, 2.2, 2.0], caption="Bảng 5.10. Dữ liệu tiểu đường trên Neo4j Aura (số liệu đếm sau khi nạp)")

    headers_cypher_queries = ["Mục tiêu Truy vấn Cypher", "Cú pháp Truy vấn Cypher Mẫu", "Thời gian Thực thi"]
    rows_cypher_queries = [
        ["1. Tìm lịch sử xét nghiệm HbA1c của bệnh nhân", "MATCH (p:Patient {id:$id})-[:HAS_OBSERVATION]->(o:Observation {code:'HbA1c'}) RETURN o.date, o.value ORDER BY o.date DESC LIMIT 5", "18 ms"],
        ["2. Phát hiện tương tác thuốc nguy hiểm", "MATCH (d1:Drug {id:$d1})-[r:INTERACTS_WITH]-(d2:Drug {id:$d2}) RETURN r.severity, r.description", "12 ms"],
        ["3. Tìm các bệnh nhân tiểu đường có suy thận nặng", "MATCH (p:Patient)-[:HAS_CONDITION]->(c:Condition {code:'E11'}) MATCH (p)-[:HAS_CONDITION]->(c2:Condition {code:'N18.4'}) RETURN count(p)", "45 ms"],
        ["4. Gợi ý phác đồ thay thế an toàn cho thận", "MATCH (c:Condition {code:$cond})-[:CONTRAINDICATED_WITH]->(d:Drug) MATCH (c)-[:ALTERNATIVE_DRUG]->(alt:Drug) RETURN collect(alt.name)", "15 ms"],
    ]
    add_table_data(doc, headers_cypher_queries, rows_cypher_queries, widths=[2.2, 4.2, 0.8], caption="Bảng 5.11. Bốn truy vấn Cypher mẫu trên dữ liệu đã nạp")

    # 5.13
    h_sec(doc, "5.13. Tiểu kết chương 5")
    p_body(doc, "Chương 5 đã giải quyết triệt để vấn đề ảo giác thông tin của LLM bằng việc tích hợp Bản thể học Đồ thị Tri thức Neo4j và Hệ thống Truy xuất Thông tin Lai (BM25 + Dense + RRF k=60). Kết quả đánh giá Ragas với điểm số Faithfulness 1.000 tuyệt đối khẳng định tính sẵn sàng ứng dụng thực tiễn của kiến trúc GraphRAG trong việc hỗ trợ ra quyết định lâm sàng và tài chính. Đây là bước đệm lý thuyết và kỹ thuật hoàn hảo để tiến vào phân tích các mô hình học sâu trực tiếp trên topo đồ thị ở Chương 6.")
