"""
FastAPI Inference Endpoint with Smart Fallback Sentiment Analysis
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import logging
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from modeling.sensitive_analyzer import SensitiveSentimentAnalyzer

app = FastAPI(title="Sensitive Sentiment Analysis API", version="4.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global analyzer
_fallback_analyzer = None
_logger = logging.getLogger(__name__)

class TextInput(BaseModel):
    text: str

class BatchTextInput(BaseModel):
    texts: List[str]

class SentimentResponse(BaseModel):
    text: str
    sentiment: str
    confidence: float
    reasoning: str = ""

class BatchSentimentResponse(BaseModel):
    results: List[SentimentResponse]

def get_analyzer():
    """Get or initialize smart fallback analyzer"""
    global _fallback_analyzer
    if _fallback_analyzer is None:
        _fallback_analyzer = SmartFallbackAnalyzer()
    return _fallback_analyzer

@app.on_event("startup")
async def startup_event():
    """Initialize Smart Fallback analyzer on startup"""
    try:
        get_analyzer()
        _logger.info("✅ Smart Fallback analyzer loaded successfully")
    except Exception as e:
        _logger.error(f"❌ Failed to load analyzer: {e}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model": "Smart Fallback", "version": "3.0.0"}

@app.post("/predict", response_model=SentimentResponse)
async def predict(input_data: TextInput):
    """Predict sentiment using Smart Fallback analyzer"""
    try:
        analyzer = get_analyzer()
        result = analyzer.analyze_sentiment(input_data.text)
        
        return SentimentResponse(
            text=input_data.text,
            sentiment=result['sentiment'],
            confidence=result['confidence'],
            reasoning=result.get('reasoning', '')
        )
    except Exception as e:
        _logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict-batch", response_model=BatchSentimentResponse)
async def predict_batch(input_data: BatchTextInput):
    """Predict sentiment for multiple texts"""
    try:
        analyzer = get_analyzer()
        results = []
        
        for text in input_data.texts:
            result = analyzer.analyze_sentiment(text)
            results.append(SentimentResponse(
                text=text,
                sentiment=result['sentiment'],
                confidence=result['confidence'],
                reasoning=result.get('reasoning', '')
            ))
        
        return BatchSentimentResponse(results=results)
    except Exception as e:
        _logger.error(f"Batch prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/model-info")
async def model_info():
    """Get model information"""
    return {
        "model_name": "Smart Fallback Sentiment Analyzer",
        "version": "3.0.0",
        "classes": ["positive", "negative", "neutral"],
        "features": [
            "Enhanced rule-based analysis",
            "Indonesian language optimized",
            "Context-aware processing",
            "Negation and intensifier handling",
            "No API quota limits"
        ],
        "accuracy": "High (Enhanced rule-based)"
    }

@app.post("/analyze")
async def analyze_detailed(input_data: TextInput):
    """Detailed sentiment analysis"""
    try:
        analyzer = get_analyzer()
        result = analyzer.analyze_sentiment(input_data.text)
        
        return {
            "text": input_data.text,
            "sentiment": result['sentiment'],
            "confidence": result['confidence'],
            "reasoning": result.get('reasoning', ''),
            "model": "Smart Fallback",
            "timestamp": "real-time"
        }
    except Exception as e:
        _logger.error(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
async def test_analyzer():
    """Test Smart Fallback analyzer with sample comments"""
    test_comments = [
        "Produk ini sangat bagus dan berkualitas tinggi!",
        "Pelayanan buruk sekali, sangat mengecewakan",
        "Biasa aja sih, tidak ada yang istimewa",
        "Timnas Indonesia juara! Sangat bangga!",
        "Kalah lagi, payah sekali performanya"
    ]
    
    analyzer = get_analyzer()
    results = []
    
    for comment in test_comments:
        result = analyzer.analyze_sentiment(comment)
        results.append({
            "text": comment,
            "sentiment": result['sentiment'],
            "confidence": result['confidence'],
            "reasoning": result.get('reasoning', '')
        })
    
    return {"test_results": results, "model": "Smart Fallback"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
