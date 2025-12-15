"use client";

import { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { TrendingUp, TrendingDown, Activity, Users, MessageSquare, Clock, Play, Square, Youtube, Database } from 'lucide-react';
import { LiveComments } from '@/components/LiveComments';
import { useStream } from '@/contexts/StreamContext';

export default function RealtimePage() {
  const { isStreaming, startStream, stopStream } = useStream();
  const [videoUrl, setVideoUrl] = useState('');
  const [currentVideo, setCurrentVideo] = useState<any>(null);
  const [liveStats, setLiveStats] = useState({
    total: 0,
    positive: 0,
    negative: 0,
    neutral: 0
  });
  const [recentComments, setRecentComments] = useState([]);

  // Sample data
  const sentimentData = [
    { name: 'Positive', value: liveStats.positive, color: '#10b981' },
    { name: 'Negative', value: liveStats.negative, color: '#ef4444' },
    { name: 'Neutral', value: liveStats.neutral, color: '#6b7280' }
  ];

  const emotionData = [
    { emotion: 'Kemarahan', count: 45 + liveStats.negative, color: '#ef4444' },
    { emotion: 'Kekecewaan', count: 38 + Math.floor(liveStats.negative * 0.8), color: '#f97316' },
    { emotion: 'Harapan', count: 25 + liveStats.positive, color: '#10b981' },
    { emotion: 'Dukungan', count: 18 + Math.floor(liveStats.positive * 0.7), color: '#3b82f6' }
  ];

  // Fetch real YouTube comments with AI analysis
  const fetchRealComments = async (url: string) => {
    try {
      const response = await fetch(`/api/youtube?action=comments&url=${encodeURIComponent(url)}&ai=true`);
      const data = await response.json();
      
      if (data.error) {
        console.error('YouTube API error:', data.error);
        return false;
      }
      
      setCurrentVideo(data.video);
      console.log(`✅ Fetched ${data.total} comments with ${data.analysis?.model} analysis`);
      console.log(`📊 Sentiment summary:`, data.analysis?.summary);
      
      // Update stats with AI analysis results
      if (data.analysis?.summary) {
        setLiveStats({
          total: data.total,
          positive: data.analysis.summary.positive || 0,
          negative: data.analysis.summary.negative || 0,
          neutral: data.analysis.summary.neutral || 0
        });
      }
      
      // Set recent comments with AI analysis
      if (data.comments) {
        setRecentComments(data.comments.slice(0, 10));
      }
      
      return true;
    } catch (error) {
      console.error('Error fetching real comments:', error);
      return false;
    }
  };

  // Auto-search timnas videos
  const autoSearchVideos = async () => {
    try {
      const response = await fetch('/api/youtube?action=search');
      const data = await response.json();
      
      if (data.videos && data.videos.length > 0) {
        // Get comments from the latest video
        const latestVideo = data.videos[0];
        const success = await fetchRealComments(`https://youtube.com/watch?v=${latestVideo.videoId}`);
        if (success) {
          setCurrentVideo(latestVideo);
        }
      }
    } catch (error) {
      console.error('Error auto-searching videos:', error);
    }
  };
  const fetchLiveStats = async () => {
    try {
      const response = await fetch('/api/live-data');
      const data = await response.json();
      if (data.stats) {
        setLiveStats(data.stats);
        setRecentComments(data.recent || []);
      }
    } catch (error) {
      console.error('Error fetching live stats:', error);
    }
  };

  // Real-time comment monitoring
  useEffect(() => {
    if (!isStreaming) return;

    const interval = setInterval(async () => {
      // Refresh comments from current video
      if (currentVideo) {
        await fetchRealComments(`https://youtube.com/watch?v=${currentVideo.id || currentVideo.videoId}`);
      } else if (videoUrl) {
        await fetchRealComments(videoUrl);
      } else {
        // Auto-search for new videos
        await autoSearchVideos();
      }
    }, 30000); // Refresh every 30 seconds
    
    return () => clearInterval(interval);
  }, [isStreaming, currentVideo, videoUrl]);

  // Initial load
  useEffect(() => {
    fetchLiveStats();
  }, []);

  const handleStartStream = async () => {
    if (videoUrl.trim()) {
      // Real YouTube URL provided
      const success = await fetchRealComments(videoUrl);
      if (success) {
        startStream(videoUrl);
      } else {
        alert('Failed to fetch YouTube data. Check video URL or try again.');
      }
    } else {
      // Auto-search mode
      await autoSearchVideos();
      startStream('auto-search-timnas');
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
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2 font-mono">🔴 Live Sentiment Analysis</h1>
          <p className="text-slate-400 flex items-center gap-2">
            <Database className="w-4 h-4" />
            Real-time YouTube comment monitoring & sentiment analysis
          </p>
        </div>
        <div className="flex items-center gap-2">
          <div className={`w-3 h-3 rounded-full ${isStreaming ? 'bg-red-500 animate-pulse' : 'bg-gray-500'}`} />
          <span className="text-sm font-mono">{isStreaming ? 'LIVE' : 'OFFLINE'}</span>
        </div>
      </div>

      {/* Stream Control */}
      <div className="glass-card rounded-2xl p-6 border border-slate-800/50 bg-slate-900/20 backdrop-blur-xl">
        <div className="flex items-center gap-4">
          <Youtube className="w-6 h-6 text-red-500" />
          <div className="flex-1">
            <input
              type="text"
              placeholder="YouTube URL (optional - leave empty for auto-search latest timnas videos)"
              value={videoUrl}
              onChange={(e) => setVideoUrl(e.target.value)}
              className="w-full px-4 py-2 bg-slate-800/50 border border-slate-700 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:border-blue-500"
              disabled={isStreaming}
            />
          </div>
          <button
            onClick={isStreaming ? stopStream : handleStartStream}
            className={`flex items-center gap-2 px-6 py-2 rounded-xl font-medium transition-all ${
              isStreaming 
                ? 'bg-red-600 hover:bg-red-700 text-white' 
                : 'bg-green-600 hover:bg-green-700 text-white'
            }`}
          >
            {isStreaming ? <Square className="w-4 h-4" /> : <Play className="w-4 h-4" />}
            {isStreaming ? 'Stop' : 'Start'} Stream
          </button>
        </div>
        <div className="flex items-center justify-between mt-2">
          <p className="text-xs text-slate-500">
            {videoUrl ? 'Monitor specific video' : 'Auto-search latest "timnas indonesia" videos'} • Real YouTube data with sentiment analysis
          </p>
          {isStreaming && (
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
              <span className="text-xs text-red-400 font-mono">LIVE</span>
            </div>
          )}
        </div>
        {currentVideo && (
          <div className="mt-3 p-3 bg-slate-800/30 rounded-lg">
            <p className="text-sm text-white font-medium">{currentVideo.title}</p>
            <p className="text-xs text-slate-400">{currentVideo.channelTitle} • {currentVideo.viewCount?.toLocaleString()} views</p>
          </div>
        )}
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard title="Total" value={liveStats.total} icon={MessageSquare} color="bg-blue-600" />
        <StatCard title="Positive" value={liveStats.positive} icon={TrendingUp} color="bg-green-600" />
        <StatCard title="Negative" value={liveStats.negative} icon={TrendingDown} color="bg-red-600" />
        <StatCard title="Users" value={Math.floor(liveStats.total * 0.7)} icon={Users} color="bg-purple-600" />
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
            <h3 className="text-lg font-semibold mb-4 text-white">Live Emotions</h3>
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

        {/* Right: Live Feed & Activity */}
        <div className="space-y-6">
          <LiveComments isStreaming={isStreaming} />
          
          {/* Recent Comments with AI Analysis */}
          <div className="glass-card rounded-2xl p-4 border border-slate-800/50 bg-slate-900/20 backdrop-blur-xl">
            <h3 className="text-lg font-semibold mb-4 text-white flex items-center gap-2">
              <Database className="w-4 h-4 text-cyan-400" />
              Recent Comments (Gemini AI)
            </h3>
            <div className="space-y-3 h-48 overflow-y-auto">
              {recentComments.length > 0 ? (
                recentComments.slice(0, 5).map((comment: any, index) => (
                  <div key={index} className="p-3 bg-slate-800/30 rounded-lg border border-slate-700/30">
                    <div className="flex items-start justify-between mb-2">
                      <div className={`px-2 py-1 rounded-full text-xs ${
                        comment.sentiment === 'positive' ? 'bg-green-500/20 text-green-400' : 
                        comment.sentiment === 'negative' ? 'bg-red-500/20 text-red-400' : 
                        'bg-gray-500/20 text-gray-400'
                      }`}>
                        {comment.sentiment?.toUpperCase()}
                      </div>
                      <div className="text-xs text-slate-400">
                        {((comment.confidence || 0) * 100).toFixed(0)}%
                      </div>
                    </div>
                    <p className="text-xs text-slate-300 mb-2">{comment.text}</p>
                    {comment.reasoning && (
                      <p className="text-xs text-slate-500 italic">
                        💭 {comment.reasoning}
                      </p>
                    )}
                    <div className="flex items-center justify-between mt-2">
                      <span className="text-xs text-slate-500">
                        {comment.model || 'AI'} • {comment.emotion}
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
                    <Clock className="w-6 h-6 mx-auto mb-2 opacity-50" />
                    <p className="text-xs">Start streaming to see AI analysis</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
