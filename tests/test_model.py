"""Test suite for sentiment analysis model."""
import pytest
import pandas as pd
import pickle
import os

# Test data loading
def test_data_exists():
    """Test if processed data file exists."""
    assert os.path.exists("data/processed/comments_clean_final.csv"), "Data file not found"

def test_data_structure():
    """Test if data has required columns."""
    df = pd.read_csv("data/processed/comments_clean_final.csv")
    required_cols = ['clean_text', 'sentiment_label', 'confidence']
    for col in required_cols:
        assert col in df.columns, f"Missing column: {col}"

def test_data_not_empty():
    """Test if dataset is not empty."""
    df = pd.read_csv("data/processed/comments_clean_final.csv")
    assert len(df) > 0, "Dataset is empty"
    assert len(df) >= 8000, f"Dataset too small: {len(df)} rows"

def test_no_missing_values():
    """Test for missing values in critical columns."""
    df = pd.read_csv("data/processed/comments_clean_final.csv")
    assert df['clean_text'].notna().all(), "Missing values in clean_text"
    assert df['sentiment_label'].notna().all(), "Missing values in sentiment_label"

def test_confidence_range():
    """Test if confidence scores are in valid range."""
    df = pd.read_csv("data/processed/comments_clean_final.csv")
    assert (df['confidence'] >= 0).all(), "Confidence < 0 found"
    assert (df['confidence'] <= 1).all(), "Confidence > 1 found"

# Test model
def test_model_exists():
    """Test if trained model exists."""
    assert os.path.exists("data/models/svm_best_regularized.pkl"), "Model file not found"

def test_model_loads():
    """Test if model can be loaded."""
    try:
        with open("data/models/svm_best_regularized.pkl", "rb") as f:
            model = pickle.load(f)
        assert model is not None
    except Exception as e:
        pytest.fail(f"Model loading failed: {e}")

def test_model_prediction():
    """Test if model can make predictions."""
    with open("data/models/svm_best_regularized.pkl", "rb") as f:
        model = pickle.load(f)
    
    test_texts = [
        "Timnas Indonesia hebat sekali",
        "PSSI gagal total",
        "Semoga lolos piala dunia"
    ]
    
    try:
        predictions = model.predict(test_texts)
        assert len(predictions) == len(test_texts)
    except Exception as e:
        pytest.fail(f"Prediction failed: {e}")

def test_sentiment_labels():
    """Test if sentiment labels are valid."""
    df = pd.read_csv("data/processed/comments_clean_final.csv")
    valid_labels = df['sentiment_label'].unique()
    assert len(valid_labels) > 0, "No sentiment labels found"
    assert 'unknown' not in valid_labels or (df['sentiment_label'] == 'unknown').sum() == 0

# Test preprocessing
def test_text_cleaning():
    """Test text cleaning function."""
    from src.preprocessing.text_cleaner import clean_text
    
    dirty_text = "Timnas!!! 123 @user #hashtag http://link.com"
    clean = clean_text(dirty_text)
    
    assert len(clean) > 0, "Cleaned text is empty"
    assert "http" not in clean, "URL not removed"
    assert "@" not in clean, "Mention not removed"
    assert "#" not in clean, "Hashtag not removed"

def test_tokenization():
    """Test tokenization."""
    import json
    df = pd.read_csv("data/processed/comments_clean_final.csv")
    
    # Check if tokens column exists and is valid
    if 'tokens' in df.columns:
        sample = df['tokens'].iloc[0]
        tokens = json.loads(sample) if isinstance(sample, str) else sample
        assert isinstance(tokens, list), "Tokens should be a list"

# Performance tests
def test_model_accuracy():
    """Test if model meets minimum accuracy threshold."""
    import json
    
    with open("data/models/best_regularization_results.json", "r") as f:
        results = json.load(f)
    
    accuracy = results.get('test_accuracy', 0)
    assert accuracy >= 0.65, f"Accuracy too low: {accuracy:.2%}"

def test_confidence_threshold():
    """Test if average confidence meets threshold."""
    df = pd.read_csv("data/processed/comments_clean_final.csv")
    avg_conf = df['confidence'].mean()
    assert avg_conf >= 0.70, f"Average confidence too low: {avg_conf:.2%}"

# Integration tests
def test_end_to_end_pipeline():
    """Test complete pipeline from text to prediction."""
    with open("data/models/svm_best_regularized.pkl", "rb") as f:
        model = pickle.load(f)
    
    # Test text
    text = "Indonesia gagal lolos piala dunia"
    
    # Should not raise exception
    try:
        prediction = model.predict([text])
        assert prediction is not None
        assert len(prediction) > 0
    except Exception as e:
        pytest.fail(f"End-to-end pipeline failed: {e}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
