from typing import Dict, Any, List, Optional
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.callbacks import AsyncIteratorCallbackHandler
import asyncio
from .base_client import BaseAPIClient
from app.settings import settings

class OpenAIClient(BaseAPIClient):
    """OpenAI client using LangChain for AI interactions"""
    
    def __init__(self, api_key: str = None, model: str = None, temperature: float = None):
        super().__init__(base_url="", api_key=api_key or settings.OPENAI_API_KEY)
        self.model = model or settings.OPENAI_MODEL
        self.temperature = temperature or settings.OPENAI_TEMPERATURE
        self.llm = ChatOpenAI(
            openai_api_key=self.api_key,
            model=self.model,
            temperature=self.temperature,
            streaming=True
        )
    
    async def generate_response(
        self, 
        system_prompt: str, 
        user_message: str, 
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate AI response using LangChain"""
        try:
            messages = []
            
            # Add system prompt
            if system_prompt:
                messages.append(SystemMessage(content=system_prompt))
            
            # Add context if provided
            if context:
                messages.append(SystemMessage(content=f"Context: {context}"))
            
            # Add user message
            messages.append(HumanMessage(content=user_message))
            
            # Generate response
            response = await self.llm.agenerate([messages])
            
            return {
                "success": True,
                "response": response.generations[0][0].text,
                "model": self.model,
                "usage": response.llm_output.get("token_usage", {}) if response.llm_output else {}
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": self.model
            }
    
    async def generate_response_with_prompt_config(
        self, 
        prompt_config: Dict[str, Any], 
        user_message: str
    ) -> Dict[str, Any]:
        """Generate response using prompt configuration"""
        system_prompt = prompt_config.get("system_prompt", "")
        docs = prompt_config.get("docs", "")
        
        return await self.generate_response(
            system_prompt=system_prompt,
            user_message=user_message,
            context=docs
        )
    
    async def make_request(self, endpoint: str, params: Dict[str, Any] = None, 
                          body: Dict[str, Any] = None, headers: Dict[str, Any] = None) -> Dict[str, Any]:
        """Override base method - not used for OpenAI"""
        raise NotImplementedError("OpenAI client uses LangChain, not direct HTTP requests")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model configuration"""
        return {
            "model": self.model,
            "temperature": self.temperature,
            "api_key_configured": bool(self.api_key)
        } 