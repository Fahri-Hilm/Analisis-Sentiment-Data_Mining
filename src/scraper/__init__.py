"""
YouTube Scraper Module for 9-Layer Sentiment Analysis

This module provides functionality to scrape YouTube videos and comments
for sentiment analysis of Indonesia's World Cup qualification failure.
"""

from .youtube_search import YouTubeSearcher
from .comment_scraper import CommentScraper
from .api_manager import APIManager

__all__ = [
    "YouTubeSearcher",
    "CommentScraper", 
    "APIManager"
]