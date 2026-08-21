import streamlit as st

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Python Tutor",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM DESIGN
# =========================================================

st.markdown(
    """
    <style>

    /* =========================
       GLOBAL
       ========================= */

    .stApp {
        background-color: #FFFFFF;
        color: #171717;
    }

    .block-container {
        max-width: 900px;
        padding-top: 40px;
        padding-bottom: 120px;
    }

    /* Hide Streamlit branding */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }


    /* =========================
       SIDEBAR
       ========================= */

    section[data-testid="stSidebar"] {
        background-color: #F7F7F7;
        border-right: 1px solid #E5E5E5;
    }

    .sidebar-title {
        font-size: 18px;
        font-weight: 600;
        color: #171717;
        margin-bottom: 5px;
    }

    .sidebar-description {
        font-size: 13px;
        color: #737373;
        margin-bottom: 25px;
    }


    /* =========================
       TITLE
       ========================= */

    .page-title {
        font-size: 32px;
        font-weight: 600;
        letter-spacing: -0.8px;
        color: #171717;
        margin-bottom: 5px;
    }

    .page-subtitle {
        font-size: 15px;
        color: #737373;
        margin-bottom: 40px;
    }


    /* =========================
       WELCOME SCREEN
       ========================= */

    .welcome {
        text-align: center;
        margin-top: 130px;
    }

    .welcome-title {
        font-size: 28px;
        font-weight: 600;
        color: #171717;
        margin-bottom: 12px;
    }

    .welcome-description {
        font-size: 15px;
        color: #737373;
    }


    /* =========================
       CHAT
       ========================= */

    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding: 20px 0 !important;
    }

    [data-testid="stChatMessageContent"] {
        font-size: 15px;
        line-height: 1.7;
    }

    [data-testid="stChatMessageContent"] p {
        color: #171717;
    }


    /* =========================
       CODE
       ========================= */

    pre {
        background-color: #F7F7F7 !important;
        border: 1px solid #E5E5E5 !important;
        border-radius: 8px !important;
    }

    code {
        font-family:
            "SFMono-Regular",
            "SF Mono",
            Consolas,
            monospace;
    }


    /* =========================
       CHAT INPUT
       ========================= */

    [data-testid="stChatInput"] {
        background-color: #FFFFFF;
    }

    [data-testid="stChatInput"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #D9D9D9 !important;
        border-radius: 14px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }

    [data-testid="stChatInput"] textarea {
        color: #171717 !important;
        font-size: 15px;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #8A8A8A;
    }


    /* =========================
       BUTTONS
       ========================= */

    .stButton button {
        background-color: #FFFFFF !important;
        color: #171717 !important;
        border: 1px solid #D9D9D9 !important;
        border-radius: 8px !important;
    }

    .stButton button:hover {
        background-color: #F2F2F2 !important;
        border-color: #BDBDBD !important;
    }


    /* =========================
       SELECT BOX
       ========================= */

    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border-color: #D9D9D9 !important;
        border-radius: 8px !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">AI Python Tutor</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-description">'
        'Your personal Python learning assistant.'
        '</div>',
        unsafe_allow_html=True
    )

    # New conversation
    if st.button(
        "+ New conversation",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

    st.divider()

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

    difficulty = st.selectbox(
        "Difficulty",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    st.divider()

    st.caption("AI Python Tutor")
    st.caption("Learn • Practice • Understand")


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# MAIN PAGE
# =========================================================

if len(st.session_state.messages) == 0:

    st.markdown(
        '<div class="welcome">'
        '<div class="welcome-title">'
        'How can I help you learn Python?'
        '</div>'
        '<div class="welcome-description">'
        'Ask a question, paste your code, or ask me to explain a concept.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# DISPLAY PREVIOUS MESSAGES
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# =========================================================
# CHAT INPUT
# =========================================================

prompt = st.chat_input("Message AI Python Tutor...")


if prompt:

    # ---------------------------------------------
    # USER MESSAGE
    # ---------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)


    # ---------------------------------------------
    # TEMPORARY AI RESPONSE
    # ---------------------------------------------

    response = (
        "Let's work through that together.\n\n"
        "### Your question\n\n"
        f"> {prompt}\n\n"
        "### Explanation\n\n"
        "I'll explain the concept step by step and keep the "
        "examples simple.\n\n"
        "### Example\n\n"
        "```python\n"
        'name = "Python"\n'
        'print(name)\n'
        "```\n\n"
        "Here, `name` is a variable that stores the text "
        '`"Python"`.\n\n'
        "### Try it yourself\n\n"
        "Change the value of `name` and run the program again."
    )


    # ---------------------------------------------
    # AI MESSAGE
    # ---------------------------------------------

    with st.chat_message("assistant"):
        st.markdown(response)


    # ---------------------------------------------
    # SAVE AI MESSAGE
    # ---------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )
