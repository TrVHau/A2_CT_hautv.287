import os, sys
os.environ['KERAS_BACKEND'] = 'torch'
import numpy as np
import torch
import keras

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from models_numpy import Dense as NPDense, ReLU as NPReLU, Conv2D as NPConv2D, MaxPool2D as NPMaxPool2D, Flatten as NPFlatten
from models_pytorch import MLP as PTMLP, CNN4 as PTCNN4
from models_keras import build_keras_mlp, build_keras_cnn4
from weights_sync import sync_mlp_weights, sync_cnn4_weights

class NPMLP:
    def __init__(self, in_features):
        self.layers = [NPDense(in_features, 16), NPReLU(), NPDense(16, 1)]
    def __call__(self, x):
        out = x
        for l in self.layers:
            out = l.forward(out)
        return out

class NPCNN4:
    def __init__(self):
        self.layers = [
            NPConv2D(1, 4, kernel_size=3, stride=1, padding=0),
            NPReLU(),
            NPMaxPool2D(2, stride=2),
            NPFlatten(),
            NPDense(4 * 9 * 9, 1)
        ]
    def __call__(self, x):
        out = x
        for l in self.layers:
            out = l.forward(out)
        return out

def test_mlp_tri_framework_parity():
    np.random.seed(42)
    torch.manual_seed(42)
    
    in_features = 10
    x_np = np.random.randn(8, in_features).astype(np.float32)
    x_pt = torch.from_numpy(x_np)
    
    # Models
    np_model = NPMLP(in_features)
    pt_model = PTMLP(in_features)
    keras_model = build_keras_mlp(in_features)
    
    # Synchronize weights
    sync_mlp_weights(np_model, pt_model, keras_model)
    
    # Forward passes
    out_np = np_model(x_np)
    with torch.no_grad():
        out_pt = pt_model(x_pt).detach().cpu().numpy()
        k_out = keras_model(x_pt)
        if hasattr(k_out, 'detach'):
            out_keras = k_out.detach().cpu().numpy()
        else:
            out_keras = np.array(k_out)
    
    diff_pt = np.max(np.abs(out_np - out_pt))
    diff_keras = np.max(np.abs(out_np - out_keras))
    
    print(f"MLP Max Discrepancy: |NumPy - PyTorch| = {diff_pt:.2e}, |NumPy - Keras| = {diff_keras:.2e}")
    assert diff_pt < 1e-6, f"PyTorch MLP parity failed: {diff_pt}"
    assert diff_keras < 1e-6, f"Keras MLP parity failed: {diff_keras}"

def test_cnn4_tri_framework_parity():
    np.random.seed(42)
    torch.manual_seed(42)
    
    x_np = np.random.randn(4, 1, 20, 20).astype(np.float32)
    x_pt = torch.from_numpy(x_np)
    
    np_model = NPCNN4()
    pt_model = PTCNN4()
    keras_model = build_keras_cnn4()
    
    sync_cnn4_weights(np_model, pt_model, keras_model)
    
    out_np = np_model(x_np)
    with torch.no_grad():
        out_pt = pt_model(x_pt).detach().cpu().numpy()
        k_out = keras_model(x_pt)
        if hasattr(k_out, 'detach'):
            out_keras = k_out.detach().cpu().numpy()
        else:
            out_keras = np.array(k_out)
    
    diff_pt = np.max(np.abs(out_np - out_pt))
    diff_keras = np.max(np.abs(out_np - out_keras))
    
    print(f"CNN4 Max Discrepancy: |NumPy - PyTorch| = {diff_pt:.2e}, |NumPy - Keras| = {diff_keras:.2e}")
    assert diff_pt < 1e-5, f"PyTorch CNN4 parity failed: {diff_pt}"
    assert diff_keras < 1e-5, f"Keras CNN4 parity failed: {diff_keras}"

if __name__ == '__main__':
    print("Running Tri-Framework Parity Tests...")
    test_mlp_tri_framework_parity()
    test_cnn4_tri_framework_parity()
    print("ALL Tri-Framework Parity Tests PASSED successfully!")
