def normalize_skill(skill):
    return skill.strip().lower()


def parse_student_skills(skills_text):
    skills = skills_text.split(",")

    return {
        normalize_skill(skill)
        for skill in skills
        if skill.strip()
    }


def calculate_skill_gap(
    student_skills,
    required_skills
):

    student = {
        normalize_skill(skill)
        for skill in student_skills
    }

    required = {
        normalize_skill(skill)
        for skill in required_skills
    }

    matched = student.intersection(required)

    missing = required.difference(student)

    return {
        "matched": sorted(matched),
        "missing": sorted(missing)
    }