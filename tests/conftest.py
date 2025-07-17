"""
Pytest configuration and fixtures for ETA Agent System tests
"""
import pytest
import requests
import time
import os
from typing import Dict, Any

# Test configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8501")
TEST_TIMEOUT = 30

@pytest.fixture(scope="session")
def backend_health_check():
    """Check if backend is healthy before running tests"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            return True
        else:
            pytest.skip("Backend is not healthy")
    except requests.exceptions.ConnectionError:
        pytest.skip("Backend is not accessible")

@pytest.fixture(scope="session")
def frontend_health_check():
    """Check if frontend is accessible before running tests"""
    try:
        response = requests.get(FRONTEND_URL, timeout=10)
        if response.status_code == 200:
            return True
        else:
            pytest.skip("Frontend is not accessible")
    except requests.exceptions.ConnectionError:
        pytest.skip("Frontend is not accessible")

@pytest.fixture
def sample_chat_payload():
    """Sample chat payload for testing"""
    return {
        "message": "Test message for integration testing",
        "agent_type": "user"
    }

@pytest.fixture
def sample_driver_payload():
    """Sample driver chat payload for testing"""
    return {
        "message": "Report traffic incident on route",
        "agent_type": "driver"
    }

@pytest.fixture
def conversation_session():
    """Fixture to maintain conversation state across tests"""
    conversation_id = None
    
    def _get_conversation_id():
        nonlocal conversation_id
        if conversation_id is None:
            # Start a new conversation
            payload = {
                "message": "Start test conversation",
                "agent_type": "user"
            }
            
            try:
                response = requests.post(
                    f"{BACKEND_URL}/chat",
                    json=payload,
                    timeout=TEST_TIMEOUT
                )
                
                if response.status_code == 200:
                    data = response.json()
                    conversation_id = data["conversation_id"]
                else:
                    conversation_id = "test-conversation-id"
            except:
                conversation_id = "test-conversation-id"
        
        return conversation_id
    
    return _get_conversation_id

@pytest.fixture
def api_client():
    """API client fixture for making requests"""
    class APIClient:
        def __init__(self, base_url: str):
            self.base_url = base_url
            self.session = requests.Session()
        
        def get(self, endpoint: str, **kwargs):
            return self.session.get(f"{self.base_url}{endpoint}", **kwargs)
        
        def post(self, endpoint: str, **kwargs):
            return self.session.post(f"{self.base_url}{endpoint}", **kwargs)
    
    return APIClient(BACKEND_URL)

# Pytest configuration
def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )

def pytest_collection_modifyitems(config, items):
    """Modify test collection"""
    for item in items:
        # Mark tests based on their names
        if "performance" in item.name.lower():
            item.add_marker(pytest.mark.slow)
        if "integration" in item.name.lower() or "api" in item.name.lower():
            item.add_marker(pytest.mark.integration)
        else:
            item.add_marker(pytest.mark.unit) 