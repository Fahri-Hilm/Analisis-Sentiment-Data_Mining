"""
Enhanced Sentiment Analyzer dengan Timnas Lexicon v2.0
Menggunakan 1,500 kata lexicon untuk analisis sentiment Layer 1
"""

import re
import pandas as pd
from typing import Dict, List, Tuple, Union
from config.timnas_lexicon_v2 import TIMNAS_LEXICON_V2, get_sentiment_score, get_lexicon_stats

class EnhancedTimnasSentimentAnalyzer:
    """
    Enhanced sentiment analyzer dengan lexicon lengkap 1,500 kata
    Layer 1: Core Sentiment Analysis dengan bobot presisi -2.0 hingga +2.0
    """
    
    def __init__(self):
        self.lexicon = TIMNAS_LEXICON_V2
        self.stats = get_lexicon_stats()
        
        # Intensifier patterns untuk meningkatkan akurasi
        self.intensifiers = {
            'sangat': 1.5, 'amat': 1.5, 'begitu': 1.3, 'sekali': 1.4,
            'banget': 1.6, 'parah': 1.7, 'total': 1.8, 'abis': 1.4,
            'lagi': 1.2, 'terus': 1.3, 'mulu': 1.4, 'melulu': 1.4
        }
        
        # Negation patterns
        self.negations = ['tidak', 'tak', 'gak', 'ga', 'nggak', 'bukan', 'jangan']
        
    def preprocess_text(self, text: str) -> str:
        """Preprocessing teks untuk analisis"""
        if not text or pd.isna(text):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def extract_sentiment_words(self, text: str) -> List[Tuple[str, float]]:
        """Extract kata-kata sentiment dengan scorenya"""
        words = text.split()
        sentiment_words = []
        
        # Check single words
        for word in words:
            if word in self.lexicon:
                sentiment_words.append((word, self.lexicon[word]))
        
        # Check multi-word phrases (up to 4 words)
        for i in range(len(words)):
            for j in range(i+2, min(i+5, len(words)+1)):
                phrase = ' '.join(words[i:j])
                if phrase in self.lexicon:
                    sentiment_words.append((phrase, self.lexicon[phrase]))
        
        return sentiment_words
    
    def apply_intensifiers(self, sentiment_words: List[Tuple[str, float]], text: str) -> List[Tuple[str, float]]:
        """Apply intensifier untuk meningkatkan/menurunkan score"""
        enhanced_words = []
        words = text.split()
        
        for phrase, score in sentiment_words:
            enhanced_score = score
            phrase_words = phrase.split()
            
            # Find position of sentiment phrase in text
            for i, word in enumerate(words):
                if word == phrase_words[0]:
                    # Check for intensifiers before the phrase
                    if i > 0 and words[i-1] in self.intensifiers:
                        multiplier = self.intensifiers[words[i-1]]
                        enhanced_score = score * multiplier
                        # Cap the score at -2.0 to +2.0
                        enhanced_score = max(-2.0, min(2.0, enhanced_score))
                    break
            
            enhanced_words.append((phrase, enhanced_score))
        
        return enhanced_words
    
    def apply_negation(self, sentiment_words: List[Tuple[str, float]], text: str) -> List[Tuple[str, float]]:
        """Apply negation untuk membalik sentiment"""
        negated_words = []
        words = text.split()
        
        for phrase, score in sentiment_words:
            negated_score = score
            phrase_words = phrase.split()
            
            # Find position of sentiment phrase in text
            for i, word in enumerate(words):
                if word == phrase_words[0]:
                    # Check for negations in previous 3 words
                    for j in range(max(0, i-3), i):
                        if words[j] in self.negations:
                            negated_score = -score * 0.8  # Reverse and slightly reduce intensity
                            break
                    break
            
            negated_words.append((phrase, negated_score))
        
        return negated_words
    
    def calculate_sentiment_score(self, text: str) -> Dict[str, Union[float, str, List]]:
        """
        Hitung sentiment score dari teks
        
        Returns:
            Dict dengan keys: score, label, confidence, words_found, details
        """
        if not text or pd.isna(text):
            return {
                'score': 0.0,
                'label': 'neutral',
                'confidence': 0.0,
                'words_found': [],
                'details': 'Empty text'
            }
        
        # Preprocess
        processed_text = self.preprocess_text(text)
        
        # Extract sentiment words
        sentiment_words = self.extract_sentiment_words(processed_text)
        
        if not sentiment_words:
            return {
                'score': 0.0,
                'label': 'neutral',
                'confidence': 0.3,
                'words_found': [],
                'details': 'No sentiment words found'
            }
        
        # Apply intensifiers
        enhanced_words = self.apply_intensifiers(sentiment_words, processed_text)
        
        # Apply negation
        final_words = self.apply_negation(enhanced_words, processed_text)
        
        # Calculate final score
        total_score = sum(score for _, score in final_words)
        word_count = len(final_words)
        
        # Average score
        avg_score = total_score / word_count if word_count > 0 else 0.0
        
        # Determine label
        if avg_score > 0.3:
            label = 'positive'
        elif avg_score < -0.3:
            label = 'negative'
        else:
            label = 'neutral'
        
        # Calculate confidence based on score magnitude and word count
        confidence = min(abs(avg_score), 1.0)
        if word_count > 1:
            confidence = min(confidence + 0.1, 1.0)
        if word_count > 3:
            confidence = min(confidence + 0.1, 1.0)
        
        return {
            'score': round(avg_score, 3),
            'label': label,
            'confidence': round(confidence, 3),
            'words_found': [word for word, _ in final_words],
            'details': f'Found {word_count} sentiment words, total_score: {total_score:.3f}'
        }
    
    def analyze_batch(self, texts: List[str]) -> List[Dict]:
        """Analyze multiple texts"""
        results = []
        for text in texts:
            result = self.calculate_sentiment_score(text)
            results.append(result)
        return results
    
    def analyze_dataframe(self, df: pd.DataFrame, text_column: str = 'text') -> pd.DataFrame:
        """Analyze sentiment untuk seluruh dataframe"""
        results = []
        
        for idx, row in df.iterrows():
            text = row[text_column] if text_column in row else ''
            result = self.calculate_sentiment_score(text)
            results.append(result)
        
        # Convert to dataframe
        result_df = pd.DataFrame(results)
        
        # Combine with original dataframe
        return pd.concat([df, result_df], axis=1)
    
    def get_lexicon_coverage(self, text: str) -> Dict:
        """Get coverage statistics untuk teks"""
        processed_text = self.preprocess_text(text)
        words = processed_text.split()
        
        total_words = len(words)
        covered_words = 0
        
        for word in words:
            if word in self.lexicon:
                covered_words += 1
        
        coverage = covered_words / total_words if total_words > 0 else 0.0
        
        return {
            'total_words': total_words,
            'covered_words': covered_words,
            'coverage_percentage': round(coverage * 100, 2),
            'lexicon_size': len(self.lexicon)
        }


def test_analyzer():
    """Test function untuk analyzer"""
    analyzer = EnhancedTimnasSentimentAnalyzer()
    
    test_cases = [
        "Sangat bangga dengan Garuda, tetap semangat!",
        "Gagal total lagi, kecewa parah dengan timnas",
        "Timnas Indonesia vs Irak babak 3 kualifikasi",
        "Goblok banget STY, strategi salah total!",
        "Optimis untuk masa depan, generasi emas Indonesia",
        "Tidak kecewa dengan performa tim, sudah maksimal"
    ]
    
    print("="*80)
    print("ENHANCED TIMNAS SENTIMENT ANALYZER - TEST RESULTS")
    print("="*80)
    print(f"Lexicon Stats: {analyzer.stats}")
    print("="*80)
    
    for text in test_cases:
        result = analyzer.calculate_sentiment_score(text)
        coverage = analyzer.get_lexicon_coverage(text)
        
        print(f"\nText: {text}")
        print(f"Score: {result['score']} | Label: {result['label']} | Confidence: {result['confidence']}")
        print(f"Words Found: {result['words_found']}")
        print(f"Coverage: {coverage['coverage_percentage']}% ({coverage['covered_words']}/{coverage['total_words']} words)")
        print(f"Details: {result['details']}")
        print("-" * 80)


if __name__ == "__main__":
    test_analyzer()
