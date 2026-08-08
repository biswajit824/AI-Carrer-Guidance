# from src.llm.sarvam import get_sarvam_llm
# from src.llm.prompts import career_prompt


# def create_career_chain():

#     llm = get_sarvam_llm()

#     chain = career_prompt | llm

#     return chain




# from src.llm.chains import create_career_chain


# src/llm/chains.py

import os

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_sarvam import ChatSarvam

load_dotenv()


def create_career_chain():

    llm = ChatSarvam(
        model="sarvam-105b",
        temperature=0.2,
        api_key=os.getenv("SARVAM_API_KEY")
    )

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are an AI Career Guidance Assistant for
Tier-2 and Tier-3 engineering students.

Your job is to provide practical, personalized,
grounded career guidance.

Do not guarantee jobs, internships, salaries,
admissions or placement outcomes.

Use the student's profile and recommendation
context to explain your reasoning.

Provide actionable recommendations.
"""
        ),
        (
            "human",
            """
Student Profile:

{profile}

Recommendation Context:

{context}

Student Question:

{question}

Give a clear and practical response.
"""
        )
    ])

    chain = prompt | llm

    return chain





#Seperate


from src.llm.sarvam import get_sarvam_llm
from src.llm.prompts import career_prompt


def create_career_chain():

    llm = get_sarvam_llm()

    return career_prompt | llm


def generate_response(
    profile,
    context,
    question
):

    chain = create_career_chain()

    try:

        response = chain.invoke(
            {
                "profile": profile,
                "context": context,
                "question": question
            }
        )

        return {
            "success": True,
            "response": response.content,
            "error": None
        }

    except Exception as e:

        return {
            "success": False,
            "response": (
                "The AI service is temporarily "
                "unavailable. Please try again."
            ),
            "error": str(e)
        }