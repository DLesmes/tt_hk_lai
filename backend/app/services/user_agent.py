from typing import Dict, Any, Optional
from datetime import datetime
from app.clients.openai_client import OpenAIClient
from app.clients.weather_client import OpenMeteoClient
from app.clients.traffic_client import OpenRouteServiceClient
from app.config.prompt_manager import prompt_manager
from app.settings import settings

class UserAgentService:
    """User agent service for providing customer updates"""
    
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
    
    async def generate_status_update(
        self, 
        conversation_id: str, 
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate a status update for the customer"""
        try:
            # Get prompt configuration
            prompt_config = prompt_manager.get_prompt_for_role(
                "user",
                version="v1",
                context=context.get("conversation_history", ""),
                origin=context.get("origin", "Unknown"),
                destination=context.get("destination", "Unknown"),
                original_eta=context.get("original_eta", "Unknown"),
                revised_eta=context.get("revised_eta", "Unknown"),
                deviation_reason=context.get("deviation_reason", "Unknown"),
                docs_text=context.get("docs_text", ""),
                message="Generate status update"
            )
            
            # Generate AI response
            ai_response = await self.openai_client.generate_response_with_prompt_config(
                prompt_config=prompt_config,
                user_message="Please provide a comprehensive status update to the customer about their shipment."
            )
            
            if not ai_response.get("success"):
                return {
                    "success": False,
                    "error": ai_response.get("error", "Failed to generate response"),
                    "conversation_id": conversation_id
                }
            
            # Get additional context data
            weather_context = await self._get_weather_context(context)
            traffic_context = await self._get_traffic_context(context)
            
            return {
                "success": True,
                "conversation_id": conversation_id,
                "status_update": ai_response["response"],
                "weather_context": weather_context,
                "traffic_context": traffic_context,
                "model_info": ai_response.get("usage", {}),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "conversation_id": conversation_id
            }
    
    async def process_user_message(
        self, 
        conversation_id: str, 
        message: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Process a message from a user/customer"""
        try:
            # Get prompt configuration
            prompt_config = prompt_manager.get_prompt_for_role(
                "user",
                version="v1",
                context=context.get("conversation_history", ""),
                origin=context.get("origin", "Unknown"),
                destination=context.get("destination", "Unknown"),
                original_eta=context.get("original_eta", "Unknown"),
                revised_eta=context.get("revised_eta", "Unknown"),
                deviation_reason=context.get("deviation_reason", "Unknown"),
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
            
            return {
                "success": True,
                "conversation_id": conversation_id,
                "response": ai_response["response"],
                "model_info": ai_response.get("usage", {}),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "conversation_id": conversation_id
            }
    
    async def generate_automated_message(
        self, 
        conversation_id: str, 
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate an automated customer message"""
        try:
            # Get prompt configuration
            prompt_config = prompt_manager.get_prompt_for_role(
                "user",
                version="v1",
                context=context.get("conversation_history", ""),
                origin=context.get("origin", "Unknown"),
                destination=context.get("destination", "Unknown"),
                original_eta=context.get("original_eta", "Unknown"),
                revised_eta=context.get("revised_eta", "Unknown"),
                deviation_reason=context.get("deviation_reason", "Unknown"),
                docs_text=context.get("docs_text", ""),
                message="Generate automated message"
            )
            
            # Generate AI response
            ai_response = await self.openai_client.generate_response_with_prompt_config(
                prompt_config=prompt_config,
                user_message="Generate a professional, automated message to inform the customer about their shipment status and any ETA changes."
            )
            
            if not ai_response.get("success"):
                return {
                    "success": False,
                    "error": ai_response.get("error", "Failed to generate response"),
                    "conversation_id": conversation_id
                }
            
            return {
                "success": True,
                "conversation_id": conversation_id,
                "automated_message": ai_response["response"],
                "model_info": ai_response.get("usage", {}),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "conversation_id": conversation_id
            }
    
    async def _get_weather_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get weather context for the route"""
        try:
            origin = context.get("origin")
            destination = context.get("destination")
            
            if not origin or not destination:
                return {"success": False, "error": "Missing origin or destination"}
            
            # Get weather for both origin and destination
            origin_weather = await self._get_weather_for_location(origin)
            dest_weather = await self._get_weather_for_location(destination)
            
            return {
                "success": True,
                "origin_weather": origin_weather,
                "destination_weather": dest_weather
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _get_traffic_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get traffic context for the route"""
        try:
            origin = context.get("origin")
            destination = context.get("destination")
            
            if not origin or not destination:
                return {"success": False, "error": "Missing origin or destination"}
            
            # Get route information
            route_data = await self._get_route_info(origin, destination)
            
            return {
                "success": True,
                "route_info": route_data
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _get_weather_for_location(self, location: str) -> Dict[str, Any]:
        """Get weather for a specific location"""
        try:
            # Geocode location
            geo_result = await self.traffic_client.geocode(location)
            
            if not geo_result.get("success"):
                return {"success": False, "error": "Failed to geocode location"}
            
            coords = self._extract_coordinates(geo_result)
            if not coords:
                return {"success": False, "error": "Invalid coordinates"}
            
            # Get weather data
            weather_data = await self.weather_client.get_current_weather(coords[0], coords[1])
            
            if weather_data.get("success"):
                # Get weather description
                current = weather_data["data"].get("current", {})
                weather_code = current.get("weather_code", 0)
                weather_description = self.weather_client.interpret_weather_code(weather_code)
                
                return {
                    "success": True,
                    "location": location,
                    "weather_description": weather_description,
                    "temperature": current.get("temperature_2m"),
                    "precipitation": current.get("precipitation"),
                    "wind_speed": current.get("wind_speed_10m")
                }
            else:
                return {"success": False, "error": "Failed to get weather data"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _get_route_info(self, origin: str, destination: str) -> Dict[str, Any]:
        """Get route information between two locations"""
        try:
            # Geocode locations
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
                    "origin": origin,
                    "destination": destination,
                    "impact_analysis": impact_analysis
                }
            else:
                return {"success": False, "error": "Failed to get route data"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _extract_coordinates(self, geo_result: Dict[str, Any]) -> Optional[tuple]:
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