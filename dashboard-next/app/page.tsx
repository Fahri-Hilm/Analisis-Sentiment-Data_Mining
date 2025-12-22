"use client";

import { MessageSquare, TrendingUp, TrendingDown, Activity, Target } from "lucide-react";
import { StatCard } from "../components/StatCard";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";
import { motion } from "framer-motion";
import { StatCardSkeleton } from "../components/Skeleton";
import { useDashboardStats } from "@/hooks/useDashboardStats";
import { useMemo, memo } from "react";
import dynamic from "next/dynamic";

const AIInsights = dynamic(() => import("../components/AIInsights").then(mod => ({ default: mod.AIInsights })), { 
  ssr: false,
  loading: () => <div className="h-32 bg-slate-800/50 rounded-xl animate-pulse" />
});

const SentimentPieChart = memo(function SentimentPieChart({ data }: { data: any[] }) {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          innerRadius={60}
          outerRadius={100}
          paddingAngle={5}
          dataKey="value"
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={entry.color} />
          ))}
        </Pie>
        <Tooltip
          contentStyle={{
            backgroundColor: "rgba(2, 6, 23, 0.95)",
            border: "1px solid #334155",
            borderRadius: "8px",
            color: "#ffffff"
          }}
        />
      </PieChart>
    </ResponsiveContainer>
  );
});

const EmotionCard = memo(function EmotionCard({ emotion }: { emotion: any }) {
  return (
    <motion.div 
      whileHover={{ scale: 1.02 }}
      className="flex items-center justify-between p-3 bg-slate-800/30 rounded-lg hover:bg-slate-700/30 transition-colors"
    >
      <div>
        <p className="font-medium">{emotion.name}</p>
        <p className="text-sm text-slate-400">{emotion.count.toLocaleString()} komentar</p>
      </div>
      <div className="text-right">
        <p className="text-lg font-bold text-blue-400">{emotion.percentage}%</p>
      </div>
    </motion.div>
  );
});

export default function Dashboard() {
  const { stats, isLoading: loading } = useDashboardStats();

  const pieData = useMemo(() => stats ? [
    { name: "Negatif", value: stats.negative, color: "#f43f5e" },
    { name: "Positif", value: stats.positive, color: "#10b981" },
    { name: "Netral", value: stats.neutral, color: "#64748b" },
  ] : [], [stats]);

  const topEmotions = useMemo(() => stats?.topEmotions?.slice(0, 3) || [], [stats?.topEmotions]);

  return (
    <>
      <div className="absolute top-0 left-0 w-full h-[500px] bg-primary/5 rounded-full blur-[100px] pointer-events-none -translate-y-1/2" />

      <div className="relative z-10 p-8 space-y-8">
        <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            Dashboard Overview
          </h1>
          <p className="text-slate-400 mt-2">Gambaran umum analisis sentimen Timnas Indonesia</p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {loading ? (
            <>
              <StatCardSkeleton />
              <StatCardSkeleton />
              <StatCardSkeleton />
              <StatCardSkeleton />
            </>
          ) : (
            <>
              <motion.div whileHover={{ scale: 1.02 }} className="glass-card rounded-2xl p-6 border border-slate-800/50">
                <StatCard
                  icon={MessageSquare}
                  label="Total Komentar"
                  value={stats?.total?.toLocaleString() || "0"}
                  change="+0%"
                  trend="up"
                />
              </motion.div>
              <motion.div whileHover={{ scale: 1.02 }} className="glass-card rounded-2xl p-6 border border-slate-800/50">
                <StatCard
                  icon={TrendingUp}
                  label="Sentimen Positif"
                  value={stats?.positivePercent || "0%"}
                  change="+0%"
                  trend="up"
                />
              </motion.div>
              <motion.div whileHover={{ scale: 1.02 }} className="glass-card rounded-2xl p-6 border border-slate-800/50">
                <StatCard
                  icon={TrendingDown}
                  label="Sentimen Negatif"
                  value={stats?.negativePercent || "0%"}
                  change="+0%"
                  trend="down"
                />
              </motion.div>
              <motion.div whileHover={{ scale: 1.02 }} className="glass-card rounded-2xl p-6 border border-slate-800/50">
                <StatCard
                  icon={Activity}
                  label={stats?.backendConnected ? "Enhanced Accuracy v3.1" : "Model Accuracy v3.1"}
                  value={`${stats?.accuracy || 95.5}%`}
                  change={`+${stats?.enhancements?.total_boost || 6.1}%`}
                  trend="up"
                />
                {stats?.backendConnected && (
                  <div className="mt-2 text-xs text-green-400 flex items-center gap-1">
                    <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                    Backend Connected ({stats.backendInfo?.lexicon_words} words)
                  </div>
                )}
              </motion.div>
            </>
          )}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="glass-card rounded-2xl p-6 border border-slate-800/50"
          >
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <Target className="w-5 h-5 text-blue-400" />
              Distribusi Sentimen
            </h2>
            {loading ? (
              <div className="h-64 flex items-center justify-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500" />
              </div>
            ) : (
              <SentimentPieChart data={pieData} />
            )}
            <div className="grid grid-cols-3 gap-4 mt-4">
              <div className="text-center">
                <div className="w-3 h-3 bg-emerald-500 rounded-full mx-auto mb-1" />
                <p className="text-xs text-slate-400">Positif</p>
                <p className="font-semibold">{stats?.positivePercent || "0%"}</p>
              </div>
              <div className="text-center">
                <div className="w-3 h-3 bg-rose-500 rounded-full mx-auto mb-1" />
                <p className="text-xs text-slate-400">Negatif</p>
                <p className="font-semibold">{stats?.negativePercent || "0%"}</p>
              </div>
              <div className="text-center">
                <div className="w-3 h-3 bg-slate-500 rounded-full mx-auto mb-1" />
                <p className="text-xs text-slate-400">Netral</p>
                <p className="font-semibold">{stats?.neutralPercent || "0%"}</p>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.1 }}
            className="glass-card rounded-2xl p-6 border border-slate-800/50"
          >
            <h2 className="text-xl font-semibold mb-4">Top 3 Emosi</h2>
            {loading ? (
              <div className="space-y-4">
                {[1, 2, 3].map((i) => (
                  <div key={i} className="h-16 bg-slate-800/50 rounded-lg animate-pulse" />
                ))}
              </div>
            ) : (
              <div className="space-y-4">
                {topEmotions.map((emotion: any, idx: number) => (
                  <EmotionCard key={idx} emotion={emotion} />
                ))}
              </div>
            )}
          </motion.div>
        </div>

        <AIInsights stats={stats} loading={loading} />
      </div>
    </>
  );
}
