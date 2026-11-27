# -*- coding: utf-8 -*-
"""
CHƯƠNG 4: SO SÁNH KIẾN TRÚC RNN, LSTM, GRU VÀ TEMPORAL ATTENTION TRÊN PYTORCH
Sinh viên thực hiện: Trần Văn Hậu | MSV: B23DCCN287 | Lớp: D23CTPM01 | Nhóm CT_09
Giảng viên hướng dẫn: PGS. TS. Trần Đình Quế

Bộ 4 mô hình chuỗi thời gian đối chuẩn:
  1. VanillaRNN: Đơn giản, độ phức tạp O(T), dễ biến mất đạo hàm
  2. LSTMModel: Bộ nhớ dài-ngắn giải quyết vanishing gradient
  3. GRUModel: Rút gọn cổng (Reset & Update Gate), tốc độ nhanh hơn ~25%
  4. TemporalAttentionLSTM: Tích hợp cơ chế Attention học trọng số alpha_t
"""

import sys
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

sys.stdout.reconfigure(encoding='utf-8')


class VanillaRNNModel(nn.Module):
    def __init__(self, input_dim=1, hidden_dim=64, num_layers=2, output_dim=1):
        super().__init__()
        self.rnn = nn.RNN(input_dim, hidden_dim, num_layers=num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        out, _ = self.rnn(x)
        # Lấy hidden state ở bước thời gian cuối cùng
        return self.fc(out[:, -1, :])


class LSTMModel(nn.Module):
    def __init__(self, input_dim=1, hidden_dim=64, num_layers=2, output_dim=1, dropout=0.2):
        super().__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers=num_layers, batch_first=True, dropout=dropout)
        self.fc = nn.Sequential(
            nn.Linear(hidden_dim, 32),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(32, output_dim)
        )

    def forward(self, x):
        out, (hn, cn) = self.lstm(x)
        return self.fc(out[:, -1, :])


class GRUModel(nn.Module):
    def __init__(self, input_dim=1, hidden_dim=64, num_layers=2, output_dim=1, dropout=0.2):
        super().__init__()
        self.gru = nn.GRU(input_dim, hidden_dim, num_layers=num_layers, batch_first=True, dropout=dropout)
        self.fc = nn.Sequential(
            nn.Linear(hidden_dim, 32),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(32, output_dim)
        )

    def forward(self, x):
        out, hn = self.gru(x)
        return self.fc(out[:, -1, :])


class TemporalAttentionLSTM(nn.Module):
    """LSTM kết hợp cơ chế Attention trên trục thời gian để tập trung vào các sự kiện then chốt."""
    def __init__(self, input_dim=1, hidden_dim=64, num_layers=2, output_dim=1, dropout=0.2):
        super().__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers=num_layers, batch_first=True, dropout=dropout)
        
        # Mạng tính trọng số Attention: score(h_t) = v^T tanh(W h_t + b)
        self.attn_dense = nn.Linear(hidden_dim, hidden_dim)
        self.attn_v = nn.Linear(hidden_dim, 1, bias=False)
        
        self.fc = nn.Sequential(
            nn.Linear(hidden_dim, 32),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(32, output_dim)
        )

    def forward(self, x):
        # out: (Batch, Seq_len, Hidden)
        out, _ = self.lstm(x)
        
        # Tính điểm năng lượng chú ý: (Batch, Seq_len, Hidden) -> (Batch, Seq_len, 1)
        energy = torch.tanh(self.attn_dense(out))
        attn_scores = self.attn_v(energy)
        
        # Phân phối softmax trên chiều trục thời gian Seq_len
        attn_weights = F.softmax(attn_scores, dim=1)  # (Batch, Seq_len, 1)
        
        # Vectơ ngữ cảnh (Context Vector): tổng có trọng số
        context = torch.sum(attn_weights * out, dim=1)  # (Batch, Hidden)
        
        prediction = self.fc(context)
        return prediction, attn_weights


def test_architectures():
    print("=" * 70)
    print("SO SÁNH 4 KIẾN TRÚC MÔ HÌNH CHUỖI THỜI GIAN (PYTORCH)")
    print("Tác giả: Trần Văn Hậu - B23DCCN287 | Nhóm CT_09")
    print("=" * 70)

    B, T, D = 8, 24, 1  # 8 mẫu, 24 bước thời gian (24 giờ), 1 chiều dữ liệu
    dummy_x = torch.randn(B, T, D)

    models = {
        "1. Vanilla RNN": VanillaRNNModel(input_dim=D, hidden_dim=64),
        "2. LSTM Model": LSTMModel(input_dim=D, hidden_dim=64),
        "3. GRU Model": GRUModel(input_dim=D, hidden_dim=64),
        "4. Temporal Attention LSTM": TemporalAttentionLSTM(input_dim=D, hidden_dim=64)
    }

    for name, m in models.items():
        params = sum(p.numel() for p in m.parameters() if p.requires_grad)
        if "Attention" in name:
            pred, attn = m(dummy_x)
            print(f"{name:28s} | Params: {params:6,d} | Out: {list(pred.shape)} | Attn: {list(attn.shape)}")
        else:
            pred = m(dummy_x)
            print(f"{name:28s} | Params: {params:6,d} | Out: {list(pred.shape)}")

    print("Architecture tests PASSED!")
    print("=" * 70)


if __name__ == "__main__":
    test_architectures()
