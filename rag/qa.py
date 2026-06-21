# rag/qa.py

from urllib.parse import urlparse

from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_core.prompts import PromptTemplate

from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain



def get_qa_chain(website_url: str, base_dir="vector_db"):

    domain = urlparse(website_url).netloc.replace(".", "_")

    persist_dir = f"{base_dir}/{domain}"


    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


    vectordb = Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings
    )


    retriever = vectordb.as_retriever(
        search_kwargs={
            "k":25
        }
    )


    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.2
    )


    prompt = PromptTemplate(
        input_variables=[
            "context",
            "input"
        ],

        template="""
Answer using ONLY the provided website content.

Rules:
- Give a brief but complete answer.
- Do not add outside information.
- If not found, say clearly.

Context:
{context}

Question:
{input}

Answer:
"""
    )


    document_chain = create_stuff_documents_chain(
        llm,
        prompt
    )


    retrieval_chain = create_retrieval_chain(
        retriever,
        document_chain
    )


    return retrieval_chain