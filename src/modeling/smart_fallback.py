"""Smart Fallback Sentiment Analysis - Enhanced Rule-based System."""
import re
from typing import Dict, List
import logging

class SmartFallbackAnalyzer:
    def __init__(self):
        """Initialize smart fallback analyzer."""
        self.logger = logging.getLogger(__name__)
        
        # Enhanced Indonesian sentiment lexicon
        self.positive_words = {
            'bagus': 0.8, 'hebat': 0.9, 'mantap': 0.8, 'keren': 0.7, 'semangat': 0.7,
            'bangga': 0.8, 'sukses': 0.9, 'luar biasa': 0.9, 'puas': 0.8, 'senang': 0.7,
            'suka': 0.6, 'recommended': 0.8, 'excellent': 0.9, 'good': 0.7, 'great': 0.8,
            'amazing': 0.9, 'perfect': 0.9, 'love': 0.8, 'best': 0.9, 'fantastic': 0.9,
            'juara': 0.9, 'menang': 0.8, 'gol': 0.7, 'victory': 0.8, 'win': 0.8
        }
        
        self.negative_words = {
            'jelek': 0.8, 'buruk': 0.8, 'kecewa': 0.9, 'gagal': 0.9, 'payah': 0.8,
            'lemah': 0.7, 'hancur': 0.9, 'mengecewakan': 0.9, 'marah': 0.8, 'benci': 0.9,
            'tidak suka': 0.8, 'bad': 0.7, 'terrible': 0.9, 'awful': 0.9, 'hate': 0.9,
            'worst': 0.9, 'kalah': 0.8, 'lose': 0.8, 'defeat': 0.8, 'fail': 0.8
        }
        
        # Intensifiers
        self.intensifiers = {
            'sangat': 1.3, 'sekali': 1.2, 'banget': 1.2, 'bgt': 1.2, 'very': 1.2,
            'really': 1.2, 'extremely': 1.4, 'super': 1.3, 'totally': 1.3
        }
        
        # Negations
        self.negations = ['tidak', 'bukan', 'gak', 'ga', 'nggak', 'no', 'not', 'never']
    
    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess text."""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs, mentions, hashtags
        text = re.sub(r'http\S+|www\S+|@\w+|#\w+', '', text)
        
        # Normalize Indonesian slang
        slang_map = {
            'gak': 'tidak', 'ga': 'tidak', 'nggak': 'tidak',
            'banget': 'sangat', 'bgt': 'sangat',
            'yg': 'yang', 'dgn': 'dengan', 'utk': 'untuk',
            'klo': 'kalau', 'krn': 'karena', 'tp': 'tapi'
        }
        
        for slang, formal in slang_map.items():
            text = re.sub(r'\b' + slang + r'\b', formal, text)
        
        # Clean extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment using enhanced rule-based approach."""
        if not text or len(text.strip()) < 2:
            return {
                'sentiment': 'neutral',
                'confidence': 0.5,
                'reasoning': 'Text too short for analysis'
            }
        
        # Preprocess
        clean_text = self.preprocess_text(text)
        words = clean_text.split()
        
        positive_score = 0.0
        negative_score = 0.0
        
        # Analyze each word with context
        for i, word in enumerate(words):
            # Check for negation in previous words
            negated = any(neg in words[max(0, i-2):i] for neg in self.negations)
            
            # Check for intensifiers in previous words
            intensifier = 1.0
            for j in range(max(0, i-2), i):
                if words[j] in self.intensifiers:
                    intensifier = self.intensifiers[words[j]]
                    break
            
            # Calculate sentiment scores
            if word in self.positive_words:
                score = self.positive_words[word] * intensifier
                if negated:
                    negative_score += score
                else:
                    positive_score += score
            
            elif word in self.negative_words:
                score = self.negative_words[word] * intensifier
                if negated:
                    positive_score += score
                else:
                    negative_score += score
        
        # Determine final sentiment
        if positive_score > negative_score:
            sentiment = 'positive'
            confidence = min(0.95, 0.6 + (positive_score - negative_score) * 0.1)
            reasoning = f"Positive indicators (score: {positive_score:.1f} vs {negative_score:.1f})"
        elif negative_score > positive_score:
            sentiment = 'negative'
            confidence = min(0.95, 0.6 + (negative_score - positive_score) * 0.1)
            reasoning = f"Negative indicators (score: {negative_score:.1f} vs {positive_score:.1f})"
        else:
            sentiment = 'neutral'
            confidence = 0.6
            reasoning = "No strong sentiment indicators detected"
        
        return {
            'sentiment': sentiment,
            'confidence': confidence,
            'reasoning': reasoning
        }

# Global instance
_fallback_analyzer = None

def get_fallback_analyzer():
    """Get or create fallback analyzer instance."""
    global _fallback_analyzer
    if _fallback_analyzer is None:
        _fallback_analyzer = SmartFallbackAnalyzer()
    return _fallback_analyzer

def analyze_with_fallback(text: str) -> Dict:
    """Quick sentiment analysis with smart fallback."""
    analyzer = get_fallback_analyzer()
    return analyzer.analyze_sentiment(text)

if __name__ == "__main__":
    # Test the fallback analyzer
    analyzer = SmartFallbackAnalyzer()
    
    test_comments = [
        "Produk ini sangat bagus dan berkualitas tinggi!",
        "Pelayanan buruk sekali, sangat mengecewakan",
        "Biasa aja sih, tidak ada yang istimewa",
        "Mantap banget! Puas bgt sama hasilnya",
        "Jelek parah, buang-buang uang aja",
        "Timnas Indonesia juara! Sangat bangga!",
        "Kalah lagi, payah sekali performanya"
    ]
    
    print("🧠 Testing Smart Fallback Analyzer:")
    print("=" * 50)
    
    for comment in test_comments:
        result = analyzer.analyze_sentiment(comment)
        print(f"Text: {comment}")
        print(f"Result: {result['sentiment']} ({result['confidence']:.2f}) - {result['reasoning']}")
        print("-" * 40)
