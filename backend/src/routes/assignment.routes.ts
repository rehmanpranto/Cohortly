import { Router } from 'express';
import { authenticate, authorize } from '../middleware/auth.middleware';

const router = Router();

router.use(authenticate);

// Assignment routes
router.post('/', authorize('ADMIN', 'INSTRUCTOR'));
router.get('/', authenticate);
router.get('/:id', authenticate);
router.put('/:id', authorize('ADMIN', 'INSTRUCTOR'));
router.delete('/:id', authorize('ADMIN', 'INSTRUCTOR'));

// Submission routes
router.post('/submissions', authorize('STUDENT'));
router.get('/submissions', authenticate);
router.get('/submissions/:id', authenticate);

// Grading routes
router.post('/submissions/:id/grade', authorize('ADMIN', 'INSTRUCTOR', 'MENTOR'));
router.get('/pending-grades', authorize('ADMIN', 'INSTRUCTOR', 'MENTOR'));

export default router;
