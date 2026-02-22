import { motion } from 'motion/react';
import { Check, X, Download, RotateCcw, Sparkles } from 'lucide-react';
import { useEffect, useState } from 'react';
import { Toast } from './toast-notification';
import { rewriteResume, downloadResume } from '../../services/api';

const fallbackSections = [
  {
    id: 1,
    original: 'Worked on various projects using React and Node.js',
    improved: 'Led development of 5+ enterprise-scale web applications using React.js and Node.js, improving user engagement by 40% and reducing load time by 30%',
    accepted: null,
  },
  {
    id: 2,
    original: 'Team player with good communication skills',
    improved: 'Collaborated cross-functionally with design, product, and QA teams of 15+ members, facilitating agile ceremonies and improving sprint velocity by 25%',
    accepted: null,
  },
  {
    id: 3,
    original: 'Experience with databases',
    improved: 'Designed and optimized PostgreSQL and MongoDB databases handling 1M+ daily transactions, reducing query response time by 50% through strategic indexing',
    accepted: null,
  },
];

const normalizeRewriteSections = (payload) => {
  const data = payload?.data ?? payload ?? {};
  const rewritten = data.rewritten_resume ?? {};

  // Flatten summary, experience, projects into sections
  const sections = [];
  let id = 1;

  // Summary section
  if (rewritten.summary) {
    sections.push({
      id: id++,
      original: 'Professional Summary',
      improved: rewritten.summary,
      accepted: null,
    });
  }

  // Experience sections
  if (Array.isArray(rewritten.experience)) {
    rewritten.experience.forEach((exp) => {
      sections.push({
        id: id++,
        original: `Experience Point ${id - 1}`,
        improved: exp,
        accepted: null,
      });
    });
  }

  // Projects sections
  if (Array.isArray(rewritten.projects)) {
    rewritten.projects.forEach((proj) => {
      sections.push({
        id: id++,
        original: `Project Point ${id - 1}`,
        improved: proj,
        accepted: null,
      });
    });
  }

  return sections.length ? sections : [];
};

export function ImproveResume({ onReanalyze, resumeInput, jdInput }) {
  const [sections, setSections] = useState(fallbackSections);
  const [isLoading, setIsLoading] = useState(false);
  const [showToast, setShowToast] = useState(false);
  const [toastMessage, setToastMessage] = useState('');
  const [toastType, setToastType] = useState('success');

  useEffect(() => {
    const fetchImprovements = async () => {
      if (!resumeInput && !jdInput) return;

      const formData = new FormData();
      if (resumeInput?.file) {
        formData.append('resume_file', resumeInput.file);
      } else if (resumeInput?.text) {
        formData.append('resume_file', new File([resumeInput.text], 'resume.txt', { type: 'text/plain' }));
      }

      if (jdInput?.file) {
        formData.append('jd_file', jdInput.file);
      } else if (jdInput?.text) {
        formData.append('jd_file', new File([jdInput.text], 'jd.txt', { type: 'text/plain' }));
      }

      setIsLoading(true);
      try {
        const response = await rewriteResume(formData);
        const normalizedSections = normalizeRewriteSections(response);
        if (normalizedSections.length) {
          setSections(normalizedSections);
        }
      } catch (error) {
        setToastMessage(error?.message || 'Rewrite request failed.');
        setToastType('error');
        setShowToast(true);
      } finally {
        setIsLoading(false);
      }
    };

    fetchImprovements();
  }, [resumeInput, jdInput]);

  const handleAccept = (id) => {
    setSections(sections.map(s => s.id === id ? { ...s, accepted: true } : s));
    setToastMessage('Improvement accepted!');
    setToastType('success');
    setShowToast(true);
  };

  const handleReject = (id) => {
    setSections(sections.map(s => s.id === id ? { ...s, accepted: false } : s));
    setToastMessage('Improvement rejected');
    setToastType('info');
    setShowToast(true);
  };

  const handleDownload = async () => {
    const acceptedSections = sections.filter(s => s.accepted === true);

    if (!acceptedSections.length) {
      setToastMessage('Select at least one improvement before downloading.');
      setToastType('warning');
      setShowToast(true);
      return;
    }

    try {
      // Construct the rewritten resume structure from accepted sections
      const payload = {
        summary: '',
        experience: [],
        projects: [],
        format: 'pdf',
      };

      acceptedSections.forEach((section) => {
        if (section.original === 'Professional Summary') {
          payload.summary = section.improved;
        } else if (section.original.startsWith('Experience Point')) {
          payload.experience.push(section.improved);
        } else if (section.original.startsWith('Project Point')) {
          payload.projects.push(section.improved);
        }
      });

      const blob = await downloadResume(payload);

      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'improved-resume.pdf';
      a.click();

      setToastMessage('Resume downloaded successfully!');
      setToastType('success');
      setShowToast(true);
    } catch (error) {
      setToastMessage(error?.message || 'Download request failed.');
      setToastType('error');
      setShowToast(true);
    }
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
          <div className="flex items-center justify-center gap-2 sm:gap-4 mb-4">
            <motion.div
              initial={{ scale: 0, rotate: -180 }}
              animate={{ scale: 1, rotate: 0 }}
              transition={{ type: "spring", stiffness: 260, damping: 20 }}
              className="hidden sm:block"
            >
              <Sparkles className="w-8 h-8 sm:w-12 h-12 text-violet-600 dark:text-violet-400" />
            </motion.div>
            <h1 className="text-3xl sm:text-4xl md:text-5xl font-black bg-gradient-to-r from-violet-700 via-fuchsia-700 to-pink-700 dark:from-violet-400 dark:via-fuchsia-400 dark:to-pink-400 bg-clip-text text-transparent tracking-tight leading-tight">
              AI-Optimized Resume
            </h1>
            <motion.div
              initial={{ scale: 0, rotate: 180 }}
              animate={{ scale: 1, rotate: 0 }}
              transition={{ type: "spring", stiffness: 260, damping: 20 }}
              className="hidden sm:block"
            >
              <Sparkles className="w-8 h-8 sm:w-12 h-12 text-pink-600 dark:text-pink-400" />
            </motion.div>
          </div>
          <p className="text-base sm:text-lg font-medium text-violet-700 dark:text-violet-300">✨ Review and apply AI-suggested improvements ✨</p>
        </motion.div>

        {/* Action Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="flex flex-col sm:flex-row justify-center gap-4 mb-8 sm:mb-12 px-4 sm:px-0"
        >
          <motion.button
            onClick={handleDownload}
            disabled={isLoading}
            className="flex items-center justify-center gap-3 px-6 sm:px-8 py-3.5 sm:py-4 rounded-xl bg-gradient-to-r from-emerald-500 to-green-600 text-white font-black text-base sm:text-lg shadow-2xl hover:shadow-emerald-500/50 transition-all duration-300"
            whileHover={{ scale: 1.05, y: -2 }}
            whileTap={{ scale: 0.98 }}
          >
            <Download className="w-5 h-5 sm:w-6 h-6" />
            Download Resume
          </motion.button>
          <motion.button
            onClick={onReanalyze}
            className="flex items-center justify-center gap-3 px-6 sm:px-8 py-3.5 sm:py-4 rounded-xl bg-white/80 dark:bg-slate-900/80 backdrop-blur-xl border-2 border-violet-300 dark:border-violet-700 text-gray-900 dark:text-white font-black text-base sm:text-lg shadow-xl hover:shadow-violet-500/50 transition-all duration-300"
            whileHover={{ scale: 1.05, y: -2 }}
            whileTap={{ scale: 0.98 }}
          >
            <RotateCcw className="w-5 h-5 sm:w-6 h-6" />
            Re-analyze
          </motion.button>
        </motion.div>

        {/* Improvement Sections */}
        <div className="space-y-6 mx-4 sm:mx-0">
          {sections.map((section, index) => (
            <motion.div
              key={section.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 + index * 0.1 }}
              className={`p-5 sm:p-8 rounded-3xl backdrop-blur-xl border-2 transition-all duration-500 shadow-xl ${section.accepted === true
                ? 'bg-emerald-500/15 dark:bg-emerald-500/25 border-emerald-500/60 shadow-emerald-500/20'
                : section.accepted === false
                  ? 'bg-red-500/15 dark:bg-red-500/25 border-red-500/60 shadow-red-500/20'
                  : 'bg-white/90 dark:bg-slate-900/80 border-white dark:border-violet-700/50 shadow-[0_20px_50px_rgba(139,92,246,0.1)]'
                }`}
            >
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 sm:gap-8">
                {/* Original */}
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <div className="px-3 py-1.5 rounded-lg bg-gray-500/20 dark:bg-gray-500/30 text-xs sm:text-sm font-black text-gray-700 dark:text-gray-300 uppercase tracking-wider">
                      📄 Original
                    </div>
                  </div>
                  <div className="p-4 sm:p-6 rounded-2xl bg-white/70 dark:bg-slate-800/70 border-2 border-gray-300 dark:border-gray-700 shadow-md">
                    <p className="text-gray-700 dark:text-gray-300 leading-relaxed text-sm sm:text-base">
                      {section.original}
                    </p>
                  </div>
                </div>

                {/* Improved */}
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <div className="px-3 py-1.5 rounded-lg bg-gradient-to-r from-violet-500 to-fuchsia-500 text-xs sm:text-sm font-black text-white shadow-lg uppercase tracking-wider">
                      ✨ AI Improved
                    </div>
                    <Sparkles className="w-4 h-4 sm:w-5 h-5 text-fuchsia-500 dark:text-fuchsia-400" />
                  </div>
                  <div className="p-4 sm:p-6 rounded-2xl bg-gradient-to-br from-violet-500/15 to-fuchsia-500/15 dark:from-violet-500/25 dark:to-fuchsia-500/25 border-2 border-violet-400/50 shadow-lg">
                    <p className="text-gray-900 dark:text-white leading-relaxed font-bold text-sm sm:text-base">
                      {section.improved}
                    </p>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex flex-row justify-end gap-3 sm:gap-4 mt-6">
                <motion.button
                  onClick={() => handleReject(section.id)}
                  disabled={section.accepted !== null}
                  className={`flex items-center flex-1 sm:flex-none justify-center gap-2 px-4 sm:px-6 py-2.5 sm:py-3 rounded-xl font-bold text-sm sm:text-base transition-all duration-300 ${section.accepted === false
                    ? 'bg-red-500 text-white'
                    : 'bg-red-500/20 dark:bg-red-500/30 text-red-700 dark:text-red-300 hover:bg-red-500/30 dark:hover:bg-red-500/40'
                    } disabled:opacity-50 disabled:cursor-not-allowed`}
                  whileHover={section.accepted === null ? { scale: 1.05 } : {}}
                  whileTap={section.accepted === null ? { scale: 0.95 } : {}}
                >
                  <X className="w-4 h-4 sm:w-5 h-5" />
                  Reject
                </motion.button>
                <motion.button
                  onClick={() => handleAccept(section.id)}
                  disabled={section.accepted !== null}
                  className={`flex items-center flex-1 sm:flex-none justify-center gap-2 px-4 sm:px-6 py-2.5 sm:py-3 rounded-xl font-bold text-sm sm:text-base transition-all duration-300 ${section.accepted === true
                    ? 'bg-green-500 text-white'
                    : 'bg-green-500/20 dark:bg-green-500/30 text-green-700 dark:text-green-300 hover:bg-green-500/30 dark:hover:bg-green-500/40'
                    } disabled:opacity-50 disabled:cursor-not-allowed`}
                  whileHover={section.accepted === null ? { scale: 1.05 } : {}}
                  whileTap={section.accepted === null ? { scale: 0.95 } : {}}
                >
                  <Check className="w-4 h-4 sm:w-5 h-5" />
                  Accept
                </motion.button>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Skill Suggestions Panel */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="mt-8 sm:mt-12 p-6 sm:p-8 rounded-3xl backdrop-blur-xl bg-white/90 dark:bg-slate-900/80 border-2 border-white dark:border-violet-700/50 shadow-[0_20px_50px_rgba(139,92,246,0.15)] dark:shadow-xl mx-4 sm:mx-0"
        >
          <h2 className="text-2xl sm:text-3xl font-black bg-gradient-to-r from-violet-600 to-fuchsia-600 dark:from-violet-400 dark:to-fuchsia-400 bg-clip-text text-transparent mb-6 tracking-tight">
            🎯 Keyword Optimization
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
            <div className="p-5 sm:p-6 rounded-2xl bg-gradient-to-br from-blue-500/15 to-cyan-500/15 dark:from-blue-500/25 dark:to-cyan-500/25 border-2 border-blue-400/40 shadow-lg hover:border-blue-500/60 transition-colors">
              <h3 className="font-black text-lg sm:text-xl text-blue-700 dark:text-blue-400 mb-3">📝 Industry Keywords</h3>
              <ul className="space-y-2 text-xs sm:text-sm text-gray-800 dark:text-gray-200 font-bold">
                <li className="flex items-start gap-2">• Agile/Scrum methodologies</li>
                <li className="flex items-start gap-2">• CI/CD pipeline</li>
                <li className="flex items-start gap-2">• Microservices architecture</li>
              </ul>
            </div>
            <div className="p-5 sm:p-6 rounded-2xl bg-gradient-to-br from-violet-500/15 to-fuchsia-500/15 dark:from-violet-500/25 dark:to-fuchsia-500/25 border-2 border-violet-400/40 shadow-lg hover:border-violet-500/60 transition-colors">
              <h3 className="font-black text-lg sm:text-xl text-violet-700 dark:text-violet-400 mb-3">📊 Quantify Impact</h3>
              <ul className="space-y-2 text-xs sm:text-sm text-gray-800 dark:text-gray-200 font-bold">
                <li className="flex items-start gap-2">• Add metrics and percentages</li>
                <li className="flex items-start gap-2">• Include team sizes</li>
                <li className="flex items-start gap-2">• Specify project scope</li>
              </ul>
            </div>
            <div className="p-5 sm:p-6 rounded-2xl bg-gradient-to-br from-orange-500/15 to-amber-500/15 dark:from-orange-500/25 dark:to-amber-500/25 border-2 border-orange-400/40 shadow-lg hover:border-orange-500/60 transition-colors md:col-span-2 lg:col-span-1">
              <h3 className="font-black text-lg sm:text-xl text-orange-700 dark:text-orange-400 mb-3">🚀 Action Verbs</h3>
              <ul className="space-y-2 text-xs sm:text-sm text-gray-800 dark:text-gray-200 font-bold">
                <li className="flex items-start gap-2">• Led, Spearheaded, Architected</li>
                <li className="flex items-start gap-2">• Optimized, Streamlined</li>
                <li className="flex items-start gap-2">• Collaborated, Facilitated</li>
              </ul>
            </div>
          </div>
        </motion.div>
      </div>

      <Toast
        message={toastMessage}
        type={toastType}
        isVisible={showToast}
        onClose={() => setShowToast(false)}
      />
    </div>
  );
}
