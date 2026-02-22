import { motion } from 'motion/react';
import { useEffect, useState } from 'react';
import { useTheme } from './theme-provider';

export function AnimatedBackground() {
  const [particles, setParticles] = useState([]);
  const { theme } = useTheme();

  useEffect(() => {
    // Balanced density for a premium feel
    const newParticles = Array.from({ length: 80 }, (_, i) => ({
      id: i,
      x: Math.random() * 100,
      y: Math.random() * 100,
      delay: Math.random() * 20,
      size: Math.random() * 4 + 1,
      duration: Math.random() * 10 + 15,
      opacity: Math.random() * 0.5 + 0.3,
      blur: Math.random() > 0.8 ? 'blur(1px)' : 'none',
      drift: Math.random() * 10 - 5,
      twinkle: Math.random() > 0.7,
      color: Math.random() > 0.6 ? '#60a5fa' : '#3b82f6' // Default starting colors
    }));
    setParticles(newParticles);
  }, []);

  return (
    <>
      {/* Background Layer: Gradients, Orbs, and Snow */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
        <div className="absolute inset-0 bg-gradient-to-br from-blue-100 via-indigo-50 to-purple-100 dark:from-[#080212] dark:via-[#110624] dark:to-[#090315]" />

        {/* Decorative large orbs */}
        <motion.div
          className="absolute top-0 -left-20 w-[800px] h-[800px] bg-violet-400/20 dark:bg-violet-600/10 rounded-full blur-[120px]"
          animate={{
            scale: [1, 1.1, 1],
            opacity: [0.2, 0.4, 0.2],
          }}
          transition={{ duration: 20, repeat: Infinity }}
        />
        <motion.div
          className="absolute bottom-0 -right-20 w-[800px] h-[800px] bg-blue-400/20 dark:bg-blue-600/10 rounded-full blur-[120px]"
          animate={{
            scale: [1.1, 1, 1.1],
            opacity: [0.3, 0.5, 0.3],
          }}
          transition={{ duration: 25, repeat: Infinity }}
        />

        {/* Snow Particles */}
        {particles.map((particle) => (
          <motion.div
            key={particle.id}
            className="absolute rounded-full"
            style={{
              width: particle.size,
              height: particle.size,
              left: `${particle.x}vw`,
              backgroundColor: theme === 'dark' ? '#ffffff' : (particle.id % 2 === 0 ? '#3b82f6' : '#6366f1'),
              opacity: theme === 'dark' ? particle.opacity : particle.opacity + 0.2,
              filter: particle.blur,
              boxShadow: theme === 'dark'
                ? `0 0 10px rgba(255,255,255,0.8)`
                : `0 0 8px rgba(59,130,246,0.3)`,
            }}
            initial={{ y: '-10vh' }}
            animate={{
              y: ['-10vh', '110vh'],
              x: ['0vw', `${(Math.sin(particle.id) * 5) + particle.drift}vw`],
              scale: particle.twinkle ? [1, 1.3, 1] : 1,
            }}
            transition={{
              duration: particle.duration,
              delay: -particle.delay,
              repeat: Infinity,
              ease: 'linear',
              scale: particle.twinkle ? {
                duration: 3 + Math.random() * 2,
                repeat: Infinity,
                ease: "easeInOut"
              } : {}
            }}
          />
        ))}

        <div className="absolute inset-0 opacity-[0.03] dark:opacity-[0.05]"
          style={{
            backgroundImage: 'radial-gradient(circle, #8b5cf6 1px, transparent 1px)',
            backgroundSize: '40px 40px'
          }}
        />
      </div>
    </>
  );
}
