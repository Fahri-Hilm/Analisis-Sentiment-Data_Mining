"use client";

import { useState, useEffect } from "react";

import { Download, Upload, Database, CheckCircle, Sparkles } from "lucide-react";

import { useDashboardStats } from "@/hooks/useDashboardStats";

export default function DatasetPage() {
  const { stats } = useDashboardStats();

  if (!stats) return (<div className="flex-1 flex items-center justify-center h-screen text-slate-400 bg-transparent">Memuat Data Dataset...</div>);

  return (
    <div className="max-w-7xl mx-auto p-8 relative">
      {/* Background Ambient Glow */}
      <div className="absolute top-0 right-0 w-full h-[500px] bg-cyan-500/5 rounded-full blur-[100px] pointer-events-none -translate-y-1/2" />

      <div className="mb-10 relative z-10">
        <h1 className="text-4xl font-bold flex items-center gap-3 bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
          <Database className="w-8 h-8 text-blue-400" />Dapur Data: Transparansi Dataset
        </h1>
        <p className="text-slate-400 text-lg mt-2 font-light tracking-wide">Kelola dan validasi data latih untuk akurasi model</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8 relative z-10">
        <div className="glass-card rounded-xl p-6 border border-blue-500/20">
          <Database className="w-8 h-8 text-blue-400 mb-4" />
          <div className="text-sm text-slate-400 mb-1 uppercase tracking-wider font-medium">Total Records</div>
          <div className="text-3xl font-bold text-white font-mono tracking-tight">{stats.total?.toLocaleString()}</div>
          <div className="text-xs text-blue-400/80 mt-2 font-medium bg-blue-500/10 inline-block px-2 py-1 rounded-full">YouTube comments</div>
        </div>
        <div className="glass-card rounded-xl p-6 border border-green-500/20">
          <CheckCircle className="w-8 h-8 text-green-400 mb-4" />
          <div className="text-sm text-slate-400 mb-1 uppercase tracking-wider font-medium">Labeled Data</div>
          <div className="text-3xl font-bold text-white font-mono tracking-tight">100%</div>
          <div className="text-xs text-green-400/80 mt-2 font-medium bg-green-500/10 inline-block px-2 py-1 rounded-full">ML Retrained (SVM)</div>
        </div>
        <div className="glass-card rounded-xl p-6 border border-purple-500/20">
          <Sparkles className="w-8 h-8 text-purple-400 mb-4" />
          <div className="text-sm text-slate-400 mb-1 uppercase tracking-wider font-medium">Model Accuracy</div>
          <div className="text-3xl font-bold text-white font-mono tracking-tight">{stats.accuracy}%</div>
          <div className="text-xs text-purple-400/80 mt-2 font-medium bg-purple-500/10 inline-block px-2 py-1 rounded-full">F1 Score: {stats.f1Score}%</div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8 relative z-10">
        <div className="glass-card rounded-2xl p-8 border border-slate-800/50">
          <h3 className="text-lg font-semibold mb-6 flex items-center gap-2 text-slate-200">Dataset Information</h3>
          <div className="space-y-5">
            {[
              { label: "Source", value: "YouTube Data API v3" },
              { label: "Collection Period", value: "November 2024" },
              { label: "Topic", value: "Timnas Gagal Piala Dunia 2026" },
              { label: "Language", value: "Indonesian (Bahasa)" },
              { label: "Data File", value: "comments_cleaned_retrained.csv", highlight: true }
            ].map((item, i) => (
              <div key={i} className="flex justify-between items-center group">
                <span className="text-slate-400 font-light">{item.label}</span>
                <span className={`font-medium ${item.highlight ? "text-blue-400 font-mono text-sm bg-blue-500/10 px-2 py-0.5 rounded" : "text-slate-200 font-mono text-sm"}`}>{item.value}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="glass-card rounded-2xl p-8 border border-slate-800/50">
          <h3 className="text-lg font-semibold mb-6 flex items-center gap-2 text-slate-200">Sentiment Distribution</h3>
          <div className="space-y-6">
            {[
              { label: "Negative", value: stats.negative, pct: stats.negativePercent, color: "bg-red-500", text: "text-red-400", hex: "#ef4444" },
              { label: "Positive", value: stats.positive, pct: stats.positivePercent, color: "bg-green-500", text: "text-green-400", hex: "#22c55e" },
              { label: "Neutral", value: stats.neutral, pct: stats.neutralPercent, color: "bg-slate-500", text: "text-slate-400", hex: "#64748b" }
            ].map((sentiment, i) => (
              <div key={i}>
                <div className="flex justify-between mb-2">
                  <span className="text-sm font-medium text-slate-400">{sentiment.label}</span>
                  <span className={`text-sm font-bold ${sentiment.text}`}>{sentiment.value?.toLocaleString()} <span className="text-slate-500 font-normal">({sentiment.pct}%)</span></span>
                </div>
                <div className="w-full bg-slate-800/50 rounded-full h-2.5 overflow-hidden">
                  <div className={`h-2.5 rounded-full ${sentiment.color} shadow-[0_0_10px_-2px] transition-all duration-1000 ease-out`} style={{ width: `${sentiment.pct}%`, boxShadow: `0 0 10px ${sentiment.hex}` }}></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="glass-card rounded-2xl p-8 border border-slate-800/50 mb-8 relative z-10 bg-slate-900/40">
        <h3 className="text-lg font-semibold mb-6 text-slate-200">Dataset Actions</h3>
        <div className="flex flex-wrap gap-4">
          <button className="flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-xl shadow-lg shadow-blue-900/20 transition-all font-medium">
            <Download className="w-5 h-5" />
            Export Dataset (CSV)
          </button>
          <button className="flex items-center gap-2 px-6 py-3 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl shadow-lg shadow-emerald-900/20 transition-all font-medium">
            <Download className="w-5 h-5" />
            Export Processed (JSON)
          </button>
          <button className="flex items-center gap-2 px-6 py-3 bg-purple-600 hover:bg-purple-500 text-white rounded-xl shadow-lg shadow-purple-900/20 transition-all font-medium">
            <Upload className="w-5 h-5" />
            Upload New Data
          </button>
        </div>
      </div>

      <div className="glass-card rounded-2xl p-8 border border-slate-800/50 relative z-10">
        <h3 className="text-lg font-semibold mb-6 flex items-center gap-2 text-slate-200">ML Model Configuration</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {[
            { label: "Algorithm", value: "SVM + TF-IDF" },
            { label: "Training Data", value: "5,631 samples" },
            { label: "Cross-Validation", value: "5-Fold CV" },
            { label: "Confidence", value: `${stats.confidence}%` }
          ].map((info, i) => (
            <div key={i} className="bg-slate-900/40 rounded-xl p-4 border border-slate-800/50 hover:border-slate-700 transition-colors">
              <div className="text-xs text-slate-500 uppercase tracking-wider mb-2 font-medium">{info.label}</div>
              <div className="font-semibold text-slate-200 text-lg">{info.value}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
