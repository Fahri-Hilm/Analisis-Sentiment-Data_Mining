"""
Football-Specific Emotions Analyzer - Layer 3
Menganalisis 6 emosi sepakbola spesifik dengan 3,000 kata lexicon
Passionate Disappointment, Strategic Frustration, Patriotic Sadness,
Constructive Anger, Respectful Acknowledgment, Future Hope
"""

import re
import pandas as pd
from typing import Dict, List, Tuple, Union
from config.football_emotions_lexicon_v3 import (
    FOOTBALL_EMOTIONS_LEXICON,
    EMOTION_LEXICONS,
    get_football_emotion_score,
    get_football_emotion_category,
    get_layer3_stats,
    get_football_emotion_distribution
)

class FootballEmotionsAnalyzer:
    """
    Layer 3 analyzer untuk 6 emosi sepakbola spesifik dengan 3,000 kata lexicon
    """
    
    def __init__(self):
        self.lexicon = FOOTBALL_EMOTIONS_LEXICON
        self.emotion_lexicons = EMOTION_LEXICONS
        self.stats = get_layer3_stats()
        
        # Intensifier patterns khusus sepakbola
        self.intensifiers = {
            'sangat': 1.5, 'amat': 1.5, 'begitu': 1.3, 'sekali': 1.4,
            'banget': 1.6, 'parah': 1.7, 'total': 1.8, 'abis': 1.4,
            'lagi': 1.2, 'terus': 1.3, 'besar': 1.4, 'tinggi': 1.3,
            'tragis': 1.6, 'hancur': 1.7, 'gagal': 1.5, 'pilu': 1.4
        }
        
        # Negation patterns
        self.negations = ['tidak', 'tak', 'gak', 'ga', 'nggak', 'bukan', 'jangan']
        
    def preprocess_text(self, text: str) -> str:
        """Preprocessing teks untuk analisis"""
        if not text or pd.isna(text):
            return ""
        
        text = text.lower()
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def extract_football_emotion_words(self, text: str) -> List[Tuple[str, float, str]]:
        """Extract kata-kata emosi sepakbola dengan score dan kategorinya"""
        words = text.split()
        emotion_words = []
        
        # Check single words
        for word in words:
            if word in self.lexicon:
                category = get_football_emotion_category(word)
                emotion_words.append((word, self.lexicon[word], category))
        
        # Check multi-word phrases (up to 5 words untuk konteks sepakbola)
        for i in range(len(words)):
            for j in range(i+2, min(i+6, len(words)+1)):
                phrase = ' '.join(words[i:j])
                if phrase in self.lexicon:
                    category = get_football_emotion_category(phrase)
                    emotion_words.append((phrase, self.lexicon[phrase], category))
        
        return emotion_words
    
    def apply_intensifiers(self, emotion_words: List[Tuple[str, float, str]], text: str) -> List[Tuple[str, float, str]]:
        """Apply intensifier untuk meningkatkan/menurunkan score"""
        enhanced_words = []
        words = text.split()
        
        for phrase, score, category in emotion_words:
            enhanced_score = score
            phrase_words = phrase.split()
            
            for i, word in enumerate(words):
                if word == phrase_words[0]:
                    # Check for intensifiers before the phrase
                    if i > 0 and words[i-1] in self.intensifiers:
                        multiplier = self.intensifiers[words[i-1]]
                        enhanced_score = score * multiplier
                        enhanced_score = max(-2.0, min(2.0, enhanced_score))
                    break
            
            enhanced_words.append((phrase, enhanced_score, category))
        
        return enhanced_words
    
    def apply_negation(self, emotion_words: List[Tuple[str, float, str]], text: str) -> List[Tuple[str, float, str]]:
        """Apply negation untuk membalik sentiment"""
        negated_words = []
        words = text.split()
        
        for phrase, score, category in emotion_words:
            negated_score = score
            phrase_words = phrase.split()
            
            for i, word in enumerate(words):
                if word == phrase_words[0]:
                    # Check for negations in previous 3 words
                    for j in range(max(0, i-3), i):
                        if words[j] in self.negations:
                            negated_score = -score * 0.6  # Reverse and reduce intensity
                            break
                    break
            
            negated_words.append((phrase, negated_score, category))
        
        return negated_words
    
    def calculate_football_emotion_scores(self, text: str) -> Dict[str, Union[float, str, List, Dict]]:
        """
        Hitung football emotion scores dari teks
        """
        if not text or pd.isna(text):
            return {
                'primary_emotion': 'neutral',
                'emotion_scores': {
                    'Passionate Disappointment': 0,
                    'Strategic Frustration': 0,
                    'Patriotic Sadness': 0,
                    'Constructive Anger': 0,
                    'Respectful Acknowledgment': 0,
                    'Future Hope': 0
                },
                'confidence': 0.0,
                'words_found': [],
                'details': 'Empty text'
            }
        
        processed_text = self.preprocess_text(text)
        emotion_words = self.extract_football_emotion_words(processed_text)
        
        if not emotion_words:
            return {
                'primary_emotion': 'neutral',
                'emotion_scores': {
                    'Passionate Disappointment': 0,
                    'Strategic Frustration': 0,
                    'Patriotic Sadness': 0,
                    'Constructive Anger': 0,
                    'Respectful Acknowledgment': 0,
                    'Future Hope': 0
                },
                'confidence': 0.3,
                'words_found': [],
                'details': 'No football emotion words found'
            }
        
        enhanced_words = self.apply_intensifiers(emotion_words, processed_text)
        final_words = self.apply_negation(enhanced_words, processed_text)
        
        # Calculate scores per emotion category
        emotion_scores = {
            'Passionate Disappointment': 0,
            'Strategic Frustration': 0,
            'Patriotic Sadness': 0,
            'Constructive Anger': 0,
            'Respectful Acknowledgment': 0,
            'Future Hope': 0
        }
        emotion_counts = {
            'Passionate Disappointment': 0,
            'Strategic Frustration': 0,
            'Patriotic Sadness': 0,
            'Constructive Anger': 0,
            'Respectful Acknowledgment': 0,
            'Future Hope': 0
        }
        
        for phrase, score, category in final_words:
            if category in emotion_scores:
                emotion_scores[category] += score
                emotion_counts[category] += 1
        
        # Average scores per category
        for emotion in emotion_scores:
            if emotion_counts[emotion] > 0:
                emotion_scores[emotion] = emotion_scores[emotion] / emotion_counts[emotion]
        
        # Determine primary emotion
        primary_emotion = max(emotion_scores, key=lambda x: abs(emotion_scores[x]))
        if abs(emotion_scores[primary_emotion]) < 0.4:
            primary_emotion = 'neutral'
        
        # Calculate confidence
        max_score = abs(emotion_scores[primary_emotion])
        confidence = min(max_score / 2.0, 1.0)
        
        word_count = len(final_words)
        if word_count > 1:
            confidence = min(confidence + 0.15, 1.0)
        if word_count > 3:
            confidence = min(confidence + 0.15, 1.0)
        
        return {
            'primary_emotion': primary_emotion,
            'emotion_scores': {k: round(v, 3) for k, v in emotion_scores.items()},
            'confidence': round(confidence, 3),
            'words_found': [{'word': word, 'score': score, 'category': cat} for word, score, cat in final_words],
            'details': f'Found {word_count} football emotion words, primary: {primary_emotion}'
        }
    
    def analyze_batch(self, texts: List[str]) -> List[Dict]:
        """Analyze multiple texts"""
        results = []
        for text in texts:
            result = self.calculate_football_emotion_scores(text)
            results.append(result)
        return results
    
    def get_football_emotion_coverage(self, text: str) -> Dict:
        """Get coverage statistics untuk teks"""
        processed_text = self.preprocess_text(text)
        words = processed_text.split()
        
        total_words = len(words)
        covered_words = 0
        emotion_coverage = {
            'Passionate Disappointment': 0,
            'Strategic Frustration': 0,
            'Patriotic Sadness': 0,
            'Constructive Anger': 0,
            'Respectful Acknowledgment': 0,
            'Future Hope': 0
        }
        
        for word in words:
            if word in self.lexicon:
                covered_words += 1
                category = get_football_emotion_category(word)
                if category in emotion_coverage:
                    emotion_coverage[category] += 1
        
        coverage = covered_words / total_words if total_words > 0 else 0.0
        
        return {
            'total_words': total_words,
            'covered_words': covered_words,
            'coverage_percentage': round(coverage * 100, 2),
            'emotion_coverage': emotion_coverage,
            'lexicon_size': len(self.lexicon)
        }
    
    def get_stats(self):
        """Get analyzer statistics"""
        return self.stats
    
    def get_emotion_distribution(self):
        """Get emotion distribution"""
        return get_football_emotion_distribution()


def test_football_emotions_analyzer():
    """Test function untuk analyzer"""
    analyzer = FootballEmotionsAnalyzer()
    
    test_cases = [
        "Sangat kecewa, hancur lebur mimpi PD 2026!",
        "STY goblok parah, strategi salah total banget!",
        "Malu jadi orang Indo, Garuda jatuh tragis",
        "Harus berubah PSSI, ganti pelatih sekarang!",
        "Respect lawan, Irak memang lebih baik",
        "Optimis generasi baru, Piala Dunia 2030!"
    ]
    
    print("="*80)
    print("FOOTBALL-SPECIFIC EMOTIONS ANALYZER - TEST RESULTS")
    print("="*80)
    print(f"Lexicon Stats: {analyzer.get_stats()}")
    print("="*80)
    
    for text in test_cases:
        result = analyzer.calculate_football_emotion_scores(text)
        coverage = analyzer.get_football_emotion_coverage(text)
        
        print(f"\nText: {text}")
        print(f"Primary Emotion: {result['primary_emotion']} | Confidence: {result['confidence']}")
        print(f"Emotion Scores: {result['emotion_scores']}")
        print(f"Words Found: {len(result['words_found'])} words")
        print(f"Coverage: {coverage['coverage_percentage']}% ({coverage['covered_words']}/{coverage['total_words']} words)")
        print(f"Details: {result['details']}")
        print("-" * 80)


if __name__ == "__main__":
    test_football_emotions_analyzer()
