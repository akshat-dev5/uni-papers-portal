import { readJsonFile } from '../utils/fileReader.js';

export const getDegrees = async (req, res) => {
    try {
        const { university } = req.query;
        if (!university) return res.status(400).json({ error: "University is required" });

        const fileName = `${university}_subjects.json`;
        const subjects = await readJsonFile(university, fileName);
        
        const degrees = [...new Set(subjects.map(item => item.degree).filter(Boolean))];
        res.status(200).json(degrees);
    } catch (error) {
        res.status(500).json({ error: "Server error" });
    }
};

export const getBranches = async (req, res) => {
    try {
        const { university, degree } = req.query;
        if (!university) return res.status(400).json({ error: "University is required" });

        const fileName = `${university}_subjects.json`;
        let subjects = await readJsonFile(university, fileName);
        
        if (degree) {
            subjects = subjects.filter(item => item.degree === degree);
        }
        
        const branches = [...new Set(subjects.map(item => item.branch).filter(Boolean))];
        res.status(200).json(branches);
    } catch (error) {
        res.status(500).json({ error: "Server error" });
    }
};

export const getSemesters = async (req, res) => {
    try {
        const { university, degree, branch } = req.query;
        if (!university) return res.status(400).json({ error: "University is required" });

        const fileName = `${university}_subjects.json`;
        let subjects = await readJsonFile(university, fileName);
        
        if (degree) subjects = subjects.filter(item => item.degree === degree);
        if (branch) subjects = subjects.filter(item => item.branch === branch);
        
        const semesters = [...new Set(subjects.map(item => item.semester).filter(Boolean))];
        res.status(200).json(semesters);
    } catch (error) {
        res.status(500).json({ error: "Server error" });
    }
};

export const getYearsAndMonths = async (req, res) => {
    try {
        const { university } = req.query;
        if (!university) return res.status(400).json({ error: "University is required" });

        const fileName = `${university}_subjects.json`;
        const subjects = await readJsonFile(university, fileName);
        
        const years = [...new Set(subjects.map(item => item.year).filter(Boolean))];
        const months = [...new Set(subjects.map(item => item.exam_month).filter(Boolean))];
        
        res.status(200).json({ years, months });
    } catch (error) {
        res.status(500).json({ error: "Server error" });
    }
};

export const getPaperCount = async (req, res) => {
    try {
        const { university } = req.query;
        if (!university) return res.status(400).json({ error: "University is required" });

        const fileName = `${university}_subjects.json`;
        const subjects = await readJsonFile(university, fileName);
        
        const totalCount = subjects.reduce((sum, item) => sum + (item.paper_count || 0), 0);
        res.status(200).json({ count: totalCount });
    } catch (error) {
        res.status(500).json({ error: "Server error" });
    }
};