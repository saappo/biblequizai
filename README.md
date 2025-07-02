# Bible Quiz AI

A Flask-based Bible quiz application with multiple difficulty levels and user interaction features, deployed on Render.

## Features

- Multiple difficulty levels (Easy, Medium, Hard)
- Interactive quiz interface
- Score tracking
- Contact form
- Mobile-responsive design
- AI-powered question generation
- RESTful API endpoints

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Development

To run the application in development mode:
```bash
python app.py
```

## Render Deployment

This application is configured for deployment on Render.

### Quick Deploy

1. **Connect to Render**:
   - Go to [Render.com](https://render.com)
   - Sign up/Login and click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will automatically detect the Python app

2. **Configure the Service**:
   - **Name**: `bible-quiz-ai` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 1`
   - **Plan**: Free (or choose a paid plan for better performance)

3. **Set Environment Variables** (Optional):
   - `SECRET_KEY`: A secure secret key for Flask
   - `FLASK_ENV`: Set to `production`

4. **Deploy**:
   - Click "Create Web Service"
   - Render will automatically build and deploy your application

### Manual Deployment

If you prefer to deploy manually:

1. Install Render CLI:
   ```bash
   npm install -g @render/cli
   ```

2. Login and deploy:
   ```bash
   render login
   render deploy
   ```

## Render Production Features

1. **Automatic HTTPS**: Render provides SSL certificates automatically
2. **Auto-scaling**: Render handles scaling based on traffic
3. **Health Checks**: Built-in health monitoring at `/health` endpoint
4. **Logging**: Comprehensive logging through Render dashboard
5. **Custom Domains**: Easy custom domain setup
6. **Environment Variables**: Secure environment variable management

## API Endpoints

- `/` - Main application page
- `/health` - Health check endpoint
- `/test` - Test API endpoint
- `/api/quiz/<difficulty>` - Quiz API endpoints (Easy, Medium, Hard)

## Local Development

To run the application locally:

1. Set up environment variables:
   ```bash
   cp env.example .env
   # Edit .env with your local settings
   ```

2. Run the application:
   ```bash
   python app.py
   ```

3. For production-like testing:
   ```bash
   gunicorn app:app --bind 0.0.0.0:5000
   ```

## Project Structure

```
BibleQuizAI/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── render.yaml           # Render deployment configuration
├── Procfile             # Process file for web servers
├── templates/           # HTML templates
│   └── index.html      # Main application page
├── static/             # Static files (CSS, JS, images)
└── api/               # API-specific files
    └── index.py       # API handler
```

## Troubleshooting

- Check the logs in the Render dashboard for any build or runtime errors
- Ensure all dependencies are listed in `requirements.txt`
- Verify the start command matches your application structure
- The health check endpoint at `/health` should return a 200 status

## License

This project is licensed under the MIT License - see the LICENSE file for details. 