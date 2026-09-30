# Bao cao Assignment 6 - RNN du bao chuoi thoi gian

## 1. Du lieu that

Notebook dung `all_stocks_5yr.csv.zip` va `online_retail_II.csv.zip` trong thu muc `data/`. Bo co phieu co `date, open, high, low, close, volume, Name`; chon ma AAPL va dung `close` lam target. Bo Online Retail II co `Invoice, Quantity, InvoiceDate, Price, Customer ID, Country`; loai invoice bat dau bang C, so luong/gia khong duong, sau do dem invoice duy nhat theo ngay.

Notebook [assignment6_rnn_real_data.ipynb](notebook/assignment6_rnn_real_data.ipynb) mo ta kich thuoc, khoang thoi gian, missing value, phan vi, skew, kurtosis, histogram, KDE, boxplot va line chart. Dieu nay dap ung yeu cau mo ta data va phan bo du lieu.

## 2. RNN va LSTM

RNN cap nhat hidden state theo:

$$h_t = tanh(W_x x_t + W_h h_{t-1} + b_h)$$

LSTM bo sung cell state va cong forget/input/output de giam vanishing gradient. Bai toan la many-to-one: 30 ngay lam dau vao, ngay tiep theo lam nhan. Loss MSE duoc toi uu tren gia tri da scale.

## 3. Quy trinh thi nghiem

Du lieu duoc chia theo thu tu thoi gian 80/20, khong shuffle. MinMaxScaler chi fit tren train. Hai framework dung cung kien truc `LSTM(32) -> Dense(16, ReLU) -> Dense(1)`, cung window 30, Adam learning rate 0.003 va cung so epoch. Metrics gom MAE, RMSE va MAPE tren don vi goc.

## 4. So sanh

Sau khi chay notebook, bang `comparison` la ket qua chinh thuc. So sanh PyTorch va Keras tren cung dataset; khong so truc tiep MAE cua gia AAPL voi MAE cua so invoice vi khac don vi. MAE/RMSE thap hon la tot hon. Nen lap lai nhieu seed hoac walk-forward validation neu can ket luan chac chan.

## 5. Ket luan

Du an da di tu du lieu that -> EDA -> lam sach -> chuan hoa khong leakage -> sliding window -> LSTM PyTorch -> LSTM Keras -> danh gia -> deployment. Mo hinh hien tai la baseline mot bien; co the mo rong voi OHLCV, ngay le, quoc gia, san pham va khuyen mai.
