"use client";

import { useEffect, useState } from "react";
import { Sparkles, Bot, RefreshCw } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface AIInsightsProps {
    stats: any;
    loading: boolean;
}

export function AIInsights({ stats, loading }: AIInsightsProps) {
    const [insight, setInsight] = useState("");
    const [displayedText, setDisplayedText] = useState("");
    const [isTyping, setIsTyping] = useState(false);
    const [key, setKey] = useState(0); // To force re-animation

    // Generate insight text based on stats
    useEffect(() => {
        if (loading || !stats) return;

        const generateInsight = () => {
            const negative = parseFloat(stats.negativePercent);
            const positive = parseFloat(stats.positivePercent);
            const total = stats.total.toLocaleString();
            const dominantEmotion = stats.topEmotions?.[0]?.name || "unknown";

            let text = `Menganalisis ${total} data komentar... `;

            if (negative > 60) {
                text += `Terdeteksi gelombang sentimen negatif yang signifikan (${negative}%). Dominasi emosi "${dominantEmotion}" menunjukkan ketidakpuasan publik yang mendalam. Isu utama tampaknya berpusat pada performa tim dan keputusan manajemen. Disarankan untuk segera merespons dengan transparansi.`;
            } else if (positive > 60) {
                text += `Sentimen positif mendominasi (${positive}%)! Publik sangat antusias dan mendukung langkah saat ini. Emosi "${dominantEmotion}" menjadi pendorong utama. Momentum ini sangat baik untuk mengebangkan inisiatif baru.`;
            } else {
                text += `Opini publik terbelah (Polarisasi seimbang). Sentimen negatif (${negative}%) dan positif (${positive}%) hampir setara. Kunci utamanya adalah mengelola narasi agar tidak condong ke arah negatif.`;
            }

            return text;
        };

        const newInsight = generateInsight();
        setInsight(newInsight);
        setDisplayedText("");
        setIsTyping(true);
        setKey((prev) => prev + 1);
    }, [stats, loading]);

    // Typing effect
    useEffect(() => {
        if (!isTyping || !insight) return;

        let currentIndex = 0;
        const interval = setInterval(() => {
            if (currentIndex < insight.length) {
                setDisplayedText(insight.slice(0, currentIndex + 1));
                currentIndex++;
            } else {
                setIsTyping(false);
                clearInterval(interval);
            }
        }, 20); // Typing speed

        return () => clearInterval(interval);
    }, [insight, key, isTyping]);

    if (loading) return null;

    return (
        <div className="glass-card rounded-2xl p-1 border border-blue-500/30 bg-gradient-to-br from-blue-500/5 to-purple-500/5 mb-8 relative overflow-hidden group">
            {/* Animated Border Gradient */}
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-blue-500/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000 pointer-events-none" />

            <div className="bg-[#020617]/80 backdrop-blur-xl rounded-xl p-6 relative z-10">
                <div className="flex items-start gap-4">
                    <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center shadow-lg shadow-blue-500/20 shrink-0">
                        <Bot className="w-6 h-6 text-white" />
                    </div>

                    <div className="flex-1">
                        <div className="flex items-center justify-between mb-2">
                            <h3 className="text-lg font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400 flex items-center gap-2">
                                AI Analysis <Sparkles className="w-4 h-4 text-purple-400 animate-pulse" />
                            </h3>
                            {isTyping && (
                                <div className="flex items-center gap-2 text-xs text-blue-400 font-mono animate-pulse">
                                    <RefreshCw className="w-3 h-3 animate-spin" />
                                    Generating insights...
                                </div>
                            )}
                        </div>

                        <p className="text-slate-200 leading-relaxed font-light text-lg min-h-[3.5rem]">
                            {displayedText}
                            {isTyping && <span className="inline-block w-2 h-5 bg-blue-400 ml-1 animate-blink align-middle"></span>}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}
