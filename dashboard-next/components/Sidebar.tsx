"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  LayoutDashboard, 
  MessageSquare, 
  TrendingUp, 
  Heart, 
  Database, 
  Activity, 
  Zap,
  FileText,
  Settings
} from "lucide-react";

export function Sidebar() {
  const pathname = usePathname();

  const analysisItems = [
    { href: "/", icon: LayoutDashboard, label: "Dashboard" },
    { href: "/sentiment", icon: TrendingUp, label: "Sentiment Analysis" },
    { href: "/emotions", icon: Heart, label: "Emotion Insights" },
    { href: "/comments", icon: MessageSquare, label: "Comments Explorer" },
    { href: "/model", icon: Activity, label: "Model Performance" },
  ];

  const toolsItems = [
    { href: "/analytics", icon: Zap, label: "Live Analyzer" },
    { href: "/dataset", icon: Database, label: "Dataset" },
    { href: "/docs", icon: FileText, label: "Documentation" },
  ];

  const NavItem = ({ item }: { item: any }) => {
    const isActive = pathname === item.href;
    return (
      <Link
        href={item.href}
        className={`group flex items-center gap-3 px-4 py-3 text-sm font-medium transition-all duration-200 relative ${isActive
            ? "text-cyan-400 bg-cyan-950/10"
            : "text-slate-400 hover:text-slate-200 hover:bg-slate-900/40 hover:translate-x-1"
          }`}
      >
        {isActive && (
          <div className="absolute left-0 top-0 bottom-0 w-1 bg-cyan-500 shadow-[0_0_12px_rgba(6,182,212,0.6)]" />
        )}
        <item.icon
          className={`w-5 h-5 transition-colors ${isActive ? "text-cyan-400" : "text-slate-500 group-hover:text-slate-300"
            }`}
        />
        <span className="tracking-wide">{item.label}</span>
      </Link>
    );
  };

  return (
    <div className="w-72 bg-[#020617]/80 border-r border-slate-800/50 flex flex-col h-screen backdrop-blur-xl fixed left-0 top-0 z-50">
      <div className="p-6 mb-2">
        <Link href="/" className="flex items-center gap-3 group">
          <div className="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/20 group-hover:scale-110 transition-transform duration-300 border border-blue-400/20">
            <Activity className="w-6 h-6 text-white" />
          </div>
          <div className="flex flex-col">
            <span className="font-bold text-xl tracking-tight text-white group-hover:text-blue-400 transition-colors font-mono">ANALYSIS</span>
            <span className="text-[10px] text-slate-400 uppercase tracking-widest font-medium">Dashboard v2.0</span>
          </div>
        </Link>
      </div>

      <div className="flex-1 overflow-y-auto py-2 space-y-8 no-scrollbar">
        <div>
          <div className="px-6 mb-3 text-xs font-semibold text-slate-500 uppercase tracking-widest font-mono">Analysis</div>
          <nav className="flex flex-col space-y-1">
            {analysisItems.map((item) => (
              <NavItem key={item.href} item={item} />
            ))}
          </nav>
        </div>

        <div>
          <div className="px-6 mb-3 text-xs font-semibold text-slate-500 uppercase tracking-widest font-mono">Tools</div>
          <nav className="flex flex-col space-y-1">
            {toolsItems.map((item) => (
              <NavItem key={item.href} item={item} />
            ))}
          </nav>
        </div>
      </div>

      <div className="p-4 border-t border-slate-800/50 bg-[#020617]/50">
        <div className="glass-card rounded-xl p-3 border border-slate-800/50 hover:border-slate-700/50 transition-colors group cursor-pointer flex items-center gap-3">
          <div className="w-9 h-9 rounded-full bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center text-white font-bold text-sm shadow-md">
            FJ
          </div>
          <div className="flex-1 min-w-0">
            <div className="text-sm font-medium text-slate-200 truncate group-hover:text-cyan-400 transition-colors">Fahri Hilm</div>
            <div className="text-xs text-slate-500 truncate font-mono">Administrator</div>
          </div>
          <Settings className="w-4 h-4 text-slate-500 group-hover:text-slate-300 transition-colors" />
        </div>
      </div>
    </div>
  );
}
