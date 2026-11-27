"""
Grad-CAM (Gradient-Weighted Class Activation Mapping) & Visual Feature Heatmap Generator
Provides explainable AI (XAI) visual attributions for Conv2D models.
"""

import numpy as np
import torch
import torch.nn.functional as F


class GradCAM:
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        
        # Register hooks
        self.target_layer.register_forward_hook(self._forward_hook)
        self.target_layer.register_full_backward_hook(self._backward_hook)

    def _forward_hook(self, module, input, output):
        self.activations = output.detach()

    def _backward_hook(self, module, grad_input, grad_output):
        self.gradients = grad_output[0].detach()

    def generate_heatmap(self, input_tensor, target_class=None):
        self.model.eval()
        self.model.zero_grad()
        
        # Forward pass
        output = self.model(input_tensor)
        
        if target_class is None:
            target_class = torch.argmax(output, dim=1).item()
            
        score = output[0, target_class]
        score.backward()
        
        # Global average pooling over gradients -> neuron importance weights
        weights = torch.mean(self.gradients, dim=(2, 3), keepdim=True)  # [1, C, 1, 1]
        
        # Linear combination of forward activation maps
        cam = torch.sum(weights * self.activations, dim=1, keepdim=True)  # [1, 1, H, W]
        cam = F.relu(cam)
        
        # Normalize between 0 and 1
        cam_np = cam.squeeze().cpu().numpy()
        cam_min, cam_max = np.min(cam_np), np.max(cam_np)
        if cam_max > cam_min:
            cam_np = (cam_np - cam_min) / (cam_max - cam_min)
        else:
            cam_np = np.zeros_like(cam_np)
            
        return cam_np, target_class, output.detach().squeeze().cpu().numpy()


def generate_synthetic_cam_overlay(image_28x28: np.ndarray, heatmap: np.ndarray):
    """Resizes heatmap to 28x28 and generates overlay matrix"""
    from scipy.ndimage import zoom
    zoom_factors = (28.0 / heatmap.shape[0], 28.0 / heatmap.shape[1])
    cam_resized = zoom(heatmap, zoom_factors, order=1)
    cam_resized = np.clip(cam_resized, 0.0, 1.0)
    
    # Create RGB heatmap overlay (Jet-like color map)
    overlay = np.zeros((28, 28, 3), dtype=np.float32)
    # Red for high activation, blue for low
    overlay[:, :, 0] = cam_resized  # Red
    overlay[:, :, 1] = 1.0 - np.abs(cam_resized - 0.5) * 2.0  # Green
    overlay[:, :, 2] = 1.0 - cam_resized  # Blue
    
    # Blend with original grayscale image
    img_expanded = np.repeat(np.expand_dims(image_28x28, axis=-1), 3, axis=-1)
    blended = 0.5 * img_expanded + 0.5 * overlay
    return np.clip(blended, 0.0, 1.0), cam_resized
