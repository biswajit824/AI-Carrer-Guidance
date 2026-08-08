FORBIDDEN_GUARANTEE_PATTERNS = [
    "guaranteed job",
    "100% placement",
    "guaranteed salary",
    "guaranteed internship",
    "job guaranteed"
]


def check_response(response):

    text = response.lower()

    for phrase in FORBIDDEN_GUARANTEE_PATTERNS:

        if phrase in text:

            return {
                "safe": False,
                "reason": "Response contains an unsupported guarantee."
            }

    return {
        "safe": True,
        "reason": None
    }




RESPONSIBLE_AI_NOTICE = """
This assistant provides indicative career guidance
based on the information provided.

It does not guarantee:
• jobs
• internships
• salaries
• admissions
• placement outcomes
• official eligibility
"""