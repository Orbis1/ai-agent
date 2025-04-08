from langchain.prompts import load_prompt
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from ai_agent.ask import model as giga
from langchain.prompts import ChatPromptTemplate


# Укажите полный путь до файла (зависит от окружения)
loader = TextLoader("./data/book.txt")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=7000,
    chunk_overlap=0,
    length_function=len,
    is_separator_regex=False,
)
documents = text_splitter.split_documents(documents)
print(f"Количество частей книги: {len(documents)}")

# Создаем шаблон для взаимодействия с моделью
map_prompt_template = """
Ты — опытный суммаризатор. Твоя задача — кратко изложить содержание следующего текста, сохраняя основные идеи и важные детали. 
Пожалуйста, напиши краткое резюме в виде нескольких предложений.

Текст: "{text}"

Резюме:
"""

combine_prompt_template = """
Ты получил несколько кратких суммаризаций различных частей текста. Твоя задача — объединить их в одну итоговую суммаризацию, сохраняя ключевые идеи и важные детали из всех частей. Пожалуйста, сделай суммаризацию как можно более краткой и информативной.

Частичные суммаризации:
{text}

Итоговая суммаризация:
"""

book_map_prompt = ChatPromptTemplate.from_template(map_prompt_template)
book_combine_prompt = ChatPromptTemplate.from_template(combine_prompt_template)

chain = load_summarize_chain(
    giga,
    chain_type="map_reduce",
    map_prompt=book_map_prompt,
    combine_prompt=book_combine_prompt,
    verbose=True,
)

res = chain.invoke({"input_documents": documents})
print(res["output_text"].replace(". ", ".\n"))
