import { motion, AnimatePresence } from 'motion/react';
import { Check, X, Info, AlertCircle } from 'lucide-react';
import { useEffect } from 'react';

export function Toast({ message, type = 'success', isVisible, onClose }) {
  useEffect(() => {
    if (isVisible) {
      const timer = setTimeout(() => {
        onClose();
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [isVisible, onClose]);

  const icons = {
    success: Check,
    error: X,
    info: Info,
    warning: AlertCircle,
  };

  const colors = {
    success: 'from-green-500 to-emerald-600',
    error: 'from-red-500 to-rose-600',
    info: 'from-blue-500 to-cyan-600',
    warning: 'from-orange-500 to-amber-600',
  };

  const Icon = icons[type] || Check;

  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          initial={{ opacity: 0, y: 50, scale: 0.9 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: 50, scale: 0.9 }}
          className="fixed top-8 left-1/2 -translate-x-1/2 z-[100]"
        >
          <div className={`flex items-center gap-3 px-6 py-4 rounded-2xl backdrop-blur-xl bg-gradient-to-r ${colors[type]} text-white shadow-2xl`}>
            <div className="p-2 rounded-full bg-white/20">
              <Icon className="w-5 h-5" />
            </div>
            <p className="font-medium">{message}</p>
            <button onClick={onClose} className="ml-2 hover:opacity-70 transition-opacity">
              <X className="w-4 h-4" />
            </button>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
