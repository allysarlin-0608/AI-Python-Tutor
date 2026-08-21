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


# ============================================================
# APPLE-INSPIRED LIQUID GLASS DESIGN
# ============================================================

st.markdown(
    """
<style>

/* ==========================================================
   BASE
   ========================================================== */

html, body, [class*="css"] {
    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "SF Pro Display",
        "SF Pro Text",
        "Helvetica Neue",
        Arial,
        sans-serif;
}

.stApp {

    background:
        radial-gradient(
            900px 500px at 15% -10%,
            rgba(255,255,255,0.98),
            transparent 70%
        ),
        radial-gradient(
            700px 500px at 90% 5%,
            rgba(225,225,230,0.65),
            transparent 70%
        ),
        linear-gradient(
            135deg,
            #f7f7f9 0%,
            #f2f2f5 100%
        );

    color: #1d1d1f;
}

.block-container {
    max-width: 1060px;
    padding-top: 48px;
    padding-bottom: 150px;
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

    background:
        linear-gradient(
            180deg,
            rgba(250,250,252,0.78),
            rgba(242,242,245,0.72)
        );

    backdrop-filter: blur(40px) saturate(140%);
    -webkit-backdrop-filter: blur(40px) saturate(140%);

    border-right: 1px solid rgba(0,0,0,0.055);
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

    margin-bottom: 27px;

    font-size: 13px;

    line-height: 1.5;

    color: #6e6e73;
}


/* ==========================================================
   SIDEBAR BUTTON
   ========================================================== */

.stButton > button {

    background:
        rgba(255,255,255,0.68) !important;

    color:
        #1d1d1f !important;

    border:
        1px solid rgba(0,0,0,0.065) !important;

    border-radius:
        13px !important;

    box-shadow:
        0 4px 14px rgba(0,0,0,0.035),
        inset 0 1px 0 rgba(255,255,255,0.95);

    transition:
        transform 180ms ease,
        background 180ms ease,
        box-shadow 180ms ease;
}

.stButton > button:hover {

    background:
        rgba(255,255,255,0.88) !important;

    transform:
        translateY(-1px);

    box-shadow:
        0 7px 20px rgba(0,0,0,0.055),
        inset 0 1px 0 rgba(255,255,255,1);
}

.stButton > button:active {

    transform:
        scale(0.985);
}


/* ==========================================================
   SELECT BOX
   ========================================================== */

div[data-baseweb="select"] > div {

    background:
        rgba(255,255,255,0.65) !important;

    border:
        1px solid rgba(0,0,0,0.065) !important;

    border-radius:
        12px !important;
}


/* ==========================================================
   WELCOME
   ========================================================== */

.welcome {

    position: relative;

    overflow: hidden;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.78),
            rgba(255,255,255,0.48)
        );

    backdrop-filter:
        blur(35px) saturate(145%);

    -webkit-backdrop-filter:
        blur(35px) saturate(145%);

    border:
        1px solid rgba(255,255,255,0.90);

    border-radius:
        28px;

    padding:
        64px 40px 58px;

    text-align:
        center;

    box-shadow:
        0 18px 55px rgba(0,0,0,0.065),
        inset 0 1px 0 rgba(255,255,255,0.98),
        inset 0 -1px 0 rgba(0,0,0,0.025);

    animation:
        fadeUp 500ms cubic-bezier(0.22,1,0.36,1);
}


/* subtle glass reflection */

.welcome::before {

    content: "";

    position: absolute;

    top: -65%;

    left: -10%;

    width: 120%;

    height: 100%;

    background:
        linear-gradient(
            115deg,
            transparent 25%,
            rgba(255,255,255,0.42) 42%,
            transparent 60%
        );

    pointer-events: none;

    opacity: 0.65;
}


.welcome-title {

    position: relative;

    font-size: 30px;

    font-weight: 650;

    letter-spacing: -0.8px;

    color: #1d1d1f;

    margin-bottom: 10px;
}

.welcome-text {

    position: relative;

    font-size: 15px;

    color: #6e6e73;
}


/* ==========================================================
   MODE SECTION
   ========================================================== */

.mode-section {

    margin-top: 28px;

    margin-bottom: 10px;
}

.mode-label {

    font-size: 13px;

    font-weight: 600;

    color: #6e6e73;

    letter-spacing: 0.1px;

    margin-bottom: 12px;
}


/* ==========================================================
   MODE CARDS
   ========================================================== */

.mode-card {

    position: relative;

    overflow: hidden;

    height: 205px;

    box-sizing: border-box;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.76),
            rgba(255,255,255,0.48)
        );

    backdrop-filter:
        blur(28px) saturate(140%);

    -webkit-backdrop-filter:
        blur(28px) saturate(140%);

    border:
        1px solid rgba(255,255,255,0.92);

    border-radius:
        22px;

    padding:
        25px;

    box-shadow:
        0 12px 35px rgba(0,0,0,0.055),
        inset 0 1px 0 rgba(255,255,255,0.98),
        inset 0 -1px 0 rgba(0,0,0,0.025);

    transition:
        transform 220ms cubic-bezier(0.22,1,0.36,1),
        box-shadow 220ms ease,
        background 220ms ease;
}


/* reflection */

.mode-card::before {

    content: "";

    position: absolute;

    top: -60px;

    left: -30%;

    width: 160%;

    height: 80px;

    background:
        linear-gradient(
            105deg,
            transparent 25%,
            rgba(255,255,255,0.42),
            transparent 70%
        );

    opacity: 0.55;

    pointer-events: none;
}


/* hover */

.mode-card:hover {

    transform:
        translateY(-4px);

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.88),
            rgba(255,255,255,0.58)
        );

    box-shadow:
        0 18px 45px rgba(0,0,0,0.075),
        inset 0 1px 0 rgba(255,255,255,1),
        inset 0 -1px 0 rgba(0,0,0,0.02);
}


/* ==========================================================
   ICON
   ========================================================== */

.mode-icon {

    position: relative;

    width: 42px;

    height: 42px;

    display: flex;

    align-items: center;

    justify-content: center;

    background:
        rgba(245,245,247,0.78);

    border:
        1px solid rgba(0,0,0,0.055);

    border-radius:
        12px;

    color:
        #1d1d1f;

    margin-bottom:
        18px;

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.95);

    transition:
        transform 220ms cubic-bezier(0.22,1,0.36,1);
}

.mode-card:hover .mode-icon {

    transform:
        scale(1.07)
        translateY(-1px);
}


/* ==========================================================
   MODE TEXT
   ========================================================== */

.mode-title {

    font-size:
        16px;

    font-weight:
        600;

    color:
        #1d1d1f;

    margin-bottom:
        7px;
}

.mode-description {

    font-size:
        13px;

    line-height:
        1.55;

    color:
        #6e6e73;
}


/* ==========================================================
   MODE BUTTON AREA
   ========================================================== */

.mode-action {

    margin-top:
        18px;
}


/* Make action buttons subtle */

.mode-action .stButton > button {

    height:
        38px;

    border-radius:
        11px !important;

    font-size:
        13px !important;

    background:
        rgba(255,255,255,0.55) !important;
}


/* ==========================================================
   CHAT
   ========================================================== */

[data-testid="stChatMessage"] {

    background:
        transparent !important;

    border:
        none !important;

    padding:
        18px 0 !important;
}

[data-testid="stChatMessageContent"] {

    max-width:
        790px;

    color:
        #1d1d1f;

    font-size:
        15px;

    line-height:
        1.75;
}


/* ==========================================================
   USER MESSAGE
   ========================================================== */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) {

    background:
        rgba(255,255,255,0.52) !important;

    border:
        1px solid rgba(255,255,255,0.75) !important;

    border-radius:
        18px !important;

    padding:
        15px 18px !important;

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.85);
}


/* ==========================================================
   CODE BLOCK
   ========================================================== */

pre {

    background:
        rgba(235,235,237,0.78) !important;

    border:
        1px solid rgba(0,0,0,0.055) !important;

    border-radius:
        15px !important;

    padding:
        17px !important;

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.85);
}


/* ==========================================================
   INPUT
   ========================================================== */

[data-testid="stChatInput"] {

    background:
        transparent !important;
}

[data-testid="stChatInput"] > div {

    background:
        rgba(255,255,255,0.78) !important;

    backdrop-filter:
        blur(32px) saturate(140%);

    -webkit-backdrop-filter:
        blur(32px) saturate(140%);

    border:
        1px solid rgba(255,255,255,0.95) !important;

    border-radius:
        22px !important;

    box-shadow:
        0 14px 45px rgba(0,0,0,0.09),
        inset 0 1px 0 rgba(255,255,255,1);
}


/* ==========================================================
   ANIMATION
   ========================================================== */

@keyframes fadeUp {

    from {
        opacity: 0;
        transform: translateY(12px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
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

    background:
        rgba(0,0,0,0.13);

    border-radius:
        20px;
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
        'Learn Python through a focused AI tutor.'
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
            "Conditions",
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

    st.caption("Mode")
    st.write(st.session_state.mode)

    st.caption("Topic")
    st.write(topic)

    st.caption("Level")
    st.write(difficulty)


# ============================================================
# MAIN
# ============================================================

if not st.session_state.messages:

    st.markdown(
        '<div class="welcome">'
        '<div class="welcome-title">'
        'How can I help you learn Python?'
        '</div>'
        '<div class="welcome-text">'
        'Choose a mode to begin.'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="mode-section">'
        '<div class="mode-label">Choose how you want to learn</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # THREE EQUAL CARDS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(
        3,
        gap="medium"
    )


    # ========================================================
    # LEARN
    # ========================================================

    with col1:

        st.markdown(
            '<div class="mode-card">'
            '<div class="mode-icon">'
            '◎'
            '</div>'
            '<div class="mode-title">'
            'Learn'
            '</div>'
            '<div class="mode-description">'
            'Understand Python concepts through '
            'clear explanations, examples, and '
            'step-by-step guidance.'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="mode-action">',
            unsafe_allow_html=True,
        )

        if st.button(
            "Start learning",
            key="learn",
            use_container_width=True,
        ):

            st.session_state.mode = "Learn"

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content":
                        "### Learn\n\n"
                        "What Python concept would you like "
                        "to understand?"
                }
            )

            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)


    # ========================================================
    # PRACTICE
    # ========================================================

    with col2:

        st.markdown(
            '<div class="mode-card">'
            '<div class="mode-icon">'
            '△'
            '</div>'
            '<div class="mode-title">'
            'Practice'
            '</div>'
            '<div class="mode-description">'
            'Build your programming skills with '
            'questions and exercises matched '
            'to your level.'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="mode-action">',
            unsafe_allow_html=True,
        )

        if st.button(
            "Start practice",
            key="practice",
            use_container_width=True,
        ):

            st.session_state.mode = "Practice"

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content":
                        "### Practice\n\n"
                        f"Let's practice **{topic}** "
                        f"at the **{difficulty}** level.\n\n"
                        "I'll give you one problem at a time."
                }
            )

            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)


    # ========================================================
    # DEBUG
    # ========================================================

    with col3:

        st.markdown(
            '<div class="mode-card">'
            '<div class="mode-icon">'
            '</>'
            '</div>'
            '<div class="mode-title">'
            'Debug'
            '</div>'
            '<div class="mode-description">'
            'Find errors in your Python code and '
            'understand exactly why they happen '
            'and how to fix them.'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="mode-action">',
            unsafe_allow_html=True,
        )

        if st.button(
            "Start debugging",
            key="debug",
            use_container_width=True,
        ):

            st.session_state.mode = "Debug"

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content":
                        "### Debug\n\n"
                        "Paste your Python code here.\n\n"
                        "I'll help you understand the error, "
                        "find its cause, and fix it."
                }
            )

            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )


# ============================================================
# CHAT INPUT
# ============================================================

prompt = st.chat_input(
    "Message AI Python Tutor..."
)


if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)


    # --------------------------------------------------------
    # TEMPORARY AI RESPONSES
    # --------------------------------------------------------

    if st.session_state.mode == "Learn":

        response = (
            "### Let's work through it\n\n"
            f"You asked about **{prompt}**.\n\n"
            "I'll start with the simplest explanation "
            "and then connect it to Python.\n\n"
            "```python\n"
            'message = "Hello, Python!"\n'
            "print(message)\n"
            "```\n\n"
            "The variable `message` stores a value, "
            "and `print()` displays it.\n\n"
            "**Key idea:**\n"
            "Understand the concept first, then practice it."
        )

    elif st.session_state.mode == "Practice":

        response = (
            f"### Practice\n\n"
            f"Topic: **{topic}**\n\n"
            f"Level: **{difficulty}**\n\n"
            "Here's your next problem:\n\n"
            "Create a Python variable and print its value.\n\n"
            "Try it yourself first."
        )

    else:

        response = (
            "### Debug\n\n"
            "Paste your Python code here.\n\n"
            "I'll check:\n\n"
            "- What the error means\n"
            "- Where the problem occurs\n"
            "- Why it happens\n"
            "- How to fix it\n"
            "- How to avoid the problem next time"
        )


    with st.chat_message("assistant"):

        st.markdown(response)


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )
