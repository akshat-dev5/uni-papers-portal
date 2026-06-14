import express from 'express';
import cors from 'cors';
import filterRoutes from './routes/filterRoutes.js';
import paperRoutes from './routes/paperRoutes.js';

const app = express();
const PORT = 5000;

app.use(cors());
app.use(express.json());

app.use('/api/filters', filterRoutes);
app.use('/api/papers', paperRoutes);

app.get('/', (req, res) => {
    res.json({ status: 'success', message: 'API is running perfectly!' });
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});