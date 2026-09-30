"""Train LSTM regressors with Keras/TensorFlow on the real datasets."""
import json
import os

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
import tensorflow as tf

from common import MODEL_DIR, DATASETS, WINDOW, load_series, make_windows, metrics, split_and_scale


def train_one(dataset: str, epochs: int = 18):
    tf.keras.utils.set_random_seed(42)
    _, values = load_series(dataset)
    scaled, scaler, split = split_and_scale(values)
    x, y = make_windows(scaled)
    train_end = split - WINDOW
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(WINDOW, 1)),
        tf.keras.layers.LSTM(32),
        tf.keras.layers.Dense(16, activation="relu"),
        tf.keras.layers.Dense(1),
    ])
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.003), loss="mse")
    model.fit(x[:train_end], y[:train_end], epochs=epochs, batch_size=64, verbose=0)
    predicted = model.predict(x[train_end:], verbose=0)
    actual_values = scaler.inverse_transform(y[train_end:])
    predicted_values = scaler.inverse_transform(predicted)
    result = metrics(actual_values, predicted_values)
    result.update({"framework": "Keras", "dataset": dataset, "window": WINDOW, "epochs": epochs})
    MODEL_DIR.mkdir(exist_ok=True)
    model.save(MODEL_DIR / f"keras_{dataset}.keras")
    with open(MODEL_DIR / f"keras_{dataset}_scaler.json", "w", encoding="utf-8") as file:
        json.dump({"min": scaler.min_.tolist(), "scale": scaler.scale_.tolist()}, file)
    return result


if __name__ == "__main__":
    results = [train_one(dataset) for dataset in DATASETS]
    with open(MODEL_DIR / "keras_metrics.json", "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2)
    print(json.dumps(results, indent=2))
