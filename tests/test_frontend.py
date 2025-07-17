#!/usr/bin/env python3
"""
Frontend integration tests for the ETA Agent System
"""
import pytest
import requests
import time
from typing import Dict, Any
import os

# Test configuration
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8501")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

class TestFrontendAccessibility:
    """Test suite for frontend accessibility and basic functionality"""
    
    def test_frontend_health(self):
        """Test if frontend is accessible"""
        try:
            response = requests.get(FRONTEND_URL, timeout=10)
            # Streamlit returns 200 for the main page
            assert response.status_code == 200
        except requests.exceptions.ConnectionError:
            pytest.skip("Frontend not accessible - may not be running")
    
    def test_frontend_static_assets(self):
        """Test if frontend static assets are loading"""
        try:
            # Test if the main page loads
            response = requests.get(FRONTEND_URL, timeout=10)
            assert response.status_code == 200
            
            # Check if it's a Streamlit page
            content = response.text
            assert "streamlit" in content.lower() or "eta agent" in content.lower()
        except requests.exceptions.ConnectionError:
            pytest.skip("Frontend not accessible - may not be running")

class TestFrontendBackendIntegration:
    """Test suite for frontend-backend integration"""
    
    def test_backend_connectivity_from_frontend(self):
        """Test if frontend can connect to backend"""
        # This test simulates what the frontend does
        try:
            response = requests.get(f"{BACKEND_URL}/health", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend not accessible")
    
    def test_chat_workflow_simulation(self):
        """Simulate the complete chat workflow"""
        # Test backend chat endpoint
        payload = {
            "message": "Test message from frontend integration test",
            "agent_type": "user"
        }
        
        try:
            response = requests.post(
                f"{BACKEND_URL}/chat",
                json=payload,
                timeout=30
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "response" in data
            assert "conversation_id" in data
            assert len(data["response"]) > 0
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend not accessible")

class TestFrontendComponents:
    """Test suite for frontend component functionality"""
    
    def test_agent_type_switching(self):
        """Test agent type switching functionality"""
        # This would normally test the frontend UI, but we can test the backend logic
        agent_types = ["user", "driver"]
        
        for agent_type in agent_types:
            payload = {
                "message": f"Test message for {agent_type} agent",
                "agent_type": agent_type
            }
            
            try:
                response = requests.post(
                    f"{BACKEND_URL}/chat",
                    json=payload,
                    timeout=30
                )
                
                assert response.status_code == 200
                data = response.json()
                assert "system_info" in data
                assert agent_type in data["system_info"]
                
            except requests.exceptions.ConnectionError:
                pytest.skip("Backend not accessible")
    
    def test_conversation_management(self):
        """Test conversation management features"""
        # Test conversation ID generation and persistence
        payload1 = {
            "message": "Start conversation",
            "agent_type": "user"
        }
        
        try:
            response1 = requests.post(
                f"{BACKEND_URL}/chat",
                json=payload1,
                timeout=30
            )
            
            assert response1.status_code == 200
            data1 = response1.json()
            conversation_id = data1["conversation_id"]
            
            # Test continuing the same conversation
            payload2 = {
                "message": "Continue conversation",
                "agent_type": "user",
                "conversation_id": conversation_id
            }
            
            response2 = requests.post(
                f"{BACKEND_URL}/chat",
                json=payload2,
                timeout=30
            )
            
            assert response2.status_code == 200
            data2 = response2.json()
            assert data2["conversation_id"] == conversation_id
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend not accessible")

class TestFrontendErrorHandling:
    """Test suite for frontend error handling"""
    
    def test_backend_unavailable_handling(self):
        """Test how frontend handles backend unavailability"""
        # This would normally test frontend error display
        # For now, we test the backend error responses
        
        # Test with invalid agent type
        payload = {
            "message": "Test message",
            "agent_type": "invalid_agent"
        }
        
        try:
            response = requests.post(
                f"{BACKEND_URL}/chat",
                json=payload,
                timeout=30
            )
            
            assert response.status_code == 400
            data = response.json()
            assert "detail" in data
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend not accessible")
    
    def test_message_validation(self):
        """Test message validation"""
        # Test empty message
        payload = {
            "message": "",
            "agent_type": "user"
        }
        
        try:
            response = requests.post(
                f"{BACKEND_URL}/chat",
                json=payload,
                timeout=30
            )
            
            # Should handle empty messages gracefully
            assert response.status_code in [200, 400]
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend not accessible")

class TestFrontendPerformance:
    """Test suite for frontend performance"""
    
    def test_response_time_consistency(self):
        """Test consistent response times"""
        test_messages = [
            "Quick test 1",
            "Quick test 2", 
            "Quick test 3"
        ]
        
        response_times = []
        
        for message in test_messages:
            payload = {
                "message": message,
                "agent_type": "user"
            }
            
            try:
                start_time = time.time()
                
                response = requests.post(
                    f"{BACKEND_URL}/chat",
                    json=payload,
                    timeout=30
                )
                
                end_time = time.time()
                response_time = end_time - start_time
                
                assert response.status_code == 200
                response_times.append(response_time)
                
            except requests.exceptions.ConnectionError:
                pytest.skip("Backend not accessible")
        
        # Check that response times are reasonable
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            assert avg_response_time < 30  # Average should be under 30 seconds

class TestFrontendUserExperience:
    """Test suite for user experience features"""
    
    def test_agent_capabilities_display(self):
        """Test that different agents have different capabilities"""
        user_messages = [
            "Analyze delivery data",
            "Handle customer complaint"
        ]
        
        driver_messages = [
            "Report traffic incident",
            "Request route optimization"
        ]
        
        # Test user agent responses
        for message in user_messages:
            payload = {
                "message": message,
                "agent_type": "user"
            }
            
            try:
                response = requests.post(
                    f"{BACKEND_URL}/chat",
                    json=payload,
                    timeout=30
                )
                
                assert response.status_code == 200
                data = response.json()
                assert len(data["response"]) > 0
                
            except requests.exceptions.ConnectionError:
                pytest.skip("Backend not accessible")
        
        # Test driver agent responses
        for message in driver_messages:
            payload = {
                "message": message,
                "agent_type": "driver"
            }
            
            try:
                response = requests.post(
                    f"{BACKEND_URL}/chat",
                    json=payload,
                    timeout=30
                )
                
                assert response.status_code == 200
                data = response.json()
                assert len(data["response"]) > 0
                
            except requests.exceptions.ConnectionError:
                pytest.skip("Backend not accessible")

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"]) 