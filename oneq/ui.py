"""Design system: one theme config, CSS, and small HTML helpers.

Two themes share every rule; only the tokens in THEMES differ.
"""
from __future__ import annotations

import html

# Wardrobe palette: the layered colours of a heritage wardrobe. Each tone has a
# light-theme ink (readable on ivory) and a dark-theme ink (readable on green-black).
PALETTE = {
    #  name           light     dark
    "teal":        ("#0f5257", "#6fb7b3"),
    "petrol":      ("#1d4e63", "#7fb0c6"),
    "peacock":     ("#0e5f6e", "#5fb3c2"),
    "navy":        ("#1b2a4a", "#9db0d6"),
    "slate":       ("#46586a", "#a9b8c6"),
    "powder":      ("#456579", "#b8cad6"),
    "forest":      ("#234232", "#8fbf9f"),
    "hunter":      ("#2f4f3a", "#9cc3a6"),
    "bottle":      ("#1f4a3a", "#7fc0a3"),
    "sage":        ("#566550", "#b4c2a5"),
    "moss":        ("#56622f", "#b9c487"),
    "olive":       ("#5f5c2c", "#c6c18a"),
    "camel":       ("#7d5b2c", "#d3b07e"),
    "tan":         ("#77603e", "#d8c09a"),
    "cognac":      ("#86441f", "#d99a6c"),
    "burgundy":    ("#6e2433", "#d58d99"),
    "oxblood":     ("#5a1f27", "#c98a8f"),
    "brass":       ("#7f6430", "#c9a866"),
    "charcoal":    ("#2e3136", "#cfd2d4"),
}
# Each topic wears its own tone so a day's set reads like a well-matched outfit.
TOPIC_TONES = {
    "hallmarks": "teal", "oncogenes": "burgundy", "dna_repair": "petrol", "immunotherapy": "peacock",
    "genomics": "navy", "single_cell": "bottle", "spatial": "sage", "drug_dev": "cognac", "trials": "slate",
    "biomarkers": "camel", "tme": "moss", "epigenetics": "olive", "metastasis": "oxblood", "pathology": "tan",
    "radiation": "powder", "epidemiology": "charcoal", "heme": "burgundy", "cell_biology": "forest",
}
# Leaderboard periods and app sections each get a pairing (accent, partner).
PERIOD_TONES = {"daily": ("teal", "camel"), "weekly": ("petrol", "sage"),
                "monthly": ("navy", "cognac"), "overall": ("bottle", "brass")}
SECTION_TONES = {"quiz": "teal", "leaderboard": "navy", "progress": "forest", "about": "cognac",
                 "admin": "slate", "chat": "peacock", "onboarding": "petrol"}
# Mascot body colour follows the outfit it wears: (light body, dark body).
OUTFIT_TONES = {"": ("#0f5257", "#1f6b6b"), "lab_coat": ("#0f5257", "#1f6b6b"), "goggles": ("#1d4e63", "#2a6680"),
                "headphones": ("#1b2a4a", "#2c3f66"), "crown": ("#1f4a3a", "#2c6450"), "wizard_hat": ("#5a1f27", "#7a333d"),
                "party_hat": ("#86441f", "#9a5a33"), "pipette": ("#56622f", "#6d7a40")}


def tone(name: str, theme: str) -> str:
    light, dark = PALETTE.get(name, PALETTE["teal"])
    return dark if THEMES.get(theme, {}).get("base") == "dark" else light


THEMES = {
    # Light: ivory and cream linen, charcoal text, deep teal and midnight navy leading.
    "ivory": dict(
        bg="#f5f0e6", surface="#fbf8f2", surface2="#efe8da", ink="#24272a", sub="#3f4448", muted="#6b645a",
        line="rgba(36,39,42,.10)", line2="rgba(36,39,42,.17)",
        primary="#0f5257", primary_hi="#13666b", on_primary="#f8f4ec", secondary="#1b2a4a", navy="#1b2a4a",
        brass="#a8874a", brass_ink="#7f6430", brass_soft="rgba(168,135,74,.14)", focus="rgba(15,82,87,.22)",
        good="#1f4a3a", kind="#86441f", camel="#b8935f",
        shadow="0 1px 0 rgba(255,255,255,.7) inset, 0 1px 2px rgba(36,39,42,.04), 0 8px 24px rgba(27,42,74,.07)",
        mascot=("#0f5257", "#f5efe2", "#a8874a"), base="light"),
    # Dark: midnight navy-black with teal undertone, ivory text, brass and powder blue.
    "ink": dict(
        bg="#0d1519", surface="#132026", surface2="#1a2a31", ink="#efe9dc", sub="#d3cdc0", muted="#a39b8c",
        line="rgba(239,233,220,.08)", line2="rgba(239,233,220,.15)",
        primary="#6fb7b3", primary_hi="#86c6c2", on_primary="#0b1417", secondary="#9db0d6", navy="#9db0d6",
        brass="#c9a866", brass_ink="#c9a866", brass_soft="rgba(201,168,102,.14)", focus="rgba(111,183,179,.30)",
        good="#7fc0a3", kind="#d99a6c", camel="#d3b07e",
        shadow="0 1px 0 rgba(255,255,255,.03) inset, 0 1px 2px rgba(0,0,0,.3), 0 12px 32px rgba(0,0,0,.30)",
        mascot=("#1f6b6b", "#efe9dc", "#c9a866"), base="dark"),
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
.oq-line { margin-top:12px; padding-left:16px; border-left:2px solid var(--camel); color:var(--sub); font-size:16px; line-height:1.55;
  animation:oq-fade .4s ease; }

/* surfaces */
.oq-card { background:var(--surface); border:1px solid var(--line); border-radius:12px; padding:24px; margin:16px 0;
  box-shadow:var(--shadow); animation:oq-in .35s cubic-bezier(.2,.7,.2,1); }
.oq-card h3 { margin:8px 0 0; line-height:1.35; color:var(--ink); }
.oq-card p { color:var(--sub); margin:8px 0 0; font-size:15px; line-height:1.6; }
.oq-card.good { border-left:2px solid var(--good); } .oq-card.kind { border-left:2px solid var(--kind); } .oq-card.toned { border-top:2px solid var(--c); }
.oq-meta { display:flex; gap:8px; flex-wrap:wrap; align-items:center; }
.oq-tag { font-size:12px; color:var(--muted); padding:2px 8px; border:1px solid var(--line2); border-radius:6px; }
.oq-tag.accent { color:var(--secondary); border-color:color-mix(in srgb, var(--secondary) 35%, transparent); }
.oq-tag.tone { color:var(--c); border-color:color-mix(in srgb, var(--c) 40%, transparent);
  background:color-mix(in srgb, var(--c) 9%, transparent); }
.oq-sec { border-top:2px solid var(--c, var(--primary)); padding-top:16px; margin-top:8px; }
.oq-sec .oq-eyebrow { color:var(--c); }
.oq-pal { display:flex; gap:4px; margin:8px 0 0; } .oq-pal i { flex:1; height:4px; border-radius:2px; }
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
.oq-pod.p1 .step { height:96px; color:var(--brass-ink); border-top:2px solid var(--brass); } .oq-pod.p2 .step { border-top:2px solid var(--b); } .oq-pod.p3 .step { border-top:2px solid var(--camel); } .oq-pod.p2 .step { height:72px; } .oq-pod.p3 .step { height:56px; }
.oq-pod.p1 { animation-delay:.08s; } .oq-pod.p3 { animation-delay:.16s; }
.oq-mono { width:40px; height:40px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center;
  font-size:14px; font-weight:600; color:var(--mono-ink,#f8f4ec); background:var(--m, var(--primary)); letter-spacing:.02em; }
.oq-pod.p1 .oq-mono { width:52px; height:52px; font-size:16px; box-shadow:0 0 0 2px var(--bg), 0 0 0 3px var(--brass); }
.oq-list { border:1px solid var(--line); border-radius:12px; overflow:hidden; background:var(--surface); margin-top:8px; }
.oq-row { display:flex; align-items:center; gap:16px; padding:12px 16px; border-top:1px solid var(--line); transition:background .15s ease; }
.oq-row:first-child { border-top:none; } .oq-row:hover { background:var(--surface2); }
.oq-row.me { background:color-mix(in srgb, var(--a, var(--brass)) 11%, transparent); box-shadow:inset 2px 0 0 var(--a, var(--brass)); }
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
.stApp input::placeholder, .stApp textarea::placeholder { color:var(--muted) !important; opacity:1; }
.stApp div[data-baseweb="select"], .stApp div[data-baseweb="select"] > div, .stApp div[data-baseweb="select"] div { background-color:var(--surface) !important; color:var(--ink) !important; }
.stApp div[data-baseweb="popover"] ul, .stApp div[data-baseweb="popover"] li { background:var(--surface) !important; color:var(--ink) !important; }
.stApp input, .stApp textarea { border-color:var(--line2) !important; }
div[data-testid="stChatMessage"] [data-testid^="stChatMessageAvatar"] { background:var(--surface2) !important; color:var(--primary) !important; border:1px solid var(--line2); }
div[data-testid="stProgress"] div[role="progressbar"] > div > div { background:var(--primary) !important; }
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


_MONO = ["teal", "petrol", "navy", "bottle", "hunter", "moss", "cognac", "burgundy", "slate", "olive", "peacock", "oxblood"]


def monogram(name: str) -> str:
    parts = [p for p in str(name).replace(".", " ").split() if p]
    ini = (parts[0][0] + (parts[1][0] if len(parts) > 1 else "")).upper() if parts else "?"
    bg = PALETTE[_MONO[sum(map(ord, str(name))) % len(_MONO)]][0]  # deep tones read with ivory text in both themes
    return f'<span class="oq-mono" style="--m:{bg}">{esc(ini)}</span>'


def topic_tag(subtopic: str, label: str, theme: str) -> str:
    return f'<span class="oq-tag tone" style="--c:{tone(TOPIC_TONES.get(subtopic, "teal"), theme)}">{esc(label)}</span>'


def section(key: str, eyebrow: str, theme: str) -> str:
    return (f'<div class="oq-sec" style="--c:{tone(SECTION_TONES.get(key, "teal"), theme)}">'
            f'<div class="oq-eyebrow">{esc(eyebrow)}</div></div>')


def period_vars(period: str, theme: str) -> str:
    a, b = PERIOD_TONES.get(period, PERIOD_TONES["overall"])
    return f"--a:{tone(a, theme)};--b:{tone(b, theme)}"


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


def podium(rows: list[dict], period: str = "overall", theme: str = DEFAULT_THEME) -> str:
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
    return f'<div class="oq-podium" style="{period_vars(period, theme)}">{cells}</div>'


def lb_rows(rows: list[dict], me_id: int, period: str = "overall", theme: str = DEFAULT_THEME) -> str:
    if not rows:
        return ""
    body = "".join(
        f'<div class="oq-row {"me" if r["user_id"] == me_id else ""}"><div class="rk">{r["rank"]}</div>{monogram(r["name"])}'
        f'<div class="who"><b>{esc(r["name"])}</b><span>{esc(r["title"])} · {esc(r["level"])}</span></div>'
        f'<div class="st">{r["streak"]}d</div><div class="sc">{r["score"]:,}</div></div>' for r in rows)
    return f'<div class="oq-list" style="{period_vars(period, theme)}">{body}</div>'


def lb_row(r: dict, me: bool) -> str:
    return lb_rows([r], r["user_id"] if me else -1)


def share_card(name: str, streak: int, rank: int, of: int, title: str, day) -> str:
    return (f"1Q · {day:%b %d}\n{name}, {title}\n"
            f"{streak}-day streak · Rank {rank} of {of}\n"
            f"Today's set: complete\nCan you match my streak? Take today's 1Q.")


def share_html(name: str, streak: int, rank: int, of: int, title: str, day) -> str:
    """Share card: midnight navy with a teal-to-camel rule and brass type. Streak and rank only."""
    return (f'<div style="background:#1b2a4a;color:#f5f0e6;border-radius:12px;padding:24px;margin:16px 0;'
            f'box-shadow:0 8px 24px rgba(27,42,74,.18)">'
            f'<div style="font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:#c9a866">1Q · {day:%b %d}</div>'
            f'<div style="font-family:Fraunces,Georgia,serif;font-size:28px;margin-top:8px">{esc(name)}</div>'
            f'<div style="color:#b8cad6;font-size:14px">{esc(title)}</div>'
            f'<div style="display:flex;gap:4px;margin:16px 0"><i style="flex:2;height:3px;background:#6fb7b3"></i>'
            f'<i style="flex:1;height:3px;background:#7fc0a3"></i><i style="flex:1;height:3px;background:#b8935f"></i>'
            f'<i style="flex:1;height:3px;background:#a8874a"></i></div>'
            f'<div style="font-size:16px">{streak}-day streak · Rank {rank} of {of}</div></div>')
