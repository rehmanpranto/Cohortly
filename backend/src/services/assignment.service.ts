import prisma from '../config/database';
import { SubmissionStatus } from '@prisma/client';
import { isDeadlinePassed } from '../utils/helpers.utils';

export interface CreateAssignmentDto {
  lessonId: string;
  title: string;
  description: string;
  maxScore: number;
  deadline?: Date;
}

export interface CreateSubmissionDto {
  assignmentId: string;
  studentId: string;
  submissionUrl?: string;
  content?: string;
}

export interface GradeSubmissionDto {
  submissionId: string;
  score: number;
  feedback?: string;
  gradedBy: string;
}

class AssignmentService {
  async createAssignment(data: CreateAssignmentDto) {
    return prisma.assignment.create({
      data: {
        lessonId: data.lessonId,
        title: data.title,
        description: data.description,
        maxScore: data.maxScore,
        deadline: data.deadline,
      },
      include: {
        lesson: {
          include: {
            module: {
              include: {
                bootcamp: true,
              },
            },
          },
        },
      },
    });
  }

  async getAssignments(lessonId?: string) {
    const where: any = {};
    if (lessonId) where.lessonId = lessonId;

    return prisma.assignment.findMany({
      where,
      include: {
        lesson: {
          include: {
            module: true,
          },
        },
        _count: {
          select: {
            submissions: true,
          },
        },
      },
      orderBy: { createdAt: 'desc' },
    });
  }

  async getAssignmentById(id: string) {
    const assignment = await prisma.assignment.findUnique({
      where: { id },
      include: {
        lesson: {
          include: {
            module: {
              include: {
                bootcamp: true,
              },
            },
          },
        },
        submissions: {
          include: {
            student: {
              select: {
                id: true,
                fullName: true,
                email: true,
              },
            },
            grade: true,
          },
        },
      },
    });

    if (!assignment) {
      throw new Error('Assignment not found');
    }

    return assignment;
  }

  async updateAssignment(id: string, data: Partial<CreateAssignmentDto>) {
    return prisma.assignment.update({
      where: { id },
      data,
    });
  }

  async deleteAssignment(id: string) {
    return prisma.assignment.delete({
      where: { id },
    });
  }

  // Submission Management
  async createSubmission(data: CreateSubmissionDto) {
    // Check if submission already exists
    const existing = await prisma.submission.findUnique({
      where: {
        assignmentId_studentId: {
          assignmentId: data.assignmentId,
          studentId: data.studentId,
        },
      },
    });

    if (existing) {
      throw new Error('Submission already exists for this assignment');
    }

    // Check deadline
    const assignment = await prisma.assignment.findUnique({
      where: { id: data.assignmentId },
    });

    if (!assignment) {
      throw new Error('Assignment not found');
    }

    const isLate =
      assignment.deadline && isDeadlinePassed(assignment.deadline);

    return prisma.submission.create({
      data: {
        assignmentId: data.assignmentId,
        studentId: data.studentId,
        submissionUrl: data.submissionUrl,
        content: data.content,
        status: isLate ? SubmissionStatus.LATE : SubmissionStatus.SUBMITTED,
        submittedAt: new Date(),
      },
      include: {
        assignment: true,
        student: {
          select: {
            id: true,
            fullName: true,
            email: true,
          },
        },
      },
    });
  }

  async getSubmissions(assignmentId?: string, studentId?: string) {
    const where: any = {};
    if (assignmentId) where.assignmentId = assignmentId;
    if (studentId) where.studentId = studentId;

    return prisma.submission.findMany({
      where,
      include: {
        assignment: {
          include: {
            lesson: {
              include: {
                module: true,
              },
            },
          },
        },
        student: {
          select: {
            id: true,
            fullName: true,
            email: true,
          },
        },
        grade: true,
      },
      orderBy: { submittedAt: 'desc' },
    });
  }

  async getSubmissionById(id: string) {
    const submission = await prisma.submission.findUnique({
      where: { id },
      include: {
        assignment: {
          include: {
            lesson: {
              include: {
                module: {
                  include: {
                    bootcamp: true,
                  },
                },
              },
            },
          },
        },
        student: {
          select: {
            id: true,
            fullName: true,
            email: true,
          },
        },
        grade: {
          include: {
            gradedByUser: {
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

    if (!submission) {
      throw new Error('Submission not found');
    }

    return submission;
  }

  async gradeSubmission(data: GradeSubmissionDto) {
    // Check if submission exists
    const submission = await prisma.submission.findUnique({
      where: { id: data.submissionId },
      include: { assignment: true },
    });

    if (!submission) {
      throw new Error('Submission not found');
    }

    if (data.score > submission.assignment.maxScore) {
      throw new Error('Score exceeds maximum score');
    }

    // Check if grade already exists
    const existingGrade = await prisma.grade.findUnique({
      where: { submissionId: data.submissionId },
    });

    if (existingGrade) {
      // Update existing grade
      return prisma.grade.update({
        where: { submissionId: data.submissionId },
        data: {
          score: data.score,
          feedback: data.feedback,
          gradedBy: data.gradedBy,
          gradedAt: new Date(),
        },
        include: {
          submission: {
            include: {
              student: {
                select: {
                  id: true,
                  fullName: true,
                  email: true,
                },
              },
              assignment: true,
            },
          },
          gradedByUser: {
            select: {
              id: true,
              fullName: true,
              email: true,
            },
          },
        },
      });
    }

    // Create new grade
    const grade = await prisma.grade.create({
      data: {
        submissionId: data.submissionId,
        score: data.score,
        feedback: data.feedback,
        gradedBy: data.gradedBy,
      },
      include: {
        submission: {
          include: {
            student: {
              select: {
                id: true,
                fullName: true,
                email: true,
              },
            },
            assignment: true,
          },
        },
        gradedByUser: {
          select: {
            id: true,
            fullName: true,
            email: true,
          },
        },
      },
    });

    // Update submission status
    await prisma.submission.update({
      where: { id: data.submissionId },
      data: { status: SubmissionStatus.GRADED },
    });

    return grade;
  }

  async getPendingGrades(instructorId?: string) {
    return prisma.submission.findMany({
      where: {
        status: {
          in: [SubmissionStatus.SUBMITTED, SubmissionStatus.LATE],
        },
      },
      include: {
        assignment: {
          include: {
            lesson: {
              include: {
                module: {
                  include: {
                    bootcamp: true,
                  },
                },
              },
            },
          },
        },
        student: {
          select: {
            id: true,
            fullName: true,
            email: true,
          },
        },
      },
      orderBy: { submittedAt: 'asc' },
    });
  }
}

export default new AssignmentService();
