from typing import Dict, Any, Optional, Tuple
import uuid
from datetime import datetime
from app.clients.openai_client import OpenAIClient
from app.clients.weather_client import OpenMeteoClient
from app.clients.traffic_client import OpenRouteServiceClient
from app.config.prompt_manager import prompt_manager
from app.settings import settings

class DriverAgentService:
    """Driver agent service for handling driver interactions"""
    
    def __init__(self):
        self.openai_client = OpenAIClient(
            api_key=settings.OPENAI_API_KEY,
            model=settings.OPENAI_MODEL,
            temperature=settings.OPENAI_TEMPERATURE
        )
        self.weather_client = OpenMeteoClient()
        self.traffic_client = OpenRouteServiceClient(
            api_key=settings.TRAFFIC_API_KEY
        )
    
    async def process_driver_message(
        self, 
        conversation_id: str, 
        message: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Process a message from a driver"""
        try:
            # Get prompt configuration
            prompt_config = prompt_manager.get_prompt_for_role(
                "driver",
                version="v1",
                context=context.get("conversation_history", ""),
                origin=context.get("origin", "Unknown"),
                destination=context.get("destination", "Unknown"),
                timestamp_of_anomaly=context.get("timestamp_of_anomaly", "Unknown"),
                current_eta=context.get("current_eta", "Unknown"),
                docs_text=context.get("docs_text", ""),
                message=message
            )
            
            # Generate AI response
            ai_response = await self.openai_client.generate_response_with_prompt_config(
                prompt_config=prompt_config,
                user_message=message
            )
            
            if not ai_response.get("success"):
                return {
                    "success": False,
                    "error": ai_response.get("error", "Failed to generate response"),
                    "conversation_id": conversation_id
                }
            
            # Analyze message for route/ETA information
            analysis = await self._analyze_driver_message(message, context)
            
            # Validate route if mentioned
            route_validation = None
            if analysis.get("mentions_route"):
                route_validation = await self._validate_proposed_route(context)
            
            # Check weather conditions
            weather_data = None
            if context.get("current_location"):
                weather_data = await self._get_weather_conditions(context["current_location"])
            
            return {
                "success": True,
                "conversation_id": conversation_id,
                "response": ai_response["response"],
                "analysis": analysis,
                "route_validation": route_validation,
                "weather_conditions": weather_data,
                "model_info": ai_response.get("usage", {}),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "conversation_id": conversation_id
            }
    
    async def _analyze_driver_message(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze driver message for key information"""
        message_lower = message.lower()
        
        analysis = {
            "mentions_route": False,
            "mentions_eta": False,
            "mentions_weather": False,
            "mentions_traffic": False,
            "mentions_support": False,
            "extracted_info": {}
        }
        
        # Check for route mentions
        route_keywords = ["route", "way", "path", "direction", "road"]
        if any(keyword in message_lower for keyword in route_keywords):
            analysis["mentions_route"] = True
        
        # Check for ETA mentions
        eta_keywords = ["eta", "time", "arrival", "delivery", "schedule"]
        if any(keyword in message_lower for keyword in eta_keywords):
            analysis["mentions_eta"] = True
        
        # Check for weather mentions
        weather_keywords = ["weather", "rain", "snow", "storm", "wind", "fog"]
        if any(keyword in message_lower for keyword in weather_keywords):
            analysis["mentions_weather"] = True
        
        # Check for traffic mentions
        traffic_keywords = ["traffic", "jam", "congestion", "delay", "slow"]
        if any(keyword in message_lower for keyword in traffic_keywords):
            analysis["mentions_traffic"] = True
        
        # Check for support mentions
        support_keywords = ["help", "support", "assistance", "problem", "issue"]
        if any(keyword in message_lower for keyword in support_keywords):
            analysis["mentions_support"] = True
        
        return analysis
    
    async def _validate_proposed_route(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a proposed route using traffic API"""
        try:
            origin = context.get("origin")
            destination = context.get("destination")
            
            if not origin or not destination:
                return {"success": False, "error": "Missing origin or destination"}
            
            # Geocode locations to get coordinates
            origin_geo = await self.traffic_client.geocode(origin)
            dest_geo = await self.traffic_client.geocode(destination)
            
            if not origin_geo.get("success") or not dest_geo.get("success"):
                return {"success": False, "error": "Failed to geocode locations"}
            
            # Extract coordinates
            origin_coords = self._extract_coordinates(origin_geo)
            dest_coords = self._extract_coordinates(dest_geo)
            
            if not origin_coords or not dest_coords:
                return {"success": False, "error": "Invalid coordinates"}
            
            # Get route
            route_data = await self.traffic_client.get_route(origin_coords, dest_coords)
            
            if route_data.get("success"):
                # Analyze route impact
                impact_analysis = self.traffic_client.analyze_route_impact(route_data)
                
                return {
                    "success": True,
                    "route_data": route_data["data"],
                    "impact_analysis": impact_analysis
                }
            else:
                return {"success": False, "error": "Failed to get route data"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _get_weather_conditions(self, location: str) -> Dict[str, Any]:
        """Get weather conditions for a location"""
        try:
            # Geocode location to get coordinates
            geo_result = await self.traffic_client.geocode(location)
            
            if not geo_result.get("success"):
                return {"success": False, "error": "Failed to geocode location"}
            
            coords = self._extract_coordinates(geo_result)
            if not coords:
                return {"success": False, "error": "Invalid coordinates"}
            
            # Get weather data
            weather_data = await self.weather_client.get_current_weather(coords[0], coords[1])
            
            if weather_data.get("success"):
                # Analyze weather impact
                impact_analysis = self.weather_client.get_weather_impact_on_eta(weather_data)
                
                return {
                    "success": True,
                    "weather_data": weather_data["data"],
                    "impact_analysis": impact_analysis
                }
            else:
                return {"success": False, "error": "Failed to get weather data"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _extract_coordinates(self, geo_result: Dict[str, Any]) -> Optional[Tuple[float, float]]:
        """Extract coordinates from geocoding result"""
        try:
            features = geo_result.get("data", {}).get("features", [])
            if features:
                coords = features[0].get("geometry", {}).get("coordinates", [])
                if len(coords) >= 2:
                    # OpenRouteService returns [longitude, latitude]
                    return (coords[1], coords[0])  # Convert to (latitude, longitude)
            return None
        except Exception:
            return None
    
    async def get_next_questions(self, conversation_history: str) -> Dict[str, Any]:
        """Get suggested next questions based on conversation history"""
        try:
            prompt_config = prompt_manager.get_prompt_for_role(
                "driver",
                version="v1",
                context=conversation_history,
                docs_text="",
                message="What should I ask next?"
            )
            
            response = await self.openai_client.generate_response_with_prompt_config(
                prompt_config=prompt_config,
                user_message="Based on our conversation, what are the most important questions I should ask next to gather all necessary information for the ETA update?"
            )
            
            return {
                "success": True,
                "suggested_questions": response.get("response", ""),
                "model_info": response.get("usage", {})
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            } 