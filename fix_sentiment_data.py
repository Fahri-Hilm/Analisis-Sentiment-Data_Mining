#!/usr/bin/env python3
"""
Script to fix sentiment data in the CSV file
"""
import pandas as pd
import numpy as np

def fix_sentiment_data():
    # Read the CSV file
    df = pd.read_csv('/home/fj/Desktop/PROJECT/Campus/DM/Analisis-Sentiment-Data_Mining/data/processed/comments_cleaned.csv')
    
    print(f"Original data shape: {df.shape}")
    print(f"Original core_sentiment unique values: {df['core_sentiment'].unique()[:10]}")
    
    # Count valid sentiment values
    valid_sentiments = ['positive', 'negative', 'neutral']
    valid_mask = df['core_sentiment'].isin(valid_sentiments)
    
    print(f"Valid sentiment rows: {valid_mask.sum()}")
    print(f"Invalid sentiment rows: {(~valid_mask).sum()}")
    
    # For invalid sentiment values, try to infer from other columns or set as 'unknown'
    # First, let's see what's in the invalid rows
    invalid_df = df[~valid_mask]
    print(f"\nSample invalid sentiment values:")
    print(invalid_df['core_sentiment'].value_counts().head(10))
    
    # Try to fix based on patterns or set to 'unknown'
    df_fixed = df.copy()
    
    # If core_sentiment_score exists, use it to infer sentiment
    if 'core_sentiment_score' in df.columns:
        # Positive score > 0.5 = positive, < -0.5 = negative, else neutral
        score_mask = ~valid_mask & pd.notna(df['core_sentiment_score'])
        
        df_fixed.loc[score_mask & (df['core_sentiment_score'] > 0.5), 'core_sentiment'] = 'positive'
        df_fixed.loc[score_mask & (df['core_sentiment_score'] < -0.5), 'core_sentiment'] = 'negative'
        df_fixed.loc[score_mask & (df['core_sentiment_score'].between(-0.5, 0.5)), 'core_sentiment'] = 'neutral'
    
    # For remaining invalid values, set to 'unknown'
    still_invalid = ~df_fixed['core_sentiment'].isin(valid_sentiments + ['unknown'])
    df_fixed.loc[still_invalid, 'core_sentiment'] = 'unknown'
    
    print(f"\nAfter fixing:")
    print(df_fixed['core_sentiment'].value_counts())
    
    # Save the fixed data
    output_path = '/home/fj/Desktop/PROJECT/Campus/DM/Analisis-Sentiment-Data_Mining/data/processed/comments_cleaned_fixed.csv'
    df_fixed.to_csv(output_path, index=False)
    
    print(f"\nFixed data saved to: {output_path}")
    
    # Update the symlink to point to the fixed file
    import os
    symlink_path = '/home/fj/Desktop/PROJECT/Campus/DM/Analisis-Sentiment-Data_Mining/data/processed/comments_clean_final.csv'
    if os.path.exists(symlink_path):
        os.remove(symlink_path)
    os.symlink('comments_cleaned_fixed.csv', symlink_path)
    
    print(f"Updated symlink to point to fixed file")
    
    return df_fixed

if __name__ == "__main__":
    fix_sentiment_data()
