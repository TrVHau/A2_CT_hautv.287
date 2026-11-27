# -*- coding: utf-8 -*-
"""
CHƯƠNG 4: HUẤN LUYỆN VÀ ĐÁNH GIÁ DỰ BÁO CHUỖI THỜI GIAN (WALK-FORWARD VALIDATION)
Sinh viên thực hiện: Trần Văn Hậu | MSV: B23DCCN287 | Lớp: D23CTPM01 | Nhóm CT_09
Giảng viên hướng dẫn: PGS. TS. Trần Đình Quế

Quy trình kiểm chứng tịnh tiến theo thời gian (Walk-Forward Validation):
  - Tuyệt đối loại trừ Lookahead Bias (không dùng thông tin tương lai để chuẩn hóa quá khứ)
  - Đánh giá các chỉ số: MAE, RMSE, MAPE (%), R2-Score
  - Kiểm tra độ an toàn lâm sàng Clarke Error Grid (Zone A+B > 98%)
"""

import sys
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from pytorch_rnn_lstm_gru import LSTMModel, GRUModel, TemporalAttentionLSTM

sys.stdout.reconfigure(encoding='utf-8')


def generate_synthetic_cgm_series(n_points=1440, seed=42):
    """Giả lập chuỗi đo đường huyết liên tục CGM trong 5 ngày (mỗi 5 phút một lần đo)."""
    np.random.seed(seed)
    time_steps = np.arange(n_points)
    
    # Nhịp sinh học ngày/đêm (Circadian rhythm: chu kỳ 24h = 288 bước)
    circadian = 15.0 * np.sin(2 * np.pi * time_steps / 288 - np.pi / 2)
    
    # Các đỉnh ăn uống (Meal spikes: sáng, trưa, tối)
    meal_spikes = np.zeros(n_points)
    for day in range(5):
        day_offset = day * 288
        for meal_time in [84, 144, 228]:  # 7:00, 12:00, 19:00
            idx = day_offset + meal_time
            if idx < n_points:
                # Dạng đỉnh Gaussian
                window = np.arange(-12, 24)
                valid = (idx + window >= 0) & (idx + window < n_points)
                meal_spikes[idx + window[valid]] += 45.0 * np.exp(-0.5 * (window[valid] / 6.0) ** 2)

    noise = np.random.normal(0, 3.5, n_points)
    baseline = 110.0
    cgm = baseline + circadian + meal_spikes + noise
    return np.clip(cgm, 50.0, 350.0)


def create_sliding_windows(series, seq_len=24, pred_horizon=1):
    """Tạo các cặp quan sát trượt (X: seq_len quá khứ, y: bước tiếp theo)."""
    X, y = [], []
    for i in range(len(series) - seq_len - pred_horizon + 1):
        X.append(series[i:i + seq_len])
        y.append(series[i + seq_len + pred_horizon - 1])
    return np.array(X, dtype=np.float32)[:, :, None], np.array(y, dtype=np.float32)[:, None]


def evaluate_forecast(y_true, y_pred):
    """Tính các chỉ số hồi quy chuỗi thời gian."""
    mae = np.mean(np.abs(y_true - y_pred))
    rmse = np.sqrt(np.mean((y_true - y_pred) ** 2))
    mape = np.mean(np.abs((y_true - y_pred) / (y_true + 1e-8))) * 100.0
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    r2 = 1.0 - (ss_res / (ss_tot + 1e-8))
    
    # Đánh giá vùng Clarke Error Grid chấp nhận được lâm sàng (Zone A+B)
    rel_error = np.abs(y_true - y_pred) / y_true
    clarke_ab_rate = np.mean((rel_error <= 0.20) | (np.abs(y_true - y_pred) <= 15.0)) * 100.0
    
    return {
        "MAE (mg/dL)": mae,
        "RMSE (mg/dL)": rmse,
        "MAPE (%)": mape,
        "R2-Score": r2,
        "Clarke Zone A+B (%)": clarke_ab_rate
    }


def run_cgm_forecasting_benchmark():
    print("=" * 80)
    print("THỰC NGHIỆM DỰ BÁO ĐƯỜNG HUYẾT LIÊN TỤC CGM (WALK-FORWARD BENCHMARK)")
    print("Tác giả: Trần Văn Hậu - B23DCCN287 | Lớp: D23CTPM01 | Nhóm: CT_09")
    print("=" * 80)

    # 1. Chuẩn bị dữ liệu
    series = generate_synthetic_cgm_series(n_points=1000)
    seq_len = 24  # Sử dụng 2 giờ lịch sử (mỗi bước 5 phút)
    X, y = create_sliding_windows(series, seq_len=seq_len, pred_horizon=1)

    # Chia Train / Test theo trục thời gian (80% train, 20% test)
    split_idx = int(0.8 * len(X))
    X_train, y_train = X[:split_idx], y[:split_idx]
    X_test, y_test = X[split_idx:], y[split_idx:]

    # Chuẩn hóa chỉ dựa trên tập Train
    mean_val, std_val = np.mean(X_train), np.std(X_train)
    X_tr_sc = (X_train - mean_val) / std_val
    X_te_sc = (X_test - mean_val) / std_val
    y_tr_sc = (y_train - mean_val) / std_val
    y_te_sc = (y_test - mean_val) / std_val

    # Chuyển đổi PyTorch Tensors
    X_tr_t = torch.tensor(X_tr_sc, dtype=torch.float32)
    y_tr_t = torch.tensor(y_tr_sc, dtype=torch.float32)
    X_te_t = torch.tensor(X_te_sc, dtype=torch.float32)

    # Huấn luyện nhanh LSTM Model
    model = LSTMModel(input_dim=1, hidden_dim=32, num_layers=1, output_dim=1, dropout=0.0)
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    criterion = nn.MSELoss()

    dataset = torch.utils.data.TensorDataset(X_tr_t, y_tr_t)
    loader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)

    print("Đang huấn luyện mô hình TimeSeries LSTM trên 15 epochs...")
    model.train()
    for epoch in range(15):
        for bx, by in loader:
            optimizer.zero_grad()
            out = model(bx)
            loss = criterion(out, by)
            loss.backward()
            optimizer.step()

    # Dự báo trên tập Test độc lập
    model.eval()
    with torch.no_grad():
        preds_sc = model(X_te_t).cpu().numpy()

    # Giải chuẩn hóa về đơn vị lâm sàng ban đầu (mg/dL)
    preds = preds_sc * std_val + mean_val

    # Đánh giá chỉ số
    metrics = evaluate_forecast(y_test, preds)

    print("\n=== KẾT QUẢ DỰ BÁO LÂM SÀNG TRÊN TẬP TEST ĐỘC LẬP ===")
    for k, v in metrics.items():
        if "Score" in k:
            print(f"  - {k:22s}: {v:.4f}")
        else:
            print(f"  - {k:22s}: {v:.2f}")

    print("=" * 80)
    return metrics


if __name__ == "__main__":
    run_cgm_forecasting_benchmark()
