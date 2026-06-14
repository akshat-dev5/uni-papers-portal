import { readJsonFile } from '../utils/fileReader.js';

export const getPapers = async (req, res) => {
    try {
        const { university, degree, branch, semester, year, month, search } = req.query;

        if (!university) {
            return res.status(400).json({ error: "University is required" });
        }

        const fileName = `${university}_papers.json`;
        let papers = await readJsonFile(university, fileName);

        if (degree) papers = papers.filter(p => p.degree === degree);
        if (branch) papers = papers.filter(p => p.branch === branch);
        if (semester) papers = papers.filter(p => String(p.semester) === String(semester));
        if (year) papers = papers.filter(p => String(p.year) === String(year));
        if (month) papers = papers.filter(p => p.exam_month === month);

        if (search) {
            const searchLower = search.toLowerCase();
            papers = papers.filter(p => 
                (p.subject_name && p.subject_name.toLowerCase().includes(searchLower)) ||
                (p.subject_code && String(p.subject_code).toLowerCase().includes(searchLower)) ||
                (p.branch && p.branch.toLowerCase().includes(searchLower)) ||
                (p.degree && p.degree.toLowerCase().includes(searchLower))
            );
        }

        res.status(200).json(papers);
    } catch (error) {
        res.status(500).json({ error: "Server error" });
    }
};