"""Adaptive difficulty (Elo per subtopic) and spaced-repetition scheduling.

Pure functions only, so they are easy to test.
"""
from __future__ import annotations

import random
from datetime import date, timedelta

LEVEL_RATING = {1: 800, 2: 1000, 3: 1200, 4: 1400, 5: 1600}
LEVEL_NAMES = {1: "Basics", 2: "Foundation", 3: "Working scientist", 4: "Advanced", 5: "Expert"}

from . import roles as _roles

REVIEW_INTERVALS = [1, 3, 7]  # days; passing the last stage retires the concept
K = 32


def role_start_level(role: str, llm_guess=None) -> int:
    return _roles.start_level(role, llm_guess)


def role_start_rating(role: str, llm_guess=None) -> float:
    return float(LEVEL_RATING[role_start_level(role, llm_guess)])


def expected(rating: float, q_rating: float) -> float:
    return 1.0 / (1.0 + 10 ** ((q_rating - rating) / 400.0))


def update_rating(rating: float, q_level: int, correct: bool, k: float = K) -> float:
    q = LEVEL_RATING.get(int(q_level), 1000)
    return rating + k * ((1.0 if correct else 0.0) - expected(rating, q))


def rating_to_level(rating: float) -> int:
    best = min(LEVEL_RATING, key=lambda lv: abs(LEVEL_RATING[lv] - rating))
    return best


def placement_rating(start: float, results: list[tuple[int, bool]]) -> float:
    """Refine a starting rating from placement answers [(level, correct)]."""
    r = start
    for lvl, ok in results:
        r = update_rating(r, lvl, ok, k=64)
    return max(700.0, min(1700.0, r))


def next_placement_level(start_level: int, results: list[bool]) -> int:
    lvl = start_level
    for ok in results:
        lvl = min(5, lvl + 1) if ok else max(1, lvl - 1)
    return lvl


def pick_subtopics(mastery: dict[str, tuple[float, int]], all_subtopics: list[str], n: int,
                   rng: random.Random | None = None) -> list[str]:
    """Choose n subtopic slots, favoring ones seen least so users meet new material."""
    rng = rng or random.Random()
    weights = []
    for s in all_subtopics:
        seen = mastery.get(s, (0, 0))[1]
        weights.append(1.0 / (1 + seen) + (0.6 if seen == 0 else 0))
    out = []
    for _ in range(n):
        out.append(rng.choices(all_subtopics, weights=weights)[0])
    return out


def split_new_review(total: int, review_due: int) -> tuple[int, int]:
    """About 70% new, 30% review, capped by what is actually due."""
    rev = min(review_due, round(total * 0.3))
    return total - rev, rev


def schedule_after_answer(stage: int, correct: bool, today: date) -> tuple[int, date | None, bool]:
    """Return (new_stage, next_due, retired) for a review item."""
    if not correct:
        return 0, today + timedelta(days=REVIEW_INTERVALS[0]), False
    stage += 1
    if stage >= len(REVIEW_INTERVALS):
        return stage, None, True
    return stage, today + timedelta(days=REVIEW_INTERVALS[stage]), False
