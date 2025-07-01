"""
Simple storage solution using file-based storage
No external subscriptions needed!
"""

import os
import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional

class SimpleStorage:
    """Simple storage using file-based storage"""
    
    def __init__(self):
        self.use_kv = os.getenv('KV_URL') is not None
        self.db_file = 'biblequiz.db'
        
    def store_question(self, question_data: Dict) -> bool:
        """Store a question"""
        try:
            if self.use_kv:
                return self._store_in_kv(question_data)
            else:
                return self._store_in_sqlite(question_data)
        except Exception as e:
            print(f"Error storing question: {e}")
            return False
    
    def get_questions(self, difficulty: str = None, limit: int = 10) -> List[Dict]:
        """Get questions"""
        try:
            if self.use_kv:
                return self._get_from_kv(difficulty, limit)
            else:
                return self._get_from_sqlite(difficulty, limit)
        except Exception as e:
            print(f"Error getting questions: {e}")
            return []
    
    def _store_in_kv(self, question_data: Dict) -> bool:
        """Store in file system"""
        # This uses file-based storage
        # For now, we'll use a simple file-based approach
        return self._store_in_sqlite(question_data)
    
    def _store_in_sqlite(self, question_data: Dict) -> bool:
        """Store in SQLite file"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Create table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT,
                choices TEXT,
                correct_index INTEGER,
                verse TEXT,
                difficulty TEXT,
                created_at TEXT
            )
        """)
        
        # Insert question
        cursor.execute("""
            INSERT INTO questions (question, choices, correct_index, verse, difficulty, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            question_data['question'],
            json.dumps(question_data['choices']),
            question_data['correct_index'],
            question_data['verse'],
            question_data.get('difficulty', 'Easy'),
            datetime.utcnow().isoformat()
        ))
        
        conn.commit()
        conn.close()
        return True
    
    def _get_from_kv(self, difficulty: str = None, limit: int = 10) -> List[Dict]:
        """Get from file system"""
        # This uses file-based storage
        # For now, we'll use a simple file-based approach
        return self._get_from_sqlite(difficulty, limit)
    
    def _get_from_sqlite(self, difficulty: str = None, limit: int = 10) -> List[Dict]:
        """Get from SQLite file"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        if difficulty:
            cursor.execute("""
                SELECT question, choices, correct_index, verse, difficulty, created_at
                FROM questions 
                WHERE difficulty = ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (difficulty, limit))
        else:
            cursor.execute("""
                SELECT question, choices, correct_index, verse, difficulty, created_at
                FROM questions 
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,))
        
        questions = []
        for row in cursor.fetchall():
            questions.append({
                'question': row[0],
                'choices': json.loads(row[1]),
                'correct_index': row[2],
                'verse': row[3],
                'difficulty': row[4],
                'created_at': row[5]
            })
        
        conn.close()
        return questions

# Global storage instance
storage = SimpleStorage() 