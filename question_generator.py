import os
import logging
from datetime import datetime
from openai import OpenAI
from models import db, Question, Quiz
from flask import current_app
import json

# Configure logging
logging.basicConfig(
    filename='question_generation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def is_duplicate_question(text, options, correct_answer):
    """Check if a question already exists in the database"""
    question_hash = Question.generate_hash(text, options, correct_answer)
    return Question.query.filter_by(question_hash=question_hash).first() is not None

def generate_questions_for_difficulty(difficulty, num_questions=5, max_attempts=3):
    """
    Generate Bible questions for a specific difficulty level using ChatGPT.
    Includes duplicate checking and retry logic.
    """
    questions_generated = 0
    attempts = 0
    all_questions = []
    
    while questions_generated < num_questions and attempts < max_attempts:
        try:
            # Calculate how many more questions we need
            remaining = num_questions - questions_generated
            if remaining <= 0:
                break
                
            # Initialize OpenAI client with just the API key
            client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            
            prompt = f"""Generate {remaining} unique Bible quiz questions for the {difficulty} difficulty level.
            Each question must be challenging but fair, and include:
            - A clear, well-formulated question
            - Four possible answers (only one correct)
            - The correct answer
            - A category (Old Testament, New Testament, or General)
            - A brief explanation of the answer (optional)
            
            Format the response as a JSON array of objects with these fields:
            - text: the question
            - options: array of 4 possible answers
            - correct_answer: the correct answer (must match one of the options exactly)
            - category: Old Testament, New Testament, or General
            - explanation: brief explanation of the answer (optional)
            
            Make sure the questions are:
            1. Biblically accurate
            2. Appropriate for the {difficulty} difficulty level
            3. Clear and unambiguous
            4. Educational and meaningful
            5. Unique and not commonly known
            """
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a Bible quiz question generator that creates high-quality, educational questions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            try:
                new_questions = json.loads(response.choices[0].message.content)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {str(e)}")
                logger.error(f"Raw response: {response.choices[0].message.content}")
                attempts += 1
                continue
            
            # Filter out duplicates
            unique_questions = []
            for q in new_questions:
                if not is_duplicate_question(q['text'], q['options'], q['correct_answer']):
                    unique_questions.append(q)
                else:
                    logger.info(f"Duplicate question found and skipped: {q['text']}")
            
            all_questions.extend(unique_questions)
            questions_generated += len(unique_questions)
            
            if len(unique_questions) < len(new_questions):
                logger.info(f"Found {len(new_questions) - len(unique_questions)} duplicate questions")
            
            attempts += 1
            
        except Exception as e:
            logger.error(f"Error generating questions for {difficulty} (attempt {attempts}): {str(e)}")
            attempts += 1
    
    if questions_generated < num_questions:
        logger.warning(f"Could only generate {questions_generated} unique questions for {difficulty} after {attempts} attempts")
    
    return all_questions[:num_questions]  # Return only the requested number of questions

def store_questions(questions, difficulty):
    """
    Store generated questions in the database.
    """
    try:
        # Create a new quiz for today's questions
        quiz = Quiz(
            title=f"Daily Quiz - {datetime.utcnow().strftime('%Y-%m-%d')}",
            difficulty=difficulty,
            is_active=True
        )
        db.session.add(quiz)
        db.session.flush()  # Get the quiz ID
        
        # Add questions to the quiz
        for q in questions:
            question = Question(
                quiz_id=quiz.id,
                text=q['text'],
                options=q['options'],
                correct_answer=q['correct_answer'],
                category=q['category'],
                difficulty=difficulty,
                explanation=q.get('explanation', ''),
                question_hash=Question.generate_hash(q['text'], q['options'], q['correct_answer'])
            )
            db.session.add(question)
        
        db.session.commit()
        logger.info(f"Successfully stored {len(questions)} questions for {difficulty} difficulty")
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error storing questions for {difficulty}: {str(e)}")
        raise

def generate_daily_questions():
    """
    Generate and store questions for all difficulty levels.
    This function should be called daily via a scheduler.
    """
    try:
        difficulties = ['Easy', 'Medium', 'Hard']
        for difficulty in difficulties:
            questions = generate_questions_for_difficulty(difficulty)
            store_questions(questions, difficulty)
            
        logger.info("Successfully generated and stored all daily questions")
        return True
        
    except Exception as e:
        logger.error(f"Error in daily question generation: {str(e)}")
        return False

if __name__ == '__main__':
    # This allows the script to be run directly for testing
    from app import app
    with app.app_context():
        generate_daily_questions() 