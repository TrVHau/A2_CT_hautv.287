# -*- coding: utf-8 -*-
"""
CHƯƠNG 2: MẠNG NƠ-RON NHIỀU LỚP (MLP) CÀI ĐẶT THUẦN TỪ ĐẦU BẰNG PYTHON & NUMPY
Sinh viên thực hiện: Trần Văn Hậu | MSV: B23DCCN287 | Lớp: D23CTPM01 | Nhóm CT_09
Giảng viên hướng dẫn: PGS. TS. Trần Đình Quế

Hiện thực hóa toàn bộ:
  - Khởi tạo trọng số He (Kaiming Normal) cho hàm kích hoạt ReLU
  - Lan truyền tiến (Forward Pass): Affine transform -> ReLU -> Affine -> ReLU -> Affine -> Sigmoid
  - Hàm mất mát Binary Cross-Entropy (BCE)
  - Lan truyền ngược (Backward Pass): Đạo hàm giải tích ma trận cho từng lớp
  - Tối ưu hóa hạ gradient (Mini-batch Gradient Descent)
"""

import numpy as np


def relu(z):
    """Hàm kích hoạt Rectified Linear Unit: max(0, z)"""
    return np.maximum(0, z)


def relu_derivative(z):
    """Đạo hàm bậc 1 của hàm ReLU: 1 nếu z > 0, ngược lại bằng 0"""
    return (z > 0).astype(float)


def sigmoid(z):
    """Hàm kích hoạt Sigmoid với cơ chế chống tràn số học (numerical overflow clipping)"""
    z_clipped = np.clip(z, -25.0, 25.0)
    return 1.0 / (1.0 + np.exp(-z_clipped))


class ScratchMLP:
    """Mạng nơ-ron nhiều lớp (Multilayer Perceptron) thuần bằng NumPy."""
    def __init__(self, in_dim=8, h1=64, h2=32, out_dim=1, lr=0.01, random_state=42):
        self.lr = lr
        np.random.seed(random_state)
        
        # Khởi tạo He Normal cho các tầng ẩn ReLU: std = sqrt(2 / fan_in)
        self.W1 = np.random.randn(in_dim, h1) * np.sqrt(2.0 / in_dim)
        self.b1 = np.zeros((1, h1))
        
        self.W2 = np.random.randn(h1, h2) * np.sqrt(2.0 / h1)
        self.b2 = np.zeros((1, h2))
        
        # Khởi tạo Xavier/Glorot cho tầng ra Sigmoid: std = sqrt(2 / (fan_in + fan_out))
        self.W3 = np.random.randn(h2, out_dim) * np.sqrt(2.0 / (h2 + out_dim))
        self.b3 = np.zeros((1, out_dim))

    def forward(self, X):
        """Lan truyền tiến qua 3 tầng (Layer 1 -> Layer 2 -> Layer 3)"""
        # Tầng ẩn 1
        self.Z1 = np.dot(X, self.W1) + self.b1
        self.A1 = relu(self.Z1)
        
        # Tầng ẩn 2
        self.Z2 = np.dot(self.A1, self.W2) + self.b2
        self.A2 = relu(self.Z2)
        
        # Tầng ra
        self.Z3 = np.dot(self.A2, self.W3) + self.b3
        self.A3 = sigmoid(self.Z3)
        return self.A3

    def compute_loss(self, y_true, y_pred):
        """Hàm mất mát Binary Cross-Entropy (BCE)"""
        m = y_true.shape[0]
        eps = 1e-12
        y_p = np.clip(y_pred, eps, 1.0 - eps)
        loss = - (1.0 / m) * np.sum(y_true * np.log(y_p) + (1.0 - y_true) * np.log(1.0 - y_p))
        return loss

    def backward(self, X, y_true, y_pred):
        """Lan truyền ngược tính toán gradient giải tích ma trận theo quy tắc chuỗi"""
        m = X.shape[0]
        y_t = y_true.reshape(-1, 1)
        
        # Đạo hàm của BCE kết hợp hàm Sigmoid tại tầng ra: dZ3 = y_pred - y_true
        self.dZ3 = y_pred - y_t
        self.dW3 = (1.0 / m) * np.dot(self.A2.T, self.dZ3)
        self.db3 = (1.0 / m) * np.sum(self.dZ3, axis=0, keepdims=True)

        # Lan truyền ngược qua Tầng ẩn 2
        self.dA2 = np.dot(self.dZ3, self.W3.T)
        self.dZ2 = self.dA2 * relu_derivative(self.Z2)
        self.dW2 = (1.0 / m) * np.dot(self.A1.T, self.dZ2)
        self.db2 = (1.0 / m) * np.sum(self.dZ2, axis=0, keepdims=True)

        # Lan truyền ngược qua Tầng ẩn 1
        self.dA1 = np.dot(self.dZ2, self.W2.T)
        self.dZ1 = self.dA1 * relu_derivative(self.Z1)
        self.dW1 = (1.0 / m) * np.dot(X.T, self.dZ1)
        self.db1 = (1.0 / m) * np.sum(self.dZ1, axis=0, keepdims=True)

        return {
            'W1': self.dW1, 'b1': self.db1,
            'W2': self.dW2, 'b2': self.db2,
            'W3': self.dW3, 'b3': self.db3
        }

    def update_params(self, lr=None):
        """Cập nhật trọng số theo thuật toán hạ gradient (SGD)"""
        rate = lr if lr is not None else self.lr
        self.W3 -= rate * self.dW3
        self.b3 -= rate * self.db3
        self.W2 -= rate * self.dW2
        self.b2 -= rate * self.db2
        self.W1 -= rate * self.dW1
        self.b1 -= rate * self.db1

    def fit(self, X, y, epochs=200, batch_size=32, verbose=False):
        """Huấn luyện mô hình theo mini-batch"""
        m = X.shape[0]
        history = []
        for epoch in range(epochs):
            # Xáo trộn ngẫu nhiên dữ liệu theo epoch
            indices = np.random.permutation(m)
            X_shuffled = X[indices]
            y_shuffled = y[indices]

            for i in range(0, m, batch_size):
                X_batch = X_shuffled[i:i + batch_size]
                y_batch = y_shuffled[i:i + batch_size]

                y_pred = self.forward(X_batch)
                self.backward(X_batch, y_batch, y_pred)
                self.update_params()

            if (epoch + 1) % 50 == 0 or epoch == 0:
                full_pred = self.forward(X)
                loss = self.compute_loss(y.reshape(-1, 1), full_pred)
                history.append(loss)
                if verbose:
                    print(f"Epoch {epoch+1:03d}/{epochs} - Loss: {loss:.4f}")
        return history

    def predict_proba(self, X):
        return self.forward(X).flatten()

    def predict(self, X, threshold=0.5):
        probs = self.predict_proba(X)
        return (probs >= threshold).astype(int)


if __name__ == "__main__":
    print("Kiểm tra hoạt động ScratchMLP:")
    np.random.seed(42)
    X_toy = np.random.randn(100, 8)
    y_toy = (X_toy[:, 0] + X_toy[:, 1] > 0).astype(int)
    
    mlp = ScratchMLP(in_dim=8, h1=64, h2=32, out_dim=1, lr=0.05)
    hist = mlp.fit(X_toy, y_toy, epochs=100, verbose=True)
    preds = mlp.predict(X_toy)
    acc = np.mean(preds == y_toy)
    print(f"Toy dataset training accuracy: {acc * 100:.2f}%")
