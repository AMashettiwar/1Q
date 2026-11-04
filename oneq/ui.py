"""Design system: one theme config, CSS, and small HTML helpers.

Two themes share every rule; only the tokens in THEMES differ.
"""
from __future__ import annotations

import html
import json

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
.block-container { max-width:1360px; padding:40px 48px 96px; margin:0 auto; }
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
.stRadio, .stRadio > div, div[data-testid="stRadio"] > div, div[role="radiogroup"] label > div:last-child { width:100% !important; max-width:100% !important; }
div[role="radiogroup"] { display:flex !important; flex-direction:column; gap:8px; width:100%; }
div[role="radiogroup"] label { width:100%; margin:0 !important; padding:14px 16px; border-radius:10px; background:var(--surface);
  border:1px solid var(--line2); transition:border-color .15s ease, background .15s ease, box-shadow .15s ease; }
div[role="radiogroup"] label:hover { border-color:var(--muted); }
div[role="radiogroup"] label:is(:has(input:checked),[data-selected="true"]) { border-color:var(--primary); box-shadow:0 0 0 3px var(--focus); }
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
.stSelectbox div[role="group"] { background:var(--surface) !important; border:1px solid var(--line2) !important; border-radius:8px !important; }
.stSelectbox div[role="group"] input, .stSelectbox div[role="group"] button { background:transparent !important; color:var(--ink) !important; }
div[role="listbox"], .react-aria-Popover, .react-aria-ListBox { background:var(--surface) !important; color:var(--ink) !important; border:1px solid var(--line2); }
div[role="listbox"] [role="option"] { color:var(--ink) !important; }
div[role="listbox"] [role="option"][data-focused], div[role="listbox"] [role="option"]:hover { background:var(--surface2) !important; }
.stApp input::placeholder, .stApp textarea::placeholder { color:var(--muted) !important; opacity:1; }
.stApp div[data-baseweb="select"], .stApp div[data-baseweb="select"] > div, .stApp div[data-baseweb="select"] div { background-color:var(--surface) !important; color:var(--ink) !important; }
.stApp div[data-baseweb="popover"] ul, .stApp div[data-baseweb="popover"] li { background:var(--surface) !important; color:var(--ink) !important; }
.stApp input, .stApp textarea { border-color:var(--line2) !important; }
div[data-testid="stChatMessage"] [data-testid^="stChatMessageAvatar"] { background:var(--surface2) !important; color:var(--primary) !important; border:1px solid var(--line2); }
div[data-testid="stProgress"] div[role="progressbar"] > div > div { background:var(--primary) !important; }
.st-key-oneq_hidden { display:none !important; }
.oq-chat-head { font-family:'Fraunces',serif; font-size:18px; margin:24px 0 8px; color:var(--ink); }

/* ---------- 1Q, the living mascot ----------
   Layers: .m-rig (pointer lean, set by JS) > .m-body (squash/stretch) > .m-face (look-at) > .m-eyes (blink).
   All parts use transform-box so origins sit on the character, and every motion is spring-eased. */
.oneq-avatar { flex-shrink:0; overflow:visible; cursor:pointer; -webkit-tap-highlight-color:transparent; }
.oneq-avatar * { transform-box:fill-box; }
.oneq-avatar .m-rig { transform-origin:50% 100%; transition:transform .5s var(--spring); }
.oneq-avatar .m-body { transform-origin:50% 100%; animation:m-breathe 4.2s ease-in-out infinite; }
.oneq-avatar .m-face { transition:transform .35s var(--spring); }
.oneq-avatar .m-eyes { transform-origin:50% 50%; transition:transform .09s ease-in; }
.oneq-avatar.blinking .m-eyes { transform:scaleY(.08); }
.oneq-avatar .m-mouth { transform-origin:50% 30%; }
.oneq-avatar.talking .m-mouth { animation:m-talk .18s ease-in-out infinite alternate; }
.oneq-avatar.talking .m-body { animation:m-talkbob .36s ease-in-out infinite alternate; }
.oneq-avatar .m-orbit { transform-origin:50% 50%; animation:m-spin 28s linear infinite; }
.oneq-avatar .m-shadow { transform-origin:50% 50%; animation:m-shadow 4.2s ease-in-out infinite; }
.oneq-avatar .m-burst { opacity:0; transform-origin:50% 50%; }
.oneq-avatar .m-z { opacity:0; }
.oneq-avatar .m-cheeks { transition:opacity .4s ease; }
.oneq-avatar:hover .m-cheeks, .oneq-avatar[data-react="joy"] .m-cheeks, .oneq-avatar[data-react="shake"] .m-cheeks { opacity:.35; }
.oneq-avatar:hover .m-rig { animation:m-wave .9s var(--spring) 1; }
.oneq-avatar.poked .m-body { animation:m-squash .5s var(--spring) 1; }
/* reactions, replayed by JS whenever the server sends a new one */
.oneq-avatar.react[data-react="joy"] .m-body { animation:m-joy 1.1s var(--spring) 1, m-breathe 4.2s ease-in-out 1.1s infinite; }
.oneq-avatar.react[data-react="joy"] .m-burst { animation:m-burst .9s cubic-bezier(.2,.8,.2,1) .35s 1; }
.oneq-avatar.react[data-react="joy"] .m-shadow { animation:m-shadowjump 1.1s var(--spring) 1; }
.oneq-avatar[data-react="empathy"] .m-rig { animation:m-empathy 1.6s cubic-bezier(.3,.7,.3,1) 1 forwards; }
.oneq-avatar[data-react="think"] .m-rig { animation:m-think 3.6s ease-in-out infinite; }
.oneq-avatar[data-react="sleep"] .m-body { animation:m-breathe 6.5s ease-in-out infinite; }
.oneq-avatar[data-react="sleep"] .m-z { animation:m-z 3.2s ease-in-out infinite; }
.oneq-avatar[data-react="shake"] .m-rig { animation:m-shake .5s ease-in-out 2; }
.oneq-avatar[data-react="squint"] .m-rig { animation:m-squint 2.4s ease-in-out 1; }
@keyframes m-breathe { 0%,100%{transform:scale(1,1)} 50%{transform:scale(1.018,.985)} }
@keyframes m-shadow { 0%,100%{transform:scaleX(1)} 50%{transform:scaleX(1.04)} }
@keyframes m-talk { from{transform:scaleY(.7)} to{transform:scaleY(1.25)} }
@keyframes m-talkbob { from{transform:translateY(0) scale(1,1)} to{transform:translateY(-1.5px) scale(.99,1.01)} }
@keyframes m-spin { to{transform:rotate(360deg)} }
@keyframes m-wave { 0%{transform:rotate(0)} 25%{transform:rotate(-7deg)} 55%{transform:rotate(5deg)} 80%{transform:rotate(-2deg)} 100%{transform:rotate(0)} }
@keyframes m-squash { 0%{transform:scale(1,1)} 25%{transform:scale(1.12,.86)} 55%{transform:scale(.94,1.08)} 80%{transform:scale(1.02,.98)} 100%{transform:scale(1,1)} }
@keyframes m-joy { 0%{transform:translateY(0) scale(1,1)} 18%{transform:translateY(0) scale(1.14,.84)}
  42%{transform:translateY(-22px) scale(.9,1.12)} 62%{transform:translateY(0) scale(1.1,.9)} 78%{transform:translateY(-4px) scale(.98,1.02)} 100%{transform:translateY(0) scale(1,1)} }
@keyframes m-shadowjump { 0%,100%{transform:scaleX(1);opacity:.16} 42%{transform:scaleX(.6);opacity:.07} }
@keyframes m-burst { 0%{opacity:0;transform:scale(.7)} 30%{opacity:1} 100%{opacity:0;transform:scale(1.25)} }
@keyframes m-empathy { 0%{transform:rotate(0) translateY(0)} 40%{transform:rotate(-6deg) translateY(2px)} 100%{transform:rotate(-3deg) translateY(1px)} }
@keyframes m-think { 0%,100%{transform:rotate(0)} 30%,70%{transform:rotate(5deg) translateY(-1px)} }
@keyframes m-z { 0%{opacity:0;transform:translate(0,4px)} 30%{opacity:.9} 100%{opacity:0;transform:translate(6px,-10px)} }
@keyframes m-shake { 0%,100%{transform:rotate(0)} 20%{transform:rotate(-9deg)} 40%{transform:rotate(8deg)} 60%{transform:rotate(-6deg)} 80%{transform:rotate(4deg)} }
@keyframes m-squint { 0%,100%{transform:translateX(0)} 30%{transform:translateX(-3px)} 60%{transform:translateX(3px)} }
.oq-line .caret { display:inline-block; width:1px; height:1em; background:var(--ink); margin-left:2px; vertical-align:-2px; animation:oq-caret .9s steps(1) infinite; }
@keyframes oq-caret { 50%{opacity:0} }
@keyframes oq-in { from{opacity:0; transform:translateY(6px)} to{opacity:1; transform:none} }
@keyframes oq-fade { from{opacity:0} to{opacity:1} }
@keyframes oq-rise { from{opacity:0; transform:translateY(12px)} to{opacity:1; transform:none} }
@media (prefers-reduced-motion: reduce) { * { animation:none !important; transition:none !important; } }
@media (max-width:640px) {
  .block-container { padding:24px 16px 80px; }
  .oq-hero { gap:16px; } .oq-hero h1 { font-size:28px; } .oneq-avatar { width:72px; height:72px; }
  .oq-card { padding:16px; } .oq-podium { gap:8px; }
}
/* ================= expert layer: tokens, chrome, components ================= */
:root { --r-sm:6px; --r-md:10px; --r-lg:14px; --r-xl:20px;
  --e1:0 1px 2px rgba(15,25,30,.05); --e2:0 1px 2px rgba(15,25,30,.04), 0 6px 16px rgba(15,25,30,.06);
  --e3:0 2px 4px rgba(15,25,30,.05), 0 18px 40px rgba(15,25,30,.10); }
/* hide default Streamlit chrome, keep the sidebar control */
[data-testid="stToolbar"], [data-testid="stDecoration"], #MainMenu, footer, [data-testid="stStatusWidget"],
.stDeployButton, [data-testid="stAppDeployButton"] { display:none !important; }
header[data-testid="stHeader"] { height:48px; background:transparent !important; }
[data-testid="stHeaderActionElements"], .stMarkdown a.anchor-link, [data-testid="stHeadingWithActionElements"] a { display:none !important; }
.sr-only { position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0 0 0 0); white-space:nowrap; }
/* type: fluid display sizes with optical sizing; 4px baseline rhythm */
body { font-size:15px; line-height:1.6; }
.oq-display, .oq-hero h1, h1, h2 { font-optical-sizing:auto; text-wrap:balance; }
.oq-hero h1 { font-size:clamp(28px, 1.6vw + 18px, 44px); line-height:1.08; letter-spacing:-.02em; }
h2, .oq-display { font-size:clamp(24px, 1vw + 18px, 32px) !important; line-height:1.15; margin:4px 0 8px !important; }
.oq-card h3 { font-size:clamp(18px, .5vw + 15px, 22px) !important; text-wrap:pretty; }
.oq-num, .oq-row .sc, .oq-row .st, .oq-pod .sc, .oq-stat .v, .oq-ring .t b { font-variant-numeric:tabular-nums; font-feature-settings:"tnum"; }
.oq-ic { vertical-align:-2px; flex-shrink:0; }
/* surfaces use the elevation scale */
.oq-card { border-radius:var(--r-lg); box-shadow:var(--e2); }
.oq-note { border-radius:var(--r-md); }
/* hero */
.oq-hero { padding:16px 0 24px; gap:clamp(16px, 2vw, 32px); }
.oq-hero .oneq-avatar { width:clamp(84px, 6vw + 48px, 128px); height:auto; }
.oq-line { min-height:1.6em; }
/* progress charts */
.oq-chart { animation:oq-in .6s var(--ease) both; }
.oq-radar svg { max-width:420px; display:block; margin:0 auto; overflow:visible; }
.oq-rshape { transform-origin:50% 50%; transform-box:view-box; animation:oq-grow .9s var(--spring) both; }
.oq-rdot { opacity:0; animation:oq-fade .3s var(--ease) both; }
@keyframes oq-grow { from { transform:scale(.2); opacity:0; } to { transform:scale(1); opacity:1; } }
@keyframes oq-fade { to { opacity:1; } }
[data-testid="stVegaLiteChart"], [data-testid="stArrowVegaLiteChart"] { animation:oq-in .6s var(--ease) both; }
[data-testid="stVerticalBlock"] > div:nth-child(2) [data-testid="stVegaLiteChart"] { animation-delay:.08s; }
@media (prefers-reduced-motion: reduce) { .oq-rshape, .oq-rdot, .oq-chart { animation:none !important; opacity:1; } }
/* segmented tabs (react-aria tabs in Streamlit 1.66) */
div[role="tablist"] { gap:4px; padding:4px; background:var(--surface2); border:1px solid var(--line); border-radius:12px; width:fit-content; max-width:100%;
  overflow-x:auto; scrollbar-width:none; border-bottom:1px solid var(--line) !important; box-shadow:none !important; }
div[role="tablist"]::-webkit-scrollbar { display:none; }
div[role="tablist"]::after, div[role="tablist"]::before { display:none !important; }
[data-testid="stTab"] { height:36px; padding:0 16px !important; border-radius:9px; display:flex; align-items:center; margin:0 !important;
  transition:background .2s var(--ease), color .2s var(--ease), box-shadow .2s var(--ease); white-space:nowrap; color:var(--muted); border:none !important; }
[data-testid="stTab"] p { font-size:14px !important; font-weight:500; color:inherit !important; margin:0; }
[data-testid="stTab"]:hover { color:var(--ink); }
[data-testid="stTab"][aria-selected="true"] { background:var(--surface); box-shadow:var(--e1), 0 0 0 1px var(--line); color:var(--ink); }
.react-aria-SelectionIndicator, div[data-baseweb="tab-highlight"], div[data-baseweb="tab-border"] { display:none !important; }
div[role="tabpanel"] { padding-top:24px; animation:oq-in .4s var(--ease); }
/* answer option cards: letter key, press, select, lock */
[data-testid="stElementContainer"]:has(> [data-testid="stRadio"]), [data-testid="stRadio"], [data-testid="stRadio"] > div,
div[role="radiogroup"], div[role="radiogroup"] label { width:100% !important; max-width:100% !important; }
div[role="radiogroup"] { display:flex !important; flex-direction:column; align-items:stretch !important; gap:8px; counter-reset:opt; }
div[role="radiogroup"] label { counter-increment:opt; position:relative; display:flex !important; align-items:center; min-height:56px;
  padding:14px 16px 14px 60px !important; border-radius:var(--r-md) !important; background:var(--surface); border:1px solid var(--line2);
  box-shadow:var(--e1); cursor:pointer; transition:border-color .18s var(--ease), box-shadow .18s var(--ease), transform .12s var(--ease), background .18s var(--ease);
  animation:oq-in .45s var(--ease) both; }
div[role="radiogroup"] label:nth-child(2) { animation-delay:.05s; } div[role="radiogroup"] label:nth-child(3) { animation-delay:.1s; }
div[role="radiogroup"] label:nth-child(4) { animation-delay:.15s; }
div[role="radiogroup"] label::before { content:counter(opt, upper-alpha); position:absolute; left:16px; top:50%; transform:translateY(-50%);
  width:28px; height:28px; border-radius:8px; display:grid; place-items:center; font:600 12px/1 'Inter',sans-serif; letter-spacing:.04em;
  color:var(--muted); border:1px solid var(--line2); background:var(--surface2); transition:all .2s var(--spring); }
label[data-testid="stRadioOption"] > div > div:first-child:not([data-testid]) { display:none !important; }
label[data-testid="stRadioOption"] > div { width:100%; }
div[role="radiogroup"] label:hover { border-color:color-mix(in srgb, var(--primary) 45%, var(--line2)); transform:translateY(-1px); box-shadow:var(--e2); }
div[role="radiogroup"] label:active { transform:scale(.992); }
div[role="radiogroup"] label:is(:has(input:checked),[data-selected="true"]) { border-color:var(--primary); background:color-mix(in srgb, var(--primary) 6%, var(--surface));
  box-shadow:0 0 0 3px var(--focus), var(--e2); }
div[role="radiogroup"] label:is(:has(input:checked),[data-selected="true"])::before { background:var(--primary); color:var(--on-primary); border-color:var(--primary); transform:translateY(-50%) scale(1.06); }
div[role="radiogroup"] label:has(input:focus-visible) { outline:2px solid var(--primary); outline-offset:2px; }
div[role="radiogroup"] label p { font-size:15px !important; line-height:1.45; }
.oq-kbd { display:inline-flex; gap:4px; align-items:center; color:var(--muted); font-size:12px; margin-top:8px; }
.oq-kbd kbd { font:500 11px/1 'Inter',sans-serif; padding:3px 6px; border-radius:5px; border:1px solid var(--line2); background:var(--surface); color:var(--sub); box-shadow:0 1px 0 var(--line2); }
/* buttons */
.stButton > button, .stFormSubmitButton > button { min-height:44px; border-radius:var(--r-md); }
.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primaryFormSubmit"] { background:var(--primary); color:var(--on-primary); border-color:var(--primary);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.14), var(--e1); }
.stFormSubmitButton > button[kind="primaryFormSubmit"] p { color:var(--on-primary) !important; }
*:focus-visible { outline:2px solid var(--primary) !important; outline-offset:2px; }
/* feedback reveal */
.oq-card.good, .oq-card.kind { animation:oq-reveal .5s var(--spring) both; }
@keyframes oq-reveal { from{opacity:0; transform:translateY(8px) scale(.985)} to{opacity:1; transform:none} }
.oq-verdict { display:inline-flex; align-items:center; gap:6px; font-size:12px; letter-spacing:.12em; text-transform:uppercase; font-weight:600; }
.oq-card.good .oq-verdict { color:var(--good); } .oq-card.kind .oq-verdict { color:var(--kind); }
/* stats */
.oq-stats { display:grid; grid-template-columns:repeat(auto-fit, minmax(96px, 1fr)); gap:8px; margin:16px 0; }
.oq-stat { background:var(--surface); border:1px solid var(--line); border-radius:var(--r-md); padding:12px; }
.oq-stat .l { display:flex; gap:6px; align-items:center; font-size:12px; color:var(--muted); letter-spacing:.02em; }
.oq-stat .v { font-family:'Fraunces',serif; font-size:22px; color:var(--ink); margin-top:4px; line-height:1.15; overflow-wrap:normal; word-break:keep-all; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.oq-stat .v small { font-family:'Inter',sans-serif; font-size:12px; color:var(--muted); margin-left:4px; }
section[data-testid="stSidebar"] .oq-stats { grid-template-columns:1fr 1fr; }
section[data-testid="stSidebar"] .oq-stat:last-child { grid-column:span 2; }
section[data-testid="stSidebar"] .oq-stat .v { font-size:clamp(16px,1.4vw,20px); }
/* summary moment */
.oq-summary { position:relative; padding:32px; margin:8px 0 24px; border-radius:var(--r-xl); background:var(--surface); border:1px solid var(--line);
  box-shadow:var(--e3); overflow:hidden; animation:oq-reveal .7s var(--spring) both; }
.oq-summary::before { content:""; position:absolute; inset:0 0 auto 0; height:4px;
  background:linear-gradient(90deg, var(--primary) 0 40%, var(--navy) 40% 60%, var(--good) 60% 75%, var(--camel) 75% 90%, var(--brass) 90%); }
.oq-summary p { color:var(--sub); margin:0 0 8px; }
.oq-summary .oq-stat { background:var(--surface2); }
.oq-summary .oq-stats .oq-stat { animation:oq-in .5s var(--ease) both; }
.oq-summary .oq-stats .oq-stat:nth-child(2) { animation-delay:.08s; } .oq-summary .oq-stats .oq-stat:nth-child(3) { animation-delay:.16s; }
/* leaderboard motion */
.oq-row { animation:oq-in .45s var(--ease) both; }
.oq-row:nth-child(2){animation-delay:.03s} .oq-row:nth-child(3){animation-delay:.06s} .oq-row:nth-child(4){animation-delay:.09s}
.oq-row:nth-child(5){animation-delay:.12s} .oq-row:nth-child(6){animation-delay:.15s} .oq-row:nth-child(7){animation-delay:.18s}
.oq-row:nth-child(8){animation-delay:.21s}
.oq-row .st { display:inline-flex; gap:4px; align-items:center; justify-content:flex-end; }
.oq-pod .step { transform-origin:bottom; animation:oq-grow .7s var(--spring) both; }
.oq-pod.p1 .step { animation-delay:.12s; } .oq-pod.p3 .step { animation-delay:.2s; }
@keyframes oq-grow { from{transform:scaleY(.2); opacity:0} to{transform:none; opacity:1} }
.oq-move { display:inline-flex; align-items:center; gap:4px; font-size:13px; padding:2px 8px; border-radius:999px; background:var(--surface2); color:var(--sub); }
.oq-move.up { color:var(--good); } .oq-move.down { color:var(--kind); }
/* skeletons */
.oq-skel { border-radius:var(--r-md); background:linear-gradient(90deg, var(--surface2) 0%, var(--surface) 50%, var(--surface2) 100%);
  background-size:200% 100%; animation:oq-shimmer 1.3s linear infinite; }
@keyframes oq-shimmer { to { background-position:-200% 0; } }
/* charts sit on our surface */
[data-testid="stVegaLiteChart"], [data-testid="stArrowVegaLiteChart"] { background:var(--surface); border:1px solid var(--line); border-radius:var(--r-lg); padding:16px; }
/* responsive */
@media (min-width:1800px) { .block-container { max-width:1400px; padding-top:56px; } body { font-size:16px; } }
@media (max-width:1024px) { .block-container { padding:32px 28px 88px; }
  [class*="st-key-grid_"] > div > [data-testid="stHorizontalBlock"], [class*="st-key-grid_"] [data-testid="stHorizontalBlock"] { flex-direction:column; flex-wrap:wrap; }
  [class*="st-key-grid_"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] { width:100% !important; flex:1 1 100% !important; min-width:100% !important; }
  .st-key-quiz_side { position:static; } }
.st-key-quiz_side { position:sticky; top:72px; padding:20px; background:var(--surface); border:1px solid var(--line); border-radius:18px; box-shadow:var(--shadow); }
.st-key-quiz_side .oq-stats { grid-template-columns:1fr 1fr !important; }
@media (min-width:1025px) { .st-key-share_rail { position:sticky; top:72px; } }
.st-key-quiz_side .oq-row .who span { display:none; } .st-key-quiz_side .oq-row > * { flex-shrink:0; } .st-key-quiz_side .oq-row .who { flex:1 1 auto; min-width:0; flex-shrink:1; } .st-key-quiz_side .oq-row { padding:10px 12px; } .st-key-quiz_side .oq-row .who b { white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
@media (max-width:768px) { .oq-summary { padding:24px; } div[role="tablist"] { width:100%; } }
@media (max-width:640px) { .oq-hero { align-items:flex-start; } div[role="radiogroup"] label { padding-left:56px !important; }
  .oq-stats { grid-template-columns:repeat(3, 1fr); } .oq-stat .v { font-size:18px; } }
@media (prefers-reduced-motion: reduce) { *, *::before { animation:none !important; transition:none !important; } }
/* ================= v3: refinement layer ================= */
:root { --s1:4px; --s2:8px; --s3:12px; --s4:16px; --s5:24px; --s6:32px; --s7:48px; }
/* type: 13 / 15 / 17 / 22 / 30 / 44, serif display, sans UI */
.oq-h { display:flex; align-items:baseline; justify-content:space-between; margin:32px 0 12px; }
.oq-h h3 { font-size:20px !important; margin:0 !important; letter-spacing:-.01em; }
.oq-h span { font-size:12px; color:var(--muted); }
.oq-fine { font-size:12.5px; color:var(--muted); line-height:1.5; margin-top:12px; display:flex; gap:6px; align-items:center; justify-content:center; text-align:center; }
.stApp h3 { letter-spacing:-.01em; }
/* sign-in card */
.st-key-login_card { max-width:460px; margin:40px auto 0; padding:0 32px 28px; background:var(--surface); border:1px solid var(--line);
  border-radius:24px; box-shadow:var(--e3); position:relative; overflow:visible; animation:oq-in .6s var(--ease) both; }
.st-key-login_card::before { content:""; position:absolute; inset:0 0 auto 0; height:132px; border-radius:24px 24px 0 0;
  background:radial-gradient(120% 100% at 50% 0%, color-mix(in srgb, var(--primary) 16%, transparent), transparent 70%); pointer-events:none; }
.oq-hero.login { flex-direction:column; text-align:center; gap:0; border:none; padding:0 0 4px; margin:0; align-items:center; }
.oq-hero.login .oq-stage { margin-top:-56px; height:150px; display:flex; align-items:flex-end; justify-content:center; }
.oq-hero.login .oneq-avatar { width:140px !important; height:auto; animation:oq-peek 1.4s cubic-bezier(.3,1.35,.5,1) both; filter:drop-shadow(0 10px 14px rgba(15,25,30,.14)); }
@keyframes oq-peek { 0%{transform:translateY(46px) scale(.9); opacity:0} 40%{transform:translateY(10px) rotate(-5deg); opacity:1} 62%{transform:translateY(6px) rotate(5deg)} 100%{transform:none} }
.oq-bubble { position:relative; margin:10px 0 18px; padding:12px 16px; border-radius:16px; background:var(--surface2); border:1px solid var(--line);
  max-width:360px; transition:transform .3s var(--spring); }
.oq-bubble::before { content:""; position:absolute; top:-7px; left:50%; width:12px; height:12px; background:var(--surface2);
  border-left:1px solid var(--line); border-top:1px solid var(--line); transform:translateX(-50%) rotate(45deg); }
.oq-bubble .oq-line { border:none; padding:0; margin:0; font-size:15px; color:var(--ink); min-height:auto; }
.oq-bubble.pop { animation:oq-pop .35s var(--spring); }
@keyframes oq-pop { 0%{transform:scale(.96)} 60%{transform:scale(1.02)} 100%{transform:none} }
.oq-hero.login h1 { font-size:30px !important; margin:2px 0 18px !important; }
.oq-hero.login .oq-eyebrow { margin:0; }
.st-key-login_card [data-testid="stTextInput"] label p { font-size:13px; font-weight:500; color:var(--sub) !important; }
.st-key-login_card input { height:44px; font-size:15px !important; }
/* pills */
[data-testid="stButtonGroup"] { margin-top:-4px; }
[data-testid="stButtonGroup"] button { border-radius:999px !important; min-height:30px !important; padding:2px 12px !important; font-size:12.5px !important;
  background:transparent !important; border:1px solid var(--line2) !important; color:var(--sub) !important; transition:all .15s var(--ease); }
[data-testid="stButtonGroup"] button:hover { border-color:var(--primary) !important; color:var(--primary) !important; }
[data-testid="stButtonGroup"] button[aria-checked="true"], [data-testid="stButtonGroup"] button[kind$="Active"] { background:var(--primary) !important; color:var(--on-primary) !important; border-color:var(--primary) !important; }
[data-testid="stButtonGroup"] button p { font-size:12.5px !important; color:inherit !important; }
/* inputs */
.stTextInput input:focus, .stTextInput div[data-baseweb="input"]:focus-within { border-color:var(--primary) !important; box-shadow:0 0 0 3px var(--focus) !important; }
.stTextInput div[data-baseweb="input"] { border-radius:10px !important; border:1px solid var(--line2) !important; background:var(--surface) !important; transition:box-shadow .15s, border-color .15s; }
/* locked answers */
.oq-opts { display:flex; flex-direction:column; gap:8px; margin:16px 0 4px; }
.oq-opt { display:flex; align-items:center; gap:12px; padding:12px 14px; border-radius:var(--r-md); border:1px solid var(--line); background:var(--surface);
  color:var(--muted); font-size:15px; animation:oq-in .35s var(--ease) both; }
.oq-opt .k { width:26px; height:26px; border-radius:7px; display:grid; place-items:center; font:600 12px/1 Inter,sans-serif; border:1px solid var(--line2); background:var(--surface2); flex-shrink:0; }
.oq-opt .t { flex:1; } .oq-opt .mk { display:flex; }
.oq-opt.right { color:var(--ink); border-color:color-mix(in srgb, var(--good) 55%, transparent); background:color-mix(in srgb, var(--good) 8%, var(--surface)); animation:oq-in .35s var(--ease) both, oq-settle .6s var(--spring) .2s; }
.oq-opt.right .k { background:var(--good); border-color:var(--good); color:var(--on-primary); } .oq-opt.right .mk { color:var(--good); }
.oq-opt.wrong { color:var(--ink); border-color:color-mix(in srgb, var(--kind) 50%, transparent); background:color-mix(in srgb, var(--kind) 6%, var(--surface)); animation:oq-in .35s var(--ease) both, oq-nudge .45s ease .15s; }
.oq-opt.wrong .k { background:var(--kind); border-color:var(--kind); color:var(--on-primary); } .oq-opt.wrong .mk { color:var(--kind); }
@keyframes oq-settle { 0%{transform:scale(1)} 40%{transform:scale(1.015)} 100%{transform:none} }
@keyframes oq-nudge { 20%{transform:translateX(-4px)} 40%{transform:translateX(4px)} 60%{transform:translateX(-2px)} 80%{transform:translateX(1px)} }
.oq-explain { margin-top:16px; padding:14px 16px; border-radius:var(--r-md); background:var(--surface2); border:1px solid var(--line); }
.oq-explain .oq-eyebrow { margin-bottom:4px; color:var(--brass-ink); }
.oq-explain p { margin:0 !important; color:var(--ink) !important; }
/* progress bar */
div[data-testid="stProgress"] div[role="progressbar"] { height:6px !important; border-radius:999px; background:var(--surface2) !important; }
div[data-testid="stProgress"] div[role="progressbar"] > div { border-radius:999px; }
div[data-testid="stProgress"] div[role="progressbar"] > div > div { border-radius:999px; background:linear-gradient(90deg, var(--primary), color-mix(in srgb, var(--primary) 60%, var(--brass))) !important; transition:width .6s var(--ease); }
.oq-qbar { display:flex; gap:4px; margin:4px 0 0; } .oq-qbar i { flex:1; height:4px; border-radius:2px; background:var(--line2); transition:background .4s var(--ease); }
.oq-qbar i.on { background:var(--primary); } .oq-qbar i.now { background:var(--brass); animation:oq-breath 1.6s ease-in-out infinite; }
@keyframes oq-breath { 50%{opacity:.45} }
/* confetti-lite */
.oq-confetti { position:absolute; inset:0; pointer-events:none; overflow:hidden; }
.oq-confetti i { position:absolute; top:-12px; width:7px; height:11px; border-radius:2px; opacity:0; animation:oq-fall 1.8s cubic-bezier(.2,.6,.4,1) both; }
@keyframes oq-fall { 0%{opacity:0; transform:translate(0,0) rotate(0)} 10%{opacity:1} 100%{opacity:0; transform:translate(var(--dx), 260px) rotate(var(--r))} }
/* tables (admin) */
.oq-table { border:1px solid var(--line); border-radius:var(--r-lg); overflow:hidden; background:var(--surface); }
.oq-table table { width:100%; border-collapse:collapse; font-size:14px; }
.oq-table th { text-align:left; font-size:11.5px; letter-spacing:.08em; text-transform:uppercase; font-weight:500; color:var(--muted); padding:10px 16px; background:var(--surface2); }
.oq-table td { padding:12px 16px; border-top:1px solid var(--line); color:var(--ink); font-variant-numeric:tabular-nums; }
.oq-table tr:hover td { background:color-mix(in srgb, var(--primary) 4%, transparent); }
/* empty states */
.oq-empty { display:flex; flex-direction:column; align-items:center; gap:8px; color:var(--muted); background:color-mix(in srgb, var(--surface) 60%, transparent); }
.oq-empty .oq-ic { color:var(--brass); }
/* sidebar: quiet, no default chrome */
section[data-testid="stSidebar"] { width:320px !important; }
section[data-testid="stSidebar"] h3 { font-size:22px !important; margin-bottom:0 !important; }
[data-testid="stSidebarCollapseButton"] button, [data-testid="stExpandSidebarButton"], [data-testid="stSidebarCollapsedControl"] button {
  border-radius:10px !important; border:1px solid var(--line2) !important; background:var(--surface) !important; color:var(--sub) !important; box-shadow:var(--e1); }
[data-testid="stSidebarCollapseButton"] button:hover, [data-testid="stExpandSidebarButton"]:hover { color:var(--primary) !important; border-color:var(--primary) !important; }
.st-key-poke button { min-height:32px !important; font-size:12.5px !important; border-radius:999px !important; padding:0 12px !important; background:transparent !important; }
/* toggles */
[data-testid="stCheckbox"] label span[role="checkbox"], label[data-baseweb="checkbox"] > div:first-child { transition:background .2s var(--ease); }
/* charts: our card, quiet axes */
[data-testid="stVegaLiteChart"] summary, [data-testid="stVegaLiteChart"] details, .vega-embed .vega-actions, .vega-embed summary { display:none !important; }
/* chat */
.stChatMessage, div[data-testid="stChatMessage"] { gap:10px; }
div[data-testid="stChatMessage"] [data-testid="stChatMessageContent"] { background:var(--surface2); border:1px solid var(--line); border-radius:14px; padding:8px 12px; font-size:14px; }
div[data-testid="stChatMessage"]:has([aria-label*="user" i]) [data-testid="stChatMessageContent"] { background:color-mix(in srgb, var(--primary) 9%, var(--surface)); }
section[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] { border-radius:14px !important; border-color:var(--line) !important; background:var(--bg); }
/* toast */
[data-testid="stToast"] { background:var(--surface) !important; border:1px solid var(--line2); border-radius:12px !important; box-shadow:var(--e3); color:var(--ink); }
.oq-note-i { display:flex; gap:12px; align-items:flex-start; } .oq-note-i .oq-ic { color:var(--brass); margin-top:3px; }
[class*="st-key-role_pill"] [data-testid="stButtonGroup"] > div, [class*="st-key-role_pill"] div[data-baseweb="button-group"] { display:flex !important; flex-direction:row !important; flex-wrap:wrap !important; gap:6px !important; }
[class*="st-key-role_pill"] .stButtonGroup { display:flex !important; flex-wrap:wrap !important; gap:6px !important; } [class*="st-key-role_pill"] .stButtonGroup > div { flex-direction:row !important; flex-wrap:wrap !important; gap:6px !important; width:auto !important; }
[class*="st-key-role_pill"] button { width:auto !important; flex:0 0 auto !important; }

/* ================= v4: mascots, stage, progress, chat, review ================= */
__MASCOTCSS__
/* header stage: the chosen character, large and alive */
.oq-hero.main { gap:28px; padding:20px 0 28px; }
.oq-stage.hero { position:relative; width:168px; height:176px; flex:0 0 168px; display:flex; align-items:flex-end; justify-content:center; }
.oq-stage.hero .halo { position:absolute; left:50%; top:52%; width:150px; height:150px; transform:translate(-50%,-50%); border-radius:50%;
  background:radial-gradient(circle at 50% 45%, var(--brass-soft), transparent 68%); opacity:.9; animation:oq-halo 6s ease-in-out infinite; }
.oq-stage.hero .floor { position:absolute; bottom:6px; left:50%; width:110px; height:10px; transform:translateX(-50%); border-radius:50%;
  background:radial-gradient(closest-side, rgba(0,0,0,.14), transparent); }
.oq-stage svg.oq-m { position:relative; width:168px !important; height:auto; filter:drop-shadow(0 10px 18px rgba(15,25,30,.16)); }
@keyframes oq-halo { 50% { transform:translate(-50%,-50%) scale(1.06); opacity:.7; } }
.oq-hero.main .oq-copy { flex:1; min-width:0; }
.oq-hero.main .oq-line { position:relative; display:inline-block; margin-top:14px; padding:12px 16px; border:1px solid var(--line); border-left:1px solid var(--line);
  background:var(--surface); border-radius:4px 16px 16px 16px; box-shadow:var(--shadow); max-width:560px; color:var(--ink); font-size:15.5px; }
.oq-hero.main .oq-line::before { content:""; position:absolute; left:-7px; top:10px; width:12px; height:12px; background:var(--surface);
  border-left:1px solid var(--line); border-bottom:1px solid var(--line); transform:rotate(45deg); }
.oq-says { display:flex; gap:8px; align-items:center; color:var(--muted); font-size:13.5px; padding-top:6px; }
.oq-says .oq-ic { color:var(--brass); flex-shrink:0; }
.oq-hero.login .oq-stage { margin-top:-92px; height:190px; }
.oq-hero.login svg.oq-m { width:180px !important; height:auto; filter:drop-shadow(0 12px 16px rgba(15,25,30,.16)); }
.st-key-login_card { margin-top:110px !important; }
@media (max-width:640px) {
  .oq-hero.main { gap:14px; padding:12px 0 18px; align-items:flex-start; }
  .oq-stage.hero { width:104px; height:112px; flex-basis:104px; } .oq-stage svg.oq-m { width:104px !important; }
  .oq-stage.hero .halo { width:96px; height:96px; } .oq-hero.main h1 { font-size:26px !important; }
  .oq-hero.login svg.oq-m { width:150px !important; } .oq-hero.login .oq-stage { height:160px; margin-top:-80px; }
}
/* picker */
.oq-pick-head { text-align:center; max-width:620px; margin:12px auto 28px; }
.oq-pick-head h1 { font-size:44px !important; margin:6px 0 10px !important; }
.oq-pick-head p { color:var(--sub); font-size:16px; margin:0; }
.oq-mcard { background:var(--surface); border:1px solid var(--line); border-radius:20px; padding:12px 12px 14px; text-align:center;
  box-shadow:var(--shadow); transition:transform .3s var(--spring), box-shadow .3s, border-color .3s; animation:oq-in .5s var(--ease) both; }
.oq-mcard:hover { transform:translateY(-4px); box-shadow:0 18px 36px -20px rgba(15,40,45,.45); }
.oq-mcard.on { border-color:var(--brass); box-shadow:0 0 0 3px var(--brass-soft), var(--shadow); }
.oq-mcard .st { border-radius:14px; background:radial-gradient(120% 90% at 50% 20%, var(--surface), var(--surface2)); aspect-ratio:1/1.02;
  display:grid; place-items:center; overflow:hidden; }
.oq-mcard .st svg { width:94%; height:auto; }
.oq-mcard h4 { font-family:'Fraunces',Georgia,serif; font-weight:500; font-size:19px; margin:12px 0 4px; color:var(--ink); }
.oq-mcard p { font-size:12.5px; line-height:1.45; color:var(--sub); margin:0; min-height:54px; }
.oq-mcard q { display:block; font-family:'Fraunces',Georgia,serif; font-style:italic; font-size:13px; color:var(--ink); margin:10px 0 0;
  padding-top:10px; border-top:1px dashed var(--line); min-height:56px; }
.oq-mcard.compact p, .oq-mcard.compact q { display:none; } .oq-mcard.compact h4 { font-size:15px; margin:8px 0 0; }
.oq-mcard .sel { display:inline-flex; gap:4px; align-items:center; font-size:11px; letter-spacing:.12em; text-transform:uppercase; color:var(--brass); margin-top:6px; }
[class*="_card"] [data-testid="stButton"] button { border-radius:999px !important; }
.oq-label { font-size:14px; color:var(--ink); margin:4px 0 8px; }
@media (max-width:640px) { .oq-pick-head h1 { font-size:32px !important; } .oq-mcard p { min-height:0; } .oq-mcard q { min-height:0; } }
/* heatmap */
.oq-heat { background:var(--surface); border:1px solid var(--line); border-radius:16px; padding:18px 20px 14px; box-shadow:var(--shadow); overflow:hidden; }
.oq-heat .grid { display:grid; grid-template-rows:repeat(7, 1fr); grid-auto-flow:column; grid-auto-columns:minmax(0, 1fr); gap:4px; }
.oq-heat .grid i { display:block; aspect-ratio:1; border-radius:3px; background:var(--surface2); max-width:22px; animation:oq-fade .5s ease both; }
.oq-heat .grid i.l1 { background:color-mix(in srgb, var(--primary) 28%, var(--surface2)); }
.oq-heat .grid i.l2 { background:color-mix(in srgb, var(--primary) 55%, var(--surface2)); }
.oq-heat .grid i.l3 { background:var(--primary); } .oq-heat .grid i.today { outline:2px solid var(--brass); outline-offset:1px; }
.oq-heat .grid i.out { visibility:hidden; }
.oq-heat .wrap { display:grid; grid-template-columns:28px 1fr; gap:8px; }
.oq-heat .days { display:grid; grid-template-rows:repeat(7, 1fr); gap:4px; font-size:10.5px; color:var(--muted); align-items:center; }
.oq-heat .months { display:grid; grid-auto-flow:column; grid-auto-columns:minmax(0, 1fr); gap:4px; margin:0 0 6px 36px; font-size:10.5px; color:var(--muted); }
.oq-heat .foot { display:flex; justify-content:space-between; align-items:center; margin-top:12px; font-size:12px; color:var(--muted); }
.oq-heat .key { display:flex; gap:4px; align-items:center; } .oq-heat .key i { width:11px; height:11px; border-radius:3px; display:inline-block; background:var(--surface2); }
.oq-heat .key i.l1 { background:color-mix(in srgb, var(--primary) 28%, var(--surface2)); } .oq-heat .key i.l2 { background:color-mix(in srgb, var(--primary) 55%, var(--surface2)); }
.oq-heat .key i.l3 { background:var(--primary); }
/* chart cards */
[data-testid="stVegaLiteChart"], .oq-radar { background:var(--surface); border:1px solid var(--line); border-radius:16px; padding:14px; box-shadow:var(--shadow); }
.oq-radar svg { max-width:440px; }
.oq-legend { display:flex; flex-wrap:wrap; gap:6px 14px; margin:10px 2px 0; font-size:12px; color:var(--sub); }
.oq-legend span { display:inline-flex; align-items:center; gap:6px; } .oq-legend i { width:9px; height:9px; border-radius:50%; display:inline-block; }
.oq-badges { display:flex; flex-wrap:wrap; gap:8px; }
.oq-badge { display:inline-flex; gap:8px; align-items:center; padding:8px 12px 8px 8px; border:1px solid var(--line); border-radius:999px; background:var(--surface);
  font-size:13px; color:var(--ink); box-shadow:var(--shadow); }
.oq-badge b { width:24px; height:24px; border-radius:50%; display:grid; place-items:center; background:var(--brass-soft); color:var(--brass-ink); }
/* chat */
.oq-chat-head { display:flex; align-items:center; gap:10px; margin:22px 0 10px; padding-top:16px; border-top:1px solid var(--line); font-family:inherit; }
.oq-chat-head svg.oq-m { width:40px !important; height:auto; flex-shrink:0; }
.oq-chat-head b { display:block; font-family:'Fraunces',serif; font-weight:500; font-size:17px; color:var(--ink); }
.oq-chat-head span { display:block; font-size:12px; color:var(--muted); }
.oq-chat-head .live { margin-left:auto; width:8px; height:8px; border-radius:50%; background:var(--good); box-shadow:0 0 0 3px color-mix(in srgb, var(--good) 22%, transparent); }
.oq-thread { display:flex; flex-direction:column; gap:10px; padding:2px; }
.oq-msg { max-width:88%; padding:10px 13px; font-size:13.5px; line-height:1.5; border-radius:16px; animation:oq-in .3s var(--ease) both; word-wrap:break-word; }
.oq-msg.a { align-self:flex-start; background:var(--surface); border:1px solid var(--line); color:var(--ink); border-bottom-left-radius:4px; }
.oq-msg.u { align-self:flex-end; background:var(--primary); color:var(--on-primary); border-bottom-right-radius:4px; }
.oq-msg .who { display:block; font-size:10.5px; letter-spacing:.1em; text-transform:uppercase; opacity:.6; margin-bottom:3px; }
.st-key-chat_box { background:var(--surface2); border:1px solid var(--line); border-radius:16px; padding:10px; }
[data-testid="stSidebar"] [data-testid="stForm"] { display:flex; gap:8px; }
[data-testid="stSidebar"] [data-testid="stForm"] input { border-radius:999px !important; padding-left:14px !important; }
[data-testid="stSidebar"] [data-testid="stFormSubmitButton"] button { border-radius:999px !important; background:var(--primary) !important; color:var(--on-primary) !important; border:none !important; }
/* review */
.oq-revhead { display:flex; gap:10px; align-items:center; color:var(--muted); font-size:13px; margin:-4px 0 6px; }
.oq-revhead .dot { width:3px; height:3px; border-radius:50%; background:var(--muted); }
details.oq-rev { background:var(--surface); border:1px solid var(--line); border-radius:14px; margin:10px 0; box-shadow:var(--shadow); overflow:hidden; }
details.oq-rev summary { list-style:none; cursor:pointer; display:grid; grid-template-columns:30px 1fr auto; gap:12px; align-items:center; padding:16px 18px; }
details.oq-rev summary::-webkit-details-marker { display:none; }
details.oq-rev .n { width:30px; height:30px; border-radius:50%; display:grid; place-items:center; font-size:12px; font-weight:600; }
details.oq-rev.good .n { background:color-mix(in srgb, var(--good) 16%, transparent); color:var(--good); }
details.oq-rev.kind .n { background:color-mix(in srgb, var(--kind) 16%, transparent); color:var(--kind); }
details.oq-rev .q { color:var(--ink); font-size:15px; line-height:1.45; }
details.oq-rev .chev { color:var(--muted); transition:transform .25s var(--ease); }
details.oq-rev[open] .chev { transform:rotate(180deg); }
details.oq-rev .body { padding:0 18px 18px 60px; }
details.oq-rev .said { font-family:'Fraunces',serif; font-style:italic; color:var(--sub); font-size:14px; margin:12px 0 0; }
details.oq-rev .yours { font-size:12px; letter-spacing:.08em; text-transform:uppercase; color:var(--muted); margin:2px 0 6px; }
@media (max-width:640px) { details.oq-rev .body { padding:0 14px 14px; } }
.oq-summary .fig { position:absolute; right:18px; top:10px; width:150px; } .oq-summary .fig svg { width:150px !important; height:auto; }
@media (max-width:640px) { .oq-summary .fig { position:static; margin:-6px auto 0; } }
.oq-qhead { display:flex; align-items:center; justify-content:space-between; }
@media (max-width:640px) { .st-key-login_card { margin-top:56px; padding:0 20px 20px; border-radius:20px; } .oq-hero.login .oneq-avatar { width:120px !important; } .oq-hero.login h1 { font-size:26px !important; } }
</style>
"""


def css(theme: str = DEFAULT_THEME) -> str:
    t = THEMES.get(theme, THEMES[DEFAULT_THEME])
    vars_ = ":root {--spring:cubic-bezier(.34,1.56,.64,1);" + "".join(f"--{k.replace('_', '-')}:{v};" for k, v in t.items() if isinstance(v, str)) + "}"
    if t["base"] == "dark":
        vars_ += " :root { color-scheme: dark; }"
    vars_ += " :root{--spring:cubic-bezier(.34,1.56,.64,1);--ease:cubic-bezier(.2,.7,.2,1);}"
    from .mascots import CSS as MCSS
    return _CSS.replace("__VARS__", vars_).replace("__MASCOTCSS__", MCSS)


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
  P.document.addEventListener('mousedown', (e) => { if ((e.target.innerText||'').match(/Lock it in|Submit today/)) push(); }, true);
})();
</script>
"""



LIVE_JS = """
<script>
(function(){
  const W = window, D = document;
  if (W.__oneqLive) return; W.__oneqLive = true;
  const reduce = W.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let px = W.innerWidth/2, py = W.innerHeight/3, lastMove = Date.now();
  const track = (x, y) => { px = x; py = y; lastMove = Date.now(); };
  D.addEventListener('pointermove', e => track(e.clientX, e.clientY), {passive:true});
  D.addEventListener('touchstart', e => { const t = e.touches[0]; if (t) track(t.clientX, t.clientY); }, {passive:true});

  // Eyes and head follow the pointer with a soft lag. Each frame eases 12% toward the target.
  const state = new WeakMap();
  function frame(){
    D.querySelectorAll('svg.oneq-avatar').forEach(svg => {
      const st = state.get(svg) || {fx:0, fy:0, r:0}; state.set(svg, st);
      const b = svg.getBoundingClientRect(); if (!b.width) return;
      const cx = b.left + b.width/2, cy = b.top + b.height/2;
      let dx = (px - cx) / Math.max(240, b.width*3), dy = (py - cy) / Math.max(240, b.height*3);
      const idle = Date.now() - lastMove > 6000 || svg.dataset.react === 'sleep';
      if (idle) { dx = Math.sin(Date.now()/2600)*.25; dy = .15; }
      if (svg.dataset.react === 'think') { dx = .55; dy = -.6; }
      dx = Math.max(-1, Math.min(1, dx)); dy = Math.max(-1, Math.min(1, dy));
      st.fx += (dx*4.5 - st.fx)*.12; st.fy += (dy*3.5 - st.fy)*.12; st.r += (dx*4 - st.r)*.08;
      const face = svg.querySelector('.m-face'), rig = svg.querySelector('.m-rig');
      if (face) face.style.transform = `translate(${st.fx.toFixed(2)}px, ${st.fy.toFixed(2)}px)`;
      if (rig && !svg.matches(':hover') && !['empathy','think','shake','squint'].includes(svg.dataset.react))
        rig.style.transform = `rotate(${st.r.toFixed(2)}deg)`;
      else if (rig) rig.style.transform = '';
    });
    if (!reduce) W.requestAnimationFrame(frame);
  }
  // Natural blinking: random gaps of 2 to 6 s, with an occasional double blink.
  function blink(){
    D.querySelectorAll('svg.oneq-avatar').forEach(svg => {
      if (svg.dataset.react === 'sleep') return;
      svg.classList.add('blinking'); setTimeout(() => svg.classList.remove('blinking'), 120);
      if (Math.random() < .2) setTimeout(() => { svg.classList.add('blinking'); setTimeout(() => svg.classList.remove('blinking'), 110); }, 260);
    });
    setTimeout(blink, 2000 + Math.random()*4000);
  }
  // Clicking 1Q squashes it; three quick clicks send a real tickle to the server.
  let clicks = [];
  D.addEventListener('click', e => {
    const svg = e.target.closest && e.target.closest('svg.oneq-avatar'); if (!svg) return;
    svg.classList.remove('poked'); void svg.getBBox(); svg.classList.add('poked');
    setTimeout(() => svg.classList.remove('poked'), 520);
    const now = Date.now(); clicks = clicks.filter(t => now - t < 1200); clicks.push(now);
    const btn = [...D.querySelectorAll('button')].find(b => (b.innerText||'').trim() === 'Poke 1Q');
    if (btn && clicks.length >= 2) { clicks = []; btn.click(); }
    // Login screen (no Poke button): 1Q answers pokes with local banter, no server round trip.
    const hero = svg.closest('.oq-hero'); const pokes = hero && hero.dataset.pokes;
    if (!btn && pokes) {
      const list = JSON.parse(pokes); const line = hero.querySelector('.oq-line');
      hero._pi = ((hero._pi ?? -1) + 1) % list.length;
      if (line) { line.textContent = list[hero._pi]; }
      svg.dataset.react = clicks.length >= 3 ? 'shake' : 'joy';
      svg.classList.remove('react'); void svg.getBBox(); svg.classList.add('react');
      svg.classList.add('talking'); setTimeout(() => { svg.classList.remove('react'); svg.classList.remove('talking'); }, 1200);
    }
  });
  // While someone types their email on the login screen, 1Q bobs along and peeks at the field.
  D.addEventListener('input', e => {
    if (!e.target.matches || !e.target.matches('input[type="text"], input:not([type])')) return;
    const svg = D.querySelector('.oq-hero[data-pokes] svg.oneq-avatar'); if (!svg || reduce) return;
    svg.classList.add('talking'); clearTimeout(svg._tt); svg._tt = setTimeout(() => svg.classList.remove('talking'), 380);
  }, true);
  // Replay a reaction once per new server reaction id; type out the speech line while 1Q "talks".
  const seen = {};
  function wake(root){
    root.querySelectorAll('svg.oneq-avatar').forEach(svg => {
      const rid = svg.dataset.rid + ':' + svg.dataset.react;
      if (seen[rid]) return; seen[rid] = true;
      if (!reduce) { svg.classList.add('react'); setTimeout(() => svg.classList.remove('react'), 1800); }
    });
    root.querySelectorAll('.oq-line:not([data-typed])').forEach(el => {
      el.dataset.typed = '1'; const full = el.textContent; el.dataset.full = full; const key = 'oq-said:' + full;
      if (reduce || W.sessionStorage.getItem(key)) return;
      W.sessionStorage.setItem(key, '1');
      const svg = el.closest('.oq-hero') && el.closest('.oq-hero').querySelector('svg.oneq-avatar');
      el.textContent = ''; const caret = D.createElement('span'); caret.className = 'caret';
      el.appendChild(caret); svg && svg.classList.add('talking');
      let i = 0; const step = () => {
        i += full[i] === ' ' ? 2 : 1;
        el.firstChild && el.firstChild.nodeType === 3 ? el.firstChild.textContent = full.slice(0, i) : el.insertBefore(D.createTextNode(full.slice(0, i)), caret);
        if (i < full.length) setTimeout(step, /[.,!?]/.test(full[i-1]) ? 120 : 22);
        else { svg && svg.classList.remove('talking'); setTimeout(() => caret.remove(), 900); }
      }; step();
    });
    // Count-up for scores and stats.
    root.querySelectorAll('[data-count]:not([data-counted])').forEach(el => {
      el.dataset.counted = '1'; const to = +el.dataset.count; if (reduce || !to) return;
      const t0 = performance.now(), dur = 900;
      const tick = t => { const k = Math.min(1, (t - t0)/dur), e = 1 - Math.pow(1 - k, 3);
        el.textContent = Math.round(to*e).toLocaleString(); if (k < 1) requestAnimationFrame(tick); };
      requestAnimationFrame(tick);
    });
  }
  new MutationObserver(() => wake(D)).observe(D.body, {childList:true, subtree:true});
  // Keyboard: 1-4 or A-D picks an answer, Enter locks it in or moves on.
  D.addEventListener('keydown', e => {
    const tag = (e.target.tagName || '').toLowerCase();
    if (tag === 'input' || tag === 'textarea' || e.metaKey || e.ctrlKey || e.altKey) return;
    const main = D.querySelector('[data-testid="stMain"]'); if (!main) return;
    const k = e.key.toLowerCase(), idx = '1234'.indexOf(k) >= 0 ? '1234'.indexOf(k) : 'abcd'.indexOf(k);
    const opts = main.querySelectorAll('div[role="radiogroup"] label');
    if (idx >= 0 && opts[idx]) { opts[idx].click(); e.preventDefault(); return; }
    if (e.key === 'Enter') {
      const b = [...main.querySelectorAll('button')].find(b => /^(Lock it in|Next question|See my review|Next)$/.test((b.innerText||'').trim()) && !b.disabled);
      if (b) { b.click(); e.preventDefault(); }
    }
  });
  // Login / first run: 1Q reacts live to the title being typed. Rules come from avatar.role_react_js_rules().
  D.addEventListener('input', e => {
    const inp = e.target; if (!inp.closest || !inp.closest('.st-key-login_role')) return;
    const hero = D.querySelector('.oq-hero.login'); if (!hero) return;
    const line = hero.querySelector('.oq-bubble p'), svg = hero.querySelector('svg.oneq-avatar');
    const rules = JSON.parse(hero.dataset.rules || '[]'), v = ' ' + inp.value.toLowerCase().trim() + ' ';
    clearTimeout(hero._rt);
    if (svg) { svg.dataset.react = 'think'; }
    if (line && v.trim().length < 3) { line.textContent = hero.dataset.typing; return; }
    hero._rt = setTimeout(() => {
      const hit = rules.find(r => r[0].some(k => v.includes(k))) || [[], hero.dataset.fallback, 'happy'];
      if (line) { line.textContent = hit[1]; line.parentElement.classList.remove('pop'); void line.offsetWidth; line.parentElement.classList.add('pop'); }
      if (svg) { svg.dataset.react = hit[2] === 'cheering' ? 'joy' : 'think'; svg.classList.remove('react'); void svg.getBBox(); svg.classList.add('react');
        svg.classList.add('talking'); setTimeout(() => svg.classList.remove('talking'), 900); }
    }, 260);
  }, true);
  // ---- the five selectable mascots (svg.oq-m): pupils follow the pointer, clicks tickle, typing reacts.
  const setX = (m, x) => { m.classList.forEach(c => c.startsWith('x-') && m.classList.remove(c)); m.classList.add('x-' + x); };
  function eyes(){
    D.querySelectorAll('svg.oq-m').forEach(m => {
      if (m.classList.contains('x-thinking') || m.classList.contains('x-sleepy')) return;
      const r = m.getBoundingClientRect(); if (!r.width) return;
      const dx = px - (r.left + r.width/2), dy = py - (r.top + r.height*.42), d = Math.hypot(dx, dy) || 1, k = Math.min(1, d/300) * 3.4;
      m.querySelectorAll('.pupil').forEach(p => p.style.transform = `translate(${(dx/d*k).toFixed(2)}px,${(dy/d*k).toFixed(2)}px)`);
    });
    if (!reduce) W.requestAnimationFrame(eyes);
  }
  D.addEventListener('click', e => {
    const m = e.target.closest && e.target.closest('svg.oq-m'); if (!m) return;
    const back = m.dataset.expr || 'happy'; setX(m, 'ticklish'); clearTimeout(m._tk);
    m._tk = setTimeout(() => setX(m, back), 1500);
    const now = Date.now(); clicks = clicks.filter(t => now - t < 1200); clicks.push(now);
    const btn = [...D.querySelectorAll('button')].find(b => (b.innerText||'').trim() === 'Poke 1Q');
    if (btn && clicks.length >= 2) { clicks = []; btn.click(); return; }
    const hero = m.closest('.oq-hero'); const pokes = hero && hero.dataset.pokes;
    if (!btn && pokes) { const list = JSON.parse(pokes), line = hero.querySelector('.oq-line');
      hero._pi = ((hero._pi ?? -1) + 1) % list.length; if (line) line.textContent = list[hero._pi]; }
  });
  D.addEventListener('input', e => {
    const inp = e.target; if (!inp.closest || !inp.closest('.st-key-login_role')) return;
    const hero = D.querySelector('.oq-hero.login'), m = hero && hero.querySelector('svg.oq-m'); if (!m) return;
    const rules = JSON.parse(hero.dataset.rules || '[]'), v = ' ' + inp.value.toLowerCase().trim() + ' ';
    setX(m, 'thinking'); clearTimeout(m._rt);
    m._rt = setTimeout(() => { const hit = rules.find(r => r[0].some(k => v.includes(k)));
      setX(m, v.trim().length < 3 ? 'thinking' : (hit && hit[2] === 'cheering') ? 'cheering' : 'happy'); }, 300);
  }, true);
  if (!reduce) W.requestAnimationFrame(eyes);
  wake(D); if (!reduce) { W.requestAnimationFrame(frame); setTimeout(blink, 1800); }
})();
</script>
"""



# One line-icon set: 24px grid, 1.6 stroke, round caps. No emoji anywhere in the UI.
ICONS = {
    "flame": '<path d="M12 3c1 3.5 5 5.5 5 10a5 5 0 0 1-10 0c0-2.2 1.2-3.6 2.4-4.6.2 1.6 1 2.6 2.1 3.1C11 9 11 6 12 3z"/>',
    "shield": '<path d="M12 3l7 3v5c0 4.5-3 8.2-7 10-4-1.8-7-5.5-7-10V6l7-3z"/><path d="M9 12l2 2 4-4"/>',
    "level": '<path d="M4 20V14M10 20V9M16 20V4M22 20H2"/>',
    "trophy": '<path d="M8 4h8v5a4 4 0 0 1-8 0V4z"/><path d="M8 6H5a3 3 0 0 0 3 4M16 6h3a3 3 0 0 1-3 4M12 13v4M8 21h8M9 17h6"/>',
    "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M6 18l2.5-2.5M15.5 8.5L18 6"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "x": '<path d="M6 6l12 12M18 6L6 18"/>',
    "up": '<path d="M12 19V5M6 11l6-6 6 6"/>',
    "down": '<path d="M12 5v14M6 13l6 6 6-6"/>',
    "dash": '<path d="M6 12h12"/>',
    "points": '<circle cx="12" cy="12" r="8"/><path d="M12 8v8M9 10.5h4.5a1.5 1.5 0 0 1 0 3H9"/>',
    "chat": '<path d="M4 5h16v11H9l-5 4V5z"/>',
    "key": '<rect x="3" y="7" width="18" height="11" rx="2"/><path d="M7 11h1M11 11h1M15 11h2M7 14.5h10"/>',
    "calendar": '<rect x="4" y="5" width="16" height="15" rx="2"/><path d="M4 10h16M9 3v4M15 3v4"/>',
}


def icon(name: str, size: int = 16) -> str:
    return (f'<svg class="oq-ic" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS.get(name, "")}</svg>')


def num(v) -> str:
    """Tabular number that counts up on first paint."""
    if isinstance(v, (int, float)):
        return f'<span class="oq-num" data-count="{int(v)}">{int(v):,}</span>'
    return f'<span>{esc(v)}</span>'


def stats(items) -> str:
    cells = "".join(f'<div class="oq-stat"><div class="l">{icon(ic, 14)}{esc(lbl)}</div>'
                    f'<div class="v">{num(v)}<small>{esc(unit)}</small></div></div>' for ic, lbl, v, unit in items)
    return f'<div class="oq-stats">{cells}</div>'


def summary(points: int, streak: int, title: str, extra: str = "", figure: str = "") -> str:
    """End-of-day moment. Private to the user, and still no right or wrong counts."""
    return (f'<div class="oq-summary">{f"<div class=fig>{figure}</div>" if figure else ""}<div class="oq-eyebrow">{icon("spark", 12)} Set complete</div>'
            f'<h2 class="oq-display">That is today done.</h2><p>A fresh twelve unlocks at midnight, your time.</p>'
            + stats([("points", "Points today", points, "pts"), ("flame", "Streak", streak, "days"),
                     ("trophy", "Title", title, "")]) + extra + '</div>')


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


def hero(svg: str, title: str, line: str, sub: str = "", pokes: list[str] | None = None) -> str:
    data = f" data-pokes='{esc(json.dumps(pokes))}'" if pokes else ""
    return (f'<div class="oq-hero main"{data}><div class="oq-stage hero"><span class="halo"></span><span class="floor"></span>{svg}</div>'
            f'<div class="oq-copy">{f"<div class=oq-eyebrow>{esc(sub)}</div>" if sub else ""}<h1>{esc(title)}</h1>'
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
                  f'<div class="sc">{num(r["score"])} pts · {r["streak"]}d streak</div><div class="step">{n}</div></div>')
    return f'<div class="oq-podium" style="{period_vars(period, theme)}">{cells}</div>'


def lb_rows(rows: list[dict], me_id: int, period: str = "overall", theme: str = DEFAULT_THEME) -> str:
    if not rows:
        return ""
    body = "".join(
        f'<div class="oq-row {"me" if r["user_id"] == me_id else ""}"><div class="rk">{r["rank"]}</div>{monogram(r["name"])}'
        f'<div class="who"><b>{esc(r["name"])}</b><span>{esc(r["title"])} · {esc(r["level"])}</span></div>'
        f'<div class="st">{icon("flame", 12)}{r["streak"]}</div><div class="sc">{num(r["score"])}</div></div>'
        for r in rows)
    return f'<div class="oq-list" style="{period_vars(period, theme)}">{body}</div>'


def lb_row(r: dict, me: bool) -> str:
    return lb_rows([r], r["user_id"] if me else -1)


def share_card(name: str, streak: int, rank: int, of: int, title: str, day) -> str:
    return (f"1Q · {day:%b %d}\n{name}, {title}\n"
            f"{streak}-day streak · Rank {rank} of {of}\n"
            f"Today's set: complete\nCan you match my streak? Take today's 1Q.")


def share_html(name: str, streak: int, rank: int, of: int, title: str, day, figure: str = "", buddy: str = "") -> str:
    """Share card: midnight navy with a teal-to-camel rule and brass type. Streak and rank only."""
    fig = (f'<div style="position:absolute;right:16px;bottom:8px;width:96px">{figure}</div>' if figure else "")
    return (f'<div style="position:relative;background:#1b2a4a;color:#f5f0e6;border-radius:16px;padding:24px 128px 24px 24px;margin:16px 0;'
            f'box-shadow:0 8px 24px rgba(27,42,74,.18);overflow:hidden">{fig}'
            f'<div style="font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:#c9a866">1Q · {day:%b %d}'
            f'{" · with " + esc(buddy) if buddy else ""}</div>'
            f'<div style="font-family:Fraunces,Georgia,serif;font-size:28px;margin-top:8px">{esc(name)}</div>'
            f'<div style="color:#b8cad6;font-size:14px">{esc(title)}</div>'
            f'<div style="display:flex;gap:4px;margin:16px 0"><i style="flex:2;height:3px;background:#6fb7b3"></i>'
            f'<i style="flex:1;height:3px;background:#7fc0a3"></i><i style="flex:1;height:3px;background:#b8935f"></i>'
            f'<i style="flex:1;height:3px;background:#a8874a"></i></div>'
            f'<div style="font-size:16px">{streak}-day streak · Rank {rank} of {of}</div></div>')


def radar(topics: list[dict], theme: str = DEFAULT_THEME, size: int = 320) -> str:
    """Animated spider chart of topic mastery (0-5). Inline SVG, themed, draws in on load."""
    import math
    if len(topics) < 3:
        return ""
    t = THEMES[theme]
    n, c, R = len(topics), size / 2, size / 2 - 78
    vmax = max(2.5, min(5.0, max(d["level"] for d in topics) * 1.2))  # zoom so early learners still see a shape
    pt = lambda i, v: (c + R * v / vmax * math.sin(2 * math.pi * i / n), c - R * v / vmax * math.cos(2 * math.pi * i / n))
    rings = "".join(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in (pt(i, lv) for i in range(n)))}" '
                    f'fill="none" stroke="{t["line"]}" stroke-width="1"/>' for lv in [vmax * f for f in (.2, .4, .6, .8, 1)])
    spokes = "".join(f'<line x1="{c}" y1="{c}" x2="{pt(i, 5)[0]:.1f}" y2="{pt(i, 5)[1]:.1f}" stroke="{t["line"]}"/>' for i in range(n))
    shape = " ".join(f"{x:.1f},{y:.1f}" for x, y in (pt(i, d["level"]) for i, d in enumerate(topics)))
    teal = tone("teal", theme)
    dots, labels = "", ""
    for i, d in enumerate(topics):
        x, y = pt(i, d["level"])
        col = tone(TOPIC_TONES.get(d.get("key", ""), "teal"), theme)
        dots += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{col}" class="oq-rdot" style="animation-delay:{.5 + i * .05:.2f}s"><title>{esc(d["topic"])}: {d["level"]}</title></circle>'
        lx, ly = pt(i, vmax * 1.14)
        anchor = "middle" if abs(lx - c) < 8 else ("start" if lx > c else "end")
        words, l1, l2 = d["topic"].split(), "", ""
        for wd in words:
            if len(l1) + len(wd) < 15 and not l2:
                l1 = (l1 + " " + wd).strip()
            else:
                l2 = (l2 + " " + wd).strip()
        l2 = l2 if len(l2) <= 18 else l2[:17] + "…"
        y0 = ly + (5 if not l2 else -3)
        labels += (f'<text x="{lx:.1f}" y="{y0:.1f}" text-anchor="{anchor}" font-size="15" font-weight="600" fill="{t["ink"]}">{esc(l1)}'
                   + (f'<tspan x="{lx:.1f}" dy="17">{esc(l2)}</tspan>' if l2 else "") + "</text>")
    return (f'<div class="oq-chart oq-radar"><svg viewBox="-70 -14 {size + 140} {size + 28}" width="100%" role="img" '
            f'aria-label="Topic mastery radar">{rings}{spokes}'
            f'<polygon class="oq-rshape" points="{shape}" fill="{teal}" fill-opacity=".18" stroke="{teal}" stroke-width="2" '
            f'stroke-linejoin="round"/>{dots}{labels}</svg></div>')


# ---------------------------------------------------------------- v3 components
def login_hero(svg: str, title: str, line: str, sub: str = "", pokes=None, rules=None, typing: str = "") -> str:
    """Centered sign-in hero: the mascot peeks up from behind the card and talks in a speech bubble."""
    fallback = "Love it. I'll start gentle and grow with you."
    data = (f" data-pokes='{esc(json.dumps(pokes or []))}' data-rules='{esc(json.dumps(rules or []))}'"
            f" data-typing='{esc(typing)}' data-fallback='{esc(fallback)}'")
    return (f'<div class="oq-hero login"{data}><div class="oq-stage">{svg}</div>'
            f'<div class="oq-bubble"><p class="oq-line">{esc(line)}</p></div>'
            f'<div class="oq-eyebrow">{esc(sub)}</div><h1>{esc(title)}</h1></div>')


def locked_options(options: list[str], answer: int, pick: int) -> str:
    """The four options after lock-in: the right one settles in green, a wrong pick in burgundy."""
    rows = ""
    for i, o in enumerate(options):
        cls = "right" if i == answer else ("wrong" if i == pick else "")
        mark = icon("check", 14) if i == answer else (icon("x", 14) if i == pick else "")
        rows += (f'<div class="oq-opt {cls}" style="animation-delay:{i * .04:.2f}s"><span class="k">{"ABCD"[i]}</span>'
                 f'<span class="t">{esc(o)}</span><span class="mk">{mark}</span></div>')
    return f'<div class="oq-opts" role="list">{rows}</div>'


def confetti(n: int = 26) -> str:
    """Confetti-lite: CSS-only, one short fall in wardrobe tones, skipped under reduced motion."""
    cols = ["#0f5257", "#a8874a", "#6e2433", "#1b2a4a", "#b8935f", "#234232"]
    bits = "".join(f'<i style="left:{(i * 37) % 100}%;background:{cols[i % len(cols)]};animation-delay:{(i % 7) * .07:.2f}s;'
                   f'--dx:{((i * 53) % 60) - 30}px;--r:{(i * 97) % 360}deg"></i>' for i in range(n))
    return f'<div class="oq-confetti" aria-hidden="true">{bits}</div>'


def skeleton(lines: int = 3) -> str:
    return ('<div class="oq-card" aria-busy="true"><div class="oq-skel" style="height:12px;width:30%"></div>'
            '<div class="oq-skel" style="height:22px;width:85%;margin-top:14px"></div>'
            + "".join('<div class="oq-skel" style="height:52px;margin-top:10px"></div>' for _ in range(lines + 1))
            + '<div class="oq-fine" style="margin-top:12px">1Q is writing today\'s questions…</div></div>')


def table(rows: list[dict], cols: list[tuple[str, str]], empty: str = "Nothing here yet.") -> str:
    if not rows:
        return f'<div class="oq-empty">{icon("spark", 18)}<div>{esc(empty)}</div></div>'
    head = "".join(f"<th>{esc(lbl)}</th>" for _, lbl in cols)
    body = "".join("<tr>" + "".join(f"<td>{esc(r.get(k, ''))}</td>" for k, _ in cols) + "</tr>" for r in rows)
    return f'<div class="oq-table"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def heading(text: str, note: str = "") -> str:
    return f'<div class="oq-h"><h3>{esc(text)}</h3>{f"<span>{esc(note)}</span>" if note else ""}</div>'


def empty(text: str, ic: str = "spark") -> str:
    return f'<div class="oq-empty">{icon(ic, 18)}<div>{esc(text)}</div></div>'


def note(text: str, ic: str = "spark") -> str:
    return f'<div class="oq-note oq-note-i">{icon(ic, 16)}<div>{esc(text)}</div></div>'


# ---------------------------------------------------------------- v4 components
def picker_head(eyebrow: str, title: str, sub: str) -> str:
    return f'<div class="oq-pick-head"><div class="oq-eyebrow">{esc(eyebrow)}</div><h1>{esc(title)}</h1><p>{esc(sub)}</p></div>'


def mascot_card(svg: str, name: str, tagline: str, line: str, on: bool = False, compact: bool = False) -> str:
    sel = f'<div class="sel">{icon("check", 12)}Your 1Q</div>' if on else ""
    return (f'<div class="oq-mcard{" on" if on else ""}{" compact" if compact else ""}"><div class="st">{svg}</div>'
            f'<h4>{esc(name)}</h4>{sel}<p>{esc(tagline)}</p>{f"<q>{esc(line)}</q>" if line else ""}</div>')


def review_card(n: int, q: dict, ok: bool, pick: int | None, line: str) -> str:
    """Collapsible review row: number, question, then your locked answer against the right one."""
    right = q["options"][q["answer_index"]]
    yours = (f'<div class="yours">You picked {"ABCD"[pick]}{" · correct" if ok else ""}</div>' if pick is not None
             else '<div class="yours">Your pick was not recorded</div>')
    sr = (f'<span class="sr-only">Your pick: {esc(q["options"][pick])}. </span>' if pick is not None and not ok else "")
    opts = locked_options(q["options"], q["answer_index"], pick if pick is not None else q["answer_index"])
    return (f'<details class="oq-rev {"good" if ok else "kind"}"{"" if ok else " open"}><summary><span class="n">{n}</span>'
            f'<span class="q"><span class="sr-only">Q{n}. </span>{esc(q["question"])}</span>'
            f'<span class="chev">{icon("down", 16)}</span></summary><div class="body">{yours}{sr}{opts}'
            f'<span class="sr-only">Answer: {esc(right)}</span>'
            f'<div class="oq-explain"><div class="oq-eyebrow">Mechanism</div><p>{esc(q["explanation"])}</p></div>'
            f'<p class="said">{esc(line)}</p></div></details>')


def heatmap(activity: list[dict], today, weeks: int = 18) -> str:
    """GitHub-style calendar that always fits its card: last `weeks` weeks, Monday-first."""
    from datetime import date as _d, timedelta
    pts = {}
    for r in activity:
        d = r["day"] if isinstance(r["day"], _d) else _d.fromisoformat(str(r["day"])[:10])
        pts[d] = pts.get(d, 0) + (r.get("points") or 0)
    start = today - timedelta(days=today.weekday() + 7 * (weeks - 1))
    mx = max([v for v in pts.values()] + [1])
    cells, months, last_m = "", "", None
    for w in range(weeks):
        wk = start + timedelta(days=7 * w)
        months += f"<span>{wk:%b}</span>" if wk.month != last_m else "<span></span>"
        last_m = wk.month
        for i in range(7):
            d = wk + timedelta(days=i)
            v = pts.get(d, 0)
            lv = 0 if v <= 0 else 1 if v < mx * .34 else 2 if v < mx * .67 else 3
            cls = ("out" if d > today else f"l{lv}") + (" today" if d == today else "")
            cells += f'<i class="{cls}" style="animation-delay:{w * .015:.3f}s" title="{d:%b %d}: {v} pts"></i>'
    days = "".join(f"<span>{x}</span>" for x in ["Mon", "", "Wed", "", "Fri", "", ""])
    active = sum(1 for v in pts.values() if v > 0)
    return (f'<div class="oq-heat"><div class="months">{months}</div><div class="wrap"><div class="days">{days}</div>'
            f'<div class="grid">{cells}</div></div><div class="foot"><span>{active} active day{"s" if active != 1 else ""}</span>'
            f'<span class="key">Less <i></i><i class="l1"></i><i class="l2"></i><i class="l3"></i> More</span></div></div>')


def legend(rows: list[dict]) -> str:
    return '<div class="oq-legend">' + "".join(f'<span><i style="background:{r["color"]}"></i>{esc(r["topic"])}</span>' for r in rows) + "</div>"


def badges(names: list[str]) -> str:
    if not names:
        return empty("No badges yet. Finish a set and the first one shows up here.", "trophy")
    return '<div class="oq-badges">' + "".join(f'<span class="oq-badge"><b>{icon("trophy", 13)}</b>{esc(n.replace("_", " ").title())}</span>'
                                               for n in names) + "</div>"


def chat_thread(hist: list[dict], user_name: str = "You") -> str:
    out = "".join(f'<div class="oq-msg {"a" if m["role"] == "assistant" else "u"}"><span class="who">'
                  f'{"1Q" if m["role"] == "assistant" else "You"}</span>{esc(m["content"])}</div>' for m in hist)
    return f'<div class="oq-thread">{out}</div>'
