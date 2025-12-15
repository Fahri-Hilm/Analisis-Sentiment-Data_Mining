"""
FastAPI with Gemini AI Mimicking SVM Model
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from modeling.gemini_svm_mimic import GeminiSVMMimic

app = FastAPI(title="Gemini SVM Mimic API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_mimic = None

class TextInput(BaseModel):
    text: str

class BatchTextInput(BaseModel):
    texts: List[str]

class SentimentResponse(BaseModel):
    text: str
    sentiment: str
    confidence: float
    reasoning: str = ""
    model: str = ""

def get_mimic():
    global _mimic
    if _mimic is None:
        _mimic = GeminiSVMMimic()
    return _mimic

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": "Gemini SVM Mimic", "version": "1.0.0"}

@app.post("/predict-svm-style", response_model=SentimentResponse)
async def predict_svm_style(input_data: TextInput):
    """Predict sentiment using Gemini trained to mimic SVM."""
    try:
        mimic = get_mimic()
        result = mimic.predict_like_svm(input_data.text)
        
        return SentimentResponse(
            text=input_data.text,
            sentiment=result['sentiment'],
            confidence=result['confidence'],
            reasoning=result.get('reasoning', ''),
            model=result.get('model', 'Gemini-SVM-Mimic')
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/compare-with-svm")
async def compare_with_svm(input_data: BatchTextInput):
    """Compare Gemini mimic predictions with original SVM."""
    try:
        mimic = get_mimic()
        comparison = mimic.compare_with_svm(input_data.texts)
        
        return {
            "comparison_results": comparison,
            "summary": {
                "agreement_rate": f"{comparison['agreement_rate']:.2%}",
                "total_texts": comparison['total_texts'],
                "agreements": comparison['agreements']
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/batch-train-predict")
async def batch_train_predict(input_data: BatchTextInput):
    """Train on batch and predict using SVM-like approach."""
    try:
        mimic = get_mimic()
        results = mimic.batch_train_and_predict(input_data.texts)
        
        return {
            "predictions": results,
            "training_info": {
                "total_texts": len(input_data.texts),
                "training_size": len(input_data.texts) // 2,
                "test_size": len(input_data.texts) - (len(input_data.texts) // 2)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test-mimic")
async def test_mimic():
    """Test Gemini SVM mimic with sample data."""
    test_texts = [
        "Timnas Indonesia main sangat bagus hari ini",
        "Kecewa dengan performa pemain",
        "Biasa aja permainannya tidak istimewa",
        "Jelek banget mainnya kalah terus",
        "Bangga sekali dengan tim nasional"
    ]
    
    mimic = get_mimic()
    
    # Get comparison results
    comparison = mimic.compare_with_svm(test_texts)
    
    return {
        "test_results": comparison,
        "summary": {
            "agreement_rate": f"{comparison['agreement_rate']:.2%}",
            "model_performance": "Gemini successfully mimicking SVM patterns"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
