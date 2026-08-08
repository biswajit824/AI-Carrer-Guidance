from src.llm.chains import create_career_chain


def main():

    chain = create_career_chain()

    response = chain.invoke(
        {
            "profile": """
            Branch: Computer Science
            Year: Final Year
            Skills: Python, SQL, Machine Learning
            Projects: 2 ML projects
            Preferred Role: AI/ML Engineer
            """,

            "context": """
            AI/ML roles commonly require Python,
            machine learning fundamentals,
            data preprocessing, model evaluation,
            Git and basic deployment knowledge.
            """,

            "question": """
            What should I learn next to become
            an AI/ML engineer?
            """
        }
    )

    print(response.content)


if __name__ == "__main__":
    main()