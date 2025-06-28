"""
Test script to verify environment variables are working
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=== Environment Variables Test ===")
print(f"BLOB_READ_WRITE_TOKEN: {'✅ Set' if os.getenv('BLOB_READ_WRITE_TOKEN') else '❌ Not set'}")
print(f"OPENAI_API_KEY: {'✅ Set' if os.getenv('OPENAI_API_KEY') else '❌ Not set'}")
print(f"SECRET_KEY: {'✅ Set' if os.getenv('SECRET_KEY') else '❌ Not set'}")

print("\n=== Testing Blob Storage ===")
try:
    from vercel_blob_storage import blob_storage
    print("✅ Blob storage module imported successfully")
    
    # Test storing a question
    test_question = {
        'question': 'Test question?',
        'choices': ['A', 'B', 'C'],
        'correct_index': 0,
        'verse': 'Test verse',
        'difficulty': 'Easy'
    }
    
    result = blob_storage.store_question(test_question)
    print(f"✅ Question storage test: {'Success' if result else 'Failed'}")
    
    # Test getting questions
    questions = blob_storage.get_questions(limit=5)
    print(f"✅ Question retrieval test: Found {len(questions)} questions")
    
except Exception as e:
    print(f"❌ Error testing blob storage: {e}")

print("\n=== Test Complete ===") 