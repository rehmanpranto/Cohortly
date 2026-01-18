# 🚀 Vercel Deployment Guide - Cohortly

## 🎯 Overview

This guide will help you deploy your Cohortly application to Vercel.

---

## 📦 Project Structure

Cohortly has two parts:
- **Frontend:** Next.js application (to be deployed on Vercel)
- **Backend:** Node.js/Express API (to be deployed on Render/Railway/Heroku)

---

## 🌐 Part 1: Deploy Backend (Required First!)

### Option A: Deploy to Render (Recommended - Free Tier)

1. **Sign up at [Render](https://render.com/)**

2. **Create New Web Service:**
   - Click **New** > **Web Service**
   - Connect your GitHub repository: `rehmanpranto/Cohortly`
   - Root Directory: `backend`
   - Environment: `Node`
   - Build Command: `npm install && npx prisma generate`
   - Start Command: `npm start`

3. **Add Environment Variables:**
   ```
   DATABASE_URL=postgresql://neondb_owner:npg_U3HCRaThw6JY@ep-falling-shadow-a1v2rodx-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
   JWT_ACCESS_SECRET=bootcamp-mgmt-secret-2026-access-token-key
   JWT_REFRESH_SECRET=bootcamp-mgmt-secret-2026-refresh-token-key
   JWT_ACCESS_EXPIRY=15m
   JWT_REFRESH_EXPIRY=7d
   PORT=5000
   NODE_ENV=production
   CORS_ORIGIN=https://your-frontend-url.vercel.app
   ```

4. **Deploy and get your backend URL** (e.g., `https://cohortly-backend.onrender.com`)

### Option B: Deploy to Railway

1. Sign up at [Railway](https://railway.app/)
2. New Project > Deploy from GitHub
3. Select `rehmanpranto/Cohortly`
4. Set root directory: `backend`
5. Add all environment variables
6. Deploy and get your backend URL

---

## 🎨 Part 2: Deploy Frontend to Vercel

### Step 1: Prepare Frontend

Update `frontend/.env.local`:

```bash
NEXT_PUBLIC_API_URL=https://your-backend-url.onrender.com/api/v1
```

### Step 2: Deploy to Vercel

#### Method A: Vercel Dashboard (Easiest)

1. **Sign up/Login to [Vercel](https://vercel.com/)**

2. **Import Project:**
   - Click **Add New** > **Project**
   - Import from GitHub: `rehmanpranto/Cohortly`
   - Select the repository

3. **Configure Project:**
   - **Framework Preset:** Next.js
   - **Root Directory:** `frontend` ✅ (IMPORTANT!)
   - **Build Command:** `npm run build` (auto-detected)
   - **Output Directory:** `.next` (auto-detected)
   - **Install Command:** `npm install` (auto-detected)

4. **Add Environment Variables:**
   Click **Environment Variables** and add:
   ```
   Name: NEXT_PUBLIC_API_URL
   Value: https://your-backend-url.onrender.com/api/v1
   ```

5. **Click Deploy** 🚀

6. **Update Backend CORS:**
   After deployment, copy your Vercel URL (e.g., `https://cohortly.vercel.app`)
   Go back to Render/Railway and update:
   ```
   CORS_ORIGIN=https://cohortly.vercel.app
   ```

#### Method B: Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Navigate to frontend
cd frontend

# Login to Vercel
vercel login

# Deploy
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? cohortly
# - Directory? ./ (current directory)
# - Override settings? No

# Deploy to production
vercel --prod
```

---

## ⚙️ Configure Environment Variables in Vercel

### Via Dashboard:

1. Go to your project in Vercel
2. Click **Settings** > **Environment Variables**
3. Add:

| Name | Value | Environment |
|------|-------|-------------|
| `NEXT_PUBLIC_API_URL` | `https://your-backend.onrender.com/api/v1` | Production, Preview, Development |

### Via CLI:

```bash
vercel env add NEXT_PUBLIC_API_URL
# Enter value: https://your-backend.onrender.com/api/v1
# Select environments: Production, Preview, Development
```

---

## 🔧 Update Frontend API Configuration

Update `frontend/src/store/authStore.ts` if needed:

```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api/v1';
```

Update `frontend/src/app/signup/page.tsx`:

```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api/v1';
```

---

## 🔄 Auto-Deploy on Git Push

### Enable Automatic Deployments:

1. In Vercel Dashboard, go to **Settings** > **Git**
2. **Production Branch:** `master` or `main`
3. Enable **Automatic deployments from Git**

Now every push to `master` will automatically deploy! 🎉

---

## 🐛 Common Issues & Solutions

### Issue 1: "Root Directory not found"
**Solution:** 
- In Vercel project settings, set **Root Directory** to `frontend`
- Or move frontend files to root (not recommended)

### Issue 2: "Build failed - Module not found"
**Solution:**
```bash
# Make sure all dependencies are in package.json
cd frontend
npm install
npm run build  # Test locally first
```

### Issue 3: "API calls failing (CORS error)"
**Solution:**
- Update backend `CORS_ORIGIN` to include your Vercel URL
- Check if backend is running (visit backend URL in browser)

### Issue 4: "Environment variables not working"
**Solution:**
- Must start with `NEXT_PUBLIC_` for client-side access
- Redeploy after adding environment variables
- Check spelling and exact variable names

### Issue 5: "404 on page refresh"
**Solution:** Next.js handles this automatically, but ensure:
```json
// vercel.json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/" }
  ]
}
```

---

## 📱 Custom Domain Setup

### Add Custom Domain:

1. Go to **Project Settings** > **Domains**
2. Click **Add Domain**
3. Enter your domain: `cohortly.com`
4. Add DNS records at your registrar:

```
Type: A
Name: @
Value: 76.76.21.21

Type: CNAME  
Name: www
Value: cname.vercel-dns.com
```

5. Wait for DNS propagation (1-48 hours)
6. Vercel will automatically provision SSL certificate

---

## 🔒 Security Best Practices

### 1. Environment Variables
- ✅ Never commit `.env` files
- ✅ Use Vercel's environment variables
- ✅ Rotate secrets regularly

### 2. API Security
- ✅ Update CORS to only allow your frontend domain
- ✅ Enable rate limiting on backend
- ✅ Use HTTPS only (Vercel provides free SSL)

### 3. Database
- ✅ Use strong database passwords
- ✅ Enable SSL for database connections
- ✅ Whitelist only backend IP if possible

---

## 📊 Monitor Your Deployment

### Vercel Analytics:
1. Go to **Analytics** tab
2. View page views, performance metrics
3. Free tier: 100k page views/month

### Vercel Logs:
1. Go to **Deployments** > Select deployment
2. Click **View Function Logs**
3. Debug errors and API calls

---

## 🚀 Deployment Checklist

### Backend (Render/Railway):
- [ ] Create web service
- [ ] Set root directory to `backend`
- [ ] Add all environment variables
- [ ] Run database migrations
- [ ] Test API endpoints
- [ ] Note backend URL

### Frontend (Vercel):
- [ ] Import GitHub repository
- [ ] Set root directory to `frontend`
- [ ] Add `NEXT_PUBLIC_API_URL` environment variable
- [ ] Deploy to production
- [ ] Test all pages and features
- [ ] Update backend CORS with Vercel URL

### Post-Deployment:
- [ ] Test user registration
- [ ] Test login/logout
- [ ] Test student portal
- [ ] Test admin dashboard
- [ ] Check API calls in browser console
- [ ] Verify SSL certificate (green lock)
- [ ] Set up custom domain (optional)
- [ ] Enable auto-deploy on push

---

## 💡 Pro Tips

1. **Preview Deployments:** Every Git branch gets a preview URL
2. **Rollback:** Click **Redeploy** on previous deployment
3. **Environment-specific builds:** Use `NEXT_PUBLIC_ENV` variable
4. **Edge Functions:** Consider edge runtime for faster API routes
5. **Image Optimization:** Vercel automatically optimizes images

---

## 🔗 Useful Commands

```bash
# Check build locally
cd frontend
npm run build
npm start

# Test production build
npm run build && npm start

# Deploy specific branch
vercel --prod --branch staging

# View logs
vercel logs

# Remove deployment
vercel rm cohortly
```

---

## 📞 Need Help?

- **Vercel Docs:** https://vercel.com/docs
- **Next.js Deployment:** https://nextjs.org/docs/deployment
- **Vercel Support:** support@vercel.com
- **Community:** https://github.com/vercel/vercel/discussions

---

## 🎯 Expected URLs After Deployment

- **Frontend:** `https://cohortly.vercel.app`
- **Backend:** `https://cohortly-backend.onrender.com`
- **API Base:** `https://cohortly-backend.onrender.com/api/v1`

---

## 🔄 Continuous Deployment Workflow

```
1. Make changes locally
2. Test: npm run dev
3. Commit: git add . && git commit -m "Your message"
4. Push: git push origin master
5. Vercel automatically deploys
6. Check deployment at: https://cohortly.vercel.app
```

---

**Last Updated:** January 19, 2026  
**Status:** Ready for Deployment  
**Estimated Time:** 30-60 minutes
