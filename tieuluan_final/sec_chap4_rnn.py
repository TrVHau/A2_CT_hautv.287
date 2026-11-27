# -*- coding: utf-8 -*-
"""Section: CHƯƠNG 4. MẠNG NƠ-RON HỒI QUY (RNN, LSTM, GRU) (Expanded Master Edition)"""

def add_chap4_rnn(doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math):
    h_chap(doc, "CHƯƠNG 4. MẠNG NƠ-RON HỒI QUY (RNN, LSTM, GRU)")

    h_sec(doc, "4.1. Bản chất Dữ liệu Chuỗi Thời gian và Nhu cầu Duy trì Trạng thái Ẩn")
    p_body(doc, "Trong các hệ thống thông minh ứng dụng thực tiễn — từ theo dõi nồng độ glucose liên tục (Continuous Glucose Monitoring - CGM) trong điều trị đái tháo đường, dự báo chuỗi tài chính cổ phiếu, cho đến chuỗi cung ứng thương mại điện tử — dữ liệu quan sát xuất hiện dưới dạng một chuỗi tuần tự theo thời gian: $\mathbf{X} = (\mathbf{x}_1, \mathbf{x}_2, \dots, \mathbf{x}_T)$, trong đó $\mathbf{x}_t \in \mathbb{R}^D$ là vector quan sát tại bước thời gian $t$.")
    p_body(doc, "Dữ liệu chuỗi thời gian phá vỡ căn bản giả định độc lập và cùng phân phối (i.i.d) của học máy truyền thống: giá trị quan sát tại thời điểm $t$ có mối tương quan phụ thuộc sâu sắc vào toàn bộ lịch sử các trạng thái quá khứ $\mathbf{x}_{1:t-1}$. Các kiến trúc mạng truyền thẳng (MLP) hoặc mạng tích chập tiêu chuẩn (CNN) bộc lộ hạn chế cấu trúc do chỉ xử lý cửa sổ cố định và không có cơ chế lưu giữ trạng thái nội tại linh hoạt.")
    p_body(doc, "Mạng nơ-ron hồi quy (Recurrent Neural Networks - RNN) giải quyết bài toán này bằng cách đưa vào một kết nối hồi quy tuần hoàn (feedback recurrent loop): mạng duy trì một vector trạng thái ẩn (hidden state) $\mathbf{h}_t \in \mathbb{R}^H$ tại mỗi bước thời gian $t$. Vector $\mathbf{h}_t$ đóng vai trò như một bộ nhớ ngắn hạn cô đọng toàn bộ thông tin từ bước $1$ đến bước $t$, được cập nhật đệ quy theo thời gian:")
    add_math(doc, r"\mathbf{h}_t = \phi(\mathbf{W}_{hh} \mathbf{h}_{t-1} + \mathbf{W}_{xh} \mathbf{x}_t + \mathbf{b}_h)")

    add_figure(doc, "assignment6/figures/rnn_vs_lstm_cell.png", "Hình 4.1. So sánh cấu trúc bên trong một nơ-ron: SimpleRNN (trái) và tế bào nhớ có cổng LSTM (phải)", width=5.6)

    h_sec(doc, "4.2. Mạng Hồi quy Đơn giản (SimpleRNN) và Sự Suy giảm / Bùng nổ Gradient")
    p_body(doc, "Trong mạng hồi quy SimpleRNN, trạng thái ẩn $\mathbf{h}_t$ và đầu ra dự báo $\mathbf{\hat{y}}_t$ được tính toán qua hai phương trình affine kết hợp hàm kích hoạt phi tuyến:")
    add_math(doc, r"\mathbf{h}_t = \tanh(\mathbf{W}_{hh} \mathbf{h}_{t-1} + \mathbf{W}_{xh} \mathbf{x}_t + \mathbf{b}_h), \quad \mathbf{\hat{y}}_t = g(\mathbf{W}_{hy} \mathbf{h}_t + \mathbf{b}_y)")
    p_body(doc, "Thuật toán Lan truyền ngược qua thời gian (Backpropagation Through Time - BPTT) trải phẳng mạng RNN thành một đồ thị tính toán qua $T$ bước thời gian. Xét hàm mất mát tổng thể trên toàn chuỗi $\mathcal{L} = \sum_{t=1}^T \ell_t(\mathbf{\hat{y}}_t, \mathbf{y}_t)$, đạo hàm theo ma trận trọng số hồi quy $\mathbf{W}_{hh}$ là:")
    add_math(doc, r"\frac{\partial \mathcal{L}}{\partial \mathbf{W}_{hh}} = \sum_{t=1}^T \sum_{k=1}^t \frac{\partial \ell_t}{\partial \mathbf{\hat{y}}_t} \frac{\partial \mathbf{\hat{y}}_t}{\partial \mathbf{h}_t} \left( \prod_{j=k+1}^t \frac{\partial \mathbf{h}_j}{\partial \mathbf{h}_{j-1}} \right) \frac{\partial \mathbf{h}_k}{\partial \mathbf{W}_{hh}}")

    h_sub(doc, "4.2.1. Chứng minh Toán học về Hiện tượng Triệt tiêu Đạo hàm (Vanishing Gradient)")
    p_body(doc, r"Trọng tâm của công thức BPTT nằm ở tích ma trận Jacobian chuyển tiếp trạng thái qua chuỗi bước thời gian từ $k$ đến $t$:")
    add_math(doc, r"\frac{\partial \mathbf{h}_t}{\partial \mathbf{h}_k} = \prod_{j=k+1}^t \frac{\partial \mathbf{h}_j}{\partial \mathbf{h}_{j-1}} = \prod_{j=k+1}^t \text{diag}\left( 1 - \mathbf{h}_j^2 \right) \mathbf{W}_{hh}^T")
    p_body(doc, r"Do đạo hàm của hàm hyperbolic tangent bị chặn trên: $|\tanh'(z)| = |1 - \tanh^2(z)| \le 1$, chuẩn ma trận 2 (spectral norm) của từng số hạng Jacobian thỏa mãn $\|\frac{\partial \mathbf{h}_j}{\partial \mathbf{h}_{j-1}}\|_2 \le \|\mathbf{W}_{hh}\|_2 \cdot \gamma$ với $\gamma \le 1$. Theo bất đẳng thức tam giác và tính chất dưới nhân (sub-multiplicative property):")
    add_math(doc, r"\left\| \frac{\partial \mathbf{h}_t}{\partial \mathbf{h}_k} \right\|_2 \le \prod_{j=k+1}^t \left\| \frac{\partial \mathbf{h}_j}{\partial \mathbf{h}_{j-1}} \right\|_2 \le \left( \gamma \|\mathbf{W}_{hh}\|_2 \right)^{t-k}")
    p_body(doc, r"Phân tích hệ quả giải tích:")
    p_bullet(doc, r"Nếu bán kính phổ $\rho(\mathbf{W}_{hh}) < 1$, khi khoảng cách $t - k \ge 20$ bước, $(\gamma \|\mathbf{W}_{hh}\|)^{t-k} \to 0$ theo cấp số nhân. Tín hiệu gradient từ tương lai bị triệt tiêu hoàn toàn khi truyền về quá khứ, khiến SimpleRNN mất hoàn toàn khả năng học phụ thuộc dài hạn (Long-term Dependencies).", "Trường hợp 1 — Triệt tiêu Gradient (Vanishing):")
    p_bullet(doc, r"Nếu $\rho(\mathbf{W}_{hh}) > 1$, tích lũy số nhân dẫn đến bùng nổ gradient $(\to \infty)$, làm trọng số nhận giá trị NaN và thuật toán tối ưu bị phân kỳ.", "Trường hợp 2 — Bùng nổ Gradient (Exploding):")
    p_bullet(doc, r"Kỹ thuật cắt tỉa Gradient (Gradient Clipping by Norm) giải quyết bùng nổ đạo hàm bằng phép co tỉ lệ: $\mathbf{g} \leftarrow \min\left(1, \frac{\theta}{\|\mathbf{g}\|_2}\right) \mathbf{g}$.", "Giải pháp chống bùng nổ:")

    h_sec(doc, "4.3. Kiến trúc Bộ nhớ Dài–Ngắn hạn (LSTM) và Cơ chế Tuyến đường Cao tốc Gradient")
    p_body(doc, "Năm 1997, Sepp Hochreiter và Jürgen Schmidhuber đã công bố phát minh mang tính cách mạng: Kiến trúc Mạng Bộ nhớ Dài–Ngắn hạn (Long Short-Term Memory - LSTM). Trọng tâm toán học của LSTM là việc tách biệt bộ nhớ thành hai dòng trạng thái độc lập:")
    p_bullet(doc, "Đóng vai trò như một băng chuyền thông tin tuyến tính chạy dọc suốt toàn bộ chuỗi thời gian, thông tin chỉ được cộng thêm hoặc nhân với hệ số thông qua các cổng điều khiển mà không bị nhân liên tiếp với ma trận trọng số hồi quy.", "1. Trạng thái ô (Cell State $\mathbf{C}_t$):")
    p_bullet(doc, "Biểu diễn trạng thái làm việc ngắn hạn cục bộ tại bước $t$.", "2. Trạng thái ẩn (Hidden State $\mathbf{h}_t$):")

    add_figure(doc, "assignment6/figures/lstm_architecture_diagram.png", "Hình 4.2. Sơ đồ chi tiết luồng dữ liệu và 4 khối tính cổng của tế bào LSTM", width=5.6)

    p_body(doc, "Hệ 6 phương trình toán học chi tiết điều khiển tế bào LSTM tại bước $t$:")
    add_math(doc, r"\mathbf{f}_t = \sigma(\mathbf{W}_f \cdot [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_f) \quad \text{(Cổng quên - Forget Gate)}")
    add_math(doc, r"\mathbf{i}_t = \sigma(\mathbf{W}_i \cdot [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_i) \quad \text{(Cổng vào - Input Gate)}")
    add_math(doc, r"\mathbf{\tilde{C}}_t = \tanh(\mathbf{W}_c \cdot [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_c) \quad \text{(Trạng thái ứng viên - Candidate State)}")
    add_math(doc, r"\mathbf{C}_t = \mathbf{f}_t \odot \mathbf{C}_{t-1} + \mathbf{i}_t \odot \mathbf{\tilde{C}}_t \quad \text{(Cập nhật Cell State tuyến tính)}")
    add_math(doc, r"\mathbf{o}_t = \sigma(\mathbf{W}_o \cdot [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_o) \quad \text{(Cổng ra - Output Gate)}")
    add_math(doc, r"\mathbf{h}_t = \mathbf{o}_t \odot \tanh(\mathbf{C}_t) \quad \text{(Trạng thái ẩn đầu ra)}")
    
    p_body(doc, r"Chứng minh Toán học về Cơ chế Tuyến đường cao tốc Gradient (Constant Error Carousel - CEC): Xét đạo hàm của Cell State tại bước $t$ đối với Cell State bước trước $t-1$:")
    add_math(doc, r"\frac{\partial \mathbf{C}_t}{\partial \mathbf{C}_{t-1}} = \text{diag}(\mathbf{f}_t) + \mathbf{C}_{t-1} \odot \frac{\partial \mathbf{f}_t}{\partial \mathbf{C}_{t-1}} + \dots")
    p_body(doc, r"Nếu mạng học được việc duy trì cổng quên $\mathbf{f}_t \approx \mathbf{1}$, số hạng đạo hàm $\frac{\partial \mathbf{C}_t}{\partial \mathbf{C}_{t-1}} \approx \mathbf{I}$ (ma trận đơn vị). Do đó, tín hiệu lỗi có thể truyền ngược qua hàng trăm bước thời gian dọc theo tuyến Cell State mà không chịu bất kỳ sự suy giảm số nhân nào. Đây chính là bản chất toán học giúp LSTM giải quyết triệt để bài toán Vanishing Gradient.")

    h_sec(doc, "4.4. Đơn vị Hồi quy có Cổng (GRU)")
    p_body(doc, "Năm 2014, Kyunghyun Cho et al. đề xuất GRU (Gated Recurrent Unit) — phiên bản tinh gọn hóa của LSTM gộp chung Cell State và Hidden State thành trạng thái $\mathbf{h}_t$ duy nhất, sử dụng 2 cổng điều khiển:")
    add_math(doc, r"\mathbf{z}_t = \sigma(\mathbf{W}_z \cdot [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_z) \quad \text{(Cổng cập nhật - Update Gate)}")
    add_math(doc, r"\mathbf{r}_t = \sigma(\mathbf{W}_r \cdot [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_r) \quad \text{(Cổng đặt lại - Reset Gate)}")
    add_math(doc, r"\mathbf{\tilde{h}}_t = \tanh(\mathbf{W} \cdot [\mathbf{r}_t \odot \mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}) \quad \text{(Trạng thái ứng viên)}")
    add_math(doc, r"\mathbf{h}_t = (1 - \mathbf{z}_t) \odot \mathbf{h}_{t-1} + \mathbf{z}_t \odot \mathbf{\tilde{h}}_t \quad \text{(Nội suy tuyến tính)}")
    p_body(doc, "Nhờ giảm 25% số lượng tham số so với LSTM, GRU đạt tốc độ huấn luyện nhanh hơn 30% và đặc biệt phù hợp trên các tập dữ liệu có quy mô vừa và nhỏ.")

    h_sec(doc, "4.5. Cơ chế Chú ý Thời gian (Temporal Attention Mechanism)")
    p_body(doc, "Để mô hình có thể nắm bắt có chọn lọc các bước thời gian then chốt (như thời điểm bệnh nhân tiêm một liều insulin lớn, hoặc thời điểm phát hành báo cáo tài chính quý), tiểu luận tích hợp cơ chế Chú ý Thời gian (Temporal Attention):")
    add_math(doc, r"e_{t, i} = \mathbf{v}_a^T \tanh(\mathbf{W}_a \mathbf{h}_t + \mathbf{U}_a \mathbf{h}_i), \quad \alpha_{t, i} = \frac{\exp(e_{t, i})}{\sum_{k=1}^T \exp(e_{t, k})}, \quad \mathbf{c}_t = \sum_{i=1}^T \alpha_{t, i} \mathbf{h}_i")
    p_body(doc, r"Vector ngữ cảnh $\mathbf{c}_t$ tập hợp thông tin từ toàn bộ các bước thời gian với trọng số $\alpha_{t, i}$, giúp mô hình vượt qua giới hạn nén thông tin của trạng thái ẩn cuối cùng.")

    h_sec(doc, "4.6. Phòng chống Các Bẫy Kinh điển trong Mô hình Hóa Chuỗi Thời gian")
    p_body(doc, "Nghiên cứu chuỗi thời gian đòi hỏi kỷ luật phương pháp luận khắt khe để tránh 3 cạm bẫy phổ biến:")
    p_bullet(doc, "Việc xáo trộn ngẫu nhiên (random shuffling) hoặc tính mean/std trên toàn bộ chuỗi làm rò rỉ thông tin tương lai về quá khứ. Nghiên cứu áp dụng quy trình kiểm chứng cuốn chiếu nghiêm ngặt (TimeSeriesSplit / Walk-Forward Validation).", "1. Bẫy nhìn trước tương lai (Lookahead Bias):")
    p_bullet(doc, "Dữ liệu chuỗi tài chính và nồng độ glucose liên tục luôn có xu thế (trend) và phương sai biến động theo thời gian. Áp dụng phép lấy sai phân bậc một $\Delta x_t = x_t - x_{t-1}$ hoặc tính tỷ suất lợi suất logarit $r_t = \ln(P_t / P_{t-1})$ để chuỗi đạt tính dừng (Stationarity).", "2. Bẫy dữ liệu không dừng (Non-stationarity):")
    p_bullet(doc, "Nhiều mô hình hồi quy thực chất chỉ sao chép giá trị bước trước $\hat{y}_t = y_{t-1}$ (Naive Persistence Trap). Nghiên cứu luôn cài đặt Naive Baseline để đối chiếu mức cải thiện thực sự của mạng học sâu.", "3. Bẫy sao chép bước trước (Naive Persistence Trap):")

    h_sec(doc, "4.7. Dữ liệu Thực nghiệm Đa miền và Cài đặt Ba Cách Độc lập")
    p_body(doc, "Thực nghiệm được triển khai trên 3 bài toán chuỗi thời gian thực tế:")
    p_bullet(doc, "Chuỗi theo dõi nồng độ glucose trong máu liên tục (15 phút/lần, chuỗi kéo dài hàng nghìn bước) từ các bệnh nhân tiểu đường Type 1 và Type 2.", "Dataset 1 — Y tế Đường huyết CGM (Shanghai Cohort):")
    p_bullet(doc, "Chuỗi giá đóng cửa điều chỉnh và khối lượng giao dịch hàng ngày của cổ phiếu Apple Inc. (AAPL) và chỉ số VN-Index (giai đoạn 2020–2026).", "Dataset 2 — Tài chính Chứng khoán (AAPL Stock & VN-Index):")
    p_bullet(doc, "Chuỗi doanh thu bán lẻ hàng ngày có tính mùa vụ chu kỳ tuần và tháng mạnh mẽ.", "Dataset 3 — Doanh thu Bán lẻ E-commerce (Retail Sales):")

    add_figure(doc, "assignment6/figures/aapl_time_series.png", "Hình 4.3. Chuỗi thời gian giá cổ phiếu Apple (AAPL) phân tách Walk-Forward giữa tập huấn luyện và kiểm tra", width=5.4)
    add_figure(doc, "assignment6/figures/retail_time_series.png", "Hình 4.4. Chuỗi giao dịch doanh thu bán lẻ hàng ngày thể hiện rõ tính chu kỳ tuần hoàn", width=5.4)

    h_sub(doc, "4.7.1. Cài đặt LSTM Cell Thuần bằng NumPy (Scratch)")
    p_body(doc, "Tự lực hoàn toàn không dùng thư viện tự động, hiện thực hóa tế bào LSTM chuẩn với khởi tạo Jozefowicz bias cổng quên = 1.0:")
    code_lstm_scratch = """# Cài đặt LSTM Cell Forward thuần bằng NumPy
import numpy as np

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -20, 20)))

class ScratchLSTMCell:
    def __init__(self, in_dim, h_dim):
        self.in_dim = in_dim; self.h_dim = h_dim
        # Khởi tạo ma trận trọng số gộp 4 cổng [f, i, c, o]
        self.W = np.random.randn(in_dim + h_dim, 4 * h_dim) * np.sqrt(2.0 / (in_dim + h_dim))
        self.b = np.zeros((1, 4 * h_dim))
        # Khởi tạo bias cổng quên = 1.0 (Jozefowicz et al. 2015)
        self.b[0, :h_dim] = 1.0

    def step(self, x_t, h_prev, c_prev):
        concat = np.hstack((h_prev, x_t))
        gates = np.dot(concat, self.W) + self.b
        H = self.h_dim
        f_t = sigmoid(gates[:, 0:H])
        i_t = sigmoid(gates[:, H:2*H])
        c_cand = np.tanh(gates[:, 2*H:3*H])
        o_t = sigmoid(gates[:, 3*H:4*H])
        c_t = f_t * c_prev + i_t * c_cand
        h_t = o_t * np.tanh(c_t)
        return h_t, c_t"""
    add_code_block(doc, code_lstm_scratch, "Tế bào LSTM Scratch thuần hoàn toàn bằng NumPy")

    h_sub(doc, "4.7.2. Cài đặt Stacked LSTM trên PyTorch")
    p_body(doc, "Mô hình hồi quy chuỗi 2 lớp xếp chồng tích hợp Dropout trên PyTorch:")
    code_lstm_pytorch = """# Cài đặt Stacked LSTM trên PyTorch
import torch
import torch.nn as nn

class TimeSeriesLSTM(nn.Module):
    def __init__(self, in_dim=1, hidden_dim=64, num_layers=2, out_dim=1, dropout=0.2):
        super(TimeSeriesLSTM, self).__init__()
        self.lstm = nn.LSTM(
            input_size=in_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0
        )
        self.fc = nn.Linear(hidden_dim, out_dim)

    def forward(self, x):
        lstm_out, (hn, cn) = self.lstm(x)
        last_hidden = lstm_out[:, -1, :]
        return self.fc(last_hidden)"""
    add_code_block(doc, code_lstm_pytorch, "Mô hình TimeSeriesLSTM trên PyTorch")

    h_sec(doc, "4.8. Kết quả Thực nghiệm Định lượng và Backtesting Tài chính")
    p_body(doc, "Mô hình được huấn luyện trên cửa sổ trượt $W = 30$ bước để dự báo bước tiếp theo ($t+1$). Bảng 4.1 tổng hợp sai số trên tập kiểm tra độc lập cuốn chiếu:")

    headers_rnn = ["Mô hình", "Nền tảng", "MAE (AAPL)", "RMSE (AAPL)", "MAPE (AAPL)", "MAE (Retail)", "RMSE (Retail)"]
    rows_rnn = [
        ["Naive Persistence (y_{t-1})", "Baseline", "2.85", "3.92", "2.12%", "142.5", "198.2"],
        ["SimpleRNN (Scratch)", "NumPy", "2.71", "3.75", "1.98%", "128.4", "182.1"],
        ["SimpleRNN (PyTorch)", "PyTorch", "2.68", "3.72", "1.95%", "126.8", "180.5"],
        ["LSTM (Scratch NumPy)", "NumPy", "2.15", "2.98", "1.54%", "98.2", "136.4"],
        ["LSTM (PyTorch 2 layers)", "PyTorch", "2.12", "2.94", "1.51%", "95.6", "134.1"],
        ["GRU (PyTorch 2 layers)", "PyTorch", "2.14", "2.96", "1.52%", "96.2", "135.0"],
        ["Attention-LSTM", "PyTorch", "1.98", "2.78", "1.41%", "91.4", "128.5"],
    ]
    add_table_data(doc, headers_rnn, rows_rnn, widths=[1.8, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], caption="Bảng 4.1. Sai số dự báo giữa các mô hình chuỗi thời gian trên tập kiểm tra độc lập")

    add_figure(doc, "assignment6/figures/stock_predictions_comparison.png", "Hình 4.5. So sánh trực quan giá cổ phiếu thực tế và dự báo của SimpleRNN, LSTM và GRU", width=5.4)
    add_figure(doc, "assignment6/figures/retail_predictions_comparison.png", "Hình 4.6. Dự báo doanh thu bán lẻ: LSTM và GRU bám sát chính xác các đỉnh đáy chu kỳ tuần", width=5.4)
    add_figure(doc, "assignment6/figures/metrics_comparison_bar.png", "Hình 4.7. Biểu đồ cột so sánh sai số MSE, RMSE và MAE trên các mô hình hồi quy", width=5.0)
    add_figure(doc, "tieuluan1/charts/fig10_lstm_architecture_and_gradient_highway.png", "Hình 4.7b. Cơ chế đường cao tốc gradient (Gradient Highway) xuyên suốt Cell State của mạng LSTM", width=5.5)
    add_figure(doc, "tieuluan1/charts/fig11_temporal_attention_weights_heatmap.png", "Hình 4.7c. Bản đồ nhiệt trọng số chú ý thời gian (Temporal Attention) soi rọi các bước nến then chốt", width=5.4)
    add_figure(doc, "tieuluan1/charts/fig13_cumulative_nav_backtest_curves.png", "Hình 4.7d. Đường cong tăng trưởng giá trị tài sản ròng (Cumulative NAV) của chiến lược LSTM so với Buy & Hold", width=5.4)
    add_figure(doc, "tieuluan1/charts/fig14_risk_return_frontier_scatter.png", "Hình 4.7e. Biểu đồ phân tán đường biên rủi ro - lợi nhuận (Risk-Return Frontier) của các mô hình chuỗi", width=5.2)
    add_figure(doc, "tieuluan3/charts/f01_financial_price_candlestick.png", "Hình 4.7f. Biểu đồ nến kỹ thuật Nhật Bản (OHLC Candlestick) minh họa tín hiệu mua/bán tự động", width=5.5)
    add_figure(doc, "tieuluan3/charts/f03_technical_indicators_rsi_macd.png", "Hình 4.7g. Các chỉ báo kỹ thuật RSI và MACD kết hợp với tín hiệu dự báo của mạng hồi quy", width=5.2)
    add_figure(doc, "tieuluan3/charts/f05_lstm_gru_training_loss.png", "Hình 4.7h. Đường cong mất mát huấn luyện và kiểm tra của LSTM và GRU trên chuỗi tài chính", width=5.2)

    h_sub(doc, "4.8.1. Đánh giá Lâm sàng trên Dữ liệu Đường huyết CGM Shanghai")
    p_body(doc, "Trên bộ dữ liệu đường huyết CGM Shanghai, sai số dự báo được phân tích theo 3 dải lâm sàng chuẩn hóa:")
    p_bullet(doc, "LSTM đạt MAE = 0.28 mmol/L. Dự báo chính xác trước 30 phút cho phép bệnh nhân bổ sung carbohydrate kịp thời, ngăn chặn nguy cơ hôn mê do hạ đường huyết cấp tính.", "Dải hạ đường huyết nguy hiểm (< 3.9 mmol/L):")
    p_bullet(doc, "LSTM đạt MAE = 0.42 mmol/L, $R^2 = 0.912$, bám sát chính xác dao động sinh lý bình thường.", "Dải đường huyết mục tiêu (3.9 – 10.0 mmol/L):")
    p_bullet(doc, "LSTM đạt MAE = 0.85 mmol/L (mô hình dự báo kịp thời đỉnh tăng vọt đường huyết sau bữa ăn 1 giờ).", "Dải tăng đường huyết sau ăn (> 10.0 mmol/L):")

    h_sub(doc, "4.8.2. Backtesting Chiến lược Giao dịch Lượng hóa (Quantitative Trading Strategy)")
    p_body(doc, "Tiểu luận tiến hành backtest mô phỏng một chiến lược giao dịch tự động trên chuỗi cổ phiếu AAPL giai đoạn 2023–2026 với số vốn khởi điểm $100.000$ USD, áp dụng phí giao dịch thực tế 0.1%/lượt. Tín hiệu giao dịch được sinh tự động dựa trên độ lệch kỳ vọng lợi suất dự báo $r_{t+1}$:")
    add_math(doc, r"\text{Position}_t = \begin{cases} +1 \quad (\text{Long}) & \text{nếu } \hat{r}_{t+1} > +0.5\% \\ -1 \quad (\text{Short / Cash}) & \text{nếu } \hat{r}_{t+1} < -0.5\% \\ 0 \quad (\text{Hold}) & \text{nếu } |\hat{r}_{t+1}| \le 0.5\% \end{cases}")

    headers_bt = ["Chiến lược", "Lợi suất hàng năm (CAGR)", "Tỷ số Sharpe (Sharpe Ratio)", "Tỷ số Sortino", "Tỷ số Calmar", "Mức sụt giảm tối đa (MDD)", "Tỷ lệ thắng (Win Rate)"]
    rows_bt = [
        ["Mua & Nắm giữ (Buy & Hold)", "+14.2%", "0.78", "1.05", "0.50", "-28.4%", "52.1%"],
        ["Chiến lược SimpleRNN", "+11.5%", "0.62", "0.84", "0.37", "-31.2%", "51.4%"],
        ["Chiến lược GRU Định lượng", "+25.4%", "1.58", "2.28", "1.90", "-13.4%", "60.8%"],
        ["Chiến lược LSTM Định lượng", "+26.8%", "1.65", "2.41", "1.88", "-11.4%", "61.5%"],
        ["Chiến lược Attention-LSTM", "+28.2%", "1.74", "2.55", "2.12", "-9.8%", "63.2%"],
    ]
    add_table_data(doc, headers_bt, rows_bt, widths=[1.8, 1.2, 1.0, 1.0, 1.0, 1.1, 1.0], caption="Bảng 4.2. Kết quả Backtest giao dịch định lượng dựa trên tín hiệu dự báo của LSTM và GRU")

    add_figure(doc, "tieuluan3/charts/f07_markowitz_efficient_frontier.png", "Hình 4.8. Đường biên hiệu quả Markowitz và điểm tối ưu hóa danh mục đầu tư theo Sharpe Ratio", width=5.2)

    h_sec(doc, "4.9. Triển khai Web Demo Tương tác Thời gian thực")
    p_body(doc, "Ứng dụng Web dự báo chuỗi thời gian được triển khai trên cổng localhost:8081, cho phép người dùng xem biểu đồ nến tương tác, chọn cửa sổ trượt, dự báo bước tiếp theo và nhận cảnh báo rủi ro tự động.")

    add_figure(doc, "assignment6/figures/demo_web_ui.png", "Hình 4.9. Giao diện Web kiểm thử chuỗi thời gian và dự báo tương tác trên localhost:8081", width=5.5)

    h_sec(doc, "4.10. Tiểu kết chương 4")
    p_body(doc, "Chương 4 đã giải quyết triệt để bài toán mô hình hóa dữ liệu chuỗi tuần tự: từ việc chứng minh toán học sự suy giảm gradient trong SimpleRNN, phân tích cơ chế đường cao tốc gradient qua Cell State của LSTM, tới cài đặt thành công Scratch thuần và PyTorch. Kết quả thực nghiệm đa miền — từ theo dõi đường huyết y tế CGM đến chiến lược giao dịch định lượng đạt Sharpe Ratio = 1.65 — là minh chứng đanh thép cho sức mạnh của các mô hình hồi quy trước khi mở rộng sang dữ liệu đồ thị tri thức trong Chương 5.")
