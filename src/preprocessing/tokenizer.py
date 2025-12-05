"""Tokenization utilities specialized for Indonesian text."""
from __future__ import annotations

import logging
import re
from typing import Iterable, List

import nltk
from nltk.tokenize import word_tokenize


class IndonesianTokenizer:
    """Word tokenizer with lightweight normalization for Indonesian text."""

    def __init__(self, preserve_case: bool = False):
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

        self.preserve_case = preserve_case
        self._non_word_pattern = re.compile(r"^\W+$")
        self._ensure_nltk_resource("punkt")

    def _ensure_nltk_resource(self, resource: str) -> None:
        try:
            nltk.data.find(f"tokenizers/{resource}")
        except LookupError:
            self.logger.info("Downloading NLTK resource: %s", resource)
            nltk.download(resource)

    def tokenize(self, text: str) -> List[str]:
        """Tokenize a single text string."""
        if not text:
            return []

        try:
            tokens = word_tokenize(text)
        except LookupError:
            self._ensure_nltk_resource("punkt")
            tokens = word_tokenize(text)

        processed = []
        for token in tokens:
            token = token.strip()
            if not token or self._non_word_pattern.match(token):
                continue
            processed.append(token if self.preserve_case else token.lower())

        return processed

    def tokenize_batch(self, texts: Iterable[str]) -> List[List[str]]:
        """Tokenize an iterable of texts."""
        return [self.tokenize(text) for text in texts or []]
