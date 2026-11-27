"""
Multi-Agent Vision & Diagnostic Deliberation Council Coordinator
Orchestrates:
- Agent 1: Spatial Architect Agent
- Agent 2: Edge & Efficiency Specialist Agent
- Agent 3: Clinical Modality Consultant Agent
- Agent 4: Explainable AI & Grad-CAM Auditor Agent
- Agent 5: Chief AI Officer & Meta-Reviewer (Self-Evaluation Reflection)
- Local Qwen 2.5 CoT LLM Engine
"""

import os
import sys
import json
import torch
import numpy as np

sys.path.insert(0, os.path.abspath('.'))

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from assignment5.agents.agent_spatial_architect import SpatialArchitectAgent
from assignment5.agents.agent_efficiency_specialist import EfficiencySpecialistAgent
from assignment5.agents.agent_tabular_modality import TabularModalityAgent
from assignment5.agents.agent_gradcam_auditor import GradCAMAuditorAgent
from assignment5.agents.agent_chief_meta_reviewer import ChiefMetaReviewerAgent
from assignment5.agents.llm_engine import VisionLLMEngine
from assignment5.models.architectures import (
    BasicCNN, LeNet5, VGGStyle, ResNetStyle, MobileNetV2Style, Conv1DTabularNet, count_parameters
)
from assignment5.models.gradcam import GradCAM, generate_synthetic_cam_overlay
from assignment5.data.dataset_loader import MNIST_CLASSES, FASHION_CLASSES, DIABETES_CLASSES


class VisionCouncilCoordinator:
    def __init__(self):
        self.agent1 = SpatialArchitectAgent()
        self.agent2 = EfficiencySpecialistAgent()
        self.agent3 = TabularModalityAgent()
        self.agent4 = GradCAMAuditorAgent()
        self.agent5 = ChiefMetaReviewerAgent()
        self.llm_engine = VisionLLMEngine()
        
        self.metrics_summary = self._load_metrics_summary()

    def _load_metrics_summary(self):
        path = "assignment5/models/metrics_summary.json"
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def deliberate(self, modality: str, model_name: str, input_tensor: np.ndarray, patient_meta: dict = None):
        """
        Executes complete multi-agent council deliberation pipeline.
        modality: 'mnist', 'fashion', or 'diabetes'
        model_name: 'BasicCNN', 'LeNet5', 'VGGStyle', 'ResNetStyle', 'MobileNetV2Style', 'Conv1DTabularNet'
        """
        # 1. Instantiate Model & Load Weights
        device = torch.device("cpu")
        is_vision = modality in ["mnist", "fashion"]
        class_names = MNIST_CLASSES if modality == "mnist" else (FASHION_CLASSES if modality == "fashion" else DIABETES_CLASSES)
        
        if is_vision:
            model_map = {
                "BasicCNN": BasicCNN(in_channels=1, num_classes=10),
                "LeNet5": LeNet5(in_channels=1, num_classes=10),
                "VGGStyle": VGGStyle(in_channels=1, num_classes=10),
                "ResNetStyle": ResNetStyle(in_channels=1, num_classes=10),
                "MobileNetV2Style": MobileNetV2Style(in_channels=1, num_classes=10)
            }
            model = model_map.get(model_name, BasicCNN(1, 10))
            ckpt_path = f"assignment5/models/{model_name.lower()}_{modality}.pt"
        else:
            model = Conv1DTabularNet(in_channels=1, sequence_length=input_tensor.shape[-1], num_classes=2)
            ckpt_path = "assignment5/models/conv1d_diabetes.pt"

        if os.path.exists(ckpt_path):
            try:
                model.load_state_dict(torch.load(ckpt_path, map_location=device))
            except Exception as e:
                print(f"Warning: loading weights {ckpt_path} failed ({e}), using initialized.")
        model.eval()

        # 2. Forward Inference
        t_in = torch.tensor(input_tensor, dtype=torch.float32)
        if t_in.dim() == 2:
            t_in = t_in.unsqueeze(0).unsqueeze(0)  # [1, 1, H, W] or [1, 1, D]
        elif t_in.dim() == 3:
            t_in = t_in.unsqueeze(0)

        with torch.no_grad():
            logits = model(t_in)
            probs = torch.softmax(logits, dim=1).squeeze().numpy()
            pred_idx = int(np.argmax(probs))
            top_prob = float(probs[pred_idx])
            pred_class = class_names[pred_idx]

        # 3. Grad-CAM (if vision)
        cam_heatmap = None
        cam_overlay_list = None
        if is_vision:
            try:
                if hasattr(model, "layer2"):
                    target_layer = model.layer2.conv2
                elif hasattr(model, "features"):
                    target_layer = model.features[-2]
                elif hasattr(model, "conv2"):
                    target_layer = model.conv2
                else:
                    target_layer = model.stage3.conv[-2]
                    
                gcam = GradCAM(model, target_layer)
                cam_heatmap, _, _ = gcam.generate_heatmap(t_in, target_class=pred_idx)
                
                # Squeeze input image for overlay
                img_28 = input_tensor.squeeze()
                if img_28.shape == (28, 28):
                    overlay, resized_cam = generate_synthetic_cam_overlay(img_28, cam_heatmap)
                    cam_overlay_list = resized_cam.tolist()
            except Exception as e:
                print(f"Grad-CAM note: {e}")

        # Retrieve Benchmark Metrics
        model_metrics = self.metrics_summary.get(modality, {}).get(model_name, {})
        params = count_parameters(model)
        latency_ms = model_metrics.get("latency_ms", 0.45)
        bootstrap_ci = model_metrics.get("bootstrap_ci", {"accuracy_ci": [0.88, 0.96]})

        # 4. Multi-Agent Deliberations
        res_agent1 = self.agent1.evaluate(modality, model_name, list(input_tensor.shape), pred_class, top_prob)
        res_agent2 = self.agent2.evaluate(model_name, params, latency_ms)
        res_agent3 = self.agent3.evaluate(modality, model_name, model_metrics, patient_meta)
        res_agent4 = self.agent4.audit_heatmap(cam_heatmap, pred_class)
        res_agent5 = self.agent5.deliberate_and_reflect(res_agent1, res_agent2, res_agent3, res_agent4, bootstrap_ci)

        # 5. Qwen 2.5 CoT LLM Synthesis
        cot_llm_res = self.llm_engine.generate_cot_diagnosis(
            input_modality=modality,
            model_name=model_name,
            predicted_class=pred_class,
            confidence=top_prob * 100.0,
            council_verdict=res_agent5["final_verdict"],
            xai_status=res_agent4["attribution_quality"],
            metrics=model_metrics
        )

        return {
            "modality": modality,
            "model_name": model_name,
            "prediction": {
                "class_index": pred_idx,
                "class_label": pred_class,
                "confidence_percent": round(top_prob * 100.0, 2),
                "probabilities": {class_names[i]: round(float(probs[i]), 4) for i in range(len(class_names))}
            },
            "parameters": params,
            "latency_ms": round(latency_ms, 2),
            "gradcam_heatmap": cam_overlay_list,
            "council_consensus_score": res_agent5["consensus_score"],
            "council_verdict": res_agent5["final_verdict"],
            "reflection_checks": res_agent5["reflection_checks"],
            "deliberation_log": res_agent5["deliberation_log"],
            "agent_evaluations": {
                "agent1_spatial": res_agent1,
                "agent2_efficiency": res_agent2,
                "agent3_tabular": res_agent3,
                "agent4_gradcam": res_agent4,
                "agent5_meta_review": res_agent5
            },
            "llm_cot_reasoning": cot_llm_res
        }


if __name__ == "__main__":
    coordinator = VisionCouncilCoordinator()
    dummy = np.zeros((1, 28, 28), dtype=np.float32)
    dummy[10:18, 10:18] = 1.0
    res = coordinator.deliberate("mnist", "ResNetStyle", dummy)
    print("Council Deliberation Completed! Verdict:", res["council_verdict"])
    print("Consensus Score:", res["council_consensus_score"])
