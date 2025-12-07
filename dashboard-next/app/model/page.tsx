"use client";

import { Activity, Target, TrendingUp, Zap } from "lucide-react";
import { motion } from "framer-motion";
import { useDashboardStats } from "@/hooks/useDashboardStats";
import { StatCard } from "@/components/StatCard";

export default function ModelPerformance() {
  const { stats, isLoading } = useDashboardStats();

  return (
    <div className="relative z-10 p-8 space-y-8">
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-4xl font-bold bg-gradient-to-r from-green-400 to-blue-500 bg-clip-text text-transparent">
          Model Performance
        </h1>
        <p className="text-slate-400 mt-2">Metrik performa model machine learning SVM + TF-IDF</p>
      </motion.div>

      {/* Model Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {isLoading ? (
          <>
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-32 bg-slate-800/50 rounded-xl animate-pulse" />
            ))}
          </>
        ) : (
          <>
            <StatCard
              label="Accuracy"
              value={`${stats?.accuracy || 0}%`}
              icon={Target}
              change="+0%"
              trend="up"
            />
            <StatCard
              label="F1-Score"
              value={`${stats?.f1Score || 0}%`}
              icon={TrendingUp}
              change="+0%"
              trend="up"
            />
            <StatCard
              label="Confidence"
              value={`${stats?.confidence || 0}%`}
              icon={Zap}
              change="+0%"
              trend="up"
            />
          </>
        )}
      </div>

      {/* Model Details */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-2xl p-6"
      >
        <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
          <Activity className="w-5 h-5 text-green-400" />
          Classification Report
        </h2>
        
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-slate-700">
                <th className="text-left py-3 px-4 text-slate-400 font-medium">Class</th>
                <th className="text-center py-3 px-4 text-slate-400 font-medium">Precision</th>
                <th className="text-center py-3 px-4 text-slate-400 font-medium">Recall</th>
                <th className="text-center py-3 px-4 text-slate-400 font-medium">F1-Score</th>
                <th className="text-center py-3 px-4 text-slate-400 font-medium">Support</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-b border-slate-800 hover:bg-slate-800/30">
                <td className="py-3 px-4 font-medium">Negative</td>
                <td className="text-center py-3 px-4">0.91</td>
                <td className="text-center py-3 px-4">0.95</td>
                <td className="text-center py-3 px-4">0.93</td>
                <td className="text-center py-3 px-4">13,419</td>
              </tr>
              <tr className="border-b border-slate-800 hover:bg-slate-800/30">
                <td className="py-3 px-4 font-medium">Positive</td>
                <td className="text-center py-3 px-4">0.85</td>
                <td className="text-center py-3 px-4">0.76</td>
                <td className="text-center py-3 px-4">0.80</td>
                <td className="text-center py-3 px-4">5,597</td>
              </tr>
              <tr className="border-b border-slate-800 hover:bg-slate-800/30">
                <td className="py-3 px-4 font-medium">Neutral</td>
                <td className="text-center py-3 px-4">0.72</td>
                <td className="text-center py-3 px-4">0.58</td>
                <td className="text-center py-3 px-4">0.64</td>
                <td className="text-center py-3 px-4">212</td>
              </tr>
              <tr className="bg-slate-800/50 font-semibold">
                <td className="py-3 px-4">Weighted Avg</td>
                <td className="text-center py-3 px-4 text-green-400">0.89</td>
                <td className="text-center py-3 px-4 text-green-400">0.89</td>
                <td className="text-center py-3 px-4 text-green-400">0.91</td>
                <td className="text-center py-3 px-4">19,228</td>
              </tr>
            </tbody>
          </table>
        </div>
      </motion.div>

      {/* Model Info */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1 }}
          className="bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-2xl p-6"
        >
          <h3 className="text-lg font-semibold mb-4">Model Architecture</h3>
          <div className="space-y-3">
            <div className="flex justify-between py-2 border-b border-slate-800">
              <span className="text-slate-400">Algorithm</span>
              <span className="font-medium">Support Vector Machine (SVM)</span>
            </div>
            <div className="flex justify-between py-2 border-b border-slate-800">
              <span className="text-slate-400">Vectorization</span>
              <span className="font-medium">TF-IDF</span>
            </div>
            <div className="flex justify-between py-2 border-b border-slate-800">
              <span className="text-slate-400">Features</span>
              <span className="font-medium">2,000 optimized</span>
            </div>
            <div className="flex justify-between py-2 border-b border-slate-800">
              <span className="text-slate-400">Kernel</span>
              <span className="font-medium">Linear</span>
            </div>
            <div className="flex justify-between py-2">
              <span className="text-slate-400">Regularization</span>
              <span className="font-medium">C=1.0</span>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className="bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-2xl p-6"
        >
          <h3 className="text-lg font-semibold mb-4">Training Details</h3>
          <div className="space-y-3">
            <div className="flex justify-between py-2 border-b border-slate-800">
              <span className="text-slate-400">Dataset Size</span>
              <span className="font-medium">19,228 comments</span>
            </div>
            <div className="flex justify-between py-2 border-b border-slate-800">
              <span className="text-slate-400">Train/Test Split</span>
              <span className="font-medium">80% / 20%</span>
            </div>
            <div className="flex justify-between py-2 border-b border-slate-800">
              <span className="text-slate-400">Cross-Validation</span>
              <span className="font-medium">5-fold</span>
            </div>
            <div className="flex justify-between py-2 border-b border-slate-800">
              <span className="text-slate-400">Preprocessing</span>
              <span className="font-medium">Sastrawi Stemmer</span>
            </div>
            <div className="flex justify-between py-2">
              <span className="text-slate-400">Status</span>
              <span className="font-medium text-green-400">Production Ready ✅</span>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
