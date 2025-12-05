"""
Final Cleanup - Hybrid Approach
Solid logic + Smart fallback untuk short text
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

NEUTRAL_KEYWORDS = [
    'pemain', 'pelatih', 'tim', 'pertandingan', 'laga', 'match', 'game', 'babak',
    'skor', 'score', 'hasil', 'statistik', 'data', 'analisis', 'taktik', 'strategi',
    'formasi', 'substitusi', 'kartu', 'wasit', 'referee', 'lapangan', 'stadion'
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

def final_cleanup_hybrid(df):
    """
    Hybrid approach:
    1. Solid logic untuk text dengan keywords
    2. Smart fallback untuk short text tanpa keywords
    """
    df = df.copy()
    
    unknown_mask = df['core_sentiment'].str.lower().str.contains('unknown', na=False)
    unknown_count = unknown_mask.sum()
    
    logger.info(f"Final cleanup hybrid: {unknown_count} unknown sentiments")
    
    labeled_count = 0
    
    for idx in df[unknown_mask].index:
        text = str(df.loc[idx, 'clean_text']).lower()
        word_count = len(text.split())
        
        # Count keywords
        pos_count = count_keywords(text, POSITIVE_KEYWORDS)
        neg_count = count_keywords(text, NEGATIVE_KEYWORDS)
        neutral_count = count_keywords(text, NEUTRAL_KEYWORDS)
        has_neg = has_negation(text)
        total_keywords = pos_count + neg_count
        
        # ===== PHASE 1: SOLID LOGIC (Ada keyword yang jelas) =====
        
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
        
        if pos_count > 0 and pos_count == neg_count:
            if '!' in text:
                df.loc[idx, 'core_sentiment'] = 'positive'
            elif '?' in text:
                df.loc[idx, 'core_sentiment'] = 'neutral'
            else:
                df.loc[idx, 'core_sentiment'] = 'neutral'
            labeled_count += 1
            continue
        
        # ===== PHASE 2: SMART FALLBACK (Tidak ada keyword) =====
        
        if total_keywords == 0:
            # Strategy 1: Question mark = NEUTRAL (pasti pertanyaan)
            if '?' in text:
                df.loc[idx, 'core_sentiment'] = 'neutral'
                labeled_count += 1
                continue
            
            # Strategy 2: Neutral keywords found = NEUTRAL
            if neutral_count > 0:
                df.loc[idx, 'core_sentiment'] = 'neutral'
                labeled_count += 1
                continue
            
            # Strategy 3: Exclamation mark + short text
            # Exclamation biasanya emotional, tapi tanpa keywords = ambiguous
            # Jadi label sebagai NEUTRAL (conservative)
            if '!' in text and word_count < 5:
                df.loc[idx, 'core_sentiment'] = 'neutral'
                labeled_count += 1
                continue
            
            # Strategy 4: Very short text (1-2 words) tanpa keywords
            # Terlalu pendek untuk determine sentiment dengan pasti
            # Tapi jika ada punctuation, gunakan itu sebagai clue
            if word_count <= 2:
                if '!' in text:
                    # Exclamation on very short text = likely positive
                    df.loc[idx, 'core_sentiment'] = 'positive'
                elif '?' in text:
                    # Question = neutral
                    df.loc[idx, 'core_sentiment'] = 'neutral'
                else:
                    # No punctuation, no keywords = neutral (safest)
                    df.loc[idx, 'core_sentiment'] = 'neutral'
                labeled_count += 1
                continue
            
            # Strategy 5: Medium text (3-5 words) tanpa keywords
            # Gunakan punctuation sebagai clue
            if word_count <= 5:
                if '!' in text:
                    df.loc[idx, 'core_sentiment'] = 'neutral'
                elif '?' in text:
                    df.loc[idx, 'core_sentiment'] = 'neutral'
                else:
                    df.loc[idx, 'core_sentiment'] = 'neutral'
                labeled_count += 1
                continue
            
            # Strategy 6: Longer text (> 5 words) tanpa keywords
            # Jika masih tidak ada keywords, label sebagai neutral
            df.loc[idx, 'core_sentiment'] = 'neutral'
            labeled_count += 1
    
    logger.info(f"Labeled: {labeled_count}")
    
    return df

def get_final_stats(df):
    """Get final statistics"""
    stats = df['core_sentiment'].value_counts()
    total = len(df)
    
    print(f"\n{'='*70}")
    print(f"FINAL STATISTICS - HYBRID APPROACH")
    print(f"{'='*70}")
    print(f"Total Comments: {total}")
    print(f"Positive: {stats.get('positive', 0):>6} ({stats.get('positive', 0)/total*100:>5.1f}%)")
    print(f"Negative: {stats.get('negative', 0):>6} ({stats.get('negative', 0)/total*100:>5.1f}%)")
    print(f"Neutral:  {stats.get('neutral', 0):>6} ({stats.get('neutral', 0)/total*100:>5.1f}%)")
    print(f"Unknown:  {stats.get('unknown', 0):>6} ({stats.get('unknown', 0)/total*100:>5.1f}%)")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    df = pd.read_csv('data/processed/optimized_clean_comments_v6_emotion_enhanced.csv')
    
    print("Before Final Cleanup (Hybrid):")
    get_final_stats(df)
    
    df = final_cleanup_hybrid(df)
    
    print("After Final Cleanup (Hybrid):")
    get_final_stats(df)
    
    df.to_csv('data/processed/optimized_clean_comments_v6_emotion_final_hybrid.csv', index=False)
    print("Saved to: data/processed/optimized_clean_comments_v6_emotion_final_hybrid.csv")
