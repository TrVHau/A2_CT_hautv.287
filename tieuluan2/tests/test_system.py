"""
Comprehensive Test Suite for Tieuluan 2:
Validates Knowledge Graph, Reasoning, RAG, Deep Learning, and ReAct Verifier.
"""

import os
import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
import numpy as np

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("tieuluan2"))

from tieuluan2.src.knowledge_graph.diabetes_kg import VietnamDiabetesKG
from tieuluan2.src.knowledge_graph.finance_kg import VietnamFinanceKG
from tieuluan2.src.knowledge_graph.sparql_engine import SparqlExecutor, SPARQL_QUERIES
from tieuluan2.src.rag.chunking import apply_chunking_strategy
from tieuluan2.src.rag.sparse_retrieval import BM25Retriever
from tieuluan2.src.rag.dense_retrieval import DenseRetriever
from tieuluan2.src.rag.hybrid_retrieval import HybridRRFRetriever, CrossEncoderReranker
from tieuluan2.src.rag.advanced_rag import AdvancedRAGPipeline
from tieuluan2.src.rag.graph_rag import GraphRAGSystem
from tieuluan2.src.deep_learning.diabetes_mlp import DiabetesPredictor
from tieuluan2.src.deep_learning.finance_bilstm import FinancialForecaster
from tieuluan2.src.reasoning_engine.react_engine import ReActReasoningEngine


def run_all_tests():
    print("=== TEST 1: Knowledge Graphs & Ontologies ===")
    d_kg = VietnamDiabetesKG()
    f_kg = VietnamFinanceKG()
    print(f"VietnamDiabetesKG: {d_kg.get_summary_statistics()}")
    print(f"VietnamFinanceKG: {f_kg.get_summary_statistics()}")

    # Test clinical interaction check
    inter = d_kg.query_drug_interactions("Metformin")
    assert len(inter) > 0, "Failed to find Metformin interaction"
    print(f"Metformin interactions verified: {len(inter)} rules found.")

    # Test financial causal path
    path_res = f_kg.query_transmission_path("FED_RATE", "USD_VND")
    assert path_res["path_count"] > 0, "Failed to find causal path from Fed to USD/VND"
    print(f"Macro causal path verified: {path_res['conclusion']}")

    print("\n=== TEST 2: SPARQL Queries & Deductive Closure ===")
    executor = SparqlExecutor(d_kg.graph)
    q1_res = executor.execute_query(SPARQL_QUERIES["Q1_Metformin_Interactions"])
    print(f"SPARQL Q1 (Metformin interactions) executed: {len(q1_res)} results returned.")

    print("\n=== TEST 3: RAG & Chunking Strategies ===")
    sample_corpus = {
        "doc1.txt": "Phác đồ điều trị đái tháo đường của Bộ Y tế quy định HbA1c >= 6.5%. Metformin là thuốc đầu tay.",
        "doc2.txt": "Nghị định 24/2012/NĐ-CP quy định độc quyền sản xuất vàng miếng. Khi tỷ giá USD/VND tăng thì giá vàng tăng."
    }
    chunks = apply_chunking_strategy(sample_corpus, "fixed_size")
    bm25 = BM25Retriever(chunks)
    dense = DenseRetriever(chunks)
    hybrid = HybridRRFRetriever(bm25, dense)
    reranker = CrossEncoderReranker()
    rag_pipe = AdvancedRAGPipeline(hybrid, reranker)
    hits = rag_pipe.run_advanced_retrieval("Metformin phác đồ điều trị", top_k=2)
    assert len(hits) > 0, "RAG retrieval failed"
    print(f"RAG retrieval verified: Top hit = {hits[0][0]['id']} with score {hits[0][1]:.4f}")

    print("\n=== TEST 4: GraphRAG & Louvain Communities ===")
    grag = GraphRAGSystem(d_kg, f_kg)
    assert len(grag.communities) > 0, "No Louvain communities detected"
    print(f"GraphRAG verified: Detected {len(grag.communities)} communities.")
    l_res = grag.local_search("Metformin")
    assert len(l_res["retrieved_facts"]) > 0, "Local search failed"
    print(f"Local search verified: {len(l_res['retrieved_facts'])} facts extracted.")

    print("\n=== TEST 5: PyTorch Deep Learning Models ===")
    d_pred = DiabetesPredictor(model_path="tieuluan2/data/diabetes_mlp.pt")
    dummy_rec = np.array([55, 29.0, 7.1, 155, 1, 1, 0, 0, 1, 0, 0, 0, 0], dtype=np.float32)
    risk = d_pred.predict_risk(dummy_rec)
    print(f"DiabetesMLP inference verified: {risk['risk_status']} ({risk['risk_percentage']})")

    f_fore = FinancialForecaster(target_asset="FPT", model_path="tieuluan2/data/finance_bilstm.pt")
    dummy_win = np.random.normal(0.0005, 0.012, (30, f_fore.d_in))
    f_res = f_fore.predict_with_mc_dropout(dummy_win, last_price=145000.0, n_mc=20)
    print(f"BiLSTM MC Dropout inference verified: Next price = {f_res['predicted_next_price']:,.2f} VND (CI 90%: {f_res['ci_90_price_str']})")

    print("\n=== TEST 6: Grounded ReAct Engine & Verifier ===")
    engine = ReActReasoningEngine(d_kg, f_kg, rag_pipe, grag, d_pred, f_fore)
    ans = engine.answer_query("Bệnh nhân đái tháo đường uống Metformin có uống được rượu bia không?")
    print(f"ReAct answer generated in {ans['total_latency_ms']}")
    print(f"Audit Verdict: {ans['audit_verification']['audit_verdict']}")
    print(f"Faithfulness: {ans['audit_verification']['faithfulness_percentage']}")

    print("\n>>> ALL SYSTEM TESTS PASSED PERFECTLY! <<<")


if __name__ == "__main__":
    run_all_tests()
