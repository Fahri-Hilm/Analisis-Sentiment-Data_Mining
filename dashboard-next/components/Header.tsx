"use client";

import { usePathname } from 'next/navigation';
import Link from 'next/link';
import { BarChart3, Radio } from 'lucide-react';

export function Header() {
  const pathname = usePathname();
  const isRealtime = pathname.startsWith('/realtime');

  return (
    <div className="bg-slate-900/50 backdrop-blur-xl border-b border-slate-800/50 px-8 py-4 sticky top-0 z-40">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-white font-mono">
            {isRealtime ? '🔴 Live Analysis' : '📊 Static Analysis'}
          </h1>
          <p className="text-sm text-slate-400">
            {isRealtime 
              ? 'Real-time sentiment monitoring and analysis' 
              : 'Comprehensive sentiment analysis dashboard'
            }
          </p>
        </div>
        
        <div className="flex items-center gap-2">
          <Link 
            href="/" 
            className={`px-4 py-2 rounded-xl font-medium transition-all duration-200 flex items-center gap-2 ${
              !isRealtime 
                ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/20' 
                : 'bg-slate-800/50 text-slate-300 hover:bg-slate-700/50 hover:text-white'
            }`}
          >
            <BarChart3 className="w-4 h-4" />
            Static Mode
          </Link>
          <Link 
            href="/realtime" 
            className={`px-4 py-2 rounded-xl font-medium transition-all duration-200 flex items-center gap-2 ${
              isRealtime 
                ? 'bg-red-600 text-white shadow-lg shadow-red-500/20' 
                : 'bg-slate-800/50 text-slate-300 hover:bg-slate-700/50 hover:text-white'
            }`}
          >
            <Radio className="w-4 h-4" />
            Live Mode
          </Link>
        </div>
      </div>
    </div>
  );
}
