"use client";

import { useState } from 'react';
import { Play, Square, Activity, Clock, MessageSquare, AlertCircle } from 'lucide-react';

interface StreamControlsProps {
  onStreamStart?: (videoId: string) => void;
  onStreamStop?: () => void;
}

export function StreamControls({ onStreamStart, onStreamStop }: StreamControlsProps) {
  const [isStreaming, setIsStreaming] = useState(false);
  const [videoId, setVideoId] = useState('');
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState({ 
    comments: 0, 
    uptime: '00:00:00',
    startTime: null as Date | null
  });

  const handleStart = async () => {
    if (!videoId.trim()) return;
    
    setLoading(true);
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setIsStreaming(true);
      setStats(prev => ({ ...prev, startTime: new Date() }));
      onStreamStart?.(videoId);
      
      // Start uptime counter
      const interval = setInterval(() => {
        if (stats.startTime) {
          const now = new Date();
          const diff = now.getTime() - stats.startTime.getTime();
          const hours = Math.floor(diff / 3600000);
          const minutes = Math.floor((diff % 3600000) / 60000);
          const seconds = Math.floor((diff % 60000) / 1000);
          setStats(prev => ({
            ...prev,
            uptime: `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
          }));
        }
      }, 1000);
      
    } catch (error) {
      console.error('Failed to start stream:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleStop = async () => {
    setLoading(true);
    try {
      await new Promise(resolve => setTimeout(resolve, 500));
      setIsStreaming(false);
      setStats({ comments: 0, uptime: '00:00:00', startTime: null });
      onStreamStop?.();
    } catch (error) {
      console.error('Failed to stop stream:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-card rounded-2xl p-6 border border-slate-800/50 bg-slate-900/20 backdrop-blur-xl">
      <h3 className="text-xl font-semibold mb-6 text-white flex items-center gap-2">
        <Activity className="w-5 h-5 text-cyan-400" />
        Stream Control
      </h3>
      
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-300 mb-2">
            YouTube Video ID
          </label>
          <input
            type="text"
            value={videoId}
            onChange={(e) => setVideoId(e.target.value)}
            placeholder="Enter YouTube Video ID (e.g., dQw4w9WgXcQ)"
            className="w-full px-4 py-3 bg-slate-800/50 border border-slate-700 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-transparent transition-all"
            disabled={isStreaming}
          />
          <p className="text-xs text-slate-500 mt-1">
            Extract from YouTube URL: youtube.com/watch?v=<strong>VIDEO_ID</strong>
          </p>
        </div>
        
        {!isStreaming ? (
          <button
            onClick={handleStart}
            disabled={!videoId.trim() || loading}
            className="w-full bg-green-600 hover:bg-green-700 disabled:bg-slate-700 disabled:text-slate-400 text-white px-6 py-3 rounded-xl font-medium transition-all duration-200 flex items-center justify-center gap-2"
          >
            {loading ? (
              <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            ) : (
              <Play className="w-5 h-5" />
            )}
            {loading ? 'Starting Stream...' : 'Start Stream'}
          </button>
        ) : (
          <button
            onClick={handleStop}
            disabled={loading}
            className="w-full bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-xl font-medium transition-all duration-200 flex items-center justify-center gap-2"
          >
            {loading ? (
              <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            ) : (
              <Square className="w-5 h-5" />
            )}
            {loading ? 'Stopping...' : 'Stop Stream'}
          </button>
        )}
      </div>

      {/* Stream Status */}
      <div className="mt-6 pt-6 border-t border-slate-700/50">
        <div className="flex items-center gap-2 mb-4">
          <div className={`w-3 h-3 rounded-full ${isStreaming ? 'bg-red-500 animate-pulse' : 'bg-gray-500'}`} />
          <span className="text-sm font-mono font-medium">
            {isStreaming ? 'LIVE STREAMING' : 'OFFLINE'}
          </span>
        </div>

        {isStreaming && (
          <div className="space-y-3">
            <h4 className="text-sm font-medium text-slate-300">Stream Statistics</h4>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm text-slate-400 flex items-center gap-2">
                  <MessageSquare className="w-4 h-4" />
                  Comments Processed
                </span>
                <span className="text-sm font-mono text-cyan-400">{stats.comments}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-slate-400 flex items-center gap-2">
                  <Clock className="w-4 h-4" />
                  Stream Uptime
                </span>
                <span className="text-sm font-mono text-cyan-400">{stats.uptime}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-slate-400">Video ID</span>
                <span className="text-sm font-mono text-slate-300 truncate max-w-[120px]">{videoId}</span>
              </div>
            </div>
          </div>
        )}

        {!isStreaming && videoId && (
          <div className="bg-blue-500/10 border border-blue-500/20 rounded-xl p-3">
            <div className="flex items-start gap-2">
              <AlertCircle className="w-4 h-4 text-blue-400 mt-0.5 flex-shrink-0" />
              <div>
                <p className="text-sm text-blue-400 font-medium">Ready to Stream</p>
                <p className="text-xs text-blue-300/70">Click "Start Stream" to begin real-time analysis</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
