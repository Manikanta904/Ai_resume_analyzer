
import { motion } from 'motion/react';
import { ATSScoreRing } from './ats-score-ring';
import { SkillChip } from './skill-chip';
import { ScrollToTop } from './scroll-to-top';
import { Briefcase, Target, TrendingUp, ArrowRight, ChevronDown, ChevronUp, Lightbulb, Sparkles } from 'lucide-react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { useState } from 'react';

export function AnalysisDashboard({ data, onImprove }) {
  const [expandedInsights, setExpandedInsights] = useState([]);

  const skillCoverageData = [
    { name: 'Matched', value: data.matchedSkills.length, color: '#10b981' },
    { name: 'Missing', value: data.missingSkills.length, color: '#ef4444' },
  ];

  const skillComparisonData = [
    {
      category: 'Technical',
      resume: data.matchedSkills.filter(s => !s.toLowerCase().includes('communication') && !s.toLowerCase().includes('leadership')).length,
      jd: data.matchedSkills.length + data.missingSkills.filter(s => !s.toLowerCase().includes('communication') && !s.toLowerCase().includes('leadership')).length,
    },
    {
      category: 'Soft Skills',
      resume: data.matchedSkills.filter(s => s.toLowerCase().includes('communication') || s.toLowerCase().includes('leadership')).length,
      jd: 3,
    },
  ];

  const toggleInsight = (index) => {
    setExpandedInsights((prev) =>
      prev.includes(index) ? prev.filter((i) => i !== index) : [...prev, index]
    );
  };

  return (
    <div className="min-h-screen relative overflow-hidden bg-transparent py-12 px-6">
      <div className="max-w-7xl mx-auto relative z-10">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8 sm:mb-12 px-4"
        >
          <div className="flex items-center justify-center gap-2 sm:gap-4 mb-4 text-center">
            <motion.div
              initial={{ scale: 0, rotate: -180 }}
              animate={{ scale: 1, rotate: 0 }}
              transition={{ type: "spring", stiffness: 260, damping: 20 }}
              className="hidden sm:block"
            >
              <Sparkles className="w-8 h-8 sm:w-10 h-10 text-violet-600 dark:text-violet-400" />
            </motion.div>
            <h1 className="text-3xl sm:text-4xl md:text-5xl font-black bg-gradient-to-r from-violet-700 via-fuchsia-700 to-pink-700 dark:from-violet-400 dark:via-fuchsia-400 dark:to-pink-400 bg-clip-text text-transparent tracking-tight">
              Analysis Results
            </h1>
            <motion.div
              initial={{ scale: 0, rotate: 180 }}
              animate={{ scale: 1, rotate: 0 }}
              transition={{ type: "spring", stiffness: 260, damping: 20 }}
              className="hidden sm:block"
            >
              <Sparkles className="w-8 h-8 sm:w-10 h-10 text-pink-600 dark:text-pink-400" />
            </motion.div>
          </div>
          <p className="text-base sm:text-lg font-medium text-violet-700 dark:text-violet-300">✨ AI-powered insights for your resume ✨</p>
        </motion.div>

        {/* Top Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8 sm:mb-12 px-4 sm:px-0">
          {/* ATS Score */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.1 }}
            className="col-span-1 flex justify-center items-center p-6 sm:p-8 rounded-3xl backdrop-blur-xl bg-white/90 dark:bg-slate-900/80 border-2 border-white dark:border-violet-700/50 shadow-[0_20px_50px_rgba(139,92,246,0.15)] dark:shadow-2xl"
          >
            <div className="scale-75 sm:scale-100">
              <ATSScoreRing score={data.atsScore} size={240} />
            </div>
          </motion.div>

          {/* Match Percentage & Role */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="md:col-span-2 space-y-6"
          >
            {/* Match Percentage */}
            <div className="relative group p-6 sm:p-8 rounded-3xl backdrop-blur-xl bg-white/90 dark:bg-slate-900/80 border-2 border-white dark:border-violet-700/50 overflow-hidden shadow-[0_20px_50px_rgba(139,92,246,0.15)] dark:shadow-xl">
              <div className="absolute inset-0 bg-gradient-to-r from-violet-500/10 to-fuchsia-500/10 dark:from-violet-500/20 dark:to-fuchsia-500/20 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
              <div className="relative flex items-center justify-between">
                <div className="flex items-center gap-3 sm:gap-4">
                  <div className="p-3 sm:p-5 rounded-2xl bg-gradient-to-br from-violet-600 to-fuchsia-700 shadow-xl shadow-violet-500/20">
                    <Target className="w-6 h-6 sm:w-10 h-10 text-white" />
                  </div>
                  <div>
                    <div className="text-xs sm:text-sm font-black text-violet-700 dark:text-violet-400 mb-1 uppercase tracking-widest">Resume Match</div>
                    <div className="text-4xl sm:text-5xl md:text-6xl font-black bg-gradient-to-r from-violet-700 to-fuchsia-700 dark:from-violet-400 dark:to-fuchsia-400 bg-clip-text text-transparent">
                      {data.matchPercentage}%
                    </div>
                  </div>
                </div>
                <TrendingUp className="w-10 h-10 sm:w-16 h-16 text-violet-500/20 dark:text-violet-500/40" />
              </div>
            </div>

            {/* Detected Role */}
            <div className="relative group p-6 sm:p-8 rounded-3xl backdrop-blur-xl bg-white/90 dark:bg-slate-900/80 border-2 border-white dark:border-pink-700/50 overflow-hidden shadow-[0_20px_50px_rgba(236,72,153,0.15)] dark:shadow-xl">
              <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-pink-500/10 dark:from-blue-500/20 dark:to-pink-500/20 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
              <div className="relative flex items-center gap-3 sm:gap-4">
                <div className="p-3 sm:p-5 rounded-2xl bg-gradient-to-br from-blue-600 to-pink-700 shadow-xl shadow-pink-500/20">
                  <Briefcase className="w-6 h-6 sm:w-10 h-10 text-white" />
                </div>
                <div>
                  <div className="text-xs sm:text-sm font-black text-pink-700 dark:text-pink-400 mb-1 uppercase tracking-widest">Detected Role</div>
                  <div className="text-xl sm:text-2xl md:text-3xl font-black text-slate-900 dark:text-white leading-tight underline decoration-pink-500/30 decoration-4">
                    {data.detectedRole}
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Skills Analysis */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="mb-8 sm:mb-12 p-5 sm:p-8 rounded-3xl backdrop-blur-xl bg-white/90 dark:bg-slate-900/80 border-2 border-white dark:border-violet-700/50 shadow-[0_20px_50px_rgba(139,92,246,0.15)] dark:shadow-xl mx-4 sm:mx-0"
        >
          <h2 className="text-2xl sm:text-3xl font-black bg-gradient-to-r from-violet-700 to-fuchsia-700 dark:from-violet-400 dark:to-fuchsia-400 bg-clip-text text-transparent mb-6">
            Skill Analysis
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 sm:gap-8 mb-8">
            {/* Matched Skills */}
            <div className="space-y-4">
              <h3 className="text-base sm:text-lg font-bold text-green-700 dark:text-green-400 flex items-center gap-2">
                <div className="w-2.5 h-2.5 rounded-full bg-green-500 animate-pulse" />
                Matched Skills ({data.matchedSkills.length})
              </h3>
              <div className="flex flex-wrap gap-2 sm:gap-3">
                {data.matchedSkills.map((skill, index) => (
                  <SkillChip key={index} skill={skill} type="matched" delay={index * 0.05} />
                ))}
              </div>
            </div>

            {/* Missing Skills */}
            <div className="space-y-4">
              <h3 className="text-base sm:text-lg font-bold text-red-700 dark:text-red-400 flex items-center gap-2">
                <div className="w-2.5 h-2.5 rounded-full bg-red-500 animate-pulse" />
                Missing Skills ({data.missingSkills.length})
              </h3>
              <div className="flex flex-wrap gap-2 sm:gap-3">
                {data.missingSkills.map((skill, index) => (
                  <SkillChip key={index} skill={skill} type="missing" delay={index * 0.05} />
                ))}
              </div>
            </div>
          </div>

          {/* Must-Have vs Good-to-Have */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6">
            <div className="p-5 sm:p-6 rounded-2xl bg-gradient-to-br from-orange-500/15 to-red-500/15 dark:from-orange-500/25 dark:to-red-500/25 border-2 border-orange-400/40 shadow-lg">
              <h3 className="text-lg sm:text-xl font-black text-orange-700 dark:text-orange-400 mb-3 flex items-center gap-2">
                🔥 Must-Have Skills
              </h3>
              <ul className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {data.mustHaveSkills.map((skill, index) => (
                  <li key={index} className="text-gray-800 dark:text-gray-200 flex items-center gap-2 text-sm sm:text-base font-semibold">
                    <div className="w-1.5 h-1.5 rounded-full bg-orange-500 shrink-0" />
                    {skill}
                  </li>
                ))}
              </ul>
            </div>
            <div className="p-5 sm:p-6 rounded-2xl bg-gradient-to-br from-blue-500/15 to-cyan-500/15 dark:from-blue-500/25 dark:to-cyan-500/25 border-2 border-blue-400/40 shadow-lg">
              <h3 className="text-lg sm:text-xl font-black text-blue-700 dark:text-blue-400 mb-3 flex items-center gap-2">
                ✨ Good-to-Have Skills
              </h3>
              <ul className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {data.goodToHaveSkills.map((skill, index) => (
                  <li key={index} className="text-gray-800 dark:text-gray-200 flex items-center gap-2 text-sm sm:text-base font-semibold">
                    <div className="w-1.5 h-1.5 rounded-full bg-blue-500 shrink-0" />
                    {skill}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </motion.div>

        {/* Charts */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 sm:gap-8 mb-8 sm:mb-12 mx-4 sm:mx-0">
          {/* Pie Chart */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
            className="p-6 sm:p-8 rounded-3xl backdrop-blur-xl bg-white/90 dark:bg-slate-900/80 border-2 border-white dark:border-violet-700/50 shadow-[0_20px_50px_rgba(139,92,246,0.1)] dark:shadow-xl"
          >
            <h3 className="text-xl sm:text-2xl font-black text-slate-900 dark:text-white mb-6">📊 Skill Coverage</h3>
            <div className="h-[250px] sm:h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={skillCoverageData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {skillCoverageData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </motion.div>

          {/* Bar Chart */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.5 }}
            className="p-6 sm:p-8 rounded-3xl backdrop-blur-xl bg-white/90 dark:bg-slate-900/80 border-2 border-white dark:border-fuchsia-700/50 shadow-[0_20px_50px_rgba(236,72,153,0.1)] dark:shadow-xl"
          >
            <h3 className="text-xl sm:text-2xl font-black text-slate-900 dark:text-white mb-6">📈 Resume vs Job Description</h3>
            <div className="h-[250px] sm:h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={skillComparisonData}>
                  <XAxis dataKey="category" stroke="#9ca3af" fontSize={12} />
                  <YAxis stroke="#9ca3af" fontSize={12} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'rgba(0, 0, 0, 0.8)',
                      border: 'none',
                      borderRadius: '12px',
                      color: '#fff',
                      fontSize: '12px'
                    }}
                  />
                  <Legend wrapperStyle={{ fontSize: '12px' }} />
                  <Bar dataKey="resume" fill="#8b5cf6" name="Your Resume" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="jd" fill="#ec4899" name="Job Description" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </motion.div>
        </div>

        {/* AI Insights & Suggestions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="mb-8 sm:mb-12 p-5 sm:p-8 rounded-3xl backdrop-blur-xl bg-white/90 dark:bg-slate-900/80 border-2 border-white dark:border-violet-700/50 shadow-[0_20px_50px_rgba(139,92,246,0.15)] dark:shadow-xl mx-4 sm:mx-0"
        >
          <div className="flex items-center gap-3 mb-6">
            <div className="p-3 sm:p-4 rounded-xl bg-gradient-to-br from-amber-500 to-orange-600 shadow-xl shadow-amber-500/20">
              <Lightbulb className="w-6 h-6 sm:w-8 h-8 text-white" />
            </div>
            <h2 className="text-2xl sm:text-3xl font-black bg-gradient-to-r from-amber-700 to-orange-700 dark:from-amber-400 dark:to-orange-400 bg-clip-text text-transparent">
              💡 AI Insights & Suggestions
            </h2>
          </div>

          <div className="space-y-4">
            {data.insights.map((insight, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.7 + index * 0.1 }}
                className="border-2 border-violet-200 dark:border-violet-700 rounded-2xl overflow-hidden shadow-md"
              >
                <button
                  onClick={() => toggleInsight(index)}
                  className="w-full p-4 sm:p-6 flex items-center justify-between bg-gradient-to-r from-violet-50 to-fuchsia-50 dark:from-slate-800 dark:to-violet-900 hover:from-violet-100 hover:to-fuchsia-100 dark:hover:from-slate-700 dark:hover:to-violet-800 transition-colors duration-300 gap-4"
                >
                  <span className="text-left font-bold text-gray-900 dark:text-white text-sm sm:text-base">{insight}</span>
                  {expandedInsights.includes(index) ? (
                    <ChevronUp className="w-5 h-5 text-violet-600 dark:text-violet-400 shrink-0" />
                  ) : (
                    <ChevronDown className="w-5 h-5 text-violet-600 dark:text-violet-400 shrink-0" />
                  )}
                </button>
                {expandedInsights.includes(index) && (
                  <motion.div
                    initial={{ height: 0 }}
                    animate={{ height: 'auto' }}
                    className="p-4 sm:p-6 bg-gradient-to-r from-violet-500/10 to-fuchsia-500/10 dark:from-violet-500/20 dark:to-fuchsia-500/20 border-t-2 border-violet-200 dark:border-violet-700"
                  >
                    <p className="text-gray-800 dark:text-gray-200 font-medium text-sm sm:text-base leading-relaxed">
                      {data.suggestions[index] || 'Consider adding more details about your experience with this skill.'}
                    </p>
                  </motion.div>
                )}
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Improve Resume CTA */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="text-center px-4"
        >
          <motion.button
            onClick={onImprove}
            className="group relative px-10 sm:px-16 py-4 sm:py-6 rounded-2xl font-black text-lg sm:text-xl text-white overflow-hidden shadow-2xl transition-all duration-300"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.98 }}
          >
            <div className="absolute inset-0 bg-gradient-to-r from-violet-600 via-fuchsia-600 to-pink-600" />
            <motion.div
              className="absolute inset-0 bg-gradient-to-r from-violet-500 via-fuchsia-500 to-pink-500 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
            />
            <div className="absolute inset-0 opacity-0 group-hover:opacity-100 blur-3xl bg-gradient-to-r from-violet-600 to-pink-600 transition-opacity duration-300" />
            <span className="relative flex items-center justify-center gap-3">
              <Sparkles className="w-5 h-5 sm:w-6 h-6" />
              Improve Resume with AI
              <motion.div
                animate={{ x: [0, 5, 0] }}
                transition={{ duration: 1.5, repeat: Infinity }}
              >
                <ArrowRight className="w-5 h-5 sm:w-6 h-6" />
              </motion.div>
            </span>
          </motion.button>
        </motion.div>
      </div>

      <ScrollToTop />
    </div>
  );
}

