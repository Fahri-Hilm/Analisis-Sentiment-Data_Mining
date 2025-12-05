"""
OPTIMIZED 5-LAYER SENTIMENT FRAMEWORK
Fokus pada ACTIONABLE INSIGHTS & REAL PROBLEMS

Berdasarkan analisis 10,950 komentar real, framework ini dirancang untuk:
1. Identifikasi masalah utama dengan jelas
2. Berikan insight yang ACTIONABLE untuk stakeholder
3. Hindari kategori yang terlalu granular/overlapping
4. Fokus pada REALITAS masalah yang terjadi
"""

# ============================================================
# LAYER 1: CORE SENTIMENT (Sentimen Dasar)
# Tujuan: Klasifikasi emosi dasar - SIMPLE & CLEAR
# ============================================================
CORE_SENTIMENT = {
    'positive': {
        'description': 'Dukungan, optimisme, dan semangat positif',
        'keywords': [
            'bangga', 'semangat', 'luar biasa', 'hebat', 'mantap',
            'tetap support', 'ayo', 'terus berjuang', 'optimis', 'pasti bisa',
            'keren', 'bagus', 'salut', 'apresiasi', 'terima kasih'
        ],
        'weight': 1.0,
        'layer': 'core_sentiment'
    },
    'negative': {
        'description': 'Kekecewaan, kritik, dan sentimen negatif',
        'keywords': [
            'kecewa', 'gagal', 'kalah', 'buruk', 'jelek',
            'parah', 'hancur', 'menyedihkan', 'mengecewakan', 'bodoh',
            'tolol', 'goblok', 'payah', 'lemah', 'malu',
            'benci', 'kesal', 'muak', 'jengkel', 'marah'
        ],
        'weight': 1.0,
        'layer': 'core_sentiment'
    },
    'neutral': {
        'description': 'Observasi objektif tanpa emosi kuat',
        'keywords': [
            'fakta', 'data', 'statistik', 'realitas', 'sebenarnya',
            'memang', 'ya', 'begitu', 'seperti', 'wajar'
        ],
        'weight': 0.8,
        'layer': 'core_sentiment'
    }
}

# ============================================================
# LAYER 2: TARGET KRITIK (Who to Blame)
# Tujuan: Identifikasi SIAPA yang bertanggung jawab
# ACTIONABLE: Stakeholder bisa tau siapa yang harus berubah
# ============================================================
TARGET_KRITIK = {
    'pssi_management': {
        'description': 'Kritik ke PSSI, pengurus, dan manajemen federasi',
        'keywords': [
            'pssi', 'pengurus', 'federasi', 'fa', 'asosiasi',
            'ketua umum', 'sekjen', 'eksekutif', 'ketum', 'erick thohir',
            'manajemen', 'kebijakan', 'keputusan', 'sistem pssi', 'esco'
        ],
        'action_points': [
            'Reform struktur PSSI',
            'Transparansi finansial',
            'Profesionalisme manajemen',
            'Audit internal'
        ],
        'weight': 1.3,
        'layer': 'target_kritik',
        'priority': 'HIGH'
    },
    'coaching_staff': {
        'description': 'Kritik ke pelatih dan staf kepelatihan',
        'keywords': [
            'pelatih', 'coach', 'shin tae yong', 'sty', 'klivert', 'patrick',
            'asisten', 'staff', 'kepelatihan', 'strategi pelatih',
            'pilihan pemain', 'formasi', 'substitusi', 'taktik pelatih',
            'bima', 'peter', 'nova', 'korean'
        ],
        'action_points': [
            'Evaluasi performa pelatih',
            'Pertimbangan pergantian pelatih',
            'Training staf yang lebih baik',
            'Rekrut pelatih berpengalaman'
        ],
        'weight': 1.2,
        'layer': 'target_kritik',
        'priority': 'HIGH'
    },
    'players': {
        'description': 'Kritik ke pemain timnas',
        'keywords': [
            'pemain', 'player', 'striker', 'kiper', 'defender', 'midfielder',
            'marselino', 'egy', 'sandy', 'elkan', 'rizky', 'asnawi',
            'performa pemain', 'skill pemain', 'mental pemain', 'fisik pemain',
            'naturalisasi', 'pemain naturalisasi'
        ],
        'action_points': [
            'Intensifkan training',
            'Mental coaching',
            'Fitness improvement',
            'Seleksi pemain lebih ketat'
        ],
        'weight': 1.1,
        'layer': 'target_kritik',
        'priority': 'MEDIUM'
    },
    'opponents': {
        'description': 'Komentar tentang tim lawan (Arab Saudi, Jepang, dll)',
        'keywords': [
            'arab', 'saudi', 'jepang', 'korea', 'australia', 'china',
            'lawan', 'opponent', 'rival', 'musuh',
            'tim lawan', 'lebih kuat', 'lebih bagus', 'kelas atas'
        ],
        'action_points': [
            'Analisis kompetitor',
            'Benchmark dengan tim kuat',
            'Studi kasus kesuksesan lawan'
        ],
        'weight': 0.8,
        'layer': 'target_kritik',
        'priority': 'LOW'
    },
    'external_factors': {
        'description': 'Faktor eksternal (wasit, FIFA, COVID, dll)',
        'keywords': [
            'wasit', 'referee', 'kartu', 'penalty', 'VAR',
            'fifa', 'afc', 'korupsi', 'mafia', 'konspirasi',
            'keberuntungan', 'nasib', 'takdir', 'covid', 'pandemi'
        ],
        'action_points': [
            'Lobby ke AFC/FIFA',
            'Improve fair play',
            'Adaptasi dengan kondisi eksternal'
        ],
        'weight': 0.6,
        'layer': 'target_kritik',
        'priority': 'LOW'
    }
}

# ============================================================
# LAYER 3: ROOT CAUSE ANALYSIS (Akar Masalah)
# Tujuan: Identifikasi KENAPA gagal
# ACTIONABLE: Fokus area improvement yang spesifik
# ============================================================
ROOT_CAUSE = {
    'tactical_strategic': {
        'description': 'Masalah taktik dan strategi pertandingan',
        'keywords': [
            # Core tactical terms
            'taktik', 'strategi', 'formasi', 'skema', 'pola', 'sistem',
            '4-3-3', '5-3-2', '4-4-2', '3-5-2', '4-2-3-1',
            
            # Playing style
            'pressing', 'counter attack', 'possession', 'defending', 'attacking',
            'bertahan', 'menyerang', 'serang', 'defend', 'attack',
            'build up', 'transition', 'transisi',
            
            # Tactical execution
            'substitusi', 'pergantian', 'rotasi', 'line up', 'starting eleven',
            'susunan pemain', 'komposisi', 'penempatan', 'posisi',
            
            # Tactical problems
            'game plan', 'strategi pelatih', 'reading game', 'baca permainan',
            'salah taktik', 'taktik salah', 'formasi salah', 'salah formasi',
            'kacau', 'tidak teratur', 'tidak ada strategi', 'tanpa strategi',
            
            # Specific tactics
            'offside trap', 'marking', 'man to man', 'zona', 'zonal marking',
            'wing play', 'sayap', 'tengah', 'overlap', 'crossing',
            'set piece', 'corner', 'tendangan bebas', 'free kick',
            
            # PHRASE-BASED KEYWORDS (Multi-word tactical terms)
            'pressing tinggi', 'high pressing', 'gegenpress', 'gegenpressing',
            'tiki taka', 'tiki-taka', 'short passing', 'passing pendek',
            'build up play', 'build-up play', 'main dari belakang',
            'counter attack cepat', 'serangan balik', 'serangan cepat',
            'man to man marking', 'man marking', 'marking ketat',
            'zona marking', 'zonal defending', 'pertahanan zona',
            'false nine', 'false 9', 'striker semu',
            'wing back', 'wingback', 'bek sayap',
            'attacking midfielder', 'gelandang serang',
            'defensive midfielder', 'gelandang bertahan', 'holding midfielder',
            'total football', 'total sepakbola',
            'parking the bus', 'parkir bus', 'bertahan total',
            'possession based', 'main kuasai bola', 'menguasai bola',
            'long ball strategy', 'strategi bola panjang', 'umpan panjang',
            'set piece specialist', 'spesialis bola mati',
            'offside trap strategy', 'perangkap offside',
            'overlap run', 'lari overlap',
            'through ball', 'umpan terobosan',
            'diagonal run', 'lari diagonal',
            'switching play', 'pindah sisi', 'ganti sisi permainan'
        ],
        'solution_areas': [
            'Pelatihan taktik intensif',
            'Analisis video lawan',
            'Simulasi berbagai formasi',
            'Flexibilitas strategi'
        ],
        'weight': 1.2,
        'layer': 'root_cause',
        'priority': 'HIGH'
    },
    'technical_skill': {
        'description': 'Masalah kemampuan teknis pemain',
        'keywords': [
            # Core technical skills
            'skill', 'teknik', 'kemampuan', 'ability', 'kualitas',
            
            # Attacking skills
            'finishing', 'shooting', 'tendangan', 'tembakan', 'menembak',
            'gol', 'goal', 'mencetak', 'scoring', 'scorer',
            'dribbling', 'dribble', 'melewati', 'mengoper',
            
            # Passing skills
            'passing', 'umpan', 'operan', 'assist', 'menyilang',
            'crossing', 'umpan silang', 'throughball', 'long ball',
            
            # Ball control
            'kontrol bola', 'ball control', 'sentuhan', 'touch', 'first touch',
            'menguasai bola', 'penguasaan', 'trapping',
            
            # Defensive skills
            'tackling', 'tekel', 'rebut', 'merebut', 'blocking',
            'intercept', 'intersepsi', 'clearing', 'sapuan',
            
            # Other skills
            'heading', 'sundulan', 'menyundul', 'header',
            
            # Skill problems
            'kurang tajam', 'tumpul', 'meleset', 'miss', 'gagal',
            'akurasi', 'accuracy', 'tidak akurat', 'kurang tepat',
            'lemah', 'weak', 'payah', 'jelek', 'buruk',
            
            # Physical attributes
            'kecepatan', 'speed', 'cepat', 'lambat', 'slow',
            'stamina', 'kondisi', 'fitness', 'fisik', 'physical',
            'kelelahan', 'capek', 'tired', 'exhausted', 'loyo',
            'cedera', 'injury', 'injured', 'sakit', 'cidera',
            
            # PHRASE-BASED KEYWORDS (Multi-word technical terms)
            'kontrol bola buruk', 'kontrol bola lemah', 'kontrol bola jelek',
            'finishing lemah', 'finishing buruk', 'finishing kurang tajam',
            'umpan tidak akurat', 'passing tidak akurat', 'umpan meleset',
            'tendangan jarak jauh', 'tembakan jarak jauh', 'long range shot',
            'first touch buruk', 'sentuhan pertama buruk',
            'kemampuan dribbling', 'skill dribbling', 'dribble skill',
            'akurasi passing', 'akurasi umpan', 'ketepatan passing',
            'timing tackle', 'timing tekel', 'waktu tackle',
            'positioning buruk', 'posisi tidak tepat', 'salah posisi',
            'awareness kurang', 'kurang awareness', 'game intelligence',
            'decision making', 'pengambilan keputusan', 'keputusan buruk',
            'work rate', 'kerja keras', 'intensitas kerja',
            'off the ball movement', 'pergerakan tanpa bola',
            'vision pemain', 'visi pemain', 'kreativitas',
            'one on one', '1 vs 1', '1v1', 'duel pemain',
            'aerial duel', 'duel udara', 'pertarungan udara',
            'pace and power', 'kecepatan dan kekuatan',
            'teknik dasar', 'basic technique', 'fundamental skill',
            'shooting accuracy', 'akurasi tembakan',
            'crossing ability', 'kemampuan crossing', 'kualitas crossing',
            'defensive awareness', 'kesadaran bertahan'
        ],
        'solution_areas': [
            'Training teknis lebih intensif',
            'Fitness & conditioning program',
            'Injury prevention',
            'Skill development workshop'
        ],
        'weight': 1.1,
        'layer': 'root_cause',
        'priority': 'HIGH'
    },
    'mental_psychological': {
        'description': 'Masalah mental dan psikologi pemain',
        'keywords': [
            # Core mental terms
            'mental', 'psikologi', 'psychology', 'mindset', 'mentalitas',
            
            # Confidence
            'percaya diri', 'confidence', 'confident', 'pede', 'yakin',
            'tidak percaya diri', 'kurang pede', 'ragu', 'doubt',
            
            # Motivation & spirit
            'semangat', 'spirit', 'motivasi', 'motivation', 'motivated',
            'fighting spirit', 'never give up', 'pantang menyerah',
            'juang', 'berjuang', 'fight', 'determination',
            
            # Pressure & nerves
            'grogi', 'nervous', 'nervous breakdown', 'deg-degan',
            'tekanan', 'pressure', 'stress', 'tertekan', 'under pressure',
            'panik', 'panic', 'takut', 'afraid', 'fear', 'ketakutan',
            'cemas', 'anxious', 'anxiety', 'tegang', 'tension',
            
            # Character & attitude
            'karakter', 'character', 'sikap', 'attitude', 'behavior',
            'leadership', 'kepemimpinan', 'leader', 'pemimpin',
            'disiplin', 'discipline', 'disciplined', 'profesional',
            
            # Mental problems
            'mental down', 'mental drop', 'mental jatuh', 'collapse',
            'give up', 'menyerah', 'pasrah', 'surrender',
            'tidak fokus', 'konsentrasi', 'concentration', 'focus',
            'emosi', 'emotional', 'marah', 'frustasi', 'frustrated',
            
            # PHRASE-BASED KEYWORDS (Multi-word mental terms)
            'mental juara', 'mental pemenang', 'winner mentality',
            'mental tempe', 'mental kere', 'mental loser',
            'mental block', 'blocking mental', 'hambatan mental',
            'kepercayaan diri', 'rasa percaya diri', 'self confidence',
            'percaya diri kurang', 'kurang percaya diri',
            'fighting spirit tinggi', 'semangat juang tinggi',
            'never give up', 'tidak menyerah', 'pantang menyerah',
            'motivasi tinggi', 'highly motivated', 'semangat tinggi',
            'under pressure', 'di bawah tekanan', 'tekanan tinggi',
            'mental breakdown', 'mental collapse', 'collapse mental',
            'team spirit', 'spirit tim', 'semangat tim',
            'mental strength', 'kekuatan mental', 'mental kuat',
            'mental lemah', 'mental rapuh', 'weak mentality',
            'fokus dan konsentrasi', 'concentration level',
            'leadership quality', 'kualitas kepemimpinan',
            'positive attitude', 'sikap positif', 'attitude baik',
            'professional mentality', 'profesionalisme',
            'emotional control', 'kontrol emosi', 'mengendalikan emosi',
            'self belief', 'keyakinan diri', 'belief system',
            'comfort zone', 'zona nyaman', 'keluar zona nyaman'
        ],
        'solution_areas': [
            'Mental coaching profesional',
            'Sports psychology program',
            'Team bonding activities',
            'Confidence building'
        ],
        'weight': 1.0,
        'layer': 'root_cause',
        'priority': 'MEDIUM'
    },
    'systemic_structural': {
        'description': 'Masalah sistemik dan infrastruktur sepak bola Indonesia',
        'keywords': [
            # Core systemic terms
            'sistem', 'system', 'sistemik', 'systemic', 'struktur', 'structural',
            
            # Youth development
            'akademi', 'academy', 'pembinaan', 'grassroot', 'grass root',
            'youth development', 'pemain muda', 'junior', 'u-19', 'u-23',
            'youth', 'junior development', 'generasi', 'regenerasi',
            
            # League & competition
            'liga', 'league', 'kompetisi', 'competition', 'tournament',
            'liga 1', 'liga indonesia', 'domestic league',
            'kualitas liga', 'level liga', 'standar liga',
            
            # Infrastructure
            'infrastruktur', 'infrastructure', 'fasilitas', 'facility',
            'lapangan', 'field', 'stadion', 'stadium', 'venue',
            'training center', 'tc', 'training ground', 'training facility',
            'gym', 'medical', 'sport science',
            
            # Financial & investment
            'dana', 'fund', 'funding', 'anggaran', 'budget', 'finansial',
            'investasi', 'investment', 'sponsor', 'sponsorship',
            'money', 'uang', 'gaji', 'salary', 'bonus',
            
            # Management & organization
            'manajemen', 'management', 'organisasi', 'organization',
            'reform', 'reforma', 'perubahan', 'change',
            'transparansi', 'transparency', 'akuntabilitas', 'accountability',
            
            # Systemic problems
            'korupsi', 'corruption', 'KKN', 'nepotisme', 'nepotism',
            'mafia', 'kongkalikong', 'politik', 'politics',
            'tidak profesional', 'amatir', 'amateur', 'unprofessional',
            
            # PHRASE-BASED KEYWORDS (Multi-word systemic terms)
            'pembinaan usia dini', 'youth development system', 'sistem pembinaan',
            'akademi sepakbola', 'football academy', 'soccer academy',
            'infrastruktur buruk', 'infrastruktur tidak memadai', 'fasilitas kurang',
            'training center modern', 'tc modern', 'fasilitas training',
            'kualitas liga rendah', 'level liga rendah', 'standar liga buruk',
            'kompetisi tidak berkualitas', 'liga tidak profesional',
            'grassroot development', 'pembinaan grassroot', 'akar rumput',
            'youth system', 'sistem junior', 'pembinaan junior',
            'sport science center', 'pusat sport science',
            'medical facility', 'fasilitas medis', 'medical center',
            'investment jangka panjang', 'long term investment',
            'reforma total', 'total reform', 'perubahan menyeluruh',
            'transparansi finansial', 'financial transparency',
            'management profesional', 'manajemen profesional',
            'corruption free', 'bebas korupsi', 'anti korupsi',
            'good governance', 'tata kelola baik', 'governance system',
            'profesionalisme rendah', 'tidak profesional',
            'nepotisme merajalela', 'nepotism problem',
            'political interference', 'intervensi politik', 'campur tangan politik'
        ],
        'solution_areas': [
            'Bangun akademi sepak bola berkualitas',
            'Investasi infrastruktur jangka panjang',
            'Reforma liga profesional',
            'Youth development program'
        ],
        'weight': 1.3,
        'layer': 'root_cause',
        'priority': 'HIGH'
    }
}

# ============================================================
# LAYER 4: TIME PERSPECTIVE (Perspektif Waktu Solusi)
# Tujuan: Klasifikasi KAPAN solusi bisa direalisasikan
# ACTIONABLE: Roadmap perbaikan jangka pendek vs panjang
# ============================================================
TIME_PERSPECTIVE = {
    'immediate': {
        'description': 'Butuh action SEGERA (0-6 bulan)',
        'keywords': [
            # Urgency terms
            'sekarang', 'now', 'segera', 'immediately', 'instant',
            'langsung', 'direct', 'cepat', 'fast', 'quick',
            'urgent', 'mendesak', 'darurat', 'emergency',
            
            # Time references
            'harus', 'must', 'wajib', 'mandatory', 'required',
            'besok', 'tomorrow', 'hari ini', 'today', 'saat ini',
            'secepatnya', 'asap', 'as soon as possible',
            'minggu ini', 'this week', 'bulan ini', 'this month',
            
            # Immediate actions
            'pecat', 'fire', 'ganti', 'replace', 'change',
            'pecat sekarang', 'ganti pelatih', 'ganti coach',
            'reshuffle', 'action now', 'take action',
            'evaluasi', 'evaluate', 'review',
            
            # Current state
            'pertandingan ini', 'this match', 'laga ini', 'game ini',
            'situasi ini', 'kondisi ini', 'saat ini', 'right now',
            
            # PHRASE-BASED KEYWORDS (Multi-word urgency terms)
            'sekarang juga', 'right now', 'saat ini juga',
            'sesegera mungkin', 'as soon as possible', 'secepat mungkin',
            'action segera', 'immediate action', 'tindakan segera',
            'pecat sekarang', 'fire now', 'pecat langsung',
            'ganti pelatih sekarang', 'change coach now',
            'evaluasi langsung', 'immediate evaluation',
            'pertandingan berikutnya', 'next match', 'laga berikutnya',
            'laga selanjutnya', 'next game', 'match selanjutnya',
            'minggu depan', 'next week', 'bulan depan'
        ],
        'actions': [
            'Ganti pelatih/staf',
            'Reshuffle manajemen PSSI',
            'Evaluasi pemain segera'
        ],
        'weight': 1.2,
        'layer': 'time_perspective',
        'timeline': '0-6 bulan'
    },
    'short_term': {
        'description': 'Perbaikan jangka pendek (6 bulan - 2 tahun)',
        'keywords': [
            # Future time references
            'tahun depan', 'next year', 'next season', 'musim depan',
            'beberapa bulan', 'few months', 'bulan depan', 'next month',
            '6 bulan', 'six months', '1 tahun', 'one year', '2 tahun',
            
            # Competitions
            'qualification berikutnya', 'next qualification', 'kualifikasi',
            'piala berikutnya', 'next tournament', 'turnamen berikutnya',
            'aff', 'aff cup', 'piala aff', 'sea games', 'asean',
            'asian cup', 'piala asia', 'asian games',
            
            # Preparation
            'training camp', 'tc', 'training', 'latihan', 'persiapan',
            'preparation', 'prepare', 'siapkan', 'mempersiapkan',
            'program', 'rencana', 'plan', 'planning',
            
            # Development
            'perbaikan', 'improvement', 'develop', 'development',
            'tingkatkan', 'improve', 'enhance', 'better',
            'upgrade', 'update', 'modernisasi',
            
            # PHRASE-BASED KEYWORDS (Multi-word short-term terms)
            'tahun depan', 'next year', 'tahun 2025', 'tahun 2026',
            'musim depan', 'next season', 'season berikutnya',
            'piala aff', 'aff cup', 'piala aff berikutnya',
            'asian games', 'sea games', 'piala asia',
            'asian cup', 'afc asian cup', 'kualifikasi berikutnya',
            'next qualification', 'kualifikasi piala asia',
            'training camp intensif', 'tc intensive', 'training intensive',
            'program latihan', 'training program', 'program persiapan',
            'preparation program', 'persiapan jangka pendek',
            'perbaikan sistem', 'system improvement', 'improve system',
            'development program', 'program development',
            'upgrade fasilitas', 'facility upgrade'
        ],
        'actions': [
            'Training program baru',
            'Rekrutmen pemain muda',
            'Pelatihan intensif'
        ],
        'weight': 1.0,
        'layer': 'time_perspective',
        'timeline': '6 bulan - 2 tahun'
    },
    'long_term': {
        'description': 'Pembinaan jangka panjang (2-10 tahun)',
        'keywords': [
            # Future generations
            'generasi', 'generation', 'next generation', 'generasi muda',
            'masa depan', 'future', 'masa akan datang', 'kedepan',
            'anak cucu', 'children', 'future kids', 'nanti',
            
            # Youth development
            'pembinaan', 'development', 'youth', 'pemain muda',
            'grassroot', 'grass root', 'akademi', 'academy',
            'junior', 'u-16', 'u-17', 'u-19', 'u-20', 'u-23',
            
            # Long-term timeline
            '5 tahun', '10 tahun', '20 tahun', 'decades', 'dekade',
            'jangka panjang', 'long term', 'long-term', 'long run',
            'bertahun-tahun', 'years', 'puluhan tahun',
            
            # World Cup aspirations
            'piala dunia', 'world cup', 'wc', 'fifa world cup',
            '2026', '2030', '2034', '2038', 'world cup 2026',
            'qualification world cup', 'kualifikasi piala dunia',
            
            # Vision & legacy
            'visi', 'vision', 'misi', 'mission', 'target',
            'cita-cita', 'dream', 'impian', 'harapan',
            'legacy', 'warisan', 'fondasi', 'foundation', 'dasar',
            
            # PHRASE-BASED KEYWORDS (Multi-word long-term terms)
            'piala dunia 2026', 'world cup 2026', 'wc 2026',
            'piala dunia 2030', 'world cup 2030', 'wc 2030',
            'piala dunia 2034', 'world cup 2034',
            'kualifikasi piala dunia', 'world cup qualification',
            'qualify piala dunia', 'lolos piala dunia',
            'generasi mendatang', 'next generation', 'generasi berikutnya',
            'masa depan sepakbola', 'future of football',
            'masa depan timnas', 'future of national team',
            'jangka panjang', 'long term', 'long-term development',
            'pembinaan jangka panjang', 'long term development',
            'grassroot development', 'pembinaan grassroot',
            'youth development system', 'sistem pembinaan muda',
            'akademi sepakbola', 'football academy system',
            'visi jangka panjang', 'long term vision',
            'target piala dunia', 'world cup target',
            'mimpi piala dunia', 'world cup dream',
            'legacy sepakbola', 'football legacy',
            'fondasi kuat', 'strong foundation', 'membangun fondasi',
            'investasi masa depan', 'future investment'
        ],
        'actions': [
            'Bangun akademi berkualitas',
            'Sistem pembinaan nasional',
            'Investasi infrastruktur'
        ],
        'weight': 0.9,
        'layer': 'time_perspective',
        'timeline': '2-10 tahun'
    }
}

# ============================================================
# LAYER 5: CONSTRUCTIVENESS (Tingkat Konstruktifitas)
# Tujuan: Apakah ada SOLUSI atau hanya MARAH?
# ACTIONABLE: Filter noise vs valuable feedback
# ============================================================
CONSTRUCTIVENESS = {
    'constructive': {
        'description': 'Ada saran perbaikan yang spesifik dan konstruktif',
        'keywords': [
            # Suggestion terms
            'saran', 'suggestion', 'usul', 'propose', 'proposal',
            'sebaiknya', 'seharusnya', 'should', 'better',
            'perlu', 'need', 'needs', 'diperlukan', 'butuh',
            
            # Solution-oriented
            'harus', 'must', 'wajib', 'solusi', 'solution', 'solve',
            'perbaikan', 'fix', 'improvement', 'improve', 'perbaiki',
            'evaluasi', 'evaluate', 'review', 'analisis', 'analyze',
            
            # Recommendation
            'rekomendasikan', 'recommend', 'suggest', 'sarankan',
            'ide', 'idea', 'cara', 'way', 'method', 'strategi',
            'masukan', 'input', 'feedback', 'constructive feedback',
            
            # Conditional suggestions
            'kalau', 'jika', 'if', 'bila', 'seandainya',
            'sebaiknya', 'mungkin', 'maybe', 'perhaps', 'could',
            'coba', 'try', 'cobalah', 'mencoba', 'attempt',
            
            # Development focus
            'latihan', 'training', 'belajar', 'learn', 'study',
            'tingkatkan', 'upgrade', 'develop', 'kembangkan',
            'bangun', 'build', 'bentuk', 'create'
        ],
        'value': 'HIGH',
        'weight': 1.3,
        'layer': 'constructiveness'
    },
    'destructive': {
        'description': 'Hanya marah/komplain tanpa solusi',
        'keywords': [
            # Hatred & disgust
            'benci', 'hate', 'hatred', 'muak', 'disgusted', 'jijik',
            'kapok', 'enough', 'never again', 'jangan nonton lagi',
            
            # Hopelessness
            'gak ada harapan', 'no hope', 'hopeless', 'tanpa harapan',
            'putus asa', 'desperate', 'menyerah', 'give up',
            
            # Destructive calls
            'bubar', 'disband', 'dissolve', 'resign', 'mundur', 'resign aja',
            'pecat', 'fire', 'out', 'keluar', 'resign all',
            
            # Insults & toxicity
            'tolol', 'stupid', 'idiot', 'bodoh', 'goblok',
            'bangsat', 'anjing', 'dog', 'kampret', 'tai',
            'sampah', 'trash', 'garbage', 'busuk', 'rotten',
            'jelek', 'ugly', 'buruk', 'bad', 'payah', 'useless',
            'ngaco', 'nonsense', 'kacau', 'chaos', 'mess',
            
            # Negative emotions
            'marah', 'angry', 'anger', 'kesel', 'annoyed',
            'kecewa', 'disappointed', 'disappointing', 'malu', 'ashamed',
            'shame', 'embarrassed', 'memalukan', 'shameful'
        ],
        'value': 'LOW',
        'weight': 0.5,
        'layer': 'constructiveness'
    },
    'hopeful': {
        'description': 'Optimisme dan harapan untuk masa depan',
        'keywords': [
            # Hope & prayers
            'semoga', 'hopefully', 'mudah-mudahan', 'hopefully',
            'insya allah', 'inshallah', 'god willing', 'amin', 'amen',
            'berharap', 'hope', 'hoping', 'harapan', 'wish',
            
            # Optimism
            'optimis', 'optimistic', 'optimism', 'yakin', 'confident',
            'percaya', 'believe', 'faith', 'trust', 'keyakinan',
            'pasti bisa', 'can do', 'bisa', 'can', 'mampu', 'able',
            
            # Opportunity
            'masih ada kesempatan', 'still chance', 'kesempatan', 'opportunity',
            'ada peluang', 'there is hope', 'belum terlambat', 'not too late',
            
            # Encouragement
            'jangan menyerah', 'don\'t give up', 'never surrender',
            'terus berjuang', 'keep fighting', 'semangat', 'spirit',
            'bangkit', 'rise', 'rise up', 'comeback', 'kembali',
            
            # Support
            'dukung', 'support', 'mendukung', 'supporting', 'dukungan',
            'tetap dukung', 'always support', 'setia', 'loyal',
            'fans sejati', 'true fans', 'garuda', 'indonesia',
            
            # Future hope
            'akan lebih baik', 'will be better', 'pasti membaik',
            'next time', 'lain kali', 'kedepan', 'future', 'masa depan'
        ],
        'value': 'MEDIUM',
        'weight': 0.9,
        'layer': 'constructiveness'
    }
}

# ============================================================
# CONFIGURATION METADATA
# ============================================================
CONFIG_METADATA = {
    'version': '2.0',
    'framework_name': 'Optimized 5-Layer Sentiment Framework',
    'total_layers': 5,
    'total_categories': 18,  # Down from 34!
    'focus': 'Actionable insights & Real problems',
    'designed_for': 'Indonesia World Cup Failure Analysis',
    'date_created': '2025-11-24',
    
    'improvements_from_v1': [
        'Reduced from 34 to 18 categories (47% reduction)',
        'Removed overlapping categories',
        'Eliminated categories with <10 samples',
        'Added clear action points for each category',
        'Organized by actionability and priority',
        'Focus on WHO, WHY, WHEN, HOW'
    ],
    
    'layer_purposes': {
        'Layer 1 (Core Sentiment)': 'WHAT feeling? - Basic emotion classification',
        'Layer 2 (Target Kritik)': 'WHO to blame? - Responsibility identification',
        'Layer 3 (Root Cause)': 'WHY failed? - Problem diagnosis',
        'Layer 4 (Time Perspective)': 'WHEN to fix? - Solution timeline',
        'Layer 5 (Constructiveness)': 'HOW valuable? - Feedback quality'
    },
    
    'key_insights': {
        'top_3_categories_expected': [
            'negative + pssi_management + systemic_structural',
            'negative + coaching_staff + tactical_strategic',
            'negative + players + technical_skill'
        ],
        'actionable_for_stakeholders': {
            'PSSI': 'Layer 2 (Target) + Layer 3 (Root Cause) + Layer 4 (Timeline)',
            'Coaching Staff': 'Layer 3 (Tactical/Technical issues) + Layer 4 (Immediate actions)',
            'Media/Analyst': 'Layer 5 (Constructiveness filter) to find valuable insights'
        }
    }
}

# ============================================================
# COMBINED LAYERS FOR LABELING
# ============================================================
ALL_CATEGORIES = {
    **CORE_SENTIMENT,
    **TARGET_KRITIK,
    **ROOT_CAUSE,
    **TIME_PERSPECTIVE,
    **CONSTRUCTIVENESS
}

# Export for use in other modules
__all__ = [
    'CORE_SENTIMENT',
    'TARGET_KRITIK',
    'ROOT_CAUSE',
    'TIME_PERSPECTIVE',
    'CONSTRUCTIVENESS',
    'ALL_CATEGORIES',
    'CONFIG_METADATA'
]
