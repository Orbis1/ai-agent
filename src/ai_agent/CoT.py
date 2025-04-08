from langchain_core.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from ai_agent.llm import model as llm
import json


BASELINE_PROMPT = """
    Ответь на следующий вопрос. Избегай лишних деталей в своём ответе.

    Question: {query}

    Answer:
"""

baseline_response_prompt_template = PromptTemplate.from_template(BASELINE_PROMPT)
baseline_response_chain = baseline_response_prompt_template | llm | StrOutputParser()

VERIFICATION_QUESTION_PROMPT = """
    Твоя задача: составить от 2 до 4 вопросов, ответы на которые позволяют убедиться
    в корректности исходного ответа (Baseline Response) на вопрос (Actual Question).
    Начинай каждый вопрос с новой строки.

    ВАЖНО: не задавай вопросы, ответы на которые не помогут 
    проверить или скорректировать Baseline Response

    Actual Question: {query}
    Baseline Response: {base_response}

    Final Verification Questions:
"""

verification_question_generation_prompt_template = PromptTemplate.from_template(
    VERIFICATION_QUESTION_PROMPT
)
verification_question_generation_chain = (
    verification_question_generation_prompt_template | llm | StrOutputParser()
)

BASE_VERIFICATION_PROMPT = """
    {input}
"""

base_verification_prompt_template = PromptTemplate.from_template(
    BASE_VERIFICATION_PROMPT
)
base_verification_chain = base_verification_prompt_template | llm | StrOutputParser()

verification_chain = (
    RunnablePassthrough.assign(
        split_questions=lambda x: x["verification_questions"].split("\\n"),
    )
    | RunnablePassthrough.assign(
        answers=(
            lambda x: [{"input": q, "chat_history": []} for q in x["split_questions"]]
        )
        | base_verification_chain.map()
    )
    | (
        lambda x: "\\n".join(
            [
                "Questions: {} \nAnswer: {} \n".format(question, answer)
                for question, answer in zip(x["split_questions"], x["answers"])
            ]
        )
    )
)

FINAL_ANSWER_PROMPT = """Тебе будут даны `Original Query` и `Baseline Answer`,
проанализируй `Verification Questions & Answers`, чтобы скорректировать `Baseline Answer` и
дать максимально корректный ответ Final Refined Answer.
ВАЖНО: не включай в ответ лишнюю информацию, не отвечающую на вопрос Original Query!

Original Query: {query}
Baseline Answer: {base_response}

Verification Questions & Answer Pairs:
{verification_answers}

Final Refined Answer: """

final_answer_prompt_template = PromptTemplate.from_template(FINAL_ANSWER_PROMPT)
final_answer_chain = final_answer_prompt_template | llm | StrOutputParser()

chain = (
    RunnablePassthrough.assign(base_response=baseline_response_chain)
    | RunnablePassthrough.assign(
        verification_questions=verification_question_generation_chain
    )
    | RunnablePassthrough.assign(verification_answers=verification_chain)
    | RunnablePassthrough.assign(final_answer=final_answer_chain)
)
response = chain.invoke({"query": "Утонет ли яблоко в воде?"})


# print(json.dumps(response, indent=4, ensure_ascii=False))

with open("CoT_verification_answers.md", "w", encoding="utf-8") as file:
    file.write(response["verification_answers"])
    file.write("\n\n")
    file.write("# Финальный ответ\n\n")
    file.write(response["final_answer"])
