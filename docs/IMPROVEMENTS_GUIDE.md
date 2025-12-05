# SVM Project Improvements Guide

## Overview
Comprehensive improvements untuk project Analisis Sentimen YouTube dengan fokus pada SVM model optimization.

## 1. Text Processing Enhancements

### Emoji & Emoticon Handling
**File**: `src/preprocessing/emoji_handler.py`

Mengkonversi emoji dan emoticon ke text representation:
```python
from src.preprocessing.emoji_handler import process_emoji_emoticon

text = "Bagus! 😍 :)"
processed = process_emoji_emoticon(text)
# Output: "Bagus! cinta senang"
```

**Features**:
- 15+ emoji mappings
- Emoticon conversion
- Repeated character handling

### Negation & Intensifier Handling
**File**: `src/preprocessing/negation_handler.py`

Preserve context dengan negation markers:
```python
from src.preprocessing.negation_handler import process_negation_intensifiers

text = "tidak bagus"
processed = process_negation_intensifiers(text)
# Output: "NEG NEG_bagus"
```

**Features**:
- Negation prefix (NEG_)
- Intensifier marking (INTENS_)
- Context preservation

### Enhanced Preprocessor
**File**: `src/preprocessing/enhanced_preprocessor.py`

Full pipeline dengan semua improvements:
```python
from src.preprocessing.enhanced_preprocessor import EnhancedPreprocessor

preprocessor = EnhancedPreprocessor()
text = "Tidak bagus! 😡 :("
cleaned = preprocessor.preprocess(text)
```

## 2. SVM Model Improvements

### Advanced Hyperparameter Tuning
**File**: `src/modeling/svm_tuner.py`

Dua metode tuning:

**Grid Search** (comprehensive):
```python
from src.modeling.svm_tuner import SVMTuner

tuner = SVMTuner()
model, results = tuner.grid_search_tuning(X_train, y_train, cv=5)
```

**Randomized Search** (faster):
```python
model, results = tuner.randomized_search_tuning(X_train, y_train, n_iter=50)
```

**Parameter Space**:
- C: [0.1, 1, 10, 100, 1000]
- kernel: ['linear', 'rbf', 'poly']
- gamma: ['scale', 'auto', 0.001, 0.01, 0.1]
- degree: [2, 3, 4]
- class_weight: ['balanced', None]

### Error Analysis
**File**: `src/modeling/error_analyzer.py`

Analyze misclassifications:
```python
from src.modeling.error_analyzer import ErrorAnalyzer

analyzer = ErrorAnalyzer()
error_analysis = analyzer.analyze_errors(y_true, y_pred, texts)
per_class_errors = analyzer.get_per_class_errors(y_true, y_pred, class_names)
hard_samples = analyzer.identify_hard_samples(y_true, y_pred, y_proba)
```

**Outputs**:
- Total error count & rate
- Per-class precision/recall/F1
- Hard samples (low confidence)
- Sample-level error details

### Model Versioning
**File**: `src/modeling/model_versioning.py`

Track experiments:
```python
from src.modeling.model_versioning import ModelVersionManager

manager = ModelVersionManager()
version_path = manager.save_version(
    model, feature_extractor, label_encoder,
    metrics={'accuracy': 0.85},
    config={'kernel': 'rbf'},
    version_name='v_20231201_001'
)

# Load version
model, fe, le, metadata = manager.load_version('v_20231201_001')

# List all versions
versions = manager.list_versions()

# Get best version
best = manager.get_best_version(metric='accuracy')
```

## 3. API & Deployment

### FastAPI Inference Endpoint
**File**: `src/api/inference_api.py`

Start API:
```bash
python -m uvicorn src.api.inference_api:app --reload
```

**Endpoints**:

1. **Health Check**
```bash
curl http://localhost:8000/health
```

2. **Single Prediction**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Indonesia bagus!"}'
```

3. **Batch Prediction**
```bash
curl -X POST http://localhost:8000/predict-batch \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Text 1", "Text 2"]}'
```

4. **Model Info**
```bash
curl http://localhost:8000/model-info
```

## 4. Monitoring & Drift Detection

### Drift Detection
**File**: `src/monitoring/drift_detector.py`

Monitor model performance:
```python
from src.monitoring.drift_detector import DriftDetector

baseline_metrics = {'accuracy': 0.85, 'f1_score': 0.83}
detector = DriftDetector(baseline_metrics)

# Check performance drift
drift_info = detector.detect_performance_drift(y_true, y_pred, threshold=0.05)

# Check data drift
data_drift = detector.detect_data_drift(X_baseline, X_current)

# Get summary
summary = detector.get_drift_summary()
```

## 5. Improved Training Script

**File**: `src/modeling/train_improved_svm.py`

Run improved training:
```bash
python -m src.modeling.train_improved_svm \
  --input data/processed/clean_comments.csv \
  --output-dir data/models \
  --test-size 0.2
```

**Features**:
- Enhanced preprocessing
- N-grams (1-3)
- Hyperparameter tuning
- Error analysis
- Model versioning
- Comprehensive metrics

## 6. Usage Examples

### Complete Pipeline
```python
from src.preprocessing.enhanced_preprocessor import EnhancedPreprocessor
from src.modeling.svm_tuner import SVMTuner
from src.modeling.error_analyzer import ErrorAnalyzer
from src.modeling.model_versioning import ModelVersionManager
from src.monitoring.drift_detector import DriftDetector

# 1. Preprocess
preprocessor = EnhancedPreprocessor()
texts = preprocessor.preprocess_batch(raw_texts)

# 2. Train with tuning
tuner = SVMTuner()
model, results = tuner.grid_search_tuning(X_train, y_train)

# 3. Analyze errors
analyzer = ErrorAnalyzer()
errors = analyzer.analyze_errors(y_true, y_pred)

# 4. Version model
manager = ModelVersionManager()
manager.save_version(model, fe, le, metrics, config)

# 5. Monitor drift
detector = DriftDetector(baseline_metrics)
drift = detector.detect_performance_drift(y_true, y_pred)
```

## 7. Installation

Add new dependencies:
```bash
pip install -r requirements_improvements.txt
```

## 8. Performance Improvements Expected

- **Accuracy**: +2-5% dengan n-grams dan negation handling
- **F1-Score**: +3-7% dengan better feature extraction
- **Hard Samples**: Identified untuk manual review
- **Error Analysis**: Detailed breakdown per class
- **Model Tracking**: Full experiment history

## 9. Next Steps

1. Run improved training script
2. Compare metrics dengan baseline
3. Analyze error patterns
4. Deploy API untuk production
5. Monitor drift regularly
6. Iterate dengan feedback

## 10. File Structure

```
src/
├── preprocessing/
│   ├── emoji_handler.py          # Emoji/emoticon handling
│   ├── negation_handler.py       # Negation/intensifier handling
│   └── enhanced_preprocessor.py  # Full pipeline
├── modeling/
│   ├── svm_tuner.py              # Advanced tuning
│   ├── error_analyzer.py         # Error analysis
│   ├── model_versioning.py       # Version management
│   └── train_improved_svm.py     # Improved training script
├── api/
│   └── inference_api.py          # FastAPI endpoint
└── monitoring/
    └── drift_detector.py         # Drift detection
```

---

**Note**: Semua improvements fokus pada SVM model tanpa ensemble methods.
