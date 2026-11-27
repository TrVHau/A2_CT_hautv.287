"""
Knowledge Graph Reasoning Engine for Tieuluan 2:
- RDFS/OWL Forward Chaining Deductive Closure (fixpoint iteration)
- Multi-Step Causal Path Reasoning with Polarity Algebra (+ / -)
- Shock Propagation BFS through Macro-Economic Graph
- RDFLib Export with RDF Reification for Edge Properties
"""

import collections
from typing import Dict, List, Optional, Set, Tuple, Any
from rdflib import Graph, Literal, Namespace, RDF, RDFS, OWL, URIRef


EX = Namespace("http://ptit.edu.vn/tieuluan2/")


def rdfs_owl_closure(g: Graph) -> Tuple[Graph, int]:
    """
    Computes deductive forward chaining closure over 5 RDFS/OWL axiomatic inference rules:
    Rule 1: Transitivity of rdfs:subClassOf:
            (A, subClassOf, B) & (B, subClassOf, C) => (A, subClassOf, C)
    Rule 2: Type inheritance:
            (x, type, C) & (C, subClassOf, D) => (x, type, D)
    Rule 3: Symmetric property:
            p is SymmetricProperty & (x, p, y) => (y, p, x)
    Rule 4: Transitive property:
            p is TransitiveProperty & (x, p, y) & (y, p, z) => (x, p, z)
    Rule 5: Inverse properties:
            p inverseOf q & (x, p, y) => (y, q, x)
    Iterates until fixed point (no new triples generated).
    """
    g_out = Graph()
    for t in g:
        g_out.add(t)

    base_count = len(g_out)
    while True:
        inferred = set()

        # Rule 1: subClassOf transitivity
        subclasses = list(g_out.subject_objects(RDFS.subClassOf))
        for a, b in subclasses:
            for _, c in g_out.subject_objects(RDFS.subClassOf):
                if _ == b and (a, RDFS.subClassOf, c) not in g_out:
                    inferred.add((a, RDFS.subClassOf, c))

        # Rule 2: Type inheritance
        for inst, cls in list(g_out.subject_objects(RDF.type)):
            for _, parent in g_out.subject_objects(RDFS.subClassOf):
                if _ == cls and (inst, RDF.type, parent) not in g_out:
                    inferred.add((inst, RDF.type, parent))

        # Rule 3: Symmetric properties
        sym_props = set(g_out.subjects(RDF.type, OWL.SymmetricProperty))
        for p in sym_props:
            for s, o in list(g_out.subject_objects(p)):
                if (o, p, s) not in g_out:
                    inferred.add((o, p, s))

        # Rule 4: Transitive properties
        trans_props = set(g_out.subjects(RDF.type, OWL.TransitiveProperty))
        for p in trans_props:
            for x, y in list(g_out.subject_objects(p)):
                for y2, z in list(g_out.subject_objects(p)):
                    if y == y2 and (x, p, z) not in g_out:
                        inferred.add((x, p, z))

        # Rule 5: Inverse properties
        inv_pairs = list(g_out.subject_objects(OWL.inverseOf))
        for p, q in inv_pairs:
            for s, o in list(g_out.subject_objects(p)):
                if (o, q, s) not in g_out:
                    inferred.add((o, q, s))

        if not inferred:
            break

        for t in inferred:
            g_out.add(t)

    derived_count = len(g_out) - base_count
    return g_out, derived_count


class CausalGraphReasoner:
    """
    Multi-Step Causal Path and Shock Propagation Engine:
    - Directed edges with signs (+1 for tang_dan_toi, -1 for giam_dan_toi)
    - Path polarity product: product of edge signs along the path
    - Net effect determination and breadth-first shock propagation
    """
    def __init__(self):
        self.adj: Dict[str, List[Tuple[str, int, str]]] = collections.defaultdict(list)
        self.node_info: Dict[str, Dict[str, Any]] = {}

    def add_node(self, node_id: str, label: str, node_type: str, metadata: Optional[Dict] = None):
        self.node_info[node_id] = {
            "label": label,
            "type": node_type,
            "metadata": metadata or {}
        }

    def add_edge(self, source: str, target: str, sign: int, relation_name: str, mechanism: str = "", source_doc: str = ""):
        """sign: +1 (tang/dong_chieu) or -1 (giam/nguoc_chieu)."""
        self.adj[source].append((target, sign, relation_name, mechanism, source_doc))

    def find_all_causal_paths(self, start: str, end: str, max_depth: int = 5) -> List[Dict[str, Any]]:
        """Finds all directed causal paths from start to end up to max_depth with cumulative sign."""
        paths = []

        def dfs(curr: str, target: str, current_path: List[Tuple], visited: Set[str]):
            if len(current_path) > max_depth:
                return
            if curr == target and current_path:
                # Calculate path sign
                path_sign = 1
                for edge in current_path:
                    path_sign *= edge[2]
                paths.append({
                    "start": start,
                    "target": target,
                    "length": len(current_path),
                    "sign": path_sign,
                    "sign_str": "TĂNG (+)" if path_sign > 0 else "GIẢM (-)",
                    "steps": [
                        {
                            "from": e[0],
                            "to": e[1],
                            "sign": e[2],
                            "rel": e[3],
                            "mechanism": e[4],
                            "source_doc": e[5]
                        }
                        for e in current_path
                    ]
                })
                return

            visited.add(curr)
            for neighbor in self.adj.get(curr, []):
                nxt, sign, rel, mech, sdoc = neighbor
                if nxt not in visited:
                    dfs(nxt, target, current_path + [(curr, nxt, sign, rel, mech, sdoc)], visited)
            visited.remove(curr)

        dfs(start, end, [], set())
        return paths

    def calculate_net_effect(self, start: str, end: str) -> Dict[str, Any]:
        """Calculates net macroeconomic effect aggregating multiple paths."""
        paths = self.find_all_causal_paths(start, end)
        if not paths:
            return {
                "source": start,
                "target": end,
                "path_count": 0,
                "net_sign": 0,
                "conclusion": "Không tìm thấy kênh truyền dẫn nhân quả trực tiếp hay gián tiếp.",
                "paths": []
            }

        pos_paths = [p for p in paths if p["sign"] > 0]
        neg_paths = [p for p in paths if p["sign"] < 0]

        if pos_paths and not neg_paths:
            net_sign = 1
            conclusion = f"TÁC ĐỘNG TĂNG THUẦN NHẤT (+): Toàn bộ {len(pos_paths)} kênh truyền dẫn đều thúc đẩy tăng trưởng/tăng giá của {end}."
        elif neg_paths and not pos_paths:
            net_sign = -1
            conclusion = f"TÁC ĐỘNG GIẢM THUẦN NHẤT (-): Toàn bộ {len(neg_paths)} kênh truyền dẫn đều gây áp lực điều chỉnh giảm lên {end}."
        else:
            net_sign = 0
            conclusion = f"TÁC ĐỘNG ĐA CHIỀU (XUNG ĐỘT): Có {len(pos_paths)} kênh tác động tăng và {len(neg_paths)} kênh tác động giảm; tác động ròng phụ thuộc độ trễ và tỷ trọng dòng tiền thực tế."

        return {
            "source": start,
            "target": end,
            "path_count": len(paths),
            "pos_paths": len(pos_paths),
            "neg_paths": len(neg_paths),
            "net_sign": net_sign,
            "conclusion": conclusion,
            "paths": paths
        }

    def propagate_shock(self, origin_node: str, initial_direction: int = 1) -> Dict[str, Any]:
        """
        Breadth-First Search (BFS) shock propagation across financial network:
        initial_direction: +1 for shock increase, -1 for shock decrease
        Returns impacted nodes with cumulative shock direction and shortest causal distance.
        """
        queue = collections.deque([(origin_node, initial_direction, 0, [origin_node])])
        visited_distances = {origin_node: 0}
        impacts = {}

        while queue:
            curr, curr_dir, dist, path_nodes = queue.popleft()
            if curr != origin_node:
                impacts[curr] = {
                    "node": curr,
                    "label": self.node_info.get(curr, {}).get("label", curr),
                    "type": self.node_info.get(curr, {}).get("type", "Unknown"),
                    "direction": curr_dir,
                    "direction_str": "TĂNG (+)" if curr_dir > 0 else "GIẢM (-)",
                    "distance": dist,
                    "shortest_path": " -> ".join(path_nodes)
                }

            for nxt, sign, rel, mech, sdoc in self.adj.get(curr, []):
                new_dir = curr_dir * sign
                new_dist = dist + 1
                if nxt not in visited_distances or new_dist < visited_distances[nxt]:
                    visited_distances[nxt] = new_dist
                    queue.append((nxt, new_dir, new_dist, path_nodes + [nxt]))

        return {
            "origin": origin_node,
            "initial_shock": "TĂNG" if initial_direction > 0 else "GIẢM",
            "total_nodes_affected": len(impacts),
            "impacts": list(impacts.values())
        }
