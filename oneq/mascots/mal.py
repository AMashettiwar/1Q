"""Option 1 - Mal (Reformed): a once-rogue cell in a tiny lab coat."""
from .kit import shaded, face, arms, wrap, ao
ID = "o1"; NAME = "Mal (Reformed)"
PERSONALITY = "A once-rogue cell who went straight: lab coat, name badge, sly-sweet smirk, and all that dividing energy redirected into explaining things."
LINE = "I used to divide without permission. Now I only divide hard topics into bite-size pieces."
def svg():
    d = f'''<radialGradient id="{ID}-b" cx="36%" cy="28%" r="80%"><stop offset="0" stop-color="#cf8f84"/><stop offset=".5" stop-color="#9c4a52"/><stop offset="1" stop-color="#5e2532"/></radialGradient>
<radialGradient id="{ID}-n" cx="40%" cy="32%" r="72%"><stop offset="0" stop-color="#fbf0dc"/><stop offset=".75" stop-color="#ead2ad"/><stop offset="1" stop-color="#d6b68a"/></radialGradient>
<linearGradient id="{ID}-c" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fdfaf3"/><stop offset="1" stop-color="#e3d8c4"/></linearGradient>'''
    blob = "M120,30 C146,24 166,36 180,50 C200,66 214,84 207,110 C215,136 206,162 188,182 C172,204 146,214 120,212 C94,216 66,206 52,184 C34,164 25,138 33,112 C25,86 42,62 62,50 C78,38 96,32 120,30Z"
    nuc = "M120,52 C152,50 178,72 180,102 C182,134 156,154 120,154 C84,154 60,134 60,104 C60,74 88,52 120,52Z"
    body = shaded(ID, "b", blob, f"url(#{ID}-b)", "#3f1520", "#2a0a12", (84, 62, 16, 9), "#ffd9cc", .08)
    body += "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#5e2532" opacity=".35"/><circle cx="{x-1}" cy="{y-1}" r="{r*.4:.1f}" fill="#f6c9be" opacity=".35"/>' for x, y, r in [(52, 140, 5), (190, 92, 4), (182, 152, 3.4), (66, 82, 3)])
    body += shaded(ID, "n", nuc, f"url(#{ID}-n)", "#4e1f29", "#7a5a30", (96, 70, 12, 6), "#fff", .05)
    body += '<path d="M150,128 q6,4 12,0" stroke="#c79f6c" stroke-width="2" fill="none" opacity=".6"/>'
    coat = f'''{ao(120, 168, 60, 7, .25)}<path d="M62,170 C80,160 100,158 120,166 C140,158 160,160 178,170 L188,206 C166,222 74,222 52,206Z" fill="url(#{ID}-c)" stroke="#3f1520" stroke-width="2.4" stroke-linejoin="round"/>
<path d="M120,166 L108,196 L120,216 L132,196Z" fill="#7a2e3a" stroke="#3f1520" stroke-width="1.8"/><path d="M118,168 l2,10 l2,-10z" fill="#c9a24a"/>
<path d="M98,162 L112,192 M142,162 L128,192" stroke="#3f1520" stroke-width="2" fill="none"/>
<path d="M58,190 Q90,198 110,196" stroke="#c9bda5" stroke-width="2" fill="none" opacity=".7"/>
<rect x="146" y="186" width="20" height="15" rx="2.5" fill="#efe6d5" stroke="#3f1520" stroke-width="1.6"/><rect x="151" y="176" width="3.4" height="14" rx="1.7" fill="#1f3a5f"/><rect x="157" y="179" width="3.4" height="11" rx="1.7" fill="#7a2e3a"/>
<g><rect x="72" y="180" width="26" height="13" rx="3" fill="#f6efe1" stroke="#a8823a" stroke-width="1.6"/><text x="85" y="190" text-anchor="middle" font-family="Georgia,serif" font-size="8" font-weight="700" fill="#5e2532">MAL</text></g>'''
    st = dict(id=ID, eye="almond", brow="thin", mouth="smirk", gap=24, r=11, iris="#2f6f73", lid="#dcbc8e", blush="#b2575a", my=128, browc="#3f1520")
    a = arms((70, 172), (170, 172), 120, 128, 24, "#f4ede0", "#3f1520", "mitt", "#c7837a", wave=(46, 0, 52, -44))
    return wrap(ID, d, body + coat + face(120, 100, st) + a, (204, 28))
