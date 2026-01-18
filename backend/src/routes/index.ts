import { Router } from 'express';
import authRoutes from './auth.routes';
import leadRoutes from './lead.routes';
import bootcampRoutes from './bootcamp.routes';
import enrollmentRoutes from './enrollment.routes';
import assignmentRoutes from './assignment.routes';
import lmsRoutes from './lms.routes';
import studentDbRoutes from './studentDb.routes';

const router = Router();

// API v1 routes
router.use('/auth', authRoutes);
router.use('/leads', leadRoutes);
router.use('/bootcamps', bootcampRoutes);
router.use('/enrollments', enrollmentRoutes);
router.use('/assignments', assignmentRoutes);
router.use('/lms', lmsRoutes);
router.use('/student', studentDbRoutes);

// Health check
router.get('/health', (_req, res) => {
  res.json({
    success: true,
    message: 'API is healthy',
    timestamp: new Date().toISOString(),
  });
});

export default router;
