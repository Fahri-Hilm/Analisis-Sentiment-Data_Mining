import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { TrendingDown, TrendingUp, AlertTriangle, Lightbulb } from 'lucide-react';

const insights = [
  {
    icon: TrendingDown,
    title: "Dominasi Sentimen Negatif",
    description: "69.8% komentar menunjukkan kekecewaan terhadap performa timnas",
    color: "text-red-400",
    bg: "bg-red-500/10",
    border: "border-red-500/20"
  },
  {
    icon: AlertTriangle,
    title: "Target Kritik Utama",
    description: "PSSI dan pelatih menjadi sasaran utama kritik suporter",
    color: "text-amber-400",
    bg: "bg-amber-500/10",
    border: "border-amber-500/20"
  },
  {
    icon: TrendingUp,
    title: "Akurasi Model Tinggi",
    description: "Model SVM mencapai 89.4% akurasi dengan F1-Score 91%",
    color: "text-green-400",
    bg: "bg-green-500/10",
    border: "border-green-500/20"
  },
  {
    icon: Lightbulb,
    title: "Rekomendasi Strategis",
    description: "Fokus perbaikan manajemen dan komunikasi dengan suporter",
    color: "text-blue-400",
    bg: "bg-blue-500/10",
    border: "border-blue-500/20"
  }
];

export default function InteractiveInsights() {
  const [activeInsight, setActiveInsight] = useState(0);

  return (
    <div className="glass-card rounded-2xl p-6 border border-slate-800/50">
      <h3 className="text-xl font-semibold mb-6 flex items-center gap-2">
        <Lightbulb className="w-5 h-5 text-blue-400" />
        Key Insights
      </h3>
      
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-6">
        {insights.map((insight, idx) => (
          <motion.button
            key={idx}
            onClick={() => setActiveInsight(idx)}
            className={`p-3 rounded-xl border transition-all duration-300 ${
              activeInsight === idx 
                ? `${insight.bg} ${insight.border} ${insight.color}` 
                : 'bg-slate-800/30 border-slate-700/50 text-slate-400 hover:border-slate-600/50'
            }`}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <insight.icon className="w-5 h-5 mx-auto mb-1" />
            <p className="text-xs font-medium">{insight.title.split(' ')[0]}</p>
          </motion.button>
        ))}
      </div>

      <AnimatePresence mode="wait">
        <motion.div
          key={activeInsight}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.3 }}
          className={`p-4 rounded-xl ${insights[activeInsight].bg} ${insights[activeInsight].border} border`}
        >
          <div className="flex items-start gap-3">
            <insights[activeInsight].icon className={`w-6 h-6 ${insights[activeInsight].color} mt-1`} />
            <div>
              <h4 className={`font-semibold ${insights[activeInsight].color} mb-2`}>
                {insights[activeInsight].title}
              </h4>
              <p className="text-slate-300 text-sm leading-relaxed">
                {insights[activeInsight].description}
              </p>
            </div>
          </div>
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
