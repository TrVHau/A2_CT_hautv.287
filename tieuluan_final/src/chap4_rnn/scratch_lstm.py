# -*- coding: utf-8 -*-
"""
CHƯƠNG 4: TẾ BÀO BỘ NHỚ DÀI-NGẮN (LSTM) CÀI ĐẶT THUẦN TỪ ĐẦU BẰNG NUMPY
Sinh viên thực hiện: Trần Văn Hậu | MSV: B23DCCN287 | Lớp: D23CTPM01 | Nhóm CT_09
Giảng viên hướng dẫn: PGS. TS. Trần Đình Quế

Hiện thực hóa toàn bộ:
  1. Forward pass: Forget Gate (f_t), Input Gate (i_t), Candidate State (c_tilde_t), Cell State (c_t), Output Gate (o_t), Hidden State (h_t)
  2. Cơ chế băng chuyền lỗi bất biến CEC (Constant Error Carousel)
  3. BPTT (Backpropagation Through Time) giải tích đạo hàm ma trận
"""

import sys
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')


def sigmoid(z):
    z_c = np.clip(z, -30.0, 30.0)
    return 1.0 / (1.0 + np.exp(-z_c))


def sigmoid_derivative(a):
    return a * (1.0 - a)


def tanh_derivative(a):
    return 1.0 - a ** 2


class ScratchLSTMCell:
    """Một ô nhớ LSTM độc lập viết hoàn toàn bằng NumPy."""
    def __init__(self, input_dim: int, hidden_dim: int, seed: int = 42):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        np.random.seed(seed)

        # Trọng số ghép nối [input_dim + hidden_dim -> 4 * hidden_dim]
        concat_dim = input_dim + hidden_dim
        std = np.sqrt(2.0 / concat_dim)

        # Ghép chung 4 cổng [f, i, c, o] để tính toán ma trận một lần
        self.W = np.random.randn(concat_dim, 4 * hidden_dim) * std
        self.b = np.zeros((1, 4 * hidden_dim))
        
        # Khởi tạo Forget Gate bias = 1.0 (Jozefowicz et al. 2015) để duy trì trí nhớ dài hạn
        self.b[0, :hidden_dim] = 1.0

        # Lưu trữ trạng thái phục vụ BPTT
        self.cache = {}

    def forward(self, x_t: np.ndarray, h_prev: np.ndarray, c_prev: np.ndarray):
        """
        Lan truyền tiến cho một bước thời gian t:
        x_t: (B, input_dim)
        h_prev: (B, hidden_dim)
        c_prev: (B, hidden_dim)
        """
        B = x_t.shape[0]
        H = self.hidden_dim
        
        concat = np.hstack([x_t, h_prev])  # (B, input_dim + hidden_dim)
        gates = np.dot(concat, self.W) + self.b  # (B, 4 * H)

        # Tách 4 cổng
        f_gate = sigmoid(gates[:, 0:H])
        i_gate = sigmoid(gates[:, H:2*H])
        c_tilde = np.tanh(gates[:, 2*H:3*H])
        o_gate = sigmoid(gates[:, 3*H:4*H])

        # Cập nhật trạng thái tế bào (CEC)
        c_t = f_gate * c_prev + i_gate * c_tilde
        tanh_c_t = np.tanh(c_t)
        h_t = o_gate * tanh_c_t

        cache = {
            'x_t': x_t, 'h_prev': h_prev, 'c_prev': c_prev, 'concat': concat,
            'f': f_gate, 'i': i_gate, 'c_tilde': c_tilde, 'o': o_gate,
            'c_t': c_t, 'tanh_c_t': tanh_c_t, 'h_t': h_t
        }
        return h_t, c_t, cache

    def backward(self, dh_t: np.ndarray, dc_next: np.ndarray, cache: dict):
        """Lan truyền ngược BPTT tính toán gradient cho một bước thời gian."""
        H = self.hidden_dim
        concat = cache['concat']
        f = cache['f']
        i = cache['i']
        c_tilde = cache['c_tilde']
        o = cache['o']
        c_prev = cache['c_prev']
        tanh_c_t = cache['tanh_c_t']

        # Đạo hàm tích hợp từ h_t và c_{t+1}
        dc_t = dc_next + (dh_t * o * tanh_derivative(tanh_c_t))

        # Đạo hàm các cổng
        do = dh_t * tanh_c_t * sigmoid_derivative(o)
        dc_tilde = dc_t * i * tanh_derivative(c_tilde)
        di = dc_t * c_tilde * sigmoid_derivative(i)
        df = dc_t * c_prev * sigmoid_derivative(f)

        # Ghép gradient các cổng
        dgates = np.hstack([df, di, dc_tilde, do])  # (B, 4 * H)

        # Gradient trọng số và chệch
        dW = np.dot(concat.T, dgates)
        db = np.sum(dgates, axis=0, keepdims=True)

        # Gradient ngược cho x_t và h_{prev}
        dconcat = np.dot(dgates, self.W.T)
        dx_t = dconcat[:, :self.input_dim]
        dh_prev = dconcat[:, self.input_dim:]
        dc_prev = dc_t * f  # Gradient truyền qua CEC theo hệ số f_t

        return dx_t, dh_prev, dc_prev, dW, db


def test_scratch_lstm():
    print("=" * 70)
    print("KIỂM TRA HOẠT ĐỘNG TẾ BÀO LSTM SCRATCH THUẦN NUMPY")
    print("Tác giả: Trần Văn Hậu - B23DCCN287 | Nhóm CT_09")
    print("=" * 70)

    cell = ScratchLSTMCell(input_dim=4, hidden_dim=8)
    B = 2
    x_t = np.random.randn(B, 4)
    h_prev = np.zeros((B, 8))
    c_prev = np.zeros((B, 8))

    h_t, c_t, cache = cell.forward(x_t, h_prev, c_prev)
    print(f"Forward output h_t shape: {h_t.shape} | c_t shape: {c_t.shape}")
    assert h_t.shape == (B, 8) and c_t.shape == (B, 8)

    # Thử nghiệm BPTT
    dh_t = np.random.randn(B, 8)
    dc_next = np.zeros((B, 8))
    dx_t, dh_prev, dc_prev, dW, db = cell.backward(dh_t, dc_next, cache)

    print(f"Backward dW shape: {dW.shape} | db shape: {db.shape} | dx_t shape: {dx_t.shape}")
    assert dW.shape == (12, 32)
    print("LSTM Scratch verification PASSED!")
    print("=" * 70)


if __name__ == "__main__":
    test_scratch_lstm()
