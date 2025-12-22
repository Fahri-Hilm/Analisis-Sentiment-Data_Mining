"""
Complete Multi-Layer Timnas Sentiment Analysis API v10.0
Layer 1: Core Sentiment (1,500 words)
Layer 2: Basic Emotions (2,000 words) 
Layer 3: Football-Specific Emotions (3,000 words)
Total: 6,500 words lexicon
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from modeling.unified_sentiment_scorer import get_unified_scorer
from analysis.enhanced_sentiment_analyzer import EnhancedTimnasSentimentAnalyzer
from analysis.basic_emotions_analyzer import BasicEmotionsAnalyzer
from analysis.football_emotions_analyzer import FootballEmotionsAnalyzer

app = FastAPI(title="Complete Multi-Layer Timnas Sentiment API", version="10.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global analyzers
_lexicon_analyzer = None
_emotion_analyzer = None
_football_analyzer = None
_unified_scorer = None

class TextInput(BaseModel):
    text: str
    layers: List[str] = ["layer1", "layer2", "layer3"]  # Which layers to analyze
    include_unified: bool = False

class BatchTextInput(BaseModel):
    texts: List[str]
    layers: List[str] = ["layer1", "layer2", "layer3"]
    include_unified: bool = False

class CompleteAnalysisResponse(BaseModel):
    text: str
    layer1_result: Optional[dict] = None
    layer2_result: Optional[dict] = None
    layer3_result: Optional[dict] = None
    unified_result: Optional[dict] = None
    summary: dict = {}
    processing_time: float = 0.0

def get_analyzers():
    global _lexicon_analyzer, _emotion_analyzer, _football_analyzer, _unified_scorer
    
    if _lexicon_analyzer is None:
        _lexicon_analyzer = EnhancedTimnasSentimentAnalyzer()
    if _emotion_analyzer is None:
        _emotion_analyzer = BasicEmotionsAnalyzer()
    if _football_analyzer is None:
        _football_analyzer = FootballEmotionsAnalyzer()
    if _unified_scorer is None:
        _unified_scorer = get_unified_scorer()
    
    return _lexicon_analyzer, _emotion_analyzer, _football_analyzer, _unified_scorer

# Cache for frequent analyses
from functools import lru_cache
import hashlib

@lru_cache(maxsize=1000)
def cached_analysis(text_hash: str, layers_str: str):
    """Cached analysis for repeated texts"""
    return None  # Will be populated by actual analysis

def get_text_hash(text: str) -> str:
    """Generate hash for text caching"""
    return hashlib.md5(text.encode()).hexdigest()[:16]

@app.get("/health")
async def health_check():
    lexicon_analyzer, emotion_analyzer, football_analyzer, _ = get_analyzers()
    
    return {
        "status": "healthy",
        "version": "10.0.0",
        "total_lexicon_words": 6500,
        "layers": {
            "layer1": {"words": 1500, "categories": 3},
            "layer2": {"words": 2000, "categories": 4}, 
            "layer3": {"words": 3000, "categories": 6}
        },
        "models": ["multi-layer-lexicon", "unified-scorer"],
        "ready": True
    }

@app.post("/analyze", response_model=CompleteAnalysisResponse)
async def complete_analysis(input_data: TextInput):
    """Complete multi-layer sentiment analysis"""
    import time
    start_time = time.time()
    
    try:
        lexicon_analyzer, emotion_analyzer, football_analyzer, unified_scorer = get_analyzers()
        
        result = CompleteAnalysisResponse(text=input_data.text)
        
        # Layer 1: Core Sentiment
        if "layer1" in input_data.layers:
            layer1_result = lexicon_analyzer.calculate_sentiment_score(input_data.text)
            coverage1 = lexicon_analyzer.get_lexicon_coverage(input_data.text)
            
            result.layer1_result = {
                "sentiment": layer1_result['label'],
                "confidence": layer1_result['confidence'],
                "score": layer1_result['score'],
                "words_found": layer1_result['words_found'],
                "coverage": coverage1['coverage_percentage'],
                "layer": "Core Sentiment"
            }
        
        # Layer 2: Basic Emotions
        if "layer2" in input_data.layers:
            layer2_result = emotion_analyzer.calculate_emotion_scores(input_data.text)
            coverage2 = emotion_analyzer.get_emotion_coverage(input_data.text)
            
            result.layer2_result = {
                "primary_emotion": layer2_result['primary_emotion'],
                "emotion_scores": layer2_result['emotion_scores'],
                "confidence": layer2_result['confidence'],
                "words_found": len(layer2_result['words_found']),
                "coverage": coverage2['coverage_percentage'],
                "layer": "Basic Emotions"
            }
        
        # Layer 3: Football-Specific Emotions
        if "layer3" in input_data.layers:
            layer3_result = football_analyzer.calculate_football_emotion_scores(input_data.text)
            coverage3 = football_analyzer.get_football_emotion_coverage(input_data.text)
            
            result.layer3_result = {
                "primary_emotion": layer3_result['primary_emotion'],
                "emotion_scores": layer3_result['emotion_scores'],
                "confidence": layer3_result['confidence'],
                "words_found": len(layer3_result['words_found']),
                "coverage": coverage3['coverage_percentage'],
                "layer": "Football-Specific Emotions"
            }
        
        # Unified Model (optional)
        if input_data.include_unified:
            unified_result = unified_scorer.analyze_sentiment(input_data.text, "unified")
            result.unified_result = {
                "sentiment": unified_result['sentiment'],
                "confidence": unified_result['confidence'],
                "reasoning": unified_result['reasoning'],
                "model": unified_result['model']
            }
        
        # Summary
        result.summary = {
            "layers_analyzed": len(input_data.layers),
            "total_coverage": sum([
                result.layer1_result['coverage'] if result.layer1_result else 0,
                result.layer2_result['coverage'] if result.layer2_result else 0,
                result.layer3_result['coverage'] if result.layer3_result else 0
            ]) / len(input_data.layers),
            "dominant_sentiment": result.layer1_result['sentiment'] if result.layer1_result else "unknown",
            "dominant_emotion": result.layer3_result['primary_emotion'] if result.layer3_result else "unknown"
        }
        
        result.processing_time = round(time.time() - start_time, 3)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/analyze-batch")
async def batch_analysis(input_data: BatchTextInput):
    """Batch multi-layer analysis"""
    import time
    start_time = time.time()
    
    try:
        results = []
        
        for text in input_data.texts:
            single_input = TextInput(
                text=text,
                layers=input_data.layers,
                include_unified=input_data.include_unified
            )
            result = await complete_analysis(single_input)
            results.append(result.dict())
        
        processing_time = round(time.time() - start_time, 3)
        
        return {
            "results": results,
            "total_texts": len(input_data.texts),
            "layers_analyzed": input_data.layers,
            "processing_time": processing_time,
            "avg_time_per_text": round(processing_time / len(input_data.texts), 3)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch analysis failed: {str(e)}")

@app.get("/test-suite")
async def comprehensive_test():
    """Comprehensive test suite for all layers"""
    test_cases = [
        {
            "text": "Sangat bangga dengan Garuda, tetap semangat untuk masa depan!",
            "expected_layer1": "positive",
            "expected_layer2": "Dukungan", 
            "expected_layer3": "Future Hope"
        },
        {
            "text": "STY goblok parah, strategi salah total banget!",
            "expected_layer1": "negative",
            "expected_layer2": "Kemarahan",
            "expected_layer3": "Strategic Frustration"
        },
        {
            "text": "Hancur lebur mimpi PD 2026, patah hati Garuda",
            "expected_layer1": "negative", 
            "expected_layer2": "Kekecewaan",
            "expected_layer3": "Passionate Disappointment"
        },
        {
            "text": "Malu jadi orang Indo, Garuda jatuh tragis",
            "expected_layer1": "negative",
            "expected_layer2": "Kekecewaan", 
            "expected_layer3": "Patriotic Sadness"
        },
        {
            "text": "Harus berubah PSSI, ganti pelatih sekarang!",
            "expected_layer1": "negative",
            "expected_layer2": "Kemarahan",
            "expected_layer3": "Constructive Anger"
        },
        {
            "text": "Respect lawan, Irak memang lebih baik",
            "expected_layer1": "positive",
            "expected_layer2": "Dukungan",
            "expected_layer3": "Respectful Acknowledgment"
        }
    ]
    
    test_results = []
    correct_predictions = {"layer1": 0, "layer2": 0, "layer3": 0}
    
    for i, case in enumerate(test_cases):
        input_data = TextInput(text=case["text"])
        result = await complete_analysis(input_data)
        
        # Check predictions
        layer1_correct = result.layer1_result["sentiment"] == case["expected_layer1"]
        layer2_correct = result.layer2_result["primary_emotion"] == case["expected_layer2"]
        layer3_correct = result.layer3_result["primary_emotion"] == case["expected_layer3"]
        
        if layer1_correct:
            correct_predictions["layer1"] += 1
        if layer2_correct:
            correct_predictions["layer2"] += 1
        if layer3_correct:
            correct_predictions["layer3"] += 1
        
        test_results.append({
            "test_case": i + 1,
            "text": case["text"],
            "predictions": {
                "layer1": result.layer1_result["sentiment"],
                "layer2": result.layer2_result["primary_emotion"],
                "layer3": result.layer3_result["primary_emotion"]
            },
            "expected": {
                "layer1": case["expected_layer1"],
                "layer2": case["expected_layer2"], 
                "layer3": case["expected_layer3"]
            },
            "correct": {
                "layer1": layer1_correct,
                "layer2": layer2_correct,
                "layer3": layer3_correct
            },
            "confidences": {
                "layer1": result.layer1_result["confidence"],
                "layer2": result.layer2_result["confidence"],
                "layer3": result.layer3_result["confidence"]
            }
        })
    
    # Calculate accuracy
    total_cases = len(test_cases)
    accuracy = {
        "layer1": round(correct_predictions["layer1"] / total_cases * 100, 1),
        "layer2": round(correct_predictions["layer2"] / total_cases * 100, 1),
        "layer3": round(correct_predictions["layer3"] / total_cases * 100, 1)
    }
    
    return {
        "test_results": test_results,
        "accuracy": accuracy,
        "summary": {
            "total_test_cases": total_cases,
            "overall_accuracy": round(sum(accuracy.values()) / 3, 1),
            "best_layer": max(accuracy, key=accuracy.get),
            "status": "PASSED" if all(acc >= 80 for acc in accuracy.values()) else "NEEDS_IMPROVEMENT"
        }
    }

@app.get("/performance-benchmark")
async def performance_benchmark():
    """Performance benchmark for processing speed"""
    import time
    
    # Test texts of varying lengths
    test_texts = [
        "Bagus",  # Short
        "Timnas Indonesia main bagus hari ini",  # Medium
        "Sangat kecewa dengan performa timnas yang hancur lebur, STY goblok parah strateginya salah total, harus berubah PSSI sekarang juga untuk masa depan yang lebih baik",  # Long
    ]
    
    benchmark_results = []
    
    for i, text in enumerate(test_texts):
        # Single analysis benchmark
        start_time = time.time()
        input_data = TextInput(text=text)
        result = await complete_analysis(input_data)
        single_time = time.time() - start_time
        
        # Batch analysis benchmark (10x same text)
        start_time = time.time()
        batch_input = BatchTextInput(texts=[text] * 10)
        batch_result = await batch_analysis(batch_input)
        batch_time = time.time() - start_time
        
        benchmark_results.append({
            "text_type": ["short", "medium", "long"][i],
            "text_length": len(text),
            "single_analysis_time": round(single_time, 4),
            "batch_analysis_time": round(batch_time, 4),
            "batch_avg_per_text": round(batch_time / 10, 4),
            "words_processed": len(text.split()),
            "total_coverage": result.summary["total_coverage"]
        })
    
    return {
        "benchmark_results": benchmark_results,
        "performance_summary": {
            "avg_single_time": round(sum(r["single_analysis_time"] for r in benchmark_results) / 3, 4),
            "avg_batch_time": round(sum(r["batch_avg_per_text"] for r in benchmark_results) / 3, 4),
            "throughput_per_second": round(1 / (sum(r["single_analysis_time"] for r in benchmark_results) / 3), 1),
            "status": "OPTIMAL" if all(r["single_analysis_time"] < 0.5 for r in benchmark_results) else "NEEDS_OPTIMIZATION"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
