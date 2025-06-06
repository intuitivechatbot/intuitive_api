from qdrant_client import QdrantClient
from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings
import os

def get_retriever():
    client = QdrantClient(
        url = os.getenv("QDRANT_URL"),
        api_key = os.getenv("QDRANT_API_KEY"),  
    )

    embedder = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

    vectorstore = Qdrant(
        client=client,
        collection_name="blogs",
        embeddings=embedder
    )

    return vectorstore.as_retriever(search_kwargs={"k": 3})
