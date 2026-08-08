from langchain_core.documents import Document


def create_documents(resources):

    documents = []

    for resource in resources:

        content = f"""
Title: {resource['title']}

Category: {resource['category']}

Level: {resource['level']}

Skills:
{', '.join(resource['skills'])}

Description:
{resource['description']}
"""

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "title": resource["title"],
                    "category": resource["category"],
                    "level": resource["level"]
                }
            )
        )

    return documents