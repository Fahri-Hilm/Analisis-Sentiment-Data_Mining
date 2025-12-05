"""
Enhanced Sentiment Lexicon untuk Indonesia
Lebih comprehensive dan aggressive labeling
"""
import pandas as pd
import logging
import re

logger = logging.getLogger(__name__)

# Expanded positive keywords
POSITIVE_KEYWORDS = {
    'support': ['dukung', 'support', 'semangat', 'ayo', 'yuk', 'mari', 'bersama'],
    'praise': ['bagus', 'hebat', 'keren', 'mantap', 'sip', 'oke', 'ok', 'baik', 'sempurna',
               'luar biasa', 'fantastis', 'menakjubkan', 'bravo', 'selamat', 'sukses',
               'menang', 'juara', 'terbaik', 'top', 'excellent', 'great', 'good', 'awesome'],
    'emotion': ['love', 'suka', 'senang', 'bangga', 'percaya', 'optimis', 'harapan', 'cinta',
                'gembira', 'bahagia', 'puas', 'puas hati'],
    'action': ['menang', 'gol', 'score', 'main bagus', 'bermain bagus', 'pertahankan', 'serang'],
}

# Expanded negative keywords
NEGATIVE_KEYWORDS = {
    'criticism': ['jelek', 'buruk', 'payah', 'gagal', 'rugi', 'kecewa', 'sedih', 'marah',
                  'kesal', 'frustasi', 'benci', 'hate', 'bad', 'terrible', 'awful', 'sucks'],
    'insult': ['bodoh', 'goblok', 'tolol', 'malu', 'memalukan', 'nista', 'hina', 'rendah'],
    'failure': ['kalah', 'hancur', 'rusak', 'tidak bisa', 'tidak mampu', 'lemah', 'parah',
                'mengerikan', 'bencana', 'tragis', 'menyedihkan'],
    'emotion': ['sedih', 'kecewa', 'marah', 'kesal', 'frustasi', 'putus asa', 'pesimis'],
    'action': ['kalah', 'gol kemasukan', 'kebobolan', 'error', 'salah', 'miss'],
}

# Neutral/Context keywords
NEUTRAL_KEYWORDS = [
    'pemain', 'pelatih', 'tim', 'pertandingan', 'laga', 'match', 'game', 'babak',
    'skor', 'score', 'hasil', 'statistik', 'data', 'analisis', 'taktik', 'strategi',
    'formasi', 'substitusi', 'kartu', 'wasit', 'referee', 'lapangan', 'stadion'
]

def count_keywords(text, keywords_dict):
    """Count keywords in text"""
    text = str(text).lower()
    count = 0
    for category, keywords in keywords_dict.items():
        for kw in keywords:
            if kw in text:
                count += 1
    return count

def has_negation(text):
    """Check if text has negation"""
    negations = ['tidak', 'bukan', 'jangan', 'belum', 'nggak', 'gak', 'ga']
    text = str(text).lower()
    return any(neg in text for neg in negations)

def auto_label_aggressive(df, text_column='clean_text', sentiment_column='core_sentiment'):
    """
    Aggressive auto-labeling untuk minimize unknown
    """
    df = df.copy()
    
    unknown_mask = df[sentiment_column].str.lower().str.contains('unknown', na=False)
    unknown_count = unknown_mask.sum()
    
    logger.info(f"Found {unknown_count} unknown sentiments")
    
    labeled_count = 0
    
    for idx in df[unknown_mask].index:
        text = str(df.loc[idx, text_column]).lower()
        
        # Count keywords
        pos_count = count_keywords(text, POSITIVE_KEYWORDS)
        neg_count = count_keywords(text, NEGATIVE_KEYWORDS)
        neutral_count = sum(1 for kw in NEUTRAL_KEYWORDS if kw in text)
        
        # Check for negation (flips sentiment)
        has_neg = has_negation(text)
        
        # Decision logic
        if pos_count > 0 and pos_count > neg_count:
            if has_neg:
                df.loc[idx, sentiment_column] = 'negative'
            else:
                df.loc[idx, sentiment_column] = 'positive'
            labeled_count += 1
        elif neg_count > 0 and neg_count > pos_count:
            if has_neg:
                df.loc[idx, sentiment_column] = 'positive'
            else:
                df.loc[idx, sentiment_column] = 'negative'
            labeled_count += 1
        elif neutral_count > 0 and pos_count == 0 and neg_count == 0:
            df.loc[idx, sentiment_column] = 'neutral'
            labeled_count += 1
        elif len(text.split()) > 0:
            # Fallback: if text is very short or has no keywords, mark as neutral
            if len(text.split()) < 3:
                df.loc[idx, sentiment_column] = 'neutral'
                labeled_count += 1
    
    logger.info(f"Auto-labeled {labeled_count} unknown sentiments")
    
    return df

def get_stats(df, sentiment_column='core_sentiment'):
    """Get statistics"""
    stats = df[sentiment_column].value_counts()
    total = len(df)
    
    return {
        'total': total,
        'positive': stats.get('positive', 0),
        'negative': stats.get('negative', 0),
        'neutral': stats.get('neutral', 0),
        'unknown': stats.get('unknown', 0),
        'unknown_pct': (stats.get('unknown', 0) / total * 100) if total > 0 else 0,
        'distribution': stats.to_dict()
    }

if __name__ == "__main__":
    df = pd.read_csv('data/processed/optimized_clean_comments_v6_emotion_labeled.csv')
    
    print("Before Enhanced Labeling:")
    stats_before = get_stats(df)
    print(f"  Total: {stats_before['total']}")
    print(f"  Positive: {stats_before['positive']}")
    print(f"  Negative: {stats_before['negative']}")
    print(f"  Neutral: {stats_before['neutral']}")
    print(f"  Unknown: {stats_before['unknown']} ({stats_before['unknown_pct']:.1f}%)")
    
    df = auto_label_aggressive(df)
    
    print("\nAfter Enhanced Labeling:")
    stats_after = get_stats(df)
    print(f"  Total: {stats_after['total']}")
    print(f"  Positive: {stats_after['positive']}")
    print(f"  Negative: {stats_after['negative']}")
    print(f"  Neutral: {stats_after['neutral']}")
    print(f"  Unknown: {stats_after['unknown']} ({stats_after['unknown_pct']:.1f}%)")
    
    df.to_csv('data/processed/optimized_clean_comments_v6_emotion_enhanced.csv', index=False)
    print("\nSaved to: data/processed/optimized_clean_comments_v6_emotion_enhanced.csv")
