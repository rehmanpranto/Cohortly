# 🚀 Quick Start - Python Backend

## Install & Run in 3 Steps

### 1️⃣ Install Dependencies
```bash
cd backend-python
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 2️⃣ Start Server
```bash
uvicorn app.main:app --reload --port 5000
```

### 3️⃣ Open API Docs
Visit: http://localhost:5000/api/docs

---

## ✅ What's Working

- ✅ FastAPI application structure
- ✅ Database models (User, Bootcamp, Enrollment, Assignment, Lead)
- ✅ JWT authentication utilities
- ✅ Database connection (PostgreSQL/Neon)
- ✅ CORS middleware
- ✅ Auto-generated API documentation

---

## 🔨 To Complete

Next, I'll create:
1. Pydantic schemas (validation)
2. API routes (auth, bootcamps, enrollments, etc.)
3. Service layer (business logic)
4. Middleware (auth, error handling)

Would you like me to continue with the API implementation?
