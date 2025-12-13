"use client";

export function VideoBackground() {
  return (
    <video
      autoPlay
      loop
      muted
      playsInline
      className="fixed inset-0 w-full h-full object-cover pointer-events-none z-0 opacity-100"
    >
      <source src="/videos/vecteezy_football-stadium-at-night-an-imaginary-stadium-is-modelled_19638366.webm" type="video/webm" />
    </video>
  );
}
