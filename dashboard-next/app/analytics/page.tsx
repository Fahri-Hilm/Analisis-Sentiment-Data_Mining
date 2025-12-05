"use client";

import { useState, useEffect } from "react";
import { Sidebar } from "@/components/Sidebar";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis } from "recharts";
import { TrendingUp, Users, Target, Brain, Activity, PieChart as PieIcon } from "lucide-react";

const EMOTION_COLORS = ["#f43f5e", "#8b5cf6", "#3b82f6", "#06b6d4", "#10b981", "#f59e0b"];
const TARGET_COLORS = ["#6366f1", "#14b8a6", "#f97316", "#ec4899", "#84cc16"];
const CONSTRUCT_COLORS = ["#22c55e", "#3b82f6", "#ef4444"];

export default function AnalyticsPage() {
  const [stats, setStats] = useState<any>(null);
  useEffect(() => { fetch("/api/stats").then(r => r.json()).then(setStats); }, []);

  if (!stats) return (<div className="flex h-screen bg-[#0a1628] text-white"><Sidebar /><div className="flex-1 flex items-center justify-center text-gray-400">Memuat...</div></div>);

  const emotionData = stats.topEmotions?.map((e: any, i: number) => ({ name: e.name, value: e.count, pct: parseFloat(e.percentage), fill: EMOTION_COLORS[i % 6] })) || [];
  const targetData = stats.topTargets?.map((t: any, i: number) => ({ name: t.name, value: t.count, pct: parseFloat(t.percentage), fill: TARGET_COLORS[i % 5] })) || [];
  const sentimentData = [{ name: "Negatif", value: stats.negative, pct: parseFloat(stats.negativePercent), fill: "#ef4444" }, { name: "Positif", value: stats.positive, pct: parseFloat(stats.positivePercent), fill: "#22c55e" }, { name: "Netral", value: stats.neutral, pct: parseFloat(stats.neutralPercent), fill: "#6b7280" }];
  const constructData = stats.constructiveness?.map((c: any, i: number) => ({ name: c.name, value: c.count, pct: parseFloat(c.percentage), fill: CONSTRUCT_COLORS[i % 3] })) || [];
  const radarData = emotionData.slice(0, 6).map((e: any) => ({ subject: e.name.split(" ")[0], value: e.pct }));

  return (
    <div className="flex h-screen bg-[#0a1628] text-white overflow-hidden">
      <Sidebar />
      <div className="flex-1 overflow-y-auto p-6">
        <div className="mb-6">
          <h1 className="text-2xl font-bold flex items-center gap-3"><Activity className="w-6 h-6 text-blue-400" />Analisis Mendalam: Suara Suporter</h1>
          <p className="text-gray-400 text-sm mt-1">Eksplorasi detail emosi, target kritik, dan pola sentimen</p>
        </div>

        <div className="grid grid-cols-4 gap-4 mb-6">
          <div className="bg-gradient-to-br from-blue-600/20 to-blue-900/20 rounded-xl p-4 border border-blue-500/30"><div className="flex items-center gap-2 text-blue-400 mb-2"><Users className="w-4 h-4" /><span className="text-xs">Total</span></div><div className="text-2xl font-bold">{stats.total.toLocaleString()}</div></div>
          <div className="bg-gradient-to-br from-green-600/20 to-green-900/20 rounded-xl p-4 border border-green-500/30"><div className="flex items-center gap-2 text-green-400 mb-2"><TrendingUp className="w-4 h-4" /><span className="text-xs">Akurasi</span></div><div className="text-2xl font-bold text-green-400">{stats.accuracy}%</div></div>
          <div className="bg-gradient-to-br from-purple-600/20 to-purple-900/20 rounded-xl p-4 border border-purple-500/30"><div className="flex items-center gap-2 text-purple-400 mb-2"><Brain className="w-4 h-4" /><span className="text-xs">F1-Score</span></div><div className="text-2xl font-bold text-purple-400">{stats.f1Score}%</div></div>
          <div className="bg-gradient-to-br from-red-600/20 to-red-900/20 rounded-xl p-4 border border-red-500/30"><div className="flex items-center gap-2 text-red-400 mb-2"><Target className="w-4 h-4" /><span className="text-xs">Dominan</span></div><div className="text-xl font-bold text-red-400">Negatif {stats.negativePercent}%</div></div>
        </div>

        <div className="grid grid-cols-2 gap-4 mb-6">
          <div className="bg-[#111c2e] rounded-xl p-6 border border-gray-800 flex flex-col justify-between">
            <div>
              <h3 className="text-lg font-semibold mb-6 text-center flex items-center justify-center gap-2">
                <PieIcon className="w-5 h-5 text-blue-400" />Distribusi Sentimen
              </h3>
              <div className="relative h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie data={sentimentData} cx="50%" cy="50%" innerRadius={80} outerRadius={110} paddingAngle={5} dataKey="value" stroke="none">
                      {sentimentData.map((e, i) => (<Cell key={i} fill={e.fill} />))}
                    </Pie>
                    <Tooltip contentStyle={{ backgroundColor: "#1a2744", border: "1px solid #374151", borderRadius: "8px" }} formatter={(v: number) => [v.toLocaleString(), "Komentar"]} />
                  </PieChart>
                </ResponsiveContainer>
                <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                  <span className="text-3xl font-bold text-white">{stats.total.toLocaleString()}</span>
                  <span className="text-xs text-gray-400 uppercase tracking-wider mt-1">Total</span>
                </div>
              </div>
            </div>
            <div className="grid grid-cols-3 gap-4 mt-4 border-t border-gray-800 pt-4">
              {sentimentData.map((item, i) => (
                <div key={i} className="flex flex-col items-center text-center">
                  <div className="flex items-center gap-2 mb-1">
                    <div className="w-2 h-2 rounded-full" style={{ backgroundColor: item.fill }} />
                    <span className="text-sm font-medium text-gray-300">{item.name}</span>
                  </div>
                  <span className="text-xs text-gray-500">{item.pct}%</span>
                </div>
              ))}
            </div>
          </div>
          <div className="bg-[#111c2e] rounded-xl p-4 border border-gray-800">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2"><Brain className="w-5 h-5 text-purple-400" />Distribusi Emosi</h3>
            <div className="h-64"><ResponsiveContainer width="100%" height="100%"><BarChart data={emotionData} layout="vertical" margin={{ left: 10, right: 20 }}><CartesianGrid strokeDasharray="3 3" stroke="#1f2937" vertical={false} /><XAxis type="number" stroke="#6b7280" fontSize={10} /><YAxis type="category" dataKey="name" stroke="#9ca3af" width={100} fontSize={10} /><Tooltip contentStyle={{ backgroundColor: "#1a2744", border: "1px solid #374151", borderRadius: "8px" }} formatter={(v: number, n: string, p: any) => [v.toLocaleString() + " (" + p.payload.pct + "%)", ""]} /><Bar dataKey="value" radius={[0, 6, 6, 0]}>{emotionData.map((e: any, i: number) => <Cell key={i} fill={e.fill} />)}</Bar></BarChart></ResponsiveContainer></div>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4 mb-6">
          <div className="bg-[#111c2e] rounded-xl p-4 border border-gray-800">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2"><Target className="w-5 h-5 text-cyan-400" />Target Kritik</h3>
            <div className="h-64"><ResponsiveContainer width="100%" height="100%"><BarChart data={targetData} margin={{ left: 10, right: 20, bottom: 30 }}><CartesianGrid strokeDasharray="3 3" stroke="#1f2937" vertical={false} /><XAxis dataKey="name" stroke="#9ca3af" fontSize={9} angle={-15} textAnchor="end" height={50} /><YAxis stroke="#6b7280" fontSize={10} /><Tooltip contentStyle={{ backgroundColor: "#1a2744", border: "1px solid #374151", borderRadius: "8px" }} formatter={(v: number, n: string, p: any) => [v.toLocaleString() + " (" + p.payload.pct + "%)", ""]} /><Bar dataKey="value" radius={[6, 6, 0, 0]}>{targetData.map((t: any, i: number) => <Cell key={i} fill={t.fill} />)}</Bar></BarChart></ResponsiveContainer></div>
          </div>
          <div className="bg-[#111c2e] rounded-xl p-6 border border-gray-800 flex flex-col justify-between">
            <div>
              <h3 className="text-lg font-semibold mb-6 text-center flex items-center justify-center gap-2">
                <Activity className="w-5 h-5 text-amber-400" />Konstruktivitas
              </h3>
              <div className="relative h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie data={constructData} cx="50%" cy="50%" innerRadius={80} outerRadius={110} paddingAngle={5} dataKey="value" stroke="none">
                      {constructData.map((c: any, i: number) => (<Cell key={i} fill={c.fill} />))}
                    </Pie>
                    <Tooltip contentStyle={{ backgroundColor: "#1a2744", border: "1px solid #374151", borderRadius: "8px" }} formatter={(v: number) => [v.toLocaleString(), "Komentar"]} />
                  </PieChart>
                </ResponsiveContainer>
                <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                  <span className="text-3xl font-bold text-amber-400">{constructData[0]?.pct || 0}%</span>
                  <span className="text-xs text-gray-400 uppercase tracking-wider mt-1">{constructData[0]?.name || "N/A"}</span>
                </div>
              </div>
            </div>
            <div className="grid grid-cols-3 gap-4 mt-4 border-t border-gray-800 pt-4">
              {constructData.map((item: any, i: number) => (
                <div key={i} className="flex flex-col items-center text-center">
                  <div className="flex items-center gap-2 mb-1">
                    <div className="w-2 h-2 rounded-full" style={{ backgroundColor: item.fill }} />
                    <span className="text-sm font-medium text-gray-300">{item.name}</span>
                  </div>
                  <span className="text-xs text-gray-500">{item.pct}%</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="bg-[#111c2e] rounded-xl p-4 border border-gray-800">
            <h3 className="text-lg font-semibold mb-4">Radar Emosi</h3>
            <div className="h-64"><ResponsiveContainer width="100%" height="100%"><RadarChart data={radarData}><PolarGrid stroke="#1f2937" /><PolarAngleAxis dataKey="subject" stroke="#9ca3af" fontSize={9} /><PolarRadiusAxis stroke="#6b7280" fontSize={8} /><Radar dataKey="value" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.5} strokeWidth={2} /></RadarChart></ResponsiveContainer></div>
          </div>
          <div className="bg-[#111c2e] rounded-xl p-4 border border-gray-800">
            <h3 className="text-lg font-semibold mb-4">Ringkasan</h3>
            <div className="grid grid-cols-2 gap-3">
              <div className="bg-red-500/10 rounded-lg p-3 border border-red-500/20"><div className="text-xl font-bold text-red-400">{stats.negative.toLocaleString()}</div><div className="text-xs text-gray-400">Negatif ({stats.negativePercent}%)</div></div>
              <div className="bg-green-500/10 rounded-lg p-3 border border-green-500/20"><div className="text-xl font-bold text-green-400">{stats.positive.toLocaleString()}</div><div className="text-xs text-gray-400">Positif ({stats.positivePercent}%)</div></div>
              <div className="bg-gray-500/10 rounded-lg p-3 border border-gray-500/20"><div className="text-xl font-bold text-gray-400">{stats.neutral.toLocaleString()}</div><div className="text-xs text-gray-400">Netral ({stats.neutralPercent}%)</div></div>
              <div className="bg-blue-500/10 rounded-lg p-3 border border-blue-500/20"><div className="text-xl font-bold text-blue-400">{stats.total.toLocaleString()}</div><div className="text-xs text-gray-400">Total</div></div>
            </div>
            <div className="mt-3 p-3 bg-[#0a1628] rounded-lg"><div className="text-xs text-gray-400 mb-2">Model Performance</div><div className="flex justify-between text-sm"><span>Acc: <span className="text-green-400 font-semibold">{stats.accuracy}%</span></span><span>F1: <span className="text-blue-400 font-semibold">{stats.f1Score}%</span></span><span>Conf: <span className="text-purple-400 font-semibold">{stats.confidence}%</span></span></div></div>
          </div>
        </div>
      </div>
    </div>
  );
}
