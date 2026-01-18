import prisma from '../config/database';
import { ContentType, ResourceType } from '@prisma/client';

export interface CreateModuleDto {
  bootcampId: string;
  title: string;
  description?: string;
  orderIndex: number;
}

export interface CreateLessonDto {
  moduleId: string;
  title: string;
  description?: string;
  contentType: ContentType;
  contentUrl?: string;
  duration?: number;
  orderIndex: number;
}

export interface CreateResourceDto {
  lessonId: string;
  title: string;
  type: ResourceType;
  url: string;
}

class LMSService {
  // Module Management
  async createModule(data: CreateModuleDto) {
    return prisma.module.create({
      data: {
        bootcampId: data.bootcampId,
        title: data.title,
        description: data.description,
        orderIndex: data.orderIndex,
      },
      include: {
        bootcamp: true,
      },
    });
  }

  async getModules(bootcampId: string) {
    return prisma.module.findMany({
      where: { bootcampId },
      include: {
        lessons: {
          orderBy: { orderIndex: 'asc' },
          include: {
            _count: {
              select: {
                resources: true,
                assignments: true,
              },
            },
          },
        },
      },
      orderBy: { orderIndex: 'asc' },
    });
  }

  async getModuleById(id: string) {
    const module = await prisma.module.findUnique({
      where: { id },
      include: {
        bootcamp: true,
        lessons: {
          orderBy: { orderIndex: 'asc' },
          include: {
            resources: true,
            assignments: true,
          },
        },
      },
    });

    if (!module) {
      throw new Error('Module not found');
    }

    return module;
  }

  async updateModule(id: string, data: Partial<CreateModuleDto>) {
    return prisma.module.update({
      where: { id },
      data,
    });
  }

  async deleteModule(id: string) {
    return prisma.module.delete({
      where: { id },
    });
  }

  // Lesson Management
  async createLesson(data: CreateLessonDto) {
    return prisma.lesson.create({
      data: {
        moduleId: data.moduleId,
        title: data.title,
        description: data.description,
        contentType: data.contentType,
        contentUrl: data.contentUrl,
        duration: data.duration,
        orderIndex: data.orderIndex,
      },
      include: {
        module: {
          include: {
            bootcamp: true,
          },
        },
      },
    });
  }

  async getLessons(moduleId: string) {
    return prisma.lesson.findMany({
      where: { moduleId },
      include: {
        module: true,
        resources: true,
        assignments: true,
      },
      orderBy: { orderIndex: 'asc' },
    });
  }

  async getLessonById(id: string) {
    const lesson = await prisma.lesson.findUnique({
      where: { id },
      include: {
        module: {
          include: {
            bootcamp: true,
          },
        },
        resources: true,
        assignments: {
          include: {
            _count: {
              select: {
                submissions: true,
              },
            },
          },
        },
      },
    });

    if (!lesson) {
      throw new Error('Lesson not found');
    }

    return lesson;
  }

  async updateLesson(id: string, data: Partial<CreateLessonDto>) {
    return prisma.lesson.update({
      where: { id },
      data,
    });
  }

  async deleteLesson(id: string) {
    return prisma.lesson.delete({
      where: { id },
    });
  }

  // Resource Management
  async createResource(data: CreateResourceDto) {
    return prisma.resource.create({
      data: {
        lessonId: data.lessonId,
        title: data.title,
        type: data.type,
        url: data.url,
      },
      include: {
        lesson: true,
      },
    });
  }

  async getResources(lessonId: string) {
    return prisma.resource.findMany({
      where: { lessonId },
      include: {
        lesson: true,
      },
      orderBy: { createdAt: 'asc' },
    });
  }

  async deleteResource(id: string) {
    return prisma.resource.delete({
      where: { id },
    });
  }

  // Attendance Management
  async markAttendance(enrollmentId: string, batchId: string, sessionDate: Date, present: boolean) {
    return prisma.attendance.upsert({
      where: {
        enrollmentId_sessionDate: {
          enrollmentId,
          sessionDate,
        },
      },
      update: {
        present,
        markedAt: new Date(),
      },
      create: {
        enrollmentId,
        batchId,
        sessionDate,
        present,
      },
      include: {
        enrollment: {
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
  }

  async getAttendance(enrollmentId: string) {
    return prisma.attendance.findMany({
      where: { enrollmentId },
      orderBy: { sessionDate: 'desc' },
      include: {
        enrollment: {
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
  }

  async getBatchAttendance(batchId: string, sessionDate: Date) {
    return prisma.attendance.findMany({
      where: {
        batchId,
        sessionDate,
      },
      include: {
        enrollment: {
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
  }
}

export default new LMSService();
