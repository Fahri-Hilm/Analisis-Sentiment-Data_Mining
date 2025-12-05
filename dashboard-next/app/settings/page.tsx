"use client";

import { useState, useEffect } from "react";
import { Sidebar } from "@/components/Sidebar";
import { Settings, Cpu, Zap, Target, CheckCircle, TrendingUp } from "lucide-react";

export default function SettingsPage() {
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
          <h1 className="text-3xl font-bold mb-2">Konfigurasi Model: Di Balik Layar</h1>
          <p className="text-gray-400">Pengaturan parameter dan performa algoritma SVM</p>
        </div>

        <div className="grid grid-cols-3 gap-6 mb-6">
          <div className="bg-gradient-to-br from-[#1a2942] to-[#0f1c2e] rounded-xl p-6 border border-blue-500/20">
            <Target className="w-8 h-8 text-green-400 mb-3" />
            <div className="text-sm text-gray-400 mb-2">Model Accuracy</div>
            <div className="text-3xl font-bold text-green-400">{stats.accuracy}%</div>
            <div className="text-sm text-gray-400 mt-2">SVM + TF-IDF Classifier</div>
          </div>
          <div className="bg-gradient-to-br from-[#1a2942] to-[#0f1c2e] rounded-xl p-6 border border-blue-500/20">
            <Zap className="w-8 h-8 text-blue-400 mb-3" />
            <div className="text-sm text-gray-400 mb-2">F1-Score</div>
            <div className="text-3xl font-bold text-blue-400">{stats.f1Score}%</div>
            <div className="text-sm text-green-400 mt-2">Excellent performance</div>
          </div>
          <div className="bg-gradient-to-br from-[#1a2942] to-[#0f1c2e] rounded-xl p-6 border border-blue-500/20">
            <TrendingUp className="w-8 h-8 text-purple-400 mb-3" />
            <div className="text-sm text-gray-400 mb-2">Confidence</div>
            <div className="text-3xl font-bold text-purple-400">{stats.confidence}%</div>
            <div className="text-sm text-gray-400 mt-2">Prediction confidence</div>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-6 mb-6">
          <div className="bg-gradient-to-br from-[#1a2942] to-[#0f1c2e] rounded-xl p-6 border border-blue-500/20">
            <h3 className="text-lg font-semibold mb-4">Current Model Configuration</h3>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <div>
                  <div className="font-semibold">Model Type</div>
                  <div className="text-sm text-gray-400">Support Vector Machine (SVM)</div>
                </div>
                <div className="px-4 py-2 bg-green-500/20 text-green-400 rounded-lg text-sm flex items-center gap-2">
                  <CheckCircle className="w-4 h-4" />
                  Active
                </div>
              </div>
              <div className="flex justify-between items-center">
                <div>
                  <div className="font-semibold">Feature Extraction</div>
                  <div className="text-sm text-gray-400">TF-IDF Vectorizer</div>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <div>
                  <div className="font-semibold">Training Data</div>
                  <div className="text-sm text-gray-400">5,631 labeled comments (from {stats.total?.toLocaleString()} total)</div>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <div>
                  <div className="font-semibold">Validation Method</div>
                  <div className="text-sm text-gray-400">5-Fold Cross-Validation</div>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <div>
                  <div className="font-semibold">Model File</div>
                  <div className="text-sm text-blue-400">data/models/sentiment_svm_model.joblib</div>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-[#1a2942] to-[#0f1c2e] rounded-xl p-6 border border-blue-500/20">
            <h3 className="text-lg font-semibold mb-4">Training Results</h3>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between mb-1">
                  <span className="text-sm text-gray-400">Cross-Validation Accuracy</span>
                  <span className="text-sm font-semibold text-green-400">{stats.accuracy}%</span>
                </div>
                <div className="w-full bg-[#0f1c2e] rounded-full h-2">
                  <div className="bg-green-500 h-2 rounded-full" style={{ width: `${stats.accuracy}%` }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between mb-1">
                  <span className="text-sm text-gray-400">F1-Score (Weighted)</span>
                  <span className="text-sm font-semibold text-blue-400">{stats.f1Score}%</span>
                </div>
                <div className="w-full bg-[#0f1c2e] rounded-full h-2">
                  <div className="bg-blue-500 h-2 rounded-full" style={{ width: `${stats.f1Score}%` }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between mb-1">
                  <span className="text-sm text-gray-400">Test Set Accuracy</span>
                  <span className="text-sm font-semibold text-purple-400">{stats.confidence}%</span>
                </div>
                <div className="w-full bg-[#0f1c2e] rounded-full h-2">
                  <div className="bg-purple-500 h-2 rounded-full" style={{ width: `${stats.confidence}%` }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between mb-1">
                  <span className="text-sm text-gray-400">Overfitting Gap</span>
                  <span className="text-sm font-semibold text-yellow-400">2.6%</span>
                </div>
                <div className="w-full bg-[#0f1c2e] rounded-full h-2">
                  <div className="bg-yellow-500 h-2 rounded-full" style={{ width: "2.6%" }}></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-br from-[#1a2942] to-[#0f1c2e] rounded-xl p-6 border border-blue-500/20 mb-6">
          <h3 className="text-lg font-semibold mb-4">Sentiment Classification Results</h3>
          <div className="grid grid-cols-3 gap-4">
            <div className="bg-[#0f1c2e] rounded-lg p-4 border border-blue-500/10">
              <div className="flex items-center gap-2 mb-2">
                <div className="w-3 h-3 rounded-full bg-red-500"></div>
                <span className="font-medium">Negative</span>
              </div>
              <div className="text-2xl font-bold">{stats.negative?.toLocaleString()}</div>
              <div className="text-sm text-gray-400">{stats.negativePercent}% of total</div>
            </div>
            <div className="bg-[#0f1c2e] rounded-lg p-4 border border-blue-500/10">
              <div className="flex items-center gap-2 mb-2">
                <div className="w-3 h-3 rounded-full bg-green-500"></div>
                <span className="font-medium">Positive</span>
              </div>
              <div className="text-2xl font-bold">{stats.positive?.toLocaleString()}</div>
              <div className="text-sm text-gray-400">{stats.positivePercent}% of total</div>
            </div>
            <div className="bg-[#0f1c2e] rounded-lg p-4 border border-blue-500/10">
              <div className="flex items-center gap-2 mb-2">
                <div className="w-3 h-3 rounded-full bg-gray-500"></div>
                <span className="font-medium">Neutral</span>
              </div>
              <div className="text-2xl font-bold">{stats.neutral?.toLocaleString()}</div>
              <div className="text-sm text-gray-400">{stats.neutralPercent}% of total</div>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-br from-[#1a2942] to-[#0f1c2e] rounded-xl p-6 border border-blue-500/20">
          <h3 className="text-lg font-semibold mb-4">Model Actions</h3>
          <div className="flex gap-4">
            <button className="px-6 py-3 bg-blue-500 rounded-lg hover:bg-blue-600 transition">Retrain Model</button>
            <button className="px-6 py-3 bg-green-500 rounded-lg hover:bg-green-600 transition">Export Model</button>
            <button className="px-6 py-3 bg-purple-500 rounded-lg hover:bg-purple-600 transition">Test Model</button>
            <button className="px-6 py-3 bg-gray-600 rounded-lg hover:bg-gray-700 transition">View Logs</button>
          </div>
        </div>
      </div>
    </div>
  );
}
