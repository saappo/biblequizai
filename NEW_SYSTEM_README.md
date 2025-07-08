# Bible Quiz AI - New Day-Based Question System

## Overview

The Bible Quiz AI has been updated to use a new day-based question system that eliminates the need for ChatGPT-generated questions. Instead, questions are now stored in a database with day numbers and question types, allowing for better organization and control.

## Key Changes

### 1. Database Schema Updates

The `questions` table now includes:
- `day` (Integer): Day number (1, 2, 3, etc.) for organizing questions
- `question_type` (String): Type of question (Factual, Fill in the Blank, True/False, etc.)
- Removed `quiz_id` and `quizzes` table (no longer needed)

The `users` table now includes:
- `is_admin` (Boolean): Flag to identify admin users

### 2. Question Types

The system now supports multiple question types:
- **Factual**: Standard multiple choice questions
- **Fill in the Blank**: Questions with blanks to fill
- **True/False**: True or false questions
- **Multiple Choice**: Traditional multiple choice
- **Matching**: Matching questions

### 3. Day-Based Organization

- Questions are organized by day numbers
- Each day can have multiple questions across different difficulties
- The system automatically finds the next available day when adding questions
- Users get questions from the most recent day available

## Setup Instructions

### 1. Run Database Migration

```bash
python run_migration.py
```

This script will:
- Add the new columns to the database
- Set default values for existing questions
- Create an admin user (admin@biblequiz.com / admin123)

### 2. Add Questions

#### Option A: Using the Admin Interface
1. Go to `/admin/login`
2. Login with admin credentials
3. Use the dashboard to add questions directly

#### Option B: Using the Command Line Script

**Interactive Mode:**
```bash
python add_questions.py interactive
```

**From JSON File:**
```bash
python add_questions.py file sample_questions.json
```

**Single Question:**
```bash
python add_questions.py question '{"text": "Who built the ark?", "options": ["Noah", "Moses", "Abraham", "David"], "correct_answer": "Noah", "difficulty": "Easy", "category": "Old Testament", "question_type": "Factual"}'
```

### 3. Question Format

Questions should be in JSON format with these fields:

```json
{
  "text": "Question text here",
  "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
  "correct_answer": "Option 1",
  "difficulty": "Easy|Medium|Hard",
  "category": "Old Testament|New Testament|General",
  "question_type": "Factual|Fill in the Blank|True/False|Multiple Choice|Matching",
  "explanation": "Optional explanation for the answer"
}
```

## How It Works

### Question Selection
1. When a user starts a quiz, the system looks for questions for the most recent day
2. If no questions exist for that difficulty, it falls back to any available questions
3. If no questions exist at all, it uses the hardcoded sample questions

### Day Management
- The `Question.get_next_day()` method automatically finds the next available day
- Questions are added to the next day sequentially
- You can manually specify days if needed

### Admin Features
- **Dashboard**: View statistics and recent questions
- **Add Questions**: Form-based question addition
- **Statistics**: See total questions, days, and users
- **Recent Questions**: View the last 10 questions added

## File Structure

```
├── models.py                    # Updated database models
├── routes.py                    # Updated routes with admin functionality
├── add_questions.py            # Script to add questions
├── run_migration.py            # Database migration script
├── sample_questions.json       # Example questions
├── templates/
│   ├── admin/
│   │   ├── login.html          # Admin login page
│   │   └── dashboard.html      # Admin dashboard
└── migrations/
    └── versions/
        └── add_day_and_type_columns.py  # Database migration
```

## Benefits

1. **No ChatGPT Dependency**: No more daily API calls or costs
2. **Better Organization**: Questions organized by days
3. **Question Types**: Support for different question formats
4. **Admin Control**: Easy interface for managing questions
5. **Scalability**: Easy to add large batches of questions
6. **Consistency**: Same questions for all users on the same day

## Usage Examples

### Adding Questions via Script

```bash
# Add questions from a file
python add_questions.py file my_questions.json

# Add questions interactively
python add_questions.py interactive

# Add a single question
python add_questions.py question '{"text": "Test question?", "options": ["A", "B", "C", "D"], "correct_answer": "A", "difficulty": "Easy", "category": "General", "question_type": "Factual"}'
```

### Admin Interface

1. Navigate to `/admin/login`
2. Login with admin credentials
3. Use the dashboard to:
   - View statistics
   - Add new questions
   - See recent questions
   - Manage the system

## Migration Notes

- Existing questions will be assigned to Day 1 with "Factual" type
- The migration is safe and can be run multiple times
- No data will be lost during migration
- The system maintains backward compatibility

## Security Notes

- Change the default admin password in production
- The admin interface is protected by login_required decorator
- Only users with is_admin=True can access admin features

## Future Enhancements

- Question editing and deletion in admin interface
- Bulk question import from CSV/Excel
- Question categories and tags
- User progress tracking by day
- Question difficulty adjustment based on user performance 