import streamlit as st
import logging
from datetime import datetime
from agents.supervisor import SupervisorAgent
from security.pii_masking import PIIMasker
from config import settings

# Configure logging
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Banking AI Assistant",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f5f7fa;
    }
    .stChatMessage {
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "supervisor" not in st.session_state:
    st.session_state.supervisor = SupervisorAgent()
if "pii_masker" not in st.session_state:
    st.session_state.pii_masker = PIIMasker()

def process_user_query(user_input: str) -> str:
    """Process user query through the multi-agent system."""
    try:
        # Apply PII masking to user input
        masked_input = st.session_state.pii_masker.mask_input(user_input)
        logger.info(f"Masked input: {masked_input}")
        
        # Route through supervisor agent
        response = st.session_state.supervisor.route_query(masked_input)
        
        # Unmask sensitive data in response
        unmasked_response = st.session_state.pii_masker.unmask_output(response)
        
        return unmasked_response
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return f"I encountered an error processing your request. Error: {str(e)}"

def main():
    # Sidebar configuration
    with st.sidebar:
        st.title("🏦 Banking AI Assistant")
        st.markdown("---")
        st.subheader("System Status")
        st.info("✅ All agents online and ready")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Clear Chat"):
                st.session_state.messages = []
                st.rerun()
        with col2:
            if st.button("⚙️ Settings"):
                st.session_state.show_settings = not st.session_state.get("show_settings", False)
        
        st.markdown("---")
        st.subheader("Agent Information")
        agents_info = {
            "🧠 Supervisor Agent": "Routes queries to appropriate specialist agents",
            "📚 RAG Specialist": "Handles FAQs and policy documentation",
            "💰 Core Banking": "Manages account details and transactions",
            "📝 Onboarding": "Processes new account creation",
            "🤝 Fallback Agent": "Escalates to human support when needed"
        }
        for agent, desc in agents_info.items():
            st.caption(f"{agent}: {desc}")
    
    # Main chat interface
    st.title("🏦 Intelligent Banking Assistant")
    st.markdown("*Powered by Multi-Agent AI with LangGraph and LangChain*")
    st.markdown("---")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # User input
    user_input = st.chat_input("Ask me anything about your banking needs...")
    
    if user_input:
        # Display user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Process query
        with st.spinner("🤔 Processing your query..."):
            response = process_user_query(user_input)
        
        # Display assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray; font-size: 12px;'>
        <p>🔒 Your data is encrypted and secured • PII automatically masked</p>
        <p>Compliance: GDPR • PCI DSS • SOC 2</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
