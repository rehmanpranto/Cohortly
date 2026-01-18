import { Response, NextFunction } from 'express';
import { body, query } from 'express-validator';
import leadService from '../services/lead.service';
import { successResponse, errorResponse, paginationResponse } from '../utils/response.utils';
import { AuthRequest } from '../middleware/auth.middleware';
import { LeadStatus, LeadSource } from '@prisma/client';

// Validation rules
export const createLeadValidation = [
  body('fullName').trim().notEmpty().withMessage('Full name is required'),
  body('email').isEmail().normalizeEmail().withMessage('Valid email is required'),
  body('phone').optional().isMobilePhone('any'),
  body('source').isIn(Object.values(LeadSource)).withMessage('Invalid source'),
  body('assignedTo').optional().isUUID(),
];

export const updateLeadValidation = [
  body('fullName').optional().trim().notEmpty(),
  body('email').optional().isEmail().normalizeEmail(),
  body('phone').optional().isMobilePhone('any'),
  body('source').optional().isIn(Object.values(LeadSource)),
  body('status').optional().isIn(Object.values(LeadStatus)),
  body('assignedTo').optional().isUUID(),
];

export const addLeadLogValidation = [
  body('note').trim().notEmpty().withMessage('Note is required'),
  body('nextFollowUp').optional().isISO8601(),
];

class LeadController {
  async createLead(req: AuthRequest, res: Response, next: NextFunction): Promise<void> {
    try {
      const lead = await leadService.createLead({
        ...req.body,
        createdBy: req.user!.id,
      });
      successResponse(res, 'Lead created successfully', lead, 201);
    } catch (error: any) {
      errorResponse(res, error.message, 400);
    }
  }

  async getLeads(req: AuthRequest, res: Response, next: NextFunction): Promise<void> {
    try {
      const page = parseInt(req.query.page as string) || 1;
      const limit = parseInt(req.query.limit as string) || 20;
      
      const filters = {
        status: req.query.status as LeadStatus,
        source: req.query.source as LeadSource,
        assignedTo: req.query.assignedTo as string,
        search: req.query.search as string,
      };

      const { leads, total } = await leadService.getLeads(filters, page, limit);
      paginationResponse(res, 'Leads retrieved successfully', leads, page, limit, total);
    } catch (error: any) {
      errorResponse(res, error.message, 400);
    }
  }

  async getLeadById(req: AuthRequest, res: Response, next: NextFunction): Promise<void> {
    try {
      const lead = await leadService.getLeadById(req.params.id);
      successResponse(res, 'Lead retrieved successfully', lead);
    } catch (error: any) {
      errorResponse(res, error.message, 404);
    }
  }

  async updateLead(req: AuthRequest, res: Response, next: NextFunction): Promise<void> {
    try {
      const lead = await leadService.updateLead(req.params.id, req.body);
      successResponse(res, 'Lead updated successfully', lead);
    } catch (error: any) {
      errorResponse(res, error.message, 400);
    }
  }

  async deleteLead(req: AuthRequest, res: Response, next: NextFunction): Promise<void> {
    try {
      await leadService.deleteLead(req.params.id);
      successResponse(res, 'Lead deleted successfully');
    } catch (error: any) {
      errorResponse(res, error.message, 400);
    }
  }

  async addLeadLog(req: AuthRequest, res: Response, next: NextFunction): Promise<void> {
    try {
      const log = await leadService.addLeadLog({
        leadId: req.params.id,
        note: req.body.note,
        nextFollowUp: req.body.nextFollowUp,
        createdBy: req.user!.id,
      });
      successResponse(res, 'Lead log added successfully', log, 201);
    } catch (error: any) {
      errorResponse(res, error.message, 400);
    }
  }

  async getUpcomingFollowUps(req: AuthRequest, res: Response, next: NextFunction): Promise<void> {
    try {
      const followUps = await leadService.getUpcomingFollowUps(req.user!.id);
      successResponse(res, 'Upcoming follow-ups retrieved successfully', followUps);
    } catch (error: any) {
      errorResponse(res, error.message, 400);
    }
  }
}

export default new LeadController();
