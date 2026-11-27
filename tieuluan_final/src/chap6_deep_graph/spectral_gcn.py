# -*- coding: utf-8 -*-
"""
CHƯƠNG 6: TẦNG TÍCH CHẬP ĐỒ THỊ PHỔ KIPF & WELLING (SPECTRAL GCN) TRÊN PYTORCH & NUMPY
Sinh viên thực hiện: Trần Văn Hậu | MSV: B23DCCN287 | Lớp: D23CTPM01 | Nhóm CT_09
Giảng viên hướng dẫn: PGS. TS. Trần Đình Quế

Hiện thực hóa toàn bộ:
  1. Biến đổi chuẩn hóa renormalization trick: A_tilde = A + I_N
  2. Ma trận bậc chuẩn hóa đối xứng: D_tilde^{-1/2} A_tilde D_tilde^{-1/2}
  3. Lan truyền tiến: H^{(l+1)} = sigma( D_tilde^{-1/2} A_tilde D_tilde^{-1/2} H^{(l)} W^{(l)} )
  4. Mô hình 2-layer Spectral GCN cho phân loại đỉnh bán giám sát (Semi-Supervised Node Classification)
"""

import sys
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

sys.stdout.reconfigure(encoding='utf-8')


def compute_normalized_laplacian(adj_matrix: np.ndarray) -> np.ndarray:
    """
    Tính ma trận chuyển tiếp chuẩn hóa đối xứng theo mẹo tái chuẩn hóa Kipf & Welling (ICLR 2017):
    A_hat = D_tilde^{-1/2} * (A + I) * D_tilde^{-1/2}
    """
    N = adj_matrix.shape[0]
    # Thêm khuyên tự thân (Self-loops)
    adj_tilde = adj_matrix + np.eye(N)
    
    # Ma trận bậc (Degree Matrix)
    degrees = np.sum(adj_tilde, axis=1)
    d_inv_sqrt = np.power(degrees, -0.5)
    d_inv_sqrt[np.isinf(d_inv_sqrt)] = 0.0
    d_mat = np.diag(d_inv_sqrt)
    
    # Tích ma trận đối xứng: D^{-1/2} * A * D^{-1/2}
    norm_adj = d_mat @ adj_tilde @ d_mat
    return norm_adj


class GCNLayer(nn.Module):
    """Một tầng tích chập đồ thị phổ GCN."""
    def __init__(self, in_features: int, out_features: int, bias: bool = True):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.weight = nn.Parameter(torch.FloatTensor(in_features, out_features))
        if bias:
            self.bias = nn.Parameter(torch.FloatTensor(out_features))
        else:
            self.register_parameter('bias', None)
        self.reset_parameters()

    def reset_parameters(self):
        # Khởi tạo Glorot / Xavier Uniform
        nn.init.xavier_uniform_(self.weight)
        if self.bias is not None:
            nn.init.zeros_(self.bias)

    def forward(self, x: torch.Tensor, norm_adj: torch.Tensor) -> torch.Tensor:
        # x: (N, in_features)
        # norm_adj: (N, N)
        # support = X * W
        support = torch.mm(x, self.weight)
        # output = A_hat * support
        output = torch.mm(norm_adj, support)
        if self.bias is not None:
            output = output + self.bias
        return output


class SpectralGCN(nn.Module):
    """Mô hình 2 tầng GCN chuẩn hóa cho phân loại đỉnh trên đồ thị."""
    def __init__(self, in_features: int, hidden_dim: int, num_classes: int, dropout: float = 0.5):
        super().__init__()
        self.gc1 = GCNLayer(in_features, hidden_dim)
        self.gc2 = GCNLayer(hidden_dim, num_classes)
        self.dropout = dropout

    def forward(self, x: torch.Tensor, norm_adj: torch.Tensor) -> torch.Tensor:
        h1 = F.relu(self.gc1(x, norm_adj))
        h1 = F.dropout(h1, p=self.dropout, training=self.training)
        out = self.gc2(h1, norm_adj)
        return out


def test_spectral_gcn():
    print("=" * 70)
    print("KIỂM TRA KIẾN TRÚC SPECTRAL GCN (KIPF & WELLING ICLR 2017)")
    print("Tác giả: Trần Văn Hậu - B23DCCN287 | Nhóm CT_09")
    print("=" * 70)

    # Đồ thị vòng tròn 6 đỉnh làm mẫu
    adj = np.array([
        [0, 1, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0, 1],
        [1, 0, 0, 0, 1, 0]
    ], dtype=np.float32)

    norm_adj = compute_normalized_laplacian(adj)
    print("Ma trận kề đã chuẩn hóa đối xứng (Normalized Adj Matrix):")
    print(np.round(norm_adj, 3))

    x = torch.randn(6, 16)  # 6 đỉnh, mỗi đỉnh 16 đặc trưng
    norm_adj_t = torch.tensor(norm_adj, dtype=torch.float32)

    model = SpectralGCN(in_features=16, hidden_dim=8, num_classes=3, dropout=0.0)
    logits = model(x, norm_adj_t)

    print(f"\nKích thước đầu ra: {list(logits.shape)} (Số đỉnh: {logits.shape[0]}, Số lớp: {logits.shape[1]})")
    assert logits.shape == (6, 3)
    print("Spectral GCN verification PASSED!")
    print("=" * 70)


if __name__ == "__main__":
    test_spectral_gcn()
