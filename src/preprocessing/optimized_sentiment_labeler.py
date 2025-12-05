"""
Optimized Sentiment Labeler - 5-Layer Framework
Using sentiment_config_v2_optimized.py for actionable insights
WITH STEMMED KEYWORD MATCHING for better coverage
"""

import re
from typing import Dict, List, Any, Tuple
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.tokenize import word_tokenize
from config.sentiment_config_v2_optimized import (
    CORE_SENTIMENT,
    TARGET_KRITIK,
    ROOT_CAUSE,
    TIME_PERSPECTIVE,
    CONSTRUCTIVENESS,
    CONFIG_METADATA
)


class OptimizedSentimentLabeler:
    """
    Multi-layer sentiment labeler using optimized 5-layer framework
    Focus on: WHO-WHY-WHEN-HOW questions for actionable insights
    
    NEW: Uses STEMMED keyword matching to catch more variations
    e.g., "menyerang", "penyerangan", "diserang" all match "serang"
    """
    
    def __init__(self):
        """Initialize labeler with 5-layer config and stemmer"""
        # Initialize Sastrawi stemmer
        factory = StemmerFactory()
        self.stemmer = factory.create_stemmer()
        
        self.core_sentiment = CORE_SENTIMENT
        self.target_kritik = TARGET_KRITIK
        self.root_cause = ROOT_CAUSE
        self.time_perspective = TIME_PERSPECTIVE
        self.constructiveness = CONSTRUCTIVENESS
        
        # Compile all categories for efficient matching
        self.all_categories = {
            'layer1_core': self.core_sentiment,
            'layer2_target': self.target_kritik,
            'layer3_cause': self.root_cause,
            'layer4_time': self.time_perspective,
            'layer5_constructive': self.constructiveness
        }
        
        # Pre-stem all keywords for faster matching
        self.stemmed_keywords_cache = {}
        self._prepare_stemmed_keywords()
        
        print(f"✅ Initialized OptimizedSentimentLabeler")
        print(f"   Framework: {CONFIG_METADATA['framework_name']}")
        print(f"   Total Categories: {CONFIG_METADATA['total_categories']}")
        print(f"   Total Layers: {CONFIG_METADATA['total_layers']}")
        print(f"   Stemmed Matching: ENABLED")
        print(f"   Cached Keywords: {len(self.stemmed_keywords_cache)}")
    
    def _prepare_stemmed_keywords(self):
        """Pre-stem all keywords to avoid repeated stemming during matching"""
        for layer_name, layer_cats in self.all_categories.items():
            for cat_name, config in layer_cats.items():
                keywords = config.get('keywords', [])
                for keyword in keywords:
                    if keyword not in self.stemmed_keywords_cache:
                        # Stem each word in the keyword
                        tokens = str(keyword).lower().split()
                        stemmed = ' '.join([self.stemmer.stem(token) for token in tokens])
                        self.stemmed_keywords_cache[keyword] = stemmed
    
    def match_keywords(self, text: str, keywords: List[str]) -> Tuple[int, List[str]]:
        """
        Match keywords in text using STEMMED matching
        
        This allows matching word variations:
        - "menyerang", "penyerangan", "diserang" → all match "serang"
        - "bertahan", "pertahanan", "menahan" → all match "tahan"
        
        Args:
            text: Input text (normalized tokens joined)
            keywords: List of keywords to match
        
        Returns:
            (match_count, matched_keywords)
        """
        if not text:
            return 0, []
        
        # Tokenize and stem input text
        text_lower = text.lower()
        try:
            tokens = word_tokenize(text_lower)
            stemmed_tokens = [self.stemmer.stem(token) for token in tokens]
            stemmed_text = ' '.join(stemmed_tokens)
        except:
            # Fallback if tokenization fails
            stemmed_text = text_lower
        
        matched = []
        
        for keyword in keywords:
            # Get pre-stemmed keyword from cache
            stemmed_keyword = self.stemmed_keywords_cache.get(
                keyword,
                self.stemmer.stem(str(keyword).lower())  # fallback
            )
            
            # Match with word boundaries
            pattern = r'\b' + re.escape(stemmed_keyword) + r'\b'
            if re.search(pattern, stemmed_text):
                matched.append(keyword)
        
        return len(matched), matched
    
    def label_layer(self, text: str, layer_categories: Dict) -> Dict:
        """
        Label text for a specific layer
        
        Returns:
            {
                'label': str,
                'score': float,
                'matched_keywords': list,
                'confidence': float
            }
        """
        scores = {}
        matches_detail = {}
        
        for category_name, config in layer_categories.items():
            keywords = config.get('keywords', [])
            weight = config.get('weight', 1.0)
            
            match_count, matched_keywords = self.match_keywords(text, keywords)
            
            if match_count > 0:
                # Score = match_count * weight
                scores[category_name] = match_count * weight
                matches_detail[category_name] = {
                    'count': match_count,
                    'keywords': matched_keywords,
                    'weight': weight,
                    'score': scores[category_name]
                }
        
        # Get best match
        if scores:
            best_category = max(scores, key=scores.get)
            return {
                'label': best_category,
                'score': scores[best_category],
                'matched_keywords': matches_detail[best_category]['keywords'],
                'confidence': min(scores[best_category] / 10.0, 1.0),  # Normalize to 0-1
                'all_matches': matches_detail
            }
        else:
            return {
                'label': 'unknown',
                'score': 0.0,
                'matched_keywords': [],
                'confidence': 0.0,
                'all_matches': {}
            }
    
    def label_text(self, text: str) -> Dict[str, Any]:
        """
        Apply all 5 layers to text
        
        Returns comprehensive labeling with all layers
        """
        if not text or not isinstance(text, str):
            return self._get_default_labels()
        
        results = {}
        
        # Layer 1: Core Sentiment
        layer1 = self.label_layer(text, self.core_sentiment)
        results['core_sentiment'] = layer1['label']
        results['core_sentiment_score'] = layer1['score']
        results['core_sentiment_confidence'] = layer1['confidence']
        
        # Layer 2: Target Kritik (WHO to blame)
        layer2 = self.label_layer(text, self.target_kritik)
        results['target_kritik'] = layer2['label']
        results['target_score'] = layer2['score']
        results['target_confidence'] = layer2['confidence']
        
        # Layer 3: Root Cause (WHY failed)
        layer3 = self.label_layer(text, self.root_cause)
        results['root_cause'] = layer3['label']
        results['cause_score'] = layer3['score']
        results['cause_confidence'] = layer3['confidence']
        
        # Layer 4: Time Perspective (WHEN to fix)
        layer4 = self.label_layer(text, self.time_perspective)
        results['time_perspective'] = layer4['label']
        results['time_score'] = layer4['score']
        results['time_confidence'] = layer4['confidence']
        
        # Layer 5: Constructiveness (HOW valuable)
        layer5 = self.label_layer(text, self.constructiveness)
        results['constructiveness'] = layer5['label']
        results['constructive_score'] = layer5['score']
        results['constructive_confidence'] = layer5['confidence']
        
        # Determine primary label (highest confidence across non-core layers)
        primary_candidates = [
            ('target_kritik', layer2['confidence']),
            ('root_cause', layer3['confidence']),
            ('time_perspective', layer4['confidence']),
            ('constructiveness', layer5['confidence'])
        ]
        
        # Get best non-unknown label
        valid_candidates = [
            (key, conf) for key, conf in primary_candidates
            if results[key] != 'unknown'
        ]
        
        if valid_candidates:
            primary_key, _ = max(valid_candidates, key=lambda x: x[1])
            results['primary_label'] = results[primary_key]
        else:
            results['primary_label'] = results['core_sentiment']
        
        # Aggregate scores
        total_score = (
            layer1['score'] +
            layer2['score'] +
            layer3['score'] +
            layer4['score'] +
            layer5['score']
        )
        results['total_score'] = total_score
        
        # Average confidence
        confidences = [
            layer1['confidence'],
            layer2['confidence'],
            layer3['confidence'],
            layer4['confidence'],
            layer5['confidence']
        ]
        results['avg_confidence'] = sum(confidences) / len(confidences)
        
        # Collect all matched keywords
        all_matched = []
        for layer in [layer1, layer2, layer3, layer4, layer5]:
            all_matched.extend(layer['matched_keywords'])
        results['all_matched_keywords'] = all_matched
        
        return results
    
    def _get_default_labels(self) -> Dict[str, Any]:
        """Return default labels for empty/invalid text"""
        return {
            'core_sentiment': 'neutral',
            'core_sentiment_score': 0.0,
            'core_sentiment_confidence': 0.0,
            'target_kritik': 'unknown',
            'target_score': 0.0,
            'target_confidence': 0.0,
            'root_cause': 'unknown',
            'cause_score': 0.0,
            'cause_confidence': 0.0,
            'time_perspective': 'unknown',
            'time_score': 0.0,
            'time_confidence': 0.0,
            'constructiveness': 'unknown',
            'constructive_score': 0.0,
            'constructive_confidence': 0.0,
            'primary_label': 'neutral',
            'total_score': 0.0,
            'avg_confidence': 0.0,
            'all_matched_keywords': []
        }
    
    def get_summary(self, labels: Dict[str, Any]) -> str:
        """Generate human-readable summary"""
        summary_parts = []
        
        # Core sentiment
        summary_parts.append(f"Sentimen: {labels['core_sentiment']}")
        
        # Target (if identified)
        if labels['target_kritik'] != 'unknown':
            summary_parts.append(f"Target: {labels['target_kritik']}")
        
        # Root cause (if identified)
        if labels['root_cause'] != 'unknown':
            summary_parts.append(f"Penyebab: {labels['root_cause']}")
        
        # Time perspective (if identified)
        if labels['time_perspective'] != 'unknown':
            summary_parts.append(f"Waktu: {labels['time_perspective']}")
        
        # Constructiveness (if identified)
        if labels['constructiveness'] != 'unknown':
            summary_parts.append(f"Konstruktif: {labels['constructiveness']}")
        
        return " | ".join(summary_parts)


# Export labeler
__all__ = ['OptimizedSentimentLabeler']
