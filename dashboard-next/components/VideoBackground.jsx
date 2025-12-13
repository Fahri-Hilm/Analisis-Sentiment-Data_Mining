import { useEffect, useRef } from 'react';

export default function VideoBackground({ src, className = "" }) {
  const videoRef = useRef(null);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    const handleTimeUpdate = () => {
      const duration = video.duration;
      const current = video.currentTime;
      
      // Fade out 1 detik sebelum selesai
      if (current >= duration - 1) {
        video.style.transition = 'opacity 0.5s ease';
        video.style.opacity = '0';
        
        setTimeout(() => {
          video.currentTime = 0;
          video.style.opacity = '1';
        }, 500);
      }
    };

    video.addEventListener('timeupdate', handleTimeUpdate);
    return () => video.removeEventListener('timeupdate', handleTimeUpdate);
  }, []);

  return (
    <video
      ref={videoRef}
      className={`fixed inset-0 w-full h-full object-cover -z-10 ${className}`}
      autoPlay
      muted
      loop
      playsInline
    >
      <source src={src} type="video/mp4" />
    </video>
  );
}
