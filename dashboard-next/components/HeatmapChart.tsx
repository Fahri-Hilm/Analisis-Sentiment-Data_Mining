"use client";

import { ResponsiveContainer } from "recharts";

const heatmapData = [
  { hour: "00-06", sentiment: -0.65, intensity: 15 },
  { hour: "06-12", sentiment: -0.72, intensity: 35 },
  { hour: "12-18", sentiment: -0.68, intensity: 45 },
  { hour: "18-24", sentiment: -0.75, intensity: 25 },
];

const emotionData = [
  { emotion: "Kemarahan", pssi: 85, pelatih: 70, pemain: 60, sistem: 90 },
  { emotion: "Kekecewaan", pssi: 90, pelatih: 75, pemain: 65, sistem: 85 },
  { emotion: "Harapan", pssi: 20, pelatih: 35, pemain: 45, sistem: 15 },
  { emotion: "Dukungan", pssi: 15, pelatih: 30, pemain: 40, sistem: 10 },
];

export function HeatmapChart() {
  const getIntensityColor = (value: number) => {
    if (value >= 80) return "bg-red-600";
    if (value >= 60) return "bg-red-500";
    if (value >= 40) return "bg-orange-500";
    if (value >= 20) return "bg-yellow-500";
    return "bg-green-500";
  };

  return (
    <div className="glass-card rounded-2xl p-6 border border-slate-800/50">
      <h3 className="text-xl font-semibold mb-4">Heatmap Emosi per Target</h3>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-slate-700">
              <th className="text-left p-2">Emosi</th>
              <th className="text-center p-2">PSSI</th>
              <th className="text-center p-2">Pelatih</th>
              <th className="text-center p-2">Pemain</th>
              <th className="text-center p-2">Sistem</th>
            </tr>
          </thead>
          <tbody>
            {emotionData.map((row, i) => (
              <tr key={i} className="border-b border-slate-800">
                <td className="p-2 font-medium">{row.emotion}</td>
                <td className="p-2 text-center">
                  <div className={`inline-block w-8 h-8 rounded ${getIntensityColor(row.pssi)} flex items-center justify-center text-white text-xs font-bold`}>
                    {row.pssi}
                  </div>
                </td>
                <td className="p-2 text-center">
                  <div className={`inline-block w-8 h-8 rounded ${getIntensityColor(row.pelatih)} flex items-center justify-center text-white text-xs font-bold`}>
                    {row.pelatih}
                  </div>
                </td>
                <td className="p-2 text-center">
                  <div className={`inline-block w-8 h-8 rounded ${getIntensityColor(row.pemain)} flex items-center justify-center text-white text-xs font-bold`}>
                    {row.pemain}
                  </div>
                </td>
                <td className="p-2 text-center">
                  <div className={`inline-block w-8 h-8 rounded ${getIntensityColor(row.sistem)} flex items-center justify-center text-white text-xs font-bold`}>
                    {row.sistem}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="flex items-center gap-4 mt-4 text-xs">
        <span>Intensitas:</span>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 bg-green-500 rounded"></div>
          <span>Rendah</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 bg-yellow-500 rounded"></div>
          <span>Sedang</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 bg-red-600 rounded"></div>
          <span>Tinggi</span>
        </div>
      </div>
    </div>
  );
}
