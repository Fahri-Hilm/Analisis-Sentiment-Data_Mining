"""
FastAPI Inference Endpoint for Sentiment Analysis
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import pickle
import logging
from pathlib import Path

app = FastAPI(title="Sentiment Analysis API", version="1.0.0")

# Global model cache
_model_cache = {}
_logger = logging.getLogger(__name__)

class TextInput(BaseModel):
    text: str

class BatchTextInput(BaseModel):
    texts: List[str]

class SentimentResponse(BaseModel):
    text: str
    sentiment: str
    confidence: float

class BatchSentimentResponse(BaseModel):
    results: List[SentimentResponse]

def load_model(model_path: str = "data/models/svm_model.pkl",
              feature_path: str = "data/models/feature_extractor.pkl",
              encoder_path: str = "data/models/label_encoder.pkl"):
    """Load model and artifacts"""
    global _model_cache
    
    if 'model' in _model_cache:
        return _model_cache
    
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        
        with open(feature_path, 'rb') as f:
            feature_extractor = pickle.load(f)
        
        with open(encoder_path, 'rb') as f:
            label_encoder = pickle.load(f)
        
        _model_cache = {
            'model': model,
            'feature_extractor': feature_extractor,
            'label_encoder': label_encoder
        }
        
        return _model_cache
    except Exception as e:
        _logger.error(f"Error loading model: {e}")
        raise

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    try:
        load_model()
        _logger.info("Model loaded successfully")
    except Exception as e:
        _logger.error(f"Failed to load model: {e}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/predict", response_model=SentimentResponse)
async def predict(input_data: TextInput):
    """Predict sentiment for single text"""
    try:
        cache = load_model()
        model = cache['model']
        feature_extractor = cache['feature_extractor']
        label_encoder = cache['label_encoder']
        
        # Feature extraction
        features = feature_extractor.transform([input_data.text])
        
        # Prediction
        prediction = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]
        confidence = float(max(probabilities))
        
        return SentimentResponse(
            text=input_data.text,
            sentiment=prediction,
            confidence=confidence
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict-batch", response_model=BatchSentimentResponse)
async def predict_batch(input_data: BatchTextInput):
    """Predict sentiment for multiple texts"""
    try:
        cache = load_model()
        model = cache['model']
        feature_extractor = cache['feature_extractor']
        label_encoder = cache['label_encoder']
        
        results = []
        
        for text in input_data.texts:
            features = feature_extractor.transform([text])
            prediction = model.predict(features)[0]
            probabilities = model.predict_proba(features)[0]
            confidence = float(max(probabilities))
            
            results.append(SentimentResponse(
                text=text,
                sentiment=prediction,
                confidence=confidence
            ))
        
        return BatchSentimentResponse(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/model-info")
async def model_info():
    """Get model information"""
    try:
        cache = load_model()
        label_encoder = cache['label_encoder']
        
        return {
            "classes": label_encoder.classes_.tolist(),
            "n_classes": len(label_encoder.classes_)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
