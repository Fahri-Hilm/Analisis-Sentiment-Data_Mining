"use client";

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts";

interface AreaChartProps {
  stats?: {
    positive: number;
    neutral: number;
    negative: number;
    positivePercent: string;
    neutralPercent: string;
    negativePercent: string;
  };
}

export function AreaChart({ stats }: AreaChartProps) {
  // Use real data from stats or fallback
  const data = stats ? [
    { name: "Negative", value: stats.negative, percent: parseFloat(stats.negativePercent), color: "#ef4444" },
    { name: "Positive", value: stats.positive, percent: parseFloat(stats.positivePercent), color: "#22c55e" },
    { name: "Neutral", value: stats.neutral, percent: parseFloat(stats.neutralPercent), color: "#6b7280" },
  ] : [
    { name: "Negative", value: 13419, percent: 69.8, color: "#ef4444" },
    { name: "Positive", value: 5597, percent: 29.1, color: "#22c55e" },
    { name: "Neutral", value: 212, percent: 1.1, color: "#6b7280" },
  ];

  return (
    <div className="bg-gradient-to-br from-[#1a2942]/80 to-[#0f1c2e]/80 backdrop-blur-md rounded-xl p-6 border border-blue-500/20
                    hover:border-blue-500/40 hover:shadow-lg hover:shadow-blue-500/10 transition-all duration-300">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h3 className="text-lg font-semibold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">Sentiment Distribution</h3>
          <div className="text-sm text-gray-400">Distribusi sentimen komentar</div>
        </div>
        <div className="flex gap-4 text-xs">
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <span>Negative</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
            <span>Positive</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded-full bg-gray-500"></div>
            <span>Neutral</span>
          </div>
        </div>
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} layout="vertical">
          <CartesianGrid strokeDasharray="3 3" stroke="#1a2942" />
          <XAxis type="number" stroke="#6b7280" tickFormatter={(v) => v.toLocaleString()} />
          <YAxis type="category" dataKey="name" stroke="#6b7280" width={80} />
          <Tooltip 
            contentStyle={{ backgroundColor: "#1a2942", border: "none", borderRadius: "8px" }}
            formatter={(value: number, name: string, props: any) => [
              `${value.toLocaleString()} (${props.payload.percent}%)`,
              "Comments"
            ]}
          />
          <Bar dataKey="value" radius={[0, 8, 8, 0]} isAnimationActive={true} animationDuration={1500} animationEasing="ease-out">
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      
      {/* Summary stats below chart */}
      <div className="grid grid-cols-3 gap-4 mt-4 pt-4 border-t border-gray-700">
        <div className="text-center">
          <div className="text-2xl font-bold text-red-400">{stats?.negativePercent || "69.8"}%</div>
          <div className="text-xs text-gray-400">Negative</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-green-400">{stats?.positivePercent || "29.1"}%</div>
          <div className="text-xs text-gray-400">Positive</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-gray-400">{stats?.neutralPercent || "1.1"}%</div>
          <div className="text-xs text-gray-400">Neutral</div>
        </div>
      </div>
    </div>
  );
}
