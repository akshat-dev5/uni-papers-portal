import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

// ES Modules mein __dirname set karne ka standard tareeka
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Yeh dynamically tumhare root folder ke 'data' directory ko point karega
const DATA_DIR = path.join(__dirname, '../../data');

/**
 * Dynamically reads a JSON file from the data folder.
 * @param {string} university - Name of the folder (e.g., 'abvv')
 * @param {string} fileName - Name of the file (e.g., 'subjects.json' or 'papers.json')
 * @returns {Promise<Object|Array>} Parsed JSON data
 */
export const readJsonFile = async (university, fileName) => {
    try {
        const filePath = path.join(DATA_DIR, university, fileName);
        const fileContent = await fs.readFile(filePath, 'utf-8');
        return JSON.parse(fileContent);
    } catch (error) {
        console.error(`Error reading ${fileName} for ${university}:`, error.message);
        throw new Error(`Failed to load data for ${university}`);
    }
};