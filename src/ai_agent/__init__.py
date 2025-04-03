import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Теперь можно использовать переменные окружения
SECRET_KEY = os.getenv("SECRET_KEY")