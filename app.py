import streamlit as st

# -----------------------------------
# PAGE SETTINGS
# -----------------------------------

st.set_page_config(
    page_title="AI Python Tutor",
    page_icon="",
    layout="wide"
)

# -----------------------------------
# CHATGPT-STYLE CSS
# -----------------------------------

st.markdown("""
<style>

    /* ================================
       GLOBAL
       ================================ */

    .stApp {
        background: #FFFFFF;
        color: #171717;
    }

    .block-container {
        max-width: 900px;
        padding-top: 35px;
        padding-bottom: 100px;
    }

    /* Remove Streamlit top spacing */
    header {
        background: transparent !important;
    }


    /* ================================
       SIDEBAR
       ================================ */

    section[data-testid="stSidebar"] {
        background: #F7F7F7;
        border-right: 1px solid #E5E5E5;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 25px;
    }

    .sidebar-title {
        font-size: 18px;
        font-weight: 600;
        color: #171717;
        margin-bottom: 5px;
    }

    .sidebar-subtitle {
        font-size: 13px;
        color: #737373;
        margin-bottom: 25px;
    }


    /* ================================
       TITLE
       ================================ */

    .title {
        font-size: 32px;
        font-weight: 600;
        letter-spacing: -0.8px;
        color: #171717;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 15px;
        color: #737373;
        margin-bottom: 35px;
    }


    /* ================================
       CHAT MESSAGES
       ================================ */

    [data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;
        padding: 20px 0 !important;
    }

    [data-testid="stChatMessageContent"] {
        max-width: 760px;
        font-size: 15px;
        line-height: 1.7;
    }

    [data-testid="stChatMessageContent"] p {
        color: #171717;
    }


    /* ================================
       CODE BLOCKS
       ================================ */

    pre {
        background: #F7F7F7 !important;
        border: 1px solid #E5E5E5 !important;
        border-radius: 8px !important;
        padding: 16px !important;
    }

    code {
        font-family:
            "SFMono-Regular",
            "SF Mono",
            Consolas,
            monospace;
    }


    /* ================================
       CHAT INPUT
       ================================ */

    [data-testid="stChatInput"] {
        background: #FFFFFF;
    }

    [data-testid="stChatInput"] > div {
        border: 1px solid #D9D9D9 !important;
        border-radius: 14px !important;
        background: #FFFFFF !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }

    [data-testid="stChatInput"] textarea {
        color: #171717 !important;
        font-size: 15px;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #8A8A8A;
    }


    /* ================================
       BUTTONS
       ================================ */

    .stButton button {
        background: #FFFFFF !important;
        color: #171717 !important;
        border: 1px solid #D9D9D9 !important;
        border-radius: 8px !important;
        font-size: 14px;
    }

    .stButton button:hover {
        background: #F2F2F2 !important;
        border-color: #BDBDBD !important;
    }


    /* ================================
       SELECT BOX
       ================================ */

    div[data-baseweb="select"] > div {
        background: #FFFFFF !important;
        border-color: #D9D9D9 !important;
        border-radius: 8px !important;
    }


    /* ================================
       DIVIDERS
       ================================ */

    hr {
        border-color: #E5E5E5 !important;
    }


    /* ================================
       WELCOME
       ================================ */

    .welcome {
        text-align: center;
        margin-top: 100px;
        margin-bottom: 80px;
    }

    .welcome-title {
        font-size: 28px;
        font-weight: 600;
        color: #171717;
        margin-bottom: 10px;
    }

    .welcome-text {
        font-size: 15px;
        color: #737373;
    }

</style>
""", unsafe_allow_html=True)


# -----------------------------------
# SIDEBAR
# -----------------------------------

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">AI Python Tutor</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">'
        'Your personal Python learning assistant.'
        '</div>',
        unsafe_allow_html=True
    )

    if st.button(
        "+ New conversation",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

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
            "Classes & Objects",
            "Debugging"
        ]
    )

    level = st.selectbox(
        "Difficulty",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )


# -----------------------------------
# SESSION STATE
# -----------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------------
# MAIN AREA
# -----------------------------------

if len(st.session_state.messages) == 0:

    st.markdown("""
    <div class="welcome">

        <div class="welcome-title">
            How can I help you learn Python?
        </div>

        <div class="welcome-text">
            Ask a question, paste your code, or ask me to explain a concept.
        </div>

    </div>
    """, unsafe_allow_html=True)


# -----------------------------------
# CHAT HISTORY
# -----------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# -----------------------------------
# CHAT INPUT
# -----------------------------------

prompt = st.chat_input(
    "Message AI Python Tutor..."
)

if prompt:

    # User message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)


    # Temporary AI response
    response = f"""
I'd be happy to help you with that.

### Let's break it down

Your question was:

> {prompt}

I'll explain it step-by-step and use a simple Python example when appropriate.

```python
# Example
print("Hello, Python!")
