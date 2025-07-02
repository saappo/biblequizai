# Render Deployment Checklist

## Pre-Deployment
- [ ] Code is committed to Git repository
- [ ] All dependencies are in `requirements.txt`
- [ ] Application runs locally without errors
- [ ] Health check endpoint `/health` returns 200
- [ ] Environment variables are documented

## Render Setup
- [ ] Create Render account
- [ ] Connect Git repository
- [ ] Create new Web Service
- [ ] Configure build settings:
  - [ ] Environment: Python 3
  - [ ] Build Command: `pip install -r requirements.txt`
  - [ ] Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 1`
- [ ] Set environment variables (if needed):
  - [ ] `SECRET_KEY`
  - [ ] `FLASK_ENV=production`

## Post-Deployment Verification
- [ ] Application builds successfully
- [ ] Health check passes
- [ ] Main page loads correctly
- [ ] API endpoints respond properly
- [ ] Custom domain works (if configured)
- [ ] HTTPS is working
- [ ] Logs show no errors

## Monitoring
- [ ] Set up health check monitoring
- [ ] Configure log monitoring
- [ ] Set up alerts for downtime
- [ ] Monitor resource usage

## Troubleshooting Common Issues
- [ ] Build fails: Check `requirements.txt` and Python version
- [ ] App crashes: Check logs for error messages
- [ ] Health check fails: Verify `/health` endpoint returns 200
- [ ] Slow response: Consider upgrading to paid plan
- [ ] Environment variables not working: Check variable names and values

## Files to Verify
- [ ] `app.py` - Main Flask application
- [ ] `requirements.txt` - Python dependencies
- [ ] `render.yaml` - Render configuration
- [ ] `Procfile` - Process configuration
- [ ] `templates/index.html` - Main page template
- [ ] `README.md` - Updated documentation 