import dotenv from "dotenv";
dotenv.config();

import express from "express";
import cors from "cors";
import path from "path";
import { createServer } from "http";
import { Server } from "socket.io";

import filterRoutes from "./routes/filterRoutes.js";
import paperRoutes from "./routes/paperRoutes.js";
import solutionRoutes from "./routes/solutionRoutes.js";
import watermarkRoutes from "./routes/watermarkRoutes.js";

const app = express();
const httpServer = createServer(app);

const PORT = process.env.PORT || 5000;

const io = new Server(httpServer, {
    cors: {
        origin: "http://localhost:5173",
        methods: ["GET", "POST"]
    }
});

io.on("connection", (socket) => {
    socket.on("join-solution-room", (solutionId) => {
        socket.join(solutionId);
    });
});

app.set("io", io);

app.use(cors());
app.use(express.json());

// Serve generated watermark-cleaned PDFs
app.use(
    "/downloads",
    express.static(path.resolve("./python/final_outputs"))
);

// API routes
app.use("/api/filters", filterRoutes);
app.use("/api/papers", paperRoutes);
app.use("/api/solution", solutionRoutes);
app.use("/api/watermark", watermarkRoutes);

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

httpServer.listen(PORT, () => {
    console.log(`🚀 Server is running on port ${PORT}`);
});