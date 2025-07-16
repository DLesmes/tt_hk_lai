import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="ETA Agent System",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Backend URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

def check_backend_health():
    """Check if backend is running"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return response.status_code == 200, response.json()
    except requests.exceptions.RequestException:
        return False, None

def main():
    """Main application"""
    st.title("🚚 ETA Agent System")
    st.markdown("AI-driven logistics anomaly handling system")
    
    # Sidebar
    st.sidebar.title("System Status")
    
    # Check backend health
    is_healthy, health_data = check_backend_health()
    
    if is_healthy:
        st.sidebar.success("✅ Backend Connected")
        if health_data:
            st.sidebar.json(health_data)
    else:
        st.sidebar.error("❌ Backend Not Available")
        st.sidebar.info("Please ensure the backend is running on port 8000")
    
    # Main content
    st.header("Welcome to ETA Agent System")
    
    st.markdown("""
    This system helps manage logistics anomalies by:
    
    - **Driver Agent**: Collecting deviation information from drivers
    - **User Agent**: Providing status updates to customers
    - **External APIs**: Validating ETAs with weather and traffic data
    
    ### Getting Started
    
    1. Select your role (Driver or User)
    2. Start a conversation about an anomaly
    3. Get AI-powered assistance and ETA updates
    """)
    
    # Role selection
    st.header("Select Your Role")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚛 Driver", use_container_width=True):
            st.session_state.role = "driver"
            st.success("Driver role selected!")
    
    with col2:
        if st.button("👤 User/Customer", use_container_width=True):
            st.session_state.role = "user"
            st.success("User role selected!")
    
    # Display selected role
    if hasattr(st.session_state, 'role'):
        st.info(f"Current role: **{st.session_state.role.title()}**")
        
        if st.button("Start New Conversation"):
            st.info("Chat interface will be implemented in the next phase!")
    
    # System information
    st.sidebar.header("System Info")
    st.sidebar.markdown(f"**Backend URL**: {BACKEND_URL}")
    st.sidebar.markdown("**Frontend**: Streamlit")
    st.sidebar.markdown("**Database**: SQLite")
    st.sidebar.markdown("**AI Model**: OpenAI GPT-4")

if __name__ == "__main__":
    main() 