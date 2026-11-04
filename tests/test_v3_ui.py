"""v3 UI: role asked at sign-in, live mascot reaction rules, locked answers, mascot slot, tables."""
import json

from streamlit.testing.v1 import AppTest

from oneq import avatar, llm, ui
from tests.test_app import MockLLM


def test_role_reaction_covers_any_title():
    assert "CTO" in avatar.role_reaction("CTO")[0]
    assert "CEO" in avatar.role_reaction("Co-founder & CEO")[0]
    assert "intern" in avatar.role_reaction("Summer intern")[0].lower()
    assert "data" in avatar.role_reaction("Senior bioinformatician")[0].lower()
    assert avatar.role_reaction("Chief vibes officer")[0]  # any title gets a line
    assert avatar.role_reaction("")[0] == ""
    for line, _ in avatar.ROLE_REACT.values():
        assert avatar.is_safe(line)


def test_js_rules_serialise_in_priority_order():
    rules = avatar.role_react_js_rules()
    json.dumps(rules)
    assert rules[0][1] == avatar.ROLE_REACT["ceo"][0] and len(rules) > 5


def test_login_hero_carries_rules_and_bubble():
    h = ui.login_hero("<svg class='oneq-avatar'></svg>", "Hello", "Hi there", "sub", ["poke"], [[["cto"], "x", "happy"]], "typing")
    assert 'class="oq-hero login"' in h and "oq-bubble" in h and "data-rules" in h


def test_locked_options_mark_right_and_wrong():
    h = ui.locked_options(["a", "b", "c", "d"], 2, 0)
    assert h.count("oq-opt right") == 1 and h.count("oq-opt wrong") == 1
    assert ui.locked_options(["a", "b", "c", "d"], 1, 1).count("wrong") == 0


def test_table_and_empty_state():
    assert "No flags" in ui.table([], [("a", "A")], "No flags")
    assert "<td>x</td>" in ui.table([{"a": "x"}], [("a", "A")])
    assert "&lt;b&gt;" in ui.table([{"a": "<b>"}], [("a", "A")])


def test_every_mascot_renders_every_expression():
    from oneq import mascots
    assert mascots.ORDER == ["mal", "tee", "helix", "mito", "p53"] and mascots.DEFAULT == "mal"
    for k in mascots.ORDER:
        for e in ["happy", "thinking", "cheering", "oops", "ticklish", "sleepy", "suspicious", "missing"]:
            h = avatar.render(e, mascot=k)
            assert h.startswith("<svg") and f'data-mascot="{k}"' in h and "x-" in h
    assert 'data-mascot="mal"' in avatar.render("happy", mascot=None)
    assert 'data-mascot="mal"' in avatar.render("happy", mascot="unknown")


def test_role_at_sign_in_skips_onboarding(db, monkeypatch):
    monkeypatch.setenv("AUTH_MODE", "demo")
    llm.set_provider(MockLLM())
    try:
        at = AppTest.from_file("../app.py", default_timeout=30).run()
        at.text_input(key="login_email").input("newbie@1cell.ai")
        at.text_input(key="login_role").input("Software engineer").run()
        assert any("engineer" in m.value.lower() for m in at.markdown)
        at.button(key="login_btn").click().run()
        assert not at.exception
        at.button(key="pick_helix").click().run()
        assert not at.exception
        assert not [b for b in at.button if b.key == "ob_start"]
        assert at.radio(key="pl_0")  # straight into placement
    finally:
        llm.set_provider(None)


def test_mascot_column_migrates_old_databases(tmp_path):
    import sqlalchemy as sa
    from oneq import db
    url = f"sqlite:///{tmp_path}/old.sqlite3"
    eng = sa.create_engine(url)
    with eng.begin() as c:  # a pre-mascot schema with one existing user
        c.execute(sa.text("CREATE TABLE users (id INTEGER PRIMARY KEY, email VARCHAR(200))"))
        c.execute(sa.text("CREATE TABLE answers (id INTEGER PRIMARY KEY, user_id INTEGER)"))
        c.execute(sa.text("INSERT INTO users (id, email) VALUES (1, 'old@1cell.ai')"))
    db.get_engine(url)
    with eng.begin() as c:
        assert c.execute(sa.text("SELECT mascot FROM users WHERE id=1")).scalar() == "mal"
        cols = [r[1] for r in c.execute(sa.text("PRAGMA table_info(answers)"))]
    assert "choice" in cols


def test_mascot_choice_is_stored_and_changeable_in_settings(db, monkeypatch):
    from oneq.models import User
    from oneq import db as dbm
    monkeypatch.setenv("AUTH_MODE", "demo")
    llm.set_provider(MockLLM())
    try:
        at = AppTest.from_file("../app.py", default_timeout=30).run()
        at.text_input(key="login_email").input("picky@1cell.ai")
        at.text_input(key="login_role").input("Bioinformatician").run()
        at.button(key="login_btn").click().run()
        at.button(key="pick_p53").click().run()
        with dbm.session() as s:
            assert s.query(User).filter_by(email="picky@1cell.ai").one().mascot == "p53"
        for i in range(5):
            at.radio(key=f"pl_{i}").set_value(0).run()
            at.button(key=f"pl_next_{i}").click().run()
        assert not at.exception
        md = " ".join(m.value for m in at.markdown)
        assert 'data-mascot="p53"' in md  # header renders the chosen character
        assert at.button(key="set_mascot_p53").disabled
        at.button(key="set_mascot_tee").click().run()
        with dbm.session() as s:
            assert s.query(User).filter_by(email="picky@1cell.ai").one().mascot == "tee"
        assert 'data-mascot="tee"' in " ".join(m.value for m in at.markdown)
    finally:
        llm.set_provider(None)


def test_review_shows_the_users_pick(db):
    from datetime import date
    from oneq import db as dbm, quiz_engine as qe
    from oneq.models import User
    q = {"id": "q1", "concept_id": "c1", "subtopic": "hallmarks", "answer_index": 2, "options": ["a", "b", "c", "d"],
         "question": "?", "explanation": "e", "level": 2}
    with dbm.session() as s:
        u = User(email="r@1cell.ai", display_name="R")
        s.add(u); s.flush()
        qe.record_answer(s, u, q, 1, date(2026, 11, 4))
        assert qe.picks_today(s, u, date(2026, 11, 4)) == {"q1": 1}
    h = ui.review_card(1, q, False, 1, "line")
    assert "You picked B" in h and "Your pick: b" in h and 'oq-opt wrong' in h and 'oq-opt right' in h and "Q1." in h


def test_heatmap_fits_and_marks_today():
    from datetime import date, timedelta
    t = date(2026, 11, 4)
    h = ui.heatmap([{"day": t, "points": 12}, {"day": (t - timedelta(days=3)).isoformat(), "points": 4}], t)
    assert h.count("<i class=") >= 18 * 7 and "today" in h and "2 active days" in h
