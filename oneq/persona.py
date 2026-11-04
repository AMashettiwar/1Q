"""Generic role adaptation.

Any role text (a roles.yaml entry or free text) becomes a profile:
  function     wet-lab | computational | engineering | science | clinical | regulatory | business | operations | executive | general
  seniority    early | mid | senior | exec
  familiarity  low | medium | high   (how close the job sits to cancer biology)
  hooks        wholesome humor hooks (pipettes, code, board meetings, grants, ...)
Keyword rules decide first; if nothing matches and an LLM is configured, it classifies the title.
Profiles are cached per role text (and stored per user in session state by the app).
The profile then drives mascot lines, the login greeting, the chat system prompt, the feedback tone
and, for free-text roles, the starting level.
"""
from __future__ import annotations

import json
import re
from functools import lru_cache

FUNCTIONS = ["executive", "regulatory", "clinical", "computational", "engineering", "wet-lab",
             "science", "operations", "business", "general"]
SENIORITY = ["early", "mid", "senior", "exec"]

# Checked in order; first hit wins. Exec titles first, then the more specific functions.
FUNCTION_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("executive", ("ceo", "cto", "coo", "cfo", "cso", "chief", "founder", "president", "executive", "vp ", "vice president")),
    ("regulatory", ("regulat", "quality", "qa", "qc", "compliance")),
    ("clinical", ("clinic", "patholog", "md", "physician", "oncolog", "nurse", "medical", "msl", "trial")),
    ("computational", ("comput", "bioinform", "data scien", "statistic", "biostat")),
    ("wet-lab", ("wet", "lab", "bench", "histo", "research associate", "cell culture")),
    ("engineering", ("software", "engineer", "devops", "developer", " it", "technician", "machine learning", "ml ")),
    ("science", ("phd", "postdoc", "scientist", "biolog", "immunolog", "research")),
    ("operations", ("operation", "supply", "logistic", "facilit", "procure", "office", "admin")),
    ("business", ("sales", "market", "business", "product", "finance", "legal", "hr", "people", "program", "project",
                  "communications", "account")),
]
SENIORITY_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("exec", ("ceo", "cto", "coo", "cfo", "cso", "chief", "founder", "president", "vp ", "vice president", "executive")),
    ("early", ("intern", "student", "co-op", "trainee", "junior", "assistant", "apprentice", "technician")),
    ("senior", ("senior", "sr ", "lead", "principal", "head", "director", "manager", "staff", "phd", "postdoc", "md",
                "pathologist")),
]
FAMILIARITY = {"wet-lab": "high", "science": "high", "clinical": "high", "computational": "medium",
               "regulatory": "medium", "executive": "medium", "engineering": "low", "operations": "low",
               "business": "low", "general": "low"}
HOOKS = {
    "wet-lab": ["pipettes", "Western blots", "incubators", "cell culture"],
    "science": ["grants", "peer review", "lab meetings", "mechanisms"],
    "clinical": ["case conferences", "trial protocols", "biomarkers"],
    "computational": ["pipelines", "priors", "clusters", "notebooks"],
    "engineering": ["code review", "tests", "deploys", "uptime"],
    "regulatory": ["submissions", "audits", "SOPs", "checklists"],
    "business": ["slides", "customers", "pipelines (the sales kind)", "quarterly goals"],
    "operations": ["spreadsheets", "shipments", "freezer inventory", "schedules"],
    "executive": ["board meetings", "strategy", "investor updates", "roadmaps"],
    "general": ["coffee", "curiosity", "fun facts"],
}
# Starting level when a role is not in roles.yaml and no keyword matched.
_LEVEL = {("high", "senior"): 4, ("high", "exec"): 4, ("high", "mid"): 4, ("high", "early"): 2,
          ("medium", "senior"): 2, ("medium", "exec"): 2, ("medium", "mid"): 2, ("medium", "early"): 1}


def _rule(text: str, rules) -> str | None:
    t = f" {text.lower()} "
    for name, keys in rules:
        if any(k in t for k in keys):
            return name
    return None


def _llm_profile(role: str) -> dict | None:
    try:
        from . import llm
        p = llm.get_provider()
        if not p.available():
            return None
        raw = p.chat("Classify a biotech job title. Reply JSON only: {\"function\": one of " + json.dumps(FUNCTIONS) +
                     ", \"seniority\": one of " + json.dumps(SENIORITY) + ", \"hooks\": [2-4 short wholesome workplace "
                     "humor hooks]}." + llm.SAFETY, role[:120], json_mode=True)
        d = json.loads(re.search(r"\{.*\}", raw, re.S).group(0))
        if d.get("function") in FUNCTIONS and d.get("seniority") in SENIORITY:
            from .avatar import is_safe
            hooks = [h for h in d.get("hooks", []) if isinstance(h, str) and is_safe(h)][:4]
            return {"function": d["function"], "seniority": d["seniority"], "hooks": hooks}
    except Exception:
        return None
    return None


@lru_cache(maxsize=512)
def profile(role: str | None) -> dict:
    role = (role or "").strip()
    fn, sen, source = _rule(role, FUNCTION_RULES), _rule(role, SENIORITY_RULES), "rules"
    hooks = None
    if fn is None and role:
        guess = _llm_profile(role)
        if guess:
            fn, sen, hooks, source = guess["function"], sen or guess["seniority"], guess["hooks"] or None, "llm"
    fn = fn or "general"
    sen = sen or ("exec" if fn == "executive" else "mid")
    tech_exec = fn == "executive" and any(k in f" {role.lower()} " for k in ("cto", "technology", "engineering"))
    return {"role": role, "function": fn, "seniority": sen, "familiarity": FAMILIARITY[fn],
            "hooks": hooks or HOOKS[fn], "tech_exec": tech_exec, "source": source}


def bucket(p: dict) -> str:
    """Line-bank key for a profile."""
    fn, sen = p["function"], p["seniority"]
    if fn == "executive":
        return "cto" if p["tech_exec"] else "ceo"
    if sen == "early" and fn in ("general", "business", "operations", "science"):
        return "intern"
    return {"wet-lab": "wetlab", "computational": "comp", "engineering": "tech", "science": "phd",
            "clinical": "clinical", "regulatory": "regulatory", "business": "business",
            "operations": "ops"}.get(fn, "starter")


def start_level(p: dict) -> int:
    return _LEVEL.get((p["familiarity"], p["seniority"]), 1)


# Seniority overlay, appended to first-visit lines so the same function reads right at any level.
SENIORITY_TAGS = {
    "early": "No pressure. Every expert started right here.",
    "mid": "I will pitch it right in your sweet spot.",
    "senior": "I will skip the warm-up questions for you.",
    "exec": "Short, sharp and business-friendly.",
}
FEEDBACK_TONE = {
    "early": "Explain gently from first principles, one everyday analogy.",
    "mid": "Explain clearly with one concrete example.",
    "senior": "Be concise and mechanistic; skip the basics.",
    "exec": "Lead with the one-line takeaway and why it matters for the business, then the science.",
}


def chat_brief(p: dict) -> str:
    return (f"\nRole profile: function {p['function']}, seniority {p['seniority']}, cancer-biology familiarity "
            f"{p['familiarity']}. Tone: {FEEDBACK_TONE[p['seniority']]} Wholesome humor hooks you may use lightly: "
            f"{', '.join(p['hooks'])}.")

EXPLAIN_LABEL = {"early": "In plain words", "mid": "Why", "senior": "Mechanism", "exec": "Business takeaway"}
CHAT_HINT = {"intern": "like I am an intern", "tech": "like a system design doc", "comp": "with the data behind it",
             "phd": "at the mechanism level", "wetlab": "and how we would test it at the bench",
             "clinical": "and where it shows up in trials", "regulatory": "and what regulators look for",
             "business": "for a customer conversation", "ops": "in two sentences", "cto": "as an architecture diagram in words",
             "ceo": "for a board slide", "starter": "simply"}
