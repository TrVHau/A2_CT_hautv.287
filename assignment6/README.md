# Assignment 6 - RNN chuoi thoi gian

Notebook chinh: [notebook/assignment6_rnn_real_data.ipynb](notebook/assignment6_rnn_real_data.ipynb)

Du an dung hai bo du lieu that da co san trong `data/`:

- `all_stocks_5yr.csv.zip`: du lieu co phieu nhieu ma, notebook loc `AAPL` va du bao `close`.
- `online_retail_II.csv.zip`: du lieu giao dich ban le Online Retail II, notebook loai invoice huy va tong hop so invoice khac nhau theo ngay.

## Chay notebook

```bash
conda activate assignment2
cd /home/dau/assignment2/assignment6
jupyter notebook notebook/assignment6_rnn_real_data.ipynb
```

Chon kernel Python cua moi truong `assignment2`, sau do chay tu tren xuong duoi. Notebook trinh bay ly thuyet RNN/LSTM, ham cap nhat hidden state, EDA va phan bo, lam sach du lieu, chia chuoi theo thoi gian, MinMaxScaler khong leakage, sliding window 30 ngay, LSTM PyTorch, LSTM Keras, MAE/RMSE/MAPE, bieu do va bang so sanh.

## Web deployment

```bash
uvicorn web.pytorch_app:app --app-dir /home/dau/assignment2/assignment6 --reload --port 8001
uvicorn web.keras_app:app --app-dir /home/dau/assignment2/assignment6 --reload --port 8002
```

Mo `http://127.0.0.1:8001` cho PyTorch va `http://127.0.0.1:8002` cho Keras. Swagger o `/docs`, health check o `/health`.

## Cau truc

```text
assignment6/
├── data/                         # hai file ZIP du lieu that
├── notebook/assignment6_rnn_real_data.ipynb
├── train_pytorch.py
├── train_keras.py
├── web/pytorch_app.py
├── web/keras_app.py
├── web/index.html
└── report.md
```
