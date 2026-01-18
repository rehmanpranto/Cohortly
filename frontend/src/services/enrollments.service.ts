import api from '@/lib/api';

export interface Enrollment {
  id: string;
  studentId: string;
  bootcampId: string;
  status: 'PENDING' | 'ACTIVE' | 'COMPLETED' | 'DROPPED' | 'SUSPENDED';
  paymentStatus: 'PENDING' | 'PARTIAL' | 'PAID' | 'REFUNDED';
  progress: number;
  enrollmentDate: string;
  completionDate?: string;
  student?: any;
  bootcamp?: any;
  createdAt: string;
  updatedAt: string;
}

export interface CreateEnrollmentDto {
  studentId: string;
  bootcampId: string;
}

export interface UpdateEnrollmentDto {
  status?: 'PENDING' | 'ACTIVE' | 'COMPLETED' | 'DROPPED' | 'SUSPENDED';
  paymentStatus?: 'PENDING' | 'PARTIAL' | 'PAID' | 'REFUNDED';
  progress?: number;
}

export const enrollmentsService = {
  getAllEnrollments: async (): Promise<Enrollment[]> => {
    const response = await api.get('/enrollments');
    return response.data.data;
  },

  getEnrollmentById: async (id: string): Promise<Enrollment> => {
    const response = await api.get(`/enrollments/${id}`);
    return response.data.data;
  },

  createEnrollment: async (data: CreateEnrollmentDto): Promise<Enrollment> => {
    const response = await api.post('/enrollments', data);
    return response.data.data;
  },

  updateEnrollment: async (id: string, data: UpdateEnrollmentDto): Promise<Enrollment> => {
    const response = await api.put(`/enrollments/${id}`, data);
    return response.data.data;
  },

  deleteEnrollment: async (id: string): Promise<void> => {
    await api.delete(`/enrollments/${id}`);
  },
};
