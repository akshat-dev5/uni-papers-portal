import express from 'express';
import { getPapers } from '../controllers/paperController.js';

const router = express.Router();

router.get('/', getPapers);

export default router;