def build_prompt(context, user_input):
    formatted_context = "\n\n".join(
        f"Фрагмент {i}:\n{chunk}" for i, chunk in enumerate(context, start=1)
    )

    return f"""
        Ты — помощник по работе с документами.
        Отвечай на вопросы только на основании предоставленного контекста.
        Если ответа в контексте нет, сообщи об этом.
        Не придумывай факты.

        Контекст:
        {formatted_context}

        Вопрос:
        {user_input}

        Ответ:
        """
