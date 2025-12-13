"use client";

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

const trendData = [
  { date: "Sep 2025", positive: 35, negative: 60, neutral: 5 },
  { date: "Okt 2025", positive: 28, negative: 67, neutral: 5 },
  { date: "Nov 2025", positive: 22, negative: 73, neutral: 5 },
  { date: "Des 2025", positive: 18, negative: 77, neutral: 5 },
];

export function TrendChart() {
  return (
    <div className="glass-card rounded-2xl p-6 border border-slate-800/50">
      <h3 className="text-xl font-semibold mb-4">Trend Sentimen Bulanan</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={trendData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="date" stroke="#64748b" />
          <YAxis stroke="#64748b" />
          <Tooltip
            contentStyle={{
              backgroundColor: "rgba(2, 6, 23, 0.95)",
              border: "1px solid #334155",
              borderRadius: "8px",
            }}
          />
          <Line type="monotone" dataKey="positive" stroke="#10b981" strokeWidth={2} />
          <Line type="monotone" dataKey="negative" stroke="#f43f5e" strokeWidth={2} />
          <Line type="monotone" dataKey="neutral" stroke="#64748b" strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
