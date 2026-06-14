import axios from 'axios';

const API_BASE_URL =
    import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const API = axios.create({
    baseURL: API_BASE_URL,
});

export const getPaperCount = (university) =>
    API.get('/filters/count', { params: { university } });

export const getDegrees = (university) =>
    API.get('/filters/degrees', { params: { university } });

export const getBranches = (university, degree) =>
    API.get('/filters/branches', { params: { university, degree } });

export const getSemesters = (university, degree, branch) =>
    API.get('/filters/semesters', {
        params: { university, degree, branch }
    });

export const getYearsAndMonths = (university) =>
    API.get('/filters/years-months', {
        params: { university }
    });

export const getPapers = (params) =>
    API.get('/papers', { params });