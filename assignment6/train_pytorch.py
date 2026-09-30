"""Train LSTM regressors with PyTorch on both Assignment 6 datasets."""
import json
import random

import numpy as np
import torch
from torch import nn

from common import MODEL_DIR, DATASETS, WINDOW, load_series, make_windows, metrics, split_and_scale


class LSTMRegressor(nn.Module):
    def __init__(self, hidden_size: int = 32):
        super().__init__()
        self.lstm = nn.LSTM(input_size=1, hidden_size=hidden_size, batch_first=True)
        self.head = nn.Sequential(nn.Linear(hidden_size, 16), nn.ReLU(), nn.Linear(16, 1))

    def forward(self, values):
        output, _ = self.lstm(values)
        return self.head(output[:, -1, :])


def train_one(dataset: str, epochs: int = 18):
    torch.manual_seed(42)
    random.seed(42)
    _, values = load_series(dataset)
    scaled, scaler, split = split_and_scale(values)
    x, y = make_windows(scaled)
    train_end = split - WINDOW
    x_train, y_train = torch.tensor(x[:train_end]), torch.tensor(y[:train_end])
    x_test, y_test = torch.tensor(x[train_end:]), torch.tensor(y[train_end:])
    model = LSTMRegressor()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.003)
    loss_fn = nn.MSELoss()
    model.train()
    for _ in range(epochs):
        optimizer.zero_grad()
        loss_fn(model(x_train), y_train).backward()
        optimizer.step()
    model.eval()
    with torch.no_grad():
        predicted = model(x_test).numpy()
    actual_values = scaler.inverse_transform(y_test.numpy())
    predicted_values = scaler.inverse_transform(predicted)
    result = metrics(actual_values, predicted_values)
    result.update({"framework": "PyTorch", "dataset": dataset, "window": WINDOW, "epochs": epochs})
    MODEL_DIR.mkdir(exist_ok=True)
    torch.save({"state_dict": model.state_dict(), "window": WINDOW}, MODEL_DIR / f"pytorch_{dataset}.pth")
    with open(MODEL_DIR / f"pytorch_{dataset}_scaler.json", "w", encoding="utf-8") as file:
        json.dump({"min": scaler.min_.tolist(), "scale": scaler.scale_.tolist()}, file)
    return result


if __name__ == "__main__":
    results = [train_one(dataset) for dataset in DATASETS]
    with open(MODEL_DIR / "pytorch_metrics.json", "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2)
    print(json.dumps(results, indent=2))
