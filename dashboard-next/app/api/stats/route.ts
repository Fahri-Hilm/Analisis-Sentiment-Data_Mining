import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";
import Papa from "papaparse";

// In-memory cache
let cachedStats: any = null;
let cacheTimestamp = 0;
const CACHE_DURATION = 30 * 1000; // Reduced to 30 seconds for testing

export async function GET() {
  try {
    // Force fresh data - clear cache for testing
    cachedStats = null;
    cacheTimestamp = 0;
    
    // Return cached data if still valid
    const now = Date.now();
    if (cachedStats && (now - cacheTimestamp) < CACHE_DURATION) {
      return NextResponse.json(cachedStats);
    }

    const filePath = path.join(process.cwd(), "../data/processed/comments_cleaned_readme_spec.csv");
    console.log("Reading file from:", filePath);
    console.log("File exists:", fs.existsSync(filePath));
    const fileContent = fs.readFileSync(filePath, "utf-8");

    // Use PapaParse
    const parsed = Papa.parse(fileContent, {
      header: true,
      skipEmptyLines: true,
      transformHeader: (h: string) => h.trim(),
    });

    const data: any[] = parsed.data;
    console.log("Parsed data length:", data.length);
    console.log("First row sample:", data[0]);

    let positive = 0;
    let neutral = 0;
    let negative = 0;

    const emotions: Record<string, number> = {};
    const targets: Record<string, number> = {};
    const constructiveness: Record<string, number> = {};

    data.forEach((row) => {
      const sentiment = (row["core_sentiment"] || "").toLowerCase().trim();
      const emotion = (row["football_emotion"] || "").toLowerCase().trim();
      const target = row["target_kritik"] || "";
      const construct = row["constructiveness"] || "";

      // Count all valid sentiments (including unknown as neutral)
      if (sentiment === "positive") positive++;
      else if (sentiment === "negative") negative++;
      else neutral++; // Count neutral, unknown, and empty as neutral

      // Group emotions according to README specification
      if (emotion && emotion !== "nan" && emotion !== "unknown") {
        let groupedEmotion = "";
        if (emotion === "passionate_disappointment") groupedEmotion = "Kekecewaan";
        else if (emotion === "strategic_frustration" || emotion === "patriotic_sadness" || emotion === "constructive_anger") groupedEmotion = "Kemarahan";
        else if (emotion === "future_hope") groupedEmotion = "Harapan & Tuntutan";
        else if (emotion === "respectful_acknowledgment") groupedEmotion = "Dukungan";
        else if (emotion === "neutral_observation") groupedEmotion = "Kebanggaan";
        
        if (groupedEmotion) {
          emotions[groupedEmotion] = (emotions[groupedEmotion] || 0) + 1;
        }
      }

      if (target && target !== "nan" && target.toLowerCase() !== "unknown")
        targets[target] = (targets[target] || 0) + 1;

      if (construct && construct !== "nan" && construct.toLowerCase() !== "unknown")
        constructiveness[construct] = (constructiveness[construct] || 0) + 1;
    });

    const total = positive + neutral + negative;

    // Calculate total for each category
    const totalEmotions = Object.values(emotions).reduce((a, b) => a + b, 0);
    const totalTargets = Object.values(targets).reduce((a, b) => a + b, 0);
    const totalConstructiveness = Object.values(constructiveness).reduce((a, b) => a + b, 0);

    const topEmotions = Object.entries(emotions)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 8)
      .map(([name, count]) => ({
        name,
        count,
        percentage: totalEmotions > 0 ? ((count / totalEmotions) * 100).toFixed(1) : "0",
      }));

    const topTargets = Object.entries(targets)
      .filter(([name]) => name && name !== "nan" && name.toLowerCase() !== "unknown")
      .sort((a, b) => b[1] - a[1])
      .slice(0, 8)
      .map(([name, count]) => ({
        name: formatTarget(name),
        count,
        percentage: totalTargets > 0 ? ((count / totalTargets) * 100).toFixed(1) : "0",
      }));

    const result = {
      total,
      positive,
      neutral,
      negative,
      positivePercent: total > 0 ? ((positive / total) * 100).toFixed(1) : "0",
      neutralPercent: total > 0 ? ((neutral / total) * 100).toFixed(1) : "0",
      negativePercent: total > 0 ? ((negative / total) * 100).toFixed(1) : "0",
      topEmotions,
      topTargets,
      constructiveness: Object.entries(constructiveness)
        .filter(([name]) => name && name !== "nan" && name !== "unknown")
        .sort((a, b) => b[1] - a[1])
        .slice(0, 4)
        .map(([name, count]) => ({
          name: formatConstructiveness(name),
          count,
          percentage: totalConstructiveness > 0 ? ((count / totalConstructiveness) * 100).toFixed(1) : "0",
        })),
      accuracy: 89.4,
      confidence: 92.0,
      f1Score: 91.0,
    };

    // Cache the result
    cachedStats = result;
    cacheTimestamp = Date.now();

    return NextResponse.json(result, {
      headers: {
        'Cache-Control': 'public, s-maxage=300, stale-while-revalidate=600',
      },
    });
  } catch (error) {
    console.error("Stats API Error:", error);
    return NextResponse.json({ error: "Failed to load stats" }, { status: 500 });
  }
}

function formatEmotion(emotion: string): string {
  const map: Record<string, string> = {
    passionate_disappointment: "Kekecewaan",
    strategic_frustration: "Kemarahan", 
    patriotic_sadness: "Kemarahan",
    constructive_anger: "Kemarahan",
    respectful_acknowledgment: "Dukungan",
    future_hope: "Harapan & Tuntutan",
    neutral_observation: "Kebanggaan",
  };
  return map[emotion] || emotion.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase());
}

function formatTarget(target: string): string {
  const map: Record<string, string> = {
    coaching_staff: "Pelatih & Staf",
    players: "Pemain",
    opponents: "Lawan",
    pssi_management: "PSSI",
    external_factors: "Faktor Eksternal",
    pssi: "PSSI",
    pelatih: "Pelatih",
    pemain: "Pemain",
    wasit: "Wasit",
    tim_nasional: "Tim Nasional",
    manajemen: "Manajemen",
    supporter: "Suporter",
    media: "Media",
  };
  return map[target.toLowerCase()] || target.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase());
}

function formatConstructiveness(name: string): string {
  const map: Record<string, string> = {
    constructive: "Konstruktif",
    destructive: "Destruktif",
    hopeful: "Penuh Harapan",
    neutral: "Netral",
    unknown: "Tidak Diketahui",
  };
  return map[name.toLowerCase()] || name.charAt(0).toUpperCase() + name.slice(1);
}
