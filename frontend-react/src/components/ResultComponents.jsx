import React from 'react';
import { motion } from 'framer-motion';
import { Target, AlertCircle, Sparkles, TrendingUp, CheckCircle2 } from 'lucide-react';

export const ScoreMeter = ({ score = 0, className = "" }) => {
    const safeScore = typeof score === 'number' ? score : 0;

    const getScoreColor = (s) => {
        if (s >= 80) return 'text-emerald-400';
        if (s >= 50) return 'text-blue-400';
        return 'text-amber-400';
    };

    const circumference = 2 * Math.PI * 45;
    const offset = circumference - (safeScore / 100) * circumference;

    return (
        <div className={`relative flex flex-col items-center justify-center p-8 rounded-[2rem] ${className}`}>
            <div className="relative w-48 h-48">
                <svg className="w-full h-full transform -rotate-90">
                    <circle
                        cx="96"
                        cy="96"
                        r="45"
                        fill="transparent"
                        stroke="currentColor"
                        strokeWidth="10"
                        className="text-white/5"
                    />
                    <motion.circle
                        cx="96"
                        cy="96"
                        r="45"
                        fill="transparent"
                        stroke="currentColor"
                        strokeWidth="10"
                        strokeDasharray={circumference}
                        initial={{ strokeDashoffset: circumference }}
                        animate={{ strokeDashoffset: offset }}
                        transition={{ duration: 1.5, ease: "easeOut" }}
                        className={getScoreColor(safeScore)}
                        strokeLinecap="round"
                    />
                </svg>
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <motion.span
                        initial={{ opacity: 0, scale: 0.5 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className={`text-4xl font-black tracking-tighter ${getScoreColor(safeScore)}`}
                    >
                        {Math.round(safeScore)}<span className="text-lg opacity-50">%</span>
                    </motion.span>
                    <span className="text-[9px] font-black text-white/30 uppercase tracking-widest mt-1">Match Index</span>
                </div>
            </div>
        </div>
    );
};

export const SkillSection = ({ title, skills = [], icon: Icon, colorClass, delay = 0, className = "" }) => {
    const safeSkills = Array.isArray(skills) ? skills : [];

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay }}
            className={`p-8 rounded-[2rem] ${className}`}
        >
            <div className="flex items-center gap-3 mb-6">
                <div className={`p-2.5 rounded-xl ${colorClass.replace('bg-', 'bg-')}/10`}>
                    <Icon className={`w-5 h-5 ${colorClass.replace('bg-', 'text-')}`} />
                </div>
                <h3 className="font-black text-white text-base tracking-tight">{title}</h3>
                <span className="ml-auto text-[10px] font-black text-white/20 bg-white/5 px-2.5 py-1 rounded-lg border border-white/5">
                    {safeSkills.length} Units
                </span>
            </div>
            <div className="flex flex-wrap gap-2.5">
                {safeSkills.length > 0 ? (
                    safeSkills.map((skill, idx) => (
                        <motion.span
                            key={skill}
                            initial={{ scale: 0.9, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            transition={{ delay: delay + (idx * 0.05) }}
                            className={`px-3.5 py-2 rounded-xl text-[10px] font-bold border border-white/5 bg-white/[0.02] text-white/80 hover:border-blue-500/30 hover:bg-blue-500/5 transition-all cursor-default shadow-sm`}
                        >
                            {skill}
                        </motion.span>
                    ))
                ) : (
                    <div className="w-full py-4 text-center border border-dashed border-white/10 rounded-2xl">
                        <span className="text-[10px] text-white/20 font-bold uppercase tracking-widest">No matching identifiers</span>
                    </div>
                )}
            </div>
        </motion.div>
    );
};
