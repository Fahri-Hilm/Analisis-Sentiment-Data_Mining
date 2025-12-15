// YouTube Data API v3 Integration
const YOUTUBE_API_KEY = process.env.YOUTUBE_API_KEY || 'YOUR_API_KEY_HERE';
const YOUTUBE_API_BASE = 'https://www.googleapis.com/youtube/v3';

export interface YouTubeComment {
  id: string;
  author: string;
  text: string;
  publishedAt: string;
  likeCount: number;
  videoId: string;
}

// Extract video ID from YouTube URL
export function extractVideoId(url: string): string | null {
  const regex = /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)/;
  const match = url.match(regex);
  return match ? match[1] : null;
}

// Get video comments from YouTube API
export async function getVideoComments(videoId: string, maxResults = 50): Promise<YouTubeComment[]> {
  try {
    const response = await fetch(
      `${YOUTUBE_API_BASE}/commentThreads?part=snippet&videoId=${videoId}&maxResults=${maxResults}&order=time&key=${YOUTUBE_API_KEY}`
    );
    
    if (!response.ok) {
      throw new Error(`YouTube API error: ${response.status}`);
    }
    
    const data = await response.json();
    
    return data.items?.map((item: any) => ({
      id: item.id,
      author: item.snippet.topLevelComment.snippet.authorDisplayName,
      text: item.snippet.topLevelComment.snippet.textDisplay,
      publishedAt: item.snippet.topLevelComment.snippet.publishedAt,
      likeCount: item.snippet.topLevelComment.snippet.likeCount,
      videoId: videoId
    })) || [];
    
  } catch (error) {
    console.error('Error fetching YouTube comments:', error);
    return [];
  }
}

// Search for videos about Indonesian national team
export async function searchTimnasVideos(maxResults = 10): Promise<any[]> {
  try {
    const query = encodeURIComponent('timnas indonesia terbaru');
    const response = await fetch(
      `${YOUTUBE_API_BASE}/search?part=snippet&q=${query}&type=video&maxResults=${maxResults}&order=date&key=${YOUTUBE_API_KEY}`
    );
    
    if (!response.ok) {
      throw new Error(`YouTube API error: ${response.status}`);
    }
    
    const data = await response.json();
    
    return data.items?.map((item: any) => ({
      videoId: item.id.videoId,
      title: item.snippet.title,
      channelTitle: item.snippet.channelTitle,
      publishedAt: item.snippet.publishedAt,
      thumbnail: item.snippet.thumbnails.medium.url
    })) || [];
    
  } catch (error) {
    console.error('Error searching YouTube videos:', error);
    return [];
  }
}

// Get video info
export async function getVideoInfo(videoId: string) {
  try {
    const response = await fetch(
      `${YOUTUBE_API_BASE}/videos?part=snippet,statistics&id=${videoId}&key=${YOUTUBE_API_KEY}`
    );
    
    if (!response.ok) {
      throw new Error(`YouTube API error: ${response.status}`);
    }
    
    const data = await response.json();
    const video = data.items?.[0];
    
    if (!video) return null;
    
    return {
      id: video.id,
      title: video.snippet.title,
      channelTitle: video.snippet.channelTitle,
      publishedAt: video.snippet.publishedAt,
      viewCount: parseInt(video.statistics.viewCount),
      likeCount: parseInt(video.statistics.likeCount),
      commentCount: parseInt(video.statistics.commentCount)
    };
    
  } catch (error) {
    console.error('Error fetching video info:', error);
    return null;
  }
}
