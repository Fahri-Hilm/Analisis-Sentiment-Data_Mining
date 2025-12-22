"""
Complete Layer 3: Football-Specific Emotions Lexicon v3.0
Combines all 6 emotion categories with 3,000 words total
"""

from config.football_emotions_lexicon_v3_part1 import (
    PASSIONATE_DISAPPOINTMENT_LEXICON,
    STRATEGIC_FRUSTRATION_LEXICON
)
from config.football_emotions_lexicon_v3_part2 import (
    PATRIOTIC_SADNESS_LEXICON,
    CONSTRUCTIVE_ANGER_LEXICON,
    RESPECTFUL_ACKNOWLEDGMENT_LEXICON,
    FUTURE_HOPE_LEXICON
)

# GABUNGAN SEMUA LEXICON LAYER 3
FOOTBALL_EMOTIONS_LEXICON = {
    **PASSIONATE_DISAPPOINTMENT_LEXICON,
    **STRATEGIC_FRUSTRATION_LEXICON,
    **PATRIOTIC_SADNESS_LEXICON,
    **CONSTRUCTIVE_ANGER_LEXICON,
    **RESPECTFUL_ACKNOWLEDGMENT_LEXICON,
    **FUTURE_HOPE_LEXICON
}

# METADATA LENGKAP
LAYER3_LEXICON_INFO = {
    'version': '3.0',
    'layer': 'Layer 3 - Football-Specific Emotions',
    'total_words': len(FOOTBALL_EMOTIONS_LEXICON),
    'passionate_disappointment_words': len(PASSIONATE_DISAPPOINTMENT_LEXICON),
    'strategic_frustration_words': len(STRATEGIC_FRUSTRATION_LEXICON),
    'patriotic_sadness_words': len(PATRIOTIC_SADNESS_LEXICON),
    'constructive_anger_words': len(CONSTRUCTIVE_ANGER_LEXICON),
    'respectful_acknowledgment_words': len(RESPECTFUL_ACKNOWLEDGMENT_LEXICON),
    'future_hope_words': len(FUTURE_HOPE_LEXICON),
    'context': 'Timnas Indonesia gagal lolos Piala Dunia 2026, kalah Irak 1-0 babak 3, naturalisasi gagal',
    'slang_support': 'Twitter Indonesia 2025 (STY goblok parah, Garuda jatuh tragis, bangkit 2030)',
    'stemming_support': True,
    'weight_range': '(-2.0 to +2.0)',
    'categories': [
        'Passionate Disappointment (-2.0)',
        'Strategic Frustration (-1.5)',
        'Patriotic Sadness (-1.5)',
        'Constructive Anger (-1.0)',
        'Respectful Acknowledgment (+1.0)',
        'Future Hope (+1.5 to +2.0)'
    ]
}

def get_football_emotion_score(word):
    """Get football emotion score untuk kata tertentu"""
    return FOOTBALL_EMOTIONS_LEXICON.get(word.lower(), 0)

def get_football_emotion_category(word):
    """Get kategori emosi sepakbola untuk kata tertentu"""
    word_lower = word.lower()
    if word_lower in PASSIONATE_DISAPPOINTMENT_LEXICON:
        return 'Passionate Disappointment'
    elif word_lower in STRATEGIC_FRUSTRATION_LEXICON:
        return 'Strategic Frustration'
    elif word_lower in PATRIOTIC_SADNESS_LEXICON:
        return 'Patriotic Sadness'
    elif word_lower in CONSTRUCTIVE_ANGER_LEXICON:
        return 'Constructive Anger'
    elif word_lower in RESPECTFUL_ACKNOWLEDGMENT_LEXICON:
        return 'Respectful Acknowledgment'
    elif word_lower in FUTURE_HOPE_LEXICON:
        return 'Future Hope'
    else:
        return 'Unknown'

def get_layer3_stats():
    """Get statistik Layer 3 lexicon"""
    return LAYER3_LEXICON_INFO

def search_football_emotion_lexicon(query):
    """Cari kata dalam football emotion lexicon"""
    results = {}
    query_lower = query.lower()
    for word, score in FOOTBALL_EMOTIONS_LEXICON.items():
        if query_lower in word.lower():
            results[word] = {
                'score': score,
                'category': get_football_emotion_category(word)
            }
    return results

def get_football_emotion_distribution():
    """Get distribusi emosi sepakbola dalam lexicon"""
    return {
        'Passionate Disappointment': {
            'count': len(PASSIONATE_DISAPPOINTMENT_LEXICON),
            'range': '(-2.0)',
            'description': 'Kekecewaan mendalam dengan intensitas tinggi terhadap kegagalan timnas'
        },
        'Strategic Frustration': {
            'count': len(STRATEGIC_FRUSTRATION_LEXICON),
            'range': '(-1.5)',
            'description': 'Frustrasi terhadap strategi, taktik, dan keputusan pelatih'
        },
        'Patriotic Sadness': {
            'count': len(PATRIOTIC_SADNESS_LEXICON),
            'range': '(-1.5)',
            'description': 'Kesedihan dengan unsur nasionalisme dan kebanggaan bangsa'
        },
        'Constructive Anger': {
            'count': len(CONSTRUCTIVE_ANGER_LEXICON),
            'range': '(-1.0)',
            'description': 'Kemarahan yang membangun dengan kritik konstruktif untuk perbaikan'
        },
        'Respectful Acknowledgment': {
            'count': len(RESPECTFUL_ACKNOWLEDGMENT_LEXICON),
            'range': '(+1.0)',
            'description': 'Pengakuan terhadap kenyataan dengan respek kepada lawan'
        },
        'Future Hope': {
            'count': len(FUTURE_HOPE_LEXICON),
            'range': '(+1.5 to +2.0)',
            'description': 'Harapan dan optimisme untuk masa depan timnas Indonesia'
        }
    }

# Mapping untuk kemudahan akses
EMOTION_LEXICONS = {
    'passionate_disappointment': PASSIONATE_DISAPPOINTMENT_LEXICON,
    'strategic_frustration': STRATEGIC_FRUSTRATION_LEXICON,
    'patriotic_sadness': PATRIOTIC_SADNESS_LEXICON,
    'constructive_anger': CONSTRUCTIVE_ANGER_LEXICON,
    'respectful_acknowledgment': RESPECTFUL_ACKNOWLEDGMENT_LEXICON,
    'future_hope': FUTURE_HOPE_LEXICON
}
