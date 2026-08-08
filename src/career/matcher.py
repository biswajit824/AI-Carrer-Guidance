def calculate_role_match(student_skills, role_skills):

    student_skills = {
        skill.lower().strip()
        for skill in student_skills
    }

    role_skills = {
        skill.lower().strip()
        for skill in role_skills
    }

    matched = student_skills.intersection(role_skills)

    score = (
        len(matched) / len(role_skills)
        if role_skills
        else 0
    )

    missing = role_skills - student_skills

    return {
        "score": round(score * 100, 2),
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing)
    }


def rank_roles(student_skills, roles):

    results = []

    for role in roles:

        analysis = calculate_role_match(
            student_skills,
            role["skills"]
        )

        results.append(
            {
                "role": role["role"],
                "description": role["description"],
                "score": analysis["score"],
                "matched_skills": analysis["matched_skills"],
                "missing_skills": analysis["missing_skills"],
                "projects": role["beginner_projects"]
            }
        )

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results