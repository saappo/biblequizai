import sqlite3
import json

def setup_database():
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    
    # Create questions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        choices TEXT NOT NULL,
        correct_index INTEGER NOT NULL,
        verse TEXT NOT NULL,
        difficulty TEXT NOT NULL
    )
    ''')
    
    # Sample questions (you can replace these with your own)
    sample_questions = [
        {
            'question': 'Who built the ark according to the Bible?',
            'choices': json.dumps(['Noah', 'Moses', 'Abraham', 'David']),
            'correct_index': 0,
            'verse': 'Genesis 6:14',
            'difficulty': 'Easy'
        },
        {
            'question': 'How many days and nights did it rain during the flood?',
            'choices': json.dumps(['30', '40', '50', '60']),
            'correct_index': 1,
            'verse': 'Genesis 7:12',
            'difficulty': 'Medium'
        },
        {
            'question': 'What was the first miracle Jesus performed?',
            'choices': json.dumps(['Walking on water', 'Feeding the 5000', 'Turning water into wine', 'Raising Lazarus']),
            'correct_index': 2,
            'verse': 'John 2:1-11',
            'difficulty': 'Hard'
        }
    ]
    
    # Insert sample questions
    cursor.executemany('''
    INSERT INTO questions (question, choices, correct_index, verse, difficulty)
    VALUES (?, ?, ?, ?, ?)
    ''', [(q['question'], q['choices'], q['correct_index'], q['verse'], q['difficulty']) 
          for q in sample_questions])
    
    conn.commit()
    conn.close()
    print("Database setup complete!")

if __name__ == "__main__":
    setup_database() 