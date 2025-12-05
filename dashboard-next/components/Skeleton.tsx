"use client";

interface SkeletonProps {
  className?: string;
  variant?: "text" | "circular" | "rectangular" | "card";
}

export function Skeleton({ className = "", variant = "rectangular" }: SkeletonProps) {
  const baseClasses = "animate-pulse bg-gradient-to-r from-slate-700 via-slate-600 to-slate-700 bg-[length:200%_100%]";
  
  const variantClasses = {
    text: "h-4 rounded",
    circular: "rounded-full",
    rectangular: "rounded-lg",
    card: "rounded-xl",
  };

  return (
    <div 
      className={`${baseClasses} ${variantClasses[variant]} ${className}`}
      style={{
        animation: "shimmer 1.5s infinite",
      }}
    />
  );
}

export function StatCardSkeleton() {
  return (
    <div className="bg-gradient-to-br from-[#1a2942]/80 to-[#0f1c2e]/80 backdrop-blur-md rounded-xl p-6 border border-blue-500/20">
      <div className="flex items-center gap-3 mb-4">
        <Skeleton variant="rectangular" className="w-12 h-12 rounded-xl" />
      </div>
      <Skeleton variant="text" className="w-20 h-3 mb-2" />
      <div className="flex items-end justify-between">
        <Skeleton variant="text" className="w-24 h-8" />
        <Skeleton variant="text" className="w-12 h-4" />
      </div>
    </div>
  );
}

export function ChartSkeleton() {
  return (
    <div className="bg-gradient-to-br from-[#1a2942]/80 to-[#0f1c2e]/80 backdrop-blur-md rounded-xl p-6 border border-blue-500/20">
      <div className="flex justify-between items-center mb-6">
        <div>
          <Skeleton variant="text" className="w-40 h-5 mb-2" />
          <Skeleton variant="text" className="w-32 h-3" />
        </div>
        <div className="flex gap-4">
          <Skeleton variant="text" className="w-16 h-3" />
          <Skeleton variant="text" className="w-16 h-3" />
          <Skeleton variant="text" className="w-16 h-3" />
        </div>
      </div>
      <div className="space-y-4">
        <Skeleton variant="rectangular" className="w-full h-12" />
        <Skeleton variant="rectangular" className="w-3/4 h-12" />
        <Skeleton variant="rectangular" className="w-1/4 h-12" />
      </div>
    </div>
  );
}

export function SectionSkeleton() {
  return (
    <div className="bg-gradient-to-br from-[#1a2942]/80 to-[#0f1c2e]/80 backdrop-blur-md rounded-xl p-6 border border-blue-500/20">
      <Skeleton variant="text" className="w-40 h-5 mb-4" />
      <div className="grid grid-cols-2 gap-3">
        {[...Array(6)].map((_, i) => (
          <div key={i} className="bg-[#0f1c2e] rounded-lg p-3 border border-blue-500/10">
            <div className="flex items-center justify-between mb-2">
              <Skeleton variant="circular" className="w-8 h-8" />
              <Skeleton variant="text" className="w-12 h-5" />
            </div>
            <Skeleton variant="text" className="w-20 h-3" />
          </div>
        ))}
      </div>
    </div>
  );
}

export function InsightSkeleton() {
  return (
    <div className="bg-gradient-to-br from-slate-700/20 to-slate-800/10 rounded-xl p-4 border border-slate-500/20">
      <div className="flex items-start gap-3">
        <Skeleton variant="circular" className="w-10 h-10 flex-shrink-0" />
        <div className="flex-1">
          <Skeleton variant="text" className="w-32 h-4 mb-2" />
          <Skeleton variant="text" className="w-full h-3 mb-1" />
          <Skeleton variant="text" className="w-3/4 h-3" />
        </div>
      </div>
    </div>
  );
}

export default Skeleton;
