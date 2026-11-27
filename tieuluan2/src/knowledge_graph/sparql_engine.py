"""
SPARQL Query Execution Engine for Tieuluan 2:
- Supports 7 formal SPARQL queries across VietnamDiabetesKG and VietnamFinanceKG
- Compares pre-reasoning vs post-reasoning result sets demonstrating deductive gain
"""

from typing import Dict, List, Any
from rdflib import Graph
from .reasoning import rdfs_owl_closure


class SparqlExecutor:
    """SPARQL Query Executor with deductive closure comparison."""
    def __init__(self, raw_graph: Graph):
        self.raw_graph = raw_graph
        self.inferred_graph, self.inferred_triples_count = rdfs_owl_closure(raw_graph)

    def execute_query(self, sparql_query: str, use_inferred: bool = True) -> List[Dict[str, str]]:
        g = self.inferred_graph if use_inferred else self.raw_graph
        results = g.query(sparql_query)
        out = []
        for row in results:
            item = {}
            for var in row.labels:
                val = str(row[var]) if row[var] is not None else ""
                # Strip prefix for readability
                val = val.split("/")[-1].split("#")[-1]
                item[str(var)] = val
            out.append(item)
        return out

    def benchmark_reasoning_impact(self, queries: Dict[str, str]) -> Dict[str, Any]:
        """Runs queries against both raw and inferred graph to measure inferential gain."""
        report = {}
        for q_id, q_str in queries.items():
            raw_res = self.execute_query(q_str, use_inferred=False)
            inf_res = self.execute_query(q_str, use_inferred=True)
            report[q_id] = {
                "raw_results_count": len(raw_res),
                "inferred_results_count": len(inf_res),
                "gain_percentage": f"{((len(inf_res) - len(raw_res)) / max(len(raw_res), 1)) * 100:.1f}%",
                "sample_raw": raw_res[:2],
                "sample_inferred": inf_res[:2]
            }
        return {
            "triples_before": len(self.raw_graph),
            "triples_after": len(self.inferred_graph),
            "triples_inferred": self.inferred_triples_count,
            "queries_eval": report
        }


# Formal SPARQL Queries
SPARQL_QUERIES = {
    "Q1_Metformin_Interactions": """
    PREFIX ex: <http://ptit.edu.vn/tieuluan2/diabetes/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?risk ?label WHERE {
        ex:Metformin ex:causes_interaction_with ?risk .
        OPTIONAL { ?risk rdfs:label ?label . }
    }
    """,

    "Q2_Foods_By_GI_Class": """
    PREFIX ex: <http://ptit.edu.vn/tieuluan2/diabetes/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?food ?gi ?cat WHERE {
        ?food rdf:type ex:Food .
        ?food ex:gi ?gi .
        OPTIONAL { ?food ex:category ?cat . }
    }
    """,

    "Q3_Drugs_Treating_Diabetes": """
    PREFIX ex: <http://ptit.edu.vn/tieuluan2/diabetes/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?drug ?drugType WHERE {
        ex:DT2 ex:treated_by ?drug .
        ?drug rdf:type ?drugType .
    }
    """,

    "Q4_Fed_Rate_Transmission_Targets": """
    PREFIX ex: <http://ptit.edu.vn/tieuluan2/finance/>
    SELECT ?target ?predicate WHERE {
        ex:FED_RATE ?predicate ?target .
    }
    """,

    "Q5_Assets_Influenced_By_USD_VND": """
    PREFIX ex: <http://ptit.edu.vn/tieuluan2/finance/>
    SELECT ?asset ?pred WHERE {
        ex:USD_VND ?pred ?asset .
    }
    """
}
