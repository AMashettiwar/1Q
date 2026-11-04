"""Option 5 - Professor p53: tiny guardian-of-the-genome wizard."""
from .kit import shaded, face, arms, wrap, ao
ID = "o5"; NAME = "Professor p53"
PERSONALITY = "A tiny wizard protein, the 'guardian of the genome': bushy brows, kind crinkly eyes, a magnifying glass, and the patience of a checkpoint."
LINE = "I pause the cell cycle to fix things. You may pause for coffee. Both are valid checkpoints."
def svg():
    d = f'''<radialGradient id="{ID}-b" cx="36%" cy="30%" r="80%"><stop offset="0" stop-color="#86b8ad"/><stop offset=".55" stop-color="#3d7a6e"/><stop offset="1" stop-color="#1d463f"/></radialGradient>
<linearGradient id="{ID}-h" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#34588a"/><stop offset="1" stop-color="#12233f"/></linearGradient>
<linearGradient id="{ID}-g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ecd28a"/><stop offset="1" stop-color="#a8823a"/></linearGradient>'''
    blob = "M120,100 C172,100 198,130 198,166 C198,204 166,226 120,226 C74,226 42,204 42,166 C42,130 68,100 120,100Z"
    body = shaded(ID, "b", blob, f"url(#{ID}-b)", "#12302b", "#04140f", (78, 128, 16, 8), "#e0f2ea", .08)
    hat = f'''<g class="hat">{ao(120, 112, 62, 6, .3)}<path d="M52,108 Q120,124 188,108 Q198,100 184,95 Q120,108 56,95 Q42,100 52,108Z" fill="url(#{ID}-h)" stroke="#0a1528" stroke-width="2.2"/>
<path d="M74,100 Q94,58 110,32 Q122,12 152,6 Q138,20 140,36 Q150,68 166,100 Q120,110 74,100Z" fill="url(#{ID}-h)" stroke="#0a1528" stroke-width="2.4" stroke-linejoin="round"/>
<path d="M98,64 Q108,44 118,30" stroke="#fff" stroke-width="3" opacity=".18" fill="none" stroke-linecap="round"/>
<path d="M78,94 Q120,104 162,94 L160,84 Q120,94 81,84Z" fill="#7a2e3a" stroke="#3a1019" stroke-width="1.4"/>
<text x="121" y="95" text-anchor="middle" font-family="Georgia,serif" font-weight="700" font-size="9" fill="#f3e6cc" letter-spacing="1.2">p53</text>
<path d="M118,48 l2.6,5.2 l5.7,.8 l-4.1,4 l1,5.7 l-5.2,-2.7 l-5.2,2.7 l1,-5.7 l-4.1,-4 l5.7,-.8z" fill="url(#{ID}-g)" stroke="#6b5226" stroke-width=".8"/>
<circle cx="138" cy="70" r="2.4" fill="#ecd28a"/><circle cx="100" cy="76" r="1.8" fill="#ecd28a"/><circle cx="152" cy="7" r="5" fill="url(#{ID}-g)" stroke="#6b5226" stroke-width="1"/></g>'''
    stache = '<path d="M120,166 Q110,159 101,165 Q95,170 89,167 Q96,176 108,172 Q115,170 120,168 Q125,170 132,172 Q144,176 151,167 Q145,170 139,165 Q130,159 120,166Z" fill="#f4ecdc" stroke="#8b7d63" stroke-width="1.4"/>'
    st = dict(id=ID, eye="kind", brow="bushy", mouth="soft", gap=24, r=11, iris="#1f3a5f", lid="#3d7a6e", blush="#c46a6a", my=176)
    a = arms((56, 172), (184, 172), 120, 168, 24, "#16294a", "#0a1528", "mitt", "#86b8ad")
    lens = f'''<g class="lens">{ao(206, 236, 14, 3, .25)}<line x1="206" y1="214" x2="222" y2="234" stroke="#4e3518" stroke-width="7" stroke-linecap="round"/><line x1="206" y1="214" x2="222" y2="234" stroke="#8a6338" stroke-width="3.5" stroke-linecap="round"/>
<circle cx="198" cy="202" r="16" fill="#cfe5e3" fill-opacity=".4" stroke="url(#{ID}-g)" stroke-width="4.5"/><path d="M190,196 q4,-5 10,-5" stroke="#fff" stroke-width="2.6" fill="none" stroke-linecap="round"/></g>'''
    from .kit import E
    lens = E('happy thinking cheering oops ticklish', lens) + E('sleepy', f'<g transform="rotate(-58 214 224) translate(6 26)">{lens}</g>')
    return wrap(ID, d, body + hat + face(120, 142, st) + stache + a + lens, (204, 44))
