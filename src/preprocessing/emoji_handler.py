"""
Emoji and Emoticon Handler for Indonesian Text
"""
import re

EMOJI_DICT = {
    '😂': 'tertawa',
    '😭': 'menangis',
    '😡': 'marah',
    '😢': 'sedih',
    '😍': 'cinta',
    '🔥': 'api',
    '👍': 'bagus',
    '👎': 'jelek',
    '❤️': 'cinta',
    '💔': 'patah_hati',
    '😤': 'kesal',
    '🤦': 'menggeleng',
    '😤': 'frustrasi',
    '🙏': 'doa',
    '😎': 'keren',
}

EMOTICON_DICT = {
    ':)': 'senang',
    ':(': 'sedih',
    ':D': 'sangat_senang',
    ':P': 'jahil',
    ':/': 'bingung',
    ':O': 'terkejut',
    ';)': 'wink',
    ':(': 'kecewa',
    ':|': 'datar',
    ':@': 'marah',
}

def convert_emoji_to_text(text: str) -> str:
    """Convert emoji to text representation"""
    for emoji, word in EMOJI_DICT.items():
        text = text.replace(emoji, f' {word} ')
    return text

def convert_emoticon_to_text(text: str) -> str:
    """Convert emoticon to text representation"""
    for emoticon, word in EMOTICON_DICT.items():
        text = text.replace(emoticon, f' {word} ')
    return text

def handle_repeated_chars(text: str, max_repeat: int = 2) -> str:
    """Handle repeated characters (e.g., 'saaangat' -> 'sangat')"""
    pattern = r'(.)\1{' + str(max_repeat) + ',}'
    return re.sub(pattern, r'\1' * max_repeat, text)

def process_emoji_emoticon(text: str) -> str:
    """Process emoji and emoticon in text"""
    text = convert_emoji_to_text(text)
    text = convert_emoticon_to_text(text)
    text = handle_repeated_chars(text)
    return text
