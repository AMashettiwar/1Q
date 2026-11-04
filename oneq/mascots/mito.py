"""Option 4 - Mito: powerhouse barista-athlete."""
from .kit import shaded, face, arms, wrap, ao
ID = "o4"; NAME = "Mito"
PERSONALITY = "The powerhouse of the cell, moonlighting as a barista and personal trainer: wide-eyed, permanently caffeinated, never pushy."
LINE = "Powerhouse of the cell, reporting for duty. Your ATP is brewed, extra foam."
def svg():
    d = f'''<radialGradient id="{ID}-b" cx="34%" cy="28%" r="82%"><stop offset="0" stop-color="#efd2a6"/><stop offset=".55" stop-color="#c49a5e"/><stop offset="1" stop-color="#7f5b2e"/></radialGradient>
<linearGradient id="{ID}-i" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9a4250" stop-opacity="0"/><stop offset="1" stop-color="#7a2e3a" stop-opacity=".6"/></linearGradient>'''
    bean = "M120,62 C176,58 214,92 212,136 C210,182 170,208 120,208 C70,208 28,184 28,136 C28,90 66,64 120,62Z"
    body = shaded(ID, "b", bean, f"url(#{ID}-b)", "#4e3518", "#2a1a08", (74, 86, 18, 9), "#fff4dc", .08)
    body += f'''<clipPath id="{ID}-cl"><path d="{bean}"/></clipPath><g clip-path="url(#{ID}-cl)"><path d="M20,172 Q36,150 50,174 Q64,152 78,178 Q92,154 106,180 Q120,154 134,180 Q148,154 162,178 Q176,152 190,174 Q204,150 220,170 L220,220 L20,220Z" fill="url(#{ID}-i)"/>
<path d="M28,180 Q40,160 52,182 Q64,162 78,186 Q92,164 106,188 Q120,164 134,188 Q148,164 162,186 Q176,162 188,182 Q200,160 214,178" fill="none" stroke="#5a1f2b" stroke-width="2.4" opacity=".45"/></g>'''
    band = '''<path d="M32,112 Q120,66 208,112 L206,128 Q120,84 34,128Z" fill="#7a2e3a" stroke="#3a1019" stroke-width="2.2" stroke-linejoin="round"/>
<path d="M44,114 Q120,76 196,114" fill="none" stroke="#c9a24a" stroke-width="1.8"/><path d="M48,120 Q120,84 192,120" fill="none" stroke="#fff" stroke-width="2" opacity=".25"/>
<path d="M204,116 q12,-10 20,-6 q-6,6 -4,14 M206,124 q14,0 18,8" fill="none" stroke="#7a2e3a" stroke-width="5" stroke-linecap="round"/>'''
    st = dict(id=ID, eye="wide", brow="mid", mouth="toothy", gap=25, r=12, iris="#1f3a5f", lid="#c49a5e", blush="#b2575a", my=172, browc="#4e3518")
    a = arms((44, 160), (196, 160), 120, 172, 25, "#c49a5e", "#4e3518", "mitt", "#d8b27a")
    cup = f'''<g class="cup">{ao(212, 232, 16, 3, .28)}<path d="M196,198 L228,198 L224,230 Q212,236 200,230Z" fill="#fbf7ee" stroke="#1b2629" stroke-width="2.2"/>
<path d="M227,206 q10,0 9,9 q-1,8 -10,7" fill="none" stroke="#1b2629" stroke-width="2.4"/><rect x="194" y="194" width="36" height="6.5" rx="3.2" fill="#1f3a5f" stroke="#0e1c33" stroke-width="1.4"/>
<path d="M205,212 l5,-8 l0,6 l6,-1 l-6,10 l0,-6z" fill="#c9a24a"/><path d="M200,204 q2,16 6,24" stroke="#fff" stroke-width="2" opacity=".7" fill="none"/>
<path class="steam" d="M206,186 q-5,-7 0,-14 q5,-7 0,-14 M218,186 q-5,-7 0,-14" fill="none" stroke="#8a9a9a" stroke-width="2.2" stroke-linecap="round" opacity=".6"/></g>'''
    return wrap(ID, d, body + band + face(120, 146, st) + a + cup, (206, 34))
