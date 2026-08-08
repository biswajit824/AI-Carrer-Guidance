import os
import base64

from dotenv import load_dotenv
from sarvamai import SarvamAI

load_dotenv()


# ------------------------------------------------
# Language mapping
# ------------------------------------------------

LANGUAGE_CODES = {
    "English": "en-IN",
    "Hindi": "hi-IN",
    "Odia": "od-IN",
    "Tamil": "ta-IN",
    "Telugu": "te-IN",
    "Kannada": "kn-IN"
}


# ------------------------------------------------
# Generate speech
# ------------------------------------------------

def generate_speech(text, language):

    api_key = os.getenv("SARVAM_API_KEY")

    if not api_key:
        raise ValueError(
            "SARVAM_API_KEY is not configured."
        )

    client = SarvamAI(
        api_subscription_key=api_key
    )

    language_code = LANGUAGE_CODES.get(
        language,
        "en-IN"
    )

    response = client.text_to_speech.convert(
        text=text,
        model="bulbul:v3",
        target_language_code=language_code,
        speaker="shubh",
        pace=1.0,
        speech_sample_rate=24000
    )

    return response