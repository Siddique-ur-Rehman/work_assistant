# One place that creates the chat model (via OmniRoute).
from langchain_openai import ChatOpenAI
from app.config.settings import settings


def get_llm(model_name=None):
    return ChatOpenAI(
        model=model_name or settings.primary_model,
        openai_api_key=settings.llm_api_key,
        openai_api_base=settings.base_url,
        temperature=0.2,  # low = more factual answers
    )