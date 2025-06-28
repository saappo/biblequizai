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

## Production Deployment

1. Set up environment variables:
   - Create a `.env` file based on `.env.example`
   - Update the `SECRET_KEY` with a secure value
   - Configure `DATABASE_URL` for your production database

2. Install Gunicorn:
   ```bash
   pip install gunicorn
   ```

3. Run with Gunicorn:
   ```bash
   gunicorn -c gunicorn_config.py "app:create_app('production')"
   ```

## Production Considerations

1. **Security**:
   - Use HTTPS in production
   - Keep your SECRET_KEY secure
   - Regularly update dependencies

2. **Database**:
   - Consider using a production-grade database (PostgreSQL recommended)
   - Set up regular backups
   - Monitor database performance

3. **Monitoring**:
   - Set up logging to a proper logging service
   - Monitor server resources
   - Set up error tracking

4. **Scaling**:
   - Use a load balancer for multiple instances
   - Consider using a CDN for static files
   - Implement caching where appropriate

## License

This project is licensed under the MIT License - see the LICENSE file for details. 