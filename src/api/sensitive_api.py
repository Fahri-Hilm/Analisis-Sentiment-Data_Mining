"""
FastAPI with Sensitive Sentiment Analysis
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from modeling.sensitive_analyzer import SensitiveSentimentAnalyzer

app = FastAPI(title="Sensitive Sentiment API", version="4.0.0")

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
        _analyzer = SensitiveSentimentAnalyzer()
    return _analyzer

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": "Sensitive Analyzer", "version": "4.0.0"}

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
        "Kenapa selalu kalah sih timnas kita",
        "Semoga menang ya timnas Indonesia",
        "Mantap sekali permainannya 👍",
        "Jelek banget performanya 👎"
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
    
    return {"test_results": results, "model": "Sensitive Analyzer"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
