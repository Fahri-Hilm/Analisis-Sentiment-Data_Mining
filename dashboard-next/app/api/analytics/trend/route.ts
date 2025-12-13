import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';
import Papa from 'papaparse';

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const period = searchParams.get('period') || 'monthly';
    
    const csvPath = path.join(process.cwd(), '..', 'data', 'processed', 'comments_fixed_labels.csv');
    
    if (!fs.existsSync(csvPath)) {
      return NextResponse.json({ error: 'Data file not found' }, { status: 404 });
    }

    const csvData = fs.readFileSync(csvPath, 'utf8');
    const { data } = Papa.parse(csvData, { header: true });

    // Group by time period and calculate sentiment trends
    const trendData = data.reduce((acc: any, row: any) => {
      if (!row.published_at || !row.core_sentiment) return acc;
      
      const publishedDate = new Date(row.published_at);
      let dateKey: string;
      
      // Group by period
      if (period === 'daily') {
        dateKey = publishedDate.toISOString().slice(0, 10); // YYYY-MM-DD
      } else if (period === 'weekly') {
        const weekStart = new Date(publishedDate);
        weekStart.setDate(publishedDate.getDate() - publishedDate.getDay());
        dateKey = weekStart.toISOString().slice(0, 10);
      } else { // monthly
        dateKey = publishedDate.toISOString().slice(0, 7); // YYYY-MM
      }
      
      if (!acc[dateKey]) {
        acc[dateKey] = { positive: 0, negative: 0, neutral: 0, total: 0 };
      }
      
      acc[dateKey].total++;
      const sentiment = row.core_sentiment.toLowerCase();
      if (sentiment === 'positive') acc[dateKey].positive++;
      else if (sentiment === 'negative') acc[dateKey].negative++;
      else acc[dateKey].neutral++;
      
      return acc;
    }, {});

    // Convert to percentage and format for chart
    const formattedData = Object.entries(trendData as Record<string, any>)
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([date, counts]: [string, any]) => ({
        date: formatDateLabel(date, period),
        positive: Math.round((counts.positive / counts.total) * 100),
        negative: Math.round((counts.negative / counts.total) * 100),
        neutral: Math.round((counts.neutral / counts.total) * 100),
        total: counts.total
      }));

    return NextResponse.json({
      success: true,
      data: formattedData,
      period
    });

  } catch (error) {
    console.error('Trend analysis error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

function formatDateLabel(date: string, period: string): string {
  if (period === 'daily') {
    return new Date(date).toLocaleDateString('id-ID', { 
      day: '2-digit', 
      month: 'short' 
    });
  } else if (period === 'weekly') {
    return `Minggu ${new Date(date).toLocaleDateString('id-ID', { 
      day: '2-digit', 
      month: 'short' 
    })}`;
  } else {
    return new Date(date + '-01').toLocaleDateString('id-ID', { 
      month: 'long', 
      year: 'numeric' 
    });
  }
}
