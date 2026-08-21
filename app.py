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
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "mode" not in st.session_state:
    st.session_state.mode = "Learn"

if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = "Python Basics"


# ============================================================
# LIQUID GLASS DESIGN
# ============================================================

st.markdown(
    """
<style>

/* ==========================================================
   GLOBAL
   ========================================================== */

.stApp {
    background:
        radial-gradient(
            circle at 15% 5%,
            rgba(255, 255, 255, 0.95),
            transparent 30%
        ),
        radial-gradient(
            circle at 85% 10%,
            rgba(225, 225, 230, 0.70),
            transparent 30%
        ),
        #f5f5f7;

    color: #1d1d1f;
}

.block-container {
    max-width: 1050px;
    padding-top: 45px;
    padding-bottom: 140px;
}

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

.sidebar-brand {
    font-size: 19px;
    font-weight: 650;
    letter-spacing: -0.4px;
    color: #1d1d1f;
}

.sidebar-description {
    margin-top: 5px;
    margin-bottom: 28px;

    color: #6e6e73;
    font-size: 13px;
    line-height: 1.5;
}


/* ==========================================================
   BUTTONS
   ========================================================== */

.stButton > button {

    width: 100%;

    background: rgba(255, 255, 255, 0.68) !important;

    color: #1d1d1f !important;

    border: 1px solid rgba(0, 0, 0, 0.07) !important;

    border-radius: 14px !important;

    padding: 10px 14px !important;

    font-size: 14px !important;

    box-shadow:
        0 5px 18px rgba(0, 0, 0, 0.04),
        inset 0 1px 0 rgba(255, 255, 255, 0.9);

    transition:
        transform 0.18s ease,
        background 0.18s ease,
        box-shadow 0.18s ease;
}

.stButton > button:hover {

    background: rgba(255, 255, 255, 0.92) !important;

    transform: translateY(-2px);

    box-shadow:
        0 10px 28px rgba(0, 0, 0, 0.07),
        inset 0 1px 0 rgba(255, 255, 255, 1);
}

.stButton > button:active {

    transform: scale(0.97);
}


/* ==========================================================
   SELECT BOX
   ========================================================== */

div[data-baseweb="select"] > div {

    background: rgba(255, 255, 255, 0.70) !important;

    border: 1px solid rgba(0, 0, 0, 0.07) !important;

    border-radius: 13px !important;

    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.9);
}


/* ==========================================================
   MAIN TITLE
   ========================================================== */

.main-title {

    font-size: 42px;

    font-weight: 650;

    letter-spacing: -1.5px;

    color: #1d1d1f;

    margin-bottom: 6px;
}

.main-subtitle {

    font-size: 16px;

    color: #6e6e73;

    margin-bottom: 30px;
}


/* ==========================================================
   WELCOME GLASS
   ========================================================== */

.welcome {

    background: rgba(255, 255, 255, 0.60);

    backdrop-filter: blur(35px);
    -webkit-backdrop-filter: blur(35px);

    border: 1px solid rgba(255, 255, 255, 0.95);

    border-radius: 30px;

    padding: 65px 40px;

    text-align: center;

    box-shadow:
        0 25px 70px rgba(0, 0, 0, 0.07),
        inset 0 1px 0 rgba(255, 255, 255, 0.95);

    margin-top: 75px;

    animation: appear 0.6s ease;
}

.welcome-title {

    font-size: 30px;

    font-weight: 650;

    letter-spacing: -0.8px;

    color: #1d1d1f;

    margin-bottom: 12px;
}

.welcome-text {

    font-size: 15px;

    color: #6e6e73;

    line-height: 1.6;
}


/* ==========================================================
   MODE CARDS
   ========================================================== */

.mode-card {

    background: rgba(255, 255, 255, 0.58);

    backdrop-filter: blur(28px);
    -webkit-backdrop-filter: blur(28px);

    border: 1px solid rgba(255, 255, 255, 0.92);

    border-radius: 22px;

    padding: 25px;

    min-height: 175px;

    box-shadow:
        0 12px 35px rgba(0, 0, 0, 0.045),
        inset 0 1px 0 rgba(255, 255, 255, 0.95);

    transition:
        transform 0.25s cubic-bezier(0.22, 1, 0.36, 1),
        box-shadow 0.25s ease,
        background 0.25s ease;
}

.mode-card:hover {

    transform:
        translateY(-5px)
        scale(1.015);

    background: rgba(255, 255, 255, 0.78);

    box-shadow:
        0 20px 45px rgba(0, 0, 0, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 1);
}

.mode-icon {

    width: 44px;
    height: 44px;

    display: flex;

    align-items: center;
    justify-content: center;

    background: rgba(245, 245, 247, 0.85);

    border: 1px solid rgba(0, 0, 0, 0.06);

    border-radius: 14px;

    font-size: 20px;

    margin-bottom: 18px;

    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.95);

    transition:
        transform 0.25s cubic-bezier(0.22, 1, 0.36, 1),
        background 0.25s ease;
}

.mode-card:hover .mode-icon {

    transform:
        scale(1.10)
        translateY(-1px);

    background: #ffffff;
}

.mode-title {

    font-size: 16px;

    font-weight: 600;

    color: #1d1d1f;

    margin-bottom: 7px;
}

.mode-description {

    font-size: 13px;

    color: #6e6e73;

    line-height: 1.55;
}


/* ==========================================================
   MODE INDICATOR
   ========================================================== */

.mode-indicator {

    display: inline-block;

    background: rgba(255, 255, 255, 0.70);

    border: 1px solid rgba(0, 0, 0, 0.06);

    border-radius: 20px;

    padding: 7px 13px;

    font-size: 12px;

    color: #6e6e73;

    margin-bottom: 15px;
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

    max-width: 790px;
}


/* ==========================================================
   USER MESSAGE
   ========================================================== */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) {

    background: rgba(255, 255, 255, 0.50) !important;

    border-radius: 20px !important;

    padding: 15px 18px !important;

    margin: 5px 0 !important;
}


/* ==========================================================
   CODE
   ========================================================== */

pre {

    background: rgba(235, 235, 237, 0.78) !important;

    border: 1px solid rgba(0, 0, 0, 0.06) !important;

    border-radius: 16px !important;

    padding: 18px !important;

    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.85);
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

    background: rgba(255, 255, 255, 0.76) !important;

    backdrop-filter: blur(30px);
    -webkit-backdrop-filter: blur(30px);

    border: 1px solid rgba(255, 255, 255, 0.96) !important;

    border-radius: 23px !important;

    box-shadow:
        0 12px 45px rgba(0, 0, 0, 0.10),
        inset 0 1px 0 rgba(255, 255, 255, 1);

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
   ANIMATION
   ========================================================== */

@keyframes appear {

    from {
        opacity: 0;
        transform: translateY(10px) scale(0.985);
    }

    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}


/* ==========================================================
   DIVIDER
   ========================================================== */

hr {

    border-color: rgba(0, 0, 0, 0.06) !important;
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

    background: rgba(0, 0, 0, 0.14);

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
        '<div class="sidebar-description">'
        'Learn Python through conversation.'
        '</div>',
        unsafe_allow_html=True,
    )

    if st.button(
        "+  New conversation",
        use_container_width=True,
    ):
        st.session_state.messages = []
        st.session_state.mode = "Learn"
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

    st.caption("Current mode")
    st.write(st.session_state.mode)

    st.caption("Current topic")
    st.write(topic)

    st.caption("Difficulty")
    st.write(difficulty)


# ============================================================
# MAIN HEADER
# ============================================================

if st.session_state.messages:

    st.markdown(
        '<div class="main-title">AI Python Tutor</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="main-subtitle">'
        'Learn Python through conversation.'
        '</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# WELCOME SCREEN
# ============================================================

if not st.session_state.messages:

    st.markdown(
        '<div class="welcome">'
        '<div class="welcome-title">'
        'How can I help you learn Python?'
        '</div>'
        '<div class="welcome-text">'
        'Choose a learning mode or start a conversation.'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.write("")

    # --------------------------------------------------------
    # MODE CARDS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3, gap="medium")


    with col1:

        st.markdown(
            '<div class="mode-card">'
            '<div class="mode-icon">◇</div>'
            '<div class="mode-title">Learn</div>'
            '<div class="mode-description">'
            'Understand Python concepts with '
            'simple explanations and examples.'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "Start Learning",
            key="learn_button",
            use_container_width=True,
        ):
            st.session_state.mode = "Learn"

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": (
                        "### Learning Mode\n\n"
                        "What Python concept would you like "
                        "to understand?"
                    ),
                }
            )

            st.rerun()


    with col2:

        st.markdown(
            '<div class="mode-card">'
            '<div class="mode-icon">+</div>'
            '<div class="mode-title">Practice</div>'
            '<div class="mode-description">'
            'Practice programming with questions '
            'matched to your current level.'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "Start Practice",
            key="practice_button",
            use_container_width=True,
        ):
            st.session_state.mode = "Practice"

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": (
                        "### Practice Mode\n\n"
                        f"Let's practice **{topic}** "
                        f"at the **{difficulty}** level.\n\n"
                        "I'll give you one problem at a time."
                    ),
                }
            )

            st.rerun()


    with col3:

        st.markdown(
            '<div class="mode-card">'
            '<div class="mode-icon">&lt;/&gt;</div>'
            '<div class="mode-title">Debug</div>'
            '<div class="mode-description">'
            'Find problems in your code and understand '
            'how to fix them.'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "Start Debugging",
            key="debug_button",
            use_container_width=True,
        ):
            st.session_state.mode = "Debug"

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": (
                        "### Debug Mode\n\n"
                        "Paste your Python code here.\n\n"
                        "I'll help you identify the problem, "
                        "explain why it happens, and show you "
                        "how to fix it."
                    ),
                }
            )

            st.rerun()


# ============================================================
# CHAT HISTORY
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
    # USER MESSAGE
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
    # TEMPORARY RESPONSE
    # --------------------------------------------------------

    if st.session_state.mode == "Learn":

        response = (
            "### Let's learn this step by step\n\n"
            f"You asked about **{prompt}**.\n\n"
            "I'll start with the simplest explanation, "
            "then use a Python example.\n\n"
            "```python\n"
            'message = "Hello, Python!"\n'
            "print(message)\n"
            "```\n\n"
            "The variable `message` stores a value, "
            "and `print()` displays that value.\n\n"
            "**Key idea:**\n"
            "Break the problem into small pieces and "
            "understand each piece before moving on."
        )

    elif st.session_state.mode == "Practice":

        response = (
            f"### Practice: {topic}\n\n"
            f"**Level:** {difficulty}\n\n"
            "Here's your next question:\n\n"
            "Write a Python program that creates a "
            "variable and prints its value.\n\n"
            "Don't worry about getting it perfect. "
            "Try it first, and I'll help you improve it."
        )

    else:

        response = (
            "### Debug Mode\n\n"
            "Send me the Python code that isn't working.\n\n"
            "I'll help you identify:\n\n"
            "1. What the error means\n"
            "2. Where the problem is\n"
            "3. Why it happened\n"
            "4. How to fix it\n"
            "5. How to avoid the same problem later"
        )


    # --------------------------------------------------------
    # ASSISTANT
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        st.markdown(response)


    # --------------------------------------------------------
    # SAVE RESPONSE
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )
