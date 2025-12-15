import { NextRequest, NextResponse } from 'next/server';
import { saveComment, getStats, getRecentComments, getMemoryUsage } from '@/lib/memory-store';

export async function POST(request: NextRequest) {
  try {
    const data = await request.json();
    
    const commentData = {
      video_id: data.video_id || 'default_video',
      comment_text: data.comment || data.comment_text || '',
      sentiment: data.sentiment || 'neutral',
      emotion: data.emotion || null,
      confidence: data.confidence || 0.8
    };
    
    const saved = saveComment(commentData);
    
    return NextResponse.json({ 
      success: saved, 
      message: saved ? 'Comment saved to memory' : 'Duplicate comment ignored',
      data: commentData 
    });
  } catch (error) {
    console.error('Error saving to memory:', error);
    return NextResponse.json({ error: 'Failed to save data' }, { status: 500 });
  }
}

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const videoId = searchParams.get('video_id');
    const action = searchParams.get('action');
    
    if (action === 'recent') {
      const recentComments = getRecentComments(20);
      return NextResponse.json({ 
        data: recentComments,
        total: recentComments.length 
      });
    }
    
    if (action === 'memory') {
      return NextResponse.json(getMemoryUsage());
    }
    
    // Get stats from memory
    const stats = getStats(videoId || undefined);
    const recentComments = getRecentComments(5);
    
    return NextResponse.json({ 
      stats,
      recent: recentComments,
      storage: 'memory',
      memory: getMemoryUsage()
    });
  } catch (error) {
    console.error('Error getting memory data:', error);
    return NextResponse.json({ error: 'Failed to get data' }, { status: 500 });
  }
}
