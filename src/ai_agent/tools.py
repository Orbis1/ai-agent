import os
from rapidfuzz import fuzz, process
from datetime import datetime
from langchain.tools import tool
from ai_agent.utils import courses_database, settings

@tool
def get_all_course_names() -> str:
  """
  Возвращай к примеру названия 3-5 курсов {courses_database}.
  Если пользователь пишет про свою роль (role), то предлагай ему курсы по мере сложности (difficulty) или развернуто опиши один самый подходящий под запрос курс.
  """
  return ", ".join([course["name"] for course in courses_database])



@tool
def get_most_similar_course(name: str) -> dict:
  """
  Возвращай информацию о курсе по названию из базы данных.

  Args:
    name (str): Точное название курса.

  Returns:
    Dict: Словарь с информацией о курсе (роль, навыки, сложность, описание, ссылка).
  """

  name = name.strip().lower()
  if not courses_database:
    return {"error": "База данных курсов пуста."}

  course_names = [course["name"].lower() for course in courses_database]
  match = process.extractOne(name, course_names, scorer=fuzz.partial_ratio)

  if match and match[1] >= settings["default_similarity_threshold"] * 100:  # Используем порог из settings.json
    matching_course_index = course_names.index(match[0])
    return courses_database[matching_course_index]
  else:
    return {"error": "Курс с похожим названием не найден."}
