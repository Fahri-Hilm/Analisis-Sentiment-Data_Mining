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
    <div className="bg-gradient-to-br from-[#1a2942]/80 to-[#0f1c2e]/80 backdrop-blur-md rounded-xl p-6 
                    border border-blue-500/20 hover:scale-105 hover:border-blue-500/40 
                    hover:shadow-lg hover:shadow-blue-500/20 hover:bg-[#1a2942]/90
                    transition-all duration-300 cursor-pointer group">
      <div className="flex items-center gap-3 mb-4">
        <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center 
                        group-hover:from-blue-400 group-hover:to-blue-500 group-hover:shadow-lg group-hover:shadow-blue-500/30
                        transition-all duration-300">
          <Icon className="w-6 h-6 text-white" />
        </div>
      </div>
      <div className="text-sm text-gray-400 mb-1">{label}</div>
      <div className="flex items-end justify-between">
        <div className="text-2xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
          {displayValue}
        </div>
        <div className={`text-sm font-semibold ${trend === "up" ? "text-green-400" : "text-red-400"}`}>{change}</div>
      </div>
    </div>
  );
}
