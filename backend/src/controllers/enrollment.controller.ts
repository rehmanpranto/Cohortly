import { Request, Response } from 'express';
import { enrollmentService } from '../services/enrollment.service';
import { successResponse, errorResponse } from '../utils/response.utils';

export const createEnrollment = async (req: Request, res: Response): Promise<void> => {
  try {
    const enrollment = await enrollmentService.createEnrollment(req.body);
    successResponse(res, 'Enrollment created successfully', enrollment, 201);
  } catch (error: any) {
    errorResponse(res, error.message || 'Failed to create enrollment', 500);
  }
};

export const getAllEnrollments = async (req: Request, res: Response): Promise<void> => {
  try {
    const enrollments = await enrollmentService.getAllEnrollments();
    successResponse(res, 'Enrollments retrieved successfully', enrollments);
  } catch (error: any) {
    errorResponse(res, error.message || 'Failed to retrieve enrollments', 500);
  }
};

export const getEnrollmentById = async (req: Request, res: Response): Promise<void> => {
  try {
    const enrollment = await enrollmentService.getEnrollmentById(req.params.id);
    if (!enrollment) {
      errorResponse(res, 'Enrollment not found', 404);
      return;
    }
    successResponse(res, 'Enrollment retrieved successfully', enrollment);
  } catch (error: any) {
    errorResponse(res, error.message || 'Failed to retrieve enrollment', 500);
  }
};

export const updateEnrollment = async (req: Request, res: Response): Promise<void> => {
  try {
    const enrollment = await enrollmentService.updateEnrollment(req.params.id, req.body);
    successResponse(res, 'Enrollment updated successfully', enrollment);
  } catch (error: any) {
    errorResponse(res, error.message || 'Failed to update enrollment', 500);
  }
};

export const deleteEnrollment = async (req: Request, res: Response): Promise<void> => {
  try {
    await enrollmentService.deleteEnrollment(req.params.id);
    successResponse(res, 'Enrollment deleted successfully', null);
  } catch (error: any) {
    errorResponse(res, error.message || 'Failed to delete enrollment', 500);
  }
};

export const updateEnrollmentStatus = async (req: Request, res: Response): Promise<void> => {
  try {
    const { status } = req.body;
    const enrollment = await enrollmentService.updateEnrollmentStatus(req.params.id, status);
    successResponse(res, 'Enrollment status updated successfully', enrollment);
  } catch (error: any) {
    errorResponse(res, error.message || 'Failed to update enrollment status', 500);
  }
};

export const getEnrollmentsByStudent = async (req: Request, res: Response): Promise<void> => {
  try {
    const enrollments = await enrollmentService.getEnrollmentsByStudent(req.params.studentId);
    successResponse(res, 'Student enrollments retrieved successfully', enrollments);
  } catch (error: any) {
    errorResponse(res, error.message || 'Failed to retrieve student enrollments', 500);
  }
};

export const getEnrollmentsByBootcamp = async (req: Request, res: Response): Promise<void> => {
  try {
    const enrollments = await enrollmentService.getEnrollmentsByBootcamp(req.params.bootcampId);
    successResponse(res, 'Bootcamp enrollments retrieved successfully', enrollments);
  } catch (error: any) {
    errorResponse(res, error.message || 'Failed to retrieve bootcamp enrollments', 500);
  }
};
