# Bootcamp Management System - Backend

A production-grade, full-featured Bootcamp Management System built with Node.js, Express, TypeScript, and Neon PostgreSQL.

## 🎯 Features

### Core Modules
- **Authentication & Authorization** - JWT-based auth with role-based access control
- **Lead & CRM Management** - Complete lead tracking and conversion workflow
- **Bootcamp Management** - Create and manage bootcamps with batches
- **Enrollment System** - Student enrollment with payment tracking
- **Learning Management (LMS)** - Modules, lessons, resources, attendance
- **Assignment System** - Assignment creation, submission, and grading
- **Communication** - Announcements and notifications
- **Analytics** - Revenue tracking, enrollment metrics
- **Certificates** - Auto-generation with verification codes

### Security Features
- Bcrypt password hashing
- JWT access & refresh tokens
- Token rotation and invalidation
- Role-based access control (RBAC)
- Input validation with express-validator
- Secure environment variables

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm/yarn
- Neon PostgreSQL database (already configured)

### Installation

1. **Install dependencies:**
```powershell
cd backend
npm install
```

2. **Configure environment:**
```powershell
# Copy the .env file (already created with your DB credentials)
# Review .env and update JWT secrets for production
```

3. **Run Prisma migrations:**
```powershell
npm run prisma:generate
npm run prisma:migrate
```

4. **Seed the database:**
```powershell
npm run prisma:seed
```

5. **Start the development server:**
```powershell
npm run dev
```

The API will be available at: `http://localhost:5000`

## 📦 Database Schema

### User Roles
- `ADMIN` - Full system access
- `SALES` - Lead and enrollment management
- `INSTRUCTOR` - Curriculum and grading
- `MENTOR` - Student support and grading
- `STUDENT` - Learning access

### Core Tables
- `users` - User authentication and profiles
- `leads` - Lead capture and CRM
- `lead_logs` - Follow-up tracking
- `bootcamps` - Bootcamp programs
- `batches` - Bootcamp batches
- `enrollments` - Student enrollments
- `payments` - Payment tracking
- `modules` - Curriculum modules
- `lessons` - Lesson content
- `resources` - Learning resources
- `assignments` - Assignments
- `submissions` - Student submissions
- `grades` - Grading records
- `attendance` - Attendance tracking
- `announcements` - Batch announcements
- `notifications` - User notifications
- `certificates` - Completion certificates

## 🔌 API Endpoints

### Authentication (`/api/v1/auth`)
```
POST   /register        - Create new user account
POST   /login           - User login
POST   /refresh         - Refresh access token
POST   /logout          - Logout (invalidate refresh token)
POST   /logout-all      - Logout from all devices
GET    /me              - Get current user profile
```

### Leads (`/api/v1/leads`)
```
POST   /                - Create new lead
GET    /                - Get all leads (with filters)
GET    /follow-ups      - Get upcoming follow-ups
GET    /:id             - Get lead by ID
PUT    /:id             - Update lead
DELETE /:id             - Delete lead
POST   /:id/logs        - Add lead log/note
```

### Bootcamps (`/api/v1/bootcamps`)
```
POST   /                        - Create bootcamp
GET    /                        - Get all bootcamps
GET    /:id                     - Get bootcamp details
PUT    /:id                     - Update bootcamp
DELETE /:id                     - Soft delete bootcamp
POST   /:bootcampId/batches     - Create batch
GET    /batches                 - Get all batches
GET    /batches/:batchId        - Get batch details
POST   /batches/:batchId/instructors  - Assign instructor
POST   /batches/:batchId/mentors      - Assign mentor
```

### Enrollments (`/api/v1/enrollments`)
```
POST   /                  - Create enrollment
GET    /                  - Get enrollments (filtered)
GET    /:id               - Get enrollment details
PUT    /:id/status        - Update enrollment status
POST   /payments          - Record payment
GET    /payments          - Get all payments
GET    /payments/:id      - Get payment details
GET    /revenue/total     - Get total revenue
```

### Assignments (`/api/v1/assignments`)
```
POST   /                      - Create assignment
GET    /                      - Get assignments
GET    /:id                   - Get assignment details
PUT    /:id                   - Update assignment
DELETE /:id                   - Delete assignment
POST   /submissions           - Submit assignment
GET    /submissions           - Get submissions
GET    /submissions/:id       - Get submission details
POST   /submissions/:id/grade - Grade submission
GET    /pending-grades        - Get pending submissions
```

### LMS (`/api/v1/lms`)
```
# Modules
POST   /modules           - Create module
GET    /modules           - Get modules
GET    /modules/:id       - Get module details
PUT    /modules/:id       - Update module
DELETE /modules/:id       - Delete module

# Lessons
POST   /lessons           - Create lesson
GET    /lessons           - Get lessons
GET    /lessons/:id       - Get lesson details
PUT    /lessons/:id       - Update lesson
DELETE /lessons/:id       - Delete lesson

# Resources
POST   /resources         - Add resource
GET    /resources         - Get resources
DELETE /resources/:id     - Delete resource

# Attendance
POST   /attendance                   - Mark attendance
GET    /attendance/:enrollmentId     - Get student attendance
GET    /attendance/batch/:batchId    - Get batch attendance
```

## 🔐 Authentication

### Login
```bash
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "admin@bootcamp.com",
  "password": "Password123!"
}
```

Response:
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {
      "id": "uuid",
      "email": "admin@bootcamp.com",
      "fullName": "System Admin",
      "role": "ADMIN"
    },
    "accessToken": "jwt-token",
    "refreshToken": "refresh-token"
  }
}
```

### Protected Routes
Include JWT in Authorization header:
```
Authorization: Bearer <access-token>
```

## 👥 Default Test Accounts

After running seed script:

| Role       | Email                      | Password     |
|------------|----------------------------|--------------|
| Admin      | admin@bootcamp.com         | Password123! |
| Sales      | sales1@bootcamp.com        | Password123! |
| Instructor | instructor1@bootcamp.com   | Password123! |
| Mentor     | mentor1@bootcamp.com       | Password123! |
| Student 1  | student1@bootcamp.com      | Password123! |
| Student 2  | student2@bootcamp.com      | Password123! |

## 🏗️ Project Structure

```
backend/
├── prisma/
│   ├── schema.prisma      # Database schema
│   └── seed.ts            # Seed data
├── src/
│   ├── config/            # Configuration files
│   │   ├── config.ts      # Environment config
│   │   ├── database.ts    # Prisma client
│   │   └── logger.ts      # Winston logger
│   ├── controllers/       # Request handlers
│   │   ├── auth.controller.ts
│   │   └── lead.controller.ts
│   ├── services/          # Business logic
│   │   ├── auth.service.ts
│   │   ├── lead.service.ts
│   │   ├── bootcamp.service.ts
│   │   ├── enrollment.service.ts
│   │   ├── assignment.service.ts
│   │   └── lms.service.ts
│   ├── middleware/        # Express middleware
│   │   ├── auth.middleware.ts
│   │   ├── error.middleware.ts
│   │   ├── validate.middleware.ts
│   │   └── logger.middleware.ts
│   ├── routes/            # API routes
│   │   ├── index.ts
│   │   ├── auth.routes.ts
│   │   ├── lead.routes.ts
│   │   ├── bootcamp.routes.ts
│   │   ├── enrollment.routes.ts
│   │   ├── assignment.routes.ts
│   │   └── lms.routes.ts
│   ├── utils/             # Utility functions
│   │   ├── auth.utils.ts
│   │   ├── response.utils.ts
│   │   └── helpers.utils.ts
│   └── server.ts          # Express app entry
├── logs/                  # Application logs
├── .env                   # Environment variables
├── .env.example           # Environment template
├── package.json
└── tsconfig.json
```

## 🔧 Development

### Available Scripts

```powershell
# Development
npm run dev              # Start dev server with hot reload

# Build
npm run build            # Compile TypeScript to JavaScript
npm start                # Start production server

# Database
npm run prisma:generate  # Generate Prisma client
npm run prisma:migrate   # Run database migrations
npm run prisma:migrate:deploy  # Deploy migrations (production)
npm run prisma:seed      # Seed database with test data
npm run prisma:studio    # Open Prisma Studio (database GUI)
```

### Database Migrations

Create new migration:
```powershell
npx prisma migrate dev --name migration_name
```

Reset database:
```powershell
npx prisma migrate reset
```

## 📊 Response Format

### Success Response
```json
{
  "success": true,
  "message": "Operation successful",
  "data": { }
}
```

### Error Response
```json
{
  "success": false,
  "message": "Error message",
  "errors": []
}
```

### Paginated Response
```json
{
  "success": true,
  "message": "Data retrieved",
  "data": [],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "totalPages": 5
  }
}
```

## 🔒 Security Best Practices

1. **Change default JWT secrets** in `.env` before production
2. **Use HTTPS** in production
3. **Enable rate limiting** for API endpoints
4. **Implement CORS** whitelist for production domains
5. **Regular security audits** with `npm audit`
6. **Keep dependencies updated**
7. **Use environment-specific configs**
8. **Enable SQL injection protection** (Prisma handles this)
9. **Sanitize user inputs**
10. **Implement request logging and monitoring**

## 🧪 Testing

Test API with cURL:
```powershell
# Health check
curl http://localhost:5000/api/v1/health

# Login
curl -X POST http://localhost:5000/api/v1/auth/login `
  -H "Content-Type: application/json" `
  -d '{"email":"admin@bootcamp.com","password":"Password123!"}'

# Get leads (with auth)
curl http://localhost:5000/api/v1/leads `
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 📝 Environment Variables

Required variables in `.env`:
```
DATABASE_URL           # Neon PostgreSQL connection string
JWT_ACCESS_SECRET      # Secret for access tokens
JWT_REFRESH_SECRET     # Secret for refresh tokens
JWT_ACCESS_EXPIRY      # Access token expiry (e.g., "15m")
JWT_REFRESH_EXPIRY     # Refresh token expiry (e.g., "7d")
PORT                   # Server port (default: 5000)
NODE_ENV               # Environment (development/production)
CORS_ORIGIN            # Allowed CORS origin
EMAIL_FROM             # Email sender address
EMAIL_ENABLED          # Enable email notifications (true/false)
```

## 🚀 Deployment

### Production Checklist
- [ ] Update JWT secrets with strong random values
- [ ] Set `NODE_ENV=production`
- [ ] Configure production CORS origins
- [ ] Set up SSL/TLS certificates
- [ ] Configure production database
- [ ] Set up monitoring and logging
- [ ] Implement rate limiting
- [ ] Configure backup strategy
- [ ] Set up CI/CD pipeline
- [ ] Document API with Swagger/OpenAPI

### Deploy to Production
```powershell
# Build
npm run build

# Run migrations
npm run prisma:migrate:deploy

# Start production server
npm start
```

## 📖 Additional Resources

- [Prisma Documentation](https://www.prisma.io/docs/)
- [Express.js Guide](https://expressjs.com/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

## 🐛 Troubleshooting

### Database Connection Issues
```powershell
# Test database connection
npx prisma db pull

# View database in browser
npm run prisma:studio
```

### Migration Issues
```powershell
# Reset and re-run migrations
npx prisma migrate reset
npm run prisma:migrate
npm run prisma:seed
```

### TypeScript Errors
```powershell
# Regenerate Prisma client
npm run prisma:generate

# Clean build
Remove-Item -Recurse -Force dist
npm run build
```

## 📞 Support

For issues and questions:
1. Check existing documentation
2. Review error logs in `logs/` directory
3. Verify environment variables
4. Test with Prisma Studio

---

**Version:** 1.0.0  
**Last Updated:** January 2026  
**License:** MIT
