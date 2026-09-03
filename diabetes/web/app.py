"""
Diabetes Prediction Web App - FastAPI
Loads the saved sklearn Pipeline (with preprocessor + classifier)
"""
import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional
import os

# === Config ===
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../models/diabetes_pipeline.joblib")

# === Load model ===
try:
    model = joblib.load(MODEL_PATH)
    model_status = "loaded"
except Exception as e:
    model = None
    model_status = f"error: {str(e)}"

# === FastAPI app ===
app = FastAPI(title="Diabetes Prediction API", version="1.0")

# === Pydantic models ===
class PatientData(BaseModel):
    gender: str = Field(..., description="Gender: Female, Male, or Other")
    age: float = Field(..., ge=0, le=120, description="Age in years")
    hypertension: int = Field(..., ge=0, le=1, description="Hypertension: 0 or 1")
    heart_disease: int = Field(..., ge=0, le=1, description="Heart disease: 0 or 1")
    smoking_history: str = Field(..., description="Smoking history: No Info, current, ever, former, never, not current")
    bmi: float = Field(..., ge=10, le=80, description="BMI (Body Mass Index)")
    HbA1c_level: float = Field(..., ge=3.0, le=20.0, description="HbA1c level (%)")
    blood_glucose_level: int = Field(..., ge=50, le=500, description="Blood glucose level (mg/dL)")

class PredictionResponse(BaseModel):
    prediction: int
    label: str
    probability: Optional[dict] = None

# === Routes ===

@app.get("/")
async def serve_index():
    """Serve the main HTML page"""
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    return FileResponse(html_path)

@app.get("/health")
async def health_check():
    """Health check - verify model is loaded"""
    if model is None:
        return {"status": "error", "model": model_status}
    return {
        "status": "healthy",
        "model": "diabetes_pipeline.joblib",
        "model_type": type(model.steps[-1][1]).__name__,
        "model_status": model_status
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(data: PatientData):
    """Make diabetes prediction from patient data"""
    if model is None:
        return {"prediction": -1, "label": "Model not loaded", "probability": None}

    try:
        # Convert input to DataFrame
        input_data = pd.DataFrame([data.model_dump()])

        # Predict
        prediction = int(model.predict(input_data)[0])
        label = "Diabetes Risk" if prediction == 1 else "No Diabetes Risk"

        # Get probability if available
        probability = None
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(input_data)[0]
            probability = {
                "no_diabetes": round(float(proba[0]), 4),
                "diabetes": round(float(proba[1]), 4)
            }

        return PredictionResponse(
            prediction=prediction,
            label=label,
            probability=probability
        )
    except Exception as e:
        return {"prediction": -1, "label": f"Error: {str(e)}", "probability": None}

# === Run locally ===
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
