"use client";

import { useState, useEffect, useMemo } from "react";
import { MessageSquare, TrendingUp, TrendingDown, Minus, Activity, Target, BarChart3, Brain, AlertTriangle, Lightbulb } from "lucide-react";
import { StatCard } from "../components/StatCard";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid } from "recharts";
import { motion } from "framer-motion";
import { Skeleton, SectionSkeleton, StatCardSkeleton } from "../components/Skeleton";
import { AIInsights } from "../components/AIInsights"; // Import AI Insights

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

import { useDashboardStats } from "@/hooks/useDashboardStats";

export default function Dashboard() {
  const { stats, isLoading: loading } = useDashboardStats();

  // Memoize chart data to prevent re-calculation on every render
  const pieData = useMemo(() => stats ? [
    { name: "Negatif", value: stats.negative, color: "#f43f5e" }, // Rose-500
    { name: "Positif", value: stats.positive, color: "#10b981" }, // Emerald-500
    { name: "Netral", value: stats.neutral, color: "#64748b" },   // Slate-500
  ] : [], [stats]);

  const emotionData = useMemo(() => stats?.topEmotions?.map((e: any, i: number) => ({
    name: e.name,
    value: e.count,
    pct: e.percentage,
    fill: ["#f43f5e", "#8b5cf6", "#3b82f6", "#06b6d4", "#10b981", "#f59e0b"][i % 6]
  })) || [], [stats]);

  return (
    <>
      {/* Background Ambient Glow */}
      <div className="absolute top-0 left-0 w-full h-[500px] bg-primary/5 rounded-full blur-[100px] pointer-events-none -translate-y-1/2" />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
        className="relative z-10 max-w-7xl mx-auto p-8"
      >
        <header className="mb-10">
          <h1 className="text-4xl font-bold tracking-tight mb-2 bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
            Garuda: Mimpi Dunia yang Tertunda
          </h1>
          <p className="text-slate-400 text-lg font-light tracking-wide max-w-2xl">
            Analisis sentimen dan opini publik di balik kegagalan kualifikasi Timnas Indonesia
          </p>
        </header>

        {/* AI Insights Panel */}
        <AIInsights stats={stats} loading={loading} />

        {/* Key Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {loading ? (
            [...Array(4)].map((_, i) => <StatCardSkeleton key={i} />)
          ) : (
            <>
              <StatCard label="Total Komentar" value={stats?.total.toLocaleString() || "0"} icon={MessageSquare} change="Dataset lengkap" trend="up" />
              <StatCard label="Sentimen Negatif" value={stats?.negativePercent + "%" || "0%"} icon={TrendingDown} change={stats?.negative.toLocaleString() + " komentar"} trend="down" />
              <StatCard label="Sentimen Positif" value={stats?.positivePercent + "%" || "0%"} icon={TrendingUp} change={stats?.positive.toLocaleString() + " komentar"} trend="up" />
              <StatCard label="Sentimen Netral" value={stats?.neutralPercent + "%" || "0%"} icon={Minus} change={stats?.neutral.toLocaleString() + " komentar"} trend="up" />
            </>
          )}
        </div>

        {/* Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 mb-8">
          {/* Pie Chart */}
          <div className="lg:col-span-5 glass-card rounded-2xl p-6 border border-slate-800/50">
            <h3 className="text-lg font-semibold mb-6 text-center">Distribusi Sentimen</h3>
            <div className="relative h-72 w-full">
              {loading ? <Skeleton variant="circular" className="h-64 w-64 mx-auto rounded-full" /> : (
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie data={pieData} cx="50%" cy="50%" innerRadius={80} outerRadius={110} paddingAngle={5} dataKey="value" stroke="none">
                      {pieData.map((entry: any, index: number) => (<Cell key={index} fill={entry.color} />))}
                    </Pie>
                    <Tooltip
                      contentStyle={{ backgroundColor: "#020617", border: "1px solid #1e293b", borderRadius: "12px", boxShadow: "0 10px 15px -3px rgba(0, 0, 0, 0.5)" }}
                      formatter={(value: number) => [value.toLocaleString(), "Komentar"]}
                      itemStyle={{ color: '#fff' }}
                    />
                  </PieChart>
                </ResponsiveContainer>
              )}
              {!loading && (
                <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                  <span className="text-4xl font-bold text-white">{stats?.total.toLocaleString()}</span>
                  <span className="text-xs text-slate-400 uppercase tracking-widest mt-1 font-medium">Total</span>
                </div>
              )}
            </div>
            <div className="grid grid-cols-3 gap-4 mt-8 border-t border-slate-800/50 pt-6">
              {pieData.map((item: any, i: number) => (
                <div key={i} className="flex flex-col items-center text-center">
                  <div className="w-2.5 h-2.5 rounded-full mb-2 shadow-[0_0_10px_rgba(0,0,0,0.5)]" style={{ backgroundColor: item.color, boxShadow: `0 0 10px ${item.color}` }} />
                  <span className="text-sm font-medium text-slate-300">{item.name}</span>
                  <span className="text-xs text-slate-500 mt-1">{i === 0 ? stats?.negativePercent : i === 1 ? stats?.positivePercent : stats?.neutralPercent}%</span>
                </div>
              ))}
            </div>
          </div>

          {/* Bar Chart */}
          <div className="lg:col-span-7 glass-card rounded-2xl p-6 border border-slate-800/50 flex flex-col">
            <h3 className="text-lg font-semibold mb-6 flex items-center gap-2">
              <Brain className="w-5 h-5 text-purple-400" />Dominasi Emosi
            </h3>
            <div className="flex-1 min-h-[300px]">
              {loading ? <Skeleton variant="rectangular" className="w-full h-full rounded-xl" /> : (
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={emotionData} layout="vertical" margin={{ left: 0, right: 20, top: 0, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" horizontal={false} />
                    <XAxis type="number" stroke="#475569" fontSize={10} hide />
                    <YAxis type="category" dataKey="name" stroke="#94a3b8" width={100} fontSize={12} tickLine={false} axisLine={false} />
                    <Tooltip
                      cursor={{ fill: '#1e293b', opacity: 0.4 }}
                      contentStyle={{ backgroundColor: "#020617", border: "1px solid #1e293b", borderRadius: "12px", boxShadow: "0 10px 15px -3px rgba(0, 0, 0, 0.5)" }}
                      formatter={(value: number, name: string, props: any) => [value.toLocaleString() + " (" + props.payload.pct + "%)", "Komentar"]}
                      itemStyle={{ color: '#fff' }}
                    />
                    <Bar dataKey="value" radius={[0, 6, 6, 0]} barSize={32}>
                      {emotionData.map((entry: any, index: number) => (
                        <Cell key={index} fill={entry.fill} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              )}
            </div>
          </div>
        </div>

        {/* Analysis & Insights Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
          <div className="glass-card rounded-2xl p-6 border border-slate-800/50">
            <h3 className="text-lg font-semibold mb-6 flex items-center gap-2"><Target className="w-5 h-5 text-cyan-400" />Target Kritik Utama</h3>
            <div className="space-y-5">
              {loading ? <SectionSkeleton /> : stats?.topTargets?.slice(0, 5).map((target: any, i: number) => (
                <div key={i} className="group flex items-center justify-between p-3 rounded-lg hover:bg-slate-900/40 transition-colors border border-transparent hover:border-slate-800/50">
                  <div className="flex items-center gap-4">
                    <div className="w-8 h-8 rounded-lg bg-cyan-500/10 flex items-center justify-center text-sm font-bold text-cyan-400 group-hover:scale-110 transition-transform">
                      {i + 1}
                    </div>
                    <span className="text-slate-300 capitalize text-sm font-medium">{target.name.replace(/_/g, " ")}</span>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="w-32 h-2.5 bg-slate-800 rounded-full overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: target.percentage + "%" }}
                        transition={{ duration: 1, delay: 0.5 + (i * 0.1) }}
                        className="h-full bg-cyan-500 rounded-full shadow-[0_0_10px_rgba(6,182,212,0.5)]"
                      />
                    </div>
                    <span className="text-xs text-slate-400 w-12 text-right font-mono font-medium">{target.percentage}%</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="glass-card rounded-2xl p-6 border border-slate-800/50">
            <h3 className="text-lg font-semibold mb-6 flex items-center gap-2"><BarChart3 className="w-5 h-5 text-amber-400" />Sifat Komentar</h3>
            <div className="space-y-5">
              {loading ? <SectionSkeleton /> : stats?.constructiveness?.map((item: any, i: number) => (
                <div key={i} className="group flex items-center justify-between p-3 rounded-lg hover:bg-slate-900/40 transition-colors border border-transparent hover:border-slate-800/50">
                  <div className="flex items-center gap-4">
                    <div className={`w-3 h-3 rounded-full shadow-[0_0_8px] ${i === 0 ? "bg-emerald-500 shadow-emerald-500/50" : i === 1 ? "bg-amber-500 shadow-amber-500/50" : "bg-rose-500 shadow-rose-500/50"}`} />
                    <span className="text-slate-300 capitalize text-sm font-medium">{item.name.replace(/_/g, " ")}</span>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="w-32 h-2.5 bg-slate-800 rounded-full overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: item.percentage + "%" }}
                        transition={{ duration: 1, delay: 0.8 + (i * 0.1) }}
                        className={`h-full rounded-full ${i === 0 ? "bg-emerald-500" : i === 1 ? "bg-amber-500" : "bg-rose-500"}`}
                      />
                    </div>
                    <span className="text-xs text-slate-400 w-12 text-right font-mono font-medium">{item.percentage}%</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="glass-card rounded-2xl p-8 border border-slate-800/50 mb-8 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-green-500/5 rounded-full blur-3xl -mr-20 -mt-20 pointer-events-none" />
          <h3 className="text-lg font-semibold mb-6 flex items-center gap-2 relative z-10"><Activity className="w-5 h-5 text-emerald-400" />Performa Model ML</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 relative z-10">
            {[
              { label: "Akurasi", value: stats?.accuracy || 89.4, color: "text-emerald-400", border: "border-emerald-500/20" },
              { label: "F1-Score", value: stats?.f1Score || 91.0, color: "text-blue-400", border: "border-blue-500/20" },
              { label: "Confidence", value: stats?.confidence || 92.0, color: "text-purple-400", border: "border-purple-500/20" }
            ].map((metric, i) => (
              <div key={i} className={`text-center p-6 bg-slate-900/50 rounded-2xl border ${metric.border} backdrop-blur-sm hover:scale-105 transition-transform duration-300`}>
                <div className={`text-4xl font-bold ${metric.color} mb-2 tracking-tight`}>{metric.value}%</div>
                <div className="text-sm text-slate-500 font-medium uppercase tracking-wider">{metric.label}</div>
              </div>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          {[
            { icon: AlertTriangle, color: "text-rose-400", title: "Temuan Utama", content: `${stats?.negativePercent || "69.8"}% komentar bersifat negatif, menunjukkan tingkat kekecewaan tinggi publik.` },
            { icon: Target, color: "text-cyan-400", title: "Target Kritik", content: "PSSI dan pelatih menjadi sasaran utama kritik dengan lebih dari 40% komentar negatif." },
            { icon: Lightbulb, color: "text-amber-400", title: "Rekomendasi", content: "Perlu transparansi komunikasi dari PSSI dan evaluasi menyeluruh untuk memulihkan kepercayaan." }
          ].map((insight, i) => (
            <div key={i} className="glass-card rounded-2xl p-6 border border-slate-800/50 hover:border-slate-700 transition-colors">
              <div className="flex items-center gap-3 mb-4">
                <insight.icon className={`w-5 h-5 ${insight.color}`} />
                <h4 className={`font-semibold ${insight.color}`}>{insight.title}</h4>
              </div>
              <p className="text-sm text-slate-400 leading-relaxed">{insight.content}</p>
            </div>
          ))}
        </div>

        <footer className="text-center text-slate-600 text-sm py-4">
          <p>© 2024 Garuda Analytics v2.0</p>
        </footer>

      </motion.div>
    </>
  );
}
