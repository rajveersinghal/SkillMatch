import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Navbar from '../components/Navbar';
import { ScoreMeter, SkillSection } from '../components/ResultComponents';
import api from '../utils/api';
import { Upload, FileText, Search, Loader2, Target, AlertCircle, Sparkles, CheckCircle2 } from 'lucide-react';

const Dashboard = () => {
    const [resumeText, setResumeText] = useState('');
    const [jobDesc, setJobDesc] = useState('');
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState(null);

    const handleAnalyze = async () => {
        if (!resumeText || !jobDesc) return;
        setLoading(true);
        try {
            const response = await api.post('/documents/', {
                resume_text: resumeText,
                job_description: jobDesc
            });
            setResults(response.data);
        } catch (error) {
            console.error('Analysis failed', error);
            const errorMsg = error.response?.data?.detail || 'Analysis failed. Please check your inputs and ensure the backend is running.';
            alert(errorMsg);
        }
        setLoading(false);
    };

    return (
        <div className="min-h-screen mesh-bg selection:bg-blue-500/30 selection:text-white pb-20">
            <Navbar />
            <div className="h-24" />

            <main className="max-w-7xl mx-auto px-6 relative">
                <div className="absolute top-0 left-1/4 w-[500px] h-[500px] bg-blue-600/10 rounded-full blur-[120px] pointer-events-none" />
                <div className="absolute bottom-0 right-1/4 w-[500px] h-[500px] bg-indigo-600/10 rounded-full blur-[120px] pointer-events-none" />

                <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-start">
                    <section className="lg:col-span-5 space-y-8">
                        <div className="glass p-10 rounded-[3rem] border-white/5 shadow-2xl relative overflow-hidden group">
                            <div className="absolute inset-x-0 bottom-0 h-1 bg-gradient-to-r from-blue-600 to-indigo-600 opacity-50 group-focus-within:opacity-100 transition-opacity" />

                            <div className="flex items-center gap-4 mb-8">
                                <div className="p-3 bg-blue-600 rounded-xl shadow-xl shadow-blue-500/20 text-white">
                                    <FileText className="w-6 h-6" />
                                </div>
                                <div>
                                    <h2 className="text-xl font-black text-white tracking-tight leading-none">Resume & Job Comparison</h2>
                                    <p className="text-white/40 font-black uppercase tracking-widest mt-1 text-[8px]">Fill in the details below</p>
                                </div>
                            </div>

                            <div className="space-y-10">
                                <div className="space-y-4">
                                    <div className="flex items-center justify-between px-1">
                                        <label className="text-[8px] font-black text-white/40 uppercase tracking-[0.2em]">Job Description</label>
                                        {jobDesc && <span className="text-[8px] font-black text-blue-400 uppercase tracking-widest leading-none">Captured</span>}
                                    </div>
                                    <textarea
                                        value={jobDesc}
                                        onChange={(e) => setJobDesc(e.target.value)}
                                        placeholder="Paste the job description here..."
                                        className="w-full h-40 p-5 bg-white/5 border border-white/5 rounded-2xl focus:outline-none focus:ring-4 focus:ring-blue-500/10 focus:border-blue-500/30 transition-all resize-none text-white text-xs font-medium custom-scrollbar"
                                    />
                                </div>

                                <div className="space-y-4">
                                    <div className="flex items-center justify-between px-1">
                                        <label className="text-[8px] font-black text-white/40 uppercase tracking-[0.2em]">Your Resume</label>
                                        {resumeText && <span className="text-[8px] font-black text-blue-400 uppercase tracking-widest leading-none">Captured</span>}
                                    </div>
                                    <textarea
                                        value={resumeText}
                                        onChange={(e) => setResumeText(e.target.value)}
                                        placeholder="Paste your resume text here..."
                                        className="w-full h-40 p-5 bg-white/5 border border-white/5 rounded-2xl focus:outline-none focus:ring-4 focus:ring-blue-500/10 focus:border-blue-500/30 transition-all resize-none text-white text-xs font-medium custom-scrollbar"
                                    />
                                </div>

                                <button
                                    onClick={handleAnalyze}
                                    disabled={loading || !resumeText || !jobDesc}
                                    className="group relative w-full py-4 bg-blue-600 hover:bg-blue-500 disabled:bg-white/5 text-white font-black rounded-2xl transition-all flex items-center justify-center gap-3 shadow-xl shadow-blue-900/10 active:scale-[0.98] text-sm uppercase tracking-widest overflow-hidden"
                                >
                                    <span className="relative z-10">{loading ? 'Matching...' : 'Compare Skills'}</span>
                                    {loading ? <Loader2 className="w-5 h-5 animate-spin relative z-10" /> : <Search className="w-5 h-5 relative z-10 group-hover:scale-110 transition-transform" />}
                                    <div className="absolute inset-0 bg-gradient-to-r from-blue-400 to-indigo-400 opacity-0 group-hover:opacity-100 transition-opacity" />
                                </button>
                            </div>
                        </div>
                    </section>

                    <AnimatePresence>
                        {results && (
                            <section className="lg:col-span-7 flex flex-col gap-8">
                                <motion.div
                                    initial={{ opacity: 0, x: 100 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    exit={{ opacity: 0, x: 100 }}
                                    transition={{ type: 'spring', damping: 25, stiffness: 100 }}
                                    className="flex flex-col gap-8"
                                >
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                        <ScoreMeter score={results.match_percentage} className="glass border-white/5" />

                                        <div className="glass p-8 rounded-[2rem] border-white/5 shadow-2xl flex flex-col justify-center relative overflow-hidden group">
                                            <div className="absolute -right-8 -bottom-8 p-8 opacity-5 rotate-12 group-hover:rotate-0 transition-transform duration-700">
                                                <Sparkles className="w-24 h-24 text-white" />
                                            </div>
                                            <header className="flex items-center gap-2.5 mb-4">
                                                <div className="p-2.5 bg-amber-500/10 rounded-lg">
                                                    <Sparkles className="text-amber-500 w-5 h-5" />
                                                </div>
                                                <h3 className="text-lg font-black text-white tracking-tight">Matching Analysis</h3>
                                            </header>
                                            <p className="text-white/80 text-xs leading-relaxed font-medium">
                                                {results.match_percentage >= 80
                                                    ? "Elite compatibility. Your profile shows exceptional synergy with the requirements."
                                                    : results.match_percentage >= 50
                                                        ? "Promising alignment. Core functions match but specialized gaps exist."
                                                        : "Structural divergence. Profile lacks significant role-specific identifiers."}
                                            </p>
                                        </div>
                                    </div>

                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                        <SkillSection
                                            title="Matched Skills"
                                            skills={results.matched_skills}
                                            icon={CheckCircle2}
                                            colorClass="bg-emerald-500"
                                            className="glass border-white/5"
                                            delay={0.1}
                                        />
                                        <SkillSection
                                            title="Missing Skills"
                                            skills={results.missing_skills}
                                            icon={AlertCircle}
                                            colorClass="bg-red-500"
                                            className="glass border-white/5"
                                            delay={0.2}
                                        />
                                    </div>

                                    <div className="glass p-8 rounded-[2rem] border-white/5 shadow-2xl overflow-hidden relative group">
                                        <div className="absolute top-0 right-0 p-8 opacity-5 scale-125 rotate-12 group-hover:rotate-0 transition-all duration-1000">
                                            <Target className="w-32 h-32 text-white" />
                                        </div>
                                        <h3 className="text-xl font-black text-white mb-8 tracking-tight italic">Improvement Steps</h3>
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-10">
                                            {results.gap_analysis && Object.entries(results.gap_analysis).map(([cat, skills], idx) => (
                                                <motion.div
                                                    key={cat}
                                                    initial={{ opacity: 0, y: 20 }}
                                                    animate={{ opacity: 1, y: 0 }}
                                                    transition={{ delay: 0.4 + (idx * 0.1) }}
                                                    className="space-y-4"
                                                >
                                                    <div className="flex items-center justify-between">
                                                        <span className="text-[9px] font-black text-white/40 uppercase tracking-[0.2em]">{cat}</span>
                                                        <span className="text-blue-400 text-xs font-black font-mono">{(1 - (skills.length / 10)) * 100}% Fit</span>
                                                    </div>
                                                    <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                                                        <motion.div
                                                            initial={{ width: 0 }}
                                                            animate={{ width: `${(1 - (skills.length / 10)) * 100}%` }}
                                                            transition={{ duration: 1.5, ease: 'easeOut', delay: 0.6 }}
                                                            className="h-full bg-gradient-to-r from-blue-600 to-indigo-500 rounded-full"
                                                        />
                                                    </div>
                                                </motion.div>
                                            ))}
                                        </div>
                                    </div>
                                </motion.div>
                            </section>
                        )}
                    </AnimatePresence>
                </div>
            </main>
        </div>
    );
};

export default Dashboard;
