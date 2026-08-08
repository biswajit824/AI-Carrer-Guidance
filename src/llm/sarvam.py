import os

from langchain_sarvam import ChatSarvam

from src.config import SARVAM_MODEL


def get_sarvam_llm():

    llm = ChatSarvam(
    model="sarvam-105b",
    temperature=0.2,
    max_tokens=4096,
    reasoning_effort=None,
    api_key=os.getenv("SARVAM_API_KEY")
)

    return llm