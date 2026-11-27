"""
Comprehensive CNN Architectures for Multi-Dataset Benchmarking:
1. Basic CNN-2D
2. LeNet-5 (Modernized)
3. VGG-Style CNN
4. ResNet-Style CNN
5. MobileNetV2-Style CNN
6. Conv1D Tabular Clinical Net
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


# ---------------------------------------------------------------------------
# 1. Basic CNN-2D (Baseline)
# ---------------------------------------------------------------------------
class BasicCNN(nn.Module):
    def __init__(self, in_channels: int = 1, num_classes: int = 10):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, 16, kernel_size=3, padding=1)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(2, 2)
        
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.relu2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(2, 2)
        
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(32 * 7 * 7, 64)
        self.relu3 = nn.ReLU()
        self.fc2 = nn.Linear(64, num_classes)

    def forward(self, x):
        h = self.pool1(self.relu1(self.conv1(x)))
        h = self.pool2(self.relu2(self.conv2(h)))
        h = self.flatten(h)
        h = self.relu3(self.fc1(h))
        return self.fc2(h)


# ---------------------------------------------------------------------------
# 2. LeNet-5 Modernized (Yann LeCun 1998)
# ---------------------------------------------------------------------------
class LeNet5(nn.Module):
    def __init__(self, in_channels: int = 1, num_classes: int = 10):
        super().__init__()
        # 28x28 -> Conv 5x5 p=2 -> 28x28 -> AvgPool -> 14x14
        self.conv1 = nn.Conv2d(in_channels, 6, kernel_size=5, padding=2)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.AvgPool2d(2, 2)
        
        # 14x14 -> Conv 5x5 p=0 -> 10x10 -> AvgPool -> 5x5
        self.conv2 = nn.Conv2d(6, 16, kernel_size=5, padding=0)
        self.relu2 = nn.ReLU()
        self.pool2 = nn.AvgPool2d(2, 2)
        
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.relu3 = nn.ReLU()
        self.fc2 = nn.Linear(120, 84)
        self.relu4 = nn.ReLU()
        self.fc3 = nn.Linear(84, num_classes)

    def forward(self, x):
        h = self.pool1(self.relu1(self.conv1(x)))
        h = self.pool2(self.relu2(self.conv2(h)))
        h = self.flatten(h)
        h = self.relu3(self.fc1(h))
        h = self.relu4(self.fc2(h))
        return self.fc3(h)


# ---------------------------------------------------------------------------
# 3. VGG-Style CNN (Simonyan & Zisserman 2014)
# ---------------------------------------------------------------------------
class VGGStyle(nn.Module):
    def __init__(self, in_channels: int = 1, num_classes: int = 10):
        super().__init__()
        self.features = nn.Sequential(
            # Block 1: 28x28 -> 14x14
            nn.Conv2d(in_channels, 16, kernel_size=3, padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.Conv2d(16, 16, kernel_size=3, padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            
            # Block 2: 14x14 -> 7x7
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(32, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(0.3),
            nn.Linear(32 * 7 * 7, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        feat = self.features(x)
        return self.classifier(feat)


# ---------------------------------------------------------------------------
# 4. ResNet-Style CNN (He et al. 2015)
# ---------------------------------------------------------------------------
class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU()
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        
        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )

    def forward(self, x):
        residual = self.shortcut(x)
        out = self.bn2(self.conv2(self.relu(self.bn1(self.conv1(x)))))
        out += residual
        return self.relu(out)


class ResNetStyle(nn.Module):
    def __init__(self, in_channels: int = 1, num_classes: int = 10):
        super().__init__()
        self.prep = nn.Sequential(
            nn.Conv2d(in_channels, 16, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(16),
            nn.ReLU()
        )
        self.layer1 = ResidualBlock(16, 16, stride=1)
        self.layer2 = ResidualBlock(16, 32, stride=2)
        self.gap = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(32, num_classes)

    def forward(self, x):
        h = self.prep(x)
        h = self.layer1(h)
        h = self.layer2(h)
        h = self.gap(h)
        h = torch.flatten(h, 1)
        return self.fc(h)


# ---------------------------------------------------------------------------
# 5. MobileNetV2-Style CNN (Sandler et al. 2018)
# ---------------------------------------------------------------------------
class InvertedResidual(nn.Module):
    def __init__(self, inp, oup, stride, expand_ratio):
        super().__init__()
        self.stride = stride
        self.use_res_connect = self.stride == 1 and inp == oup
        hidden_dim = int(inp * expand_ratio)
        
        layers = []
        if expand_ratio != 1:
            layers.extend([
                nn.Conv2d(inp, hidden_dim, 1, 1, 0, bias=False),
                nn.BatchNorm2d(hidden_dim),
                nn.ReLU6()
            ])
        layers.extend([
            nn.Conv2d(hidden_dim, hidden_dim, 3, stride, 1, groups=hidden_dim, bias=False),
            nn.BatchNorm2d(hidden_dim),
            nn.ReLU6(),
            nn.Conv2d(hidden_dim, oup, 1, 1, 0, bias=False),
            nn.BatchNorm2d(oup)
        ])
        self.conv = nn.Sequential(*layers)

    def forward(self, x):
        if self.use_res_connect:
            return x + self.conv(x)
        return self.conv(x)


class MobileNetV2Style(nn.Module):
    def __init__(self, in_channels: int = 1, num_classes: int = 10):
        super().__init__()
        self.init_conv = nn.Sequential(
            nn.Conv2d(in_channels, 16, 3, 1, 1, bias=False),
            nn.BatchNorm2d(16),
            nn.ReLU6()
        )
        self.stage1 = InvertedResidual(16, 16, stride=1, expand_ratio=1)
        self.stage2 = InvertedResidual(16, 24, stride=2, expand_ratio=3)
        self.stage3 = InvertedResidual(24, 32, stride=2, expand_ratio=3)
        self.gap = nn.AdaptiveAvgPool2d((1, 1))
        self.classifier = nn.Linear(32, num_classes)

    def forward(self, x):
        h = self.init_conv(x)
        h = self.stage1(h)
        h = self.stage2(h)
        h = self.stage3(h)
        h = self.gap(h)
        h = torch.flatten(h, 1)
        return self.classifier(h)


# ---------------------------------------------------------------------------
# 6. Conv1D Tabular Clinical Nets (12 Models Benchmark - 4 Architectures for Tabular)
# ---------------------------------------------------------------------------
class BasicCNN1D(nn.Module):
    def __init__(self, in_channels: int = 1, sequence_length: int = 21, num_classes: int = 2):
        super().__init__()
        self.conv1 = nn.Conv1d(in_channels, 16, kernel_size=3, padding=1)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool1d(2, 2)
        self.conv2 = nn.Conv1d(16, 32, kernel_size=3, padding=1)
        self.relu2 = nn.ReLU()
        self.pool2 = nn.MaxPool1d(2, 2)
        
        flat_dim = 32 * (sequence_length // 4)
        self.fc1 = nn.Linear(flat_dim, 64)
        self.relu3 = nn.ReLU()
        self.fc2 = nn.Linear(64, num_classes)

    def forward(self, x):
        h = self.pool1(self.relu1(self.conv1(x)))
        h = self.pool2(self.relu2(self.conv2(h)))
        h = torch.flatten(h, 1)
        h = self.relu3(self.fc1(h))
        return self.fc2(h)


class LeNet1D(nn.Module):
    def __init__(self, in_channels: int = 1, sequence_length: int = 21, num_classes: int = 2):
        super().__init__()
        self.conv1 = nn.Conv1d(in_channels, 6, kernel_size=3, padding=1)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.AvgPool1d(2, 2)
        self.conv2 = nn.Conv1d(6, 16, kernel_size=3, padding=1)
        self.relu2 = nn.ReLU()
        self.pool2 = nn.AvgPool1d(2, 2)
        
        flat_dim = 16 * (sequence_length // 4)
        self.fc1 = nn.Linear(flat_dim, 64)
        self.relu3 = nn.ReLU()
        self.fc2 = nn.Linear(64, 32)
        self.relu4 = nn.ReLU()
        self.fc3 = nn.Linear(32, num_classes)

    def forward(self, x):
        h = self.pool1(self.relu1(self.conv1(x)))
        h = self.pool2(self.relu2(self.conv2(h)))
        h = torch.flatten(h, 1)
        h = self.relu3(self.fc1(h))
        h = self.relu4(self.fc2(h))
        return self.fc3(h)


class VGG1D(nn.Module):
    def __init__(self, in_channels: int = 1, sequence_length: int = 21, num_classes: int = 2):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv1d(in_channels, 16, kernel_size=3, padding=1),
            nn.BatchNorm1d(16),
            nn.ReLU(),
            nn.Conv1d(16, 16, kernel_size=3, padding=1),
            nn.BatchNorm1d(16),
            nn.ReLU(),
            nn.MaxPool1d(2, 2),
            
            nn.Conv1d(16, 32, kernel_size=3, padding=1),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Conv1d(32, 32, kernel_size=3, padding=1),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.AdaptiveAvgPool1d(2)
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(0.4),
            nn.Linear(32 * 2, 32),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(32, num_classes)
        )

    def forward(self, x):
        return self.classifier(self.features(x))


class ResidualBlock1D(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()
        self.conv1 = nn.Conv1d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm1d(out_channels)
        self.relu = nn.ReLU()
        self.conv2 = nn.Conv1d(out_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm1d(out_channels)
        
        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv1d(in_channels, out_channels, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm1d(out_channels)
            )

    def forward(self, x):
        res = self.shortcut(x)
        out = self.bn2(self.conv2(self.relu(self.bn1(self.conv1(x)))))
        out += res
        return self.relu(out)


class ResNet1D(nn.Module):
    def __init__(self, in_channels: int = 1, num_classes: int = 2):
        super().__init__()
        self.prep = nn.Sequential(
            nn.Conv1d(in_channels, 16, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm1d(16),
            nn.ReLU()
        )
        self.layer1 = ResidualBlock1D(16, 16, stride=1)
        self.layer2 = ResidualBlock1D(16, 32, stride=2)
        self.gap = nn.AdaptiveAvgPool1d(1)
        self.fc = nn.Linear(32, num_classes)

    def forward(self, x):
        h = self.prep(x)
        h = self.layer1(h)
        h = self.layer2(h)
        h = self.gap(h)
        h = torch.flatten(h, 1)
        return self.fc(h)


class Conv1DTabularNet(nn.Module):
    def __init__(self, in_channels: int = 1, sequence_length: int = 16, num_classes: int = 2):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv1d(in_channels, 16, kernel_size=3, padding=1),
            nn.BatchNorm1d(16),
            nn.ReLU(),
            nn.Conv1d(16, 32, kernel_size=3, padding=1),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.AdaptiveAvgPool1d(1)
        )
        self.head = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(0.2),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, num_classes)
        )

    def forward(self, x):
        # x: [Batch, 1, sequence_length]
        feat = self.features(x)
        return self.head(feat)


def count_parameters(model: nn.Module) -> int:
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


if __name__ == "__main__":
    dummy_img = torch.randn(2, 1, 28, 28)
    dummy_tab = torch.randn(2, 1, 16)
    
    models = {
        "BasicCNN": BasicCNN(),
        "LeNet5": LeNet5(),
        "VGGStyle": VGGStyle(),
        "ResNetStyle": ResNetStyle(),
        "MobileNetV2Style": MobileNetV2Style(),
        "Conv1DTabularNet": Conv1DTabularNet()
    }
    
    print("--- Model Parameters & Output Shapes ---")
    for name, m in models.items():
        inp = dummy_tab if "Tabular" in name else dummy_img
        out = m(inp)
        params = count_parameters(m)
        print(f"{name:18} | Params: {params:8,d} | Out: {list(out.shape)}")
