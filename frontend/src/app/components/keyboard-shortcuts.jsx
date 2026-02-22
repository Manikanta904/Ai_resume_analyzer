import { useEffect } from 'react';
import { useTheme } from './theme-provider';



export function KeyboardShortcuts({ onBack }) {
  const { toggleTheme } = useTheme();

  useEffect(() => {
    const handleKeyPress = (e) => {
      // Toggle theme with Ctrl/Cmd + D
      if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
        e.preventDefault();
        toggleTheme();
      }

      // Go back with Escape
      if (e.key === 'Escape' && onBack) {
        onBack();
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [toggleTheme, onBack]);

  return null;
}

