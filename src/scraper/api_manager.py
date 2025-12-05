"""
API Manager for 9-Layer Sentiment Analysis

This module provides API quota management, rate limiting,
and monitoring functionality for YouTube Data API v3.
"""

import os
import time
import json
import logging
from typing import Dict, Optional, Callable
from datetime import datetime, timedelta
from threading import Lock, Thread
from queue import Queue, Empty

from config.api_config import (
    DAILY_QUOTA_LIMIT, QUOTA_BUFFER, MAX_REQUESTS_PER_MINUTE,
    RATE_LIMIT_DELAY, QUOTA_TRACKING, QUOTA_USAGE_FILE,
    QUOTA_RESET_TIME, RETRY_ATTEMPTS, RETRY_DELAY,
    BACKOFF_FACTOR, MAX_CONSECUTIVE_ERRORS, ERROR_COOLDOWN
)

class APIManager:
    """
    API Manager for YouTube Data API v3
    
    This class manages API quota, rate limiting, and monitoring
    for YouTube Data API requests.
    """
    
    def __init__(self):
        """Initialize API manager with quota tracking"""
        self.quota_used = 0
        self.daily_quota_limit = DAILY_QUOTA_LIMIT
        self.quota_buffer = QUOTA_BUFFER
        self.requests_per_minute = 0
        self.minute_start_time = time.time()
        self.consecutive_errors = 0
        self.last_reset_time = self._get_last_reset_time()
        self.lock = Lock()
        self.logger = self._setup_logger()
        self.request_queue = Queue()
        self.monitoring_active = False
        
        # Load existing quota usage
        self.load_quota_usage()
        
        # Start monitoring thread
        self.start_monitoring()
    
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
    
    def _get_last_reset_time(self) -> datetime:
        """Get the last time quota was reset"""
        try:
            reset_time = datetime.strptime(QUOTA_RESET_TIME, "%H:%M:%S")
            now = datetime.now()
            reset_datetime = now.replace(
                hour=reset_time.hour,
                minute=reset_time.minute,
                second=reset_time.second,
                microsecond=0
            )
            
            # If reset time has passed today, use today
            # otherwise use yesterday
            if reset_datetime > now:
                reset_datetime -= timedelta(days=1)
                
            return reset_datetime
            
        except Exception as e:
            self.logger.error(f"Error parsing reset time: {e}")
            return datetime.now() - timedelta(days=1)
    
    def load_quota_usage(self):
        """Load quota usage from file"""
        try:
            if os.path.exists(QUOTA_USAGE_FILE):
                with open(QUOTA_USAGE_FILE, 'r') as f:
                    data = json.load(f)
                    self.quota_used = data.get('quota_used', 0)
                    self.last_reset_time = datetime.fromisoformat(
                        data.get('last_reset_time', datetime.now().isoformat())
                    )
                    
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
                    'daily_quota_limit': self.daily_quota_limit,
                    'quota_buffer': self.quota_buffer,
                    'last_reset_time': self.last_reset_time.isoformat(),
                    'last_updated': datetime.now().isoformat(),
                    'requests_per_minute': self.requests_per_minute
                }, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving quota usage: {e}")
    
    def check_quota_reset(self):
        """Check if quota should be reset (daily reset)"""
        now = datetime.now()
        
        # Check if it's time to reset (daily)
        if now >= self.last_reset_time + timedelta(days=1):
            with self.lock:
                self.quota_used = 0
                self.last_reset_time = now
                self.logger.info("Daily quota reset")
                self.save_quota_usage()
    
    def check_rate_limit_reset(self):
        """Check if rate limit should be reset (per minute)"""
        current_time = time.time()
        
        # Reset every minute
        if current_time - self.minute_start_time >= 60:
            with self.lock:
                self.requests_per_minute = 0
                self.minute_start_time = current_time
    
    def can_make_request(self, cost: int = 1) -> bool:
        """
        Check if a request can be made based on quota and rate limits
        
        Args:
            cost (int): Cost of the request in quota units
            
        Returns:
            bool: True if request can be made
        """
        with self.lock:
            # Check quota limit
            if self.quota_used + cost > self.daily_quota_limit - self.quota_buffer:
                self.logger.warning(f"Quota limit exceeded: {self.quota_used + cost}/{self.daily_quota_limit}")
                return False
            
            # Check rate limit
            if self.requests_per_minute >= MAX_REQUESTS_PER_MINUTE:
                self.logger.warning(f"Rate limit exceeded: {self.requests_per_minute}/{MAX_REQUESTS_PER_MINUTE}")
                return False
            
            # Check error cooldown
            if self.consecutive_errors >= MAX_CONSECUTIVE_ERRORS:
                self.logger.error("Too many consecutive errors. In cooldown.")
                return False
            
            return True
    
    def make_request(self, request_func: Callable, cost: int = 1, *args, **kwargs):
        """
        Make an API request with quota and rate limiting
        
        Args:
            request_func (Callable): Function to execute
            cost (int): Cost of the request in quota units
            *args: Arguments to pass to request_func
            **kwargs: Keyword arguments to pass to request_func
            
        Returns:
            Result of request_func or None if request failed
        """
        # Check if request can be made
        if not self.can_make_request(cost):
            return None
        
        # Wait for rate limit if needed
        self._wait_for_rate_limit()
        
        try:
            # Execute request
            result = request_func(*args, **kwargs)
            
            # Update quota usage
            with self.lock:
                self.quota_used += cost
                self.requests_per_minute += 1
                self.consecutive_errors = 0  # Reset error counter on success
            
            self.logger.info(f"Request successful. Quota used: {self.quota_used}/{self.daily_quota_limit}")
            return result
            
        except Exception as e:
            # Handle error
            with self.lock:
                self.consecutive_errors += 1
            
            self.logger.error(f"Request failed: {e}")
            
            # If too many errors, enter cooldown
            if self.consecutive_errors >= MAX_CONSECUTIVE_ERRORS:
                self.logger.info(f"Entering cooldown for {ERROR_COOLDOWN} seconds")
                time.sleep(ERROR_COOLDOWN)
            
            return None
    
    def _wait_for_rate_limit(self):
        """Wait if rate limit is approached"""
        if self.requests_per_minute >= MAX_REQUESTS_PER_MINUTE - 5:
            # Wait until next minute
            time_to_wait = 60 - (time.time() - self.minute_start_time)
            if time_to_wait > 0:
                self.logger.info(f"Rate limit approaching. Waiting {time_to_wait:.1f} seconds")
                time.sleep(time_to_wait)
        else:
            # Standard rate limiting delay
            time.sleep(RATE_LIMIT_DELAY)
    
    def get_quota_status(self) -> Dict:
        """
        Get current quota status
        
        Returns:
            Dict: Quota status information
        """
        with self.lock:
            return {
                'quota_used': self.quota_used,
                'quota_limit': self.daily_quota_limit,
                'quota_remaining': self.daily_quota_limit - self.quota_used,
                'quota_buffer': self.quota_buffer,
                'quota_percentage': (self.quota_used / self.daily_quota_limit) * 100,
                'requests_per_minute': self.requests_per_minute,
                'max_requests_per_minute': MAX_REQUESTS_PER_MINUTE,
                'consecutive_errors': self.consecutive_errors,
                'last_reset_time': self.last_reset_time.isoformat(),
                'next_reset_time': (self.last_reset_time + timedelta(days=1)).isoformat(),
                'can_make_request': self.can_make_request()
            }
    
    def start_monitoring(self):
        """Start background monitoring thread"""
        if not self.monitoring_active:
            self.monitoring_active = True
            monitor_thread = Thread(target=self._monitoring_loop, daemon=True)
            monitor_thread.start()
            self.logger.info("API monitoring started")
    
    def stop_monitoring(self):
        """Stop background monitoring thread"""
        self.monitoring_active = False
        self.logger.info("API monitoring stopped")
    
    def _monitoring_loop(self):
        """Background monitoring loop"""
        while self.monitoring_active:
            try:
                # Check quota reset
                self.check_quota_reset()
                
                # Check rate limit reset
                self.check_rate_limit_reset()
                
                # Save quota usage
                self.save_quota_usage()
                
                # Log status every 5 minutes
                if int(time.time()) % 300 == 0:
                    status = self.get_quota_status()
                    self.logger.info(f"API Status: {status['quota_percentage']:.1f}% quota used")
                
                # Sleep for 10 seconds
                time.sleep(10)
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(10)
    
    def reset_quota(self):
        """Manually reset quota (for testing)"""
        with self.lock:
            self.quota_used = 0
            self.last_reset_time = datetime.now()
            self.consecutive_errors = 0
            self.save_quota_usage()
            self.logger.info("Quota manually reset")
    
    def set_quota_limit(self, new_limit: int):
        """
        Set new daily quota limit
        
        Args:
            new_limit (int): New daily quota limit
        """
        with self.lock:
            self.daily_quota_limit = new_limit
            self.save_quota_usage()
            self.logger.info(f"Quota limit set to: {new_limit}")
    
    def get_usage_report(self) -> str:
        """
        Generate usage report
        
        Returns:
            str: Formatted usage report
        """
        status = self.get_quota_status()
        
        report = f"""
API Usage Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
================================================

Quota Usage:
  Used: {status['quota_used']:,}
  Limit: {status['quota_limit']:,}
  Remaining: {status['quota_remaining']:,}
  Percentage: {status['quota_percentage']:.1f}%
  Buffer: {status['quota_buffer']:,}

Rate Limiting:
  Requests/Minute: {status['requests_per_minute']}/{status['max_requests_per_minute']}
  Can Make Request: {status['can_make_request']}

Error Tracking:
  Consecutive Errors: {status['consecutive_errors']}/{MAX_CONSECUTIVE_ERRORS}

Reset Schedule:
  Last Reset: {status['last_reset_time']}
  Next Reset: {status['next_reset_time']}

Recommendations:
"""
        
        # Add recommendations based on usage
        if status['quota_percentage'] > 80:
            report += "  ⚠️  Quota usage is high. Consider reducing request frequency.\n"
        elif status['quota_percentage'] > 60:
            report += "  ⚠️  Quota usage is moderate. Monitor usage closely.\n"
        else:
            report += "  ✅ Quota usage is healthy.\n"
        
        if status['consecutive_errors'] > 3:
            report += "  ⚠️  Multiple consecutive errors detected. Check API configuration.\n"
        
        if not status['can_make_request']:
            report += "  ❌ Cannot make requests due to limits or errors.\n"
        
        return report


# Global API manager instance
api_manager = APIManager()


def main():
    """
    Main function to test API manager functionality
    """
    print("API Manager Test")
    print("=" * 50)
    
    # Show current status
    print(api_manager.get_usage_report())
    
    # Test quota check
    print("\nTesting quota check...")
    can_request = api_manager.can_make_request(cost=100)
    print(f"Can make request (cost=100): {can_request}")
    
    # Test rate limiting
    print("\nTesting rate limiting...")
    for i in range(5):
        can_request = api_manager.can_make_request()
        print(f"Request {i+1}: {can_request}")
        time.sleep(0.1)
    
    # Show final status
    print("\nFinal Status:")
    print(api_manager.get_usage_report())


if __name__ == "__main__":
    main()