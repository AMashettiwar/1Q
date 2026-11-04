import json
import random
from datetime import date, timedelta

import pytest
from pydantic import ValidationError

from oneq import adaptive, auth, avatar, llm, quiz_engine as qe
from oneq.seed_questions import SEED_QUESTIONS, SUBTOPICS

D = date(2026, 11, 4)  # a Wednesday


# ---------- adaptive
def test_role_start_levels():
    assert adaptive.role_start_rating("Intern") < adaptive.role_start_rating("PhD scientist")
    assert adaptive.rating_to_level(adaptive.role_start_rating("Technician")) == 1
    assert adaptive.rating_to_level(adaptive.role_start_rating("Wet-lab scientist")) >= 4


def test_elo_moves_both_ways():
    assert adaptive.update_rating(1000, 3, True) > 1000
    assert adaptive.update_rating(1000, 1, False) < 1000
    # beating an easy question gains less than beating a hard one
    assert adaptive.update_rating(1000, 1, True) - 1000 < adaptive.update_rating(1000, 5, True) - 1000


def test_placement_refines():
    assert adaptive.placement_rating(800, [(1, True)] * 5) > 800
    assert adaptive.placement_rating(1400, [(4, False)] * 5) < 1400
    assert adaptive.next_placement_level(1, [True, True]) == 3


def test_new_review_split():
    assert adaptive.split_new_review(12, 10) == (8, 4)
    assert adaptive.split_new_review(12, 1) == (11, 1)


def test_pick_subtopics_prefers_unseen():
    mm = {s: (1000, 50) for s in list(SUBTOPICS)[:-1]}
    picks = adaptive.pick_subtopics(mm, list(SUBTOPICS), 400, random.Random(1))
    assert picks.count(list(SUBTOPICS)[-1]) > 400 / len(SUBTOPICS)


# ---------- spaced repetition
def test_schedule_intervals():
    s, due, ret = adaptive.schedule_after_answer(0, True, D)
    assert (s, due, ret) == (1, D + timedelta(days=3), False)
    s, due, ret = adaptive.schedule_after_answer(1, True, D)
    assert due == D + timedelta(days=7)
    s, due, ret = adaptive.schedule_after_answer(2, True, D)
    assert ret and due is None
    s, due, ret = adaptive.schedule_after_answer(2, False, D)
    assert (s, due, ret) == (0, D + timedelta(days=1), False)


def _user(s, email="a@1cell.ai", role="Intern"):
    u = qe.get_or_create_user(s, email)
    qe.set_role(s, u, role, email.split("@")[0])
    u.placement_done = True
    return u


def test_missed_question_comes_back_twisted(db):
    with db() as s:
        u = _user(s)
        ds = qe.get_today_set(s, u, D)
        qs = json.loads(ds.questions_json)
        assert len(qs) == qe.DEFAULT_COUNT
        missed = qs[0]
        wrong = (missed["answer_index"] + 1) % 4
        assert qe.record_answer(s, u, missed, wrong, D) is False
        nxt = qe.build_daily_set(s, u, D + timedelta(days=1))
        rev = [q for q in nxt if q["kind"] == "review"]
        assert len(rev) == 1 and rev[0]["concept_id"] == missed["concept_id"]
        assert rev[0]["question"] != missed["question"]  # reworded
        assert len(rev[0]["options"]) == 4
        # same day: not due yet
        assert not [q for q in qe.build_daily_set(s, u, D) if q["kind"] == "review"]
        # answer right on the review: moves to 3 days
        qe.record_answer(s, u, rev[0], rev[0]["answer_index"], D + timedelta(days=1))
        assert not [q for q in qe.build_daily_set(s, u, D + timedelta(days=2)) if q["kind"] == "review"]
        assert [q for q in qe.build_daily_set(s, u, D + timedelta(days=4)) if q["kind"] == "review"]


def test_llm_twist_used_when_available(db):
    class Fake(llm.Provider):
        def available(self): return True
        def chat(self, system, user, json_mode=False):
            q = {"concept_id": "x", "subtopic": "genomics", "level": 2, "type": "mcq",
                 "question": "A twisted scenario about TMB in a lung sample?",
                 "options": ["a", "b", "c", "d"], "answer_index": 2, "explanation": "Because reasons here."}
            return json.dumps({"questions": [q] * 20})
    llm.set_provider(Fake())
    try:
        t = llm.twist_question(SEED_QUESTIONS[0])
        assert t["concept_id"] == SEED_QUESTIONS[0]["concept_id"]
        assert t["question"].startswith("A twisted")
    finally:
        llm.set_provider(None)


def test_bad_json_retries_then_falls_back(db):
    calls = []
    class Bad(llm.Provider):
        def available(self): return True
        def chat(self, *a, **k):
            calls.append(1)
            return "not json"
    llm.set_provider(Bad())
    try:
        assert llm.generate_questions([("genomics", 2)], []) is None
        assert len(calls) == 2
        with db() as s:
            u = _user(s)
            assert len(qe.build_daily_set(s, u, D)) == 12  # seed fallback
    finally:
        llm.set_provider(None)


# ---------- MCQ only
def test_seed_bank_is_all_four_option_mcq():
    assert len(SEED_QUESTIONS) >= 40
    for q in SEED_QUESTIONS:
        llm.QuestionModel.model_validate(q)
        assert q["type"] == "mcq" and len(q["options"]) == 4


@pytest.mark.parametrize("bad", [
    {"type": "tf", "options": ["True", "False", "x", "y"]},
    {"options": ["True", "False"], "answer_index": 0},
    {"options": ["a", "b", "c"]},
    {"options": ["a", "a", "b", "c"]},
    {"answer_index": 4},
])
def test_schema_rejects_non_mcq(bad):
    q = dict(SEED_QUESTIONS[0]) | bad
    with pytest.raises((ValidationError, ValueError)):
        llm.QuestionModel.model_validate(q)


# ---------- leaderboard
FORBIDDEN = {"correct", "wrong", "incorrect", "accuracy", "right", "answers", "percent"}


def _check_row(r):
    for k in r:
        assert not any(f in k.lower() for f in FORBIDDEN), k


def test_leaderboard_has_no_correct_counts(db):
    with db() as s:
        a, b = _user(s, "a@1cell.ai"), _user(s, "b@1cell.ai", "PhD scientist")
        for u, right in ((a, True), (b, False)):
            for q in json.loads(qe.get_today_set(s, u, D).questions_json):
                qe.record_answer(s, u, q, q["answer_index"] if right else (q["answer_index"] + 1) % 4, D)
            qe.complete_day(s, u, D, rng=random.Random(0))
        rows = qe.leaderboard(s, D)
        assert [r["rank"] for r in rows] == [1, 2]
        for r in rows:
            _check_row(r)
        # flat points per correct answer, plus the same completion bonus for everyone
        assert a.points == 12 * qe.POINTS_PER_CORRECT + qe.COMPLETION_POINTS
        assert b.points == qe.COMPLETION_POINTS
        st = qe.standing(s, a, D)
        assert set(st) == {"rank", "of", "movement", "score"}


def test_period_leaderboards(db):
    with db() as s:
        old, new = _user(s, "old@1cell.ai"), _user(s, "new@1cell.ai")
        qe.add_points(s, old, 500, D - timedelta(days=40))  # last month only
        qe.add_points(s, new, 60, D)
        qe.add_points(s, new, 30, D - timedelta(days=2))  # Monday this week
        s.flush()
        top = lambda p: qe.leaderboard(s, D, p)[0]["name"]
        assert top("overall") == "old"
        assert top("daily") == top("weekly") == top("monthly") == "new"
        for p in qe.PERIODS:
            for r in qe.leaderboard(s, D, p):
                _check_row(r)
        daily = {r["name"]: r["score"] for r in qe.leaderboard(s, D, "daily")}
        weekly = {r["name"]: r["score"] for r in qe.leaderboard(s, D, "weekly")}
        assert daily["old"] == 0 and weekly["new"] > daily["new"]


def test_top10_plus_me(db):
    with db() as s:
        users = [_user(s, f"u{i}@1cell.ai") for i in range(14)]
        for i, u in enumerate(users):
            qe.add_points(s, u, 100 * (14 - i), D)
        s.flush()
        me = users[-1]
        rows = qe.top_with_me(qe.leaderboard(s, D, "daily"), me.id, 10)
        assert len(rows) == 11 and rows[-1]["user_id"] == me.id and rows[-1]["rank"] == 14
        rows = qe.top_with_me(qe.leaderboard(s, D, "daily"), users[0].id, 10)
        assert len(rows) == 10


# ---------- streaks, shields, rewards
def _weekdays(start, n):
    d, out = start, []
    while len(out) < n:
        if d.weekday() < 5:
            out.append(d)
        d += timedelta(days=1)
    return out


def test_streak_skips_weekends_and_uses_shield():
    class U: streak = 0; best_streak = 0; shields = 0; last_completed = None
    u = U()
    days = _weekdays(D, 7)  # Wed..Thu next week, spans a weekend
    for d in days:
        qe.apply_streak(u, d)
    assert u.streak == 7 and u.shields == 1  # weekend gap did not break it
    sat = D + timedelta(days=3)
    assert sat.weekday() == 5
    nxt = _weekdays(days[-1] + timedelta(days=1), 2)
    r = qe.apply_streak(u, nxt[1])  # missed one weekday
    assert r["shields_used"] == 1 and u.streak == 8 and u.shields == 0
    later = _weekdays(nxt[1] + timedelta(days=1), 3)
    qe.apply_streak(u, later[2])  # missed two weekdays, no shield
    assert u.streak == 1


def test_weekend_set_does_not_move_streak():
    class U: streak = 3; best_streak = 3; shields = 0; last_completed = D + timedelta(days=2)  # Friday
    u = U()
    qe.apply_streak(u, D + timedelta(days=3))  # Saturday
    assert u.streak == 3
    qe.apply_streak(u, D + timedelta(days=5))  # Monday
    assert u.streak == 4


def test_roles_yaml_and_other():
    from oneq import roles
    names = roles.role_names()
    assert len(names) > 25 and names[-1] == roles.OTHER
    assert adaptive.role_start_level("Intern") == 1
    assert adaptive.role_start_level("PhD scientist") == 4
    assert adaptive.role_start_level("Senior oncologist") == 5
    assert adaptive.role_start_level("Spatial omics postdoc") == 4
    assert adaptive.role_start_level("Something new", lambda t: 2) == 2
    assert adaptive.role_start_level("Something new") == 1


def test_tone_guard_and_prompts():
    for line in avatar.all_lines():
        assert avatar.is_safe(line), line
    assert not avatar.is_safe("Haha, imagine the patient")
    assert "Never joke about" in llm.SYSTEM_Q and "patients" in llm.SAFETY


def test_complete_day_rewards(db):
    with db() as s:
        u = _user(s)
        qe.get_today_set(s, u, D)
        r = qe.complete_day(s, u, D, rng=random.Random(3))
        assert r["drop"] and r["streak"] == 1
        again = qe.complete_day(s, u, D)
        assert again["drop"] is None  # no double rewards


# ---------- auth
@pytest.mark.parametrize("email,ok", [
    ("ankith@1cell.ai", True), ("Ankith@1CELL.AI", True), ("a@evil1cell.ai", False),
    ("a@1cell.ai.evil.com", False), ("a@sub.1cell.ai", False), ("a@gmail.com", False),
    ("", False), (None, False), ("not-an-email", False), ("a@1cell.ai@x.com", False),
])
def test_domain_restriction(email, ok):
    assert auth.is_allowed_email(email, "1cell.ai") is ok


def test_otp_roundtrip():
    code, digest, exp = auth.new_otp()
    assert len(code) == 6 and auth.check_otp(code, digest, exp)
    assert not auth.check_otp("000000" if code != "000000" else "111111", digest, exp)
    assert not auth.check_otp(code, digest, 0)


def test_auth_mode_default_demo(monkeypatch):
    monkeypatch.delenv("AUTH_MODE", raising=False)
    assert auth.auth_mode() == "demo"


# ---------- avatar & integrity
def test_tickle_escalates_and_resets():
    lines = [avatar.tickle_line(i)[0] for i in range(1, len(avatar.TICKLE) + 2)]
    assert "Stop, I'm ticklish!" in lines[:5]
    assert lines[-1] == lines[0]


def test_role_flavor():
    assert avatar.role_group("Intern") == "starter"
    assert avatar.role_group("Computational scientist") == "comp"
    assert avatar.role_group("Wet-lab scientist") == "wetlab"
    assert avatar.role_group("PhD scientist") == "phd"
    assert "Ankith" in avatar.reminder_subject("Ankith", "PhD scientist", 5, D)


def test_mood_misses_you():
    from datetime import datetime
    assert avatar.mood(0, 5, datetime(2026, 11, 4, 10), False)["expression"] == "missing"
    assert avatar.mood(3, 1, datetime(2026, 11, 4, 10), True)["expression"] == "cheering"


def test_integrity_signals():
    q = "x" * 200
    assert "fast" in qe.integrity_signals(q, 800, True, [], [], 2, 2)
    assert "regular" in qe.integrity_signals(q, 9000, False, [4000, 4010, 3990, 4005, 4000], [], 2, 2)
    assert "copy_paste" in qe.integrity_signals(q, 9000, False, [], [], 2, 2, {"paste": 1})
    assert qe.integrity_signals(q, 9000, True, [5000, 12000, 7000], [True], 2, 2) == []
    assert qe.nudge_for(["fast"])


# ---------- chat
def test_chat_guard_and_rate_limit():
    from oneq import chat
    q = {"question": "Which enzyme lets tumor cells rebuild telomeres?", "options": ["Telomerase", "PARP", "Kinase", "Helicase"],
         "answer_index": 0}
    assert chat.reply([], "what's the answer?", "A", "Intern", q) in chat.REFUSALS
    assert chat.reply([], "which enzyme rebuilds telomeres in tumor cells", "A", "Intern", q) in chat.REFUSALS

    class Leaky(llm.Provider):
        def available(self): return True
        def chat(self, *a, **k): return "It is Telomerase, obviously."
    llm.set_provider(Leaky())
    try:
        assert chat.reply([], "tell me a joke about cells", "A", "Intern", q) in chat.REFUSALS
        assert "Telomerase" in chat.reply([], "tell me a joke about cells", "A", "Intern", None)
    finally:
        llm.set_provider(None)
    assert chat.reply([], "hello", "A", "Intern", None) in chat.OFFLINE
    store = {}
    rl = chat.RateLimiter(store)
    assert all(rl.allow(1000.0 + i) for i in range(chat.RATE_MAX))
    assert not rl.allow(1000.0 + chat.RATE_MAX)
