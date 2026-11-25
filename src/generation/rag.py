from src.search.hybrid_search import hybrid_search
from src.generation.prompt import build_prompt
from src.generation.llm_client import generate_answer


def rag_answer(user_input, model, client):

    search = hybrid_search(user_input, model, client)

    if not search:
        return "В документах недостаточно информации для ответа на вопрос."

    context = [i["content"] for i in search]

    prompt = build_prompt(context, user_input)
    answer = generate_answer(prompt)

    return answer
