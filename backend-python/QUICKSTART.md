# 🚀 Cohortly Backend - Quick Start

Get the Python FastAPI backend running in **3 simple steps**:

## Step 1: Install Dependencies

```bash
# Navigate to backend directory
cd backend-python

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

## Step 2: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your credentials
# At minimum, update DATABASE_URL with your PostgreSQL connection string
```

**Required .env variables:**
- `DATABASE_URL` - Your PostgreSQL connection string
- `JWT_ACCESS_SECRET` - Secret key for access tokens
- `JWT_REFRESH_SECRET` - Secret key for refresh tokens

## Step 3: Start the Server

```bash
# Run the server
python -m app.main

# Or use uvicorn directly with auto-reload
uvicorn app.main:app --reload --port 5000
```

**The server will start on:** http://localhost:5000

**API Documentation:** http://localhost:5000/api/docs

---

## ✅ What's Working

- ✅ **Database Models** - User, Bootcamp, Enrollment, Assignment, Lead
- ✅ **Authentication** - JWT-based auth with access & refresh tokens
- ✅ **API Routes** - All 5 route modules implemented:
  - `/api/v1/auth` - Register, login, refresh, profile
  - `/api/v1/bootcamps` - Full CRUD for bootcamps
  - `/api/v1/enrollments` - Student enrollment management
  - `/api/v1/assignments` - Assignment creation and tracking
  - `/api/v1/leads` - Lead management for sales
- ✅ **Role-Based Access Control** - Admin, Sales, Instructor, Mentor, Student
- ✅ **Request Validation** - Pydantic schemas for all endpoints
- ✅ **Auto Documentation** - Swagger UI and ReDoc
- ✅ **CORS Configured** - Ready for frontend integration
- ✅ **Test Suite** - pytest tests for auth and bootcamps

---

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_auth.py -v
```

---

## 📚 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get tokens
- `POST /api/v1/auth/refresh` - Refresh access token
- `GET /api/v1/auth/me` - Get current user
- `PUT /api/v1/auth/me` - Update current user

### Bootcamps
- `GET /api/v1/bootcamps` - List bootcamps (paginated)
- `POST /api/v1/bootcamps` - Create bootcamp (Instructor/Admin)
- `GET /api/v1/bootcamps/{id}` - Get bootcamp details
- `PUT /api/v1/bootcamps/{id}` - Update bootcamp
- `DELETE /api/v1/bootcamps/{id}` - Delete bootcamp

### Enrollments
- `GET /api/v1/enrollments` - List enrollments (filtered by role)
- `POST /api/v1/enrollments` - Enroll student
- `GET /api/v1/enrollments/{id}` - Get enrollment details
- `PUT /api/v1/enrollments/{id}` - Update enrollment status
- `DELETE /api/v1/enrollments/{id}` - Delete enrollment (Admin)

### Assignments
- `GET /api/v1/assignments` - List assignments
- `POST /api/v1/assignments` - Create assignment (Instructor/Admin)
- `GET /api/v1/assignments/{id}` - Get assignment details
- `PUT /api/v1/assignments/{id}` - Update assignment
- `DELETE /api/v1/assignments/{id}` - Delete assignment

### Leads
- `GET /api/v1/leads` - List leads (Sales/Admin)
- `POST /api/v1/leads` - Create lead
- `GET /api/v1/leads/{id}` - Get lead details
- `PUT /api/v1/leads/{id}` - Update lead
- `DELETE /api/v1/leads/{id}` - Delete lead

---

## 🔍 Next Steps

1. **Connect Frontend** - Update `NEXT_PUBLIC_API_URL` in frontend `.env.local`
2. **Deploy Backend** - Deploy to Render, Railway, or your platform of choice
3. **Add Features** - Email notifications, file uploads, analytics
4. **Performance Tuning** - Add caching, optimize queries
5. **Monitoring** - Add logging, error tracking, metrics

---

## 📖 Full Documentation

See [README.md](README.md) for complete documentation including:
- Detailed API endpoint descriptions
- Database schema
- Deployment guides
- Performance benchmarks
- Troubleshooting

---

**Happy Coding! 🎉**
