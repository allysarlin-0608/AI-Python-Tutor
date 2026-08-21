import streamlit as st

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Python Tutor",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# APPLE-INSPIRED LIQUID GLASS CSS
# ============================================================

st.markdown(
    """
<style>

/* ==========================================================
   ROOT
   ========================================================== */

:root {
    --background: #f5f5f7;
    --surface: rgba(255, 255, 255, 0.72);
    --surface-strong: rgba(255, 255, 255, 0.88);
    --border: rgba(0, 0, 0, 0.08);
    --text: #1d1d1f;
    --secondary: #6e6e73;
    --muted: #86868b;
}


/* ==========================================================
   APP BACKGROUND
   ========================================================== */

.stApp {
    background:
        radial-gradient(
            circle at 10% 0%,
            rgba(255,255,255,0.95),
            transparent 28%
        ),
        radial-gradient(
            circle at 90% 10%,
            rgba(225,225,230,0.75),
            transparent 30%
        ),
        #f5f5f7;

    color: var(--text);
}


/* ==========================================================
   MAIN CONTENT
   ========================================================== */

.block-container {
    max-width: 1050px;
    padding-top: 48px;
    padding-bottom: 150px;
}


/* ==========================================================
   REMOVE DEFAULT STREAMLIT BRANDING
   ========================================================== */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}


/* ==========================================================
   SIDEBAR
   ========================================================== */

section[data-testid="stSidebar"] {

    background: rgba(246, 246, 248, 0.72);

    backdrop-filter: blur(35px);
    -webkit-backdrop-filter: blur(35px);

    border-right: 1px solid rgba(0, 0, 0, 0.06);
}

section[data-testid="stSidebar"] > div {
    padding: 28px 20px;
}


/* Sidebar title */

.sidebar-brand {
    font-size: 19px;
    font-weight: 650;
    letter-spacing: -0.4px;
    color: #1d1d1f;
}

.sidebar-caption {
    margin-top: 4px;
    margin-bottom: 28px;
    color: #6e6e73;
    font-size: 13px;
    line-height: 1.5;
}


/* ==========================================================
   NEW CHAT BUTTON
   ========================================================== */

.stButton > button {

    width: 100%;

    background: rgba(255,255,255,0.68) !important;

    color: #1d1d1f !important;

    border: 1px solid rgba(0,0,0,0.07) !important;

    border-radius: 14px !important;

    padding: 10px 14px !important;

    font-size: 14px !important;

    box-shadow:
        0 4px 15px rgba(0,0,0,0.04),
        inset 0 1px 0 rgba(255,255,255,0.9);

    transition:
        transform 0.18s ease,
        background 0.18s ease,
        box-shadow 0.18s ease;
}

.stButton > button:hover {

    background: rgba(255,255,255,0.92) !important;

    transform: translateY(-1px);

    box-shadow:
        0 8px 25px rgba(0,0,0,0.07),
        inset 0 1px 0 rgba(255,255,255,1);
}


/* ==========================================================
   SELECT BOXES
   ========================================================== */

div[data-baseweb="select"] > div {

    background: rgba(255,255,255,0.68) !important;

    border: 1px solid rgba(0,0,0,0.07) !important;

    border-radius: 13px !important;

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.9);
}


/* ==========================================================
   MAIN HEADER
   ========================================================== */

.main-heading {

    font-size: 42px;

    font-weight: 650;

    letter-spacing: -1.5px;

    color: #1d1d1f;

    margin-bottom: 4px;
}

.main-subheading {

    font-size: 16px;

    color: #6e6e73;

    margin-bottom: 35px;
}


/* ==========================================================
   GLASS WELCOME PANEL
   ========================================================== */

.welcome-panel {

    background: rgba(255,255,255,0.58);

    backdrop-filter: blur(35px);
    -webkit-backdrop-filter: blur(35px);

    border: 1px solid rgba(255,255,255,0.92);

    border-radius: 30px;

    padding: 65px 45px;

    text-align: center;

    box-shadow:
        0 25px 70px rgba(0,0,0,0.07),
        inset 0 1px 0 rgba(255,255,255,0.95);

    margin-top: 70px;
}

.welcome-title {

    font-size: 30px;

    font-weight: 650;

    letter-spacing: -0.8px;

    color: #1d1d1f;

    margin-bottom: 12px;
}

.welcome-description {

    font-size: 15px;

    color: #6e6e73;

    line-height: 1.6;
}


/* ==========================================================
   FEATURE CARDS
   ========================================================== */

.feature-card {

    background: rgba(255,255,255,0.52);

    backdrop-filter: blur(25px);
    -webkit-backdrop-filter: blur(25px);

    border: 1px solid rgba(255,255,255,0.9);

    border-radius: 20px;

    padding: 22px;

    box-shadow:
        0 12px 35px rgba(0,0,0,0.045),
        inset 0 1px 0 rgba(255,255,255,0.9);
}

.feature-title {

    font-size: 15px;

    font-weight: 600;

    color: #1d1d1f;

    margin-bottom: 6px;
}

.feature-text {

    font-size: 13px;

    color: #6e6e73;

    line-height: 1.5;
}


/* ==========================================================
   CHAT
   ========================================================== */

[data-testid="stChatMessage"] {

    background: transparent !important;

    border: none !important;

    padding-top: 18px !important;

    padding-bottom: 18px !important;
}


[data-testid="stChatMessageContent"] {

    color: #1d1d1f;

    font-size: 15px;

    line-height: 1.75;

    max-width: 780px;
}


/* ==========================================================
   USER MESSAGE
   ========================================================== */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) {

    background: rgba(255,255,255,0.40) !important;

    border-radius: 20px !important;

    padding: 15px 18px !important;

    margin: 5px 0 !important;
}


/* ==========================================================
   CODE
   ========================================================== */

pre {

    background: rgba(235,235,237,0.78) !important;

    border: 1px solid rgba(0,0,0,0.06) !important;

    border-radius: 16px !important;

    padding: 18px !important;

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.8);
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


/* ==========================================================
   CHAT INPUT
   ========================================================== */

[data-testid="stChatInput"] {

    background: transparent !important;
}


[data-testid="stChatInput"] > div {

    background: rgba(255,255,255,0.76) !important;

    backdrop-filter: blur(30px);
    -webkit-backdrop-filter: blur(30px);

    border: 1px solid rgba(255,255,255,0.95) !important;

    border-radius: 23px !important;

    box-shadow:
        0 12px 45px rgba(0,0,0,0.10),
        inset 0 1px 0 rgba(255,255,255,1);

    padding: 5px !important;
}


[data-testid="stChatInput"] textarea {

    color: #1d1d1f !important;

    font-size: 15px !important;
}


[data-testid="stChatInput"] textarea::placeholder {

    color: #8e8e93 !important;
}


/* ==========================================================
   DIVIDERS
   ========================================================== */

hr {

    border-color: rgba(0,0,0,0.06) !important;
}


/* ==========================================================
   SCROLLBAR
   ========================================================== */

::-webkit-scrollbar {
    width: 7px;
}

::-webkit-scrollbar-track {
    background: transparent;
}

::-webkit-scrollbar-thumb {

    background: rgba(0,0,0,0.14);

    border-radius: 20px;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-brand">AI Python Tutor</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-caption">'
        'A simple environment for learning Python.'
        '</div>',
        unsafe_allow_html=True,
    )

    if st.button(
        "+  New conversation",
        use_container_width=True,
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
            "Operators",
            "If Statements",
            "Loops",
            "Functions",
            "Lists",
            "Dictionaries",
            "Classes & Objects",
            "Debugging",
        ],
    )

    difficulty = st.selectbox(
        "Difficulty",
        [
            "Beginner",
            "Intermediate",
            "Advanced",
        ],
    )

    st.divider()

    st.caption("Current topic")
    st.write(topic)

    st.caption("Current level")
    st.write(difficulty)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ============================================================
# MAIN HEADER
# ============================================================

if st.session_state.messages:

    st.markdown(
        '<div class="main-heading">AI Python Tutor</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="main-subheading">'
        'Learn Python through conversation.'
        '</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# WELCOME SCREEN
# ============================================================

if not st.session_state.messages:

    st.markdown(
        '<div class="welcome-panel">'
        '<div class="welcome-title">'
        'How can I help you learn Python?'
        '</div>'
        '<div class="welcome-description">'
        'Ask a question, paste your code, '
        'or explore a Python concept.'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            '<div class="feature-card">'
            '<div class="feature-title">'
            'Learn'
            '</div>'
            '<div class="feature-text">'
            'Understand Python concepts with '
            'clear explanations.'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            '<div class="feature-card">'
            '<div class="feature-title">'
            'Practice'
            '</div>'
            '<div class="feature-text">'
            'Solve small programming exercises '
            'and build your skills.'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )

    with col3:

        st.markdown(
            '<div class="feature-card">'
            '<div class="feature-title">'
            'Debug'
            '</div>'
            '<div class="feature-text">'
            'Paste your code and understand '
            'why something is not working.'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ============================================================
# CHAT INPUT
# ============================================================

prompt = st.chat_input(
    "Message AI Python Tutor..."
)


if prompt:

    # --------------------------------------------------------
    # USER
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)


    # --------------------------------------------------------
    # TEMPORARY TUTOR RESPONSE
    # --------------------------------------------------------

    response = (
        "Let's work through this step by step.\n\n"
        "### Your question\n\n"
        f"> {prompt}\n\n"
        "### Explanation\n\n"
        "I'll explain the idea in simple terms first, "
        "then connect it to Python.\n\n"
        "### Example\n\n"
        "```python\n"
        'name = "Python"\n'
        'print(name)\n'
        "```\n\n"
        "The variable `name` stores the value "
        '`"Python"`.\n\n'
        "### Practice\n\n"
        "Try changing the value of `name` and "
        "run the program again."
    )


    # --------------------------------------------------------
    # ASSISTANT
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        st.markdown(response)


    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )
