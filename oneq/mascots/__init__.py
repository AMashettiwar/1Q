"""The five selectable 1Q mascots. Each renders one layered SVG holding every expression and pose;
CSS (`CSS`) shows the active one via the class `x-<expression>` and animates breathing, blinking,
waving, jumping, wiggling and the login peek. Pupils follow the pointer via ui.LIVE_JS."""
from functools import lru_cache

from . import helix, kit, mal, mito, p53, tee

ORDER = ["mal", "tee", "helix", "mito", "p53"]
DEFAULT = "mal"
_MODS = {"mal": mal, "tee": tee, "helix": helix, "mito": mito, "p53": p53}
NAMES = {"mal": "Mal", "tee": "Captain Tee", "helix": "Professor Helix", "mito": "Mito", "p53": "Professor p53"}
TAGLINES = {
    "mal": "A reformed rogue cell. Sly smirk, big heart, now divides only hard topics.",
    "tee": "A T-cell hero. Checks every ID, salutes every good answer.",
    "helix": "A bookish double helix. Twisted puns, perfect pairing.",
    "mito": "The powerhouse of the cell. Permanently caffeinated, never pushy.",
    "p53": "Guardian of the genome. Kind eyes, big brows, infinite patience.",
}
# app expressions -> the six drawn poses
_MAP = {"happy": "happy", "thinking": "thinking", "cheering": "cheering", "oops": "oops", "ticklish": "ticklish",
        "sleepy": "sleepy", "missing": "sleepy", "suspicious": "thinking"}


def key(k: str | None) -> str:
    return k if k in _MODS else DEFAULT


@lru_cache(maxsize=None)
def _raw(k: str) -> str:
    return _MODS[k].svg()


def svg(k: str | None, expression: str = "happy", size: int | None = None, extra_cls: str = "") -> str:
    k = key(k)
    e = _MAP.get(expression, "happy")
    s = _raw(k).replace('class="m"', f'class="m oq-m x-{e} {extra_cls}" data-mascot="{k}" data-expr="{e}" role="img" '
                        f'aria-label="{NAMES[k]}, {e}"' + (f' width="{size}" height="{int(size * 260 / 240)}"' if size else ""), 1)
    return s


CSS = """
.oq-m [data-e]{display:none}
""" + "".join(f'.oq-m.x-{e} [data-e~="{e}"]{{display:inline}}' for e in kit.EXPRS) + """
.oq-m{overflow:visible;cursor:pointer;-webkit-tap-highlight-color:transparent}.oq-m *{transform-box:view-box}
.oq-m .breathe{transform-origin:120px 240px;animation:qm-br 3.8s ease-in-out infinite}
@keyframes qm-br{50%{transform:scale(1.022,.984)}}
.oq-m .blink{animation:qm-bl 5.2s infinite}@keyframes qm-bl{0%,93%,100%{transform:scaleY(1)}96%{transform:scaleY(.06)}}
.oq-m .pupil{transition:transform .14s ease-out}
.oq-m .wave{animation:qm-wv 2.8s ease-in-out infinite}@keyframes qm-wv{0%,40%,100%{transform:rotate(0)}55%{transform:rotate(14deg)}70%{transform:rotate(-6deg)}85%{transform:rotate(10deg)}}
.oq-m.x-cheering .jump{transform-origin:120px 244px;animation:qm-jp 1s cubic-bezier(.3,.7,.4,1) infinite}
@keyframes qm-jp{0%,100%{transform:translateY(0) scale(1,1)}12%{transform:translateY(0) scale(1.1,.88)}40%{transform:translateY(-18px) scale(.94,1.07)}66%{transform:translateY(0) scale(1.06,.93)}80%{transform:scale(1,1)}}
.oq-m.x-cheering .shadow{transform-origin:120px 244px;animation:qm-sh 1s infinite}@keyframes qm-sh{40%{transform:scaleX(.7);opacity:.08}}
.oq-m.x-cheering .pump{animation:qm-pm .5s ease-in-out infinite alternate}@keyframes qm-pm{to{transform:translateY(-3px)}}
.oq-m.x-ticklish .jump{transform-origin:120px 240px;animation:qm-wg .26s ease-in-out infinite}@keyframes qm-wg{0%,100%{transform:rotate(-2.6deg)}50%{transform:rotate(2.6deg)}}
.oq-m.x-thinking .rig{transform-origin:120px 240px;animation:qm-tk 4s ease-in-out infinite}@keyframes qm-tk{50%{transform:rotate(3deg)}}
.oq-m.x-oops .rig{transform-origin:120px 240px;transform:rotate(-3deg) translateY(2px);transition:transform .5s}
.oq-m.x-sleepy .rig{transform-origin:120px 240px;transform:rotate(4deg) translateY(3px)}
.oq-m.x-sleepy .breathe{animation-duration:6.5s}
.oq-m.x-thinking .pupil{transform:translate(3px,-3px)!important}
.oq-m .cape{animation:qm-cp 3s ease-in-out infinite}@keyframes qm-cp{50%{transform:skewX(2deg) scaleX(1.02)}}
.oq-m .float{animation:qm-fl 2.4s ease-in-out infinite}@keyframes qm-fl{50%{transform:translateY(-4px)}}
.oq-m .zz{animation:qm-zz 3s ease-in-out infinite}@keyframes qm-zz{0%{opacity:0;transform:translate(0,6px)}30%{opacity:1}100%{opacity:0;transform:translate(8px,-10px)}}
.oq-m .spark{transform-box:fill-box;transform-origin:center;animation:qm-sp 1.2s infinite}@keyframes qm-sp{50%{transform:scale(.55) rotate(25deg);opacity:.55}}
.oq-m .steam{animation:qm-fl 2s infinite}
.oq-m.peek .rig{animation:qm-pk 2.2s cubic-bezier(.3,1.4,.5,1) both}@keyframes qm-pk{0%{transform:translateY(120px)}35%{transform:translateY(46px) rotate(-6deg)}55%{transform:translateY(46px) rotate(6deg)}100%{transform:translateY(0)}}
.oq-m.poked .jump{animation:qm-wg .22s ease-in-out 4}
@media (prefers-reduced-motion: reduce){.oq-m *{animation:none!important}}
.oq-still .oq-m *{animation:none!important}
"""
