"""Gemini AI Sentiment Analysis - Real-time & Accurate."""
import google.generativeai as genai
import re
import time
from typing import Dict, List
import logging

class GeminiSentimentAnalyzer:
    def __init__(self, api_key: str):
        """Initialize Gemini AI sentiment analyzer."""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.logger = logging.getLogger(__name__)
        self.request_count = 0
        self.max_requests_per_hour = 15  # Conservative limit
        self.last_reset = time.time()
        
    def _check_rate_limit(self) -> bool:
        """Check if we're within rate limits."""
        current_time = time.time()
        
        # Reset counter every hour
        if current_time - self.last_reset > 3600:
            self.request_count = 0
            self.last_reset = current_time
        
        return self.request_count < self.max_requests_per_hour
        
    def _fallback_analysis(self, text: str) -> Dict:
        """Enhanced fallback sentiment analysis."""
        positive_words = ['bagus', 'hebat', 'mantap', 'keren', 'semangat', 'bangga', 'sukses', 'luar biasa', 'puas', 'senang']
        negative_words = ['jelek', 'buruk', 'kecewa', 'gagal', 'payah', 'lemah', 'hancur', 'mengecewakan', 'marah', 'benci']
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            sentiment = 'positive'
            confidence = min(0.9, 0.6 + (pos_count * 0.1))
            reasoning = f"Detected {pos_count} positive indicators"
        elif neg_count > pos_count:
            sentiment = 'negative' 
            confidence = min(0.9, 0.6 + (neg_count * 0.1))
            reasoning = f"Detected {neg_count} negative indicators"
        else:
            sentiment = 'neutral'
            confidence = 0.6
            reasoning = "No strong sentiment indicators found"
            
        return {
            'sentiment': sentiment,
            'confidence': confidence,
            'reasoning': reasoning
        }
        
    def analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment using Gemini AI with rate limiting."""
        if not text or len(text.strip()) < 2:
            return {
                'sentiment': 'neutral',
                'confidence': 0.5,
                'reasoning': 'Text too short'
            }
        
        # Check rate limit first
        if not self._check_rate_limit():
            self.logger.warning("Rate limit exceeded, using fallback analysis")
            fallback = self._fallback_analysis(text)
            return {
                **fallback,
                'reasoning': f"{fallback['reasoning']} (Rate limit reached)"
            }
        
        # Clean text
        clean_text = re.sub(r'[^\w\s]', ' ', text).strip()
        
        # Simple prompt for efficiency
        prompt = f"""Analisis sentimen: "{text}"
        
Jawab format JSON:
{{"sentiment": "positive/negative/neutral", "confidence": 0.85, "reasoning": "alasan singkat"}}"""

        try:
            self.request_count += 1
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Extract JSON from response
            import json
            if '{' in result_text and '}' in result_text:
                json_start = result_text.find('{')
                json_end = result_text.rfind('}') + 1
                json_str = result_text[json_start:json_end]
                result = json.loads(json_str)
                
                return {
                    'sentiment': result.get('sentiment', 'neutral'),
                    'confidence': float(result.get('confidence', 0.7)),
                    'reasoning': result.get('reasoning', 'AI analysis')
                }
            else:
                # Fallback parsing
                sentiment = 'neutral'
                if 'positive' in result_text.lower():
                    sentiment = 'positive'
                elif 'negative' in result_text.lower():
                    sentiment = 'negative'
                
                return {
                    'sentiment': sentiment,
                    'confidence': 0.7,
                    'reasoning': 'Parsed from AI response'
                }
                
        except Exception as e:
            self.logger.error(f"Gemini API error: {e}")
            # Use fallback analysis
            fallback = self._fallback_analysis(text)
            return {
                **fallback,
                'reasoning': f"{fallback['reasoning']} (API error)"
            }
    
    def batch_analyze(self, texts: List[str]) -> List[Dict]:
        """Analyze multiple texts with rate limiting."""
        results = []
        for i, text in enumerate(texts):
            result = self.analyze_sentiment(text)
            results.append(result)
            
            # Rate limiting - 1 request per second
            if i < len(texts) - 1:
                time.sleep(1)
        
        return results

# Global instance
_gemini_analyzer = None

def get_gemini_analyzer(api_key: str = "AIzaSyC79pEPb22JKUyXlmOjVt99vnLounyYvrY"):
    """Get or create Gemini analyzer instance."""
    global _gemini_analyzer
    if _gemini_analyzer is None:
        _gemini_analyzer = GeminiSentimentAnalyzer(api_key)
    return _gemini_analyzer

def analyze_comment_with_gemini(text: str) -> Dict:
    """Quick sentiment analysis with Gemini."""
    analyzer = get_gemini_analyzer()
    return analyzer.analyze_sentiment(text)

if __name__ == "__main__":
    # Test
    analyzer = GeminiSentimentAnalyzer("AIzaSyC79pEPb22JKUyXlmOjVt99vnLounyYvrY")
    
    test_comments = [
        "Produk ini sangat bagus dan berkualitas!",
        "Pelayanan mengecewakan sekali",
        "Biasa aja sih, nothing special"
    ]
    
    print("🤖 Testing Gemini AI Sentiment Analysis:")
    for comment in test_comments:
        result = analyzer.analyze_sentiment(comment)
        print(f"Text: {comment}")
        print(f"Result: {result}")
        print("-" * 40)
