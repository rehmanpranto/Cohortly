import prisma from '../config/database';
import { BootcampMode, BatchStatus, Prisma } from '@prisma/client';

export interface CreateBootcampDto {
  title: string;
  description: string;
  mode: BootcampMode;
  price: number;
  duration?: number;
  createdBy: string;
}

export interface CreateBatchDto {
  bootcampId: string;
  batchName: string;
  startDate: Date;
  endDate: Date;
  capacity: number;
}

class BootcampService {
  async createBootcamp(data: CreateBootcampDto) {
    return prisma.bootcamp.create({
      data: {
        title: data.title,
        description: data.description,
        mode: data.mode,
        price: data.price,
        duration: data.duration,
        createdBy: data.createdBy,
        isActive: true,
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

  async getBootcamps(page: number = 1, limit: number = 20, isActive?: boolean) {
    const where: Prisma.BootcampWhereInput = {};
    if (isActive !== undefined) {
      where.isActive = isActive;
    }

    const [bootcamps, total] = await Promise.all([
      prisma.bootcamp.findMany({
        where,
        skip: (page - 1) * limit,
        take: limit,
        orderBy: { createdAt: 'desc' },
        include: {
          createdByUser: {
            select: {
              id: true,
              fullName: true,
              email: true,
            },
          },
          _count: {
            select: {
              batches: true,
              modules: true,
            },
          },
        },
      }),
      prisma.bootcamp.count({ where }),
    ]);

    return { bootcamps, total };
  }

  async getBootcampById(id: string) {
    const bootcamp = await prisma.bootcamp.findUnique({
      where: { id },
      include: {
        createdByUser: {
          select: {
            id: true,
            fullName: true,
            email: true,
          },
        },
        batches: {
          include: {
            _count: {
              select: {
                enrollments: true,
              },
            },
          },
        },
        modules: {
          orderBy: { orderIndex: 'asc' },
          include: {
            lessons: {
              orderBy: { orderIndex: 'asc' },
            },
          },
        },
      },
    });

    if (!bootcamp) {
      throw new Error('Bootcamp not found');
    }

    return bootcamp;
  }

  async updateBootcamp(id: string, data: Partial<CreateBootcampDto>) {
    return prisma.bootcamp.update({
      where: { id },
      data,
    });
  }

  async deleteBootcamp(id: string) {
    return prisma.bootcamp.update({
      where: { id },
      data: { isActive: false },
    });
  }

  // Batch Management
  async createBatch(data: CreateBatchDto) {
    return prisma.batch.create({
      data: {
        bootcampId: data.bootcampId,
        batchName: data.batchName,
        startDate: data.startDate,
        endDate: data.endDate,
        capacity: data.capacity,
        status: BatchStatus.UPCOMING,
      },
      include: {
        bootcamp: true,
      },
    });
  }

  async getBatches(bootcampId?: string, status?: BatchStatus) {
    const where: Prisma.BatchWhereInput = {};
    if (bootcampId) where.bootcampId = bootcampId;
    if (status) where.status = status;

    return prisma.batch.findMany({
      where,
      orderBy: { startDate: 'desc' },
      include: {
        bootcamp: true,
        _count: {
          select: {
            enrollments: true,
            instructors: true,
            mentors: true,
          },
        },
      },
    });
  }

  async getBatchById(id: string) {
    const batch = await prisma.batch.findUnique({
      where: { id },
      include: {
        bootcamp: true,
        instructors: {
          include: {
            instructor: {
              select: {
                id: true,
                fullName: true,
                email: true,
              },
            },
          },
        },
        mentors: {
          include: {
            mentor: {
              select: {
                id: true,
                fullName: true,
                email: true,
              },
            },
          },
        },
        enrollments: {
          include: {
            student: {
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

    if (!batch) {
      throw new Error('Batch not found');
    }

    return batch;
  }

  async assignInstructorToBatch(batchId: string, instructorId: string) {
    return prisma.instructorBatch.create({
      data: {
        batchId,
        instructorId,
      },
    });
  }

  async assignMentorToBatch(batchId: string, mentorId: string) {
    return prisma.mentorBatch.create({
      data: {
        batchId,
        mentorId,
      },
    });
  }
}

export default new BootcampService();
