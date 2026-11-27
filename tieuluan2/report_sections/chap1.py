"""
Chapter 1: Mở đầu về Knowledge Graph và RAG
Comprehensive Academic Treatise - Standalone Independent Research
Author: Tran Van Hau - Student ID: B23DCCN287 - PTIT
"""

CHAP1_DATA = {
    "chapter_num": 1,
    "chapter_title": "CHƯƠNG 1: MỞ ĐẦU VỀ KNOWLEDGE GRAPH VÀ RAG",
    "intro_text": """
Chương này thiết lập nền tảng lý thuyết và phương pháp luận cho toàn bộ công trình nghiên cứu: Đồ thị tri thức (Knowledge Graph - KG) là gì, Kỹ thuật Sinh tăng cường truy xuất (Retrieval-Augmented Generation - RAG) là gì, vì sao sự kết hợp hữu cơ giữa hai kỹ thuật này lại giải quyết trúng và triệt để các tử huyệt cố hữu của các Mô hình Ngôn ngữ Lớn (LLM), và chúng được tích hợp với nhau như thế nào trong kiến trúc hệ sinh thái thông minh 5 tầng được đề xuất.
""",
    "sections": [
        {
            "num": "1.1",
            "title": "1.1 Bối cảnh và Thách thức Cốt tử của Trí tuệ Nhân tạo Hiện đại",
            "text": """
Sự bùng nổ của Trí tuệ Nhân tạo Tạo sinh (Generative AI) từ cuối năm 2022 với sự thống trị của các Mô hình Ngôn ngữ Lớn (Large Language Models - LLM) dựa trên kiến trúc Transformer đã tạo nên một bước ngoặt lịch sử trong Khoa học Máy tính. Các mô hình với quy mô hàng chục đến hàng trăm tỷ tham số (như GPT-4, LLaMA, Claude hay Qwen) đã chứng minh năng lực phi thường trong việc hiểu ngữ cảnh, tóm tắt tài liệu, dịch thuật và sinh văn bản tự nhiên trôi chảy gần như không thể phân biệt với con người.

Kiến trúc Transformer dựa trên cơ chế Tự chú ý Đa đầu (Multi-Head Self-Attention):
$$\\text{Attention}(Q, K, V) = \\text{softmax}\\left(\\frac{QK^T}{\\sqrt{d_k}}\\right)V$$
Trong đó các ma trận truy vấn (Query - $Q$), khóa (Key - $K$), và giá trị (Value - $V$) được tính toán từ các phép chiếu tuyến tính của vector nhúng từ vựng. Cơ chế này cho phép mô hình thu nhận các mối liên kết phụ thuộc ngữ nghĩa từ xa giữa các từ trong câu mà không bị giới hạn bởi độ dài tuần tự như các mạng hồi quy RNN truyền thống.

Tuy nhiên, khi chuyển giao các mô hình ngôn ngữ này từ các tác vụ giải trí, hội thoại thông thường sang các lĩnh vực nghiệp vụ có tính cam kết cao (High-Stakes Domains) và ràng buộc pháp lý nghiêm ngặt — tiêu biểu là **Y tế Lâm sàng** và **Phân tích Đầu tư Tài chính** tại Việt Nam — các hệ thống AI dựa trên LLM đơn lẻ lập tức bộc lộ ba "tử huyệt" mang tính bản chất:

1. **Hiện tượng Ảo giác (Hallucination)**: 
Mô hình Transformer được huấn luyện theo nguyên lý Cực đại hóa Hợp lý (Maximum Likelihood Estimation - MLE) để dự đoán phân phối xác suất của từ tiếp theo dựa trên chuỗi từ trước đó:
$$\\mathcal{L}_{\\text{MLE}}(\\theta) = - \\sum_{t=1}^T \\log P_\\theta(w_t \\mid w_1, w_2, \\dots, w_{t-1})$$
Mục tiêu toán học này tối ưu hóa "tính trôi chảy bề mặt" (Surface Fluency) và sự tương thích thống kê của ngôn ngữ, chứ **hoàn toàn không có cơ chế kiểm tra tính đúng đắn thực tế (Factual Correctness)**. Hàm kích hoạt Softmax ở tầng cuối cùng luôn buộc mô hình phải chuẩn hóa tổng xác suất trên toàn bộ từ điển từ vựng về 1:
$$P(w_t = v \\mid w_{<t}) = \\frac{\\exp(z_v / \\tau)}{\\sum_{j=1}^{|V|} \\exp(z_j / \\tau)}$$
(với $\\tau$ là nhiệt độ lấy mẫu). Điều này có nghĩa là ngay cả khi mô hình hoàn toàn không sở hữu tri thức về một sự kiện hoặc một con số, nó vẫn bị ép buộc phải gán một xác suất dương cho một từ nào đó và tiếp tục sinh văn bản.

Về mặt phân loại học thuật, ảo giác trong LLM được chia thành hai nhóm chính:
- *Ảo giác Dữ kiện (Factuality Hallucination)*: Mô hình sinh ra các phát biểu mâu thuẫn trực tiếp với tri thức thực tế của thế giới thực (Factual Inconsistency) hoặc tự bịa đặt ra các thực thể, con số, chỉ số xét nghiệm hoàn toàn không tồn tại (Factual Fabrication).
- *Ảo giác Độ trung thực (Faithfulness Hallucination)*: Mô hình không tuân thủ chỉ thị đầu vào (Instruction Inconsistency) hoặc sinh ra nội dung mâu thuẫn trực tiếp với tài liệu ngữ cảnh được cung cấp (Context Inconsistency).

Trong hai lĩnh vực của tiểu luận, hậu quả của ảo giác là khôn lường:
- *Trong Y tế Lâm sàng*: Một ảo giác về liều lượng thuốc hoặc chống chỉ định có thể tước đoạt sinh mạng bệnh nhân. Ví dụ: Nếu LLM tự ý khuyên bệnh nhân đái tháo đường típ 2 có mức lọc cầu thận eGFR = 25 mL/phút tiếp tục dùng Metformin liều cao (2000mg/ngày), bệnh nhân sẽ đối mặt với nguy cơ tích tụ acid lactic nghiêm trọng trong máu gây nhiễm toan lactic tử vong với tỷ lệ lên tới 50%.
- *Trong Đầu tư Tài chính*: Một ảo giác về số liệu lợi nhuận hoặc cơ chế quản lý tỷ giá có thể gây thiệt hại hàng trăm tỷ đồng cho nhà đầu tư. Ví dụ: Nếu LLM nhầm lẫn cơ chế định giá vàng theo Nghị định 24/2012 và Nghị định 232/2025/NĐ-CP, hoặc bịa ra mức tăng trưởng doanh thu quý của Tập đoàn Hòa Phát hay FPT, các thuật toán giao dịch tự động sẽ đưa ra quyết định giải ngân sai lầm nghiêm trọng.

2. **Thiếu Khả năng Truy vết Nguồn gốc và Minh bạch Pháp lý (Provenance & Traceability)**:
Một câu trả lời sinh ra từ các trọng số tiềm ẩn (Parametric Memory) của mạng nơ-ron là một chiếc "hộp đen" mờ đục. Mô hình không thể chứng minh con số "15 triệu đồng/lượng chênh lệch giá vàng" hay "ngưỡng HbA1c $\\ge 6.5\\%$" được trích xuất chính xác từ điều khoản nào trong văn bản pháp luật hay phác đồ điều trị nào của Bộ Y tế. Trong y khoa lâm sàng và tư vấn đầu tư chuyên nghiệp, một khuyến nghị không có khả năng dẫn chứng nguồn gốc cụ thể là hoàn toàn vô giá trị và vi phạm y đức cũng như quy định pháp luật.

3. **Độ trễ Tri thức Cố định và Chi phí Cập nhật Khổng lồ (Knowledge Cutoff & Recency Lag)**:
Tri thức trong tham số mạng nơ-ron bị đóng băng tuyệt đối tại thời điểm kết thúc quá trình tiền huấn luyện (Pre-training Cutoff). Khi cơ quan quản lý ban hành chính sách mới (ví dụ: Chính phủ ban hành Nghị định 232/2025/NĐ-CP sửa đổi cơ chế quản lý thị trường vàng), việc tái huấn luyện (re-training) hoặc tinh chỉnh (fine-tuning) một mô hình LLM khổng lồ tiêu tốn hàng trăm ngàn USD chi phí tính toán GPU, mất nhiều tuần thực thi và đối mặt với rủi ro "quên thảm họa" (Catastrophic Forgetting) đối với các tri thức đã học trước đó.
"""
        },
        {
            "num": "1.2",
            "title": "1.2 Sự Dung hợp Giữa Symbolic AI và Sub-Symbolic AI (Neuro-Symbolic Paradigm)",
            "text": """
Để giải quyết tận gốc các điểm nghẽn nêu trên, cộng đồng khoa học trí tuệ nhân tạo toàn cầu đang chứng kiến sự hội tụ mạnh mẽ về một mô hình kiến trúc mới: **Trí tuệ Nhân tạo Thần kinh - Tượng trưng (Neuro-Symbolic AI)**. Đây là sự kết hợp hữu cơ giữa hai trường phái đối nghịch trong lịch sử AI:

- **Trường phái Biểu tượng (Symbolic AI)**: Đại diện là các Hệ chuyên gia (Expert Systems), Cơ sở Tri thức Hình thức (Knowledge Bases), Bản thể học (Ontology) và Đồ thị Tri thức (Knowledge Graph). Trường phái này vận hành theo phương pháp **Suy luận Diễn dịch (Deductive Reasoning)**:
  $$\\text{Tri thức Hình thức (Rules + Triples)} + \\text{Dữ kiện Đầu vào (Facts)} \\xrightarrow{\\text{Inference Engine}} \\text{Kết luận Tất định (Truth)}$$
  *Ưu điểm*: Chính xác $100\\%$, minh bạch, có thể chứng minh hình thức, có khả năng giải thích từng bước suy luận, cập nhật tức thì với độ phức tạp $O(1)$.
  *Nhược điểm*: Cứng nhắc, không có khả năng xử lý ngôn ngữ tự nhiên mềm dẻo, khó biểu diễn các mối quan hệ mờ hoặc dữ liệu chuỗi thời gian liên tục.

- **Trường phái Phi biểu tượng (Sub-Symbolic AI / Connectionist AI)**: Đại diện là Mạng Nơ-ron Nhân tạo (Neural Networks), Học sâu (Deep Learning) và các Mô hình Ngôn ngữ Lớn (LLM). Vận hành theo phương pháp **Suy luận Quy nạp (Inductive Reasoning)**:
  $$\\text{Dữ liệu Lớn (Big Data)} \\xrightarrow{\\text{Gradient Descent}} \\text{Trọng số Tiềm ẩn (Weights)} \\xrightarrow{\\text{Inference}} \\text{Dự báo Xác suất (Probabilities)}$$
  *Ưu điểm*: Rất linh hoạt, có khả năng khái quát hóa cao, hiểu sâu sắc ngữ cảnh ngôn ngữ tự nhiên phức tạp, xử lý xuất sắc dữ liệu hình ảnh, tín hiệu và bảng số học.
  *Nhược điểm*: Mờ đục (Black-box), không đảm bảo tính đúng đắn logic, thường xuyên sinh ảo giác khi đối mặt với các suy luận đa bước.

**Mô hình Đề xuất trong Nghiên cứu này**:
Hệ thống được thiết kế dựa trên nguyên lý **Hợp nhất Bổ trợ Đa tầng**:
1. Đồ thị Tri thức (KG) đóng vai trò là "Bộ não Logic Tượng trưng": Lưu trữ cấu trúc bản thể học, quy tắc điều trị bất biến và đồ thị nhân quả vĩ mô, thực hiện suy diễn tiến (Forward Chaining) RDFS/OWL đóng kín điểm bất động.
2. Sinh Tăng cường Truy xuất (RAG) đóng vai trò là "Cầu nối Ngữ liệu Văn bản": Quét kho tài liệu pháp quy và chuyên môn chính thức để trích xuất các bằng chứng văn bản làm mỏ neo ngữ cảnh (Grounding Context).
3. Mạng Nơ-ron PyTorch đóng vai trò là "Công cụ Tính toán Định lượng": Trực tiếp dự báo nguy cơ lâm sàng (`DiabetesMLP`) và dự báo chuỗi thời gian kèm dải quạt tin cậy Bayes 90% (`BiLSTM SeqForecaster`).
4. Tác tử Lập luận ReAct đóng vai trò là "Nhạc trưởng Điều phối": Vận hành theo kế hoạch tất định, kết hợp kết quả từ cả ba phân hệ để sinh phản hồi tự nhiên, minh bạch và có kiểm chứng độ trung thực số liệu tự động.
"""
        },
        {
            "num": "1.3",
            "title": "1.3 Khái niệm Hình thức về Đồ thị Tri thức và RAG",
            "text": """
**1. Khái niệm Đồ thị Tri thức (Knowledge Graph - KG)**:
Về mặt toán học hình thức, một Đồ thị Tri thức $\\mathcal{G}$ được định nghĩa như một đồ thị có hướng, có nhãn đa quan hệ:
$$\\mathcal{G} = (\\mathcal{V}, \\mathcal{E}, \\mathcal{R}, \\mathcal{L}, \\tau_v, \\tau_e)$$
Trong đó:
- $\\mathcal{V} = \\mathcal{E}_{ent} \\cup \\mathcal{L}_{val} \\cup \\mathcal{B}_{blk}$ là tập hợp các đỉnh (nút), bao gồm các thực thể định danh duy nhất (Entities $\\mathcal{E}_{ent}$ qua URI), các giá trị hằng số nguyên tử (Literals $\\mathcal{L}_{val}$) và các nút ẩn danh (Blank nodes $\\mathcal{B}_{blk}$).
- $\\mathcal{R}$ là tập hợp hữu hạn các loại quan hệ ngữ nghĩa (vị từ - Predicates).
- $\\mathcal{E} \\subseteq \\mathcal{V} \\times \\mathcal{R} \\times \\mathcal{V}$ là tập hợp các cạnh có hướng biểu diễn các bộ ba RDF $(s, p, o)$.
- $\\tau_v, \\tau_e$ là các hàm ánh xạ kiểu ngữ nghĩa xác định bản thể học (Ontology Schema).

Khác biệt cơ bản giữa KG và Cơ sở dữ liệu quan hệ (RDBMS) là: Trong RDBMS, việc thêm một mối quan hệ mới đòi hỏi phải sửa đổi cấu trúc bảng cố định (`ALTER TABLE`), làm phát sinh các cột rỗng (NULL) và bùng nổ chi phí tính toán liên kết JOIN. Trong Đồ thị Tri thức, cấu trúc là hoàn toàn linh hoạt (Schema-flexible): Muốn biểu diễn một mối quan hệ mới chỉ cần thêm một cạnh có nhãn mới vào đồ thị. Hơn nữa, mỗi mẩu tri thức trong KG là một đơn vị nguyên tử độc lập (Atomic Fact), máy đọc hiểu trực tiếp và suy luận được.

**2. Khái niệm Sinh Tăng cường Truy xuất (Retrieval-Augmented Generation - RAG)**:
RAG phân tách bộ nhớ tiềm ẩn tham số của LLM với bộ nhớ ngoài phi tham số khổng lồ $\\mathcal{D} = \\{d_1, d_2, \\dots, d_M\\}$. Khi nhận câu hỏi truy vấn $q$, hệ thống thực hiện hai pha toán học:
- **Pha 1: Truy xuất Phân phối Xác suất (Retrieval Phase)**:
  Ước lượng phân phối xác suất liên quan $P(d \\mid q)$ trên toàn bộ kho tài liệu $\\mathcal{D}$, trích xuất tập top-$k$ đoạn văn bản có độ tương đồng cao nhất $\\mathcal{D}_q = \\{d_{(1)}, d_{(2)}, \\dots, d_{(k)}\\}$.
- **Pha 2: Sinh Văn bản Có Điều kiện Tăng cường (Augmented Generation Phase)**:
  Tích phân ngữ cảnh $\\mathcal{D}_q$ vào chuỗi sinh từ của mô hình ngôn ngữ:
  $$P(y \\mid q) = \\sum_{d \\in \\mathcal{D}_q} P(d \\mid q) \\prod_{t=1}^T P(y_t \\mid q, d, y_{1:t-1})$$
Nhờ công thức này, LLM chuyển vai trò từ "kẻ phỏng đoán xác suất" thành "chuyên gia tra cứu tài liệu và diễn giải", triệt tiêu phần lớn ảo giác ngữ nghĩa.

**3. Lịch sử Phát triển Nửa Thế kỷ của Tri thức Máy tính**:
- Thập niên 1960: Allan Quillian khởi xướng Mạng Ngữ nghĩa (Semantic Networks).
- Thập niên 1980: Douglas Lenat xây dựng đại dự án Cyc nhằm số hóa toàn bộ tri thức thường thức nhân loại thành logic bậc nhất.
- Năm 2001: Tim Berners-Lee và tổ chức W3C công bố Semantic Web với bộ tiêu chuẩn RDF, RDFS, OWL và SPARQL.
- Năm 2012: Google công bố Google Knowledge Graph với tôn chỉ "Things, not Strings", chính thức đưa đồ thị tri thức vào ứng dụng công nghiệp đại trà.
- Năm 2020: Lewis et al. và Karpukhin et al. công bố DPR và RAG tại hội nghị NeurIPS 2020.
- Năm 2024: Microsoft Research công bố GraphRAG, kết hợp thuật toán phân cụm Louvain trên đồ thị tri thức để giải quyết bài toán tóm tắt tri thức toàn cục.
"""
        },
        {
            "num": "1.4",
            "title": "1.4 Kiến trúc Tổng thể Hệ sinh thái Tri thức Đa miền 5 Tầng",
            "text": """
Toàn bộ hệ thống thông minh trong nghiên cứu này được tổ chức thành một Kiến trúc Doanh nghiệp 5 Tầng (5-Layer Enterprise Architecture) hoàn chỉnh, phân định rõ ràng trách nhiệm của từng phân hệ:

1. **Tầng 1: Tầng Dữ liệu và Ngữ liệu (Data & Corpus Layer)**:
   - Dữ liệu có cấu trúc định lượng: 96.128 hồ sơ bệnh nhân điện tử (EHR) với 13 đặc trưng lâm sàng và 2.932 phiên giao dịch lịch sử liên tục (2015-2026) của 7 tài sản tài chính.
   - Kho ngữ liệu văn bản phi cấu trúc: 17 tài liệu quy chuẩn kỹ thuật y tế và tài chính Việt Nam (D01 - D17) với tổng quy mô gần 30.000 từ.
2. **Tầng 2: Tầng Biểu diễn Tri thức (Knowledge Representation Layer)**:
   - Tri thức cấu trúc tượng trưng: VietnamDiabetesKG (23 lớp bản thể, 17 vị từ lâm sàng) và VietnamFinanceKG (16 lớp bản thể, 6 vị từ nhân quả có hướng có dấu), vận hành động cơ suy diễn tiến RDFS/OWL đến điểm bất động và 5 nhóm truy vấn SPARQL chuyên sâu.
   - Tri thức văn bản phân tán: Hệ thống chỉ mục truy xuất kép gồm Chỉ mục từ khóa thưa BM25 Okapi (tách từ tiếng Việt) và Không gian nhúng vector đa ngôn ngữ 768 chiều.
3. **Tầng 3: Tầng Mô hình Học sâu Chuyên biệt (Deep Learning Layer)**:
   - Mạng nơ-ron PyTorch `DiabetesMLP`: Gồm đúng 10.497 tham số, BatchNorm, Dropout, hàm mất mát Weighted BCE ($pos\\_weight=10.3$), hiệu chuẩn ngưỡng Youden J $\\tau=0.9016$, đạt ROC-AUC 0.9755.
   - Mạng nơ-ron PyTorch `BiLSTM SeqForecaster`: Gồm đúng 140.865 tham số, 2 tầng BiLSTM 64 chiều, Huber loss $\\delta=1.0$, tích hợp 200 lượt suy luận Monte Carlo Dropout sinh dải quạt tin cậy Bayes 90%.
4. **Tầng 4: Tầng Lập luận Tác tử và Kiểm chứng (Reasoning & Grounding Layer)**:
   - Bộ Lập kế hoạch Tất định (Deterministic Planner): Nhận diện thực thể, phân loại ý định, sinh đồ thị thực thi công cụ tuần tự (DAG), loại bỏ hoàn toàn cơ chế đa tác tử tự phát thiếu kiểm soát.
   - Vòng lặp ReAct (Thought $\\to$ Action $\\to$ Observation): Điều phối bộ 6 công cụ chuyên trách.
   - Bộ Kiểm chứng Độ trung thực Số liệu (Grounded Verifier): Chốt chặn kiểm định trích dẫn nguồn `[Dxx]` (100%) và kiểm toán số liệu định lượng bằng biểu thức chính quy ($\\text{Faithfulness} \\ge 85\\%$).
5. **Tầng 5: Tầng Trải nghiệm Người dùng (Presentation Layer)**:
   - Giao diện Web Interactive Dashboard phát triển bằng FastAPI, tích hợp đồ họa mạng lưới Cytoscape.js vật lý tương tác thời gian thực, bảng tính lâm sàng và biểu đồ dải quạt rủi ro Chart.js.
"""
        }
    ]
}
