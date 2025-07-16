#!/usr/bin/env python3
"""
Debug script for chat endpoint
"""
import requests
import json

BACKEND_URL = "http://localhost:8000"

def test_simple_chat():
    """Test simple chat request"""
    print("🔍 Testing simple chat request...")
    
    payload = {
        "message": "Hello",
        "agent_type": "user"
    }
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json=payload,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Chat request successful!")
            print(f"Response: {data.get('response', 'No response')}")
        else:
            print(f"❌ Chat request failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_backend_health():
    """Test backend health"""
    print("🔍 Testing backend health...")
    
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        print(f"Health Status: {response.status_code}")
        print(f"Health Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health check error: {e}")

if __name__ == "__main__":
    test_backend_health()
    print("\n" + "="*50)
    test_simple_chat() 