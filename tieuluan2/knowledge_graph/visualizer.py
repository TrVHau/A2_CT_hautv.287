"""
visualizer.py
Tạo cấu trúc dữ liệu và tọa độ layout 2D (Kamada-Kawai / Spring Layout)
cho giao diện mạng trực quan hóa Vis.js trên Web.
"""
import networkx as nx
from typing import Dict, Any, List
from .kg_base import KnowledgeGraph

COLOR_PALETTE = {
    "Disease": "#EF4444",           # Red
    "ClinicalIndicator": "#F59E0B", # Amber
    "Medication": "#10B981",        # Emerald
    "Biguanide": "#059669",
    "SGLT2i": "#047857",
    "Sulfonylurea": "#065F46",
    "Thiazolidinedione": "#047857",
    "Insulin": "#14B8A6",
    "Substance": "#8B5CF6",         # Violet
    "Complication": "#DC2626",      # Bright Red
    "Food": "#84CC16",              # Lime
    "LowGIFood": "#22C55E",
    "HighGIFood": "#EA580C",
    "LeanProtein": "#3B82F6",
    # Finance colors
    "GlobalFactor": "#6366F1",      # Indigo
    "DomesticFactor": "#3B82F6",    # Blue
    "PolicyEvent": "#EC4899",       # Pink
    "Stock": "#10B981",             # Green
    "GoldAsset": "#EAB308",         # Gold
    "MarketIndex": "#8B5CF6",       # Purple
    "CapitalFlow": "#F97316"        # Orange
}

def export_kg_to_vis_json(kg: KnowledgeGraph) -> Dict[str, Any]:
    """Tính toán bố cục Kamada-Kawai hoặc Spring và định dạng xuất cho Vis.js."""
    try:
        # Undirected version for layout
        undirected = kg.G.to_undirected()
        pos = nx.kamada_kawai_layout(undirected, scale=600)
    except Exception:
        pos = nx.spring_layout(kg.G, seed=42, scale=600)

    nodes = []
    for node_id, data in kg.G.nodes(data=True):
        ntype = data.get("type", "Thing")
        color = COLOR_PALETTE.get(ntype, "#6B7280")
        x, y = pos.get(node_id, (0, 0))
        
        nodes.append({
            "id": node_id,
            "label": data.get("label", node_id),
            "group": ntype,
            "title": f"<b>{data.get('label', node_id)}</b><br>Loại: {ntype}",
            "x": int(x),
            "y": int(y),
            "color": {
                "background": color,
                "border": "#1F2937",
                "highlight": {"background": "#FBBF24", "border": "#B45309"}
            },
            "font": {"color": "#FFFFFF", "size": 13, "face": "Segoe UI"}
        })

    edges = []
    for u, v, k, data in kg.G.edges(keys=True, data=True):
        sign = data.get("sign", 0)
        edge_color = "#10B981" if sign > 0 else ("#EF4444" if sign < 0 else "#94A3B8")
        
        edges.append({
            "from": u,
            "to": v,
            "label": data.get("label_vi", k),
            "arrows": "to",
            "color": {"color": edge_color, "highlight": "#F59E0B"},
            "font": {"size": 10, "align": "middle", "color": "#E2E8F0"},
            "smooth": {"type": "curvedCW", "roundness": 0.15},
            "title": f"{data.get('mechanism', data.get('note', ''))}"
        })

    return {
        "graph_name": kg.name,
        "num_nodes": len(nodes),
        "num_edges": len(edges),
        "nodes": nodes,
        "edges": edges
    }
