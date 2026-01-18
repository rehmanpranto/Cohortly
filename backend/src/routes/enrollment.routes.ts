import { Router } from 'express';
import { authenticate, authorize } from '../middleware/auth.middleware';
import {
  getAllEnrollments,
  createEnrollment,
  getEnrollmentById,
  updateEnrollment,
  deleteEnrollment,
  updateEnrollmentStatus,
  getEnrollmentsByStudent,
  getEnrollmentsByBootcamp,
} from '../controllers/enrollment.controller';

const router = Router();

router.use(authenticate);

// Enrollment routes
router.post('/', authorize('ADMIN', 'SALES'), createEnrollment);
router.get('/', authorize('ADMIN', 'SALES', 'INSTRUCTOR'), getAllEnrollments);
router.get('/student/:studentId', authorize('ADMIN', 'SALES', 'INSTRUCTOR'), getEnrollmentsByStudent);
router.get('/bootcamp/:bootcampId', authorize('ADMIN', 'SALES', 'INSTRUCTOR'), getEnrollmentsByBootcamp);
router.get('/:id', authenticate, getEnrollmentById);
router.put('/:id', authorize('ADMIN', 'SALES'), updateEnrollment);
router.put('/:id/status', authorize('ADMIN'), updateEnrollmentStatus);
router.delete('/:id', authorize('ADMIN'), deleteEnrollment);

export default router;
