# AI-Python-Tutor
A simple AI-powered Python tutor built with Streamlit and an LLM API.

## 每日學習教練（Daily Learning Coach）

A second page in the sidebar (`pages/1_每日學習教練.py`): Allysa's 15–20 minute
daily interest coach. The full coach instructions live in
`coach/system_prompt.md` and are sent as the system prompt, followed by an
auto-generated summary of her learning log.

- **Weekly schedule**: Mon/Fri 時尚、材質與珠寶 · Tue 哲學 · Wed/Sat 看書 ·
  Thu 宇宙學 · Sun 自由主題. 商業計劃 and 股票投資 can be picked any day.
- **Per-topic difficulty**: sessions 1–3 入門, 4–7 中階, 8+ 進階, counted per topic.
- **Learning log**: date, topic, level, completion, the lesson's title and
  延伸提問, and her reflection, saved to `data/learning_log.json`
  (override with `COACH_LOG_PATH`). Streaks count through yesterday so they
  never look broken before today is done. On hosts with a temporary
  filesystem (e.g. Streamlit Cloud), use the sidebar's download / import backup.
- Dates default to `Asia/Taipei` (override with `COACH_TIMEZONE`).

Run tests with `python -m pytest tests`.
