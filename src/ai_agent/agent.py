import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from langchain_gigachat.chat_models import GigaChat
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from ai_agent import GIGACHAT_API_CREDENTIALS, GIGACHAT_API_SCOPE, GIGACHAT_MODEL_NAME
from ai_agent.prompts import system_prompt  # Импортируем наш системный промпт
from ai_agent.tools import get_all_course_names, get_most_similar_course


# Инициализация модели GigaChat

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

tools = [get_all_course_names, get_most_similar_course]

agent = create_react_agent(
    model=model,
    tools=tools,
    state_modifier=system_prompt,  # Подключаем системный контекст
    checkpointer=MemorySaver(),  # Добавляем объект из библиотеки LangGraph для сохранения памяти агента
)
