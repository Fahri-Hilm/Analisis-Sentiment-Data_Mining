import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { keywords, maxVideos, maxCommentsPerVideo } = await request.json();
    
    // Simulate YouTube search for today's videos
    const today = new Date().toISOString().split('T')[0];
    
    const mockVideos = [
      {
        id: 'abc123',
        title: 'Timnas Indonesia Hari Ini - Analisis Terbaru',
        publishedAt: today,
        commentCount: 245
      },
      {
        id: 'def456', 
        title: 'Reaksi Fans Garuda Setelah Pertandingan',
        publishedAt: today,
        commentCount: 189
      },
      {
        id: 'ghi789',
        title: 'Strategi Baru Timnas untuk Piala Dunia',
        publishedAt: today,
        commentCount: 156
      }
    ].slice(0, maxVideos);

    return NextResponse.json({
      success: true,
      date: today,
      videos: mockVideos,
      totalComments: mockVideos.reduce((sum, v) => sum + Math.min(v.commentCount, maxCommentsPerVideo), 0)
    });

  } catch (error) {
    return NextResponse.json({ success: false, error: 'Search failed' }, { status: 500 });
  }
}

export async function GET() {
  return NextResponse.json({
    status: 'Daily search API ready',
    endpoints: {
      search: 'POST /api/daily-search',
      params: ['keywords', 'maxVideos', 'maxCommentsPerVideo']
    }
  });
}
