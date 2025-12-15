import { NextRequest, NextResponse } from 'next/server';
import { getVideoComments, searchTimnasVideos, getVideoInfo, extractVideoId } from '@/lib/youtube-api';
import { saveComment } from '@/lib/memory-store';

const GEMINI_API_URL = "http://localhost:8000";

// Fallback sentiment analysis
function analyzeSentimentFallback(text: string): { sentiment: string; confidence: number; emotion: string } {
  const positiveWords = ['bagus', 'hebat', 'mantap', 'keren', 'semangat', 'bangga', 'sukses', 'luar biasa'];
  const negativeWords = ['jelek', 'buruk', 'kecewa', 'gagal', 'payah', 'lemah', 'hancur', 'mengecewakan'];
  
  const lowerText = text.toLowerCase();
  const positiveCount = positiveWords.filter(word => lowerText.includes(word)).length;
  const negativeCount = negativeWords.filter(word => lowerText.includes(word)).length;
  
  if (positiveCount > negativeCount) {
    return { sentiment: 'positive', confidence: 0.7 + (positiveCount * 0.1), emotion: 'dukungan' };
  } else if (negativeCount > positiveCount) {
    return { sentiment: 'negative', confidence: 0.7 + (negativeCount * 0.1), emotion: 'kekecewaan' };
  } else {
    return { sentiment: 'neutral', confidence: 0.6, emotion: 'netral' };
  }
}

// Analyze with Gemini AI
async function analyzeSentimentWithGemini(text: string) {
  try {
    const response = await fetch(`${GEMINI_API_URL}/predict`, {
      method: "POST",
      headers: { 
        "Content-Type": "application/json",
        "Accept": "application/json"
      },
      body: JSON.stringify({ text }),
      signal: AbortSignal.timeout(8000)
    });

    if (response.ok) {
      const result = await response.json();
      
      // Map emotion based on sentiment
      const emotionMap = {
        'positive': 'dukungan',
        'negative': 'kekecewaan', 
        'neutral': 'netral'
      };
      
      return {
        sentiment: result.sentiment,
        confidence: result.confidence,
        emotion: emotionMap[result.sentiment as keyof typeof emotionMap] || 'netral',
        reasoning: result.reasoning,
        model: "Gemini AI"
      };
    }
  } catch (error) {
    console.log(`⚠️ Gemini API unavailable for text: "${text.substring(0, 30)}..."`);
  }
  
  // Fallback
  const fallback = analyzeSentimentFallback(text);
  return {
    ...fallback,
    reasoning: "Rule-based analysis (Gemini unavailable)",
    model: "Fallback"
  };
}

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const action = searchParams.get('action');
  const videoUrl = searchParams.get('url');
  const videoId = searchParams.get('videoId');
  const useAI = searchParams.get('ai') !== 'false'; // Default to true

  try {
    if (action === 'search') {
      // Search for timnas videos
      const videos = await searchTimnasVideos(10);
      return NextResponse.json({ videos });
    }

    if (action === 'comments') {
      let targetVideoId = videoId;
      
      if (videoUrl && !targetVideoId) {
        targetVideoId = extractVideoId(videoUrl);
      }
      
      if (!targetVideoId) {
        return NextResponse.json({ error: 'Invalid video ID or URL' }, { status: 400 });
      }

      console.log(`🎬 Fetching comments for video: ${targetVideoId} (AI: ${useAI})`);

      // Get video info
      const videoInfo = await getVideoInfo(targetVideoId);
      
      // Get comments
      const comments = await getVideoComments(targetVideoId, 30);
      
      console.log(`📝 Analyzing ${comments.length} comments with ${useAI ? 'Gemini AI' : 'fallback'}...`);

      // Analyze sentiment
      const processedComments = await Promise.all(
        comments.map(async (comment) => {
          const analysis = useAI 
            ? await analyzeSentimentWithGemini(comment.text)
            : analyzeSentimentFallback(comment.text);
          
          // Save to memory store
          saveComment({
            video_id: targetVideoId!,
            comment_text: comment.text,
            sentiment: analysis.sentiment,
            emotion: analysis.emotion,
            confidence: analysis.confidence
          });
          
          return {
            ...comment,
            ...analysis
          };
        })
      );

      // Calculate summary stats
      const sentimentCounts = processedComments.reduce((acc, comment) => {
        acc[comment.sentiment] = (acc[comment.sentiment] || 0) + 1;
        return acc;
      }, {} as Record<string, number>);

      const avgConfidence = processedComments.reduce((sum, c) => sum + (c.confidence || 0), 0) / processedComments.length;

      console.log(`✅ Analysis complete: ${JSON.stringify(sentimentCounts)}`);

      return NextResponse.json({
        video: videoInfo,
        comments: processedComments,
        total: comments.length,
        analysis: {
          model: processedComments[0]?.model || "Mixed",
          summary: sentimentCounts,
          avgConfidence: avgConfidence,
          aiEnabled: useAI
        }
      });
    }

    return NextResponse.json({ error: 'Invalid action' }, { status: 400 });
    
  } catch (error) {
    console.error('YouTube API error:', error);
    return NextResponse.json({ 
      error: 'Failed to fetch YouTube data',
      message: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}
