#!/usr/bin/env python3
"""
Script to add questions to the Bible Quiz database.
This script automatically finds the next available day and adds questions.
"""

import os
import sys
import json
from datetime import datetime

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, Question

def add_question(question_data):
    """
    Add a single question to the database.
    
    Args:
        question_data (dict): Dictionary containing question information
            Required keys: text, options, correct_answer, difficulty, category, question_type
            Optional keys: explanation
    """
    app = create_app()
    
    with app.app_context():
        try:
            # Get the next available day
            next_day = Question.get_next_day()
            
            # Create the question
            question = Question(
                day=next_day,
                question_type=question_data['question_type'],
                text=question_data['text'],
                options=question_data['options'],
                correct_answer=question_data['correct_answer'],
                explanation=question_data.get('explanation', ''),
                difficulty=question_data['difficulty'],
                category=question_data['category'],
                question_hash=Question.generate_hash(
                    question_data['text'], 
                    question_data['options'], 
                    question_data['correct_answer']
                )
            )
            
            # Check for duplicates
            existing = Question.query.filter_by(question_hash=question.question_hash).first()
            if existing:
                print(f"Question already exists (duplicate hash): {question_data['text'][:50]}...")
                return False
            
            # Add to database
            db.session.add(question)
            db.session.commit()
            
            print(f"Added question for Day {next_day}: {question_data['text'][:50]}...")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"Error adding question: {str(e)}")
            return False

def add_questions_from_file(filename):
    """
    Add multiple questions from a JSON file.
    
    Args:
        filename (str): Path to JSON file containing questions
    """
    try:
        with open(filename, 'r') as f:
            questions = json.load(f)
        
        if isinstance(questions, list):
            # List of questions
            for question in questions:
                add_question(question)
        elif isinstance(questions, dict):
            # Single question
            add_question(questions)
        else:
            print("Invalid JSON format. Expected list of questions or single question object.")
            
    except FileNotFoundError:
        print(f"File not found: {filename}")
    except json.JSONDecodeError:
        print(f"Invalid JSON in file: {filename}")
    except Exception as e:
        print(f"Error reading file: {str(e)}")

def interactive_add_question():
    """
    Interactive mode to add questions one by one.
    """
    print("=== Interactive Question Addition ===")
    print("Enter question details (press Enter to skip optional fields):")
    
    # Get question details
    text = input("Question text: ").strip()
    if not text:
        print("Question text is required!")
        return
    
    # Get options
    options = []
    print("Enter 4 options:")
    for i in range(4):
        option = input(f"Option {i+1}: ").strip()
        if option:
            options.append(option)
    
    if len(options) != 4:
        print("Exactly 4 options are required!")
        return
    
    correct_answer = input("Correct answer: ").strip()
    if not correct_answer:
        print("Correct answer is required!")
        return
    
    if correct_answer not in options:
        print("Correct answer must be one of the options!")
        return
    
    difficulty = input("Difficulty (Easy/Medium/Hard): ").strip().title()
    if difficulty not in ['Easy', 'Medium', 'Hard']:
        print("Difficulty must be Easy, Medium, or Hard!")
        return
    
    category = input("Category (Old Testament/New Testament): ").strip()
    if not category:
        category = "General"
    
    question_type = input("Question type (Factual/Fill in the Blank/etc): ").strip()
    if not question_type:
        question_type = "Factual"
    
    explanation = input("Explanation (optional): ").strip()
    
    # Create question data
    question_data = {
        'text': text,
        'options': options,
        'correct_answer': correct_answer,
        'difficulty': difficulty,
        'category': category,
        'question_type': question_type,
        'explanation': explanation
    }
    
    # Add the question
    if add_question(question_data):
        print("Question added successfully!")
    else:
        print("Failed to add question.")

def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python add_questions.py interactive")
        print("  python add_questions.py file <filename>")
        print("  python add_questions.py question <json_string>")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'interactive':
        interactive_add_question()
    
    elif command == 'file':
        if len(sys.argv) < 3:
            print("Please provide a filename: python add_questions.py file <filename>")
            return
        filename = sys.argv[2]
        add_questions_from_file(filename)
    
    elif command == 'question':
        if len(sys.argv) < 3:
            print("Please provide question JSON: python add_questions.py question <json_string>")
            return
        try:
            question_data = json.loads(sys.argv[2])
            add_question(question_data)
        except json.JSONDecodeError:
            print("Invalid JSON string")
    
    else:
        print(f"Unknown command: {command}")
        print("Available commands: interactive, file, question")

if __name__ == "__main__":
    main() 