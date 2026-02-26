import React from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '../context/AuthContext';
import { LogOut, User, Sparkles, LayoutDashboard, History, Settings, ShieldCheck } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';

const Navbar = () => {
    const { user, logout } = useAuth();
    const location = useLocation();

    const ADMIN_EMAIL = "admin@skillmatch.com";
    const isAdmin = user?.email === ADMIN_EMAIL;

    const navItems = [
        { name: 'Analyze', path: '/analyze', icon: LayoutDashboard },
        { name: 'History', path: '/history', icon: History },
    ];

    if (isAdmin) {
        navItems.push({ name: 'Admin', path: '/admin', icon: ShieldCheck });
    }

    return (
        <nav className="fixed top-0 left-0 right-0 z-50 px-6 py-4 overflow-hidden">
            <div className="absolute inset-0 bg-slate-950/60 backdrop-blur-2xl border-b border-white/5" />

            <div className="max-w-6xl mx-auto flex items-center justify-between relative z-10">
                <Link to="/" className="flex items-center gap-2.5 group">
                    <motion.div
                        whileHover={{ rotate: 12, scale: 1.05 }}
                        className="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/20"
                    >
                        <Sparkles className="text-white w-6 h-6" />
                    </motion.div>
                    <div className="flex flex-col">
                        <span className="text-lg font-black text-white tracking-tighter leading-none group-hover:text-blue-400 transition-colors">
                            SkillMatch
                        </span>
                        <span className="text-[7px] font-black text-blue-400 uppercase tracking-[0.3em] leading-none mt-0.5">Intelligence Hub</span>
                    </div>
                </Link>

                <div className="hidden lg:flex items-center gap-1.5 p-1 glass border-white/5 rounded-2xl bg-white/[0.01]">
                    {navItems.map((item) => (
                        <Link
                            key={item.path}
                            to={item.path}
                            className={`flex items-center gap-2 px-4 py-2 rounded-xl transition-all relative ${location.pathname === item.path
                                ? 'text-white font-black'
                                : 'text-white/40 hover:text-white/80'
                                }`}
                        >
                            {location.pathname === item.path && (
                                <motion.div
                                    layoutId="nav-glow"
                                    className="absolute inset-0 bg-blue-600/10 rounded-xl border border-blue-500/10"
                                />
                            )}
                            <item.icon className={`w-3.5 h-3.5 relative z-10 ${location.pathname === item.path ? 'text-blue-400' : ''}`} />
                            <span className="text-[9px] uppercase tracking-widest relative z-10 font-bold">{item.name}</span>
                        </Link>
                    ))}
                </div>

                <div className="flex items-center gap-5">
                    <div className="flex flex-col items-end mr-1">
                        <div className="flex items-center gap-1.5">
                            <span className="text-[9px] font-black text-white tracking-tight">{user?.email?.split('@')[0]}</span>
                            <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse shadow-[0_0_5px_rgba(16,185,129,0.5)]" />
                        </div>
                        <span className="text-[7px] font-black text-white/30 uppercase tracking-[0.2em] mt-0.5">Verified Profile</span>
                    </div>

                    <div className="h-6 w-[1px] bg-white/5" />

                    <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={logout}
                        className="group p-2.5 glass border-white/5 rounded-lg text-white/40 hover:text-red-400 hover:bg-red-500/10 transition-all flex items-center gap-2"
                        title="Deauthorize Session"
                    >
                        <LogOut className="w-4 h-4" />
                        <span className="text-[9px] font-black uppercase tracking-widest hidden sm:inline">Logout</span>
                    </motion.button>
                </div>
            </div>

            {/* Ambient light bar at the bottom */}
            <div className={`absolute bottom-0 left-1/2 -translate-x-1/2 w-48 h-[1px] bg-gradient-to-r from-transparent via-blue-500/50 to-transparent transition-opacity duration-1000 ${location.pathname !== '/' ? 'opacity-100' : 'opacity-0'}`} />
        </nav>
    );
};

export default Navbar;
