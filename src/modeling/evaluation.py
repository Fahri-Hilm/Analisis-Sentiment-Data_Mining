"""
Model Evaluation Module

This module provides comprehensive evaluation metrics and visualization
for sentiment classification models.
"""

import logging
import json
from typing import Dict, Any, List
import pandas as pd
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    roc_auc_score
)

class ModelEvaluator:
    """
    Comprehensive model evaluation with multiple metrics
    """
    
    def __init__(self):
        """Initialize evaluator"""
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        """Setup logging configuration"""
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

    def evaluate(self, y_true: np.ndarray, y_pred: np.ndarray, 
                y_pred_proba: np.ndarray = None) -> Dict[str, Any]:
        """
        Comprehensive evaluation of model predictions
        
        Args:
            y_true (np.ndarray): True labels
            y_pred (np.ndarray): Predicted labels
            y_pred_proba (np.ndarray, optional): Prediction probabilities
            
        Returns:
            Dict: Evaluation metrics
        """
        self.logger.info("Evaluating model performance...")
        
        # Basic metrics
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_true, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
        
        # Detailed classification report
        report = classification_report(y_true, y_pred, output_dict=True, zero_division=0)
        
        # Confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        
        results = {
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1_score': float(f1),
            'classification_report': report,
            'confusion_matrix': cm.tolist(),
            'confusion_matrix_labels': list(np.unique(y_true))
        }
        
        # ROC-AUC if probabilities are provided
        if y_pred_proba is not None:
            try:
                # For multiclass, use one-vs-rest approach
                from sklearn.preprocessing import label_binarize
                classes = np.unique(y_true)
                
                if len(classes) == 2:
                    # Binary classification
                    roc_auc = roc_auc_score(y_true, y_pred_proba[:, 1])
                else:
                    # Multiclass
                    y_true_bin = label_binarize(y_true, classes=classes)
                    roc_auc = roc_auc_score(y_true_bin, y_pred_proba, 
                                           average='weighted', multi_class='ovr')
                
                results['roc_auc'] = float(roc_auc)
            except Exception as e:
                self.logger.warning(f"Could not calculate ROC-AUC: {e}")
        
        self.logger.info(f"Accuracy: {accuracy:.4f}")
        self.logger.info(f"Precision: {precision:.4f}")
        self.logger.info(f"Recall: {recall:.4f}")
        self.logger.info(f"F1 Score: {f1:.4f}")
        
        return results

    def save_results(self, results: Dict[str, Any], filepath: str):
        """
        Save evaluation results to JSON file
        
        Args:
            results (Dict): Evaluation results
            filepath (str): Path to save results
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Evaluation results saved to {filepath}")
        except Exception as e:
            self.logger.error(f"Error saving results: {e}")

    def print_report(self, results: Dict[str, Any]):
        """
        Print formatted evaluation report
        
        Args:
            results (Dict): Evaluation results
        """
        print("\n" + "="*60)
        print("MODEL EVALUATION REPORT")
        print("="*60)
        print(f"\nOverall Metrics:")
        print(f"  Accuracy:  {results['accuracy']:.4f}")
        print(f"  Precision: {results['precision']:.4f}")
        print(f"  Recall:    {results['recall']:.4f}")
        print(f"  F1 Score:  {results['f1_score']:.4f}")
        
        if 'roc_auc' in results:
            print(f"  ROC-AUC:   {results['roc_auc']:.4f}")
        
        print(f"\nPer-Class Metrics:")
        report = results['classification_report']
        for label, metrics in report.items():
            if label not in ['accuracy', 'macro avg', 'weighted avg']:
                if isinstance(metrics, dict):
                    print(f"  {label}:")
                    print(f"    Precision: {metrics.get('precision', 0):.4f}")
                    print(f"    Recall:    {metrics.get('recall', 0):.4f}")
                    print(f"    F1-Score:  {metrics.get('f1-score', 0):.4f}")
                    print(f"    Support:   {metrics.get('support', 0)}")
        
        print("\n" + "="*60)
