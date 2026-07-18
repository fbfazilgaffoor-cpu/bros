import random
import streamlit as st
from groq import Groq

import config
from constants import (
    MAX_TRUST, BANISH_THRESHOLD, STREAK_BONUS_AT,
    HELPFUL_HINTS, RUDE_HINTS,
    MOOD_STYLES, MOOD_FEEL,
    SENTINEL_FALLBACKS, REPEAT_REPLIES,
)


# ── PROVIDED (completed in Lesson 4) — do not change ─────────────
def _append_log(role: str, text: str):
    st.session_state.sentinel_messages.append(f"[{role}]: {text}")

def analyze_player_tone(message: str, streak: int = 0, recent_messages: list = None) -> int:
    msg = message.lower().strip()
    if recent_messages:
        recent_lower = [m.lower().strip() for m in recent_messages[-6:]]
        if recent_lower.count(msg) >= 2:
            return 0
    delta = 4
    if len(msg) < 4:                                 delta -= 1
    if any(w in msg for w in HELPFUL_HINTS):         delta += 10
    if any(w in msg for w in RUDE_HINTS):            delta -= 12
    if "?" in msg:                                   delta += 2
    if streak >= STREAK_BONUS_AT and delta > 0:      delta += 6
    return max(-15, min(20, delta))

def get_sentinel_mood(trust: int) -> str:
    if trust < 20: return "Suspicious"
    if trust < 50: return "Watching"
    if trust < 80: return "Curious"
    return "Accepting"

def process_player_message(msg: str):
    s = st.session_state
    if not s.player_name.strip():
        st.toast("Enter your traveler name first.", icon="⚠️"); return
    if not msg.strip(): return
    recent = [m.lower().strip() for m in s.player_messages[-6:]]
    if recent.count(msg.lower().strip()) >= 2:
        st.toast("The Sentinel noticed you're repeating yourself.", icon="😐")
        _append_log("YOU", msg)
        _append_log("SENTINEL", random.choice(REPEAT_REPLIES))
        s.player_messages.append(msg); s.messages_sent += 1; return
    delta = analyze_player_tone(msg, s.streak, s.player_messages)
    s.trust_score = max(0, min(MAX_TRUST, s.trust_score + delta))
    s.sentinel_mood = get_sentinel_mood(s.trust_score)
    s.streak = s.streak + 1 if delta > 0 else 0
    _append_log("YOU", msg)
    _append_log("SENTINEL", ask_sentinel(s.player_name, msg, s.trust_score, s.sentinel_mood))
    s.player_messages.append(msg)
    s.latest_clue = "The Sentinel studies your tone."
    s.messages_sent += 1
    if s.trust_score <= BANISH_THRESHOLD and delta < 0: s.banished = True

def process_riddle_answer(answer: str):
    s = st.session_state
    if s.riddle_solved: st.toast("Logic lock already solved.", icon="ℹ️"); return
    if not answer.strip(): return
    riddle = s.riddle
    if riddle["answer"].lower() in answer.lower().strip():
        s.riddle_solved = True
        s.trust_score = min(MAX_TRUST, s.trust_score + 35)
        s.sentinel_mood = get_sentinel_mood(s.trust_score)
        s.streak += 1
        _append_log("YOU", f"Riddle: {answer}")
        _append_log("SENTINEL", random.choice([
            "Yes. That's it. I felt the lock shift just now — something old and heavy, finally moving.",
            "Hm. You actually got it. The seal loosens. Don't make me regret this.",
            "Correct. The gate remembers that answer. You're smarter than you look, traveler.",
        ]))
        s.latest_clue = "The runes brighten — a thin line of light appears in the gate."
        st.toast("Correct! The lock flashes open.", icon="✅")
    else:
        s.trust_score = max(0, s.trust_score - 5)
        s.sentinel_mood = get_sentinel_mood(s.trust_score)
        s.streak = 0
        _append_log("YOU", f"Riddle: {answer}")
        hint_reply = generate_riddle_hint(riddle["question"], riddle["answer"], riddle["hint"])
        _append_log("SENTINEL", hint_reply)
        s.latest_clue = f"Hint: {riddle['hint']}"
        st.toast("Incorrect — the seal holds.", icon="❌")


# ── YOUR CODE — write inside each function ────────────────────────

def fallback_sentinel(player_name: str, message: str, mood: str) -> str:
    pass


def ask_sentinel(player_name: str, message: str, trust: int, mood: str) -> str:
    pass


def generate_riddle_hint(riddle_question: str, riddle_answer: str, plain_hint: str) -> str:
    pass


def generate_event_narration(event_title: str, plain_description: str) -> str:
    pass
