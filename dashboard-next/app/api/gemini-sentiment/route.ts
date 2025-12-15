import { NextResponse } from "next/server";

const GEMINI_API_URL = "http://localhost:8000";

export async function POST(req: Request) {
  try {
    const { text, texts } = await req.json();
    
    if (!text && !texts) {
      return NextResponse.json({ error: "Text or texts required" }, { status: 400 });
    }

    let endpoint = "/predict";
    let payload = { text };
    
    // Batch analysis if multiple texts
    if (texts && Array.isArray(texts)) {
      endpoint = "/predict-batch";
      payload = { texts };
    }

    const response = await fetch(`${GEMINI_API_URL}${endpoint}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`Gemini API error: ${response.status}`);
    }

    const result = await response.json();
    
    return NextResponse.json({
      success: true,
      data: result,
      model: "Gemini AI",
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    console.error("Gemini sentiment API error:", error);
    
    // Fallback to simple rule-based analysis
    const fallbackAnalysis = (text: string) => {
      const positiveWords = ['bagus', 'mantap', 'keren', 'suka', 'senang', 'puas', 'recommended', 'excellent'];
      const negativeWords = ['jelek', 'buruk', 'kecewa', 'parah', 'benci', 'marah', 'tidak suka', 'mengecewakan'];
      
      const lowerText = text.toLowerCase();
      const posCount = positiveWords.filter(word => lowerText.includes(word)).length;
      const negCount = negativeWords.filter(word => lowerText.includes(word)).length;
      
      let sentiment = 'neutral';
      let confidence = 0.6;
      
      if (posCount > negCount) {
        sentiment = 'positive';
        confidence = Math.min(0.9, 0.6 + (posCount * 0.1));
      } else if (negCount > posCount) {
        sentiment = 'negative';
        confidence = Math.min(0.9, 0.6 + (negCount * 0.1));
      }
      
      return {
        text,
        sentiment,
        confidence,
        reasoning: "Fallback rule-based analysis"
      };
    };

    const { text, texts } = await req.json();
    
    if (texts && Array.isArray(texts)) {
      const results = texts.map(fallbackAnalysis);
      return NextResponse.json({
        success: true,
        data: { results },
        model: "Fallback Rule-based",
        error: "Gemini API unavailable, using fallback"
      });
    } else {
      const result = fallbackAnalysis(text);
      return NextResponse.json({
        success: true,
        data: result,
        model: "Fallback Rule-based",
        error: "Gemini API unavailable, using fallback"
      });
    }
  }
}

export async function GET() {
  return NextResponse.json({
    status: "Gemini AI Sentiment Analysis API",
    endpoints: {
      "POST /api/gemini-sentiment": "Analyze sentiment with Gemini AI",
    },
    model: "Google Gemini 2.5 Flash",
    features: [
      "Real-time AI analysis",
      "Indonesian language optimized", 
      "Contextual understanding",
      "Fallback rule-based analysis"
    ]
  });
}
