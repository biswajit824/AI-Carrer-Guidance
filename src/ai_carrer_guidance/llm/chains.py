from ai_carrer_guidance.llm.sarvam import get_sarvam_llm
from ai_carrer_guidance.llm.prompts import career_prompt


def create_career_chain():

    llm = get_sarvam_llm()

    chain = career_prompt | llm

    return chain
