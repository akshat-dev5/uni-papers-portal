import fs from "fs";
import path from "path";
import axios from "axios";
import { spawn } from "child_process";

export const runWatermarkPipeline = async (pdfUrl) => {

    const PYTHON_EXE =
        process.env.PYTHON_PATH || "python";

    const pythonDir = path.resolve("./python");

    const inputDir = path.join(pythonDir, "input_pdfs");
    const outputDir = path.join(pythonDir, "final_outputs");
    const decomposedDir = path.join(pythonDir, "decomposed_docs");

    // Create required folders
    fs.mkdirSync(inputDir, { recursive: true });
    fs.mkdirSync(outputDir, { recursive: true });
    fs.mkdirSync(decomposedDir, { recursive: true });

    // Clean input folder
    fs.readdirSync(inputDir).forEach(file => {
        fs.unlinkSync(path.join(inputDir, file));
    });

    // Clean output folder
    fs.readdirSync(outputDir).forEach(file => {
        fs.unlinkSync(path.join(outputDir, file));
    });

    // Clean decomposed docs
    if (fs.existsSync(decomposedDir)) {
        fs.rmSync(decomposedDir, {
            recursive: true,
            force: true
        });
    }

    fs.mkdirSync(decomposedDir, {
        recursive: true
    });

    // Download PDF
    const pdfPath = path.join(inputDir, "input.pdf");

    const response = await axios({
        method: "GET",
        url: pdfUrl,
        responseType: "stream"
    });

    const writer = fs.createWriteStream(pdfPath);

    response.data.pipe(writer);

    await new Promise((resolve, reject) => {
        writer.on("finish", resolve);
        writer.on("error", reject);
    });

    // Execute Python pipeline
    await new Promise((resolve, reject) => {

        const pythonProcess = spawn(
            PYTHON_EXE,
            ["run_pipeline.py"],
            {
                cwd: pythonDir
            }
        );

        pythonProcess.stdout.on("data", data => {
            console.log(data.toString());
        });

        pythonProcess.stderr.on("data", data => {
            console.error(data.toString());
        });

        pythonProcess.on("error", error => {
            reject(error);
        });

        pythonProcess.on("close", code => {

            if (code === 0) {
                resolve();
            } else {
                reject(
                    new Error(`Pipeline failed with code ${code}`)
                );
            }

        });

    });

    // Find generated PDF
    const files = fs.readdirSync(outputDir);

    const cleanPdf = files.find(
        file => file.endsWith("_clean.pdf")
    );
    
    /*for cleanup*/
    if (fs.existsSync(inputDir)) {
        fs.rmSync(inputDir, {
           recursive: true,
           force: true
        });
    }

    if (fs.existsSync(decomposedDir)) {
        fs.rmSync(decomposedDir, {
           recursive: true,
           force: true
        });
    }

    if (!cleanPdf) {
        throw new Error("Clean PDF not generated");
    }

    // Return only filename
    return cleanPdf;
};