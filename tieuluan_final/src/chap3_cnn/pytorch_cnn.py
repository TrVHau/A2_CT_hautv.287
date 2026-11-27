# -*- coding: utf-8 -*-
"""
CHƯƠNG 3: MÔ HÌNH MEDICAL-CNN VÀ RESIDUAL BLOCK TRÊN PYTORCH
Sinh viên thực hiện: Trần Văn Hậu | MSV: B23DCCN287 | Lớp: D23CTPM01 | Nhóm CT_09
Giảng viên hướng dẫn: PGS. TS. Trần Đình Quế

Kiến trúc MedicalCNN:
  - Conv2D(1 -> 32, k=3, p=1) -> BatchNorm2D -> ReLU -> MaxPool2D(2)
  - Residual Block (Conv -> BN -> ReLU -> Conv -> BN + Shortcut)
  - Conv2D(32 -> 64, k=3, p=1) -> BatchNorm2D -> ReLU -> MaxPool2D(2)
  - AdaptiveAvgPool2d((1, 1)) -> Flatten
  - Linear(64, 32) -> Dropout(0.3) -> Linear(32, num_classes)
"""

import sys
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

sys.stdout.reconfigure(encoding='utf-8')


class ResidualBlock(nn.Module):
    """Khối phần dư ResNet với kết nối tắt (Skip Connection): F(x) + x."""
    def __init__(self, channels):
        super().__init__()
        self.conv1 = nn.Conv2d(channels, channels, kernel_size=3, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(channels)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(channels, channels, kernel_size=3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(channels)

    def forward(self, x):
        residual = x
        out = self.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += residual
        return self.relu(out)


class MedicalCNN(nn.Module):
    """Mạng CNN y tế trích xuất đặc trưng hình ảnh và phân loại bệnh học."""
    def __init__(self, in_channels=1, num_classes=2):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(in_channels, 32, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),  # Giảm 1/2 kích thước
            
            ResidualBlock(32),
            
            nn.Conv2d(32, 64, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),  # Giảm tiếp 1/2
            
            ResidualBlock(64),
        )
        self.global_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64, 32),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(32, num_classes)
        )

    def forward(self, x):
        feat = self.features(x)
        pooled = self.global_pool(feat)
        out = self.classifier(pooled)
        return out

    def get_last_conv_layer(self):
        """Trả về tầng tích chập cuối cùng để phục vụ Grad-CAM hook."""
        return self.features[-1].conv2


def test_medical_cnn():
    print("=" * 70)
    print("KIỂM TRA KIẾN TRÚC MEDICAL-CNN & RESIDUAL BLOCK (PYTORCH)")
    print("Tác giả: Trần Văn Hậu - B23DCCN287 | Nhóm CT_09")
    print("=" * 70)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = MedicalCNN(in_channels=1, num_classes=2).to(device)
    
    # Tạo tensor đầu vào giả lập (Batch=4, Channels=1, 28x28)
    dummy_input = torch.randn(4, 1, 28, 28).to(device)
    output = model(dummy_input)

    total_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Tổng số tham số có thể huấn luyện: {total_params:,}")
    print(f"Input shape: {list(dummy_input.shape)} -> Output shape: {list(output.shape)}")
    assert output.shape == (4, 2), f"Expected (4, 2), got {output.shape}"
    print("MedicalCNN verification PASSED!")
    print("=" * 70)


if __name__ == "__main__":
    test_medical_cnn()
