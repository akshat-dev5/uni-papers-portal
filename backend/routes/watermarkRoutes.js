import express from 'express';
import { removeWatermark } from '../controllers/watermarkController.js';

const router = express.Router();

router.post('/remove', removeWatermark);

export default router;