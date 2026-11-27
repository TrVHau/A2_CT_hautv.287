"""
graph_rag.py
Hiện thực kiến trúc GraphRAG:
1. Liên kết thực thể (Entity Linking) ưu tiên khớp bí danh dài nhất, không phân biệt dấu
2. Phát hiện cộng đồng tri thức (Community Detection)
3. Tìm kiếm cục bộ (Local Graph Search) quanh thực thể đích
4. Tìm kiếm toàn cục (Global Graph Search) dựa trên báo cáo tóm tắt cộng đồng
"""
import re
import unicodedata
import networkx as nx
from typing import List, Dict, Any, Tuple, Optional
from ..knowledge_graph.kg_base import KnowledgeGraph

def strip_accents(text: str) -> str:
    """Xóa dấu tiếng Việt phục vụ so khớp mờ và liên kết thực thể."""
    text = unicodedata.normalize('NFD', text)
    text = re.sub(r'[\u0300-\u036f]', '', text)
    return text.lower().replace('đ', 'd')

class EntityLinker:
    def __init__(self, kgs: List[KnowledgeGraph]):
        self.kgs = kgs
        # Build lookup table: alias -> (node_id, kg_name, orig_label)
        self.alias_table: List[Tuple[str, str, str, str]] = [] # (normalized_alias, node_id, kg_name, orig_label)
        self._build_table()

    def _build_table(self):
        for kg in self.kgs:
            for node_id, data in kg.G.nodes(data=True):
                lbl = data.get("label", node_id)
                self.alias_table.append((strip_accents(node_id), node_id, kg.name, lbl))
                self.alias_table.append((strip_accents(lbl), node_id, kg.name, lbl))
            for al, node_id in kg.aliases.items():
                lbl = kg.label(node_id)
                self.alias_table.append((strip_accents(al), node_id, kg.name, lbl))

        # Sort by alias length descending (longest match first)
        self.alias_table.sort(key=lambda x: len(x[0]), reverse=True)

    def link(self, text: str) -> List[Tuple[str, str, str]]:
        """Trả về danh sách (node_id, kg_name, label) xuất hiện trong câu hỏi."""
        norm_text = strip_accents(text)
        found = []
        seen_nodes = set()

        for norm_al, node_id, kg_name, lbl in self.alias_table:
            if len(norm_al) < 2:
                continue
            # Regex word boundary check
            pattern = r'(?:\b|^)' + re.escape(norm_al) + r'(?:\b|$)'
            if re.search(pattern, norm_text):
                if node_id not in seen_nodes:
                    seen_nodes.add(node_id)
                    found.append((node_id, kg_name, lbl))

        return found

class GraphRAG:
    def __init__(self, kgs: List[KnowledgeGraph]):
        self.kgs = {kg.name: kg for kg in kgs}
        self.linker = EntityLinker(kgs)
        self.communities: Dict[str, List[Dict[str, Any]]] = {}
        self._detect_communities()

    def _detect_communities(self):
        for kg_name, kg in self.kgs.items():
            undirected = kg.G.to_undirected()
            try:
                from networkx.algorithms.community import greedy_modularity_communities
                comms = list(greedy_modularity_communities(undirected))
            except Exception:
                comms = [set(kg.G.nodes)]

            comm_list = []
            for c_idx, members in enumerate(comms):
                top_nodes = sorted(members, key=lambda n: kg.G.degree(n), reverse=True)[:4]
                labels = [kg.label(n) for n in top_nodes]
                comm_list.append({
                    "community_id": f"{kg_name}_C{c_idx}",
                    "size": len(members),
                    "members": list(members),
                    "top_labels": labels,
                    "summary": f"Cụm tri thức {kg_name} tập trung vào: {', '.join(labels)}."
                })
            self.communities[kg_name] = comm_list

    def local_search(self, query: str, max_triples: int = 6) -> List[Tuple[str, str]]:
        """Tìm kiếm cục bộ 1-hop quanh các thực thể được liên kết trong câu hỏi."""
        linked = self.linker.link(query)
        evidence = []
        seen_edges = set()

        for node_id, kg_name, _ in linked:
            kg = self.kgs[kg_name]
            # Outgoing edges
            for succ in kg.G.successors(node_id):
                for k, d in kg.G.get_edge_data(node_id, succ).items():
                    edge_sig = (node_id, succ, k)
                    if edge_sig not in seen_edges:
                        seen_edges.add(edge_sig)
                        verb = kg.verbalize(node_id, k, succ, d)
                        src = d.get("source", kg_name)
                        evidence.append((f"KG:{src}", verb))
                        if len(evidence) >= max_triples:
                            return evidence

            # Incoming edges
            for pred_node in kg.G.predecessors(node_id):
                for k, d in kg.G.get_edge_data(pred_node, node_id).items():
                    edge_sig = (pred_node, node_id, k)
                    if edge_sig not in seen_edges:
                        seen_edges.add(edge_sig)
                        verb = kg.verbalize(pred_node, k, node_id, d)
                        src = d.get("source", kg_name)
                        evidence.append((f"KG:{src}", verb))
                        if len(evidence) >= max_triples:
                            return evidence

        return evidence

    def global_search(self, query: str) -> List[Tuple[str, str]]:
        """Tìm kiếm toàn cục trên các bản tóm tắt cộng đồng tri thức."""
        results = []
        q_norm = strip_accents(query)
        for kg_name, comm_list in self.communities.items():
            for comm in comm_list:
                for lbl in comm["top_labels"]:
                    if strip_accents(lbl) in q_norm:
                        results.append((f"Comm:{comm['community_id']}", comm["summary"]))
                        break
        return results
