"""
Auto-label Unknown Sentiments dengan Keyword Matching
"""
import pandas as pd
import logging

logger = logging.getLogger(__name__)

# Sentiment keywords
POSITIVE_KEYWORDS = [
    'bagus', 'hebat', 'keren', 'mantap', 'sip', 'oke', 'ok', 'baik', 'sempurna',
    'luar biasa', 'fantastis', 'menakjubkan', 'bravo', 'selamat', 'sukses',
    'menang', 'juara', 'terbaik', 'top', 'excellent', 'great', 'good', 'awesome',
    'love', 'suka', 'senang', 'bangga', 'percaya', 'optimis', 'harapan'
]

NEGATIVE_KEYWORDS = [
    'jelek', 'buruk', 'payah', 'gagal', 'rugi', 'kecewa', 'sedih', 'marah',
    'kesal', 'frustasi', 'benci', 'hate', 'bad', 'terrible', 'awful', 'sucks',
    'kalah', 'hancur', 'rusak', 'bodoh', 'goblok', 'tolol', 'malu', 'memalukan',
    'tidak bisa', 'tidak mampu', 'lemah', 'buruk', 'parah', 'mengerikan'
]

def auto_label_unknown(df, text_column='clean_text', sentiment_column='core_sentiment'):
    """
    Auto-label unknown sentiments berdasarkan keyword matching
    """
    df = df.copy()
    
    # Find unknown rows
    unknown_mask = df[sentiment_column].str.lower().str.contains('unknown', na=False)
    unknown_count = unknown_mask.sum()
    
    logger.info(f"Found {unknown_count} unknown sentiments")
    
    labeled_count = 0
    
    for idx in df[unknown_mask].index:
        text = str(df.loc[idx, text_column]).lower()
        
        # Count positive and negative keywords
        pos_count = sum(1 for kw in POSITIVE_KEYWORDS if kw in text)
        neg_count = sum(1 for kw in NEGATIVE_KEYWORDS if kw in text)
        
        # Assign label based on keyword count
        if pos_count > neg_count and pos_count > 0:
            df.loc[idx, sentiment_column] = 'positive'
            labeled_count += 1
        elif neg_count > pos_count and neg_count > 0:
            df.loc[idx, sentiment_column] = 'negative'
            labeled_count += 1
    
    logger.info(f"Auto-labeled {labeled_count} unknown sentiments")
    
    return df

def get_labeling_stats(df, sentiment_column='core_sentiment'):
    """Get labeling statistics"""
    stats = df[sentiment_column].value_counts()
    unknown_pct = (stats.get('unknown', 0) / len(df)) * 100
    
    return {
        'total': len(df),
        'distribution': stats.to_dict(),
        'unknown_count': stats.get('unknown', 0),
        'unknown_percentage': unknown_pct
    }

if __name__ == "__main__":
    # Test
    df = pd.read_csv('data/processed/optimized_clean_comments_v6_emotion.csv')
    
    print("Before:")
    print(get_labeling_stats(df))
    
    df = auto_label_unknown(df)
    
    print("\nAfter:")
    print(get_labeling_stats(df))
    
    # Save
    df.to_csv('data/processed/optimized_clean_comments_v6_emotion_labeled.csv', index=False)
    print("\nSaved to: data/processed/optimized_clean_comments_v6_emotion_labeled.csv")
