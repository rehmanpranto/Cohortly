import { Request, Response, NextFunction } from 'express';
import { body } from 'express-validator';
import authService from '../services/auth.service';
import { successResponse, errorResponse } from '../utils/response.utils';
import { AuthRequest } from '../middleware/auth.middleware';
import { UserRole } from '@prisma/client';

// Validation rules
export const registerValidation = [
  body('email').isEmail().normalizeEmail().withMessage('Valid email is required'),
  body('password')
    .isLength({ min: 8 })
    .withMessage('Password must be at least 8 characters'),
  body('fullName').trim().notEmpty().withMessage('Full name is required'),
  body('role')
    .isIn(Object.values(UserRole))
    .withMessage('Invalid role'),
  body('phone').optional().isMobilePhone('any'),
];

export const loginValidation = [
  body('email').isEmail().normalizeEmail().withMessage('Valid email is required'),
  body('password').notEmpty().withMessage('Password is required'),
];

export const refreshTokenValidation = [
  body('refreshToken').notEmpty().withMessage('Refresh token is required'),
];

class AuthController {
  async register(req: Request, res: Response, _next: NextFunction): Promise<void> {
    try {
      const result = await authService.register(req.body);
      successResponse(res, 'Registration successful', result, 201);
    } catch (error: any) {
      errorResponse(res, error.message, 400);
    }
  }

  async login(req: Request, res: Response, _next: NextFunction): Promise<void> {
    try {
      const result = await authService.login(req.body);
      successResponse(res, 'Login successful', result);
    } catch (error: any) {
      errorResponse(res, error.message, 401);
    }
  }

  async refreshToken(req: Request, res: Response, _next: NextFunction): Promise<void> {
    try {
      const { refreshToken } = req.body;
      const result = await authService.refreshAccessToken(refreshToken);
      successResponse(res, 'Token refreshed successfully', result);
    } catch (error: any) {
      errorResponse(res, error.message, 401);
    }
  }

  async logout(req: AuthRequest, res: Response, _next: NextFunction): Promise<void> {
    try {
      const { refreshToken } = req.body;
      await authService.logout(req.user!.id, refreshToken);
      successResponse(res, 'Logout successful');
    } catch (error: any) {
      errorResponse(res, error.message, 400);
    }
  }

  async logoutAll(req: AuthRequest, res: Response, _next: NextFunction): Promise<void> {
    try {
      await authService.logoutAll(req.user!.id);
      successResponse(res, 'Logged out from all devices');
    } catch (error: any) {
      errorResponse(res, error.message, 400);
    }
  }

  async me(req: AuthRequest, res: Response, _next: NextFunction): Promise<void> {
    try {
      successResponse(res, 'User retrieved successfully', req.user);
    } catch (error: any) {
      errorResponse(res, error.message, 400);
    }
  }
}

export default new AuthController();
