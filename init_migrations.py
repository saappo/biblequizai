from app import create_app, db
from flask_migrate import Migrate, init, migrate

def init_migrations():
    app = create_app()
    migrate = Migrate(app, db)
    
    with app.app_context():
        # Initialize migrations
        init()
        # Create initial migration
        migrate()
        print("Migrations initialized successfully!")

if __name__ == '__main__':
    init_migrations() 