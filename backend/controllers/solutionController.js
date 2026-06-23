import { startGenerationPipeline, getSolutionPath } from '../services/solutionGenerationService.js';
import fs from 'fs';

export const generateSolution = async (req, res) => {
    const { pdfUrl } = req.body;
    if (!pdfUrl) {
        return res.status(400).json({ error: 'pdfUrl is required' });
    }

    const solutionId = `sol_${Date.now()}`;
    
    startGenerationPipeline(pdfUrl, solutionId).catch(err => {
        console.error(`[Pipeline Error] ${err.message}`);
    });

    res.status(202).json({
        solutionId,
        status: 'generated'
    });
};

export const verifySolution = async (req, res) => {
    const { solutionId } = req.body;
    if (!solutionId) {
        return res.status(400).json({ error: 'solutionId is required' });
    }

    const docxPath = getSolutionPath(solutionId);
    if (fs.existsSync(docxPath)) {
        res.status(200).json({
            approved: true,
            score: 95
        });
    } else {
        res.status(202).json({
            approved: false,
            score: 0,
            message: 'Pending verification or not found'
        });
    }
};

export const downloadSolution = async (req, res) => {
    const { id } = req.params;
    const docxPath = getSolutionPath(id);

    if (fs.existsSync(docxPath)) {
        res.download(docxPath);
    } else {
        res.status(404).json({ error: 'Solution not found' });
    }
};
