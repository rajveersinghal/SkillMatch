import axios from 'axios';

console.log("DEBUG: API Base URL initialized as:", import.meta.env.VITE_API_URL || '/api');
const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || '/api',
});

// Add interceptor to add token to requests
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

export default api;
