# Импорты
from ai_agent.agent import agent


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


if __name__ == "__main__":
    main()
