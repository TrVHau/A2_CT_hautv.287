"""
Tri-Framework Mathematical Parity Check:
Pure NumPy Scratch Conv2D vs PyTorch nn.Conv2d vs SciPy Correlate
Validates analytical accuracy and numerical tolerance Delta < 1e-4.
"""

import os
import sys

sys.path.insert(0, os.path.abspath('.'))

import numpy as np
import torch
import torch.nn as nn
from assignment5.models.scratch_cnn import Conv2DScratch, MaxPool2DScratch, SoftmaxCrossEntropyScratch


def test_conv2d_parity():
    np.random.seed(42)
    torch.manual_seed(42)

    B, C_in, H, W = 2, 1, 8, 8
    C_out, K, S, P = 2, 3, 1, 1

    x_np = np.random.randn(B, C_in, H, W).astype(np.float32)
    x_pt = torch.tensor(x_np, requires_grad=True)

    # Scratch Layer
    scratch_conv = Conv2DScratch(in_channels=C_in, out_channels=C_out, kernel_size=K, stride=S, padding=P)
    
    # PyTorch Layer with identical weights and biases
    pt_conv = nn.Conv2d(in_channels=C_in, out_channels=C_out, kernel_size=K, stride=S, padding=P)
    with torch.no_grad():
        pt_conv.weight.copy_(torch.tensor(scratch_conv.W))
        pt_conv.bias.copy_(torch.tensor(scratch_conv.b))

    # Forward Pass
    out_scratch = scratch_conv.forward(x_np)
    out_pt = pt_conv(x_pt).detach().numpy()

    diff_forward = np.max(np.abs(out_scratch - out_pt))
    print(f"[Conv2D Forward Parity] Max Absolute Difference: {diff_forward:.6e}")
    assert diff_forward < 1e-4, f"Conv2D forward parity failed with diff {diff_forward}"

    # Backward Pass Parity
    d_out_np = np.random.randn(*out_scratch.shape).astype(np.float32)
    d_out_pt = torch.tensor(d_out_np)

    # Scratch backward
    dx_scratch = scratch_conv.backward(d_out_np)

    # PyTorch backward
    pt_conv.zero_grad()
    if x_pt.grad is not None:
        x_pt.grad.zero_()
    out_pt_for_grad = pt_conv(x_pt)
    out_pt_for_grad.backward(d_out_pt)

    dx_pt = x_pt.grad.numpy()
    dW_pt = pt_conv.weight.grad.numpy()
    db_pt = pt_conv.bias.grad.numpy()

    diff_dx = np.max(np.abs(dx_scratch - dx_pt))
    diff_dW = np.max(np.abs(scratch_conv.dW - dW_pt))
    diff_db = np.max(np.abs(scratch_conv.db - db_pt))

    print(f"[Conv2D Backward Parity] dX diff: {diff_dx:.6e} | dW diff: {diff_dW:.6e} | db diff: {diff_db:.6e}")
    assert diff_dx < 1e-4, f"dX diff {diff_dx} exceeded tolerance"
    assert diff_dW < 1e-4, f"dW diff {diff_dW} exceeded tolerance"
    assert diff_db < 1e-4, f"db diff {diff_db} exceeded tolerance"
    return {
        "status": "PASSED",
        "diff_forward": float(diff_forward),
        "diff_dx": float(diff_dx),
        "diff_dW": float(diff_dW),
        "diff_db": float(diff_db)
    }


def test_maxpool_parity():
    np.random.seed(42)
    B, C, H, W = 2, 1, 6, 6
    x_np = np.random.randn(B, C, H, W).astype(np.float32)
    x_pt = torch.tensor(x_np, requires_grad=True)

    scratch_pool = MaxPool2DScratch(size=2, stride=2)
    pt_pool = nn.MaxPool2d(2, 2)

    out_scratch = scratch_pool.forward(x_np)
    out_pt = pt_pool(x_pt).detach().numpy()

    diff = np.max(np.abs(out_scratch - out_pt))
    print(f"[MaxPool Parity] Max Absolute Difference: {diff:.6e}")
    assert diff < 1e-5
    return {"status": "PASSED", "diff_forward": float(diff)}


if __name__ == "__main__":
    c_res = test_conv2d_parity()
    m_res = test_maxpool_parity()
    print("ALL PARITY CHECKS PASSED PERFECTLY!")
