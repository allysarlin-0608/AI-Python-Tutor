import os
import streamlit as st
try:
    import groq
    _GROQ_AVAILABLE = True
except ImportError:
    _GROQ_AVAILABLE = False
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
        st.secrets.get("GROQ_API_KEY", "")
        if hasattr(st, "secrets")
        else ""
    ) or os.environ.get("GROQ_API_KEY", "")
# ============================================================
# AI MODEL LOGIC
# ============================================================
MODEL_NAME = "openai/gpt-oss-120b"
# ------------------------------------------------------------
# BASE_SYSTEM_INSTRUCTION applies to every mode. It's what keeps this
# a *Python tutor* instead of a general-purpose chatbot: it fixes the
# scope (Python/programming only), and sets the academic-integrity rule
# (don't just hand over full solutions to what looks like graded work).
# ------------------------------------------------------------
BASE_SYSTEM_INSTRUCTION = (
    "You are AI Python Tutor, a Python-learning assistant for computer "
    "science students. You only help with Python programming topics: "
    "concepts, syntax, debugging, and practice exercises. If the student "
    "asks about anything outside Python or programming, politely decline "
    "and redirect them back to Python. Never write a complete solution to "
    "what looks like a full graded assignment prompt with no attempt "
    "attached; if the student hasn't shown their own attempted code yet, "
    "ask them to share it first. Be honest about uncertainty rather than "
    "guessing at Python behavior you're not sure of."
)
# Mode-specific behavior. Each template is filled in with the chosen topic.
SYSTEM_PROMPTS = {
    "Learn": (
        "Mode: Learn. The student is studying the topic '{topic}'. Explain "
        "concepts clearly, from first principles, using short, "
        "well-commented Python code examples. Keep answers focused and "
        "avoid overwhelming the student. End with a short check-in question "
        "to confirm understanding."
    ),
    "Practice": (
        "Mode: Practice. The student wants to practice '{topic}'. Give "
        "exactly one exercise at a time. Do not reveal the solution "
        "immediately — wait for the student's attempt, then give feedback "
        "and, only if asked or if they got it wrong twice, show the "
        "correct solution with an explanation."
    ),
    "Debug": (
        "Mode: Debug. The student will paste code and/or an error "
        "message related to '{topic}'. If they've pasted their own "
        "attempted code, identify the bug, explain why it happens in "
        "plain language, show the corrected code, and give one tip to "
        "avoid this mistake in the future. If they've only pasted an "
        "assignment description with no code of their own, ask them to "
        "share their attempt first instead of writing the solution for "
        "them. Be concise and concrete."
    ),
}
# How much the AI should assume the student already knows, per level.
DIFFICULTY_GUIDANCE = {
    "Beginner": (
        "The student is a beginner. Avoid jargon, and when you must use a "
        "technical term (e.g. 'loop', 'index'), briefly explain it the "
        "first time. Use short, heavily commented code examples."
    ),
    "Intermediate": (
        "The student is intermediate. You can use common technical terms "
        "(loops, functions, list comprehensions) without re-explaining "
        "them, but still explain anything more advanced than that."
    ),
    "Advanced": (
        "The student is advanced. You may use technical vocabulary freely "
        "(e.g. OOP terms, decorators, generators) without re-explaining "
        "basics. Keep explanations concise rather than exhaustive."
    ),
}
def get_client():
    """Return a Groq client if an API key is available, else None."""
    key = st.session_state.get("api_key", "")
    if not key or not _GROQ_AVAILABLE:
        return None
    return groq.Groq(api_key=key)
def build_system_prompt(mode: str, topic: str, difficulty: str) -> str:
    """Combine the base scope/integrity rules with the mode's behavior
    and the student's chosen experience level into one system prompt."""
    mode_template = SYSTEM_PROMPTS.get(mode, SYSTEM_PROMPTS["Learn"])
    mode_instruction = mode_template.format(topic=topic)
    depth_instruction = DIFFICULTY_GUIDANCE.get(
        difficulty, DIFFICULTY_GUIDANCE["Beginner"]
    )
    return (
        f"{BASE_SYSTEM_INSTRUCTION}\n\n"
        f"{mode_instruction}\n\n"
        f"{depth_instruction}"
    )
def to_api_messages(messages):
    """Convert session_state messages into the Groq API message format."""
    return [
        {"role": m["role"], "content": m["content"]}
        for m in messages
        if m["role"] in ("user", "assistant")
    ]
def stream_ai_response(client, system_prompt, api_messages):
    """Generator yielding text chunks from the Groq API for st.write_stream."""
    full_messages = [{"role": "system", "content": system_prompt}] + api_messages
    stream = client.chat.completions.create(
        model=MODEL_NAME,
        max_tokens=1024,
        messages=full_messages,
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta
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
    --c-50:  #050505;
    --c-100: #0c0c0c;
    --c-150: #121212;
    --c-200: #181818;
    --c-300: #292929;
    --c-400: #565656;
    --c-500: #9a9a9a;
    --c-600: #bdbdbd;
    --c-700: #d8d8d8;
    --c-800: #ececec;
    --c-900: #f5f5f5;
    --glass-fill: rgba(255,255,255,0.09);
    --glass-fill-strong: rgba(255,255,255,0.14);
    --glass-border: rgba(255,255,255,0.16);
    --glass-shadow: rgba(0,0,0,0.55);
    --glass-edge: rgba(0,0,0,0.4);
    --glass-highlight: rgba(255,255,255,0.16);
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
        radial-gradient(900px 500px at 15% -10%, rgba(255,255,255,0.05), transparent 70%),
        radial-gradient(700px 500px at 90% 5%, rgba(255,255,255,0.03), transparent 70%),
        linear-gradient(135deg, #000000 0%, var(--c-100) 100%);
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
    background: linear-gradient(180deg, rgba(10,10,10,0.92), rgba(0,0,0,0.97));
    backdrop-filter: blur(54px) saturate(140%);
    -webkit-backdrop-filter: blur(54px) saturate(140%);
    border-right: 1px solid rgba(255,255,255,0.1);
    box-shadow: inset -1px 0 0 var(--glass-edge);
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
    box-shadow: 0 0 0 3px rgba(255,255,255,0.08);
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
    backdrop-filter: blur(22px) saturate(140%);
    -webkit-backdrop-filter: blur(22px) saturate(140%);
    border: 1px solid rgba(255,255,255,0.14) !important;
    border-radius: 14px !important;
    box-shadow: 0 4px 14px var(--glass-shadow), 0 0 0 1px var(--glass-edge), inset 0 1px 0 var(--glass-highlight);
    transition: transform 180ms var(--ease-out), background 180ms ease, box-shadow 220ms ease;
}
.stButton > button:hover {
    background: var(--glass-fill-strong) !important;
    transform: translateY(-1px);
    box-shadow: 0 8px 22px rgba(0,0,0,0.45), 0 0 0 1px var(--glass-edge), inset 0 1px 0 rgba(255,255,255,0.22);
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
    background: rgba(255,255,255,0.08) !important;
    backdrop-filter: blur(20px) saturate(140%);
    -webkit-backdrop-filter: blur(20px) saturate(140%);
    border: 1px solid rgba(255,255,255,0.14) !important;
    border-radius: 12px !important;
    color: var(--c-900) !important;
    transition: box-shadow 200ms ease, border-color 200ms ease;
}
div[data-baseweb="select"]:focus-within > div,
.stTextInput input:focus {
    border-color: rgba(255,255,255,0.4) !important;
    box-shadow: 0 0 0 4px rgba(255,255,255,0.1) !important;
}
/* ==========================================================
   WELCOME
   ========================================================== */
.welcome {
    position: relative;
    overflow: hidden;
    background: linear-gradient(145deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03));
    backdrop-filter: blur(48px) saturate(140%);
    -webkit-backdrop-filter: blur(48px) saturate(140%);
    border: 1px solid rgba(255,255,255,0.14);
    border-radius: 32px;
    padding: 64px 40px 58px;
    text-align: center;
    box-shadow: 0 18px 55px var(--glass-shadow), 0 0 0 1px var(--glass-edge), inset 0 1px 0 var(--glass-highlight), inset 0 -1px 0 rgba(0,0,0,0.35);
    animation: fadeUp 550ms var(--ease-out);
}
.welcome::before {
    content: "";
    position: absolute;
    top: -65%;
    left: -10%;
    width: 120%;
    height: 100%;
    background: linear-gradient(115deg, transparent 25%, rgba(255,255,255,0.1) 42%, transparent 60%);
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
    background: linear-gradient(145deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03));
    backdrop-filter: blur(40px) saturate(140%);
    -webkit-backdrop-filter: blur(40px) saturate(140%);
    border: 1px solid rgba(255,255,255,0.14);
    border-radius: 26px;
    padding: 25px;
    box-shadow: 0 12px 35px var(--glass-shadow), 0 0 0 1px var(--glass-edge), inset 0 1px 0 var(--glass-highlight), inset 0 -1px 0 rgba(0,0,0,0.35);
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
    background: linear-gradient(105deg, transparent 25%, rgba(255,255,255,0.1), transparent 70%);
    opacity: 0.5;
    pointer-events: none;
}
.mode-card:hover {
    transform: translateY(-5px);
    background: linear-gradient(145deg, rgba(255,255,255,0.13), rgba(255,255,255,0.06));
    box-shadow: 0 20px 48px rgba(0,0,0,0.45), 0 0 0 1px var(--glass-edge), inset 0 1px 0 rgba(255,255,255,0.22), inset 0 -1px 0 rgba(0,0,0,0.3);
}
.mode-icon {
    position: relative;
    width: 42px;
    height: 42px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.14);
    border-radius: 13px;
    color: var(--c-900);
    margin-bottom: 18px;
    box-shadow: 0 0 0 1px var(--glass-edge), inset 0 1px 0 var(--glass-highlight);
    transition: transform 240ms var(--ease-out), background 240ms ease;
}
.mode-card:hover .mode-icon {
    transform: scale(1.08) translateY(-1px) rotate(-4deg);
    background: var(--c-900);
    color: var(--c-black);
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
    background: rgba(255,255,255,0.06) !important;
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
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(20px) saturate(140%);
    -webkit-backdrop-filter: blur(20px) saturate(140%);
    border: 1px solid rgba(255,255,255,0.16);
    box-shadow: 0 0 0 1px var(--glass-edge);
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
    background: rgba(255,255,255,0.09) !important;
    backdrop-filter: blur(28px) saturate(140%);
    -webkit-backdrop-filter: blur(28px) saturate(140%);
    border: 1px solid rgba(255,255,255,0.16) !important;
    border-radius: 20px !important;
    padding: 15px 18px !important;
    box-shadow: 0 0 0 1px var(--glass-edge), inset 0 1px 0 var(--glass-highlight);
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
    background: rgba(255,255,255,0.07) !important;
    backdrop-filter: blur(18px) saturate(140%);
    -webkit-backdrop-filter: blur(18px) saturate(140%);
    border: 1px solid rgba(255,255,255,0.13) !important;
    border-radius: 16px !important;
    padding: 17px !important;
    box-shadow: 0 0 0 1px var(--glass-edge), inset 0 1px 0 rgba(255,255,255,0.08);
}
code { color: var(--c-900) !important; }
/* ==========================================================
   CHAT INPUT
   ========================================================== */
[data-testid="stChatInput"] { background: transparent !important; }
[data-testid="stChatInput"] > div {
    background: rgba(255,255,255,0.09) !important;
    backdrop-filter: blur(46px) saturate(140%);
    -webkit-backdrop-filter: blur(46px) saturate(140%);
    border: 1px solid rgba(255,255,255,0.16) !important;
    border-radius: 24px !important;
    box-shadow: 0 14px 45px rgba(0,0,0,0.45), 0 0 0 1px var(--glass-edge), inset 0 1px 0 var(--glass-highlight);
    transition: box-shadow 220ms ease, border-color 220ms ease;
}
[data-testid="stChatInput"] > div:focus-within {
    box-shadow: 0 16px 50px rgba(0,0,0,0.55), 0 0 0 1px var(--glass-edge), inset 0 1px 0 rgba(255,255,255,0.22), 0 0 0 4px rgba(255,255,255,0.1);
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
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.18); border-radius: 20px; }
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
        'A focused Python tutor — explains concepts, builds practice '
        'exercises, and debugs your code. Not a general chatbot.'
        '</div>',
        unsafe_allow_html=True,
    )
    client_ready = bool(st.session_state.api_key) and _GROQ_AVAILABLE
    st.markdown(
        f'<div class="sidebar-status">'
        f'<span class="status-dot{"" if client_ready else " off"}"></span>'
        f'{"Connected to Groq" if client_ready else "Not connected"}'
        f'</div>',
        unsafe_allow_html=True,
    )
    if not client_ready:
        with st.expander("Set API key", expanded=not st.session_state.api_key):
            entered_key = st.text_input(
                "Groq API key",
                type="password",
                value=st.session_state.api_key,
                help="Or set GROQ_API_KEY as an environment variable / secret.",
            )
            if entered_key != st.session_state.api_key:
                st.session_state.api_key = entered_key
                st.rerun()
            if not _GROQ_AVAILABLE:
                st.caption("Missing package: run `pip install groq`.")
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
# Handle empty / whitespace-only input explicitly rather than silently
# sending it to the API (st.chat_input blocks a fully empty submit, but
# a message of just spaces can still get through).
if prompt is not None and prompt.strip() == "":
    st.warning("Please type a question before sending.")
elif prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    client = get_client()
    with st.chat_message("assistant"):
        if client is None:
            st.warning(
                "No Groq API key configured. Add one in the sidebar "
                "under **Set API key** to get real AI responses."
            )
            full_response = (
                "I can't reach the Groq API right now — please add a "
                "Groq API key in the sidebar and try again."
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
                full_response = f"Something went wrong calling Groq: {e}"
                st.error(full_response)
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )
