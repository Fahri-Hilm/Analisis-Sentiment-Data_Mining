"""
Error Analysis for Model Misclassifications
"""
import logging
from typing import Dict, List, Tuple
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report

class ErrorAnalyzer:
    """Analyze model errors and misclassifications"""
    
    def __init__(self):
        self.logger = self._setup_logger()
        self.error_samples = None
        self.confusion_matrix = None
    
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
    
    def analyze_errors(self, y_true: np.ndarray, y_pred: np.ndarray,
                      texts: pd.Series = None) -> Dict:
        """
        Analyze misclassifications
        """
        self.confusion_matrix = confusion_matrix(y_true, y_pred)
        
        errors = y_true != y_pred
        error_count = errors.sum()
        error_rate = error_count / len(y_true)
        
        self.logger.info(f"Total errors: {error_count}/{len(y_true)} ({error_rate:.2%})")
        
        analysis = {
            'total_errors': int(error_count),
            'error_rate': float(error_rate),
            'confusion_matrix': self.confusion_matrix.tolist(),
            'error_samples': []
        }
        
        if texts is not None:
            error_indices = np.where(errors)[0]
            for idx in error_indices[:100]:
                analysis['error_samples'].append({
                    'text': texts.iloc[idx],
                    'true_label': y_true[idx],
                    'predicted_label': y_pred[idx]
                })
        
        return analysis
    
    def get_per_class_errors(self, y_true: np.ndarray, y_pred: np.ndarray,
                            class_names: List[str]) -> Dict:
        """Get error breakdown per class"""
        report = classification_report(y_true, y_pred, 
                                      target_names=class_names,
                                      output_dict=True, zero_division=0)
        
        per_class_errors = {}
        for class_name in class_names:
            if class_name in report:
                per_class_errors[class_name] = {
                    'precision': report[class_name]['precision'],
                    'recall': report[class_name]['recall'],
                    'f1_score': report[class_name]['f1-score'],
                    'support': int(report[class_name]['support'])
                }
        
        return per_class_errors
    
    def identify_hard_samples(self, y_true: np.ndarray, y_pred: np.ndarray,
                             y_proba: np.ndarray, threshold: float = 0.6) -> Dict:
        """Identify samples with low confidence predictions"""
        max_proba = np.max(y_proba, axis=1)
        hard_samples = max_proba < threshold
        
        hard_count = hard_samples.sum()
        
        return {
            'hard_sample_count': int(hard_count),
            'hard_sample_rate': float(hard_count / len(y_true)),
            'confidence_threshold': threshold,
            'hard_sample_indices': np.where(hard_samples)[0].tolist()
        }
