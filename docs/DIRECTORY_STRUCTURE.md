# Directory Structure - Clean & Organized

## 📁 Project Structure

```
DM/
├── 📄 Main Files
│   ├── requirements.txt                # Dependencies
│   └── README.md                       # Project overview
│
├── 📚 Documentation (Start Here!)
│   ├── START_HERE.md                   # Quick start guide
│   ├── QUICK_START_IMPROVEMENTS.md     # Setup instructions
│   ├── IMPROVEMENTS_GUIDE.md           # Detailed guide
│   ├── IMPROVEMENTS_SUMMARY.md         # Summary
│   ├── IMPROVEMENTS_INDEX.md           # Complete index
│   ├── IMPROVEMENTS_COMPLETE.txt       # Status report
│   ├── IMPLEMENTATION_CHECKLIST.md     # Deployment checklist
│   └── DIRECTORY_STRUCTURE.md          # This file
│
├── 📂 src/ (Source Code)
│   ├── preprocessing/
│   │   ├── emoji_handler.py            # Emoji conversion
│   │   ├── negation_handler.py         # Negation handling
│   │   ├── enhanced_preprocessor.py    # Full pipeline
│   │   ├── text_cleaner.py             # Text cleaning
│   │   ├── tokenizer.py                # Tokenization
│   │   ├── normalizer.py               # Normalization
│   │   ├── sentiment_labeler.py        # Labeling
│   │   ├── build_dataset.py            # Dataset builder
│   │   └── build_optimized_dataset.py  # Optimized builder
│   │
│   ├── modeling/
│   │   ├── svm_tuner.py                # SVM hyperparameter tuning
│   │   ├── error_analyzer.py           # Error analysis
│   │   ├── model_versioning.py         # Version management
│   │   ├── train_improved_svm.py       # Improved training
│   │   ├── svm_model.py                # SVM model class
│   │   ├── features.py                 # Feature extraction
│   │   ├── evaluation.py               # Evaluation metrics
│   │   ├── train_model.py              # Training script
│   │   ├── train_hybrid_classifier.py  # Hybrid classifier
│   │   └── apply_hybrid_classifier.py  # Apply classifier
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── inference_api.py            # FastAPI endpoint
│   │
│   ├── monitoring/
│   │   ├── __init__.py
│   │   └── drift_detector.py           # Drift detection
│   │
│   ├── scraper/
│   │   ├── comment_scraper.py          # YouTube scraper
│   │   ├── youtube_search.py           # Search functionality
│   │   └── api_manager.py              # API management
│   │
│   ├── pipeline/
│   │   ├── data_collection.py          # Data collection
│   │   └── train_model.py              # Training pipeline
│   │
│   ├── visualization/
│   │   └── dashboard-next/             # Next.js Dashboard
│   │
│   ├── analysis/
│   │   ├── football_emotion_classifier.py  # Emotion classifier
│   │   └── analyze_unknown_keywords.py     # Keyword analysis
│   │
│   └── __init__.py
│
├── 📂 config/ (Configuration)
│   ├── sentiment_config.py             # Sentiment config
│   ├── sentiment_config_v2_optimized.py # Optimized config
│   ├── dashboard_config.py             # Dashboard config
│   ├── api_config.py                   # API config
│   └── __init__.py
│
├── 📂 data/ (Data Storage)
│   ├── raw/                            # Raw data from YouTube
│   │   ├── videos.json
│   │   ├── videos.csv
│   │   ├── comments.csv
│   │   ├── collection_summary.json
│   │   ├── expanded_run/
│   │   ├── test_run/
│   │   └── full_run/
│   │
│   ├── processed/                      # Processed data
│   │   ├── optimized_clean_comments_v6_emotion.csv
│   │   ├── optimized_clean_comments_v5_hybrid.csv
│   │   ├── optimized_clean_comments_v4_phrases.csv
│   │   ├── optimized_clean_comments_v3_stemmed.csv
│   │   ├── optimized_clean_comments_v2.csv
│   │   ├── optimized_clean_comments.csv
│   │   ├── clean_comments.csv
│   │   └── *.summary.json
│   │
│   ├── models/                         # Trained models
│   │   ├── svm_model.pkl
│   │   ├── feature_extractor.pkl
│   │   ├── label_encoder.pkl
│   │   ├── training_summary.json
│   │   ├── evaluation_results.json
│   │   ├── versions/                   # Model versions
│   │   └── hybrid/                     # Hybrid models
│   │
│   └── quota_usage.json
│
├── 📂 docs/ (Documentation)
│   └── IMPROVEMENTS_GUIDE.md           # Improvements guide
│
├── 📂 config/ (Configuration)
│   └── (config files)
│
└── 📂 .venv/ (Virtual Environment)
    └── (Python packages)
```

## 🎯 Quick Navigation

### For Getting Started
- **START_HERE.md** - Begin here!
- **QUICK_START_IMPROVEMENTS.md** - Setup guide

### For Learning
- **IMPROVEMENTS_GUIDE.md** - Complete reference
- **IMPROVEMENTS_SUMMARY.md** - Overview

### For Deployment
- **IMPLEMENTATION_CHECKLIST.md** - Deployment steps

### For Reference
- **IMPROVEMENTS_INDEX.md** - Complete index
- **IMPROVEMENTS_COMPLETE.txt** - Status report

## 📊 Key Directories

### src/
All source code organized by functionality:
- **preprocessing/** - Text processing
- **modeling/** - ML models
- **api/** - API endpoints
- **monitoring/** - Monitoring tools
- **scraper/** - Data collection
- **pipeline/** - Pipelines
- **visualization/** - Charts
- **analysis/** - Analysis tools

### data/
All data organized by stage:
- **raw/** - Raw YouTube data
- **processed/** - Cleaned data
- **models/** - Trained models

### config/
Configuration files for different components

### docs/
Documentation and guides

## 🧹 Cleanup Done

✅ Removed:
- Old dashboard files (9 files)
- Old documentation (20+ files)
- Archive folder
- Cache files (__pycache__)
- Temporary files

✅ Kept:
- Essential source code
- Current documentation
- Configuration files
- Data files
- Models

## 📈 File Count

- **Total files**: ~105
- **Python modules**: ~30
- **Documentation**: ~10
- **Data files**: ~20
- **Config files**: ~5

## 🚀 Usage

### Run Dashboard
```bash
cd dashboard-next
npm run dev
```

### Run Training
```bash
python -m src.modeling.train_improved_svm \
  --input data/processed/clean_comments.csv \
  --output-dir data/models
```

### Start API
```bash
python -m uvicorn src.api.inference_api:app --reload
```

## ✅ Status

- ✅ Clean directory structure
- ✅ Organized by functionality
- ✅ Removed unnecessary files
- ✅ Clear documentation
- ✅ Ready for production

---

**Last Updated**: 2025-12-02
**Status**: Clean & Organized
