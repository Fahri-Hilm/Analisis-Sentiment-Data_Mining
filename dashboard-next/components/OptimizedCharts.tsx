import { memo, useMemo } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const EMOTION_COLORS = ["#f43f5e", "#8b5cf6", "#3b82f6", "#06b6d4", "#10b981", "#f59e0b"];
const TARGET_COLORS = ["#6366f1", "#14b8a6", "#f97316", "#ec4899", "#84cc16"];

const tooltipStyle = {
  backgroundColor: "rgba(2, 6, 23, 0.95)",
  border: "1px solid #334155",
  borderRadius: "12px",
  boxShadow: "none",
  backdropFilter: "blur(10px)",
  color: "#ffffff"
};

export const OptimizedEmotionChart = memo(function OptimizedEmotionChart({ data }: { data: any[] }) {
  const chartData = useMemo(() => 
    data?.map((e, i) => ({ 
      name: e.name, 
      value: e.count, 
      pct: parseFloat(e.percentage), 
      fill: EMOTION_COLORS[i % 6] 
    })) || [], [data]
  );

  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart data={chartData} layout="vertical" margin={{ left: 10, right: 20 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
        <XAxis type="number" stroke="#64748b" fontSize={10} />
        <YAxis type="category" dataKey="name" stroke="#94a3b8" width={100} fontSize={11} tickLine={false} axisLine={false} />
        <Tooltip 
          cursor={{ fill: 'rgba(30, 41, 59, 0.1)' }} 
          contentStyle={tooltipStyle}
          formatter={(v: number, n: string, p: any) => [v.toLocaleString() + " (" + p.payload.pct + "%)", ""]} 
          labelStyle={{ color: '#ffffff' }}
          itemStyle={{ color: '#ffffff' }}
          wrapperStyle={{ zIndex: 9999 }}
        />
        <Bar dataKey="value" radius={[0, 6, 6, 0]} barSize={24}>
          {chartData.map((e: any, i: number) => <Cell key={i} fill={e.fill} />)}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
});

export const OptimizedTargetChart = memo(function OptimizedTargetChart({ data }: { data: any[] }) {
  const chartData = useMemo(() => 
    data?.map((t, i) => ({ 
      name: t.name, 
      value: t.count, 
      pct: parseFloat(t.percentage), 
      fill: TARGET_COLORS[i % 5] 
    })) || [], [data]
  );

  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart data={chartData} margin={{ left: 10, right: 20, bottom: 30 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
        <XAxis dataKey="name" stroke="#94a3b8" fontSize={10} angle={-15} textAnchor="end" height={60} />
        <YAxis stroke="#64748b" fontSize={10} />
        <Tooltip 
          cursor={{ fill: 'rgba(30, 41, 59, 0.1)' }} 
          contentStyle={tooltipStyle}
          formatter={(v: number, n: string, p: any) => [v.toLocaleString() + " (" + p.payload.pct + "%)", ""]} 
          labelStyle={{ color: '#ffffff' }}
          itemStyle={{ color: '#ffffff' }}
          wrapperStyle={{ zIndex: 9999 }}
        />
        <Bar dataKey="value" radius={[6, 6, 0, 0]}>
          {chartData.map((t: any, i: number) => <Cell key={i} fill={t.fill} />)}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
});

export const OptimizedPieChart = memo(function OptimizedPieChart({ data, colors }: { data: any[], colors: string[] }) {
  const chartData = useMemo(() => 
    data?.map((item, i) => ({ 
      ...item, 
      fill: colors[i % colors.length] 
    })) || [], [data, colors]
  );

  return (
    <ResponsiveContainer width="100%" height="100%">
      <PieChart>
        <Pie 
          data={chartData} 
          cx="50%" 
          cy="50%" 
          innerRadius={80} 
          outerRadius={110} 
          paddingAngle={5} 
          dataKey="value" 
          stroke="none"
        >
          {chartData.map((entry, i) => <Cell key={i} fill={entry.fill} />)}
        </Pie>
        <Tooltip 
          contentStyle={tooltipStyle}
          formatter={(v: number) => [v.toLocaleString(), "Komentar"]} 
          itemStyle={{ color: '#fff' }} 
        />
      </PieChart>
    </ResponsiveContainer>
  );
});
