import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({
    total: 8931,
    positive: 6.4,
    neutral: 75.8,
    negative: 17.7,
    accuracy: 71.9,
    confidence: 90.3,
  });
}
