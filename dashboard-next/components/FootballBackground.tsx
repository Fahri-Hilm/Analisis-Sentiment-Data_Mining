"use client";

import { useEffect, useRef } from "react";

interface FloatingElement {
  x: number;
  y: number;
  size: number;
  speedX: number;
  speedY: number;
  opacity: number;
  type: 'ball' | 'heart' | 'star' | 'comment';
  rotation: number;
  rotationSpeed: number;
}

export function FootballBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resizeCanvas();
    window.addEventListener("resize", resizeCanvas);

    const elements: FloatingElement[] = [];
    const elementCount = 25;

    // Create floating elements
    for (let i = 0; i < elementCount; i++) {
      elements.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        size: Math.random() * 20 + 10,
        speedX: (Math.random() - 0.5) * 0.3,
        speedY: (Math.random() - 0.5) * 0.3,
        opacity: Math.random() * 0.3 + 0.1,
        type: ['ball', 'heart', 'star', 'comment'][Math.floor(Math.random() * 4)] as any,
        rotation: Math.random() * Math.PI * 2,
        rotationSpeed: (Math.random() - 0.5) * 0.02,
      });
    }

    const drawFootball = (x: number, y: number, size: number, opacity: number) => {
      ctx.save();
      ctx.globalAlpha = opacity;
      ctx.fillStyle = "#ffffff";
      ctx.beginPath();
      ctx.arc(x, y, size, 0, Math.PI * 2);
      ctx.fill();
      
      // Draw pentagon pattern
      ctx.strokeStyle = "#000000";
      ctx.lineWidth = 1;
      ctx.beginPath();
      for (let i = 0; i < 5; i++) {
        const angle = (i * Math.PI * 2) / 5;
        const px = x + Math.cos(angle) * size * 0.3;
        const py = y + Math.sin(angle) * size * 0.3;
        if (i === 0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      }
      ctx.closePath();
      ctx.stroke();
      ctx.restore();
    };

    const drawHeart = (x: number, y: number, size: number, opacity: number) => {
      ctx.save();
      ctx.globalAlpha = opacity;
      ctx.fillStyle = "#ef4444";
      ctx.beginPath();
      ctx.moveTo(x, y + size * 0.3);
      ctx.bezierCurveTo(x - size * 0.5, y - size * 0.2, x - size, y + size * 0.1, x, y + size * 0.7);
      ctx.bezierCurveTo(x + size, y + size * 0.1, x + size * 0.5, y - size * 0.2, x, y + size * 0.3);
      ctx.fill();
      ctx.restore();
    };

    const drawStar = (x: number, y: number, size: number, opacity: number, rotation: number) => {
      ctx.save();
      ctx.globalAlpha = opacity;
      ctx.fillStyle = "#fbbf24";
      ctx.translate(x, y);
      ctx.rotate(rotation);
      ctx.beginPath();
      for (let i = 0; i < 5; i++) {
        const angle = (i * Math.PI * 2) / 5;
        const outerRadius = size;
        const innerRadius = size * 0.4;
        
        const outerX = Math.cos(angle) * outerRadius;
        const outerY = Math.sin(angle) * outerRadius;
        const innerX = Math.cos(angle + Math.PI / 5) * innerRadius;
        const innerY = Math.sin(angle + Math.PI / 5) * innerRadius;
        
        if (i === 0) ctx.moveTo(outerX, outerY);
        else ctx.lineTo(outerX, outerY);
        ctx.lineTo(innerX, innerY);
      }
      ctx.closePath();
      ctx.fill();
      ctx.restore();
    };

    const drawComment = (x: number, y: number, size: number, opacity: number) => {
      ctx.save();
      ctx.globalAlpha = opacity;
      ctx.fillStyle = "#3b82f6";
      ctx.fillRect(x - size * 0.6, y - size * 0.4, size * 1.2, size * 0.8);
      ctx.beginPath();
      ctx.moveTo(x - size * 0.2, y + size * 0.4);
      ctx.lineTo(x - size * 0.4, y + size * 0.7);
      ctx.lineTo(x, y + size * 0.4);
      ctx.fill();
      ctx.restore();
    };

    let animationId: number;

    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      elements.forEach((element) => {
        // Update position
        element.x += element.speedX;
        element.y += element.speedY;
        element.rotation += element.rotationSpeed;

        // Wrap around screen
        if (element.x < -element.size) element.x = canvas.width + element.size;
        if (element.x > canvas.width + element.size) element.x = -element.size;
        if (element.y < -element.size) element.y = canvas.height + element.size;
        if (element.y > canvas.height + element.size) element.y = -element.size;

        // Draw element based on type
        switch (element.type) {
          case 'ball':
            drawFootball(element.x, element.y, element.size, element.opacity);
            break;
          case 'heart':
            drawHeart(element.x, element.y, element.size, element.opacity);
            break;
          case 'star':
            drawStar(element.x, element.y, element.size, element.opacity, element.rotation);
            break;
          case 'comment':
            drawComment(element.x, element.y, element.size, element.opacity);
            break;
        }
      });

      animationId = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      window.removeEventListener("resize", resizeCanvas);
      cancelAnimationFrame(animationId);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 pointer-events-none z-0"
      style={{ background: "transparent" }}
    />
  );
}
