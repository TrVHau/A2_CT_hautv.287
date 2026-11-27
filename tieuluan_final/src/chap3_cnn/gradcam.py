# -*- coding: utf-8 -*-
"""
CHƯƠNG 3: TRỰC QUAN HÓA GIẢI THÍCH MÔ HÌNH BẰNG GRAD-CAM
Sinh viên thực hiện: Trần Văn Hậu | MSV: B23DCCN287 | Lớp: D23CTPM01 | Nhóm CT_09
Giảng viên hướng dẫn: PGS. TS. Trần Đình Quế

Hiện thực hóa thuật toán Grad-CAM (Gradient-weighted Class Activation Mapping):
  1. alpha_k^c = (1 / Z) * sum_i sum_j (d y^c / d A_{i,j}^k)
  2. L_{Grad-CAM}^c = ReLU( sum_k alpha_k^c * A^k )
  3. Chuẩn hóa Min-Max và nội suy song tuyến (Bilinear Interpolation) về kích thước gốc
"""

import sys
import numpy as np
import torch
import torch.nn.functional as F
from pytorch_cnn import MedicalCNN

sys.stdout.reconfigure(encoding='utf-8')


class GradCAM:
    """Bộ giải thích Grad-CAM độc lập cho mạng nơ-ron tích chập."""
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None

        # Đăng ký Hooks
        self.target_layer.register_forward_hook(self._save_activation)
        self.target_layer.register_full_backward_hook(self._save_gradient)

    def _save_activation(self, module, input, output):
        self.activations = output.detach()

    def _save_gradient(self, module, grad_input, grad_output):
        self.gradients = grad_output[0].detach()

    def generate_heatmap(self, input_tensor, target_class=None):
        """Tạo bản đồ nhiệt Grad-CAM kích thước tương thích với ảnh đầu vào."""
        self.model.eval()
        self.model.zero_grad()

        # Forward pass
        logits = self.model(input_tensor)
        if target_class is None:
            target_class = torch.argmax(logits, dim=1).item()

        score = logits[0, target_class]
        score.backward(retain_graph=True)

        # 1. Tính trọng số tầm quan trọng kênh: alpha_k^c = Global Average Pooling của đạo hàm
        # gradients: [1, C, H, W] -> alpha: [1, C, 1, 1]
        alpha = torch.mean(self.gradients, dim=(2, 3), keepdim=True)

        # 2. Tổ hợp tuyến tính có trọng số của các bản đồ đặc trưng: sum_k alpha_k^c * A^k
        cam = torch.sum(alpha * self.activations, dim=1, keepdim=True)

        # 3. Áp dụng ReLU để chỉ giữ lại các đặc trưng có tác động tích cực đến lớp dự đoán
        cam = F.relu(cam)

        # 4. Nội suy song tuyến tính phóng to bản đồ nhiệt về kích thước ban đầu của ảnh
        cam_upsampled = F.interpolate(
            cam, size=input_tensor.shape[2:], mode='bilinear', align_corners=False
        )

        # 5. Chuẩn hóa Min-Max về đoạn [0, 1]
        cam_np = cam_upsampled.squeeze().cpu().numpy()
        cam_min, cam_max = np.min(cam_np), np.max(cam_np)
        if cam_max > cam_min:
            cam_norm = (cam_np - cam_min) / (cam_max - cam_min)
        else:
            cam_norm = np.zeros_like(cam_np)

        return cam_norm, target_class


def test_gradcam_pipeline():
    print("=" * 70)
    print("THỰC NGHIỆM GIẢI THÍCH TRỰC QUAN HÓA GRAD-CAM TRÊN MEDICAL-CNN")
    print("Tác giả: Trần Văn Hậu - B23DCCN287 | Nhóm CT_09")
    print("=" * 70)

    model = MedicalCNN(in_channels=1, num_classes=2)
    target_layer = model.get_last_conv_layer()

    gradcam = GradCAM(model, target_layer)
    dummy_img = torch.randn(1, 1, 28, 28, requires_grad=True)

    heatmap, target_cls = gradcam.generate_heatmap(dummy_img, target_class=1)
    
    print(f"Lớp mục tiêu phân tích (Target Class): {target_cls}")
    print(f"Kích thước ma trận nhiệt (Heatmap Shape): {heatmap.shape}")
    print(f"Giá trị nhiệt min: {np.min(heatmap):.4f} | max: {np.max(heatmap):.4f}")
    assert heatmap.shape == (28, 28), f"Expected (28, 28), got {heatmap.shape}"
    print("Grad-CAM generation PASSED!")
    print("=" * 70)


if __name__ == "__main__":
    test_gradcam_pipeline()
