"use client";

import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from "recharts";

export function SentimentDistribution({ stats }: { stats: any }) {
  const data = [
    { name: "Positive", value: parseFloat(stats.positivePercent), count: stats.positive, color: "#10b981" },
    { name: "Neutral", value: parseFloat(stats.neutralPercent), count: stats.neutral, color: "#6b7280" },
    { name: "Negative", value: parseFloat(stats.negativePercent), count: stats.negative, color: "#ef4444" },
  ];

  return (
    <div className="bg-gradient-to-br from-[#1a2942] to-[#0f1c2e] rounded-xl p-6 border border-blue-500/20">
      <h3 className="text-lg font-semibold mb-2">Sentiment Distribution</h3>
      <div className="text-sm text-gray-400 mb-6">Total: {stats.total.toLocaleString()} comments</div>
      <ResponsiveContainer width="100%" height={250}>
        <PieChart>
          <Pie data={data} cx="50%" cy="50%" innerRadius={50} outerRadius={80} dataKey="value" label={(entry) => `${entry.value}%`}>
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip formatter={(value: any, name: any, props: any) => [`${props.payload.count} comments (${value}%)`, name]} contentStyle={{ backgroundColor: "#1a2942", border: "none", borderRadius: "8px" }} />
        </PieChart>
      </ResponsiveContainer>
      <div className="mt-4 space-y-2">
        {data.map((item, i) => (
          <div key={i} className="flex items-center justify-between text-sm">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }}></div>
              <span>{item.name}</span>
            </div>
            <span className="text-gray-400">{item.count.toLocaleString()}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
