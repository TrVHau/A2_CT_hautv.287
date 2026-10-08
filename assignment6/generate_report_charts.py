import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import matplotlib
matplotlib.use("Agg")
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import torch
import tensorflow as tf

from common import ROOT, DATASETS, WINDOW, load_series, make_windows, split_and_scale
from train_pytorch import LSTMRegressor

fig_dir = ROOT / "figures"
fig_dir.mkdir(exist_ok=True)
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.sans-serif': 'DejaVu Sans', 'font.size': 11})

print("Generating figures...")

# 1. AAPL Stock Data Charts
df_stock, vals_stock = load_series("stock")
split_stock = int(len(df_stock) * 0.8)

plt.figure(figsize=(10, 4.5), dpi=300)
plt.plot(df_stock['date'].iloc[:split_stock], df_stock['value'].iloc[:split_stock], label='Tập huấn luyện (Train - 80%)', color='#1f77b4', lw=1.8)
plt.plot(df_stock['date'].iloc[split_stock:], df_stock['value'].iloc[split_stock:], label='Tập kiểm thử (Test - 20%)', color='#ff7f0e', lw=1.8)
plt.axvline(df_stock['date'].iloc[split_stock], color='red', linestyle='--', label='Ranh giới phân chia thời gian')
plt.title('Chuỗi giá đóng cửa cổ phiếu Apple (AAPL) giai đoạn 2013 - 2018', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Thời gian (Năm)')
plt.ylabel('Giá đóng cửa (USD)')
plt.legend(loc='upper left', frameon=True)
plt.tight_layout()
plt.savefig(fig_dir / "aapl_time_series.png")
plt.close()

# AAPL Distribution
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5), dpi=300)
sns.histplot(df_stock['value'], kde=True, ax=ax1, color='#2ca02c', bins=30)
ax1.set_title('Phân bố tần suất (Histogram & KDE) - AAPL', fontsize=11, fontweight='bold')
ax1.set_xlabel('Giá đóng cửa (USD)')
ax1.set_ylabel('Tần suất')

sns.boxplot(y=df_stock['value'], ax=ax2, color='#98df8a', width=0.4)
ax2.set_title('Biểu đồ hộp (Boxplot) - AAPL', fontsize=11, fontweight='bold')
ax2.set_ylabel('Giá đóng cửa (USD)')
plt.tight_layout()
plt.savefig(fig_dir / "aapl_distribution.png")
plt.close()

# 2. Online Retail II Data Charts
df_ret, vals_ret = load_series("transactions")
split_ret = int(len(df_ret) * 0.8)

plt.figure(figsize=(10, 4.5), dpi=300)
plt.plot(df_ret['date'].iloc[:split_ret], df_ret['value'].iloc[:split_ret], label='Tập huấn luyện (Train - 80%)', color='#1f77b4', lw=1.8)
plt.plot(df_ret['date'].iloc[split_ret:], df_ret['value'].iloc[split_ret:], label='Tập kiểm thử (Test - 20%)', color='#d62728', lw=1.8)
plt.axvline(df_ret['date'].iloc[split_ret], color='black', linestyle='--', label='Ranh giới phân chia thời gian')
plt.title('Số lượng đơn hàng duy nhất theo ngày (Online Retail II 2009 - 2011)', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Thời gian')
plt.ylabel('Số Invoice duy nhất / ngày')
plt.legend(loc='upper left', frameon=True)
plt.tight_layout()
plt.savefig(fig_dir / "retail_time_series.png")
plt.close()

# Retail Distribution
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5), dpi=300)
sns.histplot(df_ret['value'], kde=True, ax=ax1, color='#e377c2', bins=30)
ax1.set_title('Phân bố tần suất (Histogram & KDE) - Retail', fontsize=11, fontweight='bold')
ax1.set_xlabel('Số Invoice / ngày')
ax1.set_ylabel('Tần suất')

sns.boxplot(y=df_ret['value'], ax=ax2, color='#f7b6d2', width=0.4)
ax2.set_title('Biểu đồ hộp (Boxplot) - Retail', fontsize=11, fontweight='bold')
ax2.set_ylabel('Số Invoice / ngày')
plt.tight_layout()
plt.savefig(fig_dir / "retail_distribution.png")
plt.close()

# 3. Model Predictions on Test Set
# Stock Predictions
scaled_s, scaler_s, split_s = split_and_scale(vals_stock)
x_s, y_s = make_windows(scaled_s)
train_end_s = split_s - WINDOW
test_dates_s = df_stock['date'].iloc[split_s:]

keras_stock_model = tf.keras.models.load_model(ROOT / "models/keras_stock.keras")
pred_k_s = scaler_s.inverse_transform(keras_stock_model.predict(x_s[train_end_s:], verbose=0))

py_stock_model = LSTMRegressor()
ckpt = torch.load(ROOT / "models/pytorch_stock.pth", map_location="cpu", weights_only=True)
py_stock_model.load_state_dict(ckpt["state_dict"])
py_stock_model.eval()
with torch.no_grad():
    pred_p_s = py_stock_model(torch.tensor(x_s[train_end_s:])).numpy()
pred_p_s = scaler_s.inverse_transform(pred_p_s)
actual_s = scaler_s.inverse_transform(y_s[train_end_s:])

plt.figure(figsize=(11, 5), dpi=300)
plt.plot(test_dates_s, actual_s, label='Giá trị thực tế (Ground Truth)', color='black', lw=2)
plt.plot(test_dates_s, pred_k_s, label='Dự báo Keras LSTM', color='#2ca02c', lw=1.6, linestyle='--')
plt.plot(test_dates_s, pred_p_s, label='Dự báo PyTorch LSTM', color='#1f77b4', lw=1.6, linestyle=':')
plt.title('So sánh dự báo trên tập kiểm thử: Cổ phiếu AAPL', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Ngày giao dịch')
plt.ylabel('Giá đóng cửa (USD)')
plt.legend(loc='upper left', frameon=True)
plt.tight_layout()
plt.savefig(fig_dir / "stock_predictions_comparison.png")
plt.close()

# Retail Predictions
scaled_r, scaler_r, split_r = split_and_scale(vals_ret)
x_r, y_r = make_windows(scaled_r)
train_end_r = split_r - WINDOW
test_dates_r = df_ret['date'].iloc[split_r:]

keras_ret_model = tf.keras.models.load_model(ROOT / "models/keras_transactions.keras")
pred_k_r = scaler_r.inverse_transform(keras_ret_model.predict(x_r[train_end_r:], verbose=0))

py_ret_model = LSTMRegressor()
ckpt_r = torch.load(ROOT / "models/pytorch_transactions.pth", map_location="cpu", weights_only=True)
py_ret_model.load_state_dict(ckpt_r["state_dict"])
py_ret_model.eval()
with torch.no_grad():
    pred_p_r = py_ret_model(torch.tensor(x_r[train_end_r:])).numpy()
pred_p_r = scaler_r.inverse_transform(pred_p_r)
actual_r = scaler_r.inverse_transform(y_r[train_end_r:])

plt.figure(figsize=(11, 5), dpi=300)
plt.plot(test_dates_r, actual_r, label='Giá trị thực tế (Ground Truth)', color='black', lw=2)
plt.plot(test_dates_r, pred_k_r, label='Dự báo Keras LSTM', color='#2ca02c', lw=1.6, linestyle='--')
plt.plot(test_dates_r, pred_p_r, label='Dự báo PyTorch LSTM', color='#d62728', lw=1.6, linestyle=':')
plt.title('So sánh dự báo trên tập kiểm thử: Số giao dịch Online Retail II', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Ngày')
plt.ylabel('Số Invoice / ngày')
plt.legend(loc='upper left', frameon=True)
plt.tight_layout()
plt.savefig(fig_dir / "retail_predictions_comparison.png")
plt.close()

# 4. Metric Comparison Bar Chart
comp_df = pd.read_csv(ROOT / "models/notebook_comparison.csv")
fig, axes = plt.subplots(1, 3, figsize=(14, 4.5), dpi=300)

sns.barplot(data=comp_df, x='Dataset', y='MAE', hue='Framework', ax=axes[0], palette=['#2ca02c', '#1f77b4'])
axes[0].set_title('So sánh MAE (Càng thấp càng tốt)', fontweight='bold')
axes[0].set_ylabel('MAE')

sns.barplot(data=comp_df, x='Dataset', y='RMSE', hue='Framework', ax=axes[1], palette=['#2ca02c', '#1f77b4'])
axes[1].set_title('So sánh RMSE (Càng thấp càng tốt)', fontweight='bold')
axes[1].set_ylabel('RMSE')

sns.barplot(data=comp_df, x='Dataset', y='Seconds', hue='Framework', ax=axes[2], palette=['#2ca02c', '#1f77b4'])
axes[2].set_title('Thời gian huấn luyện (Giây)', fontweight='bold')
axes[2].set_ylabel('Thời gian (s)')

plt.tight_layout()
plt.savefig(fig_dir / "metrics_comparison_bar.png")
plt.close()

# 5. Architecture diagram
fig, ax = plt.subplots(figsize=(10, 4), dpi=300)
ax.axis('off')
boxes = [
    ("Đầu vào chuỗi thời gian\nShape: (Batch, 30, 1)\n30 bước thời gian quá khứ", 0.03, 0.3, 0.22, 0.4, '#e1f5fe', '#0288d1'),
    ("Lớp LSTM Layer\nHidden Size = 32\nTrích xuất phụ thuộc thời gian\nLấy Hidden State cuối (h_30)", 0.32, 0.3, 0.26, 0.4, '#e8f5e9', '#388e3c'),
    ("Fully Connected (Dense)\nUnits = 16\nActivation: ReLU\nTổng hợp phi tuyến", 0.65, 0.3, 0.18, 0.4, '#fff3e0', '#f57c00'),
    ("Lớp Đầu Ra (Output)\nUnits = 1 (Linear)\nGiá trị dự báo y_{t+1}", 0.88, 0.3, 0.11, 0.4, '#fce4ec', '#c2185b')
]
for text, x, y, w, h, bg, border in boxes:
    ax.add_patch(plt.Rectangle((x, y), w, h, facecolor=bg, edgecolor=border, lw=2, transform=ax.transAxes, zorder=2))
    ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=8.5, fontweight='bold', color='#212121', transform=ax.transAxes, zorder=3)

# Arrows
arrows = [(0.25, 0.5, 0.32, 0.5), (0.58, 0.5, 0.65, 0.5), (0.83, 0.5, 0.88, 0.5)]
for x1, y1, x2, y2 in arrows:
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", lw=2.5, color='#424242'),
                xycoords='axes fraction', textcoords='axes fraction', zorder=4)

ax.set_title("Kiến trúc mô hình LSTM Regressor cho dự báo Many-to-One", fontsize=12, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig(fig_dir / "lstm_architecture_diagram.png")
plt.close()

# 6. RNN & LSTM Cell Inner Workings Diagram
fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
ax.axis('off')

# Simple RNN vs LSTM Block
ax.add_patch(plt.Rectangle((0.05, 0.1), 0.4, 0.8, facecolor='#f5f5f5', edgecolor='#616161', lw=2, transform=ax.transAxes))
ax.text(0.25, 0.83, "Cấu trúc Vanilla RNN Cell", ha='center', va='center', fontsize=11, fontweight='bold', color='#1565c0', transform=ax.transAxes)
rnn_text = (
    "• Trạng thái ẩn: h_t duy nhất\n\n"
    "• Công thức cập nhật:\n"
    "  h_t = tanh(W_x · x_t + W_h · h_{t-1} + b)\n\n"
    "• Dự báo đầu ra:\n"
    "  y_t = W_y · h_t + b_y\n\n"
    "• Vấn đề cố hữu:\n"
    "  Vanishing / Exploding Gradient\n"
    "  Khó ghi nhớ phụ thuộc xa (> 10-15 bước)"
)
ax.text(0.08, 0.45, rnn_text, ha='left', va='center', fontsize=9.5, transform=ax.transAxes)

ax.add_patch(plt.Rectangle((0.55, 0.1), 0.4, 0.8, facecolor='#f5f5f5', edgecolor='#616161', lw=2, transform=ax.transAxes))
ax.text(0.75, 0.83, "Cấu trúc LSTM Cell (Long Short-Term Memory)", ha='center', va='center', fontsize=11, fontweight='bold', color='#2e7d32', transform=ax.transAxes)
lstm_text = (
    "• 2 Trạng thái: Cell State (c_t) & Hidden State (h_t)\n\n"
    "• 3 Cổng điều khiển (Gates):\n"
    "  1. Forget Gate: f_t = σ(W_f · [h_{t-1}, x_t] + b_f)\n"
    "  2. Input Gate:  i_t = σ(W_i · [h_{t-1}, x_t] + b_i)\n"
    "     Ứng viên:   c~_t = tanh(W_c · [h_{t-1}, x_t] + b_c)\n"
    "  3. Cập nhật:    c_t = f_t ⊙ c_{t-1} + i_t ⊙ c~_t\n"
    "  4. Output Gate: o_t = σ(W_o · [h_{t-1}, x_t] + b_o)\n"
    "     Trạng thái:  h_t = o_t ⊙ tanh(c_t)\n\n"
    "• Ưu điểm: Băng chuyền c_t bảo toàn Gradient qua thời gian"
)
ax.text(0.57, 0.45, lstm_text, ha='left', va='center', fontsize=9.5, transform=ax.transAxes)

plt.title("So sánh cơ chế hoạt động bên trong Vanilla RNN và LSTM", fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig(fig_dir / "rnn_vs_lstm_cell.png")
plt.close()

print("All charts generated successfully in figures/ directory!")
