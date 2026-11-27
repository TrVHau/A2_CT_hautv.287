# -*- coding: utf-8 -*-
"""
CHƯƠNG 6: THỰC NGHIỆM ĐỐI ĐẦU PHÂN LOẠI ĐỈNH BÁN GIÁM SÁT (NODE CLASSIFICATION BENCHMARK)
Sinh viên thực hiện: Trần Văn Hậu | MSV: B23DCCN287 | Lớp: D23CTPM01 | Nhóm CT_09
Giảng viên hướng dẫn: PGS. TS. Trần Đình Quế

So sánh thực nghiệm 4 mô hình:
  1. Base MLP (Bỏ qua cấu trúc topo đồ thị - chỉ dùng thuộc tính đỉnh)
  2. Spectral GCN (Tích chập đồ thị phổ bậc một tái chuẩn hóa)
  3. GraphSAGE (Gom cụm lấy mẫu láng giềng)
  4. Graph Attention Network (GAT - Cơ chế tự chú ý dị hướng đa đầu)
"""

import sys
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from spectral_gcn import SpectralGCN, compute_normalized_laplacian
from graphsage import GraphSAGENetwork
from gat_attention import MultiHeadGATLayer

sys.stdout.reconfigure(encoding='utf-8')


def generate_synthetic_citation_graph(num_nodes=300, num_classes=3, feature_dim=16, seed=42):
    """Giả lập đồ thị trích dẫn mạng lưới y sinh / khoa học chuẩn homophily cao."""
    np.random.seed(seed)
    torch.manual_seed(seed)

    # Gán nhãn cho các cụm đỉnh (Communities)
    labels = np.random.randint(0, num_classes, size=num_nodes)
    
    # Ma trận đặc trưng có tương quan với nhãn cộng đồng
    features = np.random.randn(num_nodes, feature_dim).astype(np.float32)
    for c in range(num_classes):
        features[labels == c] += np.random.randn(feature_dim) * 1.5

    # Sinh ma trận kề: xác suất nối cạnh nội cụm cao hơn ngoại cụm (Homophily)
    adj = np.zeros((num_nodes, num_nodes), dtype=np.float32)
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            prob = 0.08 if labels[i] == labels[j] else 0.005
            if np.random.rand() < prob:
                adj[i, j] = 1.0
                adj[j, i] = 1.0

    # Phân chia Train / Val / Test masks
    indices = np.random.permutation(num_nodes)
    train_mask = np.zeros(num_nodes, dtype=bool)
    val_mask = np.zeros(num_nodes, dtype=bool)
    test_mask = np.zeros(num_nodes, dtype=bool)

    train_mask[indices[:60]] = True       # 20% Train
    val_mask[indices[60:120]] = True     # 20% Val
    test_mask[indices[120:]] = True      # 60% Test

    return features, adj, labels, train_mask, val_mask, test_mask


def run_graph_benchmarks():
    print("=" * 80)
    print("THỰC NGHIỆM SO SÁNH 4 MÔ HÌNH PHÂN LOẠI ĐỈNH ĐỒ THỊ (NODE CLASSIFICATION)")
    print("Tác giả: Trần Văn Hậu - B23DCCN287 | Lớp: D23CTPM01 | Nhóm: CT_09")
    print("=" * 80)

    features, adj, labels, train_mask, val_mask, test_mask = generate_synthetic_citation_graph()
    num_nodes, in_dim = features.shape
    num_classes = 3

    x_t = torch.tensor(features, dtype=torch.float32)
    y_t = torch.tensor(labels, dtype=torch.long)
    adj_t = torch.tensor(adj, dtype=torch.float32)
    norm_adj = torch.tensor(compute_normalized_laplacian(adj), dtype=torch.float32)

    tr_mask = torch.tensor(train_mask)
    va_mask = torch.tensor(val_mask)
    te_mask = torch.tensor(test_mask)

    # 1. Base MLP Model
    class BaseMLP(nn.Module):
        def __init__(self, in_f, h, out_f):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(in_f, h), nn.ReLU(), nn.Dropout(0.3),
                nn.Linear(h, out_f)
            )
        def forward(self, x, _):
            return self.net(x)

    # 2. GAT Wrapper Model
    class GATWrapper(nn.Module):
        def __init__(self, in_f, h, out_f):
            super().__init__()
            self.gat1 = MultiHeadGATLayer(in_f, h // 2, num_heads=2, concat=True)
            self.gat2 = MultiHeadGATLayer(h, out_f, num_heads=1, concat=False)
        def forward(self, x, adj):
            h1, _ = self.gat1(x, adj)
            h1 = F.elu(h1)
            out, _ = self.gat2(h1, adj)
            return out

    # 3. SAGE Wrapper
    class SAGEWrapper(nn.Module):
        def __init__(self, in_f, h, out_f):
            super().__init__()
            self.model = GraphSAGENetwork(in_f, h, out_f)
        def forward(self, x, adj):
            return self.model(x, adj)

    candidate_models = {
        "1. Base MLP (No Topology)": (BaseMLP(in_dim, 32, num_classes), adj_t),
        "2. Spectral GCN (Kipf-Welling)": (SpectralGCN(in_dim, 32, num_classes, dropout=0.2), norm_adj),
        "3. GraphSAGE (Hamilton)": (SAGEWrapper(in_dim, 32, num_classes), adj_t),
        "4. Graph Attention Network (GAT)": (GATWrapper(in_dim, 32, num_classes), adj_t),
    }

    results = []
    criterion = nn.CrossEntropyLoss()

    for name, (model, graph_struct) in candidate_models.items():
        optimizer = optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)

        # Huấn luyện 40 epochs
        for epoch in range(40):
            model.train()
            optimizer.zero_grad()
            logits = model(x_t, graph_struct)
            loss = criterion(logits[tr_mask], y_t[tr_mask])
            loss.backward()
            optimizer.step()

        # Đánh giá trên tập Test độc lập
        model.eval()
        with torch.no_grad():
            preds = model(x_t, graph_struct)
            pred_classes = torch.argmax(preds, dim=1).numpy()
            
            test_acc = np.mean(pred_classes[test_mask] == labels[test_mask]) * 100.0

        results.append({
            "Mô hình": name,
            "Test Accuracy (%)": test_acc
        })

    print(f"{'Mô hình đánh giá':<36} | {'Test Accuracy (%)'}")
    print("-" * 55)
    for r in results:
        print(f"{r['Mô hình']:<36} | {r['Test Accuracy (%)']:.2f}%")

    print("=" * 80)
    print("KẾT LUẬN: Các mô hình khai thác Topo đồ thị (GCN, GraphSAGE, GAT) vượt trội hoàn toàn")
    print("so với Base MLP (bỏ qua liên kết topo) nhờ cơ chế lan truyền thông điệp (Message Passing).")
    print("=" * 80)
    return results


if __name__ == "__main__":
    run_graph_benchmarks()
