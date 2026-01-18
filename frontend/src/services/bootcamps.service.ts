import api from '@/lib/api';

export interface Bootcamp {
  id: string;
  name: string;
  description: string;
  startDate: string;
  endDate: string;
  price: number;
  capacity: number;
  status: 'DRAFT' | 'PUBLISHED' | 'ONGOING' | 'COMPLETED' | 'CANCELLED';
  syllabus?: any;
  createdAt: string;
  updatedAt: string;
}

export interface CreateBootcampDto {
  name: string;
  description: string;
  startDate: string;
  endDate: string;
  price: number;
  capacity: number;
  syllabus?: any;
}

export interface UpdateBootcampDto extends Partial<CreateBootcampDto> {
  status?: 'DRAFT' | 'PUBLISHED' | 'ONGOING' | 'COMPLETED' | 'CANCELLED';
}

export const bootcampsService = {
  getAllBootcamps: async (): Promise<Bootcamp[]> => {
    const response = await api.get('/bootcamps');
    return response.data.data;
  },

  getBootcampById: async (id: string): Promise<Bootcamp> => {
    const response = await api.get(`/bootcamps/${id}`);
    return response.data.data;
  },

  createBootcamp: async (data: CreateBootcampDto): Promise<Bootcamp> => {
    const response = await api.post('/bootcamps', data);
    return response.data.data;
  },

  updateBootcamp: async (id: string, data: UpdateBootcampDto): Promise<Bootcamp> => {
    const response = await api.put(`/bootcamps/${id}`, data);
    return response.data.data;
  },

  deleteBootcamp: async (id: string): Promise<void> => {
    await api.delete(`/bootcamps/${id}`);
  },
};
