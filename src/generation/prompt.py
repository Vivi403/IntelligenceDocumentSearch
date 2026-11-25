def build_prompt(context, user_input):
    formatted_context = "\n\n".join(context)

    return f"""
        Контекст:
        {formatted_context}

        Вопрос:
        {user_input}

        Дай краткий и точный ответ на вопрос.
        """
