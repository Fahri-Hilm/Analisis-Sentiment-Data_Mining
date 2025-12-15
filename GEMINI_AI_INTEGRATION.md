# 🤖 Gemini AI Sentiment Analysis Integration

Dashboard sekarang menggunakan **Google Gemini AI** untuk analisis sentiment real-time yang lebih akurat dan pintar!

## ✨ Features

- **Real-time AI Analysis** - Analisis sentiment menggunakan Gemini 2.5 Flash
- **Indonesian Language Optimized** - Dioptimalkan untuk bahasa Indonesia
- **Contextual Understanding** - AI memahami konteks dan nuansa
- **Reasoning Provided** - AI memberikan alasan analisisnya
- **Fallback System** - Sistem cadangan jika AI tidak tersedia

## 🚀 Quick Start

### 1. Jalankan Gemini AI API
```bash
cd /path/to/project
python run_gemini_api.py
```

API akan berjalan di: **http://localhost:8000**

### 2. Jalankan Dashboard
```bash
cd dashboard-next
npm run dev
```

Dashboard akan berjalan di: **http://localhost:3000**

### 3. Test Live Comments dengan AI
Buka: **http://localhost:3000/live-comments**

URL dengan sentiment analysis:
```
http://localhost:3000/api/live-comments?videoId=VIDEO_ID&sentiment=true
```

## 📊 API Endpoints

### Gemini AI Sentiment Analysis
```bash
# Single text analysis
POST http://localhost:8000/predict
{
  "text": "Produk ini sangat bagus dan berkualitas!"
}

# Batch analysis
POST http://localhost:8000/predict-batch
{
  "texts": ["Comment 1", "Comment 2", "Comment 3"]
}

# Model info
GET http://localhost:8000/model-info

# Test endpoint
GET http://localhost:8000/test
```

### Dashboard API Integration
```bash
# Gemini sentiment via dashboard
POST http://localhost:3000/api/gemini-sentiment
{
  "text": "Your comment here"
}

# Live comments with sentiment
GET http://localhost:3000/api/live-comments?sentiment=true&videoId=VIDEO_ID
```

## 🧪 Testing

### Test Gemini AI Model
```bash
python -c "
import sys
sys.path.append('src')
from modeling.gemini_sentiment import GeminiSentimentAnalyzer

analyzer = GeminiSentimentAnalyzer('YOUR_API_KEY')
result = analyzer.analyze_sentiment('Produk ini sangat bagus!')
print(result)
"
```

### Test API Endpoints
```bash
# Health check
curl http://localhost:8000/health

# Test prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Sangat puas dengan produk ini!"}'

# Test dashboard integration
curl -X POST http://localhost:3000/api/gemini-sentiment \
  -H "Content-Type: application/json" \
  -d '{"text": "Pelayanan mengecewakan sekali"}'
```

## 📈 Results Comparison

### Before (Rule-based)
```json
{
  "sentiment": "neutral",
  "confidence": 0.5
}
```

### After (Gemini AI)
```json
{
  "sentiment": "positive",
  "confidence": 0.95,
  "reasoning": "Komentar menggunakan kata-kata positif seperti 'sangat bagus' dan 'berkualitas'"
}
```

## 🔧 Configuration

### API Key
API key Gemini sudah dikonfigurasi di:
- `src/modeling/gemini_sentiment.py`
- `src/api/inference_api.py`

### Model Settings
- **Model**: `gemini-2.5-flash`
- **Rate Limit**: 1 request/second untuk batch
- **Timeout**: 5 seconds
- **Fallback**: Rule-based analysis

## 🎯 Live Dashboard Integration

### Real-time Comments Analysis
1. Buka **Live Comments** page
2. Masukkan YouTube Video ID
3. Enable "Analyze Sentiment" 
4. Lihat hasil analisis AI real-time

### Features di Dashboard:
- ✅ Real-time sentiment analysis
- ✅ AI reasoning display
- ✅ Confidence scores
- ✅ Sentiment distribution charts
- ✅ Fallback system
- ✅ Model information

## 🚨 Troubleshooting

### Gemini API Error
```bash
# Check if API is running
curl http://localhost:8000/health

# Restart API
python run_gemini_api.py
```

### Dashboard Integration Issues
```bash
# Check dashboard API
curl http://localhost:3000/api/gemini-sentiment

# Check live comments
curl "http://localhost:3000/api/live-comments?sentiment=true"
```

### Fallback System
Jika Gemini AI tidak tersedia, sistem akan otomatis menggunakan rule-based analysis sebagai backup.

## 📊 Performance

- **Accuracy**: Very High (AI-powered)
- **Speed**: ~1-2 seconds per comment
- **Languages**: Indonesian + English
- **Reliability**: High (with fallback)

## 🎉 Success!

Sekarang dashboard Anda menggunakan AI terdepan untuk analisis sentiment yang lebih akurat dan contextual! 

**Live Comments** akan menampilkan:
- Sentiment: positive/negative/neutral
- Confidence: 0.0 - 1.0
- AI Reasoning: Penjelasan mengapa AI memberikan label tersebut
- Model: Gemini AI atau Fallback
