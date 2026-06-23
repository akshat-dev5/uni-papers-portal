import { runWatermarkPipeline } from '../services/watermarkService.js';

export const removeWatermark = async (req, res) => {
    try {

        const { pdfUrl } = req.body;

        if (!pdfUrl) {
            return res.status(400).json({
                error: 'pdfUrl is required'
            });
        }

        const result = await runWatermarkPipeline(pdfUrl);

        return res.status(200).json({
           status: "success",
           downloadUrl: `/downloads/${result}`
        });

    } catch (error) {

        console.error(error);

        return res.status(500).json({
            error: 'Watermark removal failed'
        });
    }
};