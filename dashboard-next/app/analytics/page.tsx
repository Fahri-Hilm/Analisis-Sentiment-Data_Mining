"use client";

import { useState, useEffect } from "react";
import { PieChart, Pie, Cell, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip } from "recharts";
import { TrendingUp, Users, Target, Brain, Activity, PieChart as PieIcon } from "lucide-react";
import { OptimizedEmotionChart, OptimizedTargetChart, OptimizedPieChart } from "@/components/OptimizedCharts";

const CONSTRUCT_COLORS = ["#22c55e", "#3b82f6", "#ef4444"];

import { useDashboardStats } from "@/hooks/useDashboardStats";

export default function AnalyticsPage() {
  const { stats } = useDashboardStats();

  if (!stats) return (<div className="flex-1 flex items-center justify-center h-screen text-slate-400 bg-transparent">Memuat Data Analisis...</div>);

  const sentimentData = [{ name: "Negatif", value: stats.negative, pct: parseFloat(stats.negativePercent), fill: "#ef4444" }, { name: "Positif", value: stats.positive, pct: parseFloat(stats.positivePercent), fill: "#22c55e" }, { name: "Netral", value: stats.neutral, pct: parseFloat(stats.neutralPercent), fill: "#6b7280" }];
  const constructData = stats.constructiveness?.map((c: any, i: number) => ({ name: c.name, value: c.count, pct: parseFloat(c.percentage), fill: CONSTRUCT_COLORS[i % 3] })) || [];
  const radarData = stats.topEmotions?.slice(0, 6).map((e: any) => ({ subject: e.name.split(" ")[0], value: parseFloat(e.percentage) })) || [];

  return (
    <div className="max-w-7xl mx-auto p-8 relative">
      <div className="absolute top-0 right-0 w-full h-[500px] bg-blue-500/5 rounded-full blur-[100px] pointer-events-none -translate-y-1/2" />

      <div className="mb-10 relative z-10">
        <h1 className="text-4xl font-bold flex items-center gap-3 bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent"><Activity className="w-8 h-8 text-blue-400" />Analisis Mendalam: Suara Suporter</h1>
        <p className="text-slate-400 text-lg mt-2 font-light tracking-wide">Eksplorasi detail emosi, target kritik, dan pola sentimen</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8 relative z-10">
        <div className="glass-card rounded-xl p-6 border border-blue-500/20"><div className="flex items-center gap-2 text-blue-400 mb-2 font-medium"><Users className="w-4 h-4" /><span className="text-xs uppercase tracking-wider">Total</span></div><div className="text-3xl font-bold text-white">{stats.total.toLocaleString()}</div></div>
        <div className="glass-card rounded-xl p-6 border border-green-500/20"><div className="flex items-center gap-2 text-green-400 mb-2 font-medium"><TrendingUp className="w-4 h-4" /><span className="text-xs uppercase tracking-wider">Akurasi</span></div><div className="text-3xl font-bold text-green-400">{stats.accuracy}%</div></div>
        <div className="glass-card rounded-xl p-6 border border-purple-500/20"><div className="flex items-center gap-2 text-purple-400 mb-2 font-medium"><Brain className="w-4 h-4" /><span className="text-xs uppercase tracking-wider">F1-Score</span></div><div className="text-3xl font-bold text-purple-400">{stats.f1Score}%</div></div>
        <div className="glass-card rounded-xl p-6 border border-red-500/20"><div className="flex items-center gap-2 text-red-400 mb-2 font-medium"><Target className="w-4 h-4" /><span className="text-xs uppercase tracking-wider">Dominan</span></div><div className="text-2xl font-bold text-red-400">Negatif {stats.negativePercent}%</div></div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8 relative z-10">
        <div className="glass-card rounded-2xl p-6 border border-slate-800/50 flex flex-col">
          <div>
            <h3 className="text-lg font-semibold mb-8 text-center flex items-center justify-center gap-2 text-slate-200">
              <PieIcon className="w-5 h-5 text-blue-400" />Distribusi Sentimen
            </h3>
            <div className="relative h-72 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={sentimentData} cx="50%" cy="50%" innerRadius={80} outerRadius={110} paddingAngle={5} dataKey="value" stroke="none">
                    {sentimentData.map((e, i) => (<Cell key={i} fill={e.fill} />))}
                  </Pie>
                  <Tooltip contentStyle={{ backgroundColor: "#020617", border: "1px solid #1e293b", borderRadius: "12px", boxShadow: "0 10px 15px -3px rgba(0, 0, 0, 0.5)" }} formatter={(v: number) => [v.toLocaleString(), "Komentar"]} itemStyle={{ color: '#fff' }} />
                </PieChart>
              </ResponsiveContainer>
              <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                <span className="text-4xl font-bold text-white">{stats.total.toLocaleString()}</span>
                <span className="text-xs text-slate-400 uppercase tracking-widest mt-1 font-medium">Total</span>
              </div>
            </div>
          </div>
          <div className="grid grid-cols-3 gap-4 mt-8 border-t border-slate-800/50 pt-6">
            {sentimentData.map((item, i) => (
              <div key={i} className="flex flex-col items-center text-center">
                <div className="flex items-center gap-2 mb-1">
                  <div className="w-2.5 h-2.5 rounded-full shadow-[0_0_8px]" style={{ backgroundColor: item.fill, boxShadow: `0 0 8px ${item.fill}` }} />
                  <span className="text-sm font-medium text-slate-300">{item.name}</span>
                </div>
                <span className="text-xs text-slate-500 font-mono">{item.pct}%</span>
              </div>
            ))}
          </div>
        </div>
        <div className="glass-card rounded-2xl p-6 border border-slate-800/50">
          <h3 className="text-lg font-semibold mb-6 flex items-center gap-2 text-slate-200"><Brain className="w-5 h-5 text-purple-400" />Distribusi Emosi</h3>
          <div className="h-80"><OptimizedEmotionChart data={stats.topEmotions} /></div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8 relative z-10">
        <div className="glass-card rounded-2xl p-6 border border-slate-800/50">
          <h3 className="text-lg font-semibold mb-6 flex items-center gap-2 text-slate-200"><Target className="w-5 h-5 text-cyan-400" />Target Kritik</h3>
          <div className="h-80"><OptimizedTargetChart data={stats.topTargets} /></div>
        </div>
        <div className="glass-card rounded-2xl p-6 border border-slate-800/50 flex flex-col justify-between">
          <div>
            <h3 className="text-lg font-semibold mb-8 text-center flex items-center justify-center gap-2 text-slate-200">
              <Activity className="w-5 h-5 text-amber-400" />Konstruktivitas
            </h3>
            <div className="relative h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={constructData} cx="50%" cy="50%" innerRadius={80} outerRadius={110} paddingAngle={5} dataKey="value" stroke="none">
                    {constructData.map((c: any, i: number) => (<Cell key={i} fill={c.fill} />))}
                  </Pie>
                  <Tooltip contentStyle={{ backgroundColor: "#020617", border: "1px solid #1e293b", borderRadius: "12px" }} formatter={(v: number) => [v.toLocaleString(), "Komentar"]} itemStyle={{ color: '#fff' }} />
                </PieChart>
              </ResponsiveContainer>
              <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                <span className="text-4xl font-bold text-amber-400">{constructData[0]?.pct || 0}%</span>
                <span className="text-xs text-slate-400 uppercase tracking-wider mt-1 font-medium">{constructData[0]?.name || "N/A"}</span>
              </div>
            </div>
          </div>
          <div className="grid grid-cols-3 gap-4 mt-4 border-t border-slate-800/50 pt-6">
            {constructData.map((item: any, i: number) => (
              <div key={i} className="flex flex-col items-center text-center">
                <div className="flex items-center gap-2 mb-1">
                  <div className="w-2.5 h-2.5 rounded-full shadow-[0_0_8px]" style={{ backgroundColor: item.fill, boxShadow: `0 0 8px ${item.fill}` }} />
                  <span className="text-sm font-medium text-slate-300">{item.name}</span>
                </div>
                <span className="text-xs text-slate-500 font-mono">{item.pct}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 relative z-10">
        <div className="glass-card rounded-2xl p-6 border border-slate-800/50">
          <h3 className="text-lg font-semibold mb-6 text-slate-200">Radar Emosi</h3>
          <div className="h-72"><ResponsiveContainer width="100%" height="100%"><RadarChart data={radarData}><PolarGrid stroke="#1e293b" /><PolarAngleAxis dataKey="subject" stroke="#94a3b8" fontSize={11} /><PolarRadiusAxis stroke="#64748b" fontSize={10} /><Radar dataKey="value" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.4} strokeWidth={2} /></RadarChart></ResponsiveContainer></div>
        </div>
        <div className="glass-card rounded-2xl p-6 border border-slate-800/50">
          <h3 className="text-lg font-semibold mb-6 text-slate-200">Ringkasan</h3>
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-rose-500/10 rounded-xl p-4 border border-rose-500/20"><div className="text-2xl font-bold text-rose-400">{stats.negative.toLocaleString()}</div><div className="text-xs text-rose-300/70 mt-1 uppercase tracking-wider">Negatif ({stats.negativePercent}%)</div></div>
            <div className="bg-emerald-500/10 rounded-xl p-4 border border-emerald-500/20"><div className="text-2xl font-bold text-emerald-400">{stats.positive.toLocaleString()}</div><div className="text-xs text-emerald-300/70 mt-1 uppercase tracking-wider">Positif ({stats.positivePercent}%)</div></div>
            <div className="bg-slate-500/10 rounded-xl p-4 border border-slate-500/20"><div className="text-2xl font-bold text-slate-400">{stats.neutral.toLocaleString()}</div><div className="text-xs text-slate-400/70 mt-1 uppercase tracking-wider">Netral ({stats.neutralPercent}%)</div></div>
            <div className="bg-blue-500/10 rounded-xl p-4 border border-blue-500/20"><div className="text-2xl font-bold text-blue-400">{stats.total.toLocaleString()}</div><div className="text-xs text-blue-300/70 mt-1 uppercase tracking-wider">Total</div></div>
          </div>
          <div className="mt-4 p-4 bg-slate-900/50 rounded-xl border border-slate-800"><div className="text-xs text-slate-400 mb-2 font-medium uppercase tracking-wider">Model Performance</div><div className="flex justify-between text-sm"><span>Acc: <span className="text-green-400 font-bold">{stats.accuracy}%</span></span><span>F1: <span className="text-blue-400 font-bold">{stats.f1Score}%</span></span><span>Conf: <span className="text-purple-400 font-bold">{stats.confidence}%</span></span></div></div>
        </div>
      </div>
    </div>
  );
}
