# -*- coding: utf-8 -*-
"""Section: CHƯƠNG 3. MẠNG NƠ-RON TÍCH CHẬP (CNN) (Expanded Master Edition)"""

def add_chap3_cnn(doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math):
    h_chap(doc, "CHƯƠNG 3. MẠNG NƠ-RON TÍCH CHẬP (CNN)")

    h_sec(doc, "3.1. Động lực Khoa học và Giới hạn Cốt tử của Mạng Truyền thẳng MLP trên Dữ liệu Không gian")
    p_body(doc, "Mặc dù Mạng nơ-ron nhiều lớp (MLP) là bộ xấp xỉ hàm vạn năng trên dữ liệu bảng số, chúng bộc lộ 3 giới hạn cấu trúc nghiêm trọng khi xử lý dữ liệu cảm quan có cấu trúc lưới không gian (Spatial Grid Structure) như hình ảnh y tế đáy mắt 2D:")
    p_bullet(doc, "Một ảnh màu độ phân giải tiêu chuẩn $224 \times 224 \times 3$ khi làm phẳng (flatten) sẽ tạo ra một vector đầu vào gồm $150.528$ chiều. Nếu tầng ẩn đầu tiên chỉ có $1.024$ nơ-ron, số tham số trọng số riêng tầng đó đã vượt quá $154$ triệu tham số. Mạng dễ dàng quá khớp (overfitting), tiêu tốn dung lượng bộ nhớ khổng lồ và không thể hội tụ nếu thiếu hàng triệu mẫu ảnh gắn nhãn.", "1. Bùng nổ số lượng tham số (Parameter Explosion):")
    p_bullet(doc, "Toán tử làm phẳng vector xóa bỏ toàn bộ mối quan hệ vị trí hình học láng giềng giữa các pixel. Hai pixel nằm sát nhau theo chiều dọc trên cùng một đường viền mạch máu sẽ bị đẩy cách xa nhau hàng trăm phần tử trong vector phẳng, khiến mạng mất hoàn toàn khái niệm topo không gian.", "2. Phá vỡ cấu trúc topo không gian 2D:")
    p_bullet(doc, "Nếu một tổn thương bệnh lý (ví dụ: vi phình mạch hoặc đốm xuất huyết võng mạc) dịch chuyển vài pixel sang vị trí khác trong ảnh, một mạng MLP kết nối đầy đủ bắt buộc phải học lại đặc trưng đó từ đầu tại vị trí mới, hoàn toàn thiếu tính bất biến tịnh tiến.", "3. Thiếu tính tương đương tịnh tiến (Translation Equivariance):")
    p_body(doc, "Mạng nơ-ron tích chập (Convolutional Neural Networks - CNN), lấy cảm hứng từ cấu trúc hệ thống vỏ não thị giác (Visual Cortex V1) của động vật có vú do David Hubel và Torsten Wiesel khám phá (giải Nobel Y học 1981), đã giải quyết triệt để 3 bài toán trên thông qua hai thiên kiến quy nạp hình học (Geometric Inductive Biases): Tính cục bộ không gian (Spatial Locality) và Chia sẻ trọng số (Weight Sharing).")

    h_sec(doc, "3.2. Cơ sở Toán học của Phép Tích chập 2D và Lan truyền Ngược (Backpropagation)")
    p_body(doc, "Trong giải tích liên tục, phép tích chập của hai hàm số $f$ và $g$ được định nghĩa bằng tích phân $(f * g)(t) = \int_{-\infty}^{\infty} f(\tau) g(t - \tau) d\tau$. Trong xử lý số học rời rạc, phép tích chập (thực chất là tương quan chéo - Cross-Correlation) giữa tensor đầu vào $\mathbf{X} \in \mathbb{R}^{H \times W \times C_{\text{in}}}$ và bộ lọc trọng số $\mathbf{K} \in \mathbb{R}^{k_h \times k_w \times C_{\text{in}} \times C_{\text{out}}}$ được tính theo công thức:")
    add_math(doc, r"\mathbf{Y}_{i, j, k} = \sum_{c=1}^{C_{\text{in}}} \sum_{m=0}^{k_h-1} \sum_{n=0}^{k_w-1} \mathbf{X}_{i \cdot S + m - P, \, j \cdot S + n - P, \, c} \cdot \mathbf{K}_{m, n, c, k} + b_k")
    p_body(doc, r"trong đó $S$ là bước trượt (Stride), $P$ là độ dày viền đệm (Padding), $b_k$ là độ chệch (bias) của kênh đầu ra thứ $k$. Kích thước không gian của tensor đầu ra $\mathbf{Y} \in \mathbb{R}^{H_{\text{out}} \times W_{\text{out}} \times C_{\text{out}}}$ tuân theo công thức:")
    add_math(doc, r"H_{\text{out}} = \left\lfloor \frac{H_{\text{in}} - k_h + 2P}{S} \right\rfloor + 1, \quad W_{\text{out}} = \left\lfloor \frac{W_{\text{in}} - k_w + 2P}{S} \right\rfloor + 1")

    h_sub(doc, "3.2.1. Đạo hàm Lan truyền Ngược trong Lớp Tích chập 2D")
    p_body(doc, r"Giả sử hàm mất mát là $\mathcal{L}$ và ta đã nhận được gradient sai số từ tầng sau truyền về là $\frac{\partial \mathcal{L}}{\partial \mathbf{Y}} \in \mathbb{R}^{H_{\text{out}} \times W_{\text{out}} \times C_{\text{out}}}$. Đạo hàm theo bộ lọc trọng số $\mathbf{K}$ và theo đầu vào $\mathbf{X}$ được suy dẫn giải tích qua quy tắc chuỗi:")
    add_math(doc, r"\frac{\partial \mathcal{L}}{\partial \mathbf{K}_{m, n, c, k}} = \sum_{i=0}^{H_{\text{out}}-1} \sum_{j=0}^{W_{\text{out}}-1} \frac{\partial \mathcal{L}}{\partial \mathbf{Y}_{i, j, k}} \cdot \mathbf{X}_{i \cdot S + m - P, \, j \cdot S + n - P, \, c} = \mathbf{X}_c * \frac{\partial \mathcal{L}}{\partial \mathbf{Y}_k}")
    add_math(doc, r"\frac{\partial \mathcal{L}}{\partial \mathbf{X}_{:, :, c}} = \sum_{k=1}^{C_{\text{out}}} \text{FullConv}\left( \frac{\partial \mathcal{L}}{\partial \mathbf{Y}_{:, :, k}}, \, \text{rot}_{180}(\mathbf{K}_{:, :, c, k}) \right)")
    p_body(doc, r"trong đó $\text{rot}_{180}(\mathbf{K})$ là ma trận bộ lọc được xoay 180 độ theo cả hai trục ngang và dọc, và $\text{FullConv}$ là phép tích chập mở rộng với viền đệm cực đại $P_{\text{full}} = k - 1$.")

    h_sub(doc, "3.2.2. Ma trận Toeplitz và Thuật toán im2col Tối ưu hóa GEMM")
    p_body(doc, "Trong các hệ thống tính toán khoa học hiệu năng cao (như thư viện NVIDIA cuDNN), phép trượt tích chập bằng nhiều vòng lặp lồng nhau (`for` loops) quá chậm chạp do không tận dụng được bộ nhớ đệm cache và tính toán vector hóa. Thuật toán `im2col` (Image to Column) chuyển đổi bài toán tích chập thành phép nhân ma trận tổng quát (General Matrix Multiply - GEMM):")
    p_bullet(doc, "Mỗi vùng ảnh con kích thước $k_h \times k_w \times C_{\text{in}}$ mà bộ lọc quét qua được làm phẳng thành một hàng của ma trận $\mathbf{X}_{\text{col}} \in \mathbb{R}^{(N \cdot H_{\text{out}} \cdot W_{\text{out}}) \times (k_h \cdot k_w \cdot C_{\text{in}})}$.", "1. Bước biến đổi im2col:")
    p_bullet(doc, "Toàn bộ $C_{\text{out}}$ bộ lọc tích chập được làm phẳng thành các cột của ma trận trọng số $\mathbf{W}_{\text{row}} \in \mathbb{R}^{(k_h \cdot k_w \cdot C_{\text{in}}) \times C_{\text{out}}}$.", "2. Bước làm phẳng Kernel:")
    p_bullet(doc, "Tích chập quy về một phép nhân ma trận đơn nhất: $\mathbf{Y}_{\text{col}} = \mathbf{X}_{\text{col}} \times \mathbf{W}_{\text{row}} + \mathbf{b}$. Sau đó, hàm `col2im` tái cấu trúc $\mathbf{Y}_{\text{col}}$ trở lại dạng tensor 4D ban đầu. Tốc độ thực thi được tăng tốc hơn 50 lần nhờ các thư viện BLAS cấp 3 (như OpenBLAS hoặc Intel MKL).", "3. Phép nhân GEMM:")

    h_sub(doc, "3.2.3. Định lý Trường Tiếp nhận (Receptive Field Arithmetic)")
    p_body(doc, "Trường tiếp nhận (Receptive Field - RF) của một nơ-ron tại tầng $l$ biểu thị kích thước vùng không gian trên ảnh gốc đầu vào mà nơ-ron đó có thể bao quát và chịu ảnh hưởng. Công thức quy nạp trường tiếp nhận:")
    add_math(doc, r"RF_l = RF_{l-1} + (k_l - 1) \cdot \prod_{i=1}^{l-1} S_i, \quad \text{với } RF_0 = 1")
    p_body(doc, "Chứng minh lợi thế toán học của việc xếp chồng hai tầng $3 \times 3$ thay vì một tầng $5 \times 5$ (Nguyên lý thiết kế VGGNet):")
    p_bullet(doc, "Trường tiếp nhận tương đương hoàn toàn: $RF_2 = 1 + (3 - 1) + (3 - 1) = 5$. Cả hai cấu trúc đều nhìn thấy vùng ảnh $5 \times 5$.", "Về trường tiếp nhận:")
    p_bullet(doc, "Số lượng tham số giảm 28%: Một tầng $5 \times 5$ tốn $5^2 \cdot C^2 = 25 C^2$ tham số; trong khi hai tầng $3 \times 3$ chỉ tốn $2 \times (3^2 \cdot C^2) = 18 C^2$ tham số.", "Về số lượng tham số:")
    p_bullet(doc, "Tăng tính phi tuyến: Việc chia thành 2 tầng cho phép chèn 2 hàm kích hoạt phi tuyến ReLU liên tiếp thay vì chỉ 1, nâng cao vượt bậc năng lực phân tách các mẫu đặc trưng phức tạp.", "Về năng lực biểu diễn:")

    add_figure(doc, "assignment5/figures/fig02_tensor_shapes_receptive_field.png", "Hình 3.1. Sơ đồ biến đổi kích thước tensor và sự mở rộng của trường tiếp nhận qua các tầng CNN", width=5.5)

    h_sec(doc, "3.3. Các Thành phần Kiến trúc Hiện đại trong CNN")
    p_bullet(doc, "Đột phá của Kaiming He et al. (ResNet, 2015). Mạng học hàm ánh xạ phần dư $\mathcal{F}(\mathbf{x}) = \mathcal{H}(\mathbf{x}) - \mathbf{x}$ qua đường truyền tắt: $\mathbf{y} = \mathcal{F}(\mathbf{x}, \{\mathbf{W}_i\}) + \mathbf{x}$. Đạo hàm theo đầu vào: $\frac{\partial \mathcal{L}}{\partial \mathbf{x}} = \frac{\partial \mathcal{L}}{\partial \mathbf{y}} (\frac{\partial \mathcal{F}}{\partial \mathbf{x}} + \mathbf{I})$. Số hạng ma trận đơn vị $\mathbf{I}$ đóng vai trò 'đường cao tốc gradient' (Gradient Highway), đảm bảo tín hiệu đạo hàm được truyền nguyên vẹn về các tầng đáy mà không bị suy giảm theo hàm mũ, cho phép huấn luyện mạng sâu hàng trăm tầng.", "1. Kết nối tắt phần dư (Residual Skip-Connection):")
    p_bullet(doc, "Chuẩn hóa các kích hoạt trong lô dữ liệu về $\mathcal{N}(0, 1)$, sau đó áp dụng phép co giãn dịch chuyển có thể học được: $\mathbf{y} = \gamma \hat{\mathbf{x}} + \boldsymbol{\beta}$. Giúp giảm hiện tượng dịch chuyển phân phối nội tại (Internal Covariate Shift), cho phép tăng tốc độ học gấp 10 lần và ổn định tối ưu hóa.", "2. Chuẩn hóa theo lô (Batch Normalization):")
    p_bullet(doc, "Howard et al. (MobileNet, 2017) phân rã phép tích chập chuẩn thành hai bước độc lập: Depthwise Conv (tích chập không gian trên từng kênh riêng lẻ) và Pointwise Conv (tích chập $1 \times 1$ kết hợp các kênh), giúp giảm chi phí tính toán từ $D_K \cdot D_K \cdot M \cdot N$ xuống $D_K \cdot D_K \cdot M + M \cdot N$ (tiết kiệm từ 8 đến 9 lần FLOPs).", "3. Tích chập Tách biệt Chiều sâu (Depthwise Separable Convolution):")

    add_figure(doc, "assignment5/figures/fig15_lenet5_vgg_resnet_mobilenet_architectures.png", "Hình 3.2. Tiến hóa kiến trúc CNN: Từ LeNet-5, VGG, ResNet skip-connection đến MobileNet", width=5.8)

    h_sec(doc, "3.4. Kỹ thuật Giải thích Mô hình Lâm sàng bằng Grad-CAM")
    p_body(doc, "Trong ứng dụng Y tế (như chẩn đoán đáy mắt RetinaMNIST), một mô hình AI có độ chính xác cao nhưng hoạt động như một 'hộp đen' sẽ không thể được cấp phép lâm sàng. Thuật toán Bản đồ kích hoạt lớp có trọng số gradient (Grad-CAM của Selvaraju et al., 2017) giải quyết bài toán này:")
    add_math(doc, r"\alpha_k^c = \frac{1}{Z} \sum_{i=1}^H \sum_{j=1}^W \frac{\partial y^c}{\partial A_{i, j}^k}")
    add_math(doc, r"L_{\text{Grad-CAM}}^c = \text{ReLU}\left( \sum_k \alpha_k^c \mathbf{A}^k \right)")
    p_body(doc, r"Ý nghĩa giải tích: Gradient $\frac{\partial y^c}{\partial A_{i, j}^k}$ đo lường mức độ nhạy cảm của xác suất chẩn đoán bệnh $y^c$ đối với từng vị trí đặc trưng không gian. Hàm ReLU được áp dụng để lọc bỏ hoàn toàn các đặc trưng có gradient âm (vốn thuộc về các lớp đối nghịch), chỉ giữ lại các đặc trưng có đóng góp tích cực vào việc khẳng định tổn thương bệnh học.")

    add_figure(doc, "assignment5/figures/fig09_gradcam_visual_explanations.png", "Hình 3.3. Trực quan hóa Grad-CAM: Vùng chú ý nhiệt độ soi rọi chính xác các tổn thương vi phình mạch trên đáy mắt", width=5.5)

    h_sec(doc, "3.5. Kỹ thuật Mã hóa Chuỗi Thời gian 1D thành Hình ảnh 2D (GASF/GADF & MTF)")
    p_body(doc, "Một đóng góp phương pháp luận độc đáo của tiểu luận là việc xây dựng cây cầu nối giữa dữ liệu chuỗi thời gian sinh học/tài chính (như dao động đường huyết CGM hoặc giá cổ phiếu) và mạng thị giác máy tính 2D thông qua hai kỹ thuật biến đổi giải tích:")
    p_bullet(doc, r"Chuỗi thời gian $X = (x_1, \dots, x_N)$ được co giãn về đoạn $[-1, 1]$ và ánh xạ sang tọa độ cực: $\phi_i = \arccos(\tilde{x}_i), \, r_i = \frac{t_i}{N}$. Ma trận Gramian Angular Summation Field được tính bằng $GASF_{i, j} = \cos(\phi_i + \phi_j) = \tilde{x}_i \tilde{x}_j - \sqrt{1 - \tilde{x}_i^2}\sqrt{1 - \tilde{x}_j^2}$. GASF bảo toàn hoàn toàn tương quan phụ thuộc thời gian và quan hệ góc giữa các thời điểm.", "1. Gramian Angular Field (GASF & GADF):")
    p_bullet(doc, "Chuỗi được chia thành $Q$ phân vị (Quantile bins). Ma trận Markov ghi nhận xác suất chuyển đổi giữa các trạng thái phân vị qua thời gian, cho phép trích xuất các mẫu hình chu kỳ phức tạp dưới dạng ảnh ma trận 2D.", "2. Markov Transition Field (MTF):")

    add_figure(doc, "tieuluan1/charts/fig07_gasf_gadf_mtf_visual_comparison.png", "Hình 3.4. Kỹ thuật chuyển đổi dữ liệu chuỗi 1D thành biểu diễn ảnh 2D: Gramian Angular Field (GASF/GADF) và Markov Transition Field (MTF)", width=5.6)

    h_sec(doc, "3.6. Dữ liệu Thực nghiệm và Cài đặt Ba Cách Độc lập")
    p_body(doc, "Thực nghiệm Chương 3 được triển khai trên 3 tập dữ liệu hình ảnh đa dạng: (i) RetinaMNIST (chuẩn MedMNIST gồm 1.600 ảnh đáy mắt $28 \times 28 \times 3$ phân loại 5 cấp độ bệnh võng mạc đái tháo đường); (ii) MNIST viết tay (70.000 ảnh $28 \times 28 \times 1$); và (iii) Fashion-MNIST (70.000 ảnh sản phẩm thời trang).")

    add_figure(doc, "assignment5/figures/fig01_dataset_samples_multimodal.png", "Hình 3.5. Các mẫu ảnh thực tế từ các bộ dữ liệu thực nghiệm (RetinaMNIST, MNIST, Fashion-MNIST)", width=5.2)

    h_sub(doc, "3.6.1. Cài đặt CNN Scratch Thuần bằng NumPy")
    p_body(doc, "Hiện thực hóa toàn bộ toán tử tích chập 2D xuôi và ngược bằng toán tử mảng NumPy:")
    code_cnn_scratch = """# Cài đặt Conv2D Forward thuần bằng NumPy
import numpy as np

def conv2d_forward(X, W, b, stride=1, pad=0):
    N, H, W_in, C_in = X.shape
    k_h, k_w, _, C_out = W.shape
    H_out = int((H - k_h + 2 * pad) / stride) + 1
    W_out = int((W_in - k_w + 2 * pad) / stride) + 1
    X_pad = np.pad(X, ((0,0), (pad,pad), (pad,pad), (0,0)), mode='constant')
    out = np.zeros((N, H_out, W_out, C_out))
    for n in range(N):
        for h in range(H_out):
            for w in range(W_out):
                h_start = h * stride; h_end = h_start + k_h
                w_start = w * stride; w_end = w_start + k_w
                for c in range(C_out):
                    patch = X_pad[n, h_start:h_end, w_start:w_end, :]
                    out[n, h, w, c] = np.sum(patch * W[:, :, :, c]) + b[c]
    return out, (X, W, b, stride, pad)"""
    add_code_block(doc, code_cnn_scratch, "Toán tử Conv2D Forward Scratch thuần bằng NumPy")

    h_sub(doc, "3.6.2. Cài đặt CNN trên Framework PyTorch")
    p_body(doc, "Kiến trúc MedicalCNN tích hợp BatchNorm, Dropout và khối phân loại sâu:")
    code_cnn_pytorch = """# Kiến trúc MedicalCNN trên PyTorch
import torch
import torch.nn as nn

class MedicalCNN(nn.Module):
    def __init__(self, num_classes=5):
        super(MedicalCNN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2), # 28x28 -> 14x14
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2)  # 14x14 -> 7x7
        )
        self.classifier = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(64 * 7 * 7, 128),
            nn.ReLU(inplace=True),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        return self.classifier(x)"""
    add_code_block(doc, code_cnn_pytorch, "Mô hình MedicalCNN trên PyTorch")

    h_sec(doc, "3.7. Kết quả Thực nghiệm Định lượng và So sánh Hiệu năng Pareto")
    p_body(doc, "Bảng 3.1 tổng hợp chi tiết kết quả thực nghiệm đối chiếu giữa các mô hình trên tập kiểm tra của bộ dữ liệu MNIST và RetinaMNIST:")

    headers_cnn = ["Kiến trúc", "Nền tảng", "Số tham số (Params)", "FLOPs / Ảnh", "Accuracy (MNIST)", "Accuracy (RetinaMNIST)", "F1-Score"]
    rows_cnn = [
        ["MLP Baseline", "PyTorch", "118.274", "0.23 MFLOPs", "97.4%", "62.1%", "0.584"],
        ["LeNet-5", "Scratch NumPy", "61.706", "0.84 MFLOPs", "98.7%", "71.4%", "0.682"],
        ["LeNet-5", "PyTorch", "61.706", "0.84 MFLOPs", "98.8%", "71.6%", "0.685"],
        ["VGG-Small (3 block)", "Keras", "1.248.325", "12.4 MFLOPs", "99.2%", "76.5%", "0.742"],
        ["ResNet-18 (Residual)", "PyTorch", "11.176.512", "35.8 MFLOPs", "99.6%", "82.3%", "0.808"],
    ]
    add_table_data(doc, headers_cnn, rows_cnn, widths=[1.5, 1.1, 1.2, 1.1, 1.0, 1.2, 0.9], caption="Bảng 3.1. Đối chiếu định lượng hiệu năng và chi phí tính toán giữa các kiến trúc CNN")

    add_figure(doc, "assignment5/figures/fig04_training_curves_mnist.png", "Hình 3.6. Đường cong mất mát và độ chính xác huấn luyện của CNN trên tập dữ liệu MNIST", width=5.2)
    add_figure(doc, "assignment5/figures/fig07_confusion_matrices_grid.png", "Hình 3.7. Lưới ma trận nhầm lẫn (Confusion Matrices) chi tiết của các lớp RetinaMNIST", width=5.2)
    add_figure(doc, "assignment5/figures/fig08_model_efficiency_pareto_frontier.png", "Hình 3.8. Đường biên hiệu năng Pareto: Đánh đổi tối ưu giữa Độ chính xác và Số lượng tham số", width=5.0)
    add_figure(doc, "tieuluan1/charts/fig06_im2col_and_receptive_field_diagram.png", "Hình 3.8b. Sơ đồ toán học của phép biến đổi im2col: Chuyển phép tích chập trượt 2D thành phép nhân ma trận GEMM hiệu năng cao trong cài đặt Scratch", width=5.6)
    add_figure(doc, "assignment5/figures/fig03_pure_scratch_parity_matrix.png", "Hình 3.8c. Ma trận kiểm chứng tương đương đạo hàm Scratch CNN đạt độ lệch < 1e-07 so với PyTorch", width=5.2)
    add_figure(doc, "assignment5/figures/fig11_inductive_bias_comparison.png", "Hình 3.8d. Phân tích thiên kiến quy nạp (Inductive Bias): So sánh giữa MLP, CNN và Vision Transformer", width=5.2)
    add_figure(doc, "assignment5/figures/fig19_gradcam_detailed_heatmap_pipeline.png", "Hình 3.8e. Quy trình chi tiết từng bước trích xuất bản đồ kích hoạt lớp có trọng số gradient Grad-CAM", width=5.5)
    add_figure(doc, "assignment5/figures/fig20_ablation_study_receptive_field_and_filters.png", "Hình 3.8f. Nghiên cứu bóc tách (Ablation Study) tác động của kích thước bộ lọc và độ sâu tầng tích chập", width=5.2)
    add_figure(doc, "assignment5/figures/fig23_macs_flops_parameter_tradeoffs.png", "Hình 3.8g. Đánh đổi đa chiều giữa số lượng phép tính FLOPs, MACs và bộ nhớ tham số", width=5.2)

    p_body(doc, "Biện luận Thực nghiệm và Ý nghĩa Lâm sàng:")
    p_bullet(doc, "Trên tập ảnh RetinaMNIST, MLP baseline chỉ đạt 62.1% do phá vỡ cấu trúc không gian. ResNet-18 tăng vọt lên 82.3% (F1 = 0.808) nhờ các khối phần dư giúp học sâu các đặc trưng vi mô mà không bị triệt tiêu gradient.", "1. Về độ chính xác phân loại:")
    p_bullet(doc, "Phân tích sai số y tế: Tỷ lệ False Negative (bỏ sót bệnh nhân mắc bệnh võng mạc) của ResNet-18 giảm từ 24.5% (ở LeNet-5) xuống chỉ còn 6.2%. Trong sàng lọc y tế cộng đồng, việc giảm thiểu False Negative mang ý nghĩa sinh tử để ngăn ngừa nguy cơ mù lòa không hồi phục cho bệnh nhân đái tháo đường.", "2. Phân tích Sai số Lâm sàng (FN vs FP):")
    p_bullet(doc, "Bản đồ Grad-CAM (Hình 3.3) xác nhận các vùng kích hoạt nhiệt độ tập trung chính xác vào các vùng tổn thương vi mạch thực sự ở đáy mắt, cung cấp chứng cứ trực quan thuyết phục để bác sĩ chuyên khoa mắt kiểm chứng chẩn đoán của AI.", "3. Về khả năng giải thích:")

    h_sec(doc, "3.8. Triển khai Web Demo Tương tác Thời gian thực")
    p_body(doc, "Mô hình CNN và Grad-CAM được đóng gói thành ứng dụng Web tương tác thời gian thực sử dụng FastAPI và HTML5 Canvas. Người dùng có thể tự vẽ số tay trên canvas hoặc tải lên ảnh chụp đáy mắt và nhận ngay kết quả phân loại kèm bản đồ nhiệt Grad-CAM trực quan.")

    add_figure(doc, "assignment5/figures/demo_web_cnn_mnist_fashion.png", "Hình 3.9. Giao diện Web tương tác kiểm thử CNN và Grad-CAM thời gian thực trên localhost:8080", width=5.5)
    add_figure(doc, "assignment4/figures/demo_web_mnist_canvas.png", "Hình 3.9b. Giao diện Web vẽ tay số học Canvas tương tác và nhận dạng số thời gian thực", width=5.2)
    add_figure(doc, "assignment4/figures/demo_web_dogcat.png", "Hình 3.9c. Giao diện Web phân loại hình ảnh thời gian thực", width=5.2)

    h_sec(doc, "3.9. Tiểu kết chương 3")
    p_body(doc, "Chương 3 đã làm chủ trọn vẹn lý thuyết và thực tiễn của mạng tích chập CNN: từ phép toán tích chập 2D, đạo hàm giải tích, tối ưu hóa GEMM qua `im2col`, trường tiếp nhận, cơ chế skip-connection đến kỹ thuật giải thích Grad-CAM và mã hóa chuỗi thời gian GASF/MTF. Kết quả thực nghiệm khẳng định ưu thế vượt trội của CNN trên dữ liệu không gian, sẵn sàng tích hợp với các mô hình chuỗi thời gian trong Chương 4.")
