import { NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

export async function GET() {
  try {
    // Path to the fixed dataset
    const dataPath = path.join(process.cwd(), '..', 'data', 'processed', 'comments_fixed_labels.csv')
    
    // Check if file exists
    if (!fs.existsSync(dataPath)) {
      // Fallback to mock data if file doesn't exist
      return NextResponse.json({
        sentiment: [
          { name: 'Negative', value: 13421, percentage: 69.8, color: '#ef4444', accuracy: 89.4 },
          { name: 'Positive', value: 5595, percentage: 29.1, color: '#22c55e', accuracy: 89.4 },
          { name: 'Neutral', value: 212, percentage: 1.1, color: '#6b7280', accuracy: 89.4 }
        ],
        target: [
          { name: 'General System', value: 8499, percentage: 44.2, color: '#3b82f6', accuracy: 92.4 },
          { name: 'Coaching Staff', value: 4532, percentage: 23.6, color: '#8b5cf6', accuracy: 92.4 },
          { name: 'Players', value: 2296, percentage: 11.9, color: '#f59e0b', accuracy: 92.4 },
          { name: 'Opponents', value: 2002, percentage: 10.4, color: '#10b981', accuracy: 92.4 },
          { name: 'PSSI Management', value: 1075, percentage: 5.6, color: '#f97316', accuracy: 92.4 },
          { name: 'External Factors', value: 824, percentage: 4.3, color: '#ec4899', accuracy: 92.4 }
        ],
        emotion: [
          { name: 'Neutral', value: 9057, percentage: 47.1, color: '#6b7280', accuracy: 91.0 },
          { name: 'Hopeful', value: 4260, percentage: 22.2, color: '#22c55e', accuracy: 91.0 },
          { name: 'Disappointed', value: 4134, percentage: 21.5, color: '#ef4444', accuracy: 91.0 },
          { name: 'Frustrated', value: 1300, percentage: 6.8, color: '#f59e0b', accuracy: 91.0 },
          { name: 'Supportive', value: 477, percentage: 2.5, color: '#3b82f6', accuracy: 91.0 }
        ],
        constructiveness: [
          { name: 'Constructive', value: 7272, percentage: 37.8, color: '#22c55e', accuracy: 77.7 },
          { name: 'Neutral', value: 5917, percentage: 30.8, color: '#6b7280', accuracy: 77.7 },
          { name: 'Hopeful', value: 5001, percentage: 26.0, color: '#f59e0b', accuracy: 77.7 },
          { name: 'Destructive', value: 1038, percentage: 5.4, color: '#ef4444', accuracy: 77.7 }
        ]
      })
    }

    // Read and parse CSV file
    const csvData = fs.readFileSync(dataPath, 'utf-8')
    const lines = csvData.split('\n')
    const headers = lines[0].split(',')
    
    // Find column indices
    const sentimentIdx = headers.indexOf('core_sentiment')
    const targetIdx = headers.indexOf('target_kritik')
    const emotionIdx = headers.indexOf('emotion_simple')
    const constructiveIdx = headers.indexOf('constructiveness')

    // Count occurrences
    const counts = {
      sentiment: {} as Record<string, number>,
      target: {} as Record<string, number>,
      emotion: {} as Record<string, number>,
      constructiveness: {} as Record<string, number>
    }

    let totalRows = 0

    for (let i = 1; i < lines.length; i++) {
      if (lines[i].trim() === '') continue
      
      const row = lines[i].split(',')
      totalRows++

      // Count sentiment
      const sentiment = row[sentimentIdx]?.trim()
      if (sentiment) counts.sentiment[sentiment] = (counts.sentiment[sentiment] || 0) + 1

      // Count target
      const target = row[targetIdx]?.trim()
      if (target) counts.target[target] = (counts.target[target] || 0) + 1

      // Count emotion
      const emotion = row[emotionIdx]?.trim()
      if (emotion) counts.emotion[emotion] = (counts.emotion[emotion] || 0) + 1

      // Count constructiveness
      const constructive = row[constructiveIdx]?.trim()
      if (constructive) counts.constructiveness[constructive] = (counts.constructiveness[constructive] || 0) + 1
    }

    // Convert to required format
    const formatData = (data: Record<string, number>, colors: string[], accuracy: number) => {
      return Object.entries(data)
        .map(([name, value], index) => ({
          name: name.charAt(0).toUpperCase() + name.slice(1).replace(/_/g, ' '),
          value,
          percentage: (value / totalRows) * 100,
          color: colors[index % colors.length],
          accuracy
        }))
        .sort((a, b) => b.value - a.value)
    }

    const result = {
      sentiment: formatData(counts.sentiment, ['#ef4444', '#22c55e', '#6b7280'], 89.4),
      target: formatData(counts.target, ['#3b82f6', '#8b5cf6', '#f59e0b', '#10b981', '#f97316', '#ec4899'], 92.4),
      emotion: formatData(counts.emotion, ['#6b7280', '#22c55e', '#ef4444', '#f59e0b', '#3b82f6'], 91.0),
      constructiveness: formatData(counts.constructiveness, ['#22c55e', '#ef4444', '#6b7280', '#f59e0b'], 77.7)
    }

    return NextResponse.json(result)

  } catch (error) {
    console.error('Error reading layer data:', error)
    
    // Return fallback data on error
    return NextResponse.json({
      sentiment: [
        { name: 'Negative', value: 13421, percentage: 69.8, color: '#ef4444', accuracy: 89.4 },
        { name: 'Positive', value: 5595, percentage: 29.1, color: '#22c55e', accuracy: 89.4 },
        { name: 'Neutral', value: 212, percentage: 1.1, color: '#6b7280', accuracy: 89.4 }
      ],
      target: [
        { name: 'General System', value: 8499, percentage: 44.2, color: '#3b82f6', accuracy: 92.4 },
        { name: 'Coaching Staff', value: 4532, percentage: 23.6, color: '#8b5cf6', accuracy: 92.4 },
        { name: 'Players', value: 2296, percentage: 11.9, color: '#f59e0b', accuracy: 92.4 },
        { name: 'Opponents', value: 2002, percentage: 10.4, color: '#10b981', accuracy: 92.4 },
        { name: 'PSSI Management', value: 1075, percentage: 5.6, color: '#f97316', accuracy: 92.4 },
        { name: 'External Factors', value: 824, percentage: 4.3, color: '#ec4899', accuracy: 92.4 }
      ],
      emotion: [
        { name: 'Neutral', value: 9057, percentage: 47.1, color: '#6b7280', accuracy: 91.0 },
        { name: 'Hopeful', value: 4260, percentage: 22.2, color: '#22c55e', accuracy: 91.0 },
        { name: 'Disappointed', value: 4134, percentage: 21.5, color: '#ef4444', accuracy: 91.0 },
        { name: 'Frustrated', value: 1300, percentage: 6.8, color: '#f59e0b', accuracy: 91.0 },
        { name: 'Supportive', value: 477, percentage: 2.5, color: '#3b82f6', accuracy: 91.0 }
      ],
      constructiveness: [
        { name: 'Constructive', value: 7272, percentage: 37.8, color: '#22c55e', accuracy: 77.7 },
        { name: 'Neutral', value: 5917, percentage: 30.8, color: '#6b7280', accuracy: 77.7 },
        { name: 'Hopeful', value: 5001, percentage: 26.0, color: '#f59e0b', accuracy: 77.7 },
        { name: 'Destructive', value: 1038, percentage: 5.4, color: '#ef4444', accuracy: 77.7 }
      ]
    })
  }
}
