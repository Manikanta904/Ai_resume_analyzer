import { Moon, Sun } from 'lucide-react';
import { motion } from 'motion/react';
import { useTheme } from './theme-provider';

export function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();

  return (
    <motion.button
      onClick={toggleTheme}
      className="fixed top-6 right-6 z-50 p-4 rounded-2xl bg-gradient-to-r from-violet-500/20 to-fuchsia-500/20 dark:from-violet-500/30 dark:to-fuchsia-500/30 backdrop-blur-xl border border-violet-300/30 dark:border-violet-400/30 shadow-2xl hover:shadow-violet-500/50 transition-all duration-300 group"
      whileHover={{ scale: 1.1, rotate: 5 }}
      whileTap={{ scale: 0.95 }}
    >
      <motion.div
        initial={false}
        animate={{ rotate: theme === 'dark' ? 0 : 180 }}
        transition={{ duration: 0.5, ease: [0.4, 0, 0.2, 1] }}
      >
        {theme === 'dark' ? (
          <Moon className="w-6 h-6 text-violet-300" />
        ) : (
          <Sun className="w-6 h-6 text-amber-500" />
        )}
      </motion.div>
      <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-violet-500/30 to-fuchsia-500/30 opacity-0 group-hover:opacity-100 blur-xl transition-opacity duration-300" />
    </motion.button>
  );
}
