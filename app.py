import os
import streamlit as st

try:
    import anthropic
    _ANTHROPIC_AVAILABLE = True
except ImportError:
    _ANTHROPIC_AVAILABLE = False


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Python Tutor",
    page_icon="◎",
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

if "api_key" not in st.session_state:
    st.session_state.api_key = (
        st.secrets.get("ANTHROPIC_API_KEY", "")
        if hasattr(st, "secrets")
        else ""
    ) or os.environ.get("ANTHROPIC_API_KEY", "")


# ============================================================
# AI MODEL LOGIC
# ============================================================

MODEL_NAME = "claude-sonnet-4-6"

SYSTEM_PROMPTS = {
    "Learn": (
        "You are a patient, encouraging Python tutor in 'Learn' mode. "
        "The student is studying the topic '{topic}' at a '{difficulty}' level. "
        "Explain concepts clearly, from first principles, using short, "
        "well-commented Python code examples. Keep answers focused and "
        "avoid overwhelming the student. End with a short check-in question "
        "to confirm understanding."
    ),
    "Practice": (
        "You are a Python tutor in 'Practice' mode. The student wants to "
        "practice '{topic}' at a '{difficulty}' level. Give exactly one "
        "exercise at a time. Do not reveal the solution immediately — "
        "wait for the student's attempt, then give feedback and, only if "
        "asked or if they got it wrong twice, show the correct solution "
        "with an explanation."
    ),
    "Debug": (
        "You are a Python debugging assistant in 'Debug' mode. The student "
        "will paste code and/or an error message. Identify the bug, explain "
        "why it happens in plain language, show the corrected code, and "
        "give one tip to avoid this mistake in the future. Be concise and "
        "concrete."
    ),
}


def get_client():
    """Return an Anthropic client if an API key is available, else None."""
    key = st.session_state.get("api_key", "")
    if not key or not _ANTHROPIC_AVAILABLE:
        return None
    return anthropic.Anthropic(api_key=key)


def build_system_prompt(mode: str, topic: str, difficulty: str) -> str:
    template = SYSTEM_PROMPTS.get(mode, SYSTEM_PROMPTS["Learn"])
    return template.format(topic=topic, difficulty=difficulty)


def to_api_messages(messages):
    """Convert session_state messages into the Anthropic API message format."""
    return [
        {"role": m["role"], "content": m["content"]}
        for m in messages
        if m["role"] in ("user", "assistant")
    ]


def stream_ai_response(client, system_prompt, api_messages):
    """Generator yielding text chunks from the Claude API for st.write_stream."""
    with client.messages.stream(
        model=MODEL_NAME,
        max_tokens=1024,
        system=system_prompt,
        messages=api_messages,
    ) as stream:
        for text in stream.text_stream:
            yield text


# ============================================================
# APPLE-INSPIRED LIQUID GLASS DESIGN — STRICT MONOCHROME
# ============================================================

st.markdown(
    """
<style>

/* ==========================================================
   MONOCHROME PALETTE (strict R=G=B, no hue anywhere)
   ========================================================== */

:root {
    --c-white: #ffffff;
    --c-black: #000000;

    --c-50:  #fafafa;
    --c-100: #f5f5f5;
    --c-150: #eeeeee;
    --c-200: #e5e5e5;
    --c-300: #d4d4d4;
    --c-400: #a3a3a3;
    --c-500: #737373;
    --c-600: #525252;
    --c-700: #3f3f3f;
    --c-800: #262626;
    --c-900: #171717;

    --glass-fill: rgba(255,255,255,0.62);
    --glass-fill-strong: rgba(255,255,255,0.85);
    --glass-border: rgba(255,255,255,0.9);
    --glass-shadow: rgba(0,0,0,0.08);

    --ease-out: cubic-bezier(0.22,1,0.36,1);
}


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
        radial-gradient(900px 500px at 15% -10%, rgba(255,255,255,0.98), transparent 70%),
        radial-gradient(700px 500px at 90% 5%, rgba(229,229,229,0.6), transparent 70%),
        linear-gradient(135deg, var(--c-100) 0%, var(--c-150) 100%);
    color: var(--c-900);
}

.block-container {
    max-width: 1060px;
    padding-top: 48px;
    padding-bottom: 150px;
}

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { background: transparent !important; }

* { scrollbar-width: thin; }


/* ==========================================================
   SIDEBAR
   ========================================================== */

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(250,250,250,0.8), rgba(240,240,240,0.75));
    backdrop-filter: blur(40px) saturate(120%);
    -webkit-backdrop-filter: blur(40px) saturate(120%);
    border-right: 1px solid rgba(0,0,0,0.06);
}

section[data-testid="stSidebar"] > div {
    padding: 28px 20px;
}

.sidebar-brand {
    font-size: 19px;
    font-weight: 650;
    letter-spacing: -0.4px;
    color: var(--c-900);
    display: flex;
    align-items: center;
    gap: 8px;
}

.sidebar-description {
    margin-top: 5px;
    margin-bottom: 24px;
    font-size: 13px;
    line-height: 1.5;
    color: var(--c-500);
}

.sidebar-status {
    display: flex;
    align-items: center;
    gap: 7px;
    font-size: 12px;
    color: var(--c-500);
    margin-top: 4px;
}

.status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--c-900);
    box-shadow: 0 0 0 3px rgba(0,0,0,0.06);
    animation: pulse 2.2s ease-in-out infinite;
}

.status-dot.off {
    background: var(--c-400);
    animation: none;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.35; }
}


/* ==========================================================
   BUTTONS
   ========================================================== */

.stButton > button {
    background: var(--glass-fill) !important;
    color: var(--c-900) !important;
    border: 1px solid rgba(0,0,0,0.07) !important;
    border-radius: 13px !important;
    box-shadow: 0 4px 14px var(--glass-shadow), inset 0 1px 0 rgba(255,255,255,0.95);
    transition: transform 180ms var(--ease-out), background 180ms ease, box-shadow 220ms ease;
}

.stButton > button:hover {
    background: var(--glass-fill-strong) !important;
    transform: translateY(-1px);
    box-shadow: 0 8px 22px rgba(0,0,0,0.1), inset 0 1px 0 rgba(255,255,255,1);
}

.stButton > button:active {
    transform: scale(0.97);
    transition: transform 90ms ease;
}


/* ==========================================================
   INPUTS / SELECT
   ========================================================== */

div[data-baseweb="select"] > div,
.stTextInput input {
    background: rgba(255,255,255,0.65) !important;
    border: 1px solid rgba(0,0,0,0.07) !important;
    border-radius: 12px !important;
    color: var(--c-900) !important;
    transition: box-shadow 200ms ease, border-color 200ms ease;
}

div[data-baseweb="select"]:focus-within > div,
.stTextInput input:focus {
    border-color: rgba(0,0,0,0.25) !important;
    box-shadow: 0 0 0 4px rgba(0,0,0,0.06) !important;
}


/* ==========================================================
   WELCOME
   ========================================================== */

.welcome {
    position: relative;
    overflow: hidden;
    background: linear-gradient(145deg, rgba(255,255,255,0.8), rgba(255,255,255,0.5));
    backdrop-filter: blur(35px) saturate(120%);
    -webkit-backdrop-filter: blur(35px) saturate(120%);
    border: 1px solid rgba(255,255,255,0.92);
    border-radius: 28px;
    padding: 64px 40px 58px;
    text-align: center;
    box-shadow: 0 18px 55px var(--glass-shadow), inset 0 1px 0 rgba(255,255,255,0.98), inset 0 -1px 0 rgba(0,0,0,0.025);
    animation: fadeUp 550ms var(--ease-out);
}

.welcome::before {
    content: "";
    position: absolute;
    top: -65%;
    left: -10%;
    width: 120%;
    height: 100%;
    background: linear-gradient(115deg, transparent 25%, rgba(255,255,255,0.45) 42%, transparent 60%);
    pointer-events: none;
    opacity: 0.6;
    animation: sheen 3.5s ease-in-out infinite;
}

@keyframes sheen {
    0%, 100% { transform: translateX(-4%); opacity: 0.35; }
    50% { transform: translateX(4%); opacity: 0.65; }
}

.welcome-title {
    position: relative;
    font-size: 30px;
    font-weight: 650;
    letter-spacing: -0.8px;
    color: var(--c-900);
    margin-bottom: 10px;
}

.welcome-text {
    position: relative;
    font-size: 15px;
    color: var(--c-500);
}


/* ==========================================================
   MODE SECTION
   ========================================================== */

.mode-section {
    margin-top: 28px;
    margin-bottom: 10px;
    animation: fadeUp 550ms var(--ease-out) 80ms both;
}

.mode-label {
    font-size: 13px;
    font-weight: 600;
    color: var(--c-500);
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
    background: linear-gradient(145deg, rgba(255,255,255,0.78), rgba(255,255,255,0.5));
    backdrop-filter: blur(28px) saturate(120%);
    -webkit-backdrop-filter: blur(28px) saturate(120%);
    border: 1px solid rgba(255,255,255,0.94);
    border-radius: 22px;
    padding: 25px;
    box-shadow: 0 12px 35px var(--glass-shadow), inset 0 1px 0 rgba(255,255,255,0.98), inset 0 -1px 0 rgba(0,0,0,0.025);
    transition: transform 240ms var(--ease-out), box-shadow 240ms ease, background 240ms ease;
    animation: cardIn 520ms var(--ease-out) both;
}

.mode-card.d1 { animation-delay: 60ms; }
.mode-card.d2 { animation-delay: 140ms; }
.mode-card.d3 { animation-delay: 220ms; }

@keyframes cardIn {
    from { opacity: 0; transform: translateY(16px) scale(0.98); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
}

.mode-card::before {
    content: "";
    position: absolute;
    top: -60px;
    left: -30%;
    width: 160%;
    height: 80px;
    background: linear-gradient(105deg, transparent 25%, rgba(255,255,255,0.45), transparent 70%);
    opacity: 0.5;
    pointer-events: none;
}

.mode-card:hover {
    transform: translateY(-5px);
    background: linear-gradient(145deg, rgba(255,255,255,0.92), rgba(255,255,255,0.62));
    box-shadow: 0 20px 48px rgba(0,0,0,0.1), inset 0 1px 0 rgba(255,255,255,1), inset 0 -1px 0 rgba(0,0,0,0.02);
}

.mode-icon {
    position: relative;
    width: 42px;
    height: 42px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--c-100);
    border: 1px solid rgba(0,0,0,0.06);
    border-radius: 12px;
    color: var(--c-900);
    margin-bottom: 18px;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.95);
    transition: transform 240ms var(--ease-out), background 240ms ease;
}

.mode-card:hover .mode-icon {
    transform: scale(1.08) translateY(-1px) rotate(-4deg);
    background: var(--c-900);
    color: var(--c-white);
}

.mode-title {
    font-size: 16px;
    font-weight: 600;
    color: var(--c-900);
    margin-bottom: 7px;
}

.mode-description {
    font-size: 13px;
    line-height: 1.55;
    color: var(--c-500);
}

.mode-action { margin-top: 18px; }

.mode-action .stButton > button {
    height: 38px;
    border-radius: 11px !important;
    font-size: 13px !important;
    background: rgba(255,255,255,0.55) !important;
}


/* ==========================================================
   ACTIVE MODE PILL
   ========================================================== */

.active-mode-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 7px 14px;
    border-radius: 999px;
    background: rgba(255,255,255,0.65);
    border: 1px solid rgba(0,0,0,0.07);
    font-size: 12.5px;
    font-weight: 600;
    color: var(--c-700);
    margin-bottom: 18px;
    animation: fadeUp 400ms var(--ease-out) both;
}

.active-mode-pill .dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--c-900);
}


/* ==========================================================
   CHAT
   ========================================================== */

[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 18px 0 !important;
    animation: msgIn 380ms var(--ease-out) both;
}

@keyframes msgIn {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}

[data-testid="stChatMessageContent"] {
    max-width: 790px;
    color: var(--c-900);
    font-size: 15px;
    line-height: 1.75;
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: rgba(255,255,255,0.55) !important;
    border: 1px solid rgba(255,255,255,0.8) !important;
    border-radius: 18px !important;
    padding: 15px 18px !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.9);
}

[data-testid="chatAvatarIcon-assistant"],
[data-testid="chatAvatarIcon-user"] {
    background: var(--c-900) !important;
    filter: grayscale(1);
}


/* ==========================================================
   CODE BLOCK
   ========================================================== */

pre {
    background: rgba(235,235,235,0.8) !important;
    border: 1px solid rgba(0,0,0,0.06) !important;
    border-radius: 15px !important;
    padding: 17px !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.85);
}

code { color: var(--c-900) !important; }


/* ==========================================================
   CHAT INPUT
   ========================================================== */

[data-testid="stChatInput"] { background: transparent !important; }

[data-testid="stChatInput"] > div {
    background: rgba(255,255,255,0.8) !important;
    backdrop-filter: blur(32px) saturate(120%);
    -webkit-backdrop-filter: blur(32px) saturate(120%);
    border: 1px solid rgba(255,255,255,0.96) !important;
    border-radius: 22px !important;
    box-shadow: 0 14px 45px rgba(0,0,0,0.1), inset 0 1px 0 rgba(255,255,255,1);
    transition: box-shadow 220ms ease, border-color 220ms ease;
}

[data-testid="stChatInput"] > div:focus-within {
    box-shadow: 0 16px 50px rgba(0,0,0,0.14), inset 0 1px 0 rgba(255,255,255,1), 0 0 0 4px rgba(0,0,0,0.05);
}


/* ==========================================================
   SHARED ANIMATIONS
   ========================================================== */

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}


/* ==========================================================
   SCROLLBAR
   ========================================================== */

::-webkit-scrollbar { width: 7px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.14); border-radius: 20px; }

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-brand">◎ AI Python Tutor</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-description">'
        'Learn Python through a focused AI tutor, powered by Claude.'
        '</div>',
        unsafe_allow_html=True,
    )

    client_ready = bool(st.session_state.api_key) and _ANTHROPIC_AVAILABLE

    st.markdown(
        f'<div class="sidebar-status">'
        f'<span class="status-dot{"" if client_ready else " off"}"></span>'
        f'{"Connected to Claude" if client_ready else "Not connected"}'
        f'</div>',
        unsafe_allow_html=True,
    )

    if not client_ready:
        with st.expander("Set API key", expanded=not st.session_state.api_key):
            entered_key = st.text_input(
                "Anthropic API key",
                type="password",
                value=st.session_state.api_key,
                help="Or set ANTHROPIC_API_KEY as an environment variable / secret.",
            )
            if entered_key != st.session_state.api_key:
                st.session_state.api_key = entered_key
                st.rerun()
            if not _ANTHROPIC_AVAILABLE:
                st.caption("Missing package: run `pip install anthropic`.")

    if st.button("+  New conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.mode = "Learn"
        st.rerun()

    st.divider()

    st.markdown("### Learning")

    topic = st.selectbox(
        "Topic",
        [
            "Python Basics", "Variables", "Data Types", "Operators",
            "Conditions", "Loops", "Functions", "Lists",
            "Dictionaries", "Classes & Objects", "Debugging",
        ],
    )

    difficulty = st.selectbox(
        "Difficulty",
        ["Beginner", "Intermediate", "Advanced"],
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
        '<div class="welcome-title">How can I help you learn Python?</div>'
        '<div class="welcome-text">Choose a mode to begin.</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="mode-section">'
        '<div class="mode-label">Choose how you want to learn</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3, gap="medium")

    # ------------------------------------------------------
    # LEARN
    # ------------------------------------------------------
    with col1:
        st.markdown(
            '<div class="mode-card d1">'
            '<div class="mode-icon">◎</div>'
            '<div class="mode-title">Learn</div>'
            '<div class="mode-description">'
            'Understand Python concepts through clear explanations, '
            'examples, and step-by-step guidance.'
            '</div></div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="mode-action">', unsafe_allow_html=True)
        if st.button("Start learning", key="learn", use_container_width=True):
            st.session_state.mode = "Learn"
            st.session_state.messages.append({
                "role": "assistant",
                "content": (
                    "### Learn\n\n"
                    "What Python concept would you like to understand?"
                ),
            })
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ------------------------------------------------------
    # PRACTICE
    # ------------------------------------------------------
    with col2:
        st.markdown(
            '<div class="mode-card d2">'
            '<div class="mode-icon">△</div>'
            '<div class="mode-title">Practice</div>'
            '<div class="mode-description">'
            'Build your programming skills with questions and '
            'exercises matched to your level.'
            '</div></div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="mode-action">', unsafe_allow_html=True)
        if st.button("Start practice", key="practice", use_container_width=True):
            st.session_state.mode = "Practice"
            st.session_state.messages.append({
                "role": "assistant",
                "content": (
                    "### Practice\n\n"
                    f"Let's practice **{topic}** at the **{difficulty}** level.\n\n"
                    "I'll give you one problem at a time."
                ),
            })
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ------------------------------------------------------
    # DEBUG
    # ------------------------------------------------------
    with col3:
        st.markdown(
            '<div class="mode-card d3">'
            '<div class="mode-icon">&lt;/&gt;</div>'
            '<div class="mode-title">Debug</div>'
            '<div class="mode-description">'
            'Find errors in your Python code and understand exactly '
            'why they happen and how to fix them.'
            '</div></div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="mode-action">', unsafe_allow_html=True)
        if st.button("Start debugging", key="debug", use_container_width=True):
            st.session_state.mode = "Debug"
            st.session_state.messages.append({
                "role": "assistant",
                "content": (
                    "### Debug\n\n"
                    "Paste your Python code here.\n\n"
                    "I'll help you understand the error, find its cause, "
                    "and fix it."
                ),
            })
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown(
        f'<div class="active-mode-pill"><span class="dot"></span>{st.session_state.mode} mode</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ============================================================
# CHAT INPUT — REAL AI MODEL CALL
# ============================================================

prompt = st.chat_input("Message AI Python Tutor...")

if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    client = get_client()

    with st.chat_message("assistant"):
        if client is None:
            st.warning(
                "No Claude API key configured. Add one in the sidebar "
                "under **Set API key** to get real AI responses."
            )
            full_response = (
                "I can't reach the Claude API right now — please add an "
                "Anthropic API key in the sidebar and try again."
            )
            st.markdown(full_response)
        else:
            system_prompt = build_system_prompt(
                st.session_state.mode, topic, difficulty
            )
            api_history = to_api_messages(st.session_state.messages)
            try:
                full_response = st.write_stream(
                    stream_ai_response(client, system_prompt, api_history)
                )
            except Exception as e:
                full_response = f"Something went wrong calling Claude: {e}"
                st.error(full_response)

    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )
