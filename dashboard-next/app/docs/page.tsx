"use client";


import { FileText, Brain, Database, Workflow, Code, BarChart3, Target, Zap, TrendingUp, CheckCircle, BookOpen } from "lucide-react";

export default function DocsPage() {
  return (
    <div className="max-w-7xl mx-auto p-8 relative">
      {/* Background Ambient Glow */}
      <div className="absolute top-0 right-0 w-full h-[500px] bg-indigo-500/5 rounded-full blur-[100px] pointer-events-none -translate-y-1/2" />

      <div className="mb-10 relative z-10">
        <h1 className="text-4xl font-bold flex items-center gap-3 bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
          <BookOpen className="w-8 h-8 text-blue-400" />
          Dokumentasi Sistem
        </h1>
        <p className="text-slate-400 text-lg mt-2 font-light tracking-wide">Panduan lengkap arsitektur dan penggunaan sistem • v2.0 • SVM + TF-IDF</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-8 relative z-10">
        {[
          { icon: Database, label: "Dataset", value: "19,228", color: "text-blue-400" },
          { icon: Target, label: "Accuracy", value: "89.4%", color: "text-green-400" },
          { icon: TrendingUp, label: "F1-Score", value: "91.0%", color: "text-purple-400" },
          { icon: Zap, label: "Confidence", value: "92.0%", color: "text-cyan-400" }
        ].map((stat, i) => (
          <div key={i} className="glass-card rounded-xl p-6 border border-slate-800/50">
            <div className="flex items-center gap-2 mb-2">
              <stat.icon className={`w-4 h-4 ${stat.color}`} />
              <span className="text-xs text-slate-500 uppercase tracking-wider font-medium">{stat.label}</span>
            </div>
            <p className={`text-2xl font-bold ${stat.color}`}>{stat.value}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8 relative z-10">
        <div className="glass-card rounded-2xl p-8 border border-slate-800/50">
          <h2 className="text-xl font-semibold flex items-center gap-2 mb-6 text-slate-200">
            <FileText className="w-5 h-5 text-blue-400" />About Project
          </h2>
          <p className="text-slate-300 leading-relaxed font-light mb-6">
            Sistem analisis sentimen untuk menganalisis respon publik Indonesia terhadap pertandingan kualifikasi Piala Dunia 2026 melawan Bahrain menggunakan algoritma Machine Learning.
          </p>
          <div className="space-y-4">
            {[
              { label: "Data Source", value: "YouTube Comments" },
              { label: "Total Dataset", value: "19,228 komentar" },
              { label: "Period", value: "Post-match Indonesia vs Bahrain" }
            ].map((item, i) => (
              <div key={i} className="flex justify-between items-center text-sm border-b border-slate-800/50 pb-2 last:border-0 last:pb-0">
                <span className="text-slate-500">{item.label}</span>
                <span className="text-slate-200 font-medium">{item.value}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="glass-card rounded-2xl p-8 border border-slate-800/50">
          <h2 className="text-xl font-semibold flex items-center gap-2 mb-6 text-slate-200">
            <Brain className="w-5 h-5 text-purple-400" />ML Model
          </h2>
          <div className="space-y-4">
            {[
              { label: "Algorithm", value: "Support Vector Machine (SVM)" },
              { label: "Feature Extraction", value: "TF-IDF Vectorization" },
              { label: "Train/Test Split", value: "80% Training / 20% Testing" }
            ].map((item, i) => (
              <div key={i} className="bg-slate-900/40 rounded-xl p-4 border border-slate-800/50">
                <p className="text-xs text-slate-500 uppercase tracking-wider mb-1 font-medium">{item.label}</p>
                <p className="text-sm font-semibold text-slate-200">{item.value}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="glass-card rounded-2xl p-8 border border-slate-800/50 mb-8 relative z-10 bg-slate-900/40">
        <h2 className="text-xl font-semibold flex items-center gap-2 mb-6 text-slate-200">
          <Workflow className="w-5 h-5 text-cyan-400" />Processing Pipeline
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          {["Data Collection", "Preprocessing", "Labeling", "Training", "Evaluation"].map((step, i) => (
            <div key={i} className="text-center group">
              <div className="bg-slate-900/50 rounded-xl p-4 mb-3 border border-slate-800/50 group-hover:border-cyan-500/30 transition-colors">
                <div className="w-10 h-10 bg-cyan-500/10 rounded-full flex items-center justify-center mx-auto mb-3 shadow-[0_0_10px_-2px_rgba(6,182,212,0.2)]">
                  <span className="text-cyan-400 font-bold">{i + 1}</span>
                </div>
                <p className="text-xs text-slate-300 font-medium uppercase tracking-wide">{step}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 relative z-10">
        <div className="glass-card rounded-2xl p-8 border border-slate-800/50">
          <h2 className="text-xl font-semibold flex items-center gap-2 mb-6 text-slate-200">
            <BarChart3 className="w-5 h-5 text-green-400" />Model Performance
          </h2>
          <div className="space-y-4">
            {[
              { label: "Accuracy", value: 89.4, color: "bg-green-500" },
              { label: "F1-Score", value: 91.0, color: "bg-blue-500" },
              { label: "Precision", value: 88.5, color: "bg-purple-500" },
              { label: "Recall", value: 93.5, color: "bg-cyan-500" },
            ].map((metric, i) => (
              <div key={i}>
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-slate-400 font-medium">{metric.label}</span>
                  <span className="text-white font-bold">{metric.value}%</span>
                </div>
                <div className="h-2.5 bg-slate-800 rounded-full overflow-hidden">
                  <div className={`h-full ${metric.color} rounded-full shadow-[0_0_8px]`} style={{ width: `${metric.value}%` }} />
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="glass-card rounded-2xl p-8 border border-slate-800/50">
          <h2 className="text-xl font-semibold flex items-center gap-2 mb-6 text-slate-200">
            <Code className="w-5 h-5 text-amber-400" />Multi-Layer Labels
          </h2>
          <div className="space-y-3">
            {[
              { name: "Sentiment", desc: "Positive, Negative, Neutral", color: "text-green-400" },
              { name: "Emotion", desc: "Kekecewaan, Kemarahan, Harapan, dll", color: "text-purple-400" },
              { name: "Target", desc: "PSSI, Pelatih, Pemain, dll", color: "text-cyan-400" },
              { name: "Constructiveness", desc: "Constructive vs Destructive", color: "text-amber-400" },
            ].map((label, i) => (
              <div key={i} className="flex items-start gap-4 bg-slate-900/40 rounded-xl p-4 border border-slate-800/50 hover:bg-slate-800/60 transition-colors">
                <CheckCircle className={`w-5 h-5 ${label.color} mt-0.5 shrink-0`} />
                <div>
                  <p className="text-sm font-semibold text-slate-200">{label.name}</p>
                  <p className="text-xs text-slate-500 mt-1">{label.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
