"""High-level text preprocessing pipeline for Indonesian YouTube comments."""
from __future__ import annotations

import logging
from typing import Dict, List, Optional

import pandas as pd

from .normalizer import TextNormalizer
from .sentiment_labeler import SentimentLexiconLabeler
from .text_cleaner import TextCleaner
from .tokenizer import IndonesianTokenizer


class TextPreprocessor:
    """Combine cleaning, tokenization, normalization, and labeling."""

    def __init__(
        self,
        *,
        min_tokens: int = 1,
        remove_stopwords: bool = True,
        extra_stopwords: Optional[List[str]] = None,
        enable_labeling: bool = True,
    ):
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

        self.min_tokens = max(1, min_tokens)
        self.cleaner = TextCleaner()
        self.tokenizer = IndonesianTokenizer()
        self.normalizer = TextNormalizer(extra_stopwords=extra_stopwords)
        self.labeler = SentimentLexiconLabeler() if enable_labeling else None
        self.remove_stopwords = remove_stopwords

    def process_text(self, text: str) -> Dict:
        cleaned = self.cleaner.clean_text(text)
        cleaned = self.cleaner.clean_indonesian_text(cleaned)
        tokens = self.tokenizer.tokenize(cleaned)

        if self.remove_stopwords:
            tokens_no_stop = self.normalizer.remove_stopwords(tokens)
        else:
            tokens_no_stop = tokens

        stemmed_tokens = self.normalizer.stem_tokens(tokens_no_stop)
        stemmed_tokens = [tok for tok in stemmed_tokens if tok]

        if len(stemmed_tokens) < self.min_tokens:
            return {
                "clean_text": cleaned,
                "tokens": tokens,
                "tokens_no_stop": tokens_no_stop,
                "stemmed_tokens": stemmed_tokens,
                "normalized_text": " ".join(stemmed_tokens),
                "sentiment_label": "unknown",
                "sentiment_layer": "unknown",
                "sentiment_score": 0.0,
                "confidence": 0.0,
                "matched_categories": [],
            }

        normalized_text = " ".join(stemmed_tokens)
        sentiment_label = "unknown"
        sentiment_layer = "unknown"
        sentiment_score = 0.0
        confidence = 0.0
        matched_categories: List[Dict] = []

        if self.labeler:
            label_info = self.labeler.label_text(
                normalized_text,
                tokens=stemmed_tokens,
            )
            sentiment_label = label_info.get("label", "unknown")
            sentiment_layer = label_info.get("layer", "unknown")
            sentiment_score = float(label_info.get("score", 0.0))
            confidence = float(label_info.get("confidence", 0.0))
            matched_categories = label_info.get("matches", [])

        return {
            "clean_text": cleaned,
            "tokens": tokens,
            "tokens_no_stop": tokens_no_stop,
            "stemmed_tokens": stemmed_tokens,
            "normalized_text": normalized_text,
            "sentiment_label": sentiment_label,
            "sentiment_layer": sentiment_layer,
            "sentiment_score": sentiment_score,
            "confidence": confidence,
            "matched_categories": matched_categories,
        }

    def process_dataframe(
        self,
        df: pd.DataFrame,
        text_column: str = "text",
        drop_short: bool = True,
        batch_size: int = 1000,
    ) -> pd.DataFrame:
        """Process an entire dataframe and return augmented version."""
        if text_column not in df.columns:
            raise ValueError(f"Column '{text_column}' not found in dataframe")

        processed_records: List[Dict] = []
        total = len(df)
        
        for idx, text in enumerate(df[text_column].fillna(""), 1):
            if idx % 500 == 0 or idx == total:
                cache_size = len(self.normalizer._stem_cache) if hasattr(self.normalizer, '_stem_cache') else 0
                print(f"Processing: {idx}/{total} ({idx/total*100:.1f}%) | Cache: {cache_size} words", flush=True)
            processed_records.append(self.process_text(text))

        processed_df = pd.DataFrame(processed_records)
        result = pd.concat([df.reset_index(drop=True), processed_df], axis=1)

        if drop_short:
            mask = result["normalized_text"].astype(str).str.len() >= 3
            result = result[mask]

        return result.reset_index(drop=True)
