"""
Train Hybrid ML Classifier for Unknown Comment Labeling
Target: Reduce unknown rate from 65% to <10% while maintaining >85% accuracy
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import json
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class HybridClassifierTrainer:
    """
    Train ML classifiers for each layer to predict unknown labels
    Uses TF-IDF features from cleaned comment text
    """
    
    def __init__(self, data_path: str, output_dir: str = 'data/models/hybrid'):
        self.data_path = data_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Will store trained models and vectorizers
        self.models = {}
        self.vectorizers = {}
        self.metrics = {}
        
    def load_data(self):
        """Load V4 labeled dataset"""
        logger.info(f"Loading data from {self.data_path}")
        self.df = pd.read_csv(self.data_path)
        logger.info(f"Loaded {len(self.df):,} comments")
        
        # Log distribution
        logger.info("\nData Distribution:")
        for layer in ['root_cause', 'time_perspective', 'constructiveness']:
            dist = self.df[layer].value_counts()
            logger.info(f"\n{layer}:")
            for label, count in dist.items():
                pct = count / len(self.df) * 100
                logger.info(f"  {label}: {count:,} ({pct:.1f}%)")
    
    def prepare_layer_data(self, layer_name: str, label_column: str):
        """
        Prepare training data for a specific layer
        Only use labeled comments (exclude 'unknown')
        
        Args:
            layer_name: e.g., 'layer3_cause'
            label_column: e.g., 'layer3_cause_label'
        
        Returns:
            X_train, X_test, y_train, y_test
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"Preparing data for {layer_name}")
        logger.info(f"{'='*60}")
        
        # Filter out unknown labels
        labeled_df = self.df[self.df[label_column] != 'unknown'].copy()
        logger.info(f"Labeled samples: {len(labeled_df):,} ({len(labeled_df)/len(self.df)*100:.1f}%)")
        logger.info(f"Unknown samples: {len(self.df) - len(labeled_df):,} ({(len(self.df)-len(labeled_df))/len(self.df)*100:.1f}%)")
        
        # Check class distribution
        class_dist = labeled_df[label_column].value_counts()
        logger.info(f"\nClass distribution:")
        for label, count in class_dist.items():
            logger.info(f"  {label}: {count:,}")
        
        # Split into train/test
        X = labeled_df['clean_text'].values
        y = labeled_df[label_column].values
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        logger.info(f"\nTrain size: {len(X_train):,}")
        logger.info(f"Test size: {len(X_test):,}")
        
        return X_train, X_test, y_train, y_test
    
    def train_layer_classifier(self, layer_name: str, label_column: str, 
                               max_features: int = 3000, min_df: int = 2):
        """
        Train SVM classifier for a specific layer
        
        Args:
            layer_name: e.g., 'layer3_cause'
            label_column: e.g., 'layer3_cause_label'
            max_features: Maximum TF-IDF features
            min_df: Minimum document frequency
        
        Returns:
            model, vectorizer, test_metrics
        """
        # Prepare data
        X_train, X_test, y_train, y_test = self.prepare_layer_data(layer_name, label_column)
        
        # TF-IDF Vectorization
        logger.info(f"\nCreating TF-IDF features (max_features={max_features}, min_df={min_df})")
        vectorizer = TfidfVectorizer(
            max_features=max_features,
            min_df=min_df,
            ngram_range=(1, 2),  # Unigrams and bigrams
            strip_accents='unicode',
            lowercase=True
        )
        
        X_train_tfidf = vectorizer.fit_transform(X_train)
        X_test_tfidf = vectorizer.transform(X_test)
        
        logger.info(f"TF-IDF shape: {X_train_tfidf.shape}")
        logger.info(f"Vocabulary size: {len(vectorizer.vocabulary_)}")
        
        # Train LinearSVC (faster than RBF SVM for text)
        logger.info(f"\nTraining LinearSVC classifier...")
        model = LinearSVC(
            C=1.0,
            max_iter=2000,
            random_state=42,
            class_weight='balanced'  # Handle class imbalance
        )
        
        model.fit(X_train_tfidf, y_train)
        logger.info("✅ Training complete!")
        
        # Evaluate on test set
        logger.info(f"\nEvaluating on test set...")
        y_pred = model.predict(X_test_tfidf)
        
        accuracy = accuracy_score(y_test, y_pred)
        logger.info(f"Test Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
        
        # Classification report
        report = classification_report(y_test, y_pred, output_dict=True)
        logger.info(f"\nClassification Report:")
        logger.info(classification_report(y_test, y_pred))
        
        # Cross-validation score
        logger.info(f"\nPerforming 5-fold cross-validation...")
        cv_scores = cross_val_score(
            model, X_train_tfidf, y_train, cv=5, scoring='accuracy'
        )
        logger.info(f"CV Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
        
        # Store metrics
        metrics = {
            'layer': layer_name,
            'test_accuracy': float(accuracy),
            'cv_mean': float(cv_scores.mean()),
            'cv_std': float(cv_scores.std()),
            'classification_report': report,
            'train_samples': int(len(X_train)),
            'test_samples': int(len(X_test)),
            'num_classes': int(len(np.unique(y_train))),
            'classes': list(np.unique(y_train)),
            'vocabulary_size': len(vectorizer.vocabulary_)
        }
        
        return model, vectorizer, metrics
    
    def train_all_layers(self):
        """Train classifiers for Layer 3, 4, 5"""
        logger.info("\n" + "="*60)
        logger.info("TRAINING HYBRID CLASSIFIERS FOR ALL LAYERS")
        logger.info("="*60)
        
        layers_config = [
            ('layer3_cause', 'root_cause', 3000),
            ('layer4_time', 'time_perspective', 2000),
            ('layer5_constructive', 'constructiveness', 2500)
        ]
        
        for layer_name, label_col, max_features in layers_config:
            logger.info(f"\n{'#'*60}")
            logger.info(f"# TRAINING {layer_name.upper()}")
            logger.info(f"{'#'*60}")
            
            try:
                model, vectorizer, metrics = self.train_layer_classifier(
                    layer_name, label_col, max_features
                )
                
                # Store
                self.models[layer_name] = model
                self.vectorizers[layer_name] = vectorizer
                self.metrics[layer_name] = metrics
                
                # Save model and vectorizer
                model_path = self.output_dir / f'{layer_name}_classifier.pkl'
                vectorizer_path = self.output_dir / f'{layer_name}_vectorizer.pkl'
                
                joblib.dump(model, model_path)
                joblib.dump(vectorizer, vectorizer_path)
                
                logger.info(f"\n✅ Saved model to: {model_path}")
                logger.info(f"✅ Saved vectorizer to: {vectorizer_path}")
                
            except Exception as e:
                logger.error(f"❌ Error training {layer_name}: {e}")
                import traceback
                traceback.print_exc()
        
        # Save all metrics
        metrics_path = self.output_dir / 'training_metrics.json'
        with open(metrics_path, 'w') as f:
            json.dump(self.metrics, f, indent=2)
        
        logger.info(f"\n✅ Saved all metrics to: {metrics_path}")
        
    def summarize_results(self):
        """Print summary of all models"""
        logger.info("\n" + "="*60)
        logger.info("TRAINING SUMMARY")
        logger.info("="*60)
        
        for layer_name, metrics in self.metrics.items():
            logger.info(f"\n{layer_name.upper()}:")
            logger.info(f"  Test Accuracy: {metrics['test_accuracy']:.4f} ({metrics['test_accuracy']*100:.2f}%)")
            logger.info(f"  CV Accuracy: {metrics['cv_mean']:.4f} (+/- {metrics['cv_std']:.4f})")
            logger.info(f"  Train Samples: {metrics['train_samples']:,}")
            logger.info(f"  Test Samples: {metrics['test_samples']:,}")
            logger.info(f"  Classes: {metrics['num_classes']} - {metrics['classes']}")
            logger.info(f"  Vocabulary: {metrics['vocabulary_size']:,} features")
        
        # Average accuracy
        avg_accuracy = np.mean([m['test_accuracy'] for m in self.metrics.values()])
        logger.info(f"\n{'='*60}")
        logger.info(f"AVERAGE TEST ACCURACY: {avg_accuracy:.4f} ({avg_accuracy*100:.2f}%)")
        logger.info(f"{'='*60}")
        
        if avg_accuracy >= 0.85:
            logger.info("✅ Target achieved: >85% accuracy!")
        else:
            logger.info(f"⚠️ Target not met: {avg_accuracy*100:.2f}% < 85%")


def main():
    """Main training pipeline"""
    
    # Initialize trainer
    trainer = HybridClassifierTrainer(
        data_path='data/processed/optimized_clean_comments_v4_phrases.csv',
        output_dir='data/models/hybrid'
    )
    
    # Load data
    trainer.load_data()
    
    # Train all layers
    trainer.train_all_layers()
    
    # Summarize
    trainer.summarize_results()
    
    logger.info("\n" + "="*60)
    logger.info("✅ HYBRID CLASSIFIER TRAINING COMPLETE!")
    logger.info("="*60)
    logger.info("\nNext step: Apply models to predict unknown comments")
    logger.info("Run: python src/modeling/apply_hybrid_classifier.py")


if __name__ == '__main__':
    main()
