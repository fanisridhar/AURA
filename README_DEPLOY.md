# 🚀 Quick Deployment Guide

## Deploy to Railway (Easiest - Recommended)

### Step 1: Prepare Your Repository
```bash
# Make sure all changes are committed
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### Step 2: Deploy on Railway

1. Go to [railway.app](https://railway.app) and sign up/login
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your AURA repository
4. Railway will automatically detect and start building

### Step 3: Set Environment Variables

In Railway dashboard → Your Project → Variables tab, add:

```
OPENAI_API_KEY=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
TAVILY_API_KEY=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
YOUTUBE_VIDEO_API_KEY=AIzaSyAcROR1pGW7uiLPXPp9MqQ3D8PpsOsADQk
YOUTUBE_MUSIC_API_KEY=AIzaSyAcROR1pGW7uiLPXPp9MqQ3D8PpsOsADQk
ELEVEN_LABS_API_KEY=sk_86e091e039aed9867ea1f59b228c06ffa3a015ee82a6f5ce
SPOTIFY_CLIENT_ID=a18b55dfd80e4f5083c2b982ff7410a1
SPOTIFY_CLIENT_SECRET=05b284e28422487e9808960bd640bbd8
HUGGINGFACE_TOKEN=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
REACT_APP_API_URL=https://your-app-name.railway.app
BASE_URL=https://your-app-name.railway.app
```

**Important:** Replace `your-app-name.railway.app` with your actual Railway URL (you'll see it after deployment)

### Step 4: Update Spotify Redirect URI

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Click on your app
3. Click **"Edit Settings"**
4. Add to **Redirect URIs**: `https://your-app-name.railway.app/callback`
5. Save

### Step 5: Redeploy

After setting environment variables, Railway will automatically redeploy. Your app will be live!

## Alternative: Deploy to Render

1. Go to [render.com](https://render.com) and sign up
2. Create **New Web Service**
3. Connect your GitHub repository
4. Use these settings:
   - **Build Command:** `cd frontend && npm install && npm run build && cd .. && pip install -r backend/requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add all environment variables (same as Railway)
6. Deploy!

## Testing Your Deployment

Once deployed, test:
- ✅ Chat functionality
- ✅ Journal entries loading
- ✅ Mood tracking
- ✅ Content feed (YouTube, Spotify, News)
- ✅ Spotify authentication

## Troubleshooting

**Build fails?**
- Check Railway/Render logs
- Ensure all dependencies are in `requirements.txt`
- Verify Node.js version compatibility

**API not working?**
- Check `REACT_APP_API_URL` matches your backend URL
- Verify CORS settings
- Check environment variables are set correctly

**Frontend not loading?**
- Ensure `npm run build` completed successfully
- Check that `frontend/build/` exists
- Verify static file serving in `main.py`

## Your App Will Be Live At:
- Railway: `https://your-app-name.railway.app`
- Render: `https://your-app-name.onrender.com`

Enjoy your deployed AURA! 🌟

