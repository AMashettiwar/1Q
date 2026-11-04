"""Roles and starting levels, loaded from roles.yaml at the repo root."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml

LEVELS = {"basics": 1, "intermediate": 2, "advanced": 4, "expert": 5}
OTHER = "Other (type your role)"
PATH = Path(__file__).resolve().parents[1] / "roles.yaml"


@lru_cache(maxsize=1)
def load() -> dict:
    data = yaml.safe_load(PATH.read_text()) or {}
    roles = {r["name"]: LEVELS.get(str(r.get("start_level", "basics")).lower(), 1) for r in data.get("roles", [])}
    kw = {k: [w.lower() for w in v] for k, v in (data.get("keywords") or {}).items()}
    return {"roles": roles, "keywords": kw}


def role_names() -> list[str]:
    return list(load()["roles"]) + [OTHER]


def keyword_level(text: str) -> int | None:
    t = (text or "").lower()
    for lvl in ("expert", "advanced", "intermediate", "basics"):
        if any(w in t for w in load()["keywords"].get(lvl, [])):
            return LEVELS[lvl]
    return None


def start_level(role: str, llm_guess=None) -> int:
    roles = load()["roles"]
    if role in roles:
        return roles[role]
    lvl = keyword_level(role)
    if lvl is None:
        from . import persona
        prof = persona.profile(role)
        if prof["function"] != "general":
            lvl = persona.start_level(prof)
    if lvl is None and llm_guess:
        lvl = llm_guess(role)
    return lvl or 1
