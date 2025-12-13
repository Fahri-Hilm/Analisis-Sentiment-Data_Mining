import { motion } from 'framer-motion';
import { CheckCircle, XCircle, AlertCircle, Loader2 } from 'lucide-react';

export const ProgressIndicator = ({ progress, label }: { progress: number; label: string }) => (
  <div className="mb-4">
    <div className="flex justify-between text-sm mb-2">
      <span className="text-slate-300">{label}</span>
      <span className="text-blue-400">{progress}%</span>
    </div>
    <div className="w-full bg-slate-700 rounded-full h-2">
      <motion.div
        className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full"
        initial={{ width: 0 }}
        animate={{ width: `${progress}%` }}
        transition={{ duration: 1, ease: "easeOut" }}
      />
    </div>
  </div>
);

export const StatusIndicator = ({ type, message }: { type: 'success' | 'error' | 'warning' | 'loading'; message: string }) => {
  const configs = {
    success: { icon: CheckCircle, color: 'text-green-400', bg: 'bg-green-500/10', border: 'border-green-500/20' },
    error: { icon: XCircle, color: 'text-red-400', bg: 'bg-red-500/10', border: 'border-red-500/20' },
    warning: { icon: AlertCircle, color: 'text-amber-400', bg: 'bg-amber-500/10', border: 'border-amber-500/20' },
    loading: { icon: Loader2, color: 'text-blue-400', bg: 'bg-blue-500/10', border: 'border-blue-500/20' }
  };

  const config = configs[type];
  const Icon = config.icon;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex items-center gap-3 p-3 rounded-lg border ${config.bg} ${config.border}`}
    >
      <Icon className={`w-5 h-5 ${config.color} ${type === 'loading' ? 'animate-spin' : ''}`} />
      <span className="text-slate-300">{message}</span>
    </motion.div>
  );
};

export const InfiniteScroll = ({ children, onLoadMore, hasMore, loading }: {
  children: React.ReactNode;
  onLoadMore: () => void;
  hasMore: boolean;
  loading: boolean;
}) => {
  return (
    <div className="space-y-4">
      {children}
      {hasMore && (
        <div className="flex justify-center py-4">
          {loading ? (
            <StatusIndicator type="loading" message="Memuat data..." />
          ) : (
            <button
              onClick={onLoadMore}
              className="px-6 py-2 bg-blue-500/20 border border-blue-500/30 rounded-lg text-blue-400 hover:bg-blue-500/30 transition-colors"
            >
              Muat Lebih Banyak
            </button>
          )}
        </div>
      )}
    </div>
  );
};
