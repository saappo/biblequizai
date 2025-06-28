from app import create_app, db
from models import User, Question, UserResponse, Suggestion

def create_database():
    app = create_app()
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")

if __name__ == '__main__':
    create_database() 