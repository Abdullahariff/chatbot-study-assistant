import streamlit as st
import requests
import json
from datetime import datetime

# --- CORRECTED PART: DEFINE BACKEND URL ---
# Use the actual Render URL for your FastAPI service
BACKEND_URL = "https://chatbot-study-assistant.onrender.com"

# Page configuration
st.set_page_config(
    page_title="StudyBuddy - AI Tutor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional chat interface
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stAppHeader {display:none;}
    
    /* Chat container */
    .chat-container {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 20px 0;
        max-height: 600px;
        overflow-y: auto;
    }
    
    /* User message styling */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0;
        margin-left: 20%;
        word-wrap: break-word;
        box-shadow: 0 2px 5px rgba(102, 126, 234, 0.3);
        animation: slideInRight 0.3s ease-out;
    }
    
    /* Bot message styling */
    .bot-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 0;
        margin-right: 20%;
        word-wrap: break-word;
        box-shadow: 0 2px 5px rgba(245, 87, 108, 0.3);
        animation: slideInLeft 0.3s ease-out;
    }
    
    /* System message styling */
    .system-message {
        background: #e9ecef;
        color: #6c757d;
        padding: 8px 12px;
        border-radius: 12px;
        margin: 8px auto;
        text-align: center;
        font-size: 0.9em;
        max-width: 60%;
    }
    
    /* Timestamp styling */
    .timestamp {
        font-size: 0.8em;
        color: rgba(255,255,255,0.7);
        text-align: right;
        margin-top: 4px;
    }
    
    .bot-timestamp {
        text-align: left;
    }
    
    /* Header styling */
    .chat-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 12px 12px 0 0;
        text-align: center;
        margin-bottom: 0;
    }
    
    /* Input area styling */
    .input-container {
        background: white;
        padding: 15px;
        border-radius: 0 0 12px 12px;
        border-top: 1px solid #e9ecef;
        position: sticky;
        bottom: 0;
    }
    
    /* Animations */
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* Typing indicator */
    .typing-indicator {
        display: inline-block;
        margin-right: 20%;
        background: #f1f3f4;
        padding: 12px 16px;
        border-radius: 18px;
        margin-bottom: 8px;
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    /* Status indicator */
    .status-online {
        display: inline-block;
        width: 10px;
        height: 10px;
        background-color: #28a745;
        border-radius: 50%;
        margin-left: 8px;
        animation: blink 2s infinite;
    }
    
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0.3; }
    }
    
    /* Sidebar styling */
    .sidebar-content {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    
    /* Custom button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "system",
        "content": "Welcome to StudyBuddy! 🎓 I'm here to help you with Computer Science topics.",
        "timestamp": datetime.now().strftime("%H:%M")
    })

if 'api_status' not in st.session_state:
    st.session_state.api_status = "unknown"

# Function to check API health
def check_api_health():
    try:
        # Use the correct backend URL
        response = requests.get(f"{BACKEND_URL}/health", timeout=3)
        if response.status_code == 200:
            st.session_state.api_status = "online"
            return True
        else:
            st.session_state.api_status = "error"
            return False
    except requests.exceptions.RequestException:
        st.session_state.api_status = "offline"
        return False

# Function to send message to API
def send_message(message):
    try:
        # Use the correct backend URL
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json={"prompt": message},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"❌ Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return f"❌ Connection Error: {str(e)}"

# Main layout
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    # Header
    st.markdown("""
    <div class="chat-header">
        <h2>🎓 StudyBuddy</h2>
        <p style="margin: 0; font-size: 1.1em;">Your AI Computer Science Tutor</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check API status
    api_online = check_api_health()
    status_color = "🟢" if api_online else "🔴"
    status_text = "Online" if api_online else "Offline"
    
    st.markdown(f"""
    <div style="text-align: center; padding: 10px; background: white; margin-bottom: 20px;">
        <span style="color: #6c757d;">Status: {status_color} {status_text}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Display messages
        for message in st.session_state.messages:
            timestamp = message.get("timestamp", datetime.now().strftime("%H:%M"))
            
            if message["role"] == "system":
                st.markdown(f"""
                <div class="system-message">
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            
            elif message["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    {message["content"]}
                    <div class="timestamp">{timestamp}</div>
                </div>
                """, unsafe_allow_html=True)
            
            elif message["role"] == "assistant":
                st.markdown(f"""
                <div class="bot-message">
                    {message["content"]}
                    <div class="timestamp bot-timestamp">{timestamp}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Input area
with col2:
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    # Create input form
    with st.form(key="chat_form", clear_on_submit=True):
        col_input, col_button = st.columns([4, 1])
        
        with col_input:
            user_input = st.text_input(
                "Type your message...",
                placeholder="Ask me about Data Structures, Algorithms, OS, etc.",
                label_visibility="collapsed"
            )
        
        with col_button:
            send_button = st.form_submit_button("Send 📤")
    
    # Quick action buttons
    st.markdown("**Quick Actions:**")
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    
    with col_btn1:
        if st.button("📚 Explain Topic"):
            st.session_state.last_button_prompt = "Explain binary search with code"
            st.rerun()
    
    with col_btn2:
        if st.button("❓ Take Quiz"):
            st.session_state.last_button_prompt = "Give me a quiz on data structures"
            st.rerun()
    
    with col_btn3:
        if st.button("💡 Study Tips"):
            st.session_state.last_button_prompt = "Give me study tips for algorithms"
            st.rerun()
    
    # Check if a button was clicked and trigger the logic
    if "last_button_prompt" in st.session_state and st.session_state.last_button_prompt:
        user_input = st.session_state.last_button_prompt
        del st.session_state.last_button_prompt # Clear the prompt
        send_button = True
    
    st.markdown('</div>', unsafe_allow_html=True)

# Handle message sending
if send_button and user_input and api_online:
    # Add user message
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": timestamp
    })
    
    # Show typing indicator
    with col2:
        st.markdown("""
        <div class="typing-indicator">
            <span>StudyBuddy is typing...</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Get bot response
    bot_response = send_message(user_input)
    
    # Add bot response
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_response,
        "timestamp": datetime.now().strftime("%H:%M")
    })
    
    # Rerun to update the chat
    st.rerun()

elif send_button and user_input and not api_online:
    st.error("❌ StudyBuddy is currently offline. Please check if the backend server is running.")

elif send_button and not user_input:
    st.warning("⚠️ Please enter a message before sending.")

# Sidebar with information
with st.sidebar:
    st.markdown("""
    <div class="sidebar-content">
        <h3>🎓 StudyBuddy Features</h3>
        <ul style="list-style-type: none; padding-left: 0;">
            <li>📖 <b>Topic Explanations</b><br>Get clear explanations with code examples</li><br>
            <li>❓ <b>Interactive Quizzes</b><br>Test your knowledge with MCQs</li><br>
            <li>💡 <b>Study Tips</b><br>Get personalized study recommendations</li><br>
            <li>🔖 <b>Bookmark Suggestions</b><br>Important topics to remember</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [{
            "role": "system",
            "content": "Welcome to StudyBuddy! 🎓 I'm here to help you with Computer Science topics.",
            "timestamp": datetime.now().strftime("%H:%M")
        }]
        st.rerun()
    
    st.markdown("""
    <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-top: 20px;">
        <h4>📋 Supported Topics</h4>
        <ul style="font-size: 0.9em; color: #6c757d;">
            <li>Data Structures & Algorithms</li>
            <li>Operating Systems</li>
            <li>Database Management</li>
            <li>Computer Networks</li>
            <li>Machine Learning</li>
            <li>Software Engineering</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Auto-scroll to bottom (JavaScript injection)
st.markdown("""
<script>
    var chatContainer = document.querySelector('.chat-container');
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
</script>
""", unsafe_allow_html=True)
