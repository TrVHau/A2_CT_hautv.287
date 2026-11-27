"""
FastAPI Web Dashboard for Assignment 05:
Multi-Modal CNN Benchmarking & 5-Agent Collaborative Vision Council
"""

import os
import sys
import json
import base64
import numpy as np
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

sys.path.insert(0, os.path.abspath('.'))

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from assignment5.agents.council_coordinator import VisionCouncilCoordinator
from assignment5.models.parity_check import test_conv2d_parity, test_maxpool_parity
from assignment5.data.dataset_loader import (
    load_mnist_dataset, load_fashion_dataset, load_diabetes_conv1d_dataset,
    MNIST_CLASSES, FASHION_CLASSES, DIABETES_CLASSES
)

app = FastAPI(
    title="Assignment 05 - Advanced CNN Benchmarking & Vision Council",
    description="State-of-the-Art Multi-Modal CNN Intelligent Diagnostic & Benchmarking System",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static figures
os.makedirs("assignment5/figures", exist_ok=True)
app.mount("/figures", StaticFiles(directory="assignment5/figures"), name="figures")

coordinator = VisionCouncilCoordinator()

# Pre-cache small sets of samples for rapid UI testing
mX_tr, my_tr, mX_vl, my_vl, mX_te, my_te = load_mnist_dataset()
fX_tr, fy_tr, fX_vl, fy_vl, fX_te, fy_te = load_fashion_dataset()
dX_tr, dy_tr, dX_vl, dy_vl, dX_te, dy_te, feat_names = load_diabetes_conv1d_dataset()


class DeliberateRequest(BaseModel):
    modality: str
    model_name: str
    sample_index: int = 0
    custom_canvas: list = None


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    template_path = "assignment5/web/templates/index.html"
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<h1>Assignment 05 Web Dashboard Initializing...</h1>")


@app.get("/api/metrics")
async def get_metrics():
    summary_path = "assignment5/models/metrics_summary.json"
    if os.path.exists(summary_path):
        with open(summary_path, "r", encoding="utf-8") as f:
            return JSONResponse(content=json.load(f))
    return JSONResponse(content={"error": "Metrics summary not found"})


@app.get("/api/knowledge-graph")
async def get_knowledge_graph():
    kg_path = "assignment5/knowledge_graph/cnn_kg.json"
    if os.path.exists(kg_path):
        with open(kg_path, "r", encoding="utf-8") as f:
            return JSONResponse(content=json.load(f))
    return JSONResponse(content={"nodes": [], "edges": []})


@app.get("/api/parity")
async def get_parity_metrics():
    try:
        c_res = test_conv2d_parity()
        m_res = test_maxpool_parity()
        return JSONResponse(content={"conv2d": c_res, "maxpool": m_res, "status": "ALL_PARITY_PASSED"})
    except Exception as e:
        return JSONResponse(content={"status": "FAILED", "error": str(e)})


@app.get("/api/sample-data/{modality}")
async def get_sample_data(modality: str):
    if modality == "mnist":
        samples = []
        for i in range(10):
            samples.append({
                "index": i,
                "label": int(my_te[i]),
                "class_name": MNIST_CLASSES[my_te[i]],
                "matrix": mX_te[i, 0].tolist()
            })
        return JSONResponse(content={"modality": "mnist", "samples": samples})
    elif modality == "fashion":
        samples = []
        for i in range(10):
            samples.append({
                "index": i,
                "label": int(fy_te[i]),
                "class_name": FASHION_CLASSES[fy_te[i]],
                "matrix": fX_te[i, 0].tolist()
            })
        return JSONResponse(content={"modality": "fashion", "samples": samples})
    else:
        samples = []
        for i in range(10):
            samples.append({
                "index": i,
                "label": int(dy_te[i]),
                "class_name": DIABETES_CLASSES[dy_te[i]],
                "vector": dX_te[i, 0].tolist(),
                "feature_names": feat_names.tolist() if hasattr(feat_names, 'tolist') else list(feat_names)
            })
        return JSONResponse(content={"modality": "diabetes", "samples": samples})


@app.post("/api/deliberate")
async def deliberate_case(req: DeliberateRequest):
    modality = req.modality.lower()
    model_name = req.model_name
    idx = max(0, min(req.sample_index, 9))

    if req.custom_canvas and len(req.custom_canvas) == 28:
        # Use custom drawn matrix
        inp = np.array(req.custom_canvas, dtype=np.float32)
        if modality == "mnist":
            inp = (inp - 0.1307) / 0.3081
        else:
            inp = (inp - 0.2860) / 0.3530
        input_tensor = np.expand_dims(inp, axis=0)
    else:
        if modality == "mnist":
            input_tensor = mX_te[idx]
        elif modality == "fashion":
            input_tensor = fX_te[idx]
        else:
            input_tensor = dX_te[idx]

    result = coordinator.deliberate(modality, model_name, input_tensor)
    return JSONResponse(content=result)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("assignment5.web.app:app", host="0.0.0.0", port=8005, reload=False)
