import { motion } from 'framer-motion';

export const SkeletonChart = () => (
  <div className="h-80 flex items-center justify-center">
    <motion.div 
      className="w-16 h-16 border-4 border-blue-500/20 border-t-blue-500 rounded-full"
      animate={{ rotate: 360 }}
      transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
    />
  </div>
);

export const PulseCard = ({ children, delay = 0 }: { children: React.ReactNode, delay?: number }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ delay, duration: 0.5 }}
    whileHover={{ scale: 1.02, transition: { duration: 0.2 } }}
    className="glass-card rounded-2xl p-6 border border-slate-800/50 hover:border-blue-500/30 transition-all duration-300"
  >
    {children}
  </motion.div>
);

export const FloatingElements = () => (
  <div className="fixed inset-0 pointer-events-none overflow-hidden">
    {[...Array(6)].map((_, i) => (
      <motion.div
        key={i}
        className="absolute w-2 h-2 bg-blue-400/20 rounded-full"
        style={{
          left: `${Math.random() * 100}%`,
          top: `${Math.random() * 100}%`,
        }}
        animate={{
          y: [-20, 20],
          opacity: [0.2, 0.8, 0.2],
        }}
        transition={{
          duration: 3 + Math.random() * 2,
          repeat: Infinity,
          delay: Math.random() * 2,
        }}
      />
    ))}
  </div>
);
