import { Request, Response } from 'express';
import studentDbService from '../services/studentDb.service';
import { successResponse, errorResponse } from '../utils/response.utils';
import prisma from '../config/database';

// Extend Request type to include user from auth middleware
interface AuthRequest extends Request {
  user?: {
    id: string;
    email: string;
    role: string;
  };
}

/**
 * Get database connection credentials for student
 * Returns passwordless connection information
 */
export const getStudentDbCredentials = async (req: AuthRequest, res: Response): Promise<void> => {
  try {
    const userId = req.user?.id;
    const userEmail = req.user?.email;

    if (!userId || !userEmail) {
      errorResponse(res, 'User not authenticated', 401);
      return;
    }

    // Validate student has access
    const hasAccess = await studentDbService.validateStudentAccess(userId);
    if (!hasAccess) {
      errorResponse(res, 'Only active students can access database credentials', 403);
      return;
    }

    // Generate credentials
    const credentials = await studentDbService.generateStudentCredentials(userId, userEmail);

    // Log access for audit
    await studentDbService.logDatabaseAccess(userId, 'Retrieved credentials');

    successResponse(res, 'Database credentials retrieved successfully', {
      credentials: {
        host: credentials.host,
        database: credentials.database,
        username: credentials.username,
        port: credentials.port,
        sslmode: credentials.sslmode,
        connectionString: credentials.connectionString,
      },
      pgpassContent: studentDbService.generatePgpassContent(credentials),
      setupInstructions: studentDbService.generateSetupInstructions(userId, credentials),
    });
  } catch (error: any) {
    errorResponse(res, error.message || 'Failed to retrieve database credentials', 500);
  }
};

/**
 * Get setup instructions only (without sensitive credentials)
 */
export const getDbSetupInstructions = async (req: AuthRequest, res: Response): Promise<void> => {
  try {
    const userId = req.user?.id;
    const userEmail = req.user?.email;

    if (!userId || !userEmail) {
      errorResponse(res, 'User not authenticated', 401);
      return;
    }

    // Validate student has access
    const hasAccess = await studentDbService.validateStudentAccess(userId);
    if (!hasAccess) {
      errorResponse(res, 'Only active students can access database setup', 403);
      return;
    }

    // Generate credentials (will be masked in instructions)
    const credentials = await studentDbService.generateStudentCredentials(userId, userEmail);
    const instructions = studentDbService.generateSetupInstructions(userId, credentials);

    successResponse(res, 'Setup instructions retrieved successfully', {
      instructions,
      quickStart: {
        windows: `Run setup-db.ps1 script provided in your student portal`,
        linux: `Run setup-db.sh script provided in your student portal`,
        manual: `Create .pgpass file with credentials from /api/v1/student/db-credentials`,
      },
    });
  } catch (error: any) {
    errorResponse(res, error.message || 'Failed to retrieve setup instructions', 500);
  }
};

/**
 * Test database connection for student
 */
export const testDbConnection = async (req: AuthRequest, res: Response): Promise<void> => {
  try {
    const userId = req.user?.id;

    if (!userId) {
      errorResponse(res, 'User not authenticated', 401);
      return;
    }

    // Validate student has access
    const hasAccess = await studentDbService.validateStudentAccess(userId);
    if (!hasAccess) {
      errorResponse(res, 'Only active students can test database connection', 403);
      return;
    }

    // Test connection by querying user's own data
    const result = await prisma.user.findUnique({
      where: { id: userId },
      select: { id: true, email: true, fullName: true },
    });

    if (result) {
      await studentDbService.logDatabaseAccess(userId, 'Connection test successful');
      successResponse(res, 'Database connection successful', {
        connected: true,
        timestamp: new Date().toISOString(),
        user: result,
      });
    } else {
      errorResponse(res, 'Database connection test failed', 500);
    }
  } catch (error: any) {
    errorResponse(res, error.message || 'Database connection test failed', 500);
  }
};

export default {
  getStudentDbCredentials,
  getDbSetupInstructions,
  testDbConnection,
};
