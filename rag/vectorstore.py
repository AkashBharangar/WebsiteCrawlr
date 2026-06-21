import os
import shutil
from urllib.parse import urlparse

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings



def create_vectorstore(chunks, website_url: str, base_dir="vector_db"):

    domain = urlparse(website_url).netloc.replace(".", "_")

    persist_dir = os.path.join(
        base_dir,
        domain
    )


    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)


    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


    Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        persist_directory=persist_dir
    )


    return persist_dir