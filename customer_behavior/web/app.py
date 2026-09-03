"""
Customer Behavior & Review Recommendation Web App - FastAPI
Loads the saved sklearn Pipeline (Multimodal: Tabular + TF-IDF Text + Logistic Regression)
"""
import os
from typing import Optional, Dict, Any, List
import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

# === Config ===
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../models/customer_behavior_pipeline.joblib")

# === Load model ===
try:
    model = joblib.load(MODEL_PATH)
    model_status = "loaded"
except Exception as e:
    model = None
    model_status = f"error: {str(e)}"

# === FastAPI app ===
app = FastAPI(
    title="Customer Behavior & Review Recommendation API",
    description="API for predicting whether a customer will recommend a clothing product based on rating, metadata, and review text.",
    version="1.0"
)

# === Pydantic models ===
class ReviewInput(BaseModel):
    age: int = Field(..., ge=18, le=100, description="Customer Age (18 - 100)")
    rating: int = Field(..., ge=1, le=5, description="Product Rating (1 - 5 stars)")
    positive_feedback_count: int = Field(0, ge=0, le=1000, description="Number of positive feedback upvotes")
    division_name: str = Field(..., description="Division Name, e.g., General, General Petite, Initmates")
    department_name: str = Field(..., description="Department Name, e.g., Dresses, Tops, Bottoms, Intimate, Jackets, Trend")
    class_name: str = Field(..., description="Class Name, e.g., Dresses, Blouses, Knits, Pants, Sweaters, Jeans, etc.")
    title: Optional[str] = Field("", description="Review Title")
    review_text: str = Field(..., min_length=1, description="Customer Review Text")

class PredictionMetrics(BaseModel):
    review_length: int
    word_count: int
    has_title: bool

class PredictionResponse(BaseModel):
    prediction: int
    label: str
    confidence: float
    probability: Optional[Dict[str, float]] = None
    metrics: Optional[PredictionMetrics] = None

# === Routes ===

@app.get("/")
async def serve_index():
    """Serve the main HTML web interface"""
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    return FileResponse(html_path)

@app.get("/health")
async def health_check():
    """Health check endpoint to verify pipeline status"""
    if model is None:
        return {"status": "error", "model": model_status}
    
    classifier_name = "Unknown"
    if hasattr(model, "steps") and len(model.steps) > 0:
        classifier_name = type(model.steps[-1][1]).__name__

    return {
        "status": "healthy",
        "model_file": "customer_behavior_pipeline.joblib",
        "classifier": classifier_name,
        "model_status": model_status
    }

@app.get("/categories")
async def get_categories():
    """Return valid category options for form dropdowns"""
    return {
        "divisions": ["General", "General Petite", "Initmates"],
        "departments": ["Dresses", "Tops", "Bottoms", "Intimate", "Jackets", "Trend"],
        "classes": [
            "Dresses", "Blouses", "Knits", "Pants", "Sweaters", "Jeans",
            "Outerwear", "Skirts", "Jackets", "Lounge", "Swim", "Fine gauge",
            "Sleep", "Shorts", "Legwear", "Trend", "Intimates", "Layering",
            "Casual bottoms", "Chemises"
        ]
    }

@app.get("/samples")
async def get_sample_data():
    """Return pre-defined realistic samples for quick testing"""
    return [
        {
            "id": "sample_pos",
            "title": "Positive Review (High Recommendation)",
            "data": {
                "age": 32,
                "rating": 5,
                "positive_feedback_count": 12,
                "division_name": "General",
                "department_name": "Dresses",
                "class_name": "Dresses",
                "title": "Absolutely stunning dress!",
                "review_text": "The fabric is high quality, fit is perfection and I received endless compliments throughout the evening."
            }
        },
        {
            "id": "sample_neg",
            "title": "Negative Review (Not Recommended)",
            "data": {
                "age": 45,
                "rating": 1,
                "positive_feedback_count": 8,
                "division_name": "General",
                "department_name": "Tops",
                "class_name": "Blouses",
                "title": "Terrible quality and huge sizing",
                "review_text": "Terrible quality and very cheap material. Sizing is completely off and huge. Extremely disappointed and returning immediately."
            }
        },
        {
            "id": "sample_mixed",
            "title": "Mixed / Moderate Review (Borderline)",
            "data": {
                "age": 28,
                "rating": 3,
                "positive_feedback_count": 2,
                "division_name": "General Petite",
                "department_name": "Bottoms",
                "class_name": "Pants",
                "title": "Nice color but awkward fit",
                "review_text": "The color matches the photos, but the waistband is much tighter than expected and fabric wrinkles easily."
            }
        }
    ]

@app.post("/predict", response_model=PredictionResponse)
async def predict(data: ReviewInput):
    """Predict customer recommendation decision using the multimodal pipeline"""
    if model is None:
        return PredictionResponse(
            prediction=-1,
            label="Model not loaded",
            confidence=0.0,
            probability=None,
            metrics=None
        )

    try:
        # Preprocess text and feature engineering
        title_clean = (data.title or "").strip()
        review_clean = (data.review_text or "").strip()
        full_text = f"{title_clean} {review_clean}".strip()
        
        review_length = len(full_text)
        word_count = len(full_text.split())
        has_title = 1 if len(title_clean) > 0 else 0

        # Construct input DataFrame matching pipeline feature names
        sample_df = pd.DataFrame([{
            'Age': data.age,
            'Rating': data.rating,
            'Positive Feedback Count': data.positive_feedback_count,
            'review_length': review_length,
            'word_count': word_count,
            'has_title': has_title,
            'Division Name': data.division_name.strip(),
            'Department Name': data.department_name.strip(),
            'Class Name': data.class_name.strip(),
            'full_text': full_text
        }])

        # Inference
        pred = int(model.predict(sample_df)[0])
        label = "Recommended (Khuyến nghị)" if pred == 1 else "Not Recommended (Không khuyến nghị)"

        # Probability calculation
        probability = None
        confidence = 1.0
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(sample_df)[0]
            prob_0 = round(float(proba[0]), 4)
            prob_1 = round(float(proba[1]), 4)
            probability = {
                "not_recommended": prob_0,
                "recommended": prob_1
            }
            confidence = prob_1 if pred == 1 else prob_0

        metrics = PredictionMetrics(
            review_length=review_length,
            word_count=word_count,
            has_title=bool(has_title)
        )

        return PredictionResponse(
            prediction=pred,
            label=label,
            confidence=round(confidence * 100, 2),
            probability=probability,
            metrics=metrics
        )
    except Exception as e:
        return PredictionResponse(
            prediction=-1,
            label=f"Error: {str(e)}",
            confidence=0.0,
            probability=None,
            metrics=None
        )

# === Run locally ===
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
