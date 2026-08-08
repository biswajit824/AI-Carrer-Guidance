import os
from dotenv import load_dotenv

load_dotenv()

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

SARVAM_MODEL = "sarvam-105b"

if not SARVAM_API_KEY:
    raise RuntimeError(
        "SARVAM_API_KEY is missing. "
        "Please add it to your .env file."
    )