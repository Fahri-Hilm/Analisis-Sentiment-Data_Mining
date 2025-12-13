import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';
import Papa from 'papaparse';

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const target = searchParams.get('target');
    
    const csvPath = path.join(process.cwd(), '..', 'data', 'processed', 'comments_fixed_labels.csv');
    
    if (!fs.existsSync(csvPath)) {
      return NextResponse.json({ error: 'Data file not found' }, { status: 404 });
    }

    const csvData = fs.readFileSync(csvPath, 'utf8');
    const { data } = Papa.parse(csvData, { header: true });

    if (target) {
      // Return specific target details
      const targetComments = data.filter((row: any) => 
        row.target_kritik?.toLowerCase().includes(target.toLowerCase())
      );
      
      return NextResponse.json({
        success: true,
        target: {
          name: target,
          total: targetComments.length,
          sentiments: calculateSentiments(targetComments),
          sampleComments: targetComments.slice(0, 5).map((row: any) => row.clean_text)
        }
      });
    }

    // Group by target and calculate stats
    const targetStats = data.reduce((acc: any, row: any) => {
      const target = row.target_kritik || 'unknown';
      const sentiment = row.core_sentiment?.toLowerCase() || 'neutral';
      
      if (!acc[target]) {
        acc[target] = { positive: 0, negative: 0, neutral: 0, total: 0 };
      }
      
      acc[target].total++;
      acc[target][sentiment]++;
      
      return acc;
    }, {});

    // Format for charts
    const formattedData = Object.entries(targetStats as Record<string, any>)
      .map(([name, stats]: [string, any]) => ({
        name: formatTargetName(name),
        value: stats.total,
        positive: Math.round((stats.positive / stats.total) * 100),
        negative: Math.round((stats.negative / stats.total) * 100),
        neutral: Math.round((stats.neutral / stats.total) * 100),
        sentiment: (stats.negative - stats.positive) / stats.total,
        color: getSentimentColor((stats.negative - stats.positive) / stats.total)
      }))
      .sort((a, b) => b.value - a.value)
      .slice(0, 8);

    return NextResponse.json({
      success: true,
      data: formattedData
    });

  } catch (error) {
    console.error('Target analysis error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

function calculateSentiments(comments: any[]) {
  const total = comments.length;
  const positive = comments.filter(c => c.core_sentiment?.toLowerCase() === 'positive').length;
  const negative = comments.filter(c => c.core_sentiment?.toLowerCase() === 'negative').length;
  const neutral = total - positive - negative;
  
  return {
    positive: Math.round((positive / total) * 100),
    negative: Math.round((negative / total) * 100),
    neutral: Math.round((neutral / total) * 100)
  };
}

function formatTargetName(target: string): string {
  const mapping: { [key: string]: string } = {
    'coaching_staff': 'Pelatih',
    'players': 'Pemain',
    'pssi_management': 'PSSI',
    'system_infrastructure': 'Sistem',
    'referee': 'Wasit',
    'unknown': 'Lainnya'
  };
  return mapping[target] || target;
}

function getSentimentColor(sentiment: number): string {
  if (sentiment > 0.5) return '#dc2626';
  if (sentiment > 0.2) return '#f43f5e';
  if (sentiment > -0.2) return '#64748b';
  if (sentiment > -0.5) return '#10b981';
  return '#059669';
}
