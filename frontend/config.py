"""
Frontend configuration and settings
"""
import os
from typing import Dict, List

# Backend API Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
API_TIMEOUT = 30  # seconds

# Frontend Configuration
PAGE_TITLE = "ETA Agent System"
PAGE_ICON = "🚚"
LAYOUT = "wide"
INITIAL_SIDEBAR_STATE = "expanded"

# Agent Types
AGENT_TYPES = ["user", "driver"]

# Chat Configuration
MAX_MESSAGE_LENGTH = 1000
MESSAGE_HISTORY_LIMIT = 100

# UI Configuration
CHAT_INPUT_HEIGHT = 100
METRICS_COLUMNS = 4

# Status Colors
STATUS_COLORS = {
    "online": "#4caf50",
    "offline": "#f44336",
    "warning": "#ff9800",
    "info": "#2196f3"
}

# Message Types
MESSAGE_TYPES = {
    "user": {
        "background": "#e3f2fd",
        "border": "#2196f3",
        "icon": "👤"
    },
    "agent": {
        "background": "#f3e5f5",
        "border": "#9c27b0",
        "icon": "🤖"
    },
    "system": {
        "background": "#fff3e0",
        "border": "#ff9800",
        "icon": "⚙️"
    }
}

# Agent Capabilities
AGENT_CAPABILITIES = {
    "user": {
        "title": "User Agent",
        "description": "AI-powered logistics analyst for customer support and anomaly resolution",
        "capabilities": [
            "📊 Analyze logistics data and ETA reports",
            "🚨 Handle anomaly detection and resolution",
            "📈 Provide optimization recommendations",
            "🔍 Investigate delivery issues",
            "📋 Generate reports and summaries"
        ]
    },
    "driver": {
        "title": "Driver Agent",
        "description": "Real-time route optimization and incident reporting for drivers",
        "capabilities": [
            "🚗 Real-time route optimization",
            "⚡ Traffic and weather integration",
            "🛣️ Dynamic ETA updates",
            "🚨 Incident reporting and handling",
            "📱 Mobile-friendly interactions"
        ]
    }
}

# CSS Styles
CUSTOM_CSS = """
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: #333333;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .agent-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .system-message {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
    }
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }
    .status-online {
        background-color: #4caf50;
    }
    .status-offline {
        background-color: #f44336;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        color: #333333;
    }
    .metric-card h3 {
        color: #555555;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
    }
    .metric-card h2 {
        color: #333333;
        margin: 0;
        font-size: 1.5rem;
        font-weight: bold;
    }
    .agent-info-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    .capability-item {
        margin: 0.5rem 0;
        padding: 0.5rem;
        background: rgba(255,255,255,0.1);
        border-radius: 5px;
        color: white;
    }
    
    /* Additional readability improvements */
    .stTextInput > div > div > input {
        color: #333333;
    }
    
    .stTextArea > div > div > textarea {
        color: #333333;
    }
    
    .stSelectbox > div > div > div {
        color: #333333;
    }
    
    /* Ensure all text in Streamlit components is readable */
    .stMarkdown {
        color: #333333;
    }
    
    /* Improve sidebar readability */
    .css-1d391kg {
        color: #333333;
    }
</style>
"""

# Error Messages
ERROR_MESSAGES = {
    "backend_unavailable": "Backend service is currently unavailable. Please check if the server is running.",
    "connection_error": "Unable to connect to the backend service. Please check your network connection.",
    "timeout_error": "Request timed out. Please try again.",
    "invalid_response": "Received invalid response from the server.",
    "message_too_long": f"Message is too long. Maximum length is {MAX_MESSAGE_LENGTH} characters.",
    "empty_message": "Please enter a message before sending."
}

# Success Messages
SUCCESS_MESSAGES = {
    "message_sent": "Message sent successfully!",
    "conversation_cleared": "Conversation history cleared.",
    "new_conversation": "Started new conversation.",
    "status_refreshed": "System status updated."
}

# Loading Messages
LOADING_MESSAGES = [
    "🤖 Agent is thinking...",
    "🔍 Analyzing the situation...",
    "📊 Processing logistics data...",
    "🚗 Checking route conditions...",
    "⚡ Gathering real-time information..."
] 