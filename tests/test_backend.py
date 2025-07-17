#!/usr/bin/env python3
"""
Backend integration tests for the ETA Agent System
"""
import pytest
import requests
import json
import asyncio
from typing import Dict, Any
import os

# Test configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
TEST_TIMEOUT = 30

class TestBackendAPI:
    """Test suite for backend API endpoints"""
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = requests.get(f"{BACKEND_URL}/", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "ETA Agent System" in data["message"]
    
    def test_api_status_endpoint(self):
        """Test API status endpoint"""
        response = requests.get(f"{BACKEND_URL}/api/status", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert "api" in data
        assert "version" in data
        assert "database" in data
    
    def test_chat_endpoint_user_agent(self):
        """Test chat endpoint with user agent"""
        payload = {
            "message": "Hello, I need help with a delivery",
            "agent_type": "user"
        }
        
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json=payload,
            timeout=TEST_TIMEOUT
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "conversation_id" in data
        assert "system_info" in data
        assert len(data["response"]) > 0
    
    def test_chat_endpoint_driver_agent(self):
        """Test chat endpoint with driver agent"""
        payload = {
            "message": "There's traffic on my route",
            "agent_type": "driver"
        }
        
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json=payload,
            timeout=TEST_TIMEOUT
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "conversation_id" in data
        assert "system_info" in data
        assert len(data["response"]) > 0
    
    def test_chat_endpoint_invalid_agent(self):
        """Test chat endpoint with invalid agent type"""
        payload = {
            "message": "Hello",
            "agent_type": "invalid_agent"
        }
        
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json=payload,
            timeout=TEST_TIMEOUT
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "Invalid agent type" in data["detail"]
    
    def test_chat_endpoint_empty_message(self):
        """Test chat endpoint with empty message"""
        payload = {
            "message": "",
            "agent_type": "user"
        }
        
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json=payload,
            timeout=TEST_TIMEOUT
        )
        
        # Should handle empty messages gracefully
        assert response.status_code in [200, 400]
    
    def test_conversation_persistence(self):
        """Test conversation ID persistence"""
        # First message
        payload1 = {
            "message": "Start a conversation",
            "agent_type": "user"
        }
        
        response1 = requests.post(
            f"{BACKEND_URL}/chat",
            json=payload1,
            timeout=TEST_TIMEOUT
        )
        
        assert response1.status_code == 200
        data1 = response1.json()
        conversation_id = data1["conversation_id"]
        assert conversation_id is not None
        
        # Second message with same conversation ID
        payload2 = {
            "message": "Continue the conversation",
            "agent_type": "user",
            "conversation_id": conversation_id
        }
        
        response2 = requests.post(
            f"{BACKEND_URL}/chat",
            json=payload2,
            timeout=TEST_TIMEOUT
        )
        
        assert response2.status_code == 200
        data2 = response2.json()
        assert data2["conversation_id"] == conversation_id

class TestExternalAPIs:
    """Test suite for external API integrations"""
    
    def test_weather_api(self):
        """Test weather API endpoint"""
        response = requests.get(f"{BACKEND_URL}/weather/test", timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
    
    def test_traffic_api(self):
        """Test traffic API endpoint"""
        response = requests.get(f"{BACKEND_URL}/traffic/test", timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert "status" in data

class TestAgentServices:
    """Test suite for agent service functionality"""
    
    def test_user_agent_capabilities(self):
        """Test user agent specific capabilities"""
        test_messages = [
            "Analyze this delivery data",
            "Provide ETA recommendations",
            "Handle customer complaint",
            "Generate delivery report"
        ]
        
        for message in test_messages:
            payload = {
                "message": message,
                "agent_type": "user"
            }
            
            response = requests.post(
                f"{BACKEND_URL}/chat",
                json=payload,
                timeout=TEST_TIMEOUT
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "response" in data
            assert len(data["response"]) > 0
    
    def test_driver_agent_capabilities(self):
        """Test driver agent specific capabilities"""
        test_messages = [
            "Report traffic incident",
            "Request route optimization",
            "Update delivery status",
            "Check weather conditions"
        ]
        
        for message in test_messages:
            payload = {
                "message": message,
                "agent_type": "driver"
            }
            
            response = requests.post(
                f"{BACKEND_URL}/chat",
                json=payload,
                timeout=TEST_TIMEOUT
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "response" in data
            assert len(data["response"]) > 0

class TestErrorHandling:
    """Test suite for error handling"""
    
    def test_malformed_request(self):
        """Test handling of malformed requests"""
        # Missing required fields
        payload = {"agent_type": "user"}
        
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json=payload,
            timeout=TEST_TIMEOUT
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_large_message(self):
        """Test handling of very large messages"""
        large_message = "A" * 10000  # 10KB message
        
        payload = {
            "message": large_message,
            "agent_type": "user"
        }
        
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json=payload,
            timeout=TEST_TIMEOUT
        )
        
        # Should handle large messages gracefully
        assert response.status_code in [200, 400, 413]

class TestPerformance:
    """Test suite for performance"""
    
    def test_response_time(self):
        """Test response time for chat requests"""
        payload = {
            "message": "Quick test message",
            "agent_type": "user"
        }
        
        import time
        start_time = time.time()
        
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json=payload,
            timeout=TEST_TIMEOUT
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert response_time < 30  # Should respond within 30 seconds
    
    def test_concurrent_requests(self):
        """Test handling of concurrent requests"""
        import threading
        import time
        
        results = []
        errors = []
        
        def make_request():
            try:
                payload = {
                    "message": f"Concurrent test {threading.current_thread().name}",
                    "agent_type": "user"
                }
                
                response = requests.post(
                    f"{BACKEND_URL}/chat",
                    json=payload,
                    timeout=TEST_TIMEOUT
                )
                
                results.append(response.status_code == 200)
            except Exception as e:
                errors.append(str(e))
        
        # Create 5 concurrent requests
        threads = []
        for i in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Check results
        assert len(errors) == 0, f"Errors occurred: {errors}"
        assert len(results) == 5
        assert all(results), "Not all requests were successful"

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"]) 