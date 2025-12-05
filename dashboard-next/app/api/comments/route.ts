import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

export async function GET() {
  try {
    const filePath = path.join(process.cwd(), "../data/processed/comments_cleaned_retrained.csv");
    const fileContent = fs.readFileSync(filePath, "utf-8");
    const lines = fileContent.split("\n");
    const header = lines[0].split(",");
    const dataLines = lines.slice(1, 201); // Get 200 comments
    
    // Find column indices
    const getIndex = (name: string) => header.findIndex(h => h.trim().toLowerCase().includes(name.toLowerCase()));
    
    const cleanTextIdx = getIndex("clean_text");
    const textIdx = getIndex("text");
    const sentimentIdx = getIndex("core_sentiment");
    const emotionIdx = getIndex("football_emotion");
    const targetIdx = getIndex("target_kritik");
    const constructivenessIdx = getIndex("constructiveness");
    const dateIdx = getIndex("published_at");
    const confidenceIdx = getIndex("emotion_confidence");
    
    const comments = dataLines
      .filter((line) => line.trim())
      .map((line, index) => {
        const parts = parseCSVLine(line);
        return {
          id: index + 1,
          text: parts[cleanTextIdx] || parts[textIdx] || "No text",
          sentiment: mapSentiment(parts[sentimentIdx] || ""),
          emotion: parts[emotionIdx] || "neutral_observation",
          category: mapCategory(parts[emotionIdx] || ""),
          target: parts[targetIdx] || "Umum",
          constructiveness: parts[constructivenessIdx] || "unknown",
          confidence: parseFloat(parts[confidenceIdx]) * 100 || 85,
          date: parts[dateIdx]?.split("T")[0] || "2024-10-01",
        };
      });

    return NextResponse.json(comments);
  } catch (error) {
    console.error("API Error:", error);
    return NextResponse.json({ error: "Failed to load comments" }, { status: 500 });
  }
}

// Parse CSV line handling quoted fields
function parseCSVLine(line: string): string[] {
  const result: string[] = [];
  let current = "";
  let inQuotes = false;
  
  for (let i = 0; i < line.length; i++) {
    const char = line[i];
    if (char === '"') {
      inQuotes = !inQuotes;
    } else if (char === ',' && !inQuotes) {
      result.push(current.trim());
      current = "";
    } else {
      current += char;
    }
  }
  result.push(current.trim());
  return result;
}

function mapSentiment(label: string): string {
  if (!label) return "neutral";
  const lower = label.toLowerCase();
  if (lower === "positive") return "positive";
  if (lower === "negative") return "negative";
  return "neutral";
}

function mapCategory(emotion: string): string {
  if (!emotion) return "General Comment";
  const lower = emotion.toLowerCase();
  if (lower.includes("passionate_disappointment")) return "Passionate Disappointment";
  if (lower.includes("strategic_frustration")) return "Strategic Frustration";
  if (lower.includes("patriotic_sadness")) return "Patriotic Sadness";
  if (lower.includes("constructive_anger")) return "Constructive Anger";
  if (lower.includes("respectful_acknowledgment")) return "Respectful Acknowledgment";
  if (lower.includes("future_hope")) return "Future Hope";
  if (lower.includes("neutral_observation")) return "Neutral Observation";
  return "General Comment";
}
