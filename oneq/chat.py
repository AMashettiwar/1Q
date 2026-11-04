"""1Q chat: cancer-domain Q&A and small talk, with an answer guard during quizzes."""
from __future__ import annotations

import random
import re
import time

from . import persona
from . import avatar, llm

RATE_WINDOW_S, RATE_MAX, DAILY_MAX = 600, 15, 80

REFUSALS = [
    "Nice try! I'm sworn to secrecy until you lock in your answer. Then I will tell you everything.",
    "My lips are sealed. Well, my membrane is. Answer first, then we chat about it.",
    "I would love to help, but that would be a spoiler. Lock it in and I am all yours.",
    "Ooh, sneaky. I only talk about the current question after you answer it.",
]
OFFLINE = [
    "My thinking cloud is on a coffee break, so I am running on pocket knowledge. Ask me again in a minute?",
    "Signal is weak in here, like a faint band on a western blot. Try me again shortly.",
    "My big brain is napping right now, so chat is limited. Try the quiz and I will cheer you on!",
    "I can't reach my thinking cloud at the moment. Ask me again a bit later?",
    "Chat is offline for a moment. Here is a fun fact instead: elephants carry about 20 copies of TP53.",
]
SLOW_DOWN = "Whoa, that is a lot of questions! Give me a minute to catch my breath. Cells need rest too."

SYSTEM = ("You are 1Q, the mascot and study buddy of 1Q, a daily cancer-biology quiz at 1cell.ai. You are very smart, "
          "warm, funny, and encouraging. You answer questions about cancer biology, oncology, immunotherapy, genomics, "
          "single-cell and spatial biology, drug development, trials and biomarkers clearly and accurately, in short "
          "paragraphs. Adapt examples and jokes to the user's role. If asked about medical advice for a real person, say "
          "kindly that you can't give medical advice and suggest talking to their doctor. No em dashes." + llm.SAFETY)


def _tokens(t: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9\-]{4,}", t.lower())}


def asks_about(msg: str, q: dict) -> bool:
    """Does the message look like it is about the active question?"""
    m = msg.lower()
    if re.search(r"\b(answer|which option|correct option|right one|is it [a-d]\b|option [a-d1-4])\b", m):
        return True
    qt = _tokens(q["question"]) | {w for o in q["options"] for w in _tokens(o)}
    overlap = _tokens(msg) & qt
    return len(overlap) >= 3 or any(o.lower() in m for o in q["options"] if len(o) > 5)


def leaks(reply: str, q: dict) -> bool:
    right = q["options"][q["answer_index"]].lower()
    return len(right) > 3 and right in reply.lower()


class RateLimiter:
    def __init__(self, store: dict):
        self.s = store.setdefault("chat_times", [])

    def allow(self, now: float | None = None) -> bool:
        now = now or time.time()
        recent = [t for t in self.s if now - t < RATE_WINDOW_S]
        today = [t for t in self.s if now - t < 86400]
        if len(recent) >= RATE_MAX or len(today) >= DAILY_MAX:
            return False
        self.s.append(now)
        return True


def reply(history: list[dict], msg: str, name: str, role: str | None, active_q: dict | None) -> str:
    if active_q and asks_about(msg, active_q):
        return random.choice(REFUSALS)
    p = llm.get_provider()
    if not p.available():
        if any(k in msg.lower() for k in avatar.KEYWORDS):
            return avatar.KEYWORDS[next(k for k in avatar.KEYWORDS if k in msg.lower())]
        return random.choice(OFFLINE)
    guard = ""
    if active_q:
        guard = ("\nA quiz question is active right now. Never reveal, hint at, or rule out options for it: "
                 f"'{active_q['question']}' Options: {active_q['options']}. If asked, refuse playfully.")
    convo = "\n".join(f"{m['role']}: {m['content']}" for m in history[-8:])
    try:
        out = p.chat(SYSTEM + f"\nUser: {name}, role at 1cell.ai: {role or 'unknown'}." + persona.chat_brief(persona.profile(role)) + guard,
                     f"Conversation so far:\n{convo}\nuser: {msg}\nReply as 1Q.").strip()
    except Exception:
        return random.choice(OFFLINE)
    if not out or not avatar.is_safe_chat(out):
        return "Let me keep things light and kind. Ask me anything about cancer biology and I will dig in!"
    if active_q and leaks(out, active_q):
        return random.choice(REFUSALS)
    return out[:1500]
