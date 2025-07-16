from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import aiohttp
import asyncio
from pydantic import BaseModel

class BaseAPIClient(ABC):
    """Base class for all external API clients"""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url
        self.api_key = api_key
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    @abstractmethod
    async def make_request(self, endpoint: str, params: Dict[str, Any] = None, 
                          body: Dict[str, Any] = None, headers: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make HTTP request to API endpoint"""
        pass
    
    def handle_error(self, response: aiohttp.ClientResponse) -> Dict[str, Any]:
        """Handle API error responses"""
        return {
            "success": False,
            "error": True,
            "status_code": response.status,
            "message": f"API request failed with status {response.status}"
        }
    
    async def _make_http_request(self, method: str, endpoint: str, 
                                params: Dict[str, Any] = None,
                                body: Dict[str, Any] = None,
                                headers: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make HTTP request with error handling"""
        if not self.session:
            raise RuntimeError("Client not initialized. Use async context manager.")
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            async with self.session.request(
                method, url, 
                params=params, 
                json=body, 
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data
                    }
                else:
                    return self.handle_error(response)
                    
        except asyncio.TimeoutError:
            return {
                "success": False,
                "error": "Request timeout"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            } 