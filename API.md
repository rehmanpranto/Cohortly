# 📡 API DOCUMENTATION

Complete API reference for the Bootcamp Management System.

**Base URL:** `http://localhost:5000/api/v1`

**Authentication:** Bearer Token (JWT)

---

## 📋 Table of Contents

1. [Response Format](#response-format)
2. [Authentication](#authentication)
3. [Lead Management](#lead-management)
4. [Bootcamp Management](#bootcamp-management)
5. [Enrollment & Payments](#enrollment--payments)
6. [LMS (Learning Management)](#lms-learning-management)
7. [Assignments & Grading](#assignments--grading)
8. [Error Codes](#error-codes)

---

## RESPONSE FORMAT

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

---

## AUTHENTICATION

### Register User

**POST** `/auth/register`

**Body:**
```json
{
  "email": "user@example.com",
  "password": "YourSecurePassword",
  "fullName": "John Doe",
  "phone": "+1234567890",
  "role": "STUDENT"
}
```

**Roles:** `ADMIN`, `SALES`, `INSTRUCTOR`, `MENTOR`, `STUDENT`

**Response:** `201 Created`
```json
{
  "success": true,
  "message": "Registration successful",
  "data": {
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "fullName": "John Doe",
      "role": "STUDENT"
    },
    "accessToken": "jwt-access-token",
    "refreshToken": "jwt-refresh-token"
  }
}
```

---

### Login

**POST** `/auth/login`

**Body:**
```json
{
  "email": "admin@bootcamp.com",
  "password": "YourPassword"
}
```

**Response:** `200 OK`
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
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

---

### Refresh Token

**POST** `/auth/refresh`

**Body:**
```json
{
  "refreshToken": "your-refresh-token"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "Token refreshed successfully",
  "data": {
    "accessToken": "new-access-token"
  }
}
```

---

### Logout

**POST** `/auth/logout`

**Headers:** `Authorization: Bearer <token>`

**Body:**
```json
{
  "refreshToken": "your-refresh-token"
}
```

**Response:** `200 OK`

---

### Get Current User

**GET** `/auth/me`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "User retrieved successfully",
  "data": {
    "id": "uuid",
    "email": "admin@bootcamp.com",
    "role": "ADMIN"
  }
}
```

---

## LEAD MANAGEMENT

**Permissions:** `ADMIN`, `SALES`

### Create Lead

**POST** `/leads`

**Headers:** `Authorization: Bearer <token>`

**Body:**
```json
{
  "fullName": "Jane Prospect",
  "email": "jane@example.com",
  "phone": "+1234567890",
  "source": "WEBSITE",
  "assignedTo": "sales-user-id"
}
```

**Source values:** `WEBSITE`, `REFERRAL`, `SOCIAL_MEDIA`, `ADVERTISEMENT`, `DIRECT`, `OTHER`

**Response:** `201 Created`

---

### Get All Leads

**GET** `/leads`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `page` - Page number (default: 1)
- `limit` - Items per page (default: 20)
- `status` - Filter by status (NEW, CONTACTED, FOLLOWUP, INTERESTED, ENROLLED, LOST)
- `source` - Filter by source
- `assignedTo` - Filter by assigned user ID
- `search` - Search in name, email, phone

**Example:**
```
GET /leads?page=1&limit=20&status=NEW&search=jane
```

**Response:** `200 OK` (Paginated)

---

### Get Lead by ID

**GET** `/leads/:id`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "Lead retrieved successfully",
  "data": {
    "id": "uuid",
    "fullName": "Jane Prospect",
    "email": "jane@example.com",
    "phone": "+1234567890",
    "source": "WEBSITE",
    "status": "NEW",
    "assignedToUser": {
      "id": "uuid",
      "fullName": "Sarah Sales",
      "email": "sales@bootcamp.com"
    },
    "logs": [
      {
        "id": "uuid",
        "note": "Initial contact made",
        "nextFollowUp": "2026-01-20T10:00:00Z",
        "createdAt": "2026-01-18T14:30:00Z"
      }
    ]
  }
}
```

---

### Update Lead

**PUT** `/leads/:id`

**Headers:** `Authorization: Bearer <token>`

**Body:**
```json
{
  "status": "INTERESTED",
  "phone": "+1234567891"
}
```

**Response:** `200 OK`

---

### Delete Lead

**DELETE** `/leads/:id`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`

---

### Add Lead Log

**POST** `/leads/:id/logs`

**Headers:** `Authorization: Bearer <token>`

**Body:**
```json
{
  "note": "Called and discussed course details",
  "nextFollowUp": "2026-01-25T10:00:00Z"
}
```

**Response:** `201 Created`

---

### Get Upcoming Follow-ups

**GET** `/leads/follow-ups`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
Returns follow-ups for next 7 days for current user

---

## BOOTCAMP MANAGEMENT

### Create Bootcamp

**POST** `/bootcamps`

**Permissions:** `ADMIN`

**Headers:** `Authorization: Bearer <token>`

**Body:**
```json
{
  "title": "Full Stack Web Development",
  "description": "Complete MERN stack bootcamp",
  "mode": "HYBRID",
  "price": 1999.00,
  "duration": 16
}
```

**Mode values:** `LIVE`, `RECORDED`, `HYBRID`

**Response:** `201 Created`

---

### Get All Bootcamps

**GET** `/bootcamps`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `page` - Page number
- `limit` - Items per page
- `isActive` - Filter by active status (true/false)

**Response:** `200 OK` (Paginated)

---

### Get Bootcamp by ID

**GET** `/bootcamps/:id`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "Bootcamp retrieved successfully",
  "data": {
    "id": "uuid",
    "title": "Full Stack Web Development",
    "description": "Complete MERN stack bootcamp",
    "mode": "HYBRID",
    "price": "1999.00",
    "duration": 16,
    "isActive": true,
    "batches": [
      {
        "id": "uuid",
        "batchName": "FS-2026-JAN",
        "startDate": "2026-02-01T00:00:00Z",
        "endDate": "2026-05-31T00:00:00Z",
        "capacity": 30,
        "status": "UPCOMING"
      }
    ],
    "modules": [
      {
        "id": "uuid",
        "title": "Introduction to Web Development",
        "orderIndex": 1,
        "lessons": []
      }
    ]
  }
}
```

---

### Update Bootcamp

**PUT** `/bootcamps/:id`

**Permissions:** `ADMIN`

**Headers:** `Authorization: Bearer <token>`

**Body:** (Partial update supported)
```json
{
  "price": 2199.00,
  "isActive": true
}
```

**Response:** `200 OK`

---

### Create Batch

**POST** `/bootcamps/:bootcampId/batches`

**Permissions:** `ADMIN`

**Headers:** `Authorization: Bearer <token>`

**Body:**
```json
{
  "batchName": "FS-2026-MAR",
  "startDate": "2026-03-01T00:00:00Z",
  "endDate": "2026-06-30T00:00:00Z",
  "capacity": 30
}
```

**Response:** `201 Created`

---

### Get All Batches

**GET** `/bootcamps/batches`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `bootcampId` - Filter by bootcamp
- `status` - Filter by status (UPCOMING, ONGOING, COMPLETED, CANCELLED)

**Response:** `200 OK`

---

### Get Batch by ID

**GET** `/bootcamps/batches/:batchId`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
Includes bootcamp, instructors, mentors, enrollments

---

### Assign Instructor to Batch

**POST** `/bootcamps/batches/:batchId/instructors`

**Permissions:** `ADMIN`

**Headers:** `Authorization: Bearer <token>`

**Body:**
```json
{
  "instructorId": "instructor-user-id"
}
```

**Response:** `201 Created`

---

### Assign Mentor to Batch

**POST** `/bootcamps/batches/:batchId/mentors`

**Permissions:** `ADMIN`

**Headers:** `Authorization: Bearer <token>`

**Body:**
```json
{
  "mentorId": "mentor-user-id"
}
```

**Response:** `201 Created`

---

## ENROLLMENT & PAYMENTS

### Create Enrollment

**POST** `/enrollments`

**Permissions:** `ADMIN`, `SALES`

**Headers:** `Authorization: Bearer <token>`

**Body:**
```json
{
  "studentId": "student-user-id",
  "batchId": "batch-id"
}
```

**Response:** `201 Created`

---

### Get Enrollments

**GET** `/enrollments`

**Permissions:** `ADMIN`, `SALES`, `INSTRUCTOR`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `studentId` - Filter by student
- `batchId` - Filter by batch
- `status` - Filter by status (PENDING, ACTIVE, COMPLETED, DROPPED, SUSPENDED)

**Response:** `200 OK`

---

### Get Enrollment by ID

**GET** `/enrollments/:id`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
Includes student, batch, payments, attendances

---

### Update Enrollment Status

**PUT** `/enrollments/:id/status`

**Permissions:** `ADMIN`

**Headers:** `Authorization: Bearer <token>`

**Body:**
```json
{
  "status": "ACTIVE"
}
```

**Status values:** `PENDING`, `ACTIVE`, `COMPLETED`, `DROPPED`, `SUSPENDED`

**Response:** `200 OK`

---

### Record Payment

**POST** `/enrollments/payments`

**Permissions:** `ADMIN`, `SALES`

**Headers:** `Authorization: Bearer <token>`

**Body:**
```json
{
  "enrollmentId": "enrollment-id",
  "amount": 1999.00,
  "method": "CREDIT_CARD",
  "transactionId": "TXN123456"
}
```

**Method values:** `CREDIT_CARD`, `DEBIT_CARD`, `UPI`, `NET_BANKING`, `CASH`, `OTHER`

**Response:** `201 Created`

---

### Get Payments

**GET** `/enrollments/payments`

**Permissions:** `ADMIN`, `SALES`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `enrollmentId` - Filter by enrollment

**Response:** `200 OK`

---

### Get Payment by ID

**GET** `/enrollments/payments/:id`

**Permissions:** `ADMIN`, `SALES`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`

---

### Get Total Revenue

**GET** `/enrollments/revenue/total`

**Permissions:** `ADMIN`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "Total revenue retrieved",
  "data": {
    "totalRevenue": "15999.00"
  }
}
```

---

## LMS (LEARNING MANAGEMENT)

### Create Module

**POST** `/lms/modules`

**Permissions:** `ADMIN`, `INSTRUCTOR`

**Headers:** `Authorization: Bearer <token>`

**Body:**
```json
{
  "bootcampId": "bootcamp-id",
  "title": "Introduction to JavaScript",
  "description": "JavaScript fundamentals",
  "orderIndex": 1
}
```

**Response:** `201 Created`

---

### Get Modules

**GET** `/lms/modules`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `bootcampId` - Required

**Response:** `200 OK`

---

### Create Lesson

**POST** `/lms/lessons`

**Permissions:** `ADMIN`, `INSTRUCTOR`

**Headers:** `Authorization: Bearer <token>`

**Body:**
```json
{
  "moduleId": "module-id",
  "title": "Variables and Data Types",
  "description": "Learn about JS variables",
  "contentType": "VIDEO",
  "contentUrl": "https://example.com/video.mp4",
  "duration": 45,
  "orderIndex": 1
}
```

**Content Type values:** `VIDEO`, `DOCUMENT`, `LINK`, `QUIZ`, `TEXT`

**Response:** `201 Created`

---

### Get Lessons

**GET** `/lms/lessons`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `moduleId` - Required

**Response:** `200 OK`

---

### Add Resource

**POST** `/lms/resources`

**Permissions:** `ADMIN`, `INSTRUCTOR`

**Headers:** `Authorization: Bearer <token>`

**Body:**
```json
{
  "lessonId": "lesson-id",
  "title": "JavaScript Cheat Sheet",
  "type": "PDF",
  "url": "https://example.com/cheatsheet.pdf"
}
```

**Resource Type values:** `PDF`, `VIDEO`, `LINK`, `CODE`, `IMAGE`, `OTHER`

**Response:** `201 Created`

---

### Mark Attendance

**POST** `/lms/attendance`

**Permissions:** `ADMIN`, `INSTRUCTOR`, `MENTOR`

**Headers:** `Authorization: Bearer <token>`

**Body:**
```json
{
  "enrollmentId": "enrollment-id",
  "batchId": "batch-id",
  "sessionDate": "2026-02-01T10:00:00Z",
  "present": true
}
```

**Response:** `201 Created`

---

### Get Student Attendance

**GET** `/lms/attendance/:enrollmentId`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`

---

### Get Batch Attendance

**GET** `/lms/attendance/batch/:batchId`

**Permissions:** `ADMIN`, `INSTRUCTOR`, `MENTOR`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `sessionDate` - Required (ISO 8601 format)

**Response:** `200 OK`

---

## ASSIGNMENTS & GRADING

### Create Assignment

**POST** `/assignments`

**Permissions:** `ADMIN`, `INSTRUCTOR`

**Headers:** `Authorization: Bearer <token>`

**Body:**
```json
{
  "lessonId": "lesson-id",
  "title": "Build a Todo App",
  "description": "Create a functional todo application using React",
  "maxScore": 100,
  "deadline": "2026-02-15T23:59:59Z"
}
```

**Response:** `201 Created`

---

### Get Assignments

**GET** `/assignments`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `lessonId` - Filter by lesson

**Response:** `200 OK`

---

### Get Assignment by ID

**GET** `/assignments/:id`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
Includes lesson, module, bootcamp, submissions

---

### Submit Assignment

**POST** `/assignments/submissions`

**Permissions:** `STUDENT`

**Headers:** `Authorization: Bearer <token>`

**Body:**
```json
{
  "assignmentId": "assignment-id",
  "submissionUrl": "https://github.com/student/todo-app",
  "content": "Implemented all features as requested"
}
```

**Response:** `201 Created`

---

### Get Submissions

**GET** `/assignments/submissions`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `assignmentId` - Filter by assignment
- `studentId` - Filter by student

**Response:** `200 OK`

---

### Grade Submission

**POST** `/assignments/submissions/:id/grade`

**Permissions:** `ADMIN`, `INSTRUCTOR`, `MENTOR`

**Headers:** `Authorization: Bearer <token>`

**Body:**
```json
{
  "score": 95,
  "feedback": "Excellent work! Good code structure and complete implementation."
}
```

**Response:** `201 Created`

---

### Get Pending Submissions

**GET** `/assignments/pending-grades`

**Permissions:** `ADMIN`, `INSTRUCTOR`, `MENTOR`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
Returns all submitted but ungraded assignments

---

## ERROR CODES

| Status Code | Meaning |
|-------------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Authentication required or failed |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error - Server error |

### Common Error Responses

**401 Unauthorized**
```json
{
  "success": false,
  "message": "Authentication required"
}
```

**403 Forbidden**
```json
{
  "success": false,
  "message": "Access denied: insufficient permissions"
}
```

**404 Not Found**
```json
{
  "success": false,
  "message": "Resource not found"
}
```

**400 Validation Error**
```json
{
  "success": false,
  "message": "Validation failed",
  "errors": [
    {
      "field": "email",
      "message": "Valid email is required"
    }
  ]
}
```

---

## AUTHENTICATION HEADERS

All protected endpoints require JWT token:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## TESTING WITH CURL

### Login
```powershell
curl -X POST http://localhost:5000/api/v1/auth/login `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"admin@bootcamp.com\",\"password\":\"YourPassword\"}'
```

### Get Bootcamps (Authenticated)
```powershell
$token = "your-token-here"
curl http://localhost:5000/api/v1/bootcamps `
  -H "Authorization: Bearer $token"
```

---

**API Version:** 1.0.0  
**Last Updated:** January 2026
