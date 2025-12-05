#!/usr/bin/env python3
"""Script to write clean page.tsx file"""

content = '''"use client";

import { useState, useEffect } from "react";
import {
  MessageSquare,
  TrendingUp,
  TrendingDown,
  Minus,
  Trophy,
  Activity,
  Target,
  Heart,
  Zap,
  Users,
  BarChart3,
  Smile,
  Frown,
  Meh,
} from "lucide-react";
import Sidebar from "../components/Sidebar";
import StatCard from "../components/StatCard";
import AreaChart from "../components/AreaChart";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";

interface StatsData {
  total_comments: number;
  sentiment_distribution: {
    positive: number;
    negative: number;
    neutral: number;
  };
  sentiment_percentage: {
    positive: number;
    negative: number;
    neutral: number;
  };
  football_emotions: { [key: string]: number };
  target_kritik: { [key: string]: number };
  constructiveness: { [key: string]: number };
  model_performance: {
    accuracy: number;
    f1_score: number;
    model_name: string;
    confidence: number;
  };
  sample_comments: Array<{
    text: string;
    sentiment: string;
    emotion?: string;
  }>;
}

function getEmotionEmoji(emotion: string): string {
  const emojiMap: { [key: string]: string } = {
    kekecewaan: "😞", disappointment: "😞",
    kemarahan: "😠", anger: "😠",
    harapan: "🙏", hope: "🙏",
    kesedihan: "😢", sadness: "😢",
    frustrasi: "😤", frustration: "😤",
    optimisme: "😊", optimism: "😊",
    dukungan: "💪", support: "💪",
    kritik: "📝", criticism: "📝",
    sarkasme: "😏", sarcasm: "😏",
    netral: "😐", neutral: "😐",
  };
  return emojiMap[emotion.toLowerCase()] || "📊";
}

function getTargetEmoji(target: string): string {
  const targetMap: { [key: string]: string } = {
    pssi: "🏛️", federation: "🏛️",
    pelatih: "👨‍🏫", coach: "👨‍🏫", coaching_staff: "👨‍🏫",
    pemain: "⚽", player: "⚽", players: "⚽",
    tim: "👥", team: "👥",
    wasit: "🟨", referee: "🟨",
    suporter: "📣", supporter: "📣", fans: "📣",
    media: "📺",
    umum: "🌐", general: "🌐",
  };
  return targetMap[target.toLowerCase()] || "🎯";
}

function getConstructEmoji(type: string): string {
  const constructMap: { [key: string]: string } = {
    konstruktif: "✅", constructive: "✅",
    destruktif: "❌", destructive: "❌",
    penuh_harapan: "🌟", hopeful: "🌟",
    netral: "➖", neutral: "➖",
  };
  return constructMap[type.toLowerCase()] || "📝";
}

function getConstructBg(type: string): string {
  const bgMap: { [key: string]: string } = {
    konstruktif: "bg-green-500/20 border-green-500/30",
    constructive: "bg-green-500/20 border-green-500/30",
    destruktif: "bg-red-500/20 border-red-500/30",
    destructive: "bg-red-500/20 border-red-500/30",
    penuh_harapan: "bg-yellow-500/20 border-yellow-500/30",
    hopeful: "bg-yellow-500/20 border-yellow-500/30",
    netral: "bg-gray-500/20 border-gray-500/30",
    neutral: "bg-gray-500/20 border-gray-500/30",
  };
  return bgMap[type.toLowerCase()] || "bg-slate-700/50 border-slate-600/50";
}

export default function Dashboard() {
  const [stats, setStats] = useState<StatsData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/stats")
      .then((res) => res.json())
      .then((data) => {
        setStats(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching stats:", err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="flex min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        <Sidebar />
        <main className="flex-1 p-8">
          <div className="flex items-center justify-center h-full">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
          </div>
        </main>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="flex min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        <Sidebar />
        <main className="flex-1 p-8">
          <div className="text-center text-red-400">
            <p>Error loading dashboard data</p>
          </div>
        </main>
      </div>
    );
  }

  const sentimentColors = ["#22c55e", "#eab308", "#ef4444"];
  const sentimentData = [
    { name: "Positive", value: stats.sentiment_distribution.positive },
    { name: "Neutral", value: stats.sentiment_distribution.neutral },
    { name: "Negative", value: stats.sentiment_distribution.negative },
  ];

  return (
    <div className="flex min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <Sidebar />
      <main className="flex-1 p-8 overflow-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">
            ⚽ Timnas Indonesia Sentiment Dashboard
          </h1>
          <p className="text-slate-400">
            Analisis sentimen komentar YouTube tentang Timnas Indonesia gagal lolos Piala Dunia 2026
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            title="Total Comments"
            value={stats.total_comments.toLocaleString()}
            icon={<MessageSquare className="w-6 h-6" />}
            color="blue"
          />
          <StatCard
            title="Positive"
            value={`${stats.sentiment_percentage.positive.toFixed(1)}%`}
            subtitle={`${stats.sentiment_distribution.positive.toLocaleString()} comments`}
            icon={<TrendingUp className="w-6 h-6" />}
            color="green"
          />
          <StatCard
            title="Neutral"
            value={`${stats.sentiment_percentage.neutral.toFixed(1)}%`}
            subtitle={`${stats.sentiment_distribution.neutral.toLocaleString()} comments`}
            icon={<Minus className="w-6 h-6" />}
            color="yellow"
          />
          <StatCard
            title="Negative"
            value={`${stats.sentiment_percentage.negative.toFixed(1)}%`}
            subtitle={`${stats.sentiment_distribution.negative.toLocaleString()} comments`}
            icon={<TrendingDown className="w-6 h-6" />}
            color="red"
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
            <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
              <BarChart3 className="w-5 h-5 text-blue-400" />
              Sentiment Distribution
            </h2>
            <AreaChart stats={stats} />
          </div>

          <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
            <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
              <Activity className="w-5 h-5 text-purple-400" />
              Sentiment Breakdown
            </h2>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={sentimentData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={5}
                    dataKey="value"
                    label={({ name, percent }) =>
                      `${name}: ${(percent * 100).toFixed(1)}%`
                    }
                  >
                    {sentimentData.map((entry, index) => (
                      <Cell
                        key={`cell-${index}`}
                        fill={sentimentColors[index % sentimentColors.length]}
                      />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#1e293b",
                      border: "1px solid #334155",
                      borderRadius: "8px",
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
            <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
              <Heart className="w-5 h-5 text-red-400" />
              Football Emotions
            </h2>
            <div className="grid grid-cols-2 gap-3">
              {Object.entries(stats.football_emotions || {})
                .sort(([, a], [, b]) => b - a)
                .slice(0, 6)
                .map(([emotion, count]) => (
                  <div
                    key={emotion}
                    className="bg-slate-700/50 rounded-lg p-3 border border-slate-600/50"
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-2xl">{getEmotionEmoji(emotion)}</span>
                      <span className="text-lg font-bold text-white">
                        {count.toLocaleString()}
                      </span>
                    </div>
                    <p className="text-sm text-slate-400 mt-1 capitalize">
                      {emotion.replace(/_/g, " ")}
                    </p>
                  </div>
                ))}
            </div>
          </div>

          <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
            <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
              <Target className="w-5 h-5 text-orange-400" />
              Target Kritik
            </h2>
            <div className="grid grid-cols-2 gap-3">
              {Object.entries(stats.target_kritik || {})
                .sort(([, a], [, b]) => b - a)
                .slice(0, 6)
                .map(([target, count]) => (
                  <div
                    key={target}
                    className="bg-slate-700/50 rounded-lg p-3 border border-slate-600/50"
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-2xl">{getTargetEmoji(target)}</span>
                      <span className="text-lg font-bold text-white">
                        {count.toLocaleString()}
                      </span>
                    </div>
                    <p className="text-sm text-slate-400 mt-1 capitalize">
                      {target.replace(/_/g, " ")}
                    </p>
                  </div>
                ))}
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
            <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
              <Zap className="w-5 h-5 text-yellow-400" />
              Constructiveness
            </h2>
            <div className="grid grid-cols-2 gap-3">
              {Object.entries(stats.constructiveness || {})
                .sort(([, a], [, b]) => b - a)
                .slice(0, 4)
                .map(([type, count]) => (
                  <div
                    key={type}
                    className={`rounded-lg p-4 border ${getConstructBg(type)}`}
                  >
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-2xl">{getConstructEmoji(type)}</span>
                      <span className="text-lg font-bold text-white">
                        {count.toLocaleString()}
                      </span>
                    </div>
                    <p className="text-sm text-slate-300 capitalize">
                      {type.replace(/_/g, " ")}
                    </p>
                  </div>
                ))}
            </div>
          </div>

          <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
            <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
              <Trophy className="w-5 h-5 text-yellow-400" />
              Model Performance
            </h2>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-slate-400">Model</span>
                <span className="text-white font-medium">
                  {stats.model_performance?.model_name || "SVM + TF-IDF"}
                </span>
              </div>
              <div>
                <div className="flex justify-between mb-1">
                  <span className="text-slate-400">Accuracy</span>
                  <span className="text-green-400 font-medium">
                    {((stats.model_performance?.accuracy || 0.894) * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="w-full bg-slate-700 rounded-full h-2">
                  <div
                    className="bg-green-500 h-2 rounded-full"
                    style={{
                      width: `${(stats.model_performance?.accuracy || 0.894) * 100}%`,
                    }}
                  ></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between mb-1">
                  <span className="text-slate-400">F1 Score</span>
                  <span className="text-blue-400 font-medium">
                    {((stats.model_performance?.f1_score || 0.91) * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="w-full bg-slate-700 rounded-full h-2">
                  <div
                    className="bg-blue-500 h-2 rounded-full"
                    style={{
                      width: `${(stats.model_performance?.f1_score || 0.91) * 100}%`,
                    }}
                  ></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between mb-1">
                  <span className="text-slate-400">Confidence</span>
                  <span className="text-purple-400 font-medium">
                    {((stats.model_performance?.confidence || 0.92) * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="w-full bg-slate-700 rounded-full h-2">
                  <div
                    className="bg-purple-500 h-2 rounded-full"
                    style={{
                      width: `${(stats.model_performance?.confidence || 0.92) * 100}%`,
                    }}
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
          <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
            <Users className="w-5 h-5 text-cyan-400" />
            Sample Comments
          </h2>
          <div className="space-y-3">
            {(stats.sample_comments || []).slice(0, 5).map((comment, idx) => (
              <div
                key={idx}
                className="bg-slate-700/50 rounded-lg p-4 border border-slate-600/50"
              >
                <div className="flex items-start gap-3">
                  <div
                    className={`p-2 rounded-full ${
                      comment.sentiment === "positive"
                        ? "bg-green-500/20"
                        : comment.sentiment === "negative"
                        ? "bg-red-500/20"
                        : "bg-yellow-500/20"
                    }`}
                  >
                    {comment.sentiment === "positive" ? (
                      <Smile className="w-5 h-5 text-green-400" />
                    ) : comment.sentiment === "negative" ? (
                      <Frown className="w-5 h-5 text-red-400" />
                    ) : (
                      <Meh className="w-5 h-5 text-yellow-400" />
                    )}
                  </div>
                  <div className="flex-1">
                    <p className="text-slate-300 text-sm">{comment.text}</p>
                    <div className="flex gap-2 mt-2">
                      <span
                        className={`text-xs px-2 py-1 rounded ${
                          comment.sentiment === "positive"
                            ? "bg-green-500/20 text-green-400"
                            : comment.sentiment === "negative"
                            ? "bg-red-500/20 text-red-400"
                            : "bg-yellow-500/20 text-yellow-400"
                        }`}
                      >
                        {comment.sentiment}
                      </span>
                      {comment.emotion && (
                        <span className="text-xs px-2 py-1 rounded bg-slate-600/50 text-slate-300">
                          {comment.emotion}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}
'''

with open('dashboard-next/app/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
print("File written successfully!")
