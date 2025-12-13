import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Calendar, GitCompare, ZoomIn, TrendingDown, TrendingUp } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, ResponsiveContainer, Tooltip } from 'recharts';

const timelineData = [
  { date: 'Sep 2024', sentiment: -0.7, event: 'Kegagalan kualifikasi dimulai' },
  { date: 'Oct 2024', sentiment: -0.8, event: 'Kekalahan beruntun' },
  { date: 'Nov 2024', sentiment: -0.9, event: 'Eliminasi resmi' },
  { date: 'Dec 2024', sentiment: -0.6, event: 'Evaluasi dan harapan baru' }
];

export const TimelineView = () => {
  const [selectedPeriod, setSelectedPeriod] = useState('all');

  return (
    <div className="glass-card rounded-2xl p-6 border border-slate-800/50">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-semibold flex items-center gap-2">
          <Calendar className="w-5 h-5 text-blue-400" />
          Timeline Sentimen
        </h3>
        <select
          value={selectedPeriod}
          onChange={(e) => setSelectedPeriod(e.target.value)}
          className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-1 text-white"
        >
          <option value="all">Semua Periode</option>
          <option value="recent">3 Bulan Terakhir</option>
          <option value="peak">Periode Puncak</option>
        </select>
      </div>

      <div className="h-64 mb-6">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={timelineData}>
            <XAxis dataKey="date" stroke="#64748b" />
            <YAxis stroke="#64748b" />
            <Tooltip
              contentStyle={{
                backgroundColor: "rgba(2, 6, 23, 0.95)",
                border: "1px solid #334155",
                borderRadius: "8px"
              }}
            />
            <Line
              type="monotone"
              dataKey="sentiment"
              stroke="#3b82f6"
              strokeWidth={3}
              dot={{ fill: '#3b82f6', strokeWidth: 2, r: 6 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="space-y-3">
        {timelineData.map((item, idx) => (
          <motion.div
            key={idx}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: idx * 0.1 }}
            className="flex items-center gap-4 p-3 bg-slate-800/30 rounded-lg"
          >
            <div className={`w-3 h-3 rounded-full ${item.sentiment < -0.8 ? 'bg-red-500' : item.sentiment < -0.6 ? 'bg-amber-500' : 'bg-green-500'}`} />
            <div className="flex-1">
              <p className="font-medium text-white">{item.event}</p>
              <p className="text-sm text-slate-400">{item.date}</p>
            </div>
            <div className="flex items-center gap-1">
              {item.sentiment < -0.7 ? (
                <TrendingDown className="w-4 h-4 text-red-400" />
              ) : (
                <TrendingUp className="w-4 h-4 text-green-400" />
              )}
              <span className="text-sm font-mono">{item.sentiment.toFixed(1)}</span>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export const ComparisonMode = () => {
  const [compareMode, setCompareMode] = useState(false);

  const beforeData = { negative: 45, positive: 35, neutral: 20 };
  const afterData = { negative: 70, positive: 25, neutral: 5 };

  return (
    <div className="glass-card rounded-2xl p-6 border border-slate-800/50">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-semibold flex items-center gap-2">
          <GitCompare className="w-5 h-5 text-purple-400" />
          Perbandingan Sentimen
        </h3>
        <button
          onClick={() => setCompareMode(!compareMode)}
          className={`px-4 py-2 rounded-lg transition-colors ${
            compareMode 
              ? 'bg-purple-500 text-white' 
              : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
          }`}
        >
          {compareMode ? 'Mode Normal' : 'Mode Perbandingan'}
        </button>
      </div>

      <AnimatePresence mode="wait">
        {compareMode ? (
          <motion.div
            key="comparison"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="grid grid-cols-2 gap-6"
          >
            <div className="space-y-3">
              <h4 className="font-semibold text-green-400">Sebelum Eliminasi</h4>
              {Object.entries(beforeData).map(([key, value]) => (
                <div key={key} className="flex justify-between items-center p-2 bg-slate-800/30 rounded">
                  <span className="capitalize text-slate-300">{key}</span>
                  <span className="font-bold text-white">{value}%</span>
                </div>
              ))}
            </div>
            <div className="space-y-3">
              <h4 className="font-semibold text-red-400">Setelah Eliminasi</h4>
              {Object.entries(afterData).map(([key, value]) => (
                <div key={key} className="flex justify-between items-center p-2 bg-slate-800/30 rounded">
                  <span className="capitalize text-slate-300">{key}</span>
                  <span className="font-bold text-white">{value}%</span>
                </div>
              ))}
            </div>
          </motion.div>
        ) : (
          <motion.div
            key="normal"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="text-center py-8"
          >
            <GitCompare className="w-12 h-12 text-slate-500 mx-auto mb-4" />
            <p className="text-slate-400">Aktifkan mode perbandingan untuk melihat perubahan sentimen</p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export const DrillDownCapability = ({ data }: { data: any }) => {
  const [drillLevel, setDrillLevel] = useState(0);
  const [breadcrumb, setBreadcrumb] = useState(['Overview']);

  const drillDown = (category: string) => {
    setDrillLevel(drillLevel + 1);
    setBreadcrumb([...breadcrumb, category]);
  };

  const drillUp = (level: number) => {
    setDrillLevel(level);
    setBreadcrumb(breadcrumb.slice(0, level + 1));
  };

  return (
    <div className="glass-card rounded-2xl p-6 border border-slate-800/50">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-semibold flex items-center gap-2">
          <ZoomIn className="w-5 h-5 text-cyan-400" />
          Detail Analysis
        </h3>
        <div className="flex items-center gap-2 text-sm">
          {breadcrumb.map((crumb, idx) => (
            <div key={idx} className="flex items-center gap-2">
              <button
                onClick={() => drillUp(idx)}
                className="text-blue-400 hover:text-blue-300"
              >
                {crumb}
              </button>
              {idx < breadcrumb.length - 1 && <span className="text-slate-500">/</span>}
            </div>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        {['Kekecewaan', 'Kemarahan', 'Harapan'].map((emotion, idx) => (
          <motion.button
            key={emotion}
            onClick={() => drillDown(emotion)}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="p-4 bg-slate-800/30 border border-slate-700/50 rounded-lg hover:border-cyan-500/50 transition-colors"
          >
            <div className="text-lg font-bold text-white">{(Math.random() * 5000 + 1000).toFixed(0)}</div>
            <div className="text-sm text-slate-400">{emotion}</div>
            <ZoomIn className="w-4 h-4 text-cyan-400 mt-2 mx-auto" />
          </motion.button>
        ))}
      </div>
    </div>
  );
};
