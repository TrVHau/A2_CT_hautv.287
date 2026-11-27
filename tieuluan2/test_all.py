"""
test_all.py
Hệ thống kiểm thử tự động toàn diện:
1. Đồ thị tri thức (VietnamDiabetesKG & VietnamFinanceKG)
2. Bộ máy suy luận nhân quả đa bước & lan truyền cú sốc
3. Pipeline RAG 5 chiến lược phân mảnh & Hybrid RRF + Reranker
4. Mô hình học sâu ResMLP & BiLSTM Attention MC Dropout
5. Tác tử ReAct Orchestrator & Bộ kiểm chứng Verifier
"""
import unittest
import sys
import os
import torch
import numpy as np

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from tieuluan2.knowledge_graph import build_vietnam_diabetes_kg, build_vietnam_finance_kg, impact_paths, propagate_shock
from tieuluan2.rag import (
    chunk_fixed, chunk_sentences, chunk_recursive, chunk_parent_child, chunk_semantic,
    DocumentCorpus, BM25Retriever, DenseRetriever, HybridRRFRetriever, CrossEncoderReranker, GraphRAG
)
from tieuluan2.models import DiabetesResMLP, BiLSTMAttentionForecaster
from tieuluan2.agents import ReActAgent, VerifierAgent

class TestIntelligentSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n=== SETUP TEST SUITE TIEU LUAN 2 ===")
        cls.agent = ReActAgent()

    def test_01_knowledge_graphs(self):
        print("\n--- Test 1: Knowledge Graph Structure & Constraints ---")
        hkg = self.agent.hkg
        fkg = self.agent.fkg
        self.assertGreaterEqual(len(hkg.G.nodes), 15)
        self.assertGreaterEqual(len(hkg.G.edges), 15)
        self.assertGreaterEqual(len(fkg.G.nodes), 12)
        self.assertGreaterEqual(len(fkg.G.edges), 12)
        print(f"Diabetes KG: {len(hkg.G.nodes)} nodes, {len(hkg.G.edges)} edges [PASS]")
        print(f"Finance KG: {len(fkg.G.nodes)} nodes, {len(fkg.G.edges)} edges [PASS]")

    def test_02_causal_reasoning(self):
        print("\n--- Test 2: Multi-Hop Causal Reasoning ---")
        fkg = self.agent.fkg
        res_fpt = impact_paths(fkg, "Ty_Gia_USD_VND", "FPT")
        self.assertEqual(res_fpt["net_sign"], 1)
        print(f"Impact USD/VND -> FPT: {res_fpt['verdict']} [PASS]")

        res_hpg = impact_paths(fkg, "Ty_Gia_USD_VND", "HPG")
        self.assertEqual(res_hpg["net_sign"], -1)
        print(f"Impact USD/VND -> HPG: {res_hpg['verdict']} [PASS]")

        shocks = propagate_shock(fkg, "Chi_So_DXY", initial_shock=1.0)
        self.assertIn("Ty_Gia_USD_VND", shocks)
        print(f"Shock Propagation from DXY: {len(shocks)} affected nodes [PASS]")

    def test_03_rag_pipeline(self):
        print("\n--- Test 3: Multi-Strategy RAG Pipeline ---")
        sample_doc = "Đái tháo đường típ 2 là bệnh mạn tính. HbA1c >= 6.5% là tiêu chuẩn chẩn đoán. Metformin là thuốc hàng đầu."
        c_fix = chunk_fixed(sample_doc, chunk_size=40, overlap=10)
        c_rec = chunk_recursive(sample_doc, chunk_size=50)
        self.assertGreater(len(c_fix), 0)
        self.assertGreater(len(c_rec), 0)

        # Retrieval check
        q = "Tiêu chuẩn chẩn đoán HbA1c"
        hybrid_res = self.agent.hybrid.search(q, top_k=5)
        self.assertGreater(len(hybrid_res), 0)
        reranked = self.agent.reranker.rerank(q, hybrid_res, top_k=3)
        self.assertGreater(len(reranked), 0)
        print(f"Hybrid RRF retrieved {len(hybrid_res)} chunks, Reranker selected top {len(reranked)} [PASS]")

    def test_04_deep_learning_models(self):
        print("\n--- Test 4: Deep Learning Models (ResMLP & BiLSTM) ---")
        # Test ResMLP
        dummy_patient = torch.zeros(1, 8)
        prob = self.agent.health_model.predict_proba(dummy_patient)
        self.assertTrue(0.0 <= prob.item() <= 1.0)
        print(f"ResMLP Output Probability: {prob.item():.4f} [PASS]")

        # Test BiLSTM with Attention & MC Dropout
        dummy_seq = torch.zeros(1, 30, 7)
        mc_res = self.agent.finance_model.predict_mc_dropout(dummy_seq, last_price=100.0, n_samples=50)
        self.assertIn("ci_90_price", mc_res)
        self.assertLess(mc_res["ci_90_price"][0], mc_res["ci_90_price"][1])
        print(f"BiLSTM MC Dropout 90% CI: [{mc_res['ci_90_price'][0]} - {mc_res['ci_90_price'][1]}] [PASS]")

    def test_05_react_agent_execution(self):
        print("\n--- Test 5: ReAct Agent Full Execution Loop ---")
        # Healthcare case with profile
        q_health = "Tôi nam 52 tuổi, HbA1c 7.3, glucose lúc đói 138, BMI 26.5. Đang uống Metformin có uống bia được không?"
        res_h = self.agent.run(q_health)
        self.assertEqual(res_h["domain"], "health")
        self.assertGreater(len(res_h["trace"]), 3)
        self.assertIn("chan_doan_nguy_co", res_h["observations"])
        self.assertIn("kg_y_te", res_h["observations"])
        self.assertTrue(res_h["verification"]["passed"] or res_h["verification"]["used"] == "deterministic_template_fallback")
        print(f"ReAct Healthcare Query Result: Domain={res_h['domain']}, Total time={res_h['total_ms']}ms [PASS]")

        # Finance case with forecast
        q_fin = "Tỷ giá USD/VND tăng thì cổ phiếu FPT và HPG bị tác động thế nào, dự báo phiên tới?"
        res_f = self.agent.run(q_fin)
        self.assertEqual(res_f["domain"], "finance")
        self.assertIn("kg_tai_chinh", res_f["observations"])
        self.assertIn("du_bao_bilstm", res_f["observations"])
        print(f"ReAct Finance Query Result: Domain={res_f['domain']}, Total time={res_f['total_ms']}ms [PASS]")

    def test_06_verifier_auditor(self):
        print("\n--- Test 6: Verifier Agent & Hallucination Guard ---")
        verifier = VerifierAgent(min_faithfulness=0.8)
        evidence = [("SRC1", "FPT xuất khẩu phần mềm doanh thu tăng 25%"), ("SRC2", "HbA1c 6.5% chẩn đoán đái tháo đường")]
        
        # Valid cited text
        valid_draft = "Doanh thu xuất khẩu phần mềm FPT tăng 25% [1] theo tiêu chuẩn chẩn đoán [2]."
        v1 = verifier.verify(valid_draft, evidence)
        self.assertTrue(v1["passed"])

        # Hallucinated text with unsupported number and no citation
        hallucinated = "Doanh thu tăng 999% và lợi nhuận đạt 888 tỷ."
        v2 = verifier.verify(hallucinated, evidence)
        self.assertFalse(v2["passed"])
        print("Verifier correctly approved grounded draft and rejected hallucination [PASS]")

if __name__ == "__main__":
    unittest.main()
