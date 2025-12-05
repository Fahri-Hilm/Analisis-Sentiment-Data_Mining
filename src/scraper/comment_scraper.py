"""
YouTube Comment Scraper for 9-Layer Sentiment Analysis

This module provides functionality to scrape comments from YouTube videos
related to Indonesia's World Cup qualification failure.
"""

import os
import time
import json
import pandas as pd
import logging
from typing import List, Dict, Optional, Generator
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config.api_config import (
    YOUTUBE_API_KEY, YOUTUBE_API_VERSION, YOUTUBE_API_SERVICE_NAME,
    COMMENT_PARAMS, RATE_LIMIT_DELAY, RETRY_ATTEMPTS, RETRY_DELAY,
    BACKOFF_FACTOR, TARGET_COMMENTS, COMMENTS_PER_VIDEO_MIN,
    QUOTA_TRACKING, QUOTA_USAGE_FILE, BACKUP_ENABLED,
    BACKUP_INTERVAL, BACKUP_PATH
)

class CommentScraper:
    """
    YouTube Comment Scraper for Indonesia World Cup Failure Analysis
    
    This class handles scraping comments from YouTube videos with
    quota management, progress tracking, and backup functionality.
    """
    
    def __init__(self):
        """Initialize YouTube API client and logging"""
        self.youtube = build(
            YOUTUBE_API_SERVICE_NAME,
            YOUTUBE_API_VERSION,
            developerKey=YOUTUBE_API_KEY
        )
        self.logger = self._setup_logger()
        self.quota_used = 0
        self.comments_collected = 0
        self.videos_processed = 0
        self.load_quota_usage()
        
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
    
    def load_quota_usage(self):
        """Load quota usage from file"""
        try:
            if os.path.exists(QUOTA_USAGE_FILE):
                with open(QUOTA_USAGE_FILE, 'r') as f:
                    data = json.load(f)
                    self.quota_used = data.get('quota_used', 0)
                    self.logger.info(f"Loaded quota usage: {self.quota_used}")
        except Exception as e:
            self.logger.error(f"Error loading quota usage: {e}")
            self.quota_used = 0
    
    def save_quota_usage(self):
        """Save quota usage to file"""
        try:
            os.makedirs(os.path.dirname(QUOTA_USAGE_FILE), exist_ok=True)
            with open(QUOTA_USAGE_FILE, 'w') as f:
                json.dump({
                    'quota_used': self.quota_used,
                    'comments_collected': self.comments_collected,
                    'videos_processed': self.videos_processed,
                    'last_updated': time.time()
                }, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving quota usage: {e}")
    
    def get_video_comments(self, video_id: str, max_comments: int = 1000) -> List[Dict]:
        """
        Get all comments for a specific video
        
        Args:
            video_id (str): YouTube video ID
            max_comments (int): Maximum number of comments to collect
            
        Returns:
            List[Dict]: List of comment data
        """
        comments = []
        next_page_token = None
        
        try:
            self.logger.info(f"Collecting comments for video: {video_id}")
            
            while len(comments) < max_comments:
                # Check quota before making request
                if self.quota_used >= 10000 - QUOTA_TRACKING['comment_list_cost']:
                    self.logger.warning("Approaching quota limit. Stopping comment collection.")
                    break
                
                # Prepare request parameters
                params = COMMENT_PARAMS.copy()
                params['videoId'] = video_id
                params['maxResults'] = min(100, max_comments - len(comments))
                
                if next_page_token:
                    params['pageToken'] = next_page_token
                
                # Execute request with retry logic
                for attempt in range(RETRY_ATTEMPTS):
                    try:
                        response = self.youtube.commentThreads().list(**params).execute()
                        
                        # Update quota usage
                        self.quota_used += QUOTA_TRACKING['comment_list_cost']
                        
                        # Process comments
                        items = response.get('items', [])
                        for item in items:
                            comment_data = self._extract_comment_data(item, video_id)
                            if comment_data:
                                comments.append(comment_data)
                        
                        # Check for next page
                        next_page_token = response.get('nextPageToken')
                        if not next_page_token:
                            break
                        
                        self.logger.info(f"Collected {len(comments)} comments so far...")
                        break
                        
                    except HttpError as e:
                        self.logger.error(f"HTTP Error on attempt {attempt + 1}: {e}")
                        if attempt < RETRY_ATTEMPTS - 1:
                            time.sleep(RETRY_DELAY * (BACKOFF_FACTOR ** attempt))
                        else:
                            raise e
                
                # Rate limiting between requests
                time.sleep(RATE_LIMIT_DELAY)
                
                # Backup comments if enabled
                if BACKUP_ENABLED and len(comments) % BACKUP_INTERVAL == 0:
                    self._backup_comments(comments, video_id)
            
            self.logger.info(f"Collected {len(comments)} comments for video {video_id}")
            
        except Exception as e:
            self.logger.error(f"Error collecting comments for video {video_id}: {e}")
        
        return comments
    
    def _extract_comment_data(self, item: Dict, video_id: str) -> Optional[Dict]:
        """
        Extract relevant data from comment item
        
        Args:
            item (Dict): Comment item from YouTube API
            video_id (str): Video ID
            
        Returns:
            Optional[Dict]: Extracted comment data or None if invalid
        """
        try:
            snippet = item.get('snippet', {})
            top_level_comment = snippet.get('topLevelComment', {})
            comment_snippet = top_level_comment.get('snippet', {})
            
            # Extract comment text
            text = comment_snippet.get('textDisplay', '').strip()
            if not text or len(text) < 10:  # Skip short/empty comments
                return None
            
            # Extract metadata
            comment_data = {
                'comment_id': item.get('id', ''),
                'video_id': video_id,
                'text': text,
                'author': comment_snippet.get('authorDisplayName', ''),
                'author_channel_id': comment_snippet.get('authorChannelId', ''),
                'like_count': comment_snippet.get('likeCount', 0),
                'reply_count': snippet.get('totalReplyCount', 0),
                'published_at': comment_snippet.get('publishedAt', ''),
                'updated_at': comment_snippet.get('updatedAt', ''),
                'is_reply': False,
                'parent_comment_id': None
            }
            
            return comment_data
            
        except Exception as e:
            self.logger.error(f"Error extracting comment data: {e}")
            return None
    
    def get_comment_replies(self, parent_comment_id: str, max_replies: int = 10) -> List[Dict]:
        """
        Get replies for a specific comment
        
        Args:
            parent_comment_id (str): Parent comment ID
            max_replies (int): Maximum number of replies to collect
            
        Returns:
            List[Dict]: List of reply data
        """
        replies = []
        
        try:
            params = {
                'part': 'snippet',
                'parentId': parent_comment_id,
                'maxResults': max_replies,
                'textFormat': 'plainText'
            }
            
            response = self.youtube.comments().list(**params).execute()
            self.quota_used += QUOTA_TRACKING['comment_list_cost']
            
            items = response.get('items', [])
            for item in items:
                reply_data = self._extract_reply_data(item)
                if reply_data:
                    replies.append(reply_data)
            
        except Exception as e:
            self.logger.error(f"Error getting replies for comment {parent_comment_id}: {e}")
        
        return replies
    
    def _extract_reply_data(self, item: Dict) -> Optional[Dict]:
        """
        Extract relevant data from reply item
        
        Args:
            item (Dict): Reply item from YouTube API
            
        Returns:
            Optional[Dict]: Extracted reply data or None if invalid
        """
        try:
            snippet = item.get('snippet', {})
            
            text = snippet.get('textDisplay', '').strip()
            if not text or len(text) < 10:
                return None
            
            reply_data = {
                'comment_id': item.get('id', ''),
                'video_id': snippet.get('videoId', ''),
                'text': text,
                'author': snippet.get('authorDisplayName', ''),
                'author_channel_id': snippet.get('authorChannelId', ''),
                'like_count': snippet.get('likeCount', 0),
                'published_at': snippet.get('publishedAt', ''),
                'updated_at': snippet.get('updatedAt', ''),
                'is_reply': True,
                'parent_comment_id': snippet.get('parentId', '')
            }
            
            return reply_data
            
        except Exception as e:
            self.logger.error(f"Error extracting reply data: {e}")
            return None
    
    def scrape_videos_comments(self, video_ids: List[str]) -> List[Dict]:
        """
        Scrape comments from multiple videos
        
        Args:
            video_ids (List[str]): List of video IDs
            
        Returns:
            List[Dict]: List of all comments
        """
        all_comments = []
        
        for i, video_id in enumerate(video_ids):
            self.logger.info(f"Processing video {i+1}/{len(video_ids)}: {video_id}")
            
            # Check if we've collected enough comments
            if self.comments_collected >= TARGET_COMMENTS:
                self.logger.info(f"Target comments ({TARGET_COMMENTS}) reached. Stopping.")
                break
            
            # Get comments for this video
            video_comments = self.get_video_comments(video_id)
            
            # Filter videos with minimum comments
            if len(video_comments) >= COMMENTS_PER_VIDEO_MIN:
                all_comments.extend(video_comments)
                self.comments_collected += len(video_comments)
                self.videos_processed += 1
            else:
                self.logger.info(f"Video {video_id} has only {len(video_comments)} comments (minimum: {COMMENTS_PER_VIDEO_MIN})")
            
            # Save quota usage
            self.save_quota_usage()
            
            # Progress update
            progress = (self.comments_collected / TARGET_COMMENTS) * 100
            self.logger.info(f"Progress: {progress:.1f}% ({self.comments_collected}/{TARGET_COMMENTS} comments)")
        
        return all_comments
    
    def _backup_comments(self, comments: List[Dict], video_id: str):
        """
        Backup comments to file
        
        Args:
            comments (List[Dict]): Comments to backup
            video_id (str): Video ID for filename
        """
        try:
            os.makedirs(BACKUP_PATH, exist_ok=True)
            backup_file = os.path.join(BACKUP_PATH, f"comments_{video_id}_{int(time.time())}.json")
            
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(comments, f, indent=2, ensure_ascii=False)
                
            self.logger.info(f"Backed up {len(comments)} comments to {backup_file}")
            
        except Exception as e:
            self.logger.error(f"Error backing up comments: {e}")
    
    def save_comments_to_csv(self, comments: List[Dict], filename: str = "data/raw/comments.csv"):
        """
        Save comments to CSV file
        
        Args:
            comments (List[Dict]): Comments to save
            filename (str): Output filename
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            # Convert to DataFrame
            df = pd.DataFrame(comments)
            
            # Save to CSV
            df.to_csv(filename, index=False, encoding='utf-8')
            
            self.logger.info(f"Saved {len(comments)} comments to {filename}")
            
        except Exception as e:
            self.logger.error(f"Error saving comments to CSV: {e}")
    
    def get_collection_summary(self) -> Dict:
        """
        Get summary of comment collection
        
        Returns:
            Dict: Collection statistics
        """
        return {
            'total_comments': self.comments_collected,
            'videos_processed': self.videos_processed,
            'quota_used': self.quota_used,
            'quota_remaining': 10000 - self.quota_used,
            'target_comments': TARGET_COMMENTS,
            'progress_percentage': (self.comments_collected / TARGET_COMMENTS) * 100 if TARGET_COMMENTS > 0 else 0,
            'avg_comments_per_video': self.comments_collected / self.videos_processed if self.videos_processed > 0 else 0
        }


def main():
    """
    Main function to test comment scraping functionality
    """
    scraper = CommentScraper()
    
    # Example video IDs (in real implementation, these would come from search results)
    video_ids = [
        "dQw4w9WgXcQ",  # Example video ID
        "jNQXAC9IVRw",  # Example video ID
        # Add more video IDs as needed
    ]
    
    # Scrape comments
    comments = scraper.scrape_videos_comments(video_ids)
    
    # Save to CSV
    scraper.save_comments_to_csv(comments)
    
    # Print summary
    summary = scraper.get_collection_summary()
    print("Collection Summary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()