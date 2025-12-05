"""
Sentiment Re-training Pipeline
==============================
Train ML model menggunakan data yang sudah berlabel untuk memprediksi data unknown.

Metodologi:
1. Load data dengan label (positive, negative, neutral) sebagai training set
2. TF-IDF vectorization pada clean_text
3. Train model (Logistic Regression + Naive Bayes ensemble)
4. Evaluate dengan cross-validation
5. Predict data unknown
6. Save hasil ke CSV baru
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import VotingClassifier
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Paths
DATA_DIR = Path(__file__).parent.parent.parent / "data"
INPUT_FILE = DATA_DIR / "processed" / "comments_cleaned.csv"
OUTPUT_FILE = DATA_DIR / "processed" / "comments_cleaned_retrained.csv"
MODEL_DIR = DATA_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)

def load_data():
    """Load and prepare data"""
    print("📂 Loading data...")
    df = pd.read_csv(INPUT_FILE)
    print(f"   Total rows: {len(df):,}")
    
    # Separate labeled and unknown
    labeled_mask = df['core_sentiment'].isin(['positive', 'negative', 'neutral'])
    df_labeled = df[labeled_mask].copy()
    df_unknown = df[~labeled_mask].copy()
    
    print(f"   Labeled data: {len(df_labeled):,}")
    print(f"   Unknown data: {len(df_unknown):,}")
    
    return df, df_labeled, df_unknown

def prepare_features(df_labeled, df_unknown):
    """Prepare TF-IDF features"""
    print("\n🔧 Preparing TF-IDF features...")
    
    # Use clean_text, fallback to text if missing
    df_labeled['text_for_ml'] = df_labeled['clean_text'].fillna(df_labeled['text'])
    df_unknown['text_for_ml'] = df_unknown['clean_text'].fillna(df_unknown['text'])
    
    # Remove any remaining NaN
    df_labeled = df_labeled[df_labeled['text_for_ml'].notna()].copy()
    df_unknown = df_unknown[df_unknown['text_for_ml'].notna()].copy()
    
    # TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),  # unigrams and bigrams
        min_df=2,
        max_df=0.95,
        strip_accents='unicode',
        lowercase=True
    )
    
    # Fit on all text, transform separately
    all_text = pd.concat([df_labeled['text_for_ml'], df_unknown['text_for_ml']])
    vectorizer.fit(all_text)
    
    X_labeled = vectorizer.transform(df_labeled['text_for_ml'])
    X_unknown = vectorizer.transform(df_unknown['text_for_ml'])
    y_labeled = df_labeled['core_sentiment']
    
    print(f"   Feature dimensions: {X_labeled.shape}")
    print(f"   Vocabulary size: {len(vectorizer.vocabulary_)}")
    
    return X_labeled, y_labeled, X_unknown, df_labeled, df_unknown, vectorizer

def train_model(X, y):
    """Train ensemble model"""
    print("\n🤖 Training ML model...")
    
    # Create ensemble of Logistic Regression + Naive Bayes
    lr = LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42)
    nb = MultinomialNB(alpha=0.1)
    
    ensemble = VotingClassifier(
        estimators=[('lr', lr), ('nb', nb)],
        voting='soft'
    )
    
    # Cross-validation
    print("   Running 5-fold cross-validation...")
    cv_scores = cross_val_score(ensemble, X, y, cv=5, scoring='accuracy')
    print(f"   CV Accuracy: {cv_scores.mean():.3f} (+/- {cv_scores.std()*2:.3f})")
    
    # Train-test split for detailed evaluation
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Fit model
    ensemble.fit(X_train, y_train)
    
    # Evaluate
    y_pred = ensemble.predict(X_test)
    print("\n📊 Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # Confusion matrix
    print("📋 Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred, labels=['negative', 'neutral', 'positive'])
    print(f"              Predicted")
    print(f"              neg    neu    pos")
    print(f"Actual neg   {cm[0,0]:5d}  {cm[0,1]:5d}  {cm[0,2]:5d}")
    print(f"       neu   {cm[1,0]:5d}  {cm[1,1]:5d}  {cm[1,2]:5d}")
    print(f"       pos   {cm[2,0]:5d}  {cm[2,1]:5d}  {cm[2,2]:5d}")
    
    # Retrain on full labeled data
    print("\n🔄 Retraining on full labeled data...")
    ensemble.fit(X, y)
    
    return ensemble

def predict_unknown(model, X_unknown, df_unknown):
    """Predict labels for unknown data"""
    print("\n🎯 Predicting unknown data...")
    
    predictions = model.predict(X_unknown)
    probabilities = model.predict_proba(X_unknown)
    
    df_unknown = df_unknown.copy()
    df_unknown['core_sentiment_new'] = predictions
    df_unknown['sentiment_confidence'] = probabilities.max(axis=1)
    
    print("   Prediction distribution:")
    print(df_unknown['core_sentiment_new'].value_counts())
    
    return df_unknown

def save_results(df_original, df_labeled, df_unknown, model, vectorizer):
    """Save results"""
    print("\n💾 Saving results...")
    
    # Create final dataframe
    df_final = df_original.copy()
    
    # Update unknown rows with new predictions
    unknown_indices = df_unknown.index
    df_final.loc[unknown_indices, 'core_sentiment'] = df_unknown['core_sentiment_new'].values
    
    # Add confidence for unknown (if column doesn't exist)
    if 'ml_retrain_confidence' not in df_final.columns:
        df_final['ml_retrain_confidence'] = np.nan
    df_final.loc[unknown_indices, 'ml_retrain_confidence'] = df_unknown['sentiment_confidence'].values
    
    # Mark which rows were retrained
    df_final['was_retrained'] = False
    df_final.loc[unknown_indices, 'was_retrained'] = True
    
    # Save CSV
    df_final.to_csv(OUTPUT_FILE, index=False)
    print(f"   Saved to: {OUTPUT_FILE}")
    
    # Save model and vectorizer
    joblib.dump(model, MODEL_DIR / "sentiment_model.joblib")
    joblib.dump(vectorizer, MODEL_DIR / "tfidf_vectorizer.joblib")
    print(f"   Model saved to: {MODEL_DIR}")
    
    return df_final

def main():
    print("=" * 60)
    print("🚀 SENTIMENT RE-TRAINING PIPELINE")
    print("=" * 60)
    
    # Load data
    df_original, df_labeled, df_unknown = load_data()
    
    # Prepare features
    X_labeled, y_labeled, X_unknown, df_labeled, df_unknown, vectorizer = prepare_features(df_labeled, df_unknown)
    
    # Train model
    model = train_model(X_labeled, y_labeled)
    
    # Predict unknown
    df_unknown = predict_unknown(model, X_unknown, df_unknown)
    
    # Save results
    df_final = save_results(df_original, df_labeled, df_unknown, model, vectorizer)
    
    # Final summary
    print("\n" + "=" * 60)
    print("✅ FINAL SENTIMENT DISTRIBUTION")
    print("=" * 60)
    print(df_final['core_sentiment'].value_counts())
    print()
    print("Percentage:")
    print((df_final['core_sentiment'].value_counts(normalize=True) * 100).round(1))
    
    print("\n🎉 Pipeline completed successfully!")
    return df_final

if __name__ == "__main__":
    main()
