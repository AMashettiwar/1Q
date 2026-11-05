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


REACTIONS = {"cheering": "joy", "oops": "empathy", "thinking": "think", "sleepy": "sleep", "missing": "sleep",
             "ticklish": "shake", "suspicious": "squint", "happy": "idle"}


def svg(expression: str = "happy", accessory: str = "", energy: int = 100, size: int = 104,
        palette: tuple = ("#0f5257", "#f4efe4", "#a8874a"), react_id: int = 0) -> str:
    """1Q as layered parts so the front end can animate it: orbit, body (squash and stretch),
    face (tracks the pointer), eyes (blink), mouth (talks), a brass burst for joy and Zs for sleep."""
    body, eye, brass = palette
    e = expression if expression in _EYES else "happy"
    op = 0.62 + 0.38 * max(0, min(100, energy)) / 100
    fill = lambda t: t.replace("{eye}", eye).replace("{brass}", brass)
    gid = f"{abs(hash((body, size))) % 99991}"
    burst = "".join(
        f'<line x1="{60 + 48 * c:.1f}" y1="{60 + 48 * s_:.1f}" x2="{60 + 56 * c:.1f}" y2="{60 + 56 * s_:.1f}"/>'
        for c, s_ in [(1, 0), (.5, .866), (-.5, .866), (-1, 0), (-.5, -.866), (.5, -.866)])
    return (
        f'<svg class="oneq-avatar" data-react="{REACTIONS.get(e, "idle")}" data-rid="{react_id}" data-expr="{e}" '
        f'width="{size}" height="{size}" viewBox="-8 -14 136 140" role="img" aria-label="1Q, {e}" '
        f'xmlns="http://www.w3.org/2000/svg">'
        f'<ellipse class="m-shadow" cx="60" cy="116" rx="26" ry="3.5" fill="{body}" opacity=".16"/>'
        f'<g class="m-orbit"><ellipse cx="60" cy="60" rx="56" ry="20" fill="none" stroke="{brass}" stroke-width="1.2" '
        f'stroke-opacity=".6" transform="rotate(-18 60 60)"/><circle cx="113" cy="46" r="2.6" fill="{brass}"/></g>'
        f'<defs><radialGradient id="oqL{gid}" cx=".32" cy=".26" r=".75"><stop offset="0" stop-color="#fff" stop-opacity=".30"/>'
        f'<stop offset=".55" stop-color="#fff" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="oqD{gid}" cx=".62" cy=".78" r=".7"><stop offset=".35" stop-color="#000" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="#000" stop-opacity=".30"/></radialGradient></defs>'
        f'<g class="m-rig"><g class="m-body">'
        f'<g class="m-hand l"><ellipse cx="22" cy="74" rx="8" ry="7" fill="{body}"/><ellipse cx="22" cy="74" rx="8" ry="7" fill="url(#oqL{gid})"/>'
        f'<ellipse cx="22" cy="74" rx="8" ry="7" fill="none" stroke="{brass}" stroke-opacity=".5"/></g>'
        f'<g class="m-hand r"><ellipse cx="98" cy="74" rx="8" ry="7" fill="{body}"/><ellipse cx="98" cy="74" rx="8" ry="7" fill="url(#oqL{gid})"/>'
        f'<ellipse cx="98" cy="74" rx="8" ry="7" fill="none" stroke="{brass}" stroke-opacity=".5"/></g>'
        f'<circle cx="60" cy="60" r="40" fill="{body}" opacity="{op:.2f}"/>'
        f'<circle cx="60" cy="60" r="40" fill="url(#oqD{gid})"/><circle cx="60" cy="60" r="40" fill="url(#oqL{gid})"/>'
        f'<g fill="{eye}" opacity=".10"><circle cx="40" cy="80" r="2.2"/><circle cx="84" cy="84" r="1.6"/><circle cx="76" cy="90" r="2.6"/>'
        f'<circle cx="36" cy="58" r="1.4"/></g>'
        f'<path d="M88 78 a40 40 0 0 1 -30 21" fill="none" stroke="#fff" stroke-opacity=".28" stroke-width="2" stroke-linecap="round"/>'
        f'<circle cx="60" cy="60" r="40" fill="none" stroke="{brass}" stroke-opacity=".45"/>'
        f'<ellipse cx="45" cy="36" rx="9" ry="5.5" fill="#fff" opacity=".32" transform="rotate(-30 45 36)"/>'
        f'<circle cx="54" cy="31" r="2" fill="#fff" opacity=".5"/>'
        f'<g class="m-face" stroke="{eye}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round">'
        f'<g class="m-eyes">{fill(_EYES[e])}</g><g class="m-mouth">{fill(_MOUTH[e])}</g>'
        f'<g class="m-cheeks" stroke="none" fill="{brass}" opacity="0"><circle cx="38" cy="66" r="4"/><circle cx="82" cy="66" r="4"/></g></g>'
        f'{fill(ACCESSORIES.get(accessory, ""))}</g></g>'
        f'<g class="m-burst" stroke="{brass}" stroke-width="2.2" stroke-linecap="round">{burst}</g>'
        f'<g class="m-z" fill="{brass}" font-family="Fraunces, Georgia, serif" font-size="14">'
        f'<text x="94" y="20">z</text><text x="104" y="6" font-size="10">z</text></g>'
        f'</svg>'
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
    if h < 5 or h >= 23:
        part = "Hello, night owl"
    else:
        part = "Good morning" if h < 12 else "Good afternoon" if h < 17 else "Good evening"
    return f"{part}, {name}."


def roll_mystery(rng: random.Random, owned: list[str]) -> tuple[str, str, str]:
    choices = [d for d in MYSTERY_DROPS if not (d[0] in ("accessory", "badge") and d[1] in owned)]
    return rng.choice(choices or MYSTERY_DROPS)


# ---------------------------------------------------------------- role flavor
def role_group(role: str | None) -> str:
    """Line-bank key for any role, via the generic profile in persona.py."""
    from . import persona
    return persona.bucket(persona.profile(role))




ROLE_LINES = {
    "intern": {
        "greet": ["Intern energy detected. Curious, caffeinated, unstoppable.",
                  "Every senior scientist started exactly where you are. You are in great company."],
        "first": "First day with me? I will go easy. Mostly. Cells have a sense of humor.",
        "back": "Back again! At this rate you will be mentoring the next intern.",
        "night": "Late-night intern study session? Legendary. I brought imaginary snacks.",
        "streak": "{n} days straight. Your onboarding doc is getting jealous.",
        "right": ["Look at you, out-learning your onboarding doc.", "Rookie? Not today."],
        "wrong": ["Great attempt. This one shows up in PhD qualifiers.",
                  "You just learned something lots of scientists had to look up once."],
        "remind": "Your brain cells signed up for 12 reps today",
    },
    "tech": {
        "greet": ["Build passed. Now let's compile some biology.",
                  "Think of a cell as a very old codebase with no comments. Let's read it."],
        "first": "Hello, engineer. DNA is just a 4-letter encoding with very strict code review.",
        "back": "Welcome back. Your knowledge cache is warm and ready.",
        "night": "Late-night deploy and a late-night quiz? Respect. Hydrate like a well-tuned server.",
        "streak": "{n}-day streak. That is better uptime than most staging servers.",
        "right": ["All tests green.", "Merged on the first review."],
        "wrong": ["Nice reasoning. Here is the one config flag that flips it.",
                  "Edge case found. Here is the patch."],
        "remind": "git pull today's 1Q, it has 12 new commits",
    },
    "wetlab": {
        "greet": ["Gloves on, brain on. Today's protocol takes 4 minutes, no incubation.",
                  "No pipette calibration needed for this one. I promise."],
        "first": "Welcome to the bench, digital edition. No gloves required.",
        "back": "You came back! Like a perfectly reproducible result.",
        "night": "Night shift at the bench? Your cells are asleep. Your brain, apparently, is not.",
        "streak": "{n} days in a row. More consistent than any incubator I know.",
        "right": ["Cleaner than a single band on a Western.", "That answer passed QC on the first run."],
        "wrong": ["Good thinking at the bench. Here is the result that holds up.",
                  "Every protocol gets a second run. Here is the version that works."],
        "remind": "Your cells are fed. Are you? (Quiz-wise.)",
    },
    "comp": {
        "greet": ["Your pipeline is green. Time to run the human model.",
                  "No conda environment needed. Just your neurons."],
        "first": "New sample loaded. Let's estimate your priors.",
        "back": "Welcome back. Your model has been retrained on fresh data.",
        "night": "Jobs queued, cluster humming, and you are here with me. Nice.",
        "streak": "{n}-day streak. Statistically significant.",
        "right": ["Converged on the first epoch.", "That answer had zero NaNs."],
        "wrong": ["Nice reasoning. Here is the one extra data point that flips it.",
                  "Your prior was reasonable. Here is the posterior update."],
        "remind": "git pull today's 1Q, it has 12 new commits",
    },
    "phd": {
        "greet": ["Doctor, your daily peer review is ready. Reviewer 2 is on vacation.",
                  "Talk shop with me. I brought mechanisms."],
        "first": "Doctor, welcome. I skipped the textbook chapter and went straight to mechanisms.",
        "back": "Welcome back, Doctor. Your committee would approve of this consistency.",
        "night": "Midnight science, the classic PhD move. I will keep the questions sharp.",
        "streak": "{n} days straight. That is a publishable trend.",
        "right": ["Accepted without revisions.", "Your committee would nod slowly at that one."],
        "wrong": ["Great hypothesis. The evidence points the other way, here is the story.",
                  "This one is subtle even for experts. Here is the mechanism."],
        "remind": "Today's set has a mechanism you will want to argue about",
    },
    "cto": {
        "greet": ["CTO on deck. Today's roadmap: twelve questions, zero tech debt.",
                  "Let's architect some biology. I promise the diagrams are cuter."],
        "first": "Welcome, CTO. Think of me as a very small platform team for your science knowledge.",
        "back": "Back for another sprint. Velocity looks great.",
        "night": "Late-night architecture review? I will keep it to twelve tickets.",
        "streak": "{n}-day streak. Your learning platform has excellent uptime.",
        "right": ["Approved at architecture review.", "Scales beautifully."],
        "wrong": ["Solid instinct. Here is the biology behind the curtain.",
                  "Good call to ask. Here is the systems view."],
        "remind": "Twelve tickets in today's sprint. All small.",
    },
    "ceo": {
        "greet": ["Big picture today: twelve questions that make every board slide sharper.",
                  "Executive summary: you are about to understand the science even better."],
        "first": "Welcome, chief. Think of today as a four-minute science briefing before the board meeting.",
        "back": "Welcome back. Your strategy just gained a stronger science foundation.",
        "night": "Burning the midnight oil? Quick science briefing, then rest. Doctor 1Q's orders.",
        "streak": "{n}-day streak. That is leadership by example.",
        "right": ["That is a board-ready answer.", "Investors would love that clarity."],
        "wrong": ["Great question to get wrong now, not in a pitch. Here is the story.",
                  "Here is the one-slide version of the science."],
        "remind": "Your 4-minute science briefing is ready",
    },
    "clinical": {
        "greet": ["Rounds with me take four minutes and nobody pages you.", "Today's case conference: twelve quick cases."],
        "first": "Welcome! I speak fluent biomarker and a little bit of pun.",
        "back": "Back for another round. Your clinical instincts are warming up.",
        "night": "Late shift? I will keep the questions crisp and kind.",
        "streak": "{n} days straight. Textbook adherence to the protocol.",
        "right": ["Spot on, like a perfect stain.", "Diagnosis: sharp."],
        "wrong": ["Reasonable call. Here is the evidence that tips it.", "Good differential. Here is the deciding clue."],
        "remind": "Twelve quick cases are waiting",
    },
    "regulatory": {
        "greet": ["Today's submission: twelve questions, zero redlines.", "Checklist ready. Every box is a fun fact."],
        "first": "Welcome! I come pre-validated and fully documented.",
        "back": "Welcome back. Audit trail shows excellent attendance.",
        "night": "Late-night review? I promise no surprise findings.",
        "streak": "{n}-day streak. That is fully compliant consistency.",
        "right": ["Approved on first review.", "That answer would sail through any audit."],
        "wrong": ["Good catch to make here, not in a submission. Here is the detail.", "Minor finding. Here is the fix."],
        "remind": "Your daily SOP: twelve questions",
    },
    "business": {
        "greet": ["Today's pitch: twelve questions that make customer chats sparkle.", "Quick science, big talking points."],
        "first": "Welcome! I turn cell biology into stories customers love.",
        "back": "Welcome back. Your science storytelling just leveled up.",
        "night": "Late night prep? I will keep it slide-sized.",
        "streak": "{n}-day streak. That is a great quarter.",
        "right": ["Closed with confidence.", "That is a talking point for your next meeting."],
        "wrong": ["Great one to learn before a customer asks. Here is the story.", "Here is the one-slide version."],
        "remind": "Twelve talking points are waiting",
    },
    "ops": {
        "greet": ["Inventory check: twelve fresh questions in stock.", "Everything ships on time today, including your quiz."],
        "first": "Welcome! I keep things organized, like a perfectly labeled freezer box.",
        "back": "Welcome back. Your knowledge inventory is restocked.",
        "night": "Night shift logistics? Twelve small packages, then rest.",
        "streak": "{n} days on schedule. Flawless logistics.",
        "right": ["Delivered on time.", "Perfectly filed."],
        "wrong": ["Good instinct. Here is the label that goes on this one.", "Small reroute. Here is the right shelf."],
        "remind": "Twelve questions, delivered fresh",
    },
    "starter": {
        "greet": ["Curious minds welcome. Twelve questions, four minutes, lots of fun.",
                  "Every expert started exactly where you are. You are in great company."],
        "first": "Welcome! I am 1Q, part cell, part comedian. Let's learn something cool.",
        "back": "Welcome back! I saved your seat.",
        "night": "Quizzing at midnight? Respect. Even mitochondria take breaks though.",
        "streak": "{n} days in a row. I am doing a tiny cartwheel.",
        "right": ["Look at you go.", "Rookie? Not today."],
        "wrong": ["Great attempt. This one trips up lots of scientists.",
                  "You just learned something lots of scientists had to look up once."],
        "remind": "Your brain cells signed up for 12 reps today",
    },
}

LOGIN_LINES = {
    "night": ["Hello, night owl. I am awake too. Cells never fully sleep.",
              "Late shift? Sign in and I will keep it short and sweet."],
    "morning": ["Good morning! I already had my coffee. It was glucose.",
                "Morning! My mitochondria are fully charged."],
    "afternoon": ["Afternoon slump? Twelve questions beat a third coffee.",
                  "Perfect timing. Post-lunch neurons are my favorite kind."],
    "evening": ["Evening! Let's end the day a little smarter.",
                "Golden hour for learning. I made it up, but it sounds right."],
}
LOGIN_POKES = ["Hey! That tickles.", "I am a cell, not a button. Okay, I am also a button.",
               "Type your email, I promise I will not read it out loud.", "Stop, I'm ticklish!",
               "Boop received. Booping back.", "Careful, I divide when I laugh."]


def daypart(now: datetime) -> str:
    h = now.hour
    return "night" if h < 5 or h >= 23 else "morning" if h < 12 else "afternoon" if h < 17 else "evening"


def login_line(now: datetime, known: dict | None = None) -> str:
    """Mascot line on the login screen. known: {name, role, streak} for a returning email."""
    if known:
        g = role_group(known.get("role"))
        st = known.get("streak") or 0
        tail = ROLE_LINES[g]["streak"].format(n=st) if st >= 2 else ROLE_LINES[g]["back"]
        return f"Oh hi, {known.get('name') or 'friend'}! {tail}"
    return LOGIN_LINES[daypart(now)][now.toordinal() % 2]


def persona_line(role: str | None, now: datetime, streak: int, first_time: bool, days_away: int | None) -> str:
    """Home greeting tuned by persona, first visit vs returning, time of day and streak."""
    from . import persona
    p = persona.profile(role)
    L = ROLE_LINES[persona.bucket(p)]
    if first_time:
        return f"{L['first']} {persona.SENIORITY_TAGS[p['seniority']]}"
    if daypart(now) == "night":
        return L["night"]
    if streak >= 2:
        return L["streak"].format(n=streak)
    if days_away is not None and days_away >= 1:
        return L["back"]
    return L["greet"][now.toordinal() % len(L["greet"])]


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


_CHAT_BANNED = ["politic", "election", "religio", "church", "pray", "stupid", "dumb", "idiot", "loser", "ugly", "shame"]


def is_safe_chat(text: str) -> bool:
    """Chat answers may discuss science plainly (patients, cell death); only block the off-limits topics and insults."""
    t = f" {text.lower()} "
    return not any(b in t for b in _CHAT_BANNED)


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
    out = ASK_LINES + [l for v in TOPIC_QUIPS.values() for l in v] + list(ROLE_ASK.values())
    out += CORRECT + WRONG + FAST_CORRECT + SLOW_THINK + HINTS + TICKLE + CHEATING + SAYS
    out += list(STREAK_MILESTONES.values()) + list(KEYWORDS.values()) + [MIDNIGHT, FRIDAY_BOSS, IDLE]
    out += [t for d in MYSTERY_DROPS for t in [d[2]]]
    for grp in ROLE_LINES.values():
        for v in grp.values():
            out += v if isinstance(v, list) else [v]
    for v in LOGIN_LINES.values():
        out += v
    return out + LOGIN_POKES


# ---------------------------------------------------------------- live role reaction (login / first run)
# 1Q reacts to whatever title someone types. Keyword rules only (instant, no LLM), so it also runs in the browser.
ROLE_REACT = {
    "ceo": ("A CEO! Twelve questions, zero board slides. Deal?", "cheering"),
    "cto": ("A CTO! Biology is the oldest tech stack. Let's read its source code.", "cheering"),
    "intern": ("An intern! Best title for learning. I'll start friendly and level up with you.", "happy"),
    "executive": ("A leader! I'll keep it crisp and strategic. Like a good memo.", "cheering"),
    "regulatory": ("Regulatory! Every answer I give comes with a paper trail. Promise.", "happy"),
    "clinical": ("Clinical brain detected. I'll bring the mechanisms, you bring the instincts.", "happy"),
    "computational": ("A data person! My priors just updated in your favor.", "happy"),
    "wet-lab": ("Bench scientist! I can smell the 70% ethanol from here. Respectfully.", "happy"),
    "engineering": ("An engineer! Think of a cell as legacy code with amazing uptime.", "happy"),
    "science": ("A fellow scientist. I'll skip the warm-up and go straight to mechanisms.", "cheering"),
    "operations": ("Ops! The real reason the freezers stay cold. Huge respect.", "happy"),
    "business": ("Business side! I'll translate the biology into plain, useful English.", "happy"),
    "general": ("Nice to meet you! I'll start gentle and grow with you.", "happy"),
}
ROLE_TYPING = ("Ooh, typing… I'm guessing scientist. Or wizard.", "thinking")


def role_reaction(role: str | None) -> tuple[str, str]:
    """(line, expression) for a typed title, from keyword rules only."""
    from . import persona
    r = f" {(role or '').strip().lower()} "
    if not r.strip():
        return ("", "happy")
    if any(k in r for k in (" ceo ", "chief executive", "founder")):
        return ROLE_REACT["ceo"]
    if any(k in r for k in (" cto ", "chief technology")):
        return ROLE_REACT["cto"]
    if any(k in r for k in ("intern", "student", "trainee")):
        return ROLE_REACT["intern"]
    fn = persona._rule(r, persona.FUNCTION_RULES) or "general"
    return ROLE_REACT[fn]


def role_unmatched(role: str | None) -> bool:
    """True when no keyword rule knows this title, so the mascot should repeat it back."""
    from . import persona
    r = f" {(role or '').strip().lower()} "
    return not (any(k in r for k in (" ceo ", "chief executive", "founder", " cto ", "chief technology", "intern", "student", "trainee"))
                or persona._rule(r, persona.FUNCTION_RULES))


def role_react_js_rules() -> list:
    """Same rules, serialised for the browser: [[keywords], line, expression] in priority order."""
    from . import persona
    rules = [[[" ceo ", "chief executive", "founder"], *ROLE_REACT["ceo"]],
             [[" cto ", "chief technology"], *ROLE_REACT["cto"]],
             [["intern", "student", "trainee"], *ROLE_REACT["intern"]]]
    rules += [[list(kws), *ROLE_REACT[fn]] for fn, kws in persona.FUNCTION_RULES]
    return rules


# ---------------------------------------------------------------- the five mascots
# Each user picks a character (User.mascot); every character shares the same role-aware line banks.
def mascot_key(k: str | None) -> str:
    from . import mascots
    return mascots.key(k)


def react_line(role: str | None, kind: str, mascot: str | None = None, rng: random.Random | None = None) -> str:
    """Quiz reaction from the shared role-adaptive banks (same for every mascot)."""
    r = rng or random
    return role_line(role, kind, r) if r.random() < .6 else pick(CORRECT if kind == "right" else WRONG, r)


def render(expression: str = "happy", accessory: str = "", energy: int = 100, mascot: str | None = None,
           size: int | None = None, **_) -> str:
    """The user's chosen character in the given expression."""
    from . import mascots
    return mascots.svg(mascot, expression, size)


# ---------------------------------------------------------------- pre-question lines (shared by every mascot)
ASK_LINES = [
    "New question, fresh cells. I am holding my breath. I do not have lungs, so this is easy.",
    "Read it twice, answer once. That is my whole strategy. And my only strategy.",
    "This one looks innocent. Questions are like cells: always check the receptors.",
    "Take your time. The clock is mostly decorative. Like my eyebrows.",
    "I know the answer. I am not telling. My lips are sealed. My membrane too.",
    "Ooh, a good one. I would lean in, but I am already leaning.",
    "Trust your first instinct. Then check it, like a good control.",
    "Fun fact: I get ticklish when you hover over the right answer. Just kidding. Mostly.",
    "Deep breath. You have seen harder ones before breakfast.",
    "Brain warmed up? Mine is doing little stretches.",
]

TOPIC_QUIPS = {
    "hallmarks": ["Hallmarks time. Cancer cells have a whole checklist. Overachievers, honestly.",
                  "Ten hallmarks, one question. You only need the one."],
    "oncogenes": ["Oncogenes are the gas pedal, suppressors the brakes. Pick your pedal.",
                  "p53 is watching this one closely. It watches everything closely."],
    "dna_repair": ["DNA repair question. Bring your tiny molecular toolbox.",
                   "Somewhere a repair enzyme is clocking in for its shift. Let's join it."],
    "immunotherapy": ["Immune system question. T cells love a good mystery.",
                      "Checkpoints ahead. Show your badge to the T cell."],
    "genomics": ["Genomics! Three billion letters and we only need the right one.",
                 "Somewhere a sequencer just beeped in approval."],
    "single_cell": ["Single-cell question. Every cell gets its own spotlight today.",
                    "One cell at a time. Very civilized."],
    "spatial": ["Spatial biology: where you are matters. Location, location, location.",
                "Cells have neighbours too. Some of them are chatty."],
    "drug_dev": ["Drug development question. Lock and key, but tinier.",
                 "Targeted therapy: aim small, think big."],
    "trials": ["Clinical trials question. Randomize your nerves and go.",
               "Phases, arms, endpoints. Very organized. I approve."],
    "biomarkers": ["Biomarker time. Little molecular breadcrumbs, waiting to be read.",
                   "Biomarkers are clues. You are the detective."],
    "tme": ["Tumor microenvironment: it is a whole neighbourhood in there.",
            "The neighbours always know something. Ask the fibroblasts."],
    "epigenetics": ["Epigenetics: same script, different highlighter.",
                    "Methyl groups are tiny sticky notes. Read them carefully."],
    "metastasis": ["Invasion and metastasis. Cells with a travel itinerary.",
                   "Some cells pack a suitcase. This question is about the packing list."],
    "pathology": ["Pathology and imaging. Squint like a microscope. Nicely.",
                  "Pink, purple, patterns. Pathologists see poetry in there."],
    "radiation": ["Radiation and surgery: precision is the whole game.",
                  "Steady hands, steady beam, steady you."],
    "epidemiology": ["Screening and prevention. Big numbers, big picture.",
                     "Epidemiology: where one decimal point can tell a story."],
}

ROLE_ASK = {
    "intern": "Pro tip from your favourite cell: elimination works wonders.",
    "tech": "Treat it like a bug report: read the error, then the stack.",
    "wetlab": "Think bench-side: what would the gel show?",
    "comp": "Think of it as a feature you need to explain to a model.",
    "phd": "Mechanism first, memory second. You know the drill.",
    "cto": "Systems thinking applies to cells too. Find the bottleneck.",
    "ceo": "One-line answer, big-picture reason. Your favourite format.",
    "clinical": "Bench to bedside in one click. You know this road.",
    "regulatory": "Read it like a label: every word is there for a reason.",
    "business": "Cut through the jargon. The answer is usually the plain one.",
    "ops": "Process of elimination is still a process. Run it.",
    "starter": "No pressure. Every answer teaches me something too.",
}


def ask_line(role: str | None, subtopic: str | None, rng: random.Random | None = None) -> str:
    """Witty, wholesome line shown before a question: topic quip, role tip or a general one-liner."""
    r = rng or random
    roll = r.random()
    if subtopic in TOPIC_QUIPS and roll < .55:
        out = r.choice(TOPIC_QUIPS[subtopic])
    elif roll < .75:
        out = ROLE_ASK.get(role_group(role), ROLE_ASK["starter"])
    else:
        out = r.choice(ASK_LINES)
    return out if is_safe(out) else r.choice([l for l in ASK_LINES if is_safe(l)])


# extra reactions in the ticklish style
CORRECT += [
    "Nailed it! I would high-five you but I am mostly cytoplasm.",
    "Correct! I just did a little wiggle. You missed it. It was majestic.",
    "Yes! That answer had excellent posture.",
    "Bullseye. My mitochondria are throwing a tiny party.",
]
WRONG += [
    "Close one! That option was a very convincing decoy.",
    "Not this time, but now you know it forever. That is how memory works.",
    "Plot twist! The explanation below is genuinely fun, I promise.",
    "Tricky one. Even the textbooks had a draft two of this.",
]
_filter_banks()


# ---- wider shared banks (same for every mascot) so lines rarely repeat
_MORE_QUIPS = {
    "hallmarks": ["Ten hallmarks, one question. Pick your favourite child.", "Hanahan and Weinberg would want you to read every option."],
    "oncogenes": ["Gas pedal or brake? Classic oncogene energy.", "One mutation to rule them all? Let us see."],
    "dna_repair": ["Repair crews on standby. Read carefully, fix later.", "Mismatch spotted? So far, just in the options."],
    "immunotherapy": ["T cells are watching. No pressure.", "Checkpoint ahead. Show your badge, I mean your answer."],
    "genomics": ["Reading the genome one option at a time.", "Variant calling, but make it multiple choice."],
    "single_cell": ["Every cell has a story. This one has four endings.", "Cluster your thoughts, then pick."],
    "spatial": ["Location, location, location. Even for cells.", "Where it sits matters. So does what you pick."],
    "drug_dev": ["From bench to bedside in one click.", "Phase one: read. Phase two: decide."],
    "trials": ["Randomise your doubts, not your answer.", "Primary endpoint: you, getting this right."],
    "biomarkers": ["A good biomarker is specific. So is a good guess.", "Sensitivity check: how sure are you?"],
    "tme": ["The neighbourhood matters. Even in tumours.", "Stroma, immune cells, vessels. Busy block."],
    "epigenetics": ["Same DNA, different mood. Epigenetics, everyone.", "Methyl groups optional. Focus required."],
    "metastasis": ["Cells on the move. Stay put and think.", "Seed and soil, but make it a quiz."],
    "pathology": ["Zoom in. The answer is in the details.", "H and E stands for Highly Educated guess."],
    "radiation": ["Fractionate your thinking. Small steps.", "Dose of facts incoming."],
    "epidemiology": ["Correlation is not causation. Your answer is, though.", "Population-level thinking, single-click answer."],
}
for _k, _v in _MORE_QUIPS.items():
    TOPIC_QUIPS.setdefault(_k, []).extend(_v)
ASK_LINES += [
    "Read twice, click once. My favourite protocol.", "I believe in you more than I believe in p-values.",
    "Take a breath. The question is not going anywhere.", "This one is a good one. I picked it myself. Kind of.",
    "Trust your first instinct, then check it.", "Fun fact: you are already better at this than yesterday.",
    "Coffee optional. Curiosity required.", "Four options, one winner, zero judgement.",
    "I am cheering quietly so you can think.", "Smart people pause here. You are smart.",
]
HINTS += [
    "Rule out the option that sounds too absolute.", "Think about which one breaks the pattern.",
    "Ask what the mechanism actually needs.", "Two options can sound alike. Spot the difference.",
    "Picture the pathway step by step.", "The textbook answer is usually the simple one.",
]
CORRECT += [
    "Clean result. Reviewer two has no notes.", "That answer just got published in my heart.",
    "Right on. You make this look easy.", "Correct. I am doing a tiny happy dance.",
]
WRONG += [
    "Close one. Now you will never forget it.", "Not this time, but the explanation is a good read.",
    "Every expert got this wrong once. Welcome to the club.", "Plot twist. Let us see why.",
]
