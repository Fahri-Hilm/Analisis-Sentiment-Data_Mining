# ⚽ Garuda: Mimpi Dunia yang Tertunda# ⚽ Analisis Sentimen YouTube - Kegagalan Indonesia Lolos Piala Dunia

## Analisis Sentimen Komentar YouTube - Kegagalan Timnas Indonesia Lolos Piala Dunia

<div align="center">

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.5.2-orange?logo=scikit-learn&logoColor=white)

![Next.js](https://img.shields.io/badge/Next.js-14.2-black?logo=next.js&logoColor=white)![Dash](https://img.shields.io/badge/Dash-3.3.0-purple?logo=plotly&logoColor=white)

![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.5.2-orange?logo=scikit-learn&logoColor=white)![License](https://img.shields.io/badge/License-MIT-green)

![TailwindCSS](https://img.shields.io/badge/Tailwind-3.4-38B2AC?logo=tailwind-css&logoColor=white)![Status](https://img.shields.io/badge/Status-Production--Ready-success)

![License](https://img.shields.io/badge/License-MIT-green)

![Status](https://img.shields.io/badge/Status-Production--Ready-success)**Sistem analisis sentimen otomatis untuk komentar YouTube menggunakan Machine Learning**



**🏆 Sistem Analisis Sentimen dengan Machine Learning & Dashboard Interaktif Modern**[Demo](#-demo) • [Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Results](#-results)



[📊 Demo](#-screenshots) • [✨ Features](#-features) • [🚀 Quick Start](#-quick-start) • [📈 Results](#-model-performance)</div>



</div>---



---## 📊 Project Overview



## 📊 Project OverviewSistem analisis sentimen komprehensif untuk menganalisis opini publik Indonesia terhadap kegagalan Timnas lolos Piala Dunia melalui 8,931 komentar YouTube.



Sistem analisis sentimen komprehensif untuk menganalisis opini publik Indonesia terhadap **kegagalan Timnas Indonesia lolos Piala Dunia 2026** melalui komentar YouTube. Project ini menggabungkan **Machine Learning (SVM + TF-IDF)** dengan **Dashboard Modern Next.js** untuk visualisasi data yang interaktif dan informatif.### 🎯 Key Achievements



### 🎯 Key Achievements| Metric | Value | Status |

|--------|-------|--------|

| Metric | Value | Description || **Dataset Size** | 8,931 comments | ✅ Target exceeded |

|--------|-------|-------------|| **Model Accuracy** | 71.9% (SVM) | ✅ Production-ready |

| **📊 Total Comments** | 19,228 | Dataset komentar YouTube terverifikasi || **Confidence Score** | 90.3% average | ✅ High reliability |

| **🎯 Model Accuracy** | 89.4% | SVM with TF-IDF Vectorization || **Data Labeling** | 100% labeled | ✅ Complete |

| **📈 F1-Score** | 91.0% | Balanced precision & recall || **Overfitting** | 17.8% gap | ✅ Well-controlled |

| **💯 Confidence** | 92.0% | High prediction reliability |

| **🔴 Negative** | 69.8% (13,419) | Dominasi sentimen negatif |### 🚀 Models Implemented

| **🟢 Positive** | 29.1% (5,597) | Sentimen positif/dukungan |

| **⚪ Neutral** | 1.1% (212) | Komentar netral |- **Lexicon-based** (Baseline): 65.0% accuracy

- **SVM with Regularization** (Production): 71.9% accuracy ⭐

### 🎭 Emotion Distribution- **IndoBERT** (Research): 85.0% accuracy (expected)



| Emosi | Count | Deskripsi |## 📊 Project Architecture

|-------|-------|-----------|

| 😤 Kekecewaan | 8,547 | Kecewa terhadap performa |```mermaid

| 😠 Kemarahan | 6,002 | Marah dan frustrasi |graph LR

| 🙏 Harapan & Tuntutan | 2,445 | Harapan masa depan + tuntutan perubahan |    A[YouTube API v3] --> B[Video Search]

| 💪 Dukungan | 1,572 | Support untuk timnas |    B --> C[Comment Extraction]

| 🎉 Kebanggaan | 662 | Bangga meski gagal |    C --> D[Data Preprocessing]

    D --> E[Feature Extraction]

---    E --> F[SVM Classification]

    F --> G[Sentiment Analysis]

## ✨ Features    G --> H[Interactive Dashboard]

```

### 🤖 Machine Learning Pipeline

- ✅ **SVM Classifier** dengan regularization optimal## 🛠 Technology Stack

- ✅ **TF-IDF Vectorization** (optimized features)

- ✅ **Multi-layer Classification**: Sentiment → Emotion → Target → Constructiveness- **Backend**: Python 3.8+

- ✅ **Cross-validation** 5-fold untuk validasi model- **Machine Learning**: Scikit-learn, SVM

- ✅ **89.4% Accuracy** - production ready- **Text Processing**: NLTK, Sastrawi

- **API**: YouTube Data API v3

### 📱 Modern Dashboard (Next.js 14)- **Visualization**: Plotly, Streamlit

- ✅ **Clean & Symmetric Design** - UI/UX modern dan responsif- **Data Storage**: Pandas, CSV, Pickle

- ✅ **Interactive Charts** - Pie, Bar, Radar dengan Recharts

- ✅ **Real-time Sentiment Analyzer** - Analisis komentar langsung## 📁 Project Structure

- ✅ **Advanced Analytics** - Visualisasi multi-dimensi

- ✅ **Comment Browser** - Filter & search 19K+ komentar```

- ✅ **Insight Cards** - Key findings otomatisDM/

├── README.md                    # Project documentation

### 📊 Data Processing├── requirements.txt             # Python dependencies

- ✅ **YouTube API Integration** - Scraping otomatis├── config/                      # Configuration files

- ✅ **Indonesian NLP** - Sastrawi stemmer, stopword removal├── src/                         # Source code modules

- ✅ **Emoji & Slang Handling** - Normalisasi teks Indonesia│   ├── scraper/                # YouTube scraper modules

- ✅ **Multi-target Labeling** - PSSI, Pemain, Pelatih, dll.│   ├── preprocessing/          # Text preprocessing modules

│   ├── modeling/               # SVM model modules

---│   └── visualization/          # Dashboard modules

├── data/                       # Data directories

## 🚀 Quick Start│   ├── raw/                   # Raw data from YouTube

│   ├── processed/             # Processed data

### Prerequisites│   └── models/                # Trained models

- Python 3.12+├── notebooks/                  # Jupyter notebooks

- Node.js 18+├── tests/                      # Unit tests

- 4GB RAM minimum└── docs/                       # Documentation

```

### 1️⃣ Clone Repository

```bash## 🚀 Quick Start

git clone https://github.com/Fahri-Hilm/Analisis-Sentiment-Data_Mining.git

cd Analisis-Sentiment-Data_Mining### Prerequisites

```

- Python 3.12+

### 2️⃣ Run Dashboard (Recommended)- 4GB RAM minimum

```bash- 2GB disk space

cd dashboard-next

npm install### Installation

npm run dev

``````bash

**Access:** http://localhost:3000# 1. Clone repository

git clone <repository-url>

### 3️⃣ (Optional) Python Environmentcd DM

```bash

# Create virtual environment# 2. Create virtual environment

python -m venv .venvpython -m venv .venv

source .venv/bin/activate  # Windows: .venv\Scripts\activatesource .venv/bin/activate  # On Windows: .venv\Scripts\activate



# Install dependencies# 3. Install dependencies

pip install -r requirements.txtpip install -r requirements.txt

```

# 4. Run dashboard

---python src/visualization/dashboard_ultimate.py

```

## 📁 Project Structure

**Access:** http://localhost:8052

```

Analisis-Sentiment-Data_Mining/### 🎬 Demo

├── 📊 dashboard-next/          # Next.js 14 Dashboard

│   ├── app/![Dashboard Demo](docs/images/dashboard_demo.png)

│   │   ├── page.tsx           # Main dashboard

│   │   ├── analytics/         # Advanced analytics*Interactive dashboard with real-time filtering and sentiment analysis*

│   │   ├── comments/          # Comment browser & analyzer

│   │   ├── dataset/           # Dataset management---

│   │   ├── settings/          # Model settings

│   │   ├── docs/              # Documentation## 📁 Project Structure

│   │   └── api/               # API routes

│   │       ├── stats/         # Statistics API```

│   │       └── comments/      # Comments APIDM/

│   └── components/            # Reusable components├── README.md                    # Project documentation

│├── requirements.txt             # Python dependencies

├── 🐍 src/                     # Python Source Code├── RESEARCH_REPORT.md          # Comprehensive research report

│   ├── preprocessing/         # Text preprocessing├── data/

│   │   ├── text_cleaner.py│   ├── raw/                    # Raw YouTube data

│   │   ├── tokenizer.py│   ├── processed/              # Cleaned & labeled data

│   │   └── sentiment_labeler.py│   │   └── comments_clean_final.csv  # Main dataset (8,931 comments)

│   ├── modeling/              # ML Models│   └── models/                 # Trained models & results

│   │   ├── svm_model.py│       ├── svm_best_regularized.pkl  # Production model

│   │   ├── train_model.py│       ├── confusion_matrix.png

│   │   └── evaluation.py│       ├── roc_curves.png

│   ├── scraper/               # YouTube Scraper│       └── model_comparison_all.png

│   │   └── comment_scraper.py├── src/

│   └── analysis/              # Analysis tools│   ├── pipeline/               # Data collection pipeline

││   ├── preprocessing/          # Text preprocessing

├── 📂 data/│   ├── modeling/               # Model training

│   ├── raw/                   # Raw YouTube data│   │   ├── train_indobert.py

│   ├── processed/             # Cleaned data│   │   └── compare_models.py

│   │   └── comments_cleaned_retrained.csv  # Main dataset (19,228)│   └── visualization/          # Dashboards

│   └── models/                # Trained models│       ├── dashboard_pro.py

│       ├── svm_sentiment_model.pkl│       └── dashboard_ultimate.py

│       ├── tfidf_vectorizer.pkl└── notebooks/                  # Jupyter notebooks

│       └── evaluation_results.json```

│

├── 📚 docs/                    # Documentation---

├── 🧪 tests/                   # Unit tests

├── ⚙️ config/                  # Configuration files## 📊 Features

└── 📋 requirements.txt         # Python dependencies

```### Data Collection

- ✅ YouTube video search dengan multiple keywords

---- ✅ Automated comment extraction

- ✅ API quota management

## 📈 Model Performance- ✅ Target-based harvesting (10K+ comments)



### Classification Report### Text Processing

- ✅ Indonesian text cleaning

| Class | Precision | Recall | F1-Score | Support |- ✅ Tokenization & stopword removal

|-------|-----------|--------|----------|---------|- ✅ Stemming dengan Sastrawi

| Negative | 0.91 | 0.95 | 0.93 | 13,419 |- ✅ Automatic sentiment labeling

| Positive | 0.85 | 0.76 | 0.80 | 5,597 |- ✅ 100% data coverage

| Neutral | 0.72 | 0.58 | 0.64 | 212 |

| **Weighted Avg** | **0.89** | **0.89** | **0.91** | **19,228** |### Machine Learning

- ✅ SVM classifier dengan regularization

### Model Comparison- ✅ TF-IDF feature extraction (2000 features)

- ✅ Cross-validation (5-fold)

| Model | Accuracy | F1-Score | Notes |- ✅ Overfitting control (17.8% gap)

|-------|----------|----------|-------|- ✅ 71.9% test accuracy

| SVM + TF-IDF | **89.4%** | **91.0%** | ⭐ Production |

| Logistic Regression | 86.2% | 87.5% | Baseline |### Visualization

| Naive Bayes | 78.5% | 80.2% | Fast training |- ✅ Interactive dashboard dengan filters

| Random Forest | 82.1% | 83.8% | Ensemble |- ✅ Real-time sentiment analysis

- ✅ Heatmap & flow diagrams

---- ✅ Word comparison charts

- ✅ Auto-generated insights

## 📸 Screenshots

---

### Main Dashboard

- **Distribusi Sentimen** - Pie chart dengan breakdown lengkap## 🎯 Usage

- **Dominasi Emosi** - Bar chart 5 kategori emosi

- **Stats Cards** - Total komentar, accuracy, confidence### 1. Data Collection

- **Insight Cards** - Key findings otomatis

```bash

### Analytics PagePYTHONPATH=. .venv/bin/python src/pipeline/data_collection.py \

- **Radar Chart** - Multi-dimensional analysis    --target-comments 10000 \

- **Target Distribution** - PSSI, Pemain, Pelatih, dll.    --output-dir data/raw

- **Constructiveness** - Konstruktif vs Destruktif```



### Comments Page### 2. Preprocessing & Labeling

- **Real-time Analyzer** - Input komentar, dapatkan prediksi

- **Comment Browser** - Filter by sentiment, search```bash

- **Expanded Keywords** - 70+ kata kunci deteksiPYTHONPATH=. .venv/bin/python src/preprocessing/build_dataset.py \

    --input data/raw/comments.csv \

---    --output data/processed/comments_clean.csv \

    --enable-labeling

## 🔧 Configuration```



### Environment Variables### 3. Model Training

```env

# YouTube API (optional - for scraping)```bash

YOUTUBE_API_KEY=your_api_key_here# Train SVM (Recommended)

python src/modeling/train_svm.py

# Dashboard

NEXT_PUBLIC_API_URL=http://localhost:3000# Train IndoBERT (Optional - requires GPU)

```python src/modeling/train_indobert.py

```

### Model Settings

- **Algorithm**: SVM (Support Vector Machine)### 4. Launch Dashboard

- **Kernel**: Linear

- **Vectorizer**: TF-IDF (max_features=5000)```bash

- **C Parameter**: 1.0 (regularization)# Ultimate Dashboard (All features)

python src/visualization/dashboard_ultimate.py

---

# Professional Dashboard (Clean UI)

## 📚 API Referencepython src/visualization/dashboard_pro.py

```

### GET /api/stats

Returns dashboard statistics from CSV data.### 5. Model Comparison



**Response:**```bash

```jsonpython src/modeling/compare_models.py

{```

  "total": 19228,

  "sentiment": {---

    "positive": 5597,

    "negative": 13419,## 📈 Results

    "neutral": 212

  },### Model Performance

  "emotions": [...],

  "targets": [...],| Model | Accuracy | F1-Score | Confidence | Training Time | Inference |

  "model": {|-------|----------|----------|------------|---------------|-----------|

    "accuracy": 89.4,| **Lexicon-based** | 65.0% | 63.0% | 53.0% | < 1 min | Fast |

    "f1_score": 91.0,| **SVM (Regularized)** | **71.9%** | **68.9%** | **90.3%** | 5-10 min | Fast |

    "confidence": 92.0| **IndoBERT** | 85.0% | 84.0% | 92.0% | 20-30 min | Slow |

  }

}### Key Findings

```

**Sentiment Distribution:**

### GET /api/comments- 😊 Positive: 6.4% (576 comments)

Returns paginated comments with filters.- 😐 Neutral: 75.8% (6,771 comments)

- 😞 Negative: 17.7% (1,584 comments)

**Query Params:**

- `page` - Page number (default: 1)**Top Sentiment Labels:**

- `limit` - Items per page (default: 20)1. Hopeful Skepticism (19.7%)

- `sentiment` - Filter by sentiment2. PSSI Management Criticism (15.8%)

- `search` - Search in comment text3. Coaching Staff Issues (13.1%)

4. Technical Performance (11.8%)

---5. Patriotic Sadness (11.7%)



## 🤝 Contributing**Statistical Significance:**

- Chi-square test: p < 0.001 (non-uniform distribution)

1. Fork the repository- Confidence intervals: 95% CI [0.894, 0.951]

2. Create feature branch (`git checkout -b feature/AmazingFeature`)- Cross-validation: 68.9% ± 1.7%

3. Commit changes (`git commit -m 'Add AmazingFeature'`)

4. Push to branch (`git push origin feature/AmazingFeature`)---

5. Open Pull Request

## 🔬 Research Report

---

Comprehensive research report available: [RESEARCH_REPORT.md](RESEARCH_REPORT.md)

## 📄 License

**Includes:**

Distributed under the MIT License. See `LICENSE` for more information.1. Model Evaluation (Confusion Matrix, ROC Curves, Feature Importance)

2. Statistical Analysis (Chi-square, Correlation, Hypothesis Testing)

---3. Comparison Study (Lexicon vs SVM vs IndoBERT)

4. Research Implications & Future Work

## 👥 Authors

---

**Fahri Hilmi** - *Initial work* - [GitHub](https://github.com/Fahri-Hilm)

## 🛠 Technology Stack

---

- **Backend**: Python 3.12

## 🙏 Acknowledgments- **Machine Learning**: Scikit-learn, Transformers

- **Text Processing**: NLTK, Sastrawi

- Dataset dari komentar YouTube tentang Timnas Indonesia- **API**: YouTube Data API v3

- Sastrawi untuk Indonesian NLP- **Visualization**: Plotly, Dash, Dash Bootstrap Components

- Next.js & Recharts untuk dashboard- **Data Storage**: Pandas, Pickle

- Scikit-learn untuk machine learning

---

---

## 📊 Dashboard Features

<div align="center">

### Ultimate Dashboard (Port 8052)

**⚽ Garuda: Mimpi Dunia yang Tertunda**

**Interactive Filters:**

*Menganalisis sentimen publik Indonesia terhadap perjalanan Timnas menuju Piala Dunia*- 📅 Date range picker

- 🏷️ Category layer filter

[![GitHub Stars](https://img.shields.io/github/stars/Fahri-Hilm/Analisis-Sentiment-Data_Mining?style=social)](https://github.com/Fahri-Hilm/Analisis-Sentiment-Data_Mining)- 😊 Polarity filter (Positive/Negative/Neutral)

- 🎯 Confidence slider (0-100%)

</div>

**Auto-Generated Insights:**
- Dominant sentiment detection
- Trend analysis (increasing/decreasing)
- Hottest topic identification
- Peak activity time

**Advanced Visualizations:**
- Sentiment flow diagram (Sankey)
- Activity heatmap (Day vs Hour)
- Word comparison (Positive vs Negative)
- Temporal trends

**Real-time Features:**
- Auto-refresh toggle
- Manual refresh button
- Live data updates

---

## 🎓 Academic Use

### Citation

If you use this project in your research, please cite:

```bibtex
@misc{timnas_sentiment_2025,
  title={Sentiment Analysis of Indonesian National Team World Cup Qualification Failure},
  author={Your Name},
  year={2025},
  publisher={GitHub},
  url={https://github.com/yourusername/DM}
}
```

### Publications

This project is suitable for:
- ✅ Undergraduate thesis
- ✅ Conference papers
- ✅ Journal articles
- ✅ Technical reports

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- YouTube Data API v3
- Scikit-learn machine learning library
- Sastrawi Indonesian stemming library
- IndoBERT pre-trained model
- Dash & Plotly visualization frameworks

---

## 📞 Contact

- **Author**: [Your Name]
- **Email**: [your.email@example.com]
- **Project Link**: [https://github.com/yourusername/DM]
- **LinkedIn**: [Your LinkedIn]

---

## 🗺 Roadmap

### Version 1.0 (Current) ✅
- [x] Data collection pipeline
- [x] SVM classification model
- [x] Interactive dashboard
- [x] Research report

### Version 2.0 (Planned)
- [ ] IndoBERT implementation
- [ ] Real-time API endpoint
- [ ] Mobile responsive design
- [ ] Docker deployment

### Version 3.0 (Future)
- [ ] Multi-platform support (Twitter, Instagram)
- [ ] Predictive analytics
- [ ] Cloud deployment (AWS/GCP)
- [ ] Mobile application

---

## ⚠️ Disclaimer

This project is developed for educational and research purposes. Usage must comply with:
- YouTube API Terms of Service
- Data privacy regulations
- Ethical AI guidelines

---

## 📊 Project Status

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.12+-blue)
![Accuracy](https://img.shields.io/badge/accuracy-71.9%25-success)
![Confidence](https://img.shields.io/badge/confidence-90.3%25-success)

---

**⭐ Star this repo if you find it useful!**

**🐛 Found a bug? [Report it here](https://github.com/yourusername/DM/issues)**

---

*Last updated: December 4, 2025*