import express from 'express';
import cors from 'cors';
import { createServer } from 'http';
import { Server } from 'socket.io';
import filterRoutes from './routes/filterRoutes.js';
import paperRoutes from './routes/paperRoutes.js';
import solutionRoutes from './routes/solutionRoutes.js';

const app = express();
const httpServer = createServer(app);
const PORT = process.env.PORT || 5000;

const io = new Server(httpServer, {
    cors: {
        origin: "http://localhost:5173",
        methods: ["GET", "POST"]
    }
});

app.use(cors());
app.use(express.json());

io.on('connection', (socket) => {
    socket.on('join-solution-room', (solutionId) => {
        socket.join(solutionId);
    });
});

app.set('io', io);

app.use('/api/filters', filterRoutes);
app.use('/api/papers', paperRoutes);
app.use('/api/solution', solutionRoutes);

app.get('/', (req, res) => {
    res.status(200).json({
        status: 'success',
        message: 'API is running perfectly!'
    });
});

app.get('/health', (req, res) => {
    res.status(200).json({
        status: 'healthy'
    });
});

httpServer.listen(PORT, () => {
    console.log(`🚀 Server is running on port ${PORT}`);
});