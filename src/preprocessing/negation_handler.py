"""
Negation Handler for Indonesian Text
Handles negation patterns to preserve context
"""
import re

NEGATION_WORDS = {
    'tidak': 'NEG',
    'bukan': 'NEG',
    'jangan': 'NEG',
    'belum': 'NEG',
    'tiada': 'NEG',
    'tanpa': 'NEG',
    'nggak': 'NEG',
    'gak': 'NEG',
    'ga': 'NEG',
}

def handle_negation(text: str) -> str:
    """
    Handle negation by prefixing negation marker to following words
    Example: 'tidak bagus' -> 'NEG_bagus'
    """
    words = text.split()
    result = []
    
    for i, word in enumerate(words):
        lower_word = word.lower()
        
        if lower_word in NEGATION_WORDS:
            result.append(NEGATION_WORDS[lower_word])
            if i + 1 < len(words):
                next_word = words[i + 1]
                result.append(f"NEG_{next_word}")
                words[i + 1] = None
        elif word is not None:
            result.append(word)
    
    return ' '.join([w for w in result if w is not None])

def handle_intensifiers(text: str) -> str:
    """Handle intensifiers like 'sangat', 'sekali', 'banget'"""
    intensifiers = ['sangat', 'sekali', 'banget', 'amat', 'luar_biasa']
    
    for intensifier in intensifiers:
        pattern = rf'\b{intensifier}\s+(\w+)'
        text = re.sub(pattern, rf'INTENS_{intensifier}_\1', text, flags=re.IGNORECASE)
    
    return text

def process_negation_intensifiers(text: str) -> str:
    """Process both negation and intensifiers"""
    text = handle_negation(text)
    text = handle_intensifiers(text)
    return text
