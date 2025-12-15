"""
FastAPI with Unified Sentiment Scoring - Consistent scoring across all models
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from modeling.unified_sentiment_scorer import get_unified_scorer

app = FastAPI(title="Unified Sentiment Analysis API", version="7.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_scorer = None

class TextInput(BaseModel):
    text: str
    model_type: str = "realtime"  # "static", "realtime", or "unified"

class BatchTextInput(BaseModel):
    texts: List[str]
    model_type: str = "realtime"

class SentimentResponse(BaseModel):
    text: str
    sentiment: str
    confidence: float
    reasoning: str = ""
    model: str = ""
    scores: dict = {}

def get_scorer():
    global _scorer
    if _scorer is None:
        _scorer = get_unified_scorer()
    return _scorer

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": "Unified Sentiment Scorer", "version": "7.0.0"}

@app.post("/predict", response_model=SentimentResponse)
async def predict(input_data: TextInput):
    try:
        scorer = get_scorer()
        result = scorer.analyze_sentiment(input_data.text, input_data.model_type)
        
        return SentimentResponse(
            text=input_data.text,
            sentiment=result['sentiment'],
            confidence=result['confidence'],
            reasoning=result['reasoning'],
            model=result['model'],
            scores=result['scores']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict-batch")
async def predict_batch(input_data: BatchTextInput):
    try:
        scorer = get_scorer()
        results = scorer.batch_analyze(input_data.texts, input_data.model_type)
        
        return {
            "results": results,
            "total": len(results),
            "model_type": input_data.model_type,
            "model": "Unified Sentiment Scorer"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/model-info")
async def model_info():
    scorer = get_scorer()
    return scorer.get_model_info()

@app.get("/test")
async def test_analyzer():
    test_comments = [
        "Timnas Indonesia main sangat bagus hari ini",
        "Kecewa dengan performa pemain yang jelek", 
        "Biasa aja permainannya tidak istimewa",
        "Kenapa selalu kalah sih timnas kita?",
        "Mantap sekali permainannya, bangga!"
    ]
    
    scorer = get_scorer()
    
    # Test all model types
    results = {}
    for model_type in ["static", "realtime", "unified"]:
        model_results = scorer.batch_analyze(test_comments, model_type)
        results[model_type] = model_results
    
    return {
        "test_results": results,
        "model": "Unified Sentiment Scorer",
        "note": "Shows consistent scoring across static, realtime, and unified models"
    }

@app.get("/compare-models")
async def compare_models():
    """Compare how different model types score the same texts."""
    test_texts = [
        "Timnas Indonesia bermain dengan sangat baik",
        "Performa yang mengecewakan dari para pemain",
        "Permainan biasa saja, tidak ada yang istimewa",
        "Mengapa timnas selalu kesulitan mencetak gol?",
        "Luar biasa! Permainan terbaik musim ini!"
    ]
    
    scorer = get_scorer()
    comparison = {}
    
    for model_type in ["static", "realtime", "unified"]:
        results = scorer.batch_analyze(test_texts, model_type)
        comparison[model_type] = {
            "results": results,
            "summary": {
                "positive": sum(1 for r in results if r['sentiment'] == 'positive'),
                "negative": sum(1 for r in results if r['sentiment'] == 'negative'),
                "neutral": sum(1 for r in results if r['sentiment'] == 'neutral'),
                "avg_confidence": sum(r['confidence'] for r in results) / len(results)
            }
        }
    
    return {
        "comparison": comparison,
        "test_texts": test_texts,
        "note": "Comparison shows how unified scorer adapts to different model behaviors"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
