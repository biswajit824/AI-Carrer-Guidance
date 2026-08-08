from langchain_sarvam import ChatSarvam

from src.config import SARVAM_MODEL


def get_sarvam_llm():

    llm = ChatSarvam(
        model=SARVAM_MODEL,
        temperature=0.2,
        max_tokens=2048,
    )

    return llm