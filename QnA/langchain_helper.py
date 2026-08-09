import os

from dotenv import load_dotenv

# LangChain imports
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import CSVLoader
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Sarvam AI
from langchain_sarvam import ChatSarvam


load_dotenv()


# -----------------------------
# Initialize Sarvam AI LLM
# -----------------------------

llm = ChatSarvam(
    model="sarvam-105b",
    temperature=0.1,
    api_key=os.environ["SARVAM_API_KEY"]
)


# -----------------------------
# Initialize Embeddings
# -----------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# FAISS storage path

vectordb_file_path = "faiss_index"



# -----------------------------
# Create Vector Database
# -----------------------------

def create_vector_db():

    loader = CSVLoader(
        file_path="codebasics_faqs.csv",
        source_column="prompt",
        encoding="latin-1"
    )

    documents = loader.load()


    vectordb = FAISS.from_documents(
        documents=documents,
        embedding=embeddings
    )


    vectordb.save_local(
        vectordb_file_path
    )

    print("Vector database created successfully!")



# -----------------------------
# Create RAG Chain
# -----------------------------

def get_qa_chain():


    vectordb = FAISS.load_local(
        vectordb_file_path,
        embeddings,
        allow_dangerous_deserialization=True
    )


    retriever = vectordb.as_retriever(
        search_kwargs={
            "k":3
        }
    )


    prompt_template = """

You are a helpful assistant.

Answer the question only using the given context.

If the answer is not present in the context,
say:
"I don't know."

Context:

{context}


Question:

{question}


Answer:

"""


    prompt = PromptTemplate.from_template(
        prompt_template
    )



    # RAG Chain

    chain = (

        {
            "context": retriever,
            "question": RunnablePassthrough()
        }

        | prompt

        | llm

        | StrOutputParser()

    )


    return chain



# -----------------------------
# Main Execution
# -----------------------------

if __name__ == "__main__":


    # Run this only once
    create_vector_db()


    chain = get_qa_chain()


    response = chain.invoke(
        "Do you have javascript course?"
    )


    print("\nAnswer:")
    print(response)