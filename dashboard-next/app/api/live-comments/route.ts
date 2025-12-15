import { NextResponse } from "next/server";

const YOUTUBE_API_KEY = process.env.YOUTUBE_API_KEY;
const GEMINI_API_URL = "http://localhost:8000";

// Enhanced fallback sentiment analysis with unified patterns
function analyzeSentimentFallback(text: string) {
  // Unified lexicon for consistent fallback scoring
  const sentimentLexicon = {
    positive: {
      strong: ['sangat bagus', 'luar biasa', 'excellent', 'fantastic', 'amazing', 'perfect', 'mantap sekali', 'keren banget', 'hebat sekali'],
      medium: ['bagus', 'mantap', 'keren', 'hebat', 'good', 'great', 'nice', 'puas', 'senang', 'suka', 'bangga', 'juara', 'menang', 'gol', 'sukses'],
      weak: ['lumayan', 'cukup', 'ok', 'okay', 'fine', 'baik', 'bisa', 'tidak buruk']
    },
    negative: {
      strong: ['sangat jelek', 'sangat buruk', 'terrible', 'awful', 'horrible', 'kecewa sekali', 'marah sekali', 'payah banget', 'parah banget'],
      medium: ['jelek', 'buruk', 'kecewa', 'gagal', 'payah', 'lemah', 'bad', 'marah', 'benci', 'kalah', 'mengecewakan', 'tidak suka'],
      weak: ['kurang', 'tidak', 'bukan', 'gak', 'ga', 'nggak', 'salah', 'minus']
    }
  };
  
  const lowerText = text.toLowerCase();
  let positiveScore = 0;
  let negativeScore = 0;
  
  // Calculate scores with weights
  Object.entries(sentimentLexicon.positive).forEach(([strength, words]) => {
    const weight = strength === 'strong' ? 3 : strength === 'medium' ? 2 : 1;
    words.forEach(word => {
      if (lowerText.includes(word)) positiveScore += weight;
    });
  });
  
  Object.entries(sentimentLexicon.negative).forEach(([strength, words]) => {
    const weight = strength === 'strong' ? 3 : strength === 'medium' ? 2 : 1;
    words.forEach(word => {
      if (lowerText.includes(word)) negativeScore += weight;
    });
  });
  
  // Apply unified thresholds
  const totalScore = positiveScore + negativeScore;
  if (totalScore === 0) {
    return { sentiment: 'neutral', confidence: 0.65 };
  }
  
  const posRatio = positiveScore / totalScore;
  const negRatio = negativeScore / totalScore;
  
  // Unified decision thresholds
  if (posRatio >= 0.35 && posRatio > negRatio) {
    return { 
      sentiment: 'positive', 
      confidence: Math.min(0.95, 0.6 + posRatio * 0.3)
    };
  } else if (negRatio >= 0.35 && negRatio > posRatio) {
    return { 
      sentiment: 'negative', 
      confidence: Math.min(0.95, 0.6 + negRatio * 0.3)
    };
  } else {
    return { sentiment: 'neutral', confidence: 0.65 };
  }
}

// Enhanced filtering system
async function filterRelevantComments(comments: any[]) {
  const relevantComments = [];
  
  for (const comment of comments) {
    const text = comment.text.toLowerCase();
    const originalText = comment.text;
    
    // Enhanced football keywords
    const footballKeywords = [
      'timnas', 'indonesia', 'sepak bola', 'football', 'soccer', 'bola',
      'pemain', 'player', 'pelatih', 'coach', 'pertandingan', 'match',
      'gol', 'goal', 'menang', 'kalah', 'win', 'lose', 'juara', 'champion',
      'garuda', 'merah putih', 'pssi', 'aff', 'piala dunia', 'world cup',
      'shin tae-yong', 'sty', 'egy', 'witan', 'pratama', 'arhan',
      'elkan', 'baggott', 'jordi', 'asnawi', 'rizky ridho', 'marselino',
      'tactic', 'taktik', 'formasi', 'formation', 'strategy', 'strategi'
    ];
    
    // Enhanced spam detection
    const spamKeywords = [
      'subscribe', 'like and subscribe', 'follow me', 'check out', 'link bio',
      'promo', 'diskon', 'murah', 'http', 'www', '.com', '.id', 'wa.me',
      'jual', 'beli', 'order', 'dm', 'chat', 'whatsapp', 'telegram',
      'first', 'pertamax', 'komen pertama', 'pin dong', 'pin please'
    ];
    
    // Quality checks
    const hasFootballContext = footballKeywords.some(keyword => text.includes(keyword));
    const isSpam = spamKeywords.some(spam => text.includes(spam));
    const isTooShort = originalText.trim().length < 8;
    const isJustEmojis = originalText.replace(/[\w\s]/g, '').length > originalText.length * 0.6;
    const hasRepeatedChars = /(.)\1{4,}/.test(originalText); // 5+ repeated chars
    const isAllCaps = originalText.length > 10 && originalText === originalText.toUpperCase();
    
    // Opinion indicators
    const opinionWords = [
      'bagus', 'jelek', 'keren', 'mantap', 'parah', 'buruk', 'suka', 'benci',
      'setuju', 'tidak setuju', 'harusnya', 'seharusnya', 'kenapa', 'mengapa',
      'good', 'bad', 'great', 'terrible', 'should', 'why', 'how'
    ];
    const hasOpinion = opinionWords.some(word => text.includes(word));
    
    // Scoring system
    let relevanceScore = 0;
    if (hasFootballContext) relevanceScore += 3;
    if (hasOpinion) relevanceScore += 2;
    if (originalText.length > 30) relevanceScore += 1;
    if (originalText.includes('?')) relevanceScore += 1; // Questions often relevant
    
    // Penalty system
    if (isSpam) relevanceScore -= 5;
    if (isTooShort) relevanceScore -= 2;
    if (isJustEmojis) relevanceScore -= 3;
    if (hasRepeatedChars) relevanceScore -= 2;
    if (isAllCaps) relevanceScore -= 1;
    
    // Include if score is positive
    if (relevanceScore > 0) {
      relevantComments.push({
        ...comment,
        relevanceScore,
        filterReason: hasFootballContext ? 'Football context' : 
                     hasOpinion ? 'Opinion detected' : 'General relevance'
      });
    }
  }
  
  // Sort by relevance score (highest first)
  return relevantComments.sort((a, b) => b.relevanceScore - a.relevanceScore);
}

// Analyze sentiment with Unified Scoring System
async function analyzeSentimentWithUnified(text: string) {
  try {
    console.log(`🎯 Analyzing with Unified Scorer: "${text.substring(0, 50)}..."`);
    
    const response = await fetch(`${GEMINI_API_URL}/predict`, {
      method: "POST",
      headers: { 
        "Content-Type": "application/json",
        "Accept": "application/json"
      },
      body: JSON.stringify({ 
        text,
        model_type: "realtime"  // Use realtime model behavior for live comments
      }),
      signal: AbortSignal.timeout(10000)
    });

    if (response.ok) {
      const result = await response.json();
      console.log(`✅ Unified Scorer result: ${result.sentiment} (${result.confidence})`);
      return {
        sentiment: result.sentiment,
        confidence: result.confidence,
        reasoning: result.reasoning,
        model: "Unified-Realtime",
        scores: result.scores
      };
    } else {
      console.log(`❌ Unified Scorer API error: ${response.status}`);
    }
  } catch (error) {
    console.log(`⚠️ Unified Scorer API unavailable: ${error}`);
  }
  
  // Enhanced fallback with consistent scoring
  const fallback = analyzeSentimentFallback(text);
  return {
    ...fallback,
    reasoning: "Enhanced fallback analysis (Unified Scorer unavailable)",
    model: "Unified-Fallback"
  };
}

export async function GET(req: Request) {
  try {
    const { searchParams } = new URL(req.url);
    const videoId = searchParams.get("videoId") || "lDtSjKb_8Jo";
    const analyzeSentiment = searchParams.get("sentiment") === "true";
    const filterRelevant = searchParams.get("filter") !== "false"; // Default to true
    const maxResults = parseInt(searchParams.get("maxResults") || "200"); // Increased default
    
    if (!YOUTUBE_API_KEY) {
      return NextResponse.json({ error: "YouTube API key not configured" }, { status: 500 });
    }

    // Fetch multiple pages to get more comments
    let allComments: any[] = [];
    let nextPageToken = "";
    let fetchCount = 0;
    const maxFetches = Math.ceil(maxResults / 50); // YouTube API max per request is 50

    do {
      const url = `https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId=${videoId}&maxResults=50&order=time&key=${YOUTUBE_API_KEY}${nextPageToken ? `&pageToken=${nextPageToken}` : ''}`;
      
      const response = await fetch(url);
      
      if (!response.ok) {
        if (fetchCount === 0) {
          throw new Error(`YouTube API error: ${response.status}`);
        }
        break; // If not first request, just break and use what we have
      }

      const data = await response.json();
      
      const pageComments = data.items?.map((item: any) => {
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

      allComments = [...allComments, ...pageComments];
      nextPageToken = data.nextPageToken || "";
      fetchCount++;
      
      // Stop if we have enough comments or no more pages
      if (allComments.length >= maxResults || !nextPageToken || fetchCount >= maxFetches) {
        break;
      }
      
    } while (nextPageToken && fetchCount < maxFetches);

    console.log(`📥 Fetched ${allComments.length} raw comments from ${fetchCount} API calls`);

    // Trim to requested amount
    let comments = allComments.slice(0, maxResults);

    // Filter for relevant comments
    if (filterRelevant) {
      const beforeFilter = comments.length;
      comments = await filterRelevantComments(comments);
      console.log(`🔍 Filtered from ${beforeFilter} to ${comments.length} relevant comments`);
    }

    // Add sentiment analysis if requested
    if (analyzeSentiment && comments.length > 0) {
      console.log(`🤖 Analyzing sentiment for ${comments.length} comments...`);
      
      const sentimentPromises = comments.map(async (comment) => {
        const sentimentData = await analyzeSentimentWithUnified(comment.text);
        return {
          ...comment,
          sentiment: sentimentData.sentiment,
          confidence: sentimentData.confidence,
          reasoning: sentimentData.reasoning,
          model: sentimentData.model,
          scores: sentimentData.scores
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
        totalFetched: allComments.length,
        videoId,
        isLive: true,
        filtered: filterRelevant,
        maxResults,
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
      totalFetched: allComments.length,
      videoId,
      isLive: true,
      filtered: filterRelevant,
      maxResults,
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
