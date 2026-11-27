import os
os.environ['KERAS_BACKEND'] = 'torch'
import keras
from keras import layers

def build_keras_mlp(in_features):
    inputs = layers.Input(shape=(in_features,))
    z = layers.Dense(16, activation='relu')(inputs)
    outputs = layers.Dense(1)(z)
    model = keras.Model(inputs=inputs, outputs=outputs, name='Keras_MLP')
    return model

def build_keras_cnn4():
    # Input shape: (1, 20, 20) channels_first
    inputs = layers.Input(shape=(1, 20, 20))
    z = layers.Conv2D(4, kernel_size=3, data_format='channels_first', activation='relu')(inputs)
    z = layers.MaxPooling2D(2, data_format='channels_first')(z)
    z = layers.Flatten()(z)
    outputs = layers.Dense(1)(z)
    model = keras.Model(inputs=inputs, outputs=outputs, name='Keras_CNN4')
    return model

def build_keras_cnn8():
    inputs = layers.Input(shape=(1, 20, 20))
    z = layers.Conv2D(8, kernel_size=3, data_format='channels_first', activation='relu')(inputs)
    z = layers.MaxPooling2D(2, data_format='channels_first')(z)
    z = layers.Flatten()(z)
    outputs = layers.Dense(1)(z)
    model = keras.Model(inputs=inputs, outputs=outputs, name='Keras_CNN8')
    return model

def build_keras_simplernn(seq_len=20, in_features=1, hidden_size=8):
    inputs = layers.Input(shape=(seq_len, in_features))
    z = layers.SimpleRNN(hidden_size)(inputs)
    outputs = layers.Dense(1)(z)
    model = keras.Model(inputs=inputs, outputs=outputs, name='Keras_SimpleRNN')
    return model

def build_keras_lstm(seq_len=20, in_features=1, hidden_size=8):
    inputs = layers.Input(shape=(seq_len, in_features))
    z = layers.LSTM(hidden_size)(inputs)
    outputs = layers.Dense(1)(z)
    model = keras.Model(inputs=inputs, outputs=outputs, name='Keras_LSTM')
    return model

def build_keras_gru(seq_len=20, in_features=1, hidden_size=8):
    inputs = layers.Input(shape=(seq_len, in_features))
    z = layers.GRU(hidden_size)(inputs)
    outputs = layers.Dense(1)(z)
    model = keras.Model(inputs=inputs, outputs=outputs, name='Keras_GRU')
    return model
