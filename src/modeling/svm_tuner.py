"""
Advanced SVM Hyperparameter Tuning with Optimization
"""
import logging
from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import f1_score, precision_score, recall_score

class SVMTuner:
    """Advanced SVM hyperparameter tuning"""
    
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.logger = self._setup_logger()
        self.best_model = None
        self.best_params = None
        self.tuning_results = None
    
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
    
    def grid_search_tuning(self, X_train, y_train: pd.Series, 
                          cv: int = 5) -> Tuple[SVC, Dict[str, Any]]:
        """
        Comprehensive grid search for SVM hyperparameters
        """
        param_grid = {
            'C': [0.1, 1, 10, 100, 1000],
            'kernel': ['linear', 'rbf', 'poly'],
            'gamma': ['scale', 'auto', 0.001, 0.01, 0.1],
            'degree': [2, 3, 4],
            'class_weight': ['balanced', None]
        }
        
        self.logger.info("Starting comprehensive grid search...")
        
        label_encoder = LabelEncoder()
        y_encoded = label_encoder.fit_transform(y_train)
        
        grid_search = GridSearchCV(
            SVC(random_state=self.random_state, probability=True),
            param_grid,
            cv=cv,
            scoring='f1_weighted',
            n_jobs=-1,
            verbose=2
        )
        
        grid_search.fit(X_train, y_encoded)
        
        self.best_model = grid_search.best_estimator_
        self.best_params = grid_search.best_params_
        self.tuning_results = {
            'best_params': grid_search.best_params_,
            'best_score': grid_search.best_score_,
            'cv_results': grid_search.cv_results_
        }
        
        self.logger.info(f"Best parameters: {self.best_params}")
        self.logger.info(f"Best CV score: {grid_search.best_score_:.4f}")
        
        return self.best_model, self.tuning_results
    
    def randomized_search_tuning(self, X_train, y_train: pd.Series,
                                n_iter: int = 50, cv: int = 5) -> Tuple[SVC, Dict[str, Any]]:
        """
        Randomized search for faster tuning with large parameter space
        """
        param_dist = {
            'C': np.logspace(-2, 3, 20),
            'kernel': ['linear', 'rbf', 'poly'],
            'gamma': np.logspace(-4, 1, 20),
            'degree': [2, 3, 4],
            'class_weight': ['balanced', None]
        }
        
        self.logger.info(f"Starting randomized search with {n_iter} iterations...")
        
        label_encoder = LabelEncoder()
        y_encoded = label_encoder.fit_transform(y_train)
        
        random_search = RandomizedSearchCV(
            SVC(random_state=self.random_state, probability=True),
            param_dist,
            n_iter=n_iter,
            cv=cv,
            scoring='f1_weighted',
            n_jobs=-1,
            random_state=self.random_state,
            verbose=2
        )
        
        random_search.fit(X_train, y_encoded)
        
        self.best_model = random_search.best_estimator_
        self.best_params = random_search.best_params_
        self.tuning_results = {
            'best_params': random_search.best_params_,
            'best_score': random_search.best_score_,
            'cv_results': random_search.cv_results_
        }
        
        self.logger.info(f"Best parameters: {self.best_params}")
        self.logger.info(f"Best CV score: {random_search.best_score_:.4f}")
        
        return self.best_model, self.tuning_results
    
    def get_tuning_summary(self) -> Dict[str, Any]:
        """Get summary of tuning results"""
        if self.tuning_results is None:
            raise ValueError("No tuning results available")
        
        cv_results = self.tuning_results['cv_results']
        
        summary = {
            'best_params': self.best_params,
            'best_score': self.tuning_results['best_score'],
            'mean_test_score': cv_results['mean_test_score'].max(),
            'std_test_score': cv_results['std_test_score'][np.argmax(cv_results['mean_test_score'])],
            'total_iterations': len(cv_results['mean_test_score'])
        }
        
        return summary
