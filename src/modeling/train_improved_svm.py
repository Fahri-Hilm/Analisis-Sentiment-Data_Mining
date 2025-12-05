"""
Improved SVM Training with Advanced Features
"""
import argparse
import json
import logging
from pathlib import Path
from typing import Dict, Any, Tuple

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score

from src.modeling.features import FeatureExtractor
from src.modeling.svm_tuner import SVMTuner
from src.modeling.error_analyzer import ErrorAnalyzer
from src.modeling.model_versioning import ModelVersionManager
from src.preprocessing.enhanced_preprocessor import EnhancedPreprocessor


def setup_logging() -> logging.Logger:
    """Setup logging"""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


def load_and_prepare_data(file_path: str, logger: logging.Logger) -> Tuple[pd.DataFrame, pd.Series, pd.Series]:
    """Load and prepare data"""
    logger.info(f"Loading data from {file_path}")
    
    df = pd.read_csv(file_path)
    df = df.dropna(subset=['sentiment_label', 'clean_text'])
    
    # Map to broad sentiment
    def map_sentiment(label):
        positive = ['positive_support', 'respectful_acknowledgment', 'fans_supporters']
        negative = ['pssi_management', 'opponents', 'patriotic_sadness', 
                   'negative_criticism', 'frustration_expression', 'passionate_disappointment']
        
        if label in positive:
            return 'positive'
        elif label in negative:
            return 'negative'
        else:
            return 'neutral'
    
    df['broad_sentiment'] = df['sentiment_label'].apply(map_sentiment)
    
    # Filter classes with sufficient samples
    sentiment_counts = df['broad_sentiment'].value_counts()
    valid_sentiments = sentiment_counts[sentiment_counts >= 2].index
    df = df[df['broad_sentiment'].isin(valid_sentiments)]
    
    X = df['clean_text']
    y = df['broad_sentiment']
    
    logger.info(f"Loaded {len(df)} samples")
    logger.info(f"Class distribution: {y.value_counts().to_dict()}")
    
    return df, X, y


def train_improved_svm(X_train: pd.Series, y_train: pd.Series,
                      X_test: pd.Series, y_test: pd.Series,
                      logger: logging.Logger) -> Dict[str, Any]:
    """Train improved SVM with tuning"""
    
    # Feature extraction with n-grams
    logger.info("Extracting features with n-grams...")
    feature_extractor = FeatureExtractor(
        max_features=5000,
        ngram_range=(1, 3),  # Include trigrams
        min_df=2,
        max_df=0.95
    )
    
    X_train_features = feature_extractor.fit_transform(X_train)
    X_test_features = feature_extractor.transform(X_test)
    
    # Encode labels
    label_encoder = LabelEncoder()
    y_train_encoded = label_encoder.fit_transform(y_train)
    y_test_encoded = label_encoder.transform(y_test)
    
    # Hyperparameter tuning
    logger.info("Starting hyperparameter tuning...")
    tuner = SVMTuner(random_state=42)
    model, tuning_results = tuner.grid_search_tuning(
        X_train_features, y_train, cv=5
    )
    
    # Predictions
    y_pred_encoded = model.predict(X_test_features)
    y_pred = label_encoder.inverse_transform(y_pred_encoded)
    y_proba = model.predict_proba(X_test_features)
    
    # Error analysis
    logger.info("Analyzing errors...")
    error_analyzer = ErrorAnalyzer()
    error_analysis = error_analyzer.analyze_errors(y_test_encoded, y_pred_encoded, X_test)
    per_class_errors = error_analyzer.get_per_class_errors(y_test_encoded, y_pred_encoded, 
                                                           label_encoder.classes_)
    hard_samples = error_analyzer.identify_hard_samples(y_test_encoded, y_pred_encoded, y_proba)
    
    # Metrics
    accuracy = accuracy_score(y_test_encoded, y_pred_encoded)
    class_report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
    
    results = {
        'model': model,
        'feature_extractor': feature_extractor,
        'label_encoder': label_encoder,
        'metrics': {
            'accuracy': float(accuracy),
            'tuning_score': float(tuning_results['best_score']),
            'best_params': tuning_results['best_params'],
            'class_report': class_report,
            'per_class_errors': per_class_errors,
            'error_analysis': error_analysis,
            'hard_samples': hard_samples
        }
    }
    
    logger.info(f"Test Accuracy: {accuracy:.4f}")
    logger.info(f"Tuning Score: {tuning_results['best_score']:.4f}")
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Train improved SVM model")
    parser.add_argument("--input", type=str, default="data/processed/clean_comments.csv")
    parser.add_argument("--output-dir", type=str, default="data/models")
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--random-state", type=int, default=42)
    
    args = parser.parse_args()
    logger = setup_logging()
    
    try:
        # Load data
        df, X, y = load_and_prepare_data(args.input, logger)
        
        # Split data
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=args.test_size, 
                random_state=args.random_state, stratify=y
            )
        except ValueError:
            logger.warning("Stratified split failed, using regular split")
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=args.test_size, 
                random_state=args.random_state
            )
        
        logger.info(f"Training set: {len(X_train)}, Test set: {len(X_test)}")
        
        # Train improved SVM
        results = train_improved_svm(X_train, y_train, X_test, y_test, logger)
        
        # Save artifacts
        output_path = Path(args.output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        import pickle
        with open(output_path / "svm_model.pkl", 'wb') as f:
            pickle.dump(results['model'], f)
        
        results['feature_extractor'].save(str(output_path / "feature_extractor.pkl"))
        
        with open(output_path / "label_encoder.pkl", 'wb') as f:
            pickle.dump(results['label_encoder'], f)
        
        with open(output_path / "evaluation_results.json", 'w') as f:
            json.dump(results['metrics'], f, indent=2, ensure_ascii=False)
        
        logger.info("Training completed successfully!")
        
        print("\n" + "="*60)
        print("IMPROVED SVM TRAINING SUMMARY")
        print("="*60)
        print(f"Test Accuracy: {results['metrics']['accuracy']:.4f}")
        print(f"Tuning Score: {results['metrics']['tuning_score']:.4f}")
        print(f"Best Parameters: {results['metrics']['best_params']}")
        print(f"Hard Samples: {results['metrics']['hard_samples']['hard_sample_count']}")
        print(f"Error Rate: {results['metrics']['error_analysis']['error_rate']:.2%}")
        print("="*60)
        
    except Exception as e:
        logger.error(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()
