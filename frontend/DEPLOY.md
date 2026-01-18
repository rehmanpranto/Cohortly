# Cohortly Frontend - Vercel Deployment

## 🚀 Quick Deploy to Vercel

### Step 1: Set Root Directory
When importing from GitHub, **IMPORTANT:** Set **Root Directory** to `frontend`

### Step 2: Environment Variables
Add this environment variable in Vercel:

```
NEXT_PUBLIC_API_URL=https://your-backend-url.onrender.com/api/v1
```

### Step 3: Deploy Settings
- **Framework:** Next.js (auto-detected)
- **Build Command:** `npm run build`
- **Output Directory:** `.next`
- **Install Command:** `npm install`
- **Node Version:** 18.x or 20.x

### Step 4: Deploy
Click **Deploy** button!

---

## 📋 Complete Guide
See the main deployment guide at: `../VERCEL_DEPLOYMENT_GUIDE.md`

---

## 🔗 Expected Result
Your frontend will be live at: `https://cohortly.vercel.app`
