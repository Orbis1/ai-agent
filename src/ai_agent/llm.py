from langchain_gigachat.chat_models import GigaChat

from ai_agent import GIGACHAT_API_CREDENTIALS, GIGACHAT_API_SCOPE, GIGACHAT_MODEL_NAME

model = GigaChat(
    credentials=GIGACHAT_API_CREDENTIALS,
    scope=GIGACHAT_API_SCOPE,
    model=GIGACHAT_MODEL_NAME,
    verify_ssl_certs=False,
    profanity_check=False,
    timeout=600,
    top_p=0.3,
    temperature=0.1,
    max_tokens=6000,
)
