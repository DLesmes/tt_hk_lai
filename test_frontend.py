#!/usr/bin/env python3
"""
Test script for the ETA Agent System Frontend
"""
import requests
import json
import time
from datetime import datetime

# Configuration
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:8501"

def test_backend_health():
    """Test backend health endpoint"""
    print("🔍 Testing backend health...")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is healthy")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend connection failed: {e}")
        return False

def test_chat_endpoint():
    """Test chat endpoint"""
    print("\n💬 Testing chat endpoint...")
    
    test_messages = [
        {
            "message": "Hello, I need help with a delivery delay",
            "agent_type": "user",
            "expected_keywords": ["delay", "delivery", "help"]
        },
        {
            "message": "There's heavy traffic on the highway",
            "agent_type": "driver",
            "expected_keywords": ["traffic", "route", "weather"]
        }
    ]
    
    for i, test_case in enumerate(test_messages, 1):
        print(f"   Test {i}: {test_case['message']}")
        
        try:
            payload = {
                "message": test_case["message"],
                "agent_type": test_case["agent_type"]
            }
            
            response = requests.post(
                f"{BACKEND_URL}/chat",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Response received")
                print(f"   📝 Response: {data.get('response', 'No response')[:100]}...")
                print(f"   🆔 Conversation ID: {data.get('conversation_id', 'None')}")
                
                # Check for expected keywords in response
                response_text = data.get('response', '').lower()
                found_keywords = [kw for kw in test_case['expected_keywords'] if kw in response_text]
                if found_keywords:
                    print(f"   🎯 Found expected keywords: {found_keywords}")
                else:
                    print(f"   ⚠️  No expected keywords found")
                
            else:
                print(f"   ❌ Chat request failed: {response.status_code}")
                print(f"   📄 Error: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Chat request error: {e}")
        
        time.sleep(1)  # Small delay between requests

def test_agent_services():
    """Test individual agent services"""
    print("\n🤖 Testing agent services...")
    
    # Test user agent
    print("   Testing User Agent...")
    try:
        payload = {
            "message": "Analyze this delivery data and provide recommendations",
            "agent_type": "user"
        }
        
        response = requests.post(f"{BACKEND_URL}/chat", json=payload, timeout=30)
        if response.status_code == 200:
            print("   ✅ User agent responding")
        else:
            print(f"   ❌ User agent failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ User agent error: {e}")
    
    # Test driver agent
    print("   Testing Driver Agent...")
    try:
        payload = {
            "message": "Report traffic incident on route",
            "agent_type": "driver"
        }
        
        response = requests.post(f"{BACKEND_URL}/chat", json=payload, timeout=30)
        if response.status_code == 200:
            print("   ✅ Driver agent responding")
        else:
            print(f"   ❌ Driver agent failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Driver agent error: {e}")

def test_external_apis():
    """Test external API integrations"""
    print("\n🌐 Testing external API integrations...")
    
    # Test weather API
    print("   Testing Weather API...")
    try:
        response = requests.get(f"{BACKEND_URL}/weather/test", timeout=10)
        if response.status_code == 200:
            print("   ✅ Weather API working")
        else:
            print(f"   ⚠️  Weather API test failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Weather API error: {e}")
    
    # Test traffic API
    print("   Testing Traffic API...")
    try:
        response = requests.get(f"{BACKEND_URL}/traffic/test", timeout=10)
        if response.status_code == 200:
            print("   ✅ Traffic API working")
        else:
            print(f"   ⚠️  Traffic API test failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Traffic API error: {e}")

def test_frontend_components():
    """Test frontend component imports"""
    print("\n🎨 Testing frontend components...")
    
    try:
        # Test config import
        from frontend.config import PAGE_TITLE, AGENT_TYPES, CUSTOM_CSS
        print("   ✅ Config module imported successfully")
        print(f"   📝 Page title: {PAGE_TITLE}")
        print(f"   🤖 Agent types: {AGENT_TYPES}")
        
        # Test utils import
        from frontend.utils import APIUtils, DataUtils, UIUtils, SessionUtils
        print("   ✅ Utils modules imported successfully")
        
        # Test components import
        from frontend.components import (
            HeaderComponent, SidebarComponent, MetricsComponent,
            ChatComponent, AgentInfoComponent, ErrorComponent
        )
        print("   ✅ Component modules imported successfully")
        
        # Test main app import
        from frontend.app import ETAAgentFrontend
        print("   ✅ Main app module imported successfully")
        
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
    except Exception as e:
        print(f"   ❌ Component test error: {e}")

def main():
    """Main test runner"""
    print("🚚 ETA Agent System - Frontend Test Suite")
    print("=" * 50)
    
    # Test backend connectivity
    if not test_backend_health():
        print("\n❌ Backend is not available. Please start the backend first.")
        print("   Run: docker-compose up backend")
        return
    
    # Test chat functionality
    test_chat_endpoint()
    
    # Test agent services
    test_agent_services()
    
    # Test external APIs
    test_external_apis()
    
    # Test frontend components
    test_frontend_components()
    
    print("\n" + "=" * 50)
    print("✅ Frontend test suite completed!")
    print("\n📋 Next steps:")
    print("   1. Start the frontend: streamlit run frontend/app.py")
    print("   2. Open browser to: http://localhost:8501")
    print("   3. Test the chat interface with different agent types")
    print("   4. Verify system status and metrics display")

if __name__ == "__main__":
    main() 