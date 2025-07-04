# Bible Quiz AI - Deployment Checklist

## ✅ Pre-Deployment Checklist

### Environment Setup
- [x] PostgreSQL dependency added (`psycopg2-binary`)
- [x] Environment variables configured in `render.yaml`
- [x] Production configuration updated
- [x] Database URL handling improved
- [x] Health check endpoint exists (`/health`)

### Application Files
- [x] `app.py` - Main application file
- [x] `requirements.txt` - All dependencies listed
- [x] `render.yaml` - Render configuration
- [x] `config.py` - Environment-specific configuration
- [x] `models.py` - Database models
- [x] `routes.py` - Application routes
- [x] `deploy.py` - Deployment helper script
- [x] `init_db.py` - Database initialization script

### Database
- [x] PostgreSQL support added
- [x] Database URL conversion for Render
- [x] Table creation on app startup
- [x] Migration support (if needed)

## 🚀 Render Deployment Steps

### 1. Prepare Your Repository
```bash
# Run deployment check
python deploy.py

# Commit all changes
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Create Render Web Service
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub/GitLab repository
4. Select the Bible Quiz AI repository

### 3. Configure the Service
- **Name**: `bible-quiz-ai`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 1`
- **Plan**: Free (or choose paid for better performance)

### 4. Set Environment Variables
In the Render dashboard, add these environment variables:
- `FLASK_ENV`: `production`
- `SECRET_KEY`: `your-secure-secret-key-here`
- `DATABASE_URL`: `postgresql://...` (Render will provide this)

### 5. Deploy
1. Click "Create Web Service"
2. Wait for build to complete (2-5 minutes)
3. Check logs for any errors

## 🔍 Post-Deployment Verification

### Health Check
- [ ] Visit `https://your-app.onrender.com/health`
- [ ] Should return: `{"status": "healthy", "message": "Bible Quiz AI is running on Render!"}`

### Application Features
- [ ] Home page loads: `https://your-app.onrender.com/`
- [ ] Quiz pages work: `https://your-app.onrender.com/public-quiz/Easy`
- [ ] Database connection works
- [ ] User registration/login works

### Common Issues & Solutions

#### Build Fails
- Check `requirements.txt` has all dependencies
- Verify Python version compatibility
- Check build logs for specific errors

#### Database Connection Fails
- Verify `DATABASE_URL` is set correctly
- Check if PostgreSQL service is running
- Ensure `psycopg2-binary` is in requirements

#### Health Check Fails
- Verify `/health` endpoint returns 200
- Check application logs for errors
- Ensure gunicorn is starting correctly

#### Application Errors
- Check Flask logs in Render dashboard
- Verify environment variables are set
- Test locally with production config

## 📞 Support
If deployment fails:
1. Check Render logs for specific error messages
2. Run `python deploy.py` locally to verify setup
3. Test with minimal configuration first
4. Contact Render support if needed

## 🎯 Success Criteria
- [ ] Application deploys without errors
- [ ] Health check endpoint returns 200
- [ ] Database tables are created
- [ ] Quiz functionality works
- [ ] User registration works
- [ ] Application is accessible via HTTPS 