import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Sparkles, Target, Zap, Shield, Lock, ChevronRight, BarChart3, CheckCircle2, ArrowRight, RotateCcw, Maximize2, Route, UserCircle2, Plus, Minus, Mail } from 'lucide-react';

const FeatureCard = ({ icon: Icon, title, description, delay, className = "" }) => (
    <motion.div
        initial={{ opacity: 0, scale: 0.98 }}
        whileInView={{ opacity: 1, scale: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.4, delay }}
        className={`group p-6 glass rounded-2xl hover:bg-white/5 transition-all duration-300 cursor-default ${className}`}
    >
        <div className="w-10 h-10 bg-blue-500/5 rounded-lg flex items-center justify-center mb-5 border border-blue-500/10 group-hover:border-blue-500/20 transition-all duration-300">
            <Icon className="w-5 h-5 text-blue-400/80 group-hover:text-blue-400" />
        </div>
        <h3 className="text-lg font-bold text-white mb-2 tracking-tight group-hover:text-blue-400 transition-colors">{title}</h3>
        <p className="text-slate-400 text-sm leading-relaxed font-medium opacity-70">
            {description}
        </p>
    </motion.div>
);

// NeuralCore removed for spatial optimization

const LandingPage = () => {
    const navigate = useNavigate();

    return (
        <div className="min-h-screen mesh-bg selection:bg-blue-500/30 selection:text-white">
            <div className="h-4" />

            <header className="relative pt-4 pb-10 px-6 overflow-hidden">
                <div className="absolute inset-0 mask-radial opacity-20 pointer-events-none">
                    <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-blue-600/60 rounded-full blur-[160px]" />
                </div>

                <div className="max-w-6xl mx-auto text-center relative z-10">
                    <motion.div
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="inline-flex items-center gap-2.5 px-3 py-1 rounded-full glass border-white/5 text-blue-400/80 font-bold text-[9px] mb-6 tracking-[0.2em]"
                    >
                        <Sparkles className="w-3.5 h-3.5 fill-current opacity-50" /> AI-POWERED CAREER MATCHING
                    </motion.div>

                    <motion.h1
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8, ease: "easeOut" }}
                        className="text-3xl md:text-5xl lg:text-6xl font-black text-white mb-4 tracking-tighter leading-[1.05]"
                    >
                        Analyze Your Resume.<br />
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-300 text-glow inline-block py-2">
                            Match the Job.
                        </span><br />
                        <span className="text-slate-500/50 italic font-serif">Upgrade Your Skills.</span>
                    </motion.h1>

                    <motion.p
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.4, duration: 1 }}
                        className="text-sm md:text-base max-w-xl mx-auto mb-8 leading-relaxed font-medium text-white"
                    >
                        SkillMatch is an AI-powered platform that compares your resume with job descriptions,
                        identifies skill gaps, and suggests what to learn next.
                    </motion.p>

                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.6 }}
                        className="flex flex-col sm:flex-row items-center justify-center gap-6"
                    >
                        <div className="flex flex-col items-center gap-6">
                            <button
                                onClick={() => navigate('/login')}
                                className="group relative px-10 py-5 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-2xl shadow-xl shadow-blue-500/20 flex items-center gap-3 transition-all active:scale-95 text-base tracking-wide overflow-hidden"
                            >
                                <span className="relative z-10 font-black">Analyze My Resume Now</span>
                                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                                <div className="absolute inset-0 bg-gradient-to-r from-blue-400 to-indigo-400 opacity-0 group-hover:opacity-100 transition-opacity" />
                            </button>
                            <p className="text-slate-500 font-bold text-[10px] uppercase tracking-widest opacity-60 italic">
                                Free • No credit card • Instant results
                            </p>
                        </div>

                    </motion.div>
                </div>
            </header>

            {/* PROBLEM STATEMENT SECTION */}
            <section className="pt-4 pb-4 px-6 relative overflow-hidden">
                <div className="max-w-6xl mx-auto">
                    <div className="p-10 rounded-[2.5rem] border border-white/5 relative overflow-hidden flex flex-col md:flex-row items-center gap-12">
                        <div className="md:w-1/2">
                            <h2 className="text-3xl md:text-4xl font-extrabold text-white mb-6 tracking-tighter leading-tight">Why Job Matching Is <br /><span className="text-blue-400">Still So Difficult.</span></h2>
                            <p className="text-white/40 font-bold uppercase tracking-widest text-[8px] mb-6 opacity-50">Understanding the challenges in modern job hunting.</p>
                            <div className="w-12 h-1 bg-blue-500/20 rounded-full" />
                        </div>
                        <div className="md:w-1/2 grid grid-cols-1 gap-4">
                            {[
                                { t: "Keyword Guessing Cycles", i: RotateCcw, d: "Eliminate the manual trial-and-error of resume optimization." },
                                { t: "The ATS 'Black Hole' Effect", i: Maximize2, d: "Understand exactly why your profile isn't clearing automated filters." },
                                { t: "Ambiguous Career Trajectories", i: Route, d: "Replace guesswork with a clear, skill-based roadmap to your next role." },
                                { t: "Subjective Manual Evaluation", i: UserCircle2, d: "Standardize your value proposition with objective neural analytics." }
                            ].map((point, i) => (
                                <motion.div
                                    key={i}
                                    initial={{ opacity: 0, x: 10 }}
                                    whileInView={{ opacity: 1, x: 0 }}
                                    transition={{ delay: i * 0.1 }}
                                    className="flex items-start gap-4 p-5 rounded-2xl bg-white/[0.02] border border-white/5 group hover:bg-white/[0.04] transition-all"
                                >
                                    <div className="w-10 h-10 rounded-xl bg-blue-500/5 flex items-center justify-center flex-shrink-0 group-hover:bg-blue-500/10 transition-colors">
                                        <point.i className="w-5 h-5 text-blue-400 opacity-60 group-hover:opacity-100 transition-opacity" />
                                    </div>
                                    <div className="space-y-1">
                                        <h4 className="text-white font-bold text-sm tracking-tight">{point.t}</h4>
                                        <p className="text-white/40 text-[10px] uppercase font-bold tracking-widest leading-relaxed">{point.d}</p>
                                    </div>
                                </motion.div>
                            ))}
                        </div>
                    </div>
                </div>
            </section>

            {/* HOW IT WORKS SECTION */}
            <section className="py-8 px-6">
                <div className="max-w-6xl mx-auto">
                    <header className="text-center mb-12">
                        <h2 className="text-2xl md:text-3xl font-extrabold text-white mb-4 tracking-tighter">How SkillMatch <span className="text-blue-500/80">Works.</span></h2>
                        <p className="text-white/40 font-bold uppercase tracking-widest text-[8px]">Our step-by-step analysis process</p>
                    </header>

                    <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
                        {[
                            { step: "01", title: "Upload", desc: "Digital Document Upload" },
                            { step: "02", title: "Analyze", desc: "Text Normalization" },
                            { step: "03", title: "Extract", desc: "Skill Extraction" },
                            { step: "04", title: "Match", desc: "Vector Analysis" },
                            { step: "05", title: "Results", desc: "Actionable Insights" }
                        ].map((item, i) => (
                            <motion.div
                                key={i}
                                initial={{ opacity: 0, y: 10 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                transition={{ delay: i * 0.1 }}
                                className="relative group"
                            >
                                <div className="p-8 border border-white/5 rounded-2xl h-full flex flex-col items-center text-center hover:bg-white/[0.02] transition-all">
                                    <div className="w-8 h-8 bg-blue-500/10 border border-blue-500/20 rounded-full flex items-center justify-center text-blue-400 mb-6 font-bold text-xs">
                                        {i + 1}
                                    </div>
                                    <h4 className="text-white font-bold text-xs tracking-widest mb-3">{item.title}</h4>
                                    <p className="text-white/50 font-medium text-[10px] leading-relaxed uppercase tracking-widest">{item.desc}</p>
                                </div>
                                {i < 4 && (
                                    <div className="hidden md:block absolute top-1/2 -right-3 -translate-y-1/2 z-20 opacity-20">
                                        <ChevronRight className="w-4 h-4 text-blue-400" />
                                    </div>
                                )}
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>

            <main className="relative py-8 px-6">
                <div className="max-w-6xl mx-auto">
                    <header className="text-center mb-12">
                        <h2 className="text-2xl md:text-3xl font-extrabold text-white mb-4 tracking-tighter">Key <span className="text-blue-500 italic">Features.</span></h2>
                        <div className="w-10 h-1 bg-blue-500/20 mx-auto rounded-full" />
                    </header>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-16">
                        <FeatureCard
                            icon={Shield}
                            title="Secure Login"
                            description="Your data is safe & private with encrypted session handling."
                            delay={0.1}
                        />
                        <FeatureCard
                            icon={BarChart3}
                            title="Resume & JD Analysis"
                            description="Deep semantic comparison supports PDF, DOCX, and raw text."
                            delay={0.2}
                        />
                        <FeatureCard
                            icon={Sparkles}
                            title="Match Percentage"
                            description="Clear resume–job fit score based on intent, not just keywords."
                            delay={0.3}
                        />
                        <FeatureCard
                            icon={Target}
                            title="Skill Gap Detection"
                            description="Know exactly which critical assets are missing from your profile."
                            delay={0.4}
                        />
                        <FeatureCard
                            icon={Zap}
                            title="Skill Suggestions"
                            description="Get contextual recommendations to improve your match accuracy."
                            delay={0.5}
                        />
                        <FeatureCard
                            icon={Lock}
                            title="Secure Vault"
                            description="Your profile data is encrypted and processed locally for maximum privacy."
                            delay={0.6}
                        />
                    </div>

                    {/* SKILLMATCH IN ACTION SECTION */}
                    <div id="demo-section" className="p-10 rounded-[2.5rem] border border-white/5 relative overflow-hidden group mb-16 bg-white/[0.01]">
                        <div className="absolute top-0 right-0 p-20 opacity-[0.02] transition-all duration-1000">
                            <BarChart3 className="w-64 h-64 text-white" />
                        </div>

                        <div className="flex flex-col lg:flex-row items-center gap-20 relative z-10">
                            <div className="lg:w-1/2 space-y-6">
                                <div>
                                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/5 border border-blue-500/10 text-blue-400/60 text-[8px] font-bold tracking-widest uppercase mb-4">
                                        Smart Analysis
                                    </div>
                                    <h3 className="text-2xl md:text-3xl font-extrabold text-white tracking-tighter mb-4">See SkillMatch <br /><span className="text-blue-500 italic">In Action.</span></h3>
                                    <p className="text-white/60 font-medium text-xs leading-relaxed tracking-tight">
                                        Clear. Simple. Actionable. <br />
                                        Easy-to-use tools for complex job matching.
                                    </p>
                                </div>

                                <div className="space-y-3">
                                    {[
                                        { label: "Predictive Analytics", val: "94%" },
                                        { label: "Semantic Mapping", val: "High" },
                                        { label: "Decision Support", val: "Real-time" }
                                    ].map((stat, i) => (
                                        <div key={i} className="flex items-center justify-between p-4 rounded-xl bg-white/[0.02] border border-white/5">
                                            <span className="text-white/30 font-bold text-[9px] uppercase tracking-widest">{stat.label}</span>
                                            <span className="text-white font-bold text-xs">{stat.val}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            <div className="lg:w-1/2 w-full">
                                <motion.div
                                    whileHover={{ y: -5 }}
                                    className="p-10 rounded-3xl border border-white/10 bg-white/[0.01] transition-all"
                                >
                                    <div className="flex justify-between items-center mb-12">
                                        <div className="text-4xl font-extrabold text-white tracking-tighter">72<span className="text-blue-500/50">%</span></div>
                                        <div className="text-right">
                                            <div className="text-[8px] font-bold text-white/30 uppercase tracking-widest mb-2">Match Result</div>
                                            <div className="h-1 w-32 bg-white/5 rounded-full overflow-hidden">
                                                <motion.div initial={{ width: 0 }} whileInView={{ width: '72%' }} className="h-full bg-blue-500/60" />
                                            </div>
                                        </div>
                                    </div>

                                    <div className="space-y-8">
                                        <div>
                                            <div className="text-[8px] font-bold text-blue-400/50 uppercase tracking-widest mb-4">Your Skills</div>
                                            <div className="flex flex-wrap gap-2">
                                                {['Python', 'React', 'FastAPI', 'NLP'].map(s => (
                                                    <span key={s} className="px-3 py-1.5 border border-white/10 text-slate-300 text-[10px] font-bold rounded-lg bg-white/[0.02]">
                                                        {s}
                                                    </span>
                                                ))}
                                            </div>
                                        </div>
                                        <div>
                                            <div className="text-[8px] font-bold text-white/30 uppercase tracking-widest mb-4">Skills to Learn</div>
                                            <div className="flex flex-wrap gap-2">
                                                {['Docker', 'Redis'].map(s => (
                                                    <span key={s} className="px-3 py-1.5 border border-white/5 text-slate-500 text-[10px] font-medium rounded-lg">
                                                        {s}
                                                    </span>
                                                ))}
                                            </div>
                                        </div>
                                    </div>
                                </motion.div>
                            </div>
                        </div>
                    </div>

                    {/* WHY SKILLMATCH COMPARISON */}
                    <div className="mb-12 px-6">
                        <header className="text-center mb-12">
                            <h2 className="text-2xl md:text-3xl font-extrabold text-white mb-4 tracking-tighter">What Makes us <span className="text-blue-500/80">Different?</span></h2>
                        </header>
                        <div className="max-w-4xl mx-auto">
                            <table className="w-full border-separate border-spacing-0 border border-white/5 rounded-3xl overflow-hidden text-left bg-white/[0.01]">
                                <thead>
                                    <tr className="bg-white/[0.03] text-[9px] font-bold uppercase tracking-[0.2em] text-white/40">
                                        <th className="p-8 border-b border-white/5">Feature</th>
                                        <th className="p-8 border-b border-white/5 text-blue-400 font-black text-xs italic">SkillMatch</th>
                                        <th className="p-8 border-b border-white/5 text-white/20">Others</th>
                                    </tr>
                                </thead>
                                <tbody className="text-xs font-medium text-white/60">
                                    {[
                                        ["Match Logic", "Easy to Understand", "Black-box"],
                                        ["Feedback", "Clear results", "Generic / None"],
                                        ["Guidance", "What to learn next", "Just rejection"],
                                        ["Approach", "AI-based matching", "Text matching"]
                                    ].map(([f, s, o], i) => (
                                        <tr key={i} className="group hover:bg-white/[0.01] transition-colors">
                                            <td className="p-8 border-b border-white/5 group-last:border-b-0">{f}</td>
                                            <td className="p-8 border-b border-white/5 group-last:border-b-0 text-white font-bold">{s}</td>
                                            <td className="p-8 border-b border-white/5 group-last:border-b-0 text-white/10">{o}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>

                    {/* FAQ SECTION */}
                    <div className="mb-8 px-6">
                        <header className="text-center mb-12">
                            <h2 className="text-2xl md:text-3xl font-extrabold text-white mb-4 tracking-tighter">Frequently Asked <span className="text-blue-500/80">Questions.</span></h2>
                            <p className="text-white/40 font-bold uppercase tracking-widest text-[8px]">Answers to common questions about SkillMatch</p>
                        </header>
                        <div className="max-w-3xl mx-auto space-y-4">
                            {[
                                { q: "How does the AI Engine calculate match scores?", a: "We use advanced algorithms to map your skills to job requirements, ensuring a deep and accurate match." },
                                { q: "Is my personal resume data stored permanently?", a: "No. Your data is encrypted during the session and processed for analysis. We prioritize privacy over data harvesting." },
                                { q: "How accurate are the skill gap suggestions?", a: "Our taxonomy is updated weekly against global job trends, providing 94% accuracy in identifying critical technical requirements." },
                                { q: "Can I use SkillMatch for different industries?", a: "Currently, we are optimized for Tech, Data, and Product roles, where semantic skill mapping is most critical." }
                            ].map((faq, i) => (
                                <motion.div
                                    key={i}
                                    initial={{ opacity: 0, y: 10 }}
                                    whileInView={{ opacity: 1, y: 0 }}
                                    className="p-6 rounded-2xl border border-white/5 bg-white/[0.01] hover:bg-white/[0.02] transition-all cursor-default group"
                                >
                                    <h4 className="text-white font-bold text-sm mb-3 flex items-center justify-between">
                                        {faq.q}
                                        <Plus className="w-4 h-4 text-blue-500/30 group-hover:text-blue-500 transition-colors" />
                                    </h4>
                                    <p className="text-white/60 text-xs font-medium leading-relaxed">
                                        {faq.a}
                                    </p>
                                </motion.div>
                            ))}
                        </div>
                    </div>

                </div>
            </main>

            <footer className="py-8 glass border-t-0 mt-4 relative overflow-hidden group">
                <div className="absolute bottom-0 left-0 w-full h-[1px] bg-gradient-to-r from-blue-600 via-indigo-600 to-transparent opacity-20 group-hover:opacity-100 transition-opacity" />
                <div className="max-w-6xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-6">
                    <div className="flex flex-col md:flex-row items-center gap-10">
                        <div className="flex items-center gap-4">
                            <div className="w-9 h-9 bg-blue-600 rounded-lg flex items-center justify-center shadow-lg shadow-blue-500/20 group-hover:rotate-6 transition-transform">
                                <Sparkles className="text-white w-5 h-5" />
                            </div>
                            <div className="flex flex-col">
                                <span className="text-lg font-black text-white tracking-tighter leading-none">SkillMatch</span>
                                <span className="text-[7px] font-black text-blue-500/50 uppercase tracking-[0.3em] mt-0.5">Built with Advanced AI Technology</span>
                            </div>
                        </div>

                        <div className="relative group/input hidden lg:block">
                            <div className="absolute inset-y-0 left-4 flex items-center pointer-events-none">
                                <Mail className="w-3.5 h-3.5 text-slate-600 group-focus-within/input:text-blue-500 transition-colors" />
                            </div>
                            <input
                                type="text"
                                placeholder="STAY UPDATED"
                                className="bg-white/[0.02] border border-white/5 rounded-xl py-2.5 pl-10 pr-4 text-[9px] font-black tracking-widest text-white w-64 focus:outline-none focus:border-blue-500/30 focus:bg-white/5 transition-all"
                                readOnly
                            />
                        </div>
                    </div>

                    <div className="flex gap-8 items-center">
                        <div className="flex gap-5">
                            <a href="#" className="text-white/40 hover:text-blue-400 font-bold uppercase text-[9px] tracking-widest transition-colors">GitHub</a>
                            <a href="#" className="text-white/40 hover:text-blue-400 font-bold uppercase text-[9px] tracking-widest transition-colors">LinkedIn</a>
                        </div>
                        <div className="h-3 w-[1px] bg-white/5 hidden md:block" />
                        <p className="text-white/30 text-[9px] font-black uppercase tracking-[0.2em]">© 2026 SkillMatch AI</p>
                    </div>
                </div>
            </footer>
        </div>
    );
};

export default LandingPage;
