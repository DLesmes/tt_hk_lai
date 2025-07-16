"""
Frontend UI components
"""
import streamlit as st
from datetime import datetime
from typing import Dict, List, Optional, Any
from config import (
    AGENT_TYPES, AGENT_CAPABILITIES, CUSTOM_CSS, 
    CHAT_INPUT_HEIGHT, METRICS_COLUMNS, LOADING_MESSAGES
)
from utils import APIUtils, DataUtils, UIUtils, SessionUtils
import time

class HeaderComponent:
    """Header component for the application"""
    
    @staticmethod
    def render():
        """Render the main header"""
        st.markdown("""
        <div class="main-header">
            <h1>🚚 ETA Agent System</h1>
            <p>AI-driven logistics anomaly handling and ETA optimization</p>
        </div>
        """, unsafe_allow_html=True)

class SidebarComponent:
    """Sidebar component with agent selection and system status"""
    
    @staticmethod
    def render():
        """Render the sidebar"""
        with st.sidebar:
            SidebarComponent._render_agent_selection()
            st.divider()
            SidebarComponent._render_system_status()
            st.divider()
            SidebarComponent._render_quick_actions()
    
    @staticmethod
    def _render_agent_selection():
        """Render agent selection section"""
        st.header("🤖 Agent Selection")
        
        agent_type = st.selectbox(
            "Choose Agent Type",
            AGENT_TYPES,
            index=0 if st.session_state.selected_agent == "user" else 1,
            help="Select which agent you want to interact with"
        )
        
        if agent_type != st.session_state.selected_agent:
            st.session_state.selected_agent = agent_type
            st.session_state.messages = []
            st.session_state.conversation_id = None
            st.rerun()
    
    @staticmethod
    def _render_system_status():
        """Render system status section"""
        st.header("📊 System Status")
        
        # Refresh status button
        if st.button("🔄 Refresh Status"):
            SessionUtils.update_system_status()
            st.rerun()
        
        # Status indicators
        backend_status = st.session_state.system_status.get("status", "offline")
        status_color = "🟢" if backend_status == "online" else "🔴"
        status_text = "Online" if backend_status == "online" else "Offline"
        
        st.markdown(f"{status_color} Backend: {status_text}")
        
        if backend_status == "online":
            st.success("All systems operational")
        else:
            st.error("Backend service unavailable")
    
    @staticmethod
    def _render_quick_actions():
        """Render quick actions section"""
        st.header("⚡ Quick Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Clear Chat"):
                SessionUtils.clear_messages()
                st.rerun()
        
        with col2:
            if st.button("🔄 New Conversation"):
                st.session_state.conversation_id = None
                st.rerun()

class MetricsComponent:
    """Metrics display component"""
    
    @staticmethod
    def render():
        """Render metrics dashboard"""
        col1, col2, col3, col4 = st.columns(METRICS_COLUMNS)
        
        with col1:
            st.markdown(UIUtils.create_metric_card(
                "Active Conversations", 
                "1", 
                "📈"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(UIUtils.create_metric_card(
                "Agent Type", 
                st.session_state.selected_agent.title(), 
                "🤖"
            ), unsafe_allow_html=True)
        
        with col3:
            st.markdown(UIUtils.create_metric_card(
                "Messages", 
                str(SessionUtils.get_message_count()), 
                "💬"
            ), unsafe_allow_html=True)
        
        with col4:
            backend_status = st.session_state.system_status.get("status", "offline")
            status = "🟢 Online" if backend_status == "online" else "🔴 Offline"
            st.markdown(UIUtils.create_metric_card(
                "System Status", 
                status, 
                "🌐"
            ), unsafe_allow_html=True)

class ChatComponent:
    """Chat interface component"""
    
    @staticmethod
    def render():
        """Render the chat interface"""
        st.header("💬 Chat Interface")
        
        # Display chat messages
        ChatComponent._render_messages()
        
        # Message input
        st.divider()
        ChatComponent._render_message_input()
    
    @staticmethod
    def _render_messages():
        """Render chat messages"""
        chat_container = st.container()
        
        with chat_container:
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.markdown(UIUtils.create_chat_message(
                        "user", 
                        message["content"], 
                        message["timestamp"]
                    ), unsafe_allow_html=True)
                elif message["role"] == "agent":
                    st.markdown(UIUtils.create_chat_message(
                        "agent", 
                        message["content"], 
                        message["timestamp"],
                        st.session_state.selected_agent
                    ), unsafe_allow_html=True)
                elif message["role"] == "system":
                    st.markdown(UIUtils.create_chat_message(
                        "system", 
                        message["content"], 
                        message["timestamp"]
                    ), unsafe_allow_html=True)
    
    @staticmethod
    def _render_message_input():
        """Render message input form"""
        with st.form("chat_form", clear_on_submit=True):
            col1, col2 = st.columns([4, 1])
            
            with col1:
                user_input = st.text_area(
                    "Type your message here...",
                    height=CHAT_INPUT_HEIGHT,
                    placeholder="Describe the logistics situation, ask about ETAs, or report an anomaly..."
                )
            
            with col2:
                st.write("")  # Spacer
                st.write("")  # Spacer
                send_button = st.form_submit_button("🚀 Send", use_container_width=True)
            
            if send_button and user_input.strip():
                ChatComponent._handle_message_send(user_input.strip())
    
    @staticmethod
    def _handle_message_send(message: str):
        """Handle message sending"""
        # Validate message
        is_valid, error_msg = DataUtils.validate_message(message)
        if not is_valid:
            UIUtils.show_error_message(error_msg)
            return
        
        # Add user message to chat
        SessionUtils.add_message("user", message)
        
        # Show loading spinner with random message
        import random
        loading_msg = random.choice(LOADING_MESSAGES)
        
        with st.spinner(loading_msg):
            # Send message to backend
            response = APIUtils.send_chat_message(
                message, 
                st.session_state.selected_agent,
                st.session_state.conversation_id
            )
            
            if response:
                # Update conversation ID if provided
                if "conversation_id" in response:
                    st.session_state.conversation_id = response["conversation_id"]
                
                # Add agent response to chat
                formatted_response = DataUtils.format_agent_response(response)
                SessionUtils.add_message("agent", formatted_response["content"])
                
                # Add system info if available
                if formatted_response.get("system_info"):
                    SessionUtils.add_message(
                        "system", 
                        f"System: {formatted_response['system_info']}"
                    )
            else:
                # Add error message
                SessionUtils.add_message(
                    "system", 
                    "Error: Unable to get response from agent"
                )
        
        st.rerun()

class AgentInfoComponent:
    """Agent information component"""
    
    @staticmethod
    def render():
        """Render agent information"""
        st.header("ℹ️ Agent Information")
        
        agent_type = st.session_state.selected_agent
        agent_info = AGENT_CAPABILITIES.get(agent_type, {})
        
        st.markdown(f"""
        <div class="agent-info-card">
            <h3>{agent_info.get('title', 'Agent')}</h3>
            <p>{agent_info.get('description', 'AI-powered logistics agent')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("Capabilities:")
        for capability in agent_info.get('capabilities', []):
            st.markdown(f"""
            <div class="capability-item">
                {capability}
            </div>
            """, unsafe_allow_html=True)
        
        # Add some helpful tips
        st.subheader("💡 Tips:")
        if agent_type == "user":
            st.markdown("""
            - Ask about delivery status and ETAs
            - Report logistics anomalies or issues
            - Request optimization recommendations
            - Get detailed analysis of delivery data
            """)
        else:
            st.markdown("""
            - Report traffic incidents or delays
            - Request route optimization
            - Update delivery status
            - Get weather and traffic information
            """)

class ErrorComponent:
    """Error handling component"""
    
    @staticmethod
    def render_connection_error():
        """Render connection error message"""
        st.error("""
        🔌 **Connection Error**
        
        Unable to connect to the backend service. Please ensure:
        - The backend server is running on port 8000
        - Docker containers are started
        - Network connectivity is available
        """)
        
        if st.button("🔄 Retry Connection"):
            SessionUtils.update_system_status()
            st.rerun()
    
    @staticmethod
    def render_backend_error():
        """Render backend error message"""
        st.error("""
        ⚠️ **Backend Service Error**
        
        The backend service is not responding properly. Please check:
        - Backend logs for errors
        - Database connectivity
        - API service status
        """)

class LoadingComponent:
    """Loading component"""
    
    @staticmethod
    def render_full_page_loading():
        """Render full page loading"""
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <h2>🚚 Loading ETA Agent System...</h2>
            <p>Please wait while we initialize the system</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.spinner("Initializing..."):
            time.sleep(2)  # Simulate loading time 