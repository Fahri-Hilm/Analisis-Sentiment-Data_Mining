"""
Final Cleanup - Improved dengan Logic yang Lebih Solid
Tidak asal tebak, tapi berdasarkan evidence
"""
import pandas as pd
import logging

logger = logging.getLogger(__name__)

# Comprehensive keyword dictionary
POSITIVE_KEYWORDS = [
    'bagus', 'hebat', 'keren', 'mantap', 'sip', 'oke', 'ok', 'baik', 'sempurna',
    'luar biasa', 'fantastis', 'menakjubkan', 'bravo', 'selamat', 'sukses',
    'menang', 'juara', 'terbaik', 'top', 'excellent', 'great', 'good', 'awesome',
    'love', 'suka', 'senang', 'bangga', 'percaya', 'optimis', 'harapan', 'cinta',
    'gembira', 'bahagia', 'puas', 'dukung', 'support', 'semangat', 'ayo', 'yuk',
    'gol', 'score', 'menang', 'kemenangan', 'pertahankan', 'serang', 'main bagus'
]

NEGATIVE_KEYWORDS = [
    'jelek', 'buruk', 'payah', 'gagal', 'rugi', 'kecewa', 'sedih', 'marah',
    'kesal', 'frustasi', 'benci', 'hate', 'bad', 'terrible', 'awful', 'sucks',
    'bodoh', 'goblok', 'tolol', 'malu', 'memalukan', 'nista', 'hina', 'rendah',
    'kalah', 'hancur', 'rusak', 'tidak bisa', 'tidak mampu', 'lemah', 'parah',
    'mengerikan', 'bencana', 'tragis', 'menyedihkan', 'gol kemasukan', 'kebobolan',
    'error', 'salah', 'miss', 'kegagalan', 'kekalahan'
]

NEGATION_WORDS = ['tidak', 'bukan', 'jangan', 'belum', 'nggak', 'gak', 'ga', 'tiada']

def count_keywords(text, keywords):
    """Count keywords dalam text"""
    text = str(text).lower()
    return sum(1 for kw in keywords if kw in text)

def has_negation(text):
    """Check negation"""
    text = str(text).lower()
    return any(neg in text for neg in NEGATION_WORDS)

def final_cleanup_improved(df):
    """
    Final cleanup dengan logic yang lebih solid
    Hanya label jika ada evidence yang jelas
    """
    df = df.copy()
    
    unknown_mask = df['core_sentiment'].str.lower().str.contains('unknown', na=False)
    unknown_count = unknown_mask.sum()
    
    logger.info(f"Final cleanup improved: {unknown_count} unknown sentiments")
    
    labeled_count = 0
    confidence_scores = []
    
    for idx in df[unknown_mask].index:
        text = str(df.loc[idx, 'clean_text']).lower()
        
        # Count keywords
        pos_count = count_keywords(text, POSITIVE_KEYWORDS)
        neg_count = count_keywords(text, NEGATIVE_KEYWORDS)
        has_neg = has_negation(text)
        
        # Calculate confidence score
        total_keywords = pos_count + neg_count
        
        # RULE 1: Clear positive evidence
        if pos_count > 0 and pos_count > neg_count:
            if has_neg:
                # "tidak bagus" → negative
                df.loc[idx, 'core_sentiment'] = 'negative'
                confidence = neg_count / max(total_keywords, 1)
            else:
                df.loc[idx, 'core_sentiment'] = 'positive'
                confidence = pos_count / max(total_keywords, 1)
            labeled_count += 1
            confidence_scores.append(confidence)
            continue
        
        # RULE 2: Clear negative evidence
        if neg_count > 0 and neg_count > pos_count:
            if has_neg:
                # "tidak jelek" → positive
                df.loc[idx, 'core_sentiment'] = 'positive'
                confidence = pos_count / max(total_keywords, 1)
            else:
                df.loc[idx, 'core_sentiment'] = 'negative'
                confidence = neg_count / max(total_keywords, 1)
            labeled_count += 1
            confidence_scores.append(confidence)
            continue
        
        # RULE 3: Equal keywords - use punctuation as tiebreaker
        if pos_count > 0 and pos_count == neg_count:
            if '!' in text:
                # Exclamation usually positive
                df.loc[idx, 'core_sentiment'] = 'positive'
            elif '?' in text:
                # Question usually neutral
                df.loc[idx, 'core_sentiment'] = 'neutral'
            else:
                # Default to neutral
                df.loc[idx, 'core_sentiment'] = 'neutral'
            labeled_count += 1
            confidence_scores.append(0.5)
            continue
        
        # RULE 4: No keywords found - use text characteristics
        if total_keywords == 0:
            # Check for question mark
            if '?' in text:
                df.loc[idx, 'core_sentiment'] = 'neutral'
                labeled_count += 1
                confidence_scores.append(0.3)
                continue
            
            # Check for exclamation mark (usually emotional, but without keywords = neutral)
            if '!' in text:
                df.loc[idx, 'core_sentiment'] = 'neutral'
                labeled_count += 1
                confidence_scores.append(0.3)
                continue
            
            # Very short text (< 3 words) - likely neutral
            if len(text.split()) < 3:
                df.loc[idx, 'core_sentiment'] = 'neutral'
                labeled_count += 1
                confidence_scores.append(0.2)
                continue
            
            # Default: neutral (conservative approach)
            df.loc[idx, 'core_sentiment'] = 'neutral'
            labeled_count += 1
            confidence_scores.append(0.1)
    
    avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
    
    logger.info(f"Labeled: {labeled_count}, Avg Confidence: {avg_confidence:.2f}")
    
    return df

def get_final_stats(df):
    """Get final statistics"""
    stats = df['core_sentiment'].value_counts()
    total = len(df)
    
    print(f"\n{'='*70}")
    print(f"FINAL STATISTICS - IMPROVED")
    print(f"{'='*70}")
    print(f"Total Comments: {total}")
    print(f"Positive: {stats.get('positive', 0):>6} ({stats.get('positive', 0)/total*100:>5.1f}%)")
    print(f"Negative: {stats.get('negative', 0):>6} ({stats.get('negative', 0)/total*100:>5.1f}%)")
    print(f"Neutral:  {stats.get('neutral', 0):>6} ({stats.get('neutral', 0)/total*100:>5.1f}%)")
    print(f"Unknown:  {stats.get('unknown', 0):>6} ({stats.get('unknown', 0)/total*100:>5.1f}%)")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    df = pd.read_csv('data/processed/optimized_clean_comments_v6_emotion_enhanced.csv')
    
    print("Before Final Cleanup (Improved):")
    get_final_stats(df)
    
    df = final_cleanup_improved(df)
    
    print("After Final Cleanup (Improved):")
    get_final_stats(df)
    
    df.to_csv('data/processed/optimized_clean_comments_v6_emotion_final_improved.csv', index=False)
    print("Saved to: data/processed/optimized_clean_comments_v6_emotion_final_improved.csv")
