from typing import Dict, Any, List, Tuple, Optional
import aiohttp
from .base_client import BaseAPIClient

class OpenRouteServiceClient(BaseAPIClient):
    """OpenRouteService traffic API client (https://openrouteservice.org/dev/#/api-docs)"""
    
    def __init__(self, api_key: Optional[str] = None):
        # OpenRouteService offers free tier without API key
        super().__init__(base_url="https://api.openrouteservice.org/v2", api_key=api_key)
    
    async def get_route(
        self, 
        start_coords: Tuple[float, float], 
        end_coords: Tuple[float, float],
        profile: str = "driving-car"
    ) -> Dict[str, Any]:
        """Get route between two points"""
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8"
        }
        
        if self.api_key:
            headers["Authorization"] = self.api_key
        
        body = {
            "coordinates": [
                [start_coords[1], start_coords[0]],  # [longitude, latitude]
                [end_coords[1], end_coords[0]]
            ],
            "profile": profile,
            "format": "json"
        }
        
        return await self.make_request("/directions/driving-car", body=body, headers=headers)
    
    async def get_route_with_waypoints(
        self, 
        coordinates: List[Tuple[float, float]],
        profile: str = "driving-car"
    ) -> Dict[str, Any]:
        """Get route with multiple waypoints"""
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8"
        }
        
        if self.api_key:
            headers["Authorization"] = self.api_key
        
        # Convert coordinates to [longitude, latitude] format
        coords_list = [[lon, lat] for lat, lon in coordinates]
        
        body = {
            "coordinates": coords_list,
            "profile": profile,
            "format": "json"
        }
        
        return await self.make_request("/directions/driving-car", body=body, headers=headers)
    
    async def get_alternative_routes(
        self, 
        start_coords: Tuple[float, float], 
        end_coords: Tuple[float, float],
        alternatives: int = 2
    ) -> Dict[str, Any]:
        """Get alternative routes"""
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8"
        }
        
        if self.api_key:
            headers["Authorization"] = self.api_key
        
        body = {
            "coordinates": [
                [start_coords[1], start_coords[0]],  # [longitude, latitude]
                [end_coords[1], end_coords[0]]
            ],
            "profile": "driving-car",
            "format": "json",
            "alternatives": alternatives
        }
        
        return await self.make_request("/directions/driving-car", body=body, headers=headers)
    
    async def geocode(self, location: str) -> Dict[str, Any]:
        """Geocode a location string to coordinates"""
        params = {
            "text": location,
            "size": 1
        }
        
        headers = {
            "Accept": "application/json"
        }
        
        if self.api_key:
            headers["Authorization"] = self.api_key
        
        return await self.make_request("/geocode/search", params=params, headers=headers)
    
    async def reverse_geocode(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """Reverse geocode coordinates to location name"""
        params = {
            "point.lat": latitude,
            "point.lon": longitude,
            "size": 1
        }
        
        headers = {
            "Accept": "application/json"
        }
        
        if self.api_key:
            headers["Authorization"] = self.api_key
        
        return await self.make_request("/geocode/reverse", params=params, headers=headers)
    
    async def make_request(self, endpoint: str, params: Dict[str, Any] = None, 
                          body: Dict[str, Any] = None, headers: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make HTTP request to OpenRouteService API"""
        method = "POST" if body else "GET"
        return await self._make_http_request(method, endpoint, params=params, body=body, headers=headers)
    
    def analyze_route_impact(self, route_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze route data for ETA impact"""
        if not route_data.get("success"):
            return {"impact": "unknown", "reason": "Route data unavailable"}
        
        features = route_data.get("data", {}).get("features", [])
        if not features:
            return {"impact": "unknown", "reason": "No route features found"}
        
        # Get the first (best) route
        route = features[0]
        properties = route.get("properties", {})
        summary = properties.get("summary", {})
        
        distance = summary.get("distance", 0)  # in meters
        duration = summary.get("duration", 0)  # in seconds
        
        # Convert to more readable units
        distance_km = distance / 1000
        duration_hours = duration / 3600
        
        # Calculate average speed
        avg_speed = distance_km / duration_hours if duration_hours > 0 else 0
        
        # Analyze for potential delays
        impact = "minimal"
        reasons = []
        
        if avg_speed < 30:  # Slow average speed
            impact = "moderate"
            reasons.append("Slow average speed")
        
        if distance_km > 100:  # Long distance
            impact = "moderate"
            reasons.append("Long route distance")
        
        return {
            "impact": impact,
            "reasons": reasons,
            "distance_km": round(distance_km, 2),
            "duration_hours": round(duration_hours, 2),
            "avg_speed_kmh": round(avg_speed, 2),
            "raw_distance": distance,
            "raw_duration": duration
        } 