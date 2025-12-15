import { NextResponse } from "next/server";

const YOUTUBE_API_KEY = process.env.YOUTUBE_API_KEY;
const GEMINI_API_URL = "http://localhost:8000";

// Fallback sentiment analysis
function analyzeSentimentFallback(text: string) {
  const positiveWords = ['bagus', 'mantap', 'keren', 'suka', 'senang', 'puas', 'recommended', 'excellent', 'good', 'great'];
  const negativeWords = ['jelek', 'buruk', 'kecewa', 'parah', 'benci', 'marah', 'tidak suka', 'mengecewakan', 'bad', 'terrible'];
  
  const lowerText = text.toLowerCase();
  const posCount = positiveWords.filter(word => lowerText.includes(word)).length;
  const negCount = negativeWords.filter(word => lowerText.includes(word)).length;
  
  if (posCount > negCount) return { sentiment: 'positive', confidence: 0.7 };
  if (negCount > posCount) return { sentiment: 'negative', confidence: 0.7 };
  return { sentiment: 'neutral', confidence: 0.6 };
}

// Filter comments for relevance
async function filterRelevantComments(comments: any[]) {
  const relevantComments = [];
  
  for (const comment of comments) {
    const text = comment.text.toLowerCase();
    
    // Quick relevance check
    const footballKeywords = [
      'timnas', 'indonesia', 'sepak bola', 'football', 'soccer',
      'pemain', 'player', 'pelatih', 'coach', 'pertandingan', 'match',
      'gol', 'goal', 'menang', 'kalah', 'win', 'lose', 'juara'
    ];
    
    const spamKeywords = [
      'subscribe', 'like and subscribe', 'follow me', 'check out',
      'promo', 'diskon', 'murah', 'http', 'www', '.com'
    ];
    
    // Filter logic
    const hasFootballContext = footballKeywords.some(keyword => text.includes(keyword));
    const isSpam = spamKeywords.some(spam => text.includes(spam));
    const isTooShort = comment.text.trim().length < 10;
    const isJustEmojis = comment.text.length < 5 || comment.text.replace(/[a-zA-Z0-9\s]/g, '').length > comment.text.length * 0.5;
    
    // Include if relevant
    if (!isSpam && !isTooShort && !isJustEmojis && (hasFootballContext || comment.text.length > 20)) {
      relevantComments.push({
        ...comment,
        filterReason: hasFootballContext ? 'Football context' : 'General opinion'
      });
    }
  }
  
  return relevantComments;
}

// Analyze sentiment with Gemini AI
async function analyzeSentimentWithGemini(text: string) {
  try {
    console.log(`🤖 Analyzing with Gemini: "${text.substring(0, 50)}..."`);
    
    const response = await fetch(`${GEMINI_API_URL}/predict`, {
      method: "POST",
      headers: { 
        "Content-Type": "application/json",
        "Accept": "application/json"
      },
      body: JSON.stringify({ text }),
      signal: AbortSignal.timeout(10000)
    });

    if (response.ok) {
      const result = await response.json();
      console.log(`✅ Gemini result: ${result.sentiment} (${result.confidence})`);
      return {
        sentiment: result.sentiment,
        confidence: result.confidence,
        reasoning: result.reasoning,
        model: "Aggressive AI"
      };
    } else {
      console.log(`❌ Gemini API error: ${response.status}`);
    }
  } catch (error) {
    console.log(`⚠️ Gemini API unavailable: ${error}`);
  }
  
  // Fallback
  const fallback = analyzeSentimentFallback(text);
  return {
    ...fallback,
    reasoning: "Rule-based analysis (AI unavailable)",
    model: "Fallback"
  };
}

export async function GET(req: Request) {
  try {
    const { searchParams } = new URL(req.url);
    const videoId = searchParams.get("videoId") || "lDtSjKb_8Jo";
    const analyzeSentiment = searchParams.get("sentiment") === "true";
    const filterRelevant = searchParams.get("filter") !== "false"; // Default to true
    
    if (!YOUTUBE_API_KEY) {
      return NextResponse.json({ error: "YouTube API key not configured" }, { status: 500 });
    }

    const response = await fetch(
      `https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId=${videoId}&maxResults=50&order=time&key=${YOUTUBE_API_KEY}`
    );

    if (!response.ok) {
      throw new Error(`YouTube API error: ${response.status}`);
    }

    const data = await response.json();
    
    let comments = data.items?.map((item: any) => {
      const snippet = item.snippet.topLevelComment.snippet;
      return {
        id: item.id,
        text: snippet.textDisplay,
        author: snippet.authorDisplayName,
        authorChannelId: snippet.authorChannelId?.value,
        likeCount: snippet.likeCount,
        publishedAt: snippet.publishedAt,
        updatedAt: snippet.updatedAt,
        isReal: true
      };
    }) || [];

    console.log(`📥 Fetched ${comments.length} raw comments`);

    // Filter for relevant comments
    if (filterRelevant) {
      comments = await filterRelevantComments(comments);
      console.log(`🔍 Filtered to ${comments.length} relevant comments`);
    }

    // Add sentiment analysis if requested
    if (analyzeSentiment && comments.length > 0) {
      console.log(`🤖 Analyzing sentiment for ${comments.length} comments...`);
      
      const sentimentPromises = comments.map(async (comment) => {
        const sentimentData = await analyzeSentimentWithGemini(comment.text);
        return {
          ...comment,
          sentiment: sentimentData.sentiment,
          confidence: sentimentData.confidence,
          reasoning: sentimentData.reasoning,
          model: sentimentData.model
        };
      });

      comments = await Promise.all(sentimentPromises);
      
      // Add summary statistics
      const sentimentCounts = comments.reduce((acc, comment) => {
        acc[comment.sentiment] = (acc[comment.sentiment] || 0) + 1;
        return acc;
      }, {} as Record<string, number>);

      return NextResponse.json({ 
        comments,
        total: comments.length,
        videoId,
        isLive: true,
        filtered: filterRelevant,
        sentimentAnalysis: {
          enabled: true,
          model: comments[0]?.model || "Mixed",
          summary: sentimentCounts,
          avgConfidence: comments.reduce((sum, c) => sum + (c.confidence || 0), 0) / comments.length
        }
      });
    }

    return NextResponse.json({ 
      comments,
      total: comments.length,
      videoId,
      isLive: true,
      filtered: filterRelevant,
      sentimentAnalysis: { enabled: false }
    });

  } catch (error) {
    console.error("Live comments API error:", error);
    return NextResponse.json({ 
      error: "Failed to fetch live comments",
      details: error instanceof Error ? error.message : "Unknown error"
    }, { status: 500 });
  }
}
