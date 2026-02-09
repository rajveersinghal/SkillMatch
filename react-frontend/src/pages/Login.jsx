import { useState } from 'react';
import { motion } from 'framer-motion';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { authApi } from '../api/client';
import { LogIn, Mail, Lock, Loader2, ChevronLeft } from 'lucide-react';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        try {
            const { data } = await authApi.login(email, password);
            login(data.access_token, email);
            navigate('/dashboard');
        } catch (err) {
            setError(err.response?.data?.detail || 'Invalid credentials');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-rose-50 flex items-center justify-center p-6">
            <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="glass-card w-full max-w-md p-8 relative"
            >
                <Link
                    to="/"
                    className="absolute top-6 left-6 text-slate-800 opacity-40 hover:opacity-100 transition-opacity flex items-center gap-1 text-sm font-semibold"
                >
                    <ChevronLeft size={18} /> Home
                </Link>

                <div className="flex flex-col items-center mb-8">
                    <div className="bg-rose-100 p-4 rounded-full mb-4">
                        <LogIn className="text-rose-200" size={32} />
                    </div>
                    <h2 className="text-3xl font-bold text-slate-800">Welcome Back</h2>
                    <p className="text-slate-800 opacity-60">Sign in to your account</p>
                </div>

                {error && (
                    <div className="bg-red-50 text-red-500 p-3 rounded-xl mb-6 text-sm font-medium border border-red-100">
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                        <label className="block text-sm font-semibold mb-2 ml-1">Email Address</label>
                        <div className="relative">
                            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                <Mail className="text-slate-800 opacity-40" size={20} />
                            </div>
                            <input
                                type="email"
                                required
                                className="input-field !pl-12"
                                placeholder="you@example.com"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                            />
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-semibold mb-2 ml-1 text-slate-800/80">Password</label>
                        <div className="relative">
                            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                <Lock className="text-slate-800 opacity-40" size={20} />
                            </div>
                            <input
                                type="password"
                                required
                                className="input-field !pl-12"
                                placeholder="••••••••"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                        </div>
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="primary-button w-full flex items-center justify-center gap-2"
                    >
                        {loading ? <Loader2 className="animate-spin" size={20} /> : 'Sign In'}
                    </button>
                </form>

                <p className="text-center mt-8 text-sm">
                    Don't have an account? {' '}
                    <Link to="/signup" className="text-rose-300 font-bold hover:underline">
                        Sign Up
                    </Link>
                </p>
            </motion.div>
        </div>
    );
};

export default Login;
