# AURA Deployment Guide

This guide will help you deploy AURA to a public platform.

## Deployment Options

### Option 1: Railway (Recommended - Easiest)

1. **Sign up at [Railway.app](https://railway.app)**

2. **Create a new project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo" (connect your GitHub account)
   - Select this repository

3. **Set Environment Variables:**
   Go to your project → Variables tab and add:
   ```
   OPENAI_API_KEY=your_openai_key
   TAVILY_API_KEY=your_tavily_key
   YOUTUBE_VIDEO_API_KEY=your_youtube_key
   YOUTUBE_MUSIC_API_KEY=your_youtube_key
   ELEVEN_LABS_API_KEY=your_elevenlabs_key
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_secret
   HUGGINGFACE_TOKEN=your_huggingface_token
   BASE_URL=https://your-app-name.railway.app
   PORT=8000
   ```

4. **Deploy:**
   - Railway will automatically detect the `railway.json` file
   - It will build the frontend and install Python dependencies
   - Your app will be live at `https://your-app-name.railway.app`

5. **Update Spotify Redirect URI:**
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Add your Railway URL: `https://your-app-name.railway.app/callback`

6. **Update Frontend Environment:**
   - In Railway, add: `REACT_APP_API_URL=https://your-app-name.railway.app`
   - Redeploy

### Option 2: Render

1. **Sign up at [Render.com](https://render.com)**

2. **Create a new Web Service:**
   - Connect your GitHub repository
   - Select "Web Service"
   - Use these settings:
     - **Build Command:** `cd frontend && npm install && npm run build && cd .. && pip install -r backend/requirements.txt`
     - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Set Environment Variables:**
   Add all the same variables as Railway (see above)

4. **Deploy:**
   - Render will use the `render.yaml` configuration
   - Your app will be live at `https://your-app-name.onrender.com`

### Option 3: Heroku

1. **Install Heroku CLI:**
   ```bash
   brew install heroku/brew/heroku  # macOS
   ```

2. **Login and create app:**
   ```bash
   heroku login
   heroku create your-app-name
   ```

3. **Set environment variables:**
   ```bash
   heroku config:set OPENAI_API_KEY=your_key
   heroku config:set TAVILY_API_KEY=your_key
   # ... add all other keys
   heroku config:set BASE_URL=https://your-app-name.herokuapp.com
   ```

4. **Deploy:**
   ```bash
   git push heroku main
   ```

## Pre-Deployment Checklist

- [ ] Build the frontend: `cd frontend && npm run build`
- [ ] Test locally with production build
- [ ] Update all API keys in deployment platform
- [ ] Update Spotify redirect URI in Spotify Developer Dashboard
- [ ] Set BASE_URL environment variable to your production URL
- [ ] Test all features after deployment

## Building Frontend for Production

```bash
cd frontend
npm install
npm run build
```

The build folder will be created in `frontend/build/` and will be served by the FastAPI backend.

## Environment Variables Required

Make sure to set these in your deployment platform:

- `OPENAI_API_KEY` - Required for AI responses
- `TAVILY_API_KEY` - For news search
- `YOUTUBE_VIDEO_API_KEY` - For video recommendations
- `YOUTUBE_MUSIC_API_KEY` - For music recommendations
- `ELEVEN_LABS_API_KEY` - For text-to-speech (optional)
- `SPOTIFY_CLIENT_ID` - For Spotify integration
- `SPOTIFY_CLIENT_SECRET` - For Spotify integration
- `HUGGINGFACE_TOKEN` - For emotion analysis
- `BASE_URL` - Your production URL (e.g., https://your-app.railway.app)
- `PORT` - Port number (usually set automatically by platform)

## Troubleshooting

### Frontend not loading
- Check that `npm run build` completed successfully
- Verify `frontend/build/` directory exists
- Check that static files are being served correctly

### API calls failing
- Verify `REACT_APP_API_URL` is set correctly
- Check CORS settings in `main.py`
- Ensure backend is running and accessible

### Environment variables not loading
- Restart the application after adding variables
- Check variable names match exactly (case-sensitive)
- Verify variables are set in the deployment platform, not just `.env` file

## Post-Deployment

1. Test all features:
   - Chat functionality
   - Journal entries
   - Mood tracking
   - Content feed (YouTube, Spotify, News)
   - Spotify authentication

2. Monitor logs for errors

3. Set up monitoring/alerting if available

4. Consider setting up a custom domain

