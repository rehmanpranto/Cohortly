import prisma from '../config/database';
import { LeadStatus, LeadSource, Prisma } from '@prisma/client';

export interface CreateLeadDto {
  fullName: string;
  email: string;
  phone?: string;
  source: LeadSource;
  assignedTo?: string;
  createdBy: string;
}

export interface UpdateLeadDto {
  fullName?: string;
  email?: string;
  phone?: string;
  source?: LeadSource;
  status?: LeadStatus;
  assignedTo?: string;
}

export interface AddLeadLogDto {
  leadId: string;
  note: string;
  nextFollowUp?: Date;
  createdBy: string;
}

export interface LeadFilters {
  status?: LeadStatus;
  source?: LeadSource;
  assignedTo?: string;
  search?: string;
}

class LeadService {
  async createLead(data: CreateLeadDto) {
    return prisma.lead.create({
      data: {
        fullName: data.fullName,
        email: data.email,
        phone: data.phone,
        source: data.source,
        status: LeadStatus.NEW,
        assignedTo: data.assignedTo,
        createdBy: data.createdBy,
      },
      include: {
        assignedToUser: {
          select: {
            id: true,
            fullName: true,
            email: true,
          },
        },
        createdByUser: {
          select: {
            id: true,
            fullName: true,
            email: true,
          },
        },
      },
    });
  }

  async getLeads(
    filters: LeadFilters,
    page: number = 1,
    limit: number = 20
  ) {
    const where: Prisma.LeadWhereInput = {};

    if (filters.status) {
      where.status = filters.status;
    }

    if (filters.source) {
      where.source = filters.source;
    }

    if (filters.assignedTo) {
      where.assignedTo = filters.assignedTo;
    }

    if (filters.search) {
      where.OR = [
        { fullName: { contains: filters.search, mode: 'insensitive' } },
        { email: { contains: filters.search, mode: 'insensitive' } },
        { phone: { contains: filters.search, mode: 'insensitive' } },
      ];
    }

    const [leads, total] = await Promise.all([
      prisma.lead.findMany({
        where,
        skip: (page - 1) * limit,
        take: limit,
        orderBy: { createdAt: 'desc' },
        include: {
          assignedToUser: {
            select: {
              id: true,
              fullName: true,
              email: true,
            },
          },
          createdByUser: {
            select: {
              id: true,
              fullName: true,
              email: true,
            },
          },
        },
      }),
      prisma.lead.count({ where }),
    ]);

    return { leads, total };
  }

  async getLeadById(id: string) {
    const lead = await prisma.lead.findUnique({
      where: { id },
      include: {
        assignedToUser: {
          select: {
            id: true,
            fullName: true,
            email: true,
          },
        },
        createdByUser: {
          select: {
            id: true,
            fullName: true,
            email: true,
          },
        },
        logs: {
          orderBy: { createdAt: 'desc' },
          include: {
            createdByUser: {
              select: {
                id: true,
                fullName: true,
                email: true,
              },
            },
          },
        },
      },
    });

    if (!lead) {
      throw new Error('Lead not found');
    }

    return lead;
  }

  async updateLead(id: string, data: UpdateLeadDto) {
    return prisma.lead.update({
      where: { id },
      data,
      include: {
        assignedToUser: {
          select: {
            id: true,
            fullName: true,
            email: true,
          },
        },
      },
    });
  }

  async deleteLead(id: string) {
    return prisma.lead.delete({
      where: { id },
    });
  }

  async addLeadLog(data: AddLeadLogDto) {
    return prisma.leadLog.create({
      data: {
        leadId: data.leadId,
        note: data.note,
        nextFollowUp: data.nextFollowUp,
        createdBy: data.createdBy,
      },
      include: {
        createdByUser: {
          select: {
            id: true,
            fullName: true,
            email: true,
          },
        },
      },
    });
  }

  async convertLeadToStudent(
    leadId: string,
    userId: string,
    password: string
  ) {
    // This is a simplified conversion
    // In real implementation, this would create enrollment as well
    const lead = await this.getLeadById(leadId);

    // Update lead status
    await prisma.lead.update({
      where: { id: leadId },
      data: { status: LeadStatus.ENROLLED },
    });

    return {
      message: 'Lead converted to student successfully',
      leadId,
      email: lead.email,
    };
  }

  async getUpcomingFollowUps(userId: string) {
    return prisma.leadLog.findMany({
      where: {
        createdBy: userId,
        nextFollowUp: {
          gte: new Date(),
          lte: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // Next 7 days
        },
      },
      include: {
        lead: true,
        createdByUser: {
          select: {
            id: true,
            fullName: true,
            email: true,
          },
        },
      },
      orderBy: { nextFollowUp: 'asc' },
    });
  }
}

export default new LeadService();
