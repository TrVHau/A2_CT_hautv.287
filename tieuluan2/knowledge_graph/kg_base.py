"""
kg_base.py
Lớp cơ sở Đồ thị Tri thức (KnowledgeGraph) tích hợp xác thực ràng buộc bản thể học,
diễn đạt tự nhiên sang tiếng Việt và xuất RDF đồ thị ngữ nghĩa.
"""
import networkx as nx
from typing import Dict, List, Optional, Any, Tuple
from .ontology import Ontology

class KnowledgeGraph:
    def __init__(self, name: str, onto: Ontology):
        self.name = name
        self.onto = onto
        self.G = nx.MultiDiGraph(name=name)
        self.aliases: Dict[str, str] = {} # alias -> canonical node_id

    def add_node(self, node_id: str, node_type: str, label: str, aliases: Optional[List[str]] = None, **attrs):
        if not self.onto.is_a(node_type, "Thing"):
            raise ValueError(f"Loại thực thể '{node_type}' chưa được định nghĩa trong bản thể học.")
        
        self.G.add_node(node_id, type=node_type, label=label, **attrs)
        self.aliases[node_id.lower()] = node_id
        self.aliases[label.lower()] = node_id
        if aliases:
            for al in aliases:
                self.aliases[al.lower().strip()] = node_id

    def add_fact(self, s: str, p: str, o: str, source: str = "core", **attrs) -> Dict[str, Any]:
        if s not in self.G:
            raise ValueError(f"Chủ thể '{s}' chưa tồn tại trong đồ thị {self.name}.")
        if o not in self.G:
            raise ValueError(f"Đối tượng '{o}' chưa tồn tại trong đồ thị {self.name}.")
        
        s_type = self.G.nodes[s]["type"]
        o_type = self.G.nodes[o]["type"]
        
        ok, msg = self.onto.validate_triple(s_type, p, o_type)
        if not ok:
            raise ValueError(f"Ràng buộc thất bại khi thêm ({s}, {p}, {o}): {msg}")
        
        pred = self.onto.predicates[p]
        fact_data = {
            "pred": p,
            "label_vi": pred.label_vi,
            "source": source,
            **attrs
        }
        self.G.add_edge(s, o, key=p, **fact_data)
        return fact_data

    def label(self, node_id: str) -> str:
        if node_id in self.G:
            return self.G.nodes[node_id].get("label", node_id)
        return node_id

    def verbalize(self, s: str, p: str, o: str, data: Optional[Dict[str, Any]] = None) -> str:
        """Chuyển bộ ba thành câu tiếng Việt hoàn chỉnh cho LLM làm bằng chứng trích dẫn."""
        s_lbl = self.label(s)
        o_lbl = self.label(o)
        pred = self.onto.predicates.get(p)
        p_lbl = pred.label_vi if pred else p

        attrs_str = ""
        if data:
            extras = []
            for k, v in data.items():
                if k not in ("pred", "label_vi", "source"):
                    extras.append(f"{k}: {v}")
            if extras:
                attrs_str = f" ({'; '.join(extras)})"

        return f"{s_lbl} —[{p_lbl}]→ {o_lbl}{attrs_str}."

    def find_node(self, term: str) -> Optional[str]:
        t = term.lower().strip()
        return self.aliases.get(t)

    def to_rdf(self) -> str:
        """Xuất sang định dạng RDF Turtle chuẩn Semantic Web bằng rdflib."""
        from rdflib import Graph, URIRef, Literal, Namespace, RDF, RDFS
        
        EX = Namespace(f"http://example.org/{self.name}#")
        g = Graph()
        g.bind("ex", EX)
        g.bind("rdfs", RDFS)

        for n, d in self.G.nodes(data=True):
            n_uri = EX[n]
            g.add((n_uri, RDF.type, EX[d["type"]]))
            g.add((n_uri, RDFS.label, Literal(d.get("label", n), lang="vi")))

        for u, v, k, d in self.G.edges(keys=True, data=True):
            s_uri = EX[u]
            o_uri = EX[v]
            p_uri = EX[k]
            g.add((s_uri, p_uri, o_uri))

        return g.serialize(format="turtle")
