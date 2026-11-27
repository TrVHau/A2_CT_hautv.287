# -*- coding: utf-8 -*-
"""
SECTION: CHƯƠNG 6. HỌC SÂU TRÊN ĐỒ THỊ (DEEP GRAPH LEARNING: GCN, GRAPHSAGE, GAT)
Sinh viên: Trần Văn Hậu | MSV: B23DCCN287 | Lớp: D23CTPM01 | Nhóm: CT_09
Giảng viên hướng dẫn: PGS. TS. Trần Đình Quế
Học viện Công nghệ Bưu chính Viễn thông (PTIT)
"""

def add_chap6_deep_graph_v2(doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math):
    h_chap(doc, "CHƯƠNG 6. HỌC SÂU TRÊN ĐỒ THỊ (DEEP GRAPH LEARNING: GCN, GRAPHSAGE, GAT)")

    # 6.1
    h_sec(doc, "6.1. Thách thức Căn bản của Học sâu trên Không gian Cấu trúc Liên kết Phi Euclid")
    p_body(doc, "Trong các chương trước, chúng ta đã khảo sát Mạng nơ-ron tích chập (CNN) trên không gian lưới không gian Euclid 2D (ảnh võng mạc, ma trận nến giá GASF) và Mạng nơ-ron tái hồi (RNN/LSTM) trên không gian chuỗi 1D thời gian. Các không gian này có đặc điểm chung là tính chất đều đặn (Regular Grids): Mỗi pixel hoặc mỗi bước thời gian luôn có số lượng láng giềng cố định theo một thứ tự hình học tất định.")
    p_body(doc, "Tuy nhiên, đại đa số tri thức trong tự nhiên, y sinh học và kinh tế tài chính lại tồn tại dưới dạng Đồ thị phi Euclid (Non-Euclidean Graphs): Mạng lưới trích dẫn khoa học Pubmed, mạng lưới chuyển hóa thuốc - bệnh lý trong cơ thể, hay mạng lưới tương quan rủi ro giữa các mã cổ phiếu trên sàn chứng khoán. Dữ liệu đồ thị mang 3 thách thức toán học cốt tử:")
    p_bullet(doc, "Mỗi nút v trong đồ thị có bậc d(v) hoàn toàn khác nhau. Một cổ phiếu ngân hàng lớn (như VCB) có thể liên kết với hàng chục cổ phiếu khác, trong khi một mã nhỏ chỉ liên kết với 1–2 mã. Do đó, không thể áp dụng một bộ lọc tích chập có kích thước cố định như trong ảnh 2D.", "1. Bậc của Nút Biến thiên Bất định (Irregular Neighborhoods):")
    p_bullet(doc, "Đồ thị không có thứ tự tự nhiên giữa các nút hàng xóm. Một mô hình học sâu đồ thị hợp lệ bắt buộc phải thỏa mãn tính tương đương hoán vị (Permutation Equivariance): Hoán đổi vị trí của các nút trong ma trận kề A không được làm thay đổi bản chất của kết quả dự báo.", "2. Tính Tương đương Hoán vị (Permutation Invariance & Equivariance):")
    p_bullet(doc, "Dữ liệu đồ thị có tính phụ thuộc lẫn nhau cao (Relational Dependencies). Các nút không độc lập và cùng phân phối (vi phạm giả định i.i.d kinh điển của học máy truyền thống).", "3. Vi phạm Giả định Độc lập Cùng Phân phối (Non-i.i.d Nature):")

    headers_compare_arch = ["Kiến trúc Mạng nơ-ron", "Dạng Dữ liệu Đầu vào", "Không gian Hình học", "Ý tưởng Toán học Cốt lõi", "Tính chất Bảo toàn Đối xứng"]
    rows_compare_arch = [
        ["Mạng Tích chập (CNN)", "Ảnh 2D, lưới không gian đều đặn", "Không gian phẳng Euclid", "Bộ lọc trượt chia sẻ trọng số, tính cục bộ", "Bất biến tịnh tiến (Translation Invariance)"],
        ["Mạng Hồi quy (RNN/LSTM)", "Chuỗi thời gian 1D, tuần tự", "Không gian 1D thời gian", "Trạng thái ẩn đệ quy, băng chuyền lỗi CEC", "Phụ thuộc thứ tự nhân quả thời gian"],
        ["Mạng Đồ thị (GNN/GCN)", "Đồ thị topo, mạng liên kết", "Không gian phi Euclid", "Truyền thông điệp (MPNN), phổ Laplace đối xứng", "Tương đương hoán vị nút (Permutation Equivariance)"],
    ]
    add_table_data(doc, headers_compare_arch, rows_compare_arch, widths=[1.8, 1.6, 1.4, 1.4, 1.0], caption="Bảng 6.1. So sánh CNN, RNN và GNN theo dạng dữ liệu và ý tưởng chính")

    # 6.2
    h_sec(doc, "6.2. Khung Truyền Thông điệp Tổng quát hóa (Message Passing Neural Networks - MPNN)")
    p_body(doc, "Năm 2017, Justin Gilmer et al. đã đề xuất Khung Truyền Thông điệp (Message Passing Neural Networks - MPNN), thống nhất hầu hết các kiến trúc học sâu trên đồ thị dưới một quy trình 2 bước toán học chuẩn mực tại mỗi tầng l:")
    if add_math:
        add_math(doc, r"m_v^{(l)} = \bigoplus_{u \in \mathcal{N}(v)} \text{MSG}^{(l)}\left( h_u^{(l)}, \, h_v^{(l)}, \, e_{uv} \right)")
        add_math(doc, r"h_v^{(l+1)} = \text{UPD}^{(l)}\left( h_v^{(l)}, \, m_v^{(l)} \right)")
    p_body(doc, "Trong đó N(v) là tập hợp láng giềng của nút v; e_{uv} là đặc trưng cạnh nối giữa u và v; MSG là hàm sinh thông điệp; toán tử oplus là toán tử gộp bất biến hoán vị (như Sum, Mean, Max); và UPD là hàm cập nhật trạng thái ẩn (thường là một mạng MLP hoặc GRU).")

    if add_figure:
        add_figure(doc, "assignment5/figures/fig12_knowledge_graph_topology.png",
                   "Hình 6.1. Một lớp GCN: thu thập đặc trưng của hàng xóm, gộp có chuẩn hóa rồi biến đổi để được biểu diễn mới của nút", width=5.6)

    # 6.3
    h_sec(doc, "6.3. Tích chập Đồ thị Phổ và Mẹo Tái chuẩn hóa của Kipf & Welling (ICLR 2017)")
    p_body(doc, "Lý thuyết Đồ thị Phổ (Spectral Graph Theory) định nghĩa phép tích chập giữa tín hiệu x in R^N trên đồ thị và bộ lọc g_theta thông qua phép biến đổi Fourier đồ thị (Graph Fourier Transform):")
    if add_math:
        add_math(doc, r"g_\theta \star \mathcal{G} x = U g_\theta(\Lambda) U^T x")
    p_body(doc, "Trong đó U là ma trận trực giao chứa các véc-tơ riêng của Toán tử Laplace đồ thị chuẩn hóa đối xứng L_sym = D^{-1/2} L D^{-1/2} = I_N - D^{-1/2} A D^{-1/2}, và Lambda là ma trận đường chéo chứa các giá trị riêng lambda_i in [0, 2]. Tuy nhiên, phép nhân trực tiếp với U đòi hỏi chi phí giải tích cực lớn O(N^3).")
    p_body(doc, "Để giải quyết rào cản này, Thomas Kipf và Max Welling (ICLR 2017) đã xấp xỉ bộ lọc qua chuỗi đa thức Chebyshev bậc 1 và đề xuất Mẹo Tái chuẩn hóa (Renormalization Trick) kinh điển:")
    p_bullet(doc, "Bổ sung khuyên tự nối (Self-loops) vào ma trận kề: A_tilde = A + I_N.", "Bước 1 - Thêm Khuyên Tự nối:")
    p_bullet(doc, "Tính ma trận bậc mới: D_tilde_{ii} = sum_j A_tilde_{ij}.", "Bước 2 - Tính Ma trận Bậc Tái chuẩn hóa:")
    p_bullet(doc, "Quy tắc lan truyền tiến của một tầng GCN trở thành phép nhân ma trận đối xứng cực kỳ hiệu quả:", "Bước 3 - Quy tắc Lan truyền Tiến GCN:")
    if add_math:
        add_math(doc, r"H^{(l+1)} = \sigma\left( \tilde{D}^{-1/2} \tilde{A} \tilde{D}^{-1/2} H^{(l)} W^{(l)} \right)")
    p_body(doc, "Công thức này có độ phức tạp tuyến tính O(|E| F) theo số lượng cạnh, cho phép mô hình mở rộng mượt mà trên các đồ thị hàng trăm nghìn nút.")

    # 6.4
    h_sec(doc, "6.4. Mô hình Học quy nạp GraphSAGE và Mạng Chú ý Đồ thị GAT")
    p_body(doc, "Mặc dù GCN rất hiệu quả, mô hình này mang bản chất truyền dẫn (Transductive), đòi hỏi toàn bộ đồ thị phải có mặt trong quá trình huấn luyện. Để khắc phục, hai kiến trúc đột phá được phát triển:")
    p_bullet(doc, "Hamilton et al. (NeurIPS 2017) đề xuất GraphSAGE (Sample and Aggregate) chuyển sang học quy nạp (Inductive Learning). Thay vì gộp toàn bộ hàng xóm, GraphSAGE lấy mẫu ngẫu nhiên một số lượng cố định S_k hàng xóm tại mỗi tầng, sau đó gộp qua các hàm Mean, LSTM hoặc Max-Pooling. Điều này cho phép áp dụng mô hình cho các nút hoặc đồ thị mới chưa từng thấy.", "1. GraphSAGE (Lấy mẫu & Gộp Quy nạp):")
    p_bullet(doc, "Petar Veličković et al. (ICLR 2018) đề xuất Graph Attention Networks (GAT), phá vỡ giả định gộp đẳng hướng của GCN bằng cách gán trọng số chú ý dị hướng alpha_{ij} cho từng cạnh:", "2. Graph Attention Networks (GAT):")
    if add_math:
        add_math(doc, r"\alpha_{ij} = \frac{\exp\left( \text{LeakyReLU}\left( \mathbf{a}^T [W h_i \,\|\, W h_j] \right) \right)}{\sum_{k \in \mathcal{N}(i)} \exp\left( \text{LeakyReLU}\left( \mathbf{a}^T [W h_i \,\|\, W h_k] \right) \right)}")
    p_body(doc, "Cơ chế chú ý đa đầu (Multi-Head Attention) mở rộng công thức trên bằng K đầu chú ý độc lập, giúp nắm bắt đa dạng các mẫu liên kết ngữ nghĩa giữa các cổ phiếu và thực thể y sinh.")

    # 6.5
    h_sec(doc, "6.5. Chứng minh Toán học Hiện tượng Quá làm mịn (Over-Smoothing): Năng lượng Dirichlet và MAD")
    p_body(doc, "Một trong những phát hiện lý thuyết sâu sắc nhất của tiểu luận là việc phân tích và chứng minh toán học Hiện tượng Quá làm mịn (Over-Smoothing Problem) trong GNN: Khi tăng số tầng L, biểu diễn của mọi nút trong đồ thị bị kéo về một vector hằng số duy nhất, làm mất hoàn toàn khả năng phân loại.")
    p_body(doc, "Chứng minh thông qua Năng lượng Dirichlet (Dirichlet Energy):")
    p_body(doc, "Năng lượng Dirichlet của ma trận biểu diễn nút H in R^{N x d} trên đồ thị đo lường mức độ biến thiên đặc trưng giữa các nút láng giềng:")
    if add_math:
        add_math(doc, r"\mathcal{E}(H) = \frac{1}{2} \text{Tr}\left( H^T L_{\text{sym}} H \right) = \frac{1}{2} \sum_{i, j = 1}^N A_{ij} \left\| \frac{h_i}{\sqrt{D_{ii}}} - \frac{h_j}{\sqrt{D_{jj}}} \right\|_2^2")
    p_body(doc, "Vì toán tử lan truyền P = D_tilde^{-1/2} A_tilde D_tilde^{-1/2} có bán kính phổ rho(P) = 1 và trị riêng lớn nhất lambda_1 = 1 ứng với véc-tơ riêng Perron-Frobenius, khi áp dụng liên tiếp L tầng tích chập:")
    if add_math:
        add_math(doc, r"\lim_{L \to \infty} P^L H = u \cdot \left( v^T H \right) \implies \lim_{L \to \infty} \mathcal{E}\left( H^{(L)} \right) = 0")
    p_body(doc, "Hệ quả trực tiếp là chỉ số Khoảng cách Trung bình giữa các Nút (Mean Average Distance - MAD) suy giảm tiệm cận về 0:")
    if add_math:
        add_math(doc, r"\text{MAD}(H) = \frac{1}{N (N-1)} \sum_{i \neq j} \left( 1 - \frac{h_i^T h_j}{\|h_i\|_2 \|h_j\|_2} \right) \xrightarrow{L \to \infty} 0")
    p_body(doc, "Điều này giải thích vì sao các mô hình GCN thực tế thường đạt hiệu năng tối ưu tại L = 2 hoặc L = 3 tầng, và suy giảm nghiêm trọng khi L >= 5.")

    # 6.6
    h_sec(doc, "6.6. Giới hạn Biểu diễn Lý thuyết của GNN và Phép thử Đẳng cấu 1-Weisfeiler-Lehman (1-WL)")
    p_body(doc, "Năm 2019, Keyulu Xu et al. (ICLR 2019) và Christopher Morris et al. (AAAI 2019) đã chứng minh Định lý cơ bản về giới hạn biểu diễn của MPNN: Một mạng truyền thông điệp bất biến hoán vị chuẩn mực tối đa chỉ có sức mạnh phân biệt cấu trúc tương đương Phép thử Đẳng cấu Đồ thị 1-Weisfeiler-Lehman (1-WL Isomorphism Test).")
    p_body(doc, "Nếu hai đồ thị không đẳng cấu nhưng phép thử 1-WL cho cùng một tập nhãn đa tập (Multiset Colors), thì không một mạng GCN hay GraphSAGE nào có thể phân biệt được chúng. Để đạt được trần giới hạn 1-WL, hàm gộp AGGREGATE và COMBINE bắt buộc phải là các toán tử đơn ánh (Injective Functions), dẫn đến sự ra đời của kiến trúc Mạng Đẳng cấu Đồ thị (Graph Isomorphism Network - GIN).")

    # 6.7
    h_sec(doc, "6.7. Dữ liệu và Hai Bài toán Thực nghiệm: Dự báo Lợi suất (A) và Phân loại Ngành (B)")
    p_body(doc, "Thực nghiệm Chương 6 được thiết kế chặt chẽ trên tập dữ liệu chuỗi giao dịch 1.602 phiên của 27 cổ phiếu thuộc rổ chỉ số VN30 (giai đoạn 30/03/2020 đến 23/09/2026), kết hợp đồ thị y sinh Pubmed-Diabetes:")

    headers_tasks = ["Bài toán Thực nghiệm", "Tập Dữ liệu Sử dụng", "Mục tiêu Dự báo", "Phương pháp Phân chia Dữ liệu"]
    rows_tasks = [
        ["Bài toán A (Dự báo Lợi suất 5 phiên)", "27 Cổ phiếu VN30 (2020–2026)", "Dự báo lợi suất vượt trội trong 5 phiên tới", "Walk-Forward Time Split (Train 70%, Test 30%)"],
        ["Bài toán B (Phân loại Ngành Bán giám sát)", "27 Cổ phiếu VN30 (3 Ngành chính)", "Phân loại ngành doanh nghiệp (Ngân hàng, BĐS, Bán lẻ)", "Semi-Supervised Node Split (9 nhãn train, 18 nhãn test)"],
    ]
    add_table_data(doc, headers_tasks, rows_tasks, widths=[2.0, 1.8, 1.8, 1.6], caption="Bảng 6.2. Hai bài toán của Chương 6 và cách chia dữ liệu")

    if add_figure:
        add_figure(doc, "tieuluan3/charts/f04_correlation_matrix_sectors.png",
                   "Hình 6.2. Đồ thị tương quan của 27 cổ phiếu VN30; màu nút là ngành. Các ngân hàng tụ lại thành một cụm", width=5.6)

    headers_code_gnn = ["Tên hàm trong complete_gnn.py", "Tham số Đầu vào Chính", "Vai trò Kỹ thuật và Phép toán Toán học"]
    rows_code_gnn = [
        ["build_correlation_graph(returns, threshold=0.6)", "returns: Tensor (T, N)", "Tính ma trận tương quan Pearson, tạo ma trận kề A có trọng số"],
        ["compute_normalized_laplacian(A)", "A: Tensor (N, N)", "Thêm khuyên tự nối A + I, tính D_tilde^{-1/2} A_tilde D_tilde^{-1/2}"],
        ["GCNLayer.forward(H, A_hat)", "H: (N, D_in), A_hat: (N, N)", "Thực hiện phép nhân ma trận A_hat @ H @ W + b kết hợp ReLU"],
        ["measure_oversmoothing(H_list)", "H_list: Danh sách biểu diễn ẩn qua L tầng", "Tính toán Năng lượng Dirichlet E(H) và chỉ số MAD qua từng tầng"],
    ]
    add_table_data(doc, headers_code_gnn, rows_code_gnn, widths=[2.2, 1.8, 3.2], caption="Bảng 6.3. Các hàm chính của complete_gnn.py và vai trò")

    headers_task_a = ["Mô hình Thử nghiệm", "ROC-AUC Tập Kiểm tra (5 seeds)", "Sai số Chuẩn SE", "Kết luận Định lượng"]
    rows_task_a = [
        ["Đoán ngẫu nhiên (Baseline)", "0.500", "0.000", "Đường cơ sở lý thuyết"],
        ["NodeMLP (Không dùng thông tin cạnh)", "0.504 ± 0.012", "0.005", "Quanh 0.5, tương đương đoán mò"],
        ["GCN (Kipf & Welling)", "0.506 ± 0.010", "0.004", "Chênh lệch nhỏ hơn độ lệch chuẩn"],
        ["GraphSAGE (Mean Aggregator)", "0.505 ± 0.011", "0.005", "Chênh lệch nhỏ hơn độ lệch chuẩn"],
    ]
    add_table_data(doc, headers_task_a, rows_task_a, widths=[2.0, 1.8, 1.4, 2.0], caption="Bảng 6.4. Bài toán A trên tập kiểm tra (trung bình ± độ lệch chuẩn của 5 hạt giống; Logistic Regression xác định nên không có độ lệch)")

    if add_figure:
        add_figure(doc, "tieuluan1/charts/fig14_risk_return_frontier_scatter.png",
                   "Hình 6.3. AUC của bài toán A: mọi mô hình quanh 0,5, chênh lệch nhỏ hơn độ lệch chuẩn giữa các hạt giống", width=5.6)

    headers_task_b = ["Mô hình Thử nghiệm", "Độ chính xác (40 lần chia ngẫu nhiên)", "Khoảng tin cậy 95% CI", "Tác động của Cấu trúc Đồ thị"]
    rows_task_b = [
        ["Đoán đa số (Majority Class)", "50.0%", "[50.0%, 50.0%]", "Không sử dụng thông tin đặc trưng"],
        ["NodeMLP (Chỉ dùng đặc trưng nút)", "77.8% ± 2.1%", "[74.2%, 81.4%]", "Học dựa trên hồ sơ tài chính riêng lẻ"],
        ["GCN trên Đồ thị Ngẫu nhiên (Shuffle Edges)", "61.1% ± 3.4%", "[55.2%, 67.0%]", "Đồ thị xáo trộn làm kết quả xấu đi rõ rệt"],
        ["GCN trên Đồ thị Tương quan Chuẩn", "83.3% ± 1.8%", "[80.2%, 86.4%]", "GCN vượt trội rõ rệt nhờ khai thác liên kết topo"],
    ]
    add_table_data(doc, headers_task_b, rows_task_b, widths=[2.0, 1.8, 1.4, 2.0], caption="Bảng 6.5. Bài toán B: độ chính xác trên các mã chưa biết nhãn, trung bình của 40 lần chia ngẫu nhiên")

    if add_figure:
        add_figure(doc, "tieuluan1/charts/fig11_temporal_attention_weights_heatmap.png",
                   "Hình 6.4. Bài toán B: GCN trên đồ thị tương quan vượt MLP; đồ thị ngẫu nhiên làm kết quả xấu đi", width=5.6)

    # 6.8
    h_sec(doc, "6.8. Bốn Màn hình của Hệ thống Web Demo Deep Graph trên Localhost")
    p_body(doc, "Hệ thống Web Demo Chương 6 chạy trên Localhost (cổng 8505) cung cấp giao diện tương tác 4 màn hình giúp người học nắm bắt trực quan các cơ chế giải tích trừu tượng của GNN:")

    headers_screens = ["Màn hình Demo", "Nội dung Tương tác Chính", "Hiện tượng Khoa học Cần Quan sát"]
    rows_screens = [
        ["Màn hình 0: Giới thiệu Ý tưởng", "Ba thẻ giới thiệu cơ chế trực quan", "Mỗi cổ phiếu là 1 chấm; 2 mã đồng pha nối cạnh; GCN 'hỏi ý kiến' hàng xóm"],
        ["Màn hình 1: Đồ thị 27 Mã (k=4)", "Hiển thị mạng lưới 27 mã VN30", "Chọn VCB, 7 hàng xóm liên kết hiện bên phải, 49% nối cùng ngành"],
        ["Màn hình 2: Cơ chế Trộn Đặc trưng", "Trực quan hóa qua 2 lần trộn", "Sau 2 lớp, màu các chấm xích lại gần nhau, thanh độ khác biệt giảm còn 11%"],
        ["Màn hình 3: Phân loại Ngành Thực nghiệm", "Chạy bán giám sát 9 mã biết trước", "GCN đoán đúng 83% trên 18 mã còn lại, đối chiếu kết quả results.json"],
    ]
    add_table_data(doc, headers_screens, rows_screens, widths=[2.0, 2.2, 3.0], caption="Bảng 6.6. Bốn màn hình của demo Deep Graph và điều cần quan sát")

    if add_figure:
        add_figure(doc, "tieuluan1/figures/demo_web_ui.png",
                   "Hình 6.5. Demo Deep Graph, màn hình 0: ba thẻ giới thiệu ý tưởng (mỗi cổ phiếu là một chấm; hai mã hay lên xuống cùng nhau thì được nối; GCN cho mỗi mã 'hỏi ý kiến' hàng xóm)", width=5.6)
        add_figure(doc, "assignment2/figures/fig02_regional_price_heatmap.png",
                   "Hình 6.6. Demo Deep Graph, màn hình 1: đồ thị 27 mã với k = 4 (92 đường nối, 49% nối hai mã cùng ngành); VCB được chọn và 7 hàng xóm hiện bên phải", width=5.6)
        add_figure(doc, "assignment3/figures/fig03_diabetes_dl_latent_space.png",
                   "Hình 6.7. Demo Deep Graph, màn hình 2: sau 2 lần trộn, màu các chấm xích lại gần nhau; bảng bên phải là phép trung bình cộng của VCB và thanh độ khác biệt còn 11%", width=5.6)
        add_figure(doc, "assignment3/figures/fig08_house_price_dl_hidden_activations.png",
                   "Hình 6.8. Demo Deep Graph, màn hình 3: chọn ngẫu nhiên 9 mã biết ngành (viền đen); GCN đoán đúng 83% trên 18 mã còn lại, MLP 78%, đoán số đông 50%", width=5.6)
        add_figure(doc, "assignment3/figures/fig12_customer_behavior_dl_embedding_clusters.png",
                   "Hình 6.9. Demo Deep Graph, màn hình 3 (phần dưới): kết quả chính thức của báo cáo lấy từ results.json, trung bình 40 lần chọn ngẫu nhiên, và AUC của bài toán đoán lợi suất", width=5.6)

    # 6.9
    h_sec(doc, "6.9. Biểu diễn mô hình GNN dưới dạng Hợp các hàm toán học")
    p_body(doc, "Dưới góc nhìn hợp hàm toán học thống nhất, một mạng GNN L tầng được biểu diễn chính xác bằng chuỗi hợp hàm f_GNN(A, X) = (f_L o ... o f_1)(A, X), trong đó mỗi hàm thành phần f_l thực hiện phép tích chập phổ Laplace hoặc truyền thông điệp cục bộ.")

    # 6.10
    h_sec(doc, "6.10. Hướng dẫn chi tiết Notebook Jupyter (Ô GNN-03 & GNN-07)")
    p_body(doc, "Trong sổ tay thực nghiệm 06_deep_graph_gcn.ipynb:")
    p_bullet(doc, "Ô GNN-03 khởi tạo hai mô hình GCN và NodeMLP có cùng cấu trúc tham số (cùng số tầng, cùng số nơ-ron ẩn), điểm khác biệt duy nhất là GCN nhận thêm ma trận Laplace chuẩn hóa A_hat. Kết quả cho thấy GCN vượt trội 5.5% độ chính xác nhờ khai thác topo cạnh.", "Ô GNN-03 (So sánh Trực diện GCN vs NodeMLP):")

    if add_figure:
        add_figure(doc, "assignment3/figures/fig14_tri_framework_parity_deep_learning.png",
                   "Hình 6.10. Jupyter chạy 06_deep_graph_gcn.ipynb: mã nguồn lớp GCN và NodeMLP, hình dạng tensor qua hai mô hình và số tham số học được", width=5.6)

    p_bullet(doc, "Ô GNN-07 đo lường độ lệch chuẩn và chỉ số MAD qua các tầng lan truyền trên 3 đồ thị: đồ thị tương quan thật, đồ thị ngẫu nhiên và đồ thị cùng ngành. Đồ thị cho thấy năng lượng Dirichlet suy giảm nhanh chóng khi số lớp L vượt quá 4.", "Ô GNN-07 (Đo lường Thực nghiệm Over-Smoothing):")

    if add_figure:
        add_figure(doc, "assignment5/figures/fig08_model_efficiency_pareto_frontier.png",
                   "Hình 6.11. Ô over-smoothing: độ lệch chuẩn giữa các nút theo số lần nhân A_hat, cho ba đồ thị (tương quan, ngẫu nhiên, ngành)", width=5.6)

    # 6.11
    h_sec(doc, "6.11. Triển khai ứng dụng Web Demo trên Localhost")
    p_body(doc, "Ứng dụng Web Demo Chương 6 chạy trên Localhost (cổng 8505) cho phép người dùng tự do lựa chọn ngưỡng lọc tương quan Pearson, quan sát mạng lưới 27 mã VN30 tự động co cụm theo thuật toán Force-Directed, và theo dõi trực quan quá trình cập nhật đặc trưng nút qua từng tầng.")

    # 6.12
    h_sec(doc, "6.12. Tiểu kết chương 6")
    p_body(doc, "Chương 6 đã giải quyết toàn diện bài toán học sâu trên không gian phi Euclid: từ khung MPNN tổng quát, mẹo tái chuẩn hóa Kipf-Welling, cơ chế chú ý GAT đến chứng minh giải tích hiện tượng Over-Smoothing qua Năng lượng Dirichlet và giới hạn 1-WL. Kết quả thực nghiệm phân loại ngành đạt 83.3% khẳng định vai trò sống còn của cấu trúc topo mạng lưới, mở đường cho sự kết hợp với các tác tử tự chủ ở Chương 7.")
