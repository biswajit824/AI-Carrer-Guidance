import os

import streamlit as st
from dotenv import load_dotenv
from sarvamai import SarvamAI


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    # page_title="Career AI",
    # page_icon="🎓",
    layout="wide"
)


# ============================================================
# ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

# Current supported Sarvam chat model
SARVAM_MODEL = "sarvam-105b"


# ============================================================
# SARVAM AI CLIENT
# ============================================================

sarvam_client = None

if SARVAM_API_KEY:

    try:

        sarvam_client = SarvamAI(
            api_subscription_key=SARVAM_API_KEY
        )

    except Exception:

        sarvam_client = None


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "readiness_score" not in st.session_state:
    st.session_state.readiness_score = None

if "gps_result" not in st.session_state:
    st.session_state.gps_result = None

if "gap_result" not in st.session_state:
    st.session_state.gap_result = None

if "ai_roadmap" not in st.session_state:
    st.session_state.ai_roadmap = None


# ============================================================
# CAREER ROLE REQUIREMENTS
# ============================================================

CAREER_ROLES = {

    "Software Engineer": {

        "Python": 80,
        "DSA": 90,
        "SQL": 70,
        "OOP": 75,
        "DBMS": 70,
        "Git": 60,
        "Development": 80,
        "Communication": 70

    },

    "AI/ML Engineer": {

        "Python": 85,
        "DSA": 65,
        "SQL": 65,
        "Statistics": 75,
        "Machine Learning": 85,
        "Deep Learning": 80,
        "GenAI": 75,
        "Git": 60,
        "Deployment": 70

    },

    "Data Analyst": {

        "Python": 70,
        "SQL": 90,
        "Excel": 80,
        "Statistics": 75,
        "Power BI": 80,
        "Data Visualization": 75,
        "Communication": 70

    },

    "GenAI Engineer": {

        "Python": 80,
        "LLM APIs": 85,
        "Prompt Engineering": 70,
        "RAG": 85,
        "Embeddings": 75,
        "Vector Databases": 70,
        "Git": 60,
        "Deployment": 75

    }
}


# ============================================================
# SKILL IMPORTANCE
# ============================================================

SKILL_IMPORTANCE = {

    "Python": 1.2,
    "DSA": 1.0,
    "SQL": 1.0,
    "OOP": 1.0,
    "DBMS": 1.0,
    "Git": 0.8,
    "Development": 1.1,
    "Communication": 0.8,

    "Statistics": 1.0,
    "Machine Learning": 1.3,
    "Deep Learning": 1.2,
    "GenAI": 1.3,
    "Deployment": 1.2,

    "Excel": 0.8,
    "Power BI": 1.0,
    "Data Visualization": 1.0,

    "LLM APIs": 1.2,
    "Prompt Engineering": 1.0,
    "RAG": 1.3,
    "Embeddings": 1.1,
    "Vector Databases": 1.1
}


# ============================================================
# NAVIGATION
# ============================================================

def go_home():

    st.session_state.page = "home"

    st.rerun()


def go_to_page(page_name):

    st.session_state.page = page_name

    st.rerun()


# ============================================================
# CAREER GPS CALCULATION
# ============================================================

def calculate_readiness(
    student_skills,
    required_skills
):

    total_score = 0
    valid_skills = 0

    for skill, required_level in required_skills.items():

        if required_level <= 0:
            continue

        current_level = student_skills.get(
            skill,
            0
        )

        skill_score = (
            current_level /
            required_level
        ) * 100

        skill_score = min(
            skill_score,
            100
        )

        total_score += skill_score

        valid_skills += 1

    if valid_skills == 0:
        return 0

    return round(
        total_score /
        valid_skills,
        1
    )


# ============================================================
# READINESS LEVEL
# ============================================================

def get_readiness_level(score):

    if score >= 80:

        return (
            "🟢 Job Ready",
            "You have a strong foundation for this career."
        )

    elif score >= 60:

        return (
            "🟡 Almost Ready",
            "You are close. Focus on your major skill gaps."
        )

    elif score >= 40:

        return (
            "🟠 Developing",
            "You have a foundation, but several skills need improvement."
        )

    else:

        return (
            "🔴 Needs Preparation",
            "Focus on building your fundamentals."
        )


# ============================================================
# SARVAM AI - GENERATE 30/60/90 DAY CAREER ROADMAP
# ============================================================

def generate_career_roadmap(
    target_role,
    readiness_score,
    skill_gaps,
    student_name=""
):

    # --------------------------------------------------------
    # CHECK SARVAM CLIENT
    # --------------------------------------------------------

    if sarvam_client is None:

        return None, (
            "Sarvam AI is not configured. "
            "Please check your SARVAM_API_KEY in the .env file."
        )

    # --------------------------------------------------------
    # CHECK SKILL GAPS
    # --------------------------------------------------------

    if not skill_gaps:

        return None, (
            "No skill-gap data was found. "
            "Please complete the Skill Gap Analyzer first."
        )

    # --------------------------------------------------------
    # CONVERT GAPS TO TEXT
    # --------------------------------------------------------

    gap_lines = []

    for gap in skill_gaps:

        gap_lines.append(
            f"""
Skill: {gap['skill']}
Current Level: {gap['current']}/100
Required Level: {gap['required']}/100
Gap: {gap['gap']} points
Priority: {gap['priority']}
"""
        )

    gap_text = "\n".join(gap_lines)

    # ========================================================
    # 30/60/90 DAY AI PROMPT
    # ========================================================

    prompt = f"""
You are an expert career mentor specializing in helping
Tier-2 and Tier-3 engineering students in India become
job-ready.

Create a highly personalized 30/60/90-day career roadmap
based ONLY on the student's target role, readiness score,
and actual skill gaps.

============================================================
STUDENT PROFILE
============================================================

Name:
{student_name if student_name else "Student"}

Target Role:
{target_role}

Career Readiness:
{readiness_score}/100

============================================================
ACTUAL SKILL GAP ANALYSIS
============================================================

{gap_text}

============================================================
ROADMAP OBJECTIVE
============================================================

The student has approximately 2-3 hours per day.

The roadmap must take the student from their CURRENT
skill level toward JOB READINESS.

The roadmap must be divided into:

DAY 1-30  = FOUNDATION PHASE
DAY 31-60 = SKILL BUILDING + PROJECT PHASE
DAY 61-90 = JOB READINESS PHASE

============================================================
IMPORTANT RULES
============================================================

1. Use the actual skill gaps provided above.

2. Prioritize the largest and most important gaps first.

3. Do NOT assume the student is an expert.

4. If a skill has a very low current level,
   start from fundamentals.

5. Every week must explicitly say WHAT TO LEARN.

6. Every week must contain practical coding/practice tasks.

7. Every week must contain measurable outcomes.

8. Include projects where relevant.

9. Include Git and GitHub practice.

10. Include resume improvement.

11. Include interview preparation.

12. Include DSA/interview practice where relevant
    to the selected career.

13. Include portfolio preparation.

14. Include job application preparation.

15. Do not give generic motivational advice.

16. Every task must be something the student can actually do.

17. Keep the workload realistic:
    approximately 2-3 hours per day.

18. Progress logically:

Learning
→ Practice
→ Mini Project
→ Major Project
→ Portfolio
→ Resume
→ Interview Preparation
→ Job Applications

19. Do not waste early weeks on resume or job applications.
    Technical foundation comes first.

20. Do not put advanced topics before their prerequisites.

21. Adapt the roadmap to the target role.

22. For example:
    - Software Engineer → Python, DSA, SQL, OOP, DBMS,
      Git, development, interviews.
    - AI/ML Engineer → Python, statistics, ML, DL,
      GenAI, deployment, projects.
    - Data Analyst → SQL, Excel, statistics, Power BI,
      visualization, portfolio.
    - GenAI Engineer → Python, LLM APIs, prompting,
      RAG, embeddings, vector databases, deployment.

============================================================
30 / 60 / 90 DAY STRUCTURE
============================================================

DAY 1-30:
FOUNDATION PHASE

Main objective:
Build the fundamental technical skills required
for the target career.

DAY 31-60:
SKILL BUILDING + PROJECT PHASE

Main objective:
Strengthen technical skills and build practical
portfolio projects.

DAY 61-90:
JOB READINESS PHASE

Main objective:
Convert technical skills and projects into
job-readiness through interviews, resume,
GitHub and applications.

============================================================
OUTPUT FORMAT
============================================================

CAREER GOAL:

Explain:
- Target role
- What the student needs to become job-ready
- The overall 90-day objective


CURRENT READINESS:

Readiness Score:
<score>/100

Readiness Level:
<Job Ready / Almost Ready / Developing / Needs Preparation>

Explain the student's biggest weaknesses based on
the actual skill gaps.


============================================================
DAYS 1-30 — FOUNDATION PHASE
============================================================

WEEK 1 — DAYS 1-7

WHAT TO LEARN:
<List specific concepts>

SKILLS:
<List skills>

DAILY PLAN:
Day 1:
Day 2:
Day 3:
Day 4:
Day 5:
Day 6:
Day 7:

PRACTICE:
<Specific exercises>

EXPECTED OUTCOME:
<Measurable outcome>


WEEK 2 — DAYS 8-14

WHAT TO LEARN:
<List specific concepts>

SKILLS:
<List skills>

DAILY PLAN:
Day 8:
Day 9:
Day 10:
Day 11:
Day 12:
Day 13:
Day 14:

PRACTICE:
<Specific exercises>

EXPECTED OUTCOME:
<Measurable outcome>


WEEK 3 — DAYS 15-21

WHAT TO LEARN:
<List specific concepts>

SKILLS:
<List skills>

DAILY PLAN:
Day 15:
Day 16:
Day 17:
Day 18:
Day 19:
Day 20:
Day 21:

PRACTICE:
<Specific exercises>

EXPECTED OUTCOME:
<Measurable outcome>


WEEK 4 — DAYS 22-30

WHAT TO LEARN:
<List specific concepts>

SKILLS:
<List skills>

DAILY PLAN:
Day 22:
Day 23:
Day 24:
Day 25:
Day 26:
Day 27:
Day 28:
Day 29:
Day 30:

PRACTICE:
<Specific exercises>

EXPECTED OUTCOME:
<Measurable outcome>


============================================================
30-DAY MILESTONE
============================================================

BY DAY 30:

Technical Skills:
<What should be learned>

Practical Skills:
<What should be practiced>

Project Progress:
<What should be completed>

SELF-ASSESSMENT:
<What the student should be able to do>


============================================================
DAYS 31-60 — SKILL BUILDING + PROJECT PHASE
============================================================

WEEK 5 — DAYS 31-37

WHAT TO LEARN:
<List specific concepts>

SKILLS:
<List skills>

DAILY PLAN:
Day 31:
Day 32:
Day 33:
Day 34:
Day 35:
Day 36:
Day 37:

PRACTICE:
<Specific exercises>

EXPECTED OUTCOME:
<Measurable outcome>


WEEK 6 — DAYS 38-44

WHAT TO LEARN:
<List specific concepts>

SKILLS:
<List skills>

DAILY PLAN:
Day 38:
Day 39:
Day 40:
Day 41:
Day 42:
Day 43:
Day 44:

PRACTICE:
<Specific exercises>

EXPECTED OUTCOME:
<Measurable outcome>


WEEK 7 — DAYS 45-51

WHAT TO LEARN:
<List specific concepts>

SKILLS:
<List skills>

DAILY PLAN:
Day 45:
Day 46:
Day 47:
Day 48:
Day 49:
Day 50:
Day 51:

PRACTICE:
<Specific exercises>

PROJECT WORK:
<What project work should be completed>

EXPECTED OUTCOME:
<Measurable outcome>


WEEK 8 — DAYS 52-60

WHAT TO LEARN:
<List specific concepts>

SKILLS:
<List skills>

DAILY PLAN:
Day 52:
Day 53:
Day 54:
Day 55:
Day 56:
Day 57:
Day 58:
Day 59:
Day 60:

PROJECT WORK:
<What should be completed>

GITHUB:
<What should be uploaded>

EXPECTED OUTCOME:
<Measurable outcome>


============================================================
60-DAY MILESTONE
============================================================

BY DAY 60:

Technical Skills:
<Expected level>

Projects:
<Projects that should be completed>

GitHub:
<Expected GitHub progress>

Portfolio:
<Expected portfolio progress>

SELF-ASSESSMENT:
<What the student should now be capable of>


============================================================
DAYS 61-90 — JOB READINESS PHASE
============================================================

WEEK 9 — DAYS 61-67

WHAT TO LEARN:
<List interview/job-relevant concepts>

SKILLS:
<List skills>

DAILY PLAN:
Day 61:
Day 62:
Day 63:
Day 64:
Day 65:
Day 66:
Day 67:

INTERVIEW PRACTICE:
<Specific practice>

EXPECTED OUTCOME:
<Measurable outcome>


WEEK 10 — DAYS 68-74

WHAT TO LEARN:
<List concepts>

SKILLS:
<List skills>

DAILY PLAN:
Day 68:
Day 69:
Day 70:
Day 71:
Day 72:
Day 73:
Day 74:

INTERVIEW PRACTICE:
<Specific practice>

EXPECTED OUTCOME:
<Measurable outcome>


WEEK 11 — DAYS 75-81

WHAT TO LEARN:
<List concepts>

SKILLS:
<List skills>

DAILY PLAN:
Day 75:
Day 76:
Day 77:
Day 78:
Day 79:
Day 80:
Day 81:

RESUME:
<Specific resume tasks>

GITHUB:
<Specific GitHub tasks>

EXPECTED OUTCOME:
<Measurable outcome>


WEEK 12 — DAYS 82-88

WHAT TO LEARN:
<List final technical topics>

SKILLS:
<List skills>

DAILY PLAN:
Day 82:
Day 83:
Day 84:
Day 85:
Day 86:
Day 87:
Day 88:

MOCK INTERVIEWS:
<Specific mock interview tasks>

JOB APPLICATIONS:
<Specific application tasks>

EXPECTED OUTCOME:
<Measurable outcome>


WEEK 13 — DAYS 89-90

FINAL JOB READINESS

DAY 89:
<Final preparation tasks>

DAY 90:
<Final assessment and job application tasks>

FINAL PROJECT:
<What should be demonstrated>

FINAL INTERVIEW PREPARATION:
<What should be revised>


============================================================
90-DAY FINAL MILESTONE
============================================================

BY DAY 90:

TECHNICAL SKILLS:
<List skills the student should have developed>

PROJECTS:
<List portfolio projects>

GITHUB:
<Expected GitHub state>

RESUME:
<Expected resume state>

INTERVIEW:
<Expected interview readiness>

JOB APPLICATIONS:
<Recommended application target>


============================================================
FINAL JOB-READY CHECKLIST
============================================================

[ ] Core technical skills completed

[ ] Skill gaps significantly reduced

[ ] At least one strong portfolio project

[ ] GitHub profile organized

[ ] Resume optimized for target role

[ ] LinkedIn profile updated

[ ] DSA/interview preparation completed where relevant

[ ] Technical interview practice completed

[ ] Behavioral interview preparation completed

[ ] Mock interviews completed

[ ] Job applications started

============================================================
FINAL ADVICE
============================================================

Give exactly 5 highly specific recommendations
based on this student's actual skill gaps.

Do not give generic motivational advice.

The recommendations must be actionable and
specific to the target role.
"""

    # ========================================================
    # CALL SARVAM AI
    # ========================================================

    try:

        response = sarvam_client.chat.completions(

            model=SARVAM_MODEL,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert career mentor "
                        "for Tier-2 and Tier-3 engineering "
                        "students in India. "
                        "Create practical, personalized "
                        "and job-focused career roadmaps."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.4,

            # Disable reasoning so the model has
            # more tokens available for the roadmap.
            reasoning_effort=None,

            # Starter tier supports up to 4096.
            max_tokens=4096
        )

        # ----------------------------------------------------
        # EXTRACT RESPONSE
        # ----------------------------------------------------

        if (
            response
            and response.choices
            and response.choices[0].message
        ):

            content = (
                response
                .choices[0]
                .message
                .content
            )

            if content:

                return content, None

        return None, (
            "Sarvam AI returned an empty response."
        )

    except Exception as e:

        return None, (
            f"Sarvam AI Error: {str(e)}"
        )


# ============================================================
# HOME PAGE
# ============================================================

def home_page():

    # st.title(
    #     "🎓 Career AI"
    # )

    # st.write(
    #     "Your AI-powered career guidance platform "
    #     "for engineering students."
    # )

    st.divider()

    st.subheader(
        "🚀 Explore Career Tools"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "🎯 Career GPS",
            use_container_width=True,
            type="primary",
            key="home_career_gps_button"
        ):

            go_to_page(
                "career_gps"
            )

        st.caption(
            "Check your overall career readiness."
        )

    with col2:

        if st.button(
            "🔍 Skill Gap Analyzer",
            use_container_width=True,
            type="primary",
            key="home_skill_gap_button"
        ):

            go_to_page(
                "skill_gap"
            )

        st.caption(
            "Find the skills you need to improve."
        )

    with col3:

        if st.button(
            "🗺️ Career Roadmap",
            use_container_width=True,
            type="primary",
            key="home_roadmap_button"
        ):

            go_to_page(
                "roadmap"
            )

        st.caption(
            "Get your personalized 30/60/90-day roadmap."
        )


# ============================================================
# CAREER GPS PAGE
# ============================================================

def career_gps_page():

    if st.button(
        "← Back to Home",
        key="gps_back_home_button"
    ):

        go_home()

    st.title(
        "🎯 Career GPS"
    )

    st.subheader(
        "Career Readiness Analyzer"
    )

    st.write(
        "Find out how prepared you are for your target "
        "career based on your current skills."
    )

    st.divider()

    st.header(
        "👨‍🎓 Student Profile"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        name = st.text_input(
            "Your Name",
            placeholder="Enter your name",
            key="gps_student_name"
        )

    with col2:

        cgpa = st.number_input(
            "CGPA",
            min_value=0.0,
            max_value=10.0,
            value=7.0,
            step=0.1,
            key="gps_cgpa"
        )

    with col3:

        college_tier = st.selectbox(
            "College Tier",
            [
                "Tier-2",
                "Tier-3"
            ],
            key="gps_college_tier"
        )

    st.header(
        "🎯 Target Career"
    )

    target_role = st.selectbox(
        "Which career are you targeting?",
        list(CAREER_ROLES.keys()),
        key="gps_target_role"
    )

    required_skills = CAREER_ROLES[
        target_role
    ]

    st.header(
        "💻 Rate Your Current Skills"
    )

    st.info(
        "Rate yourself honestly from 0 to 100."
    )

    student_skills = {}

    skill_items = list(
        required_skills.keys()
    )

    columns = st.columns(2)

    for index, skill in enumerate(
        skill_items
    ):

        with columns[index % 2]:

            student_skills[skill] = st.slider(
                skill,
                min_value=0,
                max_value=100,
                value=0,
                step=5,
                key=f"gps_skill_{skill}"
            )

    st.divider()

    if st.button(
        "🚀 Calculate My Career Readiness",
        type="primary",
        use_container_width=True,
        key="gps_calculate_button"
    ):

        readiness_score = calculate_readiness(
            student_skills,
            required_skills
        )

        st.session_state.readiness_score = (
            readiness_score
        )

        st.session_state.gps_result = {

            "name": name,

            "cgpa": cgpa,

            "college_tier": college_tier,

            "target_role": target_role,

            "skills": student_skills,

            "required_skills": required_skills
        }

        # Clear previous AI roadmap
        st.session_state.ai_roadmap = None

    if st.session_state.gps_result is not None:

        result = st.session_state.gps_result

        readiness_score = (
            st.session_state.readiness_score
        )

        readiness_level, description = (
            get_readiness_level(
                readiness_score
            )
        )

        st.divider()

        st.header(
            "📊 Your Career Readiness"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Career Readiness",
                f"{readiness_score}/100"
            )

        with col2:

            st.metric(
                "Target Role",
                result["target_role"]
            )

        with col3:

            st.metric(
                "College Tier",
                result["college_tier"]
            )

        st.progress(
            int(readiness_score)
        )

        st.subheader(
            readiness_level
        )

        st.write(
            description
        )

        st.divider()

        st.subheader(
            "📋 Skill Comparison"
        )

        for skill, required_level in (
            result["required_skills"].items()
        ):

            current_level = (
                result["skills"].get(
                    skill,
                    0
                )
            )

            if required_level > 0:

                percentage = min(
                    (
                        current_level /
                        required_level
                    ) * 100,
                    100
                )

            else:

                percentage = 100

            st.write(
                f"**{skill}** — "
                f"Your Level: {current_level} | "
                f"Required: {required_level}"
            )

            st.progress(
                int(percentage)
            )

        st.divider()

        st.subheader(
            "💡 Recommendation"
        )

        if readiness_score >= 80:

            st.success(
                "You are relatively well prepared. "
                "Focus on interviews, projects, "
                "and real-world experience."
            )

        elif readiness_score >= 60:

            st.warning(
                "You are getting close to being job-ready. "
                "Focus on your weakest skills."
            )

        elif readiness_score >= 40:

            st.warning(
                "You have started building the foundation. "
                "Strengthen your core technical skills."
            )

        else:

            st.error(
                "You need to strengthen your fundamentals "
                "before targeting this role."
            )


# ============================================================
# SKILL GAP ANALYZER
# ============================================================

def skill_gap_page():

    if st.button(
        "← Back to Home",
        key="gap_back_home_button"
    ):

        go_home()

    st.title(
        "🔍 Skill Gap Analyzer"
    )

    st.subheader(
        "Find exactly what you need to improve."
    )

    st.write(
        "We compare your current skill level with "
        "the expected skill level for your target career."
    )

    st.divider()

    st.header(
        "👨‍🎓 Student Profile"
    )

    col1, col2 = st.columns(2)

    with col1:

        student_name = st.text_input(
            "Your Name",
            placeholder="Enter your name",
            key="gap_student_name"
        )

    with col2:

        gps_role = None

        if st.session_state.gps_result:

            gps_role = st.session_state.gps_result.get(
                "target_role"
            )

        role_options = list(
            CAREER_ROLES.keys()
        )

        default_index = 0

        if gps_role in role_options:

            default_index = role_options.index(
                gps_role
            )

        target_role = st.selectbox(
            "Target Career",
            role_options,
            index=default_index,
            key="gap_target_role"
        )

    required_skills = CAREER_ROLES[
        target_role
    ]

    st.header(
        "💻 Your Current Skill Level"
    )

    st.info(
        "Rate each skill honestly from 0 to 100."
    )

    student_skills = {}

    skills = list(
        required_skills.keys()
    )

    columns = st.columns(2)

    for index, skill in enumerate(
        skills
    ):

        with columns[index % 2]:

            student_skills[skill] = st.slider(
                skill,
                min_value=0,
                max_value=100,
                value=0,
                step=5,
                key=f"gap_skill_{skill}"
            )

    st.divider()

    if st.button(
        "🔎 Analyze My Skill Gap",
        type="primary",
        use_container_width=True,
        key="gap_analyze_button"
    ):

        gaps = []

        for skill, required in (
            required_skills.items()
        ):

            current = student_skills.get(
                skill,
                0
            )

            gap = max(
                required - current,
                0
            )

            importance = (
                SKILL_IMPORTANCE.get(
                    skill,
                    1.0
                )
            )

            priority_score = (
                gap * importance
            )

            if gap >= 40:

                priority = "🔴 Critical"

            elif gap >= 25:

                priority = "🟠 High"

            elif gap >= 10:

                priority = "🟡 Medium"

            elif gap > 0:

                priority = "🔵 Low"

            else:

                priority = "🟢 No Gap"

            gaps.append({

                "skill": skill,

                "current": current,

                "required": required,

                "gap": gap,

                "priority": priority,

                "priority_score": priority_score
            })

        gaps.sort(
            key=lambda x: x["priority_score"],
            reverse=True
        )

        st.session_state.gap_result = {

            "student_name": student_name,

            "target_role": target_role,

            "gaps": gaps
        }

        st.session_state.ai_roadmap = None

    if st.session_state.gap_result is not None:

        result = (
            st.session_state.gap_result
        )

        gaps = result["gaps"]

        st.divider()

        st.header(
            "📊 Your Skill Gap Analysis"
        )

        st.write(
            f"Target Role: **{result['target_role']}**"
        )

        if result["student_name"]:

            st.write(
                f"Student: **{result['student_name']}**"
            )

        st.divider()

        st.subheader(
            "🚨 Top Skills You Should Improve"
        )

        top_gaps = [

            item
            for item in gaps
            if item["gap"] > 0

        ][:3]

        if top_gaps:

            for index, item in enumerate(
                top_gaps,
                start=1
            ):

                st.write(
                    f"### {index}. {item['skill']}"
                )

                col1, col2, col3, col4 = (
                    st.columns(4)
                )

                with col1:

                    st.metric(
                        "Current",
                        item["current"]
                    )

                with col2:

                    st.metric(
                        "Required",
                        item["required"]
                    )

                with col3:

                    st.metric(
                        "Gap",
                        item["gap"]
                    )

                with col4:

                    st.write(
                        item["priority"]
                    )

        else:

            st.success(
                "🎉 You currently have no major skill gaps!"
            )

        st.divider()

        st.subheader(
            "📋 Complete Skill Analysis"
        )

        for item in gaps:

            skill = item["skill"]

            current = item["current"]

            required = item["required"]

            gap = item["gap"]

            priority = item["priority"]

            st.write(
                f"**{skill}**"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    f"Your Level: **{current}/100**"
                )

            with col2:

                st.write(
                    f"Required: **{required}/100**"
                )

            if required > 0:

                progress = min(
                    (
                        current /
                        required
                    ) * 100,
                    100
                )

            else:

                progress = 100

            st.progress(
                int(progress)
            )

            if gap == 0:

                st.success(
                    f"{skill}: No significant gap"
                )

            else:

                st.warning(
                    f"{skill}: Gap of {gap} points "
                    f"— {priority}"
                )

            st.divider()

        st.subheader(
            "💡 What Should You Do Next?"
        )

        if top_gaps:

            first_gap = top_gaps[0]

            st.info(
                f"Your highest-priority skill is "
                f"**{first_gap['skill']}**. "
                f"Focus on improving this skill before "
                f"moving to lower-priority areas."
            )

            if len(top_gaps) >= 2:

                st.write(
                    f"**Next:** "
                    f"{top_gaps[1]['skill']}"
                )

            if len(top_gaps) >= 3:

                st.write(
                    f"**Then:** "
                    f"{top_gaps[2]['skill']}"
                )

        else:

            st.success(
                "Your profile is well aligned with "
                "your selected career."
            )


# ============================================================
# ADAPTIVE 30/60/90 DAY CAREER ROADMAP
# ============================================================

def roadmap_page():

    if st.button(
        "← Back to Home",
        key="roadmap_back_home_button"
    ):

        go_home()

    st.title(
        "🗺️ Adaptive 30/60/90-Day Career Roadmap"
    )

    st.subheader(
        "Turn your skill gaps into a personalized "
        "90-day job-readiness plan."
    )

    st.write(
        "Sarvam AI analyzes your Career GPS score "
        "and Skill Gap Analysis to create a roadmap "
        "showing exactly what to learn every week."
    )

    st.divider()

    # --------------------------------------------------------
    # REQUIRED DATA
    # --------------------------------------------------------

    gps_result = st.session_state.get(
        "gps_result"
    )

    gap_result = st.session_state.get(
        "gap_result"
    )

    readiness_score = st.session_state.get(
        "readiness_score"
    )

    # --------------------------------------------------------
    # GPS CHECK
    # --------------------------------------------------------

    if gps_result is None:

        st.warning(
            "⚠️ Career GPS has not been completed yet."
        )

        if st.button(
            "🎯 Complete Career GPS",
            key="roadmap_go_gps"
        ):

            go_to_page(
                "career_gps"
            )

        return

    # --------------------------------------------------------
    # GAP CHECK
    # --------------------------------------------------------

    if gap_result is None:

        st.warning(
            "⚠️ Skill Gap Analysis has not been completed yet."
        )

        if st.button(
            "🔍 Complete Skill Gap Analysis",
            key="roadmap_go_gap"
        ):

            go_to_page(
                "skill_gap"
            )

        return

    # --------------------------------------------------------
    # EXTRACT DATA
    # --------------------------------------------------------

    gps_target_role = gps_result.get(
        "target_role"
    )

    gap_target_role = gap_result.get(
        "target_role"
    )

    student_name = gps_result.get(
        "name",
        ""
    )

    gaps = gap_result.get(
        "gaps",
        []
    )

    # --------------------------------------------------------
    # ROLE CONSISTENCY
    # --------------------------------------------------------

    if gps_target_role != gap_target_role:

        st.error(
            "⚠️ Your Career GPS and Skill Gap Analyzer "
            "are targeting different careers."
        )

        st.write(
            f"Career GPS: **{gps_target_role}**"
        )

        st.write(
            f"Skill Gap Analyzer: **{gap_target_role}**"
        )

        st.info(
            "Please use the same target role in both modules."
        )

        return

    target_role = gps_target_role

    # --------------------------------------------------------
    # PROFILE SUMMARY
    # --------------------------------------------------------

    st.header(
        "👤 Your Career Profile"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Target Role",
            target_role
        )

    with col2:

        st.metric(
            "Career Readiness",
            f"{readiness_score}/100"
        )

    with col3:

        active_gaps = len([
            gap
            for gap in gaps
            if gap["gap"] > 0
        ])

        st.metric(
            "Skill Gaps",
            active_gaps
        )

    # --------------------------------------------------------
    # 30 / 60 / 90 OVERVIEW
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "📅 90-Day Roadmap Structure"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            "**DAYS 1-30**\n\n"
            "🏗️ Foundation Phase\n\n"
            "Build the fundamental skills "
            "required for your target role."
        )

    with col2:

        st.warning(
            "**DAYS 31-60**\n\n"
            "🚀 Skill + Project Phase\n\n"
            "Strengthen your skills and build "
            "practical portfolio projects."
        )

    with col3:

        st.success(
            "**DAYS 61-90**\n\n"
            "💼 Job Readiness Phase\n\n"
            "Prepare your resume, GitHub, interviews "
            "and job applications."
        )

    # --------------------------------------------------------
    # PRIORITY SKILLS
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "🚨 Priority Skills"
    )

    active_gap_list = [

        gap
        for gap in gaps
        if gap["gap"] > 0

    ]

    priority_gaps = active_gap_list[:5]

    if priority_gaps:

        for index, gap in enumerate(
            priority_gaps,
            start=1
        ):

            st.write(
                f"**{index}. {gap['skill']}** "
                f"— Current: {gap['current']} "
                f"| Required: {gap['required']} "
                f"| Gap: {gap['gap']} "
                f"| {gap['priority']}"
            )

    else:

        st.success(
            "🎉 No significant skill gaps were detected."
        )

    # --------------------------------------------------------
    # SARVAM AI
    # --------------------------------------------------------

    st.divider()

    st.header(
        "🤖 AI Career Mentor"
    )

    if sarvam_client is None:

        st.error(
            "❌ Sarvam AI is not configured."
        )

        st.info(
            "Create or update your .env file:"
        )

        st.code(
            "SARVAM_API_KEY=your_actual_api_key"
        )

        return

    st.success(
        "✅ Sarvam AI is connected."
    )

    st.write(
        "Sarvam AI will generate a 30/60/90-day roadmap "
        "with weekly learning goals and daily tasks "
        "based on your actual skill gaps."
    )

    # --------------------------------------------------------
    # GENERATE ROADMAP
    # --------------------------------------------------------

    if st.button(
        "🚀 Generate My 30/60/90-Day Roadmap",
        type="primary",
        use_container_width=True,
        key="generate_ai_roadmap_button"
    ):

        with st.spinner(
            "🤖 Sarvam AI is creating your 90-day career plan..."
        ):

            roadmap, error = (
                generate_career_roadmap(

                    target_role=target_role,

                    readiness_score=readiness_score,

                    skill_gaps=active_gap_list,

                    student_name=student_name
                )
            )

        if roadmap:

            st.session_state.ai_roadmap = roadmap

            st.success(
                "🎉 Your personalized 30/60/90-day roadmap is ready!"
            )

        else:

            st.session_state.ai_roadmap = None

            st.error(
                error if error else
                "Unable to generate roadmap."
            )

    # --------------------------------------------------------
    # DISPLAY ROADMAP
    # --------------------------------------------------------

    if st.session_state.ai_roadmap:

        st.divider()

        st.header(
            "🗺️ Your Personalized 30/60/90-Day Roadmap"
        )

        st.markdown(
            st.session_state.ai_roadmap
        )

        # ----------------------------------------------------
        # REGENERATE
        # ----------------------------------------------------

        st.divider()

        if st.button(
            "🔄 Generate New Roadmap",
            key="regenerate_roadmap_button"
        ):

            st.session_state.ai_roadmap = None

            st.rerun()


# ============================================================
# PAGE ROUTER
# ============================================================

if st.session_state.page == "home":

    home_page()

elif st.session_state.page == "career_gps":

    career_gps_page()

elif st.session_state.page == "skill_gap":

    skill_gap_page()

elif st.session_state.page == "roadmap":

    roadmap_page()







# def run_app():
#     if st.session_state.page == "home":
#         home_page()
#     elif st.session_state.page == "career_gps":
#         career_gps_page()
#     elif st.session_state.page == "skill_gap":
#         skill_gap_page()
#     elif st.session_state.page == "roadmap":
#         roadmap_page()    



