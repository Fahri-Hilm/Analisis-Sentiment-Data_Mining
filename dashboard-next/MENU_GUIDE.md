# 🗺️ Menu Navigation Guide - Garuda Dashboard

## 📊 Struktur Menu yang Sudah Diimplementasikan

```
┌─────────────────────────────────────────────────────────────┐
│  🏠 GARUDA - Sentiment Analysis Dashboard                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────┐
│   📊 ANALYSIS       │  ← Menu Utama (Analisis Data)
├─────────────────────┤
│ 📈 Dashboard        │  → Gambaran Umum (Overview)
│ 📊 Sentiment        │  → Analisis Sentimen Detail
│ 😤 Emotions         │  → Analisis Emosi Mendalam
│ 💬 Comments         │  → Browse 19K+ Komentar
│ 🤖 Model            │  → Performa ML Model
└─────────────────────┘

┌─────────────────────┐
│   🛠️ TOOLS          │  ← Menu Sekunder (Utilitas)
├─────────────────────┤
│ ⚡ Live Analyzer    │  → Prediksi Real-time
│ 📁 Dataset          │  → Manajemen Dataset
│ 📖 Documentation    │  → Dokumentasi Teknis
└─────────────────────┘
```

---

## 🎯 Detail Setiap Halaman

### 1️⃣ **Dashboard** - Halaman Utama
**Route:** `/`
**Waktu Baca:** ~30 detik

**Yang Ditampilkan:**
```
┌─────────────────────────────────────────────────────┐
│  📊 Dashboard Overview                              │
│  Gambaran umum analisis sentimen Timnas Indonesia  │
├─────────────────────────────────────────────────────┤
│                                                     │
│  [Total: 19,228]  [Positif: 29.1%]                │
│  [Negatif: 69.8%] [Accuracy: 89.4%]               │
│                                                     │
│  ┌──────────────┐  ┌──────────────┐               │
│  │ Pie Chart    │  │ Top 3 Emosi  │               │
│  │ Sentimen     │  │ - Kekecewaan │               │
│  │ Distribution │  │ - Kemarahan  │               │
│  └──────────────┘  │ - Harapan    │               │
│                    └──────────────┘               │
│                                                     │
│  💡 AI Insights (Key Findings)                     │
└─────────────────────────────────────────────────────┘
```

**Keputusan Design:**
- ✅ Hanya 4 metric cards (tidak overwhelming)
- ✅ 1 pie chart + 1 list (simple & clear)
- ✅ AI Insights untuk highlight otomatis

---

### 2️⃣ **Sentiment Analysis** - Analisis Sentimen
**Route:** `/sentiment`
**Waktu Baca:** ~2-3 menit

**Yang Ditampilkan:**
```
┌─────────────────────────────────────────────────────┐
│  📊 Analisis Sentimen                               │
│  Detail analisis berdasarkan target & konstruktif  │
├─────────────────────────────────────────────────────┤
│                                                     │
│  🎯 Sentimen Berdasarkan Target                    │
│  ┌─────────────────────────────────────────────┐  │
│  │  Bar Chart (Horizontal)                     │  │
│  │  - PSSI: 8,547 komentar                     │  │
│  │  - Pemain: 6,002 komentar                   │  │
│  │  - Pelatih: 2,445 komentar                  │  │
│  └─────────────────────────────────────────────┘  │
│                                                     │
│  ┌──────────────────┐  ┌──────────────────┐       │
│  │ Konstruktivitas  │  │ Distribusi       │       │
│  │ Progress Bars    │  │ Target (Pie)     │       │
│  │ - Konstruktif    │  │                  │       │
│  │ - Non-konstruktif│  │                  │       │
│  └──────────────────┘  └──────────────────┘       │
└─────────────────────────────────────────────────────┘
```

**Layer yang Ditampilkan:**
- ✅ Sentiment by Target (Bar Chart)
- ✅ Constructiveness breakdown
- ✅ Target distribution (Pie Chart)

---

### 3️⃣ **Emotion Insights** - Analisis Emosi
**Route:** `/emotions`
**Waktu Baca:** ~2-3 menit

**Yang Ditampilkan:**
```
┌─────────────────────────────────────────────────────┐
│  😤 Analisis Emosi                                  │
│  Distribusi dan intensitas emosi dalam komentar    │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ❤️ Distribusi Emosi (Horizontal Bar)              │
│  ┌─────────────────────────────────────────────┐  │
│  │  Kekecewaan    ████████████████ 44.5%       │  │
│  │  Kemarahan     ████████████ 31.2%           │  │
│  │  Harapan       ████ 12.7%                   │  │
│  │  Dukungan      ██ 8.2%                      │  │
│  │  Kebanggaan    █ 3.4%                       │  │
│  └─────────────────────────────────────────────┘  │
│                                                     │
│  ┌──────────────────┐  ┌──────────────────┐       │
│  │ Radar Chart      │  │ Emotion Cards    │       │
│  │ Intensitas       │  │ Detail per emosi │       │
│  │ 5 Emosi          │  │ dengan count     │       │
│  └──────────────────┘  └──────────────────┘       │
└─────────────────────────────────────────────────────┘
```

**Layer yang Ditampilkan:**
- ✅ All 5 emotions (Kekecewaan, Kemarahan, Harapan, Dukungan, Kebanggaan)
- ✅ Radar chart untuk intensitas
- ✅ Individual emotion cards dengan detail

---

### 4️⃣ **Comments Explorer** - Browser Komentar
**Route:** `/comments`
**Waktu Baca:** Variable (research tool)

**Yang Ditampilkan:**
```
┌─────────────────────────────────────────────────────┐
│  💬 Comments Explorer                               │
│  Browse dan search 19,228 komentar                 │
├─────────────────────────────────────────────────────┤
│                                                     │
│  🔍 [Search...] [Filter: All] [Sort: Latest]      │
│                                                     │
│  ┌─────────────────────────────────────────────┐  │
│  │ Comment #1                                   │  │
│  │ "Kecewa banget sama performa timnas..."     │  │
│  │ 😤 Kekecewaan | 🔴 Negatif | 🎯 PSSI        │  │
│  └─────────────────────────────────────────────┘  │
│                                                     │
│  ┌─────────────────────────────────────────────┐  │
│  │ Comment #2                                   │  │
│  │ "Semangat terus untuk timnas..."            │  │
│  │ 💪 Dukungan | 🟢 Positif | 🎯 Pemain        │  │
│  └─────────────────────────────────────────────┘  │
│                                                     │
│  [← Prev] Page 1 of 962 [Next →]                  │
└─────────────────────────────────────────────────────┘
```

**Features:**
- ✅ Search by keyword
- ✅ Filter by sentiment/emotion/target
- ✅ Pagination (20 per page)
- ✅ Full label display

---

### 5️⃣ **Model Performance** - Metrik Model
**Route:** `/model`
**Waktu Baca:** ~1-2 menit

**Yang Ditampilkan:**
```
┌─────────────────────────────────────────────────────┐
│  🤖 Model Performance                               │
│  Metrik performa model ML SVM + TF-IDF             │
├─────────────────────────────────────────────────────┤
│                                                     │
│  [Accuracy: 89.4%] [F1: 91%] [Confidence: 92%]    │
│                                                     │
│  📊 Classification Report                          │
│  ┌─────────────────────────────────────────────┐  │
│  │ Class    │ Prec │ Recall │ F1  │ Support   │  │
│  │ Negative │ 0.91 │ 0.95   │ 0.93│ 13,419    │  │
│  │ Positive │ 0.85 │ 0.76   │ 0.80│ 5,597     │  │
│  │ Neutral  │ 0.72 │ 0.58   │ 0.64│ 212       │  │
│  └─────────────────────────────────────────────┘  │
│                                                     │
│  ┌──────────────────┐  ┌──────────────────┐       │
│  │ Model Arch       │  │ Training Details │       │
│  │ - SVM            │  │ - 19K dataset    │       │
│  │ - TF-IDF         │  │ - 5-fold CV      │       │
│  │ - 2K features    │  │ - 80/20 split    │       │
│  └──────────────────┘  └──────────────────┘       │
└─────────────────────────────────────────────────────┘
```

**Layer yang Ditampilkan:**
- ✅ 3 Key metrics (Accuracy, F1, Confidence)
- ✅ Full classification report
- ✅ Model architecture details
- ✅ Training configuration

---

### 6️⃣ **Live Analyzer** - Prediksi Real-time
**Route:** `/analytics`
**Waktu Baca:** Interactive tool

**Yang Ditampilkan:**
```
┌─────────────────────────────────────────────────────┐
│  ⚡ Live Sentiment Analyzer                         │
│  Analisis sentimen komentar secara real-time       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  📝 Input Komentar:                                │
│  ┌─────────────────────────────────────────────┐  │
│  │ Ketik komentar di sini...                   │  │
│  │                                              │  │
│  │                                              │  │
│  └─────────────────────────────────────────────┘  │
│                                                     │
│  [🔍 Analyze]                                      │
│                                                     │
│  📊 Hasil Analisis:                                │
│  ┌─────────────────────────────────────────────┐  │
│  │ Sentimen: 🔴 NEGATIF (85% confidence)       │  │
│  │ Emosi: 😤 Kekecewaan                        │  │
│  │ Target: 🎯 PSSI                             │  │
│  │ Konstruktif: ✅ Ya                          │  │
│  └─────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## 🎨 Visual Hierarchy

### Information Density per Page

```
Dashboard       ████░░░░░░ 40%  (Light - Quick overview)
Sentiment       ██████░░░░ 60%  (Medium - Detailed analysis)
Emotions        ██████░░░░ 60%  (Medium - Detailed analysis)
Comments        ████████░░ 80%  (Heavy - Research tool)
Model           ██████░░░░ 60%  (Medium - Technical metrics)
Live Analyzer   ████░░░░░░ 40%  (Light - Interactive tool)
```

---

## 🚦 User Flow Recommendations

### **Untuk Casual User (5 menit)**
```
Dashboard → Lihat overview → Done ✅
```

### **Untuk Analyst (15 menit)**
```
Dashboard → Sentiment Analysis → Emotion Insights → Done ✅
```

### **Untuk Researcher (30+ menit)**
```
Dashboard → Sentiment → Emotions → Comments Explorer → Model Performance ✅
```

### **Untuk Developer (Technical)**
```
Model Performance → Documentation → Live Analyzer → API Testing ✅
```

---

## 📈 Comparison: Before vs After

### **BEFORE (Old Structure)**
```
┌─────────────────────────────────────┐
│  Dashboard (Single Page)            │
│  ↓                                   │
│  - 4 Metric Cards                   │
│  - Sentiment Pie Chart              │
│  - Emotion Bar Chart                │
│  - Target Bar Chart                 │
│  - Constructiveness Chart           │
│  - Radar Chart                      │
│  - AI Insights                      │
│  - Top Categories                   │
│  - Heatmap                          │
│  - Timeline                         │
│  ↓                                   │
│  [Scroll... scroll... scroll...]    │
│  ↓                                   │
│  [User overwhelmed 😵]              │
└─────────────────────────────────────┘
```

### **AFTER (New Structure)**
```
┌──────────────┐
│  Dashboard   │ → Overview (Clean & Simple)
└──────┬───────┘
       │
       ├─→ Sentiment Analysis (Detail Target)
       │
       ├─→ Emotion Insights (Detail Emosi)
       │
       ├─→ Comments Explorer (Browse Data)
       │
       └─→ Model Performance (Technical)

[User happy 😊 - Easy to navigate!]
```

---

## 🎯 Apa yang Dipindahkan ke Mana?

### **Dari Dashboard Lama → Dashboard Baru**
- ✅ 4 Metric Cards (Total, Positif, Negatif, Accuracy)
- ✅ Sentiment Pie Chart
- ✅ Top 3 Emotions (simplified)
- ✅ AI Insights

### **Dari Dashboard Lama → Sentiment Page**
- ✅ Target Bar Chart (lengkap)
- ✅ Constructiveness Analysis
- ✅ Target Distribution Pie

### **Dari Dashboard Lama → Emotions Page**
- ✅ All 5 Emotions Bar Chart
- ✅ Radar Chart
- ✅ Emotion Cards dengan detail

### **Dari Dashboard Lama → Model Page**
- ✅ Classification Report
- ✅ Model Architecture
- ✅ Training Details

### **Tetap di Halaman Masing-masing**
- ✅ Comments Explorer (sudah ada)
- ✅ Live Analyzer (sudah ada)
- ✅ Dataset (sudah ada)
- ✅ Documentation (sudah ada)

---

## ✨ Keuntungan Struktur Baru

### **1. Better UX**
- ✅ Tidak overwhelming di first load
- ✅ Progressive disclosure (user explore sesuai kebutuhan)
- ✅ Faster page load (lazy loading per route)

### **2. Better Performance**
- ✅ Code splitting otomatis (Next.js routing)
- ✅ Smaller bundle size per page
- ✅ Faster initial render

### **3. Better Maintainability**
- ✅ Separated concerns (1 page = 1 purpose)
- ✅ Easier to debug
- ✅ Easier to add new features

### **4. Better Scalability**
- ✅ Easy to add new analysis pages
- ✅ Easy to add new tools
- ✅ Modular architecture

---

## 🔄 Migration Checklist

- [x] Create new page structure (`/sentiment`, `/emotions`, `/model`)
- [x] Update Sidebar navigation
- [x] Simplify Dashboard to overview only
- [x] Move detailed charts to respective pages
- [x] Test all routes
- [x] Ensure all data layers accessible
- [x] Update documentation

---

## 🚀 Next Steps

1. **Test semua halaman:**
   ```bash
   npm run dev
   ```

2. **Navigate ke setiap menu:**
   - Dashboard: http://localhost:3000/
   - Sentiment: http://localhost:3000/sentiment
   - Emotions: http://localhost:3000/emotions
   - Comments: http://localhost:3000/comments
   - Model: http://localhost:3000/model
   - Live Analyzer: http://localhost:3000/analytics

3. **Verify semua data muncul dengan benar**

---

## 📝 Notes

- **Semua layer data tetap bisa diakses** - hanya dipindahkan ke halaman yang lebih sesuai
- **Dashboard tetap informatif** - tapi tidak overwhelming
- **Navigation intuitif** - user tahu harus ke mana untuk cari info spesifik
- **Responsive design** - semua halaman mobile-friendly

---

**Status:** ✅ **IMPLEMENTED & READY TO USE**

**Last Updated:** 2025-12-08
**Version:** 2.0
