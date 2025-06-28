from app import create_app, db
from flask_migrate import upgrade

def init_database():
    app = create_app()
    with app.app_context():
        # Create all tables
        db.create_all()
        # Run any pending migrations
        upgrade()
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_database() 