"""
Agent 1: Vision Architect & Spatial Feature Agent
Analyzes tensor spatial hierarchies, receptive fields, local vs global textures, and inductive biases.
"""

import numpy as np


class SpatialArchitectAgent:
    def __init__(self):
        self.name = "Vision Architect Agent"
        self.role = "Spatial Feature & Architectural Hierarchy Specialist"

    def evaluate(self, input_modality: str, model_name: str, input_shape: list, top_class: str, top_prob: float):
        reasoning = []
        if input_modality in ["mnist", "fashion"]:
            reasoning.append(f"Input is a 2D spatial grid {input_shape} with strong local translational covariance.")
            if "ResNet" in model_name:
                reasoning.append("ResNet residual skip connections preserve high-frequency spatial gradients, enabling deep semantic feature abstraction without vanishing gradients.")
            elif "VGG" in model_name:
                reasoning.append("VGG stacked 3x3 convolutions create an effective 7x7 receptive field with 45% fewer parameters than a single 7x7 kernel.")
            elif "MobileNet" in model_name:
                reasoning.append("MobileNetV2 inverted residuals decouple spatial filtering (depthwise 3x3) from cross-channel synthesis (pointwise 1x1).")
            elif "LeNet" in model_name:
                reasoning.append("LeNet-5 utilizes 5x5 receptive fields with average pooling; effective for simple handwritten digits, but suffers on complex garment textures.")
            else:
                reasoning.append("Baseline 2-stage CNN provides adequate local pattern matching with modest receptive field coverage.")
        else:
            reasoning.append(f"Input is a 1D tabular vector {input_shape}. 1D convolutions assume sequential adjacent correlation.")
            reasoning.append("Warning: Arbitrary column ordering in clinical tables weakens the spatial inductive bias assumption.")

        confidence = float(np.clip(top_prob * 100.0, 50.0, 99.0))
        recommendation = "Optimal Spatial Architecture" if "ResNet" in model_name or "MobileNet" in model_name else "Baseline Standard"

        return {
            "agent": self.name,
            "role": self.role,
            "confidence_score": round(confidence, 1),
            "verdict": recommendation,
            "reasoning": reasoning,
            "architectural_insights": {
                "spatial_inductive_bias": "STRONG" if input_modality != "diabetes" else "WEAK/MISMATCHED",
                "receptive_field_depth": "High (Level 4)" if "ResNet" in model_name or "VGG" in model_name else "Moderate (Level 2)"
            }
        }
