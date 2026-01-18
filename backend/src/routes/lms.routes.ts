import { Router } from 'express';
import { authenticate, authorize } from '../middleware/auth.middleware';

const router = Router();

router.use(authenticate);

// Module routes
router.post('/modules', authorize('ADMIN', 'INSTRUCTOR'));
router.get('/modules', authenticate);
router.get('/modules/:id', authenticate);
router.put('/modules/:id', authorize('ADMIN', 'INSTRUCTOR'));
router.delete('/modules/:id', authorize('ADMIN', 'INSTRUCTOR'));

// Lesson routes
router.post('/lessons', authorize('ADMIN', 'INSTRUCTOR'));
router.get('/lessons', authenticate);
router.get('/lessons/:id', authenticate);
router.put('/lessons/:id', authorize('ADMIN', 'INSTRUCTOR'));
router.delete('/lessons/:id', authorize('ADMIN', 'INSTRUCTOR'));

// Resource routes
router.post('/resources', authorize('ADMIN', 'INSTRUCTOR'));
router.get('/resources', authenticate);
router.delete('/resources/:id', authorize('ADMIN', 'INSTRUCTOR'));

// Attendance routes
router.post('/attendance', authorize('ADMIN', 'INSTRUCTOR', 'MENTOR'));
router.get('/attendance/:enrollmentId', authenticate);
router.get('/attendance/batch/:batchId', authorize('ADMIN', 'INSTRUCTOR', 'MENTOR'));

export default router;
