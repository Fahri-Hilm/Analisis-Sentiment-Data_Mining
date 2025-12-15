"""Sensitive Sentiment Analyzer - Better Detection for Indonesian Comments."""
import re
from typing import Dict
import logging

class SensitiveSentimentAnalyzer:
    def __init__(self):
        """Initialize sensitive analyzer with comprehensive lexicon."""
        self.logger = logging.getLogger(__name__)
        
        # Expanded positive indicators
        self.positive_patterns = {
            # Direct positive words
            r'\b(bagus|hebat|mantap|keren|amazing|excellent|good|great|perfect|love|best|fantastic)\b': 0.8,
            r'\b(puas|senang|suka|bangga|recommended|juara|menang|gol|victory|win|sukses)\b': 0.7,
            r'\b(luar biasa|sangat bagus|very good|so good|really good)\b': 0.9,
            
            # Positive expressions
            r'\b(semangat|ayo|gas|let\'s go|come on)\b': 0.6,
            r'\b(terima kasih|thanks|thank you)\b': 0.5,
            r'\b(setuju|agree|support|dukung)\b': 0.6,
            
            # Positive emojis/expressions
            r'(👍|😊|😍|🔥|💪|❤️|♥️)': 0.7,
            r'\b(wkwk|haha|hehe|lol)\b': 0.4,
        }
        
        # Expanded negative indicators  
        self.negative_patterns = {
            # Direct negative words
            r'\b(jelek|buruk|kecewa|gagal|payah|lemah|hancur|mengecewakan|terrible|awful|bad|worst)\b': 0.8,
            r'\b(marah|benci|hate|angry|mad|furious)\b': 0.9,
            r'\b(kalah|lose|defeat|fail|disaster)\b': 0.7,
            
            # Negative expressions
            r'\b(tidak suka|don\'t like|hate it|gak suka|ga suka)\b': 0.8,
            r'\b(bodoh|stupid|idiot|tolol|goblok)\b': 0.9,
            r'\b(sampah|trash|garbage|waste)\b': 0.8,
            
            # Criticism patterns
            r'\b(kenapa|why|mengapa)\s+(tidak|gak|ga|nggak|never|no)\b': 0.6,
            r'\b(harusnya|should|seharusnya)\b': 0.5,
            r'\b(salah|wrong|mistake|error)\b': 0.6,
            
            # Negative emojis
            r'(👎|😞|😠|😡|💔|😢|😭)': 0.8,
        }
        
        # Context patterns that indicate sentiment
        self.context_patterns = {
            # Positive contexts
            r'\b(semoga|hope|mudah-mudahan)\s+\w+\s+(menang|juara|sukses|bagus)\b': 0.7,
            r'\b(bangga|proud)\s+(dengan|of|sama)\b': 0.8,
            r'\b(terima kasih|thanks)\s+(untuk|for|buat)\b': 0.6,
            
            # Negative contexts  
            r'\b(kenapa|why)\s+(selalu|always|terus|sering)\s+\w*\s*(kalah|gagal|jelek)\b': 0.8,
            r'\b(sudah|already|udah)\s+(muak|bosan|tired|fed up)\b': 0.7,
            r'\b(jangan|don\'t|stop)\s+\w*\s*(lagi|again|more)\b': 0.6,
        }
        
        # Intensifiers
        self.intensifiers = {
            r'\b(sangat|very|really|extremely|super|banget|bgt|sekali)\b': 1.3,
            r'\b(agak|sedikit|little|bit|slightly)\b': 0.7,
            r'\b(terlalu|too|overly)\b': 1.2,
        }
        
        # Negations
        self.negations = [
            r'\b(tidak|bukan|gak|ga|nggak|no|not|never|don\'t|doesn\'t|won\'t)\b'
        ]
    
    def preprocess_text(self, text: str) -> str:
        """Enhanced preprocessing."""
        if not text:
            return ""
        
        text = text.lower()
        
        # Normalize common Indonesian internet slang
        slang_map = {
            'gak': 'tidak', 'ga': 'tidak', 'nggak': 'tidak',
            'banget': 'sangat', 'bgt': 'sangat', 'bgt': 'sangat',
            'yg': 'yang', 'dgn': 'dengan', 'utk': 'untuk',
            'krn': 'karena', 'tp': 'tapi', 'klo': 'kalau',
            'udah': 'sudah', 'blm': 'belum', 'jgn': 'jangan',
            'gmn': 'gimana', 'knp': 'kenapa', 'emg': 'memang'
        }
        
        for slang, formal in slang_map.items():
            text = re.sub(r'\b' + slang + r'\b', formal, text)
        
        return text.strip()
    
    def analyze_sentiment(self, text: str) -> Dict:
        """Analyze with enhanced sensitivity."""
        if not text or len(text.strip()) < 2:
            return {
                'sentiment': 'neutral',
                'confidence': 0.5,
                'reasoning': 'Text too short'
            }
        
        clean_text = self.preprocess_text(text)
        
        positive_score = 0.0
        negative_score = 0.0
        reasons = []
        
        # Check for negation context
        has_negation = any(re.search(neg, clean_text) for neg in self.negations)
        
        # Find intensifiers
        intensifier_multiplier = 1.0
        for pattern, multiplier in self.intensifiers.items():
            if re.search(pattern, clean_text):
                intensifier_multiplier = max(intensifier_multiplier, multiplier)
                break
        
        # Analyze positive patterns
        for pattern, weight in self.positive_patterns.items():
            matches = re.findall(pattern, clean_text)
            if matches:
                score = len(matches) * weight * intensifier_multiplier
                if has_negation:
                    negative_score += score
                    reasons.append(f"Negated positive: {matches}")
                else:
                    positive_score += score
                    reasons.append(f"Positive: {matches}")
        
        # Analyze negative patterns
        for pattern, weight in self.negative_patterns.items():
            matches = re.findall(pattern, clean_text)
            if matches:
                score = len(matches) * weight * intensifier_multiplier
                if has_negation:
                    positive_score += score
                    reasons.append(f"Negated negative: {matches}")
                else:
                    negative_score += score
                    reasons.append(f"Negative: {matches}")
        
        # Analyze context patterns
        for pattern, weight in self.context_patterns.items():
            if re.search(pattern, clean_text):
                if 'menang|juara|sukses|bagus|bangga|thanks' in pattern:
                    positive_score += weight
                    reasons.append("Positive context")
                else:
                    negative_score += weight
                    reasons.append("Negative context")
        
        # Lower threshold for classification
        threshold = 0.3  # More sensitive threshold
        
        if positive_score > negative_score + threshold:
            sentiment = 'positive'
            confidence = min(0.95, 0.55 + (positive_score - negative_score) * 0.15)
        elif negative_score > positive_score + threshold:
            sentiment = 'negative'
            confidence = min(0.95, 0.55 + (negative_score - positive_score) * 0.15)
        else:
            sentiment = 'neutral'
            confidence = 0.5 + abs(positive_score - negative_score) * 0.1
        
        reasoning = f"Pos:{positive_score:.1f} Neg:{negative_score:.1f} - {'; '.join(reasons[:2])}" if reasons else "No clear indicators"
        
        return {
            'sentiment': sentiment,
            'confidence': confidence,
            'reasoning': reasoning
        }

# Global instance
_sensitive_analyzer = None

def get_sensitive_analyzer():
    """Get or create sensitive analyzer instance."""
    global _sensitive_analyzer
    if _sensitive_analyzer is None:
        _sensitive_analyzer = SensitiveSentimentAnalyzer()
    return _sensitive_analyzer

def analyze_with_sensitivity(text: str) -> Dict:
    """Quick sentiment analysis with high sensitivity."""
    analyzer = get_sensitive_analyzer()
    return analyzer.analyze_sentiment(text)

if __name__ == "__main__":
    # Test the sensitive analyzer
    analyzer = SensitiveSentimentAnalyzer()
    
    test_comments = [
        "Eric Tohir tuh megang inter Milan jja gx bisa hasilnya jelek",
        "Kenapa selalu kalah sih timnas kita",
        "Semoga menang ya timnas Indonesia",
        "Bangga sama pemain kita",
        "Harusnya main lebih bagus lagi",
        "Sudah muak lihat permainan kayak gini",
        "Mantap sekali permainannya 👍",
        "Jelek banget performanya 👎"
    ]
    
    print("🎯 Testing Sensitive Analyzer:")
    print("=" * 50)
    
    for comment in test_comments:
        result = analyzer.analyze_sentiment(comment)
        print(f"Text: {comment}")
        print(f"Result: {result['sentiment']} ({result['confidence']:.2f}) - {result['reasoning']}")
        print("-" * 40)
