import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        background: "#0f172a", // Elegant slate-900
        foreground: "#f1f5f9", // slate-100
        primary: { 
          DEFAULT: "#3b82f6", // Blue-500
          foreground: "#ffffff",
          light: "#60a5fa", // Blue-400
          dark: "#2563eb", // Blue-600
        },
        secondary: { 
          DEFAULT: "#64748b", // Slate-500
          foreground: "#ffffff" 
        },
        muted: { 
          DEFAULT: "#1e293b", // Slate-800
          foreground: "#94a3b8" // Slate-400
        },
        accent: { 
          DEFAULT: "#06b6d4", // Cyan-500
          foreground: "#ffffff" 
        },
        card: { 
          DEFAULT: "rgba(15, 23, 42, 0.6)", // Elegant glass
          foreground: "#f1f5f9" 
        },
        // Sentiment Colors - Elegant palette
        sentiment: {
          positive: "#10b981", // Emerald-500
          negative: "#ef4444", // Red-500
          neutral: "#6b7280", // Gray-500
        },
      },
      animation: {
        "fade-in": "fade-in 0.5s ease-out",
        "slide-up": "slide-up 0.5s ease-out",
        "scale-in": "scale-in 0.3s ease-out",
        "shimmer": "shimmer 2s ease-in-out infinite",
        "float": "float 6s ease-in-out infinite",
        "glow-pulse": "glow-pulse 2s ease-in-out infinite",
      },
      keyframes: {
        "fade-in": {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        "slide-up": {
          "0%": { transform: "translateY(20px)", opacity: "0" },
          "100%": { transform: "translateY(0)", opacity: "1" },
        },
        "scale-in": {
          "0%": { transform: "scale(0.95)", opacity: "0" },
          "100%": { transform: "scale(1)", opacity: "1" },
        },
        "shimmer": {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.5" },
        },
        "float": {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-10px)" },
        },
        "glow-pulse": {
          "0%, 100%": { 
            boxShadow: "0 0 20px rgba(59, 130, 246, 0.3)" 
          },
          "50%": { 
            boxShadow: "0 0 30px rgba(59, 130, 246, 0.5)" 
          },
        },
      },
      container: {
        center: true,
        padding: "2rem",
        screens: {
          "2xl": "1400px",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      spacing: {
        "18": "4.5rem",
        "88": "22rem",
      },
      borderRadius: {
        "2xl": "1rem",
        "3xl": "1.5rem",
      },
    },
  },
  plugins: [],
};
export default config;
