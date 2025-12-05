"""
Final Cleanup - Label remaining unknown dengan aggressive strategy
"""
import pandas as pd
import logging
import numpy as np

logger = logging.getLogger(__name__)

def final_cleanup(df):
    """
    Final aggressive cleanup untuk unknown
    Strategy: Gunakan text length, word count, dan pattern matching
    """
    df = df.copy()
    
    unknown_mask = df['core_sentiment'].str.lower().str.contains('unknown', na=False)
    unknown_count = unknown_mask.sum()
    
    logger.info(f"Final cleanup: {unknown_count} unknown sentiments")
    
    labeled_count = 0
    
    for idx in df[unknown_mask].index:
        text = str(df.loc[idx, 'clean_text']).lower()
        
        # Strategy 1: Check for question marks (usually neutral/inquiry)
        if '?' in text:
            df.loc[idx, 'core_sentiment'] = 'neutral'
            labeled_count += 1
            continue
        
        # Strategy 2: Check for exclamation marks (usually emotional)
        if '!' in text:
            # Count positive/negative words
            pos_words = ['bagus', 'hebat', 'keren', 'mantap', 'sip', 'oke', 'baik', 'sempurna']
            neg_words = ['jelek', 'buruk', 'payah', 'gagal', 'rugi', 'kecewa', 'sedih', 'marah']
            
            pos_count = sum(1 for w in pos_words if w in text)
            neg_count = sum(1 for w in neg_words if w in text)
            
            if pos_count > neg_count:
                df.loc[idx, 'core_sentiment'] = 'positive'
            elif neg_count > pos_count:
                df.loc[idx, 'core_sentiment'] = 'negative'
            else:
                df.loc[idx, 'core_sentiment'] = 'neutral'
            labeled_count += 1
            continue
        
        # Strategy 3: Very short text (< 5 words) = neutral
        if len(text.split()) < 5:
            df.loc[idx, 'core_sentiment'] = 'neutral'
            labeled_count += 1
            continue
        
        # Strategy 4: Check for specific patterns
        if any(word in text for word in ['ayo', 'semangat', 'dukung', 'support']):
            df.loc[idx, 'core_sentiment'] = 'positive'
            labeled_count += 1
            continue
        
        if any(word in text for word in ['kalah', 'gagal', 'hancur', 'rusak']):
            df.loc[idx, 'core_sentiment'] = 'negative'
            labeled_count += 1
            continue
        
        # Strategy 5: Default to neutral for remaining
        df.loc[idx, 'core_sentiment'] = 'neutral'
        labeled_count += 1
    
    logger.info(f"Final cleanup labeled: {labeled_count} sentiments")
    
    return df

def get_final_stats(df):
    """Get final statistics"""
    stats = df['core_sentiment'].value_counts()
    total = len(df)
    
    print(f"\n{'='*60}")
    print(f"FINAL STATISTICS")
    print(f"{'='*60}")
    print(f"Total Comments: {total}")
    print(f"Positive: {stats.get('positive', 0)} ({stats.get('positive', 0)/total*100:.1f}%)")
    print(f"Negative: {stats.get('negative', 0)} ({stats.get('negative', 0)/total*100:.1f}%)")
    print(f"Neutral: {stats.get('neutral', 0)} ({stats.get('neutral', 0)/total*100:.1f}%)")
    print(f"Unknown: {stats.get('unknown', 0)} ({stats.get('unknown', 0)/total*100:.1f}%)")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    df = pd.read_csv('data/processed/optimized_clean_comments_v6_emotion_enhanced.csv')
    
    print("Before Final Cleanup:")
    get_final_stats(df)
    
    df = final_cleanup(df)
    
    print("After Final Cleanup:")
    get_final_stats(df)
    
    df.to_csv('data/processed/optimized_clean_comments_v6_emotion_final.csv', index=False)
    print("Saved to: data/processed/optimized_clean_comments_v6_emotion_final.csv")
