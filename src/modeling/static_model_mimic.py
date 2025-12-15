"""Static Model Mimic - Enhanced Rule-based System to Mimic Dashboard Models."""
import joblib
import pandas as pd
import numpy as np
import json
from typing import Dict, List
import logging
import warnings
import re
warnings.filterwarnings('ignore')

class StaticModelMimic:
    def __init__(self):
        """Initialize static model mimic system."""
        self.logger = logging.getLogger(__name__)
        
        # Load model performance data
        self.load_model_characteristics()
        
        # Enhanced Indonesian sentiment patterns based on static model behavior
        self.sentiment_patterns = self._build_sentiment_patterns()
    
    def load_model_characteristics(self):
        """Load characteristics of static models."""
        try:
            # Load performance summary
            with open('data/models/performance_summary.json', 'r') as f:
                self.performance_data = json.load(f)
            
            # Load model comparison data
            with open('data/models/model_comparison.json', 'r') as f:
                self.comparison_data = json.load(f)
            
            self.logger.info("✅ Loaded model characteristics")
        except Exception as e:
            self.logger.error(f"❌ Failed to load model data: {e}")
            self.performance_data = {}
            self.comparison_data = {}
    
    def _build_sentiment_patterns(self):
        """Build sentiment patterns based on static model behavior."""
        return {
            'positive': {
                'strong': [
                    r'\b(sangat bagus|luar biasa|excellent|fantastic|amazing|perfect)\b',
                    r'\b(mantap sekali|keren banget|hebat sekali)\b',
                    r'\b(puas banget|senang sekali|bangga sekali)\b'
                ],
                'medium': [
                    r'\b(bagus|mantap|keren|hebat|good|great|nice)\b',
                    r'\b(puas|senang|suka|bangga|recommended)\b',
                    r'\b(juara|menang|gol|victory|win|sukses)\b'
                ],
                'weak': [
                    r'\b(lumayan|cukup|ok|okay|fine|baik)\b',
                    r'\b(bisa|dapat|mampu|sanggup)\b'
                ]
            },
            'negative': {
                'strong': [
                    r'\b(sangat jelek|sangat buruk|terrible|awful|horrible)\b',
                    r'\b(kecewa sekali|marah sekali|benci sekali)\b',
                    r'\b(payah banget|lemah sekali|hancur total)\b'
                ],
                'medium': [
                    r'\b(jelek|buruk|kecewa|gagal|payah|lemah|bad|terrible)\b',
                    r'\b(marah|benci|hate|angry|kalah|lose|defeat)\b',
                    r'\b(mengecewakan|tidak suka|don\'t like)\b'
                ],
                'weak': [
                    r'\b(kurang|tidak|bukan|gak|ga|nggak)\b',
                    r'\b(salah|wrong|mistake|error)\b'
                ]
            },
            'neutral': {
                'indicators': [
                    r'\b(biasa|normal|standar|rata-rata|average)\b',
                    r'\b(mungkin|perhaps|maybe|kayaknya)\b',
                    r'\b(tidak tahu|don\'t know|entah)\b'
                ]
            },
            'questions': [
                r'\b(kenapa|why|mengapa|gimana|bagaimana|how|kapan|when|dimana|where)\b',
                r'\?'
            ]
        }
    
    def analyze_with_static_model_style(self, text: str) -> Dict:
        """Analyze sentiment mimicking static dashboard model behavior."""
        
        if not text or len(text.strip()) < 2:
            return self._create_result('neutral', 0.5, 'Text too short')
        
        text_lower = text.lower()
        
        # Calculate sentiment scores based on patterns
        positive_score = self._calculate_sentiment_score(text_lower, 'positive')
        negative_score = self._calculate_sentiment_score(text_lower, 'negative')
        neutral_score = self._calculate_sentiment_score(text_lower, 'neutral')
        question_score = self._calculate_question_score(text_lower)
        
        # Adjust scores based on static model characteristics
        # Static model tends to be more conservative (like SVM with 73.4% accuracy)
        conservative_factor = 0.85  # Mimic static model conservatism
        
        positive_score *= conservative_factor
        negative_score *= conservative_factor
        
        # Questions often indicate negative sentiment in football context
        if question_score > 0:
            negative_score += question_score * 0.3
        
        # Determine final sentiment (mimicking static model decision boundaries)
        total_score = positive_score + negative_score + neutral_score
        
        if total_score == 0:
            return self._create_result('neutral', 0.6, 'No clear indicators (static model style)')
        
        # Mimic static model thresholds
        pos_ratio = positive_score / total_score
        neg_ratio = negative_score / total_score
        
        # Static model decision logic (conservative thresholds)
        if pos_ratio > 0.4 and pos_ratio > neg_ratio:
            confidence = min(0.9, 0.6 + pos_ratio * 0.3)
            return self._create_result('positive', confidence, f'Positive patterns detected (score: {positive_score:.2f})')
        elif neg_ratio > 0.4 and neg_ratio > pos_ratio:
            confidence = min(0.9, 0.6 + neg_ratio * 0.3)
            return self._create_result('negative', confidence, f'Negative patterns detected (score: {negative_score:.2f})')
        else:
            confidence = 0.55 + (neutral_score / total_score) * 0.2
            return self._create_result('neutral', confidence, f'Mixed or neutral patterns (pos: {pos_ratio:.2f}, neg: {neg_ratio:.2f})')
    
    def _calculate_sentiment_score(self, text: str, sentiment_type: str) -> float:
        """Calculate sentiment score for given type."""
        if sentiment_type not in self.sentiment_patterns:
            return 0.0
        
        score = 0.0
        patterns = self.sentiment_patterns[sentiment_type]
        
        if sentiment_type in ['positive', 'negative']:
            # Strong patterns
            for pattern in patterns.get('strong', []):
                matches = len(re.findall(pattern, text))
                score += matches * 3.0
            
            # Medium patterns
            for pattern in patterns.get('medium', []):
                matches = len(re.findall(pattern, text))
                score += matches * 2.0
            
            # Weak patterns
            for pattern in patterns.get('weak', []):
                matches = len(re.findall(pattern, text))
                score += matches * 1.0
        else:
            # Neutral indicators
            for pattern in patterns.get('indicators', []):
                matches = len(re.findall(pattern, text))
                score += matches * 1.5
        
        return score
    
    def _calculate_question_score(self, text: str) -> float:
        """Calculate question score."""
        score = 0.0
        for pattern in self.sentiment_patterns['questions']:
            matches = len(re.findall(pattern, text))
            score += matches * 1.0
        return score
    
    def _create_result(self, sentiment: str, confidence: float, reasoning: str) -> Dict:
        """Create standardized result."""
        return {
            'sentiment': sentiment,
            'confidence': confidence,
            'reasoning': reasoning,
            'model': 'Static-Model-Mimic',
            'mimic_info': {
                'mimics': 'SVM Pipeline (73.4% accuracy)',
                'characteristics': 'Conservative, rule-based patterns',
                'decision_style': 'Threshold-based classification'
            }
        }
    
    def batch_analyze(self, texts: List[str]) -> List[Dict]:
        """Analyze multiple texts."""
        results = []
        for text in texts:
            result = self.analyze_with_static_model_style(text)
            results.append(result)
        return results
    
    def get_model_info(self) -> Dict:
        """Get information about the mimic system."""
        return {
            'mimic_target': 'Static Dashboard Models',
            'primary_model': 'SVM Pipeline',
            'accuracy_target': '73.4%',
            'characteristics': {
                'conservative_thresholds': True,
                'rule_based_patterns': True,
                'indonesian_optimized': True,
                'football_context_aware': True
            },
            'performance_data': self.performance_data,
            'comparison_data': self.comparison_data
        }

# Global instance
_static_model_mimic = None

def get_static_model_mimic():
    """Get or create static model mimic instance."""
    global _static_model_mimic
    if _static_model_mimic is None:
        _static_model_mimic = StaticModelMimic()
    return _static_model_mimic

def analyze_like_static_dashboard(text: str) -> Dict:
    """Quick analysis mimicking static dashboard models."""
    mimic = get_static_model_mimic()
    return mimic.analyze_with_static_model_style(text)

if __name__ == "__main__":
    # Test static model mimic
    mimic = StaticModelMimic()
    
    print("📊 Testing Static Model Mimic System:")
    print("=" * 60)
    
    # Show model info
    model_info = mimic.get_model_info()
    print(f"🎯 Target Model: {model_info['primary_model']}")
    print(f"📈 Target Accuracy: {model_info['accuracy_target']}")
    
    # Test predictions
    test_texts = [
        "Timnas Indonesia main sangat bagus hari ini",
        "Kecewa dengan performa pemain yang jelek",
        "Biasa aja permainannya tidak istimewa",
        "Kenapa selalu kalah sih timnas kita?",
        "Mantap sekali permainannya, bangga!",
        "Jelek banget performanya, payah",
        "Lumayan lah hasilnya cukup memuaskan"
    ]
    
    print(f"\n🔍 Testing on {len(test_texts)} texts:")
    print("-" * 60)
    
    results = mimic.batch_analyze(test_texts)
    
    for i, (text, result) in enumerate(zip(test_texts, results)):
        sentiment = result['sentiment']
        confidence = result['confidence']
        reasoning = result['reasoning']
        
        # Color coding
        color = "🟢" if sentiment == "positive" else "🔴" if sentiment == "negative" else "🟡"
        
        print(f"{i+1}. {color} {sentiment.upper()} ({confidence:.2f})")
        print(f"   Text: {text}")
        print(f"   Reasoning: {reasoning}")
        print()
    
    # Summary
    sentiment_counts = {}
    for result in results:
        sentiment = result['sentiment']
        sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
    
    print("📊 Results Summary:")
    for sentiment, count in sentiment_counts.items():
        percentage = (count / len(results)) * 100
        print(f"   {sentiment.capitalize()}: {count}/{len(results)} ({percentage:.1f}%)")
    
    print(f"\n✅ Static Model Mimic working successfully!")
    print(f"🎯 Mimicking: {model_info['primary_model']} behavior")
