"use client";

import { useEffect, useState, useRef } from "react";

interface AnimatedProgressBarProps {
  value: number;
  label: string;
  color?: "green" | "blue" | "purple" | "red" | "yellow";
  showGlow?: boolean;
}

export function AnimatedProgressBar({ 
  value, 
  label, 
  color = "green",
  showGlow = true 
}: AnimatedProgressBarProps) {
  const [width, setWidth] = useState(0);
  const [isVisible, setIsVisible] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  const colorClasses = {
    green: {
      bar: "bg-gradient-to-r from-green-500 to-emerald-400",
      text: "text-green-400",
      glow: "shadow-green-500/50",
    },
    blue: {
      bar: "bg-gradient-to-r from-blue-500 to-cyan-400",
      text: "text-blue-400",
      glow: "shadow-blue-500/50",
    },
    purple: {
      bar: "bg-gradient-to-r from-purple-500 to-pink-400",
      text: "text-purple-400",
      glow: "shadow-purple-500/50",
    },
    red: {
      bar: "bg-gradient-to-r from-red-500 to-orange-400",
      text: "text-red-400",
      glow: "shadow-red-500/50",
    },
    yellow: {
      bar: "bg-gradient-to-r from-yellow-500 to-amber-400",
      text: "text-yellow-400",
      glow: "shadow-yellow-500/50",
    },
  };

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          observer.unobserve(entry.target);
        }
      },
      { threshold: 0.3 }
    );

    if (ref.current) {
      observer.observe(ref.current);
    }

    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    if (isVisible) {
      const timer = setTimeout(() => setWidth(value), 100);
      return () => clearTimeout(timer);
    }
  }, [isVisible, value]);

  return (
    <div ref={ref}>
      <div className="flex justify-between mb-1">
        <span className="text-gray-400">{label}</span>
        <span className={`${colorClasses[color].text} font-medium`}>
          {value.toFixed(1)}%
        </span>
      </div>
      <div className="w-full bg-[#0f1c2e] rounded-full h-2.5 overflow-hidden">
        <div
          className={`h-2.5 rounded-full ${colorClasses[color].bar} ${showGlow ? `shadow-lg ${colorClasses[color].glow}` : ""}`}
          style={{
            width: `${width}%`,
            transition: "width 1.5s cubic-bezier(0.4, 0, 0.2, 1)",
          }}
        />
      </div>
    </div>
  );
}

export default AnimatedProgressBar;
