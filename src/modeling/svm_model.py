"""
SVM Model Module for Sentiment Analysis

This module implements the SVM classifier with hyperparameter tuning
and model persistence capabilities.
"""

import pickle
import logging
from typing import Dict, Any, Optional, Tuple
import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import LabelEncoder

class SVMSentimentModel:
    """
    Support Vector Machine classifier for sentiment analysis
    """
    
    def __init__(self, 
                 kernel: str = 'linear',
                 C: float = 1.0,
                 class_weight: str = 'balanced',
                 random_state: int = 42):
        """
        Initialize SVM Model
        
        Args:
            kernel (str): Kernel type
            C (float): Regularization parameter
            class_weight (str): Class weight strategy
            random_state (int): Random seed
        """
        self.logger = self._setup_logger()
        self.kernel = kernel
        self.C = C
        self.class_weight = class_weight
        self.random_state = random_state
        
        self.model = SVC(
            kernel=kernel,
            C=C,
            class_weight=class_weight,
            random_state=random_state,
            probability=True  # Enable probability estimates
        )
        
        self.label_encoder = LabelEncoder()
        self.is_fitted = False
        
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

    def fit(self, X, y: pd.Series) -> 'SVMSentimentModel':
        """
        Train the SVM model
        
        Args:
            X: Feature matrix (sparse or dense)
            y (pd.Series): Target labels
            
        Returns:
            self
        """
        self.logger.info(f"Training SVM on {X.shape[0]} samples with {X.shape[1]} features...")
        
        # Encode labels
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Train model
        self.model.fit(X, y_encoded)
        self.is_fitted = True
        
        self.logger.info(f"Training complete. Classes: {self.label_encoder.classes_}")
        return self

    def predict(self, X) -> np.ndarray:
        """
        Predict sentiment labels
        
        Args:
            X: Feature matrix
            
        Returns:
            Array of predicted labels
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")
        
        y_pred_encoded = self.model.predict(X)
        return self.label_encoder.inverse_transform(y_pred_encoded)

    def predict_proba(self, X) -> np.ndarray:
        """
        Predict sentiment probabilities
        
        Args:
            X: Feature matrix
            
        Returns:
            Array of class probabilities
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")
        
        return self.model.predict_proba(X)

    def hyperparameter_tuning(self, X, y: pd.Series, 
                             param_grid: Optional[Dict] = None,
                             cv: int = 5) -> Dict[str, Any]:
        """
        Perform hyperparameter tuning using GridSearchCV
        
        Args:
            X: Feature matrix
            y (pd.Series): Target labels
            param_grid (Dict, optional): Parameter grid for search
            cv (int): Number of cross-validation folds
            
        Returns:
            Dict: Best parameters and score
        """
        if param_grid is None:
            param_grid = {
                'C': [0.1, 1, 10, 100],
                'kernel': ['linear', 'rbf'],
                'class_weight': ['balanced', None]
            }
        
        self.logger.info("Starting hyperparameter tuning...")
        
        # Encode labels
        y_encoded = self.label_encoder.fit_transform(y)
        
        # GridSearch
        grid_search = GridSearchCV(
            SVC(random_state=self.random_state, probability=True),
            param_grid,
            cv=cv,
            scoring='f1_weighted',
            n_jobs=-1,
            verbose=1
        )
        
        grid_search.fit(X, y_encoded)
        
        # Update model with best parameters
        self.model = grid_search.best_estimator_
        self.is_fitted = True
        
        self.logger.info(f"Best parameters: {grid_search.best_params_}")
        self.logger.info(f"Best score: {grid_search.best_score_:.4f}")
        
        return {
            'best_params': grid_search.best_params_,
            'best_score': grid_search.best_score_,
            'cv_results': grid_search.cv_results_
        }

    def save(self, model_path: str, encoder_path: str):
        """
        Save model and label encoder
        
        Args:
            model_path (str): Path to save the model
            encoder_path (str): Path to save the encoder
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before saving")
        
        try:
            with open(model_path, 'wb') as f:
                pickle.dump(self.model, f)
            self.logger.info(f"Model saved to {model_path}")
            
            with open(encoder_path, 'wb') as f:
                pickle.dump(self.label_encoder, f)
            self.logger.info(f"Label encoder saved to {encoder_path}")
            
        except Exception as e:
            self.logger.error(f"Error saving model: {e}")
            raise e

    @staticmethod
    def load(model_path: str, encoder_path: str) -> 'SVMSentimentModel':
        """
        Load model and label encoder
        
        Args:
            model_path (str): Path to load the model from
            encoder_path (str): Path to load the encoder from
            
        Returns:
            SVMSentimentModel: Loaded instance
        """
        try:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            
            with open(encoder_path, 'rb') as f:
                label_encoder = pickle.load(f)
            
            # Create instance and set attributes
            instance = SVMSentimentModel()
            instance.model = model
            instance.label_encoder = label_encoder
            instance.is_fitted = True
            
            instance.logger.info(f"Model loaded from {model_path}")
            instance.logger.info(f"Label encoder loaded from {encoder_path}")
            
            return instance
            
        except Exception as e:
            logging.getLogger(__name__).error(f"Error loading model: {e}")
            raise e
