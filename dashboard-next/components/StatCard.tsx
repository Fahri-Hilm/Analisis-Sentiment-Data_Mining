"use client";

import { LucideIcon } from "lucide-react";
import { useCountUp } from "@/hooks/useCountUp";
import { useEffect, useState } from "react";

interface StatCardProps {
  icon: LucideIcon;
  label: string;
  value: string;
  change: string;
  trend: "up" | "down";
}

export function StatCard({ icon: Icon, label, value, change, trend }: StatCardProps) {
  const [mounted, setMounted] = useState(false);

  const numericValue = parseFloat(value.replace(/[^0-9.-]/g, ""));
  const isPercentage = value.includes("%");
  const decimals = isPercentage ? 1 : 0;

  const { formattedValue } = useCountUp({
    end: isNaN(numericValue) ? 0 : numericValue,
    duration: 2000,
    decimals: decimals,
    suffix: isPercentage ? "%" : "",
  });

  useEffect(() => {
    setMounted(true);
  }, []);

  const displayValue = mounted && !isNaN(numericValue) ? formattedValue : value;

  return (
    <div className="elegant-card group overflow-hidden">
      {/* Icon with elegant background */}
      <div className="flex items-start justify-between mb-5">
        <div className="p-3 rounded-xl bg-gradient-to-br from-blue-500/10 to-cyan-500/10 
                      border border-blue-500/20 group-hover:border-blue-400/40 
                      transition-all duration-300 group-hover:scale-105">
          <Icon className="w-5 h-5 text-blue-400" strokeWidth={2} />
        </div>
        
        {/* Trend badge */}
        <span className={`text-xs font-medium px-2.5 py-1 rounded-lg transition-smooth ${
          trend === "up" 
            ? 'text-emerald-400 bg-emerald-500/10 border border-emerald-500/20' 
            : 'text-red-400 bg-red-500/10 border border-red-500/20'
        }`}>
          {change}
        </span>
      </div>

      {/* Value - Large elegant number */}
      <div className="stat-number text-slate-50 mb-2 group-hover:text-white transition-smooth">
        {displayValue}
      </div>

      {/* Label */}
      <p className="text-sm text-slate-400 font-medium tracking-tight group-hover:text-slate-300 transition-smooth">
        {label}
      </p>

      {/* Subtle bottom accent line */}
      <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r 
                    from-transparent via-blue-500/30 to-transparent 
                    opacity-0 group-hover:opacity-100 transition-smooth" />
    </div>
  );
}
