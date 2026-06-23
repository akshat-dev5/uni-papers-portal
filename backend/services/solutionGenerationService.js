import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export const getSolutionPath = (solutionId) => {
    return path.resolve(__dirname, '..', 'temp', 'generated-solutions', `${solutionId}.docx`);
};

export const startGenerationPipeline = (pdfUrl, solutionId) => {
    return new Promise((resolve, reject) => {
        const pythonScriptPath = path.resolve(__dirname, '..', 'ai_pipeline', 'main.py');
        const tempDirPath = path.resolve(__dirname, '..', 'temp');
        
        console.log(`[Pipeline] Starting 3-Agent generation for ${solutionId}`);
        // Use the Python executable from the virtual environment where dependencies are installed
        const pythonExecutable = 'D:\\MUQP_Internship\\ocr_env\\Scripts\\python.exe';
        
        const pythonProcess = spawn(pythonExecutable, [
            pythonScriptPath,
            '--url', pdfUrl,
            '--id', solutionId,
            '--temp_dir', tempDirPath
        ]);

        pythonProcess.stdout.on('data', (data) => {
            console.log(`[AI Pipeline ${solutionId}]: ${data.toString()}`);
        });

        pythonProcess.stderr.on('data', (data) => {
            console.error(`[AI Pipeline Error ${solutionId}]: ${data.toString()}`);
        });

        pythonProcess.on('close', (code) => {
            if (code === 0) {
                console.log(`[Pipeline] Successfully finished generating ${solutionId}`);
                resolve();
            } else {
                reject(new Error(`Python script exited with code ${code}`));
            }
        });
    });
};
