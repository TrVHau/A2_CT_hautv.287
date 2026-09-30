"""Shared time-series loading, scaling, windowing, and evaluation helpers."""
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import MinMaxScaler


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
MODEL_DIR = ROOT / "models"
WINDOW = 30
DATASETS = {
    "stock": DATA_DIR / "all_stocks_5yr.csv.zip",
    "transactions": DATA_DIR / "online_retail_II.csv.zip",
}


def load_series(dataset: str):
    path = DATASETS[dataset]
    if not path.exists():
        raise FileNotFoundError(f"Missing real dataset: {path}")
    if dataset == "stock":
        source = pd.read_csv(path, compression="zip", parse_dates=["date"])
        frame = (source[source["Name"].eq("AAPL")]
                 .sort_values("date")[["date", "close"]]
                 .rename(columns={"close": "value"})
                 .dropna())
    else:
        source = pd.read_csv(path, compression="zip", parse_dates=["InvoiceDate"])
        source["Invoice"] = source["Invoice"].astype(str)
        source = source[~source["Invoice"].str.startswith("C", na=False)]
        source = source[(source["Quantity"] > 0) & (source["Price"] > 0)].dropna(subset=["InvoiceDate", "Invoice"])
        frame = (source.assign(date=source["InvoiceDate"].dt.floor("D"))
                 .groupby("date", as_index=False)["Invoice"].nunique()
                 .rename(columns={"Invoice": "value"})
                 .sort_values("date"))
    return frame, frame[["value"]].to_numpy(dtype="float32")


def split_and_scale(values: np.ndarray):
    split = int(len(values) * 0.8)
    scaler = MinMaxScaler()
    scaler.fit(values[:split])
    scaled = scaler.transform(values).astype("float32")
    return scaled, scaler, split


def make_windows(values: np.ndarray, window: int = WINDOW):
    x, y = [], []
    for index in range(window, len(values)):
        x.append(values[index - window:index])
        y.append(values[index])
    return np.asarray(x, dtype="float32"), np.asarray(y, dtype="float32")


def metrics(actual: np.ndarray, predicted: np.ndarray):
    return {
        "mae": round(float(mean_absolute_error(actual, predicted)), 4),
        "rmse": round(float(np.sqrt(mean_squared_error(actual, predicted))), 4),
    }
