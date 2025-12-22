"use client";

import { useState, useEffect } from "react";
import { RefreshCw, Youtube, User, Clock, ThumbsUp, Brain, Zap } from "lucide-react";

interface LiveComment {
  id: string;
  text: string;
  author: string;
  authorChannelId?: string;
  likeCount: number;
  publishedAt: string;
  updatedAt: string;
  isReal: boolean;
  sentiment?: string;
  confidence?: number;
  reasoning?: string;
  model?: string;
  relevanceScore?: number;
  filterReason?: string;
  layers?: {
    layer1?: any;
    layer2?: any;
    layer3?: any;
  };
  coverage?: number;
}

export default function LiveCommentsPage() {
  const [comments, setComments] = useState<LiveComment[]>([]);
  const [loading, setLoading] = useState(false);
  const [videoId, setVideoId] = useState("lDtSjKb_8Jo");
  const [lastUpdate, setLastUpdate] = useState<string>("");
  const [aiEnabled, setAiEnabled] = useState(true);
  const [filterEnabled, setFilterEnabled] = useState(true);
  const [maxComments, setMaxComments] = useState(200);
  const [totalFetched, setTotalFetched] = useState(0);

  const fetchLiveComments = async () => {
    setLoading(true);
    try {
      const url = `/api/live-comments?videoId=${videoId}&maxResults=${maxComments}${aiEnabled ? '&sentiment=true' : ''}${filterEnabled ? '&filter=true' : '&filter=false'}`;
      const response = await fetch(url);
      const data = await response.json();
      
      if (data.comments) {
        setComments(data.comments);
        setTotalFetched(data.totalFetched || data.total);
        setLastUpdate(new Date().toLocaleTimeString());
      }
    } catch (error) {
      console.error("Error fetching live comments:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLiveComments();
  }, [videoId, aiEnabled, filterEnabled, maxComments]);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('id-ID');
  };

  const getSentimentColor = (sentiment?: string) => {
    switch (sentiment) {
      case 'positive': return 'text-green-400 bg-green-500/10 border-green-500/20';
      case 'negative': return 'text-red-400 bg-red-500/10 border-red-500/20';
      case 'neutral': return 'text-yellow-400 bg-yellow-500/10 border-yellow-500/20';
      default: return 'text-slate-400 bg-slate-500/10 border-slate-500/20';
    }
  };

  const getSentimentIcon = (sentiment?: string) => {
    switch (sentiment) {
      case 'positive': return '😊';
      case 'negative': return '😞';
      case 'neutral': return '😐';
      default: return '🤔';
    }
  };

  return (
    <div className="max-w-7xl mx-auto p-8">
      <div className="mb-8">
        <h1 className="text-4xl font-bold flex items-center gap-3 bg-gradient-to-r from-red-400 to-red-600 bg-clip-text text-transparent">
          <Youtube className="w-8 h-8 text-red-500" />
          Live YouTube Comments
        </h1>
        <p className="text-slate-400 text-lg mt-2">Komentar real-time dengan analisis sentiment AI</p>
      </div>

      <div className="glass-card rounded-2xl p-6 border border-slate-800/50 mb-6">
        <div className="flex items-center gap-4 mb-4">
          <input
            type="text"
            value={videoId}
            onChange={(e) => setVideoId(e.target.value)}
            placeholder="YouTube Video ID"
            className="flex-1 bg-slate-900/50 border border-slate-700/50 rounded-xl px-4 py-3 text-white"
          />
          <select
            value={maxComments}
            onChange={(e) => setMaxComments(parseInt(e.target.value))}
            className="bg-slate-900/50 border border-slate-700/50 rounded-xl px-4 py-3 text-white"
          >
            <option value={100}>100 Comments</option>
            <option value={200}>200 Comments</option>
            <option value={500}>500 Comments</option>
            <option value={1000}>1000 Comments</option>
          </select>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <input
                type="checkbox"
                id="aiEnabled"
                checked={aiEnabled}
                onChange={(e) => setAiEnabled(e.target.checked)}
                className="w-4 h-4 text-blue-600 bg-slate-900 border-slate-600 rounded"
              />
              <label htmlFor="aiEnabled" className="text-sm text-slate-300 flex items-center gap-1">
                <Brain className="w-4 h-4 text-blue-400" />
                AI Analysis
              </label>
            </div>
            <div className="flex items-center gap-2">
              <input
                type="checkbox"
                id="filterEnabled"
                checked={filterEnabled}
                onChange={(e) => setFilterEnabled(e.target.checked)}
                className="w-4 h-4 text-green-600 bg-slate-900 border-slate-600 rounded"
              />
              <label htmlFor="filterEnabled" className="text-sm text-slate-300 flex items-center gap-1">
                <span className="text-green-400">🔍</span>
                Smart Filter
              </label>
            </div>
            <button
              onClick={fetchLiveComments}
              disabled={loading}
              className="px-6 py-3 bg-red-600 hover:bg-red-500 disabled:bg-slate-700 text-white rounded-xl flex items-center gap-2 transition-all"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              {loading ? 'Loading...' : 'Refresh'}
            </button>
          </div>
        </div>
        
        {lastUpdate && (
          <div className="flex items-center justify-between text-sm text-slate-400">
            <div className="flex items-center gap-4">
              <span>Last updated: {lastUpdate}</span>
              <span className="text-slate-500">•</span>
              <span className="text-green-400">{comments.length} relevant comments</span>
              {totalFetched > comments.length && (
                <>
                  <span className="text-slate-500">•</span>
                  <span className="text-slate-500">{totalFetched} total fetched</span>
                </>
              )}
            </div>
            <div className="flex items-center gap-4">
              {aiEnabled && (
                <span className="flex items-center gap-1 text-blue-400">
                  <Zap className="w-3 h-3" />
                  AI Analysis
                </span>
              )}
              {filterEnabled && (
                <span className="flex items-center gap-1 text-green-400">
                  🔍 Smart Filter
                </span>
              )}
            </div>
          </div>
        )}
      </div>

      <div className="glass-card rounded-2xl p-6 border border-slate-800/50">
        <h2 className="text-xl font-semibold mb-6 text-slate-200 flex items-center gap-2">
          <User className="w-5 h-5 text-blue-400" />
          Real Comments ({comments.length})
        </h2>

        {loading ? (
          <div className="space-y-4">
            {[1,2,3,4,5].map(i => (
              <div key={i} className="animate-pulse p-4 rounded-xl bg-slate-900/20">
                <div className="h-4 bg-slate-800 rounded w-1/4 mb-2"></div>
                <div className="h-6 bg-slate-800 rounded w-3/4"></div>
              </div>
            ))}
          </div>
        ) : (
          <div className="space-y-4 max-h-[600px] overflow-y-auto">
            {comments.map((comment) => (
              <div key={comment.id} className="p-4 rounded-xl border border-slate-800/50 bg-slate-900/20 hover:bg-slate-900/30 transition-all">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-gradient-to-br from-red-500 to-red-600 rounded-full flex items-center justify-center">
                      <User className="w-4 h-4 text-white" />
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <p className="font-semibold text-slate-200">{comment.author}</p>
                        {comment.relevanceScore && (
                          <span className="px-2 py-1 text-xs bg-green-500/20 text-green-400 rounded-full border border-green-500/30">
                            Score: {comment.relevanceScore}
                          </span>
                        )}
                      </div>
                      <div className="flex items-center gap-2 text-xs text-slate-400">
                        <Clock className="w-3 h-3" />
                        {formatDate(comment.publishedAt)}
                        {comment.filterReason && (
                          <>
                            <span>•</span>
                            <span className="text-green-400">{comment.filterReason}</span>
                          </>
                        )}
                        {comment.likeCount > 0 && (
                          <>
                            <span>•</span>
                            <ThumbsUp className="w-3 h-3" />
                            {comment.likeCount}
                          </>
                        )}
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="px-2 py-1 bg-green-500/10 text-green-400 text-xs rounded-full border border-green-500/20">
                      REAL
                    </span>
                    {comment.sentiment && (
                      <span className={`px-2 py-1 text-xs rounded-full border ${getSentimentColor(comment.sentiment)}`}>
                        {getSentimentIcon(comment.sentiment)} {comment.sentiment.toUpperCase()}
                      </span>
                    )}
                  </div>
                </div>
                
                <p className="text-slate-300 leading-relaxed mb-3">{comment.text}</p>
                
                {comment.sentiment && aiEnabled && (
                  <div className="mt-3 p-3 bg-slate-800/30 rounded-lg border border-slate-700/30">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-xs text-slate-400 flex items-center gap-1">
                        <Brain className="w-3 h-3" />
                        {comment.model || 'AI Analysis'}
                      </span>
                      <span className="text-xs text-slate-400">
                        Confidence: {((comment.confidence || 0) * 100).toFixed(0)}%
                      </span>
                    </div>
                    {comment.reasoning && (
                      <p className="text-xs text-slate-400 italic">
                        "{comment.reasoning}"
                      </p>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
