from langchain.chat_models import init_chat_model

from ptc1.config.settings import settings


def get_llm():
    return init_chat_model(
        model=f"google_genai:{settings.model_name}",
        temperature=0.2,
        api_key=settings.google_api_key,
    )


llm = get_llm()