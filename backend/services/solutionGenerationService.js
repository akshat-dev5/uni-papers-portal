import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export const getSolutionPath = (solutionId) => {
    return path.resolve(__dirname, '..', 'temp', 'generated-solutions', `${solutionId}.docx`);
};

export const startGenerationPipeline = (pdfUrl, solutionId, io) => {
    return new Promise((resolve, reject) => {
        const pythonScriptPath = path.resolve(__dirname, '..', 'ai_pipeline', 'main.py');
        const tempDirPath = path.resolve(__dirname, '..', 'temp');
        
        const pythonExecutable = process.env.PYTHON_PATH || 'python';
        
        const pythonProcess = spawn(pythonExecutable, [
            pythonScriptPath,
            '--url', pdfUrl,
            '--id', solutionId,
            '--temp_dir', tempDirPath
        ]);

        pythonProcess.stdout.on('data', (data) => {
            const output = data.toString().trim();
            if (output) {
                console.log(`[AI Pipeline ${solutionId}]: ${output}`);
                if (io) {
                    io.to(solutionId).emit('pipeline-log', { log: output });
                }
            }
        });

        pythonProcess.stderr.on('data', (data) => {
            const output = data.toString().trim();
            if (output && !output.includes("Warning")) {
                console.error(`[AI Pipeline Error ${solutionId}]: ${output}`);
                if (io) {
                    io.to(solutionId).emit('pipeline-log', { log: `ERROR: ${output}` });
                }
            }
        });

        pythonProcess.on('close', (code) => {
            if (code === 0) {
                console.log(`[Pipeline] Successfully finished generating ${solutionId}`);
                if (io) {
                    io.to(solutionId).emit('pipeline-complete', { status: 'success' });
                }
                resolve();
            } else {
                if (io) {
                    io.to(solutionId).emit('pipeline-error', { status: 'failed', code });
                }
                reject(new Error(`Python script exited with code ${code}`));
            }
        });
    });
};