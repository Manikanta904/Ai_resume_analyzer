import { useState, useEffect } from 'react';
import { ThemeProvider } from './components/theme-provider';
import { ThemeToggle } from './components/theme-toggle';
import { AnimatedBackground } from './components/animated-background';
import { LandingPage } from './components/landing-page';
import { AnalysisDashboard } from './components/analysis-dashboard';
import { ImproveResume } from './components/improve-resume';
import { LoadingScreen } from './components/loading-screen';
import { PageTransition } from './components/page-transition';
import { KeyboardShortcuts } from './components/keyboard-shortcuts';
import { Toast } from './components/toast-notification';
import { analyzeResume } from '../services/api';



const flattenInsightItems = (aiInsights) => {
  if (!aiInsights || typeof aiInsights !== 'object') {
    return { insights: [], suggestions: [] };
  }

  const sections = [
    aiInsights.summary,
    aiInsights.experience,
    aiInsights.projects,
    aiInsights.skills,
  ].filter(Boolean);

  return {
    insights: sections.flatMap((section) => section?.issues ?? []),
    suggestions: sections.flatMap((section) => section?.suggestions ?? []),
  };
};

const normalizeAnalysisData = (payload) => {
  const data = payload?.data ?? payload ?? {};
  const flattened = flattenInsightItems(data.ai_insights);

  return {
    atsScore: data.atsScore ?? data.ats_score ?? 0,
    matchPercentage: data.matchPercentage ?? data.resume_match_score ?? 0,
    detectedRole: data.detectedRole ?? data.role ?? 'Unknown',
    matchedSkills: data.matchedSkills ?? data.matched_skills ?? [],
    missingSkills: data.missingSkills ?? data.missing_skills ?? [],
    mustHaveSkills: data.mustHaveSkills ?? data.must_have_skills ?? [],
    goodToHaveSkills: data.goodToHaveSkills ?? data.good_to_have_skills ?? [],
    insights: data.insights ?? flattened.insights,
    suggestions: data.suggestions ?? data.recommendations ?? flattened.suggestions,
  };
};


export default function App() {
  const [currentScreen, setCurrentScreen] = useState('landing');
  const [analysisData, setAnalysisData] = useState(null);
  const [lastSubmission, setLastSubmission] = useState(null);
  const [toastMessage, setToastMessage] = useState('');
  const [toastType, setToastType] = useState('error');
  const [showToast, setShowToast] = useState(false);

  // Fix: Ensure page loads at the top on every screen change
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'instant' });
  }, [currentScreen]);

  const showError = (message) => {
    setToastMessage(message);
    setToastType('error');
    setShowToast(true);
  };

  const handleAnalyze = async (resume, jd) => {
    setCurrentScreen('loading');
    setLastSubmission({ resume, jd });

    const formData = new FormData();
    if (resume?.file) {
      formData.append('resume_file', resume.file);
    } else if (resume?.text) {
      formData.append('resume_file', new File([resume.text], 'resume.txt', { type: 'text/plain' }));
    }

    if (jd?.file) {
      formData.append('jd_file', jd.file);
    } else if (jd?.text) {
      formData.append('jd_file', new File([jd.text], 'jd.txt', { type: 'text/plain' }));
    }

    try {
      const result = await analyzeResume(formData);
      const normalized = normalizeAnalysisData(result);
      setAnalysisData(normalized);
      setCurrentScreen('analysis');
    } catch (error) {
      showError(error?.message || 'Analyze request failed.');
      setCurrentScreen('landing');
    }
  };

  const handleImprove = () => {
    if (!analysisData || !lastSubmission) {
      showError('Please analyze a resume before improving it.');
      return;
    }
    setCurrentScreen('improve');
  };

  const handleReanalyze = () => {
    setCurrentScreen('landing');
  };

  return (
    <ThemeProvider>
      <div className="relative min-h-screen transition-colors duration-500">
        <AnimatedBackground />
        <ThemeToggle />
        <KeyboardShortcuts onBack={currentScreen !== 'landing' ? handleReanalyze : undefined} />

        <PageTransition pageKey={currentScreen}>
          {currentScreen === 'landing' && (
            <LandingPage onAnalyze={handleAnalyze} />
          )}

          {currentScreen === 'loading' && (
            <LoadingScreen />
          )}

          {currentScreen === 'analysis' && analysisData && (
            <AnalysisDashboard data={analysisData} onImprove={handleImprove} />
          )}

          {currentScreen === 'improve' && (
            <ImproveResume
              onReanalyze={handleReanalyze}
              resumeInput={lastSubmission?.resume}
              jdInput={lastSubmission?.jd}
            />
          )}
        </PageTransition>
      </div>

      <Toast
        message={toastMessage}
        type={toastType}
        isVisible={showToast}
        onClose={() => setShowToast(false)}
      />
    </ThemeProvider>
  );
}

