#!/usr/bin/env python3
"""
Fix labeling accuracy using actual column names
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
import pickle

def simplify_labels(df):
    """Simplify labels based on actual columns"""
    
    # Use core_sentiment as base (already 3 classes)
    df['sentiment_clean'] = df['core_sentiment'].str.lower()
    
    # Simplify target_kritik to fewer classes
    target_map = {
        'pssi_management': 'management',
        'management_decisions': 'management', 
        'coaching_staff': 'coaching',
        'coaching_changes': 'coaching',
        'players': 'team',
        'technical_performance': 'team',
        'tactical_issues': 'team',
        'systemic_problems': 'system',
        'infrastructure': 'system',
        'youth_investment': 'system',
        'opponents': 'external',
        'referees': 'external',
        'media_analysts': 'external'
    }
    
    df['target_clean'] = df['target_kritik'].map(target_map)
    df['target_clean'] = df['target_clean'].fillna('general')
    
    # Simplify football_emotion to main categories
    emotion_map = {
        'kekecewaan': 'disappointment',
        'kemarahan': 'anger', 
        'frustrasi': 'frustration',
        'harapan': 'hope',
        'dukungan': 'support',
        'kebanggaan': 'pride',
        'netral': 'neutral'
    }
    
    df['emotion_clean'] = df['football_emotion'].map(emotion_map)
    df['emotion_clean'] = df['emotion_clean'].fillna('neutral')
    
    return df

def train_improved_model(X, y, model_name):
    """Train improved model with better parameters"""
    
    # Better vectorization
    vectorizer = TfidfVectorizer(
        max_features=2000,
        ngram_range=(1, 2),
        min_df=3,
        max_df=0.9,
        sublinear_tf=True
    )
    X_tfidf = vectorizer.fit_transform(X)
    
    # Split with stratification
    X_train, X_test, y_train, y_test = train_test_split(
        X_tfidf, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Optimized SVM
    model = SVC(
        C=1.0, 
        gamma='scale', 
        kernel='rbf',
        class_weight='balanced',  # Handle imbalance
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    
    # Cross validation
    cv_scores = cross_val_score(model, X_tfidf, y, cv=5, scoring='f1_weighted')
    
    print(f"\n=== {model_name} ===")
    print(f"Test Accuracy: {accuracy:.3f}")
    print(f"CV F1-Score: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
    print(f"Class distribution: {pd.Series(y).value_counts().to_dict()}")
    
    return model, vectorizer, accuracy, report, cv_scores

def main():
    # Load data
    df = pd.read_csv('data/processed/comments_cleaned_readme_spec.csv')
    
    print(f"Original data shape: {df.shape}")
    print(f"Available columns: {list(df.columns)}")
    
    # Check current label distributions
    print(f"\nCurrent core_sentiment distribution:")
    print(df['core_sentiment'].value_counts())
    
    print(f"\nCurrent target_kritik distribution:")
    print(df['target_kritik'].value_counts().head(10))
    
    # Simplify labels
    df_clean = simplify_labels(df)
    
    # Remove rows with missing text or labels
    df_clean = df_clean.dropna(subset=['clean_text', 'sentiment_clean', 'target_clean'])
    
    print(f"\nAfter cleaning: {df_clean.shape}")
    print(f"\nSentiment distribution:")
    print(df_clean['sentiment_clean'].value_counts())
    
    print(f"\nTarget distribution:")
    print(df_clean['target_clean'].value_counts())
    
    # Train models
    sentiment_model, sentiment_vec, sentiment_acc, sentiment_report, sentiment_cv = train_improved_model(
        df_clean['clean_text'], df_clean['sentiment_clean'], "Sentiment Classifier"
    )
    
    target_model, target_vec, target_acc, target_report, target_cv = train_improved_model(
        df_clean['clean_text'], df_clean['target_clean'], "Target Classifier"
    )
    
    emotion_model, emotion_vec, emotion_acc, emotion_report, emotion_cv = train_improved_model(
        df_clean['clean_text'], df_clean['emotion_clean'], "Emotion Classifier"
    )
    
    # Save improved models
    models = {
        'sentiment': (sentiment_model, sentiment_vec),
        'target': (target_model, target_vec), 
        'emotion': (emotion_model, emotion_vec)
    }
    
    for name, (model, vectorizer) in models.items():
        with open(f'data/models/{name}_improved.pkl', 'wb') as f:
            pickle.dump((model, vectorizer), f)
    
    # Save cleaned dataset
    df_clean.to_csv('data/processed/comments_improved_labels.csv', index=False)
    
    # Summary
    print(f"\n{'='*50}")
    print(f"IMPROVEMENT RESULTS")
    print(f"{'='*50}")
    print(f"Sentiment Accuracy: {sentiment_acc:.1%} (CV: {sentiment_cv.mean():.1%})")
    print(f"Target Accuracy: {target_acc:.1%} (CV: {target_cv.mean():.1%})")
    print(f"Emotion Accuracy: {emotion_acc:.1%} (CV: {emotion_cv.mean():.1%})")
    print(f"\nModels saved to data/models/*_improved.pkl")
    print(f"Cleaned data saved to data/processed/comments_improved_labels.csv")

if __name__ == "__main__":
    main()
