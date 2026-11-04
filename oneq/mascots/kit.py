"""Rendering kit for 1Q mascots v2: shading, arms, per-character faces.
Every character supplies its own face style; this file only holds the drawing primitives."""
INK = "#1b2629"
EXPRS = ["happy", "thinking", "cheering", "oops", "ticklish", "sleepy"]

def E(names, inner, cls=""):
    return f'<g data-e="{names}" class="{cls}">{inner}</g>'

def defs_common(p):
    return f'''<filter id="{p}-tex" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="7"/>
<feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .55 0"/><feComposite in2="SourceGraphic" operator="in"/></filter>
<filter id="{p}-blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.4"/></filter>
<filter id="{p}-blur6" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
<linearGradient id="{p}-rim" x1="0" y1="0" x2="1" y2=".25"><stop offset=".55" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff" stop-opacity=".75"/></linearGradient>'''

def shaded(p, key, d, fill, stroke, shade="#000", spec=(0, 0, 0, 0), rimc="#f4e6c8", tex=.18):
    """Body path with AO, rim light, specular and fine membrane texture."""
    sx, sy, rx, ry = spec
    return f'''<clipPath id="{p}-{key}c"><path d="{d}"/></clipPath>
<path d="{d}" fill="{fill}"/>
<g clip-path="url(#{p}-{key}c)">
 <path d="{d}" fill="none" stroke="{shade}" stroke-width="26" opacity=".16" filter="url(#{p}-blur6)" transform="translate(-6 8)"/>
 <path d="{d}" fill="none" stroke="{rimc}" stroke-width="7" opacity=".55" filter="url(#{p}-blur)" transform="translate(-5 -4)" style="mix-blend-mode:screen"/>
 <rect x="0" y="0" width="240" height="260" filter="url(#{p}-tex)" opacity="{tex}"/>
 {f'<ellipse cx="{sx}" cy="{sy}" rx="{rx}" ry="{ry}" fill="#fff" opacity=".55" filter="url(#{p}-blur)"/><ellipse cx="{sx+2}" cy="{sy-1}" rx="{rx*.35:.1f}" ry="{ry*.3:.1f}" fill="#fff" opacity=".85"/>' if rx else ''}
</g>
<path d="{d}" fill="none" stroke="{stroke}" stroke-width="2.6" stroke-linejoin="round"/>'''

def ao(cx, cy, rx, ry, op=.22):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#000" opacity="{op}" style="filter:blur(3px)"/>'

# ---------- arms ----------
def _arm(s, e, h, col, dark, hand, hcol, w=12):
    (sx, sy), (ex, ey), (hx, hy) = s, e, h
    d = f"M{sx},{sy} Q{ex},{ey} {hx},{hy}"
    if hand == "glove":
        hd = f'<circle cx="{hx}" cy="{hy}" r="8.5" fill="{hcol}" stroke="{dark}" stroke-width="2.2"/><circle cx="{hx-3}" cy="{hy-3}" r="2.4" fill="#fff" opacity=".5"/>'
    elif hand == "cuff":
        hd = f'<circle cx="{hx}" cy="{hy}" r="7.5" fill="{hcol}" stroke="{dark}" stroke-width="2.2"/>'
    else:
        hd = f'<circle cx="{hx}" cy="{hy}" r="7.8" fill="{hcol}" stroke="{dark}" stroke-width="2.2"/><circle cx="{hx-2.5}" cy="{hy-2.5}" r="2" fill="#fff" opacity=".45"/>'
    return (f'<path d="{d}" fill="none" stroke="{dark}" stroke-width="{w+4.4}" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="#fff" stroke-width="2.5" stroke-linecap="round" opacity=".22" transform="translate(-2 -2)"/>{hd}')

def arms(L, R, cx, cheekY, gap, col, dark, hand="mitt", hcol=None, w=12, wave=(26, -2, 30, -30)):
    """Per-expression poses. L,R are shoulder points. Returns data-e groups."""
    hcol = hcol or col
    (lx, ly), (rx, ry) = L, R
    A = lambda s, e, h: _arm(s, e, h, col, dark, hand, hcol, w)
    rest_l = A(L, (lx-16, ly+14), (lx-12, ly+34))
    rest_r = A(R, (rx+16, ry+14), (rx+12, ry+34))
    out = [
        E("happy", rest_l + f'<g class="wave" style="transform-origin:{rx}px {ry}px">' + A(R, (rx+wave[0], ry+wave[1]), (rx+wave[2], ry+wave[3])) + '</g>'),
        E("thinking", rest_l + A(R, (rx+8, ry+30), (cx+10, cheekY+18))),
        E("cheering", A(L, (lx-28, ly-10), (lx-26, ly-46)) + A(R, (rx+28, ry-10), (rx+26, ry-46)), "pump"),
        E("oops", A(L, (lx-16, ly+30), (cx-gap-6, cheekY+2)) + A(R, (rx+16, ry+30), (cx+gap+6, cheekY+2))),
        E("ticklish", A(L, (lx-2, ly+26), (lx+12, ly+24)) + A(R, (rx+2, ry+26), (rx-12, ry+24))),
        E("sleepy", A(L, (lx-8, ly+24), (lx-4, ly+44)) + A(R, (rx+8, ry+24), (rx+4, ry+44))),
    ]
    return "".join(out)

# ---------- faces ----------
def face(cx, cy, st):
    """st: dict(eye=, brow=, mouth=, gap=, r=, iris=, lid=, blush=, my=, browc=)."""
    g, r = st["gap"], st["r"]; my = st["my"]; iris = st["iris"]; lid = st["lid"]; bc = st.get("browc", INK)
    L, R = cx - g, cx + g
    out = []

    def eye(x, mode="open"):
        k = st["eye"]
        if k == "bead":
            s = r * .55
            return (f'<g class="blink" style="transform-origin:{x}px {cy}px"><g class="pupil"><ellipse cx="{x}" cy="{cy}" rx="{s}" ry="{s*1.15:.1f}" fill="{INK}"/>'
                    f'<circle cx="{x+s*.35:.1f}" cy="{cy-s*.4:.1f}" r="{s*.36:.1f}" fill="#fff"/></g></g>')
        ry = r * {"round": 1.15, "wide": 1.32, "almond": .92, "kind": 1.05}[k]
        rx = r * (1.1 if k == "almond" else 1)
        ir = r * {"round": .72, "wide": .46, "almond": .66, "kind": .64}[k]
        lidcov = {"round": 0, "wide": 0, "almond": .24, "kind": .34}[k]
        clip = f'{st["id"]}-ec{int(x)}'
        lidp = ""
        if lidcov:
            top = cy - ry; ly = top + 2 * ry * lidcov
            tilt = 3 if (k == "almond" and x > cx) else (-3 if k == "almond" else 0)
            lidp = (f'<path d="M{x-rx-2},{top-2} L{x+rx+2},{top-2} L{x+rx+2},{ly+tilt} Q{x},{ly+3} {x-rx-2},{ly-tilt} Z" fill="{lid}"/>'
                    f'<path d="M{x-rx},{ly-tilt} Q{x},{ly+3} {x+rx},{ly+tilt}" fill="none" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/>')
        lash = ""
        if k == "almond":
            sgn = -1 if x < cx else 1
            lash = f'<path d="M{x+sgn*rx},{cy-2} l{sgn*5},-4" stroke="{INK}" stroke-width="2.4" stroke-linecap="round"/>'
        return (f'<clipPath id="{clip}"><ellipse cx="{x}" cy="{cy}" rx="{rx}" ry="{ry:.1f}"/></clipPath>'
                f'<g class="blink" style="transform-origin:{x}px {cy}px"><ellipse cx="{x}" cy="{cy}" rx="{rx}" ry="{ry:.1f}" fill="#fffcf3"/>'
                f'<g clip-path="url(#{clip})"><ellipse cx="{x}" cy="{cy-ry*.6:.1f}" rx="{rx}" ry="{ry*.5:.1f}" fill="#9aa" opacity=".22"/>'
                f'<g class="pupil"><circle cx="{x}" cy="{cy+1}" r="{ir:.1f}" fill="{iris}"/><circle cx="{x}" cy="{cy+1}" r="{ir*.55:.1f}" fill="{INK}"/>'
                f'<circle cx="{x}" cy="{cy+1}" r="{ir*.95:.1f}" fill="none" stroke="#000" stroke-opacity=".25" stroke-width="1.2"/>'
                f'<circle cx="{x+ir*.38:.1f}" cy="{cy-ir*.35:.1f}" r="{max(1.6, ir*.32):.1f}" fill="#fff"/><circle cx="{x-ir*.35:.1f}" cy="{cy+ir*.45:.1f}" r="{max(.9, ir*.14):.1f}" fill="#fff" opacity=".85"/></g>'
                f'{lidp}</g><ellipse cx="{x}" cy="{cy}" rx="{rx}" ry="{ry:.1f}" fill="none" stroke="{INK}" stroke-width="2.4"/>{lash}</g>')

    out.append(E("happy thinking oops", eye(L) + eye(R)))
    arc = lambda x: f'<path d="M{x-r},{cy+3} Q{x},{cy-r-3} {x+r},{cy+3}" fill="none" stroke="{INK}" stroke-width="3.6" stroke-linecap="round"/>'
    out.append(E("cheering", arc(L) + arc(R)))
    sq = (f'<path d="M{L-r+1},{cy-6} L{L+r-2},{cy} L{L-r+1},{cy+6}" fill="none" stroke="{INK}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>'
          f'<path d="M{R+r-1},{cy-6} L{R-r+2},{cy} L{R+r-1},{cy+6}" fill="none" stroke="{INK}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>')
    out.append(E("ticklish", sq))
    slp = lambda x: f'<path d="M{x-r},{cy} Q{x},{cy+r*.8:.1f} {x+r},{cy}" fill="none" stroke="{INK}" stroke-width="3.2" stroke-linecap="round"/>'
    out.append(E("sleepy", slp(L) + slp(R)))

    # brows: style decides thickness/shape
    bs = st["brow"]; by = cy - r * 1.3 - (6 if bs != "bushy" else 4)
    def brow(x, lift=0, tilt=0, flip=1):
        if bs == "bushy":
            return (f'<path d="M{x-12},{by+2-lift+tilt*flip} Q{x-4},{by-9-lift} {x+3},{by-4-lift} Q{x+9},{by-9-lift} {x+13},{by+1-lift-tilt*flip} '
                    f'Q{x},{by+4-lift} {x-12},{by+2-lift+tilt*flip}Z" fill="#f4ecdc" stroke="#8b7d63" stroke-width="1.6"/>')
        w = {"thick": 5.5, "thin": 2.6, "mid": 3.6}[bs]
        return f'<path d="M{x-9},{by+1-lift+tilt*flip} Q{x},{by-5-lift} {x+9},{by+1-lift-tilt*flip}" fill="none" stroke="{bc}" stroke-width="{w}" stroke-linecap="round"/>'
    out.append(E("happy", brow(L, 1) + brow(R, 1)))
    out.append(E("cheering", brow(L, 5) + brow(R, 5)))
    out.append(E("thinking", brow(L, -2, 0) + brow(R, 6, 0)))
    out.append(E("oops", brow(L, 2, 4, 1) + brow(R, 2, 4, -1)))
    out.append(E("ticklish", brow(L, 4, 2, 1) + brow(R, 4, 2, -1)))
    out.append(E("sleepy", brow(L, -3) + brow(R, -3)))

    bl = st["blush"]
    out.append(E("happy thinking cheering oops sleepy", f'<ellipse cx="{L-5}" cy="{my-4}" rx="7.5" ry="4.2" fill="{bl}" opacity=".42" filter="url(#{st["id"]}-blur)"/><ellipse cx="{R+5}" cy="{my-4}" rx="7.5" ry="4.2" fill="{bl}" opacity=".42" filter="url(#{st["id"]}-blur)"/>'))
    out.append(E("ticklish", f'<ellipse cx="{L-4}" cy="{my-5}" rx="10" ry="5.5" fill="{bl}" opacity=".85" filter="url(#{st["id"]}-blur)"/><ellipse cx="{R+4}" cy="{my-5}" rx="10" ry="5.5" fill="{bl}" opacity=".85" filter="url(#{st["id"]}-blur)"/>'))
    out.append(mouths(cx, my, st["mouth"]))
    return "\n".join(out)

TONGUE = "#c26a66"
def mouths(cx, my, m):
    o = []
    open_big = (f'<path d="M{cx-14},{my-4} Q{cx},{my-1} {cx+14},{my-4} Q{cx+12},{my+17} {cx},{my+17} Q{cx-12},{my+17} {cx-14},{my-4}Z" fill="#3a1d22" stroke="{INK}" stroke-width="2"/>'
                f'<path d="M{cx-7},{my+11} Q{cx},{my+5} {cx+7},{my+11} Q{cx},{my+16} {cx-7},{my+11}Z" fill="{TONGUE}"/>')
    if m == "smirk":   # Mal: lopsided reformed-rogue smirk with one tiny fang
        o.append(E("happy", f'<path d="M{cx-12},{my} Q{cx-2},{my+9} {cx+12},{my-5}" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/><path d="M{cx+3},{my+3.2} l2,5 l2.5,-6.2" fill="#fffcf3" stroke="{INK}" stroke-width="1.3" stroke-linejoin="round"/>'))
        o.append(E("thinking", f'<path d="M{cx-8},{my+3} Q{cx},{my} {cx+9},{my-2}" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'))
    elif m == "hero":  # Tee: wide square heroic grin with teeth
        o.append(E("happy", f'<path d="M{cx-15},{my-3} L{cx+15},{my-3} Q{cx+13},{my+12} {cx},{my+12} Q{cx-13},{my+12} {cx-15},{my-3}Z" fill="#3a1d22" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/><path d="M{cx-13},{my-2} L{cx+13},{my-2} L{cx+12},{my+3} L{cx-12},{my+3}Z" fill="#fffcf3"/><path d="M{cx-6},{my+9} Q{cx},{my+5} {cx+6},{my+9} Q{cx},{my+12} {cx-6},{my+9}Z" fill="{TONGUE}"/>'))
        o.append(E("thinking", f'<path d="M{cx-9},{my+2} L{cx+9},{my}" stroke="{INK}" stroke-width="3.2" stroke-linecap="round"/>'))
    elif m == "teeth2":  # Helix: polite smile, two buck teeth
        o.append(E("happy", f'<path d="M{cx-11},{my-2} Q{cx},{my+11} {cx+11},{my-2} Z" fill="#3a1d22" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/><rect x="{cx-5}" y="{my-2}" width="4.6" height="5.5" rx="1" fill="#fffcf3"/><rect x="{cx+.4}" y="{my-2}" width="4.6" height="5.5" rx="1" fill="#fffcf3"/>'))
        o.append(E("thinking", f'<path d="M{cx-6},{my+2} Q{cx-2},{my-1} {cx+2},{my+2} Q{cx+6},{my+5} {cx+9},{my+1}" fill="none" stroke="{INK}" stroke-width="2.8" stroke-linecap="round"/>'))
    elif m == "toothy":  # Mito: big caffeinated open grin
        o.append(E("happy", f'<path d="M{cx-16},{my-4} Q{cx},{my+1} {cx+16},{my-4} Q{cx+12},{my+16} {cx},{my+16} Q{cx-12},{my+16} {cx-16},{my-4}Z" fill="#3a1d22" stroke="{INK}" stroke-width="2.2"/><path d="M{cx-13},{my-2} Q{cx},{my+2} {cx+13},{my-2} L{cx+12},{my+3} Q{cx},{my+6} {cx-12},{my+3}Z" fill="#fffcf3"/><path d="M{cx-7},{my+11} Q{cx},{my+6} {cx+7},{my+11} Q{cx},{my+15} {cx-7},{my+11}Z" fill="{TONGUE}"/>'))
        o.append(E("thinking", f'<path d="M{cx-8},{my+2} Q{cx-4},{my-2} {cx},{my+2} Q{cx+4},{my+6} {cx+8},{my+2}" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'))
    else:  # soft (p53): small warm smile, readable under a trimmed moustache
        o.append(E("happy", f'<path d="M{cx-9},{my} Q{cx},{my+10} {cx+9},{my} Z" fill="#3a1d22" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/><path d="M{cx-4},{my+5} Q{cx},{my+3} {cx+4},{my+5} Q{cx},{my+7.5} {cx-4},{my+5}Z" fill="{TONGUE}"/>'))
        o.append(E("thinking", f'<path d="M{cx-6},{my+2} Q{cx},{my-1} {cx+7},{my+2}" fill="none" stroke="{INK}" stroke-width="2.8" stroke-linecap="round"/>'))
    o.append(E("cheering", open_big))
    o.append(E("oops", f'<path d="M{cx-9},{my+4} q4.5,-5 9,0 q4.5,5 9,0" fill="none" stroke="{INK}" stroke-width="2.8" stroke-linecap="round"/>'))
    o.append(E("ticklish", f'<path d="M{cx-12},{my-3} Q{cx},{my-1} {cx+12},{my-3} Q{cx+9},{my+13} {cx},{my+13} Q{cx-9},{my+13} {cx-12},{my-3}Z" fill="#3a1d22" stroke="{INK}" stroke-width="2"/><path d="M{cx-6},{my+8} Q{cx},{my+3} {cx+6},{my+8} Q{cx},{my+12} {cx-6},{my+8}Z" fill="{TONGUE}"/>'))
    o.append(E("sleepy", f'<ellipse cx="{cx+2}" cy="{my+3}" rx="3.6" ry="4.6" fill="#3a1d22" stroke="{INK}" stroke-width="1.6"/><path d="M{cx+6},{my+6} q3,4 1,8 q-3,-2 -1,-8z" fill="#bfe0e6" opacity=".9"/>'))
    return "\n".join(o)

def extras(x, y, accent="#b8925a", ink="#2f5d62"):
    return "\n".join([
        E("thinking", f'<g class="float"><circle cx="{x-8}" cy="{y+20}" r="3" fill="{accent}"/><circle cx="{x}" cy="{y+9}" r="4.5" fill="{accent}"/><text x="{x+6}" y="{y}" font-family="Georgia,serif" font-size="26" font-weight="700" fill="{accent}">?</text></g>'),
        E("cheering", "".join(f'<path class="spark" style="animation-delay:{d}s" d="M{a},{b-8} L{a+2.2},{b-2.2} L{a+8},{b} L{a+2.2},{b+2.2} L{a},{b+8} L{a-2.2},{b+2.2} L{a-8},{b} L{a-2.2},{b-2.2}Z" fill="#c9a24a"/>' for a, b, d in [(x+4, y+6, 0), (x-176, y+20, .3), (x+10, y+70, .6), (x-168, y+80, .45)])),
        E("oops", f'<path d="M{x-6},{y+34} q-7,11 0,16 q7,-5 0,-16Z" fill="#a9d0d6" stroke="{ink}" stroke-width="1.5"/>'),
        E("ticklish", f'<text class="float" x="{x-14}" y="{y+18}" font-family="Georgia,serif" font-style="italic" font-size="16" fill="#7a2e3a">hee</text><text class="float" style="animation-delay:.4s" x="{x-186}" y="{y+40}" font-family="Georgia,serif" font-style="italic" font-size="14" fill="#7a2e3a">hee!</text>'),
        E("sleepy", f'<g class="zz"><text x="{x-8}" y="{y+26}" font-family="Georgia,serif" font-size="14" fill="{ink}">z</text><text x="{x+2}" y="{y+10}" font-family="Georgia,serif" font-size="20" fill="{ink}">Z</text></g>'),
    ])

def wrap(oid, defs, layers, extra_xy=(200, 30)):
    return f'''<svg class="m" data-id="{oid}" viewBox="0 0 240 260" xmlns="http://www.w3.org/2000/svg">
<defs>{defs_common(oid)}{defs}</defs>
<ellipse class="shadow" cx="120" cy="244" rx="64" ry="8" fill="#1d2b2e" opacity=".16" filter="url(#{oid}-blur)"/>
<g class="rig"><g class="jump"><g class="breathe">{layers}</g></g></g>
{extras(*extra_xy)}
</svg>'''
