def create_roadmap(skill_gaps):

    skills = skill_gaps["missing_skills"]

    roadmap = {
        "days_0_30": [],
        "days_31_60": [],
        "days_61_90": []
    }

    for index, skill in enumerate(skills):

        if index < 2:
            roadmap["days_0_30"].append(
                f"Learn the fundamentals of {skill}"
            )

        elif index < 4:
            roadmap["days_31_60"].append(
                f"Practice {skill} through exercises and projects"
            )

        else:
            roadmap["days_61_90"].append(
                f"Build a project demonstrating {skill}"
            )

    return roadmap