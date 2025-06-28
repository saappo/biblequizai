"""
Simple storage solution using Vercel Blob storage
Included in Vercel Pro plan - no additional subscriptions needed!
"""

import os
import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional
import tempfile

try:
    from vercel_blob import put, get, del_
    BLOB_AVAILABLE = True
except ImportError:
    BLOB_AVAILABLE = False
    print("Vercel Blob not available, using local storage")

class VercelBlobStorage:
    """Simple storage using Vercel Blob storage"""
    
    def __init__(self):
        self.db_filename = 'biblequiz.db'
        self.blob_store_url = os.getenv('BLOB_READ_WRITE_TOKEN')
        
    def store_question(self, question_data: Dict) -> bool:
        """Store a question in the database"""
        try:
            # Create/update SQLite database
            conn = sqlite3.connect(self.db_filename)
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
            
            # Upload database to Vercel Blob (if available)
            if self.blob_store_url and BLOB_AVAILABLE:
                self._upload_to_blob()
            
            return True
            
        except Exception as e:
            print(f"Error storing question: {e}")
            return False
    
    def get_questions(self, difficulty: str = None, limit: int = 10) -> List[Dict]:
        """Get questions from the database"""
        try:
            # Download from Blob if available
            if self.blob_store_url and BLOB_AVAILABLE:
                self._download_from_blob()
            
            conn = sqlite3.connect(self.db_filename)
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
            
        except Exception as e:
            print(f"Error getting questions: {e}")
            return []
    
    def _upload_to_blob(self):
        """Upload database file to Vercel Blob storage"""
        try:
            if not BLOB_AVAILABLE:
                return
                
            # Read the database file
            with open(self.db_filename, 'rb') as f:
                db_data = f.read()
            
            # Upload to Vercel Blob
            blob = put(self.db_filename, db_data, {'access': 'public'})
            print(f"Database uploaded to Blob: {blob.url}")
            
        except Exception as e:
            print(f"Error uploading to blob: {e}")
    
    def _download_from_blob(self):
        """Download database file from Vercel Blob storage"""
        try:
            if not BLOB_AVAILABLE:
                return
                
            # Try to download from Blob
            try:
                blob_data = get(self.db_filename)
                with open(self.db_filename, 'wb') as f:
                    f.write(blob_data)
                print("Database downloaded from Blob")
            except:
                print("No existing database in Blob, using local file")
                
        except Exception as e:
            print(f"Error downloading from blob: {e}")

# Global storage instance
blob_storage = VercelBlobStorage() 