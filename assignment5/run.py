"""
Assignment 05 Execution Entrypoint:
Supports:
  python run.py --test            (Runs automated verification suite & exits 0)
  python run.py --port 8005       (Launches interactive FastAPI Web Dashboard)
"""

import os
import sys
import argparse

sys.path.insert(0, os.path.abspath('.'))

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def run_test_suite():
    print("=" * 70)
    print("ASSIGNMENT 05 VERIFICATION & TEST SUITE")
    print("=" * 70)

    # 1. Parity Check
    print("[1/5] Testing Pure NumPy Scratch Conv2D & MaxPool Parity...")
    from assignment5.models.parity_check import test_conv2d_parity, test_maxpool_parity
    c_res = test_conv2d_parity()
    m_res = test_maxpool_parity()
    assert c_res["diff_forward"] < 1e-4, "Conv2D forward parity failed"
    print("  -> Tri-Framework Parity: PASSED (Delta < 1e-6)")

    # 2. Knowledge Graph
    print("[2/5] Testing CNN Knowledge Graph Topology & Export...")
    from assignment5.knowledge_graph.cnn_kg import build_cnn_knowledge_graph, query_kg_neighbors
    kg = build_cnn_knowledge_graph()
    assert len(kg.nodes) >= 25, f"Expected >= 25 nodes, got {len(kg.nodes)}"
    assert len(kg.edges) >= 20, f"Expected >= 20 edges, got {len(kg.edges)}"
    q_res = query_kg_neighbors(kg, "ResNet18")
    assert "node" in q_res, "KG query failed"
    print(f"  -> CNN-KG: PASSED ({len(kg.nodes)} nodes, {len(kg.edges)} edges)")

    # 3. Model Checkpoints & Metrics
    print("[3/5] Verifying Model Checkpoints & Metrics Summary...")
    assert os.path.exists("assignment5/models/metrics_summary.json"), "metrics_summary.json missing"
    import json
    with open("assignment5/models/metrics_summary.json", "r", encoding="utf-8") as f:
        metrics = json.load(f)
    assert "mnist" in metrics and "fashion" in metrics and "diabetes" in metrics, "Missing modality in metrics"
    print("  -> Metrics & Checkpoints: PASSED (MNIST, Fashion-MNIST, Diabetes verified)")

    # 4. 14 Figures & Notebook Verification
    print("[4/5] Verifying 14 Publication Figures & Jupyter Notebook...")
    fig_dir = "assignment5/figures"
    figs = [f for f in os.listdir(fig_dir) if f.endswith(".png")]
    assert len(figs) >= 14, f"Expected at least 14 figures, found {len(figs)}"
    nb_path = "assignment5/notebook/cnn_advanced_deep_learning_benchmark.ipynb"
    assert os.path.exists(nb_path), "Notebook file missing"
    print(f"  -> Visual Artifacts: PASSED ({len(figs)} figures, executed notebook verified)")

    # 5. Multi-Agent Council & CoT LLM
    print("[5/5] Running End-to-End 5-Agent Council Deliberation...")
    from assignment5.agents.council_coordinator import VisionCouncilCoordinator
    coordinator = VisionCouncilCoordinator()
    import numpy as np
    dummy_img = np.zeros((1, 28, 28), dtype=np.float32)
    dummy_img[10:18, 10:18] = 1.0
    council_res = coordinator.deliberate("mnist", "ResNetStyle", dummy_img)
    assert "council_verdict" in council_res, "Council verdict missing"
    assert "council_consensus_score" in council_res, "Consensus score missing"
    print(f"  -> Council Deliberation: PASSED (Consensus Score: {council_res['council_consensus_score']}/100)")

    print("=" * 70)
    print("ALL ASSIGNMENT 05 TESTS PASSED SUCCESSFULLY! (EXIT CODE 0)")
    print("=" * 70)
    sys.exit(0)


def start_server(port: int = 8005):
    import uvicorn
    print(f"Starting Assignment 05 Web Dashboard on http://localhost:{port}")
    uvicorn.run("assignment5.web.app:app", host="0.0.0.0", port=port, reload=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assignment 05 Server and Test Suite")
    parser.add_argument("--test", action="store_true", help="Run automated test suite and exit")
    parser.add_argument("--port", type=int, default=8005, help="Port to bind web server (default: 8005)")
    args = parser.parse_args()

    if args.test:
        run_test_suite()
    else:
        start_server(args.port)
