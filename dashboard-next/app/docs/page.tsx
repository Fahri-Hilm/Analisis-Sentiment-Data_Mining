"use client";

import { useState } from "react";
import {
  FileText,
  Brain,
  Database,
  Workflow,
  Code,
  BarChart3,
  Target,
  Zap,
  TrendingUp,
  CheckCircle,
  BookOpen,
  Search,
  Filter,
  Tags,
  Cpu,
  LineChart,
  ArrowRight,
  GitBranch,
  Layers,
  Calculator,
  FileCode,
  LayoutDashboard,
  HardDrive,
  Package,
  Monitor,
  Activity
} from "lucide-react";

export default function DocsPage() {
  const [activeTab, setActiveTab] = useState("overview");

  const workflowSteps = [
    {
      id: 1,
      title: "Data Collection",
      icon: Database,
      color: "text-blue-400",
      bg: "bg-blue-500/10",
      border: "border-blue-500/20",
      description: "Pengumpulan dataset komentar publik dari YouTube mengenai laga Indonesia vs Bahrain.",
      technical: [
        { title: "API", content: "YouTube Data API v3" },
        { title: "Query", content: "Match Highlights & Replay" }
      ],
      details: [
        { label: "Source", value: "YouTube" },
        { label: "Total", value: "19,228 Items" }
      ]
    },
    {
      id: 2,
      title: "Preprocessing",
      icon: Filter,
      color: "text-amber-400",
      bg: "bg-amber-500/10",
      border: "border-amber-500/20",
      description: "Pembersihan noise dan normalisasi teks menggunakan NLP techniques.",
      technical: [
        { title: "Regex", content: "Remove URL, Emoji, Mentions", code: "re.sub(r'...', '')" },
        { title: "Stemmer", content: "Sastrawi Library", code: "stemmer.stem(text)" }
      ],
      details: [
        { label: "Stopwords", value: "Removed" },
        { label: "Case", value: "Lowercase" }
      ]
    },
    {
      id: 3,
      title: "Feature Extraction",
      icon: FileCode,
      color: "text-purple-400",
      bg: "bg-purple-500/10",
      border: "border-purple-500/20",
      description: "Konversi teks ke vektor numerik dengan TF-IDF.",
      technical: [
        { title: "TF Formula", content: "Term Freq / Total Words", formula: "tf(t,d)" },
        { title: "IDF Formula", content: "log(N / df(t))", formula: "idf(t)" }
      ],
      details: [
        { label: "Features", value: "2000 Vectors" },
        { label: "N-gram", value: "(1,2)" }
      ]
    },
    {
      id: 4,
      title: "Modeling (SVM)",
      icon: Calculator,
      color: "text-cyan-400",
      bg: "bg-cyan-500/10",
      border: "border-cyan-500/20",
      description: "Klasifikasi sentimen menggunakan Support Vector Machine.",
      technical: [
        { title: "Hyperplane", content: "Optimal separation", formula: "w.x + b = 0" },
        { title: "Kernel", content: "Linear Kernel" }
      ],
      details: [
        { label: "Accuracy", value: "89.4%" },
        { label: "Split", value: "80:20" }
      ]
    },
    {
      id: 5,
      title: "Evaluation",
      icon: LineChart,
      color: "text-green-400",
      bg: "bg-green-500/10",
      border: "border-green-500/20",
      description: "Validasi performa model dengan metrik standar.",
      technical: [
        { title: "F1-Score", content: "Harmonic Mean", formula: "2*(P*R)/(P+R)" },
        { title: "Precision", content: "TP / (TP+FP)" }
      ],
      details: [
        { label: "Matrix", value: "Confusion Matrix" },
        { label: "Validation", value: "Cross-Val" }
      ]
    }
  ];

  const features = [
    {
      title: "Dashboard Overview",
      icon: LayoutDashboard,
      desc: "Snapshot performa sentimen secara real-time.",
      items: ["Total Comments", "Sentiment Ratio", "Top Emotions"]
    },
    {
      title: "Sentiment Analysis",
      icon: TrendingUp,
      desc: "Analisis mendalam per target (PSSI, Pemain, dll).",
      items: ["Target Breakdown", "Constructiveness", "Time Series"]
    },
    {
      title: "Emotion Insights",
      icon: Brain,
      desc: "Memahami emosi publik dibalik komentar.",
      items: ["Radar Chart", "Intensity Metrics", "5+ Emotion Classes"]
    },
    {
      title: "Comment Explorer",
      icon: Search,
      desc: "Search engine untuk 19,000+ komentar.",
      items: ["Full Text Search", "Multi-filter", "Pagination"]
    }
  ];

  const tabs = [
    { id: "overview", label: "Overview", icon: Activity },
    { id: "workflow", label: "Workflow (Pipeline)", icon: Workflow },
    { id: "architecture", label: "Architecture", icon: HardDrive },
    { id: "features", label: "Features", icon: Package },
  ];

  return (
    <div className="max-w-7xl mx-auto p-4 md:p-8 relative min-h-screen">

      {/* Header Section */}
      <div className="mb-10 text-center relative z-10">
        <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-400 via-cyan-400 to-teal-400 bg-clip-text text-transparent mb-4">
          Dokumentasi Sistem
        </h1>
        <p className="text-slate-400 text-lg max-w-2xl mx-auto">
          Panduan komprehensif analisis sentimen Timnas Indonesia vs Bahrain.
          Dari pengumpulan data hingga visualisasi dashboard.
        </p>
      </div>

      {/* Tab Navigation */}
      <div className="flex justify-center mb-12 relative z-10">
        <div className="bg-slate-900/50 p-1.5 rounded-2xl border border-slate-800/50 backdrop-blur-md flex flex-wrap justify-center gap-2">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-6 py-3 rounded-xl text-sm font-medium transition-all duration-300 ${activeTab === tab.id
                ? "bg-blue-600 text-white shadow-lg shadow-blue-500/25"
                : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
                }`}
            >
              <tab.icon className="w-4 h-4" />
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* CONTENT AREA */}
      <div className="relative z-10 min-h-[500px]">

        {/* TAB 1: OVERVIEW */}
        {activeTab === "overview" && (
          <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
            {/* Hero Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {[
                { label: "Total Data", value: "19,228", sub: "Komentar", color: "from-blue-500 to-cyan-500" },
                { label: "Akurasi Model", value: "89.4%", sub: "SVM + TF-IDF", color: "from-emerald-500 to-green-500" },
                { label: "Dominan Sentimen", value: "69.8%", sub: "Negatif (Kekecewaan)", color: "from-rose-500 to-red-500" }
              ].map((stat, i) => (
                <div key={i} className="glass-card p-6 rounded-2xl border border-slate-800/50 text-center relative overflow-hidden group">
                  <div className={`absolute inset-0 opacity-10 bg-gradient-to-br ${stat.color} group-hover:opacity-20 transition-opacity`} />
                  <h3 className="text-4xl font-bold text-white mb-2">{stat.value}</h3>
                  <p className="text-slate-400 text-sm uppercase tracking-wider font-semibold">{stat.label}</p>
                  <p className="text-slate-500 text-xs mt-1">{stat.sub}</p>
                </div>
              ))}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div className="glass-card p-8 rounded-2xl border border-slate-800/50">
                <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-3">
                  <Activity className="text-blue-400" /> Executive Summary
                </h2>
                <p className="text-slate-300 leading-relaxed mb-4">
                  Sistem ini dibangun untuk menganalisis respon publik pasca pertandingan kontroversial
                  <strong> Indonesia vs Bahrain</strong> pada Kualifikasi Piala Dunia 2026.
                </p>
                <p className="text-slate-300 leading-relaxed">
                  Tujuannya adalah mengukur tingkat kekecewaan suporter, mendeteksi target kritik (Wasit, AFC, PSSI),
                  dan memberikan insight berbasis data kepada stakeholder sepakbola nasional.
                </p>
              </div>

              <div className="glass-card p-8 rounded-2xl border border-slate-800/50">
                <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-3">
                  <Target className="text-purple-400" /> Research Objectives
                </h2>
                <ul className="space-y-4">
                  {[
                    "Mengukur sentimen publik (Positif vs Negatif)",
                    "Klasifikasi emosi (Marah, Sedih, Bangga, Harapan)",
                    "Identifikasi topik utama pembicaraan",
                    "Evaluasi performa model SVM pada teks Bahasa Indonesia"
                  ].map((item, i) => (
                    <li key={i} className="flex items-start gap-3 text-slate-300">
                      <CheckCircle className="w-5 h-5 text-green-400 shrink-0 mt-0.5" />
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}

        {/* TAB 2: WORKFLOW */}
        {activeTab === "workflow" && (
          <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <h2 className="text-2xl font-bold text-white mb-6 text-center">End-to-End Data Pipeline</h2>
            {workflowSteps.map((step, index) => (
              <div key={step.id} className="glass-card p-6 rounded-2xl border border-slate-800/50 hover:border-slate-600 transition-colors">
                <div className="flex flex-col md:flex-row gap-6">
                  <div className="shrink-0 flex flex-col items-center">
                    <div className={`w-14 h-14 rounded-2xl flex items-center justify-center ${step.bg} ${step.color} border ${step.border}`}>
                      <step.icon className="w-7 h-7" />
                    </div>
                    <div className="h-full w-0.5 bg-slate-800 my-2 rounded-full" />
                  </div>

                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="text-xl font-bold text-slate-100">{step.title}</h3>
                      <span className="text-xs font-mono text-slate-500 bg-slate-900 px-2 py-1 rounded">Stage 0{step.id}</span>
                    </div>
                    <p className="text-slate-400 mb-4">{step.description}</p>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="bg-slate-950/30 p-4 rounded-xl border border-slate-800/30">
                        <h4 className="text-xs font-bold text-blue-400 uppercase mb-3 flex items-center gap-2">
                          <Code className="w-3 h-3" /> Technical Logic
                        </h4>
                        <div className="space-y-3">
                          {step.technical.map((t: any, i) => (
                            <div key={i}>
                              <p className="text-xs text-slate-500 font-semibold">{t.title}</p>
                              <p className="text-sm text-slate-300">{t.content}</p>
                              {t.formula && <code className="text-[10px] text-emerald-400 bg-slate-900 px-1 py-0.5 rounded block mt-1 w-fit">{t.formula}</code>}
                              {t.code && <code className="text-[10px] text-amber-400 bg-slate-900 px-1 py-0.5 rounded block mt-1 w-fit">{t.code}</code>}
                            </div>
                          ))}
                        </div>
                      </div>

                      <div className="grid grid-cols-2 gap-3 content-start">
                        {step.details.map((d, i) => (
                          <div key={i} className="bg-slate-800/20 p-3 rounded-lg border border-slate-700/20">
                            <p className="text-[10px] text-slate-500 uppercase">{d.label}</p>
                            <p className="text-sm font-semibold text-slate-200">{d.value}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* TAB 3: ARCHITECTURE */}
        {activeTab === "architecture" && (
          <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">

            {/* Tech Stack */}
            <div className="glass-card p-8 rounded-2xl border border-slate-800/50">
              <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                <Layers className="text-cyan-400" /> Technology Stack
              </h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {[
                  { name: "Unknown", label: "Core", val: "Python 3.12" },
                  { name: "Scikit-Learn", label: "ML Library", val: "Version 1.5.2" },
                  { name: "Next.js", label: "Frontend", val: "App Router 14" },
                  { name: "Tailwind", label: "Styling", val: "v3.4" },
                  { name: "Recharts", label: "Viz", val: "v2.12" },
                  { name: "Pandas", label: "Data Proc", val: "DataFrame" },
                  { name: "Lucide", label: "Icons", val: "React Icons" },
                  { name: "Sastrawi", label: "NLP", val: "Bahasa Indo" },
                ].map((item, i) => (
                  <div key={i} className="bg-slate-900/40 p-4 rounded-xl border border-slate-800/50 flex flex-col items-center text-center hover:border-blue-500/30 transition-colors">
                    <div className="text-xs text-slate-500 uppercase font-bold mb-1">{item.label}</div>
                    <div className="text-slate-200 font-semibold">{item.val}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* File Structure */}
            <div className="glass-card p-8 rounded-2xl border border-slate-800/50">
              <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                <Code className="text-amber-400" /> Project Structure
              </h3>
              <div className="font-mono text-sm text-slate-400 bg-slate-950 p-6 rounded-xl border border-slate-800 overflow-x-auto">
                <pre>{`
src/
├── pipeline/          # Data collection scripts
├── preprocessing/     # Text cleaning & labeling
├── modeling/          # SVM training & evaluation
└── visualization/     # Next.js Dashboard Source
    ├── app/           # App Router Pages
    ├── components/    # Reusable UI Components
    └── public/        # Static Assets
data/
├── raw/               # Original Scraped Comments
├── processed/         # Cleaned Datasets
└── models/            # .pkl Saved Models
                   `}</pre>
              </div>
            </div>

            {/* Optimization */}
            <div className="glass-card p-8 rounded-2xl border border-slate-800/50">
              <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                <Zap className="text-yellow-400" /> Performance Optimization
              </h3>
              <ul className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {[
                  "Lazy Loading Components (Next.js Dynamic Imports)",
                  "Dataset preprocessing offline (Pre-computation)",
                  "Efficient Vectorization (Max Features Limit)",
                  "Memoized Calculations (React useMemo)",
                  "Server-side Rendering (SSR) for initial data"
                ].map((opt, i) => (
                  <li key={i} className="flex items-center gap-3 text-slate-300 text-sm bg-slate-900/20 p-3 rounded-lg">
                    <CheckCircle className="w-4 h-4 text-green-400 shrink-0" />
                    {opt}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}

        {/* TAB 4: FEATURES */}
        {activeTab === "features" && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
            {features.map((feature, i) => (
              <div key={i} className="glass-card p-6 rounded-2xl border border-slate-800/50 hover:bg-slate-900/60 transition-colors group">
                <div className="flex items-start gap-4">
                  <div className="p-3 bg-blue-500/10 rounded-xl">
                    <feature.icon className="w-6 h-6 text-blue-400" />
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-white mb-2 group-hover:text-blue-400 transition-colors">{feature.title}</h3>
                    <p className="text-sm text-slate-400 mb-4 lh-relaxed">{feature.desc}</p>
                    <div className="flex flex-wrap gap-2">
                      {feature.items.map((item, j) => (
                        <span key={j} className="text-[10px] bg-slate-950 px-2 py-1 rounded border border-slate-800 text-slate-500 font-mono">
                          {item}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

      </div>

      {/* Footer */}
      <div className="mt-20 pt-8 border-t border-slate-800/50 text-center text-slate-600 text-sm">
        <p>Created by Fahri Hilmi • Data Mining Project 2024</p>
      </div>

    </div>
  );
}
