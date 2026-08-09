import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()


LANGUAGE_CODES = {
    "English": "en-IN",
    "Hindi": "hi-IN",
    "Odia": "od-IN",
    "Tamil": "ta-IN",
    "Telugu": "te-IN",
    "Kannada": "kn-IN"
}


def generate_speech(text, language):

    api_key = os.getenv("SARVAM_API_KEY")

    if not api_key:
        raise ValueError("SARVAM_API_KEY not found in .env")

    language_code = LANGUAGE_CODES.get(language)

    if not language_code:
        raise ValueError(
            f"Unsupported language: {language}"
        )

    # Bulbul v3 REST API limit = 2500 characters
    text = text[:2400]

    url = "https://api.sarvam.ai/text-to-speech"

    headers = {
        "api-subscription-key": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "target_language_code": language_code,
        "speaker": "shubh",
        "model": "bulbul:v3"
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=60
    )

    # If Sarvam returns an error
    if response.status_code != 200:

        raise Exception(
            f"Sarvam TTS API error "
            f"{response.status_code}: "
            f"{response.text}"
        )

    data = response.json()

    if "audios" not in data:
        raise Exception(
            f"No audio returned by Sarvam: {data}"
        )

    if not data["audios"]:
        raise Exception(
            "Sarvam returned an empty audio response."
        )

    # Base64 → bytes
    audio_base64 = data["audios"][0]

    audio_bytes = base64.b64decode(
        audio_base64
    )

    return audio_bytes