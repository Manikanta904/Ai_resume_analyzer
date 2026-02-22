import { motion } from 'motion/react';
import { Check, X } from 'lucide-react';



export function SkillChip({ skill, type, delay = 0 }) {
  const isMatched = type === 'matched';

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay, type: 'spring' }}
      whileHover={{ scale: 1.05 }}
      className={`relative group inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition-all duration-300 ${isMatched
          ? 'bg-green-500/20 dark:bg-green-500/30 text-green-700 dark:text-green-300 border border-green-500/50'
          : 'bg-red-500/20 dark:bg-red-500/30 text-red-700 dark:text-red-300 border border-red-500/50'
        }`}
    >
      {isMatched ? (
        <Check className="w-4 h-4" />
      ) : (
        <X className="w-4 h-4" />
      )}
      {skill}
      <div
        className={`absolute inset-0 rounded-full blur-lg opacity-0 group-hover:opacity-50 transition-opacity duration-300 ${isMatched ? 'bg-green-500' : 'bg-red-500'
          }`}
      />
    </motion.div>
  );
}

