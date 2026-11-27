"""
FastAPI Server for Tieuluan 2 Interactive Multi-Domain Intelligence Platform:
- Healthcare AI & Nutrition Advisory
- Macroeconomics & BiLSTM Financial Forecasting
- Interactive Knowledge Graph Explorer (VietnamDiabetesKG & VietnamFinanceKG)
- RAG 25-Combination Benchmark Explorer
- ReAct Grounded Agent API with Thought Trace and Grounded Verifier Audit
"""

import os
import sys
import glob
import json
sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("tieuluan2"))

from typing import Dict, List, Any, Optional
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Import internal modules
from tieuluan2.src.knowledge_graph.diabetes_kg import VietnamDiabetesKG
from tieuluan2.src.knowledge_graph.finance_kg import VietnamFinanceKG
from tieuluan2.src.rag.chunking import apply_chunking_strategy
from tieuluan2.src.rag.sparse_retrieval import BM25Retriever
from tieuluan2.src.rag.dense_retrieval import DenseRetriever
from tieuluan2.src.rag.hybrid_retrieval import HybridRRFRetriever, CrossEncoderReranker
from tieuluan2.src.rag.advanced_rag import AdvancedRAGPipeline
from tieuluan2.src.rag.graph_rag import GraphRAGSystem
from tieuluan2.src.deep_learning.diabetes_mlp import DiabetesPredictor
from tieuluan2.src.deep_learning.finance_bilstm import FinancialForecaster
from tieuluan2.src.reasoning_engine.react_engine import ReActReasoningEngine


app = FastAPI(title="Hệ thống Tri thức & AI Đa Miền - Tiểu luận 2", version="2.0")

# Initialize Systems
print("Initializing Knowledge Graphs...")
diabetes_kg = VietnamDiabetesKG()
finance_kg = VietnamFinanceKG()

print("Loading Document Corpus for RAG...")
DOCS_DIR = os.path.join("tieuluan2", "data", "corpus_documents")
corpus_docs = {}
for filepath in glob.glob(os.path.join(DOCS_DIR, "*.txt")):
    fname = os.path.basename(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        corpus_docs[fname] = f.read()

# Build base chunks and retrievers
base_chunks = apply_chunking_strategy(corpus_docs, "semantic_boundary")
bm25_retriever = BM25Retriever(base_chunks)
dense_retriever = DenseRetriever(base_chunks)
hybrid_retriever = HybridRRFRetriever(bm25_retriever, dense_retriever, rrf_k=60)
reranker = CrossEncoderReranker()
rag_pipeline = AdvancedRAGPipeline(hybrid_retriever, reranker)

print("Initializing GraphRAG & Louvain Communities...")
graph_rag = GraphRAGSystem(diabetes_kg, finance_kg)

print("Initializing Deep Learning Models...")
diabetes_predictor = DiabetesPredictor()
finance_forecaster = FinancialForecaster(target_asset="FPT")

print("Initializing ReAct Engine & Grounded Verifier...")
react_engine = ReActReasoningEngine(
    diabetes_kg, finance_kg, rag_pipeline, graph_rag, diabetes_predictor, finance_forecaster
)

# Static files
STATIC_DIR = os.path.join("tieuluan2", "src", "web", "static")
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class ChatRequest(BaseModel):
    question: str
    patient_record: Optional[Dict[str, Any]] = None


class PatientRecordRequest(BaseModel):
    age: float = 54.0
    gender: str = "Male"
    bmi: float = 27.8
    HbA1c_level: float = 6.8
    blood_glucose_level: float = 145.0
    hypertension: int = 1
    heart_disease: int = 0
    smoking_history: str = "former"


class ForecastRequest(BaseModel):
    asset: str = "FPT"
    last_price: float = 145000.0


@app.get("/", response_class=HTMLResponse)
async def index():
    html_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Hệ thống Đồ thị Tri thức, RAG và Học sâu - Tiểu luận 2</h1>"


@app.post("/api/chat")
async def api_chat(req: ChatRequest):
    res = react_engine.answer_query(req.question, req.patient_record)
    return JSONResponse(content=res)


@app.post("/api/predict/diabetes")
async def api_predict_diabetes(req: PatientRecordRequest):
    feat_vec = react_engine._record_to_features(req.dict())
    pred = diabetes_predictor.predict_risk(feat_vec)
    return JSONResponse(content=pred)


@app.post("/api/forecast/finance")
async def api_forecast_finance(req: ForecastRequest):
    forecaster = FinancialForecaster(target_asset=req.asset)
    dummy_window = np.random.normal(0.0006, 0.0125, (30, forecaster.d_in))
    res = forecaster.predict_with_mc_dropout(dummy_window, last_price=req.last_price, n_mc=200)
    return JSONResponse(content=res)


@app.get("/api/kg/graph")
async def api_kg_graph():
    """Returns combined Knowledge Graph in Cytoscape format."""
    nodes = []
    edges = []

    # Diabetes nodes & edges
    for eid, ent in diabetes_kg.entities.items():
        nodes.append({
            "data": {
                "id": eid,
                "label": ent["name"],
                "class": ent["class"],
                "domain": "Healthcare",
                "color": "#10b981"
            }
        })
    for idx, t in enumerate(diabetes_kg.triples_raw):
        edges.append({
            "data": {
                "id": f"dh_e_{idx}",
                "source": t["subject"],
                "target": t["object"],
                "label": t["predicate"],
                "color": "#ef4444" if "causes_interaction" in t["predicate"] or "adverse" in t["predicate"] else "#64748b"
            }
        })

    # Finance nodes & edges
    for eid, ent in finance_kg.entities.items():
        nodes.append({
            "data": {
                "id": eid,
                "label": ent["name"],
                "class": ent["class"],
                "domain": "Finance",
                "color": "#3b82f6"
            }
        })
    for idx, t in enumerate(finance_kg.triples_raw):
        edges.append({
            "data": {
                "id": f"fn_e_{idx}",
                "source": t["subject"],
                "target": t["object"],
                "label": f"{t['predicate']} ({'+' if t.get('sign', 1) > 0 else '-'})",
                "color": "#22c55e" if t.get("sign", 1) > 0 else "#f97316"
            }
        })

    return JSONResponse(content={"nodes": nodes, "edges": edges, "communities": graph_rag.communities})


@app.get("/api/rag/benchmark")
async def api_rag_benchmark():
    """Returns precomputed 25-combination benchmark matrix matching the thesis."""
    matrix = [
        {"strategy": "Cố định 500 ký tự", "retriever": "Sparse BM25", "hit1": 0.58, "hit5": 0.82, "mrr": 0.69, "ndcg": 0.74, "latency_ms": 3.8},
        {"strategy": "Cố định 500 ký tự", "retriever": "Dense Multilingual", "hit1": 0.64, "hit5": 0.86, "mrr": 0.73, "ndcg": 0.78, "latency_ms": 12.4},
        {"strategy": "Cố định 500 ký tự", "retriever": "Hybrid RRF (k=60)", "hit1": 0.72, "hit5": 0.91, "mrr": 0.79, "ndcg": 0.84, "latency_ms": 15.2},
        {"strategy": "Cố định 500 ký tự", "retriever": "Cross-Encoder Rerank", "hit1": 0.78, "hit5": 0.93, "mrr": 0.84, "ndcg": 0.88, "latency_ms": 48.6},
        {"strategy": "Cố định 500 ký tự", "retriever": "GraphRAG Louvain", "hit1": 0.76, "hit5": 0.92, "mrr": 0.82, "ndcg": 0.86, "latency_ms": 32.1},

        {"strategy": "Chồng lấn (500, 100)", "retriever": "Sparse BM25", "hit1": 0.61, "hit5": 0.85, "mrr": 0.71, "ndcg": 0.76, "latency_ms": 4.1},
        {"strategy": "Chồng lấn (500, 100)", "retriever": "Dense Multilingual", "hit1": 0.67, "hit5": 0.89, "mrr": 0.76, "ndcg": 0.81, "latency_ms": 14.1},
        {"strategy": "Chồng lấn (500, 100)", "retriever": "Hybrid RRF (k=60)", "hit1": 0.75, "hit5": 0.93, "mrr": 0.82, "ndcg": 0.86, "latency_ms": 17.5},
        {"strategy": "Chồng lấn (500, 100)", "retriever": "Cross-Encoder Rerank", "hit1": 0.81, "hit5": 0.95, "mrr": 0.87, "ndcg": 0.90, "latency_ms": 52.3},
        {"strategy": "Chồng lấn (500, 100)", "retriever": "GraphRAG Louvain", "hit1": 0.79, "hit5": 0.94, "mrr": 0.85, "ndcg": 0.88, "latency_ms": 35.4},

        {"strategy": "Theo ranh giới câu", "retriever": "Sparse BM25", "hit1": 0.55, "hit5": 0.79, "mrr": 0.65, "ndcg": 0.70, "latency_ms": 3.2},
        {"strategy": "Theo ranh giới câu", "retriever": "Dense Multilingual", "hit1": 0.62, "hit5": 0.84, "mrr": 0.71, "ndcg": 0.75, "latency_ms": 11.8},
        {"strategy": "Theo ranh giới câu", "retriever": "Hybrid RRF (k=60)", "hit1": 0.70, "hit5": 0.88, "mrr": 0.77, "ndcg": 0.81, "latency_ms": 14.2},
        {"strategy": "Theo ranh giới câu", "retriever": "Cross-Encoder Rerank", "hit1": 0.76, "hit5": 0.91, "mrr": 0.82, "ndcg": 0.85, "latency_ms": 44.8},
        {"strategy": "Theo ranh giới câu", "retriever": "GraphRAG Louvain", "hit1": 0.74, "hit5": 0.90, "mrr": 0.80, "ndcg": 0.83, "latency_ms": 29.6},

        {"strategy": "Ngữ nghĩa Paragraph", "retriever": "Sparse BM25", "hit1": 0.65, "hit5": 0.88, "mrr": 0.75, "ndcg": 0.80, "latency_ms": 4.5},
        {"strategy": "Ngữ nghĩa Paragraph", "retriever": "Dense Multilingual", "hit1": 0.71, "hit5": 0.92, "mrr": 0.80, "ndcg": 0.85, "latency_ms": 16.2},
        {"strategy": "Ngữ nghĩa Paragraph", "retriever": "Hybrid RRF (k=60)", "hit1": 0.80, "hit5": 0.96, "mrr": 0.86, "ndcg": 0.90, "latency_ms": 19.8},
        {"strategy": "Ngữ nghĩa Paragraph", "retriever": "Cross-Encoder Rerank", "hit1": 0.86, "hit5": 0.98, "mrr": 0.91, "ndcg": 0.94, "latency_ms": 58.4},
        {"strategy": "Ngữ nghĩa Paragraph", "retriever": "GraphRAG Louvain", "hit1": 0.84, "hit5": 0.97, "mrr": 0.89, "ndcg": 0.92, "latency_ms": 38.2},

        {"strategy": "Phân cấp Cha - Con", "retriever": "Sparse BM25", "hit1": 0.63, "hit5": 0.87, "mrr": 0.73, "ndcg": 0.78, "latency_ms": 5.2},
        {"strategy": "Phân cấp Cha - Con", "retriever": "Dense Multilingual", "hit1": 0.70, "hit5": 0.91, "mrr": 0.79, "ndcg": 0.84, "latency_ms": 18.0},
        {"strategy": "Phân cấp Cha - Con", "retriever": "Hybrid RRF (k=60)", "hit1": 0.78, "hit5": 0.94, "mrr": 0.84, "ndcg": 0.88, "latency_ms": 21.5},
        {"strategy": "Phân cấp Cha - Con", "retriever": "Cross-Encoder Rerank", "hit1": 0.84, "hit5": 0.96, "mrr": 0.89, "ndcg": 0.92, "latency_ms": 64.2},
        {"strategy": "Phân cấp Cha - Con", "retriever": "GraphRAG Louvain", "hit1": 0.82, "hit5": 0.95, "mrr": 0.87, "ndcg": 0.90, "latency_ms": 41.5}
    ]
    return JSONResponse(content={"benchmark_matrix": matrix})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
