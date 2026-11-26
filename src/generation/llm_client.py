import ollama
import re


def generate_answer(prompt: str, max_tokens: int = 520) -> str:
    response = ollama.chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "system",
                "content": (
                    "Ты — помощник по работе с документами. "
                    "Отвечай сразу готовым ответом. "
                    "Не показывай ход рассуждений, анализ контекста "
                    "и промежуточные мысли. "
                    "Не используй вводные фразы. "
                    "Пиши кратко, связно и по существу. "
                    "Используй только предоставленный контекст."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        think=False,
        options={"num_predict": max_tokens, "temperature": 0.2},
    )

    content = response["message"]["content"].strip()
    paragraphs = re.split(r"\r?\n\s*\r?\n", content, maxsplit=1)
    resp = paragraphs[1].strip() if len(paragraphs) > 1 else ""

    return resp
