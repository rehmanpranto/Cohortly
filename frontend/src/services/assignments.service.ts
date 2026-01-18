import api from '@/lib/api';

export interface Assignment {
  id: string;
  bootcampId: string;
  title: string;
  description: string;
  dueDate: string;
  maxPoints: number;
  status: 'DRAFT' | 'PUBLISHED' | 'CLOSED';
  attachments?: any;
  bootcamp?: any;
  createdAt: string;
  updatedAt: string;
}

export interface CreateAssignmentDto {
  bootcampId: string;
  title: string;
  description: string;
  dueDate: string;
  maxPoints: number;
  attachments?: any;
}

export interface UpdateAssignmentDto extends Partial<CreateAssignmentDto> {
  status?: 'DRAFT' | 'PUBLISHED' | 'CLOSED';
}

export const assignmentsService = {
  getAllAssignments: async (): Promise<Assignment[]> => {
    const response = await api.get('/assignments');
    return response.data.data;
  },

  getAssignmentById: async (id: string): Promise<Assignment> => {
    const response = await api.get(`/assignments/${id}`);
    return response.data.data;
  },

  createAssignment: async (data: CreateAssignmentDto): Promise<Assignment> => {
    const response = await api.post('/assignments', data);
    return response.data.data;
  },

  updateAssignment: async (id: string, data: UpdateAssignmentDto): Promise<Assignment> => {
    const response = await api.put(`/assignments/${id}`, data);
    return response.data.data;
  },

  deleteAssignment: async (id: string): Promise<void> => {
    await api.delete(`/assignments/${id}`);
  },
};
