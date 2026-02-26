import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import Navbar from '../components/Navbar';
import api from '../utils/api';
import {
    ShieldCheck,
    Users,
    Database,
    BarChart3,
    Settings,
    Search,
    Plus,
    Loader2,
    Trash2,
    TrendingUp,
    ExternalLink,
    Zap,
    Cpu
} from 'lucide-react';

const AdminPanel = () => {
    const [stats, setStats] = useState({ total_users: 0, total_documents: 0 });
    const [skills, setSkills] = useState([]);
    const [newSkill, setNewSkill] = useState('');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const [statsRes, skillsRes] = await Promise.all([
                api.get('/documents/stats'),
                api.get('/documents/skills')
            ]);
            setStats(statsRes.data);
            setSkills(skillsRes.data.skills || []);
        } catch (error) {
            console.error('Failed to fetch admin data', error);
        }
        setLoading(false);
    };

    const handleAddSkill = async (e) => {
        e.preventDefault();
        if (!newSkill.trim()) return;
        try {
            await api.post('/documents/skills', { skill: newSkill });
            setSkills([...skills, newSkill.trim()]);
            setNewSkill('');
        } catch (error) {
            console.error('Failed to add skill', error);
        }
    };

    if (loading) return (
        <div className="min-h-screen flex flex-col items-center justify-center mesh-bg">
            <Loader2 className="w-12 h-12 animate-spin text-blue-600 mb-4" />
            <p className="text-[10px] font-black text-blue-400 uppercase tracking-[0.3em]">Connecting to System...</p>
        </div>
    );

    return (
        <div className="min-h-screen mesh-bg selection:bg-indigo-500/30 selection:text-white pb-20">
            <Navbar />
            <div className="h-24" />

            <main className="max-w-7xl mx-auto px-6 relative">
                <div className="absolute top-0 right-1/4 w-[600px] h-[600px] bg-indigo-600/10 rounded-full blur-[160px] pointer-events-none" />

                <header className="mb-14 relative z-10">
                    <div className="flex flex-col md:flex-row md:items-center justify-between gap-8">
                        <div className="flex items-center gap-4">
                            <div className="p-4 bg-indigo-600 rounded-2xl shadow-xl shadow-indigo-500/20 text-white">
                                <ShieldCheck className="w-8 h-8" />
                            </div>
                            <div>
                                <h1 className="text-3xl font-black text-white tracking-tighter leading-none">Admin Dashboard</h1>
                                <p className="text-white/40 font-bold mt-2 text-[10px] uppercase tracking-widest">Manage skills and view system statistics</p>
                            </div>
                        </div>
                        <div className="flex items-center gap-3 px-6 py-3 glass border-white/5 rounded-2xl text-slate-400 font-black text-xs uppercase tracking-widest">
                            <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
                            System Status: Online
                        </div>
                    </div>
                </header>

                {/* Stats Grid */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
                    {[
                        { label: 'Active Users', value: stats.total_users, icon: Users, color: 'text-blue-400', glassBg: 'after:bg-blue-500/10' },
                        { label: 'Analyses Performed', value: stats.total_documents, icon: BarChart3, color: 'text-indigo-400', glassBg: 'after:bg-indigo-500/10' },
                        { label: 'Ingestion Latency', value: '42ms', icon: Zap, color: 'text-amber-400', glassBg: 'after:bg-amber-500/10' },
                    ].map((stat, idx) => (
                        <motion.div
                            key={stat.label}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: idx * 0.1 }}
                            className={`glass p-8 rounded-[2.5rem] border-white/5 shadow-2xl relative overflow-hidden group ${stat.glassBg} after:absolute after:inset-0 after:opacity-0 hover:after:opacity-100 after:transition-opacity after:pointer-events-none`}
                        >
                            <div className={`w-12 h-12 bg-white/5 ${stat.color} rounded-xl flex items-center justify-center mb-6 border border-white/10 group-hover:scale-110 transition-transform`}>
                                <stat.icon className="w-6 h-6" />
                            </div>
                            <div className="text-2xl font-black text-white mb-1 tracking-tighter leading-none">{stat.value}</div>
                            <div className="text-[8px] font-black text-white/30 uppercase tracking-[0.2em]">{stat.label}</div>
                            <div className="absolute top-0 right-0 p-6 opacity-5 scale-125 rotate-12 group-hover:rotate-0 transition-all duration-700">
                                <stat.icon className="w-16 h-16 text-white" />
                            </div>
                        </motion.div>
                    ))}
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-start">
                    {/* Knowledge Base Base */}
                    <section className="lg:col-span-12">
                        <div className="glass p-10 rounded-[3rem] border-white/5 shadow-2xl relative overflow-hidden">
                            <div className="flex flex-col md:flex-row md:items-center justify-between gap-8 mb-10">
                                <div className="space-y-1">
                                    <div className="flex items-center gap-2 text-indigo-400 font-extrabold text-[8px] tracking-[0.3em] uppercase mb-1">
                                        <Cpu className="w-3.5 h-3.5" /> SKILL REPOSITORY
                                    </div>
                                    <h3 className="text-2xl font-black text-white tracking-tighter italic">Skill List</h3>
                                </div>
                                <form onSubmit={handleAddSkill} className="flex gap-3 w-full md:w-auto">
                                    <input
                                        type="text"
                                        value={newSkill}
                                        onChange={(e) => setNewSkill(e.target.value)}
                                        placeholder="Add new skill name..."
                                        className="px-6 py-3.5 glass border-white/5 rounded-2xl w-full md:w-80 focus:outline-none focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-500/30 transition-all text-white font-medium text-sm"
                                    />
                                    <button
                                        type="submit"
                                        className="p-3.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl transition-all shadow-xl shadow-indigo-500/20 active:scale-95 group"
                                    >
                                        <Plus className="w-5 h-5 group-hover:rotate-90 transition-transform" />
                                    </button>
                                </form>
                            </div>

                            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-6">
                                {skills.map((skill, idx) => (
                                    <motion.div
                                        key={skill}
                                        initial={{ opacity: 0, scale: 0.9 }}
                                        animate={{ opacity: 1, scale: 1 }}
                                        transition={{ delay: idx * 0.02 }}
                                        className="group relative px-6 py-4 glass border-white/5 rounded-2xl hover:bg-white/5 transition-all text-center cursor-default hover:-translate-y-1"
                                    >
                                        <span className="text-xs font-black text-white/80 group-hover:text-indigo-400 transition-colors tracking-tight">{skill}</span>
                                        <div className="absolute top-1 right-1 opacity-0 group-hover:opacity-100 transition-opacity">
                                            <button className="p-1.5 text-red-500 hover:bg-red-500/10 rounded-lg transition-all">
                                                <Trash2 className="w-3 h-3" />
                                            </button>
                                        </div>
                                    </motion.div>
                                ))}
                                {skills.length === 0 && (
                                    <div className="col-span-full py-20 text-center opacity-30">
                                        <Database className="w-16 h-16 mx-auto mb-6" />
                                        <p className="font-black uppercase tracking-widest text-xs">Skill Repository Empty</p>
                                    </div>
                                )}
                            </div>
                        </div>
                    </section>
                </div>
            </main>
        </div>
    );
};

export default AdminPanel;
