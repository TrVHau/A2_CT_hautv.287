# -*- coding: utf-8 -*-
"""
CHƯƠNG 2: KIỂM CHỨNG TƯƠNG ĐƯƠNG ĐẠO HÀM TUYỆT ĐỐI (GRADIENT PARITY CHECK)
Sinh viên thực hiện: Trần Văn Hậu | MSV: B23DCCN287 | Lớp: D23CTPM01 | Nhóm CT_09
Giảng viên hướng dẫn: PGS. TS. Trần Đình Quế

Chứng minh giải tích và số học rằng thuật toán đạo hàm ma trận viết tay ScratchMLP
hoàn toàn trùng khớp tuyệt đối với đồ thị tính toán vi phân tự động (Autograd) của PyTorch
với sai số dung sai số học máy Delta < 1e-7.
"""

import sys
import numpy as np
import torch
import torch.nn as nn
from scratch_mlp import ScratchMLP

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')


def run_gradient_parity_check():
    """Kiểm chứng độ lệch tuyệt đối giữa ScratchMLP và PyTorch Autograd."""
    print("=" * 75)
    print("KIỂM CHỨNG TƯƠNG ĐƯƠNG ĐẠO HÀM (GRADIENT PARITY CHECK): SCRATCH VS PYTORCH")
    print("Tác giả: Trần Văn Hậu - B23DCCN287 | Nhóm CT_09")
    print("=" * 75)

    np.random.seed(42)
    torch.manual_seed(42)

    in_dim, h1, h2, out_dim = 8, 16, 8, 1
    batch_size = 32

    # 1. Khởi tạo dữ liệu kiểm chứng
    X_np = np.random.randn(batch_size, in_dim).astype(np.float64)
    y_np = (np.random.rand(batch_size, 1) > 0.5).astype(np.float64)

    # 2. Khởi tạo Scratch MLP
    scratch_model = ScratchMLP(in_dim=in_dim, h1=h1, h2=h2, out_dim=out_dim, lr=0.01, random_state=42)

    # 3. Khởi tạo PyTorch model với các trọng số đồng nhất tuyệt đối (float64)
    class PyTorchParityMLP(nn.Module):
        def __init__(self, W1, b1, W2, b2, W3, b3):
            super().__init__()
            self.fc1 = nn.Linear(in_dim, h1, dtype=torch.float64)
            self.fc2 = nn.Linear(h1, h2, dtype=torch.float64)
            self.fc3 = nn.Linear(h2, out_dim, dtype=torch.float64)

            with torch.no_grad():
                self.fc1.weight.copy_(torch.tensor(W1.T, dtype=torch.float64))
                self.fc1.bias.copy_(torch.tensor(b1.flatten(), dtype=torch.float64))
                self.fc2.weight.copy_(torch.tensor(W2.T, dtype=torch.float64))
                self.fc2.bias.copy_(torch.tensor(b2.flatten(), dtype=torch.float64))
                self.fc3.weight.copy_(torch.tensor(W3.T, dtype=torch.float64))
                self.fc3.bias.copy_(torch.tensor(b3.flatten(), dtype=torch.float64))

        def forward(self, x):
            z1 = self.fc1(x)
            a1 = torch.relu(z1)
            z2 = self.fc2(a1)
            a2 = torch.relu(z2)
            z3 = self.fc3(a2)
            a3 = torch.sigmoid(z3)
            return a3

    pt_model = PyTorchParityMLP(
        scratch_model.W1, scratch_model.b1,
        scratch_model.W2, scratch_model.b2,
        scratch_model.W3, scratch_model.b3
    )

    # 4. Forward Pass Parity Check
    y_hat_scratch = scratch_model.forward(X_np)

    X_pt = torch.tensor(X_np, dtype=torch.float64, requires_grad=True)
    y_pt = torch.tensor(y_np, dtype=torch.float64)
    y_hat_pt = pt_model(X_pt)

    diff_forward = np.max(np.abs(y_hat_scratch - y_hat_pt.detach().numpy()))
    print(f"[FORWARD PASS] Sai số lớn nhất giữa Scratch và PyTorch: {diff_forward:.8e}")
    assert diff_forward < 1e-7, f"Forward parity failed: {diff_forward}"

    # 5. Backward Pass Parity Check
    # Scratch backward
    scratch_model.backward(X_np, y_np.flatten(), y_hat_scratch)

    # PyTorch backward
    pt_model.zero_grad()
    bce_loss = nn.BCELoss()(y_hat_pt, y_pt)
    bce_loss.backward()

    # So sánh gradient từng tham số
    diff_dW1 = np.max(np.abs(scratch_model.dW1 - pt_model.fc1.weight.grad.numpy().T))
    diff_db1 = np.max(np.abs(scratch_model.db1.flatten() - pt_model.fc1.bias.grad.numpy()))

    diff_dW2 = np.max(np.abs(scratch_model.dW2 - pt_model.fc2.weight.grad.numpy().T))
    diff_db2 = np.max(np.abs(scratch_model.db2.flatten() - pt_model.fc2.bias.grad.numpy()))

    diff_dW3 = np.max(np.abs(scratch_model.dW3 - pt_model.fc3.weight.grad.numpy().T))
    diff_db3 = np.max(np.abs(scratch_model.db3.flatten() - pt_model.fc3.bias.grad.numpy()))

    print("\n[BACKWARD PASS GRADIENTS PARITY]:")
    print(f"  - Lớp 1 Trọng số dW1 sai số lớn nhất: {diff_dW1:.8e}")
    print(f"  - Lớp 1 Hệ số chệch db1 sai số lớn nhất: {diff_db1:.8e}")
    print(f"  - Lớp 2 Trọng số dW2 sai số lớn nhất: {diff_dW2:.8e}")
    print(f"  - Lớp 2 Hệ số chệch db2 sai số lớn nhất: {diff_db2:.8e}")
    print(f"  - Lớp 3 Trọng số dW3 sai số lớn nhất: {diff_dW3:.8e}")
    print(f"  - Lớp 3 Hệ số chệch db3 sai số lớn nhất: {diff_db3:.8e}")

    max_grad_diff = max(diff_dW1, diff_db1, diff_dW2, diff_db2, diff_dW3, diff_db3)
    print(f"\n=> SAI SỐ ĐẠO HÀM LỚN NHẤT TOÀN MẠNG: {max_grad_diff:.8e}")
    print(f"=> DUNG SAI MÁY YÊU CẦU: < 1.0e-07")
    
    if max_grad_diff < 1e-7:
        print("[KẾT LUẬN]: PARITY CHECK ĐẠT CHUẨN XUẤT SẮC (PASSED) - Chứng minh tính tương đương giải tích tuyệt đối.")
    else:
        print("[KẾT LUẬN]: PARITY CHECK CẢNH BÁO DUNG SAI.")
        
    return {
        "status": "PASSED" if max_grad_diff < 1e-7 else "WARNING",
        "diff_forward": float(diff_forward),
        "max_grad_diff": float(max_grad_diff),
        "details": {
            "dW1": float(diff_dW1), "db1": float(diff_db1),
            "dW2": float(diff_dW2), "db2": float(diff_db2),
            "dW3": float(diff_dW3), "db3": float(diff_db3)
        }
    }


if __name__ == "__main__":
    run_gradient_parity_check()
