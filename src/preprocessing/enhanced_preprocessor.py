"""
Enhanced Text Preprocessor with Emoji, Emoticon, and Negation Handling
"""
import re
import logging
from typing import List
from src.preprocessing.emoji_handler import process_emoji_emoticon
from src.preprocessing.negation_handler import process_negation_intensifiers
from src.preprocessing.text_cleaner import TextCleaner

class EnhancedPreprocessor:
    """Enhanced preprocessing pipeline"""
    
    def __init__(self):
        self.logger = self._setup_logger()
        self.text_cleaner = TextCleaner()
    
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger
    
    def preprocess(self, text: str) -> str:
        """
        Full preprocessing pipeline:
        1. Emoji/emoticon handling
        2. Text cleaning
        3. Negation/intensifier handling
        """
        # Step 1: Handle emoji and emoticon
        text = process_emoji_emoticon(text)
        
        # Step 2: Clean text
        text = self.text_cleaner.clean(text)
        
        # Step 3: Handle negation and intensifiers
        text = process_negation_intensifiers(text)
        
        return text.strip()
    
    def preprocess_batch(self, texts: List[str]) -> List[str]:
        """Preprocess batch of texts"""
        return [self.preprocess(text) for text in texts]
