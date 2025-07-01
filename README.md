# Bible Quiz Application

A Flask-based Bible quiz application with multiple difficulty levels and user interaction features.

## Features

- Multiple difficulty levels (Easy, Medium, Hard)
- Interactive quiz interface
- Score tracking
- Contact form
- Mobile-responsive design

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

## Railway Deployment

This application is configured for deployment on Railway.

### Quick Deploy

1. **Connect to Railway**:
   - Go to [Railway.app](https://railway.app)
   - Connect your GitHub repository
   - Railway will automatically detect the Python app

2. **Set Environment Variables**:
   - `SECRET_KEY`: A secure secret key for Flask
   - `DATABASE_URL`: Railway will provide this automatically
   - `FLASK_ENV`: Set to `production`

3. **Database Setup**:
   - Railway will automatically provision a PostgreSQL database
   - The app will run migrations on first deployment

### Manual Deployment

If you prefer to deploy manually:

1. Install Railway CLI:
   ```bash
   npm install -g @railway/cli
   ```

2. Login and deploy:
   ```bash
   railway login
   railway init
   railway up
   ```

3. Set environment variables:
   ```bash
   railway variables set SECRET_KEY=your-secret-key
   railway variables set FLASK_ENV=production
   ```

## Railway Production Features

1. **Automatic HTTPS**: Railway provides SSL certificates automatically
2. **PostgreSQL Database**: Railway automatically provisions and manages your database
3. **Background Jobs**: Your question generation cron job will run automatically
4. **Auto-scaling**: Railway handles scaling based on traffic
5. **Monitoring**: Built-in logging and monitoring through Railway dashboard

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

## License

This project is licensed under the MIT License - see the LICENSE file for details. 