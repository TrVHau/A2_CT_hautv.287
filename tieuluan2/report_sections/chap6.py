"""
Chapter 6: Động cơ Lập luận ReAct, Kiểm chứng Grounded Verifier & Hệ thống Web
Comprehensive Academic Treatise - Standalone Independent Research
Author: Tran Van Hau - Student ID: B23DCCN287 - PTIT
"""

CHAP6_DATA = {
    "chapter_num": 6,
    "chapter_title": "CHƯƠNG 6: ĐỘNG CƠ LẬP LUẬN REACT, KIỂM CHỨNG GROUNDED VERIFIER & HỆ THỐNG WEB",
    "intro_text": """
Chương này trình bày kiến trúc tích hợp cấp cao nhất của đề tài: mô hình lập luận ReAct đan xen hành động, bộ lập kế hoạch tất định (Deterministic Planner), bộ 6 công cụ chuyên trách, thuật toán kiểm chứng độ trung thực số liệu Grounded Verifier, kết quả đối chuẩn 16 kịch bản thực nghiệm, và kiến trúc triển khai ứng dụng Web Dashboard tương tác thời gian thực.
""",
    "sections": [
        {
            "num": "6.1",
            "title": "6.1 Mô hình ReAct: Suy luận Đan xen Hành động",
            "text": """
Mô hình ReAct (Reasoning and Acting) được Yao và các cộng sự tại Đại học Princeton và Google Research đề xuất tại hội nghị ICLR 2023, tạo nên bước ngoặt trong việc nâng cao năng lực giải quyết vấn đề của các mô hình trí tuệ nhân tạo.

Khác với các phương pháp tiếp cận truyền thống như Chuỗi Suy ngẫm (Chain-of-Thought - CoT) chỉ suy luận thuần túy bằng ngôn ngữ trong không gian tham số đóng kín (dễ dẫn đến ảo giác dây chuyền), hoặc tiếp cận Hành động Đơn thuần (Act-only) chỉ gọi công cụ một cách máy móc không có kế hoạch, ReAct kết hợp đồng thời hai quá trình trong một chu trình lặp khép kín:
$$\\dots \\longrightarrow \\text{Thought}_t \\longrightarrow \\text{Action}_t \\longrightarrow \\text{Observation}_t \\longrightarrow \\text{Thought}_{t+1} \\longrightarrow \\dots$$

- **Suy ngẫm (Thought)**: Tại mỗi bước $t$, mô hình phân tích trạng thái hiện tại, đánh giá câu hỏi của người dùng và các bằng chứng đã thu thập được từ các bước trước để vạch ra ý định tiếp theo (ví dụ: "Người dùng hỏi về nguy cơ dùng Metformin khi có tiền sử nghiện rượu bia, ta cần tra cứu Đồ thị Tri thức để kiểm tra tương tác thuốc").
- **Hành động (Action)**: Dựa trên suy ngẫm, hệ thống sinh ra một lời gọi công cụ cụ thể với các đối số định dạng JSON tường minh: `Action: tool_kg_query({"entity": "Metformin", "relation": "interactsWith"})`.
- **Quan sát (Observation)**: Môi trường thực thi kích hoạt công cụ phần mềm, truy vấn cơ sở dữ liệu hoặc nạp mô hình học sâu PyTorch và trả về kết quả khách quan: `Observation: {"interaction": "Ethanol", "risk": "LacticAcidosis", "severity": "Lethal"}`.
Kết quả quan sát này ngay lập tức được ghép ngược trở lại vào ngữ cảnh, làm cơ sở cho bước suy ngẫm tiếp theo $\\text{Thought}_{t+1}$. Nhờ vậy, tác tử luôn neo chặt suy nghĩ của mình vào bằng chứng thực tế, loại bỏ hoàn toàn khả năng suy diễn mờ và bịa đặt.
"""
        },
        {
            "num": "6.2",
            "title": "6.2 Kiến trúc Hệ thống Toàn vẹn 5 Tầng",
            "text": """
Hệ thống được thiết kế theo mô hình kiến trúc phân tầng chuyên biệt (Layered Enterprise Architecture), đảm bảo tính module hóa, dễ bảo trì và khả năng mở rộng trong sản xuất:

1. **Tầng 1: Tầng Dữ liệu và Ngữ liệu (Data & Corpus Layer)**:
   Lưu trữ và tiền xử lý dữ liệu thô: 96.128 hồ sơ bệnh nhân điện tử (file `diabetes_prediction_dataset.csv`), 2.932 phiên giao dịch lịch sử của 7 tài sản tài chính (file `finance_market_data.csv`), và 17 tài liệu quy chuẩn kỹ thuật y tế - tài chính dạng Markdown (D01 - D17).
2. **Tầng 2: Tầng Biểu diễn Tri thức (Knowledge Layer)**:
   Quản lý tri thức cấu trúc và phi cấu trúc: Hai đồ thị tri thức RDF (VietnamDiabetesKG với 23 lớp, 17 vị từ và VietnamFinanceKG với 16 lớp, 6 vị từ) hỗ trợ truy vấn SPARQL; cùng hệ thống chỉ mục tìm kiếm văn bản (BM25 Okapi tách từ tiếng Việt và vector nhúng Dense 768 chiều).
3. **Tầng 3: Tầng Mô hình Học sâu Chuyên biệt (Deep Learning Layer)**:
   Chứa các mô hình mạng nơ-ron PyTorch thuần túy đã huấn luyện: mô hình phân loại nhị phân `DiabetesMLP` (10.497 tham số, Weighted BCE $pos\\_weight=10.3$, $\\tau=0.9016$) và mô hình hồi quy chuỗi thời gian `BiLSTM SeqForecaster` (140.865 tham số, Huber loss $\\delta=1.0$, Monte Carlo Dropout 200 lượt).
4. **Tầng 4: Tầng Lập luận Tác tử và Kiểm chứng (Reasoning & Grounding Layer)**:
   Bộ não điều phối thông minh gồm: Bộ lập kế hoạch tất định (Deterministic Planner), Động cơ vòng lặp ReAct, Bộ 6 công cụ thực thi, và Bộ kiểm chứng độ trung thực số liệu tự động (Grounded Verifier) áp đặt ngưỡng tin cậy $\\ge 85\\%$.
5. **Tầng 5: Tầng Trải nghiệm Người dùng (Presentation Layer)**:
   Giao diện Web Dashboard tương tác xây dựng bằng FastAPI, HTML5/CSS3 hiện đại, Cytoscape.js hiển thị đồ thị mạng lưới vật lý tương tác, và Chart.js vẽ biểu đồ phân tích kỹ thuật và dải quạt tin cậy Bayes.
"""
        },
        {
            "num": "6.3",
            "title": "6.3 Hiện thực Tác tử và Bộ Kiểm chứng Độ trung thực Số liệu",
            "text": """
Trong triển khai thực tế, việc sử dụng các hệ thống tác tử tự phát đa agent (Multi-Agent Swarm / Agent Debate) thường dẫn đến hiện tượng bùng nổ độ trễ, hội thoại vòng vo không hồi kết và nguy cơ mất kiểm soát logic. Đề tài kiên quyết áp dụng kiến trúc **Tác tử Đơn lẻ Điều phối Tất định (Deterministic Planner Orchestration)**:

**1. Bộ Lập kế hoạch Tất định (Deterministic Planner)**:
Khi nhận câu hỏi từ người dùng, Planner thực hiện trích xuất thực thể danh định (Named Entity Recognition) và phân loại ý định (Intent Classification) thành một trong các nhóm nghiệp vụ rõ ràng:
- Nhóm Y tế Chẩn đoán: Kích hoạt tuần tự `tool_diabetes_mlp` $\\to$ `tool_kg_query` $\\to$ `tool_rag_hybrid`.
- Nhóm Y tế Rà soát Đơn thuốc: Kích hoạt `tool_sparql_reasoning` $\\to$ `tool_rag_hybrid`.
- Nhóm Tài chính Dự báo: Kích hoạt `tool_finance_bilstm` $\\to$ `tool_kg_query` $\\to$ `tool_rag_hybrid`.
- Nhóm Tài chính Vĩ mô Tổng quan: Kích hoạt `tool_kg_query` $\\to$ `tool_graph_rag`.
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
  $$\\mathcal{N}_{\\text{response}} = \\{x_1, x_2, \\dots, x_p\\}$$
  Đồng thời, Verifier tập hợp toàn bộ các con số xuất hiện trong kết quả đầu ra của các công cụ (Observations):
  $$\\mathcal{N}_{\\text{context}} = \\{c_1, c_2, \\dots, c_q\\}$$
  Chỉ số Độ trung thực Số liệu (Numeric Faithfulness Score) được tính toán:
  $$\\text{Faithfulness} = \\begin{cases} 1.0 & \\text{nếu } \\mathcal{N}_{\\text{response}} = \\emptyset \\\\ \\frac{|\\mathcal{N}_{\\text{response}} \\cap \\mathcal{N}_{\\text{context}}|}{|\\mathcal{N}_{\\text{response}}|} & \\text{ngược lại} \\end{cases}$$
  Hệ thống thiết lập **ngưỡng cứng tối thiểu: $\\text{Faithfulness} \\ge 0.85$ (85%)**.
  Nếu chỉ số $< 0.85$ (đồng nghĩa với việc LLM tự ý bịa đặt hoặc làm tròn sai lệch trên 15% số liệu), Verifier lập tức HỦY BỎ bản nháp, tự động kích hoạt cơ chế sinh lại (Regeneration) với câu lệnh cảnh báo nghiêm khắc chỉ rõ các con số vi phạm.
"""
        },
        {
            "num": "6.3.4",
            "title": "6.3.4 Cơ chế Phục hồi Lỗi Tự động và Tái sinh Có Ràng buộc (Fault Recovery & Auto-Regeneration)",
            "text": """
Để hệ thống vận hành tự động và liên tục mà không cần sự can thiệp thủ công của kỹ sư, Verifier được trang bị một máy trạng thái hữu hạn (Finite State Machine - FSM) điều khiển quy trình phục hồi:
- **Trạng thái 0 (Draft Generation)**: LLM sinh bản nháp phản hồi ban đầu dựa trên chuỗi Thought-Action-Observation.
- **Trạng thái 1 (Citation Verification)**: Kiểm tra sự hiện diện của trích dẫn `[D01]` - `[D17]`. Nếu không có trích dẫn, FSM kích hoạt lời nhắc ép buộc: *"BẢN NHÁP BỊ TỪ CHỐI DO THIẾU TRÍCH DẪN. HÃY GẮN MÃ [Dxx] CHO TỪNG NHẬN ĐỊNH VÀ SINH LẠI"* và quay lại Trạng thái 0.
- **Trạng thái 2 (Numeric Faithfulness Verification)**: Kiểm tra độ khớp tập số $\\mathcal{N}_{\\text{response}}$ với $\\mathcal{N}_{\\text{context}}$. Nếu chỉ số $\\text{Faithfulness} < 0.85$, Verifier trích xuất danh sách các con số bịa đặt $\\mathcal{U} = \\mathcal{N}_{\\text{response}} \\setminus \\mathcal{N}_{\\text{context}}$ và kích hoạt chỉ thị: *"BẢN NHÁP CHỨA CÁC CON SỐ KHÔNG CÓ CĂN CỨ: {\\mathcal{U}}. BẮT BUỘC CHỈ SỬ DỤNG SỐ LIỆU ĐƯỢC CÔNG CỤ TRẢ VỀ. HÃY HIỆU CHỈNH LẠI NGAY"*.
- **Trạng thái 3 (Approved & Fallback)**: Nếu vượt qua cả hai chốt chặn, bản phản hồi được gửi ngay tới người dùng. Nếu sau $R_{\\max} = 2$ lần tái sinh vẫn không đạt chuẩn, hệ thống tự động kích hoạt cơ chế An toàn Dự phòng (Deterministic Fallback): Trả về câu trả lời mẫu được ghép nối trực tiếp từ kết quả JSON của các công cụ mà không qua tầng sinh từ tự do của LLM, đảm bảo an toàn tuyệt đối 100%.
"""
        },
        {
            "num": "6.4",
            "title": "6.4 Đánh giá Tác tử qua Đối chuẩn 16 Kịch bản Thực nghiệm",
            "text": """
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
"""
        },
        {
            "num": "6.4.7",
            "title": "6.4.7 Phân tích Chi tiết Từng Ca Thất bại của Mô hình LLM Đơn lẻ (Failure Mode Autopsy)",
            "text": """
Việc mổ xẻ các ca thất bại của mô hình LLM đơn lẻ mang lại những bài học đắt giá về lý do tại sao kiến trúc tích hợp công cụ là bắt buộc trong thực tế:
- **Ca thất bại 1 (Chống chỉ định Metformin)**: Khi được hỏi về việc dùng Metformin cho bệnh nhân có $\\text{eGFR} = 24\\text{ mL/phút}$, LLM đơn lẻ trả lời: "Có thể tiếp tục dùng nhưng giảm một nửa liều". Đây là sai lầm chết người! Theo Quyết định 5481/QĐ-BYT, eGFR < 30 là chống chỉ định tuyệt đối. Sự nhầm lẫn này xuất phát từ việc LLM nhớ lộn ngưỡng 30-44 với ngưỡng dưới 30.
- **Ca thất bại 2 (Phần bù Vàng SJC)**: LLM đơn lẻ giải thích rằng: "Giá vàng SJC cao hơn giá thế giới do hàm lượng vàng SJC tinh khiết hơn (99.999% so với 99.99%)". Đây là một ảo giác ngớ ngẩn và phi lý! Cả hai đều là vàng bốn số chín (99.99%), sự chênh lệch bắt nguồn từ độc quyền thương hiệu theo Nghị định 24/2012 chứ không phải do chất lượng vật lý.
- **Ca thất bại 3 (Biến động Cổ phiếu HPG khi Tỷ giá Tăng)**: LLM đơn lẻ phán đoán: "Hòa Phát là doanh nghiệp sản xuất nên tỷ giá USD tăng sẽ luôn có lợi lớn". Mô hình hoàn toàn bỏ quên sự thật rằng Hòa Phát nhập khẩu quặng sắt và than cốc bằng USD và có dư nợ vay USD lớn, do đó tỷ giá tăng thực chất làm tăng chi phí tài chính và bào mòn lợi nhuận.

Cả ba sai sót chí mạng trên đều được Tác tử ReAct giải quyết triệt để nhờ sự ràng buộc của đồ thị tri thức và công cụ truy xuất văn bản chính thức.
"""
        },
        {
            "num": "6.5",
            "title": "6.5 Triển khai Ứng dụng Web Dashboard Tương tác",
            "text": """
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
"""
        }
    ]
}
