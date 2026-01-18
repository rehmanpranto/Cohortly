import express, { Application } from 'express';
import cors from 'cors';
import config from './config/config';
import logger from './config/logger';
import routes from './routes';
import { errorHandler, notFoundHandler } from './middleware/error.middleware';
import { requestLogger } from './middleware/logger.middleware';
import './config/database'; // Initialize database connection

const app: Application = express();

// Middleware
app.use(cors({
  origin: config.cors.origin,
  credentials: true,
}));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(requestLogger);

// Routes
app.use('/api/v1', routes);

// Root endpoint
app.get('/', (_req, res) => {
  res.json({
    success: true,
    message: 'Bootcamp Management System API',
    version: '1.0.0',
    docs: '/api/v1/health',
  });
});

// Error handlers
app.use(notFoundHandler);
app.use(errorHandler);

// Start server
const PORT = config.port;

app.listen(PORT, () => {
  logger.info(`🚀 Server running on port ${PORT}`);
  logger.info(`📚 Environment: ${config.nodeEnv}`);
  logger.info(`🌐 CORS enabled for: ${config.cors.origin}`);
  logger.info(`✅ API v1 available at: http://localhost:${PORT}/api/v1`);
});

// Handle unhandled promise rejections
process.on('unhandledRejection', (err: Error) => {
  logger.error('Unhandled Promise Rejection:', err);
  process.exit(1);
});

// Handle uncaught exceptions
process.on('uncaughtException', (err: Error) => {
  logger.error('Uncaught Exception:', err);
  process.exit(1);
});

export default app;
