"""
FastAPI with Aggressive Sentiment Analysis - Minimal Neutral Results
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from modeling.aggressive_analyzer import AggressiveSentimentAnalyzer

app = FastAPI(title="Aggressive Sentiment API", version="5.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_analyzer = None

class TextInput(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    text: str
    sentiment: str
    confidence: float
    reasoning: str = ""

def get_analyzer():
    global _analyzer
    if _analyzer is None:
        _analyzer = AggressiveSentimentAnalyzer()
    return _analyzer

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": "Aggressive Analyzer", "version": "5.0.0"}

@app.post("/predict", response_model=SentimentResponse)
async def predict(input_data: TextInput):
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
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
async def test_analyzer():
    test_comments = [
        "Eric Tohir tuh megang inter Milan jja gx bisa hasilnya jelek",
        "Indonesia bisa masuk pildun kalau towel diangkat ganti kluivert",
        "Kenapa selalu kalah sih?",
        "Semoga menang ya",
        "Mantap permainannya 👍",
        "Jelek banget 👎"
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
    
    return {"test_results": results, "model": "Aggressive Analyzer"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
