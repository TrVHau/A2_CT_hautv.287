"""
dl_healthcare.py
Mô hình học sâu chẩn đoán nguy cơ đái tháo đường típ 2 (ResMLP Classifier)
tích hợp kết nối tắt (Skip Connections), chuẩn hóa theo batch và ước lượng xác suất hậu nghiệm.
"""
import torch
import torch.nn as nn
from typing import Dict, Any, List

class ResidualBlock(nn.Module):
    def __init__(self, hidden_dim: int, dropout_rate: float = 0.2):
        super().__init__()
        self.block = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.LeakyReLU(0.1),
            nn.Dropout(dropout_rate),
            nn.Linear(hidden_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim)
        )
        self.act = nn.LeakyReLU(0.1)

    def forward(self, x):
        return self.act(x + self.block(x))

class DiabetesResMLP(nn.Module):
    def __init__(self, input_dim: int = 8, hidden_dim: int = 64, dropout_rate: float = 0.2):
        super().__init__()
        self.input_layer = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.LeakyReLU(0.1)
        )
        self.res1 = ResidualBlock(hidden_dim, dropout_rate)
        self.res2 = ResidualBlock(hidden_dim, dropout_rate)
        self.head = nn.Sequential(
            nn.Linear(hidden_dim, 32),
            nn.LeakyReLU(0.1),
            nn.Dropout(dropout_rate),
            nn.Linear(32, 1)
        )

    def forward(self, x):
        h = self.input_layer(x)
        h = self.res1(h)
        h = self.res2(h)
        logits = self.head(h).squeeze(-1)
        return logits

    def predict_proba(self, x):
        with torch.no_grad():
            logits = self.forward(x)
            return torch.sigmoid(logits)
