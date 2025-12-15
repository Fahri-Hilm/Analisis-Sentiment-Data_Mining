// In-memory storage with backup for VPS deployment
import fs from 'fs';
import path from 'path';

interface LiveComment {
  id: string;
  video_id: string;
  comment_text: string;
  sentiment: string;
  emotion?: string;
  confidence: number;
  timestamp: Date;
}

// Global memory store
let comments: LiveComment[] = [];
let maxComments = 500; // Reduced for low-spec VPS
const backupFile = path.join(process.cwd(), 'data', 'backup.json');

// Load backup on startup
function loadBackup() {
  try {
    if (fs.existsSync(backupFile)) {
      const data = JSON.parse(fs.readFileSync(backupFile, 'utf8'));
      comments = data.map((c: any) => ({
        ...c,
        timestamp: new Date(c.timestamp)
      }));
      console.log(`Loaded ${comments.length} comments from backup`);
    }
  } catch (error) {
    console.log('No backup found, starting fresh');
  }
}

// Save backup periodically
function saveBackup() {
  try {
    const dir = path.dirname(backupFile);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(backupFile, JSON.stringify(comments.slice(0, 100))); // Only save last 100
  } catch (error) {
    console.error('Backup failed:', error);
  }
}

export function saveComment(data: {
  video_id: string;
  comment_text: string;
  sentiment: string;
  emotion?: string;
  confidence?: number;
}) {
  const comment: LiveComment = {
    id: `${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
    video_id: data.video_id,
    comment_text: data.comment_text,
    sentiment: data.sentiment,
    emotion: data.emotion,
    confidence: data.confidence || 0.8,
    timestamp: new Date()
  };

  // Check for duplicates (same text + video_id)
  const isDuplicate = comments.some(c => 
    c.comment_text === comment.comment_text && 
    c.video_id === comment.video_id
  );

  if (!isDuplicate) {
    comments.unshift(comment);
    
    // Keep only maxComments for memory efficiency
    if (comments.length > maxComments) {
      comments = comments.slice(0, maxComments);
    }
    return true;
  }
  return false;
}

export function getStats(videoId?: string) {
  const filtered = videoId 
    ? comments.filter(c => c.video_id === videoId)
    : comments.filter(c => {
        const hourAgo = new Date(Date.now() - 60 * 60 * 1000);
        return c.timestamp > hourAgo;
      });

  return {
    total: filtered.length,
    positive: filtered.filter(c => c.sentiment === 'positive').length,
    negative: filtered.filter(c => c.sentiment === 'negative').length,
    neutral: filtered.filter(c => c.sentiment === 'neutral').length
  };
}

export function getRecentComments(limit = 10) {
  return comments.slice(0, limit);
}

export function getMemoryUsage() {
  return {
    comments_count: comments.length,
    memory_mb: Math.round(JSON.stringify(comments).length / 1024 / 1024 * 100) / 100
  };
}

// Initialize
loadBackup();

// Auto backup every 5 minutes (light)
setInterval(saveBackup, 5 * 60 * 1000);

// Cleanup old comments every hour
setInterval(() => {
  const hourAgo = new Date(Date.now() - 2 * 60 * 60 * 1000); // Keep 2 hours
  const oldCount = comments.length;
  comments = comments.filter(c => c.timestamp > hourAgo);
  if (oldCount !== comments.length) {
    console.log(`Cleaned ${oldCount - comments.length} old comments`);
  }
}, 60 * 60 * 1000);
