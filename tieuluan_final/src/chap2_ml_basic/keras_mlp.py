# -*- coding: utf-8 -*-
"""
CHƯƠNG 2: MẠNG NƠ-RON NHIỀU LỚP (MLP) CÀI ĐẶT BẰNG KERAS / TENSORFLOW
Sinh viên thực hiện: Trần Văn Hậu | MSV: B23DCCN287 | Lớp: D23CTPM01 | Nhóm CT_09
Giảng viên hướng dẫn: PGS. TS. Trần Đình Quế

Mô hình Keras Sequential đồng dạng cấu trúc với ScratchMLP và PyTorchMLP:
  - Linear(8, 64) -> ReLU -> Dropout(0.2)
  - Linear(64, 32) -> ReLU -> Dropout(0.1)
  - Linear(32, 1) -> Sigmoid
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy as np
try:
    import tensorflow as tf
    from tensorflow.keras import layers, models, optimizers
    KERAS_AVAILABLE = True
except ImportError:
    KERAS_AVAILABLE = False


def build_keras_mlp(input_dim=8, h1=64, h2=32, lr=0.001):
    """Xây dựng mô hình MLP phân loại nhị phân trên Keras."""
    if not KERAS_AVAILABLE:
        raise ImportError("TensorFlow / Keras chưa được cài đặt.")

    model = models.Sequential([
        layers.Input(shape=(input_dim,)),
        layers.Dense(h1, activation='relu', kernel_initializer='he_normal', name="dense_1"),
        layers.Dropout(0.2, name="dropout_1"),
        layers.Dense(h2, activation='relu', kernel_initializer='he_normal', name="dense_2"),
        layers.Dropout(0.1, name="dropout_2"),
        layers.Dense(1, activation='sigmoid', kernel_initializer='glorot_normal', name="output")
    ], name="Keras_Binary_MLP")

    model.compile(
        optimizer=optimizers.Adam(learning_rate=lr),
        loss='binary_crossentropy',
        metrics=['accuracy', tf.keras.metrics.AUC(name='auc')]
    )
    return model


def train_keras_mlp(X_train, y_train, X_val=None, y_val=None, epochs=50, batch_size=32, lr=0.001):
    """Huấn luyện mô hình Keras MLP và trả về lịch sử mất mát."""
    model = build_keras_mlp(input_dim=X_train.shape[1], lr=lr)
    val_data = (X_val, y_val) if X_val is not None else None
    
    history = model.fit(
        X_train, y_train,
        validation_data=val_data,
        epochs=epochs,
        batch_size=batch_size,
        verbose=0
    )
    return model, history


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print("Testing Keras MLP architecture...")
    if KERAS_AVAILABLE:
        np.random.seed(42)
        X = np.random.randn(200, 8).astype(np.float32)
        y = (X[:, 0] + X[:, 1] > 0).astype(np.float32)
        model, hist = train_keras_mlp(X[:150], y[:150], X[150:], y[150:], epochs=10)
        preds = model.predict(X[150:], verbose=0)
        print(f"Keras MLP test successfully finished! Val Loss: {hist.history['val_loss'][-1]:.4f}")
    else:
        print("TensorFlow not installed. Skipping Keras test.")
