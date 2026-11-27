# -*- coding: utf-8 -*-
"""
CHƯƠNG 2: MẠNG NƠ-RON NHIỀU LỚP (MLP) CÀI ĐẶT BẰNG PYTORCH
Sinh viên thực hiện: Trần Văn Hậu | MSV: B23DCCN287 | Lớp: D23CTPM01 | Nhóm CT_09
Giảng viên hướng dẫn: PGS. TS. Trần Đình Quế

Mô hình PyTorch kế thừa torch.nn.Module, đồng dạng kiến trúc với ScratchMLP:
  Linear(8, 64) -> ReLU -> Dropout(0.2) -> Linear(64, 32) -> ReLU -> Dropout(0.1) -> Linear(32, 1) -> Sigmoid
"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np


class PyTorchMLP(nn.Module):
    """Mạng nơ-ron đa tầng PyTorch cho bài toán phân loại nhị phân."""
    def __init__(self, in_features=8, h1=64, h2=32, out_features=1, dropout_rate=0.2):
        super(PyTorchMLP, self).__init__()
        self.fc1 = nn.Linear(in_features, h1)
        self.relu1 = nn.ReLU()
        self.drop1 = nn.Dropout(p=dropout_rate)
        
        self.fc2 = nn.Linear(h1, h2)
        self.relu2 = nn.ReLU()
        self.drop2 = nn.Dropout(p=dropout_rate / 2.0)
        
        self.fc3 = nn.Linear(h2, out_features)
        self.sigmoid = nn.Sigmoid()
        
        # Khởi tạo He (Kaiming Normal) cho các tầng ReLU
        nn.init.kaiming_normal_(self.fc1.weight, nonlinearity='relu')
        nn.init.zeros_(self.fc1.bias)
        nn.init.kaiming_normal_(self.fc2.weight, nonlinearity='relu')
        nn.init.zeros_(self.fc2.bias)
        nn.init.xavier_normal_(self.fc3.weight)
        nn.init.zeros_(self.fc3.bias)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu1(x)
        x = self.drop1(x)
        x = self.fc2(x)
        x = self.relu2(x)
        x = self.drop2(x)
        x = self.fc3(x)
        x = self.sigmoid(x)
        return x


def train_pytorch_mlp(X_train, y_train, X_val=None, y_val=None, epochs=50, batch_size=32, lr=0.005, seed=42):
    """Huấn luyện PyTorchMLP bằng Adam và BCE Loss."""
    torch.manual_seed(seed)
    in_dim = X_train.shape[1]
    model = PyTorchMLP(in_features=in_dim)
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    X_tr_t = torch.tensor(X_train, dtype=torch.float32)
    y_tr_t = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)

    dataset = torch.utils.data.TensorDataset(X_tr_t, y_tr_t)
    loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)

    history = {'train_loss': [], 'val_loss': []}

    for epoch in range(epochs):
        model.train()
        epoch_loss = 0.0
        for b_x, b_y in loader:
            optimizer.zero_grad()
            out = model(b_x)
            loss = criterion(out, b_y)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item() * len(b_x)
        
        epoch_loss /= len(X_train)
        history['train_loss'].append(epoch_loss)

        if X_val is not None and y_val is not None:
            model.eval()
            with torch.no_grad():
                val_x_t = torch.tensor(X_val, dtype=torch.float32)
                val_y_t = torch.tensor(y_val, dtype=torch.float32).view(-1, 1)
                val_out = model(val_x_t)
                val_loss = criterion(val_out, val_y_t).item()
                history['val_loss'].append(val_loss)

    return model, history


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print("Testing PyTorch MLP...")
    np.random.seed(42)
    X = np.random.randn(200, 8).astype(np.float32)
    y = (X[:, 0] + X[:, 1] > 0).astype(np.float32)
    model, hist = train_pytorch_mlp(X[:150], y[:150], X[150:], y[150:], epochs=15)
    print(f"PyTorch MLP train completed! Final Train Loss: {hist['train_loss'][-1]:.4f}")
