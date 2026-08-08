import json
from datetime import datetime


def save_feedback(
    question,
    response,
    rating,
    comment=""
):

    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "question": question,
        "response": response,
        "rating": rating,
        "comment": comment
    }

    with open(
        "feedback.json",
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            json.dumps(record)
            + "\n"
        )