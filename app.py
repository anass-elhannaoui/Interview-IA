import streamlit as st
from openai import OpenAI
from streamlit_js_eval import streamlit_js_eval

# Setting up the Streamlit page configuration - MUST BE FIRST
st.set_page_config(
    page_title="AI Interview Assistant", 
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional minimal styling with Font Awesome icons
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        padding: 1.5rem 2rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* Professional color palette - Minimal & Clean */
    :root {
        --primary: #2563eb;
        --primary-dark: #1e40af;
        --secondary: #64748b;
        --accent: #0ea5e9;
        --success: #10b981;
        --warning: #f59e0b;
        --error: #ef4444;
        --background: #f8fafc;
        --surface: #ffffff;
        --text-primary: #0f172a;
        --text-secondary: #475569;
        --border: #e2e8f0;
    }
    
    /* Ensure proper text contrast */
    .stApp {
        background-color: var(--background);
    }
    
    .stMarkdown, .stText, .stAlert, .stSuccess, .stInfo, .stWarning, .stError {
        color: var(--text-primary) !important;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2.5rem 2rem;
        margin-bottom: 3rem;
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        color: white;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.15);
    }
    
    .main-header h1 {
        font-size: 2.25rem;
        font-weight: 700;
        margin: 0 0 0.75rem 0;
        letter-spacing: -0.02em;
    }
    
    .main-header p {
        font-size: 1.125rem;
        font-weight: 400;
        margin: 0;
        opacity: 0.95;
    }
    
    /* Info box styling */
    .stAlert {
        background-color: var(--surface);
        border: 1px solid var(--border);
        border-left: 4px solid var(--primary);
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    
    .stAlert [data-testid="stMarkdownContainer"] p {
        color: var(--text-primary) !important;
        font-size: 0.9375rem;
        line-height: 1.6;
        margin: 0;
    }
    
    /* Form section styling */
    .section-header {
        color: var(--text-primary);
        font-size: 1.25rem;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid var(--border);
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 10px;
        border: 1.5px solid var(--border);
        padding: 0.875rem 1rem;
        transition: all 0.2s ease;
        font-size: 0.9375rem;
        background: var(--surface);
        color: var(--text-primary) !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.08);
        outline: none;
    }
    
    .stTextInput label,
    .stTextArea label {
        font-weight: 500;
        color: var(--text-primary) !important;
        font-size: 0.9375rem;
        margin-bottom: 0.5rem;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        color: white !important;
        border: none;
        border-radius: 10px;
        padding: 0.875rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.2s ease;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
        cursor: pointer;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.3);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Radio and selectbox styling */
    .stRadio > div > label,
    .stSelectbox > label {
        font-weight: 500;
        color: var(--text-primary) !important;
        margin-bottom: 0.5rem;
        font-size: 0.9375rem;
    }
    
    .stRadio [data-baseweb="radio"] {
        background-color: var(--surface);
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        border: 1px solid var(--border);
    }
    
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 1.5px solid var(--border);
        background: var(--surface);
    }
    
    .stSelectbox select {
        color: var(--text-primary) !important;
    }
    
    /* Chat message styling */
    .stChatMessage {
        border-radius: 12px;
        margin-bottom: 1rem;
        padding: 1.25rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        background: var(--surface);
        border: 1px solid var(--border);
    }
    
    .stChatMessage [data-testid="stMarkdownContainer"] {
        color: var(--text-primary) !important;
    }
    
    /* Chat input styling */
    .stChatInput > div > div > textarea {
        color: var(--text-primary) !important;
        border: 1.5px solid var(--border);
        border-radius: 12px;
        padding: 1rem;
    }
    
    /* Feedback section styling */
    .feedback-container {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 2.5rem;
        margin-top: 2rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
    }
    
    /* Progress indicator */
    .progress-text {
        text-align: center;
        color: var(--text-secondary);
        font-size: 0.9375rem;
        font-weight: 500;
        margin-top: 1rem;
        padding: 0.75rem;
        background: var(--surface);
        border-radius: 8px;
        border: 1px solid var(--border);
    }
    
    /* Success message styling */
    .stSuccess {
        background-color: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-left: 4px solid var(--success);
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
    }
    
    .stSuccess [data-testid="stMarkdownContainer"] {
        color: var(--text-primary) !important;
    }
    
    /* Info message styling */
    .stInfo {
        background-color: #f0f9ff;
        border: 1px solid #bae6fd;
        border-left: 4px solid var(--accent);
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
    }
    
    .stInfo [data-testid="stMarkdownContainer"] {
        color: var(--text-primary) !important;
    }
    
    /* Column spacing */
    .row-widget.stRadio {
        background-color: var(--surface);
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid var(--border);
    }
    
    /* Icon styling */
    .icon {
        margin-right: 0.5rem;
    }
    
    /* Feedback text styling */
    .feedback-text {
        color: var(--text-primary) !important;
        line-height: 1.6;
        font-size: 0.95rem;
    }
    
    /* Ensure all text in streamlit components has proper contrast */
    .st-bb, .st-bc, .st-bd, .st-be, .st-bf, .st-bg, .st-bh, .st-bi, .st-bj, .st-bk, .st-bl, .st-bm, .st-bn, .st-bo, .st-bp, .st-bq, .st-br, .st-bs, .st-bt, .st-bu, .st-bv, .st-bw, .st-bx, .st-by, .st-bz {
        color: var(--text-primary) !important;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1><i class="fas fa-briefcase icon"></i>AI Interview Assistant</h1>
    <p>Practice your interview skills with AI-powered feedback</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state variables
if "setup_complete" not in st.session_state:
    st.session_state.setup_complete = False
if "user_message_count" not in st.session_state:
    st.session_state.user_message_count = 0
if "feedback_shown" not in st.session_state:
    st.session_state.feedback_shown = False
if "chat_complete" not in st.session_state:
    st.session_state.chat_complete = False
if "messages" not in st.session_state:
    st.session_state.messages = []

# Helper functions to update session state
def complete_setup():
    st.session_state.setup_complete = True

def show_feedback():
    st.session_state.feedback_shown = True

# Setup stage for collecting user details
if not st.session_state.setup_complete:
    # Create a centered container
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<p class="section-header"><i class="fas fa-user-circle"></i> Personal Information</p>', unsafe_allow_html=True)
        
        # Initialize session state for personal information
        if "name" not in st.session_state:
            st.session_state["name"] = ""
        if "experience" not in st.session_state:
            st.session_state["experience"] = ""
        if "skills" not in st.session_state:
            st.session_state["skills"] = ""
        
        # Get personal information input
        st.session_state["name"] = st.text_input(
            label="Full Name", 
            value=st.session_state["name"], 
            placeholder="Enter your full name", 
            max_chars=40
        )
        
        st.session_state["experience"] = st.text_area(
            label="Professional Experience", 
            value=st.session_state["experience"], 
            placeholder="Describe your relevant work experience, projects, and achievements", 
            max_chars=200,
            height=100
        )
        
        st.session_state["skills"] = st.text_area(
            label="Technical Skills", 
            value=st.session_state["skills"], 
            placeholder="List your key technical skills and competencies", 
            max_chars=200,
            height=100
        )
        
        st.markdown('<p class="section-header"><i class="fas fa-building"></i> Position & Company Details</p>', unsafe_allow_html=True)
        
        # Initialize session state for company and position information
        if "level" not in st.session_state:
            st.session_state["level"] = "Junior"
        if "position" not in st.session_state:
            st.session_state["position"] = "Data Scientist"
        if "company" not in st.session_state:
            st.session_state["company"] = "Amazon"
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.session_state["level"] = st.radio(
                "Experience Level",
                key="visibility",
                options=["Junior", "Mid-level", "Senior"],
                index=["Junior", "Mid-level", "Senior"].index(st.session_state["level"])
            )
        
        with col_b:
            st.session_state["position"] = st.selectbox(
                "Position",
                ("Data Scientist", "Data Engineer", "ML Engineer", "BI Analyst", "Financial Analyst"),
                index=("Data Scientist", "Data Engineer", "ML Engineer", "BI Analyst", "Financial Analyst").index(st.session_state["position"])
            )
        
        st.session_state["company"] = st.selectbox(
            "Target Company",
            ("Amazon", "Meta", "Udemy", "365 Company", "Nestle", "LinkedIn", "Spotify"),
            index=("Amazon", "Meta", "Udemy", "365 Company", "Nestle", "LinkedIn", "Spotify").index(st.session_state["company"])
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Button to complete setup
        if st.button("Start Interview", on_click=complete_setup, use_container_width=True):
            st.success("Setup complete! Starting your interview...")

# Helper to call OpenAI and return assistant content (synchronous)
def get_assistant_response(client, messages, model):
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": m["role"], "content": m["content"]} for m in messages],
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"[Error calling OpenAI API] {e}"

# Interview phase
if st.session_state.setup_complete and not st.session_state.feedback_shown and not st.session_state.chat_complete:
    
    st.info(
        f"""**Welcome to your interview, {st.session_state['name']}!**
        
Start by introducing yourself. The interviewer will ask you questions one at a time."""
    )
    
    # Progress indicator
    st.markdown(
        f'<p class="progress-text"><i class="fas fa-chart-line"></i> Progress: {st.session_state.user_message_count}/5 responses</p>', 
        unsafe_allow_html=True
    )
    
    # Initialize OpenAI client
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    # Setting OpenAI model if not already initialized
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o"
    
    # Initializing the system prompt for the chatbot with structured interview strategy
    if not st.session_state.messages:
        st.session_state.messages = [{
            "role": "system",
            "content": (
                f"You are an HR executive conducting a structured interview for {st.session_state['name']} "
                f"who is applying for the position of {st.session_state['level']} {st.session_state['position']} at {st.session_state['company']}.\n\n"
                f"Candidate's Background:\n"
                f"- Experience: {st.session_state['experience']}\n"
                f"- Skills: {st.session_state['skills']}\n\n"
                f"INTERVIEW STRUCTURE - Follow this exact sequence:\n"
                f"1. GREETING: Start with a warm greeting and ask the candidate to introduce themselves.\n"
                f"2. BACKGROUND: Ask ONE question about their previous experience or education relevant to the role.\n"
                f"3. TECHNICAL SKILLS: Ask ONE specific technical question related to the {st.session_state['position']} position.\n"
                f"4. BEHAVIORAL: Ask ONE behavioral question using the STAR method (Situation, Task, Action, Result).\n"
                f"5. SCENARIO: Present ONE realistic work scenario related to {st.session_state['company']} and ask how they would handle it.\n"
                f"6. CLOSING: Ask if they have any questions for you, then thank them for their time.\n\n"
                f"IMPORTANT RULES:\n"
                f"- Ask ONLY ONE question at a time and wait for the candidate's response.\n"
                f"- Do NOT write all questions at once.\n"
                f"- Keep questions focused, professional, and relevant to the {st.session_state['position']} role.\n"
                f"- Acknowledge their answers briefly before moving to the next question.\n"
                f"- Do NOT provide feedback or scores during the interview.\n"
                f"- Maintain a professional, friendly tone throughout."
            )
        }]
    
    # Display chat messages (skip system)
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Handle user input and OpenAI response
    if st.session_state.user_message_count < 5:
        if prompt := st.chat_input("Type your response here...", max_chars=1000):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get assistant reply synchronously
            assistant_content = get_assistant_response(
                client, 
                st.session_state.messages, 
                st.session_state["openai_model"]
            )
            with st.chat_message("assistant"):
                st.markdown(assistant_content)
            st.session_state.messages.append({"role": "assistant", "content": assistant_content})
            
            # Increment the user message count
            st.session_state.user_message_count += 1
    
    # Check if the user message count reaches 5
    if st.session_state.user_message_count >= 5:
        st.session_state.chat_complete = True

# Show "Get Feedback" 
if st.session_state.chat_complete and not st.session_state.feedback_shown:
    st.success("Interview completed! You've answered all questions.")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Get Detailed Feedback", on_click=show_feedback, use_container_width=True):
            st.write("Analyzing your performance...")

# Show feedback screen
if st.session_state.feedback_shown:
    st.markdown('<div class="feedback-container">', unsafe_allow_html=True)
    st.markdown('<p class="section-header"><i class="fas fa-chart-bar"></i> Your Interview Performance Feedback</p>', unsafe_allow_html=True)
    
    conversation_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
    
    # Initialize new OpenAI client instance for feedback
    feedback_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    # Generate feedback using the stored messages
    try:
        with st.spinner("Analyzing your interview responses..."):
            feedback_completion = feedback_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": """You are a helpful tool that provides feedback on an interviewee performance.
                     Before the Feedback give a score of 1 to 10.
                     Follow this format:
                     Overall Score: //Your score
                     Feedback: //Here you put your feedback
                     Give only the feedback do not ask any additional questions.
                      """},
                    {"role": "user", "content": f"This is the interview you need to evaluate. Keep in mind that you are only a tool. And you shouldn't engage in any conversation: {conversation_history}"}
                ]
            )
            feedback_text = feedback_completion.choices[0].message.content
            
            # Display feedback in a nice format
            st.markdown(f'<div class="feedback-text">{feedback_text}</div>', unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Failed to generate feedback: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Button to restart the interview
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Restart Interview", type="primary", use_container_width=True):
            streamlit_js_eval(js_expressions="parent.window.location.reload()")