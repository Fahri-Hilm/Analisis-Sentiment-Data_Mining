"""Gemini AI Comment Filter - Select Relevant Comments Only."""
import google.generativeai as genai
import time
from typing import Dict, List
import logging

class GeminiCommentFilter:
    def __init__(self, api_key: str = "AIzaSyC79pEPb22JKUyXlmOjVt99vnLounyYvrY"):
        """Initialize Gemini comment filter."""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.logger = logging.getLogger(__name__)
        self.request_count = 0
        self.max_requests = 10  # Conservative limit
        self.last_reset = time.time()
    
    def _check_rate_limit(self) -> bool:
        """Check rate limit."""
        current_time = time.time()
        if current_time - self.last_reset > 3600:  # Reset every hour
            self.request_count = 0
            self.last_reset = current_time
        return self.request_count < self.max_requests
    
    def is_relevant_comment(self, comment: str) -> Dict:
        """Check if comment is relevant using Gemini AI."""
        if not comment or len(comment.strip()) < 5:
            return {'relevant': False, 'reason': 'Too short'}
        
        # Skip if rate limit exceeded
        if not self._check_rate_limit():
            return self._fallback_filter(comment)
        
        prompt = f"""Analisis apakah komentar ini relevan untuk analisis sentiment sepak bola/timnas Indonesia:

"{comment}"

Kriteria RELEVAN:
- Membahas sepak bola, timnas, pemain, pelatih, pertandingan
- Mengandung opini, kritik, dukungan, atau emosi
- Memiliki konteks yang jelas

Kriteria TIDAK RELEVAN:
- Spam, promosi, link
- Tidak ada hubungan dengan sepak bola
- Hanya emoji atau singkatan tidak jelas
- Komentar random tanpa konteks

Jawab JSON: {{"relevant": true/false, "reason": "alasan singkat"}}"""

        try:
            self.request_count += 1
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            import json
            if '{' in result_text and '}' in result_text:
                json_start = result_text.find('{')
                json_end = result_text.rfind('}') + 1
                json_str = result_text[json_start:json_end]
                result = json.loads(json_str)
                
                return {
                    'relevant': result.get('relevant', False),
                    'reason': result.get('reason', 'AI analysis'),
                    'method': 'Gemini AI'
                }
        except Exception as e:
            self.logger.error(f"Gemini filter error: {e}")
        
        # Fallback
        return self._fallback_filter(comment)
    
    def _fallback_filter(self, comment: str) -> Dict:
        """Fallback relevance filter."""
        comment_lower = comment.lower()
        
        # Football-related keywords
        football_keywords = [
            'timnas', 'indonesia', 'sepak bola', 'football', 'soccer',
            'pemain', 'player', 'pelatih', 'coach', 'pertandingan', 'match',
            'gol', 'goal', 'menang', 'kalah', 'win', 'lose', 'juara',
            'piala dunia', 'world cup', 'aff', 'sea games', 'asian games'
        ]
        
        # Check for football context
        has_football_context = any(keyword in comment_lower for keyword in football_keywords)
        
        # Filter out obvious spam/irrelevant
        spam_indicators = [
            'http', 'www', '.com', 'subscribe', 'like and subscribe',
            'follow me', 'check out', 'promo', 'diskon', 'murah'
        ]
        
        is_spam = any(spam in comment_lower for spam in spam_indicators)
        
        # Too short or just emojis
        is_too_short = len(comment.strip()) < 10
        is_just_emojis = len(comment.strip()) < 5 or comment.count('😀') + comment.count('👍') > len(comment) / 3
        
        if is_spam:
            return {'relevant': False, 'reason': 'Spam detected', 'method': 'Fallback'}
        elif is_too_short or is_just_emojis:
            return {'relevant': False, 'reason': 'Too short/emoji only', 'method': 'Fallback'}
        elif has_football_context:
            return {'relevant': True, 'reason': 'Football context found', 'method': 'Fallback'}
        else:
            # If no clear football context but not spam, still include (might be general opinion)
            return {'relevant': True, 'reason': 'General opinion', 'method': 'Fallback'}
    
    def filter_comments(self, comments: List[Dict]) -> List[Dict]:
        """Filter list of comments for relevance."""
        filtered_comments = []
        
        for comment in comments:
            text = comment.get('text', '')
            relevance = self.is_relevant_comment(text)
            
            if relevance['relevant']:
                comment['filter_info'] = relevance
                filtered_comments.append(comment)
            else:
                self.logger.info(f"Filtered out: {text[:50]}... - {relevance['reason']}")
        
        return filtered_comments

# Global instance
_comment_filter = None

def get_comment_filter():
    """Get or create comment filter instance."""
    global _comment_filter
    if _comment_filter is None:
        _comment_filter = GeminiCommentFilter()
    return _comment_filter

def filter_relevant_comments(comments: List[Dict]) -> List[Dict]:
    """Quick comment filtering."""
    filter_instance = get_comment_filter()
    return filter_instance.filter_comments(comments)

if __name__ == "__main__":
    # Test the filter
    filter_instance = GeminiCommentFilter()
    
    test_comments = [
        "Eric Tohir tuh megang inter Milan jja gx bisa hasilnya jelek",
        "Subscribe channel gue ya guys!",
        "😀😀😀👍👍",
        "Timnas Indonesia harus main lebih bagus",
        "Check out my website www.example.com",
        "Kenapa selalu kalah sih timnas kita?",
        "abcdefg random text here",
        "Semoga menang di piala dunia nanti"
    ]
    
    print("🔍 Testing Gemini Comment Filter:")
    print("=" * 50)
    
    for comment in test_comments:
        result = filter_instance.is_relevant_comment(comment)
        status = "✅ RELEVANT" if result['relevant'] else "❌ FILTERED"
        print(f"{status}: {comment}")
        print(f"   Reason: {result['reason']} ({result['method']})")
        print("-" * 40)
