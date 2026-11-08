"""Pure logic for the daily learning coach: weekly schedule, per-topic
difficulty, streaks, the learning log, and the history context handed to
the model. Nothing in here imports Streamlit, so it can be unit tested."""
import json
import os
import re
from datetime import date, timedelta
from pathlib import Path

SYSTEM_PROMPT_PATH = Path(__file__).with_name("system_prompt.md")
DEFAULT_LOG_PATH = Path(
    os.environ.get(
        "COACH_LOG_PATH",
        Path(__file__).resolve().parent.parent / "data" / "learning_log.json",
    )
)

# Topic keys map to the seven areas in part 4 of the system prompt.
TOPICS = {
    "fashion": "時尚、材質與珠寶",
    "philosophy": "哲學",
    "reading": "看書",
    "cosmos": "宇宙學、維度理論與地外文明",
    "business": "商業計劃",
    "investing": "股票、投資與加密貨幣",
    "free": "自由主題",
}

# date.weekday(): Monday == 0. Business and investing have no fixed day;
# they only run when she picks them.
WEEKDAY_TOPIC = {
    0: "fashion",
    1: "philosophy",
    2: "reading",
    3: "cosmos",
    4: "fashion",
    5: "reading",
    6: "free",
}
WEEKDAY_ZH = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]

LEVELS = ("入門", "中階", "進階")
CLOSING_LINE = "完成後記得打勾，連續完成比完美更重要。"
SECTION_NAMES = ("今日主題", "核心概念", "具體例子", "今日任務", "延伸提問", "小提醒")


def load_system_prompt() -> str:
    return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")


def scheduled_topic(day: date) -> str:
    return WEEKDAY_TOPIC[day.weekday()]


def weekday_zh(day: date) -> str:
    return WEEKDAY_ZH[day.weekday()]


def level_for_session(session_number: int) -> str:
    """Part 6: sessions 1–3 are 入門, 4–7 中階, 8 and later 進階."""
    if session_number <= 3:
        return "入門"
    if session_number <= 7:
        return "中階"
    return "進階"


# ------------------------------------------------------------
# Learning log
# ------------------------------------------------------------
# One entry per (date, topic), following part 12 of the prompt:
#   date, topic, level, session_number, completed, title,
#   followup_question, reflection, lesson

def empty_log() -> dict:
    return {"version": 1, "entries": []}


def load_log(path: Path = DEFAULT_LOG_PATH) -> dict:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return empty_log()
    return parse_log(data)


def parse_log(data) -> dict:
    """Validate a log loaded from disk or uploaded by the user."""
    if not isinstance(data, dict) or not isinstance(data.get("entries"), list):
        raise ValueError("學習紀錄格式不正確")
    entries = [
        e for e in data["entries"]
        if isinstance(e, dict) and "date" in e and e.get("topic") in TOPICS
    ]
    return {"version": 1, "entries": entries}


def save_log(log: dict, path: Path = DEFAULT_LOG_PATH) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def find_entry(log: dict, day: date, topic: str):
    for entry in log["entries"]:
        if entry["date"] == day.isoformat() and entry["topic"] == topic:
            return entry
    return None


def topic_session_number(log: dict, topic: str, day: date) -> int:
    """How many times she has met this topic, counting today. Counted per
    topic (not global days), as part 12 asks."""
    prior = {
        e["date"] for e in log["entries"]
        if e["topic"] == topic and e["date"] < day.isoformat()
    }
    return len(prior) + 1


def start_entry(log: dict, day: date, topic: str) -> dict:
    """Return today's entry for this topic, creating it if needed."""
    entry = find_entry(log, day, topic)
    if entry is not None:
        return entry
    session_number = topic_session_number(log, topic, day)
    entry = {
        "date": day.isoformat(),
        "topic": topic,
        "session_number": session_number,
        "level": level_for_session(session_number),
        "completed": False,
        "title": "",
        "followup_question": "",
        "reflection": "",
        "lesson": "",
    }
    log["entries"].append(entry)
    log["entries"].sort(key=lambda e: e["date"])
    return entry


def completed_dates(log: dict) -> set:
    return {date.fromisoformat(e["date"]) for e in log["entries"] if e.get("completed")}


def current_streak(log: dict, today: date) -> int:
    """Consecutive completed days ending today. If today isn't done yet the
    streak still counts through yesterday, so it never reads as broken
    before she's had a chance to finish today."""
    done = completed_dates(log)
    day = today if today in done else today - timedelta(days=1)
    streak = 0
    while day in done:
        streak += 1
        day -= timedelta(days=1)
    return streak


def days_since_last_visit(log: dict, today: date):
    """Days since the most recent entry before today, or None if none."""
    earlier = [date.fromisoformat(e["date"]) for e in log["entries"]
               if e["date"] < today.isoformat()]
    if not earlier:
        return None
    return (today - max(earlier)).days


def weekly_topic_counts(log: dict, today: date) -> dict:
    """Interactions per topic over the 7 days before today (for Sunday's
    free topic, which should favor what she touched least)."""
    start = (today - timedelta(days=7)).isoformat()
    counts = {key: 0 for key in TOPICS}
    for e in log["entries"]:
        if start <= e["date"] < today.isoformat():
            counts[e["topic"]] += 1
    return counts


# ------------------------------------------------------------
# Awards: badges computed from the learning log
# ------------------------------------------------------------
# Every award is "metric >= goal". The log is replayed one day at a time,
# so each award knows the date it was earned, and a locked one shows how
# far along it is. Nothing is stored: awards always follow the log, so
# importing a backup or un-ticking a day updates them automatically.

AWARDS = (
    # key, icon, name, metric, goal, description
    ("first_step", "🌱", "第一步", "completed_days", 1, "完成第一天的學習"),
    ("streak_3", "🔥", "三日不斷", "best_streak", 3, "連續完成 3 天"),
    ("streak_7", "⚡", "一週連勝", "best_streak", 7, "連續完成 7 天"),
    ("streak_30", "🏆", "三十日修行", "best_streak", 30, "連續完成 30 天"),
    ("total_10", "📘", "十堂課", "completed_days", 10, "累計完成 10 天"),
    ("total_30", "📚", "三十堂課", "completed_days", 30, "累計完成 30 天"),
    ("total_100", "🎓", "百日學者", "completed_days", 100, "累計完成 100 天"),
    ("explorer", "🧭", "全主題探索者", "topics_covered", len(TOPICS), "七個主題都至少完成一次"),
    ("deep_diver", "💎", "深度玩家", "max_topic_sessions", 8, "同一個主題完成 8 次，進入進階"),
    ("thinker", "💭", "反思家", "reflections", 5, "寫下 5 次對延伸提問的想法"),
    ("weekend", "☀️", "週末也在學", "full_weekends", 1, "同一個週末的六、日都完成"),
    ("perfect_week", "✨", "完美一週", "perfect_weeks", 1, "週一到週日每天都完成"),
    ("comeback", "🌈", "回來就好", "comebacks", 1, "隔了 7 天以上，又回來完成一次"),
)

COMEBACK_GAP_DAYS = 7


def _daily_metrics(log: dict, until: date = None):
    """Yield (day, metrics) after each day that has an entry, in order."""
    by_day = {}
    for e in log["entries"]:
        if until is None or e["date"] <= until.isoformat():
            by_day.setdefault(e["date"], []).append(e)

    done = set()
    topic_days = {key: set() for key in TOPICS}
    m = {metric: 0 for _, _, _, metric, _, _ in AWARDS}
    streak = 0
    last_done = None
    for iso in sorted(by_day):
        day = date.fromisoformat(iso)
        entries = by_day[iso]
        m["reflections"] += sum(1 for e in entries if str(e.get("reflection", "")).strip())
        completed = [e for e in entries if e.get("completed")]
        if completed:
            done.add(day)
            for e in completed:
                topic_days[e["topic"]].add(day)
            if last_done is not None and (day - last_done).days >= COMEBACK_GAP_DAYS:
                m["comebacks"] += 1
            streak = streak + 1 if last_done == day - timedelta(days=1) else 1
            last_done = day
            m["completed_days"] = len(done)
            m["best_streak"] = max(m["best_streak"], streak)
            m["topics_covered"] = sum(1 for days in topic_days.values() if days)
            m["max_topic_sessions"] = max(len(days) for days in topic_days.values())
            # Days replay in order, so a weekend or a Mon–Sun week can only
            # be finished on its Sunday; count it there, once.
            if day.weekday() == 6:
                if day - timedelta(days=1) in done:
                    m["full_weekends"] += 1
                if all(day - timedelta(days=i) in done for i in range(1, 7)):
                    m["perfect_weeks"] += 1
        yield day, dict(m)


def compute_awards(log: dict, until: date = None) -> list:
    """Every award with its progress and the date it was earned (or None).
    `until` ignores entries after that date."""
    earned_on = {}
    final = {metric: 0 for _, _, _, metric, _, _ in AWARDS}
    for day, metrics in _daily_metrics(log, until):
        final = metrics
        for key, _, _, metric, goal, _ in AWARDS:
            if key not in earned_on and metrics[metric] >= goal:
                earned_on[key] = day
    return [
        {
            "key": key,
            "icon": icon,
            "name": name,
            "description": description,
            "goal": goal,
            "progress": min(final[metric], goal),
            "earned_on": earned_on.get(key),
        }
        for key, icon, name, metric, goal, description in AWARDS
    ]


def earned_award_keys(log: dict, until: date = None) -> set:
    return {a["key"] for a in compute_awards(log, until) if a["earned_on"]}


# ------------------------------------------------------------
# Parsing the coach's six-block answer
# ------------------------------------------------------------

def extract_section(text: str, name: str) -> str:
    """Pull one 【...】 block's body out of a lesson, tolerating markdown
    bold/heading markers around the block titles."""
    clean = re.sub(r"[*#]+", "", text)
    pattern = rf"【{name}】\s*[:：]?\s*(.+?)(?=\n\s*【|{CLOSING_LINE[:6]}|\Z)"
    match = re.search(pattern, clean, flags=re.DOTALL)
    return match.group(1).strip() if match else ""


# ------------------------------------------------------------
# Context sent to the model
# ------------------------------------------------------------

def build_history_context(log: dict, topic: str, today: date) -> str:
    """Summarize her track record for the model, so it can apply part 6
    (no repeats, difficulty by per-topic count, a specific 小提醒)."""
    session_number = topic_session_number(log, topic, today)
    level = level_for_session(session_number)
    lines = [
        "【App 自動提供的學習紀錄】",
        f"- 今天：{today.isoformat()}（{weekday_zh(today)}）",
        f"- 今天的主題：{TOPICS[topic]}",
        f"- 這是她第 {session_number} 次接觸這個主題，依第六部分規則，難度為：{level}",
        f"- 目前連續完成天數：{current_streak(log, today)} 天",
        f"- 累計完成天數：{len(completed_dates(log))} 天",
    ]
    earned = [a for a in compute_awards(log, today) if a["earned_on"]]
    if earned:
        lines.append("- 她已經獲得的獎章：" + "、".join(a["name"] for a in earned))

    gap = days_since_last_visit(log, today)
    if gap is None:
        lines.append("- 這是她第一次使用，沒有更早的紀錄。")
    elif gap > 1:
        lines.append(
            f"- 距離上次互動已經 {gap} 天。請依第九部分情境二處理："
            "不要提到中斷，直接自然地「從這裡繼續」。"
        )

    past = [e for e in log["entries"]
            if e["topic"] == topic and e["date"] < today.isoformat()]
    if past:
        lines.append("- 這個主題過去學過的內容（避免重複，除非是刻意複習深化）：")
        for e in past[-10:]:
            status = "已完成" if e.get("completed") else "未打勾"
            lines.append(f"  - {e['date']}：{e.get('title') or '（無標題）'}（{status}）")
        last = past[-1]
        if last.get("followup_question"):
            lines.append(f"- 上次留給她的延伸提問：{last['followup_question']}")
        if last.get("reflection"):
            lines.append(f"- 她對上次延伸提問的回應：{last['reflection']}")

    if topic == "free":
        counts = weekly_topic_counts(log, today)
        summary = "、".join(
            f"{TOPICS[k]} {counts[k]} 次" for k in TOPICS if k != "free"
        )
        lines.append(f"- 過去七天各主題互動次數：{summary}")

    lines.append("- App 已經自動記錄學習軌跡，不需要再詢問她是否要開始記錄。")
    return "\n".join(lines)


def build_system_prompt(log: dict, topic: str, today: date) -> str:
    return f"{load_system_prompt()}\n\n{build_history_context(log, topic, today)}"


def build_kickoff_message(topic: str, today: date, focus: str = "") -> str:
    message = f"今天是 {today.isoformat()}，{weekday_zh(today)}。今天的主題：{TOPICS[topic]}。"
    if focus.strip():
        message += f"我今天特別想了解：{focus.strip()}"
    return message
