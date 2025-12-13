#!/usr/bin/env python3
"""
Quick fix for labelling and layering issues
"""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle

def fix_labels(df):
    """Fix unknown labels and create proper hierarchy"""
    
    # 1. Fix unknown target_kritik using keywords
    def classify_target(text):
        text = str(text).lower()
        if any(word in text for word in ['pssi', 'federasi', 'pengurus']):
            return 'pssi_management'
        elif any(word in text for word in ['pelatih', 'coach', 'taktik', 'strategi']):
            return 'coaching_staff'
        elif any(word in text for word in ['pemain', 'player', 'skill', 'teknik']):
            return 'players'
        elif any(word in text for word in ['lawan', 'opponent', 'wasit', 'referee']):
            return 'opponents'
        else:
            return 'general_system'
    
    # Apply target classification
    mask_unknown = df['target_kritik'] == 'unknown'
    df.loc[mask_unknown, 'target_kritik'] = df.loc[mask_unknown, 'clean_text'].apply(classify_target)
    
    # 2. Simplify emotion labels (merge similar ones)
    emotion_map = {
        'neutral_observation': 'neutral',
        'future_hope': 'hopeful',
        'patriotic_sadness': 'disappointed', 
        'constructive_anger': 'frustrated',
        'respectful_acknowledgment': 'supportive',
        'passionate_disappointment': 'disappointed',
        'strategic_frustration': 'frustrated'
    }
    df['emotion_simple'] = df['football_emotion'].map(emotion_map).fillna('neutral')
    
    # 3. Fix constructiveness using sentiment + keywords
    def classify_constructive(row):
        text = str(row['clean_text']).lower()
        sentiment = row['core_sentiment']
        
        if sentiment == 'positive':
            return 'constructive'
        elif any(word in text for word in ['saran', 'sebaiknya', 'harusnya', 'perlu']):
            return 'constructive'
        elif any(word in text for word in ['bodoh', 'tolol', 'goblok', 'bangsat']):
            return 'destructive'
        else:
            return 'neutral'
    
    mask_unknown_const = df['constructiveness'] == 'unknown'
    df.loc[mask_unknown_const, 'constructiveness'] = df.loc[mask_unknown_const].apply(classify_constructive, axis=1)
    
    return df

def train_quick_models(df):
    """Train models with fixed labels"""
    
    # Prepare data
    X = df['clean_text'].fillna('')
    
    models = {}
    results = {}
    
    # Train for each target
    targets = ['core_sentiment', 'target_kritik', 'emotion_simple', 'constructiveness']
    
    for target in targets:
        print(f"\n=== Training {target} ===")
        
        y = df[target]
        
        # Remove any remaining unknowns
        mask = ~y.isin(['unknown', 'nan', ''])
        X_clean = X[mask]
        y_clean = y[mask]
        
        if len(y_clean.unique()) < 2:
            print(f"Skipping {target} - insufficient classes")
            continue
            
        # Vectorize
        vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1,2))
        X_tfidf = vectorizer.fit_transform(X_clean)
        
        # Split and train
        X_train, X_test, y_train, y_test = train_test_split(
            X_tfidf, y_clean, test_size=0.2, random_state=42, stratify=y_clean
        )
        
        model = SVC(C=1.0, gamma='scale', class_weight='balanced')
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Accuracy: {accuracy:.3f}")
        print(f"Classes: {list(y_clean.unique())}")
        print(f"Distribution: {y_clean.value_counts().to_dict()}")
        
        # Save
        models[target] = (model, vectorizer)
        results[target] = accuracy
    
    return models, results

def main():
    # Load data
    df = pd.read_csv('data/processed/comments_cleaned_readme_spec.csv')
    print(f"Original shape: {df.shape}")
    
    # Fix labels
    df_fixed = fix_labels(df)
    
    # Check improvements
    print("\n=== AFTER FIXING ===")
    for col in ['target_kritik', 'emotion_simple', 'constructiveness']:
        print(f"\n{col}:")
        print(df_fixed[col].value_counts())
    
    # Train models
    models, results = train_quick_models(df_fixed)
    
    # Save everything
    df_fixed.to_csv('data/processed/comments_fixed_labels.csv', index=False)
    
    with open('data/models/fixed_models.pkl', 'wb') as f:
        pickle.dump(models, f)
    
    print(f"\n{'='*40}")
    print("LABELLING FIX RESULTS:")
    print(f"{'='*40}")
    for target, acc in results.items():
        print(f"{target}: {acc:.1%}")
    
    print(f"\nFixed dataset saved to: data/processed/comments_fixed_labels.csv")
    print(f"Models saved to: data/models/fixed_models.pkl")

if __name__ == "__main__":
    main()
