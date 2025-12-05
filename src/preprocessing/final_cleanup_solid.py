"""
Final Cleanup - Solid Logic untuk Short Text
Tidak asal tebak, hanya label jika ada evidence yang jelas
"""
import pandas as pd
import logging

logger = logging.getLogger(__name__)

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

def final_cleanup_solid(df):
    """
    Final cleanup dengan solid logic
    Untuk short text: HANYA label jika ada keyword yang jelas
    Jika tidak ada keyword → UNKNOWN (jangan asal tebak)
    """
    df = df.copy()
    
    unknown_mask = df['core_sentiment'].str.lower().str.contains('unknown', na=False)
    unknown_count = unknown_mask.sum()
    
    logger.info(f"Final cleanup solid: {unknown_count} unknown sentiments")
    
    labeled_count = 0
    kept_unknown = 0
    
    for idx in df[unknown_mask].index:
        text = str(df.loc[idx, 'clean_text']).lower()
        word_count = len(text.split())
        
        # Count keywords
        pos_count = count_keywords(text, POSITIVE_KEYWORDS)
        neg_count = count_keywords(text, NEGATIVE_KEYWORDS)
        has_neg = has_negation(text)
        total_keywords = pos_count + neg_count
        
        # ===== RULE 1: Ada keyword yang jelas =====
        if pos_count > 0 and pos_count > neg_count:
            if has_neg:
                df.loc[idx, 'core_sentiment'] = 'negative'
            else:
                df.loc[idx, 'core_sentiment'] = 'positive'
            labeled_count += 1
            continue
        
        if neg_count > 0 and neg_count > pos_count:
            if has_neg:
                df.loc[idx, 'core_sentiment'] = 'positive'
            else:
                df.loc[idx, 'core_sentiment'] = 'negative'
            labeled_count += 1
            continue
        
        # ===== RULE 2: Equal keywords - gunakan punctuation =====
        if pos_count > 0 and pos_count == neg_count:
            if '!' in text:
                df.loc[idx, 'core_sentiment'] = 'positive'
            elif '?' in text:
                df.loc[idx, 'core_sentiment'] = 'neutral'
            else:
                df.loc[idx, 'core_sentiment'] = 'neutral'
            labeled_count += 1
            continue
        
        # ===== RULE 3: Tidak ada keyword =====
        # Untuk short text: JANGAN asal tebak, tetap UNKNOWN
        if total_keywords == 0:
            # Hanya label jika ada CLEAR evidence
            
            # Evidence 1: Question mark = NEUTRAL (pasti pertanyaan)
            if '?' in text and word_count >= 2:
                df.loc[idx, 'core_sentiment'] = 'neutral'
                labeled_count += 1
                continue
            
            # Evidence 2: Exclamation + specific pattern
            if '!' in text and word_count >= 2:
                # Check untuk specific words yang pasti neutral
                neutral_words = ['pemain', 'pelatih', 'tim', 'pertandingan', 'laga', 'match', 'game']
                if any(w in text for w in neutral_words):
                    df.loc[idx, 'core_sentiment'] = 'neutral'
                    labeled_count += 1
                    continue
            
            # Evidence 3: Specific neutral patterns
            neutral_patterns = ['pemain', 'pelatih', 'tim', 'pertandingan', 'laga', 'match', 'game', 
                              'skor', 'score', 'hasil', 'statistik', 'data', 'analisis', 'taktik']
            if any(p in text for p in neutral_patterns):
                df.loc[idx, 'core_sentiment'] = 'neutral'
                labeled_count += 1
                continue
            
            # Jika tidak ada evidence yang jelas → TETAP UNKNOWN
            # Jangan asal tebak!
            kept_unknown += 1
            continue
    
    logger.info(f"Labeled: {labeled_count}, Kept Unknown: {kept_unknown}")
    
    return df

def get_final_stats(df):
    """Get final statistics"""
    stats = df['core_sentiment'].value_counts()
    total = len(df)
    
    print(f"\n{'='*70}")
    print(f"FINAL STATISTICS - SOLID LOGIC")
    print(f"{'='*70}")
    print(f"Total Comments: {total}")
    print(f"Positive: {stats.get('positive', 0):>6} ({stats.get('positive', 0)/total*100:>5.1f}%)")
    print(f"Negative: {stats.get('negative', 0):>6} ({stats.get('negative', 0)/total*100:>5.1f}%)")
    print(f"Neutral:  {stats.get('neutral', 0):>6} ({stats.get('neutral', 0)/total*100:>5.1f}%)")
    print(f"Unknown:  {stats.get('unknown', 0):>6} ({stats.get('unknown', 0)/total*100:>5.1f}%)")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    df = pd.read_csv('data/processed/optimized_clean_comments_v6_emotion_enhanced.csv')
    
    print("Before Final Cleanup (Solid):")
    get_final_stats(df)
    
    df = final_cleanup_solid(df)
    
    print("After Final Cleanup (Solid):")
    get_final_stats(df)
    
    df.to_csv('data/processed/optimized_clean_comments_v6_emotion_final_solid.csv', index=False)
    print("Saved to: data/processed/optimized_clean_comments_v6_emotion_final_solid.csv")
