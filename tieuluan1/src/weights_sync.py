import torch
import numpy as np

def sync_mlp_weights(np_model, pt_model, keras_model=None):
    """
    Copy weights from NumPy MLP to PyTorch and Keras models.
    """
    # NumPy: layer 0 is Dense(in, 16), layer 2 is Dense(16, 1)
    dense1_w = np_model.layers[0].weight.value # (16, in_features)
    dense1_b = np_model.layers[0].bias.value   # (16,)
    dense2_w = np_model.layers[2].weight.value # (1, 16)
    dense2_b = np_model.layers[2].bias.value   # (1,)

    # Copy to PyTorch
    with torch.no_grad():
        pt_model.net[0].weight.copy_(torch.from_numpy(dense1_w))
        pt_model.net[0].bias.copy_(torch.from_numpy(dense1_b))
        pt_model.net[2].weight.copy_(torch.from_numpy(dense2_w))
        pt_model.net[2].bias.copy_(torch.from_numpy(dense2_b))

    # Copy to Keras
    if keras_model is not None:
        # Keras expects kernel shape (in_features, out_features)
        keras_model.layers[1].set_weights([dense1_w.T, dense1_b])
        keras_model.layers[2].set_weights([dense2_w.T, dense2_b])

def sync_cnn4_weights(np_model, pt_model, keras_model=None):
    """
    Copy weights from NumPy CNN4 to PyTorch and Keras models.
    """
    conv_w = np_model.layers[0].weight.value  # (4, 1, 3, 3)
    conv_b = np_model.layers[0].bias.value    # (4,)
    fc_w = np_model.layers[4].weight.value    # (1, 324)
    fc_b = np_model.layers[4].bias.value      # (1,)

    with torch.no_grad():
        pt_model.conv.weight.copy_(torch.from_numpy(conv_w))
        pt_model.conv.bias.copy_(torch.from_numpy(conv_b))
        pt_model.fc.weight.copy_(torch.from_numpy(fc_w))
        pt_model.fc.bias.copy_(torch.from_numpy(fc_b))

    if keras_model is not None:
        # Keras channels_first Conv2D kernel shape is (height, width, in_channels, out_channels)
        kw = conv_w.transpose(2, 3, 1, 0)
        keras_model.layers[1].set_weights([kw, conv_b])
        keras_model.layers[4].set_weights([fc_w.T, fc_b])

def sync_lstm_weights(np_model, pt_model, keras_model=None):
    """
    Copy weights from NumPy LSTM to PyTorch and Keras models.
    """
    w_ih = np_model.layers[0].weight_ih.value  # (4*H, in_features)
    w_hh = np_model.layers[0].weight_hh.value  # (4*H, H)
    b_ih = np_model.layers[0].bias_ih.value    # (4*H,)
    fc_w = np_model.layers[1].weight.value     # (1, H)
    fc_b = np_model.layers[1].bias.value       # (1,)

    with torch.no_grad():
        pt_model.lstm.weight_ih_l0.copy_(torch.from_numpy(w_ih))
        pt_model.lstm.weight_hh_l0.copy_(torch.from_numpy(w_hh))
        pt_model.lstm.bias_ih_l0.copy_(torch.from_numpy(b_ih))
        pt_model.lstm.bias_hh_l0.zero_() # set redundant hh bias to 0
        pt_model.fc.weight.copy_(torch.from_numpy(fc_w))
        pt_model.fc.bias.copy_(torch.from_numpy(fc_b))

    if keras_model is not None:
        # PyTorch order: (i, f, g, o). Keras order: (i, f, c, o)
        # Note: g and c are both candidate cell state, identical!
        # Keras weights: [kernel (in, 4H), recurrent_kernel (H, 4H), bias (4H)]
        keras_model.layers[1].set_weights([w_ih.T, w_hh.T, b_ih])
        keras_model.layers[2].set_weights([fc_w.T, fc_b])
