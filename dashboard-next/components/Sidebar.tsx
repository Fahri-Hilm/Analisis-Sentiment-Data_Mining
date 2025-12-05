"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, MessageSquare, BarChart3, Database, Settings, FileText, Activity } from "lucide-react";

export function Sidebar() {
  const pathname = usePathname();

  const menuItems = [
    { href: "/", icon: LayoutDashboard, label: "Dashboard" },
    { href: "/comments", icon: MessageSquare, label: "Comments" },
    { href: "/analytics", icon: BarChart3, label: "Analytics" },
    { href: "/dataset", icon: Database, label: "Dataset" },
    { href: "/settings", icon: Settings, label: "Model Settings" },
    { href: "/docs", icon: FileText, label: "Documentation" },
  ];

  return (
    <div className="w-72 bg-[#0f172a] border-r border-gray-800 p-6 flex flex-col h-screen">
      <Link href="/" className="flex items-center gap-3 mb-10 px-2">
        <div className="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-900/20">
          <Activity className="w-6 h-6 text-white" />
        </div>
        <div className="flex flex-col">
          <span className="font-bold text-xl tracking-tight text-white">ANALYSIS</span>
          <span className="text-[10px] text-gray-400 uppercase tracking-widest font-medium">Dashboard</span>
        </div>
      </Link>

      <nav className="space-y-2 flex-1">
        {menuItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link key={item.href} href={item.href} className={`flex items-center gap-3 px-4 py-3.5 rounded-xl transition-all duration-200 group ${isActive ? "bg-blue-600 text-white shadow-md shadow-blue-900/20" : "text-gray-400 hover:bg-gray-800/50 hover:text-gray-200"}`}>
              <item.icon className={`w-5 h-5 ${isActive ? "text-white" : "text-gray-500 group-hover:text-gray-300"}`} />
              <span className="font-medium text-sm tracking-wide">{item.label}</span>
            </Link>
          );
        })}
      </nav>

      <div className="mt-auto">
        <div className="bg-gradient-to-br from-gray-800/50 to-gray-900/50 rounded-2xl p-5 border border-gray-700/50 shadow-xl backdrop-blur-sm">
            <div className="flex items-center gap-3 mb-4">
                <div className="p-2.5 bg-blue-500/10 rounded-lg border border-blue-500/20">
                    <FileText className="w-5 h-5 text-blue-400" />
                </div>
                <div>
                    <div className="text-sm font-semibold text-white">Need help?</div>
                    <div className="text-xs text-gray-400">Check documentation</div>
                </div>
            </div>
            <Link href="/docs" className="block w-full bg-blue-600 hover:bg-blue-500 text-white rounded-lg py-2.5 text-xs font-bold text-center transition-colors uppercase tracking-wider shadow-lg shadow-blue-900/20">
                View Docs
            </Link>
        </div>
      </div>
    </div>
  );
}
