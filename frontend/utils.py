"""
Frontend utilities for API calls, data formatting, and common operations
"""
import requests
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
import streamlit as st
from config import BACKEND_URL, API_TIMEOUT, ERROR_MESSAGES, SUCCESS_MESSAGES

class APIUtils:
    """Utility class for API operations"""
    
    @staticmethod
    def check_backend_health() -> Dict[str, Any]:
        """Check backend health status"""
        try:
            response = requests.get(f"{BACKEND_URL}/health", timeout=5)
            return {
                "status": "online" if response.status_code == 200 else "offline",
                "response": response.json() if response.status_code == 200 else None,
                "timestamp": datetime.now().isoformat()
            }
        except requests.exceptions.RequestException:
            return {
                "status": "offline",
                "response": None,
                "timestamp": datetime.now().isoformat()
            }
    
    @staticmethod
    def send_chat_message(message: str, agent_type: str, conversation_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Send a chat message to the backend"""
        try:
            payload = {
                "message": message,
                "agent_type": agent_type,
                "conversation_id": conversation_id
            }
            
            response = requests.post(
                f"{BACKEND_URL}/chat",
                json=payload,
                timeout=API_TIMEOUT
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            st.error(ERROR_MESSAGES["timeout_error"])
            return None
        except requests.exceptions.ConnectionError:
            st.error(ERROR_MESSAGES["connection_error"])
            return None
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
            return None
    
    @staticmethod
    def get_conversation_history(conversation_id: str) -> Optional[List[Dict[str, Any]]]:
        """Get conversation history from backend"""
        try:
            response = requests.get(
                f"{BACKEND_URL}/conversations/{conversation_id}",
                timeout=API_TIMEOUT
            )
            
            if response.status_code == 200:
                return response.json().get("messages", [])
            else:
                return None
                
        except requests.exceptions.RequestException:
            return None

class DataUtils:
    """Utility class for data formatting and validation"""
    
    @staticmethod
    def format_timestamp(timestamp: str) -> str:
        """Format timestamp for display"""
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return dt.strftime("%H:%M:%S")
        except:
            return timestamp
    
    @staticmethod
    def validate_message(message: str) -> tuple[bool, str]:
        """Validate chat message"""
        if not message or not message.strip():
            return False, ERROR_MESSAGES["empty_message"]
        
        if len(message) > 1000:
            return False, ERROR_MESSAGES["message_too_long"]
        
        return True, ""
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 100) -> str:
        """Truncate text to specified length"""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
    
    @staticmethod
    def format_agent_response(response: Dict[str, Any]) -> Dict[str, Any]:
        """Format agent response for display"""
        formatted = {
            "content": response.get("response", "No response received"),
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "conversation_id": response.get("conversation_id"),
            "system_info": response.get("system_info"),
            "metadata": response.get("metadata", {})
        }
        return formatted

class UIUtils:
    """Utility class for UI operations"""
    
    @staticmethod
    def show_loading_message(message: str = "Loading..."):
        """Show loading message with spinner"""
        return st.spinner(message)
    
    @staticmethod
    def show_success_message(message: str):
        """Show success message"""
        st.success(message)
    
    @staticmethod
    def show_error_message(message: str):
        """Show error message"""
        st.error(message)
    
    @staticmethod
    def show_info_message(message: str):
        """Show info message"""
        st.info(message)
    
    @staticmethod
    def show_warning_message(message: str):
        """Show warning message"""
        st.warning(message)
    
    @staticmethod
    def create_metric_card(title: str, value: str, icon: str = ""):
        """Create a metric card HTML"""
        return f"""
        <div class="metric-card">
            <h3>{icon} {title}</h3>
            <h2>{value}</h2>
        </div>
        """
    
    @staticmethod
    def create_chat_message(role: str, content: str, timestamp: str, agent_type: str = ""):
        """Create chat message HTML"""
        if role == "user":
            return f"""
            <div class="chat-message user-message">
                <strong>You:</strong> {content}
                <br><small>{timestamp}</small>
            </div>
            """
        elif role == "agent":
            agent_title = agent_type.title() if agent_type else "Agent"
            return f"""
            <div class="chat-message agent-message">
                <strong>{agent_title} Agent:</strong> {content}
                <br><small>{timestamp}</small>
            </div>
            """
        elif role == "system":
            return f"""
            <div class="chat-message system-message">
                <strong>System:</strong> {content}
                <br><small>{timestamp}</small>
            </div>
            """
        return ""

class SessionUtils:
    """Utility class for session state management"""
    
    @staticmethod
    def initialize_session_state():
        """Initialize session state variables"""
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'selected_agent' not in st.session_state:
            st.session_state.selected_agent = "user"
        if 'conversation_id' not in st.session_state:
            st.session_state.conversation_id = None
        if 'system_status' not in st.session_state:
            st.session_state.system_status = APIUtils.check_backend_health()
        if 'message_count' not in st.session_state:
            st.session_state.message_count = 0
    
    @staticmethod
    def add_message(role: str, content: str, timestamp: str = None):
        """Add message to session state"""
        if timestamp is None:
            timestamp = datetime.now().strftime("%H:%M:%S")
        
        st.session_state.messages.append({
            "role": role,
            "content": content,
            "timestamp": timestamp
        })
        st.session_state.message_count += 1
    
    @staticmethod
    def clear_messages():
        """Clear all messages from session state"""
        st.session_state.messages = []
        st.session_state.message_count = 0
    
    @staticmethod
    def get_message_count() -> int:
        """Get total message count"""
        return st.session_state.message_count
    
    @staticmethod
    def update_system_status():
        """Update system status in session state"""
        st.session_state.system_status = APIUtils.check_backend_health() 