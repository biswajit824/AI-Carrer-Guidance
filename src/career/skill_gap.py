def analyze_skill_gap(student_skills, target_role):

    student_skills = {
        skill.lower().strip()
        for skill in student_skills
    }

    required_skills = {
        skill.lower().strip()
        for skill in target_role["skills"]
    }

    missing = required_skills - student_skills

    existing = required_skills.intersection(
        student_skills
    )

    return {
        "existing_skills": sorted(existing),
        "missing_skills": sorted(missing),
        "gap_count": len(missing)
    }