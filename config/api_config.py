"""
YouTube API Configuration for 9-Layer Sentiment Analysis

This module contains configuration for YouTube Data API v3
including API key, quota management, and search parameters.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# YouTube API Configuration
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "AIzaSyCpDA7_f0dRaYkctBUeSrgxw39Fr7eQlio")
YOUTUBE_API_VERSION = "v3"
YOUTUBE_API_SERVICE_NAME = "youtube"

# API Quota Management
DAILY_QUOTA_LIMIT = 10000  # Default YouTube API quota
QUOTA_BUFFER = 2000         # Buffer untuk safety
MAX_REQUESTS_PER_MINUTE = 100
RATE_LIMIT_DELAY = 0.6      # Seconds between requests

# Search Parameters for Indonesia World Cup Failure - EXPANDED for 20K+ comments
SEARCH_QUERIES = [
    # Core queries (original)
    "kegagalan Indonesia Piala Dunia",
    "Indonesia gagal lolos Piala Dunia", 
    "Timnas Indonesia gagal Piala Dunia",
    "Indonesia tidak lolos Piala Dunia",
    "Kualifikasi Piala Dunia Indonesia gagal",
    "Indonesia gagal kualifikasi Piala Dunia",
    
    # Specific opponent matches
    "Indonesia vs Arab Saudi Piala Dunia",
    "Indonesia kalah Arab Saudi kualifikasi",
    "Indonesia vs Jepang Piala Dunia",
    "Indonesia vs Australia kualifikasi Piala Dunia",
    "Indonesia vs Bahrain Piala Dunia",
    "Indonesia vs China Piala Dunia kualifikasi",
    
    # Coach/Management related
    "Shin Tae Yong gagal Piala Dunia",
    "STY Indonesia gagal lolos",
    "Patrick Kluivert Indonesia gagal",
    "Klivert pelatih Indonesia gagal",
    "Kritik pelatih timnas Indonesia",
    "PSSI gagal Piala Dunia",
    "Erick Thohir PSSI Piala Dunia",
    "Manajemen PSSI buruk",
    
    # Emotional/reaction queries
    "sedih Indonesia gagal Piala Dunia",
    "kecewa timnas Indonesia",
    "malu Indonesia tidak lolos Piala Dunia",
    "Indonesia hancur Piala Dunia",
    "reaksi Indonesia gagal lolos Piala Dunia",
    
    # Analysis/discussion queries
    "analisis Indonesia gagal Piala Dunia",
    "penyebab Indonesia gagal lolos",
    "evaluasi timnas Indonesia Piala Dunia",
    "kenapa Indonesia tidak lolos Piala Dunia",
    "masalah sepak bola Indonesia",
    "solusi timnas Indonesia Piala Dunia",
    
    # Player-specific
    "pemain timnas Indonesia Piala Dunia",
    "performa pemain Indonesia gagal",
    "Egy Maulana Piala Dunia",
    "Marselino Ferdinan timnas",
    "naturalisasi gagal Indonesia",
    
    # Future/hope queries
    "masa depan timnas Indonesia",
    "harapan Piala Dunia Indonesia 2026",
    "Indonesia Piala Dunia 2034",
    "pembinaan sepak bola Indonesia"
]

SEARCH_PARAMS = {
    'part': 'snippet',
    'type': 'video',
    'maxResults': 50,
    'order': 'relevance',
    'publishedAfter': '2023-01-01T00:00:00Z',
    'relevanceLanguage': 'id',
    'videoDuration': 'medium',  # 4-20 menit
    'videoDefinition': 'any'
}

# Comment Extraction Parameters
COMMENT_PARAMS = {
    'part': 'snippet',
    'maxResults': 100,
    'order': 'relevance',
    'textFormat': 'plainText'
}

# Data Collection Targets
TARGET_COMMENTS = 10000
MAX_VIDEOS_TO_PROCESS = 100
COMMENTS_PER_VIDEO_MIN = 50

# Quota Tracking
QUOTA_TRACKING = {
    'search_cost': 100,        # Cost per search request
    'comment_list_cost': 1,    # Cost per comment list request
    'video_details_cost': 1    # Cost per video details request
}

# Quota Usage Tracking
QUOTA_USAGE_FILE = "data/quota_usage.json"
QUOTA_RESET_TIME = "00:00:00"  # Daily reset time

# Rate Limiting
RETRY_ATTEMPTS = 3
RETRY_DELAY = 1.0  # Seconds
BACKOFF_FACTOR = 2.0

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FILE = "logs/api_usage.log"

# Error Handling
MAX_CONSECUTIVE_ERRORS = 5
ERROR_COOLDOWN = 300  # 5 minutes

# Data Storage Paths
RAW_DATA_PATH = "data/raw/videos.json"
COMMENTS_DATA_PATH = "data/raw/comments.csv"
PROCESSED_DATA_PATH = "data/processed/"

# Backup Configuration
BACKUP_ENABLED = True
BACKUP_INTERVAL = 1000  # Every 1000 comments
BACKUP_PATH = "data/backups/"