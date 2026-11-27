"""
Agent 4: Explainable AI & Grad-CAM Diagnostic Auditor
Audits Grad-CAM visual heatmaps, examines feature attribution, and detects Shortcut Learning.
"""

import numpy as np


class GradCAMAuditorAgent:
    def __init__(self):
        self.name = "Explainable AI & Grad-CAM Auditor Agent"
        self.role = "XAI Attention & Saliency Integrity Reviewer"

    def audit_heatmap(self, heatmap: np.ndarray, predicted_class: str, is_correct: bool = True):
        observations = []
        if heatmap is None:
            return {
                "agent": self.name,
                "role": self.role,
                "status": "No Heatmap Available",
                "observations": ["Heatmap generation bypassed or non-convolutional layer."]
            }

        # Calculate activation concentration in center vs periphery
        H, W = heatmap.shape
        center_mask = np.zeros((H, W), dtype=bool)
        center_mask[H//4 : 3*H//4, W//4 : 3*W//4] = True
        
        center_energy = np.sum(heatmap[center_mask])
        total_energy = np.sum(heatmap) + 1e-8
        center_ratio = float(center_energy / total_energy)

        if center_ratio > 0.60:
            observations.append(f"Strong focal saliency ({center_ratio*100:.1f}% energy concentrated in central anatomical/digit region).")
            observations.append("Model demonstrates genuine semantic attention rather than border artifact bias.")
            audit_pass = True
        else:
            observations.append(f"Diffused or peripheral attention ({center_ratio*100:.1f}% central energy).")
            observations.append("Potential shortcut learning or background texture reliance detected.")
            audit_pass = False

        return {
            "agent": self.name,
            "role": self.role,
            "audit_pass": audit_pass,
            "saliency_focus_ratio": round(center_ratio, 3),
            "attribution_quality": "HIGH INTEGRITY" if audit_pass else "DIFFUSE / ARTIFACT PRONE",
            "observations": observations
        }
