import streamlit as st

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="AI Python Tutor",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------

st.markdown("""
<style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background-color: #F7F8FA;
        color: #111111;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
    }

    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E5E7EB;
    }

    section[data-testid="stSidebar"] h1 {
        font-size: 20px;
        font-weight: 600;
        color: #111111;
    }

    section[data-testid="stSidebar"] p {
        color: #6B7280;
        font-size: 14px;
    }

    /* ---------- HEADER ---------- */

    .main-title {
        font-size: 42px;
        font-weight: 650;
        letter-spacing: -1.5px;
        color: #111111;
        margin-bottom: 6px;
    }

    .subtitle {
        font-size: 16px;
        color: #6B7280;
        margin-bottom: 35px;
    }

    /* ---------- CHAT ---------- */

    [data-testid="stChatMessage"] {
        border-radius: 12px;
        padding: 18px 20px;
        margin-bottom: 14px;
    }

    [data-testid="stChatMessage"] p {
        font-size: 15px;
        line-height: 1.7;
    }

    /* User message */

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) {
        background-color: #EEF4FF;
        border: 1px solid #D8E5FF;
    }

    /* AI message */

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
    }

    /* ---------- CODE ---------- */

    code {
        font-family: "SFMono-Regular", Consolas, monospace;
    }

    pre {
        border: 1px solid #E5E7EB !important;
        border-radius: 8px !important;
        background-color: #F3F4F6 !important;
    }

    /* ---------- CHAT INPUT ---------- */

    [data-testid="stChatInput"] {
        border-color: #D1D5DB;
    }

    [data-testid="stChatInput"] textarea {
        font-size: 15px;
    }

    /* ---------- BUTTONS ---------- */

    .stButton > button {
        border: 1px solid #D1D5DB;
        background-color: #FFFFFF;
        color: #111111;
        border-radius: 7px;
        font-weight: 500;
    }

    .stButton > button:hover {
        border-color: #2563EB;
        color: #2563EB;
    }

    /* ---------- DIVIDER ---------- */

    .divider {
        height: 1px;
        background-color: #E5E7EB;
        margin: 25px 0;
    }

    /* ---------- INFO CARD ---------- */

    .info-card {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }

    .info-title {
        font-size: 14px;
        font-weight: 600;
        color: #111111;
        margin-bottom: 8px;
    }

    .info-text {
        font-size: 13px;
        color: #6B7280;
        line-height: 1.6;
    }

</style>
""", unsafe_allow_html=True)


# -----------------------------
# SIDEBAR
# -----------------------------

with st.sidebar:

    st.markdown("""
    <h1>Python Tutor</h1>
    <p>Your personal programming tutor.</p>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### Learning")

    topic = st.selectbox(
        "Topic",
        [
            "Python Basics",
            "Variables",
            "Data Types",
            "If Statements",
            "Loops",
            "Functions",
            "Lists",
            "Dictionaries",
            "Object-Oriented Programming",
            "Debugging"
        ]
    )

    difficulty = st.selectbox(
        "Level",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    st.markdown("---")

    if st.button("New Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("""
    <div class="info-card">
        <div class="info-title">Learning approach</div>
        <div class="info-text">
            Ask questions naturally. Your tutor will explain
            concepts step-by-step and provide examples.
        </div>
    </div>
    """, unsafe_allow_html=True)


# -----------------------------
# SESSION STATE
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# MAIN HEADER
# -----------------------------

st.markdown(
    '<div class="main-title">AI Python Tutor</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Learn Python through conversation with your personal AI tutor.'
    '</div>',
    unsafe_allow_html=True
)


# -----------------------------
# WELCOME MESSAGE
# -----------------------------

if len(st.session_state.messages) == 0:

    st.markdown("""
    <div class="info-card">
        <div class="info-title">Start learning Python</div>
        <div class="info-text">
            Ask me anything about Python. I can explain concepts,
            walk through code, find errors, and give you practice
            problems.
        </div>
    </div>
    """, unsafe_allow_html=True)


# -----------------------------
# DISPLAY CHAT HISTORY
# -----------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -----------------------------
# CHAT INPUT
# -----------------------------

prompt = st.chat_input(
    "Ask a Python question..."
)

if prompt:

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # Temporary AI response
    response = f"""
### Let's work through it

You asked:

> {prompt}

I'll explain the concept step-by-step, then give you a simple Python example and a short practice question.
"""

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
