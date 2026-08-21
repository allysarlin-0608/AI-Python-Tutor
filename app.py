import streamlit as st

# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="AI Python Tutor",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# LIQUID GLASS DESIGN
# ============================================================

st.markdown(
    """
    <style>

    /* --------------------------------------------------------
       GLOBAL
    -------------------------------------------------------- */

    .stApp {
        background:
            radial-gradient(
                circle at 20% 10%,
                rgba(255, 255, 255, 0.95),
                transparent 35%
            ),
            radial-gradient(
                circle at 80% 20%,
                rgba(230, 230, 235, 0.55),
                transparent 35%
            ),
            #f5f5f7;

        color: #1d1d1f;
    }

    .block-container {
        max-width: 1000px;
        padding-top: 40px;
        padding-bottom: 130px;
    }

    header {
        background: transparent !important;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    /* --------------------------------------------------------
       SIDEBAR
    -------------------------------------------------------- */

    section[data-testid="stSidebar"] {
        background: rgba(245, 245, 247, 0.72);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border-right: 1px solid rgba(255, 255, 255, 0.8);
    }

    .sidebar-title {
        font-size: 19px;
        font-weight: 600;
        letter-spacing: -0.3px;
        color: #1d1d1f;
    }

    .sidebar-description {
        font-size: 13px;
        color: #6e6e73;
        margin-top: 4px;
        margin-bottom: 28px;
    }


    /* --------------------------------------------------------
       TITLE
    -------------------------------------------------------- */

    .page-title {
        font-size: 38px;
        font-weight: 600;
        letter-spacing: -1.2px;
        color: #1d1d1f;
        margin-bottom: 6px;
    }

    .page-subtitle {
        font-size: 15px;
        color: #6e6e73;
        margin-bottom: 35px;
    }


    /* --------------------------------------------------------
       WELCOME GLASS
    -------------------------------------------------------- */

    .welcome-glass {
        background: rgba(255, 255, 255, 0.58);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);

        border: 1px solid rgba(255, 255, 255, 0.85);
        border-radius: 28px;

        padding: 55px 40px;
        text-align: center;

        box-shadow:
            0 20px 60px rgba(0, 0, 0, 0.07),
            inset 0 1px 0 rgba(255, 255, 255, 0.9);

        margin-top: 90px;
    }

    .welcome-title {
        font-size: 29px;
        font-weight: 600;
        letter-spacing: -0.7px;
        color: #1d1d1f;
        margin-bottom: 10px;
    }

    .welcome-description {
        font-size: 15px;
        color: #6e6e73;
    }


    /* --------------------------------------------------------
       CHAT
    -------------------------------------------------------- */

    [data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;
        padding: 18px 0 !important;
    }

    [data-testid="stChatMessageContent"] {
        font-size: 15px;
        line-height: 1.75;
        color: #1d1d1f;
    }


    /* --------------------------------------------------------
       CODE BLOCKS
    -------------------------------------------------------- */

    pre {
        background: rgba(235, 235, 237, 0.75) !important;

        border: 1px solid rgba(0, 0, 0, 0.06) !important;

        border-radius: 16px !important;

        padding: 18px !important;

        box-shadow:
            inset 0 1px 0 rgba(255, 255, 255, 0.8);
    }

    code {
        font-family:
            "SFMono-Regular",
            "SF Mono",
            Menlo,
            Monaco,
            Consolas,
            monospace;
    }


    /* --------------------------------------------------------
       CHAT INPUT
    -------------------------------------------------------- */

    [data-testid="stChatInput"] {
        background: transparent !important;
    }

    [data-testid="stChatInput"] > div {
        background: rgba(255, 255, 255, 0.72) !important;

        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);

        border: 1px solid rgba(255, 255, 255, 0.95) !important;

        border-radius: 22px !important;

        box-shadow:
            0 12px 40px rgba(0, 0, 0, 0.10),
            inset 0 1px 0 rgba(255, 255, 255, 0.95);

        padding: 5px !important;
    }

    [data-testid="stChatInput"] textarea {
        color: #1d1d1f !important;
        font-size: 15px;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #8e8e93;
    }


    /* --------------------------------------------------------
       BUTTONS
    -------------------------------------------------------- */

    .stButton > button {
        background: rgba(255, 255, 255, 0.60) !important;

        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);

        color: #1d1d1f !important;

        border: 1px solid rgba(255, 255, 255, 0.90) !important;

        border-radius: 14px !important;

        box-shadow:
            0 4px 15px rgba(0, 0, 0, 0.05),
            inset 0 1px 0 rgba(255, 255, 255, 0.9);

        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.85) !important;

        border-color: rgba(0, 0, 0, 0.08) !important;

        transform: translateY(-1px);
    }


    /* --------------------------------------------------------
       SELECT BOX
    -------------------------------------------------------- */

    div[data-baseweb="select"] > div {
        background: rgba(255, 255, 255, 0.60) !important;

        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);

        border: 1px solid rgba(255, 255, 255, 0.90) !important;

        border-radius: 13px !important;
    }


    /* --------------------------------------------------------
       DIVIDERS
    -------------------------------------------------------- */

    hr {
        border-color: rgba(0, 0, 0, 0.07) !important;
    }


    /* --------------------------------------------------------
       SCROLLBAR
    -------------------------------------------------------- */

    ::-webkit-scrollbar {
        width: 7px;
    }

    ::-webkit-scrollbar-track {
        background: transparent;
    }

    ::-webkit-scrollbar-thumb {
        background: rgba(0, 0, 0, 0.16);
        border-radius: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">AI Python Tutor</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-description">'
        'Learn Python through conversation.'
        '</div>',
        unsafe_allow_html=True
    )

    if st.button(
        "+  New conversation",
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
            "Conditions",
            "Loops",
            "Functions",
            "Lists",
            "Dictionaries",
            "Classes",
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

    st.divider()

    st.caption("AI Python Tutor")
    st.caption("Learn • Practice • Understand")


# ============================================================
# SESSION
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# WELCOME
# ============================================================

if not st.session_state.messages:

    st.markdown(
        """
        <div class="welcome-glass">

            <div class="welcome-title">
                How can I help you learn Python?
            </div>

            <div class="welcome-description">
                Ask a question, paste your code,
                or explore a Python concept.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ============================================================
# INPUT
# ============================================================

prompt = st.chat_input(
    "Message AI Python Tutor..."
)


if prompt:

    # User
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)


    # Temporary tutor response
    response = (
        "Let's work through that together.\n\n"
        "### Your question\n\n"
        f"> {prompt}\n\n"
        "### Explanation\n\n"
        "I'll explain the concept step by step "
        "and keep the example simple.\n\n"
        "### Example\n\n"
        "```python\n"
        'name = "Python"\n'
        'print(name)\n'
        "```\n\n"
        "The variable `name` stores the text "
        '`"Python"`.\n\n'
        "### Try it yourself\n\n"
        "Change the value of `name` and run the program again."
    )


    # AI
    with st.chat_message("assistant"):
        st.markdown(response)


    # Save
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )
