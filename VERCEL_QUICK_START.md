# 🎯 Vercel Deployment - Step by Step

## The Issue You're Facing:
Your `.env` file is not uploading because it's **correctly** ignored by git for security. You need to configure environment variables directly in Vercel.

---

## ✅ SOLUTION: Follow These Exact Steps

### 🔴 STEP 1: Deploy Backend First (REQUIRED!)

Before deploying to Vercel, your backend must be online.

**Quick Option - Deploy to Render (Free):**

1. Go to https://render.com/
2. Sign up with GitHub
3. Click **New** > **Web Service**
4. Connect repository: `rehmanpranto/Cohortly`
5. Configure:
   ```
   Name: cohortly-backend
   Root Directory: backend
   Environment: Node
   Build Command: npm install && npx prisma generate
   Start Command: npm start
   ```
6. Add Environment Variables (click **Advanced** > **Add Environment Variable**):
   ```
   DATABASE_URL = postgresql://neondb_owner:npg_U3HCRaThw6JY@ep-falling-shadow-a1v2rodx-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
   
   JWT_ACCESS_SECRET = bootcamp-mgmt-secret-2026-access-token-key
   
   JWT_REFRESH_SECRET = bootcamp-mgmt-secret-2026-refresh-token-key
   
   JWT_ACCESS_EXPIRY = 15m
   
   JWT_REFRESH_EXPIRY = 7d
   
   PORT = 5000
   
   NODE_ENV = production
   
   CORS_ORIGIN = *
   ```
   (We'll update CORS_ORIGIN later with your Vercel URL)

7. Click **Create Web Service**
8. Wait 5-10 minutes for deployment
9. **COPY YOUR BACKEND URL** (e.g., `https://cohortly-backend.onrender.com`)

---

### 🟢 STEP 2: Deploy Frontend to Vercel

1. **Go to https://vercel.com/**
2. Sign up/Login with GitHub
3. Click **Add New...** > **Project**
4. **Import** `rehmanpranto/Cohortly` repository

5. **⚠️ CRITICAL CONFIGURATION:**
   
   Before clicking Deploy, configure these settings:

   **Framework Preset:** Next.js ✅ (should auto-detect)
   
   **Root Directory:** Click **Edit** and enter: `frontend` ✅✅✅
   
   **Build Command:** `npm run build` (auto-detected)
   
   **Output Directory:** `.next` (auto-detected)
   
   **Install Command:** `npm install` (auto-detected)

6. **Add Environment Variables:**
   
   Click **Environment Variables** section:
   
   ```
   Name: NEXT_PUBLIC_API_URL
   Value: https://cohortly-backend.onrender.com/api/v1
   ```
   
   (Replace with YOUR backend URL from Step 1)
   
   Select: ✅ Production ✅ Preview ✅ Development

7. **Click Deploy** 🚀

8. Wait 2-5 minutes for deployment

9. **COPY YOUR VERCEL URL** (e.g., `https://cohortly.vercel.app`)

---

### 🔄 STEP 3: Update Backend CORS

1. Go back to **Render Dashboard**
2. Select your `cohortly-backend` service
3. Go to **Environment** tab
4. Find `CORS_ORIGIN` variable
5. **Edit** and change from `*` to your Vercel URL:
   ```
   CORS_ORIGIN = https://cohortly.vercel.app
   ```
   (Use YOUR actual Vercel URL)
6. Service will auto-redeploy with new CORS settings

---

## ✅ Verify Deployment

1. **Visit your Vercel URL:** `https://cohortly.vercel.app`
2. **Test Registration:**
   - Go to Sign Up page
   - Create a test account
   - Should redirect to student portal

3. **Check Browser Console:**
   - Press F12
   - Go to Console tab
   - Look for any red errors
   - API calls should go to your backend URL

4. **Test Login:**
   - Log out
   - Log back in
   - Should work smoothly

---

## 🐛 If You See Errors:

### Error: "Root Directory not found"
**Fix:** In Vercel project settings:
1. Go to **Settings** > **General**
2. Find **Root Directory**
3. Change to: `frontend`
4. Save and redeploy

### Error: "API calls failing / Network Error"
**Fix 1:** Check backend is running:
- Visit your backend URL in browser
- Should see a response (health check or error message)

**Fix 2:** Check CORS:
- Make sure `CORS_ORIGIN` in backend includes your Vercel URL
- No trailing slash in URL

**Fix 3:** Check environment variable:
- In Vercel: Settings > Environment Variables
- Must be named exactly: `NEXT_PUBLIC_API_URL`
- Must include `/api/v1` at the end
- After adding/changing env vars, redeploy from Deployments tab

### Error: "Build failed"
**Fix:** Check Vercel build logs:
1. Go to **Deployments** tab
2. Click on failed deployment
3. Read the error message
4. Usually missing dependencies or TypeScript errors

---

## 🎉 Success Checklist

- [ ] Backend deployed on Render
- [ ] Backend URL copied
- [ ] Frontend deployed on Vercel
- [ ] Root directory set to `frontend`
- [ ] Environment variable `NEXT_PUBLIC_API_URL` added
- [ ] Vercel URL copied
- [ ] Backend CORS updated with Vercel URL
- [ ] Can access landing page
- [ ] Can register new user
- [ ] Can login
- [ ] Can access student portal

---

## 🚀 Your Live URLs

After successful deployment:

| Service | URL | Status |
|---------|-----|--------|
| Frontend (Vercel) | `https://cohortly.vercel.app` | ✅ |
| Backend (Render) | `https://cohortly-backend.onrender.com` | ✅ |
| API Base URL | `https://cohortly-backend.onrender.com/api/v1` | ✅ |

---

## 💡 Pro Tips

1. **Free Tier Limitations:**
   - Render: Backend may sleep after 15 min inactivity (first request takes ~30s)
   - Vercel: Unlimited bandwidth for hobby projects

2. **Auto-Deploy:**
   - Push to `master` branch → Auto-deploys to Vercel
   - No need to manually redeploy

3. **Preview Deployments:**
   - Every branch gets a preview URL
   - Test features before merging to master

4. **Logs:**
   - Vercel: Deployments > View Function Logs
   - Render: Logs tab in your service

5. **Custom Domain:**
   - Vercel: Settings > Domains > Add Domain
   - Free SSL certificate included

---

## 📞 Still Having Issues?

**Check these common mistakes:**

1. ❌ Forgot to set `frontend` as root directory
2. ❌ Environment variable named wrong (must be `NEXT_PUBLIC_API_URL`)
3. ❌ Missing `/api/v1` in API URL
4. ❌ Backend not deployed/running
5. ❌ CORS not updated with Vercel URL
6. ❌ Typing wrong URLs (check for typos)

**Need help?** Share the error message and I'll help debug!

---

**Estimated Total Time:** 20-30 minutes  
**Difficulty:** Easy (just follow the steps!)  
**Cost:** $0 (Free tier for both services)
