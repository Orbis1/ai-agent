# Импорты
from ai_agent.agent import agent
from langchain.schema import HumanMessage, SystemMessage
import ai_agent.ask
from langchain.prompts import load_prompt
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import sys


# Основной цикл общения с агентом
def chat(thread_id: str = "SberAX_consultant"):
    """
    Основная функция для общения с агентом.
    """
    config = {"configurable": {"thread_id": thread_id}}
    print("Добро пожаловать в терминал общения с GigaChat!")
    print("Напишите Ваш запрос или введите 'exit' для выхода.")

    while True:
        try:
            user_input = input("\n>>: ")
            if user_input.lower() == "exit":
                print("До свидания!")
                break

            response = agent.invoke(
                {
                    "messages": [
                        (
                            "user",
                            user_input.encode("utf-8", errors="replace").decode(
                                "utf-8"
                            ),
                        )
                    ]
                },
                config=config,
            )
            print("🤖 :", response["messages"][-1].content)

        except KeyboardInterrupt:
            print("\nВыход из программы. До свидания!")
            break
        except Exception as e:
            print("Произошла ошибка:", str(e))


def main():
    print("Hello from project ai_agent!")


def ask(text: str):
    # Простой вопрос
    # messages = [HumanMessage(content=text)]

    # Использование коллекции промптов
    # prompt = load_prompt("lc://prompts/content/spell_correction.yaml")
    prompt = ChatPromptTemplate.from_template(
        "Придумай шутку про то, как встретились {персона} и {животное}"
    )
    output_parser = StrOutputParser()
    chain = prompt | ai_agent.ask.model | output_parser
    # messages = [HumanMessage(content=prompt.format(text=text))]

    # response = ai_agent.ask.model.invoke(messages).content
    response = chain.invoke({"персона": "Юрий Гагарин", "животное": "крокодил"})
    print(response)


def ask_with_args():
    question = sys.argv[1] if len(sys.argv) > 1 else "Привет"
    ask(question)


if __name__ == "__main__":
    main()
