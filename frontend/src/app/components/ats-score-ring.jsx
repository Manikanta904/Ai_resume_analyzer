import { motion } from 'motion/react';
import { useEffect, useState } from 'react';

export function ATSScoreRing({ score, size = 280 }) {
  const [displayScore, setDisplayScore] = useState(0);
  const radius = (size - 40) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (displayScore / 100) * circumference;

  useEffect(() => {
    const timer = setTimeout(() => {
      let current = 0;
      const interval = setInterval(() => {
        current += 1;
        setDisplayScore(current);
        if (current >= score) {
          clearInterval(interval);
        }
      }, 20);
      return () => clearInterval(interval);
    }, 500);
    return () => clearTimeout(timer);
  }, [score]);

  const getScoreColor = (score) => {
    if (score >= 80) return { main: '#10b981', glow: 'rgba(16, 185, 129, 0.6)' };
    if (score >= 60) return { main: '#f59e0b', glow: 'rgba(245, 158, 11, 0.6)' };
    return { main: '#ef4444', glow: 'rgba(239, 68, 68, 0.6)' };
  };

  const colors = getScoreColor(displayScore);

  return (
    <div className="relative inline-flex items-center justify-center">
      {/* Pulsing glow effect */}
      <motion.div
        className="absolute inset-0 rounded-full"
        style={{ background: `radial-gradient(circle, ${colors.glow} 0%, transparent 70%)` }}
        animate={{ scale: [1, 1.2, 1], opacity: [0.5, 0.8, 0.5] }}
        transition={{ duration: 2, repeat: Infinity }}
      />
      <svg width={size} height={size} className="transform -rotate-90">
        {/* Background circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="rgba(139, 92, 246, 0.15)"
          strokeWidth="24"
        />
        {/* Progress circle */}
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={colors.main}
          strokeWidth="24"
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 2, ease: 'easeOut' }}
          style={{
            filter: `drop-shadow(0 0 16px ${colors.glow})`,
          }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.5, type: 'spring' }}
          className="text-6xl sm:text-7xl md:text-8xl font-black bg-gradient-to-br from-violet-600 via-fuchsia-600 to-pink-600 dark:from-violet-400 dark:via-fuchsia-400 dark:to-pink-400 bg-clip-text text-transparent leading-none"
        >
          {displayScore}
        </motion.div>
        <div className="text-violet-700 dark:text-violet-400 font-bold text-sm sm:text-base md:text-lg mt-1 sm:mt-2 uppercase tracking-widest">ATS Score</div>
      </div>
    </div>
  );
}
