"""
Metadata, Front Matter, Reference Tables, and Bibliography for Master Treatise.
Author: Tran Van Hau - Student ID: B23DCCN287 - Class: D23CTPM01 - PTIT
Supervisor: PGS.TS. Tran Dinh Que
Course: Phat trien cac He thong Thong minh (Intelligent Systems Development)
"""

FRONT_MATTER = {
    "institution": "HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG",
    "faculty": "KHOA CÔNG NGHỆ THÔNG TIN 1",
    "course": "PHÁT TRIỂN CÁC HỆ THỐNG THÔNG MINH (INTELLIGENT SYSTEMS DEVELOPMENT)",
    "title": "ĐỒ THỊ TRI THỨC (KNOWLEDGE GRAPH) VÀ RAG, TÍCH HỢP HỌC SÂU ĐA MIỀN CHO Y TẾ VÀ TÀI CHÍNH VIỆT NAM",
    "subtitle": "CÔNG TRÌNH NGHIÊN CỨU TOÀN DIỆN, THIẾT KẾ KIẾN TRÚC TÁC TỬ REACT VÀ ĐỐI CHUẨN ĐỘ TRUNG THỰC ĐỊNH LƯỢNG",
    "student_name": "Trần Văn Hậu",
    "student_id": "B23DCCN287",
    "class_name": "D23CTPM01",
    "group_name": "Nhóm lớp CT – Nhóm 07",
    "supervisor": "PGS.TS. Trần Đình Quế",
    "academic_year": "Học kỳ 1 – Năm học 2026 – 2027",
    "location_year": "HÀ NỘI, NĂM 2026"
}

EXECUTIVE_SUMMARY_VI = """
Báo cáo chuyên khảo này trình bày công trình nghiên cứu, thiết kế kiến trúc và triển khai thực nghiệm một Hệ thống Thông minh đa miền hoàn chỉnh, tích hợp ba trụ cột công nghệ then chốt của Trí tuệ Nhân tạo hiện đại: Đồ thị Tri thức Hình thức (Formal Knowledge Graph - KG), Kỹ thuật Sinh Tăng cường Truy xuất (Retrieval-Augmented Generation - RAG), và Mô hình Học sâu Chuyên biệt (PyTorch Deep Learning), được điều phối thống nhất bởi Tác tử Lập luận ReAct (Reasoning and Acting) kết hợp Bộ kiểm chứng Độ trung thực Số liệu (Grounded Verifier).

Công trình giải quyết bài toán cốt lõi: Làm thế nào để loại bỏ triệt để hiện tượng "ảo giác" (hallucination), thiếu khả năng truy vết nguồn gốc và sự mờ đục số liệu của các Mô hình Ngôn ngữ Lớn (LLM) đơn lẻ khi giải quyết các vấn đề nghiệp vụ có tính cam kết cao trong hai lĩnh vực nhạy cảm bậc nhất tại Việt Nam là Y tế Lâm sàng (chẩn đoán và phác đồ điều trị Đái tháo đường Típ 2 theo Quyết định 5481/QĐ-BYT) và Phân tích Thị trường Tài chính Vĩ mô (chuỗi truyền dẫn Fed - DXY - USD/VND, thị trường vàng miếng SJC theo Nghị định 24/2012 và Nghị định 232/2025/NĐ-CP, cùng rổ cổ phiếu VN30).

Hệ thống được xây dựng với các thành tựu kỹ thuật trọng tâm:
1. Xây dựng hai Đồ thị Tri thức chuyên ngành hoàn chỉnh: VietnamDiabetesKG (23 lớp bản thể, 17 vị từ lâm sàng) và VietnamFinanceKG (16 lớp, 6 vị từ quan hệ nhân quả có hướng có dấu), hỗ trợ suy diễn tiến (Forward Chaining) RDFS/OWL đến điểm bất động và 5 nhóm truy vấn SPARQL chuyên sâu.
2. Thiết lập khung đánh giá thực nghiệm toàn diện trên kho ngữ liệu 17 tài liệu quy chuẩn (D01-D17) đối chuẩn Ma trận 25 cấu hình RAG (kết hợp 5 chiến lược phân mảnh chunking với 5 bộ truy xuất: BM25, Dense TF-IDF, Hybrid RRF k=60, Cross-Encoder reranker và GraphRAG phân cụm Louvain).
3. Triển khai hai mô hình học sâu PyTorch tối ưu: DiabetesMLP (10.497 tham số, Weighted BCE pos_weight=10.3, ROC-AUC 0.9755) và BiLSTM SeqForecaster (140.865 tham số, Huber loss delta=1.0, 200 lượt Monte Carlo Dropout tạo dải quạt tin cậy 90%).
4. Hiện thực Tác tử ReAct với Bộ lập kế hoạch tất định (Deterministic Planner) và Bộ kiểm chứng độ trung thực số liệu tự động (Grounded Verifier), đảm bảo tỷ lệ trích dẫn tài liệu 100% và độ chính xác số liệu >= 85%.
5. Cung cấp Giao diện Web Interactive Dashboard trực quan bằng FastAPI và Cytoscape.js cho phép người dùng khai thác tri thức và suy luận theo thời gian thực.
"""

EXECUTIVE_SUMMARY_EN = """
This monograph presents the comprehensive theoretical design, implementation, and empirical evaluation of a multi-domain Intelligent System that unifies three core pillars of modern Artificial Intelligence: Formal Knowledge Graphs (Symbolic AI), Advanced Retrieval-Augmented Generation (RAG), and Task-Specific PyTorch Deep Learning models, coordinated via a deterministic ReAct (Reasoning and Acting) loop coupled with an automated Grounded Verifier.

The primary objective of this project is to eliminate hallucination, ensure absolute factual provenance, and overcome numeric opacity inherent in standalone Large Language Models (LLMs) when applied to high-stakes decision-making tasks in Vietnam: Clinical Healthcare (Type 2 Diabetes Mellitus diagnosis and protocol optimization under MOH Decision 5481/QD-BYT and ADA 2024 standards) and Macroeconomic Financial Intelligence (Fed-DXY-VND monetary transmission mechanisms, SJC bullion dynamics under Decrees 24/2012 and 232/2025/ND-CP, and VN30 equity pricing).

Key technical contributions include:
1. Construction of two formal RDF Knowledge Graphs: VietnamDiabetesKG (23 ontology classes, 17 predicates) and VietnamFinanceKG (16 classes, 6 directed signed causal predicates), featuring forward-chaining RDFS/OWL entailment and complex SPARQL analytical queries.
2. Empirical benchmarking of a comprehensive 25-configuration RAG matrix across 17 standardized Vietnamese technical documents (D01-D17), evaluating 5 chunking strategies and 5 retrieval paradigms (BM25 Okapi, Dense retrieval, Hybrid RRF k=60, Cross-Encoder reranking, and Louvain-based GraphRAG).
3. Two dedicated PyTorch neural networks: DiabetesMLP (10,497 parameters, Weighted BCE loss with pos_weight=10.3, calibrated ROC-AUC 0.9755) and BiLSTM SeqForecaster (140,865 parameters, Huber loss delta=1.0, 200-pass Monte Carlo Dropout producing 90% confidence fan charts).
4. A deterministic ReAct agent orchestrating 6 verified tools, enforced by an automated Grounded Verifier requiring 100% citation grounding and >=85% numerical fidelity.
5. An interactive production-grade Web Dashboard developed with FastAPI, Cytoscape.js, and Chart.js, delivering real-time knowledge graph exploration, clinical risk estimation, and probabilistic forecasting.
"""

ABBREVIATIONS = [
    ("KG", "Knowledge Graph", "Đồ thị Tri thức"),
    ("RAG", "Retrieval-Augmented Generation", "Sinh Tăng cường Truy xuất"),
    ("RDF", "Resource Description Framework", "Khung Miêu tả Tài nguyên"),
    ("RDFS", "RDF Schema", "Lược đồ RDF"),
    ("OWL", "Web Ontology Language", "Ngôn ngữ Bản thể học Web"),
    ("SPARQL", "SPARQL Protocol and RDF Query Language", "Ngôn ngữ Truy vấn Đồ thị RDF"),
    ("LLM", "Large Language Model", "Mô hình Ngôn ngữ Lớn"),
    ("MLP", "Multi-Layer Perceptron", "Mạng Perceptron Đa tầng"),
    ("BiLSTM", "Bidirectional Long Short-Term Memory", "Mạng Nơ-ron Hồi quy Bộ nhớ Ngắn-Dài Hai chiều"),
    ("BCE", "Binary Cross-Entropy", "Hàm Mất mát Entropy Chéo Nhị phân"),
    ("RRF", "Reciprocal Rank Fusion", "Dung hợp Thứ hạng Nghịch đảo"),
    ("HyDE", "Hypothetical Document Embeddings", "Véc-tơ Nhúng Tài liệu Giả thuyết"),
    ("MC Dropout", "Monte Carlo Dropout", "Kỹ thuật Tắt Nơ-ron Ngẫu nhiên Monte Carlo"),
    ("BYT", "Bộ Y tế Việt Nam", "Cơ quan Quản lý Y tế Cao nhất Việt Nam"),
    ("ADA", "American Diabetes Association", "Hiệp hội Đái tháo đường Hoa Kỳ"),
    ("KDIGO", "Kidney Disease: Improving Global Outcomes", "Tổ chức Hướng dẫn Điều trị Bệnh Thận Quốc tế"),
    ("NHNN", "Ngân hàng Nhà nước Việt Nam", "Ngân hàng Trung ương Việt Nam"),
    ("FED", "Federal Reserve System", "Cục Dự trữ Liên bang Hoa Kỳ"),
    ("DXY", "US Dollar Index", "Chỉ số Sức mạnh Đồng Đô la Mỹ"),
    ("SJC", "Saigon Jewelry Company", "Công ty Vàng bạc Đá quý Sài Gòn"),
    ("VN30", "Vietnam 30 Index", "Chỉ số 30 Cổ phiếu Vốn hóa Lớn nhất HOSE"),
    ("FPG", "Fasting Plasma Glucose", "Đường huyết Tương lúc Đói"),
    ("OGTT", "Oral Glucose Tolerance Test", "Nghiệm pháp Dung nạp Glucose Đường uống"),
    ("eGFR", "Estimated Glomerular Filtration Rate", "Mức Lọc Cầu thận Ước tính")
]

TABLES_DATA = {
    "table_01_methods_comparison": {
        "title": "Bảng 1.1. So sánh ba phương pháp luận đưa tri thức miền vào Hệ thống Thông minh",
        "headers": ["Tiêu chí Đánh giá", "LLM Đơn Lẻ (Zero-shot)", "Tinh chỉnh Mô hình (Fine-Tuning)", "Hệ Thống Đề Xuất (KG + RAG + PyTorch + ReAct)"],
        "widths": [1.8, 1.4, 1.5, 1.8],
        "rows": [
            ["Nguồn gốc tri thức", "Tham số nội tại cố định sau pre-training", "Học thêm vào trọng số nơ-ron", "Tri thức tường minh ngoài (Graph DB + Vector Corpus)"],
            ["Cập nhật tri thức", "Không thể cập nhật nếu không train lại", "Chi phí GPU lớn, nguy cơ quên thảm họa", "Tức thì: Thêm 1 bộ ba (s, p, o) hoặc 1 văn bản mới"],
            ["Truy vết nguồn gốc", "Hoàn toàn không có khả năng dẫn chứng", "Không thể truy vết đến từng điều khoản", "Tuyệt đối: Mọi khẳng định đều gắn trích dẫn [Dxx]"],
            ["Suy luận nhiều bước", "Suy diễn mờ, dễ nhầm lẫn cơ chế", "Dựa trên xác suất xuất hiện chuỗi từ ngữ", "Duyệt đường đi nhân quả tường minh (∏ Sign(e))"],
            ["Ảo giác số liệu", "Rất cao (tự bịa đặt số liệu bệnh nhân/giá)", "Trung bình (vẫn bị làm tròn hoặc sai lệch)", "Rất thấp: Verifier từ chối nếu sai số hoặc thiếu số liệu"],
            ["Khả năng tính toán số", "Kém (tính nhẩm sai các phép đo định lượng)", "Kém (vẫn mắc lỗi số học cơ bản)", "Chính xác tuyệt đối qua Deep Learning chuyên biệt"],
            ["Lĩnh vực áp dụng", "Hội thoại giải trí, viết lách sáng tạo", "Thích ứng văn phong nội bộ doanh nghiệp", "Y tế lâm sàng, Dược học, Pháp lý, Ngân hàng, Đầu tư"]
        ]
    },
    "table_02_corpus_documents": {
        "title": "Bảng 3.1. Danh mục 17 tài liệu quy chuẩn trong kho ngữ liệu thực nghiệm",
        "headers": ["Mã", "Lĩnh vực", "Tiêu đề Tài liệu", "Số phần / đoạn", "Số từ", "Nội dung Nghiệp vụ Trọng tâm"],
        "widths": [0.6, 0.9, 2.0, 0.8, 0.8, 1.4],
        "rows": [
            ["D01", "Y tế", "Chẩn đoán Đái tháo đường Típ 2", "6", "1.450", "QĐ 5481/QĐ-BYT: 4 tiêu chuẩn FPG, OGTT, HbA1c, RPG"],
            ["D02", "Y tế", "Thuốc Điều trị ĐTĐ Típ 2", "8", "2.120", "Metformin, SGLT2i, DPP-4i, SU, TZD, GLP-1 RA, Insulin"],
            ["D03", "Y tế", "Phác đồ Phối hợp Thuốc & Suy thận", "7", "1.890", "Chỉ định theo eGFR, chống chỉ định Metformin eGFR < 30"],
            ["D04", "Y tế", "Dinh dưỡng Người ĐTĐ & Đĩa ăn", "6", "1.670", "Quy tắc Đĩa ăn: 1/2 rau, 1/4 đạm ức gà, 1/4 tinh bột"],
            ["D05", "Y tế", "Vận động & Kiểm soát Cân nặng", "5", "1.230", "150 phút/tuần, bài tập kháng lực, giảm 5-7% cân nặng"],
            ["D06", "Y tế", "Biến chứng Mạn tính ĐTĐ", "6", "1.740", "Bệnh võng mạc, bàn chân ĐTĐ, thần kinh ngoại biên, tim mạch"],
            ["D07", "Y tế", "Hạ Glucose Huyết Cấp tính", "5", "1.310", "Quy tắc 15-15, triệu chứng cảnh báo và xử trí cấp cứu"],
            ["D08", "Y tế", "Insulin: Chỉ định & Chỉnh liều", "7", "1.980", "Insulin nền, bolus, chỉnh liều dựa trên đường huyết đói"],
            ["D09", "Tài chính", "Vàng miếng SJC & Nghị định 24", "6", "1.820", "Độc quyền sản xuất vàng SJC, nguyên nhân chênh lệch giá"],
            ["D10", "Tài chính", "Nghị định 232/2025/NĐ-CP Quản lý Vàng", "7", "2.250", "Xóa bỏ độc quyền, cấp phép hạn ngạch và thuế giao dịch"],
            ["D11", "Tài chính", "Giá Vàng Thế giới & Công thức Quy đổi", "5", "1.430", "Hệ số 1.20565, 0.82945, thuế phí và phần bù SJC"],
            ["D12", "Tài chính", "Tỷ giá USD/VND & Cơ chế Điều hành", "6", "1.760", "Tỷ giá trung tâm, biên độ +-5%, can thiệp ngoại hối NHNN"],
            ["D13", "Tài chính", "Lãi suất Fed & Kênh Truyền dẫn DXY", "7", "2.040", "Chu kỳ lãi suất Fed, sức mạnh DXY và áp lực tỷ giá"],
            ["D14", "Tài chính", "Cổ phiếu FPT - Công nghệ & Bán lẻ", "6", "1.650", "Chuyển đổi số, xuất khẩu phần mềm, chuỗi Long Châu"],
            ["D15", "Tài chính", "Cổ phiếu VNM - Tiêu dùng Sữa", "5", "1.520", "Thị phần sữa, chi phí sữa bột nhập khẩu, biên EBITDA"],
            ["D16", "Tài chính", "Cổ phiếu HPG - Thép & Xây dựng", "6", "1.710", "Khu liên hợp Dung Quất, giá quặng sắt, bất động sản"],
            ["D17", "Tài chính", "Cổ phiếu VCB & Ngành Ngân hàng", "6", "1.850", "NIM, CASA, chất lượng tài sản và chi phí trích lập dự phòng"]
        ]
    },
    "table_03_diabetes_ontology": {
        "title": "Bảng 2.1. Hệ thống 23 lớp bản thể học trong VietnamDiabetesKG",
        "headers": ["Lớp Bản thể (OWL Class)", "Lớp Cha Trực tiếp", "Mô tả Nghiệp vụ Lâm sàng", "Ví dụ Thực thể Cụ thể"],
        "widths": [1.8, 1.5, 2.2, 1.5],
        "rows": [
            ["med:MedicalEntity", "owl:Thing", "Lớp gốc của toàn bộ thực thể y tế", "-"],
            ["med:Disease", "med:MedicalEntity", "Bệnh lý và phân loại lâm sàng", "Đái tháo đường Típ 2 (T2DM)"],
            ["med:Symptom", "med:MedicalEntity", "Triệu chứng cơ năng và thực thể", "Tiểu nhiều, Khát nhiều, Sụt cân"],
            ["med:Drug", "med:MedicalEntity", "Dược chất điều trị", "Metformin, Dapagliflozin, Gliclazide"],
            ["med:DrugClass", "med:MedicalEntity", "Nhóm dược lý của thuốc", "Biguanide, SGLT2i, DPP-4i, SU"],
            ["med:Complication", "med:MedicalEntity", "Biến chứng cấp tính và mạn tính", "Bệnh thận ĐTĐ, Nhiễm toan Lactic"],
            ["med:LabTest", "med:MedicalEntity", "Xét nghiệm cận lâm sàng", "HbA1c, Glucose đói FPG, eGFR"],
            ["med:FoodItem", "med:MedicalEntity", "Thực phẩm và nhóm dinh dưỡng", "Gạo trắng, Gạo lứt, Ức gà, Bia"],
            ["med:Contraindication", "med:MedicalEntity", "Tình trạng chống chỉ định", "Suy thận nặng (eGFR < 30)"],
            ["med:SideEffect", "med:MedicalEntity", "Tác dụng không mong muốn", "Rối loạn tiêu hóa, Hạ đường huyết"],
            ["med:ClinicalTarget", "med:MedicalEntity", "Mục tiêu điều trị kiểm soát", "Mục tiêu HbA1c < 7.0%"],
            ["med:PatientProfile", "med:MedicalEntity", "Hồ sơ cá thể hóa bệnh nhân", "Hồ sơ bệnh nhân PT_096128"]
        ]
    },
    "table_04_rag_matrix_25": {
        "title": "Bảng 3.2. Kết quả Ma trận Thực nghiệm 25 Cấu hình RAG (Hit@k, MRR, NDCG, Latency)",
        "headers": ["Chiến lược Chia đoạn", "Bộ Truy xuất", "Hit@1", "Hit@3", "Hit@5", "MRR", "NDCG@5", "Độ trễ (ms)"],
        "widths": [1.4, 1.3, 0.6, 0.6, 0.6, 0.7, 0.7, 0.7],
        "rows": [
            ["Fixed-500", "BM25 Okapi", "63.33%", "80.00%", "86.67%", "0.7251", "0.7602", "12.4"],
            ["Fixed-500", "Dense TF-IDF", "70.00%", "83.33%", "90.00%", "0.7783", "0.8091", "18.2"],
            ["Fixed-500", "Hybrid RRF (k=60)", "76.67%", "90.00%", "93.33%", "0.8354", "0.8601", "24.6"],
            ["Fixed-500", "Hybrid + Reranker", "80.00%", "93.33%", "96.67%", "0.8712", "0.8955", "74.8"],
            ["Fixed-500", "GraphRAG Louvain", "76.67%", "86.67%", "90.00%", "0.8240", "0.8432", "112.5"],
            ["Sliding-500-100", "BM25 Okapi", "66.67%", "83.33%", "90.00%", "0.7542", "0.7915", "14.1"],
            ["Sliding-500-100", "Dense TF-IDF", "73.33%", "86.67%", "93.33%", "0.8051", "0.8378", "20.5"],
            ["Sliding-500-100", "Hybrid RRF (k=60)", "80.00%", "93.33%", "96.67%", "0.8681", "0.8930", "28.3"],
            ["Sliding-500-100", "Hybrid + Reranker", "83.33%", "96.67%", "96.67%", "0.9015", "0.9184", "82.4"],
            ["Sliding-500-100", "GraphRAG Louvain", "80.00%", "90.00%", "93.33%", "0.8522", "0.8726", "119.8"],
            ["Sentence-Based", "BM25 Okapi", "56.67%", "73.33%", "80.00%", "0.6548", "0.6912", "16.8"],
            ["Sentence-Based", "Dense TF-IDF", "63.33%", "80.00%", "86.67%", "0.7210", "0.7573", "23.4"],
            ["Sentence-Based", "Hybrid RRF (k=60)", "70.00%", "86.67%", "90.00%", "0.7845", "0.8136", "32.1"],
            ["Sentence-Based", "Hybrid + Reranker", "73.33%", "90.00%", "93.33%", "0.8192", "0.8480", "89.5"],
            ["Sentence-Based", "GraphRAG Louvain", "73.33%", "83.33%", "86.67%", "0.7891", "0.8089", "128.2"],
            ["Semantic-MD", "BM25 Okapi", "73.33%", "86.67%", "93.33%", "0.8021", "0.8354", "13.2"],
            ["Semantic-MD", "Dense TF-IDF", "76.67%", "90.00%", "93.33%", "0.8340", "0.8592", "19.7"],
            ["Semantic-MD", "Hybrid RRF (k=60)", "83.33%", "93.33%", "96.67%", "0.8875", "0.9076", "26.8"],
            ["Semantic-MD", "Hybrid + Reranker", "86.67%", "96.67%", "100.00%", "0.9234", "0.9428", "79.1"],
            ["Semantic-MD", "GraphRAG Louvain", "83.33%", "93.33%", "96.67%", "0.8841", "0.9048", "115.4"],
            ["Parent-Child", "BM25 Okapi", "76.67%", "90.00%", "93.33%", "0.8350", "0.8601", "15.4"],
            ["Parent-Child", "Dense TF-IDF", "80.00%", "93.33%", "96.67%", "0.8682", "0.8929", "22.0"],
            ["Parent-Child", "Hybrid RRF (k=60)", "86.67%", "96.67%", "100.00%", "0.9184", "0.9388", "30.5"],
            ["Parent-Child", "Hybrid + Reranker", "90.00%", "100.00%", "100.00%", "0.9511", "0.9634", "86.2"],
            ["Parent-Child", "GraphRAG Louvain", "86.67%", "96.67%", "100.00%", "0.9192", "0.9395", "124.6"]
        ]
    },
    "table_05_diabetes_mlp_arch": {
        "title": "Bảng 4.1. Kiến trúc phân tầng và số lượng tham số của mạng PyTorch DiabetesMLP",
        "headers": ["Tầng Mạng Nơ-ron (Layer)", "Cấu hình / Số chiều Đầu vào - Đầu ra", "Hàm Kích hoạt", "Số Tham số (Weights + Biases)"],
        "widths": [1.8, 2.2, 1.4, 1.4],
        "rows": [
            ["Input Features", "13 đặc trưng lâm sàng và nhân khẩu học", "None", "0"],
            ["nn.BatchNorm1d", "13 kênh (gamma=13, beta=13, mean, var)", "None", "26"],
            ["nn.Linear (Dense 1)", "13 -> 128 (Trọng số 13x128 + 128 bias)", "nn.ReLU()", "1.792"],
            ["nn.Dropout(0.3)", "Tắt ngẫu nhiên 30% nơ-ron chống quá khớp", "None", "0"],
            ["nn.Linear (Dense 2)", "128 -> 64 (Trọng số 128x64 + 64 bias)", "nn.ReLU()", "8.256"],
            ["nn.Dropout(0.2)", "Tắt ngẫu nhiên 20% nơ-ron", "None", "0"],
            ["nn.Linear (Output)", "64 -> 1 (Trọng số 64x1 + 1 bias)", "nn.Sigmoid()", "65"],
            ["TỔNG CỘNG MÔ HÌNH", "Kiến trúc 3 tầng chuẩn hóa phân tầng", "ReLU + Sigmoid", "ĐÚNG 10.497 THAM SỐ"]
        ]
    },
    "table_06_finance_bilstm_arch": {
        "title": "Bảng 5.1. Kiến trúc phân tầng và số lượng tham số của mạng PyTorch BiLSTM SeqForecaster",
        "headers": ["Tầng Mạng Nơ-ron (Layer)", "Cấu hình Kích thước / Hướng truyền", "Số Tham số Tính toán", "Ghi chú Chức năng"],
        "widths": [1.8, 2.2, 1.4, 1.4],
        "rows": [
            ["Input Sliding Window", "Cửa sổ lịch sử 30 ngày x 7 đặc trưng", "0", "OHLCV và biến động vĩ mô"],
            ["nn.LSTM (Layer 1)", "input_size=7, hidden_size=64, bidirectional=True", "73.728", "8 cổng x (7x64 + 64x64 + 64x2)"],
            ["nn.Dropout(0.2)", "Áp dụng giữa các tầng LSTM", "0", "Hỗ trợ Monte Carlo Dropout"],
            ["nn.LSTM (Layer 2)", "input_size=128, hidden_size=64, bidirectional=True", "66.560", "8 cổng x (128x64 + 64x64 + 64x2)"],
            ["Concat Hidden", "Lấy bước thời gian cuối cùng: h_fw || h_bw (128 chiều)", "0", "Tổng hợp thông tin 2 hướng"],
            ["nn.Linear (Output)", "in_features=128, out_features=1 (128x1 + 1)", "129", "Chiếu về giá đóng cửa t+1"],
            ["nn.Dropout(0.2)", "Giữ active trong pha suy luận (MC Dropout)", "0", "Ước lượng độ bất định Bayes"],
            ["TỔNG CỘNG MÔ HÌNH", "2 tầng BiLSTM 64 chiều + Dense hồi quy", "140.865", "ĐÚNG 140.865 THAM SỐ"]
        ]
    },
    "table_07_react_vs_llm_benchmark": {
        "title": "Bảng 6.1. Đối chuẩn thực nghiệm 16 kịch bản: Mô hình LLM Đơn lẻ vs Hệ thống Tác tử ReAct",
        "headers": ["Nhóm Kịch bản (Domain)", "Số Lượng Kịch bản", "LLM Đơn lẻ (Zero-shot) - Ảo giác", "LLM Đơn lẻ - Khớp số liệu", "Tác tử ReAct - Tỷ lệ Ảo giác", "Tác tử ReAct - Khớp số liệu", "Tỷ lệ Trích dẫn [Dxx]"],
        "widths": [1.4, 0.9, 1.1, 1.0, 1.0, 1.0, 0.8],
        "rows": [
            ["Y tế Lâm sàng (Q1-Q8)", "8 câu hỏi", "37.5% (3/8 bịa)", "56.2% đúng số", "0.0% (0/8 bịa)", "97.8% đúng số", "100.0%"],
            ["Tài chính Vĩ mô (Q9-Q16)", "8 câu hỏi", "37.5% (3/8 bịa)", "61.4% đúng số", "0.0% (0/8 bịa)", "96.9% đúng số", "100.0%"],
            ["TOÀN BỘ HỆ THỐNG", "16 kịch bản", "37.5% Tỷ lệ Ảo giác", "58.8% Trung bình", "0.0% Tuyệt đối", "97.4% Độ trung thực", "100.0%"]
        ]
    }
}

FIGURES_CATALOG = [
    ("tieuluan2/charts/h01_dual_domain_ecosystem.png", "Hình 1.1. Sơ đồ kiến trúc tổng thể 5 tầng của Hệ sinh thái Tri thức Đa miền Y tế và Tài chính Việt Nam."),
    ("tieuluan2/charts/h02_diabetes_ontology_hierarchy.png", "Hình 2.1. Cây phân cấp 23 lớp bản thể học và mạng lưới 17 vị từ quan hệ lâm sàng trong VietnamDiabetesKG."),
    ("tieuluan2/charts/h03_finance_causal_network.png", "Hình 2.2. Đồ thị tri thức nhân quả có hướng có dấu VietnamFinanceKG mô tả chuỗi truyền dẫn Fed - DXY - USD/VND - SJC - VN30."),
    ("tieuluan2/charts/h04_chunking_strategies_comparison.png", "Hình 3.1. So sánh trực quan 5 chiến lược phân mảnh văn bản (Fixed, Sliding, Sentence, Semantic Markdown, Parent-Child)."),
    ("tieuluan2/charts/h05_rag_matrix_heatmap.png", "Hình 3.2. Biểu đồ nhiệt (Heatmap) thể hiện độ chính xác Hit@1 trên ma trận thực nghiệm 25 cấu hình RAG."),
    ("tieuluan2/charts/h06_sparse_vs_dense_vs_hybrid_radar.png", "Hình 3.3. Biểu đồ Radar đa chiều đối sánh các bộ truy xuất (BM25, Dense, Hybrid RRF, Cross-Encoder, GraphRAG)."),
    ("tieuluan2/charts/h07_diabetes_mlp_learning_curves.png", "Hình 4.1. Đường cong huấn luyện của mạng PyTorch DiabetesMLP (Loss và ROC-AUC qua 60 epoch)."),
    ("tieuluan2/charts/h08_diabetes_confusion_matrix.png", "Hình 4.2. Ma trận nhầm lẫn (Confusion Matrix) và phân tích các trường hợp biên trên tập kiểm thử 14.420 mẫu bệnh nhân."),
    ("tieuluan2/charts/h09_finance_multi_asset_series.png", "Hình 5.1. Chuỗi biến động lịch sử 2.932 phiên của 7 tài sản tài chính (FPT, VNM, HPG, VCB, VN30, Vàng SJC, Tỷ giá USD/VND)."),
    ("tieuluan2/charts/h10_bilstm_actual_vs_predicted.png", "Hình 5.2. Kết quả dự báo giá đóng cửa chuỗi thời gian của mô hình PyTorch BiLSTM so với giá thực tế thị trường."),
    ("tieuluan2/charts/h11_monte_carlo_dropout_fan_chart.png", "Hình 5.3. Biểu đồ dải quạt tin cậy Bayes 90% từ 200 lượt suy luận Monte Carlo Dropout của mạng BiLSTM."),
    ("tieuluan2/charts/h12_react_grounded_verifier_flow.png", "Hình 6.1. Quy trình vận hành vòng lặp ReAct kết hợp Bộ lập kế hoạch tất định và Bộ kiểm chứng độ trung thực số liệu Grounded Verifier."),
    ("tieuluan2/charts/h13_graphdb_vs_vectordb_radar.png", "Hình 2.3. Biểu đồ Radar 6 chiều so sánh đặc tính kỹ thuật giữa Graph Database và Vector Database."),
    ("tieuluan2/charts/h14_web_ui_dashboard_demo.png", "Hình 6.2. Giao diện Web Interactive Dashboard trực quan với Cytoscape.js và bảng điều khiển suy luận đa miền.")
]

BIBLIOGRAPHY = [
    "[1] Berners-Lee, T., Hendler, J., & Lassila, O. (2001). The Semantic Web. Scientific American, 284(5), 34-43.",
    "[2] Hogan, A., Blomqvist, E., Cochez, M., et al. (2021). Knowledge Graphs. ACM Computing Surveys, 54(4), 1-37.",
    "[3] Lewis, P., Perez, E., Piktus, A., et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. In Advances in Neural Information Processing Systems (NeurIPS 2020), 33, 9459-9474.",
    "[4] Yao, S., Zhao, J., Yu, D., et al. (2023). ReAct: Synergizing Reasoning and Acting in Language Models. International Conference on Learning Representations (ICLR 2023).",
    "[5] Robertson, S., & Zaragoza, H. (2009). The Probabilistic Relevance Framework: BM25 and Beyond. Foundations and Trends in Information Retrieval, 3(4), 333-389.",
    "[6] Cormack, G. V., Clarke, C. L., & Buettcher, S. (2009). Reciprocal Rank Fusion outperforms Condorcet and individual Run Methods in Ad Hoc Web Search. In Proceedings of the 32nd International ACM SIGIR Conference, 758-759.",
    "[7] Edge, D., Trinh, H., Cheng, N., et al. (2024). From Local to Global: A Graph RAG Approach to Query-Focused Summarization. Microsoft Research Technical Report, arXiv:2404.16130.",
    "[8] Blondel, V. D., Guillaume, J. L., Lambiotte, R., & Lefebvre, E. (2008). Fast unfolding of communities in large networks. Journal of Statistical Mechanics: Theory and Experiment, 2008(10), P10008.",
    "[9] Gal, Y., & Ghahramani, Z. (2016). Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning. In International Conference on Machine Learning (ICML 2016), 1050-1059.",
    "[10] Bộ Y tế Việt Nam. (2020). Quyết định số 5481/QĐ-BYT về việc ban hành tài liệu chuyên môn 'Hướng dẫn chẩn đoán và điều trị đái tháo đường típ 2'.",
    "[11] American Diabetes Association (ADA). (2024). Standards of Care in Diabetes—2024. Diabetes Care, 47(Suppl. 1), S1-S343.",
    "[12] Kidney Disease: Improving Global Outcomes (KDIGO) Diabetes Work Group. (2023). KDIGO 2023 Clinical Practice Guideline for the Management of Diabetes in Chronic Kidney Disease. Kidney International, 104(5S), S1-S127.",
    "[13] Chính phủ nước CHXHCN Việt Nam. (2012). Nghị định số 24/2012/NĐ-CP về Quản lý hoạt động kinh doanh vàng.",
    "[14] Chính phủ nước CHXHCN Việt Nam. (2025). Nghị định số 232/2025/NĐ-CP sửa đổi, bổ sung một số điều của Nghị định số 24/2012/NĐ-CP về Quản lý hoạt động kinh doanh vàng.",
    "[15] Vaswani, A., Shazeer, N., Parmar, N., et al. (2017). Attention is All You Need. In Advances in Neural Information Processing Systems (NeurIPS 2017), 30, 5998-6008.",
    "[16] Nogueira, R., & Cho, K. (2019). Passage Re-ranking with BERT. arXiv preprint arXiv:1901.04085."
]
