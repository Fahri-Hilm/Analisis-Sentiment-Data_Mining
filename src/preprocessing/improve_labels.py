#!/usr/bin/env python3
"""
Improve labeling accuracy by simplifying hierarchy and balancing data
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
from imblearn.over_sampling import SMOTE
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
        
        'negative_criticism': 'negative',
        'frustration_expression': 'negative',
        'passionate_disappointment': 'negative',
        'constructive_anger': 'negative',
        'patriotic_sadness': 'negative',
        
        'neutral_observation': 'neutral',
        'short_term_analysis': 'neutral',
        'immediate_reaction': 'neutral'
    }
    
    # Target mapping (5 classes)  
    target_map = {
        'pssi_management': 'management',
        'management_decisions': 'management',
        
        'players': 'team_performance',
        'technical_performance': 'team_performance',
        'tactical_issues': 'team_performance',
        
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

def balance_data(X, y):
    """Balance dataset using SMOTE"""
    vectorizer = TfidfVectorizer(max_features=2000, stop_words='english')
    X_tfidf = vectorizer.fit_transform(X)
    
    smote = SMOTE(random_state=42, k_neighbors=3)
    X_balanced, y_balanced = smote.fit_resample(X_tfidf, y)
    
    return X_balanced, y_balanced, vectorizer

def train_ensemble_model(X, y):
    """Train ensemble model for better accuracy"""
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Balance training data
    X_train_balanced, y_train_balanced, vectorizer = balance_data(X_train, y_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    # Ensemble classifier
    svm_clf = SVC(probability=True, C=1.0, gamma='scale', random_state=42)
    rf_clf = RandomForestClassifier(n_estimators=100, random_state=42)
    nb_clf = MultinomialNB()
    
    ensemble = VotingClassifier([
        ('svm', svm_clf),
        ('rf', rf_clf),
        ('nb', nb_clf)
    ], voting='soft')
    
    # Train
    ensemble.fit(X_train_balanced, y_train_balanced)
    
    # Predict
    y_pred = ensemble.predict(X_test_tfidf)
    
    # Evaluate
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    
    return ensemble, vectorizer, accuracy, report

def main():
    # Load data
    df = pd.read_csv('data/processed/comments_clean_final.csv')
    
    print(f"Original data shape: {df.shape}")
    print(f"Original emotion labels: {df['emotion_label'].nunique()}")
    
    # Simplify labels
    df_simple = simplify_labels(df)
    
    print(f"Simplified sentiment labels: {df_simple['sentiment_simple'].nunique()}")
    print(f"Simplified target labels: {df_simple['target_simple'].nunique()}")
    
    # Train sentiment model
    print("\n=== Training Sentiment Model ===")
    sentiment_model, sentiment_vectorizer, sentiment_acc, sentiment_report = train_ensemble_model(
        df_simple['comment_text'], df_simple['sentiment_simple']
    )
    
    print(f"Sentiment Accuracy: {sentiment_acc:.3f}")
    
    # Train target model  
    print("\n=== Training Target Model ===")
    target_model, target_vectorizer, target_acc, target_report = train_ensemble_model(
        df_simple['comment_text'], df_simple['target_simple']
    )
    
    print(f"Target Accuracy: {target_acc:.3f}")
    
    # Save models
    with open('data/models/sentiment_ensemble.pkl', 'wb') as f:
        pickle.dump((sentiment_model, sentiment_vectorizer), f)
        
    with open('data/models/target_ensemble.pkl', 'wb') as f:
        pickle.dump((target_model, target_vectorizer), f)
    
    # Save simplified dataset
    df_simple.to_csv('data/processed/comments_simplified.csv', index=False)
    
    print("\n=== Results Summary ===")
    print(f"Sentiment Model Accuracy: {sentiment_acc:.1%}")
    print(f"Target Model Accuracy: {target_acc:.1%}")
    print("Models saved to data/models/")
    print("Simplified dataset saved to data/processed/comments_simplified.csv")

if __name__ == "__main__":
    main()
