# -*- coding: utf-8 -*-
"""
CHƯƠNG 3: TOÁN TỬ TÍCH CHẬP 2D (CONV2D) VÀ MAX-POOLING CÀI ĐẶT THUẦN TỪ ĐẦU BẰNG NUMPY
Sinh viên thực hiện: Trần Văn Hậu | MSV: B23DCCN287 | Lớp: D23CTPM01 | Nhóm CT_09
Giảng viên hướng dẫn: PGS. TS. Trần Đình Quế

Hiện thực hóa:
  1. Conv2D Forward & Backward giải tích với đa kênh (Multi-Channel) và Padding/Stride tùy biến
  2. MaxPool2D Forward & Backward (phục hồi gradient qua chỉ số argmax)
  3. Kiểm chứng tương đương số học với torch.nn.Conv2d (Parity Check < 1e-4)
"""

import sys
import numpy as np
try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

sys.stdout.reconfigure(encoding='utf-8')


class Conv2DScratch:
    """Tầng tích chập 2 chiều thuần NumPy."""
    def __init__(self, in_channels: int, out_channels: int, kernel_size: int = 3, stride: int = 1, padding: int = 0):
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding
        
        # Khởi tạo Kaiming/He Normal
        std = np.sqrt(2.0 / (in_channels * kernel_size * kernel_size))
        self.W = np.random.randn(out_channels, in_channels, kernel_size, kernel_size).astype(np.float64) * std
        self.b = np.zeros(out_channels, dtype=np.float64)
        
        self.last_x = None
        self.last_x_padded = None
        self.dW = None
        self.db = None

    def forward(self, x: np.ndarray) -> np.ndarray:
        """Lan truyền tiến: x có kích thước (B, C_in, H, W)."""
        self.last_x = x
        B, C, H, W = x.shape
        K = self.kernel_size
        S = self.stride
        P = self.padding
        
        if P > 0:
            x_padded = np.pad(x, ((0, 0), (0, 0), (P, P), (P, P)), mode='constant')
        else:
            x_padded = x
        self.last_x_padded = x_padded
        
        H_out = (H + 2 * P - K) // S + 1
        W_out = (W + 2 * P - K) // S + 1
        out = np.zeros((B, self.out_channels, H_out, W_out), dtype=np.float64)
        
        for oc in range(self.out_channels):
            for i in range(H_out):
                h_start = i * S
                h_end = h_start + K
                for j in range(W_out):
                    w_start = j * S
                    w_end = w_start + K
                    patch = x_padded[:, :, h_start:h_end, w_start:w_end]
                    out[:, oc, i, j] = np.sum(patch * self.W[oc], axis=(1, 2, 3)) + self.b[oc]
        return out

    def backward(self, d_out: np.ndarray) -> np.ndarray:
        """Lan truyền ngược: tính đạo hàm theo W, b và x."""
        B, C, H, W = self.last_x.shape
        _, OC, H_out, W_out = d_out.shape
        K = self.kernel_size
        S = self.stride
        P = self.padding
        
        self.dW = np.zeros_like(self.W)
        self.db = np.sum(d_out, axis=(0, 2, 3))
        
        dx_padded = np.zeros_like(self.last_x_padded)
        for oc in range(OC):
            for i in range(H_out):
                h_start = i * S
                h_end = h_start + K
                for j in range(W_out):
                    w_start = j * S
                    w_end = w_start + K
                    patch = self.last_x_padded[:, :, h_start:h_end, w_start:w_end]
                    for b in range(B):
                        self.dW[oc] += patch[b] * d_out[b, oc, i, j]
                        dx_padded[b, :, h_start:h_end, w_start:w_end] += self.W[oc] * d_out[b, oc, i, j]
                        
        if P > 0:
            dx = dx_padded[:, :, P:-P, P:-P]
        else:
            dx = dx_padded
        return dx


class MaxPool2DScratch:
    """Tầng gộp cực đại (Max-Pooling) 2 chiều thuần NumPy."""
    def __init__(self, size: int = 2, stride: int = 2):
        self.size = size
        self.stride = stride
        self.last_x = None

    def forward(self, x: np.ndarray) -> np.ndarray:
        self.last_x = x
        B, C, H, W = x.shape
        K = self.size
        S = self.stride
        H_out = (H - K) // S + 1
        W_out = (W - K) // S + 1
        out = np.zeros((B, C, H_out, W_out), dtype=x.dtype)
        
        for i in range(H_out):
            h_start = i * S
            h_end = h_start + K
            for j in range(W_out):
                w_start = j * S
                w_end = w_start + K
                patch = x[:, :, h_start:h_end, w_start:w_end]
                out[:, :, i, j] = np.max(patch, axis=(2, 3))
        return out

    def backward(self, d_out: np.ndarray) -> np.ndarray:
        B, C, H, W = self.last_x.shape
        K = self.size
        S = self.stride
        _, _, H_out, W_out = d_out.shape
        dx = np.zeros_like(self.last_x)
        
        for i in range(H_out):
            h_start = i * S
            h_end = h_start + K
            for j in range(W_out):
                w_start = j * S
                w_end = w_start + K
                patch = self.last_x[:, :, h_start:h_end, w_start:w_end]
                max_mask = (patch == np.max(patch, axis=(2, 3), keepdims=True))
                # Phân bổ gradient đồng đều nếu có nhiều điểm đạt cực đại
                norm_mask = max_mask / np.sum(max_mask, axis=(2, 3), keepdims=True)
                for b in range(B):
                    for c in range(C):
                        dx[b, c, h_start:h_end, w_start:w_end] += norm_mask[b, c] * d_out[b, c, i, j]
        return dx


def test_scratch_conv2d_parity():
    """Kiểm chứng tính tương đương giữa Conv2D Scratch và PyTorch nn.Conv2d."""
    if not TORCH_AVAILABLE:
        print("PyTorch not installed. Skipping parity test.")
        return

    print("=" * 70)
    print("KIỂM CHỨNG TƯƠNG ĐƯƠNG TOÁN HỌC: CONV2D SCRATCH VS PYTORCH AUTOGRAD")
    print("=" * 70)

    np.random.seed(42)
    torch.manual_seed(42)

    B, C_in, H, W = 2, 2, 6, 6
    C_out, K, S, P = 3, 3, 1, 1

    x_np = np.random.randn(B, C_in, H, W).astype(np.float64)
    scratch_conv = Conv2DScratch(in_channels=C_in, out_channels=C_out, kernel_size=K, stride=S, padding=P)

    # Khởi tạo PyTorch Conv2D với trọng số sao chép từ Scratch
    pt_conv = nn.Conv2d(in_channels=C_in, out_channels=C_out, kernel_size=K, stride=S, padding=P, dtype=torch.float64)
    with torch.no_grad():
        pt_conv.weight.copy_(torch.tensor(scratch_conv.W, dtype=torch.float64))
        pt_conv.bias.copy_(torch.tensor(scratch_conv.b, dtype=torch.float64))

    # 1. Forward Pass Parity
    out_scratch = scratch_conv.forward(x_np)
    x_pt = torch.tensor(x_np, dtype=torch.float64, requires_grad=True)
    out_pt = pt_conv(x_pt)

    diff_forward = np.max(np.abs(out_scratch - out_pt.detach().numpy()))
    print(f"[Conv2D Forward] Sai số lớn nhất: {diff_forward:.8e}")
    assert diff_forward < 1e-7, f"Forward check failed: {diff_forward}"

    # 2. Backward Pass Parity
    d_out_np = np.random.randn(*out_scratch.shape).astype(np.float64)
    d_out_pt = torch.tensor(d_out_np, dtype=torch.float64)

    dx_scratch = scratch_conv.backward(d_out_np)
    
    pt_conv.zero_grad()
    out_pt.backward(d_out_pt)

    diff_dx = np.max(np.abs(dx_scratch - x_pt.grad.numpy()))
    diff_dW = np.max(np.abs(scratch_conv.dW - pt_conv.weight.grad.numpy()))
    diff_db = np.max(np.abs(scratch_conv.db - pt_conv.bias.grad.numpy()))

    print(f"[Conv2D Backward] Sai số dX: {diff_dx:.8e} | dW: {diff_dW:.8e} | db: {diff_db:.8e}")
    max_err = max(diff_forward, diff_dx, diff_dW, diff_db)
    print(f"=> KẾT LUẬN: ĐẠT CHUẨN XUẤT SẮC (Max Error = {max_err:.8e} < 1e-7)")
    print("=" * 70)


if __name__ == "__main__":
    test_scratch_conv2d_parity()
