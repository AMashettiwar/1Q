"""Design system: one theme config, CSS, and small HTML helpers.

Two themes share every rule; only the tokens in THEMES differ.
"""
from __future__ import annotations

import html

THEMES = {
    # Default light theme: warm ivory, hunter green, oxblood, antique brass.
    "ivory": dict(
        bg="#f6f1e7", surface="#fbf8f2", surface2="#f1ebdf", ink="#2a2824", sub="#4a463f", muted="#857a6b",
        line="rgba(42,40,36,.10)", line2="rgba(42,40,36,.16)",
        primary="#1f3d2b", primary_hi="#2b513b", on_primary="#f6f1e7", secondary="#6b2a2e", navy="#1e2a44",
        brass="#a8874a", brass_soft="rgba(168,135,74,.14)", focus="rgba(31,61,43,.22)",
        good="#2f5d43", kind="#9a7a3c",
        shadow="0 1px 0 rgba(255,255,255,.7) inset, 0 1px 2px rgba(42,40,36,.04), 0 8px 24px rgba(42,40,36,.06)",
        mascot=("#1f3d2b", "#f4efe4", "#a8874a"), base="light"),
    # Dark theme: green-black ink, ivory text, brass accents.
    "ink": dict(
        bg="#0e1512", surface="#141d19", surface2="#1a2520", ink="#efe9dc", sub="#d6cfc0", muted="#9d9483",
        line="rgba(239,233,220,.08)", line2="rgba(239,233,220,.14)",
        primary="#c2a061", primary_hi="#d1b073", on_primary="#11180f", secondary="#b7676b", navy="#9fb0d0",
        brass="#c2a061", brass_soft="rgba(194,160,97,.14)", focus="rgba(194,160,97,.28)",
        good="#7fb08f", kind="#d0ad6a",
        shadow="0 1px 0 rgba(255,255,255,.03) inset, 0 1px 2px rgba(0,0,0,.3), 0 12px 32px rgba(0,0,0,.28)",
        mascot=("#2f5d43", "#efe9dc", "#c2a061"), base="dark"),
}
DEFAULT_THEME = "ivory"
ALT_THEME = "ink"

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter:wght@400;500;600&display=swap');
__VARS__
/* type scale 12 / 14 / 16 / 20 / 28 / 36, spacing on an 8px grid */
html, body, .stApp, .stMarkdown, p, label, input, textarea, button { font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;
  font-feature-settings:'cv11','ss01'; -webkit-font-smoothing:antialiased; }
h1, h2, h3, .oq-display { font-family:'Fraunces',Georgia,serif !important; font-weight:600 !important; letter-spacing:-.015em; }
.stApp { background:var(--bg); color:var(--ink); }
.stApp .stMarkdown, .stApp label, .stApp [data-testid="stMetricValue"], .stApp h1, .stApp h2, .stApp h3, .stApp p { color:var(--ink); }
.stApp [data-testid="stCaptionContainer"], .stApp [data-testid="stMetricLabel"] p { color:var(--muted) !important; }
header[data-testid="stHeader"] { background:transparent; }
.block-container { max-width:760px; padding:40px 24px 96px; }
section[data-testid="stSidebar"] { background:var(--surface); border-right:1px solid var(--line); }
section[data-testid="stSidebar"] .block-container { padding-top:24px; }
h2 { font-size:28px !important; } h3 { font-size:20px !important; }

/* header block */
.oq-hero { display:flex; gap:24px; align-items:center; padding:24px 0 24px; border-bottom:1px solid var(--line); margin-bottom:24px;
  animation:oq-in .5s cubic-bezier(.2,.7,.2,1); }
.oq-hero h1 { font-size:36px; line-height:1.1; margin:0; padding:0; color:var(--ink); }
.oq-eyebrow { font-size:12px; letter-spacing:.14em; text-transform:uppercase; color:var(--muted); font-weight:500; margin-bottom:8px; }
.oq-line { margin-top:12px; padding-left:16px; border-left:2px solid var(--brass); color:var(--sub); font-size:16px; line-height:1.55;
  animation:oq-fade .4s ease; }

/* surfaces */
.oq-card { background:var(--surface); border:1px solid var(--line); border-radius:12px; padding:24px; margin:16px 0;
  box-shadow:var(--shadow); animation:oq-in .35s cubic-bezier(.2,.7,.2,1); }
.oq-card h3 { margin:8px 0 0; line-height:1.35; color:var(--ink); }
.oq-card p { color:var(--sub); margin:8px 0 0; font-size:15px; line-height:1.6; }
.oq-card.good { border-left:2px solid var(--good); } .oq-card.kind { border-left:2px solid var(--kind); }
.oq-meta { display:flex; gap:8px; flex-wrap:wrap; align-items:center; }
.oq-tag { font-size:12px; color:var(--muted); padding:2px 8px; border:1px solid var(--line2); border-radius:6px; }
.oq-tag.accent { color:var(--secondary); border-color:color-mix(in srgb, var(--secondary) 35%, transparent); }
.oq-tag.brass { color:var(--brass); border-color:color-mix(in srgb, var(--brass) 45%, transparent); }
.oq-note { padding:16px 24px; margin:16px 0; border-radius:12px; background:var(--surface2); border:1px solid var(--line);
  color:var(--sub); font-size:15px; line-height:1.6; }
.oq-note b { color:var(--ink); font-weight:600; }
.oq-small { font-size:13px; color:var(--muted); }

/* progress ring */
.oq-ring { display:flex; align-items:center; gap:16px; margin:8px 0 0; }
.oq-ring svg circle.fg { transition:stroke-dashoffset .9s cubic-bezier(.2,.7,.2,1); }
.oq-ring .t { font-size:14px; color:var(--muted); line-height:1.4; } .oq-ring .t b { color:var(--ink); font-weight:600; }

/* leaderboard */
.oq-standing { display:flex; justify-content:space-between; align-items:baseline; }
.oq-standing .big { font-family:'Fraunces',serif; font-size:36px; color:var(--ink); }
.oq-podium { display:grid; grid-template-columns:1fr 1fr 1fr; gap:16px; align-items:end; margin:24px 0 8px; }
.oq-pod { text-align:center; animation:oq-rise .6s cubic-bezier(.2,.7,.2,1) both; }
.oq-pod .nm { font-weight:600; font-size:14px; color:var(--ink); margin-top:8px; }
.oq-pod .sc { font-size:13px; color:var(--muted); font-variant-numeric:tabular-nums; }
.oq-pod .step { margin-top:12px; border-radius:8px 8px 0 0; border:1px solid var(--line); border-bottom:none; background:var(--surface);
  font-family:'Fraunces',serif; font-size:20px; color:var(--muted); display:flex; align-items:flex-start; justify-content:center; padding-top:8px; }
.oq-pod.p1 .step { height:96px; color:var(--brass); border-top:2px solid var(--brass); } .oq-pod.p2 .step { height:72px; } .oq-pod.p3 .step { height:56px; }
.oq-pod.p1 { animation-delay:.08s; } .oq-pod.p3 { animation-delay:.16s; }
.oq-mono { width:40px; height:40px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center;
  font-size:14px; font-weight:600; color:var(--on-primary); background:var(--primary); letter-spacing:.02em; }
.oq-pod.p1 .oq-mono { width:52px; height:52px; font-size:16px; box-shadow:0 0 0 2px var(--bg), 0 0 0 3px var(--brass); }
.oq-list { border:1px solid var(--line); border-radius:12px; overflow:hidden; background:var(--surface); margin-top:8px; }
.oq-row { display:flex; align-items:center; gap:16px; padding:12px 16px; border-top:1px solid var(--line); transition:background .15s ease; }
.oq-row:first-child { border-top:none; } .oq-row:hover { background:var(--surface2); }
.oq-row.me { background:var(--brass-soft); }
.oq-row .rk { width:28px; color:var(--muted); font-variant-numeric:tabular-nums; font-size:14px; }
.oq-row .who { flex:1; } .oq-row .who b { font-weight:600; font-size:14px; color:var(--ink); }
.oq-row .who span { display:block; font-size:12px; color:var(--muted); }
.oq-row .st, .oq-row .sc { font-size:13px; color:var(--muted); font-variant-numeric:tabular-nums; min-width:56px; text-align:right; }
.oq-row .sc { color:var(--ink); font-weight:600; }
.oq-row .oq-mono { width:32px; height:32px; font-size:12px; }
.oq-empty { text-align:center; padding:40px 24px; color:var(--muted); border:1px dashed var(--line2); border-radius:12px; font-size:14px; }

/* controls */
.stButton > button, .stFormSubmitButton > button { border-radius:8px; font-weight:500; font-size:14px; min-height:40px;
  border:1px solid var(--line2); background:var(--surface); color:var(--ink); box-shadow:none;
  transition:background .15s ease, border-color .15s ease, transform .1s ease; }
.stButton > button:hover, .stFormSubmitButton > button:hover { border-color:var(--ink); color:var(--ink); background:var(--surface2); }
.stButton > button:active { transform:scale(.985); }
.stButton > button:focus-visible, .stFormSubmitButton > button:focus-visible { box-shadow:0 0 0 3px var(--focus); outline:none; }
.stButton > button[kind="primary"] { background:var(--primary); color:var(--on-primary); border-color:var(--primary); }
.stButton > button[kind="primary"]:hover { background:var(--primary-hi); border-color:var(--primary-hi); color:var(--on-primary); }
.stButton > button[kind="primary"] p { color:var(--on-primary) !important; }
.stButton > button:disabled { opacity:.45; }
div[role="radiogroup"] { display:flex !important; flex-direction:column; gap:8px; width:100%; }
div[role="radiogroup"] label { width:100%; margin:0 !important; padding:14px 16px; border-radius:10px; background:var(--surface);
  border:1px solid var(--line2); transition:border-color .15s ease, background .15s ease, box-shadow .15s ease; }
div[role="radiogroup"] label:hover { border-color:var(--muted); }
div[role="radiogroup"] label:has(input:checked) { border-color:var(--primary); box-shadow:0 0 0 3px var(--focus); }
div[role="radiogroup"] label p { color:var(--ink) !important; font-size:15px; }
.stTextInput input, .stSelectbox div[data-baseweb="select"] > div { border-radius:8px !important; background:var(--surface) !important; color:var(--ink) !important; }
button[data-baseweb="tab"] { font-size:14px; font-weight:500; color:var(--muted); }
button[data-baseweb="tab"][aria-selected="true"] { color:var(--ink); }
div[data-baseweb="tab-highlight"] { background:var(--primary) !important; height:2px; }
div[data-baseweb="tab-border"] { background:var(--line) !important; }
div[data-testid="stProgress"] > div > div > div > div { background:var(--primary) !important; }
div[data-testid="stMetric"] { border-top:1px solid var(--line); padding-top:8px; }
div[data-testid="stMetricValue"] { font-family:'Fraunces',serif; font-size:24px !important; }
div[data-testid="stChatMessage"] { background:transparent; padding:8px 0; }
.st-key-oneq_hidden { display:none !important; }
.oq-chat-head { font-family:'Fraunces',serif; font-size:18px; margin:24px 0 8px; color:var(--ink); }

/* mascot motion: slow and quiet */
.oneq-avatar { flex-shrink:0; }
.oneq-float { animation:oq-float 5s ease-in-out infinite; }
.oneq-bounce { animation:oq-bounce 1.2s cubic-bezier(.3,.7,.3,1) infinite; }
.oneq-wiggle { animation:oq-wiggle .4s ease-in-out infinite; }
.oneq-breathe { animation:oq-breathe 5s ease-in-out infinite; }
.oneq-avatar .blink { animation:oq-blink 6s infinite; transform-origin:60px 54px; }
.oneq-avatar .oneq-orbit { animation:oq-spin 24s linear infinite; transform-origin:60px 60px; }
@keyframes oq-float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-3px)} }
@keyframes oq-bounce { 0%,100%{transform:translateY(0)} 40%{transform:translateY(-6px)} }
@keyframes oq-wiggle { 0%,100%{transform:rotate(-4deg)} 50%{transform:rotate(4deg)} }
@keyframes oq-breathe { 0%,100%{opacity:1} 50%{opacity:.8} }
@keyframes oq-blink { 0%,95%,100%{transform:scaleY(1)} 97%{transform:scaleY(.1)} }
@keyframes oq-spin { to { transform:rotate(360deg); } }
@keyframes oq-in { from{opacity:0; transform:translateY(6px)} to{opacity:1; transform:none} }
@keyframes oq-fade { from{opacity:0} to{opacity:1} }
@keyframes oq-rise { from{opacity:0; transform:translateY(12px)} to{opacity:1; transform:none} }
@media (prefers-reduced-motion: reduce) { * { animation:none !important; transition:none !important; } }
@media (max-width:640px) {
  .block-container { padding:24px 16px 80px; }
  .oq-hero { gap:16px; } .oq-hero h1 { font-size:28px; } .oneq-avatar { width:72px; height:72px; }
  .oq-card { padding:16px; } .oq-podium { gap:8px; }
}
</style>
"""


def css(theme: str = DEFAULT_THEME) -> str:
    t = THEMES.get(theme, THEMES[DEFAULT_THEME])
    vars_ = ":root {" + "".join(f"--{k.replace('_', '-')}:{v};" for k, v in t.items() if isinstance(v, str)) + "}"
    if t["base"] == "dark":
        vars_ += " :root { color-scheme: dark; }"
    return _CSS.replace("__VARS__", vars_)


CSS = css()

SIGNALS_JS = """
<script>
(function(){
  const P = window; if (!P || P.__oneqSignals) return; P.__oneqSignals = {copy:0, paste:0, blur:0};
  const push = () => {
    const el = P.document.querySelector('.st-key-oneq_hidden input');
    if (!el) return;
    const setter = Object.getOwnPropertyDescriptor(P.HTMLInputElement.prototype, 'value').set;
    const active = P.document.activeElement;
    el.focus();
    setter.call(el, JSON.stringify(P.__oneqSignals));
    el.dispatchEvent(new Event('input', {bubbles:true}));
    el.blur();
    if (active && active.focus) active.focus();
  };
  P.document.addEventListener('copy', () => { P.__oneqSignals.copy++; });
  P.document.addEventListener('paste', () => { P.__oneqSignals.paste++; });
  P.document.addEventListener('visibilitychange', () => { if (P.document.hidden) P.__oneqSignals.blur++; else push(); });
  P.document.addEventListener('mousedown', (e) => { if ((e.target.innerText||'').match(/Submit today/)) push(); }, true);
})();
</script>
"""


def esc(t) -> str:
    return html.escape(str(t))


def monogram(name: str) -> str:
    parts = [p for p in str(name).replace(".", " ").split() if p]
    ini = (parts[0][0] + (parts[1][0] if len(parts) > 1 else "")).upper() if parts else "?"
    return f'<span class="oq-mono">{esc(ini)}</span>'


def hero(svg: str, title: str, line: str, sub: str = "") -> str:
    return (f'<div class="oq-hero">{svg}<div style="flex:1">'
            f'{f"<div class=oq-eyebrow>{esc(sub)}</div>" if sub else ""}<h1>{esc(title)}</h1>'
            f'<div class="oq-line">{esc(line)}</div></div></div>')


def tag(text: str, cls: str = "") -> str:
    return f'<span class="oq-tag {cls}">{esc(text)}</span>'


chip = tag


def progress_ring(done: int, total: int) -> str:
    r = 20
    c = 2 * 3.14159 * r
    off = c * (1 - (done / total if total else 0))
    return (f'<div class="oq-ring"><svg width="48" height="48" viewBox="0 0 48 48" aria-hidden="true">'
            f'<circle cx="24" cy="24" r="{r}" stroke="var(--line2)" stroke-width="3" fill="none"/>'
            f'<circle class="fg" cx="24" cy="24" r="{r}" stroke="var(--primary)" stroke-width="3" fill="none" stroke-linecap="round" '
            f'stroke-dasharray="{c:.1f}" stroke-dashoffset="{off:.1f}" transform="rotate(-90 24 24)"/></svg>'
            f'<div class="t"><b>{done} of {total}</b><br>Answers lock when you check them.</div></div>')


def podium(rows: list[dict]) -> str:
    if not rows:
        return '<div class="oq-empty">No one on this board yet. Finish today\'s set to take the first spot.</div>'
    slots = {1: rows[0], 2: rows[1] if len(rows) > 1 else None, 3: rows[2] if len(rows) > 2 else None}
    cells = ""
    for n in (2, 1, 3):
        r = slots[n]
        if r is None:
            cells += "<div></div>"
            continue
        cells += (f'<div class="oq-pod p{n}">{monogram(r["name"])}<div class="nm">{esc(r["name"])}</div>'
                  f'<div class="sc">{r["score"]:,} pts · {r["streak"]}d streak</div><div class="step">{n}</div></div>')
    return f'<div class="oq-podium">{cells}</div>'


def lb_rows(rows: list[dict], me_id: int) -> str:
    if not rows:
        return ""
    body = "".join(
        f'<div class="oq-row {"me" if r["user_id"] == me_id else ""}"><div class="rk">{r["rank"]}</div>{monogram(r["name"])}'
        f'<div class="who"><b>{esc(r["name"])}</b><span>{esc(r["title"])} · {esc(r["level"])}</span></div>'
        f'<div class="st">{r["streak"]}d</div><div class="sc">{r["score"]:,}</div></div>' for r in rows)
    return f'<div class="oq-list">{body}</div>'


def lb_row(r: dict, me: bool) -> str:
    return lb_rows([r], r["user_id"] if me else -1)


def share_card(name: str, streak: int, rank: int, of: int, title: str, day) -> str:
    return (f"1Q · {day:%b %d}\n{name}, {title}\n"
            f"{streak}-day streak · Rank {rank} of {of}\n"
            f"Today's set: complete\nCan you match my streak? Take today's 1Q.")
