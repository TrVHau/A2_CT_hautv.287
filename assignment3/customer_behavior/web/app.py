"""
Customer Behavior Prediction (NLP) Web App - FastAPI (Assignment 03)
Supports 4 models: Multinomial Naive Bayes, Logistic Regression, Random Forest, PyTorch MLP
"""
import os
import time
import re
import joblib
import numpy as np
import torch
import torch.nn as nn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

# === Paths ===
BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_DIR, "../models")

# === Define PyTorch MLP ===
class TextClassifierMLP(nn.Module):
    def __init__(self, in_features, num_classes=2):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_features, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 32),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(32, num_classes)
        )
    def forward(self, x):
        return self.net(x)

# === Load Models & Preprocessors ===
models = {}
preprocessors = {}

try:
    preprocessors['tfidf'] = joblib.load(os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl"))
    
    models['naive_bayes'] = joblib.load(os.path.join(MODEL_DIR, "cb_multinomial_naive_bayes.pkl"))
    models['logistic_regression'] = joblib.load(os.path.join(MODEL_DIR, "cb_logistic_regression.pkl"))
    models['random_forest'] = joblib.load(os.path.join(MODEL_DIR, "cb_random_forest.pkl"))
    
    # Init PyTorch DL model
    dl_model = TextClassifierMLP(in_features=len(preprocessors['tfidf'].get_feature_names_out()), num_classes=2)
    dl_model.load_state_dict(torch.load(os.path.join(MODEL_DIR, "cb_mlp_best.pth"), map_location='cpu'))
    dl_model.eval()
    models['pytorch_mlp'] = dl_model
    
    status = "All 4 models loaded successfully."
except Exception as e:
    status = f"Error loading models: {e}"

app = FastAPI(title="Customer Review Sentiment Multi-Model API (Assignment 03)", version="1.0")

class ReviewInput(BaseModel):
    review_text: str = Field(..., description="Nội dung đánh giá của khách hàng")

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9 ]+', '', text)
    text = re.sub(r'\\s+', ' ', text).strip()
    return text

@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/health")
async def health():
    return {"status": "healthy" if len(models) == 4 else "warning", "detail": status}

@app.post("/predict")
async def predict(data: ReviewInput):
    try:
        # Preprocess
        cleaned = clean_text(data.review_text)
        if len(cleaned.split()) < 3:
            return {"success": False, "error": "Vui lòng nhập đánh giá dài hơn (ít nhất 3 từ)."}
            
        vectorized = preprocessors['tfidf'].transform([cleaned]).toarray()
        
        results = {}
        for m_name, m in models.items():
            t0 = time.time()
            if m_name == "pytorch_mlp":
                with torch.no_grad():
                    logits = m(torch.tensor(vectorized, dtype=torch.float32))
                    probs = torch.softmax(logits, dim=1).numpy()[0]
                    pred = int(probs.argmax())
            else:
                pred = int(m.predict(vectorized)[0])
                probs = m.predict_proba(vectorized)[0]
                
            lat = (time.time() - t0) * 1000
            
            results[m_name] = {
                "prediction": pred,
                "label": "Khuyên dùng (Positive)" if pred == 1 else "Không khuyên dùng (Negative)",
                "probability": round(float(probs[1]), 4),
                "latency_ms": round(lat, 3)
            }
            
        return {
            "success": True,
            "results": results
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
