import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";
import Papa from "papaparse";

// In-memory cache
let cachedComments: any = null;
let cacheTimestamp = 0;
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

export async function GET(req: Request) {
  try {
    const { searchParams } = new URL(req.url);
    const search = searchParams.get("search")?.toLowerCase() || "";

    // Helper to filter comments
    const filterComments = (list: any[]) => {
      if (!search) return list;
      return list.filter(c => c.text.toLowerCase().includes(search));
    };

    // Return cached data if still valid
    const now = Date.now();
    if (cachedComments && (now - cacheTimestamp) < CACHE_DURATION) {
      return NextResponse.json({ comments: filterComments(cachedComments) });
    }

    const filePath = path.join(process.cwd(), "../data/processed/comments_cleaned_readme_spec.csv");
    const fileContent = fs.readFileSync(filePath, "utf-8");

    // Use PapaParse with preview for optimization
    // We load more than 200 now (e.g., 1000) because PapaParse is fast
    const parsed = Papa.parse(fileContent, {
      header: true,
      skipEmptyLines: true,
      preview: 1000, // Optimization: Stop after 1000 rows
      transformHeader: (h: string) => h.trim(),
    });

    const data: any[] = parsed.data;

    const comments = data.map((row: any, index: number) => {
      // Robust property access
      const text = row["clean_text"] || row["text"] || "No text";
      const sentiment = row["core_sentiment"] || "";
      const emotion = row["football_emotion"] || "neutral_observation";
      const target = row["target_kritik"] || "Umum";
      const construct = row["constructiveness"] || "unknown";
      const confidence = row["emotion_confidence"] || "0.85";
      const date = row["published_at"] || "2024-10-01";

      return {
        id: index + 1,
        text: text,
        sentiment: mapSentiment(sentiment),
        emotion: emotion,
        category: mapCategory(emotion),
        target: target,
        constructiveness: construct,
        confidence: parseFloat(confidence) * 100 || 85,
        date: date.split("T")[0],
      };
    });

    // Cache the result (CACHE ALL DATA)
    cachedComments = comments;
    cacheTimestamp = Date.now();

    return NextResponse.json({ comments: filterComments(comments) }, {
      headers: {
        'Cache-Control': 'public, s-maxage=300, stale-while-revalidate=600',
      },
    });
  } catch (error) {
    console.error("API Error:", error);
    return NextResponse.json({ error: "Failed to load comments" }, { status: 500 });
  }
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
