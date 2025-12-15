"use client";

import { useState, useEffect } from 'react';
import { MessageSquare, Activity, User, Clock, TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface Comment {
  id: string;
  author: string;
  text: string;
  sentiment: 'positive' | 'negative' | 'neutral';
  confidence: number;
  timestamp: Date;
  emotion?: string;
}

interface LiveCommentsProps {
  isStreaming?: boolean;
  maxComments?: number;
}

export function LiveComments({ isStreaming = false, maxComments = 50 }: LiveCommentsProps) {
  const [comments, setComments] = useState<Comment[]>([]);
  const [stats, setStats] = useState({
    total: 0,
    positive: 0,
    negative: 0,
    neutral: 0
  });

  // Sample comments for demo
  const sampleComments = [
    { text: "Timnas Indonesia harus lebih baik lagi", sentiment: 'negative' as const, emotion: 'Kekecewaan' },
    { text: "Tetap semangat Garuda! Pasti bisa!", sentiment: 'positive' as const, emotion: 'Dukungan' },
    { text: "Pelatih perlu strategi baru", sentiment: 'neutral' as const, emotion: 'Saran' },
    { text: "Kualitas pemain masih kurang", sentiment: 'negative' as const, emotion: 'Kritik' },
    { text: "Bangga dengan perjuangan tim", sentiment: 'positive' as const, emotion: 'Kebanggaan' },
    { text: "Semoga lolos Piala Dunia", sentiment: 'positive' as const, emotion: 'Harapan' },
    { text: "Performa hari ini mengecewakan", sentiment: 'negative' as const, emotion: 'Kekecewaan' },
    { text: "Indonesia pasti bisa bangkit", sentiment: 'positive' as const, emotion: 'Optimisme' }
  ];

  // Fetch real comments from dataset
  const fetchRealComments = async () => {
    try {
      const response = await fetch(`/api/real-comments?limit=${maxComments}`);
      const data = await response.json();
      
      if (data.comments && data.comments.length > 0) {
        const realComments = data.comments.map((comment: any) => ({
          id: comment.id,
          author: comment.author,
          text: comment.text,
          sentiment: comment.sentiment,
          confidence: comment.confidence,
          timestamp: new Date(comment.timestamp),
          emotion: comment.emotion
        }));
        
        setComments(realComments);
        setStats(data.stats);
      }
    } catch (error) {
      console.error('Error fetching real comments:', error);
      // Fallback to sample data if API fails
      setComments([]);
    }
  };

  // Simulate live streaming with real data rotation
  useEffect(() => {
    if (!isStreaming) return;

    // Initial fetch
    fetchRealComments();

    // Refresh with new random sample every 15 seconds
    const interval = setInterval(fetchRealComments, 15000);
    
    return () => clearInterval(interval);
  }, [isStreaming, maxComments]);

  const getSentimentIcon = (sentiment: string) => {
    switch (sentiment) {
      case 'positive': return <TrendingUp className="w-4 h-4" />;
      case 'negative': return <TrendingDown className="w-4 h-4" />;
      default: return <Minus className="w-4 h-4" />;
    }
  };

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'positive': return 'bg-green-500/20 text-green-400 border-green-500/30';
      case 'negative': return 'bg-red-500/20 text-red-400 border-red-500/30';
      default: return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
    }
  };

  const formatTimeAgo = (timestamp: Date) => {
    const seconds = Math.floor((new Date().getTime() - timestamp.getTime()) / 1000);
    if (seconds < 60) return `${seconds}s ago`;
    const minutes = Math.floor(seconds / 60);
    if (minutes < 60) return `${minutes}m ago`;
    const hours = Math.floor(minutes / 60);
    return `${hours}h ago`;
  };

  return (
    <div className="glass-card rounded-2xl p-6 border border-slate-800/50 bg-slate-900/20 backdrop-blur-xl h-[600px] flex flex-col">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-semibold text-white flex items-center gap-2">
          <MessageSquare className="w-5 h-5 text-cyan-400" />
          Live Comments Feed
          <span className="text-xs bg-green-500/20 text-green-400 px-2 py-1 rounded-full border border-green-500/30">
            REAL DATA
          </span>
        </h3>
        {isStreaming && (
          <div className="flex items-center gap-4 text-sm">
            <div className="flex items-center gap-1">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span className="text-green-400">{stats.positive}</span>
            </div>
            <div className="flex items-center gap-1">
              <div className="w-2 h-2 bg-red-500 rounded-full"></div>
              <span className="text-red-400">{stats.negative}</span>
            </div>
            <div className="flex items-center gap-1">
              <div className="w-2 h-2 bg-gray-500 rounded-full"></div>
              <span className="text-gray-400">{stats.neutral}</span>
            </div>
          </div>
        )}
      </div>
      
      <div className="flex-1 overflow-y-auto space-y-3">
        {!isStreaming ? (
          <div className="flex items-center justify-center h-full text-slate-400">
            <div className="text-center">
              <Activity className="w-12 h-12 mx-auto mb-4 opacity-50" />
              <p className="text-lg font-medium mb-2">Stream Offline</p>
              <p className="text-sm">Start streaming to see live comments and sentiment analysis</p>
            </div>
          </div>
        ) : comments.length === 0 ? (
          <div className="flex items-center justify-center h-full text-slate-400">
            <div className="text-center">
              <div className="w-8 h-8 border-2 border-cyan-500/30 border-t-cyan-500 rounded-full animate-spin mx-auto mb-4"></div>
              <p className="text-sm">Waiting for comments...</p>
            </div>
          </div>
        ) : (
          <div className="space-y-3">
            {comments.map((comment) => (
              <div 
                key={comment.id} 
                className="p-4 bg-slate-800/30 rounded-xl border border-slate-700/30 hover:bg-slate-800/50 transition-all duration-200 animate-in slide-in-from-top-2"
              >
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <User className="w-4 h-4 text-slate-400" />
                    <span className="text-sm font-medium text-slate-300">@{comment.author}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className={`px-2 py-1 rounded-full text-xs font-medium border flex items-center gap-1 ${getSentimentColor(comment.sentiment)}`}>
                      {getSentimentIcon(comment.sentiment)}
                      {comment.sentiment}
                    </div>
                    <div className="flex items-center gap-1 text-xs text-slate-500">
                      <Clock className="w-3 h-3" />
                      {formatTimeAgo(comment.timestamp)}
                    </div>
                  </div>
                </div>
                
                <p className="text-slate-200 mb-2">{comment.text}</p>
                
                <div className="flex items-center justify-between text-xs">
                  <div className="flex items-center gap-3">
                    {comment.emotion && (
                      <span className="text-slate-400">
                        Emotion: <span className="text-cyan-400">{comment.emotion}</span>
                      </span>
                    )}
                  </div>
                  <span className="text-slate-500">
                    Confidence: {(comment.confidence * 100).toFixed(1)}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {isStreaming && (
        <div className="mt-4 pt-4 border-t border-slate-700/50">
          <div className="flex items-center justify-between text-sm">
            <span className="text-slate-400">Total Comments: {stats.total}</span>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
              <span className="text-red-400 font-mono">LIVE</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
