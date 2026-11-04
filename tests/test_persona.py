from datetime import datetime

from oneq import avatar, persona, roles


def test_profiles_generalize():
    p = persona.profile("Regulatory Affairs Manager")
    assert (p["function"], p["seniority"]) == ("regulatory", "senior")
    assert persona.profile("Lab Manager")["function"] == "wet-lab"
    assert persona.profile("Data Engineer")["function"] == "engineering"
    assert persona.profile("CTO")["tech_exec"] and persona.bucket(persona.profile("CEO")) == "ceo"
    assert persona.profile("Barista")["function"] == "general"


def test_lines_and_levels_for_any_role():
    now = datetime(2026, 1, 1, 10)
    for r in ("Regulatory Affairs Manager", "Lab Manager", "Data Engineer", "Spatial omics wizard", "Head of People"):
        line = avatar.persona_line(r, now, 0, True, None)
        assert line and avatar.is_safe(line)
        assert "Tone:" in persona.chat_brief(persona.profile(r))
    assert roles.start_level("CEO") == roles.start_level("CTO") == 2
    assert roles.start_level("Senior oncology nurse") >= 2


def test_login_lines():
    assert "Priya" in avatar.login_line(datetime(2026, 1, 1, 9), {"name": "Priya", "role": "PhD scientist", "streak": 4})
    assert avatar.login_line(datetime(2026, 1, 1, 2)) in avatar.LOGIN_LINES["night"]
