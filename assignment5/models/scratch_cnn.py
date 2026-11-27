"""
Pure NumPy Scratch CNN Engine with Exact Forward & Backward Analytic Gradients
Provides mathematical baseline and parity checking for Conv2D, MaxPool, Dense, and CrossEntropy.
"""

import numpy as np


class Conv2DScratch:
    def __init__(self, in_channels: int, out_channels: int, kernel_size: int = 3, stride: int = 1, padding: int = 0):
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding
        
        # He / Kaiming normal initialization
        std = np.sqrt(2.0 / (in_channels * kernel_size * kernel_size))
        self.W = np.random.randn(out_channels, in_channels, kernel_size, kernel_size) * std
        self.b = np.zeros(out_channels)
        
        self.last_x = None
        self.dW = None
        self.db = None

    def forward(self, x: np.ndarray) -> np.ndarray:
        # x: [B, C_in, H, W]
        self.last_x = x
        B, C, H, W = x.shape
        K = self.kernel_size
        S = self.stride
        P = self.padding
        
        if P > 0:
            x_padded = np.pad(x, ((0, 0), (0, 0), (P, P), (P, P)), mode='constant')
        else:
            x_padded = x
        self.last_x_padded = x_padded
        
        H_out = (H + 2 * P - K) // S + 1
        W_out = (W + 2 * P - K) // S + 1
        out = np.zeros((B, self.out_channels, H_out, W_out), dtype=np.float32)
        
        for oc in range(self.out_channels):
            for i in range(H_out):
                h_start = i * S
                h_end = h_start + K
                for j in range(W_out):
                    w_start = j * S
                    w_end = w_start + K
                    patch = x_padded[:, :, h_start:h_end, w_start:w_end]
                    # elementwise product summed over (C_in, K, K)
                    out[:, oc, i, j] = np.sum(patch * self.W[oc], axis=(1, 2, 3)) + self.b[oc]
        return out

    def backward(self, d_out: np.ndarray) -> np.ndarray:
        # d_out: [B, C_out, H_out, W_out]
        B, C, H, W = self.last_x.shape
        _, OC, H_out, W_out = d_out.shape
        K = self.kernel_size
        S = self.stride
        P = self.padding
        
        self.dW = np.zeros_like(self.W)
        self.db = np.sum(d_out, axis=(0, 2, 3))
        
        dx_padded = np.zeros_like(self.last_x_padded)
        for oc in range(OC):
            for i in range(H_out):
                h_start = i * S
                h_end = h_start + K
                for j in range(W_out):
                    w_start = j * S
                    w_end = w_start + K
                    patch = self.last_x_padded[:, :, h_start:h_end, w_start:w_end]
                    for b in range(B):
                        self.dW[oc] += patch[b] * d_out[b, oc, i, j]
                        dx_padded[b, :, h_start:h_end, w_start:w_end] += self.W[oc] * d_out[b, oc, i, j]
                        
        if P > 0:
            dx = dx_padded[:, :, P:-P, P:-P]
        else:
            dx = dx_padded
        return dx


class MaxPool2DScratch:
    def __init__(self, size: int = 2, stride: int = 2):
        self.size = size
        self.stride = stride
        self.last_x = None

    def forward(self, x: np.ndarray) -> np.ndarray:
        self.last_x = x
        B, C, H, W = x.shape
        K = self.size
        S = self.stride
        H_out = (H - K) // S + 1
        W_out = (W - K) // S + 1
        out = np.zeros((B, C, H_out, W_out), dtype=np.float32)
        
        for i in range(H_out):
            h_start = i * S
            h_end = h_start + K
            for j in range(W_out):
                w_start = j * S
                w_end = w_start + K
                patch = x[:, :, h_start:h_end, w_start:w_end]
                out[:, :, i, j] = np.max(patch, axis=(2, 3))
        return out

    def backward(self, d_out: np.ndarray) -> np.ndarray:
        B, C, H, W = self.last_x.shape
        K = self.size
        S = self.stride
        _, _, H_out, W_out = d_out.shape
        dx = np.zeros_like(self.last_x)
        
        for i in range(H_out):
            h_start = i * S
            h_end = h_start + K
            for j in range(W_out):
                w_start = j * S
                w_end = w_start + K
                patch = self.last_x[:, :, h_start:h_end, w_start:w_end]
                max_vals = np.max(patch, axis=(2, 3), keepdims=True)
                mask = (patch == max_vals)
                mask_sum = np.sum(mask, axis=(2, 3), keepdims=True)
                norm_mask = mask / np.maximum(mask_sum, 1.0)
                dx[:, :, h_start:h_end, w_start:w_end] += norm_mask * d_out[:, :, i:i+1, j:j+1]
        return dx


class ReluScratch:
    def __init__(self):
        self.last_x = None

    def forward(self, x: np.ndarray) -> np.ndarray:
        self.last_x = x
        return np.maximum(0, x)

    def backward(self, d_out: np.ndarray) -> np.ndarray:
        return d_out * (self.last_x > 0)


class DenseScratch:
    def __init__(self, in_features: int, out_features: int):
        self.in_features = in_features
        self.out_features = out_features
        std = np.sqrt(2.0 / in_features)
        self.W = np.random.randn(in_features, out_features) * std
        self.b = np.zeros(out_features)
        self.last_x = None
        self.dW = None
        self.db = None

    def forward(self, x: np.ndarray) -> np.ndarray:
        self.last_x = x
        return np.dot(x, self.W) + self.b

    def backward(self, d_out: np.ndarray) -> np.ndarray:
        self.dW = np.dot(self.last_x.T, d_out)
        self.db = np.sum(d_out, axis=0)
        return np.dot(d_out, self.W.T)


class SoftmaxCrossEntropyScratch:
    def __init__(self):
        self.probs = None
        self.y_one_hot = None

    def forward(self, logits: np.ndarray, y: np.ndarray) -> float:
        # logits: [B, C], y: [B] (integer class labels)
        B, C = logits.shape
        shifted = logits - np.max(logits, axis=1, keepdims=True)
        exp_logits = np.exp(shifted)
        self.probs = exp_logits / np.sum(exp_logits, axis=1, keepdims=True)
        
        self.y_one_hot = np.zeros((B, C))
        self.y_one_hot[np.arange(B), y] = 1.0
        
        loss = -np.mean(np.sum(self.y_one_hot * np.log(self.probs + 1e-12), axis=1))
        return float(loss)

    def backward(self) -> np.ndarray:
        # Exact analytic gradient: dL / dz = (probs - y_one_hot) / B
        B = self.probs.shape[0]
        return (self.probs - self.y_one_hot) / B


class PureNumPyScratchCNN:
    """End-to-End CNN from pure mathematical primitives"""
    def __init__(self):
        self.conv1 = Conv2DScratch(in_channels=1, out_channels=4, kernel_size=3, stride=1, padding=1)
        self.relu1 = ReluScratch()
        self.pool1 = MaxPool2DScratch(size=2, stride=2)
        # 28x28 -> pool1 -> 14x14 * 4 channels = 784
        self.dense = DenseScratch(in_features=4 * 14 * 14, out_features=10)
        self.criterion = SoftmaxCrossEntropyScratch()

    def forward(self, x: np.ndarray) -> np.ndarray:
        h = self.conv1.forward(x)
        h = self.relu1.forward(h)
        h = self.pool1.forward(h)
        self.flat_shape = h.shape
        h_flat = h.reshape(h.shape[0], -1)
        logits = self.dense.forward(h_flat)
        return logits

    def compute_loss(self, logits: np.ndarray, y: np.ndarray) -> float:
        return self.criterion.forward(logits, y)

    def backward(self):
        d_logits = self.criterion.backward()
        d_flat = self.dense.backward(d_logits)
        d_pool = d_flat.reshape(self.flat_shape)
        d_relu = self.pool1.backward(d_pool)
        d_conv = self.relu1.backward(d_relu)
        self.conv1.backward(d_conv)

    def step(self, lr: float = 0.01):
        self.dense.W -= lr * self.dense.dW
        self.dense.b -= lr * self.dense.db
        self.conv1.W -= lr * self.conv1.dW
        self.conv1.b -= lr * self.conv1.b
