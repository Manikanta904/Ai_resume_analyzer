

import { motion } from 'motion/react';
import { Upload, FileText, Sparkles, ArrowRight, Briefcase, Rocket, AlertCircle } from 'lucide-react';
import { useState } from 'react';
import { Toast } from './toast-notification';

export function LandingPage({ onAnalyze }) {
  const [resumeFile, setResumeFile] = useState(null);
  const [resumeText, setResumeText] = useState('');
  const [jdFile, setJdFile] = useState(null);
  const [jdText, setJdText] = useState('');

  const [isDraggingResume, setIsDraggingResume] = useState(false);
  const [isDraggingJD, setIsDraggingJD] = useState(false);
  const [showError, setShowError] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const handleResumeFileSelect = (file) => {
    if (file.type === 'application/pdf' ||
      file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' ||
      file.type === 'text/plain') {
      setResumeFile(file);
      setResumeText(''); // Clear text if file is uploaded
    }
  };

  const handleJdFileSelect = (file) => {
    if (file.type === 'application/pdf' ||
      file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' ||
      file.type === 'text/plain') {
      setJdFile(file);
      setJdText(''); // Clear text if file is uploaded
    }
  };

  const getWordCount = (text) => {
    return text.trim().split(/\s+/).filter(word => word.length > 0).length;
  };

  const resumeWordCount = getWordCount(resumeText);
  const jdWordCount = getWordCount(jdText);

  const isResumeValid = !!resumeFile || resumeWordCount >= 20;
  const isJdValid = !!jdFile || jdWordCount >= 10;

  const handleAnalyze = () => {
    if (!isResumeValid) {
      setErrorMessage('Resume must be uploaded or contain at least 20 words.');
      setShowError(true);
      return;
    }
    if (!isJdValid) {
      setErrorMessage('Job Description must be uploaded or contain at least 10 words.');
      setShowError(true);
      return;
    }

    onAnalyze(
      { file: resumeFile, text: resumeText },
      { file: jdFile, text: jdText }
    );
  };

  const isAnalyzeDisabled = !isResumeValid || !isJdValid;

  return (
    <div className="min-h-screen relative flex flex-col items-center justify-center py-12 px-4 bg-transparent transition-colors duration-500 overflow-hidden">
      {/* Background Glows */}
      <div className="absolute top-0 left-0 w-full h-full pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[60%] h-[60%] bg-violet-500/15 dark:bg-violet-900/20 blur-[130px] rounded-full" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[60%] h-[60%] bg-pink-500/15 dark:bg-pink-900/20 blur-[130px] rounded-full" />
      </div>

      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="relative z-10 flex items-center gap-2 mb-12"
      >
        <Sparkles className="w-5 h-5 text-violet-500 dark:text-violet-400" />
        <span className="text-violet-900 dark:text-violet-200 font-bold tracking-wider text-sm sm:text-base uppercase">
          Intelligent Resume & Job Match Engine
        </span>
        <Sparkles className="w-5 h-5 text-violet-500 dark:text-violet-400" />
      </motion.div>

      {/* Main Content */}
      <div className="relative z-10 w-full max-w-6xl flex flex-col items-center">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 w-full mb-12">

          {/* Resume Section */}
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-white/90 dark:bg-[#2d1b4d]/50 backdrop-blur-xl rounded-[32px] p-8 border-2 border-white dark:border-violet-500/20 shadow-[0_30px_60px_rgba(139,92,246,0.15)] dark:shadow-2xl relative group overflow-hidden"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-pink-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />

            <div className="relative z-10">
              <div className="flex items-center gap-4 mb-8">
                <div className="p-3 bg-pink-500/10 dark:bg-pink-500/20 rounded-2xl">
                  <FileText className="w-6 h-6 text-pink-600 dark:text-pink-400" />
                </div>
                <h2 className="text-2xl font-bold text-slate-900 dark:text-white">Upload Resume</h2>
              </div>

              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-semibold text-violet-700 dark:text-violet-300 mb-3">Paste Resume Text</label>
                  <textarea
                    value={resumeText}
                    onChange={(e) => {
                      setResumeText(e.target.value);
                      if (e.target.value) setResumeFile(null);
                    }}
                    placeholder="Paste the content of your resume here..."
                    className="w-full h-40 bg-white dark:bg-[#150a24] border-2 border-slate-100 dark:border-violet-500/30 rounded-2xl p-4 text-slate-900 dark:text-violet-100 placeholder-slate-400 dark:placeholder-violet-400/50 focus:outline-none focus:ring-2 focus:ring-violet-500/50 resize-none transition-all shadow-inner"
                  />
                  <div className="mt-2 space-y-2">
                    <p className="text-[11px] text-violet-500 dark:text-violet-400 font-medium italic">
                      Note: Resume Text must be 20 words or above
                    </p>
                    {resumeText.trim() && resumeWordCount < 20 && (
                      <div className="flex items-center gap-1.5 text-rose-500 dark:text-rose-400 text-[11px] font-bold animate-pulse">
                        <AlertCircle className="w-3.5 h-3.5" />
                        <span>Currently: {resumeWordCount} words (Min 20 required)</span>
                      </div>
                    )}
                    {resumeText.trim() && resumeWordCount >= 20 && (
                      <div className="flex items-center gap-1.5 text-emerald-500 dark:text-emerald-400 text-[11px] font-bold">
                        <Sparkles className="w-3.5 h-3.5" />
                        <span>Requirement met! ({resumeWordCount} words)</span>
                      </div>
                    )}
                  </div>
                </div>

                <div className="relative py-4 flex items-center">
                  <div className="flex-grow border-t border-violet-200 dark:border-violet-500/20"></div>
                  <span className="flex-shrink mx-4 text-[10px] font-bold text-violet-500 dark:text-violet-400 tracking-[0.2em]">OR UPLOAD FILE</span>
                  <div className="flex-grow border-t border-violet-200 dark:border-violet-500/20"></div>
                </div>

                <div
                  onDragOver={(e) => { e.preventDefault(); setIsDraggingResume(true); }}
                  onDragLeave={() => setIsDraggingResume(false)}
                  onDrop={(e) => {
                    e.preventDefault();
                    setIsDraggingResume(false);
                    const file = e.dataTransfer.files[0];
                    if (file) handleResumeFileSelect(file);
                  }}
                  className={`relative group cursor-pointer border-2 border-dashed rounded-2xl p-8 transition-all duration-300 flex flex-col items-center text-center ${isDraggingResume
                    ? 'border-pink-500 bg-pink-500/5'
                    : 'border-violet-300 dark:border-violet-500/30 hover:border-violet-400 dark:hover:border-violet-500/50 bg-slate-50/50 dark:bg-transparent'
                    }`}
                >
                  <input
                    type="file"
                    className="absolute inset-0 opacity-0 cursor-pointer"
                    onChange={(e) => {
                      const file = e.target.files?.[0];
                      if (file) handleResumeFileSelect(file);
                    }}
                    accept=".pdf,.docx,.txt"
                  />

                  {resumeFile ? (
                    <div className="flex flex-col items-center gap-2">
                      <div className="p-3 bg-green-500/10 dark:bg-green-500/20 rounded-full mb-2">
                        <FileText className="w-8 h-8 text-green-600 dark:text-green-400" />
                      </div>
                      <span className="text-slate-900 dark:text-white font-medium break-all">{resumeFile.name}</span>
                      <span className="text-slate-500 dark:text-violet-400 text-xs">{(resumeFile.size / 1024).toFixed(1)} KB</span>
                    </div>
                  ) : (
                    <>
                      <div className="p-3 mb-4 bg-pink-500/10 rounded-2xl">
                        <Upload className="w-8 h-8 text-pink-600 dark:text-pink-400" />
                      </div>
                      <p className="text-slate-900 dark:text-white font-bold mb-1">
                        Drag & drop or <span className="text-cyan-600 dark:text-cyan-400">browse</span>
                      </p>
                      <p className="text-slate-500 dark:text-violet-400 text-xs font-medium">PDF, DOCX, or TXT</p>
                    </>
                  )}
                </div>
              </div>
            </div>
          </motion.div>

          {/* JD Section */}
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-white/90 dark:bg-[#2d1b4d]/50 backdrop-blur-xl rounded-[32px] p-8 border-2 border-white dark:border-violet-500/20 shadow-[0_30px_60px_rgba(139,92,246,0.15)] dark:shadow-2xl relative group overflow-hidden"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-violet-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />

            <div className="relative z-10">
              <div className="flex items-center gap-4 mb-8">
                <div className="p-3 bg-violet-500/10 dark:bg-violet-500/20 rounded-2xl">
                  <Briefcase className="w-6 h-6 text-violet-600 dark:text-violet-400" />
                </div>
                <h2 className="text-2xl font-bold text-slate-900 dark:text-white">Job Description</h2>
              </div>

              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-semibold text-violet-700 dark:text-violet-300 mb-3">Paste JD Text</label>
                  <textarea
                    value={jdText}
                    onChange={(e) => {
                      setJdText(e.target.value);
                      if (e.target.value) setJdFile(null);
                    }}
                    placeholder="Paste the job requirements and description here..."
                    className="w-full h-40 bg-white dark:bg-[#150a24] border-2 border-slate-100 dark:border-violet-500/30 rounded-2xl p-4 text-slate-900 dark:text-violet-100 placeholder-slate-400 dark:placeholder-violet-400/50 focus:outline-none focus:ring-2 focus:ring-violet-500/50 resize-none transition-all shadow-inner"
                  />
                  <div className="mt-2 space-y-2">
                    <p className="text-[11px] text-violet-500 dark:text-violet-400 font-medium italic">
                      Note: JD Text must be 10 words or above
                    </p>
                    {jdText.trim() && jdWordCount < 10 && (
                      <div className="flex items-center gap-1.5 text-rose-500 dark:text-rose-400 text-[11px] font-bold animate-pulse">
                        <AlertCircle className="w-3.5 h-3.5" />
                        <span>Currently: {jdWordCount} words (Min 10 required)</span>
                      </div>
                    )}
                    {jdText.trim() && jdWordCount >= 10 && (
                      <div className="flex items-center gap-1.5 text-emerald-500 dark:text-emerald-400 text-[11px] font-bold">
                        <Sparkles className="w-3.5 h-3.5" />
                        <span>Requirement met! ({jdWordCount} words)</span>
                      </div>
                    )}
                  </div>
                </div>

                <div className="relative py-4 flex items-center">
                  <div className="flex-grow border-t border-violet-200 dark:border-violet-500/20"></div>
                  <span className="flex-shrink mx-4 text-[10px] font-bold text-violet-500 dark:text-violet-400 tracking-[0.2em]">OR UPLOAD FILE</span>
                  <div className="flex-grow border-t border-violet-200 dark:border-violet-500/20"></div>
                </div>

                <div
                  onDragOver={(e) => { e.preventDefault(); setIsDraggingJD(true); }}
                  onDragLeave={() => setIsDraggingJD(false)}
                  onDrop={(e) => {
                    e.preventDefault();
                    setIsDraggingJD(false);
                    const file = e.dataTransfer.files[0];
                    if (file) handleJdFileSelect(file);
                  }}
                  className={`relative group cursor-pointer border-2 border-dashed rounded-2xl p-8 transition-all duration-300 flex flex-col items-center text-center ${isDraggingJD
                    ? 'border-pink-500 bg-pink-500/5'
                    : 'border-violet-300 dark:border-violet-500/30 hover:border-violet-400 dark:hover:border-violet-500/50 bg-slate-50/50 dark:bg-transparent'
                    }`}
                >
                  <input
                    type="file"
                    className="absolute inset-0 opacity-0 cursor-pointer"
                    onChange={(e) => {
                      const file = e.target.files?.[0];
                      if (file) handleJdFileSelect(file);
                    }}
                    accept=".pdf,.docx,.txt"
                  />

                  {jdFile ? (
                    <div className="flex flex-col items-center gap-2">
                      <div className="p-3 bg-green-500/10 dark:bg-green-500/20 rounded-full mb-2">
                        <FileText className="w-8 h-8 text-green-600 dark:text-green-400" />
                      </div>
                      <span className="text-slate-900 dark:text-white font-medium break-all">{jdFile.name}</span>
                      <span className="text-slate-500 dark:text-violet-400 text-xs">{(jdFile.size / 1024).toFixed(1)} KB</span>
                    </div>
                  ) : (
                    <>
                      <div className="p-3 mb-4 bg-violet-500/10 rounded-2xl">
                        <Upload className="w-8 h-8 text-violet-600 dark:text-violet-400" />
                      </div>
                      <p className="text-slate-900 dark:text-white font-bold mb-1">
                        Drag & drop or <span className="text-cyan-600 dark:text-cyan-400">browse</span>
                      </p>
                      <p className="text-slate-500 dark:text-violet-400 text-xs font-medium">Upload Job Post PDF/DOCX</p>
                    </>
                  )}
                </div>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Action Button */}
        <motion.button
          onClick={handleAnalyze}
          whileHover={!isAnalyzeDisabled ? { scale: 1.02 } : {}}
          whileTap={!isAnalyzeDisabled ? { scale: 0.98 } : {}}
          className={`group relative px-12 py-5 rounded-[20px] overflow-hidden transition-all duration-300 shadow-xl shadow-violet-500/10 ${isAnalyzeDisabled ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          <div className="absolute inset-0 bg-gradient-to-r from-violet-600 to-pink-600" />
          <div className="absolute inset-0 bg-gradient-to-r from-violet-500 to-pink-500 opacity-0 group-hover:opacity-100 transition-opacity" />
          <span className="relative flex items-center justify-center gap-3 text-white font-black text-lg uppercase tracking-tighter">
            <Rocket className="w-5 h-5 group-hover:animate-bounce" />
            Analyze Resume
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </span>
        </motion.button>

        {/* Footer */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="mt-12 flex items-center gap-3"
        >
          <div className="h-[1px] w-8 bg-violet-300 dark:bg-violet-800" />
          <Rocket className="w-4 h-4 text-pink-500 rotate-45" />
          <span className="text-violet-600 dark:text-violet-400/80 text-[10px] font-black uppercase tracking-[0.3em] whitespace-nowrap">
            Powered by Advanced AI Technology
          </span>
          <div className="h-[1px] w-8 bg-violet-300 dark:bg-violet-800" />
        </motion.div>
      </div>
      <Toast
        message={errorMessage}
        type="error"
        isVisible={showError}
        onClose={() => setShowError(false)}
      />
    </div>
  );
}

