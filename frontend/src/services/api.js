import axios from 'axios';

const API = axios.create({
    baseURL: 'http://localhost:5000/api',
});

// Filters API Calls (Reads from subjects.json via backend)
export const getPaperCount = (university) => API.get('/filters/count', { params: { university } });
export const getDegrees = (university) => API.get('/filters/degrees', { params: { university } });
export const getBranches = (university, degree) => API.get('/filters/branches', { params: { university, degree } });
export const getSemesters = (university, degree, branch) => API.get('/filters/semesters', { params: { university, degree, branch } });
export const getYearsAndMonths = (university) => API.get('/filters/years-months', { params: { university } });

// Main Data API Call (Reads from papers.json via backend)
export const getPapers = (params) => API.get('/papers', { params });