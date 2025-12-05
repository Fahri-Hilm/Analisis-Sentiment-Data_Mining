"""Lexicon-based sentiment labeling leveraging the 9-layer configuration."""
from __future__ import annotations

import logging
from typing import Dict, List, Tuple

from config import sentiment_config


class SentimentLexiconLabeler:
    """Assign sentiment categories based on keyword matches per layer."""

    def __init__(self, min_hits: int = 1, min_score_threshold: float = 0.5):
        self.logger = logging.getLogger(self.__class__.__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )
            )
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

        self.min_hits = min_hits
        self.min_score_threshold = min_score_threshold
        self.lexicon = self._build_lexicon()
        self.sentiment_groups = self._build_sentiment_groups()

    def _build_lexicon(self) -> Dict[str, Dict]:
        lexicon: Dict[str, Dict] = {}
        for attr in dir(sentiment_config):
            if not attr.isupper():
                continue
            layer_value = getattr(sentiment_config, attr)
            if not isinstance(layer_value, dict):
                continue

            for category, meta in layer_value.items():
                if not isinstance(meta, dict):
                    continue

                keywords = [kw.lower() for kw in meta.get("keywords", []) if kw]
                lexicon[category] = {
                    "layer": attr.lower(),
                    "keywords": keywords,
                    "weight": float(meta.get("weight", 1.0)),
                    "description": meta.get("description", ""),
                }
        return lexicon

    def _build_sentiment_groups(self) -> Dict[str, str]:
        """Map categories to sentiment polarity."""
        positive = ['positive_support', 'future_hope', 'respectful_acknowledgment', 
                   'constructive_suggestions', 'player_development_focus', 'youth_investment']
        negative = ['negative_criticism', 'frustration_expression', 'passionate_disappointment',
                   'strategic_frustration', 'patriotic_sadness', 'constructive_anger']
        neutral = ['neutral_observation', 'hopeful_skepticism']
        
        groups = {}
        for cat in positive:
            groups[cat] = 'positive'
        for cat in negative:
            groups[cat] = 'negative'
        for cat in neutral:
            groups[cat] = 'neutral'
        return groups

    def label_text(self, text: str, tokens: List[str] | None = None) -> Dict:
        text_lower = (text or "").lower()
        token_list = [tok.lower() for tok in (tokens or text_lower.split()) if tok]

        matches: List[Tuple[str, float, int, Dict]] = []
        for category, meta in self.lexicon.items():
            hit_count = 0
            for keyword in meta["keywords"]:
                if " " in keyword:
                    if keyword in text_lower:
                        hit_count += 1
                else:
                    hit_count += token_list.count(keyword)

            if hit_count >= self.min_hits:
                score = hit_count * meta["weight"]
                matches.append((category, score, hit_count, meta))

        if not matches:
            return {
                "label": "unknown",
                "layer": "unknown",
                "score": 0.0,
                "confidence": 0.0,
                "matches": [],
            }

        matches.sort(key=lambda item: item[1], reverse=True)
        top_category, top_score, top_hits, top_meta = matches[0]
        
        # Validasi minimum score threshold
        if top_score < self.min_score_threshold:
            return {
                "label": "unknown",
                "layer": "unknown",
                "score": top_score,
                "confidence": 0.0,
                "matches": [],
            }
        
        # Deteksi konflik sentiment
        sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
        for category, score, _, _ in matches:
            polarity = self.sentiment_groups.get(category, 'other')
            if polarity in sentiment_counts:
                sentiment_counts[polarity] += score
        
        total_score = sum(sentiment_counts.values())
        has_conflict = (sentiment_counts['positive'] > 0 and sentiment_counts['negative'] > 0)
        
        # Hitung confidence (normalized 0-1)
        if len(matches) > 1:
            second_score = matches[1][1]
            confidence = min(1.0, (top_score - second_score) / top_score) if top_score > 0 else 0.0
        else:
            confidence = 1.0 if top_score >= self.min_score_threshold else 0.0
        
        # Jika ada konflik kuat, tandai sebagai mixed
        if has_conflict and confidence < 0.6:
            top_category = "hopeful_skepticism"  # mixed emotion category
            top_meta = self.lexicon.get(top_category, top_meta)
        
        detailed_matches = [
            {
                "category": category,
                "layer": meta["layer"],
                "hits": hits,
                "score": score,
            }
            for category, score, hits, meta in matches
        ]

        return {
            "label": top_category,
            "layer": top_meta["layer"],
            "score": top_score,
            "confidence": round(confidence, 3),
            "sentiment_distribution": sentiment_counts,
            "matches": detailed_matches,
        }
