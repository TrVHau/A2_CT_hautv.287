# -*- coding: utf-8 -*-
"""
CHƯƠNG 6: MẠNG CHÚ Ý ĐỒ THỊ GRAPH ATTENTION NETWORK (GAT - VELICKOVIC ET AL. ICLR 2018)
Sinh viên thực hiện: Trần Văn Hậu | MSV: B23DCCN287 | Lớp: D23CTPM01 | Nhóm CT_09
Giảng viên hướng dẫn: PGS. TS. Trần Đình Quế

Hiện thực hóa toàn bộ:
  1. Cơ chế tự chú ý dị hướng (Anisotropic Attention): e_{ij} = LeakyReLU( a^T [Wh_i || Wh_j] )
  2. Hệ số chú ý chuẩn hóa Softmax trên tập láng giềng: alpha_{ij} = exp(e_{ij}) / sum_{k} exp(e_{ik})
  3. Cơ chế Đa đầu chú ý (Multi-Head Attention) tăng cường tính ổn định của gradient
  4. Lớp mô hình GAT cho phân loại đỉnh trên đồ thị
"""

import sys
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

sys.stdout.reconfigure(encoding='utf-8')


class GraphAttentionHead(nn.Module):
    """Một đầu tự chú ý đơn lẻ trong GAT."""
    def __init__(self, in_features: int, out_features: int, alpha: float = 0.2):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.alpha = alpha

        self.W = nn.Linear(in_features, out_features, bias=False)
        self.a = nn.Parameter(torch.empty(size=(2 * out_features, 1)))
        nn.init.xavier_uniform_(self.W.weight)
        nn.init.xavier_uniform_(self.a)

    def forward(self, h: torch.Tensor, adj: torch.Tensor) -> torch.Tensor:
        # h: (N, in_features)
        # adj: (N, N)
        N = h.shape[0]
        Wh = self.W(h)  # (N, out_features)

        # Tính toán ma trận ghép đôi (Wh_i || Wh_j) cho tất cả các cặp đỉnh
        Wh_repeat1 = Wh.repeat_interleave(N, dim=0)  # (N*N, out_features)
        Wh_repeat2 = Wh.repeat(N, 1)                 # (N*N, out_features)
        all_pairs = torch.cat([Wh_repeat1, Wh_repeat2], dim=1)  # (N*N, 2*out_features)

        e = torch.matmul(all_pairs, self.a).view(N, N)
        e = F.leaky_relu(e, negative_slope=self.alpha)

        # Mặt nạ hóa các cạnh không tồn tại (chỉ giữ lại cạnh thực sự và khuyên tự thân)
        adj_with_loops = adj + torch.eye(N, device=adj.device)
        mask = (adj_with_loops == 0)
        e = e.masked_fill(mask, -1e9)

        # Chuẩn hóa Softmax theo từng hàng
        alpha_weights = F.softmax(e, dim=1)

        # Tổng hợp biểu diễn có trọng số: H' = alpha * Wh
        h_prime = torch.matmul(alpha_weights, Wh)
        return h_prime, alpha_weights


class MultiHeadGATLayer(nn.Module):
    """Tầng GAT đa đầu chú ý (Multi-Head GAT Layer)."""
    def __init__(self, in_features: int, out_features: int, num_heads: int = 4, concat: bool = True):
        super().__init__()
        self.num_heads = num_heads
        self.concat = concat
        self.heads = nn.ModuleList([
            GraphAttentionHead(in_features, out_features) for _ in range(num_heads)
        ])

    def forward(self, h: torch.Tensor, adj: torch.Tensor):
        head_outputs = []
        attn_list = []
        for head in self.heads:
            out, attn = head(h, adj)
            head_outputs.append(out)
            attn_list.append(attn)

        if self.concat:
            # Ghép nối các đầu: (N, num_heads * out_features)
            return torch.cat(head_outputs, dim=1), attn_list
        else:
            # Trung bình cộng các đầu (thường dùng ở tầng cuối)
            return torch.mean(torch.stack(head_outputs), dim=0), attn_list


def test_gat():
    print("=" * 70)
    print("KIỂM TRA KIẾN TRÚC GRAPH ATTENTION NETWORK (GAT - PYTORCH)")
    print("Tác giả: Trần Văn Hậu - B23DCCN287 | Nhóm CT_09")
    print("=" * 70)

    # Đồ thị 4 đỉnh
    adj = torch.tensor([
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 0]
    ], dtype=torch.float32)

    x = torch.randn(4, 16)  # 4 đỉnh, 16 đặc trưng

    # Multi-head GAT với 3 đầu, mỗi đầu sinh 8 chiều -> tổng 24 chiều
    gat = MultiHeadGATLayer(in_features=16, out_features=8, num_heads=3, concat=True)
    out, attn = gat(x, adj)

    print(f"Input features: {list(x.shape)} -> Multi-Head GAT Output: {list(out.shape)}")
    print(f"Số lượng đầu chú ý (Attention Heads): {len(attn)}")
    print(f"Trọng số chú ý đầu 1 (Head 1 Attention):\n{attn[0].detach().numpy().round(3)}")

    assert out.shape == (4, 24)
    print("GAT Multi-Head Attention verification PASSED!")
    print("=" * 70)


if __name__ == "__main__":
    test_gat()
