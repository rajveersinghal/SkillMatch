import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Lock, Mail, Loader2, UserPlus, ArrowRight, Home } from 'lucide-react';

const RegisterPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const { register } = useAuth();
    const navigate = useNavigate();

    const validateEmail = (email) => {
        return String(email)
            .toLowerCase()
            .match(
                /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
            );
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if (!validateEmail(email)) {
            setError('Please enter a valid email address.');
            return;
        }

        setLoading(true);

        const result = await register(email, password);
        if (result.success) {
            navigate('/login');
        } else {
            setError(result.error);
        }
        setLoading(false);
    };

    return (
        <div className="min-h-screen mesh-bg flex items-center justify-center p-4 md:p-6 relative overflow-y-auto py-10 md:py-20">
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-indigo-600/20 rounded-full blur-[120px] pointer-events-none" />

            <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="w-full max-w-md z-10"
            >
                <div className="glass p-8 md:p-12 rounded-[2.5rem] md:rounded-[3.5rem] border-white/5 shadow-2xl relative overflow-hidden group">
                    <div className="absolute inset-x-0 bottom-0 h-1 bg-gradient-to-r from-indigo-600 to-blue-600 opacity-50 group-focus-within:opacity-100 transition-opacity" />

                    <Link
                        to="/"
                        className="absolute top-8 left-8 p-3 glass border-white/5 rounded-xl text-white/30 hover:text-white hover:bg-white/5 transition-all group/home"
                        title="Back to Home"
                    >
                        <Home className="w-5 h-5 group-hover/home:scale-110 transition-transform" />
                    </Link>

                    <div className="flex flex-col items-center mb-12">
                        <motion.div
                            initial={{ rotate: 10 }}
                            animate={{ rotate: 0 }}
                            className="w-20 h-20 bg-indigo-600 rounded-[2rem] flex items-center justify-center shadow-2xl shadow-indigo-500/20 mb-6"
                        >
                            <UserPlus className="text-white w-10 h-10" />
                        </motion.div>
                        <h1 className="text-3xl font-black text-white tracking-tighter">
                            SkillMatch <span className="text-indigo-400 italic">Sign Up</span>
                        </h1>
                        <p className="text-white/40 font-bold mt-2 uppercase tracking-[0.2em] text-[9px]">Create your account</p>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-8">
                        <div className="space-y-3">
                            <label className="text-[9px] font-black text-white/40 uppercase tracking-[0.2em] ml-2">Email Address</label>
                            <div className="relative">
                                <Mail className="absolute left-6 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
                                <input
                                    type="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    placeholder="agent@skillmatch.com"
                                    className="w-full pl-16 pr-6 py-5 bg-white/5 border border-white/5 rounded-[1.5rem] focus:outline-none focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-500/30 text-white font-medium transition-all"
                                    required
                                />
                            </div>
                        </div>

                        <div className="space-y-3">
                            <label className="text-[9px] font-black text-white/40 uppercase tracking-[0.2em] ml-2">Password</label>
                            <div className="relative">
                                <Lock className="absolute left-6 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
                                <input
                                    type="password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    placeholder="••••••••"
                                    className="w-full pl-16 pr-6 py-5 bg-white/5 border border-white/5 rounded-[1.5rem] focus:outline-none focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-500/30 text-white font-medium transition-all"
                                    required
                                />
                            </div>
                        </div>

                        {error && (
                            <motion.div
                                initial={{ opacity: 0, x: -10 }}
                                animate={{ opacity: 1, x: 0 }}
                                className="p-4 glass bg-red-500/10 border-red-500/20 rounded-2xl text-red-400 text-[10px] font-bold leading-relaxed flex items-center gap-3"
                            >
                                <div className="w-1.5 h-1.5 bg-red-500 rounded-full animate-pulse" />
                                {error}
                            </motion.div>
                        )}

                        <button
                            type="submit"
                            disabled={loading}
                            className="group relative w-full py-6 bg-indigo-600 hover:bg-indigo-500 disabled:bg-white/5 disabled:text-slate-600 text-white font-black rounded-[2rem] transition-all flex items-center justify-center gap-4 shadow-2xl shadow-indigo-900/20 active:scale-[0.98] text-base uppercase tracking-[0.2em] overflow-hidden"
                        >
                            <span className="relative z-10">{loading ? 'Creating Account...' : 'Sign Up'}</span>
                            {loading ? <Loader2 className="w-6 h-6 animate-spin relative z-10" /> : <ArrowRight className="w-6 h-6 relative z-10 group-hover:translate-x-1 transition-transform" />}
                            <div className="absolute inset-0 bg-gradient-to-r from-indigo-400 to-blue-400 opacity-0 group-hover:opacity-100 transition-opacity" />
                        </button>
                    </form>

                    <p className="mt-12 text-center text-white/30 text-[10px] font-bold">
                        Already have an account? {' '}
                        <Link to="/login" className="text-indigo-400 hover:text-indigo-300 transition-colors underline decoration-2 underline-offset-8 uppercase tracking-widest ml-2">
                            Sign In
                        </Link>
                    </p>
                </div>
            </motion.div>
        </div>
    );
};

export default RegisterPage;
