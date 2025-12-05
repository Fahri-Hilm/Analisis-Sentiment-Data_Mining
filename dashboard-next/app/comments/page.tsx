"use client";

import { useState, useEffect } from "react";
import { ThumbsUp, ThumbsDown, Minus, Send, Loader, MessageSquare, Search } from "lucide-react";
import { Sidebar } from "@/components/Sidebar";

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
    if (s === "positive") return "border-green-500/30 bg-green-500/5";
    if (s === "negative") return "border-red-500/30 bg-red-500/5";
    return "border-gray-500/30 bg-gray-500/5";
  };

  return (
    <div className="flex h-screen bg-[#0a1628] text-white overflow-hidden">
      <Sidebar />
      <div className="flex-1 overflow-y-auto p-6">
        <div className="mb-6">
          <h1 className="text-2xl font-bold flex items-center gap-2">
            <MessageSquare className="w-6 h-6 text-blue-400" />Suara Netizen: Komentar Langsung
          </h1>
          <p className="text-sm text-gray-400 mt-1">Pantau dan analisis komentar publik secara real-time</p>
        </div>

        <div className="bg-[#111c2e] rounded-xl p-4 border border-gray-800 mb-6">
          <h2 className="text-lg font-semibold mb-4">Real-time Analyzer</h2>
          <div className="flex gap-3">
            <input type="text" value={inputText} onChange={(e) => setInputText(e.target.value)} onKeyDown={(e) => e.key === "Enter" && handleAnalyze()} placeholder="Ketik komentar untuk dianalisis..." className="flex-1 bg-[#0a1628] border border-gray-700 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500" />
            <button onClick={handleAnalyze} disabled={analyzing || !inputText.trim()} className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 rounded-lg flex items-center gap-2">
              {analyzing ? <Loader className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}Analyze
            </button>
          </div>
          {result && (
            <div className={`mt-4 p-4 rounded-lg border ${getColor(result.sentiment)}`}>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">{getIcon(result.sentiment)}<span className="font-semibold capitalize">{result.sentiment}</span><span className="text-gray-400 text-sm">• {result.emotion}</span></div>
                <span className="text-lg font-bold">{result.score}%</span>
              </div>
            </div>
          )}
        </div>

        <div className="bg-[#111c2e] rounded-xl p-4 border border-gray-800">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold">Dataset Comments ({filteredComments.length})</h2>
            <div className="flex gap-2">
              <div className="relative">
                <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
                <input type="text" value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} placeholder="Search..." className="bg-[#0a1628] border border-gray-700 rounded-lg pl-9 pr-4 py-2 text-sm focus:outline-none focus:border-blue-500" />
              </div>
              <select value={filter} onChange={(e) => setFilter(e.target.value)} className="bg-[#0a1628] border border-gray-700 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-500">
                <option value="all">All</option>
                <option value="positive">Positive</option>
                <option value="negative">Negative</option>
                <option value="neutral">Neutral</option>
              </select>
            </div>
          </div>
          {loading ? (<div className="text-center py-8 text-gray-400">Loading comments...</div>) : (
            <div className="space-y-2 max-h-[500px] overflow-y-auto">
              {filteredComments.slice(0, 50).map((comment) => (
                <div key={comment.id} className={`p-3 rounded-lg border ${getColor(comment.sentiment)}`}>
                  <div className="flex items-start gap-3">
                    {getIcon(comment.sentiment)}
                    <div className="flex-1 min-w-0">
                      <p className="text-sm text-gray-200 break-words">{comment.text}</p>
                      <div className="flex gap-2 mt-1"><span className="text-xs text-gray-500 capitalize">{comment.sentiment}</span>{comment.emotion && <span className="text-xs text-gray-500">• {comment.emotion}</span>}</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
