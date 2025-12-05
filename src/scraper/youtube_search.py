"""
YouTube Video Search Module for 9-Layer Sentiment Analysis

This module provides functionality to search YouTube videos related to
Indonesia's World Cup qualification failure using YouTube Data API v3.
"""

import os
import time
import json
import logging
from typing import List, Dict, Optional
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config.api_config import (
    YOUTUBE_API_KEY, YOUTUBE_API_VERSION, YOUTUBE_API_SERVICE_NAME,
    SEARCH_QUERIES, SEARCH_PARAMS, RATE_LIMIT_DELAY, RETRY_ATTEMPTS,
    RETRY_DELAY, BACKOFF_FACTOR, MAX_CONSECUTIVE_ERRORS
)

class YouTubeSearcher:
    """
    YouTube Video Searcher for Indonesia World Cup Failure Analysis
    
    This class handles searching YouTube videos related to Indonesia's
    failure to qualify for the World Cup using multiple search queries.
    """
    
    def __init__(self):
        """Initialize YouTube API client and logging"""
        self.youtube = build(
            YOUTUBE_API_SERVICE_NAME,
            YOUTUBE_API_VERSION,
            developerKey=YOUTUBE_API_KEY
        )
        self.logger = self._setup_logger()
        self.consecutive_errors = 0
        
    def _setup_logger(self) -> logging.Logger:
        """Setup logging configuration"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def search_videos(self, query: str, max_results: int = 50) -> List[Dict]:
        """
        Search YouTube videos for a specific query
        
        Args:
            query (str): Search query string
            max_results (int): Maximum number of results to return
            
        Returns:
            List[Dict]: List of video information
        """
        videos = []
        
        try:
            search_params = SEARCH_PARAMS.copy()
            search_params['q'] = query
            search_params['maxResults'] = max_results
            
            self.logger.info(f"Searching videos for query: {query}")
            
            # Execute search with retry logic
            for attempt in range(RETRY_ATTEMPTS):
                try:
                    response = self.youtube.search().list(**search_params).execute()
                    videos = response.get('items', [])
                    
                    self.logger.info(f"Found {len(videos)} videos for query: {query}")
                    self.consecutive_errors = 0  # Reset error counter on success
                    break
                    
                except HttpError as e:
                    self.logger.error(f"HTTP Error on attempt {attempt + 1}: {e}")
                    if attempt < RETRY_ATTEMPTS - 1:
                        time.sleep(RETRY_DELAY * (BACKOFF_FACTOR ** attempt))
                    else:
                        raise e
                        
        except Exception as e:
            self.logger.error(f"Error searching videos for query '{query}': {e}")
            self.consecutive_errors += 1
            
        return videos
    
    def search_all_queries(self) -> Dict[str, List[Dict]]:
        """
        Search all predefined queries related to Indonesia World Cup failure
        
        Returns:
            Dict[str, List[Dict]]: Dictionary mapping queries to video lists
        """
        all_videos = {}
        
        for query in SEARCH_QUERIES:
            if self.consecutive_errors >= MAX_CONSECUTIVE_ERRORS:
                self.logger.error("Too many consecutive errors. Stopping search.")
                break
                
            videos = self.search_videos(query)
            all_videos[query] = videos
            
            # Rate limiting between requests
            time.sleep(RATE_LIMIT_DELAY)
            
        return all_videos
    
    def get_video_details(self, video_ids: List[str]) -> List[Dict]:
        """
        Get detailed information for specific videos
        
        Args:
            video_ids (List[str]): List of video IDs
            
        Returns:
            List[Dict]: List of detailed video information
        """
        videos_details = []
        
        try:
            # Process in batches of 50 (API limit)
            batch_size = 50
            for i in range(0, len(video_ids), batch_size):
                batch_ids = video_ids[i:i + batch_size]
                
                self.logger.info(f"Getting details for {len(batch_ids)} videos")
                
                response = self.youtube.videos().list(
                    part='snippet,statistics,contentDetails',
                    id=','.join(batch_ids)
                ).execute()
                
                videos_details.extend(response.get('items', []))
                
                # Rate limiting between batches
                if i + batch_size < len(video_ids):
                    time.sleep(RATE_LIMIT_DELAY)
                    
        except Exception as e:
            self.logger.error(f"Error getting video details: {e}")
            
        return videos_details
    
    def filter_videos_by_criteria(self, videos: List[Dict]) -> List[Dict]:
        """
        Filter videos based on specific criteria
        
        Args:
            videos (List[Dict]): List of video information
            
        Returns:
            List[Dict]: Filtered list of videos
        """
        filtered_videos = []
        
        for video in videos:
            try:
                # Extract video information
                snippet = video.get('snippet', {})
                statistics = video.get('statistics', {})
                content_details = video.get('contentDetails', {})
                
                # Apply filters
                if self._meets_criteria(snippet, statistics, content_details):
                    filtered_videos.append(video)
                    
            except Exception as e:
                self.logger.error(f"Error filtering video {video.get('id', 'unknown')}: {e}")
                
        return filtered_videos
    
    def _meets_criteria(self, snippet: Dict, statistics: Dict, content_details: Dict) -> bool:
        """
        Check if video meets filtering criteria
        
        Args:
            snippet (Dict): Video snippet information
            statistics (Dict): Video statistics
            content_details (Dict): Video content details
            
        Returns:
            bool: True if video meets criteria
        """
        try:
            # View count filter (minimum 10,000 views)
            view_count = int(statistics.get('viewCount', 0))
            if view_count < 10000:
                return False
                
            # Comment count filter (minimum 100 comments)
            comment_count = int(statistics.get('commentCount', 0))
            if comment_count < 100:
                return False
                
            # Duration filter (4-20 minutes)
            duration = content_details.get('duration', '')
            if not self._is_valid_duration(duration):
                return False
                
            # Language filter (Indonesian)
            language = snippet.get('defaultLanguage', '')
            if language and not self._is_indonesian_language(language):
                return False
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error checking video criteria: {e}")
            return False
    
    def _is_valid_duration(self, duration: str) -> bool:
        """
        Check if video duration is within acceptable range (4-20 minutes)
        
        Args:
            duration (str): ISO 8601 duration string
            
        Returns:
            bool: True if duration is valid
        """
        try:
            # Parse ISO 8601 duration (PT4M30S format)
            import re
            match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
            if not match:
                return False
                
            hours = int(match.group(1) or 0)
            minutes = int(match.group(2) or 0)
            seconds = int(match.group(3) or 0)
            
            total_seconds = hours * 3600 + minutes * 60 + seconds
            total_minutes = total_seconds / 60
            
            return 4 <= total_minutes <= 20
            
        except Exception:
            return False
    
    def _is_indonesian_language(self, language: str) -> bool:
        """
        Check if language is Indonesian
        
        Args:
            language (str): Language code
            
        Returns:
            bool: True if language is Indonesian
        """
        indonesian_codes = ['id', 'in', 'indonesian']
        return language.lower() in indonesian_codes
    
    def save_search_results(self, videos: Dict[str, List[Dict]], filename: str = "data/raw/videos.json"):
        """
        Save search results to JSON file
        
        Args:
            videos (Dict[str, List[Dict]]): Search results
            filename (str): Output filename
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            # Save to JSON file
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(videos, f, indent=2, ensure_ascii=False)
                
            self.logger.info(f"Saved search results to {filename}")
            
        except Exception as e:
            self.logger.error(f"Error saving search results: {e}")
    
    def get_search_summary(self, videos: Dict[str, List[Dict]]) -> Dict:
        """
        Get summary of search results
        
        Args:
            videos (Dict[str, List[Dict]]): Search results
            
        Returns:
            Dict: Summary statistics
        """
        def _video_id_generator():
            for video_list in videos.values():
                for video in video_list:
                    yield self._extract_video_id(video)

        summary = {
            'total_queries': len(videos),
            'total_videos': sum(len(video_list) for video_list in videos.values()),
            'videos_per_query': {query: len(video_list) for query, video_list in videos.items()},
            'unique_video_count': len({video_id for video_id in _video_id_generator() if video_id})
        }
        
        return summary

    def _extract_video_id(self, video: Dict) -> str:
        """
        Extract the video ID from a search result entry.

        Args:
            video (Dict): Video metadata entry from the API response

        Returns:
            str: The extracted video ID if available, otherwise an empty string
        """
        video_id = video.get('id', '')

        if isinstance(video_id, dict):
            return (
                video_id.get('videoId')
                or video_id.get('channelId')
                or video_id.get('playlistId')
                or ''
            )

        return video_id


def main():
    """
    Main function to test YouTube search functionality
    """
    searcher = YouTubeSearcher()
    
    # Search all queries
    all_videos = searcher.search_all_queries()
    
    # Get unique video IDs
    all_video_ids = list({
        searcher._extract_video_id(video)
        for video_list in all_videos.values()
        for video in video_list
        if searcher._extract_video_id(video)
    })
    
    # Get detailed information
    detailed_videos = searcher.get_video_details(all_video_ids)
    
    # Filter videos
    filtered_videos = searcher.filter_videos_by_criteria(detailed_videos)
    
    # Save results
    searcher.save_search_results(all_videos)
    
    # Print summary
    summary = searcher.get_search_summary(all_videos)
    print("Search Summary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()