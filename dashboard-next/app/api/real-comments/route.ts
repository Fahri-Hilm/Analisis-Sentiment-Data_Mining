import { NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

interface RealComment {
  id: string;
  author: string;
  text: string;
  sentiment: string;
  emotion: string;
  confidence: number;
  timestamp: Date;
  like_count: number;
}

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const limit = parseInt(searchParams.get('limit') || '50');
    
    // Path to the real dataset
    const csvPath = path.join(process.cwd(), '..', 'data', 'processed', 'comments_fixed_labels.csv');
    
    if (!fs.existsSync(csvPath)) {
      return NextResponse.json({ error: 'Dataset not found' }, { status: 404 });
    }

    // Read CSV file
    const csvContent = fs.readFileSync(csvPath, 'utf-8');
    const lines = csvContent.split('\n');
    const headers = lines[0].split(',');
    
    // Get random sample of comments
    const dataLines = lines.slice(1).filter(line => line.trim());
    const shuffled = dataLines.sort(() => 0.5 - Math.random());
    const selectedLines = shuffled.slice(0, limit);
    
    const comments: RealComment[] = selectedLines.map((line, index) => {
      const values = line.split(',');
      
      // Map CSV columns to our structure
      const comment_id = values[0] || `real_${Date.now()}_${index}`;
      const text = values[2] || 'No comment text';
      const author = values[3] || 'Anonymous';
      const like_count = parseInt(values[5]) || 0;
      const published_at = values[7] || new Date().toISOString();
      const core_sentiment = values[16] || 'neutral';
      const emotion_simple = values[44] || 'neutral';
      const core_sentiment_confidence = parseFloat(values[18]) || 0.8;
      
      // Map sentiment values
      let sentiment = 'neutral';
      if (core_sentiment === 'positive') sentiment = 'positive';
      else if (core_sentiment === 'negative') sentiment = 'negative';
      
      return {
        id: comment_id,
        author: author.replace(/[@"]/g, ''), // Clean author name
        text: text.replace(/"/g, ''), // Clean text
        sentiment,
        emotion: emotion_simple || 'neutral',
        confidence: core_sentiment_confidence,
        timestamp: new Date(published_at),
        like_count
      };
    });

    // Calculate stats
    const stats = {
      total: comments.length,
      positive: comments.filter(c => c.sentiment === 'positive').length,
      negative: comments.filter(c => c.sentiment === 'negative').length,
      neutral: comments.filter(c => c.sentiment === 'neutral').length
    };

    return NextResponse.json({
      comments,
      stats,
      source: 'real_dataset',
      total: comments.length
    });

  } catch (error) {
    console.error('Error reading real comments:', error);
    return NextResponse.json({ 
      error: 'Failed to load real comments',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}
