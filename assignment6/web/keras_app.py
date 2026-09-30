"""FastAPI deployment for the Keras LSTM models."""
import json
from pathlib import Path

import numpy as np
import tensorflow as tf
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from common import DATASETS, MODEL_DIR, WINDOW, load_series


ROOT = Path(__file__).resolve().parents[1]
app = FastAPI(title="Assignment 6 - Keras RNN API")
models = {}
scalers = {}


class PredictionRequest(BaseModel):
    dataset: str = Field("stock", pattern="^(stock|transactions)$")
    values: list[float] = Field(default_factory=list)


@app.on_event("startup")
def startup():
    for dataset in DATASETS:
        models[dataset] = tf.keras.models.load_model(MODEL_DIR / f"keras_{dataset}.keras")
        scalers[dataset] = json.loads((MODEL_DIR / f"keras_{dataset}_scaler.json").read_text())


@app.get("/")
def index():
    return FileResponse(ROOT / "web" / "index.html")


@app.get("/series/{dataset}")
def series(dataset: str):
    if dataset not in DATASETS:
        raise HTTPException(404, "Unknown dataset")
    frame, _ = load_series(dataset)
    return {"dataset": dataset, "dates": frame.date.tail(WINDOW).dt.strftime("%Y-%m-%d").tolist(), "values": frame.value.tail(WINDOW).tolist()}


@app.get("/health")
def health():
    return {"status": "healthy", "framework": "Keras", "models": list(models)}


@app.post("/predict")
def predict(request: PredictionRequest):
    values = request.values or load_series(request.dataset)[0].value.tail(WINDOW).tolist()
    if len(values) != WINDOW:
        raise HTTPException(422, f"Exactly {WINDOW} values are required")
    scaler = scalers[request.dataset]
    scaled = np.asarray(values, dtype="float32").reshape(-1, 1) * scaler["scale"] + scaler["min"]
    predicted_scaled = float(models[request.dataset].predict(scaled.reshape(1, WINDOW, 1), verbose=0)[0, 0])
    predicted = (predicted_scaled - scaler["min"][0]) / scaler["scale"][0]
    return {"framework": "Keras", "dataset": request.dataset, "prediction": round(float(predicted), 3), "window": WINDOW}
