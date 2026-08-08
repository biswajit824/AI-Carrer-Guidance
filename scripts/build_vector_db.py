from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag.vector_store import get_vector_store


DATA_PATH = Path("data/raw/career_faqs.txt")


def load_documents():

    text = DATA_PATH.read_text(encoding="utf-8")

    document = Document(
        page_content=text,
        metadata={
            "source": "career_faqs.txt",
            "category": "career_guidance"
        }
    )

    return [document]


def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    return chunks


def build_vector_database():

    print("Loading documents...")

    documents = load_documents()

    print(f"Loaded {len(documents)} documents")

    print("Splitting documents...")

    chunks = split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    print("Creating vector database...")

    vector_store = get_vector_store()

    vector_store.add_documents(chunks)

    print("Vector database created successfully!")


if __name__ == "__main__":
    build_vector_database()