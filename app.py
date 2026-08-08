import streamlit as st

from utils.data_loader import load_json


st.set_page_config(
    page_title="CareerGenie AI",
    page_icon="🎯",
    layout="wide"
)


roles = load_json("roles.json")


st.title("🎯 CareerGenie AI")

st.markdown(
    "### Personalized AI Career & Skill-Gap Assistant"
)

st.divider()


st.header("👨‍🎓 Student Profile")


name = st.text_input(
    "Your Name"
)


branch = st.selectbox(
    "Engineering Branch",
    [
        "Computer Science",
        "Information Technology",
        "Electronics",
        "Electrical",
        "Mechanical",
        "Civil",
        "Other"
    ]
)


year = st.selectbox(
    "Year",
    [
        "1st Year",
        "2nd Year",
        "3rd Year",
        "4th Year",
        "Graduate"
    ]
)


skills = st.text_input(
    "Your Current Skills",
    placeholder="Example: Python, SQL, Machine Learning"
)


interests = st.text_input(
    "Your Interests",
    placeholder="Example: AI, GenAI, Data Science"
)


role_names = [
    role["role"]
    for role in roles
]


target_role = st.selectbox(
    "Target Career Role",
    role_names
)


study_hours = st.slider(
    "Available Study Hours Per Day",
    min_value=1,
    max_value=8,
    value=2
)


if st.button(
    "🚀 Analyze My Career",
    type="primary"
):

    if not name:
        st.warning("Please enter your name.")

    elif not skills:
        st.warning("Please enter at least one skill.")

    else:

        st.success("Profile captured successfully!")

        st.write("### Your Profile")

        st.write(f"**Name:** {name}")
        st.write(f"**Branch:** {branch}")
        st.write(f"**Year:** {year}")
        st.write(f"**Skills:** {skills}")
        st.write(f"**Interests:** {interests}")
        st.write(f"**Target Role:** {target_role}")
        st.write(f"**Study Time:** {study_hours} hours/day")