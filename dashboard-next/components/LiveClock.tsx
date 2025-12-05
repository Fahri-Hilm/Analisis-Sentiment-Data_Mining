"use client";

import { useState, useEffect } from "react";
import { Clock, Calendar } from "lucide-react";

export function LiveClock() {
  const [time, setTime] = useState(new Date());
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
    const timer = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  if (!isClient) return null;

  const hours = time.getHours().toString().padStart(2, "0");
  const minutes = time.getMinutes().toString().padStart(2, "0");
  const seconds = time.getSeconds().toString().padStart(2, "0");
  
  const days = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"];
  const months = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"];
  
  const dayName = days[time.getDay()];
  const date = time.getDate();
  const month = months[time.getMonth()];
  const year = time.getFullYear();

  return (
    <div className="flex items-center gap-4 px-4 py-2 bg-gradient-to-r from-[#1a2942]/80 to-[#0f1c2e]/80 backdrop-blur-md rounded-xl border border-blue-500/20">
      {/* Time */}
      <div className="flex items-center gap-2">
        <Clock className="w-4 h-4 text-blue-400 animate-pulse" />
        <div className="flex items-center font-mono">
          <span className="text-lg font-bold text-white">{hours}</span>
          <span className="text-lg font-bold text-blue-400 animate-pulse">:</span>
          <span className="text-lg font-bold text-white">{minutes}</span>
          <span className="text-lg font-bold text-blue-400 animate-pulse">:</span>
          <span className="text-lg font-bold text-cyan-400">{seconds}</span>
        </div>
      </div>
      
      {/* Divider */}
      <div className="h-6 w-px bg-gray-600"></div>
      
      {/* Date */}
      <div className="flex items-center gap-2">
        <Calendar className="w-4 h-4 text-purple-400" />
        <span className="text-sm text-gray-300">
          {dayName}, {date} {month} {year}
        </span>
      </div>
    </div>
  );
}
