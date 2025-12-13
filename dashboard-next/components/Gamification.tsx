import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Trophy, Star, Target, TrendingUp, Award, BookOpen } from 'lucide-react';

const achievements = [
  { id: 'explorer', icon: BookOpen, title: 'Data Explorer', desc: 'Jelajahi semua halaman', progress: 75, unlocked: true },
  { id: 'analyst', icon: TrendingUp, title: 'Sentiment Analyst', desc: 'Analisis 100+ komentar', progress: 100, unlocked: true },
  { id: 'master', icon: Trophy, title: 'Insight Master', desc: 'Temukan 10 insight', progress: 60, unlocked: false },
  { id: 'expert', icon: Award, title: 'Data Expert', desc: 'Gunakan semua filter', progress: 40, unlocked: false }
];

export const AchievementBadge = ({ achievement }: { achievement: any }) => (
  <motion.div
    whileHover={{ scale: 1.05 }}
    className={`p-4 rounded-xl border ${
      achievement.unlocked 
        ? 'bg-gradient-to-br from-yellow-500/20 to-orange-500/20 border-yellow-500/30' 
        : 'bg-slate-800/30 border-slate-700/50'
    }`}
  >
    <div className="flex items-center gap-3 mb-2">
      <achievement.icon className={`w-6 h-6 ${achievement.unlocked ? 'text-yellow-400' : 'text-slate-500'}`} />
      <div>
        <h4 className={`font-semibold ${achievement.unlocked ? 'text-yellow-400' : 'text-slate-400'}`}>
          {achievement.title}
        </h4>
        <p className="text-xs text-slate-500">{achievement.desc}</p>
      </div>
    </div>
    <div className="w-full bg-slate-700 rounded-full h-2">
      <motion.div
        className={`h-2 rounded-full ${achievement.unlocked ? 'bg-yellow-400' : 'bg-slate-600'}`}
        initial={{ width: 0 }}
        animate={{ width: `${achievement.progress}%` }}
        transition={{ duration: 1, delay: 0.2 }}
      />
    </div>
  </motion.div>
);

export const ProgressTracker = () => {
  const [userLevel, setUserLevel] = useState(3);
  const [xp, setXp] = useState(750);
  const nextLevelXp = 1000;

  return (
    <div className="glass-card rounded-xl p-4 border border-slate-800/50">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full flex items-center justify-center">
            <Star className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="font-semibold text-white">Level {userLevel}</h3>
            <p className="text-xs text-slate-400">Data Analyst</p>
          </div>
        </div>
        <div className="text-right">
          <p className="text-sm text-blue-400">{xp} XP</p>
          <p className="text-xs text-slate-500">{nextLevelXp - xp} to next level</p>
        </div>
      </div>
      <div className="w-full bg-slate-700 rounded-full h-2">
        <motion.div
          className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full"
          initial={{ width: 0 }}
          animate={{ width: `${(xp / nextLevelXp) * 100}%` }}
          transition={{ duration: 1 }}
        />
      </div>
    </div>
  );
};

export const InteractiveTutorial = () => {
  const [currentStep, setCurrentStep] = useState(0);
  const [showTutorial, setShowTutorial] = useState(false);

  const steps = [
    { title: 'Selamat Datang!', desc: 'Mari jelajahi dashboard analisis sentimen', target: '.dashboard-header' },
    { title: 'Lihat Statistik', desc: 'Kartu ini menampilkan ringkasan data', target: '.stat-cards' },
    { title: 'Analisis Chart', desc: 'Hover pada chart untuk detail', target: '.chart-container' },
    { title: 'Filter Data', desc: 'Gunakan filter untuk analisis spesifik', target: '.filter-panel' }
  ];

  return (
    <AnimatePresence>
      {showTutorial && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center"
        >
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="bg-slate-900 border border-slate-700 rounded-2xl p-6 max-w-md mx-4"
          >
            <h3 className="text-xl font-semibold text-white mb-2">{steps[currentStep].title}</h3>
            <p className="text-slate-300 mb-6">{steps[currentStep].desc}</p>
            <div className="flex justify-between">
              <button
                onClick={() => setShowTutorial(false)}
                className="px-4 py-2 text-slate-400 hover:text-white"
              >
                Skip
              </button>
              <div className="flex gap-2">
                {currentStep > 0 && (
                  <button
                    onClick={() => setCurrentStep(currentStep - 1)}
                    className="px-4 py-2 bg-slate-700 text-white rounded-lg"
                  >
                    Back
                  </button>
                )}
                <button
                  onClick={() => {
                    if (currentStep < steps.length - 1) {
                      setCurrentStep(currentStep + 1);
                    } else {
                      setShowTutorial(false);
                    }
                  }}
                  className="px-4 py-2 bg-blue-500 text-white rounded-lg"
                >
                  {currentStep < steps.length - 1 ? 'Next' : 'Finish'}
                </button>
              </div>
            </div>
          </motion.div>
        </motion.div>
      )}
      <button
        onClick={() => setShowTutorial(true)}
        className="fixed bottom-4 right-4 p-3 bg-blue-500 text-white rounded-full shadow-lg hover:bg-blue-600 transition-colors"
      >
        <BookOpen className="w-5 h-5" />
      </button>
    </AnimatePresence>
  );
};
