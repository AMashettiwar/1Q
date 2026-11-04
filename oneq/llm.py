"""LLM provider layer.

Providers register by name. Pick one with LLM_PROVIDER (default "groq").
Every provider exposes chat(system, user) -> str. Everything else (JSON
validation, retries, fallbacks) lives here so swapping providers is a
one-class change. "openai" works with any OpenAI-compatible endpoint
(set OPENAI_API_KEY and optionally OPENAI_BASE_URL).
"""
from __future__ import annotations

import json
import re
from typing import Callable, Literal

from pydantic import BaseModel, Field, ValidationError, field_validator

from . import config


class QuestionModel(BaseModel):
    concept_id: str
    subtopic: str
    level: int = Field(ge=1, le=5)
    type: Literal["mcq"] = "mcq"
    question: str = Field(min_length=10)
    options: list[str]
    answer_index: int
    explanation: str = Field(min_length=10)

    @field_validator("options")
    @classmethod
    def _opts(cls, v):
        v = [str(o).strip() for o in v]
        if len(v) != 4 or len(set(o.lower() for o in v)) != 4 or not all(v):
            raise ValueError("every question must be multiple choice with 4 distinct options")
        return v

    def model_post_init(self, _):
        if not 0 <= self.answer_index < len(self.options):
            raise ValueError("answer_index out of range")


class QuestionList(BaseModel):
    questions: list[QuestionModel]


class Provider:
    name = "base"

    def available(self) -> bool:
        return False

    def chat(self, system: str, user: str, json_mode: bool = False) -> str:  # pragma: no cover
        raise NotImplementedError


FALLBACK_MODELS = ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.6-27b"]


class GroqProvider(Provider):
    name = "groq"

    def __init__(self):
        self.key = config.get("GROQ_API_KEY")
        self.model = config.get("LLM_MODEL", "openai/gpt-oss-120b")

    def available(self):
        return bool(self.key)

    def chat(self, system, user, json_mode=False):
        from groq import Groq
        client = Groq(api_key=self.key, timeout=30)
        kw = {"response_format": {"type": "json_object"}} if json_mode else {}
        err = None
        for m in dict.fromkeys([self.model, *FALLBACK_MODELS]):  # retired models fall through to the next one
            try:
                r = client.chat.completions.create(
                    model=m, temperature=0.7,
                    messages=[{"role": "system", "content": system}, {"role": "user", "content": user}], **kw)
                self.model = m
                return r.choices[0].message.content or ""
            except Exception as e:  # noqa: BLE001
                err = e
                if "model" not in str(e).lower():
                    raise
        raise err


class OpenAICompatProvider(Provider):
    name = "openai"

    def __init__(self):
        self.key = config.get("OPENAI_API_KEY")
        self.base = config.get("OPENAI_BASE_URL")
        self.model = config.get("LLM_MODEL", "gpt-4o-mini")

    def available(self):
        return bool(self.key)

    def chat(self, system, user, json_mode=False):
        from openai import OpenAI  # optional dependency
        client = OpenAI(api_key=self.key, base_url=self.base)
        kw = {"response_format": {"type": "json_object"}} if json_mode else {}
        err = None
        for m in dict.fromkeys([self.model, *FALLBACK_MODELS]):  # retired models fall through to the next one
            try:
                r = client.chat.completions.create(
                    model=m, temperature=0.7,
                    messages=[{"role": "system", "content": system}, {"role": "user", "content": user}], **kw)
                self.model = m
                return r.choices[0].message.content or ""
            except Exception as e:  # noqa: BLE001
                err = e
                if "model" not in str(e).lower():
                    raise
        raise err


class NoneProvider(Provider):
    name = "none"


REGISTRY: dict[str, Callable[[], Provider]] = {
    "groq": GroqProvider, "openai": OpenAICompatProvider, "none": NoneProvider,
}
_override: Provider | None = None


def register(name: str, factory: Callable[[], Provider]):
    REGISTRY[name] = factory


def set_provider(p: Provider | None):
    """Test hook: force a provider instance."""
    global _override
    _override = p


def get_provider() -> Provider:
    if _override is not None:
        return _override
    name = str(config.get("LLM_PROVIDER", "groq")).lower()
    return REGISTRY.get(name, NoneProvider)()


SAFETY = (
    " HARD RULES: Humor must be light, wholesome and playful, like a mascot saying \"Stop, I'm ticklish!\": "
    "science puns and silly self-aware quips only. No edgy, sarcastic or boundary-pushing humor. Never joke about "
    "patients, suffering, illness outcomes, death, politics, religion, or anyone's mistakes. Be kind every time."
)

SYSTEM_Q = (
    "You write cancer-biology quiz questions for staff at 1cell.ai, a single-cell and spatial "
    "oncology company. Be accurate. Prefer short scenario-based stems (a patient, a dataset, an "
    "experiment) over plain recall, so answers cannot be pasted from a search. Plain language. "
    "Return ONLY JSON: {\"questions\": [{\"concept_id\": str, \"subtopic\": str, \"level\": 1-5, "
    "\"type\": \"mcq\", \"question\": str, \"options\": [exactly 4 distinct strings], \"answer_index\": int, \"explanation\": str (2-3 kind, clear "
    "sentences)}]}. Every question is multiple choice with exactly 4 options and one correct answer. No true/false, no free text, no fill-in-the-blank. A 'pick the odd one out' stem is fine if it still has 4 options. Explanations explain only; no sources or references."
    + SAFETY
)


def _extract_json(text: str):
    text = text.strip()
    m = re.search(r"\{.*\}", text, re.S)
    return json.loads(m.group(0) if m else text)


def _ask_json(prompt: str) -> list[dict] | None:
    p = get_provider()
    if not p.available():
        return None
    for _ in range(2):  # one retry on bad JSON
        try:
            raw = p.chat(SYSTEM_Q, prompt, json_mode=True)
            data = _extract_json(raw)
            if isinstance(data, list):
                data = {"questions": data}
            return [q.model_dump() for q in QuestionList.model_validate(data).questions]
        except (ValidationError, ValueError, json.JSONDecodeError):
            continue
        except Exception:
            return None
    return None


def generate_questions(slots: list[tuple[str, int]], avoid: list[str]) -> list[dict] | None:
    """slots: [(subtopic, level)]. Returns validated question dicts or None."""
    want = "\n".join(f"- subtopic={s}, level={lv}" for s, lv in slots)
    prompt = (f"Write {len(slots)} questions, one per line below:\n{want}\n"
              f"Each concept_id must be a short kebab-case slug of the concept tested. "
              f"Avoid these concepts the user has already seen: {', '.join(avoid[-60:]) or 'none'}.")
    return _ask_json(prompt)


def twist_question(q: dict) -> dict | None:
    """Reword a missed question: same concept, new wording, scenario, or distractors."""
    prompt = ("The learner missed this question yesterday. Write ONE new question that tests the "
              "SAME concept with a different scenario, wording, and distractors. It must be multiple choice with exactly 4 options. Keep concept_id, subtopic and level identical.\n" + json.dumps(q))
    out = _ask_json(prompt)
    if out:
        t = out[0]
        t["concept_id"], t["subtopic"] = q["concept_id"], q["subtopic"]
        return t
    return None


def avatar_line(situation: str, name: str) -> str | None:
    p = get_provider()
    if not p.available():
        return None
    try:
        txt = p.chat("You are 1Q, a witty, warm, very smart cell-biology mascot. One line, max 22 "
                     "words, a gentle science pun welcome, no em dashes." + SAFETY,
                     f"Learner {name}. Situation: {situation}. Say one line.")
        from .avatar import is_safe
        txt = txt.strip().strip('"')[:220]
        return txt if txt and is_safe(txt) else None
    except Exception:
        return None


def guess_level(role_text: str) -> int | None:
    """Ask the LLM for a starting level (1-5) for a free-text job title."""
    p = get_provider()
    if not p.available():
        return None
    try:
        txt = p.chat("Map a biotech job title to cancer-biology starting level. Reply with one digit: "
                     "1 basics, 2 intermediate, 4 advanced, 5 expert." + SAFETY, role_text[:120])
        m = re.search(r"[1-5]", txt)
        return int(m.group(0)) if m else None
    except Exception:
        return None
