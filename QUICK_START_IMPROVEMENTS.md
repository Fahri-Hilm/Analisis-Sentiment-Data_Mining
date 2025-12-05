# Quick Start - Project Improvements

## 1️⃣ Install Dependencies
```bash
pip install -r requirements_improvements.txt
```

## 2️⃣ Run Improved Training
```bash
python -m src.modeling.train_improved_svm \
  --input data/processed/clean_comments.csv \
  --output-dir data/models \
  --test-size 0.2
```

**Output**:
- Trained SVM model dengan hyperparameter tuning
- Feature extractor dengan n-grams (1-3)
- Error analysis report
- Model metrics dan evaluation

## 3️⃣ Start API Server
```bash
python -m uvicorn src.api.inference_api:app --reload
```

**Server**: http://localhost:8000

## 4️⃣ Test API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Single Prediction
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Indonesia bagus!"}'
```

### Batch Prediction
```bash
curl -X POST http://localhost:8000/predict-batch \
  -H "Content-Type: application/json" \
  -d '{
    "texts": [
      "Indonesia bagus!",
      "Tidak bagus",
      "Sedih sekali"
    ]
  }'
```

### Model Info
```bash
curl http://localhost:8000/model-info
```

## 5️⃣ Use Improvements in Code

### Enhanced Preprocessing
```python
from src.preprocessing.enhanced_preprocessor import EnhancedPreprocessor

preprocessor = EnhancedPreprocessor()
text = "Tidak bagus! 😡 :("
cleaned = preprocessor.preprocess(text)
print(cleaned)  # NEG NEG_bagus api sedih
```

### Error Analysis
```python
from src.modeling.error_analyzer import ErrorAnalyzer

analyzer = ErrorAnalyzer()
errors = analyzer.analyze_errors(y_true, y_pred, texts)
print(f"Error rate: {errors['error_rate']:.2%}")
print(f"Total errors: {errors['total_errors']}")
```

### Model Versioning
```python
from src.modeling.model_versioning import ModelVersionManager

manager = ModelVersionManager()

# Save version
manager.save_version(model, fe, le, metrics, config, 'v_001')

# List versions
versions = manager.list_versions()
for v in versions:
    print(f"{v['name']}: {v['metrics']}")

# Load best version
best = manager.get_best_version('accuracy')
model, fe, le, metadata = manager.load_version(best['name'])
```

### Drift Detection
```python
from src.monitoring.drift_detector import DriftDetector

baseline = {'accuracy': 0.85, 'f1_score': 0.83}
detector = DriftDetector(baseline)

drift = detector.detect_performance_drift(y_true, y_pred, threshold=0.05)
if drift['has_drift']:
    print(f"⚠️ Drift detected! Accuracy drop: {drift['accuracy_drift']:.4f}")
else:
    print("✅ No drift detected")
```

## 📊 Key Improvements

| Feature | Benefit |
|---------|---------|
| Emoji Handling | Better sentiment capture |
| Negation Handling | Context preservation |
| N-grams (1-3) | Better feature representation |
| Hyperparameter Tuning | Optimized model |
| Error Analysis | Understand misclassifications |
| Model Versioning | Track experiments |
| API Endpoint | Production deployment |
| Drift Detection | Monitor model health |

## 📁 New Modules

```
src/preprocessing/
  ├── emoji_handler.py          # Emoji/emoticon conversion
  ├── negation_handler.py       # Negation/intensifier handling
  └── enhanced_preprocessor.py  # Full pipeline

src/modeling/
  ├── svm_tuner.py              # Grid/Randomized search
  ├── error_analyzer.py         # Error breakdown
  ├── model_versioning.py       # Version management
  └── train_improved_svm.py     # Improved training

src/api/
  └── inference_api.py          # FastAPI endpoint

src/monitoring/
  └── drift_detector.py         # Drift detection
```

## 🎯 Expected Results

After running improved training:
- ✅ Accuracy: +2-5% improvement
- ✅ F1-Score: +3-7% improvement
- ✅ Better feature extraction dengan n-grams
- ✅ Detailed error analysis
- ✅ Model versioning untuk tracking
- ✅ Production-ready API

## 🔍 Monitoring

Check model performance:
```python
from src.monitoring.drift_detector import DriftDetector

detector = DriftDetector(baseline_metrics)

# Check performance drift
drift = detector.detect_performance_drift(y_true, y_pred)

# Check data drift
data_drift = detector.detect_data_drift(X_baseline, X_current)

# Get summary
summary = detector.get_drift_summary()
print(summary)
```

## 📚 Documentation

- **IMPROVEMENTS_GUIDE.md** - Detailed guide untuk semua improvements
- **IMPROVEMENTS_SUMMARY.md** - Complete summary
- **QUICK_START_IMPROVEMENTS.md** - This file

## ⚡ Performance Tips

1. **Faster Training**: Use randomized search instead of grid search
   ```python
   tuner.randomized_search_tuning(X_train, y_train, n_iter=50)
   ```

2. **Batch Processing**: Use batch prediction untuk efficiency
   ```bash
   curl -X POST http://localhost:8000/predict-batch ...
   ```

3. **Model Caching**: API automatically caches model on startup

4. **N-grams Tuning**: Adjust ngram_range untuk balance
   ```python
   FeatureExtractor(ngram_range=(1, 2))  # Faster
   FeatureExtractor(ngram_range=(1, 3))  # Better features
   ```

## 🐛 Troubleshooting

**Issue**: Model loading error
```python
# Check model path
import os
print(os.path.exists("data/models/svm_model.pkl"))
```

**Issue**: API not starting
```bash
# Check port availability
lsof -i :8000
```

**Issue**: Low accuracy
```python
# Check error analysis
analyzer = ErrorAnalyzer()
errors = analyzer.analyze_errors(y_true, y_pred)
print(errors['error_samples'][:5])
```

## 🚀 Next Steps

1. ✅ Install dependencies
2. ✅ Run improved training
3. ✅ Start API server
4. ✅ Test endpoints
5. ✅ Monitor drift
6. ✅ Iterate & improve

---

**Ready to go!** 🎉
