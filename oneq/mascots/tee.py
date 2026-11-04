"""Option 2 - Captain Tee: brave, slightly dorky T-cell hero."""
from .kit import shaded, face, arms, wrap, ao
ID = "o2"; NAME = "Captain Tee"
PERSONALITY = "A T-cell hero with a burgundy cape, receptor antennae and brass gloves: checks every ID at the door, salutes every good answer, trips over his own cape."
LINE = "I checked your ID at the door. It says 'future quiz champion.' Access granted."
def svg():
    d = f'''<radialGradient id="{ID}-b" cx="35%" cy="28%" r="80%"><stop offset="0" stop-color="#78b0ae"/><stop offset=".5" stop-color="#2f6f73"/><stop offset="1" stop-color="#173f48"/></radialGradient>
<linearGradient id="{ID}-k" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9a4250"/><stop offset=".6" stop-color="#6e2433"/><stop offset="1" stop-color="#4a1622"/></linearGradient>
<linearGradient id="{ID}-g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ecd28a"/><stop offset="1" stop-color="#a8823a"/></linearGradient>'''
    cape = f'''<g class="cape" style="transform-origin:120px 120px"><path d="M70,112 C42,152 36,200 48,232 C70,226 92,236 120,230 C148,236 170,226 192,232 C204,200 198,152 170,112Z" fill="url(#{ID}-k)" stroke="#3a1019" stroke-width="2.4" stroke-linejoin="round"/>
<path d="M78,140 C70,170 68,200 72,226 M162,140 C170,170 172,200 168,226" stroke="#3a1019" stroke-width="1.6" opacity=".45" fill="none"/></g>'''
    ant = ""
    for x, a in [(80, -26), (120, 0), (160, 26)]:
        ant += (f'<g class="ant" transform="rotate({a} {x} 72)"><path d="M{x},64 L{x},36 M{x},42 L{x-9},29 M{x},42 L{x+9},29" stroke="#123640" stroke-width="5.6" stroke-linecap="round" fill="none"/>'
                f'<path d="M{x},64 L{x},36 M{x},42 L{x-9},29 M{x},42 L{x+9},29" stroke="#3f8a8c" stroke-width="2.6" stroke-linecap="round" fill="none"/>'
                f'<circle cx="{x-9}" cy="28" r="4.6" fill="url(#{ID}-g)" stroke="#6b5226" stroke-width="1.2"/><circle cx="{x+9}" cy="28" r="4.6" fill="url(#{ID}-g)" stroke="#6b5226" stroke-width="1.2"/></g>')
    circ = "M120,50 C166,50 200,84 200,130 C200,176 166,210 120,210 C74,210 40,176 40,130 C40,84 74,50 120,50Z"
    body = shaded(ID, "b", circ, f"url(#{ID}-b)", "#0f2e36", "#04161b", (86, 80, 18, 10), "#d9f0ea", .08)
    body += "".join(f'<ellipse cx="{x}" cy="{y}" rx="4" ry="2.4" fill="#123640" opacity=".25" transform="rotate({r} {x} {y})"/>' for x, y, r in [(60, 150, 30), (178, 112, -20), (170, 176, 40), (70, 100, -30)])
    front = f'''{ao(120, 196, 30, 5, .25)}<path d="M64,170 Q120,196 176,170" fill="none" stroke="#123640" stroke-width="0"/>
<circle cx="120" cy="184" r="16" fill="url(#{ID}-g)" stroke="#6b5226" stroke-width="2"/><circle cx="120" cy="184" r="11.5" fill="none" stroke="#6b5226" stroke-width="1" opacity=".6"/>
<text x="120" y="191" text-anchor="middle" font-family="Georgia,serif" font-weight="700" font-size="18" fill="#4a1622">T</text>
<path d="M112,174 q4,-3 9,-2" stroke="#fff" stroke-width="2" fill="none" opacity=".7" stroke-linecap="round"/>
<path d="M114,142 q6,4 12,0" stroke="#123640" stroke-width="2" fill="none" opacity="0"/>'''
    st = dict(id=ID, eye="round", brow="thick", mouth="hero", gap=27, r=12.5, iris="#a8823a", lid="#2f6f73", blush="#c46a6a", my=146, browc="#0f2e36")
    a = arms((54, 150), (186, 150), 120, 146, 27, "#2f6f73", "#0f2e36", "glove", f"url(#{ID}-g)")
    clasp = ('<path d="M76,176 Q120,198 164,176" fill="none" stroke="#6b5226" stroke-width="2.4" stroke-dasharray="1 4" stroke-linecap="round"/>'
             + ''.join(f'<circle cx="{x}" cy="174" r="7.5" fill="url(#{ID}-g)" stroke="#6b5226" stroke-width="1.6"/><path d="M{x-3},174 l3,-3 l3,3 l-3,3z" fill="#7a2e3a"/><circle cx="{x-2.4}" cy="171.6" r="1.6" fill="#fff" opacity=".7"/>' for x in (74, 166)))
    return wrap(ID, d, cape + ant + body + front + clasp + face(120, 114, st) + a, (206, 32))
