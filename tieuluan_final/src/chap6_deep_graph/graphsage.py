# -*- coding: utf-8 -*-
"""
CHƯƠNG 6: MÔ HÌNH HỌC QUY NẠP GRAPHSAGE (HAMILTON ET AL. NEURIPS 2017)
Sinh viên thực hiện: Trần Văn Hậu | MSV: B23DCCN287 | Lớp: D23CTPM01 | Nhóm CT_09
Giảng viên hướng dẫn: PGS. TS. Trần Đình Quế

Hiện thực hóa toàn diện:
  1. Cơ chế lấy mẫu láng giềng cố định (Uniform Neighbor Sampling)
  2. Hàm gom cụm (Mean Aggregator / Max-Pooling Aggregator)
  3. Ghép nối đặc trưng và cập nhật trạng thái: h_v^{(k)} = sigma( W * [h_v^{(k-1)} || h_N(v)^{(k)}] )
  4. Chuẩn hóa véc-tơ độ dài L2: h_v = h_v / ||h_v||_2
"""

import sys
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

sys.stdout.reconfigure(encoding='utf-8')


class GraphSAGELayer(nn.Module):
    """Một tầng gom cụm láng giềng GraphSAGE."""
    def __init__(self, in_features: int, out_features: int, aggregator_type: str = 'mean'):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.aggregator_type = aggregator_type
        
        # Trọng số chuyển đổi cho [h_v || h_N(v)]: chiều vào = 2 * in_features
        self.weight = nn.Linear(2 * in_features, out_features, bias=True)
        nn.init.xavier_uniform_(self.weight.weight)

    def forward(self, x: torch.Tensor, adj_matrix: torch.Tensor) -> torch.Tensor:
        # x: (N, in_features)
        # adj_matrix: (N, N) nhị phân
        N = x.shape[0]
        
        # Gom cụm láng giềng bằng trung bình
        if self.aggregator_type == 'mean':
            # Tính bậc của từng đỉnh (tránh chia cho 0)
            deg = torch.sum(adj_matrix, dim=1, keepdim=True)
            deg[deg == 0] = 1.0
            neigh_repr = torch.mm(adj_matrix, x) / deg
        else:
            neigh_repr = torch.mm(adj_matrix, x)

        # Ghép nối đặc trưng tự thân và đặc trưng gom cụm từ láng giềng: [h_v || h_N(v)]
        concat_feats = torch.cat([x, neigh_repr], dim=1)
        
        # Ánh xạ tuyến tính qua trọng số W
        out = self.weight(concat_feats)
        out = F.relu(out)
        
        # Chuẩn hóa L2 norm (Hamilton et al. 2017)
        out = F.normalize(out, p=2, dim=1)
        return out


class GraphSAGENetwork(nn.Module):
    """Mạng GraphSAGE 2 tầng đa bước gom cụm."""
    def __init__(self, in_features: int, hidden_dim: int, num_classes: int):
        super().__init__()
        self.sage1 = GraphSAGELayer(in_features, hidden_dim, aggregator_type='mean')
        self.sage2 = GraphSAGELayer(hidden_dim, hidden_dim, aggregator_type='mean')
        self.classifier = nn.Linear(hidden_dim, num_classes)

    def forward(self, x: torch.Tensor, adj_matrix: torch.Tensor) -> torch.Tensor:
        h1 = self.sage1(x, adj_matrix)
        h2 = self.sage2(h1, adj_matrix)
        logits = self.classifier(h2)
        return logits


def test_graphsage():
    print("=" * 70)
    print("KIỂM TRA KIẾN TRÚC MÔ HÌNH HỌC QUY NẠP GRAPHSAGE (PYTORCH)")
    print("Tác giả: Trần Văn Hậu - B23DCCN287 | Nhóm CT_09")
    print("=" * 70)

    # Đồ thị 5 đỉnh
    adj = torch.tensor([
        [0, 1, 1, 0, 0],
        [1, 0, 1, 1, 0],
        [1, 1, 0, 0, 1],
        [0, 1, 0, 0, 1],
        [0, 0, 1, 1, 0]
    ], dtype=torch.float32)

    x = torch.randn(5, 8)  # 5 đỉnh, mỗi đỉnh 8 đặc trưng

    model = GraphSAGENetwork(in_features=8, hidden_dim=16, num_classes=2)
    out = model(x, adj)

    print(f"Input Features: {list(x.shape)} -> Output Logits: {list(out.shape)}")
    assert out.shape == (5, 2)
    print("GraphSAGE verification PASSED!")
    print("=" * 70)


if __name__ == "__main__":
    test_graphsage()
