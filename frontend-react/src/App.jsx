import React, { useEffect, lazy, Suspense } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Loader2 } from 'lucide-react';
import { AuthProvider, useAuth } from './context/AuthContext';

// Lazy load components
const LoginPage = lazy(() => import('./pages/LoginPage'));
const RegisterPage = lazy(() => import('./pages/RegisterPage'));
const Dashboard = lazy(() => import('./pages/Dashboard'));
const HistoryPage = lazy(() => import('./pages/HistoryPage'));
const AdminPanel = lazy(() => import('./pages/AdminPanel'));
const LandingPage = lazy(() => import('./pages/LandingPage'));

const ProtectedRoute = ({ children, adminOnly = false }) => {
  const { token, loading, user } = useAuth();

  if (loading) return <div className="flex items-center justify-center min-h-screen"><Loader2 className="animate-spin text-blue-600" /></div>;
  if (!token) return <Navigate to="/login" />;

  const ADMIN_EMAIL = "admin@skillmatch.com";
  if (adminOnly && user?.email !== ADMIN_EMAIL) {
    return <Navigate to="/" />;
  }

  return children;
};

// Loading fallback component
const PageLoader = () => (
  <div className="flex items-center justify-center min-h-screen">
    <Loader2 className="animate-spin text-blue-600" />
  </div>
);

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-slate-50 text-slate-900">
          <Suspense fallback={<PageLoader />}>
            <Routes>
              <Route path="/" element={<LandingPage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route path="/analyze" element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              } />
              <Route path="/history" element={
                <ProtectedRoute>
                  <HistoryPage />
                </ProtectedRoute>
              } />
              <Route path="/admin" element={
                <ProtectedRoute adminOnly>
                  <AdminPanel />
                </ProtectedRoute>
              } />
              <Route path="*" element={<Navigate to="/" />} />
            </Routes>
          </Suspense>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
