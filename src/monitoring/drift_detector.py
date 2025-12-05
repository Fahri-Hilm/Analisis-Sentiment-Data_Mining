"""
Model Drift Detection and Monitoring
"""
import logging
from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
from sklearn.metrics import f1_score, accuracy_score

class DriftDetector:
    """Detect model performance drift"""
    
    def __init__(self, baseline_metrics: Dict[str, float]):
        self.baseline_metrics = baseline_metrics
        self.logger = self._setup_logger()
        self.drift_history = []
    
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger
    
    def detect_performance_drift(self, y_true: np.ndarray, y_pred: np.ndarray,
                                threshold: float = 0.05) -> Dict[str, Any]:
        """
        Detect if model performance has drifted
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            threshold: Drift threshold (default 5%)
        """
        current_accuracy = accuracy_score(y_true, y_pred)
        current_f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
        
        baseline_accuracy = self.baseline_metrics.get('accuracy', 0)
        baseline_f1 = self.baseline_metrics.get('f1_score', 0)
        
        accuracy_drift = baseline_accuracy - current_accuracy
        f1_drift = baseline_f1 - current_f1
        
        has_drift = (abs(accuracy_drift) > threshold or 
                    abs(f1_drift) > threshold)
        
        drift_info = {
            'has_drift': has_drift,
            'accuracy_drift': float(accuracy_drift),
            'f1_drift': float(f1_drift),
            'current_accuracy': float(current_accuracy),
            'current_f1': float(current_f1),
            'baseline_accuracy': float(baseline_accuracy),
            'baseline_f1': float(baseline_f1),
            'threshold': threshold
        }
        
        if has_drift:
            self.logger.warning(f"Model drift detected! Accuracy drift: {accuracy_drift:.4f}")
        
        self.drift_history.append(drift_info)
        return drift_info
    
    def detect_data_drift(self, X_baseline: np.ndarray, X_current: np.ndarray,
                         feature_names: list = None) -> Dict[str, Any]:
        """
        Detect data distribution drift using statistical tests
        """
        from scipy import stats
        
        drift_features = []
        
        for i in range(X_baseline.shape[1]):
            baseline_col = X_baseline[:, i]
            current_col = X_current[:, i]
            
            # Kolmogorov-Smirnov test
            ks_stat, ks_pvalue = stats.ks_2samp(baseline_col, current_col)
            
            feature_name = feature_names[i] if feature_names else f"feature_{i}"
            
            if ks_pvalue < 0.05:
                drift_features.append({
                    'feature': feature_name,
                    'ks_statistic': float(ks_stat),
                    'p_value': float(ks_pvalue),
                    'drifted': True
                })
        
        return {
            'total_features': X_baseline.shape[1],
            'drifted_features': len(drift_features),
            'drift_details': drift_features
        }
    
    def get_drift_summary(self) -> Dict[str, Any]:
        """Get summary of drift history"""
        if not self.drift_history:
            return {'message': 'No drift history available'}
        
        accuracies = [d['current_accuracy'] for d in self.drift_history]
        f1_scores = [d['current_f1'] for d in self.drift_history]
        
        return {
            'total_checks': len(self.drift_history),
            'drift_detected_count': sum(1 for d in self.drift_history if d['has_drift']),
            'avg_accuracy': float(np.mean(accuracies)),
            'min_accuracy': float(np.min(accuracies)),
            'max_accuracy': float(np.max(accuracies)),
            'avg_f1': float(np.mean(f1_scores))
        }
