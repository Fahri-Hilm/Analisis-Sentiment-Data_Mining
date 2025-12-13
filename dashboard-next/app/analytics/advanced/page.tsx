"use client";

import { useState } from "react";
import { TrendingUp, Calendar, Target, BarChart3 } from "lucide-react";
import { motion } from "framer-motion";
import TrendAnalysis from "@/components/analytics/TrendAnalysis";
import ComparativeAnalysis from "@/components/analytics/ComparativeAnalysis";
import DeepDiveAnalysis from "@/components/analytics/DeepDiveAnalysis";

const tabs = [
  { id: "trend", label: "Trend Analysis", icon: TrendingUp },
  { id: "comparative", label: "Comparative Analysis", icon: BarChart3 },
  { id: "deepdive", label: "Deep Dive Analysis", icon: Target },
];

export default function AdvancedAnalytics() {
  const [activeTab, setActiveTab] = useState("trend");

  return (
    <div className="p-8 space-y-8">
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
          Advanced Analytics
        </h1>
        <p className="text-slate-400 mt-2">Analisis mendalam sentimen berdasarkan waktu, periode, dan target</p>
      </motion.div>

      <div className="flex space-x-1 bg-slate-800/30 p-1 rounded-xl">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all ${
              activeTab === tab.id
                ? "bg-blue-600 text-white"
                : "text-slate-400 hover:text-white hover:bg-slate-700/50"
            }`}
          >
            <tab.icon className="w-4 h-4" />
            {tab.label}
          </button>
        ))}
      </div>

      <motion.div
        key={activeTab}
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.3 }}
      >
        {activeTab === "trend" && <TrendAnalysis />}
        {activeTab === "comparative" && <ComparativeAnalysis />}
        {activeTab === "deepdive" && <DeepDiveAnalysis />}
      </motion.div>
    </div>
  );
}
