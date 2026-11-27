"""
dl_finance.py
Bộ dự báo chuỗi thời gian BiLSTM tích hợp cơ chế Chú ý Thời gian (Temporal Self-Attention)
và định lượng độ bất định Bayes bằng Monte Carlo Dropout (MC Dropout, 200 samples)
cho các cổ phiếu VN30 (FPT, HPG, VCB, VIC) và thị trường vàng SJC.
"""
import torch
import torch.nn as nn
import numpy as np
from typing import Dict, Any, Tuple

class TemporalAttention(nn.Module):
    def __init__(self, hidden_dim: int):
        super().__init__()
        self.attn = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.Tanh(),
            nn.Linear(hidden_dim // 2, 1)
        )

    def forward(self, rnn_out):
        # rnn_out: (batch, seq_len, hidden_dim)
        scores = self.attn(rnn_out) # (batch, seq_len, 1)
        weights = torch.softmax(scores, dim=1)
        context = torch.sum(weights * rnn_out, dim=1) # (batch, hidden_dim)
        return context, weights

class BiLSTMAttentionForecaster(nn.Module):
    def __init__(self, d_in: int = 7, hidden: int = 64, layers: int = 2, dropout: float = 0.2):
        super().__init__()
        self.d_in = d_in
        self.hidden = hidden
        self.rnn = nn.LSTM(
            input_size=d_in,
            hidden_size=hidden,
            num_layers=layers,
            batch_first=True,
            dropout=dropout if layers > 1 else 0.0,
            bidirectional=True
        )
        rnn_dim = hidden * 2 # 128
        self.attention = TemporalAttention(rnn_dim)
        self.head = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(rnn_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )

    def forward(self, x):
        # x: (batch, seq_len, d_in)
        out, _ = self.rnn(x)
        context, attn_weights = self.attention(out)
        pred = self.head(context).squeeze(-1)
        return pred

    def predict_mc_dropout(self, x: torch.Tensor, last_price: float, n_samples: int = 200, res_std: float = 0.015) -> Dict[str, Any]:
        """Thực hiện Monte Carlo Dropout với 200 lượt forward ngẫu nhiên để suy luận khoảng tin cậy 90%."""
        self.train() # Enable dropout during inference
        preds = []
        with torch.no_grad():
            for _ in range(n_samples):
                out = self.forward(x)
                # Sample with residual aleatoric noise
                sampled_ret = out.item() + np.random.normal(0, res_std)
                preds.append(sampled_ret)

        preds = np.array(preds)
        mean_ret = float(np.mean(preds))
        std_ret = float(np.std(preds))
        
        # 90% confidence interval (z = 1.645)
        ci_lower_ret = float(np.percentile(preds, 5))
        ci_upper_ret = float(np.percentile(preds, 95))

        pred_price = last_price * np.exp(mean_ret)
        price_lower = last_price * np.exp(ci_lower_ret)
        price_upper = last_price * np.exp(ci_upper_ret)

        return {
            "last_price": last_price,
            "pred_ret": round(mean_ret, 5),
            "pred_price": round(pred_price, 2),
            "ci_90_ret": [round(ci_lower_ret, 5), round(ci_upper_ret, 5)],
            "ci_90_price": [round(price_lower, 2), round(price_upper, 2)],
            "std_ret": round(std_ret, 5),
            "trend": "TĂNG" if mean_ret > 0 else "GIẢM",
            "samples_count": n_samples
        }
