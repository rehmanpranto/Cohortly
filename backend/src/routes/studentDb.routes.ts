import { Router } from 'express';
import { authenticate, authorize } from '../middleware/auth.middleware';
import {
  getStudentDbCredentials,
  getDbSetupInstructions,
  testDbConnection,
} from '../controllers/studentDb.controller';

const router = Router();

// All routes require authentication as STUDENT
router.use(authenticate);
router.use(authorize('STUDENT'));

/**
 * GET /student/db-credentials
 * Get full database connection credentials (includes password)
 */
router.get('/db-credentials', getStudentDbCredentials);

/**
 * GET /student/db-setup
 * Get setup instructions for passwordless connection
 */
router.get('/db-setup', getDbSetupInstructions);

/**
 * GET /student/db-test
 * Test database connection
 */
router.get('/db-test', testDbConnection);

export default router;
