import { Router } from 'express';
import leadController, {
  createLeadValidation,
  updateLeadValidation,
  addLeadLogValidation,
} from '../controllers/lead.controller';
import { authenticate, authorize } from '../middleware/auth.middleware';
import { validate } from '../middleware/validate.middleware';

const router = Router();

// All routes require authentication
router.use(authenticate);

// Lead Management
router.post('/', authorize('ADMIN', 'SALES'), validate(createLeadValidation), leadController.createLead);
router.get('/', authorize('ADMIN', 'SALES'), leadController.getLeads);
router.get('/follow-ups', authorize('ADMIN', 'SALES'), leadController.getUpcomingFollowUps);
router.get('/:id', authorize('ADMIN', 'SALES'), leadController.getLeadById);
router.put('/:id', authorize('ADMIN', 'SALES'), validate(updateLeadValidation), leadController.updateLead);
router.delete('/:id', authorize('ADMIN', 'SALES'), leadController.deleteLead);

// Lead Logs
router.post('/:id/logs', authorize('ADMIN', 'SALES'), validate(addLeadLogValidation), leadController.addLeadLog);

export default router;
