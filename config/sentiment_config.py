"""
9-Layer Sentiment Analysis Configuration

This module contains configuration for the 9-layer sentiment analysis framework
including layer definitions, categories, and parameters.
"""

# Layer 1: Core Sentiment Foundation
CORE_SENTIMENT = {
    'positive_support': {
        'description': 'Active support and optimism despite failure',
        'keywords': ['tetap support', 'bangga', 'jangan menyerah', 'kepala bangkit', 'semangat', 
                    'ayo', 'terus', 'lanjut', 'bisa', 'yakin', 'percaya', 'dukung', 'support'],
        'indicators': ['supportive language', 'future optimism', 'team spirit'],
        'weight': 1.0
    },
    'negative_criticism': {
        'description': 'Constructive criticism with specific points',
        'keywords': ['seharusnya', 'kurang', 'perlu perbaikan', 'evaluasi', 'kritik',
                    'salah', 'buruk', 'jelek', 'gagal', 'tidak', 'gak'],
        'indicators': ['specific issues', 'improvement suggestions', 'analytical tone'],
        'weight': 1.0
    },
    'neutral_observation': {
        'description': 'Objective analysis without emotional bias',
        'keywords': ['fakta', 'data', 'statistik', 'realitas', 'objektif',
                    'memang', 'ya', 'itu', 'ini', 'seperti', 'kayak'],
        'indicators': ['factual statements', 'statistical references', 'balanced view'],
        'weight': 0.8
    },
    'frustration_expression': {
        'description': 'Pure frustration without constructive elements',
        'keywords': ['kesal', 'benci', 'jengkel', 'muak', 'geram',
                    'nyesel', 'kapok', 'males', 'bosan', 'lelah'],
        'indicators': ['emotional outbursts', 'general complaints', 'no solutions'],
        'weight': 0.9
    },
    'hopeful_skepticism': {
        'description': 'Hope mixed with doubt about future',
        'keywords': ['mungkin', 'semoga', 'tapi', 'ragu', 'mudah-mudahan',
                    'harap', 'berharap', 'namun', 'tetapi', 'walaupun'],
        'indicators': ['mixed emotions', 'conditional hope', 'realistic expectations'],
        'weight': 0.7
    }
}

# Layer 2: Football-Specific Emotion Mapping
FOOTBALL_EMOTIONS = {
    'passionate_disappointment': {
        'description': 'Deep disappointment from passionate fans',
        'keywords': ['kecewa berat', 'patah hati', 'tidak percaya', 'hancur', 'sedih sekali',
                    'kecewa', 'sedih', 'sakit', 'nyesek', 'miris', 'speechless'],
        'intensity_range': (4, 5),
        'context': 'immediate post-match reactions',
        'weight': 1.2
    },
    'strategic_frustration': {
        'description': 'Frustration with tactical decisions',
        'keywords': ['salah strategi', 'formasi salah', 'substitusi aneh', 'taktik buruk', 'pelatih salah',
                    'strategi', 'taktik', 'formasi', 'substitusi', 'ganti pemain'],
        'intensity_range': (3, 4),
        'context': 'tactical analysis discussions',
        'weight': 1.1
    },
    'patriotic_sadness': {
        'description': 'Nationalistic sadness about country failure',
        'keywords': ['malu', 'negara', 'bangsa', 'merah putih', 'indonesia',
                    'timnas', 'garuda', 'nkri', 'tanah air'],
        'intensity_range': (3, 5),
        'context': 'national pride discussions',
        'weight': 1.0
    },
    'constructive_anger': {
        'description': 'Anger that leads to constructive discussion',
        'keywords': ['marah tapi', 'seharusnya', 'perlu', 'harus', 'kritik membangun',
                    'saran', 'usul', 'rekomendasi', 'sebaiknya', 'lebih baik'],
        'intensity_range': (2, 4),
        'context': 'improvement-oriented discussions',
        'weight': 0.9
    },
    'respectful_acknowledgment': {
        'description': 'Acknowledging opponent strength or reality',
        'keywords': ['lawan kuat', 'memang lebih baik', 'terima', 'realistis', 'mengakui',
                    'hebat', 'bagus', 'kuat', 'tangguh', 'solid'],
        'intensity_range': (1, 3),
        'context': 'sportsmanship discussions',
        'weight': 0.8
    },
    'future_hope': {
        'description': 'Hope for future improvement',
        'keywords': ['masih ada waktu', 'piala berikutnya', 'pembinaan', 'masa depan', 'optimis',
                    'kedepan', 'nanti', 'akan', 'bisa', 'pasti',
                    'lolos', 'moga', 'semoga', 'playoff', 'play off'],
        'intensity_range': (2, 4),
        'context': 'future-oriented discussions',
        'weight': 0.9
    }
}

# Layer 3: Root Cause Analysis
ROOT_CAUSES = {
    'technical_performance': {
        'subcategories': ['finishing', 'defending', 'passing', 'physical', 'mental'],
        'keywords': ['gol', 'bola mati', 'bertahan', 'stamina', 'mental', 'skill',
                    'main', 'kalah', 'menang', 'juara', 'skor', 'hasil'],
        'indicators': ['specific skill mentions', 'performance metrics'],
        'weight': 1.0
    },
    'tactical_issues': {
        'subcategories': ['formation', 'substitution', 'game_plan', 'adaptation'],
        'keywords': ['formasi', '4-3-3', 'substitusi', 'strategi', 'taktik'],
        'indicators': ['tactical terms', 'formation discussions'],
        'weight': 1.1
    },
    'management_decisions': {
        'subcategories': ['selection', 'preparation', 'leadership', 'communication'],
        'keywords': ['pelatih', 'skuad', 'pemilihan', 'persiapan', 'keputusan'],
        'indicators': ['management terms', 'decision criticism'],
        'weight': 1.2
    },
    'systemic_problems': {
        'subcategories': ['competition', 'development', 'structure', 'governance'],
        'keywords': ['kompetisi', 'pembinaan', 'struktur', 'sistem', 'organisasi'],
        'indicators': ['systemic terms', 'structural criticism'],
        'weight': 1.3
    },
    'external_factors': {
        'subcategories': ['refereeing', 'luck', 'schedule', 'conditions'],
        'keywords': ['wasit', 'kartu', 'offside', 'untung', 'nasib', 'faktor eksternal'],
        'indicators': ['external blame', 'luck references'],
        'weight': 0.8
    },
    'infrastructure': {
        'subcategories': ['facilities', 'youth', 'investment', 'long-term'],
        'keywords': ['stadion', 'akademi', 'investasi', 'pembinaan', 'fasilitas'],
        'indicators': ['infrastructure terms', 'development focus'],
        'weight': 1.0
    }
}

# Layer 4: Stakeholder Sentiment
STAKEHOLDERS = {
    'players': {
        'aspects': ['individual_performance', 'teamwork', 'attitude', 'potential'],
        'keywords': ['pemain', 'striker', 'gelandang', 'bek', 'kiper', 'tim',
                    'skuad', 'squad', 'penyerang', 'bertahan', 'tengah'],
        'sentiment_indicators': ['performance praise', 'skill criticism', 'effort recognition'],
        'weight': 1.0
    },
    'coaching_staff': {
        'aspects': ['tactical_ability', 'leadership', 'communication', 'adaptation'],
        'keywords': ['pelatih', 'asisten', 'staf', 'kepelatihan', 'instruktur',
                    'coach', 'trainer', 'sty', 'shin tae yong', 'patrick', 'kluivert',
                    'latih', 'melatih', 'pk', 'ganti pelatih', 'pecat pelatih'],
        'sentiment_indicators': ['tactical praise', 'leadership criticism', 'strategy feedback'],
        'weight': 1.2
    },
    'pssi_management': {
        'aspects': ['leadership', 'planning', 'transparency', 'execution'],
        'keywords': ['pssi', 'ketum', 'pengurus', 'kebijakan', 'manajemen',
                    'erick', 'tohir', 'thohir', 'iwan', 'bule', 'federasi',
                    'towel', 'erik', 'ganti', 'pecat', 'figc'],
        'sentiment_indicators': ['governance criticism', 'leadership evaluation', 'policy feedback'],
        'weight': 1.3
    },
    'referees': {
        'aspects': ['fairness', 'consistency', 'accuracy', 'bias'],
        'keywords': ['wasit', 'kartu', 'tendangan', 'offside', 'keputusan',
                    'referee', 'merah', 'kuning', 'penalti', 'var'],
        'sentiment_indicators': ['fairness assessment', 'bias accusations', 'accuracy evaluation'],
        'weight': 0.9
    },
    'opponents': {
        'aspects': ['strength', 'strategy', 'sportsmanship', 'ranking'],
        'keywords': ['lawan', 'rival', 'timnas', 'kuat', 'bagus', 'hebat',
                    'jepang', 'arab', 'australia', 'korea', 'china', 'thailand'],
        'sentiment_indicators': ['respect acknowledgment', 'strength recognition', 'strategy analysis'],
        'weight': 0.8
    },
    'fans_supporters': {
        'aspects': ['loyalty', 'passion', 'expectations', 'behavior'],
        'keywords': ['fans', 'supporter', 'suporter', 'penonton', 'pendukung',
                    'bobotoh', 'viking', 'aremania', 'jakmania', 'ultras'],
        'sentiment_indicators': ['fan behavior analysis', 'supporter expectations', 'loyalty assessment'],
        'weight': 0.7
    },
    'media_analysts': {
        'aspects': ['analysis_quality', 'bias', 'expertise', 'influence'],
        'keywords': ['media', 'analisis', 'komentator', 'ahli', 'pakar',
                    'wartawan', 'jurnalis', 'berita', 'liputan', 'channel'],
        'sentiment_indicators': ['media credibility', 'analysis quality', 'bias detection'],
        'weight': 0.8
    }
}

# Layer 5: Temporal-Contextual Analysis
TEMPORAL_CONTEXTS = {
    'immediate_reaction': {
        'timeframe': '0-24 hours',
        'characteristics': ['emotional', 'raw', 'spontaneous'],
        'keywords': ['baru saja', 'tadi', 'langsung', 'reaksi', 'seketika'],
        'sentiment_patterns': ['high intensity', 'emotional dominance'],
        'weight': 1.2
    },
    'short_term_analysis': {
        'timeframe': '1-7 days',
        'characteristics': ['analytical', 'detailed', 'reflective'],
        'keywords': ['kemarin', 'beberapa hari', 'evaluasi', 'analisis'],
        'sentiment_patterns': ['balanced emotion', 'detailed analysis'],
        'weight': 1.0
    },
    'medium_term_reflection': {
        'timeframe': '1-4 weeks',
        'characteristics': ['strategic', 'solution-oriented', 'comprehensive'],
        'keywords': ['minggu lalu', 'sebulan', 'refleksi', 'pembelajaran'],
        'sentiment_patterns': ['constructive focus', 'solution orientation'],
        'weight': 0.9
    },
    'long_term_perspective': {
        'timeframe': '1+ months',
        'characteristics': ['philosophical', 'systemic', 'forward-looking'],
        'keywords': ['bulan lalu', 'tahun', 'jangka panjang', 'visi'],
        'sentiment_patterns': ['systemic focus', 'future orientation'],
        'weight': 0.8
    },
    'historical_comparison': {
        'timeframe': 'cross-time',
        'characteristics': ['comparative', 'pattern-seeking', 'contextual'],
        'keywords': ['dulu', 'sebelumnya', 'sejarah', 'pola', 'perbandingan'],
        'sentiment_patterns': ['pattern recognition', 'historical context'],
        'weight': 0.7
    },
    'future_projection': {
        'timeframe': 'future-oriented',
        'characteristics': ['predictive', 'hopeful', 'strategic'],
        'keywords': ['mendatang', 'besok', 'target', 'proyeksi', 'prediksi'],
        'sentiment_patterns': ['hopeful bias', 'strategic thinking'],
        'weight': 0.9
    }
}

# Layer 6: Solution-Oriented Sentiment
SOLUTION_ORIENTED = {
    'constructive_suggestions': {
        'description': 'Specific actionable suggestions',
        'keywords': ['seharusnya', 'perlu', 'saran', 'rekomendasi', 'usul'],
        'actionability': 'high',
        'examples': ['improve finishing', 'change formation', 'better preparation'],
        'weight': 1.2
    },
    'systemic_reform_calls': {
        'description': 'Calls for structural changes',
        'keywords': ['reform', 'perubahan', 'sistem', 'struktur', 'revolusi'],
        'actionability': 'medium-high',
        'examples': ['competition reform', 'governance changes', 'development overhaul'],
        'weight': 1.1
    },
    'player_development_focus': {
        'description': 'Focus on player improvement',
        'keywords': ['pembinaan', 'pengembangan', 'akademi', 'muda', 'pelatihan'],
        'actionability': 'high',
        'examples': ['youth academy', 'training programs', 'skill development'],
        'weight': 1.0
    },
    'coaching_changes': {
        'description': 'Recommendations for coaching improvements',
        'keywords': ['pelatih baru', 'kepelatihan', 'staf', 'metode', 'pendekatan'],
        'actionability': 'medium',
        'examples': ['foreign coach', 'new methods', 'better preparation'],
        'weight': 0.9
    },
    'youth_investment': {
        'description': 'Investment in young players',
        'keywords': ['investasi', 'muda', 'generasi', 'masa depan', 'bibit'],
        'actionability': 'high',
        'examples': ['youth leagues', 'school programs', 'talent identification'],
        'weight': 1.1
    },
    'international_collaboration': {
        'description': 'Partnerships with international entities',
        'keywords': ['kerjasama', 'internasional', 'asing', 'partner', 'kolaborasi'],
        'actionability': 'medium',
        'examples': ['foreign partnerships', 'training abroad', 'technical cooperation'],
        'weight': 0.8
    }
}

# Layer 7: Predictive Analytics Configuration
PREDICTIVE_CONFIG = {
    'match_outcome': {
        'features': ['sentiment_trend', 'emotion_intensity', 'stakeholder_confidence'],
        'model_type': 'classification',
        'target_accuracy': 0.75,
        'time_horizon': 'next_match'
    },
    'performance_forecasting': {
        'features': ['historical_sentiment', 'solution_implementation', 'stakeholder_support'],
        'model_type': 'regression',
        'target_mae': 0.5,
        'time_horizon': '3_months'
    },
    'crisis_prediction': {
        'features': ['negative_sentiment_spike', 'frustration_level', 'criticism_intensity'],
        'model_type': 'anomaly_detection',
        'sensitivity': 0.8,
        'early_warning_days': 7
    },
    'fan_engagement': {
        'features': ['support_level', 'participation_rate', 'emotion_diversity'],
        'model_type': 'regression',
        'target_r2': 0.7,
        'time_horizon': '1_month'
    }
}

# Layer 8: AI-Powered Insights Configuration
AI_INSIGHTS_CONFIG = {
    'automated_reports': {
        'frequency': 'daily',
        'sections': ['executive_summary', 'key_findings', 'recommendations', 'trends'],
        'format': 'html',
        'delivery': ['dashboard', 'email']
    },
    'recommendation_engine': {
        'priority_factors': ['actionability', 'impact', 'feasibility', 'stakeholder_support'],
        'max_recommendations': 10,
        'confidence_threshold': 0.7
    },
    'anomaly_detection': {
        'methods': ['statistical', 'ml_based', 'rule_based'],
        'sensitivity': 0.8,
        'alert_threshold': 2.0
    },
    'topic_modeling': {
        'algorithm': 'lda',
        'num_topics': 10,
        'update_frequency': 'weekly'
    },
    'influencer_identification': {
        'metrics': ['engagement_rate', 'follower_count', 'sentiment_impact'],
        'top_influencers': 20,
        'update_frequency': 'daily'
    }
}

# Layer 9: Advanced Visualization Configuration
VISUALIZATION_CONFIG = {
    '3d_landscape': {
        'dimensions': ['emotion', 'intensity', 'time'],
        'color_scheme': 'viridis',
        'interactive': True,
        'update_frequency': 'real_time'
    },
    'real_time_stream': {
        'update_interval': 5,  # seconds
        'buffer_size': 1000,
        'chart_types': ['line', 'bar', 'heatmap']
    },
    'network_analysis': {
        'node_types': ['stakeholders', 'emotions', 'solutions'],
        'layout': 'force_directed',
        'interactive': True
    },
    'dashboard_layout': {
        'theme': 'dark',
        'auto_refresh': 30,  # seconds
        'panels': ['overview', 'detailed', 'predictive', 'insights']
    }
}

# Cross-Layer Integration Configuration
CROSS_LAYER_CONFIG = {
    'emotion_cause_linkage': {
        'method': 'correlation_analysis',
        'threshold': 0.5,
        'update_frequency': 'daily'
    },
    'stakeholder_emotion_mapping': {
        'method': 'matrix_analysis',
        'normalization': 'row_column',
        'visualization': 'heatmap'
    },
    'temporal_solution_evolution': {
        'method': 'time_series_analysis',
        'smoothing': 'exponential',
        'trend_detection': True
    },
    'constructive_criticism_ratio': {
        'calculation': 'constructive / total_criticism',
        'target_range': (0.6, 0.8),
        'alert_threshold': 0.5
    }
}

# Model Configuration
MODEL_CONFIG = {
    'ensemble_method': 'weighted_voting',
    'base_models': ['svm_linear', 'svm_rbf', 'random_forest', 'xgboost'],
    'cross_validation': {
        'method': 'stratified_kfold',
        'n_splits': 5,
        'shuffle': True,
        'random_state': 42
    },
    'hyperparameter_tuning': {
        'method': 'grid_search',
        'scoring': 'f1_weighted',
        'cv': 5,
        'n_jobs': -1
    }
}

# Evaluation Metrics Configuration
EVALUATION_CONFIG = {
    'primary_metrics': ['accuracy', 'precision', 'recall', 'f1_score'],
    'secondary_metrics': ['roc_auc', 'confusion_matrix', 'classification_report'],
    'layer_specific_metrics': {
        'layer_1': {'accuracy': 0.85, 'f1_weighted': 0.80},
        'layer_2': {'f1_weighted': 0.80, 'accuracy': 0.75},
        'layer_3': {'accuracy': 0.75, 'f1_weighted': 0.70},
        'layer_4': {'accuracy': 0.75, 'f1_weighted': 0.70},
        'layer_5': {'accuracy': 0.80, 'f1_weighted': 0.75},
        'layer_6': {'actionability_score': 0.70, 'relevance_score': 0.75},
        'layer_7': {'accuracy': 0.75, 'mae': 0.5},
        'layer_8': {'relevance_score': 0.80, 'novelty_score': 0.70},
        'layer_9': {'user_satisfaction': 0.85, 'response_time': 1.0}
    }
}