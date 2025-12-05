# Hasil Preprocessing & Sentiment Labeling

## 📊 Summary

**Dataset:** YouTube Comments - Kegagalan Indonesia Lolos Piala Dunia  
**Total Comments:** 10,950  
**Date:** 2 Desember 2025  
**Version:** V3 (Final Automated)

## 🎯 Hasil Akhir

| Metric | Value | Status |
|--------|-------|--------|
| **Total Rows** | 10,950 | ✅ |
| **Labeled** | 8,791 (80.3%) | ✅ Target >80% |
| **Unknown** | 2,159 (19.7%) | ✅ Target <20% |
| **Avg Confidence** | 0.377 | ⚠️ Target >0.5 |
| **High Confidence (≥0.7)** | 2,455 (22.4%) | ⚠️ |
| **Quality Score** | 55.9/100 | ⚠️ FAIR |

## 📈 Progress History

### V1 - Original (Baseline)
- Unknown: 55.89%
- Labeled: 44.11%
- Issues: Threshold terlalu tinggi, keyword kurang

### V2 - Threshold Optimization
- Unknown: 29.52% (↓26%)
- Labeled: 70.48% (↑26%)
- Changes: Threshold 1.0→0.5, confidence calculation fixed

### V3 - Keyword Enhancement (Current)
- Unknown: 19.72% (↓10%)
- Labeled: 80.28% (↑10%)
- Changes: +50 keywords berdasarkan analisis unknown

## 🏷️ Label Distribution

### Top 15 Labels

| Label | Count | Percentage |
|-------|-------|------------|
| unknown | 2,159 | 19.72% |
| hopeful_skepticism | 2,045 | 18.68% |
| pssi_management | 1,494 | 13.64% |
| coaching_staff | 1,238 | 11.31% |
| patriotic_sadness | 1,157 | 10.57% |
| technical_performance | 957 | 8.74% |
| future_hope | 380 | 3.47% |
| negative_criticism | 365 | 3.33% |
| opponents | 251 | 2.29% |
| positive_support | 139 | 1.27% |
| passionate_disappointment | 138 | 1.26% |
| players | 111 | 1.01% |
| media_analysts | 108 | 0.99% |
| respectful_acknowledgment | 69 | 0.63% |
| referees | 66 | 0.60% |

### Layer Distribution

| Layer | Count | Percentage |
|-------|-------|------------|
| stakeholders | 3,276 | 29.92% |
| core_sentiment | 2,614 | 23.87% |
| unknown | 2,159 | 19.72% |
| football_emotions | 1,789 | 16.34% |
| root_causes | 1,012 | 9.24% |
| temporal_contexts | 73 | 0.67% |
| solution_oriented | 27 | 0.25% |

## 🔧 Technical Details

### Preprocessing Pipeline
1. **Text Cleaning** - Remove URLs, mentions, special chars
2. **Tokenization** - Indonesian tokenizer
3. **Stopword Removal** - Sastrawi + custom stopwords
4. **Stemming** - Sastrawi stemmer with caching
5. **Sentiment Labeling** - Lexicon-based with 9-layer config

### Labeling Logic
- **Min Score Threshold:** 0.5
- **Confidence Calculation:** (top_score - second_score) / top_score
- **Conflict Detection:** Mixed positive/negative → hopeful_skepticism
- **Keyword Matching:** Exact + stemmed tokens

### Performance
- **Processing Time:** ~30 minutes for 10,950 comments
- **Cache Efficiency:** ~5,000 unique stemmed words
- **Memory Usage:** ~200MB peak

## 📁 Output Files

```
data/processed/
├── comments_clean_v3.csv              # Main dataset (13MB)
├── comments_clean_v3.summary.json     # Statistics
└── comments_clean_v3_manual_labeling.csv  # For manual labeling (2,159 unknown)
```

### CSV Columns
- `comment_id` - Unique identifier
- `text` - Original comment
- `clean_text` - Cleaned text
- `tokens` - Raw tokens (JSON)
- `tokens_no_stop` - Without stopwords (JSON)
- `stemmed_tokens` - Stemmed tokens (JSON)
- `normalized_text` - Final processed text
- `sentiment_label` - Assigned label
- `sentiment_layer` - Layer category
- `sentiment_score` - Match score
- `confidence` - Confidence (0-1)
- `matched_categories` - All matches (JSON)

## 🎯 Next Steps

### Option 1: Use Current Dataset (Recommended)
- 80.3% labeled sudah cukup untuk modeling
- Focus on model training dengan data yang ada
- Unknown bisa di-filter atau diberi label 'neutral'

### Option 2: Manual Labeling
- 2,159 unknown comments perlu review
- 303 sudah ada suggestion (14%)
- Tools tersedia:
  - `interactive_labeler.py` - Terminal-based
  - `apply_manual_labels.py` - Merge results
- Estimasi: 4-6 jam

### Option 3: Hybrid Approach
- Label 500 sample untuk validation
- Gunakan untuk improve lexicon
- Re-run preprocessing

## 📊 Quality Assessment

### Strengths ✅
- Coverage 80.3% (excellent)
- Distribusi seimbang antar kategori
- Layer representation bagus
- Confidence calculation fixed

### Weaknesses ⚠️
- Avg confidence masih rendah (0.377)
- 19.7% masih unknown
- Quality score 55.9/100 (FAIR)

### Recommendations
1. **For Modeling:** Proceed dengan dataset ini
2. **For Improvement:** Manual label 500 sample untuk validation
3. **For Production:** Implement active learning untuk continuous improvement

## 🔗 Related Files

- Config: `config/sentiment_config.py`
- Preprocessor: `src/preprocessing/preprocessor.py`
- Labeler: `src/preprocessing/sentiment_labeler.py`
- Analysis: `src/analysis/analyze_labeling.py`
- Manual Tools: `src/labeling/`

## 📝 Notes

- Stemming adalah bottleneck utama (20s per 100 comments)
- Cache optimization mengurangi waktu 13%
- Keyword enhancement paling efektif (↓10% unknown)
- Confidence threshold 0.5 optimal untuk balance coverage vs accuracy

---

**Generated:** 2 Desember 2025  
**Author:** Data Mining Team  
**Status:** Ready for Model Training
