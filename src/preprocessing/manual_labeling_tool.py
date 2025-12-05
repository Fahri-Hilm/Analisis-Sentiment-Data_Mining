"""
Interactive Manual Labeling Tool untuk Unknown Sentiments
"""
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def manual_label_unknown(input_file, output_file, batch_size=100):
    """
    Interactive tool untuk manual labeling unknown sentiments
    """
    df = pd.read_csv(input_file)
    
    unknown_mask = df['core_sentiment'].str.lower().str.contains('unknown', na=False)
    unknown_indices = df[unknown_mask].index.tolist()
    
    print(f"\n{'='*80}")
    print(f"Manual Labeling Tool - {len(unknown_indices)} unknown sentiments")
    print(f"{'='*80}\n")
    
    labeled_count = 0
    skipped_count = 0
    
    for i, idx in enumerate(unknown_indices[:batch_size]):
        text = df.loc[idx, 'clean_text']
        
        print(f"\n[{i+1}/{min(batch_size, len(unknown_indices))}] {text[:100]}...")
        print("Options: [p]ositive, [n]egative, [u]tral, [s]kip, [q]uit")
        
        choice = input("Label: ").lower().strip()
        
        if choice == 'p':
            df.loc[idx, 'core_sentiment'] = 'positive'
            labeled_count += 1
        elif choice == 'n':
            df.loc[idx, 'core_sentiment'] = 'negative'
            labeled_count += 1
        elif choice == 'u':
            df.loc[idx, 'core_sentiment'] = 'neutral'
            labeled_count += 1
        elif choice == 's':
            skipped_count += 1
        elif choice == 'q':
            break
    
    df.to_csv(output_file, index=False)
    
    print(f"\n{'='*80}")
    print(f"Labeled: {labeled_count}, Skipped: {skipped_count}")
    print(f"Saved to: {output_file}")
    print(f"{'='*80}\n")
    
    return df

if __name__ == "__main__":
    manual_label_unknown(
        'data/processed/optimized_clean_comments_v6_emotion_enhanced.csv',
        'data/processed/optimized_clean_comments_v6_emotion_manual.csv',
        batch_size=50
    )
