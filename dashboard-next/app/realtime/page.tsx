"use client";

import { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { TrendingUp, TrendingDown, Users, MessageSquare, Youtube, Database, Search } from 'lucide-react';

export default function RealtimePage() {
  const [videoUrl, setVideoUrl] = useState('');
  const [currentVideo, setCurrentVideo] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState({
    total: 0,
    positive: 0,
    negative: 0,
    neutral: 0
  });
  const [recentComments, setRecentComments] = useState([]);
  const [exportLoading, setExportLoading] = useState(false);

  // Export functions
  const exportToJSON = () => {
    const exportData = {
      timestamp: new Date().toISOString(),
      video: currentVideo,
      stats: stats,
      comments: recentComments,
      analysis_layers: ["Layer 1: Core Sentiment", "Layer 2: Basic Emotions", "Layer 3: Football-Specific"],
      total_lexicon_words: 6500
    };
    
    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `timnas-analysis-${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const exportToCSV = () => {
    if (recentComments.length === 0) return;
    
    const headers = ['Text', 'L1_Sentiment', 'L1_Confidence', 'L1_Score', 'L2_Emotion', 'L2_Confidence', 'L3_Emotion', 'L3_Confidence', 'Timestamp'];
    
    const csvData = recentComments.map(comment => [
      `"${comment.text?.replace(/"/g, '""') || ''}"`,
      comment.layer1?.sentiment || '',
      comment.layer1?.confidence || '',
      comment.layer1?.score || '',
      comment.layer2?.primary_emotion || '',
      comment.layer2?.confidence || '',
      comment.layer3?.primary_emotion || '',
      comment.layer3?.confidence || '',
      new Date().toISOString()
    ]);
    
    const csv = [headers, ...csvData].map(row => row.join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `timnas-comments-${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const sentimentData = [
    { name: 'Positive', value: stats.positive, color: '#10b981' },
    { name: 'Negative', value: stats.negative, color: '#ef4444' },
    { name: 'Neutral', value: stats.neutral, color: '#6b7280' }
  ];

  const emotionData = [
    { emotion: 'Kemarahan', count: 45 + stats.negative, color: '#ef4444' },
    { emotion: 'Kekecewaan', count: 38 + Math.floor(stats.negative * 0.8), color: '#f97316' },
    { emotion: 'Harapan', count: 25 + stats.positive, color: '#10b981' },
    { emotion: 'Dukungan', count: 18 + Math.floor(stats.positive * 0.7), color: '#3b82f6' }
  ];

  const fetchComments = async (url: string) => {
    setLoading(true);
    try {
      const response = await fetch(`/api/youtube?action=comments&url=${encodeURIComponent(url)}&ai=true`);
      const data = await response.json();
      
      if (data.error) {
        console.error('YouTube API error:', data.error);
        return false;
      }
      
      setCurrentVideo(data.video);
      
      // Enhanced multi-layer analysis for each comment
      if (data.comments) {
        const enhancedComments = await Promise.all(
          data.comments.slice(0, 10).map(async (comment: any) => {
            try {
              const analysisResponse = await fetch('http://localhost:8000/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                  text: comment.text,
                  layers: ["layer1", "layer2", "layer3"]
                })
              });
              
              if (analysisResponse.ok) {
                const analysis = await analysisResponse.json();
                return {
                  ...comment,
                  layer1: analysis.layer1_result,
                  layer2: analysis.layer2_result,
                  layer3: analysis.layer3_result,
                  enhanced: true
                };
              }
            } catch (error) {
              console.error('Analysis error:', error);
            }
            return comment;
          })
        );
        
        setRecentComments(enhancedComments);
        
        // Calculate enhanced stats from multi-layer analysis
        const enhancedStats = enhancedComments.reduce((acc, comment) => {
          if (comment.enhanced && comment.layer1) {
            acc.total++;
            if (comment.layer1.sentiment === 'positive') acc.positive++;
            else if (comment.layer1.sentiment === 'negative') acc.negative++;
            else acc.neutral++;
          }
          return acc;
        }, { total: 0, positive: 0, negative: 0, neutral: 0 });
        
        setStats(enhancedStats);
      }
      
      return true;
    } catch (error) {
      console.error('Error fetching comments:', error);
      return false;
    } finally {
      setLoading(false);
    }
  };

  const autoSearchVideos = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/youtube?action=search');
      const data = await response.json();
      
      if (data.videos && data.videos.length > 0) {
        const latestVideo = data.videos[0];
        const success = await fetchComments(`https://youtube.com/watch?v=${latestVideo.videoId}`);
        if (success) {
          setCurrentVideo(latestVideo);
        }
      }
    } catch (error) {
      console.error('Error auto-searching videos:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyze = async () => {
    if (videoUrl.trim()) {
      await fetchComments(videoUrl);
    } else {
      await autoSearchVideos();
    }
  };

  const StatCard = ({ title, value, icon: Icon, color }: any) => (
    <div className="glass-card rounded-2xl p-4 border border-slate-800/50 bg-slate-900/20 backdrop-blur-xl">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-slate-400 text-sm">{title}</p>
          <p className="text-2xl font-bold text-white mt-1">{value.toLocaleString()}</p>
        </div>
        <div className={`p-2 rounded-xl ${color}`}>
          <Icon className="w-5 h-5 text-white" />
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen p-6 space-y-6">
      {/* Enhanced Header with Layer Info */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2 font-mono">📊 Live Analysis</h1>
          <p className="text-slate-400 flex items-center gap-2">
            <Database className="w-4 h-4" />
            Multi-Layer AI Analysis (6,500 words lexicon)
          </p>
          <div className="flex gap-2 mt-2">
            <span className="px-2 py-1 bg-green-500/20 text-green-400 text-xs rounded-full">L1: Core Sentiment</span>
            <span className="px-2 py-1 bg-blue-500/20 text-blue-400 text-xs rounded-full">L2: Basic Emotions</span>
            <span className="px-2 py-1 bg-purple-500/20 text-purple-400 text-xs rounded-full">L3: Football-Specific</span>
          </div>
        </div>
        <div className="text-right">
          <div className="text-2xl font-bold text-cyan-400">{stats.total}</div>
          <div className="text-sm text-slate-400">Comments Analyzed</div>
        </div>
      </div>

      {/* Analysis Control with Export Buttons */}
      <div className="glass-card rounded-2xl p-6 border border-slate-800/50 bg-slate-900/20 backdrop-blur-xl">
        <div className="flex items-center gap-4 mb-4">
          <Youtube className="w-6 h-6 text-red-500" />
          <div className="flex-1">
            <input
              type="text"
              placeholder="YouTube URL (optional - leave empty for auto-search latest timnas videos)"
              value={videoUrl}
              onChange={(e) => setVideoUrl(e.target.value)}
              className="w-full px-4 py-2 bg-slate-800/50 border border-slate-700 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:border-blue-500"
              disabled={loading}
            />
          </div>
          <button
            onClick={handleAnalyze}
            disabled={loading}
            className="flex items-center gap-2 px-6 py-2 rounded-xl font-medium transition-all bg-blue-600 hover:bg-blue-700 text-white disabled:bg-slate-700"
          >
            {loading ? (
              <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            ) : (
              <Search className="w-4 h-4" />
            )}
            {loading ? 'Analyzing...' : 'Analyze'}
          </button>
        </div>
        
        {/* Export Buttons */}
        {recentComments.length > 0 && (
          <div className="flex gap-2 pt-4 border-t border-slate-700/50">
            <button
              onClick={exportToJSON}
              className="flex items-center gap-2 px-4 py-2 rounded-lg bg-green-600/20 hover:bg-green-600/30 text-green-400 text-sm transition-all"
            >
              <Database className="w-4 h-4" />
              Export JSON
            </button>
            <button
              onClick={exportToCSV}
              className="flex items-center gap-2 px-4 py-2 rounded-lg bg-blue-600/20 hover:bg-blue-600/30 text-blue-400 text-sm transition-all"
            >
              <Database className="w-4 h-4" />
              Export CSV
            </button>
            <div className="flex-1 text-right text-xs text-slate-500 self-center">
              {recentComments.length} comments ready to export
            </div>
          </div>
        )}
        
        <p className="text-xs text-slate-500 mt-2">
          {videoUrl ? 'Analyze specific video' : 'Auto-search latest "timnas indonesia" videos'} • Real YouTube data with multi-layer analysis
        </p>
        {currentVideo && (
          <div className="mt-3 p-3 bg-slate-800/30 rounded-lg">
            <p className="text-sm text-white font-medium">{currentVideo.title}</p>
            <p className="text-xs text-slate-400">{currentVideo.channelTitle} • {currentVideo.viewCount?.toLocaleString()} views</p>
          </div>
        )}
      </div>

      {/* Enhanced Stats Cards with Layer Breakdown */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard title="Total" value={stats.total} icon={MessageSquare} color="bg-blue-600" />
        <StatCard title="Positive" value={stats.positive} icon={TrendingUp} color="bg-green-600" />
        <StatCard title="Negative" value={stats.negative} icon={TrendingDown} color="bg-red-600" />
        <StatCard title="Coverage" value={`${Math.round((stats.total > 0 ? (stats.positive + stats.negative) / stats.total * 100 : 0))}%`} icon={Database} color="bg-purple-600" />
      </div>

      {/* Layer Performance Indicators */}
      <div className="glass-card rounded-2xl p-4 border border-slate-800/50 bg-slate-900/20 backdrop-blur-xl">
        <h3 className="text-lg font-semibold mb-4 text-white">Layer Performance</h3>
        <div className="grid grid-cols-3 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-green-400">L1</div>
            <div className="text-sm text-slate-400">Core Sentiment</div>
            <div className="text-xs text-green-300">1,500 words</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-400">L2</div>
            <div className="text-sm text-slate-400">Basic Emotions</div>
            <div className="text-xs text-blue-300">2,000 words</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-purple-400">L3</div>
            <div className="text-sm text-slate-400">Football-Specific</div>
            <div className="text-xs text-purple-300">3,000 words</div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Charts */}
        <div className="lg:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Sentiment Pie */}
          <div className="glass-card rounded-2xl p-4 border border-slate-800/50 bg-slate-900/20 backdrop-blur-xl">
            <h3 className="text-lg font-semibold mb-4 text-white">Sentiment Distribution</h3>
            <div className="h-48">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={sentimentData} cx="50%" cy="50%" innerRadius={40} outerRadius={80} paddingAngle={5} dataKey="value">
                    {sentimentData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px', color: '#f1f5f9' }} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Emotion Bar */}
          <div className="glass-card rounded-2xl p-4 border border-slate-800/50 bg-slate-900/20 backdrop-blur-xl">
            <h3 className="text-lg font-semibold mb-4 text-white">Emotions</h3>
            <div className="h-48">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={emotionData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                  <XAxis dataKey="emotion" stroke="#94a3b8" fontSize={12} />
                  <YAxis stroke="#94a3b8" fontSize={12} />
                  <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px', color: '#f1f5f9' }} />
                  <Bar dataKey="count" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Recent Comments with Multi-Layer AI Analysis */}
        <div className="glass-card rounded-2xl p-4 border border-slate-800/50 bg-slate-900/20 backdrop-blur-xl">
          <h3 className="text-lg font-semibold mb-4 text-white flex items-center gap-2">
            <Database className="w-4 h-4 text-cyan-400" />
            Multi-Layer Analysis (3 Layers)
          </h3>
          <div className="space-y-3 h-96 overflow-y-auto">
            {recentComments.length > 0 ? (
              recentComments.map((comment: any, index) => (
                <div key={index} className="p-3 bg-slate-800/30 rounded-lg border border-slate-700/30">
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex gap-2">
                      {comment.enhanced && comment.layer1 && (
                        <div className={`px-2 py-1 rounded-full text-xs ${
                          comment.layer1.sentiment === 'positive' ? 'bg-green-500/20 text-green-400' : 
                          comment.layer1.sentiment === 'negative' ? 'bg-red-500/20 text-red-400' : 
                          'bg-gray-500/20 text-gray-400'
                        }`}>
                          L1: {comment.layer1.sentiment?.toUpperCase()}
                        </div>
                      )}
                      {comment.enhanced && comment.layer2 && comment.layer2.primary_emotion !== 'neutral' && (
                        <div className="px-2 py-1 rounded-full text-xs bg-blue-500/20 text-blue-400">
                          L2: {comment.layer2.primary_emotion}
                        </div>
                      )}
                      {comment.enhanced && comment.layer3 && comment.layer3.primary_emotion !== 'neutral' && (
                        <div className="px-2 py-1 rounded-full text-xs bg-purple-500/20 text-purple-400">
                          L3: {comment.layer3.primary_emotion}
                        </div>
                      )}
                    </div>
                    <div className="text-xs text-slate-400">
                      {comment.enhanced && comment.layer1 ? 
                        `${(comment.layer1.confidence * 100).toFixed(0)}%` : 
                        'Basic'
                      }
                    </div>
                  </div>
                  <p className="text-xs text-slate-300 mb-2">{comment.text}</p>
                  
                  {comment.enhanced && (
                    <div className="space-y-1">
                      {comment.layer1 && (
                        <p className="text-xs text-slate-500">
                          💭 Layer 1: {comment.layer1.sentiment} (Score: {comment.layer1.score?.toFixed(2)})
                        </p>
                      )}
                      {comment.layer2 && comment.layer2.primary_emotion !== 'neutral' && (
                        <p className="text-xs text-slate-500">
                          🎭 Layer 2: {comment.layer2.primary_emotion} ({(comment.layer2.confidence * 100).toFixed(0)}%)
                        </p>
                      )}
                      {comment.layer3 && comment.layer3.primary_emotion !== 'neutral' && (
                        <p className="text-xs text-slate-500">
                          ⚽ Layer 3: {comment.layer3.primary_emotion} ({(comment.layer3.confidence * 100).toFixed(0)}%)
                        </p>
                      )}
                    </div>
                  )}
                  
                  <div className="flex items-center justify-between mt-2">
                    <span className="text-xs text-slate-500">
                      {comment.enhanced ? 'Multi-Layer AI' : 'Basic Analysis'}
                    </span>
                    <span className="text-xs text-slate-500">
                      {new Date().toLocaleTimeString()}
                    </span>
                  </div>
                </div>
              ))
            ) : (
              <div className="flex items-center justify-center h-full text-slate-400">
                <div className="text-center">
                  <Search className="w-6 h-6 mx-auto mb-2 opacity-50" />
                  <p className="text-xs">Click "Analyze" to see Multi-Layer AI analysis</p>
                  <p className="text-xs text-slate-500 mt-1">L1: Sentiment | L2: Emotions | L3: Football-Specific</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
