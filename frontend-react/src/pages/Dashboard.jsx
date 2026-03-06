import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Navbar from '../components/Navbar';
import { ScoreMeter, SkillSection, RoadmapSection } from '../components/ResultComponents';
import api from '../utils/api';
import { Upload, FileText, Search, Loader2, Target, AlertCircle, Sparkles, CheckCircle2, FileUp, Info, Lightbulb, HelpCircle } from 'lucide-react';

const Dashboard = () => {
    const [resumeFile, setResumeFile] = useState(null);
    const [jobDesc, setJobDesc] = useState('');
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState(null);

    const handleFileChange = (e) => {
        setResumeFile(e.target.files[0]);
    };

    const handleAnalyze = async () => {
        if (!resumeFile || !jobDesc) return;
        setLoading(true);
        try {
            const formData = new FormData();
            formData.append('resume_file', resumeFile);
            formData.append('job_description', jobDesc);

            const response = await api.post('/documents/', formData);
            setResults(response.data);
        } catch (error) {
            console.error('Analysis failed', error);
            const errorMsg = error.response?.data?.detail || 'Analysis failed. Please check your inputs.';
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
                                    <FileUp className="w-6 h-6" />
                                </div>
                                <div>
                                    <h2 className="text-xl font-black text-white tracking-tight leading-none">Smart Ingestion</h2>
                                    <p className="text-white/40 font-black uppercase tracking-widest mt-1 text-[8px]">Upload your professional assets</p>
                                </div>
                            </div>

                            <div className="space-y-10">
                                <div className="space-y-4">
                                    <div className="flex items-center justify-between px-1">
                                        <label className="text-[8px] font-black text-white/40 uppercase tracking-[0.2em]">Job Description</label>
                                        {jobDesc && <span className="text-[8px] font-black text-blue-400 uppercase tracking-widest leading-none">Syncing</span>}
                                    </div>
                                    <textarea
                                        value={jobDesc}
                                        onChange={(e) => setJobDesc(e.target.value)}
                                        placeholder="Paste the target job description here..."
                                        className="w-full h-40 p-5 bg-white/5 border border-white/5 rounded-2xl focus:outline-none focus:ring-4 focus:ring-blue-500/10 focus:border-blue-500/30 transition-all resize-none text-white text-xs font-medium custom-scrollbar"
                                    />
                                </div>

                                <div className="space-y-4">
                                    <div className="flex items-center justify-between px-1">
                                        <label className="text-[8px] font-black text-white/40 uppercase tracking-[0.2em]">Resume (PDF / DOCX)</label>
                                        {resumeFile && <span className="text-[8px] font-black text-emerald-400 uppercase tracking-widest leading-none">Ready</span>}
                                    </div>
                                    <div className="relative group/upload">
                                        <input
                                            type="file"
                                            onChange={handleFileChange}
                                            accept=".pdf,.docx,.doc,.txt"
                                            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                                        />
                                        <div className={`w-full py-10 px-5 border-2 border-dashed ${resumeFile ? 'border-emerald-500/30 bg-emerald-500/5' : 'border-white/10 bg-white/5'} rounded-2xl flex flex-col items-center justify-center gap-3 transition-all group-hover/upload:border-blue-500/30 group-hover/upload:bg-white/10`}>
                                            <Upload className={`w-6 h-6 ${resumeFile ? 'text-emerald-400' : 'text-white/20'}`} />
                                            <span className="text-xs font-bold text-white/40 uppercase tracking-widest">
                                                {resumeFile ? resumeFile.name : 'Drop file or click to browse'}
                                            </span>
                                        </div>
                                    </div>
                                </div>

                                <button
                                    onClick={handleAnalyze}
                                    disabled={loading || !resumeFile || !jobDesc}
                                    className="group relative w-full py-4 bg-blue-600 hover:bg-blue-500 disabled:bg-white/5 text-white font-black rounded-2xl transition-all flex items-center justify-center gap-3 shadow-xl shadow-blue-900/10 active:scale-[0.98] text-sm uppercase tracking-widest overflow-hidden"
                                >
                                    <span className="relative z-10">{loading ? 'Running Neural Analysis...' : 'Generate Strategic Match'}</span>
                                    {loading ? <Loader2 className="w-5 h-5 animate-spin relative z-10" /> : <Sparkles className="w-5 h-5 relative z-10 group-hover:rotate-12 transition-transform" />}
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
                                                <Target className="w-24 h-24 text-white" />
                                            </div>
                                            <header className="flex items-center gap-2.5 mb-4">
                                                <div className="p-2.5 bg-blue-500/10 rounded-lg">
                                                    <Info className="text-blue-500 w-5 h-5" />
                                                </div>
                                                <h3 className="text-lg font-black text-white tracking-tight italic">Strategic Fit</h3>
                                            </header>
                                            <p className="text-white/80 text-[11px] leading-relaxed font-medium mb-4">
                                                {results.insights?.status === 'success'
                                                    ? results.insights.raw_narrative.split('\n')[0].replace(/Why this Match\?: /i, '')
                                                    : results.match_percentage >= 80
                                                        ? "Elite compatibility. Your profile shows exceptional semantic synergy."
                                                        : "Competitive profile with specialized gaps detected."
                                                }
                                            </p>

                                            {results.insights?.recommended_role && (
                                                <div className="mt-auto pt-4 border-t border-white/10">
                                                    <p className="text-[9px] font-black text-white/40 uppercase tracking-widest mb-1">Recommended Role</p>
                                                    <p className="text-sm font-bold text-blue-400 capitalize">{results.insights.recommended_role}</p>
                                                </div>
                                            )}
                                        </div>
                                    </div>

                                    {/* AI DRIVEN INSIGHTS SECTION */}
                                    <div className="grid grid-cols-1 gap-8">
                                        <div className="glass p-10 rounded-[2.5rem] border-white/5 shadow-2xl relative overflow-hidden">
                                            <div className="absolute top-0 right-0 p-10 opacity-5">
                                                <Sparkles className="w-20 h-20 text-white" />
                                            </div>
                                            <h3 className="text-xl font-black text-white mb-8 tracking-tight flex items-center gap-3">
                                                <Lightbulb className="w-6 h-6 text-amber-400" />
                                                AI Strategic Narrative
                                            </h3>

                                            <div className="space-y-8">
                                                <div className="p-6 bg-white/[0.02] border border-white/5 rounded-2xl">
                                                    <h4 className="text-[9px] font-black text-blue-400 uppercase tracking-widest mb-3">Executive Summary</h4>
                                                    <p className="text-white/70 text-xs leading-relaxed font-medium">
                                                        {results.insights?.raw_narrative || "Deep analysis in progress..."}
                                                    </p>
                                                </div>

                                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                                    <div className="p-6 bg-emerald-500/5 border border-emerald-500/10 rounded-2xl">
                                                        <h4 className="text-[9px] font-black text-emerald-400 uppercase tracking-widest mb-4 flex items-center gap-2">
                                                            <HelpCircle className="w-3.5 h-3.5" />
                                                            Interview Prep
                                                        </h4>
                                                        <ul className="space-y-3">
                                                            {results.insights?.interview_questions?.length > 0 ? (
                                                                results.insights.interview_questions.map((q, i) => (
                                                                    <li key={i} className="text-[10px] text-white/50 font-bold leading-tight flex gap-2">
                                                                        <span className="text-emerald-500/50">•</span> {q}
                                                                    </li>
                                                                ))
                                                            ) : (
                                                                <li className="text-[10px] text-white/30 italic">Detailed questions generated in report...</li>
                                                            )}
                                                        </ul>
                                                    </div>
                                                    <div className="p-6 bg-amber-500/5 border border-amber-500/10 rounded-2xl">
                                                        <h4 className="text-[9px] font-black text-amber-400 uppercase tracking-widest mb-4">Resume Pivot</h4>
                                                        <p className="text-[10px] text-white/50 font-bold leading-relaxed">
                                                            {results.insights?.resume_advice || "Optimization tip will appear here."}
                                                        </p>
                                                    </div>
                                                </div>
                                            </div>
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
                                        <RoadmapSection
                                            title="Actionable Learning Roadmap"
                                            roadmap={results.learning_roadmap}
                                            icon={AlertCircle}
                                            colorClass="bg-blue-500"
                                            className="glass border-white/5"
                                            delay={0.2}
                                        />
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
