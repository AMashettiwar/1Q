"""Daily sets, answers, streaks, rewards, leaderboard. Talks to the DB."""
from __future__ import annotations

import json
import random
import statistics
from datetime import date, datetime, timedelta

from sqlalchemy import func, select

from . import adaptive, avatar, llm
from .models import PointEvent, Answer, DailySet, Mastery, RankSnapshot, ReviewItem, User
from .seed_questions import SEED_QUESTIONS, SUBTOPICS

DEFAULT_COUNT = 12
MAX_SHIELDS = 3
POINTS_PER_CORRECT = 10
COMPLETION_POINTS = 20


# ---------------------------------------------------------------- users
def get_or_create_user(s, email: str) -> User:
    email = email.strip().lower()
    u = s.scalar(select(User).where(User.email == email))
    if not u:
        u = User(email=email, display_name=email.split("@")[0].replace(".", " ").title())
        s.add(u)
        s.flush()
    return u


def set_role(s, u: User, role: str, display_name: str | None = None, avatar_emoji: str | None = None):
    first_time = u.role is None
    u.role = role
    if first_time or not u.placement_done:
        u.base_rating = adaptive.role_start_rating(role, llm.guess_level)
    if display_name:
        u.display_name = display_name.strip()[:60]
    if avatar_emoji:
        u.avatar = avatar_emoji
    s.flush()


def unlocked(u: User) -> list[str]:
    try:
        return json.loads(u.unlocked_json or "[]")
    except json.JSONDecodeError:
        return []


def _add_unlock(u: User, key: str) -> bool:
    cur = unlocked(u)
    if key in cur:
        return False
    cur.append(key)
    u.unlocked_json = json.dumps(cur)
    return True


def add_points(s, u: User, pts: int, day: date):
    u.points += pts
    s.add(PointEvent(user_id=u.id, day=day, points=pts))


# ---------------------------------------------------------------- mastery
def mastery_map(s, u: User) -> dict[str, tuple[float, int]]:
    rows = s.scalars(select(Mastery).where(Mastery.user_id == u.id)).all()
    return {m.subtopic: (m.rating, m.seen) for m in rows}


def _mastery_row(s, u: User, sub: str) -> Mastery:
    m = s.scalar(select(Mastery).where(Mastery.user_id == u.id, Mastery.subtopic == sub))
    if not m:
        m = Mastery(user_id=u.id, subtopic=sub, rating=u.base_rating, seen=0)
        s.add(m)
        s.flush()
    return m


def overall_level(s, u: User) -> int:
    mm = mastery_map(s, u)
    r = statistics.mean([v[0] for v in mm.values()]) if mm else u.base_rating
    return adaptive.rating_to_level(r)


# ---------------------------------------------------------------- questions
def shuffle_options(q: dict, rng: random.Random) -> dict:
    q = dict(q)
    correct = q["options"][q["answer_index"]]
    opts = list(q["options"])
    rng.shuffle(opts)
    q["options"], q["answer_index"] = opts, opts.index(correct)
    return q


def seed_for(sub: str, level: int, avoid: set[str], rng: random.Random) -> dict:
    pool = [q for q in SEED_QUESTIONS if q["concept_id"] not in avoid]
    same = [q for q in pool if q["subtopic"] == sub] or pool or SEED_QUESTIONS
    best = min(abs(q["level"] - level) for q in same)
    return dict(rng.choice([q for q in same if abs(q["level"] - level) == best]))


def placement_question(level: int, used: set[str], rng: random.Random) -> dict:
    pool = [q for q in SEED_QUESTIONS if q["level"] == level and q["concept_id"] not in used]
    pool = pool or [q for q in SEED_QUESTIONS if q["concept_id"] not in used]
    return shuffle_options(dict(rng.choice(pool), kind="placement"), rng)


def finish_placement(s, u: User, results: list[tuple[int, bool]]):
    u.base_rating = adaptive.placement_rating(u.base_rating, results)
    u.placement_done = True
    for m in s.scalars(select(Mastery).where(Mastery.user_id == u.id)):
        m.rating = u.base_rating
    s.flush()


def _seen_concepts(s, u: User) -> list[str]:
    return list(s.scalars(select(Answer.concept_id).where(Answer.user_id == u.id)).all())


def _twist_fallback(q: dict, rng: random.Random) -> dict:
    t = dict(q)
    frames = ["Second look, new angle: ", "Same idea, fresh scenario. A colleague asks you: ",
              "Plot twist edition: ", "You are presenting at lab meeting and someone asks: "]
    base = q["question"]
    for f in frames:
        base = base.replace(f, "")
    t["question"] = rng.choice(frames) + base
    return shuffle_options(t, rng)


def build_daily_set(s, u: User, today: date, n: int = DEFAULT_COUNT, rng: random.Random | None = None) -> list[dict]:
    rng = rng or random.Random(f"{u.id}-{today}")
    due = s.scalars(select(ReviewItem).where(ReviewItem.user_id == u.id, ReviewItem.retired.is_(False),
                                             ReviewItem.due <= today).order_by(ReviewItem.due)).all()
    n_new, n_rev = adaptive.split_new_review(n, len(due))
    out: list[dict] = []
    for item in due[:n_rev]:
        orig = json.loads(item.question_json)
        t = llm.twist_question(orig) or _twist_fallback(orig, rng)
        t.update(kind="review", review_id=item.id, concept_id=item.concept_id, subtopic=item.subtopic)
        out.append(shuffle_options(t, rng))

    mm = mastery_map(s, u)
    subs = adaptive.pick_subtopics(mm, list(SUBTOPICS), n_new, rng)
    slots = []
    for i, sub in enumerate(subs):
        lvl = adaptive.rating_to_level(mm.get(sub, (u.base_rating, 0))[0])
        if rng.random() < 0.25:
            lvl = min(5, lvl + 1)  # stretch question
        slots.append((sub, lvl))
    boss = today.weekday() == 4  # Friday boss round
    if boss:
        slots = slots[:-3] + [(sub, min(5, lv + 1)) for sub, lv in slots[-3:]]

    seen = set(_seen_concepts(s, u)) | {q["concept_id"] for q in out}
    gen = llm.generate_questions(slots, sorted(seen)) or []
    for i, (sub, lvl) in enumerate(slots):
        q = gen[i] if i < len(gen) else None
        if q is None or q["concept_id"] in seen:
            q = seed_for(sub, lvl, seen, rng)
        q = shuffle_options(q, rng)
        q["kind"] = "boss" if boss and i >= len(slots) - 3 else "new"
        seen.add(q["concept_id"])
        out.append(q)
    if rng.random() < 0.2 and out:  # wild card day: one slot becomes a surprise topic, same total count
        j = len(out) - 1
        if out[j]["kind"] == "new":
            wc = shuffle_options(seed_for(rng.choice(list(SUBTOPICS)), rng.randint(1, 5), seen, rng), rng)
            wc["kind"] = "wildcard"
            out[j] = wc
    for i, q in enumerate(out):
        q["id"] = q.get("id") or f"q-{today}-{i}"
        q["id"] = f"{q['id']}-{today}-{i}"
    return out


def get_today_set(s, u: User, today: date, n: int = DEFAULT_COUNT) -> DailySet:
    ds = s.scalar(select(DailySet).where(DailySet.user_id == u.id, DailySet.day == today))
    if not ds:
        qs = build_daily_set(s, u, today, n)
        ds = DailySet(user_id=u.id, day=today, questions_json=json.dumps(qs))
        s.add(ds)
        s.flush()
    return ds


def answered_today(s, u: User, today: date) -> dict[str, bool]:
    rows = s.scalars(select(Answer).where(Answer.user_id == u.id, Answer.day == today,
                                          Answer.is_placement.is_(False))).all()
    return {a.question_id: a.correct for a in rows}


def record_answer(s, u: User, q: dict, chosen: int, today: date, elapsed_ms: int = 0,
                  placement: bool = False) -> bool:
    correct = int(chosen) == int(q["answer_index"])
    s.add(Answer(user_id=u.id, day=today, question_id=q["id"] if not placement else q["concept_id"],
                 concept_id=q["concept_id"], subtopic=q["subtopic"], correct=correct,
                 is_placement=placement, elapsed_ms=int(elapsed_ms)))
    if placement:
        s.flush()
        return correct
    if correct:
        add_points(s, u, POINTS_PER_CORRECT, today)  # flat, no difficulty or speed scaling
    m = _mastery_row(s, u, q["subtopic"])
    m.rating = adaptive.update_rating(m.rating, q.get("level", 2), correct)
    m.seen += 1
    item = s.scalar(select(ReviewItem).where(ReviewItem.user_id == u.id, ReviewItem.concept_id == q["concept_id"]))
    if q.get("kind") == "review" and item:
        stage, due, retired = adaptive.schedule_after_answer(item.stage, correct, today)
        item.stage, item.retired = stage, retired
        if due:
            item.due = due
        if not correct:
            item.question_json = json.dumps(q)
    elif not correct:
        if item:
            item.stage, item.retired, item.due = 0, False, today + timedelta(days=1)
            item.question_json = json.dumps(q)
        else:
            s.add(ReviewItem(user_id=u.id, concept_id=q["concept_id"], subtopic=q["subtopic"],
                             question_json=json.dumps(q), due=today + timedelta(days=1), stage=0))
    s.flush()
    return correct


# ---------------------------------------------------------------- streaks and rewards
def missed_weekdays(last: date, today: date) -> int:
    """Weekdays strictly between last and today. Weekends never count."""
    d, n = last + timedelta(days=1), 0
    while d < today:
        if d.weekday() < 5:
            n += 1
        d += timedelta(days=1)
    return n


def apply_streak(u: User, today: date) -> dict:
    used = 0
    last = u.last_completed
    if last == today:
        return {"streak": u.streak, "shields_used": 0, "shield_earned": False, "new_day": False}
    if today.weekday() >= 5:  # weekend sets are welcome but do not move the streak
        return {"streak": u.streak, "shields_used": 0, "shield_earned": False, "new_day": True}
    if last is None:
        u.streak = 1
    else:
        gap = missed_weekdays(last, today)
        if gap == 0:
            u.streak += 1
        elif u.shields >= gap:
            u.shields -= gap
            used = gap
            u.streak += 1
        else:
            u.streak = 1
    earned = False
    if u.streak % 7 == 0 and u.shields < MAX_SHIELDS:
        u.shields += 1
        earned = True
    u.best_streak = max(u.best_streak, u.streak)
    u.last_completed = today
    return {"streak": u.streak, "shields_used": used, "shield_earned": earned, "new_day": True}


def live_streak(u: User, today: date) -> int:
    if not u.last_completed:
        return 0
    return u.streak if missed_weekdays(u.last_completed, today) <= u.shields else 0


def compute_title(streak: int, level: int) -> str:
    title = "Curious Cell"
    for (kind, val), name in avatar.TITLES:
        if (kind == "streak" and streak >= val) or (kind == "level" and level >= val):
            title = name
    return title


def complete_day(s, u: User, today: date, honest: bool = True, rng: random.Random | None = None) -> dict:
    rng = rng or random.Random()
    ds = s.scalar(select(DailySet).where(DailySet.user_id == u.id, DailySet.day == today))
    already = bool(ds and ds.completed)
    if ds:
        ds.completed = True
    st = apply_streak(u, today)
    res = dict(st, milestone=None, drop=None, unlocks=[], title=u.title, honest_badge=False)
    if already or not st["new_day"]:
        return res
    add_points(s, u, COMPLETION_POINTS, today)
    res["milestone"] = avatar.STREAK_MILESTONES.get(u.streak)
    lvl = overall_level(s, u)
    days = s.scalar(select(func.count()).select_from(DailySet).where(DailySet.user_id == u.id, DailySet.completed.is_(True)))
    for key, _kind, label, (rk, rv) in avatar.UNLOCKS:
        val = {"streak": u.streak, "days": days, "level": lvl}[rk]
        if val >= rv and _add_unlock(u, key):
            res["unlocks"].append(label)
    if honest:
        u.honest_days += 1
        if u.honest_days == 5 and _add_unlock(u, "honest_mode"):
            res["honest_badge"] = True
    kind, key, text = avatar.roll_mystery(rng, unlocked(u))
    if kind in ("accessory", "badge"):
        _add_unlock(u, key)
    res["drop"] = {"kind": kind, "key": key, "text": text}
    u.title = compute_title(u.streak, lvl)
    res["title"] = u.title
    s.flush()
    return res


# ---------------------------------------------------------------- leaderboard
def composite_score(points: int, streak: int, level: int) -> int:
    """Points + streak + mastery level. Raw correct/wrong counts are never shown."""
    return int(points + 10 * streak + 40 * level)


PERIODS = ("daily", "weekly", "monthly", "overall")


def period_start(period: str, today: date) -> date | None:
    if period == "daily":
        return today
    if period == "weekly":
        return today - timedelta(days=today.weekday())  # Monday
    if period == "monthly":
        return today.replace(day=1)
    return None


def leaderboard(s, today: date, period: str = "overall") -> list[dict]:
    start = period_start(period, today)
    pts = {}
    if start is not None:
        q = select(PointEvent.user_id, func.sum(PointEvent.points)).where(
            PointEvent.day >= start, PointEvent.day <= today).group_by(PointEvent.user_id)
        pts = dict(s.execute(q).all())
    rows = []
    for u in s.scalars(select(User).where(User.role.is_not(None))).all():
        p = u.points if start is None else int(pts.get(u.id, 0))
        ls = live_streak(u, today)
        lvl = overall_level(s, u)
        rows.append({"user_id": u.id, "name": u.display_name or "Anonymous cell", "avatar": u.avatar,
                     "title": u.title, "streak": ls, "level": adaptive.LEVEL_NAMES[lvl],
                     "score": composite_score(p, ls, lvl) if (start is None or p) else 0})
    rows.sort(key=lambda r: (-r["score"], -r["streak"], r["name"]))
    for i, r in enumerate(rows, 1):
        r["rank"] = i
    return rows


def snapshot_ranks(s, today: date, rows: list[dict] | None = None):
    rows = rows or leaderboard(s, today)
    for r in rows:
        snap = s.scalar(select(RankSnapshot).where(RankSnapshot.user_id == r["user_id"], RankSnapshot.day == today))
        if snap:
            snap.rank = r["rank"]
        else:
            s.add(RankSnapshot(user_id=r["user_id"], day=today, rank=r["rank"]))
    s.flush()


def top_with_me(rows: list[dict], user_id: int, n: int = 10) -> list[dict]:
    """Top n rows plus the viewer's own row if they are outside the top n."""
    top = rows[:n]
    if not any(r["user_id"] == user_id for r in top):
        top += [r for r in rows if r["user_id"] == user_id]
    return top


def standing(s, u: User, today: date) -> dict:
    rows = leaderboard(s, today)
    snapshot_ranks(s, today, rows)
    me = next((r for r in rows if r["user_id"] == u.id), None)
    prev = s.scalar(select(RankSnapshot).where(RankSnapshot.user_id == u.id, RankSnapshot.day < today)
                    .order_by(RankSnapshot.day.desc()))
    rank = me["rank"] if me else len(rows)
    return {"rank": rank, "of": len(rows), "movement": (prev.rank - rank) if prev else 0,
            "score": me["score"] if me else 0}


# ---------------------------------------------------------------- progress (private to the user)
def progress(s, u: User) -> dict:
    mm = mastery_map(s, u)
    topics = [{"topic": SUBTOPICS[k], "key": k, "level": round(min(5.0, max(0.2, (v[0] - 600) / 200)), 2)} for k, v in mm.items() if k in SUBTOPICS]
    days = s.scalars(select(DailySet.day).where(DailySet.user_id == u.id, DailySet.completed.is_(True))).all()
    reviews = s.scalar(select(func.count()).select_from(ReviewItem).where(
        ReviewItem.user_id == u.id, ReviewItem.retired.is_(False)))
    return {"topics": topics, "days": sorted(days), "pending_reviews": reviews or 0}


def admin_stats(s, today: date) -> dict:
    users = s.scalars(select(User)).all()
    part = s.execute(select(DailySet.day, func.count()).where(DailySet.completed.is_(True))
                     .group_by(DailySet.day).order_by(DailySet.day)).all()
    flagged = [{"name": u.display_name, "email": u.email, "soft_flags": u.soft_flags}
               for u in users if u.soft_flags > 0]
    return {"users": len(users), "onboarded": sum(1 for u in users if u.role),
            "today": dict(part).get(today, 0), "by_day": [{"day": d, "completed": c} for d, c in part],
            "flagged": sorted(flagged, key=lambda r: -r["soft_flags"])}


# ---------------------------------------------------------------- integrity nudges
def integrity_signals(question: str, elapsed_ms: int, correct: bool, recent_ms: list[int],
                      recent_correct: list[bool], q_level: int, user_level: int,
                      client: dict | None = None) -> list[str]:
    """Light heuristics. They suggest, never prove, outside help."""
    out = []
    min_read = max(2500, 22 * len(question))
    if correct and 0 < elapsed_ms < min_read:
        out.append("fast")
    if len(recent_ms) >= 5:
        last = recent_ms[-5:]
        if statistics.pstdev(last) < 250 and statistics.mean(last) > 1500:
            out.append("regular")
    if len(recent_correct) >= 8 and all(recent_correct[-8:]) and q_level >= user_level + 2:
        out.append("perfect_run")
    client = client or {}
    if client.get("paste", 0) or client.get("copy", 0):
        out.append("copy_paste")
    if client.get("blur", 0) >= 3:
        out.append("tab_hop")
    return out


def nudge_for(signals: list[str]) -> str | None:
    if not signals:
        return None
    m = {"fast": 1, "regular": 2, "copy_paste": 3, "tab_hop": 4, "perfect_run": 0}
    return avatar.CHEATING[m[signals[0]]]
