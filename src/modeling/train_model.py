"""
SVM Model Training Script for Sentiment Analysis
"""
import argparse
import json
import pickle
import logging
from pathlib import Path
from typing import Dict, Any, Tuple

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder

from src.modeling.features import FeatureExtractor


def setup_logging() -> logging.Logger:
    """Setup logging configuration"""
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


def load_data(file_path: str, logger: logging.Logger) -> Tuple[pd.DataFrame, pd.Series]:
    """Load and prepare data for training"""
    logger.info(f"Loading data from {file_path}")
    
    df = pd.read_csv(file_path)
    
    # Filter out samples with neutral sentiment for binary classification
    # or keep all for multi-class classification
    df = df.dropna(subset=['sentiment_label', 'clean_text'])
    
    # Group sentiment labels into broader categories for better training
    def map_sentiment_category(label):
        positive_categories = ['positive_support', 'respectful_acknowledgment', 'fans_supporters']
        negative_categories = ['pssi_management', 'opponents', 'patriotic_sadness', 
                              'negative_criticism', 'frustration_expression', 'passionate_disappointment']
        neutral_categories = ['unknown', 'technical_performance', 'management_decisions', 
                           'players', 'external_factors', 'short_term_analysis', 
                           'tactical_issues', 'systemic_reform_calls', 'future_projection']
        
        if label in positive_categories:
            return 'positive'
        elif label in negative_categories:
            return 'negative'
        else:
            return 'neutral'
    
    df['broad_sentiment'] = df['sentiment_label'].apply(map_sentiment_category)
    
    # Filter out classes with very few samples
    sentiment_counts = df['broad_sentiment'].value_counts()
    valid_sentiments = sentiment_counts[sentiment_counts >= 2].index
    df = df[df['broad_sentiment'].isin(valid_sentiments)]
    
    X = df['clean_text']
    y = df['broad_sentiment']
    
    logger.info(f"Loaded {len(df)} samples after filtering")
    logger.info(f"Class distribution: {y.value_counts().to_dict()}")
    
    return df, X, y


def train_svm_model(X_train: pd.Series, y_train: pd.Series, 
                   feature_extractor: FeatureExtractor, 
                   logger: logging.Logger) -> Tuple[SVC, LabelEncoder]:
    """Train SVM model with hyperparameter tuning"""
    logger.info("Training SVM model...")
    
    # Encode labels
    label_encoder = LabelEncoder()
    y_train_encoded = label_encoder.fit_transform(y_train)
    
    # Feature extraction
    X_train_features = feature_extractor.fit_transform(X_train)
    
    # Simplified parameter grid for faster training
    param_grid = {
        'C': [1, 10],
        'gamma': ['scale', 0.1],
        'kernel': ['rbf']
    }
    
    # Initialize SVM classifier
    svm = SVC(probability=True, random_state=42)
    
    # Perform grid search with cross-validation
    logger.info("Performing hyperparameter tuning...")
    grid_search = GridSearchCV(
        svm, param_grid, cv=5, scoring='f1_weighted', 
        n_jobs=-1, verbose=1
    )
    
    grid_search.fit(X_train_features, y_train_encoded)
    
    # Get best model
    best_model = grid_search.best_estimator_
    
    logger.info(f"Best parameters: {grid_search.best_params_}")
    logger.info(f"Best cross-validation score: {grid_search.best_score_:.4f}")
    
    return best_model, label_encoder


def evaluate_model(model: SVC, X_test: pd.Series, y_test: pd.Series,
                  X_train: pd.Series, y_train: pd.Series,
                  feature_extractor: FeatureExtractor, label_encoder: LabelEncoder,
                  logger: logging.Logger) -> Dict[str, Any]:
    """Evaluate model performance"""
    logger.info("Evaluating model...")
    
    # Transform test data
    X_test_features = feature_extractor.transform(X_test)
    y_test_encoded = label_encoder.transform(y_test)
    
    # Make predictions
    y_pred = model.predict(X_test_features)
    y_pred_original = label_encoder.inverse_transform(y_pred)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test_encoded, y_pred)
    
    # Cross-validation scores - use training data
    X_combined = pd.concat([X_train, X_test])
    y_combined = pd.concat([y_train, y_test])
    
    cv_scores = cross_val_score(
        model, feature_extractor.fit_transform(X_combined),
        label_encoder.fit_transform(y_combined), 
        cv=5, scoring='f1_weighted'
    )
    
    # Generate classification report
    class_report = classification_report(
        y_test, y_pred_original, 
        output_dict=True, zero_division=0
    )
    
    evaluation_results = {
        'accuracy': accuracy,
        'cv_mean_score': cv_scores.mean(),
        'cv_std_score': cv_scores.std(),
        'classification_report': class_report,
        'confusion_matrix': confusion_matrix(y_test, y_pred_original).tolist(),
        'class_names': label_encoder.classes_.tolist()
    }
    
    logger.info(f"Test Accuracy: {accuracy:.4f}")
    logger.info(f"Cross-validation Score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    return evaluation_results


def save_artifacts(model: SVC, feature_extractor: FeatureExtractor, 
                  label_encoder: LabelEncoder, evaluation_results: Dict[str, Any],
                  output_dir: str, logger: logging.Logger):
    """Save model and artifacts"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save model
    model_path = output_path / "svm_model.pkl"
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    logger.info(f"Model saved to {model_path}")
    
    # Save feature extractor
    feature_extractor_path = output_path / "feature_extractor.pkl"
    feature_extractor.save(str(feature_extractor_path))
    
    # Save label encoder
    encoder_path = output_path / "label_encoder.pkl"
    with open(encoder_path, 'wb') as f:
        pickle.dump(label_encoder, f)
    logger.info(f"Label encoder saved to {encoder_path}")
    
    # Save evaluation results
    results_path = output_path / "evaluation_results.json"
    with open(results_path, 'w') as f:
        json.dump(evaluation_results, f, indent=2, ensure_ascii=False)
    logger.info(f"Evaluation results saved to {results_path}")


def main():
    parser = argparse.ArgumentParser(description="Train SVM sentiment analysis model")
    parser.add_argument(
        "--input", 
        type=str, 
        default="data/processed/clean_comments.csv",
        help="Path to processed data file"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="data/models",
        help="Directory to save model artifacts"
    )
    parser.add_argument(
        "--test-size",
        type=float,
        default=0.2,
        help="Test set size ratio"
    )
    parser.add_argument(
        "--random-state",
        type=int,
        default=42,
        help="Random state for reproducibility"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logging()
    
    try:
        # Load data
        df, X, y = load_data(args.input, logger)
        
        # Split data - try stratified, fallback to regular split if needed
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=args.test_size, 
                random_state=args.random_state, stratify=y
            )
        except ValueError:
            # Fallback to regular split if stratification fails
            logger.warning("Stratified split failed, using regular split")
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=args.test_size, 
                random_state=args.random_state
            )
        
        logger.info(f"Training set size: {len(X_train)}")
        logger.info(f"Test set size: {len(X_test)}")
        
        # Initialize feature extractor
        feature_extractor = FeatureExtractor(
            max_features=5000,
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.95
        )
        
        # Train model
        model, label_encoder = train_svm_model(
            X_train, y_train, feature_extractor, logger
        )
        
        # Evaluate model
        evaluation_results = evaluate_model(
            model, X_test, y_test, X_train, y_train,
            feature_extractor, label_encoder, logger
        )
        
        # Save artifacts
        save_artifacts(
            model, feature_extractor, label_encoder, 
            evaluation_results, args.output_dir, logger
        )
        
        logger.info("Model training completed successfully!")
        
        # Print summary
        print("\n" + "="*50)
        print("MODEL TRAINING SUMMARY")
        print("="*50)
        print(f"Dataset: {args.input}")
        print(f"Training samples: {len(X_train)}")
        print(f"Test samples: {len(X_test)}")
        print(f"Test Accuracy: {evaluation_results['accuracy']:.4f}")
        print(f"CV Score: {evaluation_results['cv_mean_score']:.4f} (+/- {evaluation_results['cv_std_score']*2:.4f})")
        print(f"Model saved to: {args.output_dir}")
        print("="*50)
        
    except Exception as e:
        logger.error(f"Error during model training: {e}")
        raise


if __name__ == "__main__":
    main()
