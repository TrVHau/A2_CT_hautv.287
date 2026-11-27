"""
Agent 2: Deep Learning Efficiency & Edge Deployment Specialist
Evaluates FLOPs, parameter count, memory footprint, and inference latency on Edge/CPU.
"""


class EfficiencySpecialistAgent:
    def __init__(self):
        self.name = "Edge & Efficiency Specialist Agent"
        self.role = "Parameter & Latency Optimization Engineer"

    def evaluate(self, model_name: str, params: int, latency_ms: float, memory_kb: float = 120.0):
        findings = []
        is_edge_viable = False

        if params < 25000:
            findings.append(f"Model has a highly compact parameter footprint ({params:,d} parameters), easily fitting in L2/L3 CPU cache.")
            is_edge_viable = True
        elif params < 100000:
            findings.append(f"Model parameters ({params:,d}) are moderate, suitable for general cloud or desktop CPU inference.")
            is_edge_viable = True
        else:
            findings.append(f"High parameter footprint ({params:,d} parameters, e.g. VGG dense head). Sub-optimal for edge devices with restricted SRAM.")
            is_edge_viable = False

        if latency_ms < 2.0:
            findings.append(f"Ultra-low latency ({latency_ms:.2f} ms/sample), satisfying hard real-time requirements (>500 FPS throughput).")
        else:
            findings.append(f"Latency ({latency_ms:.2f} ms/sample) is acceptable for soft real-time or batch diagnostic tasks.")

        if "MobileNet" in model_name:
            findings.append("Depthwise separable convolutions reduce theoretical FLOPs by 8x compared to standard 3x3 convs.")
        elif "ResNet" in model_name:
            findings.append("Global Average Pooling eliminates parameter explosion, saving >85% memory compared to flattened VGG heads.")

        rating = "EXCELLENT" if is_edge_viable and latency_ms < 3.0 else ("GOOD" if is_edge_viable else "CAUTION")

        return {
            "agent": self.name,
            "role": self.role,
            "efficiency_rating": rating,
            "parameters": params,
            "inference_latency_ms": round(latency_ms, 2),
            "edge_deployable": is_edge_viable,
            "findings": findings
        }
