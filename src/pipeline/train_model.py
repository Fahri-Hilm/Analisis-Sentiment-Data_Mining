"""
Model Training Pipeline

This script orchestrates the complete training workflow:
1. Load preprocessed data
2. Extract features with TF-IDF
3. Train SVM model with optional hyperparameter tuning
4. Evaluate model performance
5. Save trained model and results
"""

import argparse
import json
import os
from pathlib import Path
from typing import Tuple

import pandas as pd
from sklearn.model_selection import train_test_split

from src.modeling.features import FeatureExtractor
from src.modeling.svm_model import SVMSentimentModel
from src.modeling.evaluation import ModelEvaluator


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train SVM sentiment analysis model"
    )
    parser.add_argument(
        "--input",
        type=str,
        default="data/processed/comments_clean.csv",
        help="Path to preprocessed comments CSV"
    )
    parser.add_argument(
        "--text-column",
        type=str,
        default="normalized_text",
        help="Column containing processed text"
    )
    parser.add_argument(
        "--label-column",
        type=str,
        default="sentiment_label",
        help="Column containing sentiment labels"
    )
    parser.add_argument(
        "--test-size",
        type=float,
        default=0.2,
        help="Proportion of data for testing"
    )
    parser.add_argument(
        "--max-features",
        type=int,
        default=5000,
        help="Maximum TF-IDF features"
    )
    parser.add_argument(
        "--tune-hyperparameters",
        action="store_true",
        help="Perform hyperparameter tuning"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="data/models",
        help="Directory to save trained models"
    )
    return parser.parse_args()


def load_data(filepath: str, text_column: str, label_column: str) -> Tuple[pd.Series, pd.Series]:
    """Load and prepare data"""
    df = pd.read_csv(filepath)
    
    # Filter out unknown/empty labels
    df = df[df[label_column].notna()]
    df = df[df[label_column] != 'unknown']
    df = df[df[text_column].notna()]
    df = df[df[text_column].str.len() > 0]
    
    X = df[text_column]
    y = df[label_column]
    
    return X, y


def main():
    args = parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("="*60)
    print("SVM SENTIMENT ANALYSIS TRAINING PIPELINE")
    print("="*60)
    
    # Load data
    print(f"\n1. Loading data from {args.input}...")
    X, y = load_data(args.input, args.text_column, args.label_column)
    print(f"   Loaded {len(X)} samples")
    print(f"   Label distribution:\n{y.value_counts()}")
    
    # Split data
    print(f"\n2. Splitting data (test_size={args.test_size})...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.test_size, random_state=42, stratify=y
    )
    print(f"   Train: {len(X_train)} samples")
    print(f"   Test:  {len(X_test)} samples")
    
    # Feature extraction
    print(f"\n3. Extracting TF-IDF features (max_features={args.max_features})...")
    feature_extractor = FeatureExtractor(max_features=args.max_features)
    X_train_features = feature_extractor.fit_transform(X_train)
    X_test_features = feature_extractor.transform(X_test)
    print(f"   Feature matrix shape: {X_train_features.shape}")
    
    # Save feature extractor
    feature_path = output_dir / "feature_extractor.pkl"
    feature_extractor.save(str(feature_path))
    
    # Train model
    print(f"\n4. Training SVM model...")
    model = SVMSentimentModel()
    
    if args.tune_hyperparameters:
        print("   Performing hyperparameter tuning...")
        tuning_results = model.hyperparameter_tuning(X_train_features, y_train)
        
        # Save tuning results
        tuning_path = output_dir / "hyperparameter_tuning.json"
        with open(tuning_path, 'w') as f:
            # Convert numpy types to native Python types for JSON serialization
            tuning_results_serializable = {
                'best_params': tuning_results['best_params'],
                'best_score': float(tuning_results['best_score'])
            }
            json.dump(tuning_results_serializable, f, indent=2)
    else:
        model.fit(X_train_features, y_train)
    
    # Save model
    model_path = output_dir / "svm_model.pkl"
    encoder_path = output_dir / "label_encoder.pkl"
    model.save(str(model_path), str(encoder_path))
    
    # Evaluate on test set
    print(f"\n5. Evaluating model...")
    y_pred = model.predict(X_test_features)
    y_pred_proba = model.predict_proba(X_test_features)
    
    evaluator = ModelEvaluator()
    results = evaluator.evaluate(y_test.values, y_pred, y_pred_proba)
    
    # Print and save results
    evaluator.print_report(results)
    
    results_path = output_dir / "evaluation_results.json"
    evaluator.save_results(results, str(results_path))
    
    # Save training summary
    summary = {
        "input_file": args.input,
        "total_samples": len(X),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "max_features": args.max_features,
        "hyperparameter_tuning": args.tune_hyperparameters,
        "test_accuracy": results['accuracy'],
        "test_f1_score": results['f1_score'],
        "label_distribution": y.value_counts().to_dict(),
        "output_directory": str(output_dir)
    }
    
    summary_path = output_dir / "training_summary.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n6. Training complete!")
    print(f"   Models saved to: {output_dir}")
    print(f"   - {model_path.name}")
    print(f"   - {encoder_path.name}")
    print(f"   - {feature_path.name}")
    print(f"   - {results_path.name}")
    print(f"   - {summary_path.name}")
    print("="*60)


if __name__ == "__main__":
    main()
