import { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [token, setToken] = useState(localStorage.getItem('token'));
    const [userEmail, setUserEmail] = useState(localStorage.getItem('userEmail'));

    const login = (newToken, email) => {
        localStorage.setItem('token', newToken);
        localStorage.setItem('userEmail', email);
        setToken(newToken);
        setUserEmail(email);
    };

    const logout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('userEmail');
        setToken(null);
        setUserEmail(null);
    };

    return (
        <AuthContext.Provider value={{ token, userEmail, login, logout, isAuthenticated: !!token }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
