from app import app, db
from question_generator import generate_daily_questions
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    with app.app_context():
        # Ensure database is initialized
        db.create_all()
        logger.info("Database initialized")
        
        logger.info("Starting question generation test...")
        try:
            result = generate_daily_questions()
            if result:
                logger.info("Successfully generated questions!")
            else:
                logger.error("Failed to generate questions")
        except Exception as e:
            logger.error(f"Error during question generation: {str(e)}")
            logger.exception("Full traceback:") 