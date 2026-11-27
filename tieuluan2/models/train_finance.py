"""
train_finance.py
Quy trình huấn luyện bộ dự báo BiLSTMAttentionForecaster trên chuỗi dữ liệu tài chính
(FPT, HPG, VCB, VIC, Vàng SJC) với cửa sổ trượt 30 phiên x 7 đặc trưng.
"""
import os
import json
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from .dl_finance import BiLSTMAttentionForecaster

def create_sliding_windows(df: pd.DataFrame, target_col="FPT", window_size=30):
    # Compute log returns
    df = df.copy()
    df["ret_target"] = np.log(df[target_col] / df[target_col].shift(1))
    df["ret_usdvnd"] = np.log(df["USD_VND"] / df["USD_VND"].shift(1))
    df["ret_xau"] = np.log(df["XAU_USD"] / df["XAU_USD"].shift(1))
    df["ret_dxy"] = np.log(df["DXY"] / df["DXY"].shift(1))
    df["ret_vn30"] = np.log(df["VN30"] / df["VN30"].shift(1))
    
    # 20-day moving average deviation
    ma20 = df[target_col].rolling(20).mean()
    df["ma20_dev"] = (df[target_col] - ma20) / (ma20 + 1e-5)
    
    # 20-day rolling volatility
    df["vol20"] = df["ret_target"].rolling(20).std()

    feature_cols = ["ret_target", "ret_usdvnd", "ret_xau", "ret_dxy", "ret_vn30", "ma20_dev", "vol20"]
    df = df.dropna().reset_index(drop=True)

    X, y, prices = [], [], []
    feats = df[feature_cols].values
    target_returns = df["ret_target"].values
    target_prices = df[target_col].values

    for i in range(len(df) - window_size):
        X.append(feats[i : i + window_size])
        y.append(target_returns[i + window_size])
        prices.append(target_prices[i + window_size - 1])

    return np.array(X, dtype=np.float32), np.array(y, dtype=np.float32), np.array(prices, dtype=np.float32), feature_cols, df

def train_finance_model(data_path="tieuluan2/data/market_series.csv", output_dir="tieuluan2/models/saved_weights"):
    os.makedirs(output_dir, exist_ok=True)
    print("Loading financial market series...")
    df = pd.read_csv(data_path)

    target_ticker = "FPT"
    X, y, prices, feat_cols, df_clean = create_sliding_windows(df, target_col=target_ticker, window_size=30)
    
    # Temporal chronological split (80% train, 20% test)
    split_idx = int(len(X) * 0.8)
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    prices_test = prices[split_idx:]

    train_dataset = torch.utils.data.TensorDataset(torch.tensor(X_train), torch.tensor(y_train))
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=64, shuffle=True)

    model = BiLSTMAttentionForecaster(d_in=len(feat_cols), hidden=64, layers=2, dropout=0.2)
    criterion = nn.HuberLoss(delta=1.0)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.002, weight_decay=1e-4)

    print("Training BiLSTMAttentionForecaster...")
    model.train()
    for epoch in range(15):
        for bx, by in train_loader:
            optimizer.zero_grad()
            pred = model(bx)
            loss = criterion(pred, by)
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()

    model.eval()
    with torch.no_grad():
        test_pred_ret = model(torch.tensor(X_test)).numpy()

    # Evaluation metrics
    rmse_model = np.sqrt(np.mean((y_test - test_pred_ret) ** 2))
    rmse_naive = np.sqrt(np.mean(y_test ** 2)) # Naive zero return forecast
    ratio = rmse_model / max(1e-5, rmse_naive)
    
    # Directional Accuracy (DA)
    da = np.mean((y_test * test_pred_ret) > 0)

    print(f"Test -> RMSE: {rmse_model:.5f}, Naive RMSE: {rmse_naive:.5f}, Ratio: {ratio:.4f} (<1.0 is predictive), DA: {da*100:.2f}%")

    weight_path = os.path.join(output_dir, "finance_bilstm.pt")
    torch.save(model.state_dict(), weight_path)

    meta = {
        "ticker": target_ticker,
        "window_size": 30,
        "feature_cols": feat_cols,
        "metrics": {
            "rmse_model": round(float(rmse_model), 5),
            "rmse_naive": round(float(rmse_naive), 5),
            "ratio_to_naive": round(float(ratio), 4),
            "directional_accuracy_pct": round(float(da * 100), 2)
        },
        "last_known_price": float(prices_test[-1])
    }
    with open(os.path.join(output_dir, "finance_meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    print(f"Saved weights to {weight_path}")
    return meta

if __name__ == "__main__":
    train_finance_model()
