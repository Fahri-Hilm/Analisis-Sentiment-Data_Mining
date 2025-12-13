#!/usr/bin/env python3
"""
Simple label improvement without SMOTE
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import pickle

def simplify_labels(df):
    """Simplify complex labels to reduce confusion"""
    
    # Sentiment mapping (3 classes)
    sentiment_map = {
        'positive_support': 'positive',
        'respectful_acknowledgment': 'positive', 
        'future_hope': 'positive',
        'hopeful_skepticism': 'positive',
        'constructive_suggestions': 'positive',
        'constructive_anger': 'positive',
        
        'negative_criticism': 'negative',
        'frustration_expression': 'negative',
        'passionate_disappointment': 'negative',
        'patriotic_sadness': 'negative',
        
        'neutral_observation': 'neutral',
        'short_term_analysis': 'neutral',
        'immediate_reaction': 'neutral'
    }
    
    # Target mapping (5 classes)  
    target_map = {
        'pssi_management': 'management',
        'management_decisions': 'management',
        
        'players': 'team',
        'technical_performance': 'team',
        'tactical_issues': 'team',
        
        'coaching_staff': 'coaching',
        'coaching_changes': 'coaching',
        
        'systemic_problems': 'system',
        'infrastructure': 'system',
        'youth_investment': 'system',
        
        'opponents': 'external',
        'referees': 'external',
        'media_analysts': 'external',
        'external_factors': 'external'
    }
    
    # Apply mappings
    df['sentiment_simple'] = df['emotion_label'].map(sentiment_map)
    df['target_simple'] = df['target_label'].map(target_map)
    
    # Fill unmapped values
    df['sentiment_simple'] = df['sentiment_simple'].fillna('neutral')
    df['target_simple'] = df['target_simple'].fillna('general')
    
    return df

def train_simple_model(X, y, model_name):
    """Train simple but effective model"""
    
    # Vectorize
    vectorizer = TfidfVectorizer(
        max_features=1500,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95
    )
    X_tfidf = vectorizer.fit_transform(X)
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X_tfidf, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train SVM
    model = SVC(C=1.0, gamma='scale', random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    
    # Cross validation
    cv_scores = cross_val_score(model, X_tfidf, y, cv=5, scoring='accuracy')
    
    print(f"\n{model_name} Results:")
    print(f"Test Accuracy: {accuracy:.3f}")
    print(f"CV Accuracy: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
    
    return model, vectorizer, accuracy, report

def main():
    # Load data
    df = pd.read_csv('data/processed/comments_clean_final.csv')
    
    print(f"Original data shape: {df.shape}")
    print(f"Original emotion labels: {df['emotion_label'].nunique()}")
    
    # Simplify labels
    df_simple = simplify_labels(df)
    
    # Remove rows with missing labels
    df_simple = df_simple.dropna(subset=['sentiment_simple', 'target_simple'])
    
    print(f"\nAfter simplification:")
    print(f"Sentiment distribution:\n{df_simple['sentiment_simple'].value_counts()}")
    print(f"\nTarget distribution:\n{df_simple['target_simple'].value_counts()}")
    
    # Train sentiment model
    sentiment_model, sentiment_vectorizer, sentiment_acc, sentiment_report = train_simple_model(
        df_simple['comment_text'], df_simple['sentiment_simple'], "Sentiment Model"
    )
    
    # Train target model  
    target_model, target_vectorizer, target_acc, target_report = train_simple_model(
        df_simple['comment_text'], df_simple['target_simple'], "Target Model"
    )
    
    # Save models
    with open('data/models/sentiment_simple.pkl', 'wb') as f:
        pickle.dump((sentiment_model, sentiment_vectorizer), f)
        
    with open('data/models/target_simple.pkl', 'wb') as f:
        pickle.dump((target_model, target_vectorizer), f)
    
    # Save simplified dataset
    df_simple.to_csv('data/processed/comments_simplified.csv', index=False)
    
    print(f"\n=== IMPROVEMENT SUMMARY ===")
    print(f"Sentiment Model Accuracy: {sentiment_acc:.1%}")
    print(f"Target Model Accuracy: {target_acc:.1%}")
    print(f"Label reduction: {df['emotion_label'].nunique()} → {df_simple['sentiment_simple'].nunique()} (sentiment)")
    print(f"Label reduction: {df['target_label'].nunique()} → {df_simple['target_simple'].nunique()} (target)")
    print("\nModels saved to data/models/")

if __name__ == "__main__":
    main()
