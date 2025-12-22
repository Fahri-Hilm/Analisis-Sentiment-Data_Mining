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
    const limit = parseInt(searchParams.get('limit') || '20');
    
    // Path to the cleaned dataset (19k comments)
    const csvPath = path.join(process.cwd(), '..', 'data', 'processed', 'comments_fixed_labels.csv');
    
    if (!fs.existsSync(csvPath)) {
      return NextResponse.json({ error: 'CSV file not found' }, { status: 404 });
    }

    // Read CSV file
    const csvContent = fs.readFileSync(csvPath, 'utf-8');
    const lines = csvContent.split('\n').filter(line => line.trim());
    const headers = lines[0].split(',');
    
    // Get random sample from 19k comments
    const dataLines = lines.slice(1).filter(line => line.trim());
    const shuffled = dataLines.sort(() => 0.5 - Math.random());
    const selectedLines = shuffled.slice(0, limit);
    
    const comments: RealComment[] = selectedLines.map((line, index) => {
      const values = line.split(',');
      
      return {
        id: values[0] || `clean_${index}`,
        author: values[3]?.replace(/[@"]/g, '') || 'Anonymous',
        text: values[2]?.replace(/"/g, '') || 'No comment',
        sentiment: values[15] || 'neutral', // core_sentiment column
        emotion: values[44] || 'neutral', // emotion_simple column
        confidence: parseFloat(values[17]) || 0.8, // core_sentiment_confidence
        timestamp: new Date(values[7] || new Date()),
        like_count: parseInt(values[5]) || 0
      };
    });

    const stats = {
      total: comments.length,
      positive: comments.filter(c => c.sentiment === 'positive').length,
      negative: comments.filter(c => c.sentiment === 'negative').length,
      neutral: comments.filter(c => c.sentiment === 'neutral').length
    };

    return NextResponse.json({
      comments,
      stats,
      source: 'cleaned_dataset_19k',
      total: comments.length
    });

  } catch (error) {
    console.error('Error reading CSV:', error);
    return NextResponse.json({ 
      error: 'Failed to load CSV comments',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}
