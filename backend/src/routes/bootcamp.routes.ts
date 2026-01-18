import { Router } from 'express';
import { authenticate, authorize } from '../middleware/auth.middleware';

const router = Router();

router.use(authenticate);

// Bootcamp routes
router.post('/', authorize('ADMIN'));
router.get('/', authenticate);
router.get('/:id', authenticate);
router.put('/:id', authorize('ADMIN'));
router.delete('/:id', authorize('ADMIN'));

// Batch routes
router.post('/:bootcampId/batches', authorize('ADMIN'));
router.get('/batches', authenticate);
router.get('/batches/:batchId', authenticate);
router.post('/batches/:batchId/instructors', authorize('ADMIN'));
router.post('/batches/:batchId/mentors', authorize('ADMIN'));

export default router;
