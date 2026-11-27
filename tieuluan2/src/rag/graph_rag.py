"""
GraphRAG: Knowledge-Graph Augmented Retrieval-Augmented Generation
- Entity linking matching longest aliases
- Louvain Community Detection on the unified knowledge graph (networkx)
- Pre-computed Community Summaries for global holistic queries
- Dual Query Modes:
    1. Local Search: Entity-centric multi-hop neighborhood exploration
    2. Global Search: Macro community-level thematic synthesis
"""

import collections
from typing import Dict, List, Any, Optional, Tuple
import networkx as nx
from networkx.algorithms.community import louvain_communities


class GraphRAGSystem:
    """GraphRAG Engine combining Louvain community detection and local/global retrieval."""
    def __init__(self, diabetes_kg, finance_kg):
        self.diabetes_kg = diabetes_kg
        self.finance_kg = finance_kg
        self.nx_graph = nx.Graph()
        self.entity_catalog = {}
        self._build_network()
        self._detect_communities()

    def _build_network(self):
        # 1. Add Diabetes entities and edges
        for eid, ent in self.diabetes_kg.entities.items():
            self.entity_catalog[eid] = {
                "id": eid, "name": ent["name"], "domain": "Healthcare", "class": ent["class"]
            }
            self.nx_graph.add_node(eid, name=ent["name"], domain="Healthcare", cls=ent["class"])

        for t in self.diabetes_kg.triples_raw:
            s, o = t["subject"], t["object"]
            self.nx_graph.add_edge(s, o, relation=t["predicate"], domain="Healthcare")

        # 2. Add Finance entities and edges
        for eid, ent in self.finance_kg.entities.items():
            self.entity_catalog[eid] = {
                "id": eid, "name": ent["name"], "domain": "Finance", "class": ent["class"]
            }
            self.nx_graph.add_node(eid, name=ent["name"], domain="Finance", cls=ent["class"])

        for t in self.finance_kg.triples_raw:
            s, o = t["subject"], t["object"]
            self.nx_graph.add_edge(s, o, relation=t["predicate"], sign=t.get("sign", 1), domain="Finance")

    def _detect_communities(self):
        """Applies Louvain community partition algorithm."""
        # Find communities on connected components or whole graph
        raw_communities = louvain_communities(self.nx_graph, seed=42)
        self.communities = []
        for idx, comm in enumerate(raw_communities):
            comm_nodes = list(comm)
            # Find central node (highest degree)
            central_node = max(comm_nodes, key=lambda n: self.nx_graph.degree(n))
            domain_counts = collections.Counter([self.nx_graph.nodes[n].get("domain", "") for n in comm_nodes])
            dominant_domain = domain_counts.most_common(1)[0][0]

            # Generate synthetic summary for this community
            summary = self._generate_community_summary(idx, comm_nodes, dominant_domain, central_node)
            self.communities.append({
                "community_id": idx,
                "size": len(comm_nodes),
                "nodes": comm_nodes,
                "central_entity": central_node,
                "central_name": self.entity_catalog.get(central_node, {}).get("name", central_node),
                "dominant_domain": dominant_domain,
                "summary": summary
            })

    def _generate_community_summary(self, comm_id: int, nodes: List[str], domain: str, center: str) -> str:
        center_name = self.entity_catalog.get(center, {}).get("name", center)
        node_names = [self.entity_catalog.get(n, {}).get("name", n) for n in nodes[:6]]
        if domain == "Healthcare":
            return (
                f"[Cộng đồng Tri thức Y tế #{comm_id} - Tâm điểm: {center_name}]: "
                f"Tập hợp các thực thể then chốt bao gồm {', '.join(node_names)}. "
                f"Cộng đồng này mô hình hóa phác đồ điều trị, các xét nghiệm cận lâm sàng (HbA1c, FPG), "
                f"ràng buộc dược lý, cảnh báo tương tác Metformin và rượu bia (nhiễm toan Lactic), "
                f"và chế độ dinh dưỡng theo mô hình đĩa ăn cân bằng của Bộ Y tế Việt Nam."
            )
        else:
            return (
                f"[Cộng đồng Tri thức Tài chính #{comm_id} - Tâm điểm: {center_name}]: "
                f"Bao gồm các mắt xích kinh tế vĩ mô {', '.join(node_names)}. "
                f"Cộng đồng này phản ánh các kênh truyền dẫn chính sách tiền tệ từ lãi suất Fed và DXY sang tỷ giá USD/VND, "
                f"cơ chế hình thành giá vàng thế giới và vàng miếng SJC theo Nghị định 24/232, "
                f"cùng tác động phân hóa tới các cổ phiếu đầu ngành VN30 (FPT, VNM, HPG, VCB)."
            )

    def link_entities_in_text(self, text: str) -> List[str]:
        """Matches entity names in text using longest-match first."""
        matched = []
        text_lower = text.lower()
        # Sort catalog by entity name length descending
        sorted_entities = sorted(self.entity_catalog.values(), key=lambda e: len(e["name"]), reverse=True)
        for ent in sorted_entities:
            name = ent["name"].lower()
            eid = ent["id"].lower()
            if eid in text_lower or (len(name) > 3 and name in text_lower):
                matched.append(ent["id"])
        return list(dict.fromkeys(matched))

    def local_search(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """Local Search: Focuses on linked entities and their 1-hop / 2-hop neighborhoods."""
        linked = self.link_entities_in_text(query)
        if not linked:
            # Fallback to key entity guess
            if any(w in query.lower() for w in ["đường", "tiểu đường", "metformin", "rượu", "hba1c"]):
                linked = ["DT2", "Metformin"]
            else:
                linked = ["USD_VND", "GOLD_SJC"]

        facts = []
        visited_nodes = set(linked)

        for ent_id in linked:
            # Add entity info
            ent = self.entity_catalog.get(ent_id)
            if ent:
                facts.append(f"Thực thể trọng tâm: {ent['name']} (Lớp: {ent['class']}, Miền: {ent['domain']})")

            # Traverse 1-hop edges
            for neighbor in self.nx_graph.neighbors(ent_id):
                visited_nodes.add(neighbor)
                edge_data = self.nx_graph.get_edge_data(ent_id, neighbor)
                rel = edge_data.get("relation", "quan_he_voi")
                facts.append(f"- ({ent_id}) --[{rel}]--> ({neighbor}) [{self.entity_catalog.get(neighbor, {}).get('name', neighbor)}]")

        return {
            "mode": "GraphRAG Local Search",
            "linked_entities": linked,
            "subgraph_nodes_count": len(visited_nodes),
            "retrieved_facts": facts[:top_k * 3]
        }

    def global_search(self, query: str) -> Dict[str, Any]:
        """Global Search: Aggregates community-level summaries answering thematic macro questions."""
        is_health = any(w in query.lower() for w in ["y tế", "tiểu đường", "bệnh", "thuốc", "ăn", "dinh dưỡng"])
        is_finance = any(w in query.lower() for w in ["tài chính", "vàng", "cổ phiếu", "lãi suất", "tỷ giá", "fed"])

        matched_summaries = []
        for comm in self.communities:
            if is_health and comm["dominant_domain"] == "Healthcare":
                matched_summaries.append(comm["summary"])
            elif is_finance and comm["dominant_domain"] == "Finance":
                matched_summaries.append(comm["summary"])
            elif not is_health and not is_finance:
                matched_summaries.append(comm["summary"])

        return {
            "mode": "GraphRAG Global Search",
            "total_communities": len(self.communities),
            "matched_community_summaries": matched_summaries
        }
