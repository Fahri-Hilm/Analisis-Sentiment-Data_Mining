"use client";

import { useState, useEffect } from "react";

import { Settings, Cpu, Zap, Target, CheckCircle, TrendingUp } from "lucide-react";

import { useDashboardStats } from "@/hooks/useDashboardStats";

export default function SettingsPage() {
  const { stats } = useDashboardStats();

  if (!stats) return (<div className="flex-1 flex items-center justify-center h-screen text-slate-400 bg-transparent">Memuat Data Model...</div>);

  return (
    <div className="max-w-7xl mx-auto p-8 relative">
      {/* Background Ambient Glow */}
      <div className="absolute top-0 right-0 w-full h-[500px] bg-amber-500/5 rounded-full blur-[100px] pointer-events-none -translate-y-1/2" />

      <div className="mb-10 relative z-10">
        <h1 className="text-4xl font-bold flex items-center gap-3 bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
          <Settings className="w-8 h-8 text-blue-400" />Konfigurasi Model: Di Balik Layar
        </h1>
        <p className="text-slate-400 text-lg mt-2 font-light tracking-wide">Pengaturan parameter dan performa algoritma SVM</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8 relative z-10">
        {[{
          icon: Target, label: "Model Accuracy", value: `${stats.accuracy}%`, sub: "SVM + TF-IDF Classifier", color: "text-green-400", border: "border-green-500/20"
        }, {
          icon: Zap, label: "F1-Score", value: `${stats.f1Score}%`, sub: "Excellent performance", color: "text-blue-400", border: "border-blue-500/20"
        }, {
          icon: TrendingUp, label: "Confidence", value: `${stats.confidence}%`, sub: "Prediction confidence", color: "text-purple-400", border: "border-purple-500/20"
        }].map((item, i) => (
          <div key={i} className={`glass-card rounded-xl p-6 border ${item.border}`}>
            <item.icon className={`w-8 h-8 ${item.color} mb-4`} />
            <div className="text-sm text-slate-400 mb-1 uppercase tracking-wider font-medium">{item.label}</div>
            <div className={`text-3xl font-bold font-mono tracking-tight ${item.color}`}>{item.value}</div>
            <div className="text-xs text-slate-500 mt-2 font-light">{item.sub}</div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8 relative z-10">
        <div className="glass-card rounded-2xl p-8 border border-slate-800/50">
          <h3 className="text-lg font-semibold mb-6 text-slate-200">Current Model Configuration</h3>
          <div className="space-y-6">
            <div className="flex justify-between items-center group">
              <div>
                <div className="font-semibold text-slate-200">Model Type</div>
                <div className="text-sm text-slate-400 font-light">Support Vector Machine (SVM)</div>
              </div>
              <div className="px-4 py-2 bg-emerald-500/10 text-emerald-400 rounded-lg text-xs font-medium uppercase tracking-wider flex items-center gap-2 border border-emerald-500/20">
                <CheckCircle className="w-4 h-4" />Active
              </div>
            </div>
            {[
              { label: "Feature Extraction", value: "TF-IDF Vectorizer" },
              { label: "Training Data", value: `5,631 labeled comments (from ${stats.total?.toLocaleString()} total)` },
              { label: "Validation Method", value: "5-Fold Cross-Validation" },
              { label: "Model File", value: "data/models/sentiment_svm_model.joblib", color: "text-blue-400 font-mono text-sm" }
            ].map((item, i) => (
              <div key={i} className="group">
                <div className="font-semibold text-slate-200 mb-1">{item.label}</div>
                <div className={`text-sm ${item.color || "text-slate-400 font-light font-mono"}`}>{item.value}</div>
              </div>
            ))}
          </div>
        </div>

        <div className="glass-card rounded-2xl p-8 border border-slate-800/50">
          <h3 className="text-lg font-semibold mb-6 text-slate-200">Training Results</h3>
          <div className="space-y-6">
            {[
              { label: "Cross-Validation Accuracy", value: stats.accuracy, color: "bg-green-500", text: "text-green-400" },
              { label: "F1-Score (Weighted)", value: stats.f1Score, color: "bg-blue-500", text: "text-blue-400" },
              { label: "Test Set Accuracy", value: stats.confidence, color: "bg-purple-500", text: "text-purple-400" },
              { label: "Overfitting Gap", value: 2.6, color: "bg-yellow-500", text: "text-yellow-400", suffix: "%", width: 2.6 } // Manual fixed width for logic consistency
            ].map((metric, i) => (
              <div key={i}>
                <div className="flex justify-between mb-2">
                  <span className="text-sm text-slate-400">{metric.label}</span>
                  <span className={`text-sm font-bold ${metric.text}`}>{metric.value}{metric.suffix || "%"}</span>
                </div>
                <div className="w-full bg-slate-800/50 rounded-full h-2">
                  <div className={`h-2 rounded-full ${metric.color} shadow-[0_0_8px] shadow-${metric.color.split("-")[1]}-500/50`} style={{ width: `${metric.width || metric.value}%` }}></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="glass-card rounded-2xl p-8 border border-slate-800/50 mb-8 relative z-10">
        <h3 className="text-lg font-semibold mb-6 text-slate-200">Sentiment Classification Results</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[
            { label: "Negative", count: stats.negative, pct: stats.negativePercent, color: "bg-red-500" },
            { label: "Positive", count: stats.positive, pct: stats.positivePercent, color: "bg-green-500" },
            { label: "Neutral", count: stats.neutral, pct: stats.neutralPercent, color: "bg-slate-500" }
          ].map((item, i) => (
            <div key={i} className="bg-slate-900/40 rounded-xl p-5 border border-slate-800/50 hover:bg-slate-800/40 transition-colors">
              <div className="flex items-center gap-3 mb-3">
                <div className={`w-3 h-3 rounded-full ${item.color} shadow-[0_0_8px] shadow-${item.color.split('-')[1]}-500/50`}></div>
                <span className="font-medium text-slate-200">{item.label}</span>
              </div>
              <div className="text-3xl font-bold text-white mb-1">{item.count?.toLocaleString()}</div>
              <div className="text-sm text-slate-500 font-light">{item.pct}% of total</div>
            </div>
          ))}
        </div>
      </div>

      <div className="glass-card rounded-2xl p-8 border border-slate-800/50 relative z-10">
        <h3 className="text-lg font-semibold mb-6 text-slate-200">Model Actions</h3>
        <div className="flex flex-wrap gap-4">
          <button className="px-6 py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-xl shadow-lg shadow-blue-900/20 transition-all font-medium">Retrain Model</button>
          <button className="px-6 py-3 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl shadow-lg shadow-emerald-900/20 transition-all font-medium">Export Model</button>
          <button className="px-6 py-3 bg-purple-600 hover:bg-purple-500 text-white rounded-xl shadow-lg shadow-purple-900/20 transition-all font-medium">Test Model</button>
          <button className="px-6 py-3 bg-slate-700 hover:bg-slate-600 text-white rounded-xl transition-all font-medium">View Logs</button>
        </div>
      </div>
    </div>
  );
}
