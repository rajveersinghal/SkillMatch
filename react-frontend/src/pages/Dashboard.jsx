import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '../context/AuthContext';
import { ingestionApi } from '../api/client';
import {
    BarChart3,
    Upload,
    FileText,
    Briefcase,
    History,
    LogOut,
    CheckCircle2,
    AlertCircle,
    Loader2,
    ChevronRight
} from 'lucide-react';

const SidebarItem = ({ icon, label, active, onClick, disabled }) => (
    <button
        disabled={disabled}
        onClick={onClick}
        className={`w-full flex items-center gap-4 px-6 py-4 rounded-xl transition-all duration-300 ${active
            ? 'bg-rose-200 text-white shadow-lg'
            : 'hover:bg-rose-100 text-slate-800 opacity-70 hover:opacity-100'
            } ${disabled ? 'cursor-not-allowed grayscale' : 'cursor-pointer'}`}
    >
        {icon}
        <span className="font-semibold">{label}</span>
    </button>
);

const Dashboard = () => {
    const { userEmail, logout } = useAuth();
    const [activeTab, setActiveTab] = useState('Dashboard');
    const [resumeText, setResumeText] = useState('');
    const [jdText, setJdText] = useState('');
    const [resumeFile, setResumeFile] = useState(null);
    const [jdFile, setJdFile] = useState(null);
    const [ingesting, setIngesting] = useState(null);
    const [success, setSuccess] = useState(null);
    const [extractedResume, setExtractedResume] = useState('');
    const [extractedJd, setExtractedJd] = useState('');

    const handleIngest = async (type) => {
        const text = type === 'resume' ? resumeText : jdText;
        const file = type === 'resume' ? resumeFile : jdFile;

        if (!text && !file) return;

        setIngesting(type);
        setSuccess(null);
        try {
            const data = file ? { file } : { text };
            const response = await ingestionApi.ingest(type, data);

            if (type === 'resume') {
                setExtractedResume(response.data.content);
            } else {
                setExtractedJd(response.data.content);
            }

            setSuccess(type);
        } catch (err) {
            console.error(err);
        } finally {
            setIngesting(null);
        }
    };

    const handleReset = (type) => {
        setSuccess(null);
        if (type === 'resume') {
            setExtractedResume('');
            setResumeFile(null);
            setResumeText('');
        } else {
            setExtractedJd('');
            setJdFile(null);
            setJdText('');
        }
    };

    const handlePlaceholderClick = (name) => {
        alert(`${name} is in processing...`);
    };

    return (
        <div className="flex h-screen bg-rose-50 overflow-hidden">
            {/* Sidebar */}
            <aside className="w-80 bg-white border-r border-rose-100 flex flex-col p-6">
                <div className="mb-12 px-4 flex items-center gap-3">
                    <div className="w-10 h-10 bg-rose-200 rounded-xl flex items-center justify-center text-white font-black text-xl shadow-lg ring-4 ring-rose-100">SM</div>
                    <h1 className="text-3xl font-black text-rose-200 tracking-tight">SkillMatch</h1>
                </div>

                <div className="flex-1 space-y-2">
                    <SidebarItem
                        icon={<BarChart3 />}
                        label="Dashboard"
                        active={activeTab === 'Dashboard'}
                        onClick={() => setActiveTab('Dashboard')}
                    />
                    <SidebarItem
                        icon={<FileText />}
                        label="My Resumes"
                        onClick={() => handlePlaceholderClick('My Resumes')}
                    />
                    <SidebarItem
                        icon={<Briefcase />}
                        label="Job Descriptions"
                        onClick={() => handlePlaceholderClick('Job Descriptions')}
                    />
                    <SidebarItem
                        icon={<History />}
                        label="History"
                        onClick={() => handlePlaceholderClick('History')}
                    />
                </div>

                <div className="border-t border-rose-100 pt-6">
                    <div className="bg-rose-50 rounded-2xl p-4 mb-6">
                        <p className="text-xs text-slate-800 opacity-50 uppercase font-black tracking-widest mb-1">Authenticated</p>
                        <p className="text-sm font-bold truncate text-slate-800">{userEmail}</p>
                    </div>
                    <button
                        onClick={logout}
                        className="w-full flex items-center gap-4 px-6 py-4 rounded-xl hover:bg-red-50 text-red-500 transition-all font-bold"
                    >
                        <LogOut size={20} />
                        Logout
                    </button>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 overflow-y-auto p-12">
                <motion.div
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="max-w-6xl mx-auto"
                >
                    <header className="mb-12">
                        <h2 className="text-4xl font-extrabold text-slate-800">Dashboard</h2>
                        <p className="text-slate-800 opacity-60">Upload and manage your professional data</p>
                    </header>

                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
                        <motion.div className="glass-card p-8 flex flex-col h-full" layout>
                            <div className="flex items-center justify-between mb-6">
                                <div className="flex items-center gap-3">
                                    <div className="p-3 bg-rose-100 rounded-xl">
                                        <FileText className="text-rose-200" />
                                    </div>
                                    <h3 className="text-2xl font-bold">Resume</h3>
                                </div>
                                <label className="cursor-pointer hover:bg-rose-50 p-2 rounded-lg transition-colors border border-dashed border-rose-200">
                                    <Upload size={18} className="text-rose-300" />
                                    <input
                                        type="file"
                                        className="hidden"
                                        accept=".pdf,.docx,.txt"
                                        onChange={(e) => setResumeFile(e.target.files[0])}
                                    />
                                </label>
                            </div>

                            {extractedResume ? (
                                <div className="flex-1 min-h-[400px] mb-6 relative">
                                    <div className="absolute top-4 right-4 bg-green-100 text-green-600 px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1">
                                        <CheckCircle2 size={12} /> Extracted
                                    </div>
                                    <textarea
                                        readOnly
                                        className="input-field w-full h-full min-h-[400px] resize-none opacity-80 cursor-default bg-rose-50/20"
                                        value={extractedResume}
                                    />
                                </div>
                            ) : resumeFile ? (
                                <div className="flex-1 min-h-[400px] mb-6 border-2 border-dashed border-rose-100 rounded-2xl flex flex-col items-center justify-center p-8 bg-rose-50/30">
                                    <FileText size={64} className="text-rose-200 mb-4" />
                                    <p className="font-bold text-slate-800">{resumeFile.name}</p>
                                    <p className="text-sm text-slate-800 opacity-50 mb-6">{(resumeFile.size / 1024).toFixed(2)} KB</p>
                                    <button
                                        onClick={() => setResumeFile(null)}
                                        className="text-rose-300 font-bold text-sm hover:underline"
                                    >
                                        Remove & Paste Text instead
                                    </button>
                                </div>
                            ) : (
                                <textarea
                                    className="input-field flex-1 min-h-[400px] mb-6 resize-none"
                                    placeholder="Paste your resume content here..."
                                    value={resumeText}
                                    onChange={(e) => setResumeText(e.target.value)}
                                />
                            )}

                            {extractedResume ? (
                                <button
                                    onClick={() => handleReset('resume')}
                                    className="primary-button bg-slate-800 hover:bg-slate-900 border-none"
                                >
                                    Start New Analysis
                                </button>
                            ) : (
                                <button
                                    onClick={() => handleIngest('resume')}
                                    disabled={ingesting === 'resume' || (!resumeText && !resumeFile)}
                                    className={`primary-button flex items-center justify-center gap-3 ${((!resumeText && !resumeFile) || ingesting) && 'opacity-50 cursor-not-allowed'}`}
                                >
                                    {ingesting === 'resume' ? <Loader2 className="animate-spin" /> : <Upload size={20} />}
                                    Analyze Resume
                                </button>
                            )}
                        </motion.div>

                        <motion.div className="glass-card p-8 flex flex-col h-full" layout>
                            <div className="flex items-center justify-between mb-6">
                                <div className="flex items-center gap-3">
                                    <div className="p-3 bg-rose-100 rounded-xl">
                                        <Briefcase className="text-rose-200" />
                                    </div>
                                    <h3 className="text-2xl font-bold">Job Description</h3>
                                </div>
                                <label className="cursor-pointer hover:bg-rose-50 p-2 rounded-lg transition-colors border border-dashed border-rose-200">
                                    <Upload size={18} className="text-rose-300" />
                                    <input
                                        type="file"
                                        className="hidden"
                                        accept=".pdf,.docx,.txt"
                                        onChange={(e) => setJdFile(e.target.files[0])}
                                    />
                                </label>
                            </div>

                            {extractedJd ? (
                                <div className="flex-1 min-h-[400px] mb-6 relative">
                                    <div className="absolute top-4 right-4 bg-green-100 text-green-600 px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1">
                                        <CheckCircle2 size={12} /> Extracted
                                    </div>
                                    <textarea
                                        readOnly
                                        className="input-field w-full h-full min-h-[400px] resize-none opacity-80 cursor-default bg-rose-50/20"
                                        value={extractedJd}
                                    />
                                </div>
                            ) : jdFile ? (
                                <div className="flex-1 min-h-[400px] mb-6 border-2 border-dashed border-rose-100 rounded-2xl flex flex-col items-center justify-center p-8 bg-rose-50/30">
                                    <Briefcase size={64} className="text-rose-200 mb-4" />
                                    <p className="font-bold text-slate-800">{jdFile.name}</p>
                                    <p className="text-sm text-slate-800 opacity-50 mb-6">{(jdFile.size / 1024).toFixed(2)} KB</p>
                                    <button
                                        onClick={() => setJdFile(null)}
                                        className="text-rose-300 font-bold text-sm hover:underline"
                                    >
                                        Remove & Paste Text instead
                                    </button>
                                </div>
                            ) : (
                                <textarea
                                    className="input-field flex-1 min-h-[400px] mb-6 resize-none"
                                    placeholder="Paste the job description here..."
                                    value={jdText}
                                    onChange={(e) => setJdText(e.target.value)}
                                />
                            )}

                            {extractedJd ? (
                                <button
                                    onClick={() => handleReset('jd')}
                                    className="primary-button bg-slate-800 hover:bg-slate-900 border-none"
                                >
                                    Start New Analysis
                                </button>
                            ) : (
                                <button
                                    onClick={() => handleIngest('jd')}
                                    disabled={ingesting === 'jd' || (!jdText && !jdFile)}
                                    className={`primary-button flex items-center justify-center gap-3 ${((!jdText && !jdFile) || ingesting) && 'opacity-50 cursor-not-allowed'}`}
                                >
                                    {ingesting === 'jd' ? <Loader2 className="animate-spin" /> : <Upload size={20} />}
                                    Analyze Job Description
                                </button>
                            )}
                        </motion.div>
                    </div>
                </motion.div>
            </main>
        </div>
    );
};

export default Dashboard;
