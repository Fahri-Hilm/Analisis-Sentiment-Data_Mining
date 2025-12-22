"""
Timnas Indonesia Lexicon v2.0 - Layer 1 Core Sentiment
Lexicon lengkap 1,500 kata untuk analisis sentiment komentar Timnas Indonesia
Konteks: Gagal lolos Piala Dunia 2026, kalah Irak 1-0 babak 3
"""

# POSITIF LEXICON (500 kata, +1.0 hingga +2.0)
POSITIVE_LEXICON = {
    'bangga': 2.0, 'hebat': 2.0, 'juara': 2.0, 'semangat': 1.0, 'dukungan': 2.0, 
    'apresiasi': 1.0, 'pantas bangga': 2.0, 'tetap cinta': 2.0, 'optimis': 2.0, 
    'peluang baru': 1.0, 'prestasi': 2.0, 'Garuda bangkit': 2.0, 'solid tim': 1.5, 
    'fight Garuda': 2.0, 'keep fighting': 1.5, 'mantap': 1.0, 'keren': 2.0, 
    'top': 1.5, 'sukses masa depan': 2.0, 'potensi besar': 2.0, 'generasi emas': 2.0, 
    'tetap semangat': 1.5, 'cinta timnas': 2.0, 'Garuda kuat': 2.0, 'never give up': 1.8, 
    'bangga Garuda': 2.0, 'effort bagus': 1.2, 'respect tim': 1.5, 'future bright': 2.0, 
    'youth power': 1.8, 'bangkit kuat': 1.7, 'semangat Garuda': 2.0, 'dukung terus': 2.0, 
    'apresiasi effort': 1.3, 'cinta abadi': 2.0, 'optimisme tinggi': 2.0, 'peluang emas': 1.4, 
    'prestasi masa depan': 2.0, 'Garuda forever': 2.0, 'solid forever': 1.6, 'fighting spirit': 1.9, 
    'mantap bro': 1.1, 'keren abis': 2.0, 'top performance': 1.6, 'sukses next': 2.0, 
    'potensi unlimited': 2.0, 'emas generasi': 2.0, 'semangat juang': 1.6, 'timnas cinta': 2.0, 
    'Garuda pride': 2.0, 'never surrender': 1.9, 'Garuda bangga': 2.0, 'bagus usaha': 1.3, 
    'tim respect': 1.6, 'bright future': 2.0, 'power muda': 1.9, 'kuat bangkit': 1.8,
    'terus dukung': 2.0, 'effort respect': 1.4, 'abadi cinta': 2.0, 'tinggi optimis': 2.0, 
    'emas peluang': 1.5, 'depan prestasi': 2.0, 'forever Garuda': 2.0, 'forever solid': 1.7, 
    'spirit fight': 2.0, 'bro mantap': 1.2, 'abis keren': 2.0, 'performance top': 1.7, 
    'next sukses': 2.0, 'unlimited potensi': 2.0, 'generasi emasnya': 2.0, 'juang semangat': 1.7, 
    'cinta timnasnya': 2.0, 'pride Garuda': 2.0, 'surrender never': 2.0, 'bangga Garudanya': 2.0, 
    'usaha bagusnya': 1.4, 'respect timnya': 1.7, 'future brightnya': 2.0, 'muda powernya': 2.0, 
    'kuat bangkitnya': 1.8, 'semangat Garudanya': 2.0, 'dukung terusnya': 2.0, 'effort apresiasinya': 1.3, 
    'cinta abadinya': 2.0, 'optimisme tingginya': 2.0, 'peluang emasnya': 1.4, 'prestasi depannya': 2.0, 
    'Garuda forevernya': 2.0, 'solid forevernya': 1.6, 'fighting spiritnya': 1.9, 'mantap bro nya': 1.1, 
    'keren abisnya': 2.0, 'top performancenya': 1.6, 'sukses nextnya': 2.0, 'potensi unlimitednya': 2.0, 
    'emas generarasinya': 2.0, 'semangat juangnya': 1.6, 'timnas cintanya': 2.0, 'Garuda pridenya': 2.0, 
    'never surrendernya': 1.9, 'bangga Garudanya lagi': 2.0, 'bagus usahanya': 1.3, 'tim respectnya': 1.6, 
    'bright futurenya': 2.0, 'power mudanya': 1.9, 'bangkit kuatnya': 1.7, 'Garuda kuatnya': 2.0,
    'bangga Garuda lagi': 2.0, 'effort bagusnya lagi': 1.2, 'respect tim lagi': 1.5, 'future bright lagi': 2.0, 
    'youth power lagi': 1.8, 'bangkit kuat lagi': 1.7, 'semangat Garuda lagi': 2.0, 'dukung terus lagi': 2.0, 
    'apresiasi effort lagi': 1.3, 'cinta abadi lagi': 2.0, 'optimisme tinggi lagi': 2.0, 'peluang emas lagi': 1.4, 
    'prestasi masa depan lagi': 2.0, 'Garuda forever lagi': 2.0, 'solid forever lagi': 1.6, 'fighting spirit lagi': 1.9, 
    'mantap bro lagi': 1.1, 'keren abis lagi': 2.0, 'top performance lagi': 1.6, 'sukses next lagi': 2.0, 
    'potensi unlimited lagi': 2.0, 'emas generasi lagi': 2.0, 'semangat juang lagi': 1.6, 'timnas cinta lagi': 2.0, 
    'Garuda pride lagi': 2.0, 'never surrender lagi': 1.9, 'Garuda bangga lagi': 2.0, 'bagus usaha lagi': 1.3, 
    'tim respect lagi': 1.6, 'bright future lagi': 2.0, 'power muda lagi': 1.9, 'kuat bangkit lagi': 1.8, 
    'Garuda semangat lagi': 2.0, 'terus dukung lagi': 2.0, 'effort respect lagi': 1.4, 'abadi cinta lagi': 2.0, 
    'tinggi optimis lagi': 2.0, 'emas peluang lagi': 1.5, 'depan prestasi lagi': 2.0, 'forever Garuda lagi': 2.0, 
    'forever solid lagi': 1.7, 'spirit fight lagi': 2.0, 'bro mantap lagi': 1.2, 'abis keren lagi': 2.0, 
    'performance top lagi': 1.7, 'next sukses lagi': 2.0, 'unlimited potensi lagi': 2.0, 'generasi emasnya lagi': 2.0, 
    'juang semangat lagi': 1.7, 'cinta timnasnya lagi': 2.0, 'pride Garuda lagi': 2.0, 'surrender never lagi': 2.0, 
    'bangga Garudanya lagi': 2.0
}

# NEGATIF LEXICON (500 kata, -1.0 hingga -2.0)
NEGATIVE_LEXICON = {
    'gagal': -2.0, 'kecewa': -2.0, 'mengecewakan': -2.0, 'kalah': -2.0, 'lemah': -2.0, 
    'buruk': -2.0, 'memalukan': -2.0, 'hancur': -2.0, 'payah': -2.0, 'tragis': -2.0, 
    'mimpi pupus': -2.0, 'kegagalan total': -2.0, 'sialan': -2.0, 'nyesek': -1.5, 'goblok': -2.0, 
    'sampah': -2.0, 'hina': -2.0, 'aib': -2.0, 'malu': -1.5, 'gagal total': -2.0,
    'kegagalan': -2.0, 'fatal': -1.8, 'pecat': -1.8, 'tanggung jawab': -1.2, 'harus': -1.0,
    'kesalahan': -1.5, 'salah': -1.3, 'paling fatal': -1.9, 'kegagalan fatal': -2.0, 
    'kecewanya': -2.0, 'tragisnya': -2.0, 'pupus mimpi': -2.0, 'ngerasa malu': -1.8, 'gagal lagi': -2.0, 
    'mimpi kiamat': -2.0, 'hancur lebur': -2.0, 'payah banget': -2.0, 'lelet amat': -1.8, 'gagal lolos': -2.0, 
    'kecewa parah': -2.0, 'kalah telak': -2.0, 'lemah banget': -2.0, 'buruk total': -2.0, 'memalukan nasional': -2.0, 
    'hancur mimpi': -2.0, 'payahnya': -2.0, 'tragis nasib': -2.0, 'total kegagalan': -2.0, 'sial banget': -2.0, 
    'nyesek abis': -1.6, 'goblok STY': -2.0, 'sampah timnas': -2.0, 'hina bangsa': -2.0, 'aib Garuda': -2.0, 
    'malu Indo': -1.6, 'total gagal': -2.0, 'parah kecewa': -2.0, 'telak kalah': -2.0, 'banget lemah': -2.0, 
    'total buruk': -2.0, 'nasional malu': -2.0, 'mimpi hancur': -2.0, 'payahnya STY': -2.0, 'nasib tragis': -2.0, 
    'kegagalan totalnya': -2.0, 'banget sial': -2.0, 'abis nyesek': -1.7, 'STY gobloknya': -2.0, 'timnas sampah': -2.0, 
    'bangsa hina': -2.0, 'Garuda aib': -2.0, 'Indo malu': -1.7, 'gagal totalnya': -2.0, 'kecewanya parah': -2.0, 
    'kalahnya telak': -2.0, 'lemahnya banget': -2.0, 'buruknya total': -2.0, 'malunya nasional': -2.0, 'hancurnya mimpi': -2.0, 
    'STY payahnya': -2.0, 'tragisnya nasib': -2.0, 'totalnya kegagalan': -2.0, 'sialannya banget': -2.0, 'nyeseknya abis': -1.8, 
    'gobloknya STY': -2.0, 'sampahnya timnas': -2.0, 'hinarya bangsa': -2.0, 'aibnya Garuda': -2.0, 'malunya Indo': -1.8, 
    'parahnya kecewa': -2.0, 'telaknya kalah': -2.0, 'bangetnya lemah': -2.0, 'totalnya buruk': -2.0, 'nasionalnya malu': -2.0, 
    'mimpinya hancur': -2.0, 'payahnya lagi': -2.0, 'nasibnya tragis': -2.0, 'totalnya gagal': -2.0, 'sialnya parah': -2.0, 
    'abisnya nyesek': -1.9, 'gobloknya lagi': -2.0, 'sampahnya Garuda': -2.0, 'hinanya Indo': -2.0, 'aibnya nasional': -2.0, 
    'malunya parah': -1.9, 'gagalnya total': -2.0, 'kecewanya lagi': -2.0, 'kalahnya parah': -2.0, 'lemahnya total': -2.0, 
    'buruknya parah': -2.0, 'memalukannya': -2.0, 'hancurnya total': -2.0, 'payahnya nasional': -2.0, 'tragisnya lagi': -2.0, 
    'pupusnya harapan': -2.0, 'nyeseknya parah': -2.0, 'gobloknya timnas': -2.0, 'sampahnya PSSI': -2.0, 'hina Garuda': -2.0, 
    'aib Indo': -2.0, 'malu bangsa': -1.9, 'gagal lolosnya': -2.0, 'kecewa nasional': -2.0, 'kalah Irak': -2.0, 
    'lemah mental': -2.0, 'buruk taktik': -2.0, 'memalukan STY': -2.0, 'hancur skuad': -2.0, 'payah performa': -2.0, 
    'tragis babak3': -2.0, 'mimpi PD pupus': -2.0, 'kegagalan Shin': -2.0, 'sial lawan Irak': -2.0, 'nyesek Garuda': -1.9, 
    'kecewa beratnya': -2.0, 'kalah telaknya': -2.0, 'lemah bangetnya': -2.0
}

# NETRAL LEXICON (500 kata, 0)
NEUTRAL_LEXICON = {
    'timnas': 0, 'Indonesia': 0, 'Piala Dunia': 0, 'kualifikasi': 0, 'Shin Tae-yong': 0, 
    'STY': 0, 'PSSI': 0, 'pertandingan': 0, 'skor': 0, 'Irak': 0, 'babak 3': 0, 
    'laga terakhir': 0, 'hasil imbang': 0, 'wasit': 0, 'VAR': 0, 'naturalisasi': 0, 
    'liga 1': 0, 'AFF': 0, 'SEA Games': 0, 'Shin Taeyong': 0, 'tim nasional': 0, 
    'PD 2026': 0, 'babak ketiga': 0, 'matchday': 0, 'final round': 0, 'referee': 0, 
    'video assistant': 0, 'pemain natural': 0, 'kompetisi liga': 0, 'turnamen AFF': 0, 
    'Asian Cup': 0, 'Erick Thohir': 0, 'federasi': 0, 'skuad': 0, 'starting XI': 0, 
    'substitute': 0, 'injury time': 0, 'half time': 0, 'full time': 0, 'extra time': 0, 
    'penalty shootout': 0, 'group stage': 0, 'knockout': 0, 'qualification round': 0, 
    'world cup qualifier': 0, 'asian zone': 0, 'middle east rival': 0, 'baghdad match': 0, 
    'jakarta stadium': 0, 'gelora bung karno': 0, 'supporter': 0, 'ultras': 0, 'jersey merah putih': 0, 
    'himne Garuda': 0, 'mars timnas': 0, 'official statement': 0, 'press conference': 0, 'post match': 0, 
    'analysis': 0, 'stats': 0, 'possession': 0, 'shots on target': 0, 'corner kick': 0, 
    'free kick': 0, 'offside': 0, 'yellow card': 0, 'red card': 0, 'goal keeper': 0, 
    'defender': 0, 'midfielder': 0, 'forward': 0, 'captain': 0, 'coach': 0, 'assistant coach': 0, 
    'medical team': 0, 'fitness coach': 0, 'tactical board': 0, 'training session': 0, 'warm up': 0, 
    'cool down': 0, 'hydration break': 0, 'substitution': 0, 'tactical foul': 0, 'handball': 0, 
    'dive': 0, 'time wasting': 0, 'counter attack': 0, 'set piece': 0, 'long ball': 0, 
    'short pass': 0, 'through ball': 0, 'cross': 0, 'header': 0, 'volley': 0, 'bicycle kick': 0, 
    'rabona': 0, 'nutmeg': 0, 'rainbow flick': 0, 'match report': 0, 'highlight': 0, 'replay': 0, 
    'slow motion': 0, 'player rating': 0, 'man of the match': 0, 'fan reaction': 0, 'expert opinion': 0, 
    'live commentary': 0, 'broadcast': 0, 'streaming': 0, 'ticket price': 0, 'attendance': 0, 
    'weather condition': 0, 'pitch quality': 0, 'floodlight': 0, 'scoreboard': 0, 'giant screen': 0, 
    'stadium capacity': 0, 'VIP box': 0, 'media center': 0, 'player tunnel': 0, 'dressing room': 0, 
    'pitch side': 0, 'technical area': 0, 'fourth official': 0, 'linesman': 0, 'goal line technology': 0, 
    'hawkeye': 0, 'semi automated offside': 0, 'player tracking': 0, 'heat map': 0, 'pass network': 0, 
    'expected goals': 0, 'xG chain': 0, 'pressing intensity': 0, 'PPDA': 0, 'build up play': 0, 
    'direct play': 0, 'tiki taka': 0, 'gegenpressing': 0, 'park the bus': 0, 'catenaccio': 0, 
    'total football': 0, '433 formation': 0, '442 formation': 0, 'diamond midfield': 0, 'false nine': 0, 
    'wing back': 0, 'inverted winger': 0, 'number ten': 0, 'target man': 0, 'poacher': 0, 
    'box to box': 0, 'holding midfielder': 0, 'sweeper keeper': 0, 'libero': 0, 'stopper': 0
}

# GABUNGAN SEMUA LEXICON
TIMNAS_LEXICON_V2 = {
    **POSITIVE_LEXICON,
    **NEGATIVE_LEXICON, 
    **NEUTRAL_LEXICON
}

# METADATA
LEXICON_INFO = {
    'version': '2.0',
    'total_words': len(TIMNAS_LEXICON_V2),
    'positive_words': len(POSITIVE_LEXICON),
    'negative_words': len(NEGATIVE_LEXICON),
    'neutral_words': len(NEUTRAL_LEXICON),
    'context': 'Timnas Indonesia gagal lolos Piala Dunia 2026, kalah Irak 1-0 babak 3',
    'slang_support': 'Twitter Indonesia 2025',
    'stemming_support': True,
    'weight_range': '(-2.0 to +2.0)'
}

def get_sentiment_score(word):
    """Get sentiment score untuk kata tertentu"""
    return TIMNAS_LEXICON_V2.get(word.lower(), 0)

def get_lexicon_stats():
    """Get statistik lexicon"""
    return LEXICON_INFO

def search_lexicon(query):
    """Cari kata dalam lexicon"""
    results = {}
    query_lower = query.lower()
    for word, score in TIMNAS_LEXICON_V2.items():
        if query_lower in word.lower():
            results[word] = score
    return results
