"""
Hanoi House Price Prediction Web App - FastAPI
Loads the saved sklearn Pipeline (Random Forest Regressor + Preprocessor)
"""
import os
from typing import Optional, Dict, Any, List
import joblib
import pandas as pd
import numpy as np
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

# === Config ===
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../models/house_price_model.pkl")
METADATA_PATH = os.path.join(os.path.dirname(__file__), "../models/model_metadata.pkl")

# === Load model & metadata ===
try:
    model = joblib.load(MODEL_PATH)
    model_status = "loaded"
except Exception as e:
    model = None
    model_status = f"error: {str(e)}"

try:
    metadata = joblib.load(METADATA_PATH)
except Exception:
    metadata = {}

# === FastAPI app ===
app = FastAPI(
    title="Hanoi House Price Prediction API",
    description="API dự đoán đơn giá (triệu VNĐ/m²) và tổng giá trị bất động sản nhà ở tại Hà Nội bằng Machine Learning (Random Forest Pipeline).",
    version="1.0"
)

# === Pydantic models ===
class HouseInput(BaseModel):
    area: float = Field(..., gt=5, le=3000, description="Diện tích nhà đất (m²), từ 5 - 3000 m²")
    length: Optional[float] = Field(None, ge=1, le=200, description="Chiều dài (m)")
    width: Optional[float] = Field(None, ge=1, le=100, description="Chiều rộng / Mặt tiền (m)")
    district: str = Field(..., description="Quận / Huyện tại Hà Nội")
    property_type: str = Field(..., description="Loại hình nhà ở (Nhà ngõ/hẻm, Nhà mặt phố, Biệt thự, Liền kề)")
    legal_status: str = Field("Đã có sổ", description="Tình trạng giấy tờ pháp lý")
    bedrooms: str = Field("3", description="Số phòng ngủ ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10+', 'Unknown')")

class HousePredictionResponse(BaseModel):
    status: str
    price_per_m2_million: float
    total_price_billion: float
    formatted_total_price: str
    price_range_low_billion: float
    price_range_high_billion: float
    derived_features: Dict[str, Any]

# === Routes ===

@app.get("/")
async def serve_index():
    """Serve the main HTML web interface"""
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    return FileResponse(html_path)

@app.get("/health")
async def health_check():
    """Health check endpoint to verify pipeline and model metrics"""
    if model is None:
        return {"status": "error", "model": model_status}
    
    return {
        "status": "healthy",
        "model_file": "house_price_model.pkl",
        "algorithm": metadata.get("model_name", "Random Forest"),
        "test_mae": round(float(metadata.get("test_mae", 0)), 2),
        "test_rmse": round(float(metadata.get("test_rmse", 0)), 2),
        "test_r2": round(float(metadata.get("test_r2", 0)), 4),
        "feature_dimension": metadata.get("feature_dimension", 55),
        "model_status": model_status
    }

@app.get("/categories")
async def get_categories():
    """Return available category options for dropdown selections"""
    urban_districts = [
        "Quận Ba Đình", "Quận Hoàn Kiếm", "Quận Tây Hồ", "Quận Cầu Giấy",
        "Quận Đống Đa", "Quận Hai Bà Trưng", "Quận Thanh Xuân", "Quận Hoàng Mai",
        "Quận Long Biên", "Quận Nam Từ Liêm", "Quận Bắc Từ Liêm", "Quận Hà Đông"
    ]
    suburban_districts = [
        "Huyện Gia Lâm", "Huyện Đông Anh", "Huyện Sóc Sơn", "Huyện Hoài Đức",
        "Huyện Thanh Trì", "Huyện Đan Phượng", "Huyện Thường Tín", "Huyện Thanh Oai",
        "Huyện Chương Mỹ", "Huyện Thạch Thất", "Huyện Quốc Oai", "Huyện Mê Linh",
        "Huyện Phúc Thọ", "Huyện Mỹ Đức", "Thị xã Sơn Tây", "Unknown"
    ]

    return {
        "districts_urban": urban_districts,
        "districts_suburban": suburban_districts,
        "property_types": [
            "Nhà ngõ, hẻm",
            "Nhà mặt phố, mặt tiền",
            "Nhà biệt thự",
            "Nhà phố liền kề",
            "Unknown"
        ],
        "legal_statuses": [
            "Đã có sổ",
            "Đang chờ sổ",
            "Giấy tờ khác",
            "Unknown"
        ],
        "bedrooms": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10+", "Unknown"]
    }

@app.get("/samples")
async def get_sample_houses():
    """Return realistic sample houses for 1-click test"""
    return [
        {
            "id": "sample_pho_co",
            "name": "Nhà Mặt Phố Cổ - Hoàn Kiếm",
            "data": {
                "area": 85.0,
                "length": 17.0,
                "width": 5.0,
                "district": "Quận Hoàn Kiếm",
                "property_type": "Nhà mặt phố, mặt tiền",
                "legal_status": "Đã có sổ",
                "bedrooms": "4"
            }
        },
        {
            "id": "sample_tay_ho",
            "name": "Biệt thự view Hồ Tây - Tây Hồ",
            "data": {
                "area": 180.0,
                "length": 18.0,
                "width": 10.0,
                "district": "Quận Tây Hồ",
                "property_type": "Nhà biệt thự",
                "legal_status": "Đã có sổ",
                "bedrooms": "5"
            }
        },
        {
            "id": "sample_cau_giay",
            "name": "Nhà Ngõ Ô Tô - Cầu Giấy",
            "data": {
                "area": 55.0,
                "length": 11.0,
                "width": 5.0,
                "district": "Quận Cầu Giấy",
                "property_type": "Nhà ngõ, hẻm",
                "legal_status": "Đã có sổ",
                "bedrooms": "3"
            }
        },
        {
            "id": "sample_dong_anh",
            "name": "Nhà Đất Ngoại Thành - Đông Anh",
            "data": {
                "area": 70.0,
                "length": 14.0,
                "width": 5.0,
                "district": "Huyện Đông Anh",
                "property_type": "Nhà ngõ, hẻm",
                "legal_status": "Đã có sổ",
                "bedrooms": "2"
            }
        }
    ]

@app.post("/predict", response_model=HousePredictionResponse)
async def predict_price(data: HouseInput):
    """Predict price per m2 and total price for a property"""
    if model is None:
        return HousePredictionResponse(
            status="error",
            price_per_m2_million=0.0,
            total_price_billion=0.0,
            formatted_total_price="Mô hình chưa sẵn sàng",
            price_range_low_billion=0.0,
            price_range_high_billion=0.0,
            derived_features={}
        )

    try:
        # Feature engineering logic matching notebook training
        has_dims = 1 if (data.length is not None and data.width is not None and data.length > 0 and data.width > 0) else 0
        
        if has_dims == 1:
            aspect_ratio = float(data.length) / (float(data.width) + 0.001)
            calc_area = float(data.length) * float(data.width)
            len_val = float(data.length)
            width_val = float(data.width)
        else:
            aspect_ratio = np.nan
            calc_area = np.nan
            len_val = np.nan
            width_val = np.nan

        has_legal = 1 if (data.legal_status and data.legal_status != "Unknown") else 0
        
        # Build dataframe matching pipeline column names
        sample_df = pd.DataFrame([{
            'Area': float(data.area),
            'Length': len_val,
            'Width': width_val,
            'Aspect_Ratio': aspect_ratio,
            'Calculated_Area': calc_area,
            'Has_Dimensions': has_dims,
            'Has_Legal_Docs': has_legal,
            'Quận': data.district.strip(),
            'Loại hình nhà ở': data.property_type.strip(),
            'Giấy tờ pháp lý': data.legal_status.strip(),
            'Bedrooms_Category': data.bedrooms.strip()
        }])

        # Prediction
        pred_price_m2 = float(model.predict(sample_df)[0])
        # Ensure positive price
        pred_price_m2 = max(pred_price_m2, 5.0)

        total_billion = (pred_price_m2 * float(data.area)) / 1000.0

        # Error margin for confidence interval (based on test MAE ~23 triệu/m2)
        mae = float(metadata.get("test_mae", 23.3))
        low_m2 = max(pred_price_m2 - mae * 0.5, 5.0)
        high_m2 = pred_price_m2 + mae * 0.5

        low_billion = (low_m2 * float(data.area)) / 1000.0
        high_billion = (high_m2 * float(data.area)) / 1000.0

        # Formatted string in Vietnamese
        if total_billion >= 1.0:
            formatted_price = f"{total_billion:.2f} Tỷ VNĐ"
        else:
            formatted_price = f"{total_billion * 1000:.0f} Triệu VNĐ"

        derived = {
            "aspect_ratio": round(aspect_ratio, 2) if has_dims else "Không có",
            "calculated_area": round(calc_area, 2) if has_dims else "Không có",
            "has_dimensions": bool(has_dims),
            "has_legal_docs": bool(has_legal)
        }

        return HousePredictionResponse(
            status="success",
            price_per_m2_million=round(pred_price_m2, 2),
            total_price_billion=round(total_billion, 2),
            formatted_total_price=formatted_price,
            price_range_low_billion=round(low_billion, 2),
            price_range_high_billion=round(high_billion, 2),
            derived_features=derived
        )
    except Exception as e:
        return HousePredictionResponse(
            status=f"error: {str(e)}",
            price_per_m2_million=0.0,
            total_price_billion=0.0,
            formatted_total_price=f"Lỗi: {str(e)}",
            price_range_low_billion=0.0,
            price_range_high_billion=0.0,
            derived_features={}
        )

# === Run locally ===
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
