"""Normalization helpers for Indonesian text (stopwords, stemming, casing)."""
from __future__ import annotations

import logging
from typing import Iterable, List, Sequence, Set

import nltk
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import (
    StopWordRemoverFactory,
)


class TextNormalizer:
    """Remove stopwords, apply stemming, and normalize Indonesian tokens."""

    def __init__(self, extra_stopwords: Sequence[str] | None = None):
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

        self.stemmer = StemmerFactory().create_stemmer()
        self.stopwords = self._load_stopwords(extra_stopwords)
        self._stem_cache = {}  # Cache untuk speed up

    def _load_stopwords(self, extra: Sequence[str] | None) -> Set[str]:
        stopwords: Set[str] = set()

        stop_factory = StopWordRemoverFactory()
        stopwords.update(stop_factory.get_stop_words())

        try:
            nltk.data.find("corpora/stopwords")
        except LookupError:
            self.logger.info("Downloading NLTK stopwords corpus")
            nltk.download("stopwords")

        try:
            from nltk.corpus import stopwords as nltk_stopwords

            stopwords.update(nltk_stopwords.words("indonesian"))
        except LookupError:
            self.logger.warning(
                "NLTK Indonesian stopwords unavailable; proceeding with Sastrawi set"
            )
        except Exception as exc:
            self.logger.error("Failed loading NLTK stopwords: %s", exc)

        if extra:
            stopwords.update(word.lower() for word in extra)

        return stopwords

    def remove_stopwords(self, tokens: Iterable[str]) -> List[str]:
        return [tok for tok in tokens if tok and tok.lower() not in self.stopwords]

    def stem_word(self, token: str) -> str:
        if not token:
            return ""
        if token not in self._stem_cache:
            self._stem_cache[token] = self.stemmer.stem(token)
        return self._stem_cache[token]

    def stem_tokens(self, tokens: Iterable[str]) -> List[str]:
        return [self.stem_word(token) for token in tokens]

    def normalize_tokens(self, tokens: Iterable[str]) -> List[str]:
        tokens_without_stop = self.remove_stopwords(tokens)
        return self.stem_tokens(tokens_without_stop)

    def normalize_text(self, text: str, tokenizer) -> str:
        tokens = tokenizer.tokenize(text)
        normalized_tokens = self.normalize_tokens(tokens)
        return " ".join(normalized_tokens)
