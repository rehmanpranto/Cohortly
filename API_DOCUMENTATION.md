# HDNB Cohortly Mobile API Documentation

## Base URL
```
https://cohortly-35gn.onrender.com/api/v1
```

## Authentication
All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

---

## 📱 API Endpoints

### 🔐 Authentication

#### 1. Login
**POST** `/api/v1/auth/login`

Login and receive JWT token.

**Request Body:**
```json
{
  "email": "student@example.com",
  "password": "yourpassword"
}
```

**Response (200):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "student@example.com",
    "full_name": "John Doe",
    "role": "student",
    "phone": "+1234567890",
    "is_active": true
  }
}
```

**Error Responses:**
- `400`: Missing email or password
- `401`: Invalid credentials
- `403`: Account inactive

---

#### 2. Register
**POST** `/api/v1/auth/register`

Register a new student account.

**Request Body:**
```json
{
  "email": "newstudent@example.com",
  "password": "securepassword",
  "full_name": "Jane Smith",
  "phone": "+1234567890"
}
```

**Response (201):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "newstudent@example.com",
    "full_name": "Jane Smith",
    "role": "student"
  }
}
```

**Error Responses:**
- `400`: Missing required fields
- `409`: Email already registered

---

#### 3. Refresh Token
**POST** `/api/v1/auth/refresh`

Get a new JWT token (requires valid token).

**Headers:**
```
Authorization: Bearer <current_token>
```

**Response (200):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### 👤 User Profile

#### 4. Get Profile
**GET** `/api/v1/user/profile`

Get current user's profile information.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "student@example.com",
  "full_name": "John Doe",
  "phone": "+1234567890",
  "role": "student",
  "is_active": true,
  "created_at": "2026-01-15T10:30:00",
  "student_profile": {
    "linkedin_url": "https://linkedin.com/in/johndoe",
    "github_url": "https://github.com/johndoe",
    "portfolio_url": "https://johndoe.com",
    "bio": "Passionate developer"
  }
}
```

---

#### 5. Update Profile
**PUT** `/api/v1/user/profile`

Update user profile.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "full_name": "John Updated Doe",
  "phone": "+9876543210"
}
```

**Response (200):**
```json
{
  "message": "Profile updated successfully"
}
```

---

### 🎓 Bootcamps

#### 6. Get All Bootcamps
**GET** `/api/v1/bootcamps`

Get all active bootcamps (public endpoint, no auth required).

**Response (200):**
```json
{
  "bootcamps": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "title": "Full Stack Web Development",
      "description": "Learn MERN stack development",
      "mode": "live",
      "price": 2999.99,
      "duration_weeks": 12,
      "created_at": "2026-01-01T00:00:00"
    }
  ]
}
```

---

#### 7. Get Bootcamp Details
**GET** `/api/v1/bootcamps/<bootcamp_id>`

Get detailed information about a bootcamp including available batches.

**Response (200):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Full Stack Web Development",
  "description": "Comprehensive web development course",
  "mode": "live",
  "price": 2999.99,
  "duration_weeks": 12,
  "batches": [
    {
      "id": "batch-uuid",
      "name": "Batch 1",
      "start_date": "2026-02-01",
      "end_date": "2026-04-30",
      "is_active": true
    }
  ]
}
```

---

### 📚 Enrollments

#### 8. Get My Enrollments
**GET** `/api/v1/enrollments`

Get all enrollments for the current student.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "enrollments": [
    {
      "id": "enrollment-uuid",
      "batch": {
        "id": "batch-uuid",
        "name": "Batch 1",
        "bootcamp": {
          "id": "bootcamp-uuid",
          "title": "Full Stack Web Development"
        }
      },
      "status": "active",
      "progress_percentage": 65,
      "enrolled_at": "2026-01-15T10:00:00",
      "completed_at": null
    }
  ]
}
```

---

#### 9. Get Enrollment Progress
**GET** `/api/v1/enrollments/<enrollment_id>/progress`

Get detailed progress including milestones for an enrollment.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "enrollment_id": "enrollment-uuid",
  "progress_percentage": 65,
  "bootcamp": {
    "id": "bootcamp-uuid",
    "title": "Full Stack Web Development",
    "duration_weeks": 12
  },
  "milestones": [
    {
      "id": "milestone-uuid",
      "title": "HTML & CSS Fundamentals",
      "description": "Master the basics of web design",
      "order": 1,
      "percentage_weight": 10,
      "completed": true,
      "completed_at": "2026-01-20T14:30:00"
    },
    {
      "id": "milestone-uuid-2",
      "title": "JavaScript Essentials",
      "description": "Learn JavaScript programming",
      "order": 2,
      "percentage_weight": 15,
      "completed": false,
      "completed_at": null
    }
  ]
}
```

---

### 📅 Class Schedule

#### 10. Get Class Schedule
**GET** `/api/v1/enrollments/<enrollment_id>/classes`

Get upcoming and past class schedules for an enrollment.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "upcoming": [
    {
      "id": "class-uuid",
      "week_number": 3,
      "topic": "React Fundamentals",
      "description": "Introduction to React library",
      "class_date": "2026-01-25",
      "class_time": "19:00",
      "duration_minutes": 120,
      "zoom_link": "https://zoom.us/j/123456789",
      "zoom_meeting_id": "123 456 789",
      "zoom_passcode": "abc123"
    }
  ],
  "past": [
    {
      "id": "class-uuid-2",
      "week_number": 2,
      "topic": "JavaScript Basics",
      "class_date": "2026-01-20",
      "recording_link": "https://zoom.us/rec/share/..."
    }
  ]
}
```

---

### 🏆 Certificates

#### 11. Get Certificate
**GET** `/api/v1/enrollments/<enrollment_id>/certificate`

Get certificate for a completed enrollment (100% progress required).

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "id": "cert-uuid",
  "verification_code": "HDNB-2026-ABCD1234",
  "issued_at": "2026-04-30T10:00:00",
  "certificate_url": null,
  "bootcamp": {
    "title": "Full Stack Web Development",
    "duration_weeks": 12
  },
  "verification_url": "/lms/certificate/verify/HDNB-2026-ABCD1234"
}
```

**Error Responses:**
- `403`: Course not completed yet
- `404`: Certificate not generated

---

### 📢 Announcements

#### 12. Get Announcements
**GET** `/api/v1/announcements`

Get announcements for student's enrolled batches.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "announcements": [
    {
      "id": "announcement-uuid",
      "title": "Class Rescheduled",
      "content": "Tomorrow's class has been moved to 8 PM",
      "priority": "high",
      "created_at": "2026-01-21T09:00:00",
      "author": {
        "name": "John Instructor",
        "role": "instructor"
      }
    }
  ]
}
```

---

### 💳 Payments

#### 13. Get Payment History
**GET** `/api/v1/payments`

Get payment history for the current student.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "payments": [
    {
      "id": "payment-uuid",
      "amount": 2999.99,
      "payment_method": "credit_card",
      "status": "completed",
      "transaction_id": "TXN_123456",
      "paid_at": "2026-01-15T10:00:00",
      "bootcamp": "Full Stack Web Development"
    }
  ]
}
```

---

### 💼 Portfolio

#### 14. Get Portfolio Items
**GET** `/api/v1/portfolio`

Get user's portfolio items.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "portfolio_items": [
    {
      "id": "portfolio-uuid",
      "item_type": "project",
      "title": "E-commerce Website",
      "description": "Full-stack e-commerce platform",
      "github_url": "https://github.com/user/ecommerce",
      "demo_url": "https://myecommerce.com",
      "image_url": "https://image.url/screenshot.png",
      "technologies": ["React", "Node.js", "MongoDB"],
      "is_featured": true,
      "created_at": "2026-01-15T10:00:00"
    }
  ]
}
```

---

### 🎯 Leads (Marketing)

#### 15. Create Lead
**POST** `/api/v1/leads`

Create a new lead (public endpoint, no auth required).

**Request Body:**
```json
{
  "full_name": "Potential Student",
  "email": "potential@example.com",
  "phone": "+1234567890",
  "source": "Mobile App",
  "interested_bootcamp": "Full Stack Web Development"
}
```

**Response (201):**
```json
{
  "message": "Lead created successfully",
  "lead_id": "lead-uuid"
}
```

---

### ❤️ Health Check

#### 16. Health Check
**GET** `/api/v1/health`

Check API health status (public endpoint).

**Response (200):**
```json
{
  "status": "healthy",
  "version": "v1",
  "timestamp": "2026-01-21T10:00:00"
}
```

---

## 🔒 Security Notes

1. **Token Expiration**: JWT tokens expire after 24 hours
2. **HTTPS Required**: All API calls should use HTTPS in production
3. **Rate Limiting**: Consider implementing rate limiting for production
4. **CORS**: Configure CORS settings for mobile app domains

## 📱 Mobile App Integration Guide

### Step 1: Login/Register
```javascript
// Example: React Native
const login = async (email, password) => {
  const response = await fetch('https://cohortly-35gn.onrender.com/api/v1/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password })
  });
  
  const data = await response.json();
  // Store token securely (AsyncStorage, SecureStore, etc.)
  await SecureStore.setItemAsync('jwt_token', data.token);
  return data;
};
```

### Step 2: Make Authenticated Requests
```javascript
const getEnrollments = async () => {
  const token = await SecureStore.getItemAsync('jwt_token');
  
  const response = await fetch('https://cohortly-35gn.onrender.com/api/v1/enrollments', {
    headers: {
      'Authorization': `Bearer ${token}`,
    }
  });
  
  return await response.json();
};
```

### Step 3: Handle Token Refresh
```javascript
const refreshToken = async () => {
  const oldToken = await SecureStore.getItemAsync('jwt_token');
  
  const response = await fetch('https://cohortly-35gn.onrender.com/api/v1/auth/refresh', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${oldToken}`,
    }
  });
  
  const data = await response.json();
  await SecureStore.setItemAsync('jwt_token', data.token);
  return data.token;
};
```

---

## 🚀 Testing the API

### Using cURL
```bash
# Login
curl -X POST https://cohortly-35gn.onrender.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"student@example.com","password":"password123"}'

# Get enrollments (replace TOKEN with actual token)
curl -X GET https://cohortly-35gn.onrender.com/api/v1/enrollments \
  -H "Authorization: Bearer TOKEN"
```

### Using Postman
1. Import endpoints into Postman
2. Set base URL: `https://cohortly-35gn.onrender.com/api/v1`
3. Add Authorization header with Bearer token
4. Test each endpoint

---

## 📝 Error Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request (missing/invalid data) |
| 401 | Unauthorized (invalid/missing token) |
| 403 | Forbidden (insufficient permissions) |
| 404 | Not Found |
| 409 | Conflict (duplicate data) |
| 500 | Internal Server Error |

---

## 🎯 Next Steps for Mobile Development

1. **Authentication Flow**: Implement login/register screens
2. **Token Management**: Store JWT securely, handle refresh
3. **Dashboard**: Display enrollments with progress bars
4. **Class Schedule**: Show upcoming classes with Zoom links
5. **Progress Tracking**: Visual milestone timeline
6. **Certificate Display**: Show and share certificates
7. **Push Notifications**: For announcements and class reminders
8. **Offline Support**: Cache data for offline access

---

## 📞 Support

For API issues or questions, contact: support@hdnbbootcamp.com
