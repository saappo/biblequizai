# Bible Quiz AI - Render Deployment Guide

## Overview
This guide will help you deploy the Bible Quiz AI application to Render.

## Prerequisites
- A Render account (free tier available)
- Your code pushed to a Git repository (GitHub, GitLab, etc.)

## Deployment Steps

### 1. Connect Your Repository
1. Log in to [Render](https://render.com)
2. Click "New +" and select "Web Service"
3. Connect your Git repository
4. Select the repository containing this Bible Quiz AI project

### 2. Configure the Service
- **Name**: `bible-quiz-ai` (or your preferred name)
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 1`
- **Plan**: Free (or choose a paid plan for better performance)

### 3. Environment Variables (Optional)
You can set these in the Render dashboard:
- `SECRET_KEY`: A secure secret key for Flask sessions
- `FLASK_ENV`: Set to `production` for production deployment

### 4. Deploy
1. Click "Create Web Service"
2. Render will automatically build and deploy your application
3. The deployment process typically takes 2-5 minutes

## Health Check
The application includes a health check endpoint at `/health` that Render will use to monitor the service.

## API Endpoints
- `/` - Main application page
- `/health` - Health check endpoint
- `/test` - Test API endpoint
- `/api/quiz/<difficulty>` - Quiz API endpoints (Easy, Medium, Hard)

## Troubleshooting
- Check the logs in the Render dashboard for any build or runtime errors
- Ensure all dependencies are listed in `requirements.txt`
- Verify the start command matches your application structure

## Features
- ✅ Flask web application
- ✅ Gunicorn WSGI server
- ✅ Health check endpoint
- ✅ Error handling
- ✅ Responsive UI with Bootstrap
- ✅ API endpoints for quiz functionality

## Support
If you encounter issues, check the Render documentation or contact Render support. 