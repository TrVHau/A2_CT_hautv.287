"""
Diabetes Prediction Web App - FastAPI (Assignment 03)
Supports 4 models: Logistic Regression, Decision Tree, Random Forest, PyTorch Deep Learning MLP
"""
import os
import time
import joblib
import numpy as np
import torch
import torch.nn as nn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict

# === Paths ===
BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_DIR, "../models")

# === Define PyTorch MLP ===
class DeeperMLP(nn.Module):
    def __init__(self, input_dim=8, num_classes=2):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, num_classes)
        )
    def forward(self, x):
        return self.network(x)

# === Load Models & Preprocessors ===
models = {}
preprocessors = {}

try:
    preprocessors['scaler'] = joblib.load(os.path.join(MODEL_DIR, "diabetes_scaler.pkl"))
    preprocessors['le_gender'] = joblib.load(os.path.join(MODEL_DIR, "le_gender.pkl"))
    preprocessors['le_smoking'] = joblib.load(os.path.join(MODEL_DIR, "le_smoking.pkl"))
    preprocessors['features'] = joblib.load(os.path.join(MODEL_DIR, "feature_names.pkl"))
    
    models['logistic_regression'] = joblib.load(os.path.join(MODEL_DIR, "diabetes_logistic_regression.pkl"))
    models['decision_tree'] = joblib.load(os.path.join(MODEL_DIR, "diabetes_decision_tree.pkl"))
    models['random_forest'] = joblib.load(os.path.join(MODEL_DIR, "diabetes_random_forest.pkl"))
    
    dl_model = DeeperMLP(input_dim=8, num_classes=2)
    dl_model.load_state_dict(torch.load(os.path.join(MODEL_DIR, "diabetes_mlp_best.pth"), map_location='cpu'))
    dl_model.eval()
    models['pytorch_mlp'] = dl_model
    
    status = "All 4 models and preprocessors loaded successfully."
except Exception as e:
    status = f"Error loading models: {e}"

app = FastAPI(title="Diabetes Prediction Multi-Model API (Assignment 03)", version="1.0")

# === Input / Output Schemas ===
class PatientInput(BaseModel):
    gender: str = Field(..., description="Female, Male, or Other")
    age: float = Field(..., ge=0, le=120)
    hypertension: int = Field(..., ge=0, le=1)
    heart_disease: int = Field(..., ge=0, le=1)
    smoking_history: str = Field(..., description="never, No Info, current, former, ever, not current")
    bmi: float = Field(..., ge=10, le=80)
    HbA1c_level: float = Field(..., ge=3.0, le=20.0)
    blood_glucose_level: int = Field(..., ge=50, le=500)
    model_choice: str = Field("all", description="logistic_regression, decision_tree, random_forest, pytorch_mlp, or all")

# === Helper: Preprocess Input ===
def preprocess_input(data: PatientInput):
    # Encode categorical
    try:
        gender_enc = preprocessors['le_gender'].transform([data.gender])[0]
    except Exception:
        gender_enc = 0
    try:
        smoking_enc = preprocessors['le_smoking'].transform([data.smoking_history])[0]
    except Exception:
        smoking_enc = 0
        
    # Build raw vector according to feature_names order:
    # ['age', 'hypertension', 'heart_disease', 'bmi', 'HbA1c_level', 'blood_glucose_level', 'gender_enc', 'smoking_enc']
    raw_vec = np.array([[
        data.age,
        data.hypertension,
        data.heart_disease,
        data.bmi,
        data.HbA1c_level,
        data.blood_glucose_level,
        gender_enc,
        smoking_enc
    ]], dtype=float)
    
    # Scale
    scaled_vec = preprocessors['scaler'].transform(raw_vec)
    return scaled_vec

# === Routes ===
@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/health")
async def health():
    return {
        "status": "healthy" if len(models) == 4 else "warning",
        "models_available": list(models.keys()),
        "detail": status
    }

@app.post("/predict")
async def predict(data: PatientInput):
    try:
        scaled_vec = preprocess_input(data)
        
        results = {}
        target_models = list(models.keys()) if data.model_choice == "all" else [data.model_choice]
        
        for m_name in target_models:
            if m_name not in models:
                continue
            m = models[m_name]
            t0 = time.time()
            if m_name == "pytorch_mlp":
                with torch.no_grad():
                    logits = m(torch.tensor(scaled_vec, dtype=torch.float32))
                    probs = torch.softmax(logits, dim=1).numpy()[0]
                    pred = int(probs.argmax())
            else:
                pred = int(m.predict(scaled_vec)[0])
                probs = m.predict_proba(scaled_vec)[0]
            lat = (time.time() - t0) * 1000  # ms
            
            results[m_name] = {
                "prediction": pred,
                "label": "Nguy cơ mắc tiểu đường" if pred == 1 else "Không có nguy cơ",
                "probability_no_diabetes": round(float(probs[0]), 4),
                "probability_diabetes": round(float(probs[1]), 4),
                "latency_ms": round(lat, 3)
            }
            
        return {
            "success": True,
            "patient_info": data.model_dump(exclude={'model_choice'}),
            "results": results
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
