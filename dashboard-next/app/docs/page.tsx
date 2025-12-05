"use client";

import { Sidebar } from "@/components/Sidebar";
import { FileText, Brain, Database, Workflow, Code, BarChart3, Target, Zap, TrendingUp, CheckCircle, BookOpen } from "lucide-react";

export default function DocsPage() {
  return (
    <div className="flex h-screen bg-[#0a1628] text-white overflow-hidden">
      <Sidebar />
      <div className="flex-1 overflow-y-auto p-6">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-2xl font-bold flex items-center gap-2">
            <BookOpen className="w-6 h-6 text-blue-400" />
            Dokumentasi Sistem
          </h1>
          <p className="text-sm text-gray-400 mt-1">Panduan lengkap arsitektur dan penggunaan sistem • v2.0 • SVM + TF-IDF</p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-4 gap-4 mb-6">
          <div className="bg-[#111c2e] rounded-xl p-4 border border-gray-800">
            <div className="flex items-center gap-2 mb-1">
              <Database className="w-4 h-4 text-blue-400" />
              <span className="text-xs text-gray-400">Dataset</span>
            </div>
            <p className="text-xl font-bold">19,228</p>
          </div>
          <div className="bg-[#111c2e] rounded-xl p-4 border border-gray-800">
            <div className="flex items-center gap-2 mb-1">
              <Target className="w-4 h-4 text-green-400" />
              <span className="text-xs text-gray-400">Accuracy</span>
            </div>
            <p className="text-xl font-bold text-green-400">89.4%</p>
          </div>
          <div className="bg-[#111c2e] rounded-xl p-4 border border-gray-800">
            <div className="flex items-center gap-2 mb-1">
              <TrendingUp className="w-4 h-4 text-purple-400" />
              <span className="text-xs text-gray-400">F1-Score</span>
            </div>
            <p className="text-xl font-bold text-purple-400">91.0%</p>
          </div>
          <div className="bg-[#111c2e] rounded-xl p-4 border border-gray-800">
            <div className="flex items-center gap-2 mb-1">
              <Zap className="w-4 h-4 text-cyan-400" />
              <span className="text-xs text-gray-400">Confidence</span>
            </div>
            <p className="text-xl font-bold text-cyan-400">92.0%</p>
          </div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          {/* About Project */}
          <div className="bg-[#111c2e] rounded-xl p-4 border border-gray-800">
            <h2 className="text-lg font-semibold flex items-center gap-2 mb-4">
              <FileText className="w-5 h-5 text-blue-400" />
              About Project
            </h2>
            <p className="text-sm text-gray-300 mb-3">
              Sistem analisis sentimen untuk menganalisis respon publik Indonesia terhadap pertandingan kualifikasi Piala Dunia 2026 melawan Bahrain menggunakan algoritma Machine Learning.
            </p>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Data Source</span>
                <span className="text-white">YouTube Comments</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Total Dataset</span>
                <span className="text-white">19,228 komentar</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Period</span>
                <span className="text-white">Post-match Indonesia vs Bahrain</span>
              </div>
            </div>
          </div>

          {/* ML Model */}
          <div className="bg-[#111c2e] rounded-xl p-4 border border-gray-800">
            <h2 className="text-lg font-semibold flex items-center gap-2 mb-4">
              <Brain className="w-5 h-5 text-purple-400" />
              ML Model
            </h2>
            <div className="space-y-3">
              <div className="bg-[#0a1628] rounded-lg p-3">
                <p className="text-xs text-gray-400 mb-1">Algorithm</p>
                <p className="text-sm font-medium">Support Vector Machine (SVM)</p>
              </div>
              <div className="bg-[#0a1628] rounded-lg p-3">
                <p className="text-xs text-gray-400 mb-1">Feature Extraction</p>
                <p className="text-sm font-medium">TF-IDF Vectorization</p>
              </div>
              <div className="bg-[#0a1628] rounded-lg p-3">
                <p className="text-xs text-gray-400 mb-1">Train/Test Split</p>
                <p className="text-sm font-medium">80% Training / 20% Testing</p>
              </div>
            </div>
          </div>
        </div>

        {/* Pipeline */}
        <div className="bg-[#111c2e] rounded-xl p-4 border border-gray-800 mb-6">
          <h2 className="text-lg font-semibold flex items-center gap-2 mb-4">
            <Workflow className="w-5 h-5 text-cyan-400" />
            Processing Pipeline
          </h2>
          <div className="grid grid-cols-5 gap-2">
            {["Data Collection", "Preprocessing", "Labeling", "Training", "Evaluation"].map((step, i) => (
              <div key={i} className="text-center">
                <div className="bg-[#0a1628] rounded-lg p-3 mb-2">
                  <div className="w-8 h-8 bg-cyan-500/20 rounded-full flex items-center justify-center mx-auto mb-2">
                    <span className="text-cyan-400 font-bold">{i + 1}</span>
                  </div>
                  <p className="text-xs text-white">{step}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Metrics & Labels */}
        <div className="grid grid-cols-2 gap-4">
          {/* Performance */}
          <div className="bg-[#111c2e] rounded-xl p-4 border border-gray-800">
            <h2 className="text-lg font-semibold flex items-center gap-2 mb-4">
              <BarChart3 className="w-5 h-5 text-green-400" />
              Model Performance
            </h2>
            <div className="space-y-3">
              {[
                { label: "Accuracy", value: 89.4, color: "bg-green-500" },
                { label: "F1-Score", value: 91.0, color: "bg-blue-500" },
                { label: "Precision", value: 88.5, color: "bg-purple-500" },
                { label: "Recall", value: 93.5, color: "bg-cyan-500" },
              ].map((metric, i) => (
                <div key={i}>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-400">{metric.label}</span>
                    <span className="text-white">{metric.value}%</span>
                  </div>
                  <div className="h-2 bg-gray-700 rounded-full overflow-hidden">
                    <div className={`h-full ${metric.color} rounded-full`} style={{ width: `${metric.value}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Labels */}
          <div className="bg-[#111c2e] rounded-xl p-4 border border-gray-800">
            <h2 className="text-lg font-semibold flex items-center gap-2 mb-4">
              <Code className="w-5 h-5 text-amber-400" />
              Multi-Layer Labels
            </h2>
            <div className="space-y-2">
              {[
                { name: "Sentiment", desc: "Positive, Negative, Neutral", color: "text-green-400" },
                { name: "Emotion", desc: "Kekecewaan, Kemarahan, Harapan, dll", color: "text-purple-400" },
                { name: "Target", desc: "PSSI, Pelatih, Pemain, dll", color: "text-cyan-400" },
                { name: "Constructiveness", desc: "Constructive vs Destructive", color: "text-amber-400" },
              ].map((label, i) => (
                <div key={i} className="flex items-start gap-3 bg-[#0a1628] rounded-lg p-3">
                  <CheckCircle className={`w-4 h-4 ${label.color} mt-0.5`} />
                  <div>
                    <p className="text-sm font-medium">{label.name}</p>
                    <p className="text-xs text-gray-400">{label.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
