import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

// In-memory cache
let cachedStats: any = null;
let cacheTimestamp = 0;
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

export async function GET() {
  try {
    // Return cached data if still valid
    const now = Date.now();
    if (cachedStats && (now - cacheTimestamp) < CACHE_DURATION) {
      return NextResponse.json(cachedStats);
    }

    const filePath = path.join(process.cwd(), "../data/processed/comments_cleaned_retrained.csv");
    const fileContent = fs.readFileSync(filePath, "utf-8");
    const lines = fileContent.split("\n");
    const header = parseCSVLine(lines[0]);
    const expectedCols = header.length;
    
    // Filter valid data lines
    const dataLines = lines.slice(1).filter((line) => {
      if (!line.trim()) return false;
      const parts = parseCSVLine(line);
      return parts.length >= expectedCols - 5;
    });
    
    // Find column indices
    const getIndex = (name: string) => header.findIndex(h => h.trim().toLowerCase().includes(name.toLowerCase()));
    
    const sentimentIdx = getIndex("core_sentiment");
    const emotionIdx = getIndex("football_emotion");
    const targetIdx = getIndex("target_kritik");
    const constructivenessIdx = getIndex("constructiveness");
    
    let positive = 0;
    let neutral = 0;
    let negative = 0;
    
    const emotions: Record<string, number> = {};
    const targets: Record<string, number> = {};
    const constructiveness: Record<string, number> = {};
    
    dataLines.forEach((line) => {
      const parts = parseCSVLine(line);
      if (parts.length < sentimentIdx + 1) return;
      
      const sentiment = (parts[sentimentIdx] || "").toLowerCase().trim();
      const emotion = (parts[emotionIdx] || "").toLowerCase().trim();
      const target = parts[targetIdx] || "";
      const construct = parts[constructivenessIdx] || "";
      
      if (sentiment === "positive") positive++;
      else if (sentiment === "negative") negative++;
      else if (sentiment === "neutral") neutral++;
      
      if (emotion && emotion !== "nan" && emotion !== "unknown" && emotion !== "neutral_observation") emotions[emotion] = (emotions[emotion] || 0) + 1;
      if (target && target !== "nan" && target.toLowerCase() !== "unknown") targets[target] = (targets[target] || 0) + 1;
      if (construct && construct !== "nan" && construct.toLowerCase() !== "unknown") constructiveness[construct] = (constructiveness[construct] || 0) + 1;
    });
    
    const total = positive + neutral + negative;
    
    // Calculate total for each category (excluding empty/nan/neutral_observation values)
    const totalEmotions = Object.values(emotions).reduce((a, b) => a + b, 0);
    const totalTargets = Object.values(targets).reduce((a, b) => a + b, 0);
    const totalConstructiveness = Object.values(constructiveness).reduce((a, b) => a + b, 0);
    
    const topEmotions = Object.entries(emotions)
      .filter(([name]) => name && name !== "nan" && name !== "unknown" && name !== "neutral_observation")
      .sort((a, b) => b[1] - a[1])
      .slice(0, 8)
      .map(([name, count]) => ({
        name: formatEmotion(name),
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
      positivePercent: ((positive / total) * 100).toFixed(1),
      neutralPercent: ((neutral / total) * 100).toFixed(1),
      negativePercent: ((negative / total) * 100).toFixed(1),
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

function formatEmotion(emotion: string): string {
  const map: Record<string, string> = {
    passionate_disappointment: "Kecewa Mendalam",
    strategic_frustration: "Frustrasi Taktik",
    patriotic_sadness: "Kesedihan Patriotik",
    constructive_anger: "Amarah Konstruktif",
    respectful_acknowledgment: "Respek",
    future_hope: "Harapan & Tuntutan",
    neutral_observation: "Observasi Netral",
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
