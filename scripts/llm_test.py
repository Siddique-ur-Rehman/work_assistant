from langchain_openai import ChatOpenAI  
from app.config.settings import settings


for model_name in [settings.primary_model, settings.fallback_model]:
    llm = ChatOpenAI(
        model=model_name,
        openai_api_key=settings.llm_api_key,  
        openai_api_base=settings.base_url,    
        temperature=0.7
    )
    
    try:
        answer = llm.invoke("Say hello in one short sentence.")
        print(f"[{model_name}] says: {answer.content}")
    except Exception as e:
        print(f"[{model_name}] failed: {e}")
