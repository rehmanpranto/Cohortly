# 🚀 BOOTCAMP MANAGEMENT SYSTEM - SETUP GUIDE

Complete step-by-step instructions to get the system running.

---

## 📋 PREREQUISITES

Before you begin, ensure you have:

- ✅ **Node.js 18+** installed ([Download](https://nodejs.org/))
- ✅ **npm or yarn** package manager
- ✅ **PowerShell** or terminal access
- ✅ **Code editor** (VS Code recommended)
- ✅ **Neon PostgreSQL** database (already configured)

---

## 🛠️ BACKEND SETUP

### Step 1: Navigate to Backend Directory

```powershell
cd h:\Bmc\backend
```

### Step 2: Install Dependencies

```powershell
npm install
```

This installs:
- Express, TypeScript, Prisma
- JWT, bcrypt for authentication
- Winston for logging
- Express-validator for validation
- All necessary dependencies

**Expected output:** Packages installed successfully

### Step 3: Verify Environment Variables

The `.env` file is already created with your Neon PostgreSQL credentials:

```powershell
cat .env
```

**Important:** For production, change the JWT secrets!

### Step 4: Generate Prisma Client

```powershell
npm run prisma:generate
```

This generates the TypeScript Prisma Client based on your schema.

**Expected output:** ✔ Generated Prisma Client

### Step 5: Run Database Migrations

```powershell
npm run prisma:migrate
```

When prompted for migration name, enter: `initial_setup`

This creates all tables in your Neon PostgreSQL database.

**Expected output:** Database synchronized successfully

### Step 6: Seed the Database

```powershell
npm run prisma:seed
```

This creates:
- 6 test user accounts (Admin, Sales, Instructor, Mentor, 2 Students)
- Sample bootcamps and batches
- Sample enrollments and payments
- Sample curriculum (modules and lessons)
- Sample assignments and submissions

**Expected output:**
```
🌱 Starting database seed...
✅ Created 6 users
✅ Created leads and logs
✅ Created 2 bootcamps
✅ Created batch with instructors and mentors
✅ Created 2 enrollments
✅ Created payments
✅ Created curriculum
✅ Created assignments
✅ Created announcement
✅ Created notifications

🎉 Seed completed successfully!

📧 Test Accounts:
   Admin:      admin@bootcamp.com / Password123!
   Sales:      sales1@bootcamp.com / Password123!
   Instructor: instructor1@bootcamp.com / Password123!
   Mentor:     mentor1@bootcamp.com / Password123!
   Student 1:  student1@bootcamp.com / Password123!
   Student 2:  student2@bootcamp.com / Password123!
```

### Step 7: Start Development Server

```powershell
npm run dev
```

**Expected output:**
```
✅ Database connected successfully
🚀 Server running on port 5000
📚 Environment: development
🌐 CORS enabled for: http://localhost:3000
✅ API v1 available at: http://localhost:5000/api/v1
```

The backend is now running! 🎉

---

## ✅ VERIFY BACKEND IS WORKING

### Test 1: Health Check

Open a new PowerShell window and run:

```powershell
curl http://localhost:5000/api/v1/health
```

**Expected response:**
```json
{
  "success": true,
  "message": "API is healthy",
  "timestamp": "2026-01-18T..."
}
```

### Test 2: Login with Admin Account

```powershell
curl -X POST http://localhost:5000/api/v1/auth/login `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"admin@bootcamp.com\",\"password\":\"Password123!\"}'
```

**Expected response:**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {
      "id": "uuid-here",
      "email": "admin@bootcamp.com",
      "fullName": "System Admin",
      "role": "ADMIN"
    },
    "accessToken": "eyJhbGciOiJIUzI1NiIs...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIs..."
  }
}
```

**Copy the accessToken** for next test!

### Test 3: Get Bootcamps (Authenticated)

Replace `YOUR_TOKEN` with the access token from previous step:

```powershell
$token = "YOUR_TOKEN_HERE"
curl http://localhost:5000/api/v1/bootcamps `
  -H "Authorization: Bearer $token"
```

If you see bootcamp data, authentication is working! ✅

---

## 🗄️ DATABASE MANAGEMENT

### Open Prisma Studio (Database GUI)

```powershell
npm run prisma:studio
```

Opens at: `http://localhost:5555`

You can:
- View all tables
- Browse data
- Edit records manually
- Run queries

### View Database Schema

```powershell
npx prisma db pull
```

This syncs the schema with your actual database.

### Reset Database (Careful!)

```powershell
npx prisma migrate reset
```

This will:
1. Drop all tables
2. Re-run all migrations
3. Re-seed the database

---

## 📊 FRONTEND SETUP (OPTIONAL)

### Create Next.js Frontend

```powershell
cd h:\Bmc
npx create-next-app@latest frontend --typescript --tailwind --app
```

Options:
- TypeScript: Yes
- ESLint: Yes
- Tailwind CSS: Yes
- `src/` directory: Yes
- App Router: Yes
- Import alias: No

### Install Additional Packages

```powershell
cd frontend
npm install axios react-query @tanstack/react-query
npm install -D @types/node
```

### Configure API URL

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:5000/api/v1
```

### Create API Client

Create `frontend/src/lib/api.ts`:

```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
```

### Create Login Page

Create `frontend/src/app/login/page.tsx`:

```typescript
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/lib/api';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await api.post('/auth/login', { email, password });
      localStorage.setItem('accessToken', response.data.data.accessToken);
      localStorage.setItem('refreshToken', response.data.data.refreshToken);
      localStorage.setItem('user', JSON.stringify(response.data.data.user));
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.message || 'Login failed');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-96">
        <h1 className="text-2xl font-bold mb-6">Bootcamp Management</h1>
        <form onSubmit={handleLogin}>
          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-3 py-2 border rounded"
              required
            />
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 border rounded"
              required
            />
          </div>
          {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
          >
            Login
          </button>
        </form>
        <div className="mt-4 text-sm text-gray-600">
          <p>Test accounts:</p>
          <p>admin@bootcamp.com / Password123!</p>
        </div>
      </div>
    </div>
  );
}
```

### Start Frontend

```powershell
cd frontend
npm run dev
```

Frontend runs at: `http://localhost:3000`

---

## 🧪 TESTING THE SYSTEM

### Test All API Endpoints

#### 1. Authentication Endpoints

```powershell
# Register new user
curl -X POST http://localhost:5000/api/v1/auth/register `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"test@example.com\",\"password\":\"Password123!\",\"fullName\":\"Test User\",\"role\":\"STUDENT\"}'

# Login
curl -X POST http://localhost:5000/api/v1/auth/login `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"admin@bootcamp.com\",\"password\":\"Password123!\"}'

# Get current user
curl http://localhost:5000/api/v1/auth/me `
  -H "Authorization: Bearer $token"
```

#### 2. Lead Management (Sales Role)

```powershell
# Login as sales
curl -X POST http://localhost:5000/api/v1/auth/login `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"sales1@bootcamp.com\",\"password\":\"Password123!\"}'

# Create lead
curl -X POST http://localhost:5000/api/v1/leads `
  -H "Authorization: Bearer $token" `
  -H "Content-Type: application/json" `
  -d '{\"fullName\":\"New Lead\",\"email\":\"lead@example.com\",\"phone\":\"+1234567890\",\"source\":\"WEBSITE\"}'

# Get all leads
curl http://localhost:5000/api/v1/leads `
  -H "Authorization: Bearer $token"
```

#### 3. Bootcamp Management

```powershell
# Get all bootcamps
curl http://localhost:5000/api/v1/bootcamps `
  -H "Authorization: Bearer $token"

# Get bootcamp by ID
curl http://localhost:5000/api/v1/bootcamps/{bootcamp-id} `
  -H "Authorization: Bearer $token"
```

---

## 🔧 TROUBLESHOOTING

### Issue: "Cannot find module '@prisma/client'"

**Solution:**
```powershell
npm run prisma:generate
```

### Issue: "Port 5000 already in use"

**Solution:**
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID)
taskkill /PID <PID> /F

# Or change port in .env
# PORT=5001
```

### Issue: Database connection failed

**Solution:**
1. Verify DATABASE_URL in `.env`
2. Check internet connection
3. Verify Neon database is active
4. Test connection:
```powershell
npx prisma db pull
```

### Issue: Migration failed

**Solution:**
```powershell
# Reset and retry
npx prisma migrate reset
npm run prisma:migrate
npm run prisma:seed
```

### Issue: TypeScript errors

**Solution:**
```powershell
# Clean and rebuild
Remove-Item -Recurse -Force dist
npm run build
```

### Issue: "refresh_tokens" table doesn't exist

**Solution:**
```powershell
# Run migrations
npm run prisma:migrate
```

---

## 📚 NEXT STEPS

### 1. Explore the API
- Use Postman or Insomnia
- Import the API endpoints
- Test each module

### 2. View Data in Prisma Studio
```powershell
npm run prisma:studio
```

### 3. Check Logs
```powershell
# View error logs
cat logs/error.log

# View all logs
cat logs/combined.log
```

### 4. Build Frontend
- Create login page
- Create dashboard for each role
- Implement CRUD operations
- Add real-time features

### 5. Deploy to Production
- Set up hosting (Vercel, Railway, AWS)
- Configure production database
- Update environment variables
- Enable HTTPS
- Set up monitoring

---

## 📞 SUPPORT

If you encounter issues:

1. ✅ Check this guide
2. ✅ Review error logs in `logs/` folder
3. ✅ Verify .env configuration
4. ✅ Test database connection with Prisma Studio
5. ✅ Check backend README.md
6. ✅ Review ARCHITECTURE.md

---

## ✨ QUICK REFERENCE

### Key Commands

```powershell
# Install dependencies
npm install

# Generate Prisma client
npm run prisma:generate

# Run migrations
npm run prisma:migrate

# Seed database
npm run prisma:seed

# Start dev server
npm run dev

# Open Prisma Studio
npm run prisma:studio

# Build for production
npm run build

# Start production server
npm start
```

### Default Ports
- Backend: `http://localhost:5000`
- Frontend: `http://localhost:3000`
- Prisma Studio: `http://localhost:5555`

### Test Accounts
- **Admin:** admin@bootcamp.com / Password123!
- **Sales:** sales1@bootcamp.com / Password123!
- **Instructor:** instructor1@bootcamp.com / Password123!
- **Mentor:** mentor1@bootcamp.com / Password123!
- **Student 1:** student1@bootcamp.com / Password123!
- **Student 2:** student2@bootcamp.com / Password123!

---

## 🎉 SUCCESS!

If you can:
- ✅ Login with test accounts
- ✅ Get healthy API response
- ✅ View data in Prisma Studio
- ✅ Access bootcamps endpoint

**Your Bootcamp Management System is ready!** 🚀

Start building features, customize the UI, and deploy to production.

---

**Last Updated:** January 2026  
**Version:** 1.0.0
