"use client";

import { LayoutDashboard, Table, CreditCard, Wrench, User, LogIn, UserPlus } from "lucide-react";

export function Sidebar() {
  return (
    <div className="w-64 bg-gradient-to-b from-[#1a2942] to-[#0f1c2e] p-6 flex flex-col">
      <div className="flex items-center gap-2 mb-8">
        <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center">
          <span className="text-white font-bold">S</span>
        </div>
        <span className="font-bold text-lg">SENTIMENT AI</span>
      </div>

      <nav className="space-y-2 flex-1">
        <a href="#" className="flex items-center gap-3 px-4 py-3 rounded-lg bg-blue-500/20 text-blue-400">
          <LayoutDashboard className="w-5 h-5" />
          <span>Dashboard</span>
        </a>
        <a href="#" className="flex items-center gap-3 px-4 py-3 rounded-lg text-gray-400 hover:bg-white/5">
          <Table className="w-5 h-5" />
          <span>Tables</span>
        </a>
        <a href="#" className="flex items-center gap-3 px-4 py-3 rounded-lg text-gray-400 hover:bg-white/5">
          <CreditCard className="w-5 h-5" />
          <span>Billing</span>
        </a>
        <a href="#" className="flex items-center gap-3 px-4 py-3 rounded-lg text-gray-400 hover:bg-white/5">
          <Wrench className="w-5 h-5" />
          <span>RTL</span>
        </a>

        <div className="pt-6">
          <div className="text-xs text-gray-500 mb-2 px-4">ACCOUNT PAGES</div>
          <a href="#" className="flex items-center gap-3 px-4 py-3 rounded-lg text-gray-400 hover:bg-white/5">
            <User className="w-5 h-5" />
            <span>Profile</span>
          </a>
          <a href="#" className="flex items-center gap-3 px-4 py-3 rounded-lg text-gray-400 hover:bg-white/5">
            <LogIn className="w-5 h-5" />
            <span>Sign In</span>
          </a>
          <a href="#" className="flex items-center gap-3 px-4 py-3 rounded-lg text-gray-400 hover:bg-white/5">
            <UserPlus className="w-5 h-5" />
            <span>Sign Up</span>
          </a>
        </div>
      </nav>

      <div className="mt-auto bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl p-4">
        <div className="text-sm font-semibold mb-2">Need help?</div>
        <div className="text-xs text-gray-200 mb-3">Check our docs</div>
        <button className="w-full bg-white text-gray-900 rounded-lg py-2 text-sm font-semibold">DOCUMENTATION</button>
      </div>
    </div>
  );
}
