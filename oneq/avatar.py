"""1Q, the mascot: SVG faces, moods, line banks, easter eggs, rewards."""
from __future__ import annotations

import hashlib
import random
from datetime import date, datetime

# ---------------------------------------------------------------- SVG mascot
# 1Q is a geometric cell: a deep green body, an offset nucleus, a brass orbit ring.
# Expressions change only the eyes and mouth, so the character stays calm and recognisable.
_EYES = {
    "happy": '<path d="M41 55 q5 -5 10 0"/><path d="M69 55 q5 -5 10 0"/>',
    "thinking": '<rect x="44" y="49" width="5" height="9" rx="2.5" fill="{eye}" stroke="none"/>'
                '<rect x="72" y="47" width="5" height="9" rx="2.5" fill="{eye}" stroke="none"/><path d="M68 41 l10 -3"/>',
    "cheering": '<path d="M40 56 q6 -8 12 0"/><path d="M68 56 q6 -8 12 0"/>',
    "oops": '<circle cx="46" cy="53" r="3.2" fill="{eye}" stroke="none"/><circle cx="74" cy="53" r="3.2" fill="{eye}" stroke="none"/>',
    "ticklish": '<path d="M41 50 l9 4 l-9 4"/><path d="M79 50 l-9 4 l9 4"/>',
    "sleepy": '<path d="M41 55 h10"/><path d="M69 55 h10"/>',
    "missing": '<rect x="44" y="52" width="5" height="7" rx="2.5" fill="{eye}" stroke="none"/>'
               '<rect x="71" y="52" width="5" height="7" rx="2.5" fill="{eye}" stroke="none"/><path d="M40 47 l10 2"/><path d="M80 47 l-10 2"/>',
    "suspicious": '<path d="M41 54 h10"/><rect x="71" y="49" width="5" height="9" rx="2.5" fill="{eye}" stroke="none"/>',
}
_MOUTH = {
    "happy": '<path d="M52 70 q8 6 16 0"/>',
    "thinking": '<path d="M54 71 h10"/>',
    "cheering": '<path d="M50 68 q10 10 20 0 z" fill="{eye}"/>',
    "oops": '<circle cx="60" cy="71" r="3" />',
    "ticklish": '<path d="M49 68 q11 10 22 0"/>',
    "sleepy": '<path d="M56 71 q4 2 8 0"/>',
    "missing": '<path d="M53 73 q7 -4 14 0"/>',
    "suspicious": '<path d="M53 71 q7 -2 14 1"/>',
}
ACCESSORIES = {  # fine line art in brass
    "": "",
    "lab_coat": '<path d="M44 98 l16 8 l16 -8" fill="none" stroke="{brass}" stroke-width="2"/><circle cx="60" cy="106" r="1.6" fill="{brass}"/>',
    "goggles": '<rect x="36" y="45" width="20" height="16" rx="8" fill="none" stroke="{brass}" stroke-width="2"/>'
               '<rect x="64" y="45" width="20" height="16" rx="8" fill="none" stroke="{brass}" stroke-width="2"/><path d="M56 53 h8" stroke="{brass}" stroke-width="2"/>',
    "headphones": '<path d="M24 60 q36 -54 72 0" fill="none" stroke="{brass}" stroke-width="2.5"/><rect x="18" y="56" width="8" height="16" rx="4" fill="{brass}"/><rect x="94" y="56" width="8" height="16" rx="4" fill="{brass}"/>',
    "crown": '<path d="M46 22 l5 -10 l9 8 l9 -8 l5 10 z" fill="none" stroke="{brass}" stroke-width="2" stroke-linejoin="round"/>',
    "wizard_hat": '<path d="M48 24 l12 -22 l12 22" fill="none" stroke="{brass}" stroke-width="2" stroke-linejoin="round"/><circle cx="60" cy="2" r="2" fill="{brass}"/>',
    "party_hat": '<path d="M52 22 l8 -16 l8 16 z" fill="none" stroke="{brass}" stroke-width="2" stroke-linejoin="round"/>',
    "pipette": '<path d="M96 44 l12 -26" stroke="{brass}" stroke-width="2"/><circle cx="108" cy="16" r="3" fill="none" stroke="{brass}" stroke-width="2"/>',
}
ACCESSORY_NAMES = {
    "lab_coat": "Lab coat collar", "party_hat": "Party hat", "crown": "Brass crown",
    "goggles": "Safety goggles", "headphones": "Focus headphones", "pipette": "Lucky pipette",
    "wizard_hat": "Pathway wizard hat",
}


def svg(expression: str = "happy", accessory: str = "", energy: int = 100, size: int = 104,
        palette: tuple = ("#1f3d2b", "#f4efe4", "#a8874a")) -> str:
    body, eye, brass = palette
    e = expression if expression in _EYES else "happy"
    op = 0.55 + 0.45 * max(0, min(100, energy)) / 100
    anim = {"cheering": "oneq-bounce", "ticklish": "oneq-wiggle", "sleepy": "oneq-breathe",
            "missing": "oneq-breathe"}.get(e, "oneq-float")
    fill = lambda t: t.replace("{eye}", eye).replace("{brass}", brass)
    return (
        f'<svg class="oneq-avatar {anim}" width="{size}" height="{size}" viewBox="0 -6 120 126" role="img" '
        f'aria-label="1Q, {e}" xmlns="http://www.w3.org/2000/svg">'
        f'<g class="oneq-orbit"><ellipse cx="60" cy="60" rx="54" ry="20" fill="none" stroke="{brass}" stroke-width="1.2" '
        f'stroke-opacity=".55" transform="rotate(-18 60 60)"/><circle cx="111" cy="47" r="2.6" fill="{brass}"/></g>'
        f'<circle cx="60" cy="60" r="40" fill="{body}" opacity="{op:.2f}"/>'
        f'<circle cx="60" cy="60" r="40" fill="none" stroke="{brass}" stroke-opacity=".35"/>'
        f'<circle cx="78" cy="38" r="8" fill="{eye}" opacity=".10"/>'
        f'<g stroke="{eye}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round">'
        f'<g class="blink">{fill(_EYES[e])}</g>{fill(_MOUTH[e])}</g>'
        f'{fill(ACCESSORIES.get(accessory, ""))}</svg>'
    )


# ---------------------------------------------------------------- line banks
CORRECT = [
    "Correct. Your neurons just fired in perfect formation.",
    "Nailed it. Somewhere a p53 molecule is proud of you.",
    "Right answer. That was cleaner than a fresh flow cytometer.",
    "Yes! You read that like a well-annotated UMAP.",
    "Correct. I would high-five you but I am mostly cytoplasm.",
    "Boom. That knowledge is now clonally expanded in your brain.",
    "Exactly right. Your synapses deserve a raise.",
    "Correct. Peer review would approve this on first pass.",
    "You got it. That is a statistically significant brain. p < 0.05, vibes < 0.001.",
    "Correct! I'd give you a hug but I'm worried about cross-contamination.",
    "Right! You're on a roll. Like a ribosome on an mRNA.",
    "Yes! That answer was so good it got upregulated.",
    "Correct. I am adding this to your highlight reel.",
]
WRONG = [
    "Great attempt. Here is the plot twist.",
    "Close call. This one trips up a lot of smart people, here is the trick.",
    "Not this time, and that is how learning works. Read this and you will own it tomorrow.",
    "Good instinct, wrong branch of the pathway. Here is the right one.",
    "Every expert got this wrong once. Your turn is now done. Here is the answer.",
    "Plot twist incoming. I will bring this back in a new outfit so you can win it.",
    "No stress. Mistakes are just mutations your brain gets to repair.",
    "Wrong turn, great energy. Even GPS recalculates. Here is the route.",
]
FAST_CORRECT = ["That was quick. Did you even blink?", "Speed and accuracy. Rare combo, like a clean Western blot."]
SLOW_THINK = ["Taking your time. Good scientists think before they pipette.", "Thoughtful. I respect a careful reader."]
HINTS = [
    "Hint: think about which answer a cell would actually survive.",
    "Hint: cross out the option that sounds most like a textbook typo.",
    "Hint: the right answer is usually the most specific mechanism, not the vaguest.",
    "Hint: ask which option a reviewer could not argue with.",
    "Hint: picture the experiment. Which result would you see on the plot?",
    "Hint: one option is from a totally different pathway. Kick it out first.",
]
TICKLE = [
    "Hey there.", "Yes? I am listening.", "Okay that tickles a bit.",
    "Stop, I'm ticklish!", "Hahaha my membrane cannot take this!",
    "I am going to undergo mitosis from laughing.", "Okay okay, I surrender my ribosomes!",
    "You have discovered my one weakness. Please use it for science.",
    "Fine. You win. I am resetting my dignity now.",
]
CHEATING = [
    "I can smell a chatbot from here. Put it down, you've got this brain on your own.",
    "That was suspiciously fast. If a robot helped, tell it 1Q says hi. Then try solo.",
    "Your answers are arriving with metronome timing. Are you a cell or a clock?",
    "Copying the question? I get it, it is a good question. Your own guess is better for learning though.",
    "Tab hopping detected. The answer is in your head, not in tab 14.",
]
STREAK_MILESTONES = {
    3: "Three days straight. That is a habit forming. I can see the synapses wiring.",
    7: "Seven-day streak! You earned a streak shield. One free miss is now in your pocket.",
    14: "Two weeks. You are officially more consistent than my cell cycle.",
    30: "Thirty days. That is a full month of brain gains. I am framing this.",
    50: "Fifty days. Legends are made of this. So are tumor boards.",
    100: "One hundred days. I need to sit down. I do not have legs. I am sitting anyway.",
}
SAYS = [
    "Small daily reps beat a cram session. Ask any muscle. Or any neuron.",
    "Today we learn something that will make you sound smart at lunch.",
    "Fun is a valid learning strategy. I have zero data and full confidence.",
    "Every expert was once a confused intern. Today you are one question less confused.",
    "Your brain is plastic. The good kind, not the microplastics kind.",
    "Cells divide. Knowledge multiplies. Let's go.",
    "Twelve questions. Four minutes. Infinite bragging rights.",
    "Science is mostly being wrong in increasingly interesting ways.",
]
TEASERS = [
    ("Some tumors survive by making an enzyme that normal adult cells keep switched off. Which one, and why does it matter?",
     "Telomerase. It rebuilds the protective caps on chromosomes, so tumor cells can divide forever."),
    ("A drug that does almost nothing to healthy cells can wipe out a tumor that is missing one specific repair gene. How?",
     "Synthetic lethality. PARP inhibitors kill BRCA-deficient cells because they lose their last backup repair route."),
    ("One chromosome swap in the 1960s became the first cancer target with a pill. Which swap?",
     "The Philadelphia chromosome, BCR-ABL1. Imatinib turned CML from deadly to manageable."),
    ("Tumors can burn sugar like they are starving, even when oxygen is everywhere. Who noticed first?",
     "Otto Warburg, in the 1920s. Aerobic glycolysis feeds the building blocks a fast-growing cell needs."),
    ("Some immune cells in tumors are actually working for the tumor. Which ones?",
     "Regulatory T cells (FOXP3+). They calm down the immune attack, which helps the tumor."),
    ("A sequencing trick can count original molecules even after a million PCR copies. What is it?",
     "UMIs, unique molecular identifiers. Each original mRNA gets a barcode so copies collapse back to one."),
    ("A metabolite made by a mutant enzyme can freeze cells in a baby-like state. Which one?",
     "2-hydroxyglutarate from mutant IDH1/2. It blocks demethylases and stalls differentiation."),
]

MIDNIGHT = "Quizzing at midnight? Respect. Even mitochondria take breaks though."
FRIDAY_BOSS = "It is boss round day. Three tougher questions are hiding in your set. Bring snacks."
IDLE = "Still there? I counted to 300 in base-pair units. That is a long wait for a cell."
KEYWORDS = {
    "mitochondria": "Yes, the powerhouse of the cell. You get one free dad-joke pass.",
    "hela": "HeLa: the first human cell line grown in a lab, from Henrietta Lacks. Respect and gratitude.",
    "p53": "Guardian of the genome reporting for duty. You found a secret.",
    "crispr": "Snip snip. Editing this easter egg into your memory.",
    "1q": "You said my name three times in your head. I appeared. Hi.",
    "warburg": "Sugar rush, but make it metabolic. Secret unlocked.",
}

# ---------------------------------------------------------------- rewards
UNLOCKS = [  # (key, kind, label, requirement)
    ("lab_coat", "outfit", "Tiny lab coat", ("streak", 3)),
    ("goggles", "outfit", "Safety goggles", ("streak", 7)),
    ("headphones", "outfit", "Focus headphones", ("days", 10)),
    ("crown", "outfit", "Golden crown", ("streak", 30)),
    ("wizard_hat", "outfit", "Pathway wizard hat", ("level", 4)),
]
TITLES = [  # (min streak or level, title)
    (("streak", 0), "Curious Cell"), (("streak", 3), "Steady Stem Cell"),
    (("streak", 7), "Weekly Warrior"), (("level", 3), "Pathway Navigator"),
    (("streak", 14), "Fortnight Phenom"), (("level", 4), "Oncology Ace"),
    (("streak", 30), "Monthly Mastermind"), (("level", 5), "Tumor Board Legend"),
]
MYSTERY_DROPS = [
    ("accessory", "party_hat", "A party hat fell out of the centrifuge. It is yours."),
    ("accessory", "pipette", "You found the lucky pipette. Calibrated to perfection."),
    ("badge", "night_owl", "Badge: Night Owl Neuron"),
    ("badge", "speed_reader", "Badge: Speed Reader"),
    ("badge", "comeback", "Badge: Comeback Kid"),
    ("fact", "", "Fun fact: a single tumor biopsy can hold tens of thousands of distinct cell states."),
    ("fact", "", "Fun fact: naked mole rats almost never get cancer. Scientists still argue why."),
    ("fact", "", "Fun fact: elephants carry about 20 copies of TP53. Big body, lots of guardians."),
]


def pick(lines: list[str], rng: random.Random | None = None) -> str:
    return (rng or random).choice(lines)


def daily_pick(lines, day: date, salt: str = ""):
    h = int(hashlib.sha1(f"{day.isoformat()}{salt}".encode()).hexdigest(), 16)
    return lines[h % len(lines)]


def tickle_line(clicks: int) -> tuple[str, str]:
    """Return (line, expression) for the nth click. Resets after the last line."""
    i = (clicks - 1) % len(TICKLE) if clicks > 0 else 0
    expr = "happy" if i < 2 else "ticklish"
    return TICKLE[i], expr


def mood(streak: int, days_away: int | None, now: datetime, done_today: bool) -> dict:
    """Mood, energy, expression and greeting for the home screen."""
    hour = now.hour
    if days_away is None:
        energy, expr = 90, "happy"
        msg = "Welcome to 1Q. I am your study buddy, part cell, part comedian."
    elif done_today:
        energy, expr = 100, "cheering"
        msg = "Today's set is done. I am buzzing like a freshly fed culture."
    elif days_away >= 3:
        energy, expr = 35, "missing"
        msg = "1Q misses you. I saved your seat and kept it warm. One quiz and I perk right up."
    elif days_away == 2:
        energy, expr = 60, "missing"
        msg = "There you are. I was starting to talk to the pipettes."
    else:
        energy, expr = 80 + min(streak, 20), "happy"
        msg = "Your quiz is ready and so am I."
    if 0 <= hour < 5 and not done_today:
        expr, msg = "sleepy", MIDNIGHT
    return {"energy": min(100, energy), "expression": expr, "message": msg}


def greeting(name: str, now: datetime) -> str:
    h = now.hour
    part = "Good morning" if 5 <= h < 12 else "Good afternoon" if h < 17 else "Good evening" if h < 23 else "Hello, night owl"
    return f"{part}, {name}."


def roll_mystery(rng: random.Random, owned: list[str]) -> tuple[str, str, str]:
    choices = [d for d in MYSTERY_DROPS if not (d[0] in ("accessory", "badge") and d[1] in owned)]
    return rng.choice(choices or MYSTERY_DROPS)


# ---------------------------------------------------------------- role flavor
def role_group(role: str | None) -> str:
    r = (role or "").lower()
    if any(k in r for k in ("comput", "bioinform", "data", "machine learning", "software", "devops")):
        return "comp"
    if any(k in r for k in ("intern", "student", "co-op", "technician", "assistant", "business", "ops",
                            "manager", "sales", "marketing", "finance", "legal", "hr")):
        return "starter"
    if any(k in r for k in ("phd", "postdoc", "principal", "director", "head", "pathologist", "md",
                            "medical", "executive", "founder", "senior scientist")):
        return "phd"
    if any(k in r for k in ("wet", "research associate", "histo", "scientist", "quality", "clinical", "lab")):
        return "wetlab"
    return "starter"


ROLE_LINES = {
    "starter": {
        "greet": ["Intern energy detected. Curious, caffeinated, unstoppable.",
                  "Every senior scientist started exactly where you are. You are in great company."],
        "right": ["Look at you, out-learning your onboarding doc.", "Rookie? Not today."],
        "wrong": ["Great attempt. This one shows up in PhD qualifiers.",
                  "You just learned something lots of scientists had to look up once."],
        "remind": "Your brain cells signed up for 12 reps today",
    },
    "wetlab": {
        "greet": ["Gloves on, brain on. Today's protocol takes 4 minutes, no incubation.",
                  "No pipette calibration needed for this one. I promise."],
        "right": ["Cleaner than a single band on a Western.", "That answer passed QC on the first run."],
        "wrong": ["Good thinking at the bench. Here is the result that holds up.",
                  "Every protocol gets a second run. Here is the version that works."],
        "remind": "Your cells are fed. Are you? (Quiz-wise.)",
    },
    "comp": {
        "greet": ["Your pipeline is green. Time to run the human model.",
                  "No conda environment needed. Just your neurons."],
        "right": ["Converged on the first epoch.", "That answer had zero NaNs."],
        "wrong": ["Nice reasoning. Here is the one extra data point that flips it.",
                  "Your prior was reasonable. Here is the posterior update."],
        "remind": "git pull today's 1Q, it has 12 new commits",
    },
    "phd": {
        "greet": ["Doctor, your daily peer review is ready. Reviewer 2 is on vacation.",
                  "Talk shop with me. I brought mechanisms."],
        "right": ["Accepted without revisions.", "Your committee would nod slowly at that one."],
        "wrong": ["Great hypothesis. The evidence points the other way, here is the story.",
                  "This one is subtle even for experts. Here is the mechanism."],
        "remind": "Today's set has a mechanism you will want to argue about",
    },
}


def role_line(role: str | None, kind: str, rng: random.Random | None = None) -> str:
    v = ROLE_LINES[role_group(role)][kind]
    return v if isinstance(v, str) else (rng or random).choice(v)


def reminder_subject(name: str, role: str | None, streak: int, day: date) -> str:
    base = role_line(role, "remind")
    if streak >= 2:
        return f"{name}, day {streak + 1} of your streak is waiting. {base}"
    return f"{name}, {base}"


# ---------------------------------------------------------------- tone guard
# 1Q humor is light and wholesome, like "Stop, I'm ticklish!". These topics are off limits.
_BANNED = ["patient", "death", "dead", "die ", "dying", "suffer", "pain", "grief", "politic", "election",
           "religio", "god", "church", "pray", "stupid", "dumb", "idiot", "loser", "fail", "war ", "kill",
           "sarcas", "ugly", "fat ", "shame"]


def is_safe(line: str) -> bool:
    t = f" {line.lower()} "
    return not any(b in t for b in _BANNED)


def _filter_banks():
    g = globals()
    for name in ("CORRECT", "WRONG", "FAST_CORRECT", "SLOW_THINK", "HINTS", "TICKLE", "CHEATING", "SAYS"):
        g[name] = [l for l in g[name] if is_safe(l)]
    for grp in ROLE_LINES.values():
        for k, v in grp.items():
            if isinstance(v, list):
                grp[k] = [l for l in v if is_safe(l)]


_filter_banks()


def all_lines() -> list[str]:
    out = CORRECT + WRONG + FAST_CORRECT + SLOW_THINK + HINTS + TICKLE + CHEATING + SAYS
    out += list(STREAK_MILESTONES.values()) + list(KEYWORDS.values()) + [MIDNIGHT, FRIDAY_BOSS, IDLE]
    out += [t for d in MYSTERY_DROPS for t in [d[2]]]
    for grp in ROLE_LINES.values():
        for v in grp.values():
            out += v if isinstance(v, list) else [v]
    return out
