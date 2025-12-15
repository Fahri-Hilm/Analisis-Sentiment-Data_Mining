"""
Unified Sentiment Scoring System
Ensures consistent scoring between static dashboard and real-time analysis
"""
import re
import json
from typing import Dict, List, Tuple
from pathlib import Path

class UnifiedSentimentScorer:
    """Unified scoring system for both static and real-time models."""
    
    def __init__(self):
        """Initialize unified scorer with consistent patterns and thresholds."""
        self.version = "1.0.0"
        self.model_name = "Unified-Sentiment-Scorer"
        
        # Consistent scoring patterns for both systems
        self.sentiment_lexicon = self._build_unified_lexicon()
        self.scoring_weights = self._build_scoring_weights()
        self.thresholds = self._build_unified_thresholds()
        
    def _build_unified_lexicon(self) -> Dict:
        """Build unified sentiment lexicon for consistent scoring."""
        return {
            'positive': {
                'strong': {
                    'words': ['sangat bagus', 'luar biasa', 'excellent', 'fantastic', 'amazing', 'perfect',
                             'mantap sekali', 'keren banget', 'hebat sekali', 'puas banget', 'senang sekali',
                             'bangga sekali', 'juara banget', 'sukses besar'],
                    'weight': 3.0
                },
                'medium': {
                    'words': ['bagus', 'mantap', 'keren', 'hebat', 'good', 'great', 'nice', 'puas', 
                             'senang', 'suka', 'bangga', 'recommended', 'juara', 'menang', 'gol', 
                             'victory', 'win', 'sukses', 'berhasil', 'oke', 'solid'],
                    'weight': 2.0
                },
                'weak': {
                    'words': ['lumayan', 'cukup', 'ok', 'okay', 'fine', 'baik', 'bisa', 'dapat', 
                             'mampu', 'sanggup', 'tidak buruk', 'tidak jelek'],
                    'weight': 1.0
                }
            },
            'negative': {
                'strong': {
                    'words': ['sangat jelek', 'sangat buruk', 'terrible', 'awful', 'horrible', 'disaster',
                             'kecewa sekali', 'marah sekali', 'benci sekali', 'payah banget', 'lemah sekali',
                             'hancur total', 'gagal total', 'parah banget'],
                    'weight': 3.0
                },
                'medium': {
                    'words': ['jelek', 'buruk', 'kecewa', 'gagal', 'payah', 'lemah', 'bad', 'terrible',
                             'marah', 'benci', 'hate', 'angry', 'kalah', 'lose', 'defeat', 'mengecewakan',
                             'tidak suka', 'salah', 'wrong', 'mistake', 'error'],
                    'weight': 2.0
                },
                'weak': {
                    'words': ['kurang ', 'tidak ', 'bukan ', 'gak ', 'nggak ', 'belum ', 'jangan ',
                             'minus', 'kurang baik', 'agak jelek'],
                    'weight': 1.0
                }
            },
            'neutral': {
                'indicators': {
                    'words': ['biasa', 'normal', 'standar', 'rata-rata', 'average', 'mungkin', 'perhaps',
                             'maybe', 'kayaknya', 'tidak tahu', 'entah', 'sepertinya', 'kelihatannya'],
                    'weight': 1.5
                }
            },
            'intensifiers': {
                'words': ['sangat', 'sekali', 'banget', 'very', 'really', 'extremely', 'super', 'ultra'],
                'multiplier': 1.3
            },
            'negators': {
                'words': ['tidak ', 'bukan ', 'gak ', 'nggak ', 'jangan ', 'never ', 'no ', 'none '],
                'effect': 'reverse'
            }
        }
    
    def _build_scoring_weights(self) -> Dict:
        """Build consistent scoring weights."""
        return {
            'text_length_bonus': 0.1,  # Bonus for longer, more detailed comments
            'question_penalty': 0.2,   # Questions often indicate problems/concerns
            'exclamation_bonus': 0.15, # Exclamations indicate strong emotions
            'context_bonus': 0.2,      # Football/timnas context bonus
            'repetition_penalty': 0.3  # Penalty for repeated characters
        }
    
    def _build_unified_thresholds(self) -> Dict:
        """Build unified decision thresholds for consistent classification."""
        return {
            'positive_threshold': 0.35,    # Minimum score ratio for positive
            'negative_threshold': 0.35,    # Minimum score ratio for negative
            'confidence_base': 0.6,        # Base confidence level
            'confidence_max': 0.95,        # Maximum confidence level
            'neutral_confidence': 0.65     # Confidence for neutral classification
        }
    
    def analyze_sentiment(self, text: str, model_type: str = "unified") -> Dict:
        """
        Unified sentiment analysis for both static and real-time systems.
        
        Args:
            text: Input text to analyze
            model_type: "static" or "realtime" or "unified"
        
        Returns:
            Dict with sentiment, confidence, reasoning, and scores
        """
        if not text or len(text.strip()) < 2:
            return self._create_result('neutral', 0.5, 'Text too short for analysis', {})
        
        # Calculate base sentiment scores
        scores = self._calculate_sentiment_scores(text)
        
        # Apply model-specific adjustments
        if model_type == "static":
            scores = self._apply_static_model_adjustments(scores, text)
        elif model_type == "realtime":
            scores = self._apply_realtime_model_adjustments(scores, text)
        
        # Determine final sentiment and confidence
        result = self._determine_final_sentiment(scores, text)
        
        # Add model-specific metadata
        result['model_type'] = model_type
        result['scorer_version'] = self.version
        result['raw_scores'] = scores
        
        return result
    
    def _calculate_sentiment_scores(self, text: str) -> Dict:
        """Calculate base sentiment scores using unified lexicon."""
        text_lower = text.lower()
        
        scores = {
            'positive': 0.0,
            'negative': 0.0,
            'neutral': 0.0,
            'modifiers': {
                'intensifiers': 0,
                'negators': 0,
                'questions': 0,
                'exclamations': 0
            }
        }
        
        # Calculate positive scores
        for strength, data in self.sentiment_lexicon['positive'].items():
            for word in data['words']:
                if word in text_lower:
                    scores['positive'] += data['weight']
        
        # Calculate negative scores  
        for strength, data in self.sentiment_lexicon['negative'].items():
            for word in data['words']:
                if word in text_lower:
                    scores['negative'] += data['weight']
        
        # Calculate neutral scores
        for word in self.sentiment_lexicon['neutral']['indicators']['words']:
            if word in text_lower:
                scores['neutral'] += self.sentiment_lexicon['neutral']['indicators']['weight']
        
        # Detect modifiers
        scores['modifiers']['intensifiers'] = sum(1 for word in self.sentiment_lexicon['intensifiers']['words'] 
                                                 if word in text_lower)
        scores['modifiers']['negators'] = sum(1 for word in self.sentiment_lexicon['negators']['words'] 
                                            if word in text_lower)
        scores['modifiers']['questions'] = len(re.findall(r'\?', text))
        scores['modifiers']['exclamations'] = len(re.findall(r'!', text))
        
        # Apply intensifiers
        if scores['modifiers']['intensifiers'] > 0:
            multiplier = self.sentiment_lexicon['intensifiers']['multiplier']
            scores['positive'] *= multiplier
            scores['negative'] *= multiplier
        
        # Apply negation (simple reversal for now)
        if scores['modifiers']['negators'] > 0:
            scores['positive'], scores['negative'] = scores['negative'], scores['positive']
        
        return scores
    
    def _apply_static_model_adjustments(self, scores: Dict, text: str) -> Dict:
        """Apply adjustments to mimic static model behavior (more conservative)."""
        # Static models are more conservative, reduce extreme scores
        conservative_factor = 0.85
        scores['positive'] *= conservative_factor
        scores['negative'] *= conservative_factor
        
        # Static models give more weight to neutral classification
        scores['neutral'] *= 1.2
        
        # Questions slightly favor negative in static model
        if scores['modifiers']['questions'] > 0:
            scores['negative'] += 0.5
        
        return scores
    
    def _apply_realtime_model_adjustments(self, scores: Dict, text: str) -> Dict:
        """Apply adjustments to mimic real-time model behavior (more aggressive)."""
        # Real-time models are more decisive, boost clear signals
        if scores['positive'] > scores['negative']:
            scores['positive'] *= 1.15
        elif scores['negative'] > scores['positive']:
            scores['negative'] *= 1.15
        
        # Real-time models reduce neutral classification
        scores['neutral'] *= 0.8
        
        # Context awareness bonus for football terms
        football_terms = ['timnas', 'indonesia', 'sepak bola', 'football', 'pemain', 'pelatih']
        if any(term in text.lower() for term in football_terms):
            # Boost the dominant sentiment
            if scores['positive'] > scores['negative']:
                scores['positive'] += 0.5
            elif scores['negative'] > scores['positive']:
                scores['negative'] += 0.5
        
        return scores
    
    def _determine_final_sentiment(self, scores: Dict, text: str) -> Dict:
        """Determine final sentiment using unified thresholds."""
        total_score = scores['positive'] + scores['negative'] + scores['neutral']
        
        if total_score == 0:
            return self._create_result('neutral', self.thresholds['neutral_confidence'], 
                                     'No sentiment indicators found', scores)
        
        # Calculate ratios
        pos_ratio = scores['positive'] / total_score
        neg_ratio = scores['negative'] / total_score
        neu_ratio = scores['neutral'] / total_score
        
        # Apply unified thresholds
        if pos_ratio >= self.thresholds['positive_threshold'] and pos_ratio > neg_ratio:
            confidence = self._calculate_confidence(pos_ratio, scores['modifiers'])
            reasoning = f"Positive sentiment detected (score: {scores['positive']:.2f}, ratio: {pos_ratio:.2f})"
            return self._create_result('positive', confidence, reasoning, scores)
        
        elif neg_ratio >= self.thresholds['negative_threshold'] and neg_ratio > pos_ratio:
            confidence = self._calculate_confidence(neg_ratio, scores['modifiers'])
            reasoning = f"Negative sentiment detected (score: {scores['negative']:.2f}, ratio: {neg_ratio:.2f})"
            return self._create_result('negative', confidence, reasoning, scores)
        
        else:
            confidence = self.thresholds['neutral_confidence'] + (neu_ratio * 0.2)
            reasoning = f"Mixed or neutral sentiment (pos: {pos_ratio:.2f}, neg: {neg_ratio:.2f}, neu: {neu_ratio:.2f})"
            return self._create_result('neutral', confidence, reasoning, scores)
    
    def _calculate_confidence(self, ratio: float, modifiers: Dict) -> float:
        """Calculate confidence score based on ratio and modifiers."""
        base_confidence = self.thresholds['confidence_base']
        
        # Boost confidence based on strength of signal
        confidence = base_confidence + (ratio * 0.3)
        
        # Adjust based on modifiers
        if modifiers['intensifiers'] > 0:
            confidence += 0.1
        if modifiers['exclamations'] > 0:
            confidence += 0.05
        if modifiers['questions'] > 0:
            confidence -= 0.05  # Questions indicate uncertainty
        
        return min(self.thresholds['confidence_max'], confidence)
    
    def _create_result(self, sentiment: str, confidence: float, reasoning: str, scores: Dict) -> Dict:
        """Create standardized result format."""
        return {
            'sentiment': sentiment,
            'confidence': round(confidence, 3),
            'reasoning': reasoning,
            'model': self.model_name,
            'version': self.version,
            'scores': {
                'positive': round(scores.get('positive', 0), 2),
                'negative': round(scores.get('negative', 0), 2),
                'neutral': round(scores.get('neutral', 0), 2)
            }
        }
    
    def batch_analyze(self, texts: List[str], model_type: str = "unified") -> List[Dict]:
        """Analyze multiple texts with consistent scoring."""
        return [self.analyze_sentiment(text, model_type) for text in texts]
    
    def get_model_info(self) -> Dict:
        """Get information about the unified scoring system."""
        return {
            'name': self.model_name,
            'version': self.version,
            'description': 'Unified sentiment scoring system for consistent results',
            'supported_models': ['static', 'realtime', 'unified'],
            'features': [
                'Consistent lexicon across models',
                'Unified decision thresholds',
                'Model-specific adjustments',
                'Indonesian language optimized',
                'Football context aware'
            ],
            'thresholds': self.thresholds,
            'lexicon_stats': {
                'positive_terms': sum(len(data['words']) for data in self.sentiment_lexicon['positive'].values()),
                'negative_terms': sum(len(data['words']) for data in self.sentiment_lexicon['negative'].values()),
                'neutral_terms': len(self.sentiment_lexicon['neutral']['indicators']['words'])
            }
        }

# Global instance for consistent usage
_unified_scorer = None

def get_unified_scorer():
    """Get or create unified scorer instance."""
    global _unified_scorer
    if _unified_scorer is None:
        _unified_scorer = UnifiedSentimentScorer()
    return _unified_scorer

def analyze_with_unified_scoring(text: str, model_type: str = "unified") -> Dict:
    """Quick analysis with unified scoring."""
    scorer = get_unified_scorer()
    return scorer.analyze_sentiment(text, model_type)

if __name__ == "__main__":
    # Test unified scoring system
    scorer = UnifiedSentimentScorer()
    
    print("🎯 Testing Unified Sentiment Scoring System")
    print("=" * 60)
    
    test_texts = [
        "Timnas Indonesia main sangat bagus hari ini",
        "Kecewa dengan performa pemain yang jelek", 
        "Biasa aja permainannya tidak istimewa",
        "Kenapa selalu kalah sih timnas kita?",
        "Mantap sekali permainannya, bangga!"
    ]
    
    model_types = ["static", "realtime", "unified"]
    
    for model_type in model_types:
        print(f"\n📊 Testing {model_type.upper()} model behavior:")
        print("-" * 40)
        
        results = scorer.batch_analyze(test_texts, model_type)
        
        for text, result in zip(test_texts, results):
            sentiment = result['sentiment']
            confidence = result['confidence']
            
            color = "🟢" if sentiment == "positive" else "🔴" if sentiment == "negative" else "🟡"
            print(f"{color} {sentiment.upper()} ({confidence:.3f}) - {text[:50]}...")
        
        # Summary
        sentiment_counts = {}
        avg_confidence = 0
        for result in results:
            sentiment = result['sentiment']
            sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
            avg_confidence += result['confidence']
        
        avg_confidence /= len(results)
        
        print(f"Summary: {sentiment_counts}, Avg Confidence: {avg_confidence:.3f}")
    
    print(f"\n✅ Unified Scoring System working successfully!")
