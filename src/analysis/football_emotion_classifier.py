"""
Football Emotion Classifier - Layer 2
Mengklasifikasikan emosi spesifik sepakbola dari komentar
Berdasarkan 6 kategori emosi konteks sepakbola Indonesia
"""

import pandas as pd
import numpy as np
import re
from typing import Dict, List, Tuple
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class FootballEmotionClassifier:
    """
    Classifier untuk 6 emosi spesifik sepakbola:
    1. Passionate Disappointment (Kekecewaan Mendalam)
    2. Strategic Frustration (Frustrasi Taktik)
    3. Patriotic Sadness (Kesedihan Nasionalis)
    4. Constructive Anger (Kemarahan Membangun)
    5. Respectful Acknowledgment (Pengakuan Respek)
    6. Future Hope (Harapan Masa Depan)
    """
    
    def __init__(self):
        self.emotion_keywords = self._build_emotion_keywords()
        self.emotion_patterns = self._build_emotion_patterns()
        
    def _build_emotion_keywords(self) -> Dict[str, List[str]]:
        """Build keyword dictionary untuk setiap emosi"""
        return {
            'passionate_disappointment': [
                # Kekecewaan mendalam dengan intensitas tinggi
                'sangat kecewa', 'kecewa berat', 'sedih banget', 'hancur', 'patah hati',
                'frustasi', 'nyesek', 'sakit hati', 'down', 'desperate',
                'gagal lagi', 'kapan menang', 'selalu kalah', 'tidak bisa',
                'mimpi buruk', 'nightmare', 'tragedi', 'bencana', 'malapetaka',
                'shock', 'terpukul', 'terluka', 'malu', 'memalukan',
                'disappointment', 'heartbreak', 'crushed', 'devastated'
            ],
            
            'strategic_frustration': [
                # Frustrasi terhadap strategi dan taktik
                'strategi salah', 'taktik salah', 'formasi salah', 'substitusi salah',
                'ganti pemain', 'kenapa tidak main', 'kenapa dimainkan', 
                'pelatih tidak paham', 'coach gak ngerti', 'taktik gak jelas',
                'pola permainan', 'sistem permainan', 'gaya bermain',
                'defensive', 'offensive', 'counter attack', 'parking bus',
                'rotasi pemain', 'line up', 'starting eleven', 'susunan pemain',
                'formasi 4-3-3', 'formasi 3-5-2', 'formasi 4-4-2',
                'strategi defense', 'strategi menyerang', 'pressing',
                'build up play', 'lini tengah', 'lini belakang', 'lini depan'
            ],
            
            'patriotic_sadness': [
                # Kesedihan dengan unsur nasionalisme
                'bangsa', 'negara', 'indonesia', 'garuda', 'merah putih',
                'bendera', 'lagu kebangsaan', 'kemerdekaan', 'tanah air',
                'nasional', 'patriot', 'cinta tanah air', 'bangga indonesia',
                'harapan bangsa', 'anak negeri', 'anak bangsa', 'pemuda indonesia',
                'generasi muda', 'masa depan indonesia', 'prestasi indonesia',
                'nama indonesia', 'kehormatan bangsa', 'harga diri bangsa',
                'martabat bangsa', 'demi indonesia', 'untuk indonesia',
                'indonesia jaya', 'indonesiaku', 'negeri tercinta',
                'bangkit indonesia', 'indonesia bisa', 'semangat garuda'
            ],
            
            'constructive_anger': [
                # Kemarahan yang membangun dengan kritik konstruktif
                'harus berubah', 'perlu perbaikan', 'harus diperbaiki', 'butuh evaluasi',
                'evaluasi total', 'benah diri', 'introspeksi', 'perbaiki',
                'ganti pelatih', 'pecat', 'harus diganti', 'cari yang baru',
                'rekrut pemain', 'naturalisasi', 'pemain asing', 'pemain bagus',
                'latihan lebih keras', 'training center', 'fasilitas', 'pembinaan',
                'regenerasi', 'akademi', 'youth development', 'pemain muda',
                'sistem liga', 'kompetisi', 'infrastruktur', 'investasi',
                'kualitas wasit', 'kualitas kompetisi', 'standar profesional',
                'managemen harus', 'pssi harus', 'federasi harus', 'pemerintah harus',
                'solusi', 'saran', 'masukan', 'kritik', 'rekomendasi'
            ],
            
            'respectful_acknowledgment': [
                # Pengakuan terhadap kenyataan dengan respek
                'memang lebih baik', 'memang hebat', 'mengakui', 'respect',
                'hormat', 'salut', 'lawan tangguh', 'lawan kuat', 'tim bagus',
                'pemain berkualitas', 'kelas dunia', 'level berbeda',
                'pengalaman', 'jam terbang', 'profesional', 'kualitas tinggi',
                'harus belajar', 'masih belajar', 'proses panjang', 'butuh waktu',
                'realistis', 'wajar', 'sesuai ekspektasi', 'sudah maksimal',
                'perjuangan bagus', 'sudah berusaha', 'fighting spirit',
                'terima kasih', 'appreciate', 'bangga walau kalah',
                'kalah terhormat', 'head up', 'tetap semangat', 'jangan menyerah'
            ],
            
            'future_hope': [
                # Harapan untuk masa depan
                'next match', 'pertandingan berikutnya', 'laga selanjutnya',
                'piala dunia depan', 'world cup 2026', 'kualifikasi berikutnya',
                'masa depan', 'kedepan', 'ke depan', 'nanti', 'suatu saat',
                'optimis', 'yakin', 'percaya', 'bisa', 'mampu', 'pasti bisa',
                'semangat', 'bangkit', 'rise up', 'comeback', 'balas dendam',
                'pemain muda', 'generasi baru', 'regenerasi', 'talenta muda',
                'potensi', 'berkembang', 'progress', 'improvement', 'lebih baik',
                'harapan', 'mimpi', 'cita-cita', 'target', 'ambisi',
                'never give up', 'pantang menyerah', 'terus berjuang',
                'tetap dukung', 'tetap support', 'always support',
                'menuju', 'towards', 'journey', 'perjalanan', 'proses'
            ]
        }
    
    def _build_emotion_patterns(self) -> Dict[str, List[str]]:
        """Build regex patterns untuk deteksi emosi"""
        return {
            'passionate_disappointment': [
                r'(kecewa|sedih|malu|hancur|nyesek)\s+(banget|sekali|berat|parah)',
                r'(sangat|begitu|amat)\s+(kecewa|sedih|malu|frustasi)',
                r'(gagal|kalah)\s+(lagi|terus|mulu|melulu)',
                r'kapan\s+(menang|lolos|juara|bisa)',
            ],
            'strategic_frustration': [
                r'(strategi|taktik|formasi|substitusi)\s+(salah|keliru|gak jelas)',
                r'(kenapa|kok)\s+(tidak|gak|ga)\s+(main|dimainkan|masuk)',
                r'(pelatih|coach)\s+(tidak|gak|ga)\s+(paham|ngerti|bisa)',
                r'(line\s*up|starting|susunan)\s+(salah|aneh|gak jelas)',
            ],
            'patriotic_sadness': [
                r'(demi|untuk|nama|harga\s*diri|martabat|kehormatan)\s+(indonesia|bangsa|negara)',
                r'(bangsa|negara|indonesia)\s+(kecewa|sedih|malu)',
                r'(garuda|merah\s*putih|sang\s*merah\s*putih)',
            ],
            'constructive_anger': [
                r'(harus|perlu|butuh)\s+(berubah|perbaikan|evaluasi|diganti)',
                r'(ganti|pecat|rekrut|cari)\s+(pelatih|pemain|coach)',
                r'(benah|perbaiki|tingkatkan)\s+(diri|sistem|kualitas|infrastruktur)',
            ],
            'respectful_acknowledgment': [
                r'(memang|emang)\s+(lebih|lebih\s*baik|hebat|bagus|kuat)',
                r'(mengakui|respect|hormat|salut|appreciate)',
                r'(harus|perlu|butuh)\s+(belajar|waktu|proses)',
                r'(sudah|telah)\s+(maksimal|berusaha|bagus)',
            ],
            'future_hope': [
                r'(next|berikut|selanjutnya|depan|kedepan)\s+(match|pertandingan|laga|piala)',
                r'(world\s*cup|piala\s*dunia)\s+(2026|depan|berikut)',
                r'(optimis|yakin|percaya|bisa|mampu|pasti)',
                r'(semangat|bangkit|comeback|rise)',
            ]
        }
    
    def _count_keyword_matches(self, text: str, keywords: List[str]) -> int:
        """Hitung jumlah keyword yang cocok dalam teks"""
        text_lower = text.lower()
        count = 0
        for keyword in keywords:
            if keyword in text_lower:
                count += 1
        return count
    
    def _count_pattern_matches(self, text: str, patterns: List[str]) -> int:
        """Hitung jumlah pattern yang cocok dalam teks"""
        count = 0
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                count += 1
        return count
    
    def _calculate_emotion_scores(self, text: str) -> Dict[str, float]:
        """Hitung score untuk setiap emosi"""
        scores = {}
        
        for emotion in self.emotion_keywords.keys():
            # Hitung keyword matches
            keyword_count = self._count_keyword_matches(
                text, 
                self.emotion_keywords[emotion]
            )
            
            # Hitung pattern matches (dengan bobot lebih tinggi)
            pattern_count = self._count_pattern_matches(
                text,
                self.emotion_patterns[emotion]
            )
            
            # Total score: keyword (1x) + pattern (2x)
            total_score = keyword_count + (pattern_count * 2)
            scores[emotion] = total_score
        
        return scores
    
    def classify_emotion(self, text: str, core_sentiment: str = None) -> Tuple[str, float, Dict[str, float]]:
        """
        Klasifikasi emosi dari teks
        
        Returns:
            Tuple[str, float, Dict]: (emotion_label, confidence, all_scores)
        """
        if not text or pd.isna(text):
            return 'unknown', 0.0, {}
        
        # Hitung scores untuk semua emosi
        scores = self._calculate_emotion_scores(text)
        
        # Jika tidak ada match sama sekali
        if max(scores.values()) == 0:
            return 'neutral_observation', 0.3, scores
        
        # Ambil emosi dengan score tertinggi
        primary_emotion = max(scores, key=scores.get)
        max_score = scores[primary_emotion]
        
        # Hitung confidence berdasarkan score relatif
        total_score = sum(scores.values())
        if total_score > 0:
            confidence = max_score / total_score
        else:
            confidence = 0.0
        
        # Adjust confidence berdasarkan absolute score
        if max_score == 1:
            confidence = min(confidence, 0.5)
        elif max_score == 2:
            confidence = min(confidence, 0.6)
        elif max_score >= 3:
            confidence = min(confidence + 0.2, 1.0)
        
        # Context adjustment berdasarkan core sentiment
        if core_sentiment:
            if core_sentiment == 'negative':
                if primary_emotion in ['passionate_disappointment', 'strategic_frustration', 'patriotic_sadness']:
                    confidence = min(confidence + 0.1, 1.0)
            elif core_sentiment == 'positive':
                if primary_emotion in ['respectful_acknowledgment', 'future_hope']:
                    confidence = min(confidence + 0.1, 1.0)
        
        return primary_emotion, confidence, scores
    
    def process_dataframe(self, df: pd.DataFrame, text_column: str = 'clean_text', 
                         sentiment_column: str = 'core_sentiment') -> pd.DataFrame:
        """
        Process seluruh dataframe dan tambahkan kolom emotion
        
        Args:
            df: DataFrame input
            text_column: Nama kolom yang berisi teks
            sentiment_column: Nama kolom yang berisi core sentiment
            
        Returns:
            DataFrame dengan kolom baru: football_emotion, emotion_confidence, emotion_scores
        """
        logger.info(f"Processing {len(df)} comments for emotion classification...")
        
        results = []
        for idx, row in df.iterrows():
            text = row[text_column] if text_column in row else ''
            sentiment = row[sentiment_column] if sentiment_column in row else None
            
            emotion, confidence, scores = self.classify_emotion(text, sentiment)
            results.append({
                'football_emotion': emotion,
                'emotion_confidence': confidence,
                'emotion_scores': str(scores)  # Store as string for CSV compatibility
            })
            
            if (idx + 1) % 1000 == 0:
                logger.info(f"Processed {idx + 1}/{len(df)} comments...")
        
        # Tambahkan hasil ke dataframe
        result_df = pd.DataFrame(results)
        df_output = pd.concat([df, result_df], axis=1)
        
        logger.info("Emotion classification completed!")
        return df_output
    
    def get_emotion_distribution(self, df: pd.DataFrame) -> pd.Series:
        """Get distribusi emosi dari dataframe"""
        return df['football_emotion'].value_counts()
    
    def get_emotion_labels(self) -> Dict[str, str]:
        """Get mapping label emosi ke deskripsi bahasa Indonesia"""
        return {
            'passionate_disappointment': 'Kekecewaan Mendalam',
            'strategic_frustration': 'Frustrasi Taktik',
            'patriotic_sadness': 'Kesedihan Nasionalis',
            'constructive_anger': 'Kemarahan Membangun',
            'respectful_acknowledgment': 'Pengakuan Respek',
            'future_hope': 'Harapan Masa Depan',
            'neutral_observation': 'Observasi Netral',
            'unknown': 'Tidak Teridentifikasi'
        }


def main():
    """Test function untuk classifier"""
    classifier = FootballEmotionClassifier()
    
    # Test cases
    test_cases = [
        ("Sangat kecewa banget dengan performa timnas, gagal lagi lolos piala dunia", "negative"),
        ("Strategi pelatih salah, kenapa tidak main pemain terbaik kita?", "negative"),
        ("Demi kehormatan bangsa Indonesia, harus bangkit lagi!", "neutral"),
        ("PSSI harus berubah total, perlu evaluasi sistem pembinaan", "negative"),
        ("Lawan memang lebih baik, kita harus belajar banyak. Respect!", "positive"),
        ("Optimis untuk piala dunia 2026, yakin Indonesia bisa!", "positive"),
    ]
    
    print("\n" + "="*80)
    print("FOOTBALL EMOTION CLASSIFIER - TEST RESULTS")
    print("="*80 + "\n")
    
    for text, sentiment in test_cases:
        emotion, confidence, scores = classifier.classify_emotion(text, sentiment)
        emotion_label = classifier.get_emotion_labels()[emotion]
        
        print(f"Text: {text[:80]}...")
        print(f"Sentiment: {sentiment}")
        print(f"Emotion: {emotion_label} ({emotion})")
        print(f"Confidence: {confidence:.2f}")
        print(f"Scores: {scores}")
        print("-" * 80 + "\n")


if __name__ == "__main__":
    main()
