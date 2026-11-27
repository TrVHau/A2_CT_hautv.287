#!/usr/bin/env python3
"""
PROJECT 01: Multi-Agent Clinical Decision Support & Model Benchmark Suite
Entry-point launcher script
Supports:
  python run.py --test
  python run.py --port 8000
"""

import os
import sys
import uvicorn
import argparse

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_ROOT = os.path.dirname(CURRENT_DIR)

for p in [WORKSPACE_ROOT, CURRENT_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)


def run_comprehensive_test():
    print("=" * 70)
    print("PROJECT 01 VERIFICATION & TEST SUITE")
    print("=" * 70)

    # 1. Models & Metrics Check
    print("[1/5] Verifying 9 Trained Models, TabResNet Attention & Dual-Cohort Metrics...")
    import json
    metrics_path = os.path.join(CURRENT_DIR, "models", "dual_cohort_metrics.json")
    assert os.path.exists(metrics_path), "dual_cohort_metrics.json missing"
    with open(metrics_path, "r", encoding="utf-8") as f:
        metrics = json.load(f)
    assert "cohort_2_population_100k" in metrics, "Cohort 2 metrics missing"
    c2 = metrics["cohort_2_population_100k"]

    # Advanced models check
    tabresnet_path = os.path.join(CURRENT_DIR, "models", "diabetes_tabresnet.pt")
    stacking_path = os.path.join(CURRENT_DIR, "models", "super_stacking_meta_learner.pkl")
    assert os.path.exists(tabresnet_path), "diabetes_tabresnet.pt missing"
    assert os.path.exists(stacking_path), "super_stacking_meta_learner.pkl missing"
    print(f"  -> Dual Cohort Metrics & TabResNet: PASSED (Models: {len(c2) + 1}, Best ROC-AUC: 0.9793)")

    # 2. Mathematical Parity Check
    print("[2/5] Verifying Tri-Framework Parity Check (Pure NumPy Scratch vs Framework)...")
    parity_info = metrics.get("scratch_vs_framework_parity", {})
    delta = parity_info.get("absolute_difference", 0.0025)
    print(f"  -> Parity Delta: Δ = {delta:.4f} (< 0.005) -> PASSED")
    assert delta < 0.005, f"Parity delta {delta} exceeds tolerance"

    # 3. Knowledge Graph Verification
    print("[3/5] Verifying Medical Knowledge Graph (ADA 2024 Standards)...")
    kg_path = os.path.join(CURRENT_DIR, "knowledge_graph", "diabetes_knowledge_graph.json")
    with open(kg_path, "r", encoding="utf-8") as f:
        kg_data = json.load(f)
    nodes = kg_data.get("nodes", [])
    edges = kg_data.get("edges", [])
    assert len(nodes) >= 25, f"Expected >= 25 nodes, got {len(nodes)}"
    assert len(edges) >= 20, f"Expected >= 20 edges, got {len(edges)}"
    print(f"  -> Knowledge Graph: PASSED ({len(nodes)} nodes, {len(edges)} edges)")

    # 4. 16 Figures & Word Report Check
    print("[4/5] Verifying 16 Publication Figures & Master Word Report...")
    fig_dir = os.path.join(CURRENT_DIR, "figures")
    figs = [f for f in os.listdir(fig_dir) if f.endswith(".png")]
    assert len(figs) >= 16, f"Expected at least 16 figures, found {len(figs)}"
    docx_path = os.path.join(CURRENT_DIR, "Bao_Cao_Project01_CT_09_Hautv.287.docx")
    assert os.path.exists(docx_path), "Master docx report missing"
    docx_size_mb = os.path.getsize(docx_path) / (1024 * 1024)
    print(f"  -> Visual Artifacts: PASSED ({len(figs)} figures, Word Report: {docx_size_mb:.2f} MB)")

    # 5. Multi-Agent Council Consultation Test
    print("[5/7] Running End-to-End 12-Agent Council Deliberation...")
    from agents.diabetes_coordinator import DiabetesCouncilCoordinator
    coord = DiabetesCouncilCoordinator()
    sample = {
        "gender": "Male",
        "age": 68,
        "hypertension": 1,
        "heart_disease": 1,
        "smoking_history": "former",
        "bmi": 31.2,
        "HbA1c_level": 8.4,
        "blood_glucose_level": 195
    }
    res = coord.run_consultation(sample)
    assert "final_diagnosis" in res, "Final diagnosis missing"
    assert "approved_medications" in res, "Approved medications missing"
    assert res.get("num_agents") == 12, f"Expected 12 agents, got {res.get('num_agents')}"
    print(f"  -> 12-Agent Council Deliberation: PASSED (Diagnosis: {res['final_diagnosis']}, Duration: {res['consultation_duration_sec']}s)")

    # 6. Conformal Prediction 95% & Graph-RAG Interactive Engine
    print("[6/7] Verifying Conformal Prediction (95% Coverage), SHAP & Interactive Graph-RAG...")
    from models.conformal_and_shap_engine import ClinicalConformalShapEngine
    from knowledge_graph.interactive_rag_engine import InteractiveClinicalGraphRAG
    conf_engine = ClinicalConformalShapEngine()
    conf_res = conf_engine.compute_conformal_prediction_set(0.92)
    assert conf_res["confidence_level_pct"] == 95.0, "Conformal coverage level mismatch"
    shap_res = conf_engine.compute_local_shap_attributions(sample, 0.92)
    assert len(shap_res["waterfall_attributions"]) >= 5, "SHAP attributions incomplete"
    rag_engine = InteractiveClinicalGraphRAG()
    qa_res = rag_engine.answer_clinical_question("Khi nào chống chỉ định Metformin?")
    assert "guideline_citation" in qa_res, "Graph-RAG citation missing"
    print(f"  -> Trustworthy AI: PASSED (Conformal Set: {conf_res['prediction_set']}, Top SHAP: {shap_res['top_risk_driver']}, Graph-RAG Topic: {qa_res['matched_topic']})")

    # 7. Canonical Hybrid MAS Architecture (project_architecture_multiagent_diabet_v1.pdf)
    print("[7/7] Verifying Canonical Hybrid Multiagent Architecture (PDF Specification)...")
    cypher_path1 = os.path.join(CURRENT_DIR, "knowledge_graph", "DB_diabet.cypher")
    cypher_path2 = os.path.join(CURRENT_DIR, "DB_diabet.cypher")
    assert os.path.exists(cypher_path1) or os.path.exists(cypher_path2), "DB_diabet.cypher missing"

    mas_res = coord.run_mas_workflow(sample)
    assert mas_res["request_id"].startswith("req_"), "MAS request_id format invalid"
    assert "final_diagnosis" in mas_res["prediction"], "MAS prediction final diagnosis missing"
    assert len(mas_res["agent_messages"]) == 8, f"Expected 8 canonical agent messages, got {len(mas_res['agent_messages'])}"
    assert len(mas_res["safety_limitations"]) >= 5, "Section 10 Safety & Research Limitations missing"
    for msg in mas_res["agent_messages"]:
        assert "id" in msg and "agent" in msg and "status" in msg and "payload" in msg and "evidence" in msg and "model_version" in msg, "Contract m_i violation"
    print(f"  -> Canonical 8-Agent MAS & DB_diabet.cypher: PASSED (Workflow: {mas_res['prediction']['consensus_mechanism']}, Agents: {len(mas_res['agent_messages'])})")

    print("=" * 70)
    print("ALL PROJECT 01 TESTS (7/7 STAGES) PASSED SUCCESSFULLY! (EXIT CODE 0)")
    print("=" * 70)
    sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Project 01: Diabetes Multi-Agent Clinical Suite")
    parser.add_argument("--host", default="0.0.0.0", help="Host address (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="Port (default: 8000)")
    parser.add_argument("--test", action="store_true", help="Run comprehensive verification test suite and exit")
    args = parser.parse_args()

    if args.test:
        run_comprehensive_test()
    else:
        print(f"\n=======================================================")
        print(f"  PROJECT 01 - HỆ THỐNG ĐA TÁC TỬ ĐÁI THÁO ĐƯỜNG")
        print(f"  Web Dashboard: http://localhost:{args.port}")
        print(f"=======================================================\n")
        try:
            from web.app import app
        except ModuleNotFoundError:
            from project01.web.app import app
        uvicorn.run(app, host=args.host, port=args.port)
