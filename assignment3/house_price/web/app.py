"""
House Price Prediction Web App - FastAPI (Assignment 03)
Supports 4 models: Ridge Regression, Decision Tree, Random Forest, PyTorch MLP
"""
import os
import time
import joblib
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

# === Paths ===
BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_DIR, "../models")

# === Define PyTorch MLP ===
class RegressorMLP(nn.Module):
    def __init__(self, in_features):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_features, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )
    def forward(self, x):
        return self.net(x)

# === Load Models & Preprocessors ===
models = {}
preprocessors = {}

try:
    preprocessors['scaler'] = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
    preprocessors['features'] = joblib.load(os.path.join(MODEL_DIR, "feature_names.pkl"))
    
    models['ridge'] = joblib.load(os.path.join(MODEL_DIR, "hp_ridge_regression.pkl"))
    models['decision_tree'] = joblib.load(os.path.join(MODEL_DIR, "hp_decision_tree.pkl"))
    models['random_forest'] = joblib.load(os.path.join(MODEL_DIR, "hp_random_forest.pkl"))
    
    # Init PyTorch DL model
    dl_model = RegressorMLP(len(preprocessors['features']))
    dl_model.load_state_dict(torch.load(os.path.join(MODEL_DIR, "hp_mlp_best.pth"), map_location='cpu'))
    dl_model.eval()
    models['pytorch_mlp'] = dl_model
    
    status = "All 4 models loaded successfully."
except Exception as e:
    status = f"Error loading models: {e}"

app = FastAPI(title="House Price Estimation Multi-Model API (Assignment 03)", version="1.0")

class HouseInput(BaseModel):
    district: str = Field("Quận Nam Từ Liêm")
    house_type: str = Field("Nhà ngõ, hẻm")
    legal_status: str = Field("Đã có sổ")
    floors: float = Field(3.0)
    bedrooms: float = Field(3.0)
    length: float = Field(10.0)
    width: float = Field(4.0)
    area: float = Field(40.0)

def preprocess_input(data: HouseInput):
    # Base dummy construction
    feature_names = preprocessors['features']
    input_dict = {f: 0 for f in feature_names}
    
    # Assign numerics
    input_dict['Floors'] = data.floors
    input_dict['Bedrooms'] = data.bedrooms
    input_dict['Length'] = data.length
    input_dict['Width'] = data.width
    input_dict['Area'] = data.area
    
    # Process categorical
    dist_col = f"District_{data.district}"
    if dist_col in input_dict:
        input_dict[dist_col] = 1
        
    type_col = f"House_Type_{data.house_type}"
    if type_col in input_dict:
        input_dict[type_col] = 1
        
    legal_col = f"Legal_Status_{data.legal_status}"
    if legal_col in input_dict:
        input_dict[legal_col] = 1
        
    vec = np.array([[input_dict[f] for f in feature_names]], dtype=float)
    scaled_vec = preprocessors['scaler'].transform(vec)
    return scaled_vec

@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/health")
async def health():
    return {"status": "healthy" if len(models) == 4 else "warning", "detail": status}

@app.post("/predict")
async def predict(data: HouseInput):
    try:
        scaled_vec = preprocess_input(data)
        results = {}
        
        for m_name, m in models.items():
            t0 = time.time()
            if m_name == "pytorch_mlp":
                with torch.no_grad():
                    pred_log = m(torch.tensor(scaled_vec, dtype=torch.float32)).numpy()[0][0]
            else:
                pred_log = m.predict(scaled_vec)[0]
                
            pred_log = np.clip(pred_log, 0, 15)  # Limit max to avoid infinity
            price_real = np.expm1(pred_log)
            lat = (time.time() - t0) * 1000
            
            results[m_name] = {
                "price_million_vnd": round(float(price_real), 2),
                "price_billion_vnd": round(float(price_real) / 1000, 2),
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
    uvicorn.run(app, host="0.0.0.0", port=8001)
