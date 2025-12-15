"use client";

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface StreamContextType {
  isStreaming: boolean;
  currentVideoId: string | null;
  startStream: (videoId: string) => void;
  stopStream: () => void;
}

const StreamContext = createContext<StreamContextType | undefined>(undefined);

export function StreamProvider({ children }: { children: ReactNode }) {
  const [isStreaming, setIsStreaming] = useState(false);
  const [currentVideoId, setCurrentVideoId] = useState<string | null>(null);

  // Persist state in localStorage
  useEffect(() => {
    const saved = localStorage.getItem('streamState');
    if (saved) {
      const { isStreaming: savedStreaming, videoId } = JSON.parse(saved);
      setIsStreaming(savedStreaming);
      setCurrentVideoId(videoId);
    }
  }, []);

  const startStream = (videoId: string) => {
    setIsStreaming(true);
    setCurrentVideoId(videoId);
    localStorage.setItem('streamState', JSON.stringify({ isStreaming: true, videoId }));
  };

  const stopStream = () => {
    setIsStreaming(false);
    setCurrentVideoId(null);
    localStorage.setItem('streamState', JSON.stringify({ isStreaming: false, videoId: null }));
  };

  return (
    <StreamContext.Provider value={{ isStreaming, currentVideoId, startStream, stopStream }}>
      {children}
    </StreamContext.Provider>
  );
}

export const useStream = () => {
  const context = useContext(StreamContext);
  if (!context) throw new Error('useStream must be used within StreamProvider');
  return context;
};
