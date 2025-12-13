"use client";

import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";

const sentimentData = [
  { name: "Negatif", value: 69.8, count: 13421, color: "#f43f5e" },
  { name: "Positif", value: 29.1, count: 5595, color: "#10b981" },
  { name: "Netral", value: 1.1, count: 212, color: "#64748b" },
];

export function SentimentChart() {
  return (
    <div className="glass-card rounded-2xl p-6 border border-slate-800/50">
      <h3 className="text-xl font-semibold mb-4">Distribusi Sentimen</h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={sentimentData}
            cx="50%"
            cy="50%"
            outerRadius={100}
            dataKey="value"
            label={({ name, value }) => `${name}: ${value}%`}
          >
            {sentimentData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip
            formatter={(value, name) => [`${value}%`, name]}
            contentStyle={{
              backgroundColor: "rgba(2, 6, 23, 0.95)",
              border: "1px solid #334155",
              borderRadius: "8px",
            }}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
