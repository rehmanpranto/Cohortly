import { PrismaClient, UserRole, LeadStatus, LeadSource, BootcampMode, BatchStatus, EnrollmentStatus } from '@prisma/client';
import * as bcrypt from 'bcrypt';

const prisma = new PrismaClient();

async function main() {
  console.log('🌱 Starting database seed...');

  // Clear existing data (optional - comment out in production)
  console.log('🧹 Cleaning database...');
  await prisma.grade.deleteMany();
  await prisma.submission.deleteMany();
  await prisma.assignment.deleteMany();
  await prisma.resource.deleteMany();
  await prisma.lesson.deleteMany();
  await prisma.module.deleteMany();
  await prisma.attendance.deleteMany();
  await prisma.certificate.deleteMany();
  await prisma.payment.deleteMany();
  await prisma.enrollment.deleteMany();
  await prisma.instructorBatch.deleteMany();
  await prisma.mentorBatch.deleteMany();
  await prisma.announcement.deleteMany();
  await prisma.notification.deleteMany();
  await prisma.batch.deleteMany();
  await prisma.bootcamp.deleteMany();
  await prisma.leadLog.deleteMany();
  await prisma.lead.deleteMany();
  await prisma.refreshToken.deleteMany();
  await prisma.user.deleteMany();

  // Create Users
  console.log('👥 Creating users...');
  const hashedPassword = await bcrypt.hash('Password123!', 10);

  const admin = await prisma.user.create({
    data: {
      email: 'admin@bootcamp.com',
      passwordHash: hashedPassword,
      fullName: 'System Admin',
      role: UserRole.ADMIN,
      phone: '+1234567890',
      isActive: true,
    },
  });

  const sales1 = await prisma.user.create({
    data: {
      email: 'sales1@bootcamp.com',
      passwordHash: hashedPassword,
      fullName: 'Sarah Sales',
      role: UserRole.SALES,
      phone: '+1234567891',
      isActive: true,
    },
  });

  const instructor1 = await prisma.user.create({
    data: {
      email: 'instructor1@bootcamp.com',
      passwordHash: hashedPassword,
      fullName: 'John Instructor',
      role: UserRole.INSTRUCTOR,
      phone: '+1234567892',
      isActive: true,
    },
  });

  const mentor1 = await prisma.user.create({
    data: {
      email: 'mentor1@bootcamp.com',
      passwordHash: hashedPassword,
      fullName: 'Mike Mentor',
      role: UserRole.MENTOR,
      phone: '+1234567893',
      isActive: true,
    },
  });

  const student1 = await prisma.user.create({
    data: {
      email: 'student1@bootcamp.com',
      passwordHash: hashedPassword,
      fullName: 'Alice Student',
      role: UserRole.STUDENT,
      phone: '+1234567894',
      isActive: true,
    },
  });

  const student2 = await prisma.user.create({
    data: {
      email: 'student2@bootcamp.com',
      passwordHash: hashedPassword,
      fullName: 'Bob Student',
      role: UserRole.STUDENT,
      phone: '+1234567895',
      isActive: true,
    },
  });

  console.log('✅ Created 6 users');

  // Create Leads
  console.log('📋 Creating leads...');
  const lead1 = await prisma.lead.create({
    data: {
      fullName: 'Charlie Prospect',
      email: 'charlie@example.com',
      phone: '+1234567896',
      source: LeadSource.WEBSITE,
      status: LeadStatus.NEW,
      createdBy: sales1.id,
      assignedTo: sales1.id,
    },
  });

  await prisma.leadLog.create({
    data: {
      leadId: lead1.id,
      note: 'Initial contact made via phone',
      nextFollowUp: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000),
      createdBy: sales1.id,
    },
  });

  console.log('✅ Created leads and logs');

  // Create Bootcamps
  console.log('🎓 Creating bootcamps...');
  const bootcamp1 = await prisma.bootcamp.create({
    data: {
      title: 'Full Stack Web Development',
      description: 'Complete full stack development bootcamp covering MERN stack, databases, and deployment.',
      mode: BootcampMode.HYBRID,
      price: 1999.00,
      duration: 16,
      isActive: true,
      createdBy: admin.id,
    },
  });

  await prisma.bootcamp.create({
    data: {
      title: 'Data Science & Machine Learning',
      description: 'Comprehensive data science bootcamp with Python, ML algorithms, and real projects.',
      mode: BootcampMode.LIVE,
      price: 2499.00,
      duration: 20,
      isActive: true,
      createdBy: admin.id,
    },
  });

  console.log('✅ Created 2 bootcamps');

  // Create Batches
  console.log('📅 Creating batches...');
  const batch1 = await prisma.batch.create({
    data: {
      bootcampId: bootcamp1.id,
      batchName: 'FS-2026-JAN',
      startDate: new Date('2026-02-01'),
      endDate: new Date('2026-05-31'),
      capacity: 30,
      status: BatchStatus.UPCOMING,
    },
  });

  await prisma.instructorBatch.create({
    data: {
      batchId: batch1.id,
      instructorId: instructor1.id,
    },
  });

  await prisma.mentorBatch.create({
    data: {
      batchId: batch1.id,
      mentorId: mentor1.id,
    },
  });

  console.log('✅ Created batch with instructors and mentors');

  // Create Enrollments
  console.log('📝 Creating enrollments...');
  const enrollment1 = await prisma.enrollment.create({
    data: {
      studentId: student1.id,
      batchId: batch1.id,
      status: EnrollmentStatus.ACTIVE,
      enrolledAt: new Date(),
    },
  });

  const enrollment2 = await prisma.enrollment.create({
    data: {
      studentId: student2.id,
      batchId: batch1.id,
      status: EnrollmentStatus.ACTIVE,
      enrolledAt: new Date(),
    },
  });

  console.log('✅ Created 2 enrollments');

  // Create Payments
  console.log('💰 Creating payments...');
  await prisma.payment.create({
    data: {
      enrollmentId: enrollment1.id,
      amount: 1999.00,
      method: 'CREDIT_CARD',
      status: 'COMPLETED',
      transactionId: 'TXN123456',
      paidAt: new Date(),
    },
  });

  await prisma.payment.create({
    data: {
      enrollmentId: enrollment2.id,
      amount: 999.00,
      method: 'UPI',
      status: 'COMPLETED',
      transactionId: 'TXN123457',
      paidAt: new Date(),
    },
  });

  console.log('✅ Created payments');

  // Create Modules and Lessons
  console.log('📚 Creating curriculum...');
  const module1 = await prisma.module.create({
    data: {
      bootcampId: bootcamp1.id,
      title: 'Introduction to Web Development',
      description: 'Basics of HTML, CSS, and JavaScript',
      orderIndex: 1,
    },
  });

  const lesson1 = await prisma.lesson.create({
    data: {
      moduleId: module1.id,
      title: 'HTML Fundamentals',
      description: 'Learn the basics of HTML5',
      contentType: 'VIDEO',
      contentUrl: 'https://example.com/videos/html-basics.mp4',
      duration: 45,
      orderIndex: 1,
    },
  });

  await prisma.resource.create({
    data: {
      lessonId: lesson1.id,
      title: 'HTML Cheat Sheet',
      type: 'PDF',
      url: 'https://example.com/resources/html-cheatsheet.pdf',
    },
  });

  console.log('✅ Created curriculum');

  // Create Assignment
  console.log('📝 Creating assignment...');
  const assignment1 = await prisma.assignment.create({
    data: {
      lessonId: lesson1.id,
      title: 'Build Your First Webpage',
      description: 'Create a personal portfolio page using HTML and CSS',
      maxScore: 100,
      deadline: new Date('2026-02-15'),
    },
  });

  await prisma.submission.create({
    data: {
      assignmentId: assignment1.id,
      studentId: student1.id,
      submissionUrl: 'https://github.com/student1/portfolio',
      status: 'SUBMITTED',
      submittedAt: new Date(),
    },
  });

  console.log('✅ Created assignments');

  // Create Announcement
  console.log('📢 Creating announcement...');
  await prisma.announcement.create({
    data: {
      batchId: batch1.id,
      title: 'Welcome to the Bootcamp!',
      message: 'Welcome everyone! Classes start on February 1st. Please check your email for the orientation schedule.',
      createdBy: instructor1.id,
    },
  });

  console.log('✅ Created announcement');

  // Create Notifications
  console.log('🔔 Creating notifications...');
  await prisma.notification.create({
    data: {
      userId: student1.id,
      title: 'Enrollment Confirmed',
      message: 'Your enrollment in Full Stack Web Development has been confirmed!',
      isRead: false,
    },
  });

  console.log('✅ Created notifications');

  console.log('');
  console.log('🎉 Seed completed successfully!');
  console.log('');
  console.log('📧 Test Accounts:');
  console.log('   Admin:      admin@bootcamp.com / Password123!');
  console.log('   Sales:      sales1@bootcamp.com / Password123!');
  console.log('   Instructor: instructor1@bootcamp.com / Password123!');
  console.log('   Mentor:     mentor1@bootcamp.com / Password123!');
  console.log('   Student 1:  student1@bootcamp.com / Password123!');
  console.log('   Student 2:  student2@bootcamp.com / Password123!');
  console.log('');
}

main()
  .catch((e) => {
    console.error('❌ Seed failed:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
