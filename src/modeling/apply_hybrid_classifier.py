"""
Apply Hybrid ML Classifier to Unknown Comments
Combine rule-based labels (V4) with ML predictions to achieve <10% unknown
"""

import pandas as pd
import numpy as np
import joblib
import json
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class HybridClassifierApplicator:
    """
    Apply trained ML models to predict unknown labels
    Combine with rule-based predictions for hybrid approach
    """
    
    def __init__(self, 
                 data_path: str,
                 models_dir: str = 'data/models/hybrid',
                 output_path: str = 'data/processed/optimized_clean_comments_v5_hybrid.csv',
                 confidence_threshold: float = 0.60):
        """
        Args:
            data_path: Path to V4 labeled dataset
            models_dir: Directory containing trained models
            output_path: Path for V5 hybrid output
            confidence_threshold: Minimum confidence to use ML prediction (0.6 = 60%)
        """
        self.data_path = data_path
        self.models_dir = Path(models_dir)
        self.output_path = output_path
        self.confidence_threshold = confidence_threshold
        
        self.models = {}
        self.vectorizers = {}
        
    def load_models(self):
        """Load trained models and vectorizers"""
        logger.info("Loading trained models and vectorizers...")
        
        layers = ['layer3_cause', 'layer4_time', 'layer5_constructive']
        
        for layer in layers:
            model_path = self.models_dir / f'{layer}_classifier.pkl'
            vectorizer_path = self.models_dir / f'{layer}_vectorizer.pkl'
            
            self.models[layer] = joblib.load(model_path)
            self.vectorizers[layer] = joblib.load(vectorizer_path)
            
            logger.info(f"✅ Loaded {layer} model and vectorizer")
        
        logger.info("All models loaded successfully!")
    
    def load_data(self):
        """Load V4 dataset"""
        logger.info(f"Loading data from {self.data_path}")
        self.df = pd.read_csv(self.data_path)
        logger.info(f"Loaded {len(self.df):,} comments")
        
        # Log current unknown rates
        logger.info("\n" + "="*60)
        logger.info("V4 UNKNOWN RATES (Before ML):")
        logger.info("="*60)
        
        for col in ['root_cause', 'time_perspective', 'constructiveness']:
            unknown_count = (self.df[col] == 'unknown').sum()
            unknown_pct = unknown_count / len(self.df) * 100
            logger.info(f"{col}: {unknown_count:,} ({unknown_pct:.1f}%)")
    
    def predict_with_confidence(self, layer_name: str, label_column: str):
        """
        Predict labels for unknown comments with confidence scores
        
        Args:
            layer_name: e.g., 'layer3_cause'
            label_column: e.g., 'root_cause'
        
        Returns:
            predictions: Series with predicted labels
            confidences: Series with confidence scores
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"Predicting {layer_name} ({label_column})")
        logger.info(f"{'='*60}")
        
        # Get unknown comments
        unknown_mask = self.df[label_column] == 'unknown'
        unknown_count = unknown_mask.sum()
        
        logger.info(f"Unknown comments: {unknown_count:,}")
        
        if unknown_count == 0:
            logger.info("No unknown comments to predict!")
            return pd.Series(index=self.df.index), pd.Series(index=self.df.index)
        
        # Get text for unknown comments
        unknown_texts = self.df.loc[unknown_mask, 'clean_text'].values
        
        # Transform to TF-IDF
        vectorizer = self.vectorizers[layer_name]
        X = vectorizer.transform(unknown_texts)
        
        # Predict
        model = self.models[layer_name]
        predictions = model.predict(X)
        
        # Get decision function scores for confidence
        # For LinearSVC, decision_function returns distance to hyperplane
        decision_scores = model.decision_function(X)
        
        # Convert to confidence: normalize decision scores
        if decision_scores.ndim == 1:
            # Binary classification
            confidences = np.abs(decision_scores)
            # Use more aggressive normalization for LinearSVC
            confidences = 1 / (1 + np.exp(-confidences / 2.0))  # Sigmoid normalization
        else:
            # Multi-class: use max score across classes
            max_scores = np.max(decision_scores, axis=1)
            # Sigmoid normalization
            confidences = 1 / (1 + np.exp(-max_scores / 2.0))
        
        # Filter by confidence threshold
        high_confidence_mask = confidences >= self.confidence_threshold
        accepted_count = high_confidence_mask.sum()
        rejected_count = unknown_count - accepted_count
        
        logger.info(f"Predictions made: {unknown_count:,}")
        logger.info(f"High confidence (>={self.confidence_threshold:.0%}): {accepted_count:,} ({accepted_count/unknown_count*100:.1f}%)")
        logger.info(f"Low confidence (rejected): {rejected_count:,} ({rejected_count/unknown_count*100:.1f}%)")
        
        # Create full series with predictions only for high confidence
        full_predictions = pd.Series('unknown', index=self.df.index)
        full_confidences = pd.Series(0.0, index=self.df.index)
        
        unknown_indices = self.df[unknown_mask].index
        for i, idx in enumerate(unknown_indices):
            if high_confidence_mask[i]:
                full_predictions.loc[idx] = predictions[i]
                full_confidences.loc[idx] = confidences[i]
        
        # Log predicted distribution
        predicted_labels = full_predictions[full_predictions != 'unknown']
        if len(predicted_labels) > 0:
            logger.info(f"\nPredicted label distribution:")
            for label, count in predicted_labels.value_counts().items():
                logger.info(f"  {label}: {count:,}")
        
        return full_predictions, full_confidences
    
    def apply_hybrid_labeling(self):
        """Apply ML predictions to unknown comments"""
        logger.info("\n" + "#"*60)
        logger.info("# APPLYING HYBRID LABELING")
        logger.info("#"*60)
        
        # Create copies for hybrid labels
        self.df['root_cause_v5'] = self.df['root_cause'].copy()
        self.df['time_perspective_v5'] = self.df['time_perspective'].copy()
        self.df['constructiveness_v5'] = self.df['constructiveness'].copy()
        
        # Also create confidence columns
        self.df['root_cause_ml_confidence'] = 0.0
        self.df['time_perspective_ml_confidence'] = 0.0
        self.df['constructiveness_ml_confidence'] = 0.0
        
        # Apply predictions for each layer
        layers_config = [
            ('layer3_cause', 'root_cause'),
            ('layer4_time', 'time_perspective'),
            ('layer5_constructive', 'constructiveness')
        ]
        
        for layer_name, label_col in layers_config:
            predictions, confidences = self.predict_with_confidence(layer_name, label_col)
            
            # Update V5 labels for previously unknown
            unknown_mask = self.df[label_col] == 'unknown'
            predicted_mask = predictions != 'unknown'
            update_mask = unknown_mask & predicted_mask
            
            self.df.loc[update_mask, f'{label_col}_v5'] = predictions[update_mask]
            self.df.loc[update_mask, f'{label_col}_ml_confidence'] = confidences[update_mask]
            
            updated_count = update_mask.sum()
            logger.info(f"✅ Updated {updated_count:,} labels for {label_col}")
    
    def calculate_improvements(self):
        """Calculate and display improvement statistics"""
        logger.info("\n" + "="*60)
        logger.info("V4 vs V5 COMPARISON")
        logger.info("="*60)
        
        results = []
        
        for v4_col, v5_col in [
            ('root_cause', 'root_cause_v5'),
            ('time_perspective', 'time_perspective_v5'),
            ('constructiveness', 'constructiveness_v5')
        ]:
            v4_unknown = (self.df[v4_col] == 'unknown').sum()
            v5_unknown = (self.df[v5_col] == 'unknown').sum()
            
            v4_pct = v4_unknown / len(self.df) * 100
            v5_pct = v5_unknown / len(self.df) * 100
            
            improvement = v4_pct - v5_pct
            labeled_added = v4_unknown - v5_unknown
            
            logger.info(f"\n{v4_col}:")
            logger.info(f"  V4 Unknown: {v4_unknown:,} ({v4_pct:.1f}%)")
            logger.info(f"  V5 Unknown: {v5_unknown:,} ({v5_pct:.1f}%)")
            logger.info(f"  Improvement: -{improvement:.1f} percentage points")
            logger.info(f"  Labels added: {labeled_added:,}")
            
            results.append({
                'layer': v4_col,
                'v4_unknown': int(v4_unknown),
                'v4_unknown_pct': float(v4_pct),
                'v5_unknown': int(v5_unknown),
                'v5_unknown_pct': float(v5_pct),
                'improvement_pp': float(improvement),
                'labels_added': int(labeled_added)
            })
        
        # Overall stats
        total_v4_unknown = sum(r['v4_unknown'] for r in results)
        total_v5_unknown = sum(r['v5_unknown'] for r in results)
        total_labeled = total_v4_unknown - total_v5_unknown
        
        logger.info(f"\n{'='*60}")
        logger.info(f"OVERALL STATISTICS:")
        logger.info(f"{'='*60}")
        logger.info(f"Total labels added: {total_labeled:,}")
        logger.info(f"Average unknown reduction: {np.mean([r['improvement_pp'] for r in results]):.1f}pp")
        
        # Check if target achieved
        target_achieved = all(r['v5_unknown_pct'] < 10.0 for r in results)
        if target_achieved:
            logger.info(f"\n🎉 TARGET ACHIEVED: All layers <10% unknown!")
        else:
            logger.info(f"\n⚠️ Some layers still >10% unknown")
            for r in results:
                if r['v5_unknown_pct'] >= 10.0:
                    logger.info(f"  - {r['layer']}: {r['v5_unknown_pct']:.1f}%")
        
        return results
    
    def save_results(self):
        """Save V5 hybrid dataset"""
        logger.info(f"\nSaving V5 hybrid dataset to {self.output_path}")
        self.df.to_csv(self.output_path, index=False)
        logger.info(f"✅ Saved {len(self.df):,} comments")
        
        # Save summary
        summary = {
            'input_file': self.data_path,
            'output_file': self.output_path,
            'total_comments': len(self.df),
            'confidence_threshold': self.confidence_threshold,
            'v4_unknown_rates': {
                'root_cause': float((self.df['root_cause'] == 'unknown').sum() / len(self.df) * 100),
                'time_perspective': float((self.df['time_perspective'] == 'unknown').sum() / len(self.df) * 100),
                'constructiveness': float((self.df['constructiveness'] == 'unknown').sum() / len(self.df) * 100)
            },
            'v5_unknown_rates': {
                'root_cause': float((self.df['root_cause_v5'] == 'unknown').sum() / len(self.df) * 100),
                'time_perspective': float((self.df['time_perspective_v5'] == 'unknown').sum() / len(self.df) * 100),
                'constructiveness': float((self.df['constructiveness_v5'] == 'unknown').sum() / len(self.df) * 100)
            },
            'distributions': {}
        }
        
        # Add V5 distributions
        for col in ['root_cause_v5', 'time_perspective_v5', 'constructiveness_v5']:
            dist = self.df[col].value_counts().to_dict()
            summary['distributions'][col] = {
                str(k): int(v) for k, v in dist.items()
            }
        
        summary_path = self.output_path.replace('.csv', '.summary.json')
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"✅ Saved summary to {summary_path}")


def main():
    """Main application pipeline"""
    
    logger.info("="*60)
    logger.info("HYBRID ML CLASSIFIER APPLICATION")
    logger.info("="*60)
    
    # Initialize applicator
    applicator = HybridClassifierApplicator(
        data_path='data/processed/optimized_clean_comments_v4_phrases.csv',
        models_dir='data/models/hybrid',
        output_path='data/processed/optimized_clean_comments_v5_hybrid.csv',
        confidence_threshold=0.40  # 40% confidence threshold - more aggressive
    )
    
    # Load models
    applicator.load_models()
    
    # Load data
    applicator.load_data()
    
    # Apply hybrid labeling
    applicator.apply_hybrid_labeling()
    
    # Calculate improvements
    results = applicator.calculate_improvements()
    
    # Save results
    applicator.save_results()
    
    logger.info("\n" + "="*60)
    logger.info("✅ HYBRID LABELING COMPLETE!")
    logger.info("="*60)
    logger.info(f"\nOutput: {applicator.output_path}")
    logger.info("Next: Validate accuracy and build dashboard")


if __name__ == '__main__':
    main()
