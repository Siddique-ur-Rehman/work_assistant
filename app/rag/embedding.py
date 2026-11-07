
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.config.settings import settings


def get_embeddings():
    return GoogleGenerativeAIEmbeddings(
        model=settings.embedding_model,
        google_api_key=settings.llm_api_key,
    )