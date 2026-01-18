import prisma from '../config/database';

export interface CreateEnrollmentDto {
  studentId: string;
  batchId: string;
  paymentStatus?: string;
}

export interface UpdateEnrollmentDto {
  status?: string;
  paymentStatus?: string;
  progress?: number;
}

export const enrollmentService = {
  async createEnrollment(data: CreateEnrollmentDto) {
    // Check if enrollment already exists
    const existing = await prisma.enrollment.findUnique({
      where: {
        studentId_batchId: {
          studentId: data.studentId,
          batchId: data.batchId,
        },
      },
    });

    if (existing) {
      throw new Error('Student is already enrolled in this batch');
    }

    // Create enrollment
    return await prisma.enrollment.create({
      data: {
        studentId: data.studentId,
        batchId: data.batchId,
        status: 'PENDING',
      },
      include: {
        student: {
          select: {
            id: true,
            fullName: true,
            email: true,
            phone: true,
          },
        },
        batch: {
          include: {
            bootcamp: {
              select: {
                id: true,
                name: true,
                description: true,
                startDate: true,
                endDate: true,
                price: true,
              },
            },
          },
        },
      },
    });
  },

  async getAllEnrollments() {
    return await prisma.enrollment.findMany({
      include: {
        student: {
          select: {
            id: true,
            fullName: true,
            email: true,
            phone: true,
          },
        },
        batch: {
          include: {
            bootcamp: {
              select: {
                id: true,
                name: true,
                description: true,
                startDate: true,
                endDate: true,
                price: true,
              },
            },
          },
        },
      },
      orderBy: {
        createdAt: 'desc',
      },
    });
  },

  async getEnrollmentById(id: string) {
    return await prisma.enrollment.findUnique({
      where: { id },
      include: {
        student: {
          select: {
            id: true,
            fullName: true,
            email: true,
            phone: true,
          },
        },
        batch: {
          include: {
            bootcamp: {
              select: {
                id: true,
                name: true,
                description: true,
                startDate: true,
                endDate: true,
                price: true,
              },
            },
          },
        },
        payments: true,
      },
    });
  },

  async updateEnrollment(id: string, data: UpdateEnrollmentDto) {
    return await prisma.enrollment.update({
      where: { id },
      data: {
        status: data.status,
        ...(data.status === 'COMPLETED' && { completedAt: new Date() }),
      },
      include: {
        student: {
          select: {
            id: true,
            fullName: true,
            email: true,
            phone: true,
          },
        },
        batch: {
          include: {
            bootcamp: {
              select: {
                id: true,
                name: true,
                description: true,
              },
            },
          },
        },
      },
    });
  },

  async deleteEnrollment(id: string) {
    return await prisma.enrollment.delete({
      where: { id },
    });
  },

  async updateEnrollmentStatus(id: string, status: string) {
    return await prisma.enrollment.update({
      where: { id },
      data: {
        status,
        ...(status === 'COMPLETED' && { completedAt: new Date() }),
      },
      include: {
        student: {
          select: {
            id: true,
            fullName: true,
            email: true,
          },
        },
        batch: {
          include: {
            bootcamp: {
              select: {
                id: true,
                name: true,
              },
            },
          },
        },
      },
    });
  },

  async getEnrollmentsByStudent(studentId: string) {
    return await prisma.enrollment.findMany({
      where: { studentId },
      include: {
        batch: {
          include: {
            bootcamp: {
              select: {
                id: true,
                name: true,
                description: true,
                startDate: true,
                endDate: true,
                price: true,
              },
            },
          },
        },
        payments: true,
      },
      orderBy: {
        createdAt: 'desc',
      },
    });
  },

  async getEnrollmentsByBootcamp(bootcampId: string) {
    // Get all batches for this bootcamp first
    const batches = await prisma.batch.findMany({
      where: { bootcampId },
      select: { id: true },
    });

    const batchIds = batches.map((b: { id: string }) => b.id);

    return await prisma.enrollment.findMany({
      where: {
        batchId: {
          in: batchIds,
        },
      },
      include: {
        student: {
          select: {
            id: true,
            fullName: true,
            email: true,
            phone: true,
          },
        },
        batch: {
          include: {
            bootcamp: {
              select: {
                id: true,
                name: true,
                description: true,
              },
            },
          },
        },
        payments: true,
      },
      orderBy: {
        createdAt: 'desc',
      },
    });
  },
};

export default enrollmentService;
