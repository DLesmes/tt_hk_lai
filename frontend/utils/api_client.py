import requests
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class APIClient:
    """API client for communicating with the backend"""
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or os.getenv("BACKEND_URL", "http://localhost:8000")
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request to backend"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
    
    def health_check(self) -> Dict[str, Any]:
        """Check backend health"""
        return self._make_request("GET", "/health")
    
    def get_api_status(self) -> Dict[str, Any]:
        """Get API status"""
        return self._make_request("GET", "/api/status")
    
    def route_conversation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Route a new conversation"""
        return self._make_request("POST", "/api/conversation/route", json=data)
    
    def send_driver_message(self, conversation_id: str, message: str) -> Dict[str, Any]:
        """Send message to driver agent"""
        data = {"conversation_id": conversation_id, "message": message}
        return self._make_request("POST", "/api/driver/chat", json=data)
    
    def send_user_message(self, conversation_id: str, message: str) -> Dict[str, Any]:
        """Send message to user agent"""
        data = {"conversation_id": conversation_id, "message": message}
        return self._make_request("POST", "/api/user/chat", json=data)
    
    def get_conversation_status(self, conversation_id: str) -> Dict[str, Any]:
        """Get conversation status"""
        return self._make_request("GET", f"/api/status/{conversation_id}")

# Global API client instance
api_client = APIClient() 