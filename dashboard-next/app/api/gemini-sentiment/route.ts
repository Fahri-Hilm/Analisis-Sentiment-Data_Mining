import { NextResponse } from "next/server";

const UNIFIED_API_URL = "http://localhost:8000";

export async function POST(req: Request) {
  try {
    const { text, texts, model_type = "realtime" } = await req.json();
    
    if (!text && !texts) {
      return NextResponse.json({ error: "Text or texts required" }, { status: 400 });
    }

    let endpoint = "/predict";
    let payload = { text, model_type };
    
    // Batch analysis if multiple texts
    if (texts && Array.isArray(texts)) {
      endpoint = "/predict-batch";
      payload = { texts, model_type };
    }

    const response = await fetch(`${UNIFIED_API_URL}${endpoint}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`Unified API error: ${response.status}`);
    }

    const result = await response.json();
    
    return NextResponse.json({
      success: true,
      data: result,
      model: "Unified Sentiment Scorer",
      model_type: model_type,
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    console.error("Unified sentiment API error:", error);
    
    // Enhanced fallback with unified patterns
    const fallbackAnalysis = (text: string) => {
      const sentimentLexicon = {
        positive: {
          strong: ['sangat bagus', 'luar biasa', 'excellent', 'fantastic', 'amazing', 'perfect', 'mantap sekali'],
          medium: ['bagus', 'mantap', 'keren', 'hebat', 'good', 'great', 'puas', 'senang', 'suka', 'juara'],
          weak: ['lumayan', 'cukup', 'ok', 'okay', 'fine', 'baik']
        },
        negative: {
          strong: ['sangat jelek', 'sangat buruk', 'terrible', 'awful', 'kecewa sekali', 'payah banget'],
          medium: ['jelek', 'buruk', 'kecewa', 'gagal', 'payah', 'bad', 'marah', 'benci', 'kalah'],
          weak: ['kurang', 'tidak', 'bukan', 'gak', 'ga', 'salah']
        }
      };
      
      const lowerText = text.toLowerCase();
      let positiveScore = 0;
      let negativeScore = 0;
      
      // Calculate weighted scores
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
      
      // Unified decision logic
      const totalScore = positiveScore + negativeScore;
      if (totalScore === 0) {
        return {
          text,
          sentiment: 'neutral',
          confidence: 0.65,
          reasoning: "No clear sentiment indicators (unified fallback)",
          model: "Unified-Fallback"
        };
      }
      
      const posRatio = positiveScore / totalScore;
      const negRatio = negativeScore / totalScore;
      
      if (posRatio >= 0.35 && posRatio > negRatio) {
        return {
          text,
          sentiment: 'positive',
          confidence: Math.min(0.95, 0.6 + posRatio * 0.3),
          reasoning: `Positive patterns detected (score: ${positiveScore}, ratio: ${posRatio.toFixed(2)})`,
          model: "Unified-Fallback"
        };
      } else if (negRatio >= 0.35 && negRatio > posRatio) {
        return {
          text,
          sentiment: 'negative',
          confidence: Math.min(0.95, 0.6 + negRatio * 0.3),
          reasoning: `Negative patterns detected (score: ${negativeScore}, ratio: ${negRatio.toFixed(2)})`,
          model: "Unified-Fallback"
        };
      } else {
        return {
          text,
          sentiment: 'neutral',
          confidence: 0.65,
          reasoning: `Mixed sentiment (pos: ${posRatio.toFixed(2)}, neg: ${negRatio.toFixed(2)})`,
          model: "Unified-Fallback"
        };
      }
    };

    const { text, texts } = await req.json();
    
    if (texts && Array.isArray(texts)) {
      const results = texts.map(fallbackAnalysis);
      return NextResponse.json({
        success: true,
        data: { results },
        model: "Unified Fallback Scorer",
        error: "Unified API unavailable, using enhanced fallback"
      });
    } else {
      const result = fallbackAnalysis(text);
      return NextResponse.json({
        success: true,
        data: result,
        model: "Unified Fallback Scorer",
        error: "Unified API unavailable, using enhanced fallback"
      });
    }
  }
}

export async function GET() {
  return NextResponse.json({
    status: "Unified Sentiment Analysis API",
    endpoints: {
      "POST /api/gemini-sentiment": "Analyze sentiment with Unified Scorer",
    },
    model: "Unified Sentiment Scorer v1.0.0",
    features: [
      "Consistent scoring across static and realtime models",
      "Indonesian language optimized", 
      "Football context aware",
      "Enhanced fallback analysis",
      "Model-specific behavior adaptation"
    ],
    model_types: {
      "static": "Conservative scoring, mimics dashboard static models",
      "realtime": "Aggressive scoring, optimized for live analysis",
      "unified": "Balanced scoring, best of both approaches"
    }
  });
}
