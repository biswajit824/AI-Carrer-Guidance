# # from src.llm.sarvam import get_sarvam_llm
# # from src.llm.prompts import career_prompt


# # def create_career_chain():

# #     llm = get_sarvam_llm()

# #     chain = career_prompt | llm

# #     return chain




# # from src.llm.chains import create_career_chain


# # src/llm/chains.py













# # import os

# # from dotenv import load_dotenv
# # from langchain_core.prompts import ChatPromptTemplate
# # from langchain_sarvam import ChatSarvam

# # load_dotenv()


# # def create_career_chain():

# #     # llm = ChatSarvam(
# #     #     model="sarvam-105b",
# #     #     temperature=0.2,
# #     #     max_tokens=10000,
# #     #     api_key=os.getenv("SARVAM_API_KEY")
# #     # )




# #     llm =  ChatSarvam(
# #          model="sarvam-105b",
# #          temperature=0.2,
# #          max_tokens=4096,
# #          reasoning_effort=None,
# #          api_key=os.getenv("SARVAM_API_KEY")
# # )


# #     prompt = ChatPromptTemplate.from_messages([
# #         (
# #             "system",
# #             """
# # You are an AI Career Guidance Assistant for
# # Tier-2 and Tier-3 engineering students.

# # Your job is to provide practical, personalized,
# # grounded career guidance.

# # Do not guarantee jobs, internships, salaries,
# # admissions or placement outcomes.

# # Use the student's profile and recommendation
# # context to explain your reasoning.

# # Provide actionable recommendations.
# # """
# #         ),
# #         (
# #             "human",
# #             """
# # Student Profile:

# # {profile}

# # Recommendation Context:

# # {context}

# # Student Question:

# # {question}

# # Give a clear and practical response.
# # """
# #         )
# #     ])

# #     chain = prompt | llm

# #     return chain





# # #Seperate


# from src.llm.sarvam import get_sarvam_llm
# from src.llm.prompts import career_prompt


# def create_career_chain():

#     llm = get_sarvam_llm()

#     return career_prompt | llm


# def generate_response(
#     profile,
#     context,
#     question
# ):

#     chain = create_career_chain()

#     try:

#         response = chain.invoke(
#             {
#                 "profile": profile,
#                 "context": context,
#                 "question": question
#             }
#         )

#         return {
#             "success": True,
#             "response": response.content,
#             "error": None
#         }

#     except Exception as e:

#         return {
#             "success": False,
#             "response": (
#                 "The AI service is temporarily "
#                 "unavailable. Please try again."
#             ),
#             "error": str(e)
#         }

















# # import os

# # from dotenv import load_dotenv
# # from langchain_core.prompts import ChatPromptTemplate
# # from langchain_sarvam import ChatSarvam

# # load_dotenv()


# # def create_career_chain():

# #     api_key = os.getenv("SARVAM_API_KEY")

# #     if not api_key:
# #         raise ValueError(
# #             "SARVAM_API_KEY is missing from .env"
# #         )

# #     llm = ChatSarvam(
# #         model="sarvam-105b",
# #         reasoning_effort=None,
# #         max_tokens=1500,
# #         temperature=0.2,
# #         api_key=api_key
# #     )

# #     prompt = ChatPromptTemplate.from_messages([
# #         (
# #             "system",
# #             """
# # You are an AI Career Guidance Assistant.

# # Give practical and personalized career guidance
# # to engineering students.

# # Do not guarantee jobs or placements.

# # Keep the response detailed but concise.
# # """
# #         ),
# #         (
# #             "human",
# #             """
# # Student Profile:

# # {profile}

# # Recommendation Context:

# # {context}

# # Question:

# # {question}

# # Give a useful career recommendation.
# # """
# #         )
# #     ])

# #     return prompt | llm
























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