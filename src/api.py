"""FastAPI server for exoplanet classification ML model."""
import os
import io
import joblib
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Exoplanet Classification API",
    description="ML API for classifying exoplanet candidates using NASA Kepler data",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model variable
model = None
model_path = "models/baseline.pkl"

# Pydantic models for request/response validation
class ExoplanetFeatures(BaseModel):
    """Features for exoplanet classification."""
    kepid: Optional[int] = None
    koi_period: Optional[float] = Field(None, description="Orbital Period [days]")
    koi_depth: Optional[float] = Field(None, description="Transit Depth [ppm]")
    koi_duration: Optional[float] = Field(None, description="Transit Duration [hours]")
    koi_impact: Optional[float] = Field(None, description="Impact Parameter")
    koi_model_snr: Optional[float] = Field(None, description="Signal-to-Noise Ratio")
    koi_steff: Optional[float] = Field(None, description="Stellar Effective Temperature [K]")
    koi_slogg: Optional[float] = Field(None, description="Stellar Surface Gravity [log10(cm/s**2)]")
    koi_srad: Optional[float] = Field(None, description="Stellar Radius [Solar radii]")
    koi_kepmag: Optional[float] = Field(None, description="Kepler-band [mag]")
    ra: Optional[float] = Field(None, description="Right Ascension [decimal degrees]")
    dec: Optional[float] = Field(None, description="Declination [decimal degrees]")

class PredictionResponse(BaseModel):
    """Response model for predictions."""
    prediction: int = Field(..., description="Predicted class (0 = false positive, 1 = planet)")
    probability: float = Field(..., description="Prediction probability")
    kepid: Optional[int] = Field(None, description="Kepler ID if provided")

class BatchPredictionResponse(BaseModel):
    """Response model for batch predictions."""
    predictions: List[PredictionResponse]
    total_samples: int

class ModelInfo(BaseModel):
    """Model information response."""
    model_path: str
    model_type: str
    is_loaded: bool
    feature_count: Optional[int] = None

def load_model():
    """Load the trained model."""
    global model
    try:
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            logger.info(f"Model loaded successfully from {model_path}")
            return True
        else:
            logger.error(f"Model file not found at {model_path}")
            return False
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        return False

def preprocess_features(features: ExoplanetFeatures) -> np.ndarray:
    """Preprocess features for model prediction."""
    # Convert to dictionary and handle None values
    feature_dict = features.dict()
    
    # Define the exact features the model was trained on (excluding kepid)
    model_features = [
        'koi_period', 'koi_depth', 'koi_duration', 'koi_impact', 
        'koi_model_snr', 'koi_steff', 'koi_slogg', 'koi_srad', 
        'koi_kepmag', 'ra', 'dec'
    ]
    
    # Extract features in the same order as training
    processed_features = []
    for feature_name in model_features:
        value = feature_dict.get(feature_name)
        if value is not None:
            processed_features.append(value)
        else:
            processed_features.append(0.0)  # Fill missing values with 0
    
    return np.array(processed_features).reshape(1, -1)

@app.on_event("startup")
async def startup_event():
    """Load model on startup."""
    load_model()

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint."""
    return {
        "message": "Exoplanet Classification API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health", response_model=Dict[str, str])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "model_loaded": str(model is not None)}

@app.get("/model/info", response_model=ModelInfo)
async def get_model_info():
    """Get model information."""
    feature_count = None
    if model is not None:
        try:
            feature_count = model.n_features_in_
        except AttributeError:
            pass
    
    return ModelInfo(
        model_path=model_path,
        model_type="XGBClassifier" if model is not None else "Unknown",
        is_loaded=model is not None,
        feature_count=feature_count
    )

@app.post("/predict", response_model=PredictionResponse)
async def predict_single(features: ExoplanetFeatures):
    """Make a single prediction."""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Preprocess features
        X = preprocess_features(features)
        
        # Make prediction
        prediction = model.predict(X)[0]
        probability = model.predict_proba(X)[0].max()
        
        return PredictionResponse(
            prediction=int(prediction),
            probability=float(probability),
            kepid=features.kepid
        )
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.post("/predict/batch", response_model=BatchPredictionResponse)
async def predict_batch(features_list: List[ExoplanetFeatures]):
    """Make batch predictions."""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    if len(features_list) > 1000:  # Limit batch size
        raise HTTPException(status_code=400, detail="Batch size too large (max 1000)")
    
    try:
        predictions = []
        
        for features in features_list:
            X = preprocess_features(features)
            prediction = model.predict(X)[0]
            probability = model.predict_proba(X)[0].max()
            
            predictions.append(PredictionResponse(
                prediction=int(prediction),
                probability=float(probability),
                kepid=features.kepid
            ))
        
        return BatchPredictionResponse(
            predictions=predictions,
            total_samples=len(predictions)
        )
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Batch prediction failed: {str(e)}")

@app.post("/predict/file")
async def predict_from_file(file: UploadFile = File(...)):
    """Make predictions from uploaded CSV file."""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    try:
        # Read CSV file
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        # Limit file size
        if len(df) > 1000:
            raise HTTPException(status_code=400, detail="File too large (max 1000 rows)")
        
        # Make predictions
        predictions = []
        for _, row in df.iterrows():
            # Convert row to ExoplanetFeatures
            features_dict = row.to_dict()
            features = ExoplanetFeatures(**features_dict)
            
            X = preprocess_features(features)
            prediction = model.predict(X)[0]
            probability = model.predict_proba(X)[0].max()
            
            predictions.append({
                "prediction": int(prediction),
                "probability": float(probability),
                "kepid": features.kepid
            })
        
        return {
            "predictions": predictions,
            "total_samples": len(predictions),
            "filename": file.filename
        }
    except Exception as e:
        logger.error(f"File prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"File prediction failed: {str(e)}")

@app.post("/model/reload")
async def reload_model():
    """Reload the model."""
    success = load_model()
    if success:
        return {"message": "Model reloaded successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to reload model")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
