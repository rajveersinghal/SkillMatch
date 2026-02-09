import { useState } from 'react';
import { motion } from 'framer-motion';
import { Link, useNavigate } from 'react-router-dom';
import { authApi } from '../api/client';
import { UserPlus, Mail, Lock, Loader2, CheckCircle2, ChevronLeft } from 'lucide-react';

const Signup = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        try {
            await authApi.register(email, password);
            setSuccess(true);
            setTimeout(() => navigate('/login'), 2000);
        } catch (err) {
            setError(err.response?.data?.detail || 'Registration failed');
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
                {!success && (
                    <Link
                        to="/"
                        className="absolute top-6 left-6 text-slate-800 opacity-40 hover:opacity-100 transition-opacity flex items-center gap-1 text-sm font-semibold"
                    >
                        <ChevronLeft size={18} /> Home
                    </Link>
                )}
                {success ? (
                    <div className="flex flex-col items-center py-12 text-center">
                        <motion.div
                            initial={{ scale: 0 }}
                            animate={{ scale: 1 }}
                            className="bg-green-100 p-4 rounded-full mb-6"
                        >
                            <CheckCircle2 className="text-green-500" size={48} />
                        </motion.div>
                        <h2 className="text-3xl font-bold text-slate-800 mb-2">Account Created!</h2>
                        <p className="text-slate-800 opacity-60">Redirecting to login...</p>
                    </div>
                ) : (
                    <>
                        <div className="flex flex-col items-center mb-8">
                            <div className="bg-rose-100 p-4 rounded-full mb-4">
                                <UserPlus className="text-rose-200" size={32} />
                            </div>
                            <h2 className="text-3xl font-bold text-slate-800">Create Account</h2>
                            <p className="text-slate-800 opacity-60">Join SkillMatch today</p>
                        </div>

                        {error && (
                            <div className="bg-red-50 text-red-500 p-3 rounded-xl mb-6 text-sm font-medium border border-red-100">
                                {error}
                            </div>
                        )}

                        <form onSubmit={handleSubmit} className="space-y-6">
                            <div>
                                <label className="block text-sm font-semibold mb-2 ml-1 text-slate-800/80">Email Address</label>
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
                                        placeholder="Min 8 characters"
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
                                {loading ? <Loader2 className="animate-spin" size={20} /> : 'Sign Up'}
                            </button>
                        </form>

                        <p className="text-center mt-8 text-sm">
                            Already have an account? {' '}
                            <Link to="/login" className="text-rose-300 font-bold hover:underline">
                                Sign In
                            </Link>
                        </p>
                    </>
                )}
            </motion.div>
        </div>
    );
};

export default Signup;
