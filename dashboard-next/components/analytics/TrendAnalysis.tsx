"use client";

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from "recharts";
import { Calendar, TrendingUp, TrendingDown } from "lucide-react";
import { motion } from "framer-motion";
import { useTrendAnalysis } from "@/hooks/useAdvancedAnalytics";
import { useState } from "react";

export default function TrendAnalysis() {
  const [period, setPeriod] = useState("monthly");
  const { data: trendData, loading } = useTrendAnalysis(period);

  // Calculate trends
  const latestTrend = trendData.length > 1 ? {
    positive: trendData[trendData.length - 1]?.positive - trendData[trendData.length - 2]?.positive || 0,
    negative: trendData[trendData.length - 1]?.negative - trendData[trendData.length - 2]?.negative || 0,
  } : { positive: 0, negative: 0 };

  const peakActivity = trendData.reduce((max, current) => 
    current.total > max.total ? current : max, 
    { date: "N/A", total: 0 }
  );

  if (loading) {
    return (
      <div className="space-y-6">
        {[1, 2, 3].map((i) => (
          <div key={i} className="h-64 bg-slate-800/50 rounded-xl animate-pulse" />
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4 mb-6">
        <select
          value={period}
          onChange={(e) => setPeriod(e.target.value)}
          className="bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-white"
        >
          <option value="daily">Harian</option>
          <option value="weekly">Mingguan</option>
          <option value="monthly">Bulanan</option>
        </select>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <motion.div className="glass-card rounded-2xl p-6 border border-slate-800/50">
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp className="w-5 h-5 text-green-400" />
            <h3 className="text-lg font-semibold">Trend Positif</h3>
          </div>
          <div className="text-3xl font-bold text-green-400">
            {latestTrend.positive > 0 ? '+' : ''}{latestTrend.positive.toFixed(1)}%
          </div>
          <p className="text-sm text-slate-400">vs periode lalu</p>
        </motion.div>

        <motion.div className="glass-card rounded-2xl p-6 border border-slate-800/50">
          <div className="flex items-center gap-2 mb-4">
            <TrendingDown className="w-5 h-5 text-red-400" />
            <h3 className="text-lg font-semibold">Trend Negatif</h3>
          </div>
          <div className="text-3xl font-bold text-red-400">
            {latestTrend.negative > 0 ? '+' : ''}{latestTrend.negative.toFixed(1)}%
          </div>
          <p className="text-sm text-slate-400">vs periode lalu</p>
        </motion.div>

        <motion.div className="glass-card rounded-2xl p-6 border border-slate-800/50">
          <div className="flex items-center gap-2 mb-4">
            <Calendar className="w-5 h-5 text-blue-400" />
            <h3 className="text-lg font-semibold">Peak Activity</h3>
          </div>
          <div className="text-3xl font-bold text-blue-400">{peakActivity.date}</div>
          <p className="text-sm text-slate-400">{peakActivity.total.toLocaleString()} komentar</p>
        </motion.div>
      </div>

      <motion.div className="glass-card rounded-2xl p-6 border border-slate-800/50">
        <h3 className="text-xl font-semibold mb-4">Distribusi Sentimen {period === 'monthly' ? 'Bulanan' : period === 'weekly' ? 'Mingguan' : 'Harian'}</h3>
        <ResponsiveContainer width="100%" height={350}>
          <BarChart data={trendData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
            <XAxis 
              dataKey="date" 
              stroke="#64748b" 
              fontSize={12}
              angle={-45}
              textAnchor="end"
              height={80}
            />
            <YAxis stroke="#64748b" />
            <Tooltip
              contentStyle={{
                backgroundColor: "rgba(2, 6, 23, 0.95)",
                border: "1px solid #334155",
                borderRadius: "8px",
              }}
              formatter={(value, name) => [`${value}%`, name === 'positive' ? 'Positif' : name === 'negative' ? 'Negatif' : 'Netral']}
            />
            <Bar dataKey="positive" fill="#10b981" name="positive" />
            <Bar dataKey="negative" fill="#f43f5e" name="negative" />
            <Bar dataKey="neutral" fill="#64748b" name="neutral" />
          </BarChart>
        </ResponsiveContainer>
      </motion.div>

      <motion.div className="glass-card rounded-2xl p-6 border border-slate-800/50">
        <h3 className="text-xl font-semibold mb-4">Volume Komentar</h3>
        <ResponsiveContainer width="100%" height={250}>
          <AreaChart data={trendData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
            <XAxis 
              dataKey="date" 
              stroke="#64748b" 
              fontSize={12}
              angle={-45}
              textAnchor="end"
              height={80}
            />
            <YAxis stroke="#64748b" />
            <Tooltip
              contentStyle={{
                backgroundColor: "rgba(2, 6, 23, 0.95)",
                border: "1px solid #334155",
                borderRadius: "8px",
              }}
              formatter={(value) => [`${value} komentar`, 'Total']}
            />
            <Area type="monotone" dataKey="total" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.3} />
          </AreaChart>
        </ResponsiveContainer>
      </motion.div>
    </div>
  );
}
