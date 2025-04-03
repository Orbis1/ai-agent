import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Теперь можно использовать переменные окружения
SECRET_KEY = os.getenv("SECRET_KEY")
GIGACHAT_API_CREDENTIALS = os.getenv("GIGACHAT_API_CREDENTIALS")
GIGACHAT_API_SCOPE = os.getenv("GIGACHAT_API_SCOPE")
GIGACHAT_MODEL_NAME = os.getenv("GIGACHAT_MODEL_NAME")
SETTINGS_PATH = os.getenv("SETTINGS_PATH")
