# 📊 Dashboard Structure - Garuda Sentiment Analysis

## 🎯 Struktur Menu Baru

Dashboard telah direorganisasi menjadi **5 halaman utama** + **3 tools** untuk pengalaman yang lebih clean dan terstruktur.

---

## 📱 Navigation Structure

### **ANALYSIS** (Menu Utama)

#### 1. **Dashboard** (`/`)
**Tujuan:** Gambaran umum (overview) sistem
**Konten:**
- ✅ 4 Key Metrics Cards (Total, Positif, Negatif, Accuracy)
- ✅ Pie Chart: Distribusi Sentimen
- ✅ Top 3 Emosi (cards)
- ✅ AI Insights

**Filosofi:** Halaman landing yang memberikan snapshot cepat tanpa overwhelming user dengan terlalu banyak data.

---

#### 2. **Sentiment Analysis** (`/sentiment`)
**Tujuan:** Detail analisis sentimen berdasarkan target dan konstruktivitas
**Konten:**
- ✅ Bar Chart: Sentimen by Target (PSSI, Pemain, Pelatih, dll)
- ✅ Progress Bars: Konstruktivitas Komentar
- ✅ Pie Chart: Distribusi Target
- ✅ Breakdown Constructive vs Non-constructive

**Use Case:** User yang ingin tahu "siapa yang paling banyak dikritik?" dan "apakah kritiknya konstruktif?"

---

#### 3. **Emotion Insights** (`/emotions`)
**Tujuan:** Analisis mendalam tentang emosi dalam komentar
**Konten:**
- ✅ Horizontal Bar Chart: Distribusi 5+ Emosi
- ✅ Radar Chart: Intensitas Emosi
- ✅ Emotion Cards: Detail per emosi dengan count & percentage
- ✅ Color-coded visualization

**Use Case:** Memahami "apa yang sebenarnya dirasakan publik?" - Kecewa? Marah? Atau masih ada harapan?

---

#### 4. **Comments Explorer** (`/comments`)
**Tujuan:** Browse dan search 19K+ komentar
**Konten:**
- ✅ Search & Filter interface
- ✅ Pagination (20 per page)
- ✅ Filter by: Sentiment, Emotion, Target
- ✅ Individual comment cards dengan semua label

**Use Case:** Researcher atau analyst yang ingin deep dive ke komentar spesifik.

---

#### 5. **Model Performance** (`/model`)
**Tujuan:** Technical metrics untuk ML model
**Konten:**
- ✅ 3 Metric Cards: Accuracy (89.4%), F1-Score (91%), Confidence (92%)
- ✅ Classification Report Table (Precision, Recall, F1, Support)
- ✅ Model Architecture Details (SVM, TF-IDF, Features)
- ✅ Training Details (Dataset size, Cross-validation, etc.)

**Use Case:** Technical audience yang ingin validasi performa model.

---

### **TOOLS** (Menu Sekunder)

#### 6. **Live Analyzer** (`/analytics`)
**Tujuan:** Real-time sentiment prediction
**Konten:**
- ✅ Text input area
- ✅ Predict button
- ✅ Result display dengan confidence score
- ✅ Sentiment + Emotion + Target prediction

**Use Case:** Testing model dengan komentar baru.

---

#### 7. **Dataset** (`/dataset`)
**Tujuan:** Dataset management & statistics
**Konten:**
- ✅ Dataset overview
- ✅ Download options
- ✅ Data quality metrics
- ✅ Sample data preview

---

#### 8. **Documentation** (`/docs`)
**Tujuan:** Project documentation
**Konten:**
- ✅ API documentation
- ✅ Model explanation
- ✅ Usage guide
- ✅ Technical specs

---

## 🎨 Design Philosophy

### **Progressive Disclosure**
- **Dashboard** = High-level overview (5 seconds to understand)
- **Sentiment/Emotions** = Medium-depth analysis (2-3 minutes exploration)
- **Comments/Model** = Deep dive (10+ minutes research)

### **Information Hierarchy**
```
Level 1: Dashboard (What happened?)
    ↓
Level 2: Sentiment + Emotions (Why it happened?)
    ↓
Level 3: Comments + Model (How we know it?)
```

### **User Journey**
1. **Casual User** → Dashboard only
2. **Analyst** → Dashboard → Sentiment → Emotions
3. **Researcher** → All pages + Comments Explorer
4. **Developer** → Model Performance + Documentation

---

## 📊 Data Flow

```
CSV Data (19,228 comments)
    ↓
API Route (/api/stats)
    ↓
useDashboardStats Hook
    ↓
All Pages (shared state)
```

**Benefit:** Single source of truth, no redundant API calls.

---

## 🚀 Performance Optimizations

1. **Lazy Loading:** Background3D loaded dynamically
2. **Memoization:** Chart data di-memoize dengan `useMemo`
3. **Code Splitting:** Setiap page adalah route terpisah
4. **Skeleton Loading:** Smooth loading experience
5. **Shared Hook:** `useDashboardStats` untuk caching

---

## 🎯 Key Improvements

### Before (Old Structure)
❌ Semua visualisasi di 1 halaman → overwhelming
❌ Scroll panjang → bad UX
❌ Sulit navigasi ke data spesifik
❌ Loading lambat (render semua sekaligus)

### After (New Structure)
✅ Separated concerns → clean & focused
✅ Progressive disclosure → better UX
✅ Easy navigation → find what you need
✅ Faster loading → lazy load per page

---

## 📱 Mobile Responsiveness

Semua halaman menggunakan:
- `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`
- Responsive charts dengan `ResponsiveContainer`
- Mobile-friendly sidebar (dapat di-collapse di future update)

---

## 🔮 Future Enhancements

1. **Dashboard:**
   - [ ] Sentiment trend over time (line chart)
   - [ ] Comparison with previous period

2. **Sentiment Analysis:**
   - [ ] Sentiment by date/time
   - [ ] Cross-tabulation sentiment × target

3. **Emotions:**
   - [ ] Emotion correlation matrix
   - [ ] Emotion transition flow

4. **Comments:**
   - [ ] Advanced filters (date range, keyword)
   - [ ] Export filtered results
   - [ ] Sentiment heatmap

5. **Model:**
   - [ ] Confusion matrix visualization
   - [ ] ROC curves
   - [ ] Feature importance chart

6. **Live Analyzer:**
   - [ ] Batch prediction (upload CSV)
   - [ ] API endpoint for external integration

---

## 📝 File Structure

```
app/
├── page.tsx                    # Dashboard (Overview)
├── sentiment/
│   └── page.tsx               # Sentiment Analysis
├── emotions/
│   └── page.tsx               # Emotion Insights
├── comments/
│   └── page.tsx               # Comments Explorer
├── model/
│   └── page.tsx               # Model Performance
├── analytics/
│   └── page.tsx               # Live Analyzer
├── dataset/
│   └── page.tsx               # Dataset Management
├── docs/
│   └── page.tsx               # Documentation
└── api/
    └── stats/
        └── route.ts           # API endpoint
```

---

## 🎨 Color Coding

- **Blue** (`#3b82f6`) - Dashboard, General
- **Green** (`#10b981`) - Positive sentiment, Success
- **Red** (`#f43f5e`) - Negative sentiment, Alerts
- **Purple** (`#8b5cf6`) - Emotions, AI features
- **Cyan** (`#06b6d4`) - Active states, Highlights
- **Slate** (`#64748b`) - Neutral, Secondary info

---

## ✅ Checklist Implementation

- [x] Create new page structure
- [x] Update Sidebar navigation
- [x] Migrate Dashboard to overview only
- [x] Create Sentiment Analysis page
- [x] Create Emotion Insights page
- [x] Create Model Performance page
- [x] Update routing
- [x] Test all pages
- [ ] Add loading states (optional)
- [ ] Add error boundaries (optional)
- [ ] Mobile optimization (optional)

---

## 🚀 How to Run

```bash
cd dashboard-next
npm run dev
```

**Access:** http://localhost:3000

---

**Built with ❤️ for better UX and cleaner architecture**
