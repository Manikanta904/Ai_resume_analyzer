
import { motion } from 'motion/react';
import { Sparkles, Brain, Cpu } from 'lucide-react';

export function LoadingScreen() {
  return (
    <div className="min-h-screen relative overflow-hidden bg-gradient-to-br from-violet-50 via-fuchsia-50 to-pink-50 dark:from-slate-950 dark:via-violet-950 dark:to-fuchsia-950 flex items-center justify-center">
      <div className="relative z-10 text-center">
        {/* Animated Icons */}
        <div className="relative w-40 h-40 mx-auto mb-8">
          <motion.div
            className="absolute inset-0 flex items-center justify-center"
            animate={{ rotate: 360 }}
            transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
          >
            <Brain className="w-24 h-24 text-violet-500 dark:text-violet-400" />
          </motion.div>
          <motion.div
            className="absolute inset-0 flex items-center justify-center"
            animate={{ rotate: -360 }}
            transition={{ duration: 4, repeat: Infinity, ease: 'linear' }}
          >
            <Cpu className="w-40 h-40 text-fuchsia-500/40 dark:text-fuchsia-400/40" />
          </motion.div>
          <motion.div
            className="absolute -top-6 -right-6"
            animate={{
              scale: [1, 1.3, 1],
              opacity: [1, 0.5, 1],
              rotate: [0, 360]
            }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            <Sparkles className="w-12 h-12 text-amber-500 dark:text-amber-400" />
          </motion.div>
          <motion.div
            className="absolute -bottom-6 -left-6"
            animate={{
              scale: [1, 1.3, 1],
              opacity: [1, 0.5, 1],
              rotate: [0, -360]
            }}
            transition={{ duration: 2, repeat: Infinity, delay: 1 }}
          >
            <Sparkles className="w-12 h-12 text-pink-500 dark:text-pink-400" />
          </motion.div>

          {/* Pulsing glow */}
          <motion.div
            className="absolute inset-0 bg-gradient-to-r from-violet-500/30 to-fuchsia-500/30 rounded-full blur-3xl"
            animate={{ scale: [1, 1.5, 1], opacity: [0.3, 0.6, 0.3] }}
            transition={{ duration: 2, repeat: Infinity }}
          />
        </div>

        {/* Loading Text */}
        <motion.h2
          className="text-4xl font-bold bg-gradient-to-r from-violet-600 via-fuchsia-600 to-pink-600 dark:from-violet-400 dark:via-fuchsia-400 dark:to-pink-400 bg-clip-text text-transparent mb-6"
          animate={{ opacity: [1, 0.5, 1] }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          ✨ Analyzing Your Resume...
        </motion.h2>

        {/* Progress Steps */}
        <div className="space-y-4 max-w-md mx-auto">
          {['Parsing document', 'Extracting skills', 'Matching with job description', 'Generating insights'].map((step, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.3 }}
              className="flex items-center gap-3 text-gray-800 dark:text-gray-200 font-medium text-lg"
            >
              <motion.div
                className="w-3 h-3 rounded-full bg-gradient-to-r from-violet-500 to-fuchsia-500"
                animate={{ scale: [1, 1.8, 1], opacity: [0.5, 1, 0.5] }}
                transition={{
                  duration: 1.5,
                  repeat: Infinity,
                  delay: index * 0.3
                }}
              />
              {step}
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}

