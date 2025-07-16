import streamlit as st
from config import PAGE_TITLE, PAGE_ICON, LAYOUT, INITIAL_SIDEBAR_STATE, CUSTOM_CSS
from components import (
    HeaderComponent, SidebarComponent, MetricsComponent, 
    ChatComponent, AgentInfoComponent, ErrorComponent, LoadingComponent
)
from utils import SessionUtils

# Page configuration
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state=INITIAL_SIDEBAR_STATE
)

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

class ETAAgentFrontend:
    def __init__(self):
        self.session_state = st.session_state
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize session state variables"""
        SessionUtils.initialize_session_state()
    
    def run(self):
        """Main application runner"""
        # Check if backend is available
        backend_status = self.session_state.system_status.get("status", "offline")
        
        if backend_status == "offline":
            # Show connection error
            HeaderComponent.render()
            ErrorComponent.render_connection_error()
            return
        
        # Render main application
        HeaderComponent.render()
        SidebarComponent.render()
        MetricsComponent.render()
        
        # Main content area
        col1, col2 = st.columns([2, 1])
        
        with col1:
            ChatComponent.render()
        
        with col2:
            AgentInfoComponent.render()

def main():
    """Main application entry point"""
    app = ETAAgentFrontend()
    app.run()

if __name__ == "__main__":
    main() 