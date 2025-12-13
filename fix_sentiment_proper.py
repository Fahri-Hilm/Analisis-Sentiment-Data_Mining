#!/usr/bin/env python3
"""
Script to properly extract sentiment from label_summary column
"""
import pandas as pd
import re

def extract_sentiment_from_label_summary():
    # Read the CSV file
    df = pd.read_csv('/home/fj/Desktop/PROJECT/Campus/DM/Analisis-Sentiment-Data_Mining/data/processed/comments_cleaned.csv')
    
    print(f"Original data shape: {df.shape}")
    
    # Extract sentiment from label_summary column
    def extract_sentiment(label_summary):
        if pd.isna(label_summary):
            return 'unknown'
        
        # Look for "Sentimen: [sentiment]" pattern
        match = re.search(r'Sentimen:\s*(\w+)', str(label_summary))
        if match:
            sentiment = match.group(1).lower()
            if sentiment in ['positive', 'negative', 'neutral']:
                return sentiment
        
        return 'unknown'
    
    # Apply extraction
    df['extracted_sentiment'] = df['label_summary'].apply(extract_sentiment)
    
    print("Sentiment distribution from label_summary:")
    print(df['extracted_sentiment'].value_counts())
    
    # Update core_sentiment with extracted values
    df['core_sentiment'] = df['extracted_sentiment']
    
    # Drop the temporary column
    df = df.drop('extracted_sentiment', axis=1)
    
    print(f"\nFinal sentiment distribution:")
    print(df['core_sentiment'].value_counts())
    
    # Save the corrected data
    output_path = '/home/fj/Desktop/PROJECT/Campus/DM/Analisis-Sentiment-Data_Mining/data/processed/comments_cleaned_corrected.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\nCorrected data saved to: {output_path}")
    
    # Update the symlink
    import os
    symlink_path = '/home/fj/Desktop/PROJECT/Campus/DM/Analisis-Sentiment-Data_Mining/data/processed/comments_clean_final.csv'
    if os.path.exists(symlink_path):
        os.remove(symlink_path)
    os.symlink('comments_cleaned_corrected.csv', symlink_path)
    
    print(f"Updated symlink to point to corrected file")
    
    return df

if __name__ == "__main__":
    extract_sentiment_from_label_summary()
