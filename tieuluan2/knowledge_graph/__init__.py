from .ontology import Ontology, Predicate
from .kg_base import KnowledgeGraph
from .diabetes_kg import build_vietnam_diabetes_kg
from .finance_kg import build_vietnam_finance_kg
from .reasoning import apply_rdfs_closure, impact_paths, propagate_shock
from .visualizer import export_kg_to_vis_json
