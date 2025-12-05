"use client";

import { useState, useEffect } from "react";

interface TypewriterProps {
  text: string;
  speed?: number;
  className?: string;
  cursor?: boolean;
  onComplete?: () => void;
}

export function Typewriter({ text, speed = 100, className = "", cursor = true, onComplete }: TypewriterProps) {
  const [displayText, setDisplayText] = useState("");
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isComplete, setIsComplete] = useState(false);

  useEffect(() => {
    if (currentIndex < text.length) {
      const timer = setTimeout(() => {
        setDisplayText((prev) => prev + text[currentIndex]);
        setCurrentIndex((prev) => prev + 1);
      }, speed);
      return () => clearTimeout(timer);
    } else {
      setIsComplete(true);
      onComplete?.();
    }
  }, [currentIndex, text, speed, onComplete]);

  return (
    <span className={className}>
      {displayText}
      {cursor && (
        <span className={`inline-block w-0.5 h-[1em] bg-current ml-1 ${isComplete ? "animate-pulse" : "animate-blink"}`}>
          |
        </span>
      )}
    </span>
  );
}

// Multiple lines typewriter
interface TypewriterLinesProps {
  lines: string[];
  speed?: number;
  lineDelay?: number;
  className?: string;
  lineClassName?: string;
}

export function TypewriterLines({ lines, speed = 50, lineDelay = 500, className = "", lineClassName = "" }: TypewriterLinesProps) {
  const [currentLine, setCurrentLine] = useState(0);
  const [completedLines, setCompletedLines] = useState<string[]>([]);

  const handleLineComplete = () => {
    if (currentLine < lines.length - 1) {
      setCompletedLines((prev) => [...prev, lines[currentLine]]);
      setTimeout(() => {
        setCurrentLine((prev) => prev + 1);
      }, lineDelay);
    }
  };

  return (
    <div className={className}>
      {completedLines.map((line, index) => (
        <div key={index} className={lineClassName}>
          {line}
        </div>
      ))}
      {currentLine < lines.length && (
        <Typewriter
          text={lines[currentLine]}
          speed={speed}
          className={lineClassName}
          cursor={true}
          onComplete={handleLineComplete}
        />
      )}
    </div>
  );
}
