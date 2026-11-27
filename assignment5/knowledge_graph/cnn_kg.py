"""
Convolutional Neural Networks & Deep Vision Architecture Knowledge Graph (CNN-KG)
Formal NetworkX Ontology with nodes, directed edges, attributes, and query engine.
"""

import json
import os
import sys
import networkx as nx

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def build_cnn_knowledge_graph() -> nx.DiGraph:
    G = nx.DiGraph()

    nodes = [
        # Paradigms
        ("Spatial_Inductive_Bias", {"category": "Paradigm", "label": "Spatial Inductive Bias", "desc": "Assumption that nearby pixels have higher spatial correlation than distant pixels."}),
        ("Weight_Sharing", {"category": "Paradigm", "label": "Weight Sharing (Tied Weights)", "desc": "Reusing identical kernel weights across spatial positions to achieve translational equivariance."}),
        ("Local_Receptive_Field", {"category": "Paradigm", "label": "Local Receptive Field", "desc": "Spatial region in the input tensor that influences a specific feature map activation."}),
        ("Equivariance_Translation", {"category": "Paradigm", "label": "Translational Equivariance", "desc": "f(g(x)) = g(f(x)): Shifting an object in the input shifts its representation correspondingly."}),
        ("Vanishing_Gradients", {"category": "Phenomenon", "label": "Vanishing Gradient Problem", "desc": "Exponential decay of backpropagated gradients in deep multi-layered architectures."}),
        ("Inductive_Mismatch_Tabular", {"category": "Phenomenon", "label": "Tabular Inductive Mismatch", "desc": "Disadvantage of Conv1D on arbitrary feature-ordered heterogeneous tabular columns."}),

        # Layers / Primitives
        ("Conv2D_Layer", {"category": "Layer", "label": "2D Convolutional Layer", "desc": "Discretized 2D cross-correlation operator with trainable kernel tensors."}),
        ("Conv1D_Layer", {"category": "Layer", "label": "1D Convolutional Layer", "desc": "1D sliding filter across temporal or sequence-ordered vector dimensions."}),
        ("Depthwise_Separable_Conv", {"category": "Layer", "label": "Depthwise Separable Conv", "desc": "Factorization into depthwise spatial convolution followed by 1x1 pointwise channel projection."}),
        ("Residual_Connection", {"category": "Layer", "label": "Residual Skip Connection", "desc": "Identity shortcut y = F(x) + x allowing pristine gradient backpropagation."}),
        ("Batch_Normalization", {"category": "Layer", "label": "Batch Normalization (BN)", "desc": "Stabilizes internal covariate shift by normalizing layer activations across mini-batches."}),
        ("Max_Pooling", {"category": "Layer", "label": "Max Pooling", "desc": "Non-linear downsampling selecting the maximum element in local windows."}),
        ("Average_Pooling", {"category": "Layer", "label": "Average Pooling", "desc": "Spatial aggregation computing local arithmetic mean across receptive windows."}),
        ("Global_Average_Pooling", {"category": "Layer", "label": "Global Average Pooling (GAP)", "desc": "Averages each spatial feature map into a single scalar, drastically eliminating dense parameters."}),
        ("Dropout", {"category": "Layer", "label": "Dropout Regularization", "desc": "Stochastic deactivation of neurons during training to prevent co-adaptation."}),

        # Architectures
        ("Basic_CNN", {"category": "Architecture", "label": "Basic Baseline CNN", "desc": "Canonical 2-stage Conv2D + MaxPool + Dense baseline network."}),
        ("LeNet5", {"category": "Architecture", "label": "LeNet-5 (LeCun 1998)", "desc": "Foundational architecture utilizing 5x5 kernels and progressive sub-sampling."}),
        ("VGG16", {"category": "Architecture", "label": "VGG-Style (Simonyan 2014)", "desc": "Deep stacked 3x3 convolutions with homogeneous blocks and Batch Normalization."}),
        ("ResNet18", {"category": "Architecture", "label": "ResNet-Style (He 2015)", "desc": "Deep residual network with identity shortcuts solving degradation across deep layers."}),
        ("MobileNetV2", {"category": "Architecture", "label": "MobileNetV2 (Sandler 2018)", "desc": "Lightweight architecture with inverted residuals and linear bottlenecks for edge computing."}),
        ("Conv1D_Tabular_Net", {"category": "Architecture", "label": "Conv1D Tabular Clinical Net", "desc": "1D convolutional network adapted for clinical biomarker risk stratification."}),
        ("NumPy_Scratch_CNN", {"category": "Architecture", "label": "NumPy Pure Scratch CNN", "desc": "Explicit forward and backward algorithmic implementation without PyTorch/Autograd."}),

        # Evaluation & Explainability
        ("CrossEntropyLoss", {"category": "Objective", "label": "Categorical Cross-Entropy Loss", "desc": "Log-loss quantifying discrepancy between ground-truth and predicted categorical probabilities."}),
        ("GradCAM_Saliency", {"category": "Explainability", "label": "Grad-CAM (Selvaraju 2017)", "desc": "Gradient-weighted Class Activation Mapping highlighting visual decision regions."}),
        ("Bootstrap_CI_95", {"category": "Metric", "label": "95% Bootstrap Confidence Intervals", "desc": "Non-parametric empirical confidence estimation via B=1000 resamples."}),
        ("Confusion_Matrix", {"category": "Metric", "label": "Multi-class Confusion Matrix", "desc": "Contingency matrix evaluating class-specific true positives, false positives, and errors."}),
        ("Macro_F1_Score", {"category": "Metric", "label": "Macro-Averaged F1-Score", "desc": "Unweighted mean of class F1 scores, crucial for evaluating imbalanced distributions."})
    ]

    for node_id, attrs in nodes:
        G.add_node(node_id, **attrs)

    edges = [
        ("Spatial_Inductive_Bias", "Conv2D_Layer", {"relation": "justifies", "desc": "Local pixel correlation motivates small spatial convolution kernels"}),
        ("Weight_Sharing", "Conv2D_Layer", {"relation": "implements", "desc": "Convolution applies identical weights across the entire tensor plane"}),
        ("Weight_Sharing", "Equivariance_Translation", {"relation": "induces", "desc": "Shared kernels guarantee translational equivariance"}),
        ("Local_Receptive_Field", "Conv2D_Layer", {"relation": "governed_by", "desc": "Kernel size and dilation dictate the effective receptive field"}),
        ("Vanishing_Gradients", "Residual_Connection", {"relation": "mitigated_by", "desc": "Skip connections allow identity gradient flow d(x+F(x))/dx = 1 + F'(x)"}),
        ("Vanishing_Gradients", "Batch_Normalization", {"relation": "stabilized_by", "desc": "BatchNorm centers variance preventing exploding/vanishing saturations"}),
        
        ("Conv2D_Layer", "Basic_CNN", {"relation": "component_of", "desc": "Core feature extraction layer in Basic baseline"}),
        ("Conv2D_Layer", "LeNet5", {"relation": "component_of", "desc": "5x5 convolution filters in LeNet"}),
        ("Conv2D_Layer", "VGG16", {"relation": "component_of", "desc": "Consecutive 3x3 conv stages in VGG"}),
        ("Depthwise_Separable_Conv", "MobileNetV2", {"relation": "component_of", "desc": "Core efficiency block in MobileNetV2"}),
        ("Residual_Connection", "ResNet18", {"relation": "core_mechanism", "desc": "Fundamental identity mapping block of ResNet"}),
        ("Global_Average_Pooling", "ResNet18", {"relation": "replaces_dense", "desc": "Eliminates millions of dense parameters before classification head"}),
        ("Batch_Normalization", "VGG16", {"relation": "accelerates", "desc": "Standardizes activations across deep 3x3 layers"}),
        ("Batch_Normalization", "ResNet18", {"relation": "standardizes", "desc": "Applied after each conv layer prior to activation addition"}),
        ("Dropout", "VGG16", {"relation": "regularizes", "desc": "Mitigates co-adaptation in dense classification heads"}),

        ("Conv1D_Layer", "Conv1D_Tabular_Net", {"relation": "component_of", "desc": "Slides 1D kernels across clinical feature vectors"}),
        ("Inductive_Mismatch_Tabular", "Conv1D_Tabular_Net", {"relation": "challenges", "desc": "Feature permutation sensitivity degrades inductive bias on tabular data"}),

        ("NumPy_Scratch_CNN", "Conv2D_Layer", {"relation": "verifies_parity", "desc": "Validates exact im2col/sliding-window mathematical parity"}),
        ("NumPy_Scratch_CNN", "CrossEntropyLoss", {"relation": "computes_exact_gradient", "desc": "Analytical backward softmax gradient dL/dz = p - y"}),

        ("ResNet18", "GradCAM_Saliency", {"relation": "interpreted_by", "desc": "Grad-CAM generates attention heatmaps at layer4 residual blocks"}),
        ("VGG16", "GradCAM_Saliency", {"relation": "interpreted_by", "desc": "Grad-CAM computes gradients relative to final conv feature map"}),

        ("Basic_CNN", "Confusion_Matrix", {"relation": "evaluated_by", "desc": "Assesses digit and garment classification accuracy"}),
        ("ResNet18", "Bootstrap_CI_95", {"relation": "statistically_validated", "desc": "Quantifies empirical bounds of test metrics"}),
        ("Conv1D_Tabular_Net", "Macro_F1_Score", {"relation": "primary_benchmark", "desc": "Evaluates clinical triage under extreme 86:14 class imbalance"})
    ]

    for src, dst, attrs in edges:
        G.add_edge(src, dst, **attrs)

    return G


def export_kg_to_json(G: nx.DiGraph, output_path: str):
    data = {
        "nodes": [{"id": n, **G.nodes[n]} for n in G.nodes],
        "edges": [{"source": u, "target": v, **G.edges[u, v]} for u, v in G.edges]
    }
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Exported Knowledge Graph: {len(G.nodes)} nodes, {len(G.edges)} edges to {output_path}")
    return data


def query_kg_neighbors(G: nx.DiGraph, node_id: str):
    if node_id not in G:
        return {"error": f"Node {node_id} not found in Knowledge Graph."}
    successors = [{"target": s, "relation": G.edges[node_id, s].get("relation"), "desc": G.edges[node_id, s].get("desc")} for s in G.successors(node_id)]
    predecessors = [{"source": p, "relation": G.edges[p, node_id].get("relation"), "desc": G.edges[p, node_id].get("desc")} for p in G.predecessors(node_id)]
    return {
        "node": node_id,
        "attributes": G.nodes[node_id],
        "outgoing_relations": successors,
        "incoming_relations": predecessors
    }


if __name__ == "__main__":
    kg = build_cnn_knowledge_graph()
    export_kg_to_json(kg, "assignment5/knowledge_graph/cnn_kg.json")
    print("Sample Query: ResNet18 neighbors ->", query_kg_neighbors(kg, "ResNet18"))
