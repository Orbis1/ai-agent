# ai-agent

# Terminal commands track

```
poetry // After asking about installation of poetry say yes

poetry add langchain-community
poetry add langchain-gigachat
poetry add langchain-chroma // ERROR: Problem encountered: Cannot compile `Python.h`

poetry add langgraph
poetry add langgraph-checkpoint
poetry add langgraph-cli
poetry add langgraph-sdk

poetry add rapidfuzz

poetry add python-dotenv --group dev
poetry add black --group dev // for .py formatting

```

# Milestones

- [x] basic poetry setup completed
- [x] used with .env
- [x] the bot from the course "IT-arch" has been launched successfully

# Libs

langchain-gigachat # Работа с API GigaChat для обработки запросов через LangChain
langchain-community # Дополнительные утилиты и инструменты от сообщества LangChain
langgraph # Построение цепочек взаимодействий между агентами и данными
langgraph-checkpoint # Сохранение и восстановление состояния диалога
langgraph-cli # CLI для управления агентами и цепочками через командную строку
langgraph-sdk # Инструменты для разработки кастомных агентов и цепочек
langchain_chroma # Интеграция LangChain с векторными базами данных Chroma
rapidfuzz # Быстрый поиск похожих строк для обработки запросов
