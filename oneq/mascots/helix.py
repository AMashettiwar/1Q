"""Option 3 - Professor Helix: bookish DNA whose whole torso is a double helix."""
import math
from .kit import shaded, face, arms, wrap, ao
ID = "o3"; NAME = "Professor Helix"
PERSONALITY = "A bookish double helix (literally: the torso is the molecule) with brass specs and a burgundy bow tie, fluent in puns and base-pairing etiquette."
LINE = "I'm a little twisted, but I always pair up right: A with T, C with G, and you with 12 good questions."
def svg():
    d = f'''<radialGradient id="{ID}-h" cx="38%" cy="28%" r="80%"><stop offset="0" stop-color="#fbf1dd"/><stop offset=".6" stop-color="#e6cda3"/><stop offset="1" stop-color="#c29f6c"/></radialGradient>
<linearGradient id="{ID}-sa" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#16294a"/><stop offset=".5" stop-color="#3b5d8f"/><stop offset="1" stop-color="#16294a"/></linearGradient>
<linearGradient id="{ID}-sb" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3f6b4f"/><stop offset=".5" stop-color="#6f9a7a"/><stop offset="1" stop-color="#26472f"/></linearGradient>'''
    # torso: two ribbons twisting, back halves drawn first, rungs between
    top, bot, amp = 146, 226, 30
    def pts(ph):
        return [(120 + amp * (.72 + .28 * math.sin(math.pi * t / 26)) * math.sin(ph + t / 26 * 2 * math.pi * .85), top + t / 26 * (bot - top)) for t in range(27)]
    A, B = pts(0), pts(math.pi)
    def segs(P, front):
        out = []
        for i in range(len(P) - 1):
            ph = i / 26 * 2 * math.pi * .85
            isfront = math.cos(ph) > 0
            if isfront == front:
                out.append(f"M{P[i][0]:.1f},{P[i][1]:.1f} L{P[i+1][0]:.1f},{P[i+1][1]:.1f}")
        return " ".join(out)
    cols = ["#7a2e3a", "#c9a24a", "#2f6f73", "#b8935f"]
    rungs = "".join(f'<line x1="{A[i][0]:.1f}" y1="{A[i][1]:.1f}" x2="{B[i][0]:.1f}" y2="{B[i][1]:.1f}" stroke="#1b2629" stroke-width="7" stroke-linecap="round"/><line x1="{A[i][0]:.1f}" y1="{A[i][1]:.1f}" x2="{B[i][0]:.1f}" y2="{B[i][1]:.1f}" stroke="{cols[(i//3)%4]}" stroke-width="4" stroke-linecap="round"/><line x1="{(A[i][0]+B[i][0])/2:.1f}" y1="{A[i][1]:.1f}" x2="{B[i][0]:.1f}" y2="{B[i][1]:.1f}" stroke="{cols[((i//3)+2)%4]}" stroke-width="4" stroke-linecap="round"/>' for i in range(1, 26, 3) if abs(A[i][0]-B[i][0]) > 10)
    rib = lambda dd, g, w=13: f'<path d="{dd}" stroke="#1b2629" stroke-width="{w+4}" stroke-linecap="round" fill="none"/><path d="{dd}" stroke="url(#{g})" stroke-width="{w}" stroke-linecap="round" fill="none"/><path d="{dd}" stroke="#fff" stroke-width="2.5" stroke-linecap="round" fill="none" opacity=".25" transform="translate(-2 -2)"/>'
    vest = f'<path d="M84,150 C78,182 80,212 92,232 L148,232 C160,212 162,182 156,150 Q120,142 84,150Z" fill="#efe4cf" opacity=".55" stroke="#c29f6c" stroke-width="1.6" stroke-dasharray="2 5"/>'
    torso = vest + ao(120, 140, 40, 8, .2) + rib(segs(A, False), f"{ID}-sa") + rib(segs(B, False), f"{ID}-sb") + rungs + rib(segs(A, True), f"{ID}-sa") + rib(segs(B, True), f"{ID}-sb")
    head = "M120,36 C156,36 178,62 178,96 C178,130 154,148 120,148 C86,148 62,130 62,96 C62,62 84,36 120,36Z"
    hd = shaded(ID, "h", head, f"url(#{ID}-h)", "#6b4e2a", "#4a3010", (92, 56, 14, 8), "#fff", .06)
    hair = '<path d="M86,48 C96,30 132,26 150,40 C140,36 128,38 120,44 C112,36 98,38 86,48Z" fill="#5a4630" stroke="#3a2a18" stroke-width="1.6"/>'
    bow = '<g><path d="M120,150 L102,141 L102,159Z M120,150 L138,141 L138,159Z" fill="#7a2e3a" stroke="#3a1019" stroke-width="2" stroke-linejoin="round"/><circle cx="120" cy="150" r="4.5" fill="#5a1f2b" stroke="#3a1019" stroke-width="1.6"/></g>'
    st = dict(id=ID, eye="bead", brow="mid", mouth="teeth2", gap=22, r=12, iris="#3f6b4f", lid="#e6cda3", blush="#c4776a", my=118, browc="#5a4630")
    glasses = '<g fill="#cfe5e3" fill-opacity=".18" stroke="#a8823a" stroke-width="2.8"><circle cx="98" cy="96" r="16"/><circle cx="142" cy="96" r="16"/></g><path d="M114,95 Q120,90 126,95 M82,92 L64,88 M158,92 L176,88" stroke="#a8823a" stroke-width="2.8" fill="none"/><path d="M88,86 l7,-4 M132,86 l7,-4" stroke="#fff" stroke-width="2.4" stroke-linecap="round" opacity=".8"/>'
    a = arms((92, 158), (148, 158), 120, 118, 22, "#e6cda3", "#6b4e2a", "cuff", "#e6cda3", w=10)
    book = '<g class="book"><path d="M30,208 L58,202 L60,226 L32,232Z" fill="#234232" stroke="#13261c" stroke-width="2"/><path d="M58,202 L60,226" stroke="#c9a24a" stroke-width="2"/><text x="44" y="220" font-family="Georgia,serif" font-size="7" fill="#c9a24a" transform="rotate(-11 44 220)">ATCG</text></g>'
    return wrap(ID, d, torso + book + hd + hair + face(120, 96, st) + glasses + bow + a, (200, 26))
