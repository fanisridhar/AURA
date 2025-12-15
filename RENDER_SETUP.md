# 🚀 Render Deployment Setup Guide

## Step-by-Step Configuration

### 1. Root Directory (Optional)
**Leave this EMPTY** - Your repository root is correct since `main.py` is at the root level.

### 2. Instance Type Selection

**For Testing/Development:**
- ✅ **Free ($0/month)** - Good for testing, but:
  - Spins down after inactivity (slow first request)
  - Limited resources (512 MB RAM, 0.1 CPU)
  - May struggle with transformers model loading

**Recommended for Production:**
- ✅ **Starter ($7/month)** - Best balance:
  - 512 MB RAM, 0.5 CPU
  - Always running (no spin-down)
  - Better for ML models
  - Supports all features

**For Heavy Usage:**
- **Standard ($25/month)** - 2 GB RAM, 1 CPU
- **Pro ($85/month)** - 4 GB RAM, 2 CPU (for high traffic)

### 3. Environment Variables Setup

Add these variables in the Environment Variables section:

```
OPENAI_API_KEY=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
TAVILY_API_KEY=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
YOUTUBE_VIDEO_API_KEY=AIzaSyAcROR1pGW7uiLPXPp9MqQ3D8PpsOsADQk
YOUTUBE_MUSIC_API_KEY=AIzaSyAcROR1pGW7uiLPXPp9MqQ3D8PpsOsADQk
ELEVEN_LABS_API_KEY=sk_86e091e039aed9867ea1f59b228c06ffa3a015ee82a6f5ce
SPOTIFY_CLIENT_ID=a18b55dfd80e4f5083c2b982ff7410a1
SPOTIFY_CLIENT_SECRET=05b284e28422487e9808960bd640bbd8
HUGGINGFACE_TOKEN=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
```

**⚠️ IMPORTANT:** After Render gives you a URL (e.g., `https://aura-app.onrender.com`), add:

```
BASE_URL=https://your-app-name.onrender.com
REACT_APP_API_URL=https://your-app-name.onrender.com
PORT=10000
```

### 4. Build & Start Commands

Render should auto-detect from `render.yaml`, but verify:

**Build Command:**
```bash
pip install -r requirements.txt && cd frontend && npm install && npm run build
```

**Start Command:**
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 5. Python Version

Make sure Python 3.11 is selected:
- Go to Settings → Environment
- Python Version: **3.11** (not 3.13!)

### 6. After Deployment

1. **Update Spotify Redirect URI:**
   - Go to https://developer.spotify.com/dashboard
   - Edit your app
   - Add: `https://your-app-name.onrender.com/callback`

2. **Test your deployment:**
   - Visit your Render URL
   - Test chat functionality
   - Check all tabs (Journal, Content, Mood)

## Troubleshooting

**Build fails?**
- Check Python version is 3.11
- Verify all environment variables are set
- Check build logs for specific errors

**App crashes on startup?**
- Check if transformers model is downloading (first run takes time)
- Verify all API keys are correct
- Check instance has enough memory (may need Starter plan)

**Slow first request?**
- Free plan spins down - upgrade to Starter for always-on

## Recommended Settings Summary

✅ **Root Directory:** Leave empty  
✅ **Instance Type:** Starter ($7/month) for production  
✅ **Python Version:** 3.11  
✅ **All Environment Variables:** Added (see above)  
✅ **Build Command:** Auto-detected from render.yaml  
✅ **Start Command:** Auto-detected from render.yaml  

