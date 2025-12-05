"""
Feature Extraction Module for Sentiment Analysis

This module handles TF-IDF vectorization and feature selection
for the sentiment analysis model.
"""

import pickle
import logging
from typing import Tuple, Optional, Any
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.base import BaseEstimator, TransformerMixin

class FeatureExtractor(BaseEstimator, TransformerMixin):
    """
    TF-IDF Feature Extractor wrapper
    """
    
    def __init__(self, 
                 max_features: int = 5000, 
                 ngram_range: Tuple[int, int] = (1, 2),
                 min_df: int = 2,
                 max_df: float = 0.95):
        """
        Initialize Feature Extractor
        
        Args:
            max_features (int): Maximum number of features
            ngram_range (Tuple[int, int]): Range for n-grams
            min_df (int): Minimum document frequency
            max_df (float): Maximum document frequency
        """
        self.logger = self._setup_logger()
        self.max_features = max_features
        self.ngram_range = ngram_range
        self.min_df = min_df
        self.max_df = max_df
        
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            min_df=min_df,
            max_df=max_df,
            sublinear_tf=True  # Apply sublinear tf scaling
        )
        
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

    def fit(self, X: pd.Series, y: Optional[pd.Series] = None) -> 'FeatureExtractor':
        """
        Fit the vectorizer to the data
        
        Args:
            X (pd.Series): Text data
            y (pd.Series, optional): Target labels
            
        Returns:
            self
        """
        self.logger.info(f"Fitting vectorizer on {len(X)} documents...")
        self.vectorizer.fit(X)
        self.logger.info(f"Vocabulary size: {len(self.vectorizer.vocabulary_)}")
        return self

    def transform(self, X: pd.Series) -> Any:
        """
        Transform data to TF-IDF matrix
        
        Args:
            X (pd.Series): Text data
            
        Returns:
            Sparse matrix of TF-IDF features
        """
        self.logger.info(f"Transforming {len(X)} documents...")
        return self.vectorizer.transform(X)

    def fit_transform(self, X: pd.Series, y: Optional[pd.Series] = None) -> Any:
        """
        Fit and transform data
        
        Args:
            X (pd.Series): Text data
            y (pd.Series, optional): Target labels
            
        Returns:
            Sparse matrix of TF-IDF features
        """
        return self.fit(X, y).transform(X)
    
    def save(self, filepath: str):
        """
        Save the feature extractor to a file
        
        Args:
            filepath (str): Path to save the file
        """
        try:
            with open(filepath, 'wb') as f:
                pickle.dump(self, f)
            self.logger.info(f"Feature extractor saved to {filepath}")
        except Exception as e:
            self.logger.error(f"Error saving feature extractor: {e}")

    @staticmethod
    def load(filepath: str) -> 'FeatureExtractor':
        """
        Load a feature extractor from a file
        
        Args:
            filepath (str): Path to load the file from
            
        Returns:
            FeatureExtractor: Loaded instance
        """
        try:
            with open(filepath, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            logging.getLogger(__name__).error(f"Error loading feature extractor: {e}")
            raise e
