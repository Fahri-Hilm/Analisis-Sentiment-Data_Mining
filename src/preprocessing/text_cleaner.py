"""
Text Cleaner for 9-Layer Sentiment Analysis

This module provides comprehensive text cleaning functionality
for Indonesian language text preprocessing.
"""

import re
import string
import logging
from typing import List, Dict, Optional, Pattern
from urllib.parse import urlparse

class TextCleaner:
    """
    Text Cleaner for Indonesian Language
    
    This class handles various text cleaning operations including
    URL removal, mention removal, hashtag processing, etc.
    """
    
    def __init__(self):
        """Initialize text cleaner with logging"""
        self.logger = self._setup_logger()
        
        # Storage for compiled Indonesian regexes
        self.indonesian_patterns: Dict[str, Pattern[str]] = {}

        # Pattern specs compiled later
        self._indonesian_pattern_specs = {
            'repeated_chars': r'([a-zA-Z])\1{2,}',
            'repeated_words': r'\b(\w+)(\s+\1){2,}\b',
            'excessive_punctuation': r'([!?.,])\1{2,}',
            'mixed_case': r'\b([A-Z][a-z]+[A-Z][a-z]+)\b',
            'numbers_in_words': r'\b(satu|dua|tiga|empat|lima|enam|tujuh|delapan|sembilan|sepuluh|puluh|ratus|ribu|juta|miliar)\b'
        }

        # Compile regex patterns for efficiency
        self._compile_patterns()
        
    def _setup_logger(self) -> logging.Logger:
        """Setup logging configuration"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def _compile_patterns(self):
        """Compile regex patterns for efficiency"""
        self.patterns = {
            # URLs
            'url': re.compile(
                r'http\S+|www\S+|https\S+',
                re.IGNORECASE
            ),
            
            # Mentions (@username)
            'mention': re.compile(
                r'@\w+',
                re.IGNORECASE
            ),
            
            # Hashtags (#tag)
            'hashtag': re.compile(
                r'#(\w+)',
                re.IGNORECASE
            ),
            
            # Email addresses
            'email': re.compile(
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                re.IGNORECASE
            ),
            
            # Phone numbers
            'phone': re.compile(
                r'\b(\+62|62|0)[0-9]{8,12}\b',
                re.IGNORECASE
            ),
            
            # Numbers
            'numbers': re.compile(r'\d+'),
            
            # Special characters and punctuation
            'special_chars': re.compile(r'[^a-zA-Z\s]'),
            
            # Extra whitespace
            'whitespace': re.compile(r'\s+'),
            
            # Line breaks and tabs
            'line_breaks': re.compile(r'[\n\r\t]'),
            
            # HTML tags
            'html': re.compile(r'<[^>]+>'),
            
            # Emojis (basic pattern)
            'emoji': re.compile(
                "["
                "\U0001F600-\U0001F64F"  # emoticons
                "\U0001F300-\U0001F5FF"  # symbols & pictographs
                "\U0001F680-\U0001F6FF"  # transport & map symbols
                "\U0001F1E0-\U0001F1FF"  # flags
                "\U00002702-\U000027B0"
                "\U000024C2-\U0001F251"
                "]",
                re.UNICODE,
            )
        }
        
        # Compile Indonesian patterns without mutating during iteration
        self.indonesian_patterns = {
            name: re.compile(pattern, re.IGNORECASE)
            for name, pattern in self._indonesian_pattern_specs.items()
        }
    
    def clean_text(self, text: str, options: Optional[Dict] = None) -> str:
        """
        Clean text with specified options
        
        Args:
            text (str): Input text to clean
            options (Dict): Cleaning options
            
        Returns:
            str: Cleaned text
        """
        if not text or not isinstance(text, str):
            return ""
        
        # Default options
        default_options = {
            'remove_urls': True,
            'remove_mentions': True,
            'process_hashtags': True,
            'remove_emails': True,
            'remove_phones': True,
            'remove_numbers': True,
            'remove_special_chars': True,
            'remove_emojis': True,
            'normalize_whitespace': True,
            'convert_to_lowercase': True,
            'remove_repeated_chars': True,
            'remove_repeated_words': True,
            'remove_excessive_punctuation': True
        }
        
        # Merge with provided options
        if options:
            default_options.update(options)
        
        cleaned_text = text
        
        try:
            # Remove HTML tags
            cleaned_text = self.patterns['html'].sub(' ', cleaned_text)
            
            # Remove URLs
            if default_options['remove_urls']:
                cleaned_text = self.patterns['url'].sub(' ', cleaned_text)
            
            # Remove mentions
            if default_options['remove_mentions']:
                cleaned_text = self.patterns['mention'].sub(' ', cleaned_text)
            
            # Process hashtags
            if default_options['process_hashtags']:
                cleaned_text = self._process_hashtags(cleaned_text)
            
            # Remove emails
            if default_options['remove_emails']:
                cleaned_text = self.patterns['email'].sub(' ', cleaned_text)
            
            # Remove phone numbers
            if default_options['remove_phones']:
                cleaned_text = self.patterns['phone'].sub(' ', cleaned_text)
            
            # Remove numbers
            if default_options['remove_numbers']:
                cleaned_text = self.patterns['numbers'].sub(' ', cleaned_text)
            
            # Remove emojis
            if default_options['remove_emojis']:
                cleaned_text = self.patterns['emoji'].sub(' ', cleaned_text)
            
            # Remove excessive punctuation
            if default_options['remove_excessive_punctuation']:
                cleaned_text = self.indonesian_patterns['excessive_punctuation'].sub(r'\1', cleaned_text)
            
            # Remove repeated characters
            if default_options['remove_repeated_chars']:
                cleaned_text = self.indonesian_patterns['repeated_chars'].sub(r'\1', cleaned_text)
            
            # Remove repeated words
            if default_options['remove_repeated_words']:
                cleaned_text = self.indonesian_patterns['repeated_words'].sub(r'\1', cleaned_text)
            
            # Remove special characters (keep letters and spaces)
            if default_options['remove_special_chars']:
                cleaned_text = self.patterns['special_chars'].sub(' ', cleaned_text)
            
            # Normalize whitespace
            if default_options['normalize_whitespace']:
                # Replace line breaks and tabs with spaces
                cleaned_text = self.patterns['line_breaks'].sub(' ', cleaned_text)
                # Normalize multiple spaces
                cleaned_text = self.patterns['whitespace'].sub(' ', cleaned_text)
            
            # Convert to lowercase
            if default_options['convert_to_lowercase']:
                cleaned_text = cleaned_text.lower()
            
            # Strip leading/trailing whitespace
            cleaned_text = cleaned_text.strip()
            
            # Final check for empty or very short text
            if len(cleaned_text) < 3:
                self.logger.warning(f"Text too short after cleaning: '{text}' -> '{cleaned_text}'")
                return ""
            
            return cleaned_text
            
        except Exception as e:
            self.logger.error(f"Error cleaning text: {e}")
            return text
    
    def _process_hashtags(self, text: str) -> str:
        """
        Process hashtags - remove # but keep the text
        
        Args:
            text (str): Input text
            
        Returns:
            str: Text with processed hashtags
        """
        def replace_hashtag(match):
            hashtag_text = match.group(1)
            return hashtag_text
        
        return self.patterns['hashtag'].sub(replace_hashtag, text)
    
    def clean_indonesian_text(self, text: str) -> str:
        """
        Clean text with Indonesian-specific rules
        
        Args:
            text (str): Input text
            
        Returns:
            str: Indonesian-cleaned text
        """
        if not text:
            return ""
        
        cleaned_text = text
        
        try:
            # Remove Indonesian-specific patterns
            # Normalize common Indonesian abbreviations
            cleaned_text = self._normalize_indonesian_abbreviations(cleaned_text)
            
            # Remove Indonesian repeated characters
            cleaned_text = self.indonesian_patterns['repeated_chars'].sub(r'\1', cleaned_text)
            
            # Remove Indonesian repeated words
            cleaned_text = self.indonesian_patterns['repeated_words'].sub(r'\1', cleaned_text)
            
            # Handle Indonesian-specific characters
            cleaned_text = self._normalize_indonesian_characters(cleaned_text)
            
            return cleaned_text
            
        except Exception as e:
            self.logger.error(f"Error cleaning Indonesian text: {e}")
            return text
    
    def _normalize_indonesian_abbreviations(self, text: str) -> str:
        """
        Normalize common Indonesian abbreviations
        
        Args:
            text (str): Input text
            
        Returns:
            str: Text with normalized abbreviations
        """
        abbreviations = {
            'yg': 'yang',
            'ygga': 'yang',
            'dgn': 'dengan',
            'dg': 'dengan',
            'tdk': 'tidak',
            'gk': 'tidak',
            'sdh': 'sudah',
            'sdhkan': 'sudahkan',
            'blm': 'belum',
            'blmkan': 'belumlah',
            'utk': 'untuk',
            'krn': 'karena',
            'karna': 'karena',
            'bsk': 'bisa',
            'bisa': 'bisa',
            'jgn': 'jangan',
            'jgnkan': 'jangan',
            'dll': 'dan lain-lain',
            'dll': 'dan lain-lain',
            'etc': 'dan lain-lain',
            'wkt': 'waktu',
            'skrg': 'sekarang',
            'sekarang': 'sekarang',
            'mrk': 'mereka',
            'kita': 'kita',
            'kami': 'kami',
            'anda': 'anda',
            'kalian': 'kalian',
            'dia': 'dia',
            'beliau': 'beliau',
            'pd': 'pada',
            'di': 'di',
            'ke': 'ke',
            'dari': 'dari',
            'untuk': 'untuk',
            'agar': 'agar',
            'supaya': 'supaya'
        }
        
        # Replace abbreviations
        for abbr, full_form in abbreviations.items():
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(abbr) + r'\b'
            text = re.sub(pattern, full_form, text, flags=re.IGNORECASE)
        
        return text
    
    def _normalize_indonesian_characters(self, text: str) -> str:
        """
        Normalize Indonesian-specific characters
        
        Args:
            text (str): Input text
            
        Returns:
            str: Text with normalized characters
        """
        # Normalize common Indonesian character variations
        char_map = {
            'é': 'e',
            'è': 'e',
            'ë': 'e',
            'á': 'a',
            'à': 'a',
            'â': 'a',
            'ã': 'a',
            'í': 'i',
            'ì': 'i',
            'î': 'i',
            'ó': 'o',
            'ò': 'o',
            'ô': 'o',
            'õ': 'o',
            'ú': 'u',
            'ù': 'u',
            'û': 'u',
            'ý': 'y',
            'ÿ': 'y',
            'ç': 'c',
            'ñ': 'n',
            'ß': 'ss'
        }
        
        for char, replacement in char_map.items():
            text = text.replace(char, replacement)
        
        return text
    
    def get_cleaning_stats(self, original_text: str, cleaned_text: str) -> Dict:
        """
        Get statistics about the cleaning process
        
        Args:
            original_text (str): Original text
            cleaned_text (str): Cleaned text
            
        Returns:
            Dict: Cleaning statistics
        """
        return {
            'original_length': len(original_text),
            'cleaned_length': len(cleaned_text),
            'reduction_percentage': ((len(original_text) - len(cleaned_text)) / len(original_text)) * 100 if original_text else 0,
            'original_words': len(original_text.split()),
            'cleaned_words': len(cleaned_text.split()),
            'word_reduction_percentage': ((len(original_text.split()) - len(cleaned_text.split())) / len(original_text.split())) * 100 if original_text.split() else 0
        }
    
    def batch_clean_texts(self, texts: List[str], options: Optional[Dict] = None) -> List[str]:
        """
        Clean multiple texts in batch
        
        Args:
            texts (List[str]): List of texts to clean
            options (Dict): Cleaning options
            
        Returns:
            List[str]: List of cleaned texts
        """
        cleaned_texts = []
        
        for i, text in enumerate(texts):
            if i % 100 == 0:
                self.logger.info(f"Cleaning text {i+1}/{len(texts)}")
            
            cleaned_text = self.clean_text(text, options)
            cleaned_texts.append(cleaned_text)
        
        self.logger.info(f"Cleaned {len(texts)} texts")
        return cleaned_texts
    
    def validate_cleaned_text(self, text: str) -> bool:
        """
        Validate if cleaned text meets quality criteria
        
        Args:
            text (str): Cleaned text to validate
            
        Returns:
            bool: True if text meets quality criteria
        """
        if not text or len(text.strip()) < 3:
            return False
        
        # Check if text contains only letters and spaces
        if not re.match(r'^[a-zA-Z\s]+$', text):
            return False
        
        # Check if text has meaningful content (not just repeated characters)
        if len(set(text.lower())) < 3:
            return False
        
        return True


def main():
    """
    Main function to test text cleaning functionality
    """
    cleaner = TextCleaner()
    
    # Test texts
    test_texts = [
        "Ini adalah contoh text dengan URL https://example.com dan mention @username #hashtag",
        "Timnas Indonesia GAGAL lagi di kualifikasi Piala Dunia!!! 😭😭",
        "Sangat kecewa dengan performa timnas... seharusnya lebih baik!!!",
        "Email: test@example.com, Phone: +628123456789",
        "RT @user: Indonesia tidak lolos Piala Dunia 2026 #PialaDunia #Timnas"
    ]
    
    print("Text Cleaning Test")
    print("=" * 50)
    
    for i, text in enumerate(test_texts):
        print(f"\nTest {i+1}:")
        print(f"Original: {text}")
        
        cleaned = cleaner.clean_text(text)
        print(f"Cleaned: {cleaned}")
        
        stats = cleaner.get_cleaning_stats(text, cleaned)
        print(f"Stats: {stats}")


if __name__ == "__main__":
    main()