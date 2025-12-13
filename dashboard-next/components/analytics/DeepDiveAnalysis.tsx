"use client";

import { TreemapChart, Treemap, ResponsiveContainer, Tooltip, PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid } from "recharts";
import { Target, Users, UserCheck, Shield } from "lucide-react";
import { motion } from "framer-motion";
import { useState } from "react";

const targetData = [
  { name: "PSSI", value: 8500, sentiment: -0.75, color: "#dc2626" },
  { name: "Pelatih", value: 4200, sentiment: -0.68, color: "#f43f5e" },
  { name: "Pemain", value: 3800, sentiment: -0.45, color: "#f97316" },
  { name: "Sistem", value: 2100, sentiment: -0.82, color: "#b91c1c" },
  { name: "Wasit", value: 600, sentiment: -0.55, color: "#fb7185" },
];

const playerData = [
  { name: "Egy Maulana", positive: 25, negative: 70, neutral: 5 },
  { name: "Witan Sulaeman", positive: 30, negative: 65, neutral: 5 },
  { name: "Marselino", positive: 45, negative: 50, neutral: 5 },
  { name: "Pratama Arhan", positive: 20, negative: 75, neutral: 5 },
  { name: "Rizky Ridho", positive: 35, negative: 60, neutral: 5 },
  { name: "Asnawi Mangkualam", positive: 28, negative: 67, neutral: 5 },
];

const coachData = [
  { aspect: "Taktik", score: 25 },
  { aspect: "Motivasi", score: 30 },
  { aspect: "Substitusi", score: 20 },
  { aspect: "Formasi", score: 35 },
  { aspect: "Komunikasi", score: 28 },
];

const pssiData = [
  { issue: "Manajemen", count: 3200, sentiment: -0.85 },
  { issue: "Kebijakan", count: 2800, sentiment: -0.78 },
  { issue: "Transparansi", count: 1900, sentiment: -0.82 },
  { issue: "Fasilitas", count: 1600, sentiment: -0.70 },
];

export default function DeepDiveAnalysis() {
  const [selectedTarget, setSelectedTarget] = useState("PSSI");

  const renderCustomTooltip = (props: any) => {
    if (props.active && props.payload) {
      return (
        <div className="bg-slate-900 border border-slate-700 rounded-lg p-3">
          <p className="text-white font-medium">{props.payload[0]?.payload?.name}</p>
          <p className="text-blue-400">Komentar: {props.payload[0]?.value?.toLocaleString()}</p>
          <p className="text-red-400">Sentimen: {(props.payload[0]?.payload?.sentiment * 100).toFixed(1)}%</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4 mb-6">
        <select
          value={selectedTarget}
          onChange={(e) => setSelectedTarget(e.target.value)}
          className="bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-white"
        >
          <option value="PSSI">PSSI</option>
          <option value="Pelatih">Pelatih</option>
          <option value="Pemain">Pemain</option>
          <option value="Sistem">Sistem</option>
        </select>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <motion.div className="glass-card rounded-2xl p-6 border border-slate-800/50">
          <div className="flex items-center gap-2 mb-4">
            <Target className="w-5 h-5 text-red-400" />
            <h3 className="text-lg font-semibold">Target Utama</h3>
          </div>
          <div className="text-2xl font-bold text-red-400">PSSI</div>
          <p className="text-sm text-slate-400">8,500 komentar (-75%)</p>
        </motion.div>

        <motion.div className="glass-card rounded-2xl p-6 border border-slate-800/50">
          <div className="flex items-center gap-2 mb-4">
            <Users className="w-5 h-5 text-orange-400" />
            <h3 className="text-lg font-semibold">Pemain Terkritik</h3>
          </div>
          <div className="text-2xl font-bold text-orange-400">Pratama Arhan</div>
          <p className="text-sm text-slate-400">75% sentimen negatif</p>
        </motion.div>

        <motion.div className="glass-card rounded-2xl p-6 border border-slate-800/50">
          <div className="flex items-center gap-2 mb-4">
            <UserCheck className="w-5 h-5 text-blue-400" />
            <h3 className="text-lg font-semibold">Pelatih</h3>
          </div>
          <div className="text-2xl font-bold text-blue-400">Shin Tae-yong</div>
          <p className="text-sm text-slate-400">4,200 komentar (-68%)</p>
        </motion.div>

        <motion.div className="glass-card rounded-2xl p-6 border border-slate-800/50">
          <div className="flex items-center gap-2 mb-4">
            <Shield className="w-5 h-5 text-purple-400" />
            <h3 className="text-lg font-semibold">Isu Sistem</h3>
          </div>
          <div className="text-2xl font-bold text-purple-400">Manajemen</div>
          <p className="text-sm text-slate-400">Kritik terbanyak (-82%)</p>
        </motion.div>
      </div>

      <motion.div className="glass-card rounded-2xl p-6 border border-slate-800/50">
        <h3 className="text-xl font-semibold mb-4">Distribusi Target Kritik</h3>
        <ResponsiveContainer width="100%" height={300}>
          <Treemap
            data={targetData}
            dataKey="value"
            aspectRatio={4/3}
            stroke="#334155"
            fill="#8884d8"
            content={({ root, depth, x, y, width, height, index, payload, colors, rank, name }) => {
              return (
                <g>
                  <rect
                    x={x}
                    y={y}
                    width={width}
                    height={height}
                    style={{
                      fill: payload?.color || colors?.[index % colors?.length],
                      stroke: "#334155",
                      strokeWidth: 2,
                      strokeOpacity: 1,
                    }}
                  />
                  {width > 60 && height > 30 && (
                    <text x={x + width / 2} y={y + height / 2} textAnchor="middle" fill="#fff" fontSize="12">
                      <tspan x={x + width / 2} dy="0">{name}</tspan>
                      <tspan x={x + width / 2} dy="15">{payload?.value?.toLocaleString()}</tspan>
                    </text>
                  )}
                </g>
              );
            }}
          />
        </ResponsiveContainer>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <motion.div className="glass-card rounded-2xl p-6 border border-slate-800/50">
          <h3 className="text-xl font-semibold mb-4">Sentimen per Pemain</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={playerData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="name" stroke="#64748b" angle={-45} textAnchor="end" height={80} />
              <YAxis stroke="#64748b" />
              <Tooltip
                contentStyle={{
                  backgroundColor: "rgba(2, 6, 23, 0.95)",
                  border: "1px solid #334155",
                  borderRadius: "8px",
                }}
              />
              <Bar dataKey="positive" fill="#10b981" />
              <Bar dataKey="negative" fill="#f43f5e" />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>

        <motion.div className="glass-card rounded-2xl p-6 border border-slate-800/50">
          <h3 className="text-xl font-semibold mb-4">Kritik Aspek Pelatih</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={coachData} layout="horizontal">
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis type="number" stroke="#64748b" />
              <YAxis dataKey="aspect" type="category" stroke="#64748b" />
              <Tooltip
                contentStyle={{
                  backgroundColor: "rgba(2, 6, 23, 0.95)",
                  border: "1px solid #334155",
                  borderRadius: "8px",
                }}
              />
              <Bar dataKey="score" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>
      </div>

      {selectedTarget === "PSSI" && (
        <motion.div className="glass-card rounded-2xl p-6 border border-slate-800/50">
          <h3 className="text-xl font-semibold mb-4">Breakdown Kritik PSSI</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {pssiData.map((item, index) => (
              <div key={index} className="bg-slate-800/30 rounded-lg p-4">
                <h4 className="font-medium text-white">{item.issue}</h4>
                <p className="text-2xl font-bold text-red-400">{item.count.toLocaleString()}</p>
                <p className="text-sm text-slate-400">Sentimen: {(item.sentiment * 100).toFixed(1)}%</p>
              </div>
            ))}
          </div>
        </motion.div>
      )}
    </div>
  );
}
