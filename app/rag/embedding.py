
from langchain_huggingface import HuggingFaceEmbeddings
from app.config.settings import settings


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        encode_kwargs={"normalize_embeddings": True},
    )