from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uuid
from app.settings import settings
from app.services.driver_agent import DriverAgentService
from app.services.user_agent import UserAgentService

# Create FastAPI application
app = FastAPI(
    title="ETA Agent System",
    description="AI-driven system for logistics anomaly handling",
    version="0.1.0",
    debug=settings.DEBUG
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://frontend:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "ETA Agent System API",
        "version": "0.1.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG
    }

# Pydantic models for request/response
class ChatRequest(BaseModel):
    message: str
    agent_type: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: Optional[str] = None
    system_info: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

@app.get("/api/status")
async def api_status():
    """API status endpoint"""
    return {
        "api": "ETA Agent System",
        "version": "0.1.0",
        "database": "SQLite",
        "ai_model": settings.OPENAI_MODEL,
        "environment": settings.ENVIRONMENT
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Chat endpoint for agent interactions"""
    try:
        # Validate agent type
        if request.agent_type not in ["user", "driver"]:
            raise HTTPException(status_code=400, detail="Invalid agent type")
        
        # Initialize appropriate agent
        if request.agent_type == "user":
            agent = UserAgentService()
            # Process the message using the user agent service
            result = await agent.process_user_message(
                conversation_id=request.conversation_id or str(uuid.uuid4()),
                message=request.message,
                context={}
            )
        else:
            agent = DriverAgentService()
            # Process the message using the driver agent service
            result = await agent.process_driver_message(
                conversation_id=request.conversation_id or str(uuid.uuid4()),
                message=request.message,
                context={}
            )
        
        # Debug: Print the result
        print(f"Agent result: {result}")
        
        # Extract response from result
        if result.get("success"):
            response = {
                "response": result.get("response", result.get("status_update", "No response generated")),
                "conversation_id": result.get("conversation_id"),
                "system_info": f"Processed by {request.agent_type} agent",
                "metadata": {
                    "model_info": result.get("model_info", {}),
                    "timestamp": result.get("timestamp")
                }
            }
        else:
            error_msg = result.get("error", "Unknown error")
            print(f"Agent failed: {error_msg}")
            raise HTTPException(status_code=500, detail=error_msg)
        
        return ChatResponse(
            response=response.get("response", "No response generated"),
            conversation_id=response.get("conversation_id"),
            system_info=response.get("system_info"),
            metadata=response.get("metadata", {})
        )
        
    except Exception as e:
        import traceback
        error_details = f"Error processing message: {str(e)}\nTraceback: {traceback.format_exc()}"
        print(f"Chat endpoint error: {error_details}")  # Log to console
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@app.get("/weather/test")
async def test_weather():
    """Test weather API endpoint"""
    try:
        from app.clients.weather_client import OpenMeteoClient
        async with OpenMeteoClient() as client:
            # Test with a sample location
            weather_data = await client.get_current_weather(40.7128, -74.0060)  # New York
            return {"status": "success", "weather_data": weather_data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/traffic/test")
async def test_traffic():
    """Test traffic API endpoint"""
    try:
        from app.clients.traffic_client import OpenRouteServiceClient
        async with OpenRouteServiceClient() as client:
            # Test with a sample route
            traffic_data = await client.get_route((40.7128, -74.0060), (42.3601, -71.0589))  # NY to Boston
            return {"status": "success", "traffic_data": traffic_data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    ) 