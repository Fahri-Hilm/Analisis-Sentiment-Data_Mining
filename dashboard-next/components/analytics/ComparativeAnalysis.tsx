"use client";

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from "recharts";
import { Calendar, ArrowUpDown, Zap } from "lucide-react";
import { motion } from "framer-motion";
import { useState } from "react";

const periodData = [
  { period: "Pre-Kualifikasi", positive: 45, negative: 50, neutral: 5, total: 3200 },
  { period: "Kualifikasi Awal", positive: 35, negative: 60, neutral: 5, total: 5800 },
  { period: "Kualifikasi Akhir", positive: 25, negative: 70, neutral: 5, total: 7400 },
  { period: "Post-Eliminasi", positive: 20, negative: 75, neutral: 5, total: 2828 },
];

const matchData = [
  { match: "vs Thailand", positive: 30, negative: 65, neutral: 5, comments: 2500 },
  { match: "vs Vietnam", positive: 40, negative: 55, neutral: 5, comments: 3200 },
  { match: "vs Malaysia", positive: 25, negative: 70, neutral: 5, comments: 4100 },
  { match: "vs Singapura", positive: 35, negative: 60, neutral: 5, comments: 2800 },
  { match: "vs Australia", positive: 22, negative: 73, neutral: 5, comments: 3600 },
  { match: "vs Arab Saudi", positive: 18, negative: 77, neutral: 5, comments: 2900 },
];

const radarData = [
  { subject: "Kemarahan", Pre: 70, Post: 85, fullMark: 100 },
  { subject: "Kekecewaan", Pre: 75, Post: 90, fullMark: 100 },
  { subject: "Harapan", Pre: 45, Post: 30, fullMark: 100 },
  { subject: "Dukungan", Pre: 40, Post: 25, fullMark: 100 },
  { subject: "Kebanggaan", Pre: 35, Post: 20, fullMark: 100 },
  { subject: "Frustrasi", Pre: 65, Post: 80, fullMark: 100 },
];

export default function ComparativeAnalysis() {
  const [selectedPeriod, setSelectedPeriod] = useState("all");

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4 mb-6">
        <select
          value={selectedPeriod}
          onChange={(e) => setSelectedPeriod(e.target.value)}
          className="bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-white"
        >
          <option value="all">Semua Periode</option>
          <option value="pre">Pre-Kualifikasi</option>
          <option value="during">Selama Kualifikasi</option>
          <option value="post">Post-Eliminasi</option>
        </select>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <motion.div className="glass-card rounded-2xl p-6 border border-slate-800/50">
          <div className="flex items-center gap-2 mb-4">
            <Calendar className="w-5 h-5 text-blue-400" />
            <h3 className="text-lg font-semibold">Periode Terburuk</h3>
          </div>
          <div className="text-2xl font-bold text-red-400">Post-Eliminasi</div>
          <p className="text-sm text-slate-400">75% sentimen negatif</p>
        </motion.div>

        <motion.div className="glass-card rounded-2xl p-6 border border-slate-800/50">
          <div className="flex items-center gap-2 mb-4">
            <ArrowUpDown className="w-5 h-5 text-yellow-400" />
            <h3 className="text-lg font-semibold">Volatilitas</h3>
          </div>
          <div className="text-2xl font-bold text-yellow-400">±15%</div>
          <p className="text-sm text-slate-400">Fluktuasi sentimen</p>
        </motion.div>

        <motion.div className="glass-card rounded-2xl p-6 border border-slate-800/50">
          <div className="flex items-center gap-2 mb-4">
            <Zap className="w-5 h-5 text-purple-400" />
            <h3 className="text-lg font-semibold">Peak Negatif</h3>
          </div>
          <div className="text-2xl font-bold text-purple-400">vs Malaysia</div>
          <p className="text-sm text-slate-400">70% negatif, 4.1K komentar</p>
        </motion.div>
      </div>

      <motion.div className="glass-card rounded-2xl p-6 border border-slate-800/50">
        <h3 className="text-xl font-semibold mb-4">Perbandingan Antar Periode</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={periodData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
            <XAxis dataKey="period" stroke="#64748b" />
            <YAxis stroke="#64748b" />
            <Tooltip
              contentStyle={{
                backgroundColor: "rgba(2, 6, 23, 0.95)",
                border: "1px solid #334155",
                borderRadius: "8px",
              }}
            />
            <Bar dataKey="positive" fill="#10b981" />
            <Bar dataKey="negative" fill="#f43f5e" />
            <Bar dataKey="neutral" fill="#64748b" />
          </BarChart>
        </ResponsiveContainer>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <motion.div className="glass-card rounded-2xl p-6 border border-slate-800/50">
          <h3 className="text-xl font-semibold mb-4">Sentimen per Pertandingan</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={matchData} layout="horizontal">
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis type="number" stroke="#64748b" />
              <YAxis dataKey="match" type="category" stroke="#64748b" />
              <Tooltip
                contentStyle={{
                  backgroundColor: "rgba(2, 6, 23, 0.95)",
                  border: "1px solid #334155",
                  borderRadius: "8px",
                }}
              />
              <Bar dataKey="positive" fill="#10b981" />
              <Bar dataKey="negative" fill="#f43f5e" />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>

        <motion.div className="glass-card rounded-2xl p-6 border border-slate-800/50">
          <h3 className="text-xl font-semibold mb-4">Radar Emosi: Pre vs Post</h3>
          <ResponsiveContainer width="100%" height={250}>
            <RadarChart data={radarData}>
              <PolarGrid stroke="#334155" />
              <PolarAngleAxis dataKey="subject" tick={{ fill: "#64748b", fontSize: 12 }} />
              <PolarRadiusAxis tick={{ fill: "#64748b", fontSize: 10 }} />
              <Radar name="Pre-Eliminasi" dataKey="Pre" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.3} />
              <Radar name="Post-Eliminasi" dataKey="Post" stroke="#f43f5e" fill="#f43f5e" fillOpacity={0.3} />
              <Tooltip
                contentStyle={{
                  backgroundColor: "rgba(2, 6, 23, 0.95)",
                  border: "1px solid #334155",
                  borderRadius: "8px",
                }}
              />
            </RadarChart>
          </ResponsiveContainer>
        </motion.div>
      </div>
    </div>
  );
}
