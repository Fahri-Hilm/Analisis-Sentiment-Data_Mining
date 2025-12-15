"""Aggressive Sentiment Analyzer - Minimal Neutral Results."""
import re
from typing import Dict

class AggressiveSentimentAnalyzer:
    def __init__(self):
        """Initialize aggressive analyzer with expanded patterns."""
        
        # Expanded positive indicators (more aggressive detection)
        self.positive_indicators = [
            # Direct positive
            r'\b(bagus|hebat|mantap|keren|good|great|excellent|amazing|perfect|best|fantastic|love|awesome)\b',
            r'\b(puas|senang|suka|bangga|recommended|juara|menang|gol|victory|win|sukses|champion)\b',
            r'\b(semangat|ayo|gas|support|dukung|setuju|agree|terima kasih|thanks)\b',
            
            # Positive context (more liberal)
            r'\b(bisa|can|could|akan|will|hope|semoga|mudah|easy|baik|ok|okay|fine)\b',
            r'\b(lanjut|continue|terus|keep|go|maju|forward|up|naik|rise)\b',
            r'\b(benar|right|correct|tepat|pas|cocok|sesuai|match)\b',
            
            # Emojis and expressions
            r'(👍|😊|😍|🔥|💪|❤️|♥️|😄|😃|🎉|✨|⭐|🌟)',
            r'\b(wkwk|haha|hehe|lol|nice|cool|wow)\b',
        ]
        
        # Expanded negative indicators
        self.negative_indicators = [
            # Direct negative
            r'\b(jelek|buruk|kecewa|gagal|payah|lemah|hancur|mengecewakan|terrible|awful|bad|worst|hate)\b',
            r'\b(marah|benci|angry|mad|furious|kalah|lose|defeat|fail|disaster|wrong|salah)\b',
            r'\b(bodoh|stupid|idiot|tolol|goblok|sampah|trash|garbage|waste)\b',
            
            # Negative context (more aggressive)
            r'\b(tidak|no|never|don\'t|won\'t|can\'t|couldn\'t|shouldn\'t|mustn\'t)\b',
            r'\b(kenapa|why|mengapa|gimana|how|kapan|when|dimana|where)\s+(tidak|gak|ga|nggak|never|no)\b',
            r'\b(harusnya|should|seharusnya|mestinya|supposed)\b',
            r'\b(susah|sulit|hard|difficult|impossible|mustahil)\b',
            
            # Criticism and complaints
            r'\b(masalah|problem|issue|trouble|error|mistake|fault)\b',
            r'\b(bosan|boring|tired|capek|lelah|muak|fed up)\b',
            
            # Negative emojis
            r'(👎|😞|😠|😡|💔|😢|😭|😤|🤬|😒)',
        ]
        
        # Question patterns (often indicate dissatisfaction)
        self.question_patterns = [
            r'\b(kenapa|why|mengapa|gimana|bagaimana|how|kapan|when|dimana|where)\b',
            r'\?',  # Question mark
        ]
        
        # Intensifiers
        self.intensifiers = [
            r'\b(sangat|very|really|extremely|super|banget|bgt|sekali|too|terlalu)\b'
        ]
    
    def analyze_sentiment(self, text: str) -> Dict:
        """Aggressive sentiment analysis with minimal neutral."""
        if not text or len(text.strip()) < 2:
            return {'sentiment': 'neutral', 'confidence': 0.5, 'reasoning': 'Text too short'}
        
        text_lower = text.lower()
        
        # Count indicators
        positive_count = sum(len(re.findall(pattern, text_lower)) for pattern in self.positive_indicators)
        negative_count = sum(len(re.findall(pattern, text_lower)) for pattern in self.negative_indicators)
        question_count = sum(len(re.findall(pattern, text_lower)) for pattern in self.question_patterns)
        intensifier_count = sum(len(re.findall(pattern, text_lower)) for pattern in self.intensifiers)
        
        # Boost scores
        intensifier_boost = 1 + (intensifier_count * 0.3)
        positive_score = positive_count * intensifier_boost
        negative_score = (negative_count + question_count * 0.5) * intensifier_boost
        
        # Very low threshold for neutral (aggressive classification)
        neutral_threshold = 0.1
        
        # Determine sentiment
        if positive_score > negative_score + neutral_threshold:
            sentiment = 'positive'
            confidence = min(0.95, 0.6 + (positive_score - negative_score) * 0.2)
            reasoning = f"Positive indicators: {positive_count}, boost: {intensifier_boost:.1f}"
        elif negative_score > positive_score + neutral_threshold:
            sentiment = 'negative'
            confidence = min(0.95, 0.6 + (negative_score - positive_score) * 0.2)
            reasoning = f"Negative indicators: {negative_count + question_count}, boost: {intensifier_boost:.1f}"
        else:
            # Even for "neutral", try to lean towards negative if there are questions or uncertainty
            if question_count > 0 or any(word in text_lower for word in ['tapi', 'but', 'however', 'namun']):
                sentiment = 'negative'
                confidence = 0.55
                reasoning = "Uncertainty/questioning detected"
            elif len(text_lower.split()) > 5:  # Longer texts lean negative (complaints are usually longer)
                sentiment = 'negative'
                confidence = 0.52
                reasoning = "Long text pattern"
            else:
                sentiment = 'neutral'
                confidence = 0.5
                reasoning = "Minimal indicators found"
        
        return {
            'sentiment': sentiment,
            'confidence': confidence,
            'reasoning': reasoning
        }

# Global instance
_aggressive_analyzer = None

def get_aggressive_analyzer():
    global _aggressive_analyzer
    if _aggressive_analyzer is None:
        _aggressive_analyzer = AggressiveSentimentAnalyzer()
    return _aggressive_analyzer

if __name__ == "__main__":
    analyzer = AggressiveSentimentAnalyzer()
    
    test_comments = [
        "Eric Tohir tuh megang inter Milan jja gx bisa hasilnya jelek",
        "Indonesia bisa masuk pildun kalau towel diangkat ganti kluivert",
        "Sudah.. timnas ggl total..di latih Mr Patrick kluiver",
        "Kenapa selalu kalah sih?",
        "Semoga menang ya",
        "Mantap permainannya",
        "Biasa aja sih",
        "Harusnya main lebih bagus",
        "Bagus sekali 👍",
        "Jelek banget 👎"
    ]
    
    print("⚡ Testing Aggressive Analyzer:")
    print("=" * 50)
    
    for comment in test_comments:
        result = analyzer.analyze_sentiment(comment)
        print(f"Text: {comment}")
        print(f"Result: {result['sentiment']} ({result['confidence']:.2f}) - {result['reasoning']}")
        print("-" * 40)
