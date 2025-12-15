import { NextResponse } from "next/server";

const UNIFIED_API_URL = "http://localhost:8000";

export async function GET() {
  try {
    // Get model info from unified scorer
    const response = await fetch(`${UNIFIED_API_URL}/model-info`);
    
    if (response.ok) {
      const modelInfo = await response.json();
      
      // Return consistent data structure with unified scoring info
      return NextResponse.json({
        total: 8931,
        positive: 6.4,
        neutral: 75.8,
        negative: 17.7,
        accuracy: 73.4,  // Updated to match unified system
        confidence: 90.3,
        model: "Unified-Static",
        scorer_version: modelInfo.version || "1.0.0",
        unified_scoring: true,
        thresholds: modelInfo.thresholds || {
          positive_threshold: 0.35,
          negative_threshold: 0.35,
          confidence_base: 0.6
        }
      });
    }
  } catch (error) {
    console.log("Unified API unavailable, using fallback data");
  }
  
  // Fallback data with unified scoring indicators
  return NextResponse.json({
    total: 8931,
    positive: 6.4,
    neutral: 75.8,
    negative: 17.7,
    accuracy: 73.4,
    confidence: 90.3,
    model: "Unified-Static-Fallback",
    unified_scoring: true,
    note: "Fallback data - unified API unavailable"
  });
}
