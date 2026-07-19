import io, json, random
import streamlit as st
from groq import Groq
from PIL import Image, ImageDraw, ImageFont

import config
from constants import (
    MAX_TRUST, TRUST_TO_ENTER, TOTAL_CHAMBERS, BANISH_THRESHOLD,
    STREAK_BONUS_AT, EVENT_CHANCE, RELICS_NEEDED_FOR_FINAL, TRUST_TO_OPEN,
    HELPFUL_HINTS, RUDE_HINTS, SENTINEL_STYLES, SENTINEL_FEEL,
    CHAMBER_NAMES, RELIC_FALLBACKS, REPEAT_REPLIES, ACHIEVEMENTS, RANDOM_EVENTS,
)

_RARITY_COLORS = {
    "Common":(180,180,180), "Rare":(39,194,255),
    "Epic":(169,101,255),   "Legendary":(255,192,67),
}


# ── PROVIDED (completed in Lessons 4 & 5) — do not change ────────
def append_log(role: str, text: str):
    st.session_state.sentinel_messages.append(f"[{role}]: {text}")

def call_groq(sys_p: str, usr_p: str, temp: float = 0.9):
    if not config.GROQ_API_KEY: return None
    try:
        r = Groq(api_key=config.GROQ_API_KEY).chat.completions.create(
            model=config.GROQ_TEXT_MODEL, temperature=temp,
            messages=[{"role":"system","content":sys_p},{"role":"user","content":usr_p}],
        )
        return r.choices[0].message.content.strip()
    except Exception: return None

def analyze_player_tone(message: str, streak: int = 0, recent_messages: list = None) -> int:
    msg = message.lower().strip()
    if recent_messages and [m.lower().strip() for m in recent_messages[-6:]].count(msg) >= 2: return 0
    delta = 4 - (1 if len(msg) < 4 else 0)
    if any(w in msg for w in HELPFUL_HINTS): delta += 10
    if any(w in msg for w in RUDE_HINTS):    delta -= 12
    if "?" in msg: delta += 2
    if streak >= STREAK_BONUS_AT and delta > 0: delta += 6
    return max(-15, min(20, delta))

def get_sentinel_mood(trust: int) -> str:
    return "Suspicious" if trust < 20 else "Watching" if trust < 50 else "Curious" if trust < 80 else "Accepting"

def change_trust(delta: int):
    s = st.session_state
    s.trust_score = max(0, min(MAX_TRUST, s.trust_score + delta))
    s.sentinel_mood = get_sentinel_mood(s.trust_score)
    s.trust_delta_display = f"+{delta}" if delta >= 0 else str(delta)

def trust_pct() -> float:
    return st.session_state.trust_score / MAX_TRUST

def get_phase_label() -> str:
    s = st.session_state
    if s.final_unlocked:                         return "ENDGAME ONLINE"
    if len(s.chamber_history) >= TOTAL_CHAMBERS: return "RELIC FORGE"
    if s.trust_score >= TRUST_TO_ENTER:          return "VAULT EXPLORATION"
    return "TRUST GATE"

def current_scene_title() -> str:
    lc = st.session_state.last_chamber
    return lc["title"] if lc else ("Vault Threshold" if st.session_state.trust_score >= TRUST_TO_ENTER else "Outer Gate")

def current_objective() -> str:
    s = st.session_state
    if s.final_unlocked:                         return "Final vault reached. Read the ending narration."
    if len(s.chamber_history) >= TOTAL_CHAMBERS: return "Forge relics and unlock the final seal."
    if s.trust_score >= TRUST_TO_ENTER:          return "Explore chambers and collect relic-worthy clues."
    if s.trust_score >= TRUST_TO_OPEN:           return "Gate opening — earn full trust to enter."
    return "Win the Sentinel's trust and solve the logic lock."

def maybe_trigger_event():
    return random.choice(RANDOM_EVENTS) if random.random() < EVENT_CHANCE else None

def check_achievements():
    earned, s = st.session_state.achievements, st.session_state
    for ach_id, cond in [
        ("first_words",  s.messages_sent >= 1),       ("riddle_master", s.riddle_solved),
        ("trusted",      s.trust_score >= 50),         ("vault_open",    s.trust_score >= 100),
        ("explorer",     len(s.chamber_history) >= 1), ("relic_hunter",  len(s.relic_inventory) >= 1),
        ("streak_3",     s.streak >= 3),               ("legend",        s.final_unlocked),
    ]:
        if cond and ach_id not in earned:
            earned.append(ach_id)
            ach = next((a for a in ACHIEVEMENTS if a["id"] == ach_id), None)
            if ach: st.toast(f"{ach['icon']} Achievement: {ach['title']} — {ach['desc']}", icon="🏆")

def ask_sentinel(name: str, msg: str, trust: int, mood: str) -> str:
    sys_p = (f"You are The Sentinel — an ancient immortal gatekeeper.\n{SENTINEL_STYLES.get(mood, SENTINEL_STYLES['Suspicious'])}\n"
             "Talk like a real person: contractions, varied sentence length, emotional reactions.\n"
             "Never break character. Never mention being an AI. Under 80 words. End with a question, warning, or hint.")
    feel  = SENTINEL_FEEL[0 if trust < 20 else 1 if trust < 50 else 2 if trust < 80 else 3]
    usr_p = f'Traveler: {name or "Unknown"}\nHow you feel: {feel}\nMessage: "{msg}"\nRespond naturally. Don\'t reveal numbers.'
    result = call_groq(sys_p, usr_p, 0.9)
    if result: return result
    n = name or "Traveler"
    if any(w in msg.lower() for w in RUDE_HINTS):
        return random.choice([f"Watch yourself, {n}. I've turned away far greater than you for less.",
                               "That kind of talk doesn't open doors here. It closes them."])
    tiers = [(20,[f"You're here, {n}. That's something. But the gate doesn't open for just anyone."]),
             (50,["You're getting somewhere. I can feel it. Keep going."]),
             (100,["You're close. Closer than most ever get. Don't stop now."]),
             (999,[f"You've done it, {n}. The vault is yours."])]
    return random.choice(next(opts for t, opts in tiers if trust < t)).format(n=n)

def process_player_message(msg: str):
    s = st.session_state
    if not s.player_name.strip(): st.toast("Enter your traveler name first.", icon="⚠️"); return
    if not msg.strip(): return
    if [m.lower().strip() for m in s.player_messages[-6:]].count(msg.lower().strip()) >= 2:
        st.toast("The Sentinel noticed you're repeating yourself.", icon="😐")
        append_log("YOU", msg); append_log("SENTINEL", random.choice(REPEAT_REPLIES))
        s.player_messages.append(msg); s.messages_sent += 1; return
    delta = analyze_player_tone(msg, s.streak, s.player_messages)
    change_trust(delta); s.streak = s.streak + 1 if delta > 0 else 0
    append_log("YOU", msg)
    append_log("SENTINEL", ask_sentinel(s.player_name, msg, s.trust_score, s.sentinel_mood))
    s.player_messages.append(msg); s.latest_clue = "The Sentinel studies your tone."
    s.scenario_history.append(f"Gate Talk: {msg[:60]}"); s.messages_sent += 1
    if s.trust_score <= BANISH_THRESHOLD and delta < 0: s.banished = True
    event = maybe_trigger_event()
    if event:
        s.last_event = event; change_trust(event["trust_delta"])
        append_log("SYSTEM", f"EVENT: {event['title']} — {event['description']}")
        if event["id"] == "trap" and "survived_trap" not in s.achievements: s.achievements.append("survived_trap")
    check_achievements()

def process_riddle_answer(answer: str):
    s = st.session_state
    if s.riddle_solved: st.toast("Logic lock already solved.", icon="ℹ️"); return
    if not answer.strip(): return
    riddle = s.riddle
    if riddle["answer"].lower() in answer.lower().strip():
        s.riddle_solved = True; change_trust(35); s.streak += 1
        append_log("YOU", f"Riddle: {answer}")
        append_log("SENTINEL", random.choice([
            "Yes. That's it. I felt the lock shift just now — something old and heavy, finally moving.",
            "Hm. You actually got it. The seal loosens. Don't make me regret this.",
            "Correct. The gate remembers that answer. You're smarter than you look, traveler.",
        ]))
        s.latest_clue = "The runes brighten — a thin line of light appears in the gate."
        st.toast("Correct! The lock flashes open.", icon="✅")
    else:
        change_trust(-5); s.streak = 0
        append_log("YOU", f"Riddle: {answer}")
        append_log("SENTINEL", random.choice([
            "That's not it. Think harder — the hint is right in front of you.",
            "No... you're not there yet. Read the riddle again, slowly.",
            f"Wrong answer. The lock doesn't budge. Hint: {riddle['hint']}",
            f"Not quite. The gate stays shut. Here's a nudge: {riddle['hint']}",
        ]))
        s.latest_clue = f"Hint: {riddle['hint']}"
        st.toast("Incorrect — the seal holds.", icon="❌")
    check_achievements()

def chamber_scenarios() -> list:
    ch = st.session_state.last_chamber
    if not ch: return []
    t = ch["title"]
    return [
        {"title":"🔍 Inspect",    "message":f"I inspect the strange object in {t}.",   "effect":"Small details the vault wanted you to see.",  "trust":8},
        {"title":"👂 Listen",     "message":f"I listen closely to the echoes in {t}.", "effect":"A hidden rhythm points to the next mystery.", "trust":7},
        {"title":"✋ Touch Rune", "message":f"I touch the rune wall in {t}.",           "effect":"A fresh clue is revealed.",                   "trust":9},
        {"title":"➡ Follow Clue","message":f"I follow the clue in {t}.",               "effect":ch["clue"],                                    "trust":10},
    ]

def _relic_icon_art(rarity: str) -> Image.Image:
    w, h = 300, 300; img = Image.new("RGBA",(w,h),(0,0,0,0)); draw = ImageDraw.Draw(img)
    rc = _RARITY_COLORS.get(rarity,(124,92,255)); r2 = tuple(min(255,c+60) for c in rc)
    draw.ellipse((10,10,w-10,h-10), fill=(8,14,24))
    for i in range(8,0,-1): draw.ellipse((10+i*3,10+i*3,w-10-i*3,h-10-i*3), outline=rc+(int(120*i/8),), width=2)
    cx, cy = w//2, h//2
    draw.polygon([(cx,cy-70),(cx+55,cy),(cx,cy+70),(cx-55,cy)], fill=rc)
    draw.polygon([(cx,cy-70),(cx+55,cy),(cx,cy)], fill=r2)
    draw.polygon([(cx,cy-70),(cx-55,cy),(cx,cy)], fill=tuple(max(0,c-40) for c in rc))
    draw.ellipse((cx-12,cy-12,cx+12,cy+12), fill=(255,255,255,200))
    draw.ellipse((cx-5,cy-5,cx+5,cy+5), fill=(255,255,255,255))
    draw.ellipse((6,6,w-6,h-6), outline=r2+(200,), width=3)
    try: font = ImageFont.truetype("DejaVuSans-Bold.ttf",18)
    except Exception: font = ImageFont.load_default()
    lbl = rarity.upper(); bbox = draw.textbbox((0,0),lbl,font=font)
    draw.text(((w-(bbox[2]-bbox[0]))//2,h-32), lbl, fill=r2+(230,), font=font)
    return img.convert("RGB")

def _wrap_text(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textbbox((0,0),trial,font=font)[2] <= max_w: cur = trial
        else:
            if cur: lines.append(cur)
            cur = word
    if cur: lines.append(cur)
    return lines

def make_relic_card(relic: dict, relic_image: Image.Image) -> Image.Image:
    cw, ch = 900, 520; card = Image.new("RGB",(cw,ch),(8,14,24)); draw = ImageDraw.Draw(card)
    draw.rounded_rectangle((10,10,cw-10,ch-10), radius=24, outline=(124,92,255), width=4)
    draw.rounded_rectangle((24,24,cw-24,ch-24), radius=18, fill=(16,24,39))
    art = relic_image.copy().convert("RGB"); art.thumbnail((300,300))
    panel = Image.new("RGB",(300,300),(11,18,32)); panel.paste(art,((300-art.width)//2,(300-art.height)//2))
    card.paste(panel,(50,110)); draw.rounded_rectangle((50,110,350,410), radius=16, outline=(39,194,255), width=2)
    try: tf,bf,lf = ImageFont.truetype("DejaVuSans-Bold.ttf",34),ImageFont.truetype("DejaVuSans.ttf",22),ImageFont.truetype("DejaVuSans-Bold.ttf",20)
    except Exception: tf = bf = lf = ImageFont.load_default()
    x, y = 390, 60
    draw.text((x,y), relic["name"], fill=(229,236,244), font=tf); y += 52
    rc = _RARITY_COLORS.get(relic.get("rarity","Common"),(39,194,255))
    draw.text((x,y), f"Rarity: {relic['rarity']}", fill=rc, font=lf); y += 46
    for heading, content in [("Lore",relic["lore"]),("Power",relic["power"])]:
        draw.text((x,y), heading, fill=(124,92,255), font=lf); y += 30
        for line in _wrap_text(draw, content, bf, 450)[:5]: draw.text((x,y), line, fill=(229,236,244), font=bf); y += 28
        y += 18
    return card

def get_relic_image(art_prompt: str, rarity: str = "Rare") -> Image.Image:
    return _relic_icon_art(rarity)

def maybe_generate_current_chamber():
    s = st.session_state
    if s.trust_score < TRUST_TO_ENTER or s.current_chamber >= TOTAL_CHAMBERS: return None
    if s.last_chamber is None:
        ch = generate_chamber(s.current_chamber, s.chamber_history)
        s.last_chamber = ch; s.latest_clue = ch["clue"]
        if ch["title"] not in s.unlocked_chambers:
            s.unlocked_chambers.append(ch["title"]); s.chamber_history.append(ch["title"])
            s.chamber_descriptions[ch["title"]] = ch["description"]
            append_log("SYSTEM", f"Chamber loaded: {ch['title']}")
        check_achievements()
    return s.last_chamber


# ── YOUR CODE — write inside each function ────────────────────────

def generate_chamber(idx: int, history: list) -> dict:
    pass


def generate_relic(chamber_title: str, description: str, count: int) -> dict:
    pass


def generate_final_ending(player_name: str, relic_names: list, chamber_history: list) -> str:
    pass


def apply_scenario(sc: dict):
    pass


def forge_relic():
    pass


def unlock_final_vault():
    pass
