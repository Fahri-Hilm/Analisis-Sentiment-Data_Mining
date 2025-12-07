import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        background: "#020617", // slate-950 (Deep Premium Dark)
        foreground: "#f8fafc", // slate-50
        primary: { DEFAULT: "#3b82f6", foreground: "#ffffff" }, // Blue-500
        secondary: { DEFAULT: "#64748b", foreground: "#ffffff" }, // Slate-500
        muted: { DEFAULT: "#1e293b", foreground: "#94a3b8" }, // Slate-800
        accent: { DEFAULT: "#06b6d4", foreground: "#ffffff" }, // Cyan-500
        card: { DEFAULT: "rgba(30, 41, 59, 0.7)", foreground: "#f8fafc" }, // Glassy Slate-800
      },
      animation: {
        "pulse-slow": "pulse-slow 3s ease-in-out infinite",
        "shimmer": "shimmer 1.5s infinite",
        "blink": "blink 1s step-end infinite",
        "float": "float 6s ease-in-out infinite",
        "glow": "glow 2s ease-in-out infinite alternate",
        "gradient-x": "gradient-x 3s ease infinite",
        "spin-slow": "spin 8s linear infinite",
      },
      keyframes: {
        "pulse-slow": {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.7" },
        },
        "shimmer": {
          "0%": { backgroundPosition: "200% 0" },
          "100%": { backgroundPosition: "-200% 0" },
        },
        "blink": {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0" },
        },
        "float": {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-10px)" },
        },
        "glow": {
          "from": { boxShadow: "0 0 10px rgba(59, 130, 246, 0.5), 0 0 20px rgba(59, 130, 246, 0.3)" },
          "to": { boxShadow: "0 0 20px rgba(59, 130, 246, 0.8), 0 0 40px rgba(59, 130, 246, 0.5)" },
        },
        "gradient-x": {
          "0%, 100%": { backgroundPosition: "0% 50%" },
          "50%": { backgroundPosition: "100% 50%" },
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
        mono: ["var(--font-mono)", "monospace"], // Add variable font
      },
    },
  },
  plugins: [],
};
export default config;
