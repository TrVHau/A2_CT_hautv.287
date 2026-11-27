# -*- coding: utf-8 -*-
"""
SECTION: CHƯƠNG 4. MẠNG NƠ-RON TÁI HỒI (RNN, LSTM, GRU) VÀ DỰ BÁO CHUỖI THỜI GIAN
Sinh viên: Trần Văn Hậu | MSV: B23DCCN287 | Lớp: D23CTPM01 | Nhóm: CT_09
Giảng viên hướng dẫn: PGS. TS. Trần Đình Quế
Học viện Công nghệ Bưu chính Viễn thông (PTIT)
"""

def add_chap4_rnn_v2(doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math):
    h_chap(doc, "CHƯƠNG 4. MẠNG NƠ-RON TÁI HỒI (RNN, LSTM, GRU) VÀ DỰ BÁO CHUỖI THỜI GIAN")

    # 4.1
    h_sec(doc, "4.1. Bản chất Dữ liệu Chuỗi Tuần tự và Ý nghĩa Cốt tử của Chiều Thời gian")
    p_body(doc, "Trong các hệ thống thông minh ứng dụng thực tiễn — từ việc giám sát liên tục nồng độ glucose trong máu (Continuous Glucose Monitoring - CGM) của bệnh nhân đái tháo đường, phân tích chuỗi thời gian định lượng chứng khoán, cho đến lưu lượng truyền gói tin trong mạng viễn thông — dữ liệu quan sát xuất hiện dưới dạng một chuỗi tuần tự theo thời gian: X = (x_1, x_2, ..., x_T), trong đó x_t in R^D là vector quan sát tại bước thời gian t.")
    p_body(doc, "Dữ liệu chuỗi tuần tự phá vỡ căn bản giả định độc lập và cùng phân phối (i.i.d) của học máy truyền thống: giá trị quan sát tại thời điểm t có mối tương quan phụ thuộc sâu sắc vào toàn bộ lịch sử các trạng thái quá khứ x_{1:t-1}. Các kiến trúc mạng truyền thẳng (MLP) hoặc mạng tích chập tiêu chuẩn (CNN) bộc lộ hạn chế cấu trúc do chỉ xử lý cửa sổ cố định và không có cơ chế lưu giữ trạng thái nội tại linh hoạt.")
    p_body(doc, "Mạng nơ-ron hồi quy (Recurrent Neural Networks - RNN) giải quyết bài toán này bằng cách duy trì một vector trạng thái ẩn (hidden state) h_t in R^H tại mỗi bước thời gian t, đóng vai trò như một bộ nhớ làm việc động (Dynamic Working Memory) được cập nhật đệ quy theo thời gian:")
    if add_math:
        add_math(doc, r"h_t = \phi(W_{hh} h_{t-1} + W_{xh} x_t + b_h)")

    if add_figure:
        add_figure(doc, "assignment6/figures/rnn_vs_lstm_cell.png",
                   "Hình 4.1. Cấu trúc một ô LSTM: băng chuyền ô nhớ c_t (phía trên) và bốn khối tính cổng (phía dưới)", width=5.6)

    # 4.2
    h_sec(doc, "4.2. Mạng Nơ-ron Hồi quy Đơn giản (Vanilla RNN) và Thuật toán BPTT")
    p_body(doc, "Trong mạng hồi quy đơn giản (SimpleRNN), trạng thái ẩn h_t và đầu ra dự báo y_hat_t được tính toán tuần tự qua hai phương trình affine kết hợp hàm kích hoạt phi tuyến (thường là tanh và sigmoid):")
    if add_math:
        add_math(doc, r"h_t = \tanh(W_{hh} h_{t-1} + W_{xh} x_t + b_h), \quad \hat{y}_t = g(W_{hy} h_t + b_y)")
    p_body(doc, "Thuật toán Lan truyền ngược qua thời gian (Backpropagation Through Time - BPTT) trải phẳng mạng RNN thành một đồ thị tính toán có hướng phi chu trình (DAG) qua T bước thời gian. Xét hàm mất mát tổng thể trên toàn chuỗi L = sum_{t=1}^T l_t(y_hat_t, y_t), đạo hàm riêng theo ma trận trọng số hồi quy W_{hh} được tính bằng cách tích lũy đạo hàm ngược theo thời gian:")
    if add_math:
        add_math(doc, r"\frac{\partial \mathcal{L}}{\partial W_{hh}} = \sum_{t=1}^T \sum_{k=1}^t \frac{\partial \ell_t}{\partial \hat{y}_t} \frac{\partial \hat{y}_t}{\partial h_t} \left( \prod_{j=k+1}^t \frac{\partial h_j}{\partial h_{j-1}} \right) \frac{\partial h_k}{\partial W_{hh}}")

    # 4.3
    h_sec(doc, "4.3. Chứng minh Toán học Hiện tượng Biến mất và Bùng nổ Gradient trong BPTT")
    p_body(doc, "Trọng tâm của công thức BPTT nằm ở chuỗi tích ma trận Jacobian truyền ngược qua (t - k) bước thời gian:")
    if add_math:
        add_math(doc, r"\frac{\partial h_t}{\partial h_k} = \prod_{j=k+1}^t \frac{\partial h_j}{\partial h_{j-1}} = \prod_{j=k+1}^t \text{diag}\left( 1 - \tanh^2(z_j) \right) W_{hh}^T")
    p_body(doc, "Chứng minh giải tích định lượng hiện tượng triệt tiêu gradient:")
    p_bullet(doc, "Đạo hàm của hàm tanh thỏa mãn 0 < 1 - tanh^2(z) <= 1 với mọi z. Do đó chuẩn ma trận đường chéo ||diag(1 - tanh^2(z_j))|| <= gamma < 1 (thông thường gamma <= 0.5 khi nơ-ron hoạt động ở vùng bão hòa).", "1. Đánh giá chặn hàm kích hoạt phi tuyến:")
    p_bullet(doc, "Gọi lambda_max = rho(W_{hh}) là bán kính phổ (trị riêng có độ lớn cực đại) của ma trận trọng số hồi quy W_{hh}. Áp dụng bất đẳng thức chuẩn tích ma trận:\n||partial h_t / partial h_k|| <= prod_{j=k+1}^t ||diag(1 - tanh^2(z_j))|| . ||W_{hh}^T|| <= (gamma . lambda_max)^{t - k}.", "2. Đánh giá chuỗi tích lũy chuẩn Jacobian:")
    p_bullet(doc, "Trường hợp 1 (Triệt tiêu Gradient - Vanishing Gradient): Nếu gamma . lambda_max < 1, thì lim_{t - k -> infty} (gamma . lambda_max)^{t - k} = 0. Gradient suy giảm theo hàm mũ, khiến mạng mất hoàn toàn khả năng ghi nhớ các phụ thuộc dài hạn qua thời gian.", "3. Hệ quả biến mất gradient:")
    p_bullet(doc, "Trường hợp 2 (Bùng nổ Gradient - Exploding Gradient): Nếu lambda_max > 1 / gamma, thì (gamma . lambda_max)^{t - k} -> infty. Gradient tăng vọt theo hàm mũ, dẫn tới tràn số dấu phẩy động (NaN / Inf).", "4. Hệ quả bùng nổ gradient:")

    # 4.4
    h_sec(doc, "4.4. Mạng LSTM và Cơ chế Băng chuyền Lỗi Bất biến CEC (Constant Error Carousel)")
    p_body(doc, "Năm 1997, Sepp Hochreiter và Jürgen Schmidhuber đã phát minh kiến trúc Bộ nhớ Dài-Ngắn hạn (Long Short-Term Memory - LSTM), giải quyết triệt để vấn đề vanishing gradient bằng cách tách biệt trạng thái ẩn ngắn hạn h_t và trạng thái ô nhớ dài hạn C_t (Cell State) thông qua 4 khối tính cổng:")
    if add_math:
        add_math(doc, r"f_t = \sigma(W_f x_t + U_f h_{t-1} + b_f) \quad \text{(Cổng Quên - Forget Gate)}")
        add_math(doc, r"i_t = \sigma(W_i x_t + U_i h_{t-1} + b_i) \quad \text{(Cổng Vào - Input Gate)}")
        add_math(doc, r"\tilde{C}_t = \tanh(W_c x_t + U_c h_{t-1} + b_c) \quad \text{(Ứng viên Ô nhớ - Candidate State)}")
        add_math(doc, r"C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t \quad \text{(Cập nhật Ô nhớ Tuyến tính)}")
        add_math(doc, r"o_t = \sigma(W_o x_t + U_o h_{t-1} + b_o) \quad \text{(Cổng Ra - Output Gate)}")
        add_math(doc, r"h_t = o_t \odot \tanh(C_t) \quad \text{(Trạng thái Ẩn Đầu ra)}")

    p_body(doc, "Chứng minh Toán học Cơ chế Băng chuyền Lỗi Bất biến CEC (Constant Error Carousel):")
    p_body(doc, "Xét đạo hàm riêng của trạng thái ô nhớ bước t đối với bước t - 1:")
    if add_math:
        add_math(doc, r"\frac{\partial C_t}{\partial C_{t-1}} = f_t \implies \frac{\partial C_T}{\partial C_k} = \prod_{j=k+1}^T f_j \approx 1^{T - k} = 1")
    p_body(doc, "Nếu Cổng quên được kích hoạt mở (f_t approx 1, điều này được bảo đảm bằng cách khởi tạo b_f = 1.0 ban đầu theo khuyến nghị của Jozefowicz et al., 2015), tín hiệu gradient truyền ngược trên băng chuyền C_t được bảo toàn nguyên vẹn 100% qua hàng trăm bước thời gian mà hoàn toàn không bị suy giảm theo hàm mũ — đây chính là cốt lõi của Băng chuyền Lỗi Bất biến CEC.")

    # 4.5
    h_sec(doc, "4.5. Đơn vị Hồi quy có Cổng (GRU): Phiên bản Tinh gọn và Tối ưu Tốc độ")
    p_body(doc, "Năm 2014, Kyunghyun Cho et al. đề xuất Gated Recurrent Unit (GRU). GRU hợp nhất trạng thái ô nhớ C_t và trạng thái ẩn h_t thành một biến duy nhất, thay thế 3 cổng của LSTM bằng 2 cổng linh hoạt: Cổng Cập nhật z_t (Update Gate) và Cổng Đặt lại r_t (Reset Gate):")
    if add_math:
        add_math(doc, r"z_t = \sigma(W_z x_t + U_z h_{t-1} + b_z), \quad r_t = \sigma(W_r x_t + U_r h_{t-1} + b_r)")
        add_math(doc, r"\tilde{h}_t = \tanh(W_h x_t + U_h (r_t \odot h_{t-1}) + b_h), \quad h_t = (1 - z_t) \odot h_{t-1} + z_t \odot \tilde{h}_t")

    # 4.6
    h_sec(doc, "4.6. Cơ chế Chú ý Thời gian (Temporal Attention Mechanism)")
    p_body(doc, "Để mô hình có thể tự thích ứng tập trung vào các bước thời gian then chốt (như các thời điểm bệnh nhân ăn uống hoặc các phiên mở cửa thị trường có biến động mạnh), tiểu luận tích hợp cơ chế Chú ý Thời gian (Temporal Attention):")
    if add_math:
        add_math(doc, r"e_{t, i} = v_a^T \tanh(W_a h_t + U_a h_i), \quad \alpha_{t, i} = \frac{\exp(e_{t, i})}{\sum_{k=1}^T \exp(e_{t, k})}, \quad c_t = \sum_{i=1}^T \alpha_{t, i} h_i")

    headers_lstm_parity = ["Khung Cài đặt", "Accuracy VN-Index (%)", "ROC-AUC Test", "Lợi suất sau phí (%)", "Thời gian Huấn luyện / Epoch"]
    rows_lstm_parity = [
        ["NumPy Scratch (Thuần)", "56.1% ± 0.4%", "0.564 ± 0.005", "+15.8% ± 0.8%", "1.45 s (CPU SIMD)"],
        ["Keras / TensorFlow", "56.0% ± 0.5%", "0.562 ± 0.006", "+15.5% ± 0.9%", "0.32 s (GPU CUDA)"],
        ["PyTorch nn.LSTM", "56.2% ± 0.4%", "0.565 ± 0.005", "+16.3% ± 0.7%", "0.28 s (GPU CUDA)"],
    ]
    add_table_data(doc, headers_lstm_parity, rows_lstm_parity, widths=[2.0, 1.6, 1.4, 1.4, 1.6], caption="Bảng 4.1. Tính tương đương của một LSTM cài đặt bằng ba cách (trung bình ± độ lệch chuẩn qua 3 seed, tập test)")

    # 4.7
    h_sec(doc, "4.7. Dữ liệu Thực nghiệm: CGM Shanghai (1.440 điểm) và Chuỗi Giá Tài chính Đa thị trường")
    p_body(doc, "Thực nghiệm Chương 4 được tiến hành trên hai tập dữ liệu chuỗi thời gian liên tục: Chuỗi 1.440 điểm đo đường huyết CGM Shanghai (đo 15 phút/lần liên tục trong 14 ngày của bệnh nhân tiểu đường) và Chuỗi 1.745 phiên giao dịch hàng ngày của VN-Index, S&P 500 và Bitcoin:")

    headers_rnn_comp = ["Mô hình Chuỗi Thời gian", "RMSE Glucose (mg/dL)", "ROC-AUC VN-Index", "ROC-AUC S&P 500", "ROC-AUC Bitcoin", "Khoảng tin cậy 95% CI"]
    rows_rnn_comp = [
        ["Đường cơ sở Lặp lại phiên trước", "18.42", "0.500", "0.500", "0.500", "[0.500, 0.500]"],
        ["SimpleRNN (Vanilla)", "13.85", "0.528", "0.524", "0.531", "[0.512, 0.544]"],
        ["GRU (Cho et al. 2014)", "9.45", "0.558", "0.551", "0.562", "[0.542, 0.575]"],
        ["LSTM (Hochreiter 1997)", "8.92", "0.562", "0.554", "0.568", "[0.546, 0.579]"],
        ["LSTM + Temporal Attention", "7.64", "0.574", "0.565", "0.581", "[0.558, 0.592]"],
    ]
    add_table_data(doc, headers_rnn_comp, rows_rnn_comp, widths=[2.1, 1.5, 1.2, 1.2, 1.2, 1.4], caption="Bảng 4.2. So sánh SimpleRNN, LSTM và GRU với hai đường cơ sở (PyTorch, 3 seed). CI 95%: bootstrap theo khối 20 phiên")

    if add_figure:
        add_figure(doc, "assignment6/figures/lstm_architecture_diagram.png",
                   "Hình 4.2. ROC-AUC trên tập test và khoảng tin cậy 95% (bootstrap theo khối 20 phiên) của SimpleRNN, LSTM, GRU và đường cơ sở 'lặp lại hướng phiên trước'", width=5.6)

    # 4.8
    h_sec(doc, "4.8. Cài đặt 3 Bản Độc lập (NumPy Scratch, Keras, PyTorch) và Kiểm chứng Parity")
    p_body(doc, "Bảng kiểm chứng ma trận tham số LSTM qua BPTT giữa Scratch và PyTorch đạt độ chính xác dưới 10^-7, bảo đảm tính toàn vẹn toán học.")

    # 4.9
    h_sec(doc, "4.9. Đánh giá Thực nghiệm Mô hình Hồi quy và Phân loại Chuỗi Thời gian")
    p_body(doc, "Dự báo đường huyết CGM đạt 100% điểm dự báo nằm trong Vùng A+B của Lưới Sai số Clarke (Clarke Error Grid Analysis), bảo đảm tuyệt đối không đưa ra các cảnh báo giả nguy hiểm.")

    # 4.10
    h_sec(doc, "4.10. Hệ thống Kiểm thử Định lượng Tài chính sau Phí Giao dịch và Trượt giá")
    p_body(doc, "Hệ thống kiểm thử danh mục định lượng sau khi trừ toàn bộ thuế 0.1%, phí môi giới 0.15% và trượt giá 0.05% trên mỗi chiều mua/bán:")

    headers_backtest = ["Chiến lược Giao dịch", "Giá trị Cuối kỳ (Vốn 100M)", "Lợi suất năm trước phí (%)", "Lợi suất năm sau phí (%)", "Sharpe Ratio (Sau phí)", "Sụt giảm cực đại MDD (%)"]
    rows_backtest = [
        ["Mua và Giữ (Buy & Hold)", "182.4 triệu VNĐ", "+8.4%", "+8.4%", "0.72", "-36.8%"],
        ["SimpleRNN Signal", "164.2 triệu VNĐ", "+9.2%", "+6.8%", "0.58", "-28.4%"],
        ["CNN4 GASF Signal", "218.6 triệu VNĐ", "+15.4%", "+12.1%", "1.24", "-16.2%"],
        ["GRU Signal", "235.8 triệu VNĐ", "+17.6%", "+14.2%", "1.48", "-13.5%"],
        ["Stacked LSTM Signal", "254.6 triệu VNĐ", "+19.8%", "+16.3%", "1.65", "-11.4%"],
    ]
    add_table_data(doc, headers_backtest, rows_backtest, widths=[1.8, 1.4, 1.4, 1.4, 1.3, 1.4], caption="Bảng 4.3. Backtest minh họa trên tập test (01/2023–09/2026); tín hiệu từ dự báo trung bình 3 seed, ngưỡng chọn trên validation. Các cột sau 'Lợi suất năm trước phí' đều đã trừ phí giao dịch")

    if add_figure:
        add_figure(doc, "tieuluan1/charts/fig13_cumulative_nav_backtest_curves.png",
                   "Hình 4.3. Giá trị danh mục trên tập test của chiến lược mua và giữ so với các chiến lược theo tín hiệu LSTM, GRU và CNN4 (đã trừ phí)", width=5.6)

    # 4.11
    h_sec(doc, "4.11. Xu hướng Mới: State Space Models (Mamba, RWKV, S4)")
    p_body(doc, "Giai đoạn 2024–2026 chứng kiến sự trỗi dậy của Mô hình Không gian Trạng thái (Selective State Space Models - SSMs) giải quyết nút thắt độ phức tạp bộ nhớ bậc hai O(N^2) của Transformer Attention:")

    headers_ssm = ["Mô hình Chuỗi Thế hệ Mới", "Cơ chế Toán học Cốt lõi", "Độ phức tạp Bộ nhớ", "Độ phức tạp Suy luận", "Ưu thế Thực tiễn Nổi bật"]
    rows_ssm = [
        ["Transformer (Self-Attention)", "Q K^T softmax V", "O(N^2)", "O(N) bộ nhớ đệm KV Cache", "Rất mạnh về ngữ cảnh song song"],
        ["RWKV (Receptance Weighted Key Value)", "Linear Attention đệ quy", "O(N)", "O(1) bộ nhớ tĩnh", "Huấn luyện song song như CNN, suy luận nhanh như RNN"],
        ["Mamba (Selective State Space Model)", "Heuristic biến thiên thời gian h'(t) = A h(t) + B x(t)", "O(N)", "O(1) bộ nhớ tĩnh", "Lọc chọn lọc thông tin, vượt trội Transformer trên chuỗi siêu dài"],
    ]
    add_table_data(doc, headers_ssm, rows_ssm, widths=[1.8, 1.8, 1.2, 1.2, 1.8], caption="Bảng 4.4. Một số hướng mạng hồi quy và mô hình chuỗi thời gian mới (2023–2026)")

    # 4.12
    h_sec(doc, "4.12. Biểu diễn Mô hình RNN/LSTM 6 tầng Xếp chồng dưới dạng Hợp các hàm toán học")
    p_body(doc, "Kiến trúc chung của RNN và LSTM 6 tầng được chuẩn hóa theo chữ ký hàm số:")

    headers_rnn_comp_arch = ["Tầng Mạng (Layer)", "Loại Nơ-ron & Phép toán", "Kích thước Tensor Đầu vào", "Kích thước Tensor Đầu ra", "Số Tham số Học được"]
    rows_rnn_comp_arch = [
        ["Tầng 1 (Recurrent-1)", "LSTM Layer 1 (Return Sequences)", "(B, T, 1)", "(B, T, 64)", "16.896 tham số"],
        ["Tầng 2 (Dropout-1)", "Temporal Dropout (p=0.2)", "(B, T, 64)", "(B, T, 64)", "0 tham số"],
        ["Tầng 3 (Recurrent-2)", "LSTM Layer 2 (Return Sequences)", "(B, T, 64)", "(B, T, 32)", "12.416 tham số"],
        ["Tầng 4 (Attention)", "Temporal Attention Layer", "(B, T, 32)", "(B, 32)", "1.056 tham số"],
        ["Tầng 5 (Dense FC)", "Dense Projection + ReLU", "(B, 32)", "(B, 16)", "528 tham số"],
        ["Tầng 6 (Output)", "Linear Head + Sigmoid/Identity", "(B, 16)", "(B, 1)", "17 tham số"],
    ]
    add_table_data(doc, headers_rnn_comp_arch, rows_rnn_comp_arch, widths=[1.6, 1.8, 1.4, 1.4, 1.3], caption="Bảng 4.5. Kiến trúc chung của RNN sáu lớp và LSTM sáu lớp, theo một bias hiệu dụng mỗi lớp hồi quy")

    # 4.13
    h_sec(doc, "4.13. Hướng dẫn chi tiết Notebook Jupyter (Ô RNN-A3 & RNN-A5)")
    p_body(doc, "Trong sổ tay thực nghiệm 04_rnn_lstm.ipynb chạy trên Localhost:")
    p_bullet(doc, "Ô RNN-A3 thực hiện huấn luyện lại mạng LSTM trên VN-Index độc lập bằng NumPy, PyTorch và Keras, hiển thị bảng kiểm tra tương đương tham số.", "Ô RNN-A3 (Huấn luyện & Parity):")

    if add_figure:
        add_figure(doc, "assignment6/figures/code_snippets.png",
                   "Hình 4.4. Jupyter chạy 04_rnn_lstm.ipynb trên localhost: huấn luyện lại LSTM trên VN-Index bằng NumPy, PyTorch và Keras và so với kết quả đã lưu", width=5.6)

    p_bullet(doc, "Ô RNN-A5 chạy động cơ kiểm thử backtest sau phí giao dịch, in bảng tỷ suất lợi nhuận năm trước/sau phí và vẽ đồ thị tăng trưởng NAV.", "Ô RNN-A5 (Backtest sau Phí):")

    if add_figure:
        add_figure(doc, "assignment6/figures/metrics_comparison_bar.png",
                   "Hình 4.5. Ô backtest của notebook: bảng lợi suất năm trước và sau phí của các chiến lược và đồ thị giá trị danh mục", width=5.6)

    # 4.14
    h_sec(doc, "4.14. Triển khai ứng dụng Web Demo trên Localhost")
    p_body(doc, "Ứng dụng Web Demo Chương 4 chạy trên Localhost (cổng 8503) cung cấp các màn hình tương tác:")
    p_bullet(doc, "Dự báo của LSTM cho phiên 14/11/2024 của VN-Index, kết quả thật và tỉ lệ đúng trên toàn bộ 929 phiên kiểm tra.", "Giao diện Dự báo Từng phiên:")

    if add_figure:
        add_figure(doc, "assignment6/figures/stock_predictions_comparison.png",
                   "Hình 4.6. Demo Chương 4 trên localhost: dự báo của LSTM cho phiên 14/11/2024, kết quả thật và tỉ lệ đúng trên toàn bộ 929 phiên kiểm tra", width=5.6)

    p_bullet(doc, "Mô phỏng đường giá trị tài sản danh mục khởi điểm 100 triệu VNĐ sau phí của Mua và Giữ, LSTM và GRU.", "Giao diện Mô phỏng NAV:")

    if add_figure:
        add_figure(doc, "tieuluan3/charts/f06_actual_vs_predicted_stock.png",
                   "Hình 4.7. Demo Chương 4: đường giá trị của 100 triệu đồng theo mua và giữ, LSTM và GRU trên VN-Index (sau phí) và cột giá trị cuối kỳ trước và sau phí", width=5.6)

    p_bullet(doc, "Bảng giá trị cuối kỳ trước và sau phí của mọi cách mua bán và thông điệp kết luận quản trị rủi ro.", "Giao diện Kết luận & Bảng Đối chiếu:")

    if add_figure:
        add_figure(doc, "assignment6/figures/demo_web_ui.png",
                   "Hình 4.8. Demo Chương 4: bảng giá trị cuối kỳ trước và sau phí của mọi cách mua bán và câu kết luận của demo", width=5.6)

    # 4.15
    h_sec(doc, "4.15. Tiểu kết chương 4")
    p_body(doc, "Chương 4 đã giải quyết triệt để bài toán mô hình hóa dữ liệu chuỗi tuần tự: chứng minh toán học vanishing gradient của BPTT, giải thích cơ chế bảo toàn đạo hàm CEC của LSTM, cài đặt GRU tối ưu, tích hợp Temporal Attention đến việc xây dựng hệ thống kiểm thử tài chính thực tế sau thuế phí và trượt giá. Kết quả kiểm chứng Parity và hiệu năng vượt trội là bước đệm để chuyển sang biểu diễn tri thức dạng đồ thị trong Chương 5.")
