import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Navbar from '../components/Navbar';
import api from '../utils/api';
import { History as HistoryIcon, ChevronRight, Calendar, Target, FileText, Trash2, Loader2, Sparkles, Filter, AlertCircle, Search } from 'lucide-react';

const HistoryPage = () => {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedItem, setSelectedItem] = useState(null);

    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async () => {
        try {
            const response = await api.get('/documents/history');
            setHistory(response.data);
        } catch (error) {
            console.error('Failed to fetch history', error);
        }
        setLoading(false);
    };

    const deleteEntry = async (id) => {
        if (!window.confirm('Are you sure you want to delete this analysis?')) return;
        try {
            await api.delete(`/documents/${id}`);
            setHistory(history.filter(item => item._id !== id));
            if (selectedItem?._id === id) setSelectedItem(null);
        } catch (error) {
            console.error('Delete failed', error);
        }
    };

    return (
        <div className="min-h-screen mesh-bg selection:bg-blue-500/30 selection:text-white pb-20">
            <Navbar />
            <div className="h-24" />

            <main className="max-w-7xl mx-auto px-6 relative">
                <div className="absolute top-0 left-1/4 w-[500px] h-[500px] bg-blue-600/10 rounded-full blur-[120px] pointer-events-none" />

                <div className="flex flex-col lg:flex-row gap-12 items-start">
                    {/* Sidebar Pane */}
                    <aside className="lg:w-1/3 w-full space-y-6 lg:sticky lg:top-28">
                        <header className="flex items-center justify-between px-1">
                            <div className="flex items-center gap-2.5">
                                <div className="p-2.5 bg-blue-600 rounded-lg shadow-lg shadow-blue-500/20 text-white">
                                    <HistoryIcon className="w-4 h-4" />
                                </div>
                                <h2 className="text-lg font-black text-white tracking-tight leading-none">Analysis History</h2>
                            </div>
                            <span className="text-[8px] font-black text-white/60 bg-white/5 px-3 py-1 rounded-full border border-white/5 uppercase tracking-widest leading-none">
                                {history.length} Sessions
                            </span>
                        </header>

                        <div className="flex flex-col gap-4 max-h-[70vh] overflow-y-auto custom-scrollbar pr-2">
                            {loading ? (
                                <div className="flex flex-col items-center justify-center p-20 glass rounded-[2.5rem]">
                                    <Loader2 className="w-8 h-8 animate-spin text-blue-500 mb-4" />
                                    <p className="text-xs font-black text-slate-500 uppercase tracking-widest">Loading History...</p>
                                </div>
                            ) : history.length > 0 ? (
                                history.map((item, idx) => (
                                    <motion.button
                                        key={item._id}
                                        initial={{ opacity: 0, x: -20 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        transition={{ delay: idx * 0.05 }}
                                        onClick={() => setSelectedItem(item)}
                                        className={`group relative p-4 rounded-2xl flex items-center gap-4 transition-all text-left overflow-hidden ${selectedItem?._id === item._id
                                            ? 'glass border-blue-500/20 shadow-xl bg-blue-500/5'
                                            : 'glass border-white/5 hover:border-white/10 hover:bg-white/5'
                                            }`}
                                    >
                                        {selectedItem?._id === item._id && (
                                            <div className="absolute inset-y-0 left-0 w-1 bg-blue-600 shadow-[0_0_10px_rgba(37,99,235,0.8)]" />
                                        )}
                                        <div className={`p-3 rounded-xl transition-colors ${selectedItem?._id === item._id ? 'bg-blue-600 text-white' : 'bg-white/5 text-slate-400 group-hover:text-blue-400'}`}>
                                            <FileText className="w-4 h-4" />
                                        </div>
                                        <div className="flex-1 min-w-0">
                                            <p className={`text-[10px] font-black truncate tracking-tight ${selectedItem?._id === item._id ? 'text-white' : 'text-slate-300'}`}>
                                                {item.job_description.slice(0, 30)}...
                                            </p>
                                            <footer className="flex items-center gap-2 mt-1 tooltip text-[8px] font-black uppercase tracking-widest text-slate-500">
                                                <span>{new Date(item.created_at).toLocaleDateString()}</span>
                                                <span className="w-1 h-1 bg-slate-700 rounded-full" />
                                                <span className="text-blue-500/70">{Math.round(item.match_percentage)}% FIT</span>
                                            </footer>
                                        </div>
                                        <ChevronRight className={`w-4 h-4 transition-transform ${selectedItem?._id === item._id ? 'text-blue-500 translate-x-1' : 'text-slate-600'}`} />
                                    </motion.button>
                                ))
                            ) : (
                                <div className="p-20 text-center glass rounded-[3rem] border-white/5">
                                    <HistoryIcon className="text-slate-700 w-12 h-12 mx-auto mb-6 opacity-20" />
                                    <p className="text-slate-500 text-xs font-black uppercase tracking-widest leading-loose">No history found.<br />Start your first match to see results here.</p>
                                </div>
                            )}
                        </div>
                    </aside>

                    {/* Main Detail View */}
                    <section className="flex-1 min-w-0">
                        <AnimatePresence mode="wait">
                            {selectedItem ? (
                                <motion.div
                                    key={selectedItem._id}
                                    initial={{ opacity: 0, y: 30 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    exit={{ opacity: 0, y: -30 }}
                                    className="space-y-8"
                                >
                                    <div className="glass p-8 rounded-[2rem] border-white/5 relative overflow-hidden group">
                                        <div className="absolute top-0 right-0 p-8 opacity-5 scale-125 rotate-12 group-hover:rotate-0 transition-all duration-1000">
                                            <Target className="w-40 h-40 text-white" />
                                        </div>

                                        <div className="flex justify-between items-start mb-8 relative z-10">
                                            <div className="space-y-1">
                                                <div className="flex items-center gap-2.5 text-blue-400 font-extrabold text-[9px] tracking-[0.3em] uppercase mb-2">
                                                    <Sparkles className="w-3.5 h-3.5" /> AI Analysis Result
                                                </div>
                                                <h3 className="text-2xl font-black text-white tracking-tighter italic">Analysis Details</h3>
                                            </div>
                                            <button
                                                onClick={() => deleteEntry(selectedItem._id)}
                                                className="p-3 glass rounded-xl text-red-400/30 hover:text-red-400 hover:bg-red-500/10 transition-all"
                                            >
                                                <Trash2 className="w-5 h-5" />
                                            </button>
                                        </div>

                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 relative z-10">
                                            <div className="space-y-3">
                                                <label className="text-[8px] font-black text-white/40 uppercase tracking-[0.2em]">Job Description</label>
                                                <div className="p-5 bg-white/[0.02] border border-white/5 rounded-2xl text-white/80 text-[10px] leading-relaxed font-medium h-40 overflow-y-auto custom-scrollbar">
                                                    {selectedItem.job_description}
                                                </div>
                                            </div>
                                            <div className="space-y-3">
                                                <label className="text-[8px] font-black text-white/40 uppercase tracking-[0.2em]">Resume Content</label>
                                                <div className="p-5 bg-white/[0.02] border border-white/5 rounded-2xl text-white/80 text-[10px] leading-relaxed font-medium h-40 overflow-y-auto custom-scrollbar">
                                                    {selectedItem.resume_text}
                                                </div>
                                            </div>
                                        </div>
                                    </div>

                                    {/* Score Summary */}
                                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                                        <div className="glass p-6 rounded-2xl border-white/5 text-center flex flex-col items-center justify-center">
                                            <div className="text-3xl font-black text-blue-500 mb-1 tracking-tighter leading-none">{Math.round(selectedItem.match_percentage)}%</div>
                                            <div className="text-[8px] font-black text-white/30 uppercase tracking-widest leading-none">Total Match Score</div>
                                        </div>
                                        <div className="glass p-6 rounded-2xl border-white/5 text-center flex flex-col items-center justify-center">
                                            <div className="text-xl font-black text-white mb-1 leading-none">{selectedItem.matched_skills?.length || 0}</div>
                                            <div className="text-[8px] font-black text-white/30 uppercase tracking-widest leading-none">Found Skills</div>
                                        </div>
                                        <div className="glass p-6 rounded-2xl border-white/5 text-center flex flex-col items-center justify-center">
                                            <div className="text-xl font-black text-amber-500 mb-1 leading-none">{selectedItem.missing_skills?.length || 0}</div>
                                            <div className="text-[8px] font-black text-white/30 uppercase tracking-widest leading-none">Missing Skills</div>
                                        </div>
                                    </div>
                                </motion.div>
                            ) : (
                                <div className="h-full flex flex-col items-center justify-center p-20 glass rounded-[4rem] border-white/5 border-dashed border-2 opacity-50">
                                    <div className="w-24 h-24 bg-white/5 rounded-full flex items-center justify-center mb-8">
                                        <Search className="text-slate-500 w-10 h-10" />
                                    </div>
                                    <h3 className="text-2xl font-black text-white mb-3 tracking-tight">Select Session</h3>
                                    <p className="text-slate-500 font-medium">Choose an entry from the Analysis History to review details.</p>
                                </div>
                            )}
                        </AnimatePresence>
                    </section>
                </div>
            </main>
        </div>
    );
};

export default HistoryPage;
