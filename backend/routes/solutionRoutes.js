import express from 'express';
import { generateSolution, verifySolution, downloadSolution } from '../controllers/solutionController.js';

const router = express.Router();

router.post('/generate', generateSolution);
router.post('/verify', verifySolution);
router.get('/download/:id', downloadSolution);

export default router;
