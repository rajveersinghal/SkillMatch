import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { Rocket, Target, Zap } from 'lucide-react';

const Landing = () => {
    return (
        <div className="min-h-screen bg-rose-50 flex flex-col items-center justify-center p-6 text-center">
            <motion.div
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                className="max-w-4xl"
            >
                <h1 className="text-6xl font-extrabold text-slate-800 mb-6">
                    Find Your Perfect <span className="text-rose-200">Skill Match</span>
                </h1>
                <p className="text-xl text-slate-800 mb-12 opacity-80">
                    The ultimate platform for resume matching and skill gap analysis.
                    Upload your resume and get instant job compatibility suggestions.
                </p>

                <div className="flex gap-6 justify-center mb-16">
                    <Link to="/signup" className="primary-button text-lg px-8">
                        Get Started Free
                    </Link>
                    <Link to="/login" className="bg-white text-rose-200 font-bold py-3 px-8 rounded-xl border border-rose-100 hover:bg-rose-50 transition-all">
                        Sign In
                    </Link>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    {[
                        { icon: <Rocket className="text-rose-200" />, title: "Fast Analysis", desc: "Get instant results from our advanced algorithms." },
                        { icon: <Target className="text-rose-200" />, title: "Precise Matching", desc: "Compare skills with industry-standard job descriptions." },
                        { icon: <Zap className="text-rose-200" />, title: "Smart Suggestions", desc: "Identify missing skills and get learning paths." }
                    ].map((feature, i) => (
                        <motion.div
                            key={i}
                            whileHover={{ y: -5 }}
                            className="glass-card p-6"
                        >
                            <div className="mb-4 flex justify-center">{feature.icon}</div>
                            <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
                            <p className="text-sm opacity-70">{feature.desc}</p>
                        </motion.div>
                    ))}
                </div>
            </motion.div>
        </div>
    );
};

export default Landing;
