"use client";

import { useState } from 'react';
import { Plus, Trash2, Play, Square } from 'lucide-react';

interface Stream {
  id: string;
  videoId: string;
  title?: string;
  isActive: boolean;
}

export function MultiStreamControls() {
  const [streams, setStreams] = useState<Stream[]>([]);
  const [newVideoId, setNewVideoId] = useState('');

  const addStream = () => {
    if (!newVideoId.trim()) return;
    
    const newStream: Stream = {
      id: Date.now().toString(),
      videoId: newVideoId.trim(),
      isActive: false
    };
    
    setStreams(prev => [...prev, newStream]);
    setNewVideoId('');
  };

  const toggleStream = (id: string) => {
    setStreams(prev => prev.map(stream => 
      stream.id === id ? { ...stream, isActive: !stream.isActive } : stream
    ));
  };

  const removeStream = (id: string) => {
    setStreams(prev => prev.filter(stream => stream.id !== id));
  };

  return (
    <div className="glass-card rounded-2xl p-6">
      <h3 className="text-xl font-semibold mb-4 text-white">Multi-Stream Control</h3>
      
      {/* Add New Stream */}
      <div className="flex gap-2 mb-4">
        <input
          type="text"
          value={newVideoId}
          onChange={(e) => setNewVideoId(e.target.value)}
          placeholder="YouTube Video ID"
          className="flex-1 px-3 py-2 bg-slate-800/50 border border-slate-700 rounded-lg text-white"
        />
        <button
          onClick={addStream}
          className="px-4 py-2 bg-cyan-600 hover:bg-cyan-700 rounded-lg flex items-center gap-2"
        >
          <Plus className="w-4 h-4" />
          Add
        </button>
      </div>

      {/* Stream List */}
      <div className="space-y-2">
        {streams.map((stream) => (
          <div key={stream.id} className="flex items-center gap-2 p-3 bg-slate-800/30 rounded-lg">
            <div className="flex-1">
              <div className="font-mono text-sm text-slate-300">{stream.videoId}</div>
              <div className={`text-xs ${stream.isActive ? 'text-green-400' : 'text-slate-500'}`}>
                {stream.isActive ? 'LIVE' : 'OFFLINE'}
              </div>
            </div>
            <button
              onClick={() => toggleStream(stream.id)}
              className={`p-2 rounded ${stream.isActive ? 'bg-red-600 hover:bg-red-700' : 'bg-green-600 hover:bg-green-700'}`}
            >
              {stream.isActive ? <Square className="w-4 h-4" /> : <Play className="w-4 h-4" />}
            </button>
            <button
              onClick={() => removeStream(stream.id)}
              className="p-2 bg-slate-600 hover:bg-slate-700 rounded"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          </div>
        ))}
      </div>

      {streams.length === 0 && (
        <div className="text-center py-8 text-slate-400">
          <p>No streams added yet</p>
          <p className="text-sm">Add YouTube Video IDs to start monitoring</p>
        </div>
      )}
    </div>
  );
}
