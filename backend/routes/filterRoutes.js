import express from 'express';
import { 
    getDegrees, 
    getBranches, 
    getSemesters, 
    getYearsAndMonths, 
    getPaperCount 
} from '../controllers/filterController.js';

const router = express.Router();

router.get('/degrees', getDegrees);
router.get('/branches', getBranches);
router.get('/semesters', getSemesters);
router.get('/years-months', getYearsAndMonths);
router.get('/count', getPaperCount);

export default router;