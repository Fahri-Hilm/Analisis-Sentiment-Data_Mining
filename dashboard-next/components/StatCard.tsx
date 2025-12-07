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

  // Parse the value to determine if it's a number
  const numericValue = parseFloat(value.replace(/[^0-9.-]/g, ""));
  const isPercentage = value.includes("%");
  const hasComma = value.includes(",");
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
    <div className="glass-card rounded-xl p-6 
                    border border-primary/20 hover:scale-105 hover:border-primary/50 
                    hover:shadow-lg hover:shadow-primary/20 hover:bg-card
                    transition-all duration-300 cursor-pointer group relative overflow-hidden">
      <div className="absolute top-0 right-0 w-32 h-32 bg-primary/5 rounded-full blur-3xl -mr-16 -mt-16 pointer-events-none" />

      <div className="flex items-center gap-3 mb-4 relative z-10">
        <div className="w-12 h-12 bg-gradient-to-br from-primary/80 to-blue-600 rounded-xl flex items-center justify-center 
                        group-hover:from-primary group-hover:to-blue-500 group-hover:shadow-lg group-hover:shadow-primary/30
                        transition-all duration-300 ring-1 ring-primary/20">
          <Icon className="w-6 h-6 text-white" />
        </div>
      </div>
      <div className="text-sm text-slate-400 mb-1 font-medium">{label}</div>
      <div className="flex items-end justify-between relative z-10">
        <div className="text-2xl font-bold bg-gradient-to-r from-white to-slate-300 bg-clip-text text-transparent font-mono">
          {displayValue}
        </div>
        <div className={`text-sm font-semibold px-2 py-0.5 rounded-full bg-slate-900/50 border border-slate-800 ${trend === "up" ? "text-emerald-400" : "text-rose-400"}`}>{change}</div>
      </div>
    </div>
  );
}
