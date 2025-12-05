"use client";

import { Target } from "lucide-react";

export function SatisfactionGauge({ value, label }: { value: number; label: string }) {
  const percentage = value;
  const circumference = 2 * Math.PI * 70;
  const offset = circumference - (percentage / 100) * circumference;

  return (
    <div className="bg-gradient-to-br from-[#1a2942] to-[#0f1c2e] rounded-xl p-6 border border-blue-500/20">
      <h3 className="text-lg font-semibold mb-2">{label}</h3>
      <div className="text-sm text-gray-400 mb-6">SVM Model Performance</div>
      <div className="relative flex items-center justify-center">
        <svg className="w-48 h-48 -rotate-90">
          <circle cx="96" cy="96" r="70" stroke="#1a2942" strokeWidth="12" fill="none" />
          <circle cx="96" cy="96" r="70" stroke="url(#gradient)" strokeWidth="12" fill="none" strokeDasharray={circumference} strokeDashoffset={offset} strokeLinecap="round" />
          <defs>
            <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#3b82f6" />
              <stop offset="100%" stopColor="#8b5cf6" />
            </linearGradient>
          </defs>
        </svg>
        <div className="absolute flex flex-col items-center">
          <div className="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center mb-2">
            <Target className="w-6 h-6 text-white" />
          </div>
          <div className="text-3xl font-bold">{value}%</div>
        </div>
      </div>
      <div className="flex justify-between text-sm text-gray-400 mt-4">
        <span>0%</span>
        <span className="text-xs">Test Accuracy</span>
        <span>100%</span>
      </div>
    </div>
  );
}
