import os

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_sarvam import ChatSarvam

load_dotenv()


def create_career_chain():

    api_key = os.getenv("SARVAM_API_KEY")

    if not api_key:
        raise ValueError(
            "SARVAM_API_KEY not found in environment variables."
        )

    llm = ChatSarvam(
        model="sarvam-105b",
        temperature=0.2,

        # IMPORTANT
        max_tokens=4096,
        reasoning_effort=None,

        api_key=api_key
    )

    prompt = ChatPromptTemplate.from_messages([

        (
            "system",
            """
You are an AI Career Guidance Assistant
for Tier-2 and Tier-3 engineering students.

Your task is to provide practical,
personalized and actionable career guidance.

Use the student's profile and the
recommendation context provided.

Do NOT guarantee:
- jobs
- internships
- salaries
- admissions
- placement outcomes

Explain your reasoning clearly.

Your response should be detailed but
easy for a student to understand.

Use Markdown formatting.

Include:

1. Career suitability analysis
2. Current strengths
3. Skill gaps
4. Priority skills to learn
5. Recommended projects
6. Learning resources/topics
7. 30-day roadmap
8. 60-day roadmap
9. 90-day roadmap
10. Interview preparation
11. Final actionable recommendations
"""
        ),

        (
            "human",
            """
STUDENT PROFILE
---------------
{profile}


RECOMMENDATION CONTEXT
----------------------
{context}


STUDENT QUESTION
----------------
{question}


Generate a personalized career guidance report.
"""
        )

    ])

    chain = prompt | llm

    return chain

