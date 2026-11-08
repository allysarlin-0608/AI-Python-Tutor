from datetime import date, timedelta

from coach import core

WED = date(2026, 9, 23)


def make_log(*entries):
    log = core.empty_log()
    for day, topic, completed in entries:
        e = core.start_entry(log, day, topic)
        e["completed"] = completed
    return log


def test_weekly_schedule():
    assert core.scheduled_topic(date(2026, 9, 21)) == "fashion"      # Mon
    assert core.scheduled_topic(date(2026, 9, 22)) == "philosophy"   # Tue
    assert core.scheduled_topic(WED) == "reading"
    assert core.scheduled_topic(date(2026, 9, 24)) == "cosmos"
    assert core.scheduled_topic(date(2026, 9, 25)) == "fashion"
    assert core.scheduled_topic(date(2026, 9, 26)) == "reading"
    assert core.scheduled_topic(date(2026, 9, 27)) == "free"
    assert core.weekday_zh(WED) == "星期三"


def test_levels_follow_part_six():
    assert [core.level_for_session(n) for n in (1, 3, 4, 7, 8, 20)] == [
        "入門", "入門", "中階", "中階", "進階", "進階"]


def test_session_number_is_per_topic():
    log = make_log(
        (date(2026, 9, 1), "philosophy", True),
        (date(2026, 9, 8), "philosophy", True),
        (date(2026, 9, 2), "reading", True),
    )
    assert core.topic_session_number(log, "philosophy", WED) == 3
    assert core.topic_session_number(log, "reading", WED) == 2
    assert core.topic_session_number(log, "cosmos", WED) == 1


def test_start_entry_is_idempotent_for_same_day():
    log = core.empty_log()
    a = core.start_entry(log, WED, "reading")
    b = core.start_entry(log, WED, "reading")
    assert a is b and len(log["entries"]) == 1


def test_streak_counts_through_yesterday_until_today_done():
    log = make_log(
        (date(2026, 9, 20), "free", True),
        (date(2026, 9, 21), "fashion", True),
        (date(2026, 9, 22), "philosophy", True),
        (WED, "reading", False),
    )
    assert core.current_streak(log, WED) == 3
    core.find_entry(log, WED, "reading")["completed"] = True
    assert core.current_streak(log, WED) == 4


def test_streak_resets_after_gap():
    log = make_log((date(2026, 9, 20), "free", True))
    assert core.current_streak(log, WED) == 0


def test_extract_section_handles_markdown():
    lesson = (
        "**【今日主題】**：哲學 — 控制二分法（入門）\n"
        "【核心概念】：重點。\n"
        "### 【延伸提問】：哪些是你能控制的？\n"
        "【小提醒】：很好。\n"
        "完成後記得打勾，連續完成比完美更重要。"
    )
    assert core.extract_section(lesson, "今日主題") == "哲學 — 控制二分法（入門）"
    assert core.extract_section(lesson, "延伸提問") == "哪些是你能控制的？"
    assert core.extract_section(lesson, "不存在") == ""


def test_history_context_mentions_past_and_gap():
    log = make_log((date(2026, 9, 9), "reading", True))
    e = log["entries"][0]
    e["title"] = "看書 — 《原子習慣》第一章（入門）"
    e["followup_question"] = "你最想養成哪個習慣？"
    e["reflection"] = "每天寫商業計劃"
    ctx = core.build_history_context(log, "reading", WED)
    assert "第 2 次" in ctx and "入門" in ctx
    assert "《原子習慣》" in ctx
    assert "每天寫商業計劃" in ctx
    assert "14 天" in ctx and "情境二" in ctx


def test_system_prompt_includes_full_instructions():
    prompt = core.build_system_prompt(core.empty_log(), "free", date(2026, 9, 27))
    assert prompt.startswith("每日興趣學習教練")
    assert core.CLOSING_LINE in prompt
    assert "過去七天各主題互動次數" in prompt


def test_log_round_trip(tmp_path):
    path = tmp_path / "log.json"
    log = make_log((WED, "cosmos", True))
    core.save_log(log, path)
    assert core.load_log(path) == log
    assert core.load_log(tmp_path / "missing.json") == core.empty_log()


# ------------------------------------------------------------
# Awards
# ------------------------------------------------------------

def awards_by_key(log, until=None):
    return {a["key"]: a for a in core.compute_awards(log, until)}


def test_no_awards_for_empty_log():
    awards = core.compute_awards(core.empty_log())
    assert len(awards) == len(core.AWARDS)
    assert all(a["earned_on"] is None and a["progress"] == 0 for a in awards)


def test_streak_awards_use_best_streak_and_record_date():
    start = date(2026, 9, 1)
    log = make_log(*[(start + timedelta(days=i), "reading", True) for i in range(7)])
    # Break, then a short new run: the best streak (7) still counts.
    core.start_entry(log, date(2026, 9, 10), "reading")["completed"] = True
    a = awards_by_key(log)
    assert a["first_step"]["earned_on"] == start
    assert a["streak_3"]["earned_on"] == date(2026, 9, 3)
    assert a["streak_7"]["earned_on"] == date(2026, 9, 7)
    assert a["streak_30"]["earned_on"] is None
    assert a["streak_30"]["progress"] == 7
    assert a["total_10"]["progress"] == 8


def test_unfinished_days_do_not_count():
    log = make_log((date(2026, 9, 1), "reading", False))
    assert core.earned_award_keys(log) == set()


def test_explorer_and_deep_diver():
    start = date(2026, 9, 1)
    log = make_log(*[(start + timedelta(days=i), key, True)
                     for i, key in enumerate(core.TOPICS)])
    assert awards_by_key(log)["explorer"]["earned_on"] == start + timedelta(days=6)

    log = make_log(*[(start + timedelta(days=2 * i), "cosmos", True) for i in range(8)])
    a = awards_by_key(log)
    assert a["deep_diver"]["earned_on"] == start + timedelta(days=14)
    assert a["explorer"]["progress"] == 1


def test_weekend_perfect_week_and_comeback():
    monday = date(2026, 9, 21)
    log = make_log(*[(monday + timedelta(days=i), "free", True) for i in range(7)])
    a = awards_by_key(log)
    assert a["weekend"]["earned_on"] == monday + timedelta(days=6)
    assert a["perfect_week"]["earned_on"] == monday + timedelta(days=6)
    assert a["comeback"]["earned_on"] is None

    back = monday + timedelta(days=6 + core.COMEBACK_GAP_DAYS)
    core.start_entry(log, back, "reading")["completed"] = True
    assert awards_by_key(log)["comeback"]["earned_on"] == back


def test_reflections_and_until():
    log = core.empty_log()
    for i in range(5):
        core.start_entry(log, date(2026, 9, 1 + i), "philosophy")["reflection"] = "想法"
    assert awards_by_key(log)["thinker"]["earned_on"] == date(2026, 9, 5)
    assert awards_by_key(log, until=date(2026, 9, 4))["thinker"]["progress"] == 4


def test_history_context_lists_awards():
    log = make_log((date(2026, 9, 22), "philosophy", True))
    assert "第一步" in core.build_history_context(log, "reading", WED)
