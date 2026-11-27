# -*- coding: utf-8 -*-
"""
CHƯƠNG 3: MÃ HÓA CHUỖI THỜI GIAN 1D THÀNH MA TRẬN HÌNH ẢNH 2D (GASF / GADF / MTF)
Sinh viên thực hiện: Trần Văn Hậu | MSV: B23DCCN287 | Lớp: D23CTPM01 | Nhóm CT_09
Giảng viên hướng dẫn: PGS. TS. Trần Đình Quế

Hiện thực hóa:
  1. Gramian Angular Summation Field (GASF)
  2. Gramian Angular Difference Field (GADF)
  3. Markov Transition Field (MTF)
Cho phép tận dụng mạng nơ-ron tích chập 2D (CNN) để khai phá chuỗi thời gian liên tục.
"""

import sys
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')


def min_max_scale(series, new_min=-1.0, new_max=1.0):
    """Chuẩn hóa chuỗi thời gian về đoạn [new_min, new_max]."""
    s_min, s_max = np.min(series), np.max(series)
    if s_max - s_min < 1e-8:
        return np.zeros_like(series)
    return (series - s_min) / (s_max - s_min) * (new_max - new_min) + new_min


def compute_gasf_gadf(series):
    """
    Tính ma trận GASF và GADF từ chuỗi 1D.
    GASF: cos(phi_i + phi_j) = x_i * x_j - sqrt(1 - x_i^2) * sqrt(1 - x_j^2)
    GADF: sin(phi_i - phi_j) = sqrt(1 - x_i^2) * x_j - x_i * sqrt(1 - x_j^2)
    """
    scaled = min_max_scale(series, -1.0, 1.0)
    # Giới hạn chặt chẽ [-1, 1] để tránh lỗi arccos
    scaled = np.clip(scaled, -1.0, 1.0)
    
    phi = np.arccos(scaled)
    # GASF = cos(phi_i + phi_j)
    gasf = np.cos(phi[:, None] + phi[None, :])
    
    # GADF = sin(phi_i - phi_j)
    gadf = np.sin(phi[:, None] - phi[None, :])
    
    return gasf, gadf


def compute_mtf(series, n_bins=8):
    """
    Tính Markov Transition Field (MTF):
    1. Phân chia chuỗi giá trị thành n_bins khoảng giá trị
    2. Ước lượng ma trận xác suất chuyển trạng thái Markov W
    3. Trải ma trận chuyển W lên trục thời gian tạo ma trận MTF
    """
    N = len(series)
    # Phân vị (Quantile binning)
    quantiles = np.linspace(0, 100, n_bins + 1)
    bin_edges = np.percentile(series, quantiles)
    bin_edges[-1] += 1e-5
    
    bins = np.digitize(series, bin_edges) - 1
    bins = np.clip(bins, 0, n_bins - 1)
    
    # Tính ma trận chuyển Markov
    W = np.zeros((n_bins, n_bins), dtype=np.float64)
    for t in range(N - 1):
        q_curr = bins[t]
        q_next = bins[t + 1]
        W[q_curr, q_next] += 1.0
        
    # Chuẩn hóa tổng hàng = 1
    row_sums = W.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1.0
    W = W / row_sums
    
    # Xây dựng ma trận MTF [N x N]
    mtf = np.zeros((N, N), dtype=np.float64)
    for i in range(N):
        for j in range(N):
            mtf[i, j] = W[bins[i], bins[j]]
            
    return mtf


def encode_timeseries_to_3channel_image(series, n_bins=8):
    """Đóng gói chuỗi 1D thành ảnh 3 kênh: Kênh 0 = GASF, Kênh 1 = GADF, Kênh 2 = MTF."""
    gasf, gadf = compute_gasf_gadf(series)
    mtf = compute_mtf(series, n_bins=n_bins)
    img_3d = np.stack([gasf, gadf, mtf], axis=0)  # Shape: (3, N, N)
    return img_3d


def test_encoding():
    print("=" * 70)
    print("KIỂM TRA MÃ HÓA CHUỖI THỜI GIAN 1D THÀNH ẢNH 2D (GASF, GADF, MTF)")
    print("Tác giả: Trần Văn Hậu - B23DCCN287 | Nhóm CT_09")
    print("=" * 70)

    # Chuỗi giả lập 64 điểm đo CGM
    np.random.seed(42)
    t = np.linspace(0, 4 * np.pi, 64)
    cgm_series = 110 + 25 * np.sin(t) + np.random.randn(64) * 3

    gasf, gadf = compute_gasf_gadf(cgm_series)
    mtf = compute_mtf(cgm_series, n_bins=8)
    img_3ch = encode_timeseries_to_3channel_image(cgm_series)

    print(f"Chuỗi đầu vào: {cgm_series.shape} điểm")
    print(f"GASF Shape: {gasf.shape} | Range: [{np.min(gasf):.2f}, {np.max(gasf):.2f}]")
    print(f"GADF Shape: {gadf.shape} | Range: [{np.min(gadf):.2f}, {np.max(gadf):.2f}]")
    print(f"MTF Shape:  {mtf.shape}  | Range: [{np.min(mtf):.2f}, {np.max(mtf):.2f}]")
    print(f"Ảnh 3 kênh tổng hợp (3, N, N): {img_3ch.shape}")
    
    assert img_3ch.shape == (3, 64, 64)
    print("1D to 2D Encoding pipeline verification PASSED!")
    print("=" * 70)


if __name__ == "__main__":
    test_encoding()
