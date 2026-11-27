import torch
import torch.nn as nn
import torch.nn.functional as F

class MLP(nn.Module):
    def __init__(self, in_features):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_features, 16),
            nn.ReLU(),
            nn.Linear(16, 1)
        )

    def forward(self, x):
        return self.net(x)

class CNN4(nn.Module):
    def __init__(self):
        super().__init__()
        # Input shape: (N, 1, 20, 20)
        # Conv2d: (20 - 3) / 1 + 1 = 18 -> (N, 4, 18, 18)
        # MaxPool2d(2): (18 - 2) / 2 + 1 = 9 -> (N, 4, 9, 9)
        # Flatten: 4 * 9 * 9 = 324 -> Linear(324, 1)
        self.conv = nn.Conv2d(1, 4, kernel_size=3)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(2)
        self.flatten = nn.Flatten()
        self.fc = nn.Linear(4 * 9 * 9, 1)

    def forward(self, x):
        z = self.pool(self.relu(self.conv(x)))
        out = self.fc(self.flatten(z))
        return out

    def get_feature_maps(self, x):
        # Extract feature maps for visualization
        z = self.conv(x)
        return z

class CNN8(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(1, 8, kernel_size=3),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(8 * 9 * 9, 1)
        )

    def forward(self, x):
        return self.net(x)

class DeepCNN(nn.Module):
    def __init__(self):
        super().__init__()
        # 1x20x20 -> Conv(4, 3, pad=1) -> 4x20x20 -> Conv(8, 3, pad=0) -> 8x18x18 -> Pool(2) -> 8x9x9 = 648
        self.net = nn.Sequential(
            nn.Conv2d(1, 4, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(4, 8, kernel_size=3),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(8 * 9 * 9, 1)
        )

    def forward(self, x):
        return self.net(x)

class ResidualBlock(nn.Module):
    """Residual Skip Connection Block for 2D financial pattern feature preservation [UPGRADE]"""
    def __init__(self, channels):
        super().__init__()
        self.conv1 = nn.Conv2d(channels, channels, kernel_size=3, padding=1)
        self.relu = nn.ReLU()
        self.conv2 = nn.Conv2d(channels, channels, kernel_size=3, padding=1)

    def forward(self, x):
        residual = x
        out = self.relu(self.conv1(x))
        out = self.conv2(out)
        out = self.relu(out + residual)
        return out

class ResNetCNN(nn.Module):
    """Modern ResNet architecture for 20x20 GASF images [UPGRADE]"""
    def __init__(self):
        super().__init__()
        self.init_conv = nn.Sequential(
            nn.Conv2d(1, 8, kernel_size=3, padding=1),
            nn.ReLU()
        )
        self.res_block = ResidualBlock(8)
        self.head = nn.Sequential(
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(8 * 10 * 10, 1)
        )

    def forward(self, x):
        z = self.init_conv(x)
        z = self.res_block(z)
        out = self.head(z)
        return out

class SimpleRNNNet(nn.Module):
    def __init__(self, in_features=1, hidden_size=8):
        super().__init__()
        self.rnn = nn.RNN(in_features, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        # x shape: (N, 20, 1)
        out, h_n = self.rnn(x)
        last_hidden = h_n[-1] # shape: (N, hidden_size)
        return self.fc(last_hidden)

class LSTMNet(nn.Module):
    def __init__(self, in_features=1, hidden_size=8):
        super().__init__()
        self.lstm = nn.LSTM(in_features, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        out, (h_n, c_n) = self.lstm(x)
        last_hidden = h_n[-1]
        return self.fc(last_hidden)

class GRUNet(nn.Module):
    def __init__(self, in_features=1, hidden_size=8):
        super().__init__()
        self.gru = nn.GRU(in_features, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        out, h_n = self.gru(x)
        last_hidden = h_n[-1]
        return self.fc(last_hidden)

class BiLSTMNet(nn.Module):
    """Bidirectional LSTM network [UPGRADE]"""
    def __init__(self, in_features=1, hidden_size=8):
        super().__init__()
        self.bilstm = nn.LSTM(in_features, hidden_size, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(hidden_size * 2, 1)

    def forward(self, x):
        out, (h_n, c_n) = self.bilstm(x)
        # Concatenate forward and backward final states
        h_fwd = h_n[-2]
        h_bwd = h_n[-1]
        h_cat = torch.cat([h_fwd, h_bwd], dim=-1)
        return self.fc(h_cat)

class TemporalAttentionLSTM(nn.Module):
    """LSTM with Bahdanau Temporal Attention Mechanism [UPGRADE]"""
    def __init__(self, in_features=1, hidden_size=8):
        super().__init__()
        self.lstm = nn.LSTM(in_features, hidden_size, batch_first=True)
        self.attention_proj = nn.Linear(hidden_size, 1, bias=False)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x, return_weights=False):
        # x: (N, 20, 1)
        outputs, _ = self.lstm(x) # (N, 20, hidden_size)
        
        # Calculate attention scores
        scores = self.attention_proj(torch.tanh(outputs)) # (N, 20, 1)
        weights = F.softmax(scores, dim=1) # (N, 20, 1)
        
        # Compute weighted context vector
        context = torch.sum(outputs * weights, dim=1) # (N, hidden_size)
        logits = self.fc(context) # (N, 1)
        
        if return_weights:
            return logits, weights.squeeze(-1)
        return logits
