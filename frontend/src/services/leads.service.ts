import api from '@/lib/api';

export interface Lead {
  id: string;
  fullName: string;
  email: string;
  phone: string;
  status: 'NEW' | 'CONTACTED' | 'FOLLOWUP' | 'INTERESTED' | 'ENROLLED' | 'LOST';
  source: string;
  notes?: string;
  createdAt: string;
  updatedAt: string;
}

export interface CreateLeadDto {
  fullName: string;
  email: string;
  phone: string;
  source: string;
  notes?: string;
}

export interface UpdateLeadDto extends Partial<CreateLeadDto> {
  status?: 'NEW' | 'CONTACTED' | 'FOLLOWUP' | 'INTERESTED' | 'ENROLLED' | 'LOST';
}

export const leadsService = {
  getAllLeads: async (): Promise<Lead[]> => {
    const response = await api.get('/leads');
    return response.data.data;
  },

  getLeadById: async (id: string): Promise<Lead> => {
    const response = await api.get(`/leads/${id}`);
    return response.data.data;
  },

  createLead: async (data: CreateLeadDto): Promise<Lead> => {
    const response = await api.post('/leads', data);
    return response.data.data;
  },

  updateLead: async (id: string, data: UpdateLeadDto): Promise<Lead> => {
    const response = await api.put(`/leads/${id}`, data);
    return response.data.data;
  },

  deleteLead: async (id: string): Promise<void> => {
    await api.delete(`/leads/${id}`);
  },

  convertLead: async (id: string): Promise<Lead> => {
    const response = await api.post(`/leads/${id}/convert`);
    return response.data.data;
  },
};
