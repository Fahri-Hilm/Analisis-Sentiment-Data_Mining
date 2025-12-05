"use client";

import { useState } from "react";
import { Plus, X, Home, FileText, BarChart3, Settings, RefreshCw, Download } from "lucide-react";
import Link from "next/link";

interface FABItem {
  icon: React.ReactNode;
  label: string;
  href?: string;
  onClick?: () => void;
  color: string;
}

export function FloatingActionButton() {
  const [isOpen, setIsOpen] = useState(false);

  const items: FABItem[] = [
    { icon: <Home className="w-4 h-4" />, label: "Dashboard", href: "/", color: "bg-blue-500 hover:bg-blue-600" },
    { icon: <FileText className="w-4 h-4" />, label: "Documentation", href: "/docs", color: "bg-purple-500 hover:bg-purple-600" },
    { icon: <BarChart3 className="w-4 h-4" />, label: "Comments", href: "/comments", color: "bg-green-500 hover:bg-green-600" },
    { icon: <RefreshCw className="w-4 h-4" />, label: "Refresh Data", onClick: () => window.location.reload(), color: "bg-yellow-500 hover:bg-yellow-600" },
    { icon: <Download className="w-4 h-4" />, label: "Export", onClick: () => alert("Export feature coming soon!"), color: "bg-cyan-500 hover:bg-cyan-600" },
  ];

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {/* Menu Items */}
      <div className={`absolute bottom-16 right-0 flex flex-col gap-3 transition-all duration-300 ${isOpen ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4 pointer-events-none"}`}>
        {items.map((item, index) => (
          <div
            key={index}
            className="flex items-center gap-3 justify-end"
            style={{ transitionDelay: `${index * 50}ms` }}
          >
            <span className="px-3 py-1.5 bg-gray-800 text-white text-sm rounded-lg shadow-lg whitespace-nowrap">
              {item.label}
            </span>
            {item.href ? (
              <Link
                href={item.href}
                className={`w-10 h-10 rounded-full ${item.color} flex items-center justify-center text-white shadow-lg transition-all duration-200 hover:scale-110`}
              >
                {item.icon}
              </Link>
            ) : (
              <button
                onClick={item.onClick}
                className={`w-10 h-10 rounded-full ${item.color} flex items-center justify-center text-white shadow-lg transition-all duration-200 hover:scale-110`}
              >
                {item.icon}
              </button>
            )}
          </div>
        ))}
      </div>

      {/* Main FAB Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`w-14 h-14 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center text-white shadow-xl transition-all duration-300 hover:scale-110 hover:shadow-2xl hover:shadow-blue-500/30 ${isOpen ? "rotate-45" : ""}`}
      >
        {isOpen ? <X className="w-6 h-6" /> : <Plus className="w-6 h-6" />}
      </button>

      {/* Pulse ring effect */}
      {!isOpen && (
        <div className="absolute inset-0 rounded-full bg-blue-500 animate-ping opacity-20 pointer-events-none"></div>
      )}
    </div>
  );
}
