"""
app.py
Máy chủ Web FastAPI hiệu năng cao phục vụ Hệ thống Tác tử Thông minh Tiểu luận 2:
- API Trò chuyện ReAct đa tác tử (/api/chat)
- API Đồ thị tri thức Vis.js tương tác (/api/kg/{kg_name})
- API So sánh đối chuẩn 4 bộ truy xuất RAG (/api/rag/compare)
- API Chuỗi thời gian tài chính & Dải tin cậy Bayes (/api/series/{ticker})
- API Chẩn đoán lâm sàng chuyên sâu (/api/predict/health)
"""
import os
import sys
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

# Ensure repository root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from tieuluan2.agents.react_orchestrator import ReActAgent
from tieuluan2.knowledge_graph.visualizer import export_kg_to_vis_json

app = FastAPI(
    title="Intelligent Multi-Agent System (KG + RAG + ReAct)",
    description="Hệ thống Tác tử Thông minh Y tế & Tài chính Việt Nam - Nâng cấp toàn diện Tiểu luận 2",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global ReAct Agent Singleton
agent = ReActAgent()

class ChatRequest(BaseModel):
    question: str
    profile: Optional[Dict[str, Any]] = None

class RAGCompareRequest(BaseModel):
    query: str
    top_k: int = 5

class HealthPredictRequest(BaseModel):
    age: float = 50.0
    gender: int = 1 # 1: Male, 0: Female
    hypertension: int = 0
    heart_disease: int = 0
    smoking_history: int = 0
    bmi: float = 25.0
    hba1c: float = 6.5
    glucose: float = 126.0

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    template_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Hệ thống Tác tử Thông minh Tiểu luận 2 đang hoạt động.</h1>"

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    try:
        result = agent.run(req.question, profile=req.profile, synthesize=True)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/api/kg/{kg_name}")
async def get_kg_data(kg_name: str):
    if kg_name.lower() in ("health", "diabetes", "y_te"):
        data = export_kg_to_vis_json(agent.hkg)
    elif kg_name.lower() in ("finance", "tai_chinh"):
        data = export_kg_to_vis_json(agent.fkg)
    else:
        return JSONResponse(status_code=404, content={"error": "Đồ thị không tồn tại"})
    return JSONResponse(content=data)

@app.post("/api/rag/compare")
async def rag_compare(req: RAGCompareRequest):
    query = req.query
    k = req.top_k
    
    # 1. BM25
    bm25_res = agent.bm25.search(query, top_k=k)
    # 2. Dense
    dense_res = agent.dense.search(query, top_k=k)
    # 3. Hybrid RRF
    hybrid_res = agent.hybrid.search(query, top_k=k)
    # 4. Hybrid + Reranker
    reranked = agent.reranker.rerank(query, hybrid_res, top_k=k)

    def _fmt(res_list):
        return [
            {"score": round(score, 4), "doc_id": c["doc_id"], "text": c["text"][:250] + "..."}
            for _, score, c in res_list
        ]

    return JSONResponse(content={
        "query": query,
        "bm25": _fmt(bm25_res),
        "dense": _fmt(dense_res),
        "hybrid_rrf": _fmt(hybrid_res),
        "reranked": _fmt(reranked)
    })

@app.get("/api/series/{ticker}")
async def get_series(ticker: str):
    t = ticker.upper()
    if agent.market_df.empty or t not in agent.market_df.columns:
        return JSONResponse(status_code=404, content={"error": f"Không tìm thấy chuỗi giá cho {ticker}"})
    
    tail_df = agent.market_df.tail(60)
    dates = tail_df["date"].tolist()
    prices = tail_df[t].tolist()
    
    return JSONResponse(content={
        "ticker": t,
        "dates": dates,
        "prices": prices,
        "latest_price": prices[-1]
    })

@app.post("/api/predict/health")
async def predict_health(req: HealthPredictRequest):
    profile = {
        "age": req.age,
        "gender": req.gender,
        "hypertension": req.hypertension,
        "heart_disease": req.heart_disease,
        "smoking_history": req.smoking_history,
        "bmi": req.bmi,
        "HbA1c_level": req.hba1c,
        "blood_glucose_level": req.glucose
    }
    tool = agent.tools["chan_doan_nguy_co"]
    obs, ev = tool.fn(profile)
    return JSONResponse(content={"observation": obs, "evidence": ev})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("tieuluan2.web.app:app", host="127.0.0.1", port=8092, reload=False)
