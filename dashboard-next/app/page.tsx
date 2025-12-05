"use client";

import { useState, useEffect } from "react";
import { MessageSquare, TrendingUp, TrendingDown, Minus, Activity, Target, BarChart3, Brain, AlertTriangle, Lightbulb } from "lucide-react";
import { Sidebar } from "../components/Sidebar";
import { StatCard } from "../components/StatCard";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid } from "recharts";

interface StatsData {
  total: number;
  positive: number;
  negative: number;
  neutral: number;
  positivePercent: string;
  negativePercent: string;
  neutralPercent: string;
  topEmotions: Array<{ name: string; count: number; percentage: string }>;
  topTargets: Array<{ name: string; count: number; percentage: string }>;
  constructiveness: Array<{ name: string; count: number; percentage: string }>;
  accuracy: number;
  f1Score: number;
  confidence: number;
}

export default function Dashboard() {
  const [stats, setStats] = useState<StatsData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/stats")
      .then((res) => res.json())
      .then((data) => { setStats(data); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  const pieData = stats ? [
    { name: "Negatif", value: stats.negative, color: "#ef4444" },
    { name: "Positif", value: stats.positive, color: "#22c55e" },
    { name: "Netral", value: stats.neutral, color: "#6b7280" },
  ] : [];

  const emotionData = stats?.topEmotions?.map((e, i) => ({
    name: e.name,
    value: e.count,
    pct: e.percentage,
    fill: ["#f43f5e", "#8b5cf6", "#3b82f6", "#06b6d4", "#10b981", "#f59e0b"][i % 6]
  })) || [];

  if (loading) {
    return (
      <div className="flex h-screen bg-[#0a1628] text-white">
        <Sidebar />
        <main className="flex-1 p-6 flex items-center justify-center">
          <div className="text-gray-400">Memuat data...</div>
        </main>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-[#0a1628] text-white overflow-hidden">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-8 bg-[#0a1628]">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white tracking-tight mb-2">Garuda: Mimpi Dunia yang Tertunda</h1>
          <p className="text-gray-400 text-base font-light tracking-wide">Analisis sentimen dan opini publik di balik kegagalan kualifikasi Timnas Indonesia</p>
        </div>

        <div className="grid grid-cols-4 gap-4 mb-6">
          <StatCard label="Total Komentar" value={stats?.total.toLocaleString() || "0"} icon={MessageSquare} change="Dataset lengkap" trend="up" />
          <StatCard label="Sentimen Negatif" value={stats?.negativePercent + "%" || "0%"} icon={TrendingDown} change={stats?.negative.toLocaleString() + " komentar"} trend="up" />
          <StatCard label="Sentimen Positif" value={stats?.positivePercent + "%" || "0%"} icon={TrendingUp} change={stats?.positive.toLocaleString() + " komentar"} trend="up" />
          <StatCard label="Sentimen Netral" value={stats?.neutralPercent + "%" || "0%"} icon={Minus} change={stats?.neutral.toLocaleString() + " komentar"} trend="down" />
        </div>

        <div className="grid grid-cols-2 gap-4 mb-6">
          <div className="bg-[#111c2e] rounded-xl p-6 border border-gray-800 flex flex-col justify-between">
            <div>
              <h3 className="text-lg font-semibold mb-6 text-center">Distribusi Sentimen</h3>
              <div className="relative h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie data={pieData} cx="50%" cy="50%" innerRadius={80} outerRadius={110} paddingAngle={5} dataKey="value" stroke="none">
                      {pieData.map((entry, index) => (<Cell key={index} fill={entry.color} />))}
                    </Pie>
                    <Tooltip contentStyle={{ backgroundColor: "#1a2744", border: "1px solid #374151", borderRadius: "8px" }} formatter={(value: number) => [value.toLocaleString(), "Komentar"]} />
                  </PieChart>
                </ResponsiveContainer>
                <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                  <span className="text-3xl font-bold text-white">{stats?.total.toLocaleString()}</span>
                  <span className="text-xs text-gray-400 uppercase tracking-wider mt-1">Total</span>
                </div>
              </div>
            </div>
            <div className="grid grid-cols-3 gap-4 mt-4 border-t border-gray-800 pt-4">
              {pieData.map((item, i) => (
                <div key={i} className="flex flex-col items-center text-center">
                  <div className="flex items-center gap-2 mb-1">
                    <div className="w-2 h-2 rounded-full" style={{ backgroundColor: item.color }} />
                    <span className="text-sm font-medium text-gray-300">{item.name}</span>
                  </div>
                  <span className="text-xs text-gray-500">{i === 0 ? stats?.negativePercent : i === 1 ? stats?.positivePercent : stats?.neutralPercent}%</span>
                </div>
              ))}
            </div>
          </div>
          <div className="bg-[#111c2e] rounded-xl p-6 border border-gray-800 flex flex-col justify-between">
            <div>
              <h3 className="text-lg font-semibold mb-6 text-center flex items-center justify-center gap-2">
                <Brain className="w-5 h-5 text-purple-400" />Dominasi Emosi
              </h3>
              <div className="h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={emotionData} layout="vertical" margin={{ left: 0, right: 20, top: 0, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" horizontal={false} />
                    <XAxis type="number" stroke="#6b7280" fontSize={10} hide />
                    <YAxis type="category" dataKey="name" stroke="#9ca3af" width={100} fontSize={11} tickLine={false} axisLine={false} />
                    <Tooltip 
                      cursor={{ fill: '#1f2937', opacity: 0.4 }}
                      contentStyle={{ backgroundColor: "#1a2744", border: "1px solid #374151", borderRadius: "8px" }} 
                      formatter={(value: number, name: string, props: any) => [value.toLocaleString() + " (" + props.payload.pct + "%)", "Komentar"]} 
                    />
                    <Bar dataKey="value" radius={[0, 4, 4, 0]} barSize={24}>
                      {emotionData.map((entry, index) => (
                        <Cell key={index} fill={entry.fill} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
            <div className="grid grid-cols-3 gap-2 mt-4 border-t border-gray-800 pt-4">
               {emotionData.slice(0, 3).map((item, i) => (
                <div key={i} className="flex flex-col items-center text-center">
                  <span className="text-xs font-medium text-gray-400 mb-1">{item.name}</span>
                  <span className="text-lg font-bold" style={{ color: item.fill }}>{item.pct}%</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4 mb-6">
          <div className="bg-[#111c2e] rounded-xl p-4 border border-gray-800">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2"><Target className="w-5 h-5 text-cyan-400" />Target Kritik Utama</h3>
            <div className="space-y-4">
              {stats?.topTargets?.slice(0, 5).map((target, i) => (
                <div key={i} className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-6 h-6 rounded-full bg-cyan-500/20 flex items-center justify-center text-xs font-bold text-cyan-400">{i + 1}</div>
                    <span className="text-gray-300 capitalize text-sm">{target.name.replace(/_/g, " ")}</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="w-32 h-2 bg-gray-700 rounded-full overflow-hidden">
                      <div className="h-full bg-cyan-500 rounded-full" style={{ width: parseFloat(target.percentage) + "%" }} />
                    </div>
                    <span className="text-xs text-gray-400 w-12 text-right font-mono">{target.percentage}%</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
          <div className="bg-[#111c2e] rounded-xl p-4 border border-gray-800">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2"><BarChart3 className="w-5 h-5 text-amber-400" />Sifat Komentar (Konstruktivitas)</h3>
            <div className="space-y-4">
              {stats?.constructiveness?.map((item, i) => (
                <div key={i} className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className={`w-2 h-2 rounded-full ${i === 0 ? "bg-green-500" : i === 1 ? "bg-amber-500" : "bg-red-500"}`} />
                    <span className="text-gray-300 capitalize text-sm">{item.name.replace(/_/g, " ")}</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="w-32 h-2 bg-gray-700 rounded-full overflow-hidden">
                      <div className={`h-full rounded-full ${i === 0 ? "bg-green-500" : i === 1 ? "bg-amber-500" : "bg-red-500"}`} style={{ width: parseFloat(item.percentage) + "%" }} />
                    </div>
                    <span className="text-xs text-gray-400 w-12 text-right font-mono">{item.percentage}%</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="bg-[#111c2e] rounded-xl p-4 border border-gray-800 mb-6">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2"><Activity className="w-5 h-5 text-green-400" />Performa Model ML</h3>
          <div className="grid grid-cols-3 gap-4">
            <div className="text-center p-4 bg-[#0a1628] rounded-lg">
              <div className="text-3xl font-bold text-green-400">{stats?.accuracy || 89.4}%</div>
              <div className="text-sm text-gray-400 mt-1">Akurasi</div>
            </div>
            <div className="text-center p-4 bg-[#0a1628] rounded-lg">
              <div className="text-3xl font-bold text-blue-400">{stats?.f1Score || 91.0}%</div>
              <div className="text-sm text-gray-400 mt-1">F1-Score</div>
            </div>
            <div className="text-center p-4 bg-[#0a1628] rounded-lg">
              <div className="text-3xl font-bold text-purple-400">{stats?.confidence || 92.0}%</div>
              <div className="text-sm text-gray-400 mt-1">Confidence</div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4">
          <div className="bg-[#111c2e] rounded-xl p-4 border border-gray-800">
            <div className="flex items-center gap-2 mb-3"><AlertTriangle className="w-5 h-5 text-red-400" /><h4 className="font-semibold text-red-400">Temuan Utama</h4></div>
            <p className="text-sm text-gray-300">{stats?.negativePercent || "69.8"}% komentar bersifat negatif, menunjukkan tingkat kekecewaan tinggi publik.</p>
          </div>
          <div className="bg-[#111c2e] rounded-xl p-4 border border-gray-800">
            <div className="flex items-center gap-2 mb-3"><Target className="w-5 h-5 text-cyan-400" /><h4 className="font-semibold text-cyan-400">Target Kritik</h4></div>
            <p className="text-sm text-gray-300">PSSI dan pelatih menjadi sasaran utama kritik dengan lebih dari 40% komentar negatif.</p>
          </div>
          <div className="bg-[#111c2e] rounded-xl p-4 border border-gray-800">
            <div className="flex items-center gap-2 mb-3"><Lightbulb className="w-5 h-5 text-amber-400" /><h4 className="font-semibold text-amber-400">Rekomendasi</h4></div>
            <p className="text-sm text-gray-300">Perlu transparansi komunikasi dari PSSI dan evaluasi menyeluruh untuk memulihkan kepercayaan.</p>
          </div>
        </div>
      </main>
    </div>
  );
}
