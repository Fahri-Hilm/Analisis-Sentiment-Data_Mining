"use client";

export function GlowingOrbs() {
  return (
    <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
      {/* Large blue orb */}
      <div 
        className="absolute w-96 h-96 rounded-full opacity-20 animate-pulse"
        style={{
          background: "radial-gradient(circle, rgba(59, 130, 246, 0.4) 0%, transparent 70%)",
          top: "10%",
          left: "5%",
          filter: "blur(60px)",
          animation: "float 8s ease-in-out infinite",
        }}
      />
      
      {/* Purple orb */}
      <div 
        className="absolute w-80 h-80 rounded-full opacity-15"
        style={{
          background: "radial-gradient(circle, rgba(139, 92, 246, 0.5) 0%, transparent 70%)",
          top: "50%",
          right: "10%",
          filter: "blur(50px)",
          animation: "float 10s ease-in-out infinite reverse",
        }}
      />
      
      {/* Cyan orb */}
      <div 
        className="absolute w-64 h-64 rounded-full opacity-20"
        style={{
          background: "radial-gradient(circle, rgba(6, 182, 212, 0.4) 0%, transparent 70%)",
          bottom: "20%",
          left: "15%",
          filter: "blur(40px)",
          animation: "float 12s ease-in-out infinite",
        }}
      />
      
      {/* Green orb */}
      <div 
        className="absolute w-48 h-48 rounded-full opacity-15"
        style={{
          background: "radial-gradient(circle, rgba(16, 185, 129, 0.4) 0%, transparent 70%)",
          top: "30%",
          right: "30%",
          filter: "blur(35px)",
          animation: "float 9s ease-in-out infinite reverse",
        }}
      />

      {/* Small accent orbs */}
      <div 
        className="absolute w-32 h-32 rounded-full opacity-25"
        style={{
          background: "radial-gradient(circle, rgba(245, 158, 11, 0.3) 0%, transparent 70%)",
          bottom: "40%",
          right: "5%",
          filter: "blur(25px)",
          animation: "float 7s ease-in-out infinite",
        }}
      />

      <style jsx>{`
        @keyframes float {
          0%, 100% {
            transform: translateY(0) translateX(0);
          }
          25% {
            transform: translateY(-20px) translateX(10px);
          }
          50% {
            transform: translateY(10px) translateX(-10px);
          }
          75% {
            transform: translateY(-10px) translateX(5px);
          }
        }
      `}</style>
    </div>
  );
}
