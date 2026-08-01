import json
from io import BytesIO

from groq import Groq
from huggingface_hub import InferenceClient
from PIL import Image, ImageDraw

import config
from constants import REQUIRED_KEYS, ROOM_FALLBACK


def validate_room_json(data: dict) -> bool:
    return all(key in data for key in REQUIRED_KEYS)


def build_fallback_room(room_name: str, theme: str, mood: str) -> dict:
    return {
        "title": room_name,
        "description": ROOM_FALLBACK["description"].format(
            room_name=room_name,
            theme=theme,
            mood=mood.lower(),
        ),
        "clue": ROOM_FALLBACK["clue"],
        "art_prompt": ROOM_FALLBACK["art_prompt"].format(
            room_name=room_name,
            theme=theme,
            mood=mood.lower(),
        ),
    }


def generate_room_json(room_name: str, theme: str, mood: str) -> dict:
    if not config.GROQ_API_KEY:
        return build_fallback_room(room_name, theme, mood)

    system_prompt = (
        "You write fantasy room descriptions. "
        "Return valid JSON only with exactly these keys: "
        "title, description, clue, art_prompt."
    )

    user_prompt = (
        f"Room name: {room_name}\n"
        f"Theme: {theme}\n"
        f"Mood: {mood}\n\n"
        "Write an immersive fantasy room description in JSON.\n"
        "Requirements:\n"
        "- title: room name\n"
        "- description: 2 to 3 vivid sentences\n"
        "- clue: one mysterious clue sentence\n"
        "- art_prompt: one visual image-generation prompt for the room\n"
        "Return JSON only."
    )

    try:
        client = Groq(api_key=config.GROQ_API_KEY)
        response = client.chat.completions.create(
            model=config.GROQ_TEXT_MODEL,
            temperature=0.9,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        text = response.choices[0].message.content.strip()
        data = json.loads(text)

        if validate_room_json(data):
            return data
    except Exception as e:
        print(f"[GROQ ERROR] {e}")

    return build_fallback_room(room_name, theme, mood)


def generate_room_image_bytes(prompt: str):
    if not config.HF_API_KEY:
        return None, "HF API key is missing."

    try:
        client = InferenceClient(
            provider=config.HF_PROVIDER,
            api_key=config.HF_API_KEY,
        )

        image = client.text_to_image(
            prompt,
            model=config.HF_IMAGE_MODEL,
        )

        buffer = BytesIO()
        image.save(buffer, format="PNG")
        return buffer.getvalue(), None

    except Exception as e:
        return None, f"Hugging Face image generation failed: {str(e)}"


def make_fallback_image(title: str) -> bytes:
    image = Image.new("RGB", (1024, 640), (11, 18, 40))
    draw = ImageDraw.Draw(image)

    draw.rectangle((70, 70, 954, 570), outline=(122, 162, 255), width=5)

    safe_title = title[:40] if title else "Room Preview"

    draw.text((110, 120), safe_title, fill=(255, 255, 255))
    draw.text(
        (110, 200),
        "Fantasy room artwork preview unavailable.",
        fill=(210, 220, 255),
    )

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def craft_room_story(room_name: str, theme: str, mood: str) -> dict:
    room_data = generate_room_json(room_name, theme, mood)

    image_bytes, image_error = generate_room_image_bytes(room_data["art_prompt"])
    if image_bytes is None:
        image_bytes = make_fallback_image(room_data["title"])

    room_data["image_bytes"] = image_bytes
    room_data["image_error"] = image_error
    return room_data