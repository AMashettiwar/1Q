"""1Q: a daily adaptive cancer-domain quiz for 1cell.ai."""
from __future__ import annotations

import json
import random
import time
from datetime import date, datetime
from zoneinfo import ZoneInfo, available_timezones

import altair as alt
import pandas as pd
import streamlit as st

from oneq import adaptive, auth, avatar, chat, llm, persona, quiz_engine as qe, roles as roles_cfg, ui
from oneq.db import session
from oneq.models import DailySet, User
from oneq.seed_questions import SUBTOPICS

st.set_page_config(page_title="1Q · daily cancer quiz", page_icon=":material/biotech:", layout="centered")
SS = st.session_state


def _tz() -> ZoneInfo:
    try:
        return ZoneInfo(SS.get("tz") or "UTC")
    except Exception:  # noqa: BLE001
        return ZoneInfo("UTC")


def now_local() -> datetime:
    return datetime.now(_tz()).replace(tzinfo=None)


def today() -> date:
    """The quiz day resets at midnight in the user's own timezone."""
    return now_local().date()


def theme() -> str:
    t = SS.get("theme", ui.DEFAULT_THEME)
    return t if t in ui.THEMES else ui.DEFAULT_THEME


def mascot(expr="happy", accessory=None, energy=100):
    if accessory is None or accessory == "":
        accessory = "lab_coat"
    pal = ui.THEMES[theme()]["mascot"]
    body = ui.OUTFIT_TONES.get(accessory, ui.OUTFIT_TONES[""])[1 if theme() == "ink" else 0]
    return avatar.svg(expr, accessory, energy, palette=(body, pal[1], pal[2]), react_id=SS.get("react_id", 0))


def say(text: str, expr: str = "happy"):
    SS["avatar_msg"], SS["avatar_expr"] = text, expr
    SS["avatar_fresh"] = True
    SS["react_id"] = SS.get("react_id", 0) + 1


# ---------------------------------------------------------------- sign-in
def sign_in() -> str | None:
    if SS.get("email"):
        return SS["email"]
    mode = auth.auth_mode()
    tz = getattr(st.context, "timezone", None) or "UTC"
    try:
        now = datetime.now(ZoneInfo(tz)).replace(tzinfo=None)
    except Exception:  # noqa: BLE001
        now = datetime.now()
    known = None
    typed = (SS.get("login_email") or "").strip().lower()
    if typed and auth.is_allowed_email(typed):
        with session() as s:
            k = s.query(User).filter_by(email=typed).first()
            if k and k.role:
                known = {"name": k.display_name, "role": k.role, "streak": k.streak}
    line = avatar.login_line(now, known) if known else (
        f"{avatar.login_line(now)} Sign in with your 1cell.ai email and let's grow some brain cells.")
    title = "Welcome back" if known else "1Q"
    st.markdown(ui.hero(mascot("cheering" if known else "happy"), title, line,
                        "Twelve questions a day. Built for 1cell.ai.", pokes=avatar.LOGIN_POKES), unsafe_allow_html=True)
    st.html(ui.LIVE_JS, unsafe_allow_javascript=True)
    st.write("")
    if mode == "google":
        g = auth.google_user()
        if g:
            SS["email"] = g
            return g
        if getattr(st.user, "is_logged_in", False):
            st.error(f"That Google account is not a @{auth.allowed_domain()} address. Please use your work account.")
            if st.button("Sign out"):
                st.logout()
            return None
        if st.button("Sign in with Google", type="primary", width="stretch"):
            st.login("google") if "google" in st.secrets.get("auth", {}) else st.login()
        return None

    email = st.text_input("Work email", placeholder=f"you@{auth.allowed_domain()}", key="login_email")
    if mode == "demo":
        st.caption("Demo mode: we only check the email domain. Anyone could type a colleague's address. "
                   "Turn on Google sign-in or email codes before real use.")
        if st.button("Enter 1Q", type="primary", width="stretch", key="login_btn"):
            if auth.is_allowed_email(email):
                SS["email"] = email.strip().lower()
                st.rerun()
            st.error(f"1Q is only open to @{auth.allowed_domain()} addresses.")
        return None

    # email_otp
    if st.button("Email me a code", width="stretch", key="otp_send"):
        if not auth.is_allowed_email(email):
            st.error(f"1Q is only open to @{auth.allowed_domain()} addresses.")
        else:
            code, digest, exp = auth.new_otp()
            try:
                auth.send_email(email, "Your 1Q sign-in code", f"Your code is {code}. It expires in 10 minutes.\n\n1Q")
                SS["otp"] = (email.strip().lower(), digest, exp)
                st.success("Code sent. Check your inbox.")
            except Exception as e:  # noqa: BLE001
                st.error(f"Could not send the email: {e}")
    if SS.get("otp"):
        code = st.text_input("6-digit code", max_chars=6, key="otp_code")
        if st.button("Verify", type="primary", key="otp_verify"):
            em, digest, exp = SS["otp"]
            if auth.check_otp(code, digest, exp):
                SS["email"] = em
                SS.pop("otp")
                st.rerun()
            st.error("That code did not match or it expired.")
    return None


# ---------------------------------------------------------------- onboarding
def onboarding(s, u: User):
    st.markdown(ui.section("onboarding", "Onboarding", theme()), unsafe_allow_html=True)
    st.markdown(ui.hero(mascot("cheering"), "Welcome to 1Q",
                        "Tell me who you are at 1cell.ai and I will pitch the questions at the right level.",
                        "Takes 20 seconds. Then 5 quick placement questions."), unsafe_allow_html=True)
    with st.form("onboard"):
        name = st.text_input("Display name (shown on the leaderboard)", value=u.display_name)
        role = st.selectbox("Your role at 1cell.ai", roles_cfg.role_names(), index=0)
        other = st.text_input("If you picked Other, type your role", placeholder="e.g. Spatial omics specialist")
        if st.form_submit_button("Start placement", type="primary", width="stretch"):
            if role == roles_cfg.OTHER:
                role = other.strip()[:60] or "Other"
            qe.set_role(s, u, role, name)
            SS["placement"] = {"results": [], "used": [], "level": adaptive.rating_to_level(u.base_rating)}
            st.rerun()


def placement(s, u: User):
    P = SS.setdefault("placement", {"results": [], "used": [], "level": adaptive.rating_to_level(u.base_rating)})
    n = len(P["results"])
    if n >= 5:
        qe.finish_placement(s, u, [tuple(r) for r in P["results"]])
        SS.pop("placement")
        say(f"Placement done. I set your starting level to {adaptive.LEVEL_NAMES[adaptive.rating_to_level(u.base_rating)]}. "
            "It will move as you learn.", "cheering")
        st.rerun()
    if "pq" not in P:
        P["pq"] = qe.placement_question(P["level"], set(P["used"]), random.Random())
    q = P["pq"]
    st.markdown(ui.hero(mascot("thinking", energy=90), "Quick placement",
                        "No pressure. These just tell me where to start.", f"Question {n + 1} of 5"), unsafe_allow_html=True)
    st.progress(n / 5)
    st.markdown(f'<div class="oq-card"><h3>{ui.esc(q["question"])}</h3></div>', unsafe_allow_html=True)
    choice = st.radio("Your answer", list(range(4)), format_func=lambda i: q["options"][i], index=None, key=f"pl_{n}")
    if st.button("Next", type="primary", disabled=choice is None, key=f"pl_next_{n}"):
        ok = qe.record_answer(s, u, q, choice, today(), placement=True)
        P["results"].append([q["level"], ok])
        P["used"].append(q["concept_id"])
        P["level"] = adaptive.next_placement_level(P["level"], [ok])
        P.pop("pq")
        st.rerun()


# ---------------------------------------------------------------- avatar
PROGRESS_LINES = [
    (0.01, "Great start. I am taking notes. Not on you, on the cells.", "thinking"),
    (0.34, "A third done. Your neurons are warming up nicely.", "thinking"),
    (0.5, "Halfway! I am doing a tiny cartwheel. Cells can do that.", "happy"),
    (0.75, "Three quarters. The finish line can see you.", "happy"),
    (1.0, "All twelve done. Your review is below.", "cheering"),
]


@st.fragment
def avatar_panel(u_name: str, mood: dict, accessory: str, progress: float | None, asking: bool = False):
    box = st.empty()
    c1, c2 = st.columns([1, 3])
    fresh = SS.pop("avatar_fresh", False)
    msg, expr = mood["message"], mood["expression"]
    if SS.get("avatar_msg") and (fresh or not progress):
        msg, expr = SS["avatar_msg"], SS.get("avatar_expr") or expr
    elif progress:
        for th, line, ex in PROGRESS_LINES:
            if progress >= th:
                msg, expr = line, ex
    if asking and not fresh and expr == "happy":
        expr = "thinking"  # 1Q ponders along while a question is open
    if c1.button("Poke 1Q", key="poke"):
        SS["tickles"] = SS.get("tickles", 0) + 1
        msg, expr = avatar.tickle_line(SS["tickles"])
        if SS["tickles"] % len(avatar.TICKLE) == 0:
            SS["tickles"] = 0
    c2.caption(f"1Q says: {avatar.daily_pick(avatar.SAYS, today())}")
    box.markdown(ui.hero(mascot(expr, accessory, mood["energy"]), avatar.greeting(u_name, now_local()), msg,
                         f"1Q energy {mood['energy']}%"), unsafe_allow_html=True)


# ---------------------------------------------------------------- quiz
def active_question(s, u: User, ds: DailySet) -> dict | None:
    if ds.completed:
        return None
    done = qe.answered_today(s, u, today())
    return next((q for q in json.loads(ds.questions_json) if q["id"] not in done), None)


def quiz_tab(s, u: User, ds: DailySet):
    st.markdown(ui.section("quiz", "01 / Today's quiz", theme()), unsafe_allow_html=True)
    qs = json.loads(ds.questions_json)
    done = qe.answered_today(s, u, today())
    total = len(qs)
    fb = SS.get("feedback")
    idx = next((i for i, q in enumerate(qs) if q["id"] not in done), None)
    if idx is None and not fb:
        if not ds.completed:
            finish_day(s, u)
            st.rerun()  # refresh the sidebar streak and progress with the completed day
        return results(s, u, ds, qs)

    st.markdown(ui.progress_ring(len(done), total), unsafe_allow_html=True)
    if not done:
        teaser_q, _ = avatar.daily_pick(avatar.TEASERS, today(), "teaser")
        st.markdown(f'<div class="oq-note"> <b>Today\'s cliffhanger</b><br>{ui.esc(teaser_q)}<br>'
                    '<small>Finish today\'s set to unlock the answer.</small></div>', unsafe_allow_html=True)
        if any(q.get("kind") == "boss" for q in qs):
            st.info(avatar.FRIDAY_BOSS)

    if fb:
        q, good = fb["q"], fb["correct"]
        right = q["options"][q["answer_index"]]
        if good:
            body = f"<p> <b>{ui.esc(right)}</b></p><p>{ui.esc(q['explanation'])}</p>"
        else:
            body = (f"<p>You picked: {ui.esc(q['options'][fb['pick']])}</p><p> <b>Answer:</b> {ui.esc(right)}</p>"
                    f"<p>{ui.esc(q['explanation'])}</p>")
        lab = persona.EXPLAIN_LABEL[persona.profile(u.role)["seniority"]]
        body = body.replace(f"<p>{ui.esc(q['explanation'])}</p>", f'<p><span class="oq-eyebrow" style="margin:0 6px 0 0">{lab}</span>{ui.esc(q["explanation"])}</p>')
        verdict = (ui.icon("check", 14) + "Correct") if good else (ui.icon("spark", 14) + "Worth a second look")
        st.markdown(f'<div class="oq-card {"good" if good else "kind"}"><div class="oq-meta"><span class="oq-verdict">{verdict}</span>'
                    f'<span class="oq-eyebrow" style="margin:0">Q{fb["n"]} · locked in</span></div><h3>{ui.esc(fb["line"])}</h3>{body}</div>', unsafe_allow_html=True)
        if st.button("Next question" if idx is not None else "See my review", type="primary",
                     width="stretch", key="next_q"):
            SS.pop("feedback")
            SS.pop("avatar_msg", None)
            st.rerun()
        return

    q = qs[idx]
    SS.setdefault("shown_at", {}).setdefault(q["id"], time.time())
    chips = ui.topic_tag(q["subtopic"], SUBTOPICS.get(q["subtopic"], q["subtopic"]), theme()) + ui.chip(adaptive.LEVEL_NAMES.get(q.get("level", 2), ""))
    chips += {"review": ui.chip("Rematch", "review"), "boss": ui.chip("Boss round", "boss"),
              "wildcard": ui.chip("Wild card", "boss")}.get(q.get("kind"), "")
    st.markdown(f'<div class="oq-card">{chips}<div class="oq-eyebrow">Question {idx + 1} of {total}</div>'
                f'<h3>{ui.esc(q["question"])}</h3></div>', unsafe_allow_html=True)
    choice = st.radio("Pick one", list(range(4)), format_func=lambda i: q["options"][i], index=None,
                      key=f"ans_{q['id']}", label_visibility="collapsed")
    c1, c2 = st.columns([3, 1])
    if c2.button("Hint", key=f"hint_{q['id']}", width="stretch"):
        SS.setdefault("hints", {})[q["id"]] = random.choice(avatar.HINTS)
    if SS.get("hints", {}).get(q["id"]):
        st.caption("1Q: " + SS["hints"][q["id"]])
    st.markdown('<div class="oq-kbd"><kbd>1</kbd><kbd>2</kbd><kbd>3</kbd><kbd>4</kbd> or <kbd>A</kbd>–<kbd>D</kbd> to choose,'
                ' <kbd>Enter</kbd> to lock in</div>', unsafe_allow_html=True)
    if c1.button("Lock it in", type="primary", disabled=choice is None, width="stretch", key=f"submit_{q['id']}"):
        elapsed = int((time.time() - SS["shown_at"][q["id"]]) * 1000)  # quiet anti-cheat signal, never shown
        ok = qe.record_answer(s, u, q, choice, today(), elapsed)
        SS.setdefault("times", []).append(elapsed)
        SS.setdefault("results", []).append(ok)
        try:
            client = json.loads(SS.get("oneq_signals") or "{}")
        except json.JSONDecodeError:
            client = {}
        prev = SS.get("prev_client", {})
        delta = {k: client.get(k, 0) - prev.get(k, 0) for k in ("copy", "paste", "blur")}
        SS["prev_client"] = client
        nudge = qe.nudge_for(qe.integrity_signals(q["question"], elapsed, ok, SS["times"], SS["results"],
                                                  q.get("level", 2), qe.overall_level(s, u), delta))
        if nudge and not SS.get("flagged_today"):
            SS["flagged_today"] = True
            u.soft_flags += 1
        rng = random.Random()
        if ok:
            line = avatar.role_line(u.role, "right") if rng.random() < .6 else avatar.pick(avatar.CORRECT)
        else:
            line = avatar.role_line(u.role, "wrong") if rng.random() < .6 else avatar.pick(avatar.WRONG)
        SS["feedback"] = {"q": q, "correct": ok, "line": line, "pick": choice, "n": idx + 1}
        if nudge:
            say(nudge, "suspicious")
        else:
            say(line, "cheering" if ok else "oops")
        st.rerun()


def finish_day(s, u: User):
    res = qe.complete_day(s, u, today(), honest=not SS.get("flagged_today"))
    SS["finish"] = res
    say(res["milestone"] or "Set complete! Your brain just did 12 reps. I am so proud I could divide.", "cheering")


def results(s, u: User, ds: DailySet, qs):
    res = SS.get("finish") or {}
    if res and not SS.get("celebrated"):
        SS["celebrated"] = True
        if res.get("milestone") or (u.streak and u.streak % 7 == 0):
            st.balloons()
    _, teaser_a = avatar.daily_pick(avatar.TEASERS, today(), "teaser")
    from sqlalchemy import func, select
    from oneq.models import PointEvent
    pts = s.scalar(select(func.coalesce(func.sum(PointEvent.points), 0)).where(
        PointEvent.user_id == u.id, PointEvent.day == today())) or 0
    st.markdown(ui.summary(int(pts), u.streak, u.title,
                           f'<div class="oq-note"><b>Cliffhanger solved.</b> {ui.esc(teaser_a)}</div>'
                           '<span class="sr-only">Today\'s set is done</span>'), unsafe_allow_html=True)
    if res.get("shields_used"):
        st.info(f" A streak shield covered {res['shields_used']} missed weekday(s). Streak saved.")
    if res.get("shield_earned"):
        st.success(" New streak shield earned. One free missed weekday is in your pocket.")
    if res.get("drop"):
        st.markdown(f'<div class="oq-note"> <b>Mystery drop:</b> {ui.esc(res["drop"]["text"])}</div>', unsafe_allow_html=True)
    for un in res.get("unlocks", []):
        st.success(f" Unlocked: {un}")
    if res.get("honest_badge"):
        st.success(" Honest Mode badge earned: five days of solo brainpower.")

    st.subheader("Today's review")
    done = qe.answered_today(s, u, today())
    picks = {}
    rng = random.Random(f"{u.id}{today()}")
    for i, q in enumerate(qs):
        ok = done.get(q["id"])
        right = q["options"][q["answer_index"]]
        if ok:
            line = avatar.role_line(u.role, "right", rng) if rng.random() < .6 else avatar.pick(avatar.CORRECT, rng)
            body = f"<p> {ui.esc(right)}</p>"
        else:
            line = avatar.role_line(u.role, "wrong", rng) if rng.random() < .6 else avatar.pick(avatar.WRONG, rng)
            mine = picks.get(q["id"])
            yours = f"<p>Your pick: {ui.esc(q['options'][mine])}</p>" if mine is not None else ""
            body = f"{yours}<p> <b>Answer:</b> {ui.esc(right)}</p>"
        st.markdown(f'<div class="oq-card {"good" if ok else "kind"}"><b>Q{i + 1}. {ui.esc(q["question"])}</b>'
                    f'<p><i>1Q: {ui.esc(line)}</i></p>{body}<p>{ui.esc(q["explanation"])}</p></div>', unsafe_allow_html=True)
    std = qe.standing(s, u, today())
    st.markdown("**Share your day** (streak and rank only, no scores):")
    st.markdown(ui.share_html(u.display_name, u.streak, std["rank"], std["of"], u.title, today()), unsafe_allow_html=True)
    st.code(ui.share_card(u.display_name, u.streak, std["rank"], std["of"], u.title, today()), language=None)
    st.caption("That is today's one attempt. Come back tomorrow for new material and a reworded rematch of anything that tripped you up.")


# ---------------------------------------------------------------- other tabs
def leaderboard_tab(s, u: User):
    st.markdown(ui.section("leaderboard", "02 / Leaderboard", theme()), unsafe_allow_html=True)
    std = qe.standing(s, u, today())
    mv = std["movement"]
    move = (f'<span class="oq-move up">{ui.icon("up", 12)}{mv}</span>' if mv > 0 else
            f'<span class="oq-move down">{ui.icon("down", 12)}{-mv}</span>' if mv < 0 else
            f'<span class="oq-move">{ui.icon("dash", 12)}Holding</span>')
    st.markdown(f'<div class="oq-card toned" style="--c:{ui.tone("navy", theme())}"><div class="oq-eyebrow">Your standing</div>'
                f'<div class="oq-standing"><div><span class="big">{ui.num(std["rank"])}</span>'
                f'<span class="oq-small"> of {std["of"]}</span></div>{move}</div>'
                f'<p>{ui.num(std["score"])} pts overall · since your last visit</p>'
                f'<span class="sr-only">Your standing: #{std["rank"]} of {std["of"]}</span></div>', unsafe_allow_html=True)
    views = st.tabs(["Daily", "Weekly", "Monthly", "Overall"])
    for view, period in zip(views, qe.PERIODS):
        with view:
            full = qe.leaderboard(s, today(), period)
            full = [r for r in full if r["score"] > 0] if period != "overall" else full
            st.markdown(ui.podium(full[:3], period, theme()), unsafe_allow_html=True)
            rows = qe.top_with_me(full, u.id, 10)[3:] if len(full) > 3 else []
            if u.id not in [r["user_id"] for r in full[:3] + rows] and period != "overall":
                st.caption("You are not on this board yet. One finished set puts you on it.")
            st.markdown(ui.lb_rows(rows, u.id, period, theme()), unsafe_allow_html=True)
    st.caption("Score blends participation points, streak and mastery level. It never shows right or wrong counts.")


def _style(chart):
    t = ui.THEMES[theme()]
    return chart.configure(background="transparent", font="Inter").configure_view(stroke=None).configure_axis(
        labelColor=t["muted"], titleColor=t["muted"], gridColor=t["line"], domainColor=t["line2"], tickColor=t["line2"])


def _mastery_chart(topics):
    df = pd.DataFrame(topics)
    df["color"] = [ui.tone(ui.TOPIC_TONES.get(k, "teal"), theme()) for k in df["key"]]
    bars = alt.Chart(df).mark_bar(cornerRadiusEnd=3, height=14).encode(
        x=alt.X("level:Q", title="Mastery level", scale=alt.Scale(domain=[0, 5])),
        y=alt.Y("topic:N", title=None, sort="-x", axis=alt.Axis(labelLimit=220)),
        color=alt.Color("color:N", scale=None), tooltip=["topic", "level"])
    return _style(bars.properties(height=max(120, 28 * len(df))))


def progress_tab(s, u: User):
    st.markdown(ui.section("progress", "03 / My progress", theme()), unsafe_allow_html=True)
    p = qe.progress(s, u)
    st.markdown(ui.stats([("flame", "Streak", u.streak, "days"), ("trophy", "Best streak", u.best_streak, "days"),
                          ("shield", "Shields", u.shields, ""), ("spark", "Rematches", p["pending_reviews"], "queued")]),
                unsafe_allow_html=True)
    th = theme()
    if not p["topics"]:
        st.caption("Your topic map fills in after your first set.")
    else:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Mastery radar")
            st.markdown(ui.radar(p["topics"], th) or "", unsafe_allow_html=True)
        with c2:
            st.subheader("Topic coverage")
            cov = pd.DataFrame(p["coverage"])
            if len(cov):
                cov["color"] = [ui.tone(ui.TOPIC_TONES.get(k, "teal"), th) for k in cov["key"]]
                donut = alt.Chart(cov).mark_arc(innerRadius=62, outerRadius=110, cornerRadius=3, padAngle=.015).encode(
                    theta=alt.Theta("answered:Q"), color=alt.Color("color:N", scale=None),
                    order=alt.Order("answered:Q", sort="descending"), tooltip=["topic", "answered"])
                st.altair_chart(_style(donut.properties(height=260)), width="stretch")
                st.caption("Share of your questions per topic.")
        st.subheader("Topic mastery")
        st.altair_chart(_mastery_chart(p["topics"]), width="stretch")
    act = pd.DataFrame(p["activity"])
    if act["points"].sum() > 0:
        st.subheader("Activity calendar")
        act["day"] = pd.to_datetime(act["day"])
        act["week"] = act["day"] - pd.to_timedelta(act["day"].dt.weekday, unit="D")
        act["dow"] = act["day"].dt.strftime("%a")
        heat = alt.Chart(act).mark_rect(cornerRadius=3, stroke=ui.THEMES[th]["bg"], strokeWidth=2).encode(
            x=alt.X("yearmonthdate(week):O", title=None, axis=alt.Axis(format="%b %d", labelAngle=0, labelOverlap=True)),
            y=alt.Y("dow:O", title=None, sort=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]),
            color=alt.Color("points:Q", legend=None, scale=alt.Scale(
                range=[ui.THEMES[th]["surface2"], ui.tone("sage", th), ui.tone("teal", th), ui.tone("navy", th)])),
            tooltip=[alt.Tooltip("day:T", format="%b %d"), "points"])
        st.altair_chart(_style(heat.properties(height=180)), width="stretch")
    c3, c4 = st.columns([3, 2])
    lv = pd.DataFrame(p["level_series"])
    if len(lv) >= 2:
        with c3:
            st.subheader("Knowledge level")
            lv["day"] = pd.to_datetime(lv["day"])
            base = alt.Chart(lv).encode(x=alt.X("day:T", title=None, axis=alt.Axis(format="%b %d")),
                                        y=alt.Y("level:Q", title="Level", scale=alt.Scale(zero=False)))
            area = base.mark_area(interpolate="monotone", color=ui.tone("teal", th), opacity=.16)
            line = base.mark_line(interpolate="monotone", color=ui.tone("teal", th), strokeWidth=2.5)
            st.altair_chart(_style((area + line + base.mark_circle(size=40, color=ui.tone("navy", th))).properties(height=200)),
                            width="stretch")
    rk = pd.DataFrame(p["rank_series"])
    if len(rk) >= 2:
        with c4:
            st.subheader("Rank over time")
            rk["day"] = pd.to_datetime(rk["day"])
            spark = alt.Chart(rk).mark_line(interpolate="monotone", color=ui.tone("brass", th), strokeWidth=2.5,
                                             point=alt.OverlayMarkDef(color=ui.tone("brass", th), size=36)).encode(
                x=alt.X("day:T", title=None, axis=alt.Axis(format="%b %d", tickCount=4)),
                y=alt.Y("rank:Q", title="Rank", scale=alt.Scale(reverse=True, zero=False), axis=alt.Axis(tickMinStep=1)))
            st.altair_chart(_style(spark.properties(height=200)), width="stretch")
            st.caption(f"Now #{int(rk['rank'].iloc[-1])}. Lower is higher on the board.")
    st.subheader("Wardrobe and badges")
    owned = qe.unlocked(u)
    outfits = [""] + [k for k in avatar.ACCESSORIES if k and k in owned]
    pick = st.selectbox("1Q outfit", outfits, index=outfits.index(u.equipped) if u.equipped in outfits else 0,
                        format_func=lambda k: avatar.ACCESSORY_NAMES.get(k, "None"))
    if pick != u.equipped:
        u.equipped = pick
    badges = [b for b in owned if b not in avatar.ACCESSORIES]
    st.write("Badges: " + (", ".join(b.replace("_", " ").title() for b in badges) if badges else "none yet. Keep going."))
    st.subheader("Settings")
    names = roles_cfg.role_names()
    cur = u.role if u.role in names else roles_cfg.OTHER
    new_role = st.selectbox("Your role (change any time)", names, index=names.index(cur), key="set_role")
    if new_role == roles_cfg.OTHER:
        new_role = st.text_input("Type your role", value=u.role if cur == roles_cfg.OTHER else "", key="set_role_other").strip()[:60] or u.role
    if new_role != u.role:
        qe.set_role(s, u, new_role)
        st.toast("Role updated. Your mastery history stays as it is.")
    zones = sorted(available_timezones())
    tz_now = u.timezone or SS.get("tz") or "UTC"
    tz = st.selectbox("Timezone (your day resets at local midnight)", zones,
                      index=zones.index(tz_now) if tz_now in zones else zones.index("UTC"), key="set_tz")
    if tz != u.timezone:
        u.timezone, SS["tz"] = tz, tz
        SS["tz_manual"] = True
        st.toast(f"Timezone set to {tz}.")
    rem = st.toggle("Daily reminder email", value=u.reminder_opt_in,
                    help="1Q emails you once a day if you have not quizzed yet. Turn off any time.")
    if rem != u.reminder_opt_in:
        u.reminder_opt_in = rem
        st.toast("Reminder settings saved.")


def about_tab(s, u: User):
    st.markdown(ui.section("about", "04 / About 1Q", theme()), unsafe_allow_html=True)
    st.markdown(f"""
<div class="oq-card"><h3>Meet 1Q</h3>
<p>1Q is your daily cancer-biology sparring partner. Every day you get {qe.DEFAULT_COUNT} questions, tuned to your role
and to how you are doing on each topic. About 70% is new material and 30% is a rematch of things you missed,
reworded so you are learning the idea and not memorizing a sentence.</p>
<p>Miss a question and it comes back tomorrow, then in 3 days, then in 7. Get it right each time and it retires.</p>
<p>Streaks earn shields (one per 7 days) so a sick day does not wipe you out. Finish a set for mystery drops,
outfits and titles. Fridays have a boss round.</p>
<p>The leaderboard ranks by points, streak and mastery level. Nobody sees your right or wrong counts. Not even me. Okay, I see them, but I am a cartoon.</p>
</div>""", unsafe_allow_html=True)
    word = st.text_input("Whisper something to 1Q", key="whisper", placeholder="psst...")
    if word:
        st.info(avatar.KEYWORDS.get(word.strip().lower(), "Hmm. Not a secret word. Try something every biologist loves."))
    st.caption(f"Questions by: {'AI + seed bank' if llm.get_provider().available() else 'built-in seed bank'} · Sign-in: {auth.auth_mode()}")


def admin_tab(s):
    st.markdown(ui.section("admin", "05 / Admin", theme()), unsafe_allow_html=True)
    a = qe.admin_stats(s, today())
    c = st.columns(3)
    c[0].metric("Users", a["users"])
    c[1].metric("Onboarded", a["onboarded"])
    c[2].metric("Finished today", a["today"])
    if a["by_day"]:
        df = pd.DataFrame(a["by_day"])
        df["day"] = pd.to_datetime(df["day"]).dt.strftime("%b %d")
        ycol = [c for c in df.columns if c != "day"][0]
        st.altair_chart(_style(alt.Chart(df).mark_bar(cornerRadiusEnd=3, size=28, color=ui.tone("petrol", theme())).encode(
            x=alt.X("day:N", title=None, sort=None, axis=alt.Axis(labelAngle=0)), y=alt.Y(f"{ycol}:Q", title="Finished sets"),
            tooltip=["day", ycol]).properties(height=220)), width="stretch")
    st.subheader("Soft integrity flags")
    st.caption("Heuristics only (very fast answers, machine-regular timing, copy/paste, tab switching). "
               "They cannot prove outside help. Use them to start a friendly conversation, nothing more.")
    st.dataframe(pd.DataFrame(a["flagged"]) if a["flagged"] else pd.DataFrame(columns=["name", "email", "soft_flags"]),
                 hide_index=True, width="stretch")


# ---------------------------------------------------------------- chat
def chat_panel(s, u: User, ds: DailySet):
    st.markdown(f'<div class="oq-chat-head" style="border-top:2px solid {ui.tone('peacock', theme())};padding-top:12px">Ask 1Q</div>', unsafe_allow_html=True)
    hist = SS.setdefault("chat", [{"role": "assistant", "content": f"Hi {u.display_name}! Ask me anything about cancer biology. "
                                   "I will not spoil a live quiz question though."}])
    box = st.container(height=300)
    for m in hist[-12:]:
        box.chat_message(m["role"], avatar=":material/blur_on:" if m["role"] == "assistant" else ":material/person:").write(m["content"])
    with st.form("chat_form", clear_on_submit=True, border=False):
        msg = st.text_input("Message 1Q", placeholder=f"e.g. explain CAR-T {persona.CHAT_HINT.get(persona.bucket(persona.profile(u.role)), 'simply')}",
                            label_visibility="collapsed", key="chat_msg")
        sent = st.form_submit_button("Send", width="stretch", key="chat_send")
    if sent and msg.strip():
        if SS.get("feedback"):
            active = None  # just answered: free to discuss
        else:
            active = active_question(s, u, ds)
        hist.append({"role": "user", "content": msg.strip()[:500]})
        if not chat.RateLimiter(SS).allow():
            ans = chat.SLOW_DOWN
        else:
            ans = chat.reply(hist[:-1], msg, u.display_name, u.role, active)
        hist.append({"role": "assistant", "content": ans})
        st.rerun()


# ---------------------------------------------------------------- main
def main():
    st.markdown(ui.css(theme()), unsafe_allow_html=True)
    email = sign_in()
    if not email:
        return
    with session() as s:
        u = qe.get_or_create_user(s, email)
        if not u.timezone:
            detected = getattr(st.context, "timezone", None)  # browser timezone
            if detected:
                u.timezone = detected
        SS["tz"] = u.timezone or "UTC"
        if "theme" not in SS:
            SS["theme"] = u.theme or ui.DEFAULT_THEME
            st.rerun()
        now = now_local()
        if "days_away" not in SS:
            SS["days_away"] = (today() - u.last_completed).days if u.last_completed else None
            SS["last_action"] = time.time()
        u.last_seen = now
        if not u.role:
            return onboarding(s, u)
        if not u.placement_done:
            return placement(s, u)

        if time.time() - SS.get("last_action", time.time()) > 300 and not SS.get("idle_shown"):
            SS["idle_shown"] = True
            say(avatar.IDLE, "sleepy")
        SS["last_action"] = time.time()

        ds = qe.get_today_set(s, u, today())
        if "greeted" not in SS:
            SS["greeted"] = True
            if (SS["days_away"] or 0) >= 2:
                say(f"Welcome back, {u.display_name}! I saved your seat. Comebacks are my favorite genre.", "cheering")
            else:
                prof = persona.profile(u.role)
                ln = llm.avatar_line(f"Greeting a {u.role} ({prof['function']}, {prof['seniority']}) with a "
                                     f"{u.streak}-day streak at {avatar.daypart(now)}. Hooks: {', '.join(prof['hooks'])}",
                                     u.display_name)
                first = SS["days_away"] is None
                say(ln or avatar.persona_line(u.role, now, u.streak, first, SS["days_away"]),
                    "sleepy" if avatar.daypart(now) == "night" and not first else "happy")
        mood = avatar.mood(u.streak, SS["days_away"], now, ds.completed)

        with st.sidebar:
            st.markdown(f"### {u.display_name}")
            st.caption(f"{u.role} · {u.title}")
            st.markdown(ui.stats([("flame", "Streak", u.streak, "days"),
                                  ("level", "Level", adaptive.LEVEL_NAMES[qe.overall_level(s, u)], ""),
                                  ("shield", "Shields", u.shields, "")]), unsafe_allow_html=True)
            n_q = len(json.loads(ds.questions_json))
            n_ans = len(qe.answered_today(s, u, today()))
            st.progress(1.0 if ds.completed else n_ans / n_q,
                        text="Today's set: done" if ds.completed else f"Today: {n_ans} of {n_q}")
            chat_panel(s, u, ds)
            dark = st.toggle("Dark theme", value=theme() == "ink", key="theme_toggle")
            if (dark and theme() != "ink") or (not dark and theme() != "ivory"):
                SS["theme"] = u.theme = "ink" if dark else "ivory"
                st.rerun()
            if st.button("Sign out", key="signout"):
                SS.clear()
                if auth.auth_mode() == "google":
                    st.logout()
                st.rerun()

        qs_today = json.loads(ds.questions_json)
        n_done = len(qe.answered_today(s, u, today()))
        prog = None if ds.completed else n_done / len(qs_today)
        asking = not ds.completed and not SS.get("feedback") and n_done < len(qs_today)
        avatar_panel(u.display_name, mood, u.equipped, prog, asking)
        with st.container(key="oneq_hidden"):
            st.text_input("signals", key="oneq_signals", label_visibility="collapsed")
        st.html(ui.SIGNALS_JS + ui.LIVE_JS, unsafe_allow_javascript=True)

        names = ["Today's Quiz", "Leaderboard", "My Progress", "About 1Q"]
        admin = auth.is_admin(email)
        if admin:
            names.append("Admin")
        tabs = st.tabs(names)
        with tabs[0]:
            quiz_tab(s, u, ds)
        with tabs[1]:
            leaderboard_tab(s, u)
        with tabs[2]:
            progress_tab(s, u)
        with tabs[3]:
            about_tab(s, u)
        if admin:
            with tabs[4]:
                admin_tab(s)


main()
