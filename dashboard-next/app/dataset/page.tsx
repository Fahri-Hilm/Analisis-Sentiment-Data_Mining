"use client";

import { useState, useEffect } from "react";
import { Sidebar } from "@/components/Sidebar";
import { Download, Upload, Database, CheckCircle, Sparkles } from "lucide-react";

export default function DatasetPage() {
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    fetch("/api/stats").then((r) => r.json()).then(setStats);
  }, []);

  if (!stats) return (
    <div className="flex h-screen bg-[#0a1628] text-white overflow-hidden">
      <Sidebar />
      <div className="flex-1 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    </div>
  );

  return (
    <div className="flex h-screen bg-[#0a1628] text-white overflow-hidden">
      <Sidebar />
      <div className="flex-1 overflow-y-auto p-6">
        <div className="mb-6">
          <h1 className="text-3xl font-bold mb-2">Dapur Data: Transparansi Dataset</h1>
          <p className="text-gray-400">Kelola dan validasi data latih untuk akurasi model</p>
        </div>

        <div className="grid grid-cols-3 gap-6 mb-6">
          <div className="bg-gradient-to-br from-[#1a2942] to-[#0f1c2e] rounded-xl p-6 border border-blue-500/20">
            <Database className="w-8 h-8 text-blue-400 mb-3" />
            <div className="text-sm text-gray-400 mb-2">Total Records</div>
            <div className="text-3xl font-bold">{stats.total?.toLocaleString()}</div>
            <div className="text-sm text-gray-400 mt-2">YouTube comments</div>
          </div>
          <div className="bg-gradient-to-br from-[#1a2942] to-[#0f1c2e] rounded-xl p-6 border border-blue-500/20">
            <CheckCircle className="w-8 h-8 text-green-400 mb-3" />
            <div className="text-sm text-gray-400 mb-2">Labeled Data</div>
            <div className="text-3xl font-bold">100%</div>
            <div className="text-sm text-green-400 mt-2">ML Retrained (SVM)</div>
          </div>
          <div className="bg-gradient-to-br from-[#1a2942] to-[#0f1c2e] rounded-xl p-6 border border-blue-500/20">
            <Sparkles className="w-8 h-8 text-purple-400 mb-3" />
            <div className="text-sm text-gray-400 mb-2">Model Accuracy</div>
            <div className="text-3xl font-bold">{stats.accuracy}%</div>
            <div className="text-sm text-gray-400 mt-2">F1 Score: {stats.f1Score}%</div>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-6 mb-6">
          <div className="bg-gradient-to-br from-[#1a2942] to-[#0f1c2e] rounded-xl p-6 border border-blue-500/20">
            <h3 className="text-lg font-semibold mb-4">Dataset Information</h3>
            <div className="space-y-4">
              <div className="flex justify-between">
                <span className="text-gray-400">Source</span>
                <span>YouTube Data API v3</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Collection Period</span>
                <span>November 2024</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Topic</span>
                <span>Timnas Gagal Piala Dunia 2026</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Language</span>
                <span>Indonesian (Bahasa)</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Data File</span>
                <span className="text-blue-400">comments_cleaned_retrained.csv</span>
              </div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-[#1a2942] to-[#0f1c2e] rounded-xl p-6 border border-blue-500/20">
            <h3 className="text-lg font-semibold mb-4">Sentiment Distribution</h3>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between mb-1">
                  <span className="text-gray-400">Negative</span>
                  <span className="text-red-400">{stats.negative?.toLocaleString()} ({stats.negativePercent}%)</span>
                </div>
                <div className="w-full bg-[#0f1c2e] rounded-full h-3">
                  <div className="bg-red-500 h-3 rounded-full" style={{ width: `${stats.negativePercent}%` }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between mb-1">
                  <span className="text-gray-400">Positive</span>
                  <span className="text-green-400">{stats.positive?.toLocaleString()} ({stats.positivePercent}%)</span>
                </div>
                <div className="w-full bg-[#0f1c2e] rounded-full h-3">
                  <div className="bg-green-500 h-3 rounded-full" style={{ width: `${stats.positivePercent}%` }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between mb-1">
                  <span className="text-gray-400">Neutral</span>
                  <span className="text-gray-400">{stats.neutral?.toLocaleString()} ({stats.neutralPercent}%)</span>
                </div>
                <div className="w-full bg-[#0f1c2e] rounded-full h-3">
                  <div className="bg-gray-500 h-3 rounded-full" style={{ width: `${stats.neutralPercent}%` }}></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-br from-[#1a2942] to-[#0f1c2e] rounded-xl p-6 border border-blue-500/20 mb-6">
          <h3 className="text-lg font-semibold mb-4">Dataset Actions</h3>
          <div className="flex gap-4">
            <button className="flex items-center gap-2 px-6 py-3 bg-blue-500 rounded-lg hover:bg-blue-600 transition">
              <Download className="w-5 h-5" />
              Export Dataset (CSV)
            </button>
            <button className="flex items-center gap-2 px-6 py-3 bg-green-500 rounded-lg hover:bg-green-600 transition">
              <Download className="w-5 h-5" />
              Export Processed (JSON)
            </button>
            <button className="flex items-center gap-2 px-6 py-3 bg-purple-500 rounded-lg hover:bg-purple-600 transition">
              <Upload className="w-5 h-5" />
              Upload New Data
            </button>
          </div>
        </div>

        <div className="bg-gradient-to-br from-[#1a2942] to-[#0f1c2e] rounded-xl p-6 border border-blue-500/20">
          <h3 className="text-lg font-semibold mb-4">ML Model Info</h3>
          <div className="grid grid-cols-4 gap-4">
            <div className="bg-[#0f1c2e] rounded-lg p-4 border border-blue-500/10">
              <div className="text-sm text-gray-400 mb-1">Algorithm</div>
              <div className="font-semibold">SVM + TF-IDF</div>
            </div>
            <div className="bg-[#0f1c2e] rounded-lg p-4 border border-blue-500/10">
              <div className="text-sm text-gray-400 mb-1">Training Data</div>
              <div className="font-semibold">5,631 samples</div>
            </div>
            <div className="bg-[#0f1c2e] rounded-lg p-4 border border-blue-500/10">
              <div className="text-sm text-gray-400 mb-1">Cross-Validation</div>
              <div className="font-semibold">5-Fold CV</div>
            </div>
            <div className="bg-[#0f1c2e] rounded-lg p-4 border border-blue-500/10">
              <div className="text-sm text-gray-400 mb-1">Confidence</div>
              <div className="font-semibold">{stats.confidence}%</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
