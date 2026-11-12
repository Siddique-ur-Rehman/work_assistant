# One place that creates the chat model (via OmniRoute).
from langchain_openai import ChatOpenAI
from app.config.settings import settings


def _make(model_name=None):
    return ChatOpenAI(
        model=model_name or settings.primary_model,
        openai_api_key=settings.llm_api_key,
        openai_api_base=settings.base_url,
        temperature=0.2,
        timeout=30,
        max_retries=1
    )
def get_llm():
    """Primary model first. If it raises an error, the backup model is used."""
    primary = _make(settings.primary_model)
    backup = _make(settings.fallback_model)
    return primary.with_fallbacks([backup])


def ask_llm(prompt, default):
    """Call the LLM. If BOTH models fail, return `default` instead of crashing."""
    try:
        return get_llm().invoke(prompt).content.strip()
    except Exception as error:
        print(f"[llm failed] {type(error).__name__}: {error}")
        return default