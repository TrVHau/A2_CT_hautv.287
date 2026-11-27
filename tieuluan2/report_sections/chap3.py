"""
Chapter 3: Kỹ thuật Retrieval-Augmented Generation (RAG)
Comprehensive Academic Treatise - Standalone Independent Research
Author: Tran Van Hau - Student ID: B23DCCN287 - PTIT
"""

CHAP3_DATA = {
    "chapter_num": 3,
    "chapter_title": "CHƯƠNG 3: KỸ THUẬT RETRIEVAL-AUGMENTED GENERATION (RAG)",
    "intro_text": """
Chương này nghiên cứu toàn diện ngăn xếp công nghệ RAG từ cơ bản đến nâng cao: phân tích các điểm nghẽn của Naive RAG, thiết lập thực nghiệm trên kho 17 tài liệu quy chuẩn tiếng Việt, khảo sát 5 chiến lược phân mảnh (chunking), đánh giá 5 phương pháp truy xuất (BM25, Dense, Hybrid RRF, Cross-Encoder, GraphRAG), xây dựng ma trận đối chuẩn 25 cấu hình, phân tích độ phức tạp tính toán và bộ nhớ, và phân tích kỹ thuật phân cụm Louvain trong GraphRAG.
""",
    "sections": [
        {
            "num": "3.1",
            "title": "3.1 Naive RAG và Các Điểm Nghẽn Cốt Tử",
            "text": """
Kiến trúc RAG nguyên bản (Naive RAG) thường được triển khai theo một đường ống tuyến tính đơn giản: Tài liệu văn bản được cắt nhỏ thành các đoạn cố định (ví dụ: 500 từ), chuyển hóa thành vector nhúng thông qua một mô hình nhúng nơ-ron (như BERT hoặc text-embedding-ada-002), lưu trữ vào cơ sở dữ liệu vector. Khi có truy vấn từ người dùng, hệ thống tính độ tương đồng cosin để lấy ra top-$k$ đoạn gần nhất và đưa trực tiếp vào câu lệnh nhắc (prompt) của LLM.

Mặc dù dễ triển khai, Naive RAG bộc lộ 4 điểm nghẽn chí mạng trong các ứng dụng thực tế:
1. **Hiện tượng Trôi dạt Ngữ nghĩa (Semantic Drift)**: Mô hình nhúng biểu diễn toàn bộ một đoạn văn dài thành một vector duy nhất. Trong các văn bản kỹ thuật y tế hoặc tài chính, một đoạn văn thường chứa nhiều thông tin phụ bên cạnh thông tin chính. Vector nhúng bị phân tán trọng số, dẫn đến việc truy xuất các đoạn văn có vẻ liên quan về mặt từ ngữ nhưng hoàn toàn lạc đề về mặt nghiệp vụ cốt lõi.
2. **Hiện tượng "Mất mát ở Giữa" (Lost in the Middle)**: Nghiên cứu của Liu et al. (Stanford, 2023) đã chỉ ra rằng các LLM dựa trên kiến trúc Transformer có xu hướng chú ý mạnh mẽ vào các đoạn văn bản ở đầu và cuối ngữ cảnh đầu vào theo đường cong chữ U (U-shaped Attention Curve), nhưng lại bỏ sót hoặc đánh giá thấp các thông tin nằm ở phần giữa của prompt. Khi Naive RAG nhồi nhét 5-10 đoạn văn bản không được sắp xếp tối ưu, chứng cứ quan trọng nằm ở giữa thường bị LLM phớt lờ.
3. **Phân mảnh Ngữ cảnh Làm Đứt gãy Chuỗi Nhân quả**: Cắt văn bản cố định theo số lượng từ mà không hiểu cấu trúc ngữ nghĩa thường xé đôi một điều khoản pháp luật, một câu điều kiện lâm sàng phức tạp (ví dụ: vế "chỉ định thuốc..." nằm ở đoạn trước, còn vế "ngoại trừ bệnh nhân có tiền sử suy thận nặng..." bị văng sang đoạn sau). Hậu quả là LLM tiếp nhận thông tin phiến diện và đưa ra chỉ định sai lầm chết người.
4. **Bùng nổ Nhiễu trong Ngữ cảnh (Context Pollution)**: Việc truy xuất các đoạn văn bản chứa nhiều từ ngữ thừa làm cạn kiệt cửa sổ ngữ cảnh hữu ích của LLM, làm tăng chi phí tính toán và gia tăng tỷ lệ kích hoạt ảo giác của mô hình.
"""
        },
        {
            "num": "3.2",
            "title": "3.2 Thiết lập Thực nghiệm Truy xuất Quy chuẩn",
            "text": """
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
- **Hit@k ($k \\in \\{1, 3, 5\\}$)**: Tỷ lệ phần trăm các câu hỏi mà đoạn văn bản chứa đáp án chính xác xuất hiện trong top-$k$ kết quả trả về.
- **MRR (Mean Reciprocal Rank)**: Nghịch đảo của thứ hạng của đoạn tài liệu đúng đầu tiên:
  $$\\text{MRR} = \\frac{1}{|Q|} \\sum_{i=1}^{|Q|} \\frac{1}{\\text{rank}_i}$$
- **NDCG@5 (Normalized Discounted Cumulative Gain)**: Đánh giá chất lượng của toàn bộ danh sách xếp hạng top-5 có tính đến vị trí xuất hiện của tài liệu liên quan:
  $$\\text{DCG}@p = \\sum_{i=1}^p \\frac{2^{\\text{rel}_i} - 1}{\\log_2(i + 1)}, \\quad \\text{NDCG}@p = \\frac{\\text{DCG}@p}{\\text{IDCG}@p}$$
- **Latency (Độ trễ truy xuất)**: Thời gian thực thi tính bằng mili-giây (ms) trên phần cứng chuẩn CPU.
"""
        },
        {
            "num": "3.3",
            "title": "3.3 Các Chiến lược Phân mảnh Văn bản (Chunking Strategies)",
            "text": """
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
"""
        },
        {
            "num": "3.4",
            "title": "3.4 Các Kỹ thuật Truy xuất: Thưa, Dày, Lai và Xếp hạng lại",
            "text": """
Sau khi văn bản được phân mảnh, hệ thống thử nghiệm 5 mô hình truy xuất tài liệu khác nhau:

**1. Truy xuất Thưa bằng BM25 Okapi (Sparse Retrieval)**:
Dựa trên mô hình xác suất và không gian vector từ vựng. Hệ thống áp dụng thuật toán tách từ tiếng Việt chuẩn, sau đó tính điểm BM25 giữa câu truy vấn $Q$ và đoạn văn $D$:
$$\\text{Score}(D, Q) = \\sum_{q_i \\in Q} \\text{IDF}(q_i) \\cdot \\frac{f(q_i, D) \\cdot (k_1 + 1)}{f(q_i, D) + k_1 \\cdot \\left(1 - b + b \\cdot \\frac{|D|}{\\text{avgdl}}\\right)}$$
Trong đó:
- $f(q_i, D)$ là tần số xuất hiện của từ $q_i$ trong đoạn văn $D$.
- $|D|$ và $\\text{avgdl}$ lần lượt là độ dài của đoạn văn và độ dài trung bình của toàn bộ các đoạn trong kho ngữ liệu.
- Các siêu tham số được tối ưu hóa cho tiếng Việt: $k_1 = 1.5$ (kiểm soát độ bão hòa tần số từ) và $b = 0.75$ (mức độ phạt độ dài đoạn văn).
- Công thức trọng số nghịch đảo tần số tài liệu chuẩn W3C:
  $$\\text{IDF}(q_i) = \\ln \\left( \\frac{N - n(q_i) + 0.5}{n(q_i) + 0.5} + 1 \\right)$$
BM25 cực kỳ mạnh mẽ trong việc tìm kiếm chính xác các từ khóa hiếm, các mã số quy chuẩn (như `5481/QĐ-BYT`, `eGFR`, `DXY`, `HPG`), hoàn toàn miễn nhiễm với hiện tượng ảo giác vector.

**2. Truy xuất Dày Ngữ nghĩa (Dense Semantic Retrieval)**:
Sử dụng không gian nhúng đa ngôn ngữ để chiếu cả câu truy vấn và đoạn văn bản thành các vector thực 768 chiều. Độ tương đồng ngữ nghĩa được tính bằng hàm tích vô hướng trên các vector đã được chuẩn hóa độ dài Euclidean ($L_2$ Normalization), tương đương với Cosine Similarity:
$$\\text{CosineSim}(q, d) = \\frac{\\mathbf{e}_q \\cdot \\mathbf{e}_d}{\\|\\mathbf{e}_q\\|_2 \\|\\mathbf{e}_d\\|_2}$$
Dense Retrieval có khả năng vượt trội trong việc hiểu các khái niệm đồng nghĩa (ví dụ: "thuốc hạ đường" tương đồng với "dược chất kiểm soát glucose"), ngay cả khi người dùng không sử dụng chính xác các thuật ngữ khoa học.

**3. Truy xuất Lai bằng Reciprocal Rank Fusion (Hybrid RRF, $k=60$)**:
Nhận thấy BM25 và Dense Retrieval có tính chất bù trừ hoàn hảo, hệ thống kết hợp kết quả xếp hạng của hai phương pháp bằng thuật toán Reciprocal Rank Fusion (RRF) nổi tiếng của Cormack et al. (SIGIR 2009):
$$\\text{RRF\\_Score}(d) = \\sum_{m \\in \\{\\text{BM25}, \\text{Dense}\\}} \\frac{1}{k + r_m(d)}$$
Với $r_m(d)$ là thứ hạng xuất hiện của tài liệu $d$ trong hệ thống truy xuất $m$, và $k = 60$ là hằng số làm mịn thứ hạng. RRF có ưu điểm vượt trội là không phụ thuộc vào thang đo điểm số nội tại vốn rất khác biệt giữa BM25 và Cosine, giúp cân bằng hoàn hảo giữa tính chính xác từ khóa và độ tương đồng khái niệm.

**4. Xếp hạng lại Bằng Cross-Encoder (Cross-Encoder Reranking)**:
Các mô hình Bi-Encoder tính toán vector của truy vấn và đoạn văn bản hoàn toàn độc lập, làm mất đi các tương tác từ vựng chéo tinh vi. Hệ thống bổ sung tầng Cross-Encoder ở giai đoạn hai: Nhận top-20 ứng viên từ bước truy xuất lai, ghép thành chuỗi đầu vào duy nhất `[CLS] Query [SEP] Passage [SEP]` và đưa qua các tầng Transformer đầy đủ cơ chế Self-Attention đa chiều. Cross-Encoder gán lại điểm liên quan với độ chính xác vượt trội, đẩy các đoạn văn chứa bằng chứng cốt lõi lên top-1.

**5. Ma trận Thực nghiệm 25 Cấu hình RAG**:
Bảng 3.2 trong báo cáo đối chuẩn toàn bộ 25 sự kết hợp giữa 5 chiến lược chia đoạn và 5 bộ truy xuất. Kết quả chỉ ra rõ ràng:
- Cấu hình thấp nhất: Phân mảnh theo câu + BM25 chỉ đạt Hit@1 = 56.67%, MRR = 0.6548.
- Cấu hình tối ưu nhất: **Cây Phân cấp Cha - Con + Hybrid RRF + Cross-Encoder Reranker** xuất sắc đạt **Hit@1 = 90.00%**, **Hit@3 = 100.00%**, **Hit@5 = 100.00%**, **MRR = 0.9511**, và **NDCG@5 = 0.9634**, với độ trễ xử lý chấp nhận được là 86.2 ms.
"""
        },
        {
            "num": "3.4.6",
            "title": "3.4.6 Phân tích Độ Phức tạp Tính toán và Bộ nhớ (Complexity & Memory Footprint)",
            "text": """
Một hệ thống RAG cấp doanh nghiệp đòi hỏi phải cân bằng tối ưu giữa độ chính xác và chi phí tài nguyên phần cứng. Hệ thống tiến hành phân tích độ phức tạp thời gian và không gian bộ nhớ:
- **Chỉ mục BM25 Okapi**:
  - *Độ phức tạp thời gian*: $O(|Q| \\cdot \\text{avg}(|L_t|))$ trong đó $|L_t|$ là độ dài danh sách nghịch đảo của từ khóa. Tốc độ tìm kiếm trung bình chỉ mất 12 - 16 ms.
  - *Không gian bộ nhớ*: Chỉ tiêu tốn 12.4 MB RAM cho toàn bộ kho ngữ liệu sau khi nén từ điển.
- **Chỉ mục Vector Dense (768 chiều)**:
  - *Độ phức tạp thời gian*: $O(N \\cdot D)$ với quét phẳng (Flat Index) hoặc $O(M \\cdot \\log N \\cdot D)$ với đồ thị HNSW. Thời gian truy vấn mất 18 - 24 ms.
  - *Không gian bộ nhớ*: Tiêu tốn 182 MB RAM để lưu trữ toàn bộ các tensor nhúng và cấu trúc đồ thị liên kết.
- **Cross-Encoder Reranker**:
  - *Độ phức tạp thời gian*: $O(K \\cdot L^2 \\cdot D_{\\text{model}})$ với $K=20$ ứng viên và chiều dài chuỗi ghép $L \\approx 512$. Đây là khâu chiếm thời gian lớn nhất (khoảng 60 - 70 ms) nhưng mang lại bước nhảy vọt về độ chính xác xếp hạng (+10% Hit@1).
- **Tổng tài nguyên hệ thống**: Toàn bộ đường ống RAG chỉ chiếm chưa tới 250 MB RAM, cho phép vận hành cực kỳ mượt mà ngay trên các máy chủ CPU phổ thông hoặc thiết bị Edge computing.
"""
        },
        {
            "num": "3.5",
            "title": "3.5 Advanced RAG: Tối ưu hóa Truy vấn Đa chặng",
            "text": """
Để xử lý các câu hỏi phức tạp hoặc có cách hành văn ngắn ngủi của người dùng, hệ thống tích hợp hai kỹ thuật RAG Nâng cao (Advanced RAG):

1. **Véc-tơ Nhúng Tài liệu Giả thuyết (Hypothetical Document Embeddings - HyDE)**:
   Khi nhận một truy vấn trừu tượng $q$, hệ thống trước tiên yêu cầu LLM đóng vai chuyên gia tạo ra một đoạn văn bản giả định $d_{\\text{hypo}}$ có thể trả lời câu hỏi đó (dù có thể chứa sai lệch nhỏ). Sau đó, vector nhúng của $d_{\\text{hypo}}$ được dùng để tìm kiếm các tài liệu thật trong kho ngữ liệu. Nguyên lý là: Đoạn văn giả định dù chưa chính xác hoàn toàn nhưng nằm cùng không gian phân phối ngôn ngữ với các tài liệu thật, giúp tìm kiếm hiệu quả hơn so với câu hỏi ngắn. Tuy nhiên, thực nghiệm cũng chỉ ra rủi ro: Đối với các truy vấn số liệu khắt khe (ví dụ: hỏi chính xác biên độ tỷ giá), nếu văn bản giả thuyết bịa sai số liệu, nó có thể dẫn dắt bộ truy xuất đi chệch hướng.
2. **Kỹ thuật Mở rộng Truy vấn Đa hướng (Multi-Query Expansion)**:
   Hệ thống sử dụng LLM để phân tích một câu hỏi phức tạp thành 3-4 câu hỏi thành phần từ các góc nhìn khác nhau (ví dụ: từ góc độ pháp lý, góc độ tài chính, và góc độ tác động doanh nghiệp). Mỗi câu hỏi con được truy xuất độc lập, sau đó toàn bộ các tập kết quả được hợp nhất bằng thuật toán RRF. Kỹ thuật này giúp bao phủ toàn bộ các khía cạnh thông tin, đặc biệt hiệu quả với các câu hỏi so sánh đa chiều.
"""
        },
        {
            "num": "3.6",
            "title": "3.6 GraphRAG: Tổng hợp Tri thức Cấu trúc trên Đồ thị",
            "text": """
GraphRAG là bước tiến hóa mang tính cách mạng được Microsoft giới thiệu năm 2024, giải quyết điểm nghẽn lớn nhất của RAG truyền thống: Khả năng tổng hợp tri thức mang tính bức tranh toàn cảnh (Query-Focused Summarization) trên toàn bộ kho tài liệu.

**Quy trình Hoạt động của GraphRAG trong Hệ thống**:
1. **Trích xuất Đồ thị Thực thể - Quan hệ**: Hệ thống quét qua các đoạn văn bản, nhận diện các thực thể danh định (Named Entities) và các quan hệ ngữ nghĩa, xây dựng một đồ thị tri thức phi cấu trúc liên kết các đoạn văn.
2. **Phát hiện Cộng đồng bằng Thuật toán Louvain**:
   Đồ thị văn bản được phân cụm thành các "cộng đồng tri thức" (Knowledge Communities) phân cấp dựa trên việc tối đa hóa hàm độ đo Modularity $Q$ của Blondel et al.:
   $$Q = \\frac{1}{2m} \\sum_{i, j} \\left[ A_{ij} - \\frac{k_i k_j}{2m} \\right] \\delta(c_i, c_j)$$
   Trong đó:
   - $A_{ij}$ là trọng số cạnh giữa nút $i$ và nút $j$.
   - $k_i = \\sum_j A_{ij}$ là tổng bậc trọng số của nút $i$.
   - $m = \\frac{1}{2} \\sum_{ij} A_{ij}$ là tổng trọng số toàn bộ các cạnh trong đồ thị.
   - $c_i, c_j$ là cộng đồng chứa nút $i$ và $j$; hàm $\\delta(c_i, c_j) = 1$ nếu cùng cộng đồng và bằng 0 nếu khác cộng đồng.
   Thuật toán lặp qua hai pha: Pha 1 di chuyển từng nút vào cộng đồng lân cận để tối đa hóa mức tăng $\\Delta Q$, pha 2 gộp các nút trong cùng cộng đồng thành một siêu nút và xây dựng đồ thị cấp cao hơn.
3. **Cơ chế Truy vấn Kép: Tìm kiếm Toàn cục (Global Search) và Cục bộ (Local Search)**:
   - **Local Search**: Khi câu hỏi nhắm vào một thực thể cụ thể (ví dụ: "Chỉ định của Metformin là gì?"), hệ thống duyệt các nút lân cận 1-hop, 2-hops và các đoạn văn gắn liền với thực thể đó.
   - **Global Search**: Khi câu hỏi yêu cầu cái nhìn tổng quan (ví dụ: "Tóm tắt toàn bộ các rủi ro vĩ mô lớn nhất đối với nền kinh tế Việt Nam hiện nay"), hệ thống truy xuất các bản tóm tắt cấp cao của các cộng đồng Louvain hàng đầu mà không cần quét qua từng đoạn văn riêng lẻ, loại bỏ hoàn toàn giới hạn ngữ cảnh của LLM.
"""
        },
        {
            "num": "3.7",
            "title": "3.7 Chiến lược Lựa chọn Kiến trúc trong Hệ thống Thực tế",
            "text": """
Từ các kết quả nghiên cứu và đối chuẩn thực nghiệm, hệ thống xác lập chiến lược định tuyến kiến trúc thông minh tùy theo bản chất của câu hỏi đầu vào:
- Đối với các câu hỏi kiểm tra sự kiện số học cụ thể hoặc đối chiếu pháp quy ngắn: Ưu tiên sử dụng **Parent-Child Chunking kết hợp Hybrid RRF và Cross-Encoder**, đảm bảo độ trễ thấp (< 90 ms) và độ chính xác Hit@1 đạt 90%.
- Đối với các câu hỏi suy luận quan hệ logic hoặc kiểm tra chống chỉ định thuốc: Định tuyến trực tiếp về **Đồ thị Tri thức và Động cơ suy diễn SPARQL**.
- Đối với các câu hỏi phân tích vĩ mô tổng quan hoặc tóm tắt chuyên sâu đa miền: Kích hoạt **GraphRAG Global Search**, cho phép tổng hợp bức tranh toàn cảnh một cách toàn diện và mạch lạc nhất.
"""
        }
    ]
}
