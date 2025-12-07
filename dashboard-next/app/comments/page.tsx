"use client";

import { useState, useEffect } from "react";
import { ThumbsUp, ThumbsDown, Minus, Send, Loader, MessageSquare, Search } from "lucide-react";


interface Comment {
  id: number;
  text: string;
  sentiment: string;
  emotion?: string;
}

const detectSentiment = (text: string) => {
  const lower = text.toLowerCase();
  let sentiment = "neutral";
  let score = 75;
  let emotion = "Netral";

  const negWords = ["gagal", "buruk", "jelek", "kecewa", "sedih", "lemah", "payah", "hancur", "pecat", "out", "mundur", "kalah", "malu", "bobrok", "evaluasi", "emosi", "nangis", "bego", "tolol", "ancur"];
  const posWords = ["bagus", "hebat", "semangat", "optimis", "harapan", "bisa", "maju", "keren", "bangga", "garuda", "terbang", "percaya", "proses", "dukung", "cinta", "salut", "top"];

  const negCount = negWords.filter(w => lower.includes(w)).length;
  const posCount = posWords.filter(w => lower.includes(w)).length;

  if (negCount > posCount) {
    sentiment = "negative";
    score = Math.min(85 + negCount * 3, 98);
    emotion = "Kekecewaan";
  } else if (posCount > negCount) {
    sentiment = "positive";
    score = Math.min(85 + posCount * 3, 98);
    emotion = "Harapan";
  }
  return { sentiment, score, emotion };
};

export default function CommentsPage() {
  const [comments, setComments] = useState<Comment[]>([]);
  const [loading, setLoading] = useState(true);
  const [inputText, setInputText] = useState("");
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState<{ sentiment: string; score: number; emotion: string } | null>(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [filter, setFilter] = useState("all");

  useEffect(() => {
    fetch("/api/comments")
      .then((res) => res.json())
      .then((data) => { setComments(data.comments || []); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  const handleAnalyze = () => {
    if (!inputText.trim()) return;
    setAnalyzing(true);
    setTimeout(() => { setResult(detectSentiment(inputText)); setAnalyzing(false); }, 500);
  };

  const filteredComments = comments.filter((c) => {
    const matchSearch = c.text.toLowerCase().includes(searchTerm.toLowerCase());
    const matchFilter = filter === "all" || c.sentiment === filter;
    return matchSearch && matchFilter;
  });

  const getIcon = (s: string) => {
    if (s === "positive") return <ThumbsUp className="w-4 h-4 text-green-400" />;
    if (s === "negative") return <ThumbsDown className="w-4 h-4 text-red-400" />;
    return <Minus className="w-4 h-4 text-gray-400" />;
  };

  const getColor = (s: string) => {
    if (s === "positive") return "border-green-500/20 bg-green-500/5 shadow-[0_0_15px_-5px_rgba(34,197,94,0.1)]";
    if (s === "negative") return "border-red-500/20 bg-red-500/5 shadow-[0_0_15px_-5px_rgba(239,68,68,0.1)]";
    return "border-slate-500/20 bg-slate-500/5";
  };

  return (
    <div className="max-w-7xl mx-auto p-8 relative">
      {/* Background Ambient Glow */}
      <div className="absolute top-0 right-0 w-full h-[500px] bg-purple-500/5 rounded-full blur-[100px] pointer-events-none -translate-y-1/2" />

      <div className="mb-10 relative z-10">
        <h1 className="text-4xl font-bold flex items-center gap-3 bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
          <MessageSquare className="w-8 h-8 text-blue-400" />Suara Netizen: Komentar Langsung
        </h1>
        <p className="text-slate-400 text-lg mt-2 font-light tracking-wide">Pantau dan analisis komentar publik secara real-time</p>
      </div>

      <div className="glass-card rounded-2xl p-6 border border-slate-800/50 mb-8 relative z-10">
        <h2 className="text-lg font-semibold mb-4 text-slate-200">Real-time Analyzer</h2>
        <div className="flex gap-3">
          <input type="text" value={inputText} onChange={(e) => setInputText(e.target.value)} onKeyDown={(e) => e.key === "Enter" && handleAnalyze()} placeholder="Ketik komentar untuk dianalisis..." className="flex-1 bg-slate-900/50 border border-slate-700/50 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all" />
          <button onClick={handleAnalyze} disabled={analyzing || !inputText.trim()} className="px-6 py-3 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 disabled:cursor-not-allowed text-white rounded-xl flex items-center gap-2 font-medium transition-all shadow-lg shadow-blue-900/20">
            {analyzing ? <Loader className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}Analyze
          </button>
        </div>
        {result && (
          <div className={`mt-6 p-4 rounded-xl border backdrop-blur-sm animate-in fade-in slide-in-from-top-2 duration-300 ${getColor(result.sentiment)}`}>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">{getIcon(result.sentiment)}<span className="font-semibold capitalize text-lg">{result.sentiment}</span><span className="text-slate-400 text-sm border-l border-slate-700 pl-3 ml-1">{result.emotion}</span></div>
              <div className="flex items-center gap-2">
                <span className="text-xs text-slate-400 uppercase tracking-wider font-medium">Confidence</span>
                <span className="text-lg font-bold">{result.score}%</span>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="glass-card rounded-2xl p-6 border border-slate-800/50 relative z-10">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-semibold text-slate-200 flex items-center gap-2"><Search className="w-5 h-5 text-slate-400" />Dataset Comments ({filteredComments.length})</h2>
          <div className="flex gap-3">
            <div className="relative">
              <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
              <input type="text" value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} placeholder="Search..." className="bg-slate-900/50 border border-slate-700/50 rounded-xl pl-9 pr-4 py-2 text-sm text-white focus:outline-none focus:border-blue-500 w-64 transition-all" />
            </div>
            <select value={filter} onChange={(e) => setFilter(e.target.value)} className="bg-slate-900/50 border border-slate-700/50 rounded-xl px-4 py-2 text-sm text-slate-300 focus:outline-none focus:border-blue-500 transition-all cursor-pointer">
              <option value="all">All Sentiments</option>
              <option value="positive">Positive Only</option>
              <option value="negative">Negative Only</option>
              <option value="neutral">Neutral Only</option>
            </select>
          </div>
        </div>
        {loading ? (<div className="text-center py-12 text-slate-500 animate-pulse">Loading comments dataset...</div>) : (
          <div className="space-y-3 max-h-[600px] overflow-y-auto pr-2 custom-scrollbar">
            {filteredComments.slice(0, 50).map((comment) => (
              <div key={comment.id} className={`p-4 rounded-xl border transition-all hover:bg-slate-900/30 ${getColor(comment.sentiment)}`}>
                <div className="flex items-start gap-4">
                  <div className="mt-1">{getIcon(comment.sentiment)}</div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-slate-200 leading-relaxed font-light">{comment.text}</p>
                    <div className="flex gap-3 mt-3 items-center">
                      <span className={`text-xs font-medium px-2 py-0.5 rounded-full uppercase tracking-wider border ${comment.sentiment === 'positive' ? 'bg-green-500/10 text-green-400 border-green-500/20' : comment.sentiment === 'negative' ? 'bg-red-500/10 text-red-400 border-red-500/20' : 'bg-slate-500/10 text-slate-400 border-slate-500/20'}`}>{comment.sentiment}</span>
                      {comment.emotion && <span className="text-xs text-slate-500 font-medium">• {comment.emotion}</span>}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
