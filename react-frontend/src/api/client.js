import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const client = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor for Auth Token
client.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export const authApi = {
    login: (email, password) => {
        const formData = new FormData();
        formData.append('username', email);
        formData.append('password', password);
        return client.post('/auth/login', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
    },
    register: (email, password) => {
        return client.post('/auth/register', { email, password });
    },
};

export const ingestionApi = {
    ingest: (type, data) => {
        const formData = new FormData();
        formData.append('data_type', type);
        if (data.file) {
            formData.append('file', data.file);
            return client.post('/ingestion/ingest', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
        } else {
            formData.append('text', data.text);
            return client.post('/ingestion/ingest', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
        }
    },
    getLatest: (type) => client.get(`/ingestion/latest/${type}`),
};

export default client;
