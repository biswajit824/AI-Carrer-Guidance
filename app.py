import streamlit as st

from src.data.loader import load_json
from src.career.matcher import rank_roles
from src.career.skill_gap import analyze_skill_gap
from src.career.roadmap import create_roadmap

from src.llm.chains import create_career_chain


st.set_page_config(
    page_title="AI Career Guidance Assistant",
    page_icon="🎓",
    layout="wide"
)


st.title("🎓 AI Career Guidance Assistant")

st.write(
    """
    Personalized career guidance for
    Tier-2 and Tier-3 engineering students.
    """
)

st.header("👤 Student Profile")

col1, col2 = st.columns(2)

with col1:

    branch = st.selectbox(
        "Engineering Branch",
        [
            "Computer Science",
            "Information Technology",
            "AI & ML",
            "Electronics",
            "Electrical",
            "Mechanical",
            "Civil"
        ]
    )

    year = st.selectbox(
        "Year",
        [
            "1st Year",
            "2nd Year",
            "3rd Year",
            "Final Year"
        ]
    )

with col2:

    preferred_role = st.selectbox(
        "Preferred Career Role",
        [
            "AI/ML Engineer",
            "Data Analyst",
            "Backend Developer"
        ]
    )

    language = st.selectbox(
        "Preferred Language",
        [
            "English",
            "Hindi",
            "Odia",
            "Tamil",
            "Telugu",
            "Kannada"
        ]
    )



skills_input = st.multiselect(
    "Your Current Skills",
    [
        "Python",
        "SQL",
        "Machine Learning",
        "Deep Learning",
        "Pandas",
        "Scikit-learn",
        "Statistics",
        "Excel",
        "Power BI",
        "Flask",
        "REST API",
        "Git",
        "Databases"
    ]
)    



projects = st.text_area(
    "Describe your projects",
    placeholder=(
        "Example: Built a machine learning "
        "project for predicting customer churn."
    )
)

learning_hours = st.slider(
    "Learning hours per day",
    min_value=1,
    max_value=8,
    value=2
)

if st.button(
    "🚀 Analyze My Career",
    type="primary"
):

    roles = load_json(
        "data/roles.json"
    )

    results = rank_roles(
        skills_input,
        roles
    )

    st.session_state["results"] = results


# --------------------------------
# AI PERSONALIZED GUIDANCE
# # --------------------------------

# if "results" in st.session_state:

#     best_role = st.session_state["results"][0]

#     profile = f"""
#     Branch: {branch}
#     Year: {year}
#     Skills: {', '.join(skills_input)}
#     Preferred Role: {preferred_role}
#     Learning Hours Per Day: {learning_hours}
#     Preferred Language: {language}
#     Projects: {projects}
#     """

#     context = f"""
#     Recommended Role:
#     {best_role['role']}

#     Skill Match:
#     {best_role['score']}%

#     Matching Skills:
#     {', '.join(best_role['matched_skills'])}

#     Missing Skills:
#     {', '.join(best_role['missing_skills'])}

#     Suggested Beginner Projects:
#     {', '.join(best_role['projects'])}
#     """

#     question = """
#     Analyze this student's profile.

#     Explain:
#     1. Why this role is suitable.
#     2. Their current strengths.
#     3. Their major skill gaps.
#     4. What they should learn first.
#     5. What project they should build.
#     6. Give a practical 30/60/90-day roadmap.
#     """

#     chain = create_career_chain()

#     with st.spinner(
#         "Generating personalized guidance..."
#     ):

#         response = chain.invoke(
#             {
#                 "profile": profile,
#                 "context": context,
#                 "question": question
#             }
#         )

#     st.session_state["ai_response"] = response.content

#     st.header("🤖 Personalized AI Guidance")

#     st.markdown(
#         st.session_state["ai_response"]
#     )



# # Chat interface
# # 
# # 
# st.header("💬 Career Q&A")
# if "messages" not in st.session_state:

#     st.session_state.messages = []

# for message in st.session_state.messages:

#     with st.chat_message(
#         message["role"]
#     ):

#         st.markdown(
#             message["content"]
#         )

# user_question = st.chat_input(
#     "Ask a career question..."
# )

# if user_question:

#     st.session_state.messages.append(
#         {
#             "role": "user",
#             "content": user_question
#         }
#     )