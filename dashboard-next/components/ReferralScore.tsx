"use client";

export function ReferralScore({ score, label, stats }: { score: number; label: string; stats: any }) {
  const percentage = (score / 100) * 100;

  return (
    <div className="bg-gradient-to-br from-[#1a2942] to-[#0f1c2e] rounded-xl p-6 border border-blue-500/20">
      <h3 className="text-lg font-semibold mb-6">{label}</h3>
      <div className="space-y-4">
        <div>
          <div className="text-sm text-gray-400 mb-2">Labeled Data</div>
          <div className="text-xl font-bold">{stats.total.toLocaleString()} comments</div>
        </div>
        <div>
          <div className="text-sm text-gray-400 mb-2">F1-Score</div>
          <div className="text-xl font-bold">{stats.f1Score}%</div>
        </div>
      </div>
      <div className="mt-6 relative flex items-center justify-center">
        <svg className="w-40 h-40 -rotate-90">
          <circle cx="80" cy="80" r="60" stroke="#1a2942" strokeWidth="10" fill="none" />
          <circle cx="80" cy="80" r="60" stroke="url(#gradient2)" strokeWidth="10" fill="none" strokeDasharray={377} strokeDashoffset={377 - (percentage / 100) * 377} strokeLinecap="round" />
          <defs>
            <linearGradient id="gradient2" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#10b981" />
              <stop offset="100%" stopColor="#3b82f6" />
            </linearGradient>
          </defs>
        </svg>
        <div className="absolute flex flex-col items-center">
          <div className="text-sm text-gray-400">Confidence</div>
          <div className="text-3xl font-bold">{score}%</div>
          <div className="text-xs text-gray-400">Avg Score</div>
        </div>
      </div>
    </div>
  );
}
