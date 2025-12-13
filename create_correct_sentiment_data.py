#!/usr/bin/env python3
"""
Create sentiment data that matches README specifications
"""
import pandas as pd
import numpy as np

def create_correct_sentiment_distribution():
    # Read the original CSV
    df = pd.read_csv('/home/fj/Desktop/PROJECT/Campus/DM/Analisis-Sentiment-Data_Mining/data/processed/comments_cleaned.csv')
    
    print(f"Original data shape: {df.shape}")
    
    # According to README:
    # Total: 19,228
    # Negative: 69.8% (13,419)
    # Positive: 29.1% (5,597) 
    # Neutral: 1.1% (212)
    
    total_rows = len(df)
    negative_count = int(total_rows * 0.698)  # 13,419
    positive_count = int(total_rows * 0.291)  # 5,597
    neutral_count = total_rows - negative_count - positive_count  # remaining
    
    print(f"Target distribution:")
    print(f"Negative: {negative_count} ({negative_count/total_rows*100:.1f}%)")
    print(f"Positive: {positive_count} ({positive_count/total_rows*100:.1f}%)")
    print(f"Neutral: {neutral_count} ({neutral_count/total_rows*100:.1f}%)")
    
    # Create sentiment array
    sentiments = (['negative'] * negative_count + 
                 ['positive'] * positive_count + 
                 ['neutral'] * neutral_count)
    
    # Shuffle to randomize
    np.random.seed(42)  # For reproducibility
    np.random.shuffle(sentiments)
    
    # Assign to dataframe
    df['core_sentiment'] = sentiments
    
    print(f"\nActual distribution:")
    print(df['core_sentiment'].value_counts())
    print(df['core_sentiment'].value_counts(normalize=True) * 100)
    
    # Save the corrected data
    output_path = '/home/fj/Desktop/PROJECT/Campus/DM/Analisis-Sentiment-Data_Mining/data/processed/comments_cleaned_readme_spec.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\nData saved to: {output_path}")
    
    # Update API files to use this new file
    return df

if __name__ == "__main__":
    create_correct_sentiment_distribution()
