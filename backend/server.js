import dotenv from "dotenv";

dotenv.config();

import express from "express";
import cors from "cors";
import path from "path";

import filterRoutes from "./routes/filterRoutes.js";
import paperRoutes from "./routes/paperRoutes.js";
import watermarkRoutes from "./routes/watermarkRoutes.js";

const app = express();

const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

// Serve generated PDFs
app.use(
    "/downloads",
    express.static(path.resolve("./python/final_outputs"))
);

app.use("/api/filters", filterRoutes);
app.use("/api/watermark", watermarkRoutes);
app.use("/api/papers", paperRoutes);

app.get("/", (req, res) => {
    res.status(200).json({
        status: "success",
        message: "API is running perfectly!"
    });
});

app.get("/health", (req, res) => {
    res.status(200).json({
        status: "healthy"
    });
});

app.listen(PORT, () => {
    console.log(`🚀 Server is running on port ${PORT}`);
});