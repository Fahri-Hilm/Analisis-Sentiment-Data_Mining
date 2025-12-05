"""
Dashboard Configuration
Konfigurasi label Bahasa Indonesia untuk dashboard visualisasi
"""

# Mapping sentiment categories ke Bahasa Indonesia
SENTIMENT_LABELS_ID = {
    # Core Sentiment (Layer 1)
    'positive_support': 'Dukungan Positif',
    'negative_criticism': 'Kritik Negatif',
    'neutral_observation': 'Pengamatan Netral',
    
    # Football-Specific Emotions (Layer 2)
    'patriotic_sadness': 'Kesedihan Patriotik',
    'passionate_disappointment': 'Kekecewaan Mendalam',
    'frustration_expression': 'Ekspresi Frustrasi',
    'immediate_reaction': 'Reaksi Spontan',
    'respectful_acknowledgment': 'Pengakuan Sportif',
    'hopeful_skepticism': 'Harapan Skeptis',
    
    # Stakeholders (Layer 3)
    'pssi_management': 'Manajemen PSSI',
    'opponents': 'Lawan Pertandingan',
    'coaching_staff': 'Staf Pelatih',
    'players': 'Para Pemain',
    'referees': 'Wasit',
    'fans_supporters': 'Fans & Suporter',
    'media_analysts': 'Media & Analis',
    
    # Technical Analysis (Layer 4)
    'tactical_issues': 'Masalah Taktik',
    'technical_performance': 'Performa Teknis',
    'management_decisions': 'Keputusan Manajemen',
    'coaching_changes': 'Pergantian Pelatih',
    
    # Structural Issues (Layer 5)
    'systemic_problems': 'Masalah Sistemik',
    'infrastructure': 'Infrastruktur',
    'youth_investment': 'Investasi Pemain Muda',
    'systemic_reform_calls': 'Seruan Reformasi Sistem',
    
    # External Context (Layer 6)
    'external_factors': 'Faktor Eksternal',
    'international_collaboration': 'Kolaborasi Internasional',
    'historical_comparison': 'Perbandingan Historis',
    
    # Forward-Looking (Layer 7)
    'future_projection': 'Proyeksi Masa Depan',
    'future_hope': 'Harapan Masa Depan',
    'constructive_suggestions': 'Saran Konstruktif',
    
    # Nuanced Sentiments (Layer 8)
    'constructive_anger': 'Kemarahan Konstruktif',
    'strategic_frustration': 'Frustrasi Strategis',
    
    # Temporal Perspective (Layer 9)
    'short_term_analysis': 'Analisis Jangka Pendek',
    'long_term_perspective': 'Perspektif Jangka Panjang',
}

# Mapping layer names ke Bahasa Indonesia
LAYER_NAMES_ID = {
    'core_sentiment': 'Sentimen Dasar',
    'football_emotions': 'Emosi Sepak Bola',
    'stakeholders': 'Pemangku Kepentingan',
    'technical_analysis': 'Analisis Teknis',
    'structural_issues': 'Isu Struktural',
    'external_context': 'Konteks Eksternal',
    'forward_looking': 'Pandangan Ke Depan',
    'nuanced_sentiments': 'Sentimen Bernuansa',
    'temporal_perspective': 'Perspektif Waktu',
}

# Color scheme untuk sentiment categories (berdasarkan tone)
SENTIMENT_COLORS = {
    # Positive tones - hijau
    'positive_support': '#2ecc71',
    'future_hope': '#27ae60',
    'respectful_acknowledgment': '#16a085',
    'constructive_suggestions': '#1abc9c',
    
    # Negative tones - merah/oranye
    'negative_criticism': '#e74c3c',
    'passionate_disappointment': '#c0392b',
    'frustration_expression': '#e67e22',
    'constructive_anger': '#d35400',
    'strategic_frustration': '#dc7633',
    
    # Sadness tones - biru
    'patriotic_sadness': '#3498db',
    'immediate_reaction': '#5dade2',
    
    # Neutral tones - abu-abu
    'neutral_observation': '#95a5a6',
    'hopeful_skepticism': '#7f8c8d',
    
    # Stakeholders - ungu/violet
    'pssi_management': '#9b59b6',
    'opponents': '#8e44ad',
    'coaching_staff': '#7d3c98',
    'players': '#6c3483',
    'referees': '#5b2c6f',
    'fans_supporters': '#4a235a',
    'media_analysts': '#884ea0',
    
    # Technical - kuning/gold
    'tactical_issues': '#f39c12',
    'technical_performance': '#f1c40f',
    'management_decisions': '#d4ac0d',
    'coaching_changes': '#b7950b',
    
    # Structural - coklat
    'systemic_problems': '#a04000',
    'infrastructure': '#ba4a00',
    'youth_investment': '#d35400',
    'systemic_reform_calls': '#ca6f1e',
    
    # External - cyan
    'external_factors': '#17a2b8',
    'international_collaboration': '#138496',
    'historical_comparison': '#0e6674',
    
    # Forward-looking - tosca
    'future_projection': '#20c997',
    
    # Temporal - pink
    'short_term_analysis': '#fd79a8',
    'long_term_perspective': '#e84393',
}

# Chart configuration
CHART_CONFIG = {
    'bar_chart': {
        'height': 500,
        'title_font_size': 18,
        'label_font_size': 12,
    },
    'pie_chart': {
        'height': 400,
        'title_font_size': 18,
    },
    'wordcloud': {
        'width': 800,
        'height': 400,
        'background_color': 'white',
        'colormap': 'viridis',
        'max_words': 100,
    },
}

# Dashboard text dalam Bahasa Indonesia
UI_TEXT = {
    'title': '📊 Dashboard Analisis Sentimen Komentar YouTube',
    'subtitle': 'Analisis Sentimen: Indonesia Gagal Lolos Piala Dunia',
    'sidebar_title': '🎛️ Pengaturan',
    'data_overview': '📈 Ringkasan Data',
    'total_comments': 'Total Komentar',
    'unique_sentiments': 'Kategori Sentimen Unik',
    'top_sentiment': 'Sentimen Teratas',
    'model_accuracy': 'Akurasi Model',
    'sentiment_distribution': '📊 Distribusi Sentimen',
    'top_categories': 'Top 15 Kategori Sentiment',
    'layer_distribution': '🥧 Distribusi Per Layer',
    'wordcloud_title': '☁️ Word Cloud',
    'select_sentiment': 'Pilih Kategori Sentiment',
    'sample_comments': '💬 Contoh Komentar',
    'showing_comments': 'Menampilkan {n} komentar dari kategori: {category}',
    'model_performance': '🎯 Performa Model',
    'confusion_matrix': 'Confusion Matrix',
    'prediction_tool': '🔮 Prediksi Sentimen (Real-time)',
    'input_placeholder': 'Masukkan komentar untuk diprediksi...',
    'predict_button': '🚀 Prediksi Sentimen',
    'prediction_result': 'Hasil Prediksi',
    'confidence_score': 'Confidence Score',
    'filter_by_layer': 'Filter berdasarkan Layer',
    'all_layers': 'Semua Layer',
    'export_data': '💾 Ekspor Data',
    'download_csv': 'Download CSV',
}

# Emoji mapping untuk sentiment categories
SENTIMENT_EMOJIS = {
    'positive_support': '👍',
    'negative_criticism': '👎',
    'neutral_observation': '😐',
    'patriotic_sadness': '😢',
    'passionate_disappointment': '😞',
    'frustration_expression': '😤',
    'immediate_reaction': '⚡',
    'respectful_acknowledgment': '🙏',
    'hopeful_skepticism': '🤔',
    'pssi_management': '🏢',
    'opponents': '⚽',
    'coaching_staff': '👔',
    'players': '👟',
    'referees': '🟨',
    'fans_supporters': '🎭',
    'media_analysts': '📺',
    'tactical_issues': '📋',
    'technical_performance': '⚙️',
    'management_decisions': '📊',
    'coaching_changes': '🔄',
    'systemic_problems': '🏗️',
    'infrastructure': '🏟️',
    'youth_investment': '🎓',
    'systemic_reform_calls': '📢',
    'external_factors': '🌍',
    'international_collaboration': '🤝',
    'historical_comparison': '📜',
    'future_projection': '🔮',
    'future_hope': '🌟',
    'constructive_suggestions': '💡',
    'constructive_anger': '🔥',
    'strategic_frustration': '♟️',
    'short_term_analysis': '📅',
    'long_term_perspective': '🗓️',
}

def get_indonesian_label(english_label):
    """Get Indonesian translation of English sentiment label"""
    return SENTIMENT_LABELS_ID.get(english_label, english_label)

def get_layer_name(english_layer):
    """Get Indonesian translation of layer name"""
    return LAYER_NAMES_ID.get(english_layer, english_layer)

def get_sentiment_color(sentiment_label):
    """Get color for sentiment category"""
    return SENTIMENT_COLORS.get(sentiment_label, '#95a5a6')

def get_sentiment_emoji(sentiment_label):
    """Get emoji for sentiment category"""
    return SENTIMENT_EMOJIS.get(sentiment_label, '📝')
