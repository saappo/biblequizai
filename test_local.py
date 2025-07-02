#!/usr/bin/env python3
"""
Test script to verify the Bible Quiz AI application works locally
"""

import requests
import time
import sys

def test_local_app():
    """Test the local Flask application"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Bible Quiz AI Application...")
    print("=" * 50)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test main page
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Main page loaded successfully")
        else:
            print(f"❌ Main page failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Main page failed: {e}")
        return False
    
    # Test API endpoints
    difficulties = ["Easy", "Medium", "Hard"]
    for difficulty in difficulties:
        try:
            response = requests.get(f"{base_url}/api/quiz/{difficulty}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {difficulty} quiz API working")
            else:
                print(f"❌ {difficulty} quiz API failed: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {difficulty} quiz API failed: {e}")
    
    # Test 404 handling
    try:
        response = requests.get(f"{base_url}/nonexistent", timeout=5)
        if response.status_code == 404:
            print("✅ 404 error handling working")
        else:
            print(f"❌ 404 error handling failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ 404 error handling failed: {e}")
    
    print("=" * 50)
    print("🎉 All tests completed!")
    return True

if __name__ == "__main__":
    print("Starting local test...")
    print("Make sure your Flask app is running on http://localhost:5000")
    print("Run: python app.py")
    print()
    
    # Give user time to start the app
    print("Waiting 3 seconds for app to start...")
    time.sleep(3)
    
    success = test_local_app()
    sys.exit(0 if success else 1) 