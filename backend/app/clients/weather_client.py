from typing import Dict, Any, Optional, Tuple, List
from datetime import datetime, timedelta
import aiohttp
from .base_client import BaseAPIClient

class OpenMeteoClient(BaseAPIClient):
    """Open-Meteo weather API client (https://open-meteo.com/en/docs)"""
    
    def __init__(self):
        super().__init__(base_url="https://api.open-meteo.com/v1")
    
    async def get_current_weather(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """Get current weather conditions"""
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,wind_direction_10m,wind_gusts_10m",
            "timezone": "auto"
        }
        
        return await self.make_request("/forecast", params=params)
    
    async def get_weather_forecast(
        self, 
        latitude: float, 
        longitude: float, 
        days: int = 7
    ) -> Dict[str, Any]:
        """Get weather forecast for specified days"""
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": "temperature_2m,precipitation_probability,weather_code,wind_speed_10m,wind_direction_10m",
            "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max",
            "timezone": "auto",
            "forecast_days": days
        }
        
        return await self.make_request("/forecast", params=params)
    
    async def get_weather_along_route(
        self, 
        coordinates: List[Tuple[float, float]]
    ) -> Dict[str, Any]:
        """Get weather conditions along a route"""
        weather_data = []
        
        for lat, lon in coordinates:
            weather = await self.get_current_weather(lat, lon)
            if weather.get("success"):
                weather_data.append({
                    "coordinates": {"lat": lat, "lon": lon},
                    "weather": weather["data"]
                })
        
        return {
            "success": True,
            "route_weather": weather_data
        }
    
    async def make_request(self, endpoint: str, params: Dict[str, Any] = None, 
                          body: Dict[str, Any] = None, headers: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make HTTP request to Open-Meteo API"""
        return await self._make_http_request("GET", endpoint, params=params)
    
    def interpret_weather_code(self, code: int) -> str:
        """Interpret WMO weather codes"""
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy", 
            3: "Overcast",
            45: "Foggy",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            56: "Light freezing drizzle",
            57: "Dense freezing drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            66: "Light freezing rain",
            67: "Heavy freezing rain",
            71: "Slight snow fall",
            73: "Moderate snow fall",
            75: "Heavy snow fall",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail"
        }
        return weather_codes.get(code, "Unknown")
    
    def get_weather_impact_on_eta(self, weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze weather impact on ETA"""
        if not weather_data.get("success"):
            return {"impact": "unknown", "reason": "Weather data unavailable"}
        
        current = weather_data.get("data", {}).get("current", {})
        weather_code = current.get("weather_code", 0)
        wind_speed = current.get("wind_speed_10m", 0)
        precipitation = current.get("precipitation", 0)
        
        impact = "minimal"
        reasons = []
        
        # Check for severe weather conditions
        if weather_code in [95, 96, 99]:  # Thunderstorms
            impact = "significant"
            reasons.append("Thunderstorm conditions")
        
        if weather_code in [65, 67, 75]:  # Heavy rain/snow
            impact = "moderate"
            reasons.append("Heavy precipitation")
        
        if wind_speed > 50:  # High winds
            impact = "moderate"
            reasons.append("High wind speeds")
        
        if weather_code in [45, 48]:  # Fog
            impact = "moderate"
            reasons.append("Foggy conditions")
        
        return {
            "impact": impact,
            "reasons": reasons,
            "weather_code": weather_code,
            "wind_speed": wind_speed,
            "precipitation": precipitation
        } 