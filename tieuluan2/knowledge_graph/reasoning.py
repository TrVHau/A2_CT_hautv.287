"""
reasoning.py
Bộ máy suy luận hình thức:
1. Quy tắc suy diễn tiến RDFS/OWL tới điểm bất động (Fixed-point closure)
2. Suy luận tác động nhân quả đa bước (Multi-Hop Causal Reasoning)
3. Lan truyền cú sốc vĩ mô (Shock Propagation) theo thuật toán BFS có suy giảm (decay)
"""
import networkx as nx
from typing import Dict, List, Any, Optional
from .kg_base import KnowledgeGraph

def apply_rdfs_closure(kg: KnowledgeGraph) -> int:
    """Suy diễn tiến trên đồ thị tri thức theo 5 luật RDFS/OWL đến khi đạt điểm bất động."""
    added_total = 0
    changed = True
    while changed:
        changed = False
        new_edges = []
        
        # Rule 1: SubClass transitivity
        # Rule 2 & 3: Transitive predicates
        for u in kg.G.nodes:
            for v in kg.G.successors(u):
                for w in kg.G.successors(v):
                    if u == w:
                        continue
                    # Check for transitive predicates
                    for k1, d1 in kg.G.get_edge_data(u, v).items():
                        pred1 = kg.onto.predicates.get(k1)
                        if pred1 and pred1.is_transitive:
                            for k2, d2 in kg.G.get_edge_data(v, w).items():
                                if k1 == k2 and not kg.G.has_edge(u, w, key=k1):
                                    new_edges.append((u, w, k1, {
                                        "source": f"inferred({d1.get('source')}+{d2.get('source')})",
                                        "inferred": True
                                    }))

        # Rule 4: Symmetric predicates
        for u, v, k, d in kg.G.edges(keys=True, data=True):
            pred = kg.onto.predicates.get(k)
            if pred and pred.is_symmetric and not kg.G.has_edge(v, u, key=k):
                new_edges.append((v, u, k, {
                    "source": f"symmetric({d.get('source')})",
                    "inferred": True
                }))

        # Apply newly inferred edges
        for u, w, k, data in new_edges:
            if not kg.G.has_edge(u, w, key=k):
                kg.G.add_edge(u, w, key=k, **data)
                added_total += 1
                changed = True

    return added_total

def impact_paths(kg: KnowledgeGraph, source: str, target: str, max_depth: int = 5) -> Dict[str, Any]:
    """Suy luận tác động đa bước từ source đến target trên đồ thị nhân quả."""
    if source not in kg.G or target not in kg.G:
        return {"paths": [], "verdict": "Không có liên kết", "net_sign": 0}

    # Find all simple paths up to max_depth
    all_paths_raw = list(nx.all_simple_edge_paths(kg.G, source, target, cutoff=max_depth))
    if not all_paths_raw:
        return {"paths": [], "verdict": "Không có đường truyền dẫn", "net_sign": 0}

    evaluated_paths = []
    path_signs = []

    for path_edges in all_paths_raw:
        path_sign = 1
        path_nodes = [source]
        step_descriptions = []
        
        for u, v, k in path_edges:
            path_nodes.append(v)
            edge_data = kg.G.get_edge_data(u, v, k)
            sign = edge_data.get("sign", 1)
            path_sign *= sign
            step_descriptions.append({
                "from": u,
                "to": v,
                "pred": k,
                "sign": sign,
                "mechanism": edge_data.get("mechanism", edge_data.get("note", "tác động")),
                "source": edge_data.get("source", "kg")
            })

        path_signs.append(path_sign)
        evaluated_paths.append({
            "nodes": path_nodes,
            "sign": path_sign,
            "direction": "TĂNG (+)" if path_sign > 0 else "GIẢM (-)",
            "steps": step_descriptions,
            "length": len(path_edges)
        })

    # Sort paths by length (shortest first)
    evaluated_paths.sort(key=lambda x: x["length"])

    # Determine net verdict
    if all(s > 0 for s in path_signs):
        verdict = "TĂNG (Tích cực +)"
        net_sign = 1
    elif all(s < 0 for s in path_signs):
        verdict = "GIẢM (Tiêu cực -)"
        net_sign = -1
    else:
        verdict = "TRÁI CHIỀU / ĐA KÊNH"
        net_sign = 0

    return {
        "source": source,
        "target": target,
        "source_label": kg.label(source),
        "target_label": kg.label(target),
        "paths": evaluated_paths,
        "verdict": verdict,
        "net_sign": net_sign
    }

def propagate_shock(kg: KnowledgeGraph, start_node: str, initial_shock: float = 1.0, decay: float = 0.7) -> Dict[str, Any]:
    """Lan truyền cú sốc vĩ mô theo thuật toán BFS có hệ số suy giảm khoảng cách."""
    if start_node not in kg.G:
        return {}

    shocks = {start_node: initial_shock}
    queue = [(start_node, initial_shock, 0)]
    visited_edges = set()

    while queue:
        curr, magnitude, depth = queue.pop(0)
        if depth >= 4:
            continue

        for succ in kg.G.successors(curr):
            for k, data in kg.G.get_edge_data(curr, succ).items():
                edge_id = (curr, succ, k)
                if edge_id in visited_edges:
                    continue
                visited_edges.add(edge_id)

                sign = data.get("sign", 1)
                transferred = magnitude * sign * decay

                if succ not in shocks or abs(transferred) > abs(shocks[succ]):
                    shocks[succ] = transferred

                queue.append((succ, transferred, depth + 1))

    return {
        node: {
            "label": kg.label(node),
            "shock_val": round(val, 4),
            "direction": "TĂNG" if val > 0 else "GIẢM"
        }
        for node, val in shocks.items()
    }
