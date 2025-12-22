"use client";

import { useState, useEffect } from "react";
import { MessageSquare, User, ThumbsUp, Calendar, RefreshCw } from "lucide-react";

interface RealComment {
  id: string;
  author: string;
  text: string;
  sentiment: string;
  emotion: string;
  confidence: number;
  timestamp: Date;
  like_count: number;
}

export function DatasetComments() {
  const [comments, setComments] = useState<RealComment[]>([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState<any>(null);

  const fetchComments = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/real-comments?limit=20');
      const data = await response.json();
      setComments(data.comments || []);
      setStats(data.stats);
    } catch (error) {
      console.error('Error fetching real comments:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchComments();
  }, []);

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'positive': return 'text-green-400 bg-green-500/10';
      case 'negative': return 'text-red-400 bg-red-500/10';
      default: return 'text-slate-400 bg-slate-500/10';
    }
  };

  const getSentimentIcon = (sentiment: string) => {
    switch (sentiment) {
      case 'positive': return '😊';
      case 'negative': return '😞';
      default: return '😐';
    }
  };

  return (
    <div className="glass-card rounded-2xl p-8 border border-slate-800/50 relative z-10">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold flex items-center gap-2 text-slate-200">
          <MessageSquare className="w-5 h-5 text-blue-400" />
          Dataset Comments ({comments.length})
        </h3>
        <button
          onClick={fetchComments}
          disabled={loading}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-500 disabled:bg-blue-800 text-white rounded-lg transition-colors text-sm"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          Refresh
        </button>
      </div>

      {stats && (
        <div className="grid grid-cols-3 gap-4 mb-6">
          <div className="bg-green-500/10 rounded-lg p-3 border border-green-500/20">
            <div className="text-green-400 text-sm font-medium">Positive</div>
            <div className="text-green-300 text-lg font-bold">{stats.positive}</div>
          </div>
          <div className="bg-red-500/10 rounded-lg p-3 border border-red-500/20">
            <div className="text-red-400 text-sm font-medium">Negative</div>
            <div className="text-red-300 text-lg font-bold">{stats.negative}</div>
          </div>
          <div className="bg-slate-500/10 rounded-lg p-3 border border-slate-500/20">
            <div className="text-slate-400 text-sm font-medium">Neutral</div>
            <div className="text-slate-300 text-lg font-bold">{stats.neutral}</div>
          </div>
        </div>
      )}

      {loading ? (
        <div className="space-y-4">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="bg-slate-800/30 rounded-lg p-4 animate-pulse">
              <div className="h-4 bg-slate-700 rounded w-3/4 mb-2"></div>
              <div className="h-3 bg-slate-700 rounded w-1/2"></div>
            </div>
          ))}
        </div>
      ) : (
        <div className="space-y-4 max-h-96 overflow-y-auto">
          {comments.map((comment) => (
            <div key={comment.id} className="bg-slate-800/30 rounded-lg p-4 border border-slate-700/50 hover:border-slate-600/50 transition-colors">
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center gap-2">
                  <User className="w-4 h-4 text-slate-400" />
                  <span className="text-sm text-slate-300 font-medium">{comment.author}</span>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSentimentColor(comment.sentiment)}`}>
                    {getSentimentIcon(comment.sentiment)} {comment.sentiment}
                  </span>
                </div>
                <div className="flex items-center gap-2 text-xs text-slate-500">
                  <ThumbsUp className="w-3 h-3" />
                  {comment.like_count}
                </div>
              </div>
              
              <p className="text-slate-200 text-sm mb-2 leading-relaxed">
                {comment.text}
              </p>
              
              <div className="flex items-center justify-between text-xs text-slate-500">
                <div className="flex items-center gap-4">
                  <span>Emotion: {comment.emotion}</span>
                  <span>Confidence: {(comment.confidence * 100).toFixed(1)}%</span>
                </div>
                <div className="flex items-center gap-1">
                  <Calendar className="w-3 h-3" />
                  {new Date(comment.timestamp).toLocaleDateString('id-ID')}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
